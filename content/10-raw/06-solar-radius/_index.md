---
title: Solar radius
description: Which solar radius an eclipse computation should use, where each value in circulation comes from, and what a 0.1 arcsecond change does to path limits, durations and contact times.
order: 6
status: working
updated: 2026-09-15
tags: [solar-radius, bailys-beads, path-limits, constants]
---

::: summary
- **Three values are in circulation.** The canonical 959.63 arcseconds at 1 au of Auwers 1891, the IAU 2015 nominal radius of exactly 695,700 km, which is 959.22 arcseconds, and an eclipse radius near 959.95 arcseconds measured from the edge of totality. They differ because they measure different layers of the Sun [@sun-rozelot-kosovichev-2026] [@sun-quaglia-2021].
- **The eclipse radius is 0.32 arcseconds, or 232 km, larger than the canonical value,** because totality ends only when the last photospheric light is gone [@sun-quaglia-2021] [@sun-lamy-2015].
- **That 0.32 arcseconds moves each path limit inward by 0.6 to 0.9 km on the ground** and costs about 1.8 s of central duration, which is roughly half a second per 0.1 arcseconds [@sun-quaglia-2021] [@sun-iota-dunham-2024].
- **Near a path limit the sensitivity is about ten times the central-line figure,** and one second of duration corresponds to about 0.03 arcseconds of radius [@sun-quaglia-2021] [@sun-wright-young-2024].
- **The settled design is two modes,** 959.63 arcseconds to reproduce almanac and NASA products and 959.95 ± 0.05 arcseconds for edge products, with the radius carried as an explicit parameter and its uncertainty published as a band [@sun-quaglia-2021] [@sun-wright-young-2024].
:::

## What this topic covers

The Sun has no hard edge, so every eclipse computation must choose a number for its radius. This topic traces each value in circulation to the measurement behind it, says which layer of the Sun that measurement records, gives the uncertainty each author quotes, and records which value each predictor uses. It then turns the disagreement into numbers a developer can act on: kilometres of path-limit shift, seconds of central duration, seconds at each contact, and the width of the uncertainty band that should be published with a limit line.

## Notes in this topic

- [Solar radius values and their provenance](solar-radius-values.md): every value, its edge definition, wavelength and uncertainty, and what each predictor uses.
- [Effect of the radius on eclipse products](effect-on-eclipse-products.md): path width, limits, durations, contact times, grazing zones, and how to expose the radius as a parameter with an uncertainty band.

## What this topic changes for the pipeline

The pipeline gains one explicit parameter, the solar radius in arcseconds at 1 au, with a default, an uncertainty and a provenance string, and a rule that the umbral products use it while the penumbral products may use the same value without measurable loss. Path-limit and duration outputs gain an uncertainty band derived from ± 0.05 arcseconds. Nothing else in the Besselian or raster formulation changes, since the radius enters only through the cone half-angles and the limb test.
