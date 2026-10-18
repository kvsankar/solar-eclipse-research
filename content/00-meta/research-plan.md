---
title: Scope and coverage
description: Seventeen research topics covering solar and lunar eclipses, occultations and transits, from finding events to local contact times and validation.
order: 1
status: working
updated: 2026-10-17
seo_title: Eclipse, Occultation and Transit Research: Scope and Coverage
---

::: summary
- **The question is how eclipse computational products are computed well enough to build one**, from the list of eclipses in a period, through world maps of the path, to the second at which totality begins for one observer standing on one hillside.
- **The reference standard is NASA SVS's 2024 work**, published as Wright and Young 2024: a lunar limb from LRO and SELENE topography, terrain under every observer, and a JPL ephemeris, traced through to the shape of the umbra on the ground.
- **All seventeen topics are covered.** Each rests on primary documents and public code, is recorded in raw notes with graded citations, and is carried into the reports.
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

## The seventeen topics

| Product | Question | Topic | Covered |
|---|---|---|---|
| Besselian elements | What is the fundamental plane and how are the elements derived from an ephemeris? | [Foundations](../10-raw/10-shared/01-foundations/_index.md) | Yes; formulas quoted from the 1961 and 1992 Supplements |
| The list of eclipses in a period | How are eclipses found and classified? | [Catalogues and types](../10-raw/20-solar-eclipses-and-transits/02-catalogs/_index.md) | Yes; Meeus's method tested against 221 catalogued eclipses |
| World maps | How are global circumstances computed from the elements? | [Global circumstances](../10-raw/20-solar-eclipses-and-transits/03-global-circumstances/_index.md) | Yes; every classic curve with its formula |
| Site tables | How are local circumstances computed? | [Local circumstances](../10-raw/20-solar-eclipses-and-transits/04-local-circumstances/_index.md) | Yes; checked against NASA's GPL JavaScript |
| Limb-corrected contacts, beads, true umbra shape | How does the lunar limb profile enter? | [Lunar limb profile](../10-raw/20-solar-eclipses-and-transits/05-lunar-limb/_index.md) | Yes; the DEM-to-profile algorithm and datasets |
| Path width and duration at the edge | Which solar radius, and what does the choice cost? | [Solar radius](../10-raw/20-solar-eclipses-and-transits/06-solar-radius/_index.md) | Yes; every value traced to its measurement |
| Every product | Which Earth figure, which time scale, how much ΔT uncertainty? | [Earth model and time scales](../10-raw/10-shared/07-earth-and-time/_index.md) | Yes; effects table with sizes |
| Every product | Which ephemeris, which lunar figure, which libration model? | [Lunar and solar model](../10-raw/10-shared/08-lunar-and-solar-model/_index.md) | Yes; kernel names and frames |
| Any product | What software and repositories exist, and how complete are they? | [Software and repositories](../10-raw/10-shared/09-software-and-repos/_index.md) | Yes; thirty repositories inventoried |
| Any product | How well do predictions match observation? | [Validation and error budget](../10-raw/20-solar-eclipses-and-transits/10-validation/_index.md) | Yes; the budget assembled and a five-level protocol |
| The reference standard | What exactly did SVS do for 2017, 2023 and 2024? | [NASA SVS and Ernie Wright](../10-raw/20-solar-eclipses-and-transits/11-svs-wright/_index.md) | Yes; the paper in full, with the datasets inventoried |
| Lunar eclipse contacts and maps | How are lunar eclipses computed, and how large is the Earth's shadow? | [Lunar eclipses](../10-raw/30-lunar-eclipses/_index.md) | Yes; three enlargement rules with constants, Herald and Sinnott 2014 read in full |
| Occultation times and graze lines | How are occultations of stars and planets by the Moon computed and reduced? | [Lunar occultations](../10-raw/40-occultations/13-lunar-occultations/_index.md) | Yes; the 1961 Supplement's method, the archive and its error budget |
| Transit contacts | How are transits of Mercury and Venus computed? | [Transits](../10-raw/20-solar-eclipses-and-transits/14-transits/_index.md) | Yes; contact solution, local formulas and predictor comparison |
| Jovian satellite phenomena | How are eclipses, occultations, transits and mutual events of the Galilean satellites computed? | [Jupiter's satellites](../10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) | Yes; theories by version and the classical two-cone method |
| Saturnian and outer satellite phenomena | How are Saturn's satellite phenomena, ring geometry and mutual events computed? | [Saturn and outer satellites](../10-raw/50-planetary-satellites/16-saturn-and-outer-satellites/_index.md) | Yes; theories, ring model and mutual-event accuracy |
| Minor-body occultation paths | How are occultations of stars by asteroids, TNOs and planets predicted and reduced? | [Planets and minor bodies](../10-raw/40-occultations/17-occultations-by-planets-and-minor-bodies/_index.md) | Yes; SORA's paper checked against its code |

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

- Transits seen from other planets, except a short section on Phobos and
  Deimos seen from Mars in the Saturn and outer satellites topic. Exoplanet
  transits and occultations by artificial satellites are also out of scope.
- Eclipse weather, photography, safety and travel.
- Historical eclipse identification as a discipline, except where it validates
  a ΔT model.

## What would change the conclusions

Ranked in [open questions](../20-reports/open-questions.md). The first three:
the SVS source code or a statement of its 2024 constants; a published
reduction of the 2024 edge observations, which would fix the default solar
radius; and a measured SVS-against-Irwin limit offset.
