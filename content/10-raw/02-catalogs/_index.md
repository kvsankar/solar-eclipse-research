---
title: Catalogues and types
description: How every solar eclipse in a period is found, how each one is typed as partial, annular, total or hybrid, and which canons and data products carry the results.
order: 2
status: working
updated: 2026-09-15
tags: [catalogues, canon, saros, eclipse-types, enumeration]
---

::: summary
- **Meeus's series finds all of them.** Chapter 52 of the 1991 *Astronomical Algorithms* needs no ephemeris, finds all 221 eclipses of 1951 to 2050 and types every one correctly, with a worst error of 1.11 min in the time of greatest eclipse [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii].
- **The NASA files are the fixture.** One ASCII catalogue of 11,898 rows and one CSV of Besselian polynomial elements for the same eclipses, both from the Five Millennium Canon, are the acceptance test set for any enumerator [@cat-nasa-5mkse-ascii] [@cat-nasa-besselian-csv].
- **The Five Millennium Catalogue uses a pair of lunar radii.** $k = 0.2724880$ for all partial and penumbral contacts and $k = 0.272281$ for all umbral and antumbral ones. The single IAU value 0.2725076, which IMCCE uses, misclassifies beaded annular eclipses as total [@cat-espenak-meeus-2009-catalog] [@cat-imcce-parametres].
- **Type is decided by the umbral radius at the surface, not on the fundamental plane.** Evaluating it at greatest eclipse and at both ends of the central line is what separates the three hybrid classes and the 94 non-central eclipses of five millennia [@cat-espenak-meeus-2009-catalog] [@cat-swisseph-swecl].
- **ΔT, not the ephemeris, sets the accuracy floor.** The catalogue's own statement is that the lunar ephemeris stays below map resolution even at $-1999$, while the standard error in ΔT exceeds 265 s before +0001 and after +2300, which is more than a degree of longitude [@cat-espenak-meeus-2006-canon].
:::

## What this topic covers

The three questions a developer meets before any path or contact time is
computed. Which new moons produce an eclipse at all, by a closed-form series, an
ephemeris minimum-distance search or a full Besselian computation. What type
each one is, from the inequalities in $\gamma$ and the umbral radius, including
the central, non-central and hybrid classes and the meaning of every column a
catalogue prints. And where a trustworthy list already exists, in what format,
with its ephemeris, its ΔT model and its lunar radius stated.

## Notes in this topic

- [Enumerating eclipses](enumerating-eclipses.md): the Meeus approximate
  search, the ephemeris-based search, the method behind the Five Millennium
  Canon, Saros and Inex numbering, and the accuracy limits set by ΔT.
- [Types and classification](types-and-classification.md): the inequalities in
  $\gamma$ and $u$ that separate partial, annular, total, hybrid, central and
  non-central eclipses, and the definition of every quantity a catalogue lists.
- [Canons and data products](canons-and-data-products.md): NASA GSFC, IMCCE,
  HMNAO, EclipseWise, Jubier, Occult, machine-readable files, open-source
  enumerators, and the older canons from Oppolzer to Mucke and Meeus.

## What this topic changes for the pipeline

Enumeration is solved and cheap, so the pipeline runs a Meeus pre-filter into a
Besselian stage rather than building a search of its own. Classification is not
a post-processing label: it depends on $k$ and on where along the path the
umbral radius is evaluated, so the enumeration stage carries only a provisional
type and the final type is assigned in the Besselian stage. Every exported row
carries a provenance record naming the ephemeris, the ΔT model and the $k$ pair,
because the only widely mirrored element set carries no statement of its own
constants.
