---
title: Phenomena of Jupiter's Galilean satellites
seo_title: Jupiter's Moons: Eclipses, Transits and Mutual Events
description: How eclipses, occultations, transits, shadow transits and mutual events of Jupiter's Galilean satellites are computed, from Sampson and Lieske to JUP365 and PHEMU.
order: 15
status: working
updated: 2026-10-17
tags: [jupiter, galilean-satellites, eclipses, occultations, transits, mutual-events, phemu]
---

::: summary
- **Five kinds of event, two geometries.** Eclipses and shadow transits are decided from the Sun. Occultations and transits are decided from the Earth. Mutual events need the Earth or the Sun in the satellites' orbital plane, which happens for about a year every 5.9 years [@jup-nsdc-guide] [@jup-saquet-2018].
- **The theory changed from analytical to numerical.** Sampson (1921) and Lieske's E-series served until the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) switched to Lainey's L1 for 2015 and to the NOE solution from 2023. JPL's JUP365 (2021, with DE440) is the current SPICE kernel [@jup-imcce-phenjupiter-readme] [@jup-naif-jup365-cmt].
- **The classical computation is two cones and an oblate Jupiter,** with separate light-time rules for the Sun path and the Earth path, and a phase correction of up to 6 minutes [@jup-thuillot-1983].
- **Published times are mid-events in TT:** half flux for an eclipse, bisection for the rest. The first or last visible speck is 1 to 15 minutes away, depending on the satellite [@jup-imcce-phenjupiter-readme] [@jup-westfall-alpo].
- **Mutual events give some of the most accurate ground-based astrometry,** 5 to 50 milliarcseconds, or 15 to 150 km, through a photometric model of the satellites' surfaces fitted to each light curve [@jup-saquet-2018] [@jup-catani-2023].
- **The history matters to the pipeline.** Io's eclipses gave the first finite speed of light in 1676, and the light-time they revealed, 33 to 53 minutes, enters every prediction [@jup-bobis-lequeux-2008] [@jup-soniakeys-jupitermoons].
:::

## What this topic covers

This topic covers how the phenomena of Jupiter's four large moons are predicted. It covers the theories of motion and the ephemeris files, with dates, versions and accuracy. It gives the shadow and disc geometry with Jupiter's flattening, the light-time rules and the phase correction. It defines what a published "start" or "end" means and how Jupiter's atmosphere blurs an eclipse. It describes the published tables and the software, and states the theory each one uses. Finally it covers mutual events: when they happen, the PHEMU campaigns from 1973 to 2021, the photometric models and the astrometric accuracy they reach.

## Notes in this topic

- [Theories and ephemerides](theories-and-ephemerides.md): Sampson, the Sampson-Lieske theory and E5, Lainey's L1 and NOE, JPL's JUP310 and JUP365, Meeus's two methods with formulas, and which program uses which.
- [Eclipses, occultations, transits and shadows](eclipses-occultations-transits-shadows.md): the four satellite-Jupiter phenomena, shadow cones, flattening, light-time, the phase correction, timing conventions, the atmosphere, published products, accuracy, and Rømer.
- [Mutual events](mutual-events.md): equinox geometry, the PHEMU campaigns, prediction, photometric models, reduction to astrometry and the accuracy achieved.

## What this topic changes for the pipeline

The pipeline needs a satellite ephemeris layer next to the planetary one, versioned as a pair such as DE440 with JUP365. The shadow-cone code must accept an oblate occulting body whose projected outline depends on the jovicentric declination. It must keep the Sun-side and Earth-side light-time paths apart. The contact solver needs a mid-event mode, half flux or bisection, because that is what the reference tables publish. Mutual events add a photometric stage, the overlap of two textured discs under a limb-darkened Sun, which no part of the solar eclipse pipeline needs. Saturn's satellite phenomena follow the same pattern and are covered in their own topic.
