---
title: Executive summary
description: The main findings on eclipse prediction methods, constants, lunar limb and terrain modelling, software availability and validation evidence.
order: 1
status: working
updated: 2026-09-30
seo_title: Solar Eclipse Calculation: Research Findings for Developers
---

::: summary
- **The classical almanac route uses Besselian elements.** Direct topocentric geometry and raster limb tests are alternatives. Comparisons must match both the method and its inputs [@bes-es1961] [@bes-quaglia-2021] [@svs-wright-young-2024].
- **Solar radius, lunar limb and terrain dominate several modern path-edge comparisons.** Omitted or inconsistent corrections elsewhere can still exceed 100 m. A numerical implementation check is separate from a physical uncertainty estimate [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-svs-4517].
- **Wright and Young 2024 specify NASA SVS's raster method.** Each map pixel is placed at terrain height and tested against an 18,000-element lunar limb profile built from LRO and Kaguya (SELENE) topography. The paper is open access, and the released maps provide reference products [@svs-wright-young-2024].
- **The solar radius is not settled by a single convention.** Recent flash-spectrum and light-curve analyses infer 959.95 to 960.01 arcseconds. Timing-based reductions also depend on the limb and detection model. Cross-program duration differences do not isolate the solar radius alone [@sun-quaglia-2021] [@sun-lamy-2015] [@val-guhl-2023].
- **Catalogue enumeration has a reproduced reference comparison.** The quoted Meeus series finds all 221 NASA eclipses for 1951 to 2050 with matching types. Lunar laser-ranging residuals constrain ephemerides, but they do not certify every position component to a centimetre [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii] [@moon-park-2021].
- **Open code covers many smooth-Moon products.** The surveyed repositories include single-eclipse limb and bead work, but no general derivation of limb-corrected path limits [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-repo-eclipse-2026-rojas].
:::

## The question and the answer

The question is what a developer needs to know to compute every solar
eclipse product, from the list of eclipses in a period to the second at which
totality begins at one place, at the depth of NASA SVS's 2024 work. The answer
is a pipeline of nine stages, given in [pipeline design](pipeline-design.md),
and a short list of decisions that matter more than the rest. The decisions
follow.

## Shared geometry, different methods and inputs

Bessel's method projects the Moon's shadow onto a plane through the Earth's
centre perpendicular to the shadow axis, the [?fundamental-plane]. Eight
[?besselian-elements] describe the shadow there. The central line is a square
root, the path limits are a root-find in one angle, the local contact times at
a site are the roots of one equation in time. The 1961 Explanatory Supplement
gives every formula with worked examples, the 1992 edition restates it in
vector form and recommends direct root-finding over the auxiliary angle, and
Stellarium's source implements it with equation numbers cited
[@bes-es1961] [@glob-es1992] [@sw-stellarium-sec-cpp].

Four input choices help explain the differences between the surveyed predictors.
Direct methods and raster tests also differ from the classical circular-shadow
algorithm [@val-quaglia-2021] [@svs-wright-young-2024].

| Constant | Values in use | Effect of the difference |
|---|---|---|
| Solar radius, angular $s_0$ or linear $R_\odot$ | 959.63″ (Auwers 1891, NASA, Espenak, Jubier, Occult); 696,000 km (SVS, USNO, Stellarium); 959.95″ (Irwin; Photo Ephemeris in its bead simulator only); 695,700 km IAU nominal (astropy, unsuitable) | 0.32″ is about 600 m per limit and 1.6 to 1.8 s of central-line duration [@sun-quaglia-2021] [@sun-wright-young-2024] |
| Lunar radius ratio $k$ | 0.2725076 (IAU 1982) for penumbral contacts; 0.272281 for umbral contacts; 0.2724880 in the Five Millennium Canon | The umbral pair differs by 1.4 km of lunar radius, about 4 s of totality and 1.4 km per limit [@bes-nasa-radius] [@val-gsfc-sepredictions] |
| ΔT | 2024: NASA 70.6 s, EclipseWise 71.5 s, Jubier 69.1 s, measured 69.20 s | 1 s is 465 cos φ metres of longitude; the 2024 misses were 0.5 to 0.8 km [@earth-usno-deltat-data] [@val-gsfc-2024-google] [@sw-jubier-2024-map] |
| Limb datum | Mean sphere with $k$; Watts charts; Kaguya LALT; LRO LOLA and SLDEM2015 on a 1737.4 km centre-of-mass sphere | Omitting the profile costs 1 to 3 km per limit and 1 to 3 s per contact; LOLA brings contacts to 0.2 to 0.3 s [@loc-nasa-limb-help] [@limb-wright-young-2024] |

The cited modern ephemeris comparisons are smaller than the dominant
uncorrected path-edge terms. Park and colleagues report lunar laser-ranging
residuals near a centimetre for recent observations. A fitted range residual
is not a bound on every three-dimensional position component. Differences
between ephemerides are comparisons, not errors against truth
[@moon-park-2021] [@moon-williams-2013] [@val-quaglia-2021].

## The reference method

Wright and Young's raster method replaces the circular-shadow assumption with
a per-observer test. For each map pixel at each time step, the pixel is placed
on the WGS84 ellipsoid at its SRTM height corrected by the EGM96 geoid. The
Moon is replaced by a [?limb-profile] $L$ of 18,000 radii at 0.02 degree
steps, built by rotating the SLDEM2015 and polar LDEM point clouds into the
observer's line of sight using the [?topocentric-libration] and keeping the
largest angular radius in each bin. The eclipse is total at that pixel if the
profile encloses the Sun's disc, tested as
$\rho = a^2 + \delta^2 - 2a\delta\cos(\theta - \phi)$ against 1 for every
element. The path limits, central line, duration contours and obscuration
contours are all extracted from the resulting raster stack, and the umbra is a
polygon with as many sides as there are limb valleys on its edge, 49 at one
2017 instant [@svs-wright-young-2024].

The constants SVS states are DE421 (DE440 in the paper's appendix), Earth
radius 6378.137 km with WGS84 flattening, a 1737.4 km lunar datum, and a Sun of
696,000 km. The 2017 run used ΔT = 68.917 s from a SPICE Earth-orientation
kernel. The released shapefiles hold umbra polygons at 1 s intervals with
libration and distance attributes, and a JSON of contact times for 32,174 US
places. These files are public reference products for the raster method.
Observed contacts and other limb-corrected predictions provide independent
validation evidence [@svs-4515-2017-path] [@svs-2024-shapefiles-zip] [@svs-cities-2024-json].

## What the observations say

Near-limit observations provide especially sensitive solar-radius tests.
Published campaigns also include central-line observations
[@sun-quaglia-2021] [@sun-lamy-2015].
At Stephenville, Texas, on 2024 April 8, an observer timed 13.7 s of totality.
Six public predictions for the same point ranged from 12.9 s to 65 s. The
smooth-Moon products with the standard radius were 40 to 50 s too long,
Jubier's limb-corrected value was 24.5 s, and Irwin's true-limb model with 959.95 arcseconds was
within a second. This cross-program comparison does not isolate the radius
effect from other input and solver differences [@val-besselian-maps-accuracy]. At Vale, Oregon, in 2017,
raising the radius from 959.63″ to 960.00″ changed the predicted duration at
a site 1.2 km inside the southern limit, as drawn with 959.63″, from 32.6 s
to 13.3 s [@val-quaglia-2021]. IOTA, which for decades reported a varying solar radius
from bead timings, now attributes that scatter to observational error and
recommends standing at least 2 km inside Jubier's limb-corrected limit
[@val-dunham-iota-2024].

## What exists to build on

The surveyed open code covers many smooth-Moon products and includes some
limb work for individual eclipses. Stellarium's `SolarEclipseComputer.cpp` computes elements, every
classic curve, KML and PNG output, with Explanatory Supplement equation
numbers in the comments. NASA's `program.js` is the 1961 local-circumstances
method in 1,200 lines of GPL JavaScript. The Swiss Ephemeris and Astronomy
Engine find eclipses geometrically without elements and give the central
point and local contacts. The surveyed versions of Skyfield, astropy, PyEphem, libnova, NOVAS and SOFA
do not provide a complete solar-contact routine. SunPy supplies obscuration
from smooth apparent discs [@loc-sunpy-eclipse-amount]. Of thirty public GitHub repositories, one
builds Baily's beads from a LOLA grid for a single eclipse, and none derives
a path limit from a limb profile [@sw-stellarium-sec-cpp]
[@sw-nasa-jsex-program-js] [@sw-swisseph-swecl] [@sw-repo-eclipse-2026-rojas].

The data is all public: NASA's CSV of 11,898 polynomial element sets, the SVS
shapefiles, LOLA LDEM grids from 4 to 1024 pixels per degree, SLDEM2015, SRTM
and Copernicus DEMs, JPL DE440 with its lunar orientation kernel, and the USNO
and IERS ΔT files [@cat-nasa-besselian-csv] [@sw-svs-5073]
[@limb-lola-ldem128-label] [@moon-naif-summaries] [@earth-usno-deltat-data].

## What to build

The [pipeline design](pipeline-design.md) has the detail. The decisions it
rests on:

1. **Two product modes, never mixed in one file.** An almanac-reproduction
   mode with $s_0 = 959.63″$, the two $k$ values, a smooth Moon and sea level,
   which must match NASA's tables to 1 km and 0.1 s. An edge mode with a
   LOLA profile, terrain, and $s_0$ near 959.95″ with a stated uncertainty,
   which must match the SVS polygons and the Stephenville and Vale records.
2. **The solar radius is a parameter with an uncertainty**, and each limit
   is evaluated at the adopted radius and its alternatives. The cited
   ± 0.05 arcsecond radius component gives about ± 0.1 km in that geometry
   [@sun-quaglia-2021].
3. **ΔT is metadata**, applied once in the hour angle, refreshed from USNO or
   IERS until the eclipse, and printed on every product with its date
   [@earth-es1992] [@earth-usno-deltat-preds].
4. **The Moon is two objects**: a centre of mass from DE440 and a figure from
   LOLA oriented by the DE440 Euler angles in the mean-Earth frame. The
   constant $k$ survives only as the datum radius and as the fallback for
   profile-free products [@moon-naif-moon-fk-de440] [@moon-archinal-2011].
5. **Validation is a five-level test suite** with pinned constants: the 1961
   worked examples, NASA's tables, the Lusaka limb example, the Vale and
   Stephenville edge records, and the IOTA bead tables
   [@val-es1961] [@val-tp2001-bulletin] [@val-guhl-tegtmeier-2018].

## The limits of this statement

Meeus's enumeration series and Kluepfel's Saros formula have comparisons
against the NASA ASCII catalogue [@cat-meeus-1991-aa] [@cat-vangent-cycles].
The end-to-end limb-and-terrain pipeline still needs validation against its
named fixtures. Table reproduction and numerical consistency do not by
themselves establish physical accuracy [@val-quaglia-2021].
Meeus's *Elements of Solar Eclipses 1951-2200* and chapter 11 of the 2013
Explanatory Supplement are documented here through implementations that
transcribe them. Remaining input-provenance questions concern Occult's
installed help, Solar Eclipse Maestro's ephemeris and ΔT, timeanddate's
ephemeris and ΔT source, and the exact SVS 2024 run
[@loc-meeus-elements-1989] [@bes-usno-expsupp] [@sw-occult4]
[@sw-timeanddate-accuracy] [@svs-wright-young-2024].
[Open questions](open-questions.md) names the artefacts that would resolve
these uncertainties.
