---
title: Method and source policy
description: How this eclipse calculation guide grades papers, official datasets and software documentation, and records formulas and constants.
order: 2
status: working
updated: 2026-09-15
seo_title: Eclipse Calculation Sources: Evidence and Citation Policy
---

::: summary
- **Every claim carries a graded citation.** The grade is rendered next to each reference so a reader can see whether a number came from a refereed paper, a NASA technical report, or a program author's own documentation.
- **Code is a primary source for what a program does.** Where a program is public, the note cites the file that computes the quantity.
- **Formulas are quoted, not paraphrased.** A note that says "the contact times are found iteratively" without the iteration is not finished.
- **Negative findings are recorded as findings, with their scope.** That a
  thing does not exist, or is not published, is a result a reader can use.
:::

## The grades, as applied here

| Grade | Used for | Example |
|---|---|---|
| `peer-reviewed` | Refereed papers, the Explanatory Supplement to the [Astronomical Almanac](https://en.wikipedia.org/wiki/Astronomical_Almanac), almanac-office publications | Stephenson, Morrison and Hohenkerk on [ΔT](../10-raw/10-shared/07-earth-and-time/delta-t-and-earth-rotation.md); Lamy and colleagues on the eclipse [solar radius](../10-raw/20-solar-eclipses-and-transits/06-solar-radius/solar-radius-values.md) |
| `primary` | NASA, [USNO](https://en.wikipedia.org/wiki/United_States_Naval_Observatory), [IMCCE](https://www.imcce.fr/), JPL, [IERS](https://www.iers.org/) and PDS publications, technical reports and data products | The [Five Millennium Canon](../10-raw/20-solar-eclipses-and-transits/02-catalogs/canons-and-data-products.md) technical publication; a [LOLA](https://lola.gsfc.nasa.gov/) digital elevation model release; a JPL DE ephemeris memo |
| `preprint` | [arXiv](https://arxiv.org/) and other unrefereed manuscripts | Ephemeris comparison preprints |
| `company` | A program author's documentation of their own program or product | [Occult](../10-raw/10-shared/09-software-and-repos/commercial-and-institutional-tools.md)'s help pages; Solar Eclipse Maestro's feature list; an [SVS](../10-raw/20-solar-eclipses-and-transits/11-svs-wright/_index.md) page describing its own method; a repository README |
| `trade` | Practitioner writing carrying data or method, outside a refereed venue | An [IOTA](https://occultations.org/) member's mailing-list analysis of edge observations |
| `survey` | Aggregated or sampled data with a stated method | A comparison table of predictors compiled by a third party |
| `vendor` | A supplier describing a product it sells, where the claim is promotional | An app store listing's accuracy claim |
| `unsourced` | Forums, undocumented repositories, encyclopaedias | A Reddit thread; a GitHub repository with no stated method |

## The rules

**A program's documentation proves what the program does, never how accurate
it is.** Accuracy comes from comparison with observation, from a refereed
paper, or from an explicit [error budget](../20-reports/error-budget.md).

**A formula is quoted with its symbols defined and its constants named.**
Eclipse computation mixes units: Earth equatorial radii on the fundamental
plane, arcseconds on the sky, kilometres on the ground, and three time scales.
A note that leaves the unit implicit has left the error in.

**An ephemeris, a ΔT model and a limb dataset are versioned, and the version
is stated.** "DE440", "LDEM_128", "Espenak and Meeus polynomial" are claims;
"a JPL ephemeris" is not.

**The algorithm and the implementation are distinguished.** [Chauvenet](https://en.wikipedia.org/wiki/William_Chauvenet), the
Explanatory Supplement and [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) give algorithms. [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak), Jubier, Herald and
Wright chose constants and data. When two programs disagree, the note says
which choice explains the difference.

**Negative findings are findings.** "No open-source implementation of a
limb-corrected path edge exists" is quotable once its scope is stated.

**The site states positions, not revisions.** When a finding supersedes an
earlier one, the page is rewritten.
