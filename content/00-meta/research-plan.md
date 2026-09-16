---
title: Scope and coverage
description: The eleven topics, the question each answers, the standard of detail they are held to, and the limits of the evidence behind them.
order: 1
status: working
updated: 2026-09-16
---

::: summary
- **The question is how eclipse computational products are computed well enough to build one**, from the list of eclipses in a period, through world maps of the path, to the second at which totality begins for one observer standing on one hillside.
- **The reference standard is NASA SVS's 2024 work**, published as Wright and Young 2024: a lunar limb from LRO and SELENE topography, terrain under every observer, and a JPL ephemeris, traced through to the shape of the umbra on the ground.
- **All eleven topics are covered.** Each rests on primary documents and public code, is recorded in raw notes with graded citations, and is carried into the reports.
- **The gaps are named artefacts**: the SVS code, Occult's help file, Meeus's *Elements*, the 2013 Supplement's eclipse chapter, and the unpublished 2024 edge reductions.
:::

## The question

Eclipse predictions are published by a handful of people and programs: Fred
Espenak's NASA and EclipseWise tables, Xavier Jubier's interactive maps, Dave
Herald's Occult, Ernie Wright's NASA SVS visualisations, and commercial sites
such as timeanddate. They agree to within a few hundred metres at the path
edge and a few seconds at a site, and the places where they disagree are the
places where the interesting modelling decisions live: the radius of the Sun,
the mountains on the Moon's limb, the height of the observer, and the
unpredictable rotation of the Earth.

The subject is **what a developer needs to know to compute every one of
these products**, and to know how good the result is, organised by product
from coarse to fine.

## The eleven topics

| Product | Question | Topic | Covered |
|---|---|---|---|
| Besselian elements | What is the fundamental plane and how are the elements derived from an ephemeris? | [Foundations](../10-raw/01-foundations/_index.md) | Yes; formulas quoted from the 1961 and 1992 Supplements |
| The list of eclipses in a period | How are eclipses found and classified? | [Catalogues and types](../10-raw/02-catalogs/_index.md) | Yes; Meeus's method tested against 221 catalogued eclipses |
| World maps | How are global circumstances computed from the elements? | [Global circumstances](../10-raw/03-global-circumstances/_index.md) | Yes; every classic curve with its formula |
| Site tables | How are local circumstances computed? | [Local circumstances](../10-raw/04-local-circumstances/_index.md) | Yes; checked against NASA's GPL JavaScript |
| Limb-corrected contacts, beads, true umbra shape | How does the lunar limb profile enter? | [Lunar limb profile](../10-raw/05-lunar-limb/_index.md) | Yes; the DEM-to-profile algorithm and datasets |
| Path width and duration at the edge | Which solar radius, and what does the choice cost? | [Solar radius](../10-raw/06-solar-radius/_index.md) | Yes; every value traced to its measurement |
| Every product | Which Earth figure, which time scale, how much ΔT uncertainty? | [Earth model and time scales](../10-raw/07-earth-and-time/_index.md) | Yes; effects table with sizes |
| Every product | Which ephemeris, which lunar figure, which libration model? | [Lunar and solar model](../10-raw/08-lunar-and-solar-model/_index.md) | Yes; kernel names and frames |
| Any product | What software and repositories exist, and how complete are they? | [Software and repositories](../10-raw/09-software-and-repos/_index.md) | Yes; thirty repositories inventoried |
| Any product | How well do predictions match observation? | [Validation and error budget](../10-raw/10-validation/_index.md) | Yes; the budget assembled and a five-level protocol |
| The reference standard | What exactly did SVS do for 2017, 2023 and 2024? | [NASA SVS and Ernie Wright](../10-raw/11-svs-wright/_index.md) | Yes; the paper in full, with the datasets inventoried |

## The standard of detail

Each raw note is written for someone who will implement from it. That sets
the bar: formulas quoted rather than described, constants named with their
provenance, datasets named with their product identifiers and download
locations, and code cited by file when the program is public.

## What is quoted rather than reproduced

- **Only the enumeration is independently reproduced.** Meeus's series and
  Kluepfel's Saros formula are implemented from their quoted constants and
  checked against the NASA catalogue. No Besselian, limb or terrain result is
  reproduced independently; each such number is quoted from its source. The
  [reading list](../20-reports/reading-list.md) names the reference cases.
- **Two standard texts are cited only at second hand**: Meeus's *Elements of
  Solar Eclipses 1951-2200* and chapter 11 of the 2013 Explanatory
  Supplement, both through implementations that transcribe them.
- **Three sources are unavailable**: Occult's help file, distributed only
  inside the Windows installer; Solar Eclipse Maestro's statement of its
  ephemeris and ΔT, which its help pages omit; and timeanddate's ephemeris,
  $k$ and ΔT source, which its accuracy page does not name.
- **NASA SVS pages are cited from Wayback Machine snapshots**, the host being
  unreachable. Snapshot dates are in the reference notes.

## What is deliberately out of scope

- Lunar eclipses, transits and occultations, except where the same machinery
  is reused and the source says so.
- Eclipse weather, photography, safety and travel.
- Historical eclipse identification as a discipline, except where it validates
  a ΔT model.

## What would change the conclusions

Ranked in [open questions](../20-reports/open-questions.md). The first three:
the SVS source code or a statement of its 2024 constants; a published
reduction of the 2024 edge observations, which would fix the default solar
radius; and a measured SVS-against-Irwin limit offset.
