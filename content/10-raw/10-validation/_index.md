---
title: Validation and error budget
description: How eclipse predictions have been checked against timed observations, how far the major predictors disagree at the path edge, and what each term contributes to the error of a modern prediction.
order: 10
status: working
updated: 2026-09-15
tags: [validation, error-budget, solar-radius, delta-t, path-edge]
---

::: summary
- **Only edge observations test a prediction.** A 0.37 arcsecond change of solar radius moves a 2017 central-line duration by 1.8 s and the duration a few hundred metres inside the southern limit by 19.3 s, so every quantitative test since 1973 has been made at or near a path limit [@val-quaglia-2021].
- **Four independent campaigns since 2010 put the eclipse solar radius between 959.95 and 960.01 arcseconds**, about 0.32 arcseconds above the 959.63 arcseconds nearly every product uses, which is 610 m per path limit [@val-lamy-2015] [@val-quaglia-2021] [@val-guhl-2023] [@val-earthsky-2024-edges].
- **The cleanest 2024 edge test observed 13.7 s of totality where six public products predicted 12.9 s to 65 s.** Only a true-limb model with the larger radius came within a second [@val-besselian-maps-accuracy].
- **At the edge the budget is dominated by three terms of 0.6 to 3 km each:** the solar radius, the lunar limb if omitted, and terrain if omitted. Everything else is below 100 m and 0.5 s once ΔT is refreshed and a profile is used [@val-quaglia-2021] [@val-gsfc-2024-google].
- **A five-level test protocol can be assembled from published cases**, from the 1961 Explanatory Supplement worked examples through the 2001 Lusaka limb corrections to the Vale, Stephenville and bead-timing records [@val-es1961] [@val-tp2001-bulletin] [@val-guhl-tegtmeier-2018].
:::

## What this topic covers

This topic asks how far eclipse predictions have actually been shown to be right. It collects the published comparisons of timed contacts and Baily's bead events against predictions, sets the major public predictors side by side and names the input behind each disagreement, and assigns seconds of contact time and metres of path edge to every term in the error of a modern prediction. It ends with reference cases and tolerances a new implementation can be tested against.

Notes in this topic:

- [Observed versus predicted](observed-vs-predicted.md): the IOTA and IOTA/ES edge campaigns from 1973, the 2017 Vale and Thermopolis results, the 2023 Cape Range results and the 2024 Stephenville experiment, with the measured offsets.
- [Predictor disagreements](predictor-disagreements.md): the inputs the NASA SVS, Espenak, Jubier, Irwin, USNO, timeanddate, Occult, Stellarium and Photo Ephemeris products state, and how far their edges and durations differ.
- [Error budget and validation protocol](error-budget-and-validation-protocol.md): the sourced per-term budget, the record of ΔT model validation, and the five-level test protocol with tolerances.

## What this topic changes for the pipeline

The solar radius stops being a constant and becomes a configuration item with a stated uncertainty and two documented modes. Every product carries a per-run error estimate and draws its path limits as a band rather than a line. The five-level protocol becomes an automated test suite, with each reference case's constants pinned beside its tolerance.
