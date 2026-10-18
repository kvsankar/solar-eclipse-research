---
title: Open questions
description: Outstanding eclipse calculation questions, each tied to the paper, dataset or code needed to resolve it and its effect on the conclusions.
order: 6
status: working
updated: 2026-10-18
seo_title: Open Questions in Solar Eclipse Algorithms and Modelling
---

::: summary
- **The code behind the SVS maps is unpublished.** The paper's SPICE examples and released shapefiles provide public reference products. Observed contacts supply independent checks. A release would let the pipeline design be checked line by line [@svs-wright-young-2024].
- **The 2024 solar radius is unsettled by the data that could settle it.** The IOTA reductions of the 2023 and 2024 bead videos are not yet published, and the 2024 limit observations collected by the Besselian Elements team have no published reduction [@sun-iota-dunham-2024] [@svs-irwin-quaglia-2024-technical].
- **Some program inputs lack a complete public description.** Occult's installed help is needed for its input policy. The cited Solar Eclipse Maestro help does not specify its ephemeris and ΔT, and timeanddate's accuracy page does not name its ephemeris, $k$ or ΔT source. Jubier's client constants are documented in the software note [@sw-occult4] [@sw-jubier-sem] [@sw-timeanddate-accuracy].
- **Two standard texts are cited only through implementations**: Meeus's *Elements of Solar Eclipses 1951-2200* and chapter 11 of the 2013 Explanatory Supplement.
- **The end-to-end limb-and-terrain pipeline needs numerical validation.** Catalogue comparisons are available for Meeus's series and Kluepfel's Saros formula. The other stages need the named table, contact and polygon fixtures before they can claim product accuracy [@cat-meeus-1991-aa] [@cat-vangent-cycles].
:::

Each research group has its own section. Within the solar section the
questions are ranked by how much a different answer would move the design.

## Shared geometry and inputs

1. **Morrison, Stephenson, Hohenkerk and Zawilski 2021 and HMNAO Table
   S15.2020.** The current ΔT sigmas by year, to replace the 2004 rule in the
   error budget [@val-morrison-2021].

2. **Smith and colleagues 2010 and Barker and colleagues 2016.** The LOLA
   centre-of-figure vector and the SLDEM2015 mean radius are secondary
   values, reported secondhand and unconfirmed against the primary
   publications [@limb-smith-2010-lola] [@limb-barker-2016-sldem].

3. **A refraction number.** The cited sources do not quantify a general physical
   contact-time shift at Sun altitudes of 2 and 5 degrees. A specified
   atmosphere and ray-traced finite-distance geometry are needed before
   assigning a correction. A common angular remapping of both limbs alone
   preserves contact [@earth-es1992].

An experiment that requires no further sources:

- Compute from LDEM the mean limb radius averaged over position angle and
  libration, and compare with 1738.09 km ($k = 0.2725076$) and 1736.65 km
  ($k = 0.272281$). The sources compared here do not give this observer-and-libration average
  [@moon-williams-2013].

## Solar eclipses and transits

### Ranked by how much a different answer would move the design

1. **The SVS source code, or an author statement of the 2024 run's ΔT,
   ephemeris and Earth DEM resolution.** The paper names DE440 and the product
   pages name DE421; the ΔT is inside an Earth-orientation kernel; the map
   pixel size is unstated. The SVS API JSON for page 5123 would settle it.
   The `umbra_hi` polygons are reference products, and the
   stage 8 design is a reconstruction [@svs-wright-young-2024]
   [@svs-5123-2024-map].

2. **A published reduction of the 2024 edge observations.** Irwin and
   Quaglia's team collected limit observations in 2024, and IOTA's Solon,
   Maine recording is promised for the Journal for Occultation Astronomy.
   These reductions would help test the radius and detection conventions.
   A change of 0.05 arcseconds is about 100 m in the cited edge geometry,
   rather than a universal bound for every path limit
   [@val-dunham-iota-2024] [@svs-irwin-quaglia-2024-technical].

3. **A quantitative SVS-against-Irwin comparison.** Difference Irwin's 2024
   limit polylines, or the Besselian Elements app's output, against SVS
   `upath_hi` at fixed longitudes. Dunham measured the Jubier-to-Irwin offset
   at 0.7 km; the SVS-to-Irwin offset is inferred, not measured
   [@val-dunham-iota-2024] [@svs-2024-shapefiles-zip].

4. **Occult 4's help file.** It is distributed inside the Windows installer
   and holds the limb dataset, the datum radius, the solar radius default, the
   bead definition and the ΔT policy of the program the occultation community
   treats as the reference. Its 2 s offset from Irwin's model at Vale is
   unexplained without it [@sw-occult4] [@val-quaglia-2021].

5. **Herald 1983's error budget should be transcribed in full.** The 1992
   Supplement points to it for "the total effect and its components" of the
   limb. Transcribe its original components and compare them with the modern
   centre-of-figure and limb-sampling terms already tabulated in the error budget
   [@limb-herald-1983] [@val-es1992].

6. **Meeus, *Elements of Solar Eclipses 1951-2200*.** Its local-circumstances
   chapter, its sampling scheme, its treatment of nutation in μ and of the
   Sun's aberration. Photo Ephemeris and several ports rest on it, and it is
   cited only through them [@loc-meeus-elements-1989].

7. **Explanatory Supplement 2013, chapter 11.** Whether the μ convention, the
   ellipsoid, the recommended $k$ or the height formulas changed from 1992,
   and the exact text of equations 11.56 to 11.94 that Stellarium
   transcribes [@bes-usno-expsupp] [@glob-es2013].

8. **The undocumented NASA CSV columns** `PNS`, `UNS`, `NCN`, `nSer`,
   `nSeq`, `nJLE`, which appear to encode limits and Saros sequence
   [@cat-nasa-besselian-csv].

9. **Jubier's ephemeris and timeanddate's inputs.** Jubier's 2024 page
   carries the Five Millennium Canon coefficients with his own ΔT of 69.1 s,
   and the limb correction is computed server-side (Watts charts when the
   libration in latitude exceeds 1.6°, Kaguya otherwise, per the client
   code), but no page states the ephemeris behind the server. timeanddate's
   accuracy page names neither its ephemeris, its $k$ nor its ΔT source [@sw-jubier-2024-map]
   [@sw-jubier-calc-js] [@sw-timeanddate-accuracy].

### Transits of Mercury and Venus

- **Meeus's *Transits* (1989) and Espenak's statement of his transit
  constants.** The NASA transit catalogues rest on the first. The second would
  confirm the inferred 8.41 arcsecond Venus semidiameter
  [@tr-nasa-mercury-catalog] [@tr-eso-eis-b1].

### Experiments that require no further sources

- Reproduce one SVS 2024 `umbra_hi` polygon from SLDEM2015 with the limb test
  as written. This is the end-to-end check of stage 8, and the paper states
  the method in enough detail to perform it [@svs-2024-shapefiles-zip].
- Compare a LOLA-derived DSK silhouette with the profile-based test.
  `gfoclt_c` supports DSK paired with POINT and the ANY condition. It
  does not support a DSK Moon paired with an ellipsoid Sun for FULL or
  ANNULAR intervals. Finite-disc contacts need a separate limb-containment
  implementation. Use two ellipsoids with `gfoclt_c` for a smooth baseline
  [@loc-spice-gfoclt].
- Difference the SVS `umbra_hi` centre coordinates against Espenak's central
  line at the same instants to put the ephemeris-plus-ΔT difference in
  kilometres [@glob-nasa-path-2024].

## Lunar eclipses

- **The current Astronomical Almanac section on lunar eclipses.** It would
  show whether the Almanac still uses Chauvenet's 2 per cent enlargement
  [@lun-herald-sinnott-2014].

## Occultations

- **Occult's help file.** It would state Occult's lunar eclipse enlargement
  rule, its graze binning, its treatment of planet phase and its asteroid
  elements. Occult is closed source and its help ships only with the
  installer [@sw-occult4].
- **The current Astronomical Almanac section on occultations.** It would show
  whether the Almanac still prints occultations of planets and bright stars
  [@occ-es1992].

## Planetary satellites

- **Lieske 1998 (E5) in full, and the NOE technical notes.** These define the
  Galilean theories behind IMCCE's tables before and after 2015
  [@jup-imcce-phenjupiter-readme].
- **A source for the height in Jupiter's atmosphere at which an eclipse
  reaches half flux.** No source read states it.
- **A ring-transmission model for satellite eclipses at Saturn.** No public
  tool examined applies ring optical depth [@sats-nssdc-rings].
- **The current Astronomical Almanac section on satellite phenomena.** It
  would show which satellite theory its tables use.
