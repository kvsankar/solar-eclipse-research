---
title: Computing Solar Eclipses: Calculation and Algorithms
description: Solar eclipse calculation and prediction algorithms, with formulas, Besselian elements, contact times, lunar limb data and accuracy comparisons.
status: working
updated: 2026-09-30
seo_title: Solar Eclipse Calculation: Algorithms, Data and Accuracy
---

![Everything this site computes is the geometry behind this photograph, and
the hardest parts of it are at the edges. The pink prominences ring a limb
that is not a circle: lunar topography moves a path limit by 1 to 3 km, and
the solar radius that sets where the corona begins is still disputed at a
third of an arcsecond. Totality of 1999 August 11, photographed from France
by Luc Viatour / [lucnix.be](https://lucnix.be), CC BY-SA 3.0
[@glob-nasa-google-2024] [@val-besselian-maps-accuracy].](img/totality-1999-viatour.jpg){.hero}

This guide covers solar eclipse calculation algorithms, their formulas,
constants, datasets and validation evidence. Start with
[how to calculate a solar eclipse](05-primer/how-an-eclipse-is-computed.md)
for the geometry, or follow the
[eclipse calculation pipeline](20-reports/pipeline-design.md) for the
implementation stages. The
[software comparison](10-raw/09-software-and-repos/_index.md) covers published
eclipse calculators and open-source libraries.

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
- **Bessel's method underlies classical eclipse tables and maps.** Direct topocentric calculations and raster limb tests provide alternative routes. Predictors differ in their algorithms as well as their constants and data [@bes-es1961] [@bes-quaglia-2021] [@svs-wright-young-2024].
- **Solar radius, lunar limb and terrain can move a path limit by hundreds of metres to kilometres.** Their effects depend on the geometry and on which corrections the predictor includes [@val-quaglia-2021] [@val-svs-4517].
- **Wright and Young 2024 describe NASA SVS's terrain-aware raster method.** It uses an 18,000-element lunar limb from LRO and Kaguya (SELENE) topography. The paper is open access, while the surveyed public releases contain data rather than the generating code [@svs-wright-young-2024] [@svs-2024-shapefiles-zip].
- **The adopted solar radius remains a modelling choice.** Flash-spectrum and light-curve studies infer values around 959.95 to 960.01 arcseconds. At Stephenville in 2024, predictions of 24.5 s and 12.9 s bracketed the observed 13.7 s. That comparison changes several implementation inputs, so it does not isolate the radius contribution [@sun-quaglia-2021] [@sun-lamy-2015] [@val-besselian-maps-accuracy].
- **The surveyed open implementations do not derive limb-corrected path limits.** Stellarium and NASA's JavaScript provide smooth-Moon products. The repository survey also includes a LOLA-based bead construction for a single eclipse [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-repo-eclipse-2026-rojas].
:::

## Start here

- [Executive summary](20-reports/executive-summary.md): the findings that
  carry the most weight.
- [Eclipse calculation algorithms and pipeline](20-reports/pipeline-design.md): nine stages with formulas,
  constants, outputs and validation cases.
- [Error budget](20-reports/error-budget.md): every input ranked in seconds
  and metres.
- [Reading list](20-reports/reading-list.md): the papers, code and datasets in
  order.
- [Primer](05-primer/_index.md): start here if you have not computed an
  eclipse before.

## The raw notes

Eleven topics, each a folder of notes with quoted formulas, graded citations
and the questions it could not close.

| Topic | What it settles |
|---|---|
| [Foundations](10-raw/01-foundations/_index.md) | The eight Besselian elements, the equations from ephemeris to elements, the constants and their provenance |
| [Catalogues and types](10-raw/02-catalogs/_index.md) | How eclipses are enumerated and classified, and which catalogues to use as fixtures |
| [Global circumstances](10-raw/03-global-circumstances/_index.md) | Central line, limits, outlines, rise and set curves, durations, and the data products |
| [Local circumstances](10-raw/04-local-circumstances/_index.md) | Contact times, magnitude, obscuration and position angles at one site, and the corrections |
| [Lunar limb profile](10-raw/05-lunar-limb/_index.md) | Watts, Kaguya and LOLA, the DEM-to-profile geometry, and Baily's beads |
| [Solar radius](10-raw/06-solar-radius/_index.md) | Every value in circulation, what each measures, and the effect on products |
| [Earth model and time](10-raw/07-earth-and-time/_index.md) | The ellipsoid, terrain and geoid, ΔT models, refraction, frames |
| [Lunar and solar model](10-raw/08-lunar-and-solar-model/_index.md) | The DE ephemerides, centre of mass against figure, $k$, libration |
| [Software and repositories](10-raw/09-software-and-repos/_index.md) | Four production lineages, the open libraries, thirty repositories, the datasets |
| [Validation](10-raw/10-validation/_index.md) | Observed against predicted, predictor disagreements, the error budget and protocol |
| [NASA SVS and Ernie Wright](10-raw/11-svs-wright/_index.md) | The 2024 paper, the SVS products and data, and the comparison with other predictors |

## Reference

- [Glossary](05-primer/glossary.md): the jargon, defined standalone, with the
  formula where a term is really a quantity.
- [Open questions](20-reports/open-questions.md): what this corpus could not
  close, each naming the artefact that would close it.
- [Method and source policy](00-meta/method-and-sources.md): the grades, and
  what each one is allowed to prove.
