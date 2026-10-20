---
title: Mutual events of the Galilean satellites
seo_title: Galilean Satellite Mutual Events: Geometry and Accuracy
description: How mutual eclipses and occultations of Jupiter's moons are predicted, modelled and reduced to astrometry, from the 1973 campaign to PHEMU21 and 2026-27.
order: 3
status: working
updated: 2026-10-17
tags: [jupiter, galilean-satellites, mutual-events, phemu, astrometry, hapke, light-curves]
---

::: summary
- **Mutual events need an equinox.** One Galilean satellite occults another when the Earth is near the satellites' common orbital plane, and eclipses another when the Sun is. That happens for about a year around each Jovian equinox, every 5.9 years: 2009, 2014 to 2015, 2021 and 2026 to 2027 [@jup-saquet-2018] [@jup-oksanen-2026].
- **The Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) has run a PHEMU campaign every season since 1985.** Light curves grew from 91 in 1973 and 166 in 1985 to 609 in 2014 to 2015. The 2021 season, with Jupiter near conjunction, gave 84 [@jup-thuillot-tanga-1997] [@jup-saquet-2018] [@jup-emelyanov-2022].
- **A light curve becomes a relative position.** The reduction fits two offsets $D_x$, $D_y$ to the ephemeris separation so that a modelled flux $K\,\Phi(X_{th}+D_x, Y_{th}+D_y)$ matches the observed one. The result is the separation at closest approach in the sky plane [@jup-saquet-2018].
- **The model needs the satellites' surfaces.** Current reductions include albedo, a Hapke or Oren-Nayar scattering law, the phase angle and limb darkening. Uneven albedo moves [Io](https://en.wikipedia.org/wiki/Io_(moon))'s photocentre by -50 to +90 km, enough to bias a uniform-disc fit [@jup-saquet-2018] [@jup-catani-2023] [@jup-vasundhara-2017].
- **Accuracy is 5 to 50 milliarcseconds, 15 to 150 km at Jupiter.** Whole-campaign rms O-C was 46 to 81 milliarcseconds in 2009, 39 to 61 in 2015 and 48 to 49 in 2021. Single well-observed series reach 5 to 10 milliarcseconds. Classical CCD astrometry gives about 100 milliarcseconds [@jup-arlot-2014] [@jup-saquet-2018] [@jup-emelyanov-2022] [@jup-catani-2023] [@jup-morgado-2019].
- **The data shape the ephemerides.** JUP310 and NOE both include PHEMU85 to PHEMU03. Lainey et al. measured the tidal dissipation of Io and Jupiter from astrometry in which mutual events were the most accurate data [@jup-saquet-2018] [@jup-lainey-2009].
:::

**The question.** When do the [?jup-galilean-satellites|Galilean satellites] produce [?mutual-event|mutual events], occulting and eclipsing one another? How are those events predicted, what photometric model turns a light curve into an astrometric position, and how accurate are the positions from each campaign?

## When mutual events happen

Saquet et al. give the condition in one sentence. "Occultations can occur when the Joviocentric declination of the Earth becomes zero, whereas eclipses can occur when the Joviocentric declination of the Sun becomes zero" [@jup-saquet-2018]. These are the [?jup-jovicentric-declination|jovicentric declinations] $D_E$ and $D_S$. [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus)'s low-accuracy method gives them [@jup-soniakeys-jupitermoons]:

$$
D_S = 3.12^{\circ}\sin(\lambda + 42.8^{\circ}), \qquad
D_E = D_S - 2.22^{\circ}\sin\psi\cos(\lambda + 22^{\circ}) - 1.30^{\circ}\,\frac{r-\Delta}{\Delta}\sin(\lambda - 100.5^{\circ}),
$$

with $\lambda = 34.35^{\circ} + 0.083091^{\circ}\,d + 0.329^{\circ}\sin V + B$, $d$ in days from J2000, and $\psi$ the phase angle, as in [theories and ephemerides](theories-and-ephemerides.md). $\lambda$ advances by one revolution in one Jovian year. $D_S$ crosses zero twice per revolution, so the seasons recur every 5.93 years. Jupiter's equator is inclined about 3.1 degrees to its orbit, so $D_S$ never exceeds that. The fastest rate of change of $D_S$ is $3.12^{\circ} \times 0.0831^{\circ} \times \pi/180 = 0.0045^{\circ}$ per day, or 1.6 degrees per year.

A rough window follows. Two satellites at radii $a_i < a_j$ in conjunction on the same side of Jupiter are separated in the sky-plane Y direction by about $(a_j - a_i)\sin D_E$. An occultation needs that to be smaller than the sum of their radii. For Io and [Europa](https://en.wikipedia.org/wiki/Europa_(moon)), $(671{,}100 - 421{,}800)\sin D_E < 1829 + 1563$ km gives $|D_E| < 0.78^{\circ}$, with the radii from the IAU values in NAIF's PCK [@sats-naif-pck00011] and the orbital radii from Westfall [@jup-westfall-alpo]. At 1.6 degrees per year that window lasts about a year. This estimate neglects the satellites' own inclinations to Jupiter's equator. It is consistent with the 2014 to 2015 season, which ran from 2014 September 1 to 2015 July 20 [@jup-saquet-2018].

Saquet et al. expected the 2021 season to be less favourable, "since the maximum of events will occur at the conjunction of Jupiter with the Sun, and 192 events will be observable" [@jup-saquet-2018]. The 1979 season had the same problem, so "very few phenomena were observed" [@jup-thuillot-tanga-1997]. Arlot's 2014 slides give the recurrence for the other giant planets: Jupiter every 6 years, Saturn every 15, Uranus every 42 [@jup-arlot-weto-2014]. Saturn's satellites are treated in their own topic.

Mutual events come in several shapes. The observing guide of IMCCE's Natural Satellites Data Center (NSDC) lists "occultation or eclipse, total, partial or annular", and notes that the light curve differs between these types [@jup-nsdc-guide]. An eclipse and an occultation of the same pair can also coincide. So et al. call this a quasi-simultaneous mutual event and observed one between Europa and [Ganymede](https://en.wikipedia.org/wiki/Ganymede_(moon)) on 22 August 2021 [@jup-so-2022].

## Campaigns from 1973 to 2021

The first predictions were made in 1956, but no observation of them is known. Brinkmann and Millis predicted the 1973 events and called for observations [@jup-thuillot-tanga-1997]. Aksnes predicted them independently from Sampson's theory with Andoyer's method. He found discrepancies of "up to 30 minutes of time for J3 and J4" between the two prediction sets [@jup-thuillot-tanga-1997]. The 1973 campaign of Aksnes and Franklin collected 91 light curves. It gave the radii of Europa, Ganymede and [Callisto](https://en.wikipedia.org/wiki/Callisto_(moon)) to 27, 32 and 75 km and corrections to Sampson's orbital elements [@jup-thuillot-tanga-1997]. Lieske used 85 mutual events in his 1978 and 1980 fits, which led to E-2 [@jup-thuillot-tanga-1997] [@jup-arlot-1982].

IMCCE, formerly part of the Bureau des longitudes, has organised the [?jup-phemu|PHEMU] campaigns since. Saquet et al. give the statistics in their Table 1 [@jup-saquet-2018].

| Campaign | Observation sites | Light curves | Observable events | Observed events | Source |
|---|---|---|---|---|---|
| 1973 | not stated | 91 | not stated | not stated | [@jup-thuillot-tanga-1997] |
| PHEMU85 | 28 | 166 | 248 | 64 | [@jup-saquet-2018] |
| PHEMU91 | 56 | 374 | 221 | 111 | [@jup-saquet-2018] |
| PHEMU97 | 42 | 292 | 390 | 148 | [@jup-saquet-2018] |
| PHEMU03 | 42 | 377 | 360 | 118 | [@jup-saquet-2018] |
| PHEMU09 | 74 | 457 | 237 | 172 | [@jup-saquet-2018] |
| PHEMU15 | 75 | 609 | 442 | 236 | [@jup-saquet-2018] |
| PHEMU21 | not in the abstract | 84 | 192 | not in the abstract | [@jup-emelyanov-2022] [@jup-so-2022] |

The PHEMU97 catalogue paper itself reports "275 observations of 148 mutual events from 42 sites" [@jup-arlot-2006]. The PHEMU03 catalogue reports "377 observations of 118 mutual events from 42 sites" [@jup-arlot-2009]. For PHEMU15, IMCCE received 643 light curves and computed astrometric results for 609. One event was recorded 17 times [@jup-saquet-2018]. For PHEMU21, MULTI-SAT predicted 242 events, of which 192 could be observed between 2021 March 3 and November 16 given Jupiter's angle from the Sun [@jup-so-2022].

## Predicting the events

IMCCE published predictions as plain tables before each campaign. The 1997 file lists "469 mutual eclipses and occultations", with local visibility files for 19 observatories and PC software to compute local conditions [@jup-imcce-phemu97-readme]. The current tool is MULTI-SAT, run jointly by IMCCE and the Sternberg Astronomical Institute (SAI) in Moscow. Its paper describes it as a facility that produces ephemerides of all natural satellites with "special features ... such as predicting the phenomena and providing configurations useful for the observers" [@jup-emelyanov-arlot-2008].

The prediction tables list, per event, the start and end in UTC, the type in the form "nEm" or "nOm", the duration, the [?impact-parameter|impact parameter], the combined magnitude and its expected drop, and the distance from Jupiter's limb [@jup-oksanen-2026]. The impact factor "is equal to zero if the event is a central passage" and "equal to unit in the case of a grazing event" [@jup-oksanen-2026]. MULTI-SAT's PHEMU21 predictions came from the theory of Lainey et al. (2009) [@jup-so-2022]. PHEMU15 predictions used NOE-5-2010-GAL with INPOP13c [@jup-saquet-2018]. [Occult](../../10-shared/09-software-and-repos/commercial-and-institutional-tools.md) also predicts Galilean mutual events [@jup-so-2022].

The geometry is the satellite analogue of a solar eclipse. For an occultation the shadow is replaced by the cone of visibility from the observer, and the reduction works in a topocentric frame. For an eclipse it works in a heliocentric frame [@jup-saquet-2018]. The eclipsing satellite's penumbra at the eclipsed one has the width $w = 2\,\delta d\,R_\odot/r$ from [the Jovian shadow](eclipses-occultations-transits-shadows.md#jupiters-shadow-at-the-satellites), with $\delta d$ the distance between the two satellites along the shadow. For Io eclipsing Europa at $\delta d \approx 250{,}000$ km that is about 450 km, about 0.3 of Europa's radius. So et al. simplify this with one effective shadow radius "17% larger than the apparent radius of umbra" and "13% smaller than apparent radius of penumbra", from formulas of Emelyanov (2003) [@jup-so-2022].

## The photometric model

The observable is the combined flux of the satellites in one aperture against time. The NSDC guide explains why these events give better astrometry than eclipses by Jupiter. Most of the satellites "have no atmosphere disturbing the light curve because of the refraction of the light" [@jup-nsdc-guide]. The photometric signal depends on how light is spread over each disc. The models have grown in steps:

| Model ingredient | Where it is used | Source |
|---|---|---|
| Uniform disc | Early 1973 reductions; So et al. 2021 | [@jup-thuillot-tanga-1997] [@jup-so-2022] |
| Polar caps and albedo spots on Europa | 1973 analyses explaining flux-drop discrepancies | [@jup-thuillot-tanga-1997] |
| Albedo maps from spacecraft mosaics | Emelyanov and Gilbert (2006), Vainu Bappu Observatory (VBO) 2014 to 2015 | [@jup-vasundhara-2017] |
| Hapke scattering parameters, leading and trailing hemispheres | VBO 2014 to 2015 | [@jup-vasundhara-2017] |
| Albedos, Hapke's law, phase effect, limb darkening | PHEMU15 reduction | [@jup-saquet-2018] |
| Oren-Nayar reflectance, solar limb darkening, numerical penumbra | Brazilian 2021 reduction | [@jup-catani-2023] |

The [?jup-hapke-model|Hapke model] describes a rough particulate surface. VBO took the Hapke parameters of Domingue and Verbiscer (1997) for the leading and trailing sides of Europa, Ganymede and Callisto, and those of McEwen et al. (1988) for Io [@jup-vasundhara-2017]. They chose each satellite's brightness distribution so that it reproduces the ground-based rotational light curve. They found that albedo maps alone fit Io and Europa but not Ganymede or Callisto [@jup-vasundhara-2017]. The [?photocentre|photocentre] shift matters. For central events Vasundhara (2002) estimated shifts of "-50 to +90 km ( -14 to +25 mas) for Io and -30 to +50 km ( -8 to +14 mas) for Europa" [@jup-vasundhara-2017]. A uniform, limb-darkened model produced "a bias along the satellite track" consistent with that shift, and the albedo model removed it [@jup-vasundhara-2017].

Catani et al. used "the complete version of the Oren-Nayer model" for the satellites. For a mutual eclipse they modelled the Sun's limb darkening with the law of Hestroffer and Magnan (1998) [@jup-catani-2023]. This is the same physics as the solar [?limb-darkening-function|limb-darkening function] in solar eclipse bead work. In a mutual eclipse it shapes the penumbral part of the light curve. They measured the albedo ratio of the two satellites on the same night with the same instrument where possible [@jup-catani-2023]. So et al. neglect light reflected from Jupiter in the flux model, citing Emelyanov et al. (2011) for the argument [@jup-so-2022].

## From light curve to position

Two reduction methods are in use. They give the same kind of result.

**Emelyanov's method (IMCCE and SAI).** Let $\Phi$ be the normalised flux, with $\Phi = 1$ outside the event. It is a function $\Phi(X(t), Y(t))$ of the projections of the satellites' angular separation on the celestial parallel and meridian. The ephemeris gives $X_{th}(t_i)$, $Y_{th}(t_i)$ at each observation time $t_i$. The method assumes constant corrections, $X(t) = X_{th}(t) + D_x$ and $Y(t) = Y_{th}(t) + D_y$. It then solves

$$
E_i = K\,\Phi\big(X_{th}(t_i) + D_x,\; Y_{th}(t_i) + D_y\big), \qquad i = 1, \dots, m,
$$

for $D_x$, $D_y$ and the scale $K$ by linearised least squares, where $E_i$ is the observed flux [@jup-saquet-2018]. The published result is $X = X_{th}(t) + D_x$, $Y = Y_{th}(t) + D_y$ at the instant of closest apparent approach. Here $X = \Delta\alpha\cos\delta$ and $Y = \Delta\delta$, "occulting minus occulted" or "eclipsing minus eclipsed" [@jup-saquet-2018]. For a total event only the position angle $P$, with $\tan P = X/Y$, can be found, and only to within 180 degrees [@jup-saquet-2018].

**The impact-parameter method (Brazil, VBO).** This method fits the impact parameter $d_0$, the central instant $t_0$ and the relative velocity $v_0$, with the apparent distance $\rho(t) = \sqrt{d_0^2 + v_0^2 (t - t_0)^2}$ [@jup-catani-2023]. It generates about nine hundred simulated light curves for each event around the ephemeris values and keeps the minimum chi-square [@jup-catani-2023]. VBO fits a shift $s$ along the track and a change $\Delta IP$ in the impact parameter. With $P$ the position angle of Jupiter's pole, they convert these to

$$
X = IP\sin P, \quad Y = IP\cos P, \qquad
(O-C)_X = s\cos P + \Delta IP\sin P, \quad (O-C)_Y = -s\sin P + \Delta IP\cos P,
$$

assuming the track is perpendicular to the pole [@jup-vasundhara-2017]. The observed instant of closest approach is $T_{obs} = T_{pred} - s/v$ [@jup-vasundhara-2017].

Timing must be good to better than 0.1 s. "The satellite Io ... has a velocity of 17.2 km s⁻¹, so that an accuracy of 0.1 s of time corresponds to an accuracy of 1.7 km in space". The internal accuracy of the theory is "around 1 km" [@jup-saquet-2018]. The NSDC asks for each photometric measure to be referred to UTC "within an accuracy at least of 0.1 second of time" [@jup-nsdc-guide].

## Achieved accuracy

| Data set | Ephemeris compared | Result | Source |
|---|---|---|---|
| Mutual events 1973 to 2003 | NOE fit | 1σ about 0.025 arcseconds | [@jup-lainey-2009] |
| PHEMU09, 457 light curves | not stated in the abstract | rms O-C 45.8 mas (RA), 81.1 mas (Dec) | [@jup-arlot-2014] |
| PHEMU15, 609 light curves | NOE-5-2010-GAL | fit σ 23.6 and 24.6 mas, rms O-C 39.2 and 60.7 mas | [@jup-saquet-2018] |
| PHEMU15, same data | JUP310 | mean rms O-C 65.5 mas, against 49.9 mas for NOE | [@jup-saquet-2018] |
| PHEMU21, 84 light curves | "current best ephemerides" | rms O-C 49 and 48 mas | [@jup-emelyanov-2022] |
| Brazil 2021, Galilean events | [DE440](../../10-shared/08-lunar-and-solar-model/ephemerides.md) with JUP365 | average 5 mas (15 km), best 2.8 mas (8.4 km) | [@jup-catani-2023] |
| VBO 2014 to 2015, seven 2E1/2O1 events | L2 (NOE-5-2010-GAL-a2) | rms 8.7 and 7.8 mas | [@jup-vasundhara-2017] |
| Mutual approximations 2016 to 2018 | not stated in the abstract | internal precision 11.3 mas | [@jup-morgado-2019] |
| Classical CCD astrometry | for comparison | about 100 mas | [@jup-morgado-2019] |

One [?milliarcsecond|milliarcsecond] is about 3 km at Jupiter. Saquet et al. convert 24 milliarcseconds to 75 km and 50 milliarcseconds to 150 km [@jup-saquet-2018]. Catani et al. use 5 milliarcseconds for 15 km [@jup-catani-2023]. The campaign-wide [?o-minus-c|O-C] figures mix professional and amateur light curves, so they measure the data as much as the ephemeris. The single-site results show what the method can do. Catani et al. found no mean offset larger than one sigma against DE440 with JUP365. They concluded that the ephemerides agree with the 2021 data "at the level of 5" milliarcseconds [@jup-catani-2023].

## What the data have been used for

Mutual-event positions enter every modern ephemeris fit. NOE-5-2010-GAL and JUP310 both use the PHEMU85 to PHEMU03 data, with different astrometric data sets otherwise [@jup-saquet-2018]. In Lainey et al. (2009), "the observations of mutual events, known to be among the most accurate observations, have a 1σ accuracy of about 0.025 arcsec and provide the best constraint of the satellite orbits for the past decades" [@jup-lainey-2009]. That fit gave $k_2/Q = 0.015 \pm 0.003$ for Io and $(1.102 \pm 0.203)\times 10^{-5}$ for Jupiter. It gave secular accelerations that shift Io, Europa and Ganymede by 55, 2125 and 2365 km over 116 years [@jup-lainey-2009].

The events also carry physics. Infrared observations of mutual events measure the volcanic activity of Io [@jup-thuillot-tanga-1997]. The 1973 light curves gave satellite radii and the first albedo maps of Europa [@jup-thuillot-tanga-1997]. The method also reaches the inner moons. A 2021 eclipse of Thebe by Ganymede gave Thebe's position to 32 milliarcseconds, 96 km [@jup-catani-2023].

## The 2026 to 2027 season

The next season is under way. A February 2026 observer presentation lists 305 predicted events between 2026 May 11 and 2027 August 10, generated with the SAI natural satellites service [@jup-oksanen-2026]. It quotes Saquet et al. on why the observations matter: "the precision of the mutual event observations is up to 20 mas for the Galilean moons (Arlot et al. 2014), or 60 km at the distance of Jupiter" [@jup-oksanen-2026] [@jup-saquet-2018]. Between seasons, mutual approximations give central instants at any time of year, with 11.3 milliarcseconds internal precision from 66 events in 2016 to 2018 [@jup-morgado-2019].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Saquet et al. (2018) [@jup-saquet-2018] | Campaign statistics 1985 to 2015, the Emelyanov reduction equations, NOE against JUP310 on one data set |
| Arlot et al. (2014) and Emelyanov et al. (2022), abstracts [@jup-arlot-2014] [@jup-emelyanov-2022] | Campaign-wide accuracy for 2009 and 2021 |
| Catani et al. (2023) [@jup-catani-2023] | A full modern model with Oren-Nayar reflectance and solar limb darkening, fitted against DE440 with JUP365 |
| Vasundhara et al. (2017) [@jup-vasundhara-2017] | Hapke parameters, albedo maps and the size of the photocentre bias |
| So et al. (2022) [@jup-so-2022] | PHEMU21 prediction counts and a simple model for a quasi-simultaneous event |
| Thuillot and Tanga (1997) [@jup-thuillot-tanga-1997] | The history of 1973 and 1979, with numbers |
| Lainey et al. (2009) [@jup-lainey-2009] | What the data are worth in a dynamical fit |
| Oksanen (2026) [@jup-oksanen-2026] | The format of the predictions and the 2026 to 2027 season |

## What a developer should do

1. **Predict with a modern ephemeris and both frames.** Compute occultations topocentrically and eclipses heliocentrically, with JUP365 and DE440 or NOE-5-2021 [@jup-saquet-2018] [@jup-naif-jup365-cmt] [@jup-imcce-noe-2021].
2. **Report what MULTI-SAT reports.** Give start and end in UTC, the "nEm"/"nOm" type, duration, impact factor, magnitude drop and distance from Jupiter's limb [@jup-oksanen-2026].
3. **Model the penumbra of the satellite's shadow.** Its width is $2\,\delta d\,R_\odot/r$, a large fraction of the eclipsed satellite's radius. A single effective radius is a known simplification [@jup-so-2022].
4. **For astrometry, use a surface model.** Use an albedo map or Hapke parameters with phase, and solar limb darkening for eclipses. A uniform disc biases positions by up to tens of milliarcseconds [@jup-vasundhara-2017] [@jup-catani-2023].
5. **Validate against the PHEMU catalogues** in IMCCE's NSDB and against the published O-C distributions [@jup-saquet-2018].

Read first: Saquet et al. (2018), Catani et al. (2023), Vasundhara et al. (2017).

## What this changes

Mutual events add a third use of the shadow-cone code, between two small spheres instead of between the Sun, a large body and a small one. The geometry is the [Besselian](../../10-shared/01-foundations/besselian-elements.md) construction with the eclipsing satellite as the Moon and the eclipsed satellite as the Earth. The new part is photometric. The pipeline would need a model of the target's surface brightness and of the Sun's limb darkening, integrated over the overlap of two discs at each time step. The solar-eclipse pipeline already computes the overlap of two discs for [obscuration](../../20-solar-eclipses-and-transits/04-local-circumstances/contact-times-and-magnitude.md).

## Open questions

- **Arlot et al. (2014) and Emelyanov et al. (2022), full texts.** Obtain both to quote their photometric models, the Hapke parameters used, and their per-satellite accuracy.
- **Emelyanov (2003) penumbra formulas.** Obtain the paper that So et al. cite for the effective umbra and penumbra radii, to quote the formulas.
- **Saquet et al. (2018) model section.** The paper gives the reduction method but cites Emelyanov and Gilbert (2006) for the photometric model. Obtain Emelyanov and Gilbert (2006), A&A 453, 1141, for the model equations.
- **PHEMU27 predictions.** Obtain IMCCE's or SAI's published prediction list for the 2026 to 2027 season, with the theory used, to replace the count taken from a presentation.
- **Oren-Nayar against Hapke.** Find a comparison of the two reflectance models on the same mutual-event light curves.
