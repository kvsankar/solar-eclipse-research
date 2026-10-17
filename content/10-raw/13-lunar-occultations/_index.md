---
title: Lunar occultations
seo_title: Lunar Occultation Calculation: Stars, Planets and Grazes
description: How occultations of stars and planets by the Moon are predicted, mapped and reduced, from cylindrical Besselian elements to grazes, Gaia positions and ΔT.
order: 13
status: working
updated: 2026-10-17
tags: [occultations, besselian, graze, iota, occult, delta-t]
---

::: summary
- **An occultation of a star is an eclipse with a cylindrical shadow.** On the fundamental plane the Moon's shadow is a circle of fixed radius $k = 0.2725$ Earth radii, given by elements at conjunction in right ascension [@occ-es1961] [@occ-es1992].
- **The limits of an occultation are where the star's track is tangent to the limb.** Near them a graze is seen. There the prediction is a limb profile and a height-corrected line on the ground, not a time [@bes-chauvenet-1863] [@occ-iota-manual-2007].
- **A planet is an occulted disc.** Its contacts are those of an eclipse of one disc by another, with the planet's radius replaced by a perpendicular that depends on phase [@bes-chauvenet-1863].
- **Star positions and the limb are no longer the limit.** With Gaia positions and LOLA heights, typical residuals are under 0.04 arcseconds and most predictions agree with video timings to 0.3 s [@limb-occult-accuracy-2016].
- **Three centuries of timings measure ΔT.** The archive from 1623, reduced with DE440 and LOLA, gives ΔT for each timing from its residual and rate [@occ-vizier-vi132c] [@cat-stephenson-2016].
:::

## What this topic covers

This topic covers the computation of lunar occultations of stars and planets. It gives the Explanatory Supplement's elements and station reduction for a star, with the coefficients and limits that the almanac offices published. It describes how the prediction programme passed from HM Nautical Almanac Office and the US Naval Observatory to ILOC and then IOTA. Grazing occultations are covered as limb-profile products: limit lines, profiles, the observer-height shift and station placement. The limb datasets themselves are in [Lunar limb profile](../05-lunar-limb/_index.md). For planets the topic gives Chauvenet's reduction to the eclipse case. It then follows the star catalogues from Robertson's ZC through XZ to Gaia, double stars, and stellar diameters from diffraction. Last, it covers the reduction of timings to residuals, Morrison's analyses, the personal equation, ΔT from the archive, and the error budget of a prediction.

## Notes in this topic

- [Besselian elements for lunar occultations](besselian-elements-for-occultations.md): the shadow cylinder, the conjunction elements, the station reduction and $kn\cos\psi$, the coefficients for nearby observers, limits and visibility maps, the values of $k$, and who publishes predictions.
- [Grazing occultations and the lunar limb](grazes-and-limb.md): graze geometry and history, the limb correction from Watts to LOLA, the graze profile, the elevation correction, station placement and graze reductions.
- [Planets, star catalogues and the reduction of occultations](planets-catalogues-and-reduction.md): occultations of planets, ZC, XZ and Gaia, epoch propagation, double stars, diameters from light curves, residuals and ΔT, the personal equation, the error budget and the software.

## What this topic changes for the pipeline

The eclipse pipeline gains a star target and a cylinder mode. The ephemeris layer must take a catalogue star with its epoch and space motion. The element stage must accept $l_1 = l_2 = k$ and zero cone angles, and the local solver must report $kn\cos\psi$, which is $k$ times the radial limb rate, and the cusp angle. The limb stage is shared unchanged, but the event position angle must be good to 0.01 degrees. Limit lines for stars become graze products with a profile and a terrain step. A reduction stage that turns an observed time into an O−C residual and its rate makes the pipeline usable for validation against the 1623 to present archive.
