---
title: NASA SVS and Ernie Wright
description: The raster-oriented, terrain-aware eclipse maps of NASA's Scientific Visualization Studio, the 2024 Astronomical Journal paper that documents them, the datasets they released, and how they differ from Espenak, Jubier and Irwin.
order: 11
status: working
updated: 2026-09-15
tags: [svs, wright, raster, lunar-limb, lola, shapefiles]
---

::: summary
- **The method is published.** Wright, E. and Young, C. A. 2024, "A Raster-oriented Method for Creating Eclipse Maps", The Astronomical Journal 168:163, published 2024 September 19, DOI 10.3847/1538-3881/ad6b23, open access under CC BY 4.0 [@svs-wright-young-2024].
- **The core idea** is to test every map pixel, at every time step, against a lunar limb profile built from the SLDEM2015 and LOLA LDEM elevation models, with the observer lifted to the SRTM terrain height above the WGS 84 ellipsoid via the EGM96 geoid [@svs-wright-young-2024].
- **The datasets** are ESRI shapefiles and KML in WGS 84 longitude and latitude: umbra polygons at 1 s and 10 s steps, path outlines, central line, duration contours at 30 s and obscuration contours at 1 per cent and 5 per cent [@svs-5073-2023-2024-map-data].
- **The constants** stated by SVS are DE421, Earth radius 6378.137 km, WGS 84 flattening, Moon datum radius 1737.4 km, Sun radius 696,000 km (959.645 arcseconds at 1 au) and, for 2017, $\Delta T$ = 68.917 s [@svs-4515-2017-path].
- **The differences** from other predictors come from the solar radius (959.63 versus 959.95 arcseconds), the limb, and terrain, not from the ephemeris. Espenak's own site says limb corrections move limits by 1 to 3 km [@svs-espenak-2024-path].
:::

## What this topic covers

This topic covers the one modern eclipse-mapping method that is both published in full and backed by released data. It takes the 2024 Astronomical Journal paper formula by formula, inventories every SVS eclipse page and the files it releases down to the shapefile schema a developer will load, and sets the SVS path against the NASA eclipse site, EclipseWise, Jubier's maps and the Besselian Elements map to say which constant explains each disagreement.

Notes in this topic:

- [Wright and Young 2024, the raster method](wright-2024-paper.md): the limb-profile construction, the limb test, the antialiasing threshold, the broken-annular criterion and the SPICE calls of Appendix A, with what the paper leaves out.
- [SVS eclipse pages and datasets](svs-products-and-data.md): every SVS eclipse product by ID, the constants each page states, and the parsed DBF schemas of the 2017 and 2024 shapefile archives.
- [SVS versus Espenak, Jubier and Irwin](svs-vs-other-predictors.md): the four predictors' inputs side by side and the size of the limb, terrain, radius and $\Delta T$ differences.

## What this topic changes for the pipeline

The limb correction stops being a post-processing step on Besselian contacts and becomes a per-pixel test, so one code path produces the path limits, central line, duration contours and obscuration contours. The released umbra polygons and cities file become the pipeline's ground truth, fixing the target constants, resolutions and outputs. The limb profile, not the ephemeris, sets the resolution floor at about 600 m.

No public code exists, and no repository by Wright or SVS was found. Every SVS page and the paper PDF were read from Wayback Machine snapshots, because svs.gsfc.nasa.gov refused connections and iopscience.iop.org sat behind a bot wall at the time of writing (2026 September). The snapshot date is recorded in the note field of each row of `refs.tsv`.
