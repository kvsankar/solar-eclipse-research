---
title: Error budget
description: Every input to an eclipse prediction ranked by its effect in seconds of contact time and metres on the ground, and the two product modes that follow.
order: 3
status: working
updated: 2026-09-16
---

::: summary
- **Nobody has published a complete budget.** Quaglia and colleagues state the ephemeris, Earth-orientation and topography terms and conclude the solar radius dominates. Espenak states the limb and ΔT terms. Wright and Young state the terrain rule. The table below assembles all three with the arithmetic that joins them [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-wright-young-2024].
- **Three terms of 0.6 to 3 km each at the edge**: the solar radius if the standard value is used, the lunar limb if omitted, and terrain if omitted. Everything else is under 100 m and 0.5 s.
- **Two gross errors are worth guarding against first**: a geometric Sun paired with an apparent Moon (38 km) and TT used where UT belongs (32 km). They are implementation bugs, not modelling choices [@earth-es1992] [@moon-skyfield-positions].
- **The residual for a true-limb, terrain-corrected product with 959.95″ is about 100 m** from the radius uncertainty, plus 60 to 130 m of spread between implementations given the same inputs [@val-quaglia-2021].
- **ΔT prediction error grows as the square of the lead time**: 0.05 s at one year, 4.6 s at twenty, 52 s at a hundred, and 265 s or more before the year 1 and after 2300 [@earth-nasa-deltat-uncertainty] [@val-gsfc-uncertainty].
:::

## The ranked budget

"Mid-path" is a site near the central line of a 2017-class eclipse with a
shadow speed near 1 km/s. "Edge" is within a few hundred metres of a limit.
Conversions used: 1″ at the Moon's mean distance is 1.86 km on the ground;
1 s of ΔT is 15.041″ of longitude, 465 m at the equator and 356 m at 40°; the
relative Moon-Sun motion of 0.364″/s gives 2.7 s of contact time per
arcsecond [@val-5mcse-tp2009] [@moon-espenak-2001-bulletin].

| Rank | Term | Mid-path contact time | Edge position or duration | Included by |
|---|---|---|---|---|
| 1 | Geometric Sun with apparent Moon | 55 s | 38 km | Everyone avoids it; test for it [@earth-es1992] |
| 2 | TT used as UT | 69 s | 32 km at the equator | Everyone avoids it; test for it [@moon-eclipsewise-2024] |
| 3 | Sphere instead of ellipsoid | tens of s | up to 21 km | Everyone [@earth-es1961] |
| 4 | Terrain omitted | seconds where the Sun's azimuth lies along the track | $h\cot a$; up to 3 km in the 2017 western states | SVS only, for the path; single-site altitude in Jubier, Occult, Swiss Ephemeris [@val-svs-4517] [@earth-espenak-tp2001] |
| 5 | Lunar limb omitted | 1 to 3 s, up to 15 s in extreme geometry | 1 to 3 km per limit; 33 s of duration at Stephenville 2024 | SVS, Jubier, Occult, Irwin, Photo Ephemeris simulator [@loc-nasa-limb-help] [@val-besselian-maps-accuracy] |
| 6 | Solar radius 959.63″ against 959.95″ | 1.6 to 1.8 s of central-line duration | 600 m per limit; 19.3 s at a site 1.2 km inside the Vale 2017 limit as drawn with 959.63″; 11 s at Stephenville | Irwin uses 959.95″, Photo Ephemeris in its bead simulator only; everyone else 959.63″ or 696,000 km [@sun-quaglia-2021] [@sun-wright-young-2024] |
| 7 | Lunar radius $k$, umbral, if the IAU value is used | about 4 s of duration | 1.4 km per limit | Espenak, Stellarium, Jubier use 0.272281; USNO and Astronomy Engine use a mean radius; the Swiss Ephemeris uses 1738.15 km globally but scales the lunar radius by 0.99916, which is 0.272281, for C2 and C3 [@bes-nasa-radius] [@val-gsfc-sepredictions] |
| 8 | ΔT prediction error, realised in 2024 | 1.4 to 2.3 s | 500 to 800 m east-west at 40° | All; the miss depends on when the prediction was frozen [@earth-usno-deltat-data] [@val-eclipsewise-2024-circ] |
| 9 | Centre of figure against centre of mass, smooth-Moon products | up to 1.4 s | 0.5 to 1 km | Absorbed by any DEM-based profile; not applied by USNO [@moon-jones-2025] [@val-usno-2024] |
| 10 | Watts-era limb data | 0.5 s | 600 to 750 m systematic at some position angles | Superseded by Kaguya and LOLA [@limb-morrison-appleby-1981] [@val-tp2001-bulletin] |
| 11 | Geoid against ellipsoid height | under 1 s | $N\cot a$, up to 170 m at a 30° Sun | SVS (EGM96); nobody else documents it [@earth-svs-4515] |
| 12 | Implementation spread on identical inputs | 2 to 4 s at Vale 2017 | 0.03″ to 0.07″ of radius, 60 to 130 m | Occult, Solar Eclipse Maestro, Irwin [@val-quaglia-2021] |
| 13 | Solar radius residual, ± 0.05″ | 0.1 s | 100 m band | The physical floor [@sun-quaglia-2021] |
| 14 | Limb sampling coarser than 18,000 elements | 0.25 s for 0.2° bins | part of the implementation spread | SVS at 0.02° [@limb-wright-young-2024] [@loc-be-2013-contacts] |
| 15 | Refraction, Sun above 5° | under 1 s at C2 and C3 | a few metres | Nobody; cancels in the relative angle [@earth-espenak-tp2001] |
| 16 | Refraction, C1 and C4 with the Sun at 1° to 5° | 10 to 80 s, unpredictable | not applicable | Nobody; state it [@earth-es1992] |
| 17 | Sidereal time inconsistency, mean against apparent | up to 1.1 s | up to 0.5 km | Consistent in every predictor documented [@earth-circ179] |
| 18 | UT1 against UTC | up to 0.9 s | up to 0.42 km | UT1 printed by Espenak, SVS, Swiss Ephemeris [@earth-iers-bulletin-a] |
| 19 | Moon light-time omitted | 1.9 s | 1.3 km | Apparent places include it [@moon-folkner-2014] |
| 20 | Ephemeris, DE421 to DE440 | under 0.01 s | under 1 m | Irrelevant [@moon-park-2021] |
| 21 | Ephemeris, DE403 to DE421, at 2020 | 0.02 s | 16 m | Irrelevant [@moon-williams-2008] |
| 22 | ELP-2000/82 truncated as in the Canon | 0.02 s | 10 m | Irrelevant for paths [@moon-espenak-meeus-canon] |
| 23 | Polar motion | 0 | about 10 m | SPICE kernels include it; nobody documents it [@earth-iers-bulletin-a] |
| 24 | Nutation model, 1980 against 2000A | 0 | under 20 m | Irrelevant [@earth-circ179] |
| 25 | TT against TDB | 1.7 ms | 2 m | Irrelevant [@earth-circ179] |
| 26 | Observer position, consumer GPS | none on time | ± 100 m | The observer's problem [@val-tp2001-bulletin] |
| 27 | Observer clock, visual timing | "a couple of seconds" | same | The observer's problem [@val-besselian-maps-accuracy] |

![Two implementation bugs dwarf every modelling choice at tens of kilometres. Below them three terms of kilometre scale separate a product that models the edge from one that does not: terrain omitted, the lunar limb omitted, and the solar radius taken as 959.63″. Everything else falls under 200 m, down to the ephemeris at under a metre. Each bar is a row of the table above [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-wright-young-2024] [@earth-es1992] [@sun-quaglia-2021].](img/error-budget.svg)

## ΔT by lead time and epoch

The a priori uncertainty of ΔT, from Huber's model as used by NASA for the
future and from Morrison and Stephenson's $\sigma = 0.8t^2$ rule with $t$ in
centuries from 1820 for the past [@earth-nasa-deltat-uncertainty]
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
their errors: about 2 km at a limit from rows 4 to 6 combined. This is the
mode for catalogues, for reproducing published tables, and for regression
tests.

**Edge mode.** LOLA profile at 18,000 elements, terrain with geoid,
$s_0 = 959.95″ ± 0.05″$, ΔT refreshed to the latest USNO or IERS value. The
residual is rows 12 and 13: about 100 to 200 m at a limit and 2 to 4 s of
duration a few hundred metres inside it. Dunham's practical margin of 2 km of
[?umbral-depth] covers the instrumental sensitivity to faint beads that no
computation removes [@val-dunham-iota-2024].

The two modes differ by design and must not share a file. A map that draws an
almanac-mode limit next to an edge-mode duration misleads by 600 m.

## How to report it

Sum the rows that apply in quadrature and print the total with the limit as a
band. Draw the limit at $s_0$ and at $s_0 \pm \sigma_s$. Within 2 km of a
limit, print the umbral depth and a warning that the radius uncertainty
dominates. For dates outside 1600 to 2300, add the ΔT gore. Store the
configuration record beside the number so that two runs can be compared term
by term [@sun-quaglia-2021] [@val-quaglia-2021].
