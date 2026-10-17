---
title: Prediction geometry and astrometry
seo_title: Asteroid Occultation Prediction: Shadow Paths and Gaia
description: How the shadow path of an asteroid, TNO or satellite occultation is computed on the fundamental plane, and how Gaia changed its uncertainty.
order: 1
status: working
updated: 2026-10-17
tags: [stellar-occultation, asteroid, tno, fundamental-plane, gaia, astrometry, sora, occult]
---

::: summary
- **The shadow is a cylinder, not a cone.** The star is a point at infinity, so the occulting body's shadow on the fundamental plane has the body's own outline, and the path width there equals the body's diameter. On the ground it widens as the diameter divided by the sine of the star's altitude [@mb-gomes-junior-2022-sora] [@mb-preston-faq].
- **Prediction is a closest-approach search.** Star positions are propagated to the epoch, matched against the ephemeris, and kept when the separation is below the body's angular radius plus the ephemeris uncertainty plus the Earth's radius. SORA (Stellar Occultation Reduction and Analysis) then refines the closest approach in three grid passes down to 0.02 s [@mb-sora-code].
- **The 1-sigma lines sit one cross-track uncertainty outside each path edge.** That uncertainty is the quadrature sum of the star and ephemeris errors, converted to kilometres by the body's distance: 1 milliarcsecond is 0.7253 km per astronomical unit [@mb-tanga-delbo-2007] [@mb-sora-code].
- **Before Gaia the error was hundreds of kilometres.** Main-belt ephemerides were rarely better than 0.5 arcseconds, and catalogue stars carried 20 to 70 milliarcseconds. By 2019 a typical main-belt path was still uncertain by more than 40 km [@mb-tanga-delbo-2007] [@mb-herald-2020].
- **Gaia removed the star error and is shrinking the orbit error.** Occultation astrometry reduced against Gaia EDR3 fits orbits at about 10 milliarcseconds against 30 to 50 milliarcseconds with older catalogues. For bright 2024 events the path is now uncertain by a few tenths of a path width [@mb-ferreira-2022] [@mb-dunham-rasc-2024-mb].
- **An observed occultation is itself the best astrometry.** The fitted centre, offset from the ephemeris and tied to one Gaia star, gives the body's position to about 1 milliarcsecond. This feeds back into the next prediction [@mb-herald-2020] [@mb-rommel-2020] [@mb-desmars-2015-nima].
- **Timing must be absolute and fast.** Chords from different observers combine only if their times agree to about 10 milliseconds. The geocentre-to-observer light-time of 0.021 s is already 600 m at a shadow speed of 30 km per second [@mb-herald-2020] [@mb-gomes-junior-2022-sora].
:::

**The question.** How is the ground track of a [?mb-stellar-occultation|stellar occultation] computed when the occulter is an asteroid, a [?mb-tno|trans-Neptunian object], a [?mb-centaur|Centaur] or a planetary satellite? Which quantities set the width of its uncertainty band, and how did the Gaia catalogues and occultation astrometry change that uncertainty? Lunar occultations use the same plane but a nearby, large occulter with a known limb, and are the subject of [Lunar occultations](../13-lunar-occultations/_index.md).

![On the fundamental plane the shadow band has the body's own width, and the dashed 1-sigma lines sit one cross-track uncertainty outside each edge. After the event, chords at several offsets fix an ellipse whose centre, compared with the ephemeris position, is the astrometric result [@mb-gomes-junior-2022-sora] [@mb-herald-2020].](img/shadow-path-and-chords.svg)

## The geometry: a cylinder on the fundamental plane

An eclipse shadow is a cone because the Sun has a finite size at a finite distance. A star is effectively at infinity and its angular size is far below the body's. SORA's authors state that "unlike an eclipse, the star is farther and its angular size is much smaller than the body's, which results in almost the same size for the body and its umbra" [@mb-gomes-junior-2022-sora]. The shadow is then a cylinder parallel to the star direction, with the cross-section of the body's projected outline. Its track on the ground is the [?mb-shadow-path|shadow path].

The reference plane is the [?fundamental-plane|fundamental plane] of [Besselian elements](../01-foundations/besselian-elements.md), with the star's direction $(\alpha_\star, \delta_\star)$ taking the place of the point Z. Herald's reduction of asteroid occultations works on this plane "using Besselian elements", with the apparent positions of both the star and the asteroid defining its orientation [@mb-herald-2020]. In the plane, the shadow radius is the body's radius $R_\circ$ at every distance along the axis. There are no cone angles and no $l_1$, $l_2$ variation. The [?path-width|path width] on the plane is therefore $2R_\circ$ for a spherical body.

SORA writes the plane coordinates as orthographic projections onto the plane perpendicular to the geocentre-star direction. For the observer and the body [@mb-gomes-junior-2022-sora]:

$$
\xi_\lambda = D_\lambda \cos\delta_\lambda \sin(\alpha_\lambda - \alpha_\star), \qquad
\eta_\lambda = D_\lambda\left[\cos\delta_\star \sin\delta_\lambda - \sin\delta_\star\cos\delta_\lambda\cos(\alpha_\lambda - \alpha_\star)\right],
$$

$$
\xi_\circ = D_\circ \cos\delta_\circ \sin(\alpha_\circ - \alpha_\star), \qquad
\eta_\circ = D_\circ\left[\cos\delta_\star \sin\delta_\circ - \sin\delta_\star\cos\delta_\circ\cos(\alpha_\circ - \alpha_\star)\right],
$$

and the observer's position relative to the body's shadow centre is $(\xi_\lambda - \xi_\circ,\ \eta_\lambda - \eta_\circ)$, which the paper calls $(x, y)$. Here $D_\lambda$, $\alpha_\lambda$ and $\delta_\lambda$ are the geocentric distance, right ascension and declination of the observer's position vector in the ICRS, and $D_\circ$, $\alpha_\circ$, $\delta_\circ$ those of the body. $\xi$ is positive towards increasing right ascension and $\eta$ towards the ICRS north pole [@mb-gomes-junior-2022-sora]. The observer terms are the eclipse coordinates $\xi = \rho\cos\phi'\sin\theta$ and $\eta = \rho\sin\phi'\cos d - \rho\cos\phi'\sin d\cos\theta$ of [Contact times and magnitude](../04-local-circumstances/contact-times-and-magnitude.md), with $d = \delta_\star$ and $\theta$ the star's local hour angle. SORA's paper writes the plane offset as $x$ and $y$ in kilometres. In the eclipse notes $x$ and $y$ are the Moon's coordinates in Earth radii, a different quantity.

The paper's exact form, used for the astrometric offset itself, is $x = D_\circ \sin[(\alpha_\star - \alpha_\circ)\cos\delta_\circ]$ and $y = D_\circ\sin(\delta_\star - \delta_\circ)$, with both positions astrometric ICRS coordinates centred at the observer [@mb-gomes-junior-2022-sora]. Because the body's position is less certain than the star's in the Gaia era, the body coordinates in this equation are the ephemeris values. The fitted displacement of the observed centre is then an ephemeris offset [@mb-gomes-junior-2022-sora].

Two approximations hide in the geocentric form. First, the star is taken to be at infinity, so all observers share one line of sight. SORA's authors note that for Proxima Centauri the topocentric and geocentric star directions differ by up to 2.3 km projected at 100 au [@mb-gomes-junior-2022-sora]. Second, all observers are referred to one instant at the geocentre. The [?light-time|light-time] across one Earth radius is 0.021 s, which at 30 km per second is 600 m on the plane and matters for near-Earth asteroids [@mb-gomes-junior-2022-sora].

## Finding the events

A prediction search crosses an ephemeris with a star catalogue. In SORA's `prediction` function the ephemeris is sampled at a fixed step, 60 s by default, and Gaia stars are downloaded for the box the path covers [@mb-sora-code]. The star positions are propagated to the middle of the interval with `apply_space_motion`, matched to the nearest ephemeris point, and kept when the separation is below

$$
\arcsin\!\left(\frac{R_\circ + R_\oplus}{D_\circ}\right) + n_\sigma\,\max(\sigma_\alpha, \sigma_\delta) + \mu_\star\,\frac{\Delta t}{2},
$$

where $R_\oplus$ is added only for a geocentric search, the multiplier $n_\sigma$ takes the value of the program argument `sigma`, default 1, $\sigma_\alpha$ and $\sigma_\delta$ are the ephemeris errors in arcseconds, $\mu_\star$ is the star's total proper motion and $\Delta t$ the search interval [@mb-sora-code]. The paper describes the same search radius as "the body's radius increased by the ephemeris 1-sigma uncertainty", with the Earth's radius added for a geocentric search [@mb-gomes-junior-2022-sora].

Each candidate is then refined. The paper gives the [?mb-closest-approach|closest approach] from two ephemeris positions bracketing the star, after Assafin et al. 2010 [@mb-gomes-junior-2022-sora]:

$$
CA = \sqrt{\Delta_1^2 - \left(\frac{\Delta_1^2 - \Delta_2^2 + \Delta_B^2}{2\Delta_B}\right)^2}, \qquad
t_0 = t_1 + (t_2 - t_1)\sqrt{\frac{\Delta_1^2 - CA^2}{\Delta_B^2}},
$$

with $\Delta_1$ and $\Delta_2$ the star's separations from the ephemeris positions at $t_1$ and $t_2$ and $\Delta_B$ the separation between those positions. The [?mb-shadow-velocity|shadow velocity] is $V_S = D_\circ \sin(\Delta_B)/(t_2 - t_1)$ [@mb-gomes-junior-2022-sora]. The released code does something different. Function `occ_params` evaluates the projected separation on a grid of ±900 s at 20 s steps, then ±20 s at 0.5 s, then ±1 s at 0.02 s. It takes the minimum each time and recurses when the minimum falls at a grid edge [@mb-sora-code]. It computes the position angle as `arctan2(-f, -g)` of the projected offset `(f, g)`, and the velocity as the change in that offset over one second, signed by the east-west direction of motion [@mb-sora-code]. The paper's two-point formula is the algorithm description. The grid search is the implementation.

Both assume straight-line motion of the shadow during the event. The paper justifies it by the short duration: at the Earth's mean orbital speed of 29.78 km per second a small body's shadow crosses the Earth in about 7 minutes. It warns that the linear path fails near quadrature, when the shadow is slow, and suggests a polynomial instead [@mb-gomes-junior-2022-sora]. Herald's reduction uses "a cubic expression representing the motion of the asteroid's shadow on the fundamental plane" [@mb-herald-2020].

The amateur prediction services split the search from the update. In Preston's 2007 description, several searchers each scanned for events with their own orbits and catalogues. Goffin covered asteroids of 40 km and larger with a compiled catalogue to about magnitude 12. Donnell and Breit used astorb.dat and Occult's Tycho-2 catalogue for asteroids of 10 km and larger [@mb-preston-update-2007]. Preston then refitted the orbit with recent astrometry and recomputed the path with Occult a month and a week before each event [@mb-preston-update-2007]. Since 2024 Preston's site states that its posted predictions are not the most current, and that current ones are distributed through OccultWatcher [@mb-preston-home]. The 2024 supplement of the Royal Astronomical Society of Canada (RASC) confirms that updates "with improved orbits during the year" are "now done only with Occult Watcher" [@mb-dunham-rasc-2024-mb].

## From closest approach to a path on the ground

SORA's map draws the path from the prediction-table values alone [@mb-sora-code]. For each time offset $\tau$ from closest approach, the shadow centre on the plane is

$$
X = CA_{\mathrm{km}} \sin PA + V_S\,\tau \cos PA', \qquad Y = CA_{\mathrm{km}} \cos PA - V_S\,\tau \sin PA',
$$

where $CA_{\mathrm{km}} = D_\circ \times CA$ in radians, $PA$ is the position angle and $PA'$ is $PA$ folded into ±90 degrees [@mb-sora-code]. The two path edges are the centre moved by $\pm R_\circ$ along $(\sin PA', \cos PA')$. The 1-sigma lines are moved by $\pm(R_\circ + D_\circ\,\sigma)$ with $\sigma$ the ephemeris error converted from milliarcseconds to radians [@mb-sora-code]. Function `xy2latlon` converts plane points to longitude and latitude. It takes the depth along the star direction on a sphere of radius `R_earth`, transforms GCRS to ITRS, reprojects the resulting site on the ellipsoid at zero height, and iterates four times [@mb-sora-code]. The map is therefore a path at sea level on the ellipsoid. It ignores observer height.

Occult's map, as Preston describes it, draws solid edges assuming a circular body [@mb-preston-faq]. Preston states that the ground width exceeds the body's width when the star is not overhead: "The width of the shadow = (diameter of asteroid) / SIN (maximum altitude of star along the path)" [@mb-preston-faq]. That expression is the width measured along the ground in the direction of the star's azimuth. On the fundamental plane the width remains the diameter.

The [?mb-one-sigma-line|1-sigma lines] are, in Preston's words, "the effect of a 1-sigma shift in the edge of the path", with "a 68% probability the actual path ... will fall somewhere between the 1-sigma lines" and the 2-sigma lines at twice the distance from each edge with 95 per cent [@mb-preston-faq]. Occult's plot header also gives the full uncertainty ellipse as major axis, minor axis and position angle [@mb-preston-faq]. Preston's event Rank is "the probability of at least one successful observation by a team of two observers where the two observers are positioned 3/4 path width apart symmetrically about the center of the path" [@mb-preston-faq].

## The uncertainty budget

Tanga and Delbo define the path uncertainty as the quadrature sum of the ephemeris and star errors [@mb-tanga-delbo-2007]:

$$
\sigma_{\mathrm{path}} = \sqrt{\sigma_{\mathrm{CEU}}^2 + \sigma_\star^2},
$$

where $\sigma_{\mathrm{CEU}}$ is the current ephemeris uncertainty of the asteroid and $\sigma_\star$ the star position error at the event epoch. They define a prediction efficiency $p = 2\theta/\sigma_{\mathrm{path}}$, with $2\theta$ the apparent diameter, and read $p = 1$ as a 68 per cent chance of seeing the event [@mb-tanga-delbo-2007]. The angular uncertainty becomes a [?mb-cross-track|cross-track] distance on the plane through the body's distance. One [?milliarcsecond|milliarcsecond] at 1 au is $1.495979\times10^{8}\ \mathrm{km}\times 4.8481\times10^{-9} = 0.7253$ km. Herald puts it as "an angular displacement of 1 mas is crudely equivalent to a displacement of the asteroid's shadow of about 1 km" for the main belt [@mb-herald-2020]. Buie quotes 31.4 km per milliarcsecond for Arrokoth at 43.3 au [@mb-buie-2020-arrokoth].

SORA's paper turns the budget into a target. The combined error must be of the order of the body's apparent radius, about 230 milliarcseconds for Ceres, 40 milliarcseconds for Pluto, and as little as 1 milliarcsecond for small distant bodies [@mb-gomes-junior-2022-sora].

### The star

Before Gaia, the star term was large and catalogue-dependent. Tanga and Delbo give about 1 milliarcsecond for FK6, 10 milliarcseconds for Hipparcos, 70 for Tycho-2 and 20 for UCAC2 in the magnitude range 10 to 14 [@mb-tanga-delbo-2007]. Preston's 2007 process preferred UCAC2 "whenever available", and treated double stars as a standing problem [@mb-preston-update-2007].

The [?mb-gaia-catalogue|Gaia releases] made the star term small. SORA's paper cites Gaia EDR3 positions below 1 milliarcsecond to magnitude 21, about 10 microarcseconds for stars brighter than magnitude 15 at the catalogue epoch, and proper motions near 20 microarcseconds per year for those stars [@mb-gomes-junior-2022-sora]. French and Souami state that DR3 proper motions are "a factor of 2 more accurate than in the DR2 catalog" [@mb-french-souami-2023]. Three residual issues remain, and each source names them:

- **Unresolved companions.** A [?mb-ruwe|RUWE] above 1.4 flags a poor single-star fit, and positive occultations of such stars "showed a significant shift from the predictions" [@mb-gomes-junior-2022-sora]. Preston's FAQ gives the same warning for DR2 and its duplicated-source flag [@mb-preston-faq].
- **Bright-star frame rotation in DR2.** Herald lists that DR2 stars brighter than about magnitude 12.5 "are affected by a frame rotation error", and that this uncertainty was not yet in the data set [@mb-herald-2020].
- **Proper-motion systematics in EDR3.** SORA's paper cites a systematic error of up to 80 microarcseconds per year for stars brighter than magnitude 13. For the 1988 Pluto occultation star it amounts to 1.10 milliarcseconds in declination against a formal error of 0.35 milliarcseconds [@mb-gomes-junior-2022-sora]. SORA can apply the Cantat-Gaudin and Brandt correction, and French and Souami applied it to DR3 [@mb-gomes-junior-2022-sora] [@mb-french-souami-2023].

SORA propagates the star from the catalogue epoch with the rigorous model of Butkevich and Lindegren 2014, including the propagation of its uncertainty, and then applies parallax for the chosen observer [@mb-gomes-junior-2022-sora]. Herald's astrometry corrects for proper motion "including foreshortening" and for parallax [@mb-herald-2020].

### The ephemeris

The ephemeris term is now the dominant one. JPL Horizons outputs, for bodies with a covariance, the right ascension and declination uncertainty and a [?mb-plane-of-sky-ellipse|plane-of-sky error ellipse]. Both are "formal +/- 3-standard-deviation" values, and Horizons warns they "can be optimistic" when there are systematic biases or long extrapolations [@sw-horizons-manual]. A 1-sigma path therefore needs the Horizons value divided by 3. The SBDB API returns the orbital covariance itself, at the JPL orbit-solution epoch, as a full matrix or an upper-triangular vector [@mb-sbdb-api]. SORA does not read either. Its ephemeris errors `error_ra` and `error_dec` are user inputs in arcseconds, and both default to zero [@mb-sora-code]. A default SORA run therefore searches with no ephemeris margin. Its map draws dashed error lines only when the separate `error` argument, in milliarcseconds, is given [@mb-sora-code].

For trans-Neptunian objects the Lucky Star group fits its own orbits with [?mb-nima|NIMA]. The least-squares correction and covariance propagation are [@mb-desmars-2015-nima]:

$$
\widehat{\Delta \mathbf{q}} = (A^T V_{\mathrm{obs}}^{-1} A)^{-1} A^T V_{\mathrm{obs}}^{-1}\,\Delta Y, \qquad
\Lambda(t) = A(t)\,\Lambda_0\,A(t)^T,
$$

where $\mathbf{q}$ is the six-element state vector, which the paper writes $C$, $A$ the matrix of partial derivatives, $\Delta Y$ the observed-minus-computed residuals, $\Lambda_0 = (A^T V_{\mathrm{obs}}^{-1} A)^{-1}$ the covariance at the epoch and $\Lambda(t)$ its linear propagation to date $t$ [@mb-desmars-2015-nima]. The weighting prevents one well-observed night from dominating [@mb-desmars-2015-nima]:

$$
\omega_i^2 = N_i\,b_i^2 + \sigma_i^2,
$$

with $N_i$ the number of observations from the same observatory on the same night, $b_i$ a bias for that observatory and catalogue, and $\sigma_i$ the individual precision. The adopted biases are 300 milliarcseconds for Minor Planet Center positions, 75 to 300 milliarcseconds for the group's own positions depending on telescope and catalogue, and zero for occultation positions [@mb-desmars-2015-nima]. The NIMA README records the occultation precision as 40 or 75 milliarcseconds. Since 2016 December 7, version 4 has also weighted offsets reduced with Gaia DR1 by $b = 40 + 20\,|\mathrm{yr} - 2015|$ mas and $\sigma = 20 + 20\,|\mathrm{yr} - 2015|$ mas [@mb-nima-readme].

The alternative is the [?mb-offset-method|ephemeris offset method]: measure the body against a reference ephemeris a few days before the event and apply that offset as a constant [@mb-gomes-junior-2022-sora]. Desmars et al. showed that the offset between NIMA and JPL ephemerides drifts "even for short time scales of a few weeks". The constant-offset method "could not accurately predict 6 out of the 13 observed positive occultations successfully predicted by NIMA" [@mb-desmars-2015-nima].

For main-belt asteroids in 2007, Preston fitted orbits with OrbFit using JPL DE405, all planets and the Moon, and 13 large asteroids as perturbers. He gave a default a priori RMS of about 1 arcsecond to ordinary astrometry and 0.12 to 0.35 arcseconds to "high accuracy" data [@mb-preston-update-2007]. For 2024, the RASC supplement takes orbital elements from JPL Horizons and star data from Gaia DR3 in Occult's own catalogue [@mb-dunham-rasc-2024-mb].

## Orbit improvement: Gaia astrometry and occultation astrometry

An occultation is itself an astrometric measurement. Herald's procedure inverts the Besselian computation [@mb-herald-2020]:

1. Find the plane coordinates of the shadow centre at the reference time.
2. Run an inverse Besselian calculation for the offset from the star's apparent position.
3. Convert that offset to the J2000 ICRS frame by removing precession, nutation and aberration.
4. Add it to the star's ICRS position corrected for parallax and proper motion.
5. Correct for the relativistic deflection of the asteroid relative to the star. This "can be significant for solar elongations as large as 145° or more".

Because the result is tied to one star, it "can be updated whenever the star position is updated" [@mb-herald-2020]. Because it is measured from the full outline, it refers to the [?centre-of-figure|centre of figure], or to the [?centre-of-mass|centre of mass] when a shape model is fitted. Image astrometry, including Gaia's, measures the [?photocentre|photocentre] [@mb-herald-2020]. For Eros at a 51 degree phase angle the photocentre is displaced by about 5 per cent of the mean diameter [@mb-herald-2020].

Ferreira et al. fitted orbits to the whole occultation record. With pre-Gaia catalogues the residuals were 30 to 50 milliarcseconds, and 80 to 90 milliarcseconds for some catalogues. With Gaia EDR3 they fell to about the 10 milliarcsecond level, an average factor of about 5 [@mb-ferreira-2022]. The core of the residual distribution has a full width at half maximum of about 10 milliarcseconds along-track and cross-track [@mb-ferreira-2022]. The authors conclude that "occultation astrometry can reach the performance of Gaia on small asteroids (5-8 km in the main belt)" [@mb-ferreira-2022]. The Gaia Focused Product Release fitted orbits of nearly 157 000 asteroids from Gaia data alone. It tested them against 5 774 occultation positions of 978 asteroids [@mb-gaia-fpr-2023]. For events within the Gaia time span the observed-minus-computed distance "peaks at about 10 mas", and away from it the ephemeris degrades by about 10 milliarcseconds per year [@mb-gaia-fpr-2023].

For distant bodies one chord is enough. Rommel et al. derived 37 positions for 19 TNOs and 4 Centaurs, 68 per cent of them single-chord, "most have intrinsic precision at the submilliarcsecond level" on the Gaia DR2 frame [@mb-rommel-2020]. Camargo et al. state that occultation positions receive the largest weights in NIMA because they are accurate at the milliarcsecond level [@mb-camargo-2018]. SORA's paper adds that such positions "can highly improve the ephemeris ... even if it is from a single-chord event" [@mb-gomes-junior-2022-sora].

The Arrokoth campaigns show the loop working on a 30 km body at 43 au. The final prediction for 2017 June 3 had a 1-sigma cross-track uncertainty of 44 km [@mb-buie-2020-arrokoth]. After new Hubble Space Telescope (HST) astrometry reduced against pre-release Gaia DR2, the July 2017 predictions reached 14 km cross-track, 0.46 milliarcseconds. With the 2017 July 17 occultation position included, the 2018 August 4 prediction was 13 km cross-track and 1.8 s, or 36 km, along-track [@mb-buie-2020-arrokoth]. Buie et al. planned station spacing with a Monte Carlo of the central line drawn from the predicted distribution. They used 15.5 km spacing for the 44 km case and 4 km spacing once the uncertainty was 14 km [@mb-buie-2020-arrokoth].

## Typical numbers before and after Gaia

| Quantity | Pre-Gaia | Gaia era | Source |
|---|---|---|---|
| Star position, catalogue stars | 10 to 70 mas | below 1 mas, about 0.01 mas for G < 15 | [@mb-tanga-delbo-2007] [@mb-gomes-junior-2022-sora] |
| Main-belt ephemeris | rarely below 500 mas (2007) | more than 40 mas typical (2019) | [@mb-tanga-delbo-2007] [@mb-herald-2020] |
| Path uncertainty at 1 au | about 350 km (2007) | not given | [@mb-tanga-delbo-2007] |
| Main-belt path uncertainty | more than 40 km (2019) | a few tenths of a path width for bright 2024 events | [@mb-herald-2020] [@mb-dunham-rasc-2024-mb] |
| Occultation astrometry, orbit residuals | 30 to 50 mas | about 10 mas | [@mb-ferreira-2022] |
| Gaia-only orbits against occultations | not available | peak about 10 mas, degrading about 10 mas per year | [@mb-gaia-fpr-2023] |
| TNO path, Arrokoth | 44 km (June 2017) | 13 to 14 km, 0.46 mas | [@mb-buie-2020-arrokoth] |
| Success rate of observed events | about 15 per cent (2005, Euraster) | not given | [@mb-tanga-delbo-2007] |

The count of events followed. Herald reports about 10 events a year in 1990 and 586 in 2019 [@mb-herald-2020]. Ferreira et al. identify a sharp rise with Hipparcos in the 1990s, a plateau from 2005 to 2015, and a new rise with Gaia DR1 in 2016 and DR2 in 2018 [@mb-ferreira-2022].

## Timing requirements

An occultation turns time into distance at the shadow velocity, typically several to tens of kilometres per second. Herald's list of improvements names accurate time as "the most critical item", seeking ways "to link accurate time (to within 10msec or less)" [@mb-herald-2020]. The common time source in that data set is a GPS receiver stamping each field of an analogue video stream. The recent anomalies were "associated with the use of NTP as a time source, personal equation for visual observations, and observers attempting an event at the limit of their system's capabilities" [@mb-herald-2020]. NTP is the Network Time Protocol. Observations are weighted by method: 5 for analogue video, 4 for digital video or photometer, 3 for sequential images or drift scans, and 1 for visual [@mb-herald-2020]. Past reports without stated time uncertainties are to receive 0.5, 1.0 or 1.5 s [@mb-herald-2020].

The Arrokoth flight of SOFIA, the Stratospheric Observatory for Infrared Astronomy, found three aircraft clocks offset from each other by 1 s steps. The likely cause was out-of-date leap-second almanac data, so the team trusted only the GPS-slaved clock recorded with the images [@mb-buie-2020-arrokoth]. Herald's time scale for reported events is UTC [@mb-herald-2020]. SORA expects UTC by default but accepts any Astropy time scale [@mb-gomes-junior-2022-sora].

The light-curve side of timing, including the sub-exposure estimate $\sigma_t = \sigma_{LC}\,t_{\mathrm{exp}}/\Delta f$, is in [Light curves, chords and results](light-curves-chords-and-results.md).

## Software, services and the data they use

| Tool or service | Role | Ephemeris used | Star catalogue | Notes |
|---|---|---|---|---|
| Occult 4 (Herald) [@sw-occult4] | Search, path maps, reduction, archive | JPL Horizons elements for 2024 predictions | Occult's own Gaia EDR3 or DR3 subset to mag 16 with UCAC4, Tycho-2 and HIP identifiers | Closed Windows program. Its observations file feeds the Planetary Data System (PDS) data set [@mb-dunham-rasc-2024-mb] [@mb-herald-2020] |
| OccultWatcher (Pavlov) [@mb-occultwatcher] | Feeds, filtering, station announcements | From each feed | From each feed | Feeds include Preston's International Occultation Timing Association (IOTA) updates, OZNZ, NAmer, E.A.O.N. and TNO extras [@mb-occultwatcher] |
| asteroidoccultation.com (Preston) [@mb-preston-home] | Updated main-belt predictions | OrbFit with DE405 in 2007 | UCAC2 and Tycho-2 in 2007, Gaia DR2 by 2019 | Current updates only through OccultWatcher since 2024 [@mb-preston-update-2007] [@mb-preston-faq] |
| Lucky Star (Sicardy et al.) [@mb-lucky-star-predictions] | TNO, Centaur and Trojan predictions and campaigns | NIMA, Genoid for satellites | Gaia DR3 | Lists $G^* = G + 2.5\log(v/20)$ to rank slow events [@mb-lucky-star-predictions] |
| SORA [@mb-sora-code] | Open Python prediction and reduction | SPICE kernels or Horizons queries | Gaia DR2, EDR3 or DR3 through VizieR or LIneA (Laboratório Interinstitucional de e-Astronomia) | Version 0.3.3, default catalogue `gaiadr3_linea` |
| JPL Horizons and SBDB [@sw-horizons-manual] [@mb-sbdb-api] | Ephemerides and covariance | JPL orbit solutions | none | Uncertainties are 3-sigma |
| Euraster (Frappa) [@mb-euraster-2023] | European results 1996 to 2022 | not applicable | not applicable | Domain expired by 2025; observations since 2023 go to SODIS [@mb-sodis] |

The [?jpl-de|JPL planetary ephemeris] enters all of these through the asteroid orbit fit and the Earth's position. French and Souami's planetary predictions use DE440 [@mb-french-souami-2023]. Preston's 2007 orbit fits used DE405 [@mb-preston-update-2007]. None of the sources cited here states which DE version Occult itself uses for asteroid work.

Occult's catalogue is described both as Gaia EDR3 and as Gaia DR3 [@mb-dunham-rasc-2024-mb]. For astrometry the two are the same: Gaia DR3 "neither contains new astrometry nor new photometric calibrations", and its astrometry is the one published as part of EDR3 [@mb-esa-gaia-dr3].

## Sources compared

| Source | Kind | What it gives that the others do not |
|---|---|---|
| Gomes-Júnior et al. 2022 [@mb-gomes-junior-2022-sora] | Method paper | Plane equations, closest-approach formulas, light-time and star-parallax limits, accuracy targets per body |
| SORA code [@mb-sora-code] | Implementation | The actual search radius, three-stage refinement, path and 1-sigma construction, sea-level ellipsoid projection |
| Herald et al. 2020 [@mb-herald-2020] | Data-set paper | Besselian reduction, inverse astrometry steps, single-chord error rules, timing goals, event counts |
| Tanga and Delbo 2007 [@mb-tanga-delbo-2007] | Analysis | Quadrature error model, efficiency factor, pre-Gaia catalogue errors |
| Desmars et al. 2015 and NIMA README [@mb-desmars-2015-nima] [@mb-nima-readme] | Orbit method | Covariance propagation, night-bias weighting, failure of the offset method |
| Ferreira et al. 2022 [@mb-ferreira-2022] | Statistics | Residual levels before and after Gaia EDR3 |
| Gaia FPR 2023 [@mb-gaia-fpr-2023] | Validation | Gaia-only orbits against occultations, 10 mas per year drift |
| Buie et al. 2020 [@mb-buie-2020-arrokoth] | Campaign | Uncertainty history of one TNO, deployment Monte Carlo |
| Preston FAQ and 2007 slides [@mb-preston-faq] [@mb-preston-update-2007] | Practitioner | Occult plot conventions, ground width, Rank, pre-Gaia update workflow |
| Horizons manual and SBDB API [@sw-horizons-manual] [@mb-sbdb-api] | Data service | 3-sigma convention, covariance access |

## What a developer should do

1. Put the fundamental plane on the star direction and compute the body's plane coordinates with SORA's equations 7 to 9, in kilometres, from apparent or astrometric positions used consistently for star and body [@mb-gomes-junior-2022-sora] [@mb-herald-2020].
2. Propagate the Gaia DR3 star with full space motion and its covariance, apply the Cantat-Gaudin and Brandt proper-motion correction for bright stars, and flag RUWE above 1.4 [@mb-gomes-junior-2022-sora].
3. Take the ephemeris from SPICE kernels or Horizons, and its covariance from the SBDB API. Map the covariance to the plane-of-sky ellipse at the event and divide Horizons 3-sigma values by 3 [@mb-sbdb-api] [@sw-horizons-manual]. In SORA, set `error_ra` and `error_dec` explicitly, because they default to zero [@mb-sora-code].
4. Form $\sigma_{\mathrm{path}}$ from the cross-track components of both errors, not from $\max(\sigma_\alpha, \sigma_\delta)$ as SORA's search does. Convert with $0.7253\,D_\circ$ km per milliarcsecond, with $D_\circ$ in astronomical units [@mb-tanga-delbo-2007] [@mb-sora-code].
5. Use a cubic in time for the shadow motion, as Herald does, so that slow events near quadrature stay correct [@mb-herald-2020] [@mb-gomes-junior-2022-sora].
6. Project to the ground with the observer's height on the ellipsoid. Report the path edges, the 1-sigma lines and the along-track time uncertainty in seconds [@mb-preston-faq].
7. Close the loop. Ingest observed occultation positions with zero bias and a precision of a few milliarcseconds into the orbit fit, as NIMA does [@mb-nima-readme].

Read SORA's paper and `prediction/core.py` first, then Herald et al. 2020 sections 4 and 5, then Desmars et al. 2015 section 3.

## What this changes

The eclipse pipeline's Besselian layer carries over with three changes. The shadow axis is the star direction and is fixed for the event. The shadow radius is the body's radius with no cone angle. The ephemeris uncertainty becomes a first-class output, because for occultations the 1-sigma band is part of the product, not a footnote. The pipeline needs a star-catalogue stage with space-motion propagation and an orbit-covariance stage, neither of which a solar-eclipse pipeline has.

## Open questions

- Obtain Occult's help file `Occult.chm` and read the asteroid-prediction topics, to record the Besselian element definitions, the DE version and how the uncertainty ellipse is built from orbit and star errors [@sw-occult4].
- Obtain Assafin et al. 2010 (A&A 515, A32) for the original closest-approach and offset method that SORA's paper cites.
- Obtain Herald's Journal for Occultation Astronomy articles on the Gaia-era prediction process to replace the 2007 Preston slides as the description of current IOTA updates [@mb-preston-update-2007].
- Obtain the orbit files of the Gaia Focused Product Release to measure the path uncertainty for main-belt events from those orbits [@mb-gaia-fpr-2023].
- Run SORA's `prediction` and Occult on the same event and star, and compare the closest-approach time, the central line and the 1-sigma lines.
