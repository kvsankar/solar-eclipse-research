---
title: Open-source libraries
description: What Stellarium, Swiss Ephemeris, Astronomy Engine, Skyfield, PyEphem, libnova, NOVAS, SOFA, astropy, sunpy, SPICE, Horizons and the Meeus ports provide toward solar eclipse computation, with the constants and methods read from their code.
order: 2
status: working
updated: 2026-09-15
tags: [software, stellarium, swisseph, skyfield, spice, astronomy-engine, meeus]
---

::: summary
- **Stellarium is the most complete open Besselian implementation.** `SolarEclipseComputer.cpp` computes elements from its own Sun and Moon positions with its constants `k` at 0.2725076 and `s` at 0.272281, solar radius 696,000 km, and cites Explanatory Supplement equations (11.56, 11.60, 11.78, 11.81) for limits, outlines and rise-set curves. It exports KML and PNG maps. No limb profile, no terrain.
- **Swiss Ephemeris computes eclipses geometrically**, not from Besselian elements. `eclipse_where()` follows Montenbruck with a lunar diameter of 3476.3 km, a solar diameter of 1,392,000 km and Earth radius 6378.14 km, claims better than 100 m on the central line, and states that the umbral and penumbral limits are not implemented. Local contacts C2 and C3 use an empirical factor `rmoon *= 0.99916`.
- **Astronomy Engine**, MIT, in five languages, finds eclipses by intersecting the shadow axis with a dilated spherical Earth (Montenbruck and Pfleger p. 184) using $R_\odot = 695{,}700$ km, mean lunar radius 1737.4 km and flattening 0.996647180302104. It returns obscuration and contact times per observer but no path limits.
- **Skyfield has lunar eclipses only.** Two open issues and one open pull request (2025) propose a geometric solar routine. PyEphem, libnova, NOVAS and SOFA provide no eclipse functions. astropy has none. sunpy provides `eclipse_amount()` with $k$ selectable between 0.2725076 and 0.272281.
- **SPICE `gfoclt_c` finds Sun-Moon occultation intervals** for an Earth-centre observer with ellipsoid or DSK shapes, and its Example 1 is exactly a solar eclipse search. It gives intervals, not contact geometry at a surface point.
- **Meeus chapter 54 ports** (astronomia, soniakeys/meeus, Starainrt/astro, astronomy-bundle PHP) give global circumstances and, in the Go and PHP cases, local circumstances from VSOP87 and ELP2000.
:::

**The question.** Which general-purpose astronomy libraries compute anything toward solar eclipses, by what method, with what constants, and where does each stop?

## Stellarium

**Where the code lives.** `src/core/SolarEclipseComputer.cpp`, 2,183 lines at commit 69888f4 of 2026-09-14, and its header, with the user interface in `src/gui/AstroCalcDialog.cpp` [@sw-stellarium-sec-cpp] [@sw-stellarium-sec-hpp] [@sw-stellarium-astrocalc]. Release v1.0, in 2022, "Added capability to create KML map of solar eclipses in AstroCalc tool" and "Added contact times of global solar eclipse in AstroCalc tool" [@sw-stellarium-v1]. Release v0.22.2 already listed "Improvements in AstroCalc: graphs, eclipses, transits" [@sw-stellarium-v022]. Release v24.2 moved "solar eclipse computations out from Planet.cpp" and from `AstroCalcDialog` into the core and "Added export of an equirectangular raster eclipse map" [@sw-stellarium-v242].

**Besselian elements.** `calcSolarEclipseBessel()` cites "Explanatory Supplement to the Astronomical Ephemeris and the American Ephemeris and Nautical Almanac (1961)". It takes geocentric equatorial Sun and Moon positions with topocentric mode disabled, the Moon's distance in Earth radii, and the Greenwich apparent sidereal time [@sw-stellarium-sec-cpp]. With $b = r_{Moon}/r_{ss}$ where $r_{ss}$ is the Sun's distance in Earth radii ($r_{ss} = d_{AU}\times 23454.7925$ from 149597870.8/6378.1366), the shadow-axis direction is

$$a = \alpha_\odot - \frac{b\cos\delta_{M}\,(\alpha_M - \alpha_\odot)}{(1-b)\cos\delta_\odot},\qquad d = \delta_\odot - \frac{b(\delta_M - \delta_\odot)}{1-b}$$

and the elements are $x = r\cos\delta_M\sin(\alpha_M - a)$, $y = r[\cos d\sin\delta_M - \cos\delta_M\sin d\cos(\alpha_M - a)]$, $z = r[\sin\delta_M\sin d + \cos\delta_M\cos d\cos(\alpha_M - a)]$, $\mu = \theta_G - a$ [@sw-stellarium-sec-cpp]. The cone half-angles use `SunEarth = 109.12278` ("696000/6378.1366", IERS Conventions 2003, with the comment that NASA's solar radius of 696,000 km comes from the IAU 1976 value of 959.63 arcsec at 1 au):

$$\sin f_1 = \frac{109.12278 + k}{r_{ss}(1-b)},\quad \sin f_2 = \frac{109.12278 - s}{r_{ss}(1-b)},\quad L_1 = z\tan f_1 + \frac{k}{\cos f_1},\quad L_2 = z\tan f_2 - \frac{s}{\cos f_2}$$

with `const double k = 0.2725076; const double s = 0.272281;` and the comment "Ratio of Moon/Earth's radius 0.2725076 is recommended by IAU for both k & s. s = 0.272281 is used by Fred Espenak/NASA for total eclipse to eliminate extreme cases ... we will use two values (same with NASA), because durations seem to agree with NASA. Source: http://eclipsewise.com/solar/SEhelp/SEradius.html" [@sw-stellarium-sec-cpp]. Element rates are finite differences over ±5 minutes [@sw-stellarium-sec-cpp]. These lines are quoted as the code writes them. They are algebraically the same construction as the one derived in [ephemeris to elements](../01-foundations/ephemeris-to-elements.md), in Stellarium's own notation.

**Global products.** `calcSolarEclipseData()` uses the ellipsoidal fundamental-plane reduction ($\rho_1 = \sqrt{1 - e^2\cos^2 d}$, $\eta_1 = y/\rho_1$, $\rho_2 = \sqrt{1 - e^2\sin^2 d}$) with the flattening taken from Stellarium's Earth model, and returns the central-line point, diameter ratio, Sun altitude, path width, duration and magnitude [@sw-stellarium-sec-cpp]. `getShadowLimitQs()` solves the limit condition from identities (11.56) and (11.60) of the 2013 Explanatory Supplement, and `zetaFromQ()` implements equation (11.81) "restoring the missing dots over a,b,c in the book (cf. eq. (11.78))" [@sw-stellarium-sec-cpp]. `generateEclipseMap()` produces greatest eclipse, P1 and P4, C1 and C2 (central start and end), penumbra limits, umbra outlines and rise-set curves, and `generateKML()` and `generatePNGMap()` write them out [@sw-stellarium-sec-hpp] [@sw-stellarium-sec-cpp]. The AstroCalc dialog exports tables of eclipses, of eclipses visible at the current location, and of contact circumstances, each with the warning that paths "during thousands of years in the past and future are not reliable due to uncertainty in ΔT" [@sw-stellarium-astrocalc].

**ΔT and ephemeris.** The default ΔT algorithm is `EspenakMeeusModified`, described as the Espenak and Meeus solution based on Morrison and Stephenson (2004) with "Values for 2015-2033 ... interpolated from observations and predictions by IERS Rapid Service/Prediction Center" [@sw-stellarium-stelcore]. Stellarium's Sun and Moon positions come from its own ephemeris settings (VSOP87 by default, optional DE430 and DE431 files), so the elements vary with the user's configuration. No limb profile or terrain is used in the eclipse code (no such term appears in `SolarEclipseComputer.cpp`) [@sw-stellarium-sec-cpp]. Licence GPL-2.0 [@sw-stellarium-sec-cpp].

## Swiss Ephemeris

The geometry these routines implement is set out in [ephemeris to elements](../01-foundations/ephemeris-to-elements.md), and the topocentric contact routines in [topocentric method](../04-local-circumstances/topocentric-method.md). This section keeps the constants and the code reading.

**Functions.** `swe_sol_eclipse_when_glob()`, `swe_sol_eclipse_when_loc()`, `swe_sol_eclipse_where()` and `swe_sol_eclipse_how()` return eclipse type flags (`SE_ECL_TOTAL`, `SE_ECL_ANNULAR`, `SE_ECL_PARTIAL`, `SE_ECL_ANNULAR_TOTAL`, `SE_ECL_CENTRAL`, `SE_ECL_NONCENTRAL`), times of maximum and contacts, magnitude, obscuration, the diameter ratio, core-shadow diameter in km, Sun azimuth and altitude, and Saros numbers [@sw-swisseph-progdoc]. The documentation states: "The northern and southern limits of the umbra and penumbra are not implemented yet" [@sw-swisseph-progdoc].

**Constants.** `swecl.c` defines `DSUN (1392000000.0 / AUNIT)`, `DMOON (3476300.0 / AUNIT)`, `DEARTH (6378140.0 * 2 / AUNIT)`, with an alternative `DSUN 1391978489.9` "consistent with 959.63 arcsec at AU distance" disabled by `#if 0` [@sw-swisseph-swecl]. `sweph.h` defines `SUN_RADIUS (959.63 / 3600 * DEGTORAD)` "Meeus germ. p 391", `EARTH_RADIUS 6378136.6` "AA 2006 K6", `EARTH_OBLATENESS (1.0/ 298.25642)`, and observer altitude limits of -500 m to 25,000 m [@sw-swisseph-sweph-h]. Version at reading: 2.10.03 [@sw-swisseph-sweph-h].

**Algorithm.** The comment above `eclipse_where()` states: "Algorithms for the central line is taken from Montenbruck, pp. 179ff., with the exception, that we consider refraction for the maxima of partial and noncentral eclipses. Geographical positions are referred to sea level / the mean ellipsoid." It lists error sources: an assumed JPL ephemeris uncertainty of 0.01 arcseconds worth about 40 m, refraction a few metres, geoid a few metres, polar motion a few metres, "For geographical locations that are interesting for observation, the error is always < 100 m. However, if the sun is close to the horizon, all of these errors can grow up to a km or more" [@sw-swisseph-swecl]. The code computes ΔT with `swe_deltat_ex()`, takes Moon and Sun Cartesian equatorial positions, and sets

$$\sin f_1 = \frac{r_\odot - r_M}{d_{SM}},\quad \sin f_2 = \frac{r_\odot + r_M}{d_{SM}},\quad d_0 = \frac{\frac{s_0}{d_{SM}}(2r_\odot - 2r_M) - 2r_M}{\cos f_1},\quad D_0 = \frac{\frac{s_0}{d_{SM}}(2r_\odot + 2r_M) + 2r_M}{\cos f_2}$$

where `s0` is the Moon's distance from the fundamental plane, which is not the almanac's $s_0$, and `r0`, equal to $\sqrt{d_M^2 - s_0^2}$, is the shadow axis distance from the geocentre. It classifies central when $R_E\cos f_1 \ge r_0$, noncentral when $r_0 \le R_E\cos f_1 + |d_0|/2$, partial when $r_0 \le R_E\cos f_2 + D_0/2$ [@sw-swisseph-swecl]. `eclipse_how()` is topocentric: it sets the observer with `swe_set_topo()`, computes apparent radii $r_M = \arcsin(R_M/\Delta_M)$ and $r_\odot = \arcsin(R_\odot/\Delta_\odot)$, the centre separation $d_{ctr}$, and classifies annular if $d_{ctr} < r_\odot - r_M$, total if $d_{ctr} < |r_\odot - r_M|$, partial if $d_{ctr} < r_\odot + r_M$ [@sw-swisseph-swecl]. `eclipse_when_loc()` finds the local maximum with `find_maximum()`, then contacts by `find_zero()` on $|r_\odot - r_M| - d_{ctr}$ for C2 and C3 and $r_\odot + r_M - d_{ctr}$ for C1 and C4, and applies `rmoon *= 0.99916; /* gives better accuracy for 2nd/3rd contacts */` before the interior contacts, then converts TT to UT by subtracting ΔT [@sw-swisseph-swecl]. That factor is an empirical stand-in for a smaller umbral $k$ (0.99916 × 3476.3/2 = 1736.7 km). There is no limb profile and no terrain.

**Licence and data.** Dual licence, AGPL or the Swiss Ephemeris Professional License at CHF 750 for the first licence [@sw-swisseph-gendoc]. Versions since 2.00 are based on JPL DE431 for -13000 to +16800, and version 2.06 introduced a ΔT algorithm based on Stephenson, Morrison and Hohenkerk 2016 [@sw-swisseph-gendoc].

## Astronomy Engine (Don Cross)

**Scope.** "Predicts lunar and solar eclipses", accuracy "always within 1 arcminute of results from NOVAS", based on "truncated VSOP87 series", MIT licence, implementations in C, C#, JavaScript, Python and Kotlin, 1,016 stars, last push 2025-01-27 [@sw-astronomy-engine-repo] [@sw-github-api-search].

**Constants.** `SUN_RADIUS_KM 695700.0`, `EARTH_EQUATORIAL_RADIUS_KM 6378.1366`, `EARTH_FLATTENING 0.996647180302104`, `EARTH_MEAN_RADIUS_KM 6371.0`, `MOON_MEAN_RADIUS_KM 1737.4`, `EARTH_ATMOSPHERE_KM 88.0` (lunar eclipses only) [@sw-astronomy-engine-h] [@sw-astronomy-engine-c].

**Method.** `CalcShadow()` projects the target onto the Sun-body axis, with $u$ the projection parameter, and defines the umbra and penumbra radii at the target's distance as

$$k = R_\odot - (1+u)(R_\odot - R_{body}),\qquad p = -R_\odot + (1+u)(R_\odot + R_{body})$$

with $r$ the perpendicular distance of the target from the axis in km [@sw-astronomy-engine-c]. `GeoidIntersect()` rotates the axis into equator-of-date coordinates, dilates $z$ by `1/EARTH_FLATTENING` "so that the Earth becomes a perfect sphere", solves the quadratic for the near intersection, and converts back to geodetic latitude and longitude with the sidereal time, citing "p 184 in Montenbruck & Pfleger's 'Astronomy on the Personal Computer', second edition" [@sw-astronomy-engine-c]. Eclipse kind follows `EclipseKindFromUmbra(k) ((k) > 0.014 ? ECLIPSE_TOTAL : ECLIPSE_ANNULAR)` [@sw-astronomy-engine-c]. The global result carries `distance`, "The distance between the Sun/Moon shadow axis and the center of the Earth, in kilometers", and the peak latitude and longitude [@sw-astronomy-engine-h]. `LocalEclipse()` finds partial begin and end within ±0.2 day and total begin and end within ±0.01 day of the geocentric peak by root-finding on observer-specific distance functions, and computes obscuration from disc overlap with `Obscuration()` [@sw-astronomy-engine-c]. The local result has `partial_begin`, `total_begin`, `peak`, `total_end`, `partial_end`, each with Sun altitude, and `obscuration` [@sw-astronomy-engine-h]. There are no Besselian elements, no path limits, no limb profile and no terrain. Several repositories in the next note build maps on it.

## Skyfield

The almanac provides `eclipselib.lunar_eclipses()` "using the techniques described in the Explanatory Supplement to the Astronomical Almanac", which finds all 3,642 lunar eclipses of AD 1000 to 2500 in the NASA lunar Canon with 0.2 per cent type disagreement and times "a few seconds earlier" [@sw-skyfield-almanac]. `eclipselib.py` uses solar radius 696,340 km, lunar radius 1,737.1 km and Danjon's enlargement, and contains no solar routine [@sw-skyfield-eclipselib]. Issue #445, in 2020, requested eclipses and offered table lookups from the NASA catalogues [@sw-skyfield-issue-445]. Pull request #1076, in 2025, adds a solar routine that "uses similar method as lunar eclipse calculation, but instead of looking for maximum of angle between earth-sun and earth-moon, it looks for minimum", classifies by penumbra, umbra or antumbra, and reports agreement with NASA over 400 years except for zero-duration and marginal partial eclipses [@sw-skyfield-pr-1076]. Issue #1078 tracks it, with no maintainer reply visible at the time of writing (2026 September) [@sw-skyfield-issue-1078]. Skyfield with JPL kernels is nonetheless the ephemeris layer used by several eclipse repositories below.

## PyEphem, libnova, NOVAS, SOFA and ERFA

PyEphem documents `separation()` and per-body `size` and `radius` attributes but no eclipse function [@sw-pyephem-quick]. libnova's solar group lists coordinates, rise and set, and `ln_get_solar_sdiam()` only [@sw-libnova-solar]. NOVAS 3.1 is "an integrated package of routines for computing various commonly needed quantities in positional astronomy" with no eclipse routine described [@sw-novas-info]. SOFA provides "an accessible and authoritative set of algorithms and procedures that implement standard models used in fundamental astronomy", release 2023-10-11, with no eclipse routine mentioned [@sw-sofa-home]. ERFA is the SOFA re-licensing and was not checked separately. These libraries supply time scales, Earth orientation and apparent places that an eclipse pipeline needs upstream of the Besselian stage.

## astropy and sunpy

An astropy issue search for "solar eclipse" returned only a light-deflection issue and a date-parsing issue, and no eclipse feature [@sw-astropy-issues]. sunpy provides `sunpy.coordinates.sun.eclipse_amount(observer, moon_radius='IAU')` where `'IAU'` is "the IAU mean radius (R_moon / R_earth = 0.2725076)" and `'minimum'` is "the mean minimum radius (R_moon / R_earth = 0.272281)", under "the simplifying assumption that the Moon has a constant radius", with the warning that "the output can be slightly inaccurate for the start/end of partial solar eclipses ... and the start/end of total solar eclipses" and that a JPL ephemeris should be used [@sw-sunpy-eclipse-amount]. The gallery example sets `de440s`, builds an ITRS observer and scans ±2 hours to find the phases [@sw-sunpy-gallery-eclipse].

## SPICE and Horizons

`gfoclt_c` finds intervals of FULL, ANNULAR, PARTIAL or ANY occultation of a back body by a front body for an observer, with ELLIPSOID, POINT or DSK shape models, and its Example 1 is "Find occultations of the Sun by the Moon (that is, solar eclipses) as seen from the center of the Earth over the month December, 2001" with light-time correction [@sw-spice-gfoclt]. `gfsep_c` searches angular separation between body centres with SPHERE or POINT shapes, notes that ELLIPSOID "is not yet implemented", and warns that a direct search for zero separation of two point targets always fails [@sw-spice-gfsep]. The NAIF Geometric Event Finding lesson uses Mars Express, not an eclipse [@sw-spice-lessons]. With an Earth-surface observer defined as a topocentric frame, `gfoclt_c` with a DSK Moon is the only off-the-shelf route to limb-shaped contact intervals found at the time of writing (2026 September), and no repository using it that way was found. Horizons offers DE440 and DE441 based observer tables including the Sun-Observer-Target angle and satellite eclipse circumstances, but no solar eclipse product [@sw-horizons-manual].

## Meeus chapter 54 ports

astronomia's `eclipse.js` returns type (None, Partial, Annular, AnnularTotal, Total), central flag, `jdeMax`, magnitude, gamma, and the umbral and penumbral radii, and computes "global eclipse circumstances ... not local circumstances or ground paths" [@sw-astronomia-eclipse]. soniakeys/meeus (Go, 376 stars, last push 2019) has the same `Solar(year)` and `Lunar(year)` scope [@sw-meeus-go-eclipse] [@sw-github-api-search]. Starainrt/astro (Go, Apache-2.0, 157 stars) goes further with built-in VSOP87 and ELP2000/82, `SolarEclipseCentralPath` for the central line, limits and greatest eclipse, `SolarEclipsePartialFootprints`, and local circumstances, reporting second-level agreement with NASA for global times [@sw-astro-go]. andrmoel/astronomy-bundle (PHP, MIT) computes C1 to C4 and maximum for an observer from VSOP87 and Meeus [@sw-astronomy-bundle-php]. PyMeeus's module index shows no eclipse module [@sw-pymeeus-docs].

## Sources compared

| Library | Global search | Besselian elements | Path and limits | Local contacts | Obscuration | Limb or terrain | Constants | Licence |
|---|---|---|---|---|---|---|---|---|
| Stellarium [@sw-stellarium-sec-cpp] | Yes | Yes, computed | Yes, KML and PNG | Yes | Yes | No | `k` 0.2725076, `s` 0.272281, $R_\odot$ 696,000 km | GPL-2.0 |
| Swiss Ephemeris [@sw-swisseph-swecl] | Yes | No | Central line only | Yes | Yes | No | $D_M$ 3476.3 km, $D_\odot$ 1,392,000 km, factor 0.99916 | AGPL or paid |
| Astronomy Engine [@sw-astronomy-engine-c] | Yes | No | Peak point only | Yes | Yes | No | $R_\odot$ 695,700 km, $R_M$ 1737.4 km | MIT |
| Skyfield [@sw-skyfield-almanac] | Lunar only | No | No | No | No | No | 696,340 km, 1737.1 km | MIT |
| sunpy [@sw-sunpy-eclipse-amount] | No | No | No | By scanning | Yes | No | $k$ 0.2725076 or 0.272281 | BSD |
| SPICE gfoclt [@sw-spice-gfoclt] | Intervals | No | No | Intervals for a frame | No | DSK shapes | Kernel radii | US Government |
| Starainrt/astro [@sw-astro-go] | Yes | Not stated | Yes | Yes | Yes | No | VSOP87, ELP2000/82 | Apache-2.0 |
| astronomia, soniakeys/meeus [@sw-astronomia-eclipse] [@sw-meeus-go-eclipse] | Yes | No | No | No | Partial magnitude | No | Meeus ch. 54 | MIT |

## What a developer should do

Use Stellarium's `SolarEclipseComputer.cpp` as the algorithmic reference for global products because it is the only open code that cites the 2013 Explanatory Supplement equation numbers for limits and outlines [@sw-stellarium-sec-cpp]. Use Swiss Ephemeris or Astronomy Engine as independent geometric cross-checks of the central line and of local contacts, remembering that both assume a mean lunar radius and that Swiss Ephemeris applies the 0.99916 factor [@sw-swisseph-swecl] [@sw-astronomy-engine-c]. Use Skyfield with DE440 or DE421 kernels as the ephemeris layer and sunpy's `eclipse_amount` for an obscuration cross-check with the two $k$ conventions [@sw-sunpy-eclipse-amount]. Treat SPICE `gfoclt_c` with a lunar DSK as the candidate route for a physically shaped Moon if a Besselian-plus-limb-profile approach proves insufficient [@sw-spice-gfoclt].

## What this changes

Nothing for the stage structure. It supplies three independent implementations for cross-validation of the Besselian stage and identifies the constants each one bakes in.

## Open questions

- Obtain Stellarium's git history for `SolarEclipseComputer.cpp` and `Planet.cpp` to date when the Besselian code first appeared and who wrote it. The sparse clone read here was at depth 1 [@sw-stellarium-sec-cpp].
- Obtain the origin of the `0.99916` factor in `swecl.c` from Astrodienst's change history [@sw-swisseph-swecl].
- Obtain the test data Astronomy Engine uses for eclipse regression tests to see whether it compares against Espenak's tables [@sw-astronomy-engine-repo].
- Obtain the final state of Skyfield pull request #1076 [@sw-skyfield-pr-1076].
