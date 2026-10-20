---
title: Saturn and outer-planet satellites
seo_title: Saturn, Uranus and Pluto Satellite Events Computed
description: How eclipses, transits, ring eclipses and mutual events of the satellites of Saturn, Uranus, Pluto and Mars are predicted, from theory to observation.
order: 16
status: working
updated: 2026-10-17
tags: [saturn, uranus, pluto, satellites, mutual-events, rings, phesat]
---

::: summary
- **Saturn's satellite phenomena are seasonal.** Transits, eclipses by the globe and [mutual events](../15-jupiter-satellites/mutual-events.md) of Mimas to [Titan](https://en.wikipedia.org/wiki/Titan_(moon)) cluster around the ring-plane crossings, which came in 1995, 2009 and 2025, 13.72 and 15.74 years apart [@sats-rpx-dps-letter] [@sats-nasa-pia10563] [@sats-baa-2025-notes].
- **The satellite ephemeris decides the prediction.** Dourneau's theory, which [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) chapter 46 condenses, is good to hundreds of kilometres. TASS 1.7 is good to tens of milliarcseconds. JPL's SAT441 and the NOE ephemerides of the Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) are better again [@sats-dourneau-1993] [@sats-arlot-2012-phesat09] [@sats-naif-sat441-cmt].
- **Saturn needs a body model that the Moon never did.** Its flattening is 0.098, and the rings range from nearly transparent, ring C, to nearly opaque, ring B. [Horizons](https://ssd.jpl.nasa.gov/horizons/) ignores both, and none of Horizons, [SPICE](https://naif.jpl.nasa.gov/naif/) and [Stellarium](https://stellarium.org/) models ring transmission [@sats-nssdc-saturn] [@sats-nssdc-rings] [@sw-horizons-manual] [@sw-spice-gfoclt] [@sats-stellarium-planet].
- **Mutual events give the best ground-based astrometry of these satellites.** They reached about 20 milliarcseconds at Saturn in 2009 and formal uncertainties below 0.01 arcseconds at Uranus in 2007 [@sats-arlot-2012-phesat09] [@sats-christou-2009].
- **The 1985 to 1990 Pluto-Charon events showed what light curves can measure,** including radii, albedo maps and the orbit. They also showed how a neglected limb-darkening term biases the radii [@sats-binzel-1985] [@sats-young-binzel-1994].
:::

## What this topic covers

This topic covers the satellite phenomena of Saturn and of the outer planets, with a short section on Mars. It describes the theories and ephemerides that place the satellites, in their dated versions, and quotes Meeus's ring and satellite formulas with their constants. It sets out the geometry of eclipses by an oblate planet and by its rings, and the conventions for the start, end and maximum of an event. It reports what the PHESAT, PHEURA and Pluto-Charon campaigns observed and how accurately. It also records which theory each common program evaluates. Jupiter's Galilean satellites share most of this geometry and are covered in [the Jupiter satellite topic](../15-jupiter-satellites/_index.md). The planetary ephemerides underneath are in [the ephemerides note](../../10-shared/08-lunar-and-solar-model/ephemerides.md), and light-time and frames in [the frames note](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md).

## Notes in this topic

- [Saturn's satellite theories and ring geometry](saturn-theories-and-ring-geometry.md): Dourneau, Harper and Taylor, TASS, NOE and SAT441 with their accuracy. It quotes Meeus chapters 45 and 46 with constants and test vectors, gives Saturn's figure and ring radii, and records which program uses which theory.
- [Phenomena and mutual events of Saturn's satellites](saturn-phenomena-and-mutual-events.md): the event types, ring-plane crossing dates, shadow and light-time geometry, timing conventions, ring eclipses of Iapetus and ring transmission. It also covers the mutual-event photometric model, the 1980 to 2025 campaigns and the limits of public tools.
- [Uranus, Neptune, Pluto and Mars satellite events](uranus-pluto-and-others.md): the 2007 Uranian season with its two-model predictions and results, [Triton](https://en.wikipedia.org/wiki/Triton_(moon)), the 1985 to 1990 Pluto-Charon events, and [Phobos](https://en.wikipedia.org/wiki/Phobos_(moon)) and Deimos.

## What this topic changes for the pipeline

The pipeline gains a satellite ephemeris layer on top of the planetary one, delivered as SPK files consistent with DE440. The body-shape layer gains an oblate primary and a ring annulus with a radial optical-depth profile, and the shadow code must handle a partially transparent occulter. The event search gains a seasonal gate on the saturnicentric or uranocentric latitudes of the Earth and the Sun. The event list must carry an uncertainty from the comparison of two independent satellite ephemerides, because events can appear or vanish between models.
