---
title: Computing Solar Eclipses
description: How solar eclipse computational products are computed, from catalogues to contact times, at the depth of NASA SVS's 2024 work.
status: working
updated: 2026-09-16
---

Solar eclipse predictions are published by a handful of people and programs,
and they agree to a few hundred metres at the edge of the path. The places
where they disagree are where the modelling decisions live. This site sets out
what a developer needs to know to compute every product, from the list of
eclipses in a century to the second totality begins on one hillside, and to
know how good the result is: the algorithm, the constants and where each one
came from, the datasets, the published implementations, and what is still
unsettled.

This site was researched and written with Anthropic's Claude — every note,
report and figure in the tree below. It was built to a fixed method: primary
documents and published code in preference to secondary coverage, formulas
quoted with their constants rather than paraphrased, negative findings
recorded as findings, and a graded citation on every substantive claim. The
grade is rendered beside each reference, so what a number rests on is visible
where it is used. That is the check on the text, and it is the one worth
using: follow a citation before relying on a figure here.
[Method and source policy](00-meta/method-and-sources.md) states the rules in
full.

::: summary
- **One algorithm underlies every eclipse product**: Bessel's fundamental-plane method, fully stated in the 1961 Explanatory Supplement. Predictors differ in their constants and data, not their mathematics [@bes-es1961].
- **Three inputs decide the edge of the path**: the solar radius, the lunar limb profile, and terrain. Each is worth 0.6 to 3 km at a limit. The ephemeris is worth under a metre [@val-quaglia-2021] [@moon-park-2021].
- **The state of the art is Wright and Young 2024**, NASA SVS's raster method with an 18,000-element lunar limb from LRO and SELENE topography and every observer on the terrain. It is published, open access, and has no public code [@svs-wright-young-2024].
- **The solar radius is the unresolved constant.** The 1891 value of 959.63″ that almost everyone uses is a third of an arcsecond smaller than what eclipse observations measure. At one 2024 edge site that difference was the last 11 s of a 65 s smooth-Moon prediction that observation cut to 13.7 s [@val-besselian-maps-accuracy].
- **No open-source code computes a limb-corrected path edge.** Stellarium and NASA's JavaScript cover the smooth-Moon problem completely [@sw-stellarium-sec-cpp].
:::

## Start here

- [Executive summary](20-reports/executive-summary.md): the findings that
  carry the most weight.
- [Pipeline design](20-reports/pipeline-design.md): nine stages with formulas,
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
