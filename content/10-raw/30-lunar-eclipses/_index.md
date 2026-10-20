---
title: Lunar eclipses
seo_title: How Lunar Eclipse Predictions Are Computed
description: How lunar eclipses are enumerated and classified, how the Earth's shadow is sized, how contacts and visibility maps are computed, and how predictions are validated.
order: 30
status: working
updated: 2026-10-17
tags: [lunar-eclipse, umbra, penumbra, shadow-enlargement, danjon, crater-timings, delta-t]
---

::: summary
- **A lunar eclipse prediction is geocentric.** The contacts are the same instant everywhere, so the product is a list of times, two magnitudes, gamma and a map of where the Moon is above the horizon at each contact [@lun-es1961] [@lun-5mcle-tp2009].
- **The computation is the solar method with the Earth as the shadow caster.** The Moon's two coordinates about the antisolar point and three limiting separations are the elements. A quadratic in time gives the six contacts P1, U1, U2, U3, U4 and P4 [@lun-es1961] [@lun-es1992].
- **The size of the Earth's shadow is a convention.** [Chauvenet](https://en.wikipedia.org/wiki/William_Chauvenet) enlarges both radii by 2 per cent, [Danjon](https://en.wikipedia.org/wiki/Andr%C3%A9_Danjon) adds a layer of 1/85 of the Earth's radius, and Herald and Sinnott add 87 km above an oblate Earth. The choice changes umbral magnitudes by 0.005, contacts by 20 to 90 seconds and the type of borderline eclipses [@lun-nasa-shadow-page] [@lun-herald-sinnott-2014].
- **Crater timings are the test.** 22,539 timings at 94 eclipses give a layer of 86.9 km with no dependence on lunar distance, season or solar cycle, and an umbra flattened only by the Earth's own figure [@lun-herald-sinnott-2014].
- **None of the predictions cited here includes brightness.** The Danjon scale grades it after the event, and volcanic aerosols can darken totality by half a magnitude or more [@lun-danjon-1921] [@lun-keen-2019].
:::

## What this topic covers

This topic covers the computation of lunar eclipse products from enumeration to validation. It sets out the classification, gamma and the [Saros](../20-solar-eclipses-and-transits/02-catalogs/enumerating-eclipses.md) behaviour of lunar eclipses, [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus)'s closed form, and the Explanatory Supplement's elements and contact solution. It quotes the shadow-radius formulas of Chauvenet, Danjon and Herald and Sinnott with their constants and shows which almanac and program uses each. It describes visibility maps, the role of [ΔT](../10-shared/07-earth-and-time/delta-t-and-earth-rotation.md), crater timings, the Danjon brightness scale and the effect of volcanic aerosols. It compares the main predictors and ends with the use of historical lunar eclipses as evidence for ΔT.

## Notes in this topic

- [Enumeration, elements and contacts](enumeration-elements-and-contacts.md): types and catalogue codes, gamma, Saros and Inex, eclipse limits, Meeus's method, the lunar [Besselian elements](../10-shared/01-foundations/besselian-elements.md), contacts, magnitudes, durations, the NASA catalogue, visibility maps and ΔT.
- [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md): the umbral and penumbral radii, the oblate Earth, the three enlargement rules with constants, their effects on magnitude, contacts and type, and which implementation uses which.
- [Observation, brightness and validation](observation-brightness-and-validation.md): crater timings and their reduction, the Danjon scale, aerosols and the limits of brightness prediction, predictor comparisons, the [error budget](../../20-reports/error-budget.md), and historical lunar eclipses as ΔT evidence.

## What this topic changes for the pipeline

Lunar eclipses reuse the ephemeris, time and Besselian stages with three changes. The element set shrinks to $x$, $y$ and the limiting separations $L_1$, $L_2$ and $L_3$. A new input, the atmospheric enlargement rule, sets those separations and must be reported with every result. The local-circumstances stage becomes a horizon computation that draws moonrise and moonset curves for each contact, and the path products disappear. Validation needs crater timings from VizieR VI/140 alongside the NASA catalogue.
