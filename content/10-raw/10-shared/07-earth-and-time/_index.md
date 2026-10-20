---
title: Earth model and time scales
description: Earth shape, terrain, ΔT, rotation, refraction and time scales in eclipse calculation, with the size and treatment of each effect.
order: 7
status: working
updated: 2026-09-30
tags: [earth-figure, delta-t, refraction, time-scales]
seo_title: Earth Models and Time Scales in Eclipse Calculation
---

::: summary
- **Use [WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System) and never a sphere.** The three modern ellipsoids differ by 3 m in equatorial radius, but feeding a geodetic latitude into spherical formulas misplaces the observer by up to 21 km [@earth-nga-wgs84] [@earth-es1961].
- **Terrain moves a [path limit](../../20-solar-eclipses-and-transits/03-global-circumstances/path-and-limits.md) by $h \cot A \sin D$**, 577 m per 1000 m of elevation at a 60° Sun and 5.7 km at 10°. NASA [SVS](../../20-solar-eclipses-and-transits/11-svs-wright/_index.md) evaluates terrain height at each mapped observer, and it measured up to 3 km of umbra shift in 2017 [@earth-espenak-tp2001] [@earth-svs-4517].
- **ΔT places the shadow on the rotating Earth through μ**, according to the element set's recorded convention, and one second of it moves every longitude by $465\cos\phi$ metres. The 2006 [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak) and [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) polynomial was 1.4 to 2.3 s high for 2024, which is 0.5 to 0.8 km at latitude 40° [@earth-es1992] [@earth-usno-deltat-data].
- **Nominal geometric contacts omit refraction.** A common one-to-one mapping of both limbs preserves contact and containment. The cited sources do not establish a general physical contact-time correction near the horizon [@earth-espenak-tp2001] [@earth-es1992].
- **Classical elements use apparent places.** Light-time and observer aberration are separate corrections. A 20.5-arcsecond inconsistency corresponds to about 38 km at lunar distance, rather than a guaranteed shift between two consistent formulations [@earth-es1992] [@earth-spice-abcorr].
:::

## What this topic covers

Three notes on the parts of an eclipse computation that concern the Earth rather than the Sun and Moon: the ellipsoid and the observer's coordinates, terrain and the elevation datasets, the rotation of the Earth and the ΔT models that describe it, and the atmospheric and frame corrections that sit between an ephemeris and a contact time.

## Notes in this topic

- [Earth figure and terrain](earth-figure-and-terrain.md): the ellipsoid behind $\rho\sin\phi'$ and $\rho\cos\phi'$, what a sphere costs, how observer height moves the path limits, what NASA SVS did with [SRTM](https://en.wikipedia.org/wiki/Shuttle_Radar_Topography_Mission) for 2017 and 2024, the free elevation datasets, and the geoid question.
- [ΔT and Earth rotation](delta-t-and-earth-rotation.md): the definition TT − UT1, where it enters the elements, the Morrison and Stephenson and Stephenson, Morrison and Hohenkerk models, the Espenak and Meeus polynomials and their tidal-acceleration correction, [IERS](https://www.iers.org/) and [USNO](https://en.wikipedia.org/wiki/United_States_Naval_Observatory) data, prediction uncertainty by lead time, the values each predictor used for 2017 and 2024, leap seconds, polar motion and sidereal time.
- [Refraction, light-time and frames](refraction-light-time-and-frames.md): the geometric-contact convention and separate atmospheric visibility treatment, the almanac and [Stellarium](https://stellarium.org/) formulas, apparent places and the 38 km aberration trap, TT versus TDB, and the table of every effect with its size and who includes it.

## What this topic changes for the pipeline

The pipeline needs a terrain stage between the global Besselian solution and the published path polygons, a ΔT provider with three regimes and a stated uncertainty, and an "apparent places" contract on the ephemeris interface. Every published coordinate needs a stated datum and every published path needs the ΔT value stamped on it. The recurring finding is one of scale: getting the Sun's aberration or the Earth's flattening wrong costs tens of kilometres, terrain costs kilometres at the limits, and a ΔT prediction error costs hundreds of metres. Geoid-height mistakes can reach hundreds of metres at low solar altitude. Polar motion and inconsistent nutation can reach tens of metres. These terms need consistent treatment even when terrain, lunar limb and solar-radius choices dominate the path-edge comparison [@earth-es1992] [@earth-circ179] [@earth-espenak-tp2001].
