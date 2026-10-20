---
title: Solar eclipse error budget
description: Rank solar eclipse prediction inputs by their effects on contact times and ground paths, and distinguish numerical checks from physical uncertainty.
order: 4
status: working
updated: 2026-10-18
seo_title: Solar Eclipse Prediction Accuracy: Timing and Path Errors
---

::: summary
- **The sources compared here quantify different error components.** Quaglia and colleagues analyse ephemeris, Earth orientation, topography and [solar radius](../10-raw/20-solar-eclipses-and-transits/06-solar-radius/solar-radius-values.md). [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak) describes limb and [ΔT](../10-raw/10-shared/07-earth-and-time/delta-t-and-earth-rotation.md) effects. Wright and Young specify terrain treatment. Their shifts and bounds are not all independent standard uncertainties [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-wright-young-2024].
- **Omitted terrain and limb can move limits by kilometres.** Solar-radius choices move the cited modern limits by hundreds of metres. Other omitted corrections and inconsistent conventions can also exceed 200 m [@val-svs-4517] [@loc-nasa-limb-help] [@sun-quaglia-2021].
- **Mixed reduction levels and incorrect time conventions can cause much larger errors.** The quoted inconsistent Sun/Moon reduction example reaches 38 km. A 69 s Earth-rotation mistake is about 32 km at the equator [@earth-es1992] [@moon-skyfield-positions].
- **The cited solar-radius component is about 100 m for ± 0.05 arcseconds.** It is separate from the reported 60 to 130 m inter-implementation spread. Neither is a universal prediction-accuracy floor [@val-quaglia-2021].
- **Huber's future ΔT model grows with lead time.** Its values are about 0.05 s at one year, 4.6 s at twenty and 52 s at a hundred. The separate historical rule $\sigma=0.8t^2$ applies to 1000 BCE through 1200 CE, with $t$ in centuries from 1820 [@earth-nasa-deltat-uncertainty] [@val-gsfc-uncertainty].
:::

This budget covers solar eclipses. The dominant input of each other event,
and the accuracy it allows, is in
[Extending the pipeline to other events](other-events.md).

## The ranked budget

"Mid-path" is a site near the [central line](../10-raw/20-solar-eclipses-and-transits/03-global-circumstances/path-and-limits.md) of a 2017-class eclipse with a
shadow speed near 1 km/s. "Edge" is within a few hundred metres of a limit.
Conversions used: 1″ at the Moon's mean distance is 1.86 km on the ground;
1 s of ΔT is 15.041″ of longitude, 465 m at the equator and 356 m at 40°; the
relative Moon-Sun motion of 0.364″/s gives 2.7 s of contact time per
arcsecond [@val-5mcse-tp2009] [@moon-espenak-2001-bulletin].

| Rank | Term | Mid-path contact time | Edge position or duration | Included by |
|---|---|---|---|---|
| 1 | Geometric Sun with apparent Moon | 55 s | 38 km | Everyone avoids it; test for it [@earth-es1992] |
| 2 | TT used as UT | Contact-time effect depends on geometry; 69 s of rotation is not a uniform contact shift | 32 km at the equator | Everyone avoids it; test for it [@moon-eclipsewise-2024] |
| 3 | Sphere instead of ellipsoid | tens of s | up to 21 km | Everyone [@earth-es1961] |
| 4 | Terrain omitted | seconds where the Sun's azimuth lies along the track | $h\cot a$; up to 3 km in the 2017 western states | [SVS](../10-raw/20-solar-eclipses-and-transits/11-svs-wright/_index.md) only, for the path; single-site altitude in Jubier, [Occult](../10-raw/10-shared/09-software-and-repos/commercial-and-institutional-tools.md), [Swiss Ephemeris](https://www.astro.com/swisseph/) [@val-svs-4517] [@earth-espenak-tp2001] |
| 5 | Lunar limb omitted | 1 to 3 s, up to 15 s in extreme geometry | 1 to 3 km per limit; 33 s of duration at Stephenville 2024 | SVS, Jubier, Occult, Irwin, Photo Ephemeris simulator [@loc-nasa-limb-help] [@val-besselian-maps-accuracy] |
| 6 | Solar radius convention | 1.8 s of central duration for 959.63 to 960.00 arcseconds in the cited case | About 600 m per limit for 959.63 to 959.95 arcseconds. The Vale comparison for 959.63 to 960.00 arcseconds reduces duration by 19.3 s. Stephenville is a cross-program comparison, not an isolated radius effect | Irwin uses 959.95″, Photo Ephemeris in its bead simulator only; everyone else 959.63″ or 696,000 km [@sun-quaglia-2021] [@sun-wright-young-2024] |
| 7 | Lunar radius $k$, umbral, if the IAU value is used | about 4 s of duration | 1.4 km per limit | Espenak, [Stellarium](https://stellarium.org/), Jubier use 0.272281; [USNO](https://en.wikipedia.org/wiki/United_States_Naval_Observatory) and Astronomy Engine use a mean radius; the Swiss Ephemeris uses 1738.15 km globally but scales the lunar radius by 0.99916, which is 0.272281, for C2 and C3 [@bes-nasa-radius] [@val-gsfc-sepredictions] |
| 8 | ΔT prediction error, realised in 2024 | 1.4 to 2.3 s | 500 to 800 m east-west at 40° | All; the miss depends on when the prediction was frozen [@earth-usno-deltat-data] [@val-eclipsewise-2024-circ] |
| 9 | [Centre of figure](../10-raw/10-shared/08-lunar-and-solar-model/lunar-figure-and-libration.md) against centre of mass, smooth-Moon products | up to 1.4 s | 0.5 to 1 km | Absorbed by any DEM-based profile; not applied by USNO [@moon-jones-2025] [@val-usno-2024] |
| 10 | Watts-era limb data | 0.5 s | 600 to 750 m systematic at some position angles | Superseded by [Kaguya](https://en.wikipedia.org/wiki/SELENE) and [LOLA](https://lola.gsfc.nasa.gov/) [@limb-morrison-appleby-1981] [@val-tp2001-bulletin] |
| 11 | [Geoid](../10-raw/10-shared/07-earth-and-time/earth-figure-and-terrain.md) against ellipsoid height | under 1 s | $N\cot a$, up to 170 m at a 30° Sun | SVS ([EGM96](https://en.wikipedia.org/wiki/Earth_Gravitational_Model)); nobody else documents it [@earth-svs-4515] |
| 12 | Implementation spread on identical inputs | 2 to 4 s at Vale 2017 | 0.03″ to 0.07″ of radius, 60 to 130 m | Occult, Solar Eclipse Maestro, Irwin [@val-quaglia-2021] |
| 13 | Solar radius residual, ± 0.05″ | 0.1 s | 100 m band | Radius component for the cited geometry [@sun-quaglia-2021] |
| 14 | Limb sampling coarser than 18,000 elements | 0.25 s for 0.2° bins | part of the implementation spread | SVS at 0.02° [@limb-wright-young-2024] [@loc-be-2013-contacts] |
| 15 | Refraction, Sun above 5° | No validated general contact-time bound in the cited sources | Common angular limb remapping preserves contact; physical ray geometry is a separate model | Nominal geometric contacts omit refraction [@earth-espenak-tp2001] [@sun-quaglia-2021] |
| 16 | Refraction near the horizon | No validated contact-time bound in this corpus | Changes displayed altitude and visibility; anomalous conditions need separate treatment | State the atmospheric and horizon model [@earth-es1992] [@earth-espenak-tp2001] |
| 17 | Sidereal time inconsistency, mean against apparent | up to 1.1 s | up to 0.5 km | Consistent in every predictor documented [@earth-circ179] |
| 18 | UT1 against UTC | up to 0.9 s | up to 0.42 km | UT1 printed by Espenak, SVS, Swiss Ephemeris [@earth-iers-bulletin-a] |
| 19 | Moon [light-time](../10-raw/10-shared/07-earth-and-time/refraction-light-time-and-frames.md) omitted | No bound follows from geocentric lunar speed alone | A reception calculation retards the barycentric target. Observer aberration is separate and can partly cancel common orbital motion | Use one consistent reduction chain [@moon-spice-spkezr] [@moon-folkner-2014] |
| 20 | Ephemeris, DE421 to [DE440](../10-raw/10-shared/08-lunar-and-solar-model/ephemerides.md) | Depends on the projected position difference and radial rate | This pair's displacement is not quantified by the cited Park paper. Its range residuals do not certify a three-dimensional position bound | Pin the releases, epoch and vector comparison [@moon-park-2021] |
| 21 | Ephemeris, DE403 to DE421, at 2020 | 0.02 s | 16 m | Irrelevant [@moon-williams-2008] |
| 22 | ELP-2000/82 truncated as in the Canon | 0.02 s | 10 m | Irrelevant for paths [@moon-espenak-meeus-canon] |
| 23 | Polar motion | 0 | about 10 m | [SPICE](https://naif.jpl.nasa.gov/naif/) kernels include it; nobody documents it [@earth-iers-bulletin-a] |
| 24 | Nutation model, 1980 against 2000A | 0 | under 20 m | Irrelevant [@earth-circ179] |
| 25 | TT against TDB | 1.7 ms | 2 m | Irrelevant [@earth-circ179] |
| 26 | Observer position, consumer GPS | none on time | ± 100 m | The observer's problem [@val-tp2001-bulletin] |
| 27 | Observer clock, visual timing | "a couple of seconds" | same | The observer's problem [@val-besselian-maps-accuracy] |

![Mixed reduction and time conventions produce errors of tens of kilometres. Terrain and limb omission reach kilometres, and the cited 0.32 arcsecond solar-radius difference moves a limit by about 600 m. Several other omitted corrections also exceed 200 m. The ephemeris bars are comparisons between releases, not bounds against truth. Each bar is a diagnostic scale from the table above [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-wright-young-2024] [@earth-es1992] [@sun-quaglia-2021].](img/error-budget.svg)

## ΔT by lead time and epoch

The a priori uncertainty of ΔT, from Huber's model as used by NASA for the
future and from Morrison and Stephenson's $\sigma = 0.8t^2$ rule with $t$ in
centuries from 1820 for 1000 BCE through 1200 CE. The other historical rows
use NASA's epoch-specific estimates [@earth-nasa-deltat-uncertainty]
[@val-gsfc-uncertainty].

| Lead time or year | $\sigma(\Delta T)$ | Longitude at 40° |
|---|---|---|
| 1 year ahead | 0.05 s | 18 m |
| 5 years ahead | 0.6 s | 0.2 km |
| 20 years ahead | 4.6 s | 1.6 km |
| 100 years ahead | 52 s | 18 km |
| Year 1900 | 0.1 s | 36 m |
| Year 1700 | 5 s | 1.8 km |
| Year 1000 | 54 s | 19 km |
| Year 0 | 265 s | 94 km |
| Year −1000 | 636 s | 226 km |
| Year 3000 | 1885 s | 670 km |

Successive historical analyses differ by more than these sigmas: the 1986 and
1997 Stephenson curves differ by 1294 s at AD 300. A past-eclipse product must
draw the gore, as the Canon does for every year before 1 and after 2300
[@val-gsfc-deltat-hist] [@cat-espenak-meeus-2006-canon].

## The two modes

The budget separates cleanly into what a product can control and what it
chooses.

**Almanac mode.** Smooth Moon with $k_2 = 0.272281$ and $k_1 = 0.2724880$ to
match the NASA GSFC tables or $0.2725076$ to match EclipseWise and the
bulletins,
$s_0 = 959.63″$, sea level, the ΔT printed with the table. The result matches
NASA or EclipseWise to 1 km at the limits and 0.1 s at a site, and carries
their modelling choices. Omitted limb and terrain and a different radius
can move a limit by kilometres. The table does not establish a combined
2 km standard uncertainty for those omissions. This is the
mode for catalogues, for reproducing published tables, and for regression
tests.

**Edge mode.** LOLA profile at 18,000 elements, terrain with geoid,
$s_0 = 959.95″ ± 0.05″$, ΔT refreshed to the latest USNO or [IERS](https://www.iers.org/) value. The
cited comparisons give a radius component near 100 m and implementation
spread of 60 to 130 m, with 2 to 4 s duration differences at the Vale site.
These are case-specific scales, not a calibrated combined uncertainty. Dunham's practical margin of 2 km of
[?umbral-depth] covers the instrumental sensitivity to faint beads that no
computation removes [@val-dunham-iota-2024].

The two modes differ by design and must not share a file. A map that draws an
almanac-mode limit next to an edge-mode duration misleads by 600 m.

## How to report it

Correct known biases before estimating uncertainty. Keep unresolved model
choices and implementation discrepancies separate from quantified input uncertainties.
Express each input's standard uncertainty in the measurement model, rather
than treating an omitted correction's full size as its standard deviation.
Quadrature requires justified independence. Correlated inputs require
covariance terms [@report-jcgm-gum-2008].

For $y=f(x_1,\ldots,x_N)$, JCGM 100:2008 equation (13) gives

$$u_c^2(y)=\sum_{i=1}^{N}\left(\frac{\partial f}{\partial x_i}\right)^2u^2(x_i)
+2\sum_{i=1}^{N-1}\sum_{j=i+1}^{N}\frac{\partial f}{\partial x_i}\frac{\partial f}{\partial x_j}u(x_i,x_j).$$

Here $u(x_i)$ is the standard uncertainty of input $x_i$, and $u(x_i,x_j)$
is their covariance. The derivatives convert each input's units to the
output's units. Apply this separately to each contact time, duration or path
coordinate. If distributions and correlations are not established, report
scenario ranges rather than assigning a coverage probability
[@report-jcgm-gum-2008].

Draw limits for the adopted solar radius and its stated alternatives. Treat
the cited 100 m radius effect as one component for that geometry. Show
umbral depth near a limit, and state the detection convention. Propagate
ΔT uncertainty for historical and distant-future products. Store the
configuration with every result [@sun-quaglia-2021] [@val-quaglia-2021].
