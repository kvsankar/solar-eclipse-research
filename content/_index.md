---
title: Computing Eclipses and Occultations
description: Solar eclipse calculation algorithms: formulas, Besselian elements, contact times and lunar limb data, extended to lunar eclipses, occultations and transits.
status: working
updated: 2026-10-18
seo_title: Eclipse, Occultation and Transit Calculation Algorithms
---

![The two cases of one shadow geometry. Left: a total solar eclipse,
1999 August 11, by Luc Viatour / [lucnix.be](https://lucnix.be),
CC BY-SA 3.0. Top centre: the transit of Venus, 2012 June 5-6, by
NASA/Goddard Space Flight Center/SDO, public domain. Top right: Saturn just
before the Moon occults it, 2024 August 21, by Sebas FL, CC BY-SA 4.0. These
three are the hidden case, where the observer stands in the shadow. Bottom
centre: a total lunar eclipse, 2026 March 3, by NASA/Michael DeMocker,
public domain. Bottom right: the shadows of Io, Ganymede and Callisto on
Jupiter, 2004 March 28, by
NASA, ESA, and E. Karkoschka (University of Arizona), public domain. These
two are the darkened case, where another body stands in the shadow. The
collage is published under CC BY-SA 4.0.](img/collage-v1.jpg){.hero}

Every event on this site is a body casting a shadow, and what matters is who
stands in it. When the observer stands in the shadow, the source is hidden:
an occultation, a transit or a solar eclipse. When another body stands in
it, that body goes dark for everyone: a lunar eclipse or the eclipse of a
planet's satellite. This site sets out how each event is computed, with the
formulas, constants, datasets and validation evidence. Solar eclipses are
covered in most depth. The [primer](05-primer/how-eclipses-occultations-and-transits-are-computed.md)
explains the two cases with pictures and animations.

The [solar eclipse pipeline](20-reports/pipeline-design.md) gives the
implementation stages, and
[extending the pipeline to other events](20-reports/other-events.md) sets out
what each other event adds. The
[software comparison](10-raw/10-shared/09-software-and-repos/_index.md) covers
published calculators and open-source libraries.

[Research and website source on GitHub](https://github.com/kvsankar/solar-eclipse-research).

Published predictors can disagree at a path limit because they use different
models and inputs [@val-quaglia-2021] [@val-besselian-maps-accuracy]. This site sets out
what a developer needs to know to compute every product, from the list of
eclipses in a century to the second totality begins on one hillside, and to
know how good the result is: the algorithm, the constants and where each one
came from, the datasets, the published implementations, and what is still
unsettled.

The source policy prioritises primary documents and published code.
Equations carry their constants, and substantive claims carry graded
citations. Follow the cited artefact before relying on a number.
[Method and source policy](00-meta/method-and-sources.md) defines the grades
and the evidence each one provides.

::: summary
- **Hidden: the observer stands in the shadow.** Occultations, transits and solar eclipses depend on where the observer stands. Their dominant inputs are the lunar limb, the star's and the body's positions, and the solar and planetary radii [@limb-occult-accuracy-2016] [@mb-ferreira-2022] [@tr-eso-eis-b1].
- **Darkened: another body stands in the shadow.** Lunar and satellite eclipses look the same from everywhere. Their dominant inputs are the enlargement of the Earth's shadow and the satellite ephemeris [@lun-herald-sinnott-2014] [@sats-arlot-2012-phesat09].
- **Solar eclipses are covered in most depth.** Bessel's method underlies classical eclipse tables and maps. Direct topocentric calculations and raster limb tests provide alternative routes. Predictors differ in their algorithms as well as their constants and data [@bes-es1961] [@bes-quaglia-2021] [@svs-wright-young-2024].
- **Solar radius, lunar limb and terrain can move a path limit by hundreds of metres to kilometres.** Their effects depend on the geometry and on which corrections the predictor includes [@val-quaglia-2021] [@val-svs-4517].
- **Wright and Young 2024 describe NASA SVS's terrain-aware raster method.** It uses an 18,000-element lunar limb from LRO and Kaguya (SELENE) topography. The paper is open access, while the surveyed public releases contain data rather than the generating code [@svs-wright-young-2024] [@svs-2024-shapefiles-zip].
- **The adopted solar radius remains a modelling choice.** Flash-spectrum and light-curve studies infer values around 959.95 to 960.01 arcseconds. At Stephenville in 2024, predictions of 24.5 s and 12.9 s bracketed the observed 13.7 s. That comparison changes several implementation inputs, so it does not isolate the radius contribution [@sun-quaglia-2021] [@sun-lamy-2015] [@val-besselian-maps-accuracy].
- **The surveyed open implementations do not derive limb-corrected path limits.** Stellarium and NASA's JavaScript provide smooth-Moon products. The repository survey also includes a LOLA-based bead construction for a single eclipse [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-repo-eclipse-2026-rojas].
:::

## Start here

- [Primer](05-primer/_index.md): start here if you have not computed an
  eclipse before.
- [Executive summary](20-reports/executive-summary.md): the findings that
  carry the most weight, for both cases and then for solar eclipses.
- [Solar eclipse pipeline](20-reports/pipeline-design.md): nine stages with
  formulas, constants, outputs and validation cases.
- [Extending the pipeline to other events](20-reports/other-events.md): how
  the same geometry serves the other events, and what each one adds.
- [Solar eclipse error budget](20-reports/error-budget.md): every input ranked
  in seconds and metres.
- [Reading list](20-reports/reading-list.md): the papers, code and datasets for
  each research group, in order.

## The research notes

Seventeen topics in five groups, each a folder of notes with quoted formulas,
graded citations and the questions it could not close.

### Shared geometry and inputs

What every event needs: the geometry, the Earth, time, the ephemerides and the software. [Group overview](10-raw/10-shared/_index.md).

| Topic | What it settles |
|---|---|
| [Foundations](10-raw/10-shared/01-foundations/_index.md) | The eight Besselian elements, the equations from ephemeris to elements, the constants and their provenance |
| [Earth model and time](10-raw/10-shared/07-earth-and-time/_index.md) | The ellipsoid, terrain and geoid, ΔT models, refraction, frames |
| [Lunar and solar model](10-raw/10-shared/08-lunar-and-solar-model/_index.md) | The DE ephemerides, centre of mass against figure, $k$, libration |
| [Software and repositories](10-raw/10-shared/09-software-and-repos/_index.md) | Four production lineages, the open libraries, thirty repositories, the datasets |

### Solar eclipses and transits

The hidden case with the Sun as the source, covered in most depth. [Group overview](10-raw/20-solar-eclipses-and-transits/_index.md).

| Topic | What it settles |
|---|---|
| [Catalogues and types](10-raw/20-solar-eclipses-and-transits/02-catalogs/_index.md) | How eclipses are enumerated and classified, and which catalogues to use as fixtures |
| [Global circumstances](10-raw/20-solar-eclipses-and-transits/03-global-circumstances/_index.md) | Central line, limits, outlines, rise and set curves, durations, and the data products |
| [Local circumstances](10-raw/20-solar-eclipses-and-transits/04-local-circumstances/_index.md) | Contact times, magnitude, obscuration and position angles at one site, and the corrections |
| [Lunar limb profile](10-raw/20-solar-eclipses-and-transits/05-lunar-limb/_index.md) | Watts, Kaguya and LOLA, the DEM-to-profile geometry, and Baily's beads |
| [Solar radius](10-raw/20-solar-eclipses-and-transits/06-solar-radius/_index.md) | Every value in circulation, what each measures, and the effect on products |
| [Validation](10-raw/20-solar-eclipses-and-transits/10-validation/_index.md) | Observed against predicted, predictor disagreements, the error budget and protocol |
| [NASA SVS and Ernie Wright](10-raw/20-solar-eclipses-and-transits/11-svs-wright/_index.md) | The 2024 paper, the SVS products and data, and the comparison with other predictors |
| [Transits of Mercury and Venus](10-raw/20-solar-eclipses-and-transits/14-transits/_index.md) | Enumeration, transit elements, contacts and local reduction formulas, the black drop and the radii |

### Lunar eclipses

The darkened case with the Moon in the Earth's shadow.

| Topic | What it settles |
|---|---|
| [Lunar eclipses](10-raw/30-lunar-eclipses/_index.md) | The lunar elements and six contacts, the three shadow enlargement rules, crater timings and brightness |

### Occultations

The hidden case with a star or a planet as the source. [Group overview](10-raw/40-occultations/_index.md).

| Topic | What it settles |
|---|---|
| [Lunar occultations](10-raw/40-occultations/13-lunar-occultations/_index.md) | Occultations of stars and planets by the Moon, grazes, star catalogues and the reduction of timings |
| [Occultations by planets and minor bodies](10-raw/40-occultations/17-occultations-by-planets-and-minor-bodies/_index.md) | Asteroid and TNO occultation paths, Gaia astrometry, light curves and chords, and planet-planet occultations |

### Planetary satellites

Both cases at Jupiter, Saturn and beyond. [Group overview](10-raw/50-planetary-satellites/_index.md).

| Topic | What it settles |
|---|---|
| [Jupiter's satellites](10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) | Eclipses, occultations, transits and shadow transits of the Galilean satellites, theories and mutual events |
| [Saturn and the outer satellites](10-raw/50-planetary-satellites/16-saturn-and-outer-satellites/_index.md) | Saturn's ring geometry, satellite theories and phenomena, and mutual events at Uranus and Pluto |

## Reference

- [Glossary](05-primer/glossary.md): the jargon, defined standalone, with the
  formula where a term is really a quantity.
- [Open questions](20-reports/open-questions.md): what this corpus could not
  close, each naming the artefact that would close it.
- [Method and source policy](00-meta/method-and-sources.md): the grades, and
  what each one is allowed to prove.
