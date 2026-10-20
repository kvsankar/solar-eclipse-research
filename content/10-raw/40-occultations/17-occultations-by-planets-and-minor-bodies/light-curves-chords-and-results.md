---
title: Light curves, chords and results
seo_title: Occultation Light Curves: Diffraction and Chord Fitting
description: How occultation light curves are modelled for diffraction, star size and exposure, how chords are fitted, and what the method has found.
order: 2
status: working
updated: 2026-10-17
tags: [stellar-occultation, light-curve, fresnel, chord, ellipse-fit, rings, tno, sora]
---

::: summary
- **A light curve gives two times per observer.** Disappearance and reappearance, with the site position, fix the ends of one chord on the [fundamental plane](../../10-shared/01-foundations/besselian-elements.md). The magnitude drop decides whether the event is detectable at all [@mb-gomes-junior-2022-sora] [@mb-herald-2020].
- **The edge is not a step.** The model is Fresnel diffraction at a straight edge, averaged over the passband, the star's projected disc and the exposure. The Fresnel scale $\sqrt{\lambda D/2}$ is about 0.3 km in the main belt and 1.2 km at 40 au [@mb-gomes-junior-2022-sora] [@mb-sora-code].
- **Sub-exposure timing is routine.** The fractional flux of the one transitional point locates the event inside the exposure, giving $\sigma_t = \sigma_{LC}\,t_{\mathrm{exp}}/\Delta f$, unless the event fell in readout dead time [@mb-gomes-junior-2022-sora].
- **Chords are fitted with a circle, an ellipse or a shape model.** An ellipse has five parameters and needs at least three well-spread chords. Single chords give a size lower limit and an astrometric position with a two-sided ambiguity that a nearby miss resolves [@mb-gomes-junior-2022-sora] [@mb-herald-2020].
- **Occultation sizes match spacecraft.** The 1984 Ceres occultation, fitted to the Dawn shape model, gives a volume-equivalent diameter of 937 ± 3 km against Dawn's 939 km [@mb-herald-2020].
- **Rings and atmospheres were found this way.** Occultations revealed Uranus's rings in 1977 and [Pluto](https://en.wikipedia.org/wiki/Pluto)'s atmosphere in 1985 and 1988. They found Chariklo's two rings in 2013, Haumea's ring in 2017 and Quaoar's two rings outside its Roche limit in 2018 to 2022 [@mb-elliot-1977] [@mb-meza-2019] [@mb-braga-ribas-2014] [@mb-ortiz-2017] [@mb-pereira-2023].
:::

**The question.** How is an occultation light curve turned into accurate disappearance and reappearance times, how are many observers' times combined into a size, shape and position, and what physical results has this produced for asteroids, trans-Neptunian objects and their environments? The prediction side is in [Prediction geometry and astrometry](prediction-geometry-and-astrometry.md).

## What the light curve measures

When the star and body are closer than the point-spread function they cannot be separated, so the photometry measures their sum. The authors of SORA (Stellar Occultation Reduction and Analysis) call the unocculted level the baseflux and the occulted level the bottomflux, "only the light reflected by the body" [@mb-gomes-junior-2022-sora]. The [?mb-magnitude-drop|magnitude drop] is [@mb-gomes-junior-2022-sora]:

$$
\Delta M = M_\circ - M_\star + 2.5\log_{10}\!\left(1 + 10^{0.4(M_\star - M_\circ)}\right),
$$

with $M_\star$ the star's magnitude and $M_\circ$ the body's in the same band. The code's `calc_magnitude_drop` computes the same quantity through the combined magnitude and also returns the normalised bottomflux $10^{0.4(M_c - M_\circ)}$ [@mb-sora-code]. The body's magnitude varies with rotation, so each observer's bottomflux is fitted separately [@mb-gomes-junior-2022-sora].

The [?mb-immersion|immersion and emersion] times are the product. SORA's paper states that "the chord's accuracy depends primarily on the accuracy of the times obtained from the light curve" [@mb-gomes-junior-2022-sora]. Herald lists the departures from a simple step. A double star gives steps or multiple events, and satellites, rings or limb topography give multiple events. There are also "gradual events caused by the star having an appreciable apparent diameter, or the effects of Fresnel diffraction" [@mb-herald-2020].

## The light-curve model

### Fresnel diffraction at the limb

The broadening of the shadow edge by diffraction is set by the [?mb-fresnel-scale|Fresnel scale] [@mb-gomes-junior-2022-sora]:

$$
F = \sqrt{\frac{\lambda D_\circ}{2}},
$$

with $\lambda$ the wavelength and $D_\circ$ the observer-body distance. SORA's paper writes it $f$. It gives $F \approx 1.2$ km for a Plutino at 39.5 au in light of 550 nm. Its simulation of a 50 km body at 20 au at 700 nm has $F = 1.02$ km [@mb-gomes-junior-2022-sora]. The same formula gives about 0.29 km for a main-belt asteroid at 2 au and 550 nm. Because $F$ is much smaller than the bodies that are actually observed, SORA treats each edge as straight and uses the one-dimensional "bar" model of Roques et al. 1987 [@mb-gomes-junior-2022-sora].

SORA's `bar_fresnel` implements the bar as two straight edges at plane positions $X_{01}$ and $X_{02}$ [@mb-sora-code]. With $x = X/F$, $x_1 = x - X_{01}/F$, $x_2 = x - X_{02}/F$, and $S_F$ and $C_F$ the Fresnel sine and cosine integrals of `scipy.special.fresnel`:

$$
\Delta C_F = C_F(x_1) - C_F(x_2), \quad \Delta S_F = S_F(x_1) - S_F(x_2),
$$

$$
I(x) = \left(1 - \frac{o}{2}(\Delta C_F + \Delta S_F)\right)^2 + \left(\frac{o}{2}(\Delta C_F - \Delta S_F)\right)^2,
$$

where $o$ is the opacity, 1 for an opaque body [@mb-sora-code]. The plane coordinate is time times the shadow speed, $X = t\,V_S$, so a fit in time is a fit in kilometres [@mb-sora-code]. For a grazing chord the paper replaces $V_S$ by the velocity normal to the local limb, $\mathbf{v}\cdot\hat{\mathbf{n}}$ [@mb-gomes-junior-2022-sora].

### Passband, star size and exposure

Three averages follow, in this order in both paper and code [@mb-gomes-junior-2022-sora] [@mb-sora-code]:

1. **Passband.** The paper says the model "should be integrated over the observed bandwidth". The code computes the bar model at two wavelengths, $\lambda_0 - \Delta\lambda/2$ and $\lambda_0 + \Delta\lambda/2$, and averages the two curves [@mb-sora-code]. This is a two-point approximation of that integral, not a passband integration.
2. **Star disc.** The star's radius projected to the body's distance is $r_\star = D_\circ R_\star / D_\star$, with $R_\star$ the stellar radius and $D_\star$ its distance [@mb-gomes-junior-2022-sora]. [Gaia](https://en.wikipedia.org/wiki/Gaia_(spacecraft)) EDR3 does not give radii, so SORA takes them from Gaia DR2 or from the empirical colour relations of van Belle 1999 and Kervella et al. 2004 using NOMAD B, V and K photometry [@mb-gomes-junior-2022-sora]. The code averages the diffraction curve over 24 offsets across the projected diameter, weighted by $\sqrt{(d_\star/2)^2 - p^2}$. That is a uniform disc collapsed to one dimension, with no limb darkening [@mb-sora-code].
3. **Exposure.** Each observed point is the mean of the model over $t \pm t_{\mathrm{exp}}/2$. The model is sampled at $\min(F/V_S,\ t_{\mathrm{exp}})/10$ [@mb-sora-code]. Readout dead time between exposures carries no information, and an event falling inside it adds the dead time to the timing uncertainty [@mb-gomes-junior-2022-sora].

The spatial resolution of one exposure is $r_t = V_S\,t_{\mathrm{exp}}$ [@mb-gomes-junior-2022-sora]. If it exceeds both $F$ and $r_\star$, the exposure dominates the edge shape. Published examples of a resolved star include a [Hipparcos](https://en.wikipedia.org/wiki/Hipparcos) star of 0.54 milliarcseconds behind Titania, 7.5 km at the satellite's distance, and a star of about 20 km projected diameter behind the Plutino Ixion [@mb-gomes-junior-2022-sora].

### Fitting the times

SORA normalises the observed curve to baseflux 1 and bottomflux 0, then minimises [@mb-gomes-junior-2022-sora]:

$$
\chi^2 = \sum_{i=1}^{N} \frac{(\phi_{i,\mathrm{obs}} - \phi_{i,\mathrm{cal}})^2}{\sigma_i^2},
$$

over immersion and emersion times drawn uniformly at random within user limits. It takes the global minimum and reads confidence limits from constant-$\chi^2$ boundaries [@mb-gomes-junior-2022-sora]. A box-fitting least-squares search after Kovács et al. 2002 supplies starting values [@mb-gomes-junior-2022-sora].

For a single transitional point the fractional flux locates the event inside the exposure, and the timing uncertainty is roughly [@mb-gomes-junior-2022-sora]:

$$
\sigma_t = \frac{\sigma_{LC}}{\Delta f}\,t_{\mathrm{exp}},
$$

with $\sigma_{LC}$ the flux noise and $\Delta f$ the drop between baseflux and bottomflux. The estimate does not depend on where in the exposure the event fell [@mb-gomes-junior-2022-sora].

The light curve itself comes from other programs. SORA's paper names PRAIA, Tangra and PyMovie [@mb-gomes-junior-2022-sora]. Herald's quality-assurance chain names Limovie, PyMovie and Tangra for photometry, and AOTA in [Occult](../../10-shared/09-software-and-repos/commercial-and-institutional-tools.md), Occular, ROTE and PyOTE for the timing analysis [@mb-herald-2020].

## From times to chords

Each time and site gives one point on the fundamental plane, through the plane equations of [Prediction geometry and astrometry](prediction-geometry-and-astrometry.md#the-geometry-a-cylinder-on-the-fundamental-plane). The [?mb-chord|chord] joins an observer's two points. Herald's reduction moves every point to a common reference time with the cubic shadow motion [@mb-herald-2020]. The reference time is the mean of all event times used. With a double star it is the mean for the primary. With an asteroid satellite it is the mean for the satellite's events, so that the satellite's orbital motion drops out [@mb-herald-2020]. SORA uses the instant of each event directly with geocentric star coordinates. It warns about the 0.021 s geocentre-to-observer [light-time](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) [@mb-gomes-junior-2022-sora].

Observers at the same site or on the same track give "only one effective chord" [@mb-gomes-junior-2022-sora]. A [?mb-negative-chord|negative chord] near the limb constrains size and shape. It also decides between the two possible centres of a single chord, north or south of it [@mb-gomes-junior-2022-sora].

## Fitting a figure to the chords

### Ellipse and circle

Both programs fit an ellipse with five free parameters: two centre coordinates, the apparent semi-major axis $a'$, the [?mb-apparent-oblateness|apparent oblateness] $\epsilon = 1 - b'/a'$ and the position angle of the minor axis [@mb-gomes-junior-2022-sora] [@mb-herald-2020]. SORA's statistic is [@mb-gomes-junior-2022-sora]:

$$
\chi^2 = \sum_{i=1}^{N} \frac{(r_{i,\mathrm{obs}} - r_{i,\mathrm{cal}})^2}{\sigma_i^2 + \sigma_{\mathrm{model}}^2},
$$

with $r_{i,\mathrm{obs}} - r_{i,\mathrm{cal}}$ the radial distance of chord end $i$ from the trial limb, measured from the ellipse centre, $\sigma_i$ its uncertainty and $\sigma_{\mathrm{model}}$ an allowance for topography. The paper states that "the default number of ellipses tested is 10 million" [@mb-gomes-junior-2022-sora]. The released code does less by default. Its `fit_ellipse` defaults to `method='least_squares'`, a convergent least-squares fit. It then samples one batch of `loop` = 10 000 trial ellipses uniformly within the user-given ranges around the best fit, and stops when `number_chi` = 10 000 values are kept [@mb-sora-code]. The 10 million of the paper is reached only by raising these arguments or by repeated calls. The Monte Carlo search alone survives as `method='chisqr'`, documented as the method of SORA 0.2.1 and earlier [@mb-sora-code]. Herald also measures residuals "along the radius of the ellipse" [@mb-herald-2020]. Herald adds a rule for misses: a miss chord enters only when it cuts the current ellipse, and then as an event point pulled 0.5 km towards the centre [@mb-herald-2020].

The circle is the fallback when the chords cannot support five parameters. Herald fits a circle of assumed diameter when chords are few or all on one side. The assumed diameter is a weighted mean of IRAS, AKARI, NEOWISE and MSX values, or else comes from the absolute magnitude [@mb-herald-2020]:

$$
D = 10^{\,3.1295 - 0.5\log_{10}(a) - 0.2H}\ \mathrm{km}, \qquad a = 0.1652,
$$

with $a$ the assumed geometric albedo and $H$ the absolute magnitude. Tanga and Delbo use $D = 1329\,p_V^{-1/2}\,10^{-H/5}$ km [@mb-tanga-delbo-2007]. The two have the same form but different constants: $10^{3.1295} = 1347$ km against 1329 km, a 1.4 per cent difference in the inferred size.

SORA's paper reports a timing problem that the ellipse can absorb. When an observer's clock is suspect, Ortiz et al. fitted a line through the chord centres and shifted the bad chord to it. This assumes the outline is an ellipse, whose chord centres are collinear [@mb-gomes-junior-2022-sora].

### Single chords and their error rules

Herald's data set handles the commonest case explicitly. For a [?mb-single-chord|single-chord event] the asteroid is placed on the chord centre, and the cross-track uncertainty is "80 per cent of the apparent assumed radius" [@mb-herald-2020]. The along-track uncertainty is 5 per cent of the assumed diameter if the chord is longer than 80 per cent of it, 10 per cent between 60 and 80 per cent, and 20 per cent below 60 per cent [@mb-herald-2020]. When chords fit a shape model the astrometric uncertainty is set "somewhat arbitrarily" at 0.02 of the diameter [@mb-herald-2020]. Ferreira et al. found 61 per cent of events single-chord and the error model "slightly conservative on average" [@mb-ferreira-2022].

### Shape models and the centre of mass

A shape model turns one projected outline into a volume. Herald compares occultation and spacecraft sizes for Ceres, Vesta, Lutetia, Mathilde, Eros and [Arrokoth](https://en.wikipedia.org/wiki/486958_Arrokoth) [@mb-herald-2020]. For Ceres, 13 photoelectric chords of 1984 November 13 fitted to the Dawn model give a volume-equivalent diameter of 937 ± 3 km against Dawn's 939 km. A free ellipse fitted to the same chords gives 960 ± 4 by 908 ± 3 km [@mb-herald-2020]. The shape model also locates the [?centre-of-mass|centre of mass]. For Eros on 2019 February 25 it was displaced from the [?centre-of-figure|centre of figure] by about 5 per cent of its length, about 3 milliarcseconds [@mb-herald-2020].

The [?mb-equivalent-radius|area-equivalent radius] $R_{eq} = \sqrt{a'b'}$ gives the geometric albedo when the absolute magnitude is known. SORA's paper prints [@mb-gomes-junior-2022-sora]:

$$
p_V = 10^{H_\odot - H_\circ}\left(\frac{149597870.7}{R_{eq}}\right)^2, \qquad H_\odot = -26.74,
$$

but the code computes $10^{0.4(H_\odot - H_\circ)}\,(\mathrm{au}/R_{eq})^2$ in both `calc_geometric_albedo` and the `Occultation` class [@mb-sora-code]. The code's form is the dimensionally consistent one. The printed equation is missing the factor 0.4.

## Results

### Asteroids

Herald's data set at NASA's Planetary Data System (PDS) held, at its 2020 description, over 15 000 observations by more than 3 300 observers of 4 400 occultations by more than 1 330 asteroids [@mb-herald-2020]. It also lists 76 double stars discovered in occultations, typically tens of milliarcseconds apart, and the diameter, separation and position angle of 30 asteroid satellites or possible satellites [@mb-herald-2020]. About 8 000 occultation light curves are at VizieR catalogue B/occ [@mb-herald-2020]. Euraster published European results from 1996 to 2022 with path maps and chord reductions "done with the help of Dave Herald's software Occult". It handed collection from 2023 to SODIS, the system of the European Section of the International Occultation Timing Association ([IOTA](https://occultations.org/)/ES) [@mb-euraster-2023] [@mb-sodis].

### Trans-Neptunian objects and Centaurs

**Chariklo, 2013 June 3.** A multi-chord occultation revealed two dense rings at orbital radii 391 and 405 km. Their widths are about 7 and 3 km and their optical depths 0.4 and 0.06, around a body of equivalent radius 124 ± 9 km [@mb-braga-ribas-2014]. The Danish 1.54 m telescope at La Silla recorded at almost 10 Hz and resolved the two rings [@mb-braga-ribas-2014]. The ring events were fitted with square-well profiles "after convolution by Fresnel diffraction, observed bandwidth, the stellar radius projected at Chariklo, and the finite integration time". These are the same four terms as the limb model above [@mb-braga-ribas-2014]. The geocentric distance of $2.031\times10^9$ km gave 9 846 km per arcsecond on the sky plane [@mb-braga-ribas-2014]. The [?normal-optical-depth|normal optical depth] requires the ring opening angle, which comes from the ellipse fitted to the ring events [@mb-braga-ribas-2014].

**Haumea, 2017 January 21.** The limb ellipse is 1 704 ± 4 km by 1 138 ± 26 km [@mb-ortiz-2017]. Secondary events fit a ring of radius about 2 287 km, width 70 km and opacity 0.5. Its opening angle is $B = \arcsin(b'_{\mathrm{ring}}/a'_{\mathrm{ring}}) = 13.8^{\circ} \pm 0.5^{\circ}$ [@mb-ortiz-2017]. Combined with rotational light curves, the occultation gave an upper limit on Haumea's density of 1 885 ± 80 kg per cubic metre and a geometric albedo of 0.51 ± 0.02. It found no global nitrogen atmosphere above 15 nbar [@mb-ortiz-2017].

**Quaoar, 2018 to 2022.** The 2022 August 9 event gave nine effective chords. The limb has an apparent semi-major axis of 579.5 ± 4.0 km and oblateness 0.12 ± 0.01. The first ring, Q1R, is at 4 057 ± 6 km, and a second ring at 2 520 ± 20 km has a normal optical depth of 0.004. "Just as Q1R, it also lies outside Quaoar's classical Roche limit" [@mb-pereira-2023].

**Pluto's atmosphere.** The atmosphere "was glimpsed during a ground-based stellar occultation observed on 1985 August 19, and fully confirmed on 1988 June 09" [@mb-meza-2019]. Refraction in an atmosphere makes the disappearance and reappearance smooth instead of sharp. That smoothness is how the atmosphere was detected. SORA's current light-curve model excludes this case [@mb-gomes-junior-2022-sora]. Eleven occultations from 2002 to 2016 show that "pressure has suffered a monotonic increase from 1988 to 2016" [@mb-meza-2019]. The 2015 June 29 event showed a [?mb-central-flash|central flash] that the authors compared with [New Horizons](https://en.wikipedia.org/wiki/New_Horizons) radio profiles [@mb-meza-2019].

**Arrokoth.** Five chords on 2017 July 17 showed "a complicated shape consistent with a contact binary with rough dimensions of 20 by 30 km". The New Horizons flyby confirmed that shape [@mb-buie-2020-arrokoth].

**Astrometry as a product.** For TNOs the position is often the main result, at sub-milliarcsecond intrinsic precision even from one chord [@mb-rommel-2020]. The feedback into predictions is described in [Prediction geometry and astrometry](prediction-geometry-and-astrometry.md#orbit-improvement-gaia-astrometry-and-occultation-astrometry).

### Uranus's rings, 1977

The ring discovery that the minor-body rings echo came from a planet. Elliot, Dunham and Mink report that "at least five rings encircle the planet Uranus" [@mb-elliot-1977]. The evidence was five brief occultations of the star SAO 158687 before and after its occultation by Uranus on 1977 March 10 [@mb-elliot-1977]. They observed from the Kuiper Airborne Observatory's 91 cm telescope with a three-channel photometer recording 10 ms integrations [@mb-elliot-1977]. These facts come from the paper's opening paragraph. The ring timings are not quoted here. The planetary side of that event is in [Planets, satellites and mutual planetary occultations](planets-satellites-and-mutual-planetary-occultations.md).

## Sources compared

| Source | Kind | Light-curve model | Figure fitting | Unique content |
|---|---|---|---|---|
| Gomes-Júnior et al. 2022 [@mb-gomes-junior-2022-sora] | Method paper | Bar diffraction, band, star, exposure | Ellipse, $\sigma_{\mathrm{model}}$, 10 million trial ellipses stated as default | Timing formula, light-time warning, albedo equation printed without 0.4 |
| SORA code [@mb-sora-code] | Implementation | Two-wavelength average, uniform 1D disc, box exposure | Least-squares ellipse, then 10 000 random samples by default against the paper's 10 million | What the model actually computes |
| Herald et al. 2020 [@mb-herald-2020] | Data-set paper | Not modelled, timing tools named | Ellipse, circle, shape model, miss rule | Single-chord error rules, Ceres and Eros checks, data-set counts |
| Braga-Ribas et al. 2014 [@mb-braga-ribas-2014] | Discovery | Square-well ring convolved with four terms | Ring ellipse | Chariklo ring radii, widths, depths |
| Ortiz et al. 2017 [@mb-ortiz-2017] | Discovery | Square-well | Limb and ring ellipses | Haumea ring, opening angle, density limit |
| Pereira et al. 2023 [@mb-pereira-2023] | Discovery | Lorentzian ring profile | Nine-chord ellipse | Second Quaoar ring |
| Meza et al. 2019 [@mb-meza-2019] | Atmosphere | Refractive | Not applicable | Pluto pressure record |

## What a developer should do

1. Build the edge model as SORA does, as straight-edge Fresnel diffraction convolved with star disc and exposure. Replace its two-wavelength average with a real passband integration, and add limb darkening when $r_\star$ is comparable to $F$ [@mb-sora-code].
2. Fit times with explicit dead-time handling and report $\sigma_t$ per event [@mb-gomes-junior-2022-sora].
3. Move all chord ends to one reference time with the cubic shadow motion before fitting [@mb-herald-2020].
4. Fit a circle, an ellipse or a shape model according to the chord distribution. Use Herald's miss rule and single-chord error rules as the documented baseline [@mb-herald-2020].
5. Use the code's albedo formula with the factor 0.4, not the printed one [@mb-sora-code].

Read SORA's section 2.2 and `lightcurve/core.py` first, then Herald et al. 2020 sections 4 and 5.

## What this changes

Nothing in the eclipse pipeline. Occultation reduction adds a separate inverse stage that eclipse work does not have: from timed events back to the body's outline and position. It reuses the fundamental-plane geometry, and it needs a physical-optics model of the edge that eclipse [contact times](../../20-solar-eclipses-and-transits/04-local-circumstances/contact-times-and-magnitude.md) never use.

## Open questions

- Obtain Roques, Moncuquet and Sicardy 1987 (AJ 93, 1549) to check the bar model and its sign conventions against SORA's `bar_fresnel`.
- Obtain the AOTA documentation in Occult's help file to compare its diffraction and star-diameter treatment with SORA's [@sw-occult4].
- Obtain Morgado et al. 2023 (Nature 614, 239) for Quaoar's first ring, which is cited here only through Pereira et al. 2023 [@mb-pereira-2023].
- Obtain the PDS asteroid occultation bundle and its `bundle_description.txt` to record the current version, field definitions and stated issues [@mb-herald-2020].
- Obtain the full Elliot, Dunham and Mink 1977 paper for the ring timings and the prediction that put the airborne telescope in place [@mb-elliot-1977].
