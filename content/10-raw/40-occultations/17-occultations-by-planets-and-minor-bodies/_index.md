---
title: Occultations by planets and minor bodies
seo_title: Stellar Occultations by Asteroids, TNOs, Planets and Moons
description: How occultations of stars by asteroids, TNOs, planets and satellites are predicted and reduced, and how planet-planet occultations are found.
order: 17
status: working
updated: 2026-10-17
tags: [stellar-occultation, asteroid, tno, planets, gaia, sora, occult, mutual-occultation]
---

::: summary
- **The shadow of a body against a star is a cylinder.** Its width on the [fundamental plane](../../10-shared/01-foundations/besselian-elements.md) equals the body's diameter, and on the ground it widens as the diameter divided by the sine of the star's altitude [@mb-gomes-junior-2022-sora] [@mb-preston-faq].
- **Prediction is limited by astrometry, not geometry.** The path's 1-sigma lines sit one cross-track uncertainty outside each edge, and 1 milliarcsecond is 0.7253 km per astronomical unit of distance [@mb-tanga-delbo-2007] [@mb-sora-code].
- **[Gaia](https://en.wikipedia.org/wiki/Gaia_(spacecraft)) changed the error from hundreds of kilometres to fractions of a [path width](../../20-solar-eclipses-and-transits/03-global-circumstances/path-and-limits.md).** Occultation astrometry reduced against Gaia EDR3 fits orbits at about 10 milliarcseconds, against 30 to 50 with older catalogues [@mb-ferreira-2022] [@mb-dunham-rasc-2024-mb].
- **Reduction models diffraction, star size and exposure, then fits chords.** The light-curve model of SORA (Stellar Occultation Reduction and Analysis) and Herald's ellipse, circle and shape-model fits are the documented methods [@mb-gomes-junior-2022-sora] [@mb-herald-2020].
- **The method found rings and atmospheres.** Uranus's rings in 1977, [Pluto](https://en.wikipedia.org/wiki/Pluto)'s atmosphere in 1988, and rings around Chariklo, Haumea and Quaoar [@mb-elliot-1977] [@mb-meza-2019] [@mb-braga-ribas-2014] [@mb-ortiz-2017] [@mb-pereira-2023].
- **Planet-planet occultations are eclipse geometry with a planet as the source.** The last was Venus and Jupiter in 1818, and the next is the same pair in 2065 [@mb-gray-mutual] [@mb-bogan-mutual].
:::

## What this topic covers

This topic covers occultations of stars by bodies other than the Moon: asteroids, trans-Neptunian objects, Centaurs, the giant planets and their satellites, and the rare occultations of one planet by another. It gives the fundamental-plane geometry of the shadow path and the formulas that SORA and Herald's Occult-based reductions use. It quantifies the uncertainty budget from the star catalogue and the orbit before and after Gaia, and describes how light curves are modelled and chords fitted. It also records what the method has found and how the prediction services fit together. Lunar occultations are in [Lunar occultations](../13-lunar-occultations/_index.md).

## Notes in this topic

- [Prediction geometry and astrometry](prediction-geometry-and-astrometry.md): the cylinder shadow on the fundamental plane, the event search, the path and 1-sigma lines, the star and ephemeris [error budget](../../../20-reports/error-budget.md), Gaia and occultation astrometry, timing, and the software and services.
- [Light curves, chords and results](light-curves-chords-and-results.md): the diffraction, star-size and exposure model, sub-exposure timing, chord fitting with ellipses, circles and shape models, and the results for asteroids, TNOs and rings.
- [Planets, satellites and mutual planetary occultations](planets-satellites-and-mutual-planetary-occultations.md): SPICE-based predictions for the giant planets, [Titan](https://en.wikipedia.org/wiki/Titan_(moon)) and [Triton](https://en.wikipedia.org/wiki/Triton_(moon)), satellite astrometry from occultations, and the geometry and lists of planet-planet occultations.

## What this topic changes for the pipeline

The Besselian stage generalises: the source can be the Sun, a star at infinity or a planet, and the occulter can be the Moon, a minor body or a planet. For a star the shadow axis is fixed and the shadow radius is the body's radius. The pipeline gains three stages that eclipse work does not need: star-catalogue propagation with Gaia space motion, orbit covariance mapped to a cross-track uncertainty, and an inverse reduction from timed chords back to a size, shape and astrometric position.
