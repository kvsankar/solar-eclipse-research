---
title: Earth model and time scales
description: The figure of the Earth, observer height and terrain, ΔT and Earth rotation, refraction, light-time and time scales, with the size of every effect and which predictors include it.
order: 7
status: working
updated: 2026-09-15
tags: [earth-figure, delta-t, refraction, time-scales]
---

::: summary
- **Use WGS 84 and never a sphere.** The three modern ellipsoids differ by 3 m in equatorial radius, but feeding a geodetic latitude into spherical formulas misplaces the observer by up to 21 km [@earth-nga-wgs84] [@earth-es1961].
- **Terrain moves a path limit by $h \cot A \sin D$**, 577 m per 1000 m of elevation at a 60° Sun and 5.7 km at 10°. NASA SVS is the only predictor that puts every observer on the terrain, and it measured up to 3 km of umbra shift in 2017 [@earth-espenak-tp2001] [@earth-svs-4517].
- **ΔT enters only through μ**, and one second of it moves every longitude by $465\cos\phi$ metres. The 2006 Espenak and Meeus polynomial was 1.4 to 2.3 s high for 2024, which is 0.5 to 0.8 km at latitude 40° [@earth-es1992] [@earth-usno-deltat-data].
- **Refraction is left out of contact times, and that is right above a 5° Sun.** A common lift of both disks cancels, leaving seconds at first and last contact below 5° and under a second at second and third contact [@earth-espenak-tp2001] [@earth-es1992].
- **The elements are built from apparent places.** Using a geometric Sun displaces the shadow axis by 20.5 arcseconds, which is 38 km on the ground [@earth-es1992].
:::

## What this topic covers

Three notes on the parts of an eclipse computation that concern the Earth rather than the Sun and Moon: the ellipsoid and the observer's coordinates, terrain and the elevation datasets, the rotation of the Earth and the ΔT models that describe it, and the atmospheric and frame corrections that sit between an ephemeris and a contact time.

## Notes in this topic

- [Earth figure and terrain](earth-figure-and-terrain.md): the ellipsoid behind $\rho\sin\phi'$ and $\rho\cos\phi'$, what a sphere costs, how observer height moves the path limits, what NASA SVS did with SRTM for 2017 and 2024, the free elevation datasets, and the geoid question.
- [ΔT and Earth rotation](delta-t-and-earth-rotation.md): the definition TT − UT1, where it enters the elements, the Morrison and Stephenson and Stephenson, Morrison and Hohenkerk models, the Espenak and Meeus polynomials and their tidal-acceleration correction, IERS and USNO data, prediction uncertainty by lead time, the values each predictor used for 2017 and 2024, leap seconds, polar motion and sidereal time.
- [Refraction, light-time and frames](refraction-light-time-and-frames.md): why refraction is left out of contact times and why that is mostly right, the almanac and Stellarium formulas, apparent places and the 38 km aberration trap, TT versus TDB, and the table of every effect with its size and who includes it.

## What this topic changes for the pipeline

The pipeline needs a terrain stage between the global Besselian solution and the published path polygons, a ΔT provider with three regimes and a stated uncertainty, and an "apparent places" contract on the ephemeris interface. Every published coordinate needs a stated datum and every published path needs the ΔT value stamped on it. The recurring finding is one of scale: getting the Sun's aberration or the Earth's flattening wrong costs tens of kilometres, terrain costs kilometres at the limits, and a ΔT prediction error costs hundreds of metres, while the geoid, polar motion, the nutation model, TDB and refraction above 5° together cost less than the metre-level error of the ephemeris itself [@moon-park-2021].
