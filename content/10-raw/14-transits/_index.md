---
title: Transits of Mercury and Venus
seo_title: Transits of Mercury and Venus: How Contact Times Are Computed
description: How transits of Mercury and Venus are enumerated and predicted, the constants that move their contact times, and what observations show.
order: 14
status: working
updated: 2026-10-17
tags: [transits, mercury, venus, black-drop, solar-radius, astronomical-unit]
---

::: summary
- **A transit is a solar eclipse by a planet, and the almanacs compute it that way.** The 1961 Explanatory Supplement adapts Bessel's eclipse theory with the planet in place of the Moon, and Stellarium uses the solar-eclipse elements with the planet's radius as $k$ [@tr-es1961] [@tr-stellarium-transits].
- **The NASA catalogues list 94 Mercury transits from 1601 to 2300 and 81 Venus transits from 2000 BCE to 4000 CE.** Their elements and algorithms come from Meeus's *Transits* (1989), and the cycles are 13, 33 and 46 years for Mercury and 8, 105.5, 8 and 121.5 years for Venus [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog].
- **Local contact times come from a three-constant formula per contact.** The yearbook form $T = T_0 + a\,\rho\sin\phi' + b\,\rho\cos\phi'\cos(c + \lambda)$ is still printed by the Institute of Applied Astronomy of the Russian Academy of Sciences (IAA RAS), and the longitude sign differs between sources [@tr-iaa-2019] [@tr-es1961].
- **The solar and planetary radii dominate the residual differences.** One arcsecond of contact radius moves an interior contact by 10 to 21 seconds of time at the modern transits, computed from the Supplement's contact solution with the published elements [@tr-es1961] [@tr-eso-eis-b1] [@tr-ew-tm2016] [@tr-ew-tm2019] [@tr-jubier-mtc-js] [@tr-jubier-vtc-js]. The 4 to 5 second differences between Espenak and the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) for 2004 match a Venus semidiameter of 8.41 against 8.34 arcseconds [@cat-meeus-1991-aa] [@tr-nasa-oh2004] [@tr-eso-eis-b1].
- **The black drop is the telescope and atmosphere blurring a limb-darkened edge.** The Transition Region and Coronal Explorer (TRACE) showed it from space at a Mercury transit, so it does not need a planetary atmosphere [@tr-spg-2004].
- **Transits measured the astronomical unit and now measure the solar radius.** Newcomb's 1874 and 1882 reduction gave 8.79 arcseconds of solar parallax, the 2004 public campaign recovered the astronomical unit to 0.007 per cent after a selection, and space timings give radii from 959.57 to 960.12 arcseconds [@tr-eso-eis-f5] [@tr-eso-vt2004-results] [@tr-emilio-2012] [@tr-emilio-2020].
:::

## What this topic covers

This topic covers the computation of transits of Mercury and Venus across the Sun as seen from the Earth. It traces enumeration through node passages and recurrence cycles, the almanac elements in heliocentric and geocentric form, the contact-time solution and the local reduction formulas, the constants that matter, and the observations that test the predictions. It reuses the solar-eclipse machinery of [Besselian elements](../01-foundations/besselian-elements.md), [local circumstances](../04-local-circumstances/_index.md), [solar radius](../06-solar-radius/_index.md) and [Earth and time](../07-earth-and-time/_index.md), and states only what differs for a planet. Transits seen from other planets are outside it, except Phobos and Deimos, which the [Saturn and outer satellites](../16-saturn-and-outer-satellites/uranus-pluto-and-others.md) topic covers briefly.

## Notes in this topic

- [Enumerating transits and their elements](enumeration-and-elements.md): the node condition and limits, the Mercury and Venus cycles and series, grazing and topocentric-only transits, how the NASA, IMCCE, Stellarium and Swiss Ephemeris lists are computed, and the elements in the Supplement's heliocentric form, Stellarium's vector form, Jubier's polynomial form and the IAA yearbook form.
- [Transit contacts and local circumstances](contacts-and-local-circumstances.md): the contact solution, least separation and position angles, the rigorous and linearised local formulas with worked examples, ΔT and the longitude sign, the radius constants each source uses, a sensitivity figure, and predictor-against-predictor comparisons for 2004, 2016 and 2019.
- [Observations, the black drop and the solar radius](observations-black-drop-and-solar-radius.md): the black drop and its four explanations, the Venus aureole, Halley's and Delisle's methods, the historical solar parallax values, the VT-2004 analysis, solar radius results from transits, and the observed-minus-predicted contacts that exist.

## What this topic changes for the pipeline

The element and contact stages become body-agnostic. The radius of the occulting body, the exact rather than small-ratio point-Z formulas, and both semidiameters must be inputs, and a prediction must carry its planetary radius beside $s_0$, ΔT and the ephemeris. The catalogue schema needs room for missing geocentric contacts and for topocentric-only events. The validation suite gains space-based transit timings, which test the solar radius without a lunar limb profile.
