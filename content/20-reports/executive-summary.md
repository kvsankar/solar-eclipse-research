---
title: Executive summary
description: One algorithm, four constants that decide the edges, one published state-of-the-art method, and no open-source implementation of it.
order: 1
status: working
updated: 2026-09-16
---

::: summary
- **Every published eclipse product derives from one algorithm**, Bessel's fundamental-plane method as set out in the 1961 Explanatory Supplement and restated in 1992. The algebra is settled and quoted in full in the raw notes. What separates predictors is their constants and data, not their mathematics [@bes-es1961] [@glob-es1992].
- **Three inputs decide the edge of the path**: the solar radius, the lunar limb profile, and the observer's terrain height. Each is worth 0.6 to 3 km at a path limit and seconds to tens of seconds of totality there. Everything else is below 100 m once ΔT is refreshed and the umbral $k$ or a limb profile is used; the ephemeris is under 1 m [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-svs-4517].
- **The state of the art is published and reproducible in principle.** Wright and Young 2024 describe the NASA SVS raster method: every map pixel is lifted to terrain height and tested against an 18,000-element lunar limb profile built from LRO and SELENE topography. The paper is open access. The code is not [@svs-wright-young-2024].
- **The solar radius is the unresolved constant.** Almost every predictor uses Auwers' 1891 value of 959.63 arcseconds. Four eclipse campaigns since 2010 measure 959.95 to 960.01 arcseconds. The difference moves each limit by about 600 m and, at one 2024 edge site, was the last 11 s of a 65 s smooth-Moon prediction that observation cut to 13.7 s [@sun-quaglia-2021] [@val-besselian-maps-accuracy].
- **Enumeration and the ephemeris are solved problems.** Meeus's approximate method, implemented from its quoted constants, finds all 221 eclipses of 1951 to 2050 with no type errors, and JPL DE440 places the Moon to about a metre. Effort belongs in ΔT, the limb and the radius [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii] [@moon-park-2021].
- **No open-source code computes a limb-corrected path edge.** Stellarium is the complete open Besselian implementation with a smooth Moon, and NASA's GPL JavaScript is the reference for local circumstances. A limb-and-terrain pipeline has to be written [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js].
:::

## The question and the answer

The question is what a developer needs to know to compute every solar
eclipse product, from the list of eclipses in a period to the second at which
totality begins at one place, at the depth of NASA SVS's 2024 work. The answer
is a pipeline of nine stages, given in [pipeline design](pipeline-design.md),
and a short list of decisions that matter more than the rest. The decisions
follow.

## One algorithm, many constants

Bessel's method projects the Moon's shadow onto a plane through the Earth's
centre perpendicular to the shadow axis, the [?fundamental-plane]. Eight
[?besselian-elements] describe the shadow there. The central line is a square
root, the path limits are a root-find in one angle, the local contact times at
a site are the roots of one equation in time. The 1961 Explanatory Supplement
gives every formula with worked examples, the 1992 edition restates it in
vector form and recommends direct root-finding over the auxiliary angle, and
Stellarium's source implements it with equation numbers cited
[@bes-es1961] [@glob-es1992] [@sw-stellarium-sec-cpp].

The predictors differ because they choose differently on four numbers.

| Constant | Values in use | Effect of the difference |
|---|---|---|
| Solar radius $s_0$ | 959.63″ (Auwers 1891, NASA, Espenak, Jubier, Occult); 696,000 km (SVS, USNO, Stellarium); 959.95″ (Irwin; Photo Ephemeris in its bead simulator only); 695,700 km IAU nominal (astropy, unsuitable) | 0.32″ is about 600 m per limit and 1.6 to 1.8 s of central-line duration [@sun-quaglia-2021] [@sun-wright-young-2024] |
| Lunar radius ratio $k$ | 0.2725076 (IAU 1982) for penumbral contacts; 0.272281 for umbral contacts; 0.2724880 in the Five Millennium Canon | The umbral pair differs by 1.4 km of lunar radius, about 4 s of totality and 1.4 km per limit [@bes-nasa-radius] [@val-gsfc-sepredictions] |
| ΔT | 2024: NASA 70.6 s, EclipseWise 71.5 s, Jubier 69.1 s, measured 69.20 s | 1 s is 465 cos φ metres of longitude; the 2024 misses were 0.5 to 0.8 km [@earth-usno-deltat-data] [@val-gsfc-2024-google] [@sw-jubier-2024-map] |
| Limb datum | Mean sphere with $k$; Watts charts; Kaguya LALT; LRO LOLA and SLDEM2015 on a 1737.4 km centre-of-mass sphere | Omitting the profile costs 1 to 3 km per limit and 1 to 3 s per contact; LOLA brings contacts to 0.2 to 0.3 s [@loc-nasa-limb-help] [@limb-wright-young-2024] |

The ephemeris is not on the list. Every JPL ephemeris since DE421 puts the
Moon within a few metres of truth in the present century, which is under 10 ms
of contact time [@moon-park-2021] [@moon-williams-2013].

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
places. These files are the only public ground truth for a limb-corrected
product [@svs-4515-2017-path] [@svs-2024-shapefiles-zip] [@svs-cities-2024-json].

## What the observations say

Every quantitative test of a prediction has been made at a path limit,
because the sensitivity there is about ten times that of the central line [@sun-quaglia-2021].
At Stephenville, Texas, on 2024 April 8, an observer timed 13.7 s of totality.
Six public predictions for the same point ranged from 12.9 s to 65 s. The
smooth-Moon products with the standard radius were 40 to 50 s too long,
Jubier's limb-corrected value was 24.5 s, and Irwin's true-limb model with 959.95″ was
within a second [@val-besselian-maps-accuracy]. At Vale, Oregon, in 2017,
raising the radius from 959.63″ to 960.00″ changed the predicted duration at
a site 1.2 km inside the southern limit, as drawn with 959.63″, from 32.6 s
to 13.3 s [@val-quaglia-2021]. IOTA, which for decades reported a varying solar radius
from bead timings, now attributes that scatter to observational error and
recommends standing at least 2 km inside Jubier's limb-corrected limit
[@val-dunham-iota-2024].

## What exists to build on

Open code covers the smooth-Moon problem completely and the limb problem not
at all. Stellarium's `SolarEclipseComputer.cpp` computes elements, every
classic curve, KML and PNG output, with Explanatory Supplement equation
numbers in the comments. NASA's `program.js` is the 1961 local-circumstances
method in 1,200 lines of GPL JavaScript. The Swiss Ephemeris and Astronomy
Engine find eclipses geometrically without elements and give the central
point and local contacts. Skyfield, astropy, PyEphem, libnova, NOVAS and SOFA
ship no solar-eclipse routine. Of thirty public GitHub repositories, one
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
2. **The solar radius is a parameter with an uncertainty**, and every limit
   is drawn as a band. With ± 0.05″ the band is about ± 0.1 km
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

Only two results here are reproduced independently: Meeus's enumeration
series and Kluepfel's Saros formula, each implemented from the quoted
constants and checked against the NASA ASCII catalogue
[@cat-meeus-1991-aa] [@cat-vangent-cycles]. Every Besselian, limb and terrain
number is quoted from its source rather than recomputed. Meeus's *Elements of
Solar Eclipses 1951-2200* and chapter 11 of the 2013 Explanatory Supplement
are cited only through implementations that transcribe them. Occult's help
file, Solar Eclipse Maestro's statement of its ephemeris and ΔT,
timeanddate's ephemeris and ΔT source, and the SVS 2024 ΔT are all
unavailable. These are the first entries in
[open questions](open-questions.md).
