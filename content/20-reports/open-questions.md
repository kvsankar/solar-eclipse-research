---
title: Open questions
description: The artefacts that would most change the conclusions, ranked, each naming the document, dataset or line of code to obtain.
order: 5
status: working
updated: 2026-09-16
---

::: summary
- **The code behind the SVS maps is unpublished.** The paper's ten lines of SPICE calls and the released shapefiles are the only ground truth. A release would let the pipeline design be checked line by line [@svs-wright-young-2024].
- **The 2024 solar radius is unsettled by the data that could settle it.** The IOTA reductions of the 2023 and 2024 bead videos are not yet published, and the 2024 limit observations collected by the Besselian Elements team have no published reduction [@sun-iota-dunham-2024] [@svs-irwin-quaglia-2024-technical].
- **Three sources are unavailable**: Occult's help file, distributed only inside the Windows installer; Solar Eclipse Maestro's statement of its ephemeris and ΔT, which its help pages omit; and timeanddate's ephemeris, $k$ and ΔT source, which its accuracy page does not name. Jubier's browser calculator is public, and its constants are in the software note.
- **Two standard texts are cited only through implementations**: Meeus's *Elements of Solar Eclipses 1951-2200* and chapter 11 of the 2013 Explanatory Supplement.
- **Only the enumeration is independently reproduced.** Meeus's series and Kluepfel's Saros formula are implemented and checked against the NASA catalogue; every Besselian, limb and terrain number is quoted from its source. The first act of any implementation is to reproduce the reference cases.
:::

## Ranked by how much a different answer would move the design

1. **The SVS source code, or an author statement of the 2024 run's ΔT,
   ephemeris and Earth DEM resolution.** The paper names DE440 and the product
   pages name DE421; the ΔT is inside an Earth-orientation kernel; the map
   pixel size is unstated. The SVS API JSON for page 5123 would settle it.
   Until then the `umbra_hi` polygons are the ground truth and the
   stage 8 design is a reconstruction [@svs-wright-young-2024]
   [@svs-5123-2024-map].

2. **A published reduction of the 2024 edge observations.** Irwin and
   Quaglia's team collected limit observations in 2024, and IOTA's Solon,
   Maine recording is promised for the Journal for Occultation Astronomy.
   Either would decide whether 959.95″ or a value nearer 960.0″ is the
   default, which moves every edge-mode limit by up to 100 m
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
   limb. The centre-of-figure and limb-sampling terms remain unquantified
   [@limb-herald-1983] [@val-es1992].

6. **Meeus, *Elements of Solar Eclipses 1951-2200*.** Its local-circumstances
   chapter, its sampling scheme, its treatment of nutation in μ and of the
   Sun's aberration. Photo Ephemeris and several ports rest on it, and it is
   cited only through them [@loc-meeus-elements-1989].

7. **Explanatory Supplement 2013, chapter 11.** Whether the μ convention, the
   ellipsoid, the recommended $k$ or the height formulas changed from 1992,
   and the exact text of equations 11.56 to 11.94 that Stellarium
   transcribes [@bes-usno-expsupp] [@glob-es2013].

8. **Morrison, Stephenson, Hohenkerk and Zawilski 2021 and HMNAO Table
   S15.2020.** The current ΔT sigmas by year, to replace the 2004 rule in the
   error budget [@val-morrison-2021].

9. **Smith and colleagues 2010 and Barker and colleagues 2016.** The LOLA
   centre-of-figure vector and the SLDEM2015 mean radius are secondary
   values, unconfirmed against the primary publications, neither of which is
   accessible [@limb-smith-2010-lola] [@limb-barker-2016-sldem].

10. **A refraction number.** No published source quantifies the effect of
    standard refraction on first and fourth contact at Sun altitudes of 2° and 5° in
    seconds. A ray-traced test case would replace the bound derived in
    the Earth-and-time note [@earth-es1992].

11. **The undocumented NASA CSV columns** `PNS`, `UNS`, `NCN`, `nSer`,
    `nSeq`, `nJLE`, which appear to encode limits and Saros sequence
    [@cat-nasa-besselian-csv].

12. **Jubier's ephemeris and timeanddate's inputs.** Jubier's 2024 page
    carries the Five Millennium Canon coefficients with his own ΔT of 69.1 s,
    and the limb correction is computed server-side (Watts charts when the
    libration in latitude exceeds 1.6°, Kaguya otherwise, per the client
    code), but no page states the ephemeris behind the server. timeanddate's
    accuracy page names neither its ephemeris, its $k$ nor its ΔT source [@sw-jubier-2024-map]
    [@sw-jubier-calc-js] [@sw-timeanddate-accuracy].

## Experiments that require no further sources

- Reproduce one SVS 2024 `umbra_hi` polygon from SLDEM2015 with the limb test
  as written. This is the end-to-end check of stage 8, and the paper states
  the method in enough detail to perform it [@svs-2024-shapefiles-zip].
- Run SPICE `gfoclt_c` with a `pinpoint` surface site, an ellipsoid Sun and a
  LOLA-derived DSK Moon, and compare its FULL interval with a limb-corrected
  C2 to C3 from Occult or Solar Eclipse Maestro. If it agrees to a second,
  a DSK Moon is a second route to a shaped limb [@loc-spice-gfoclt].
- Compute from LDEM the mean limb radius averaged over position angle and
  libration, and compare with 1738.09 km ($k = 0.2725076$) and 1736.65 km
  ($k = 0.272281$). No published value exists [@moon-williams-2013].
- Difference the SVS `umbra_hi` centre coordinates against Espenak's central
  line at the same instants to put the ephemeris-plus-ΔT difference in
  kilometres [@glob-nasa-path-2024].
