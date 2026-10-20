---
title: NASA SVS and Ernie Wright
description: NASA SVS terrain-aware eclipse maps, the Wright and Young 2024 paper, released datasets and comparisons with other eclipse predictors.
order: 11
status: working
updated: 2026-09-30
tags: [svs, wright, raster, lunar-limb, lola, shapefiles]
seo_title: NASA SVS Eclipse Calculation: Wright and Young's Method
---

::: summary
- **The method is published.** Wright, E. and Young, C. A. 2024, "A Raster-oriented Method for Creating Eclipse Maps", The Astronomical Journal 168:163, published 2024 September 19, DOI 10.3847/1538-3881/ad6b23, open access under CC BY 4.0 [@svs-wright-young-2024].
- **The core idea** is to test every map pixel, at every time step, against a lunar [limb profile](../05-lunar-limb/limb-profile-methods.md) built from the SLDEM2015 and [LOLA](https://pds-geosciences.wustl.edu/missions/lro/lola.htm) LDEM elevation models, with the observer lifted to the [SRTM](https://en.wikipedia.org/wiki/Shuttle_Radar_Topography_Mission) terrain height above the [WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System) ellipsoid via the [EGM96](https://en.wikipedia.org/wiki/Earth_Gravitational_Model) [geoid](../../10-shared/07-earth-and-time/earth-figure-and-terrain.md) [@svs-wright-young-2024].
- **The datasets** are ESRI [shapefiles](https://en.wikipedia.org/wiki/Shapefile) and KML in WGS 84 longitude and latitude: umbra polygons at 1 s and 10 s steps, path outlines, [central line](../03-global-circumstances/path-and-limits.md), duration contours at 30 s and [obscuration](../04-local-circumstances/contact-times-and-magnitude.md) contours at 1 per cent and 5 per cent [@svs-5073-2023-2024-map-data].
- **The constants** stated by SVS are DE421, Earth radius 6378.137 km, WGS 84 flattening, Moon datum radius 1737.4 km, Sun radius 696,000 km (959.645 arcseconds at 1 au) and, for 2017, $\Delta T$ = 68.917 s [@svs-4515-2017-path].
- **Limb and terrain are explicit sources of path differences.** [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak) states that limb corrections shift limits by 1 to 3 km. Solar-radius and Earth-orientation differences also matter. Ephemeris effects require matched-epoch comparison [@svs-espenak-2024-path] [@svs-wright-young-2024].
:::

## What this topic covers

This topic covers a published raster eclipse-mapping method backed by released data. It takes the 2024 Astronomical Journal paper formula by formula, inventories every SVS eclipse page and the files it releases down to the shapefile schema a developer will load, and sets the SVS path against the NASA eclipse site, EclipseWise, Jubier's maps and the Besselian Elements map to say which constant explains each disagreement.

Notes in this topic:

- [Wright and Young 2024, the raster method](wright-2024-paper.md): the limb-profile construction, the limb test, the antialiasing threshold, the broken-annular criterion and the [SPICE](https://naif.jpl.nasa.gov/naif/) calls of Appendix A, with what the paper leaves out.
- [SVS eclipse pages and datasets](svs-products-and-data.md): every SVS eclipse product by ID, the constants each page states, and the parsed DBF schemas of the 2017 and 2024 shapefile archives.
- [SVS versus Espenak, Jubier and Irwin](svs-vs-other-predictors.md): the four predictors' inputs side by side and the size of the limb, terrain, radius and $\Delta T$ differences.

## What this topic changes for the pipeline

The raster approach replaces a contact-time post-processing correction with a per-pixel limb test. Released polygons and city times provide reference products, while observed contacts supply independent evidence. The 0.02-degree profile spacing corresponds to about 600 m along the lunar circumference. It is a sampling interval, rather than a terrestrial path-edge uncertainty [@svs-wright-young-2024] [@svs-2024-shapefiles-zip] [@val-quaglia-2021].

The compared paper and SVS product pages do not provide a source release of the raster solver. Bibliography notes identify the archived copies used for the documented releases [@svs-wright-young-2024] [@svs-5073-2023-2024-map-data].
