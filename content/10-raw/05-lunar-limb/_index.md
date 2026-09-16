---
title: Lunar limb profile
description: How the Moon's mountains and valleys enter an eclipse computation, from Watts' 1963 charts to LOLA and Kaguya DEMs, and what they change in contact times, path limits and Baily's beads.
order: 5
status: working
updated: 2026-09-15
tags: [lunar-limb, watts, lola, kaguya, bailys-beads]
---

::: summary
- **The Moon's silhouette departs from a circle by up to about 3 arcseconds,** about 6 km at the Moon, which moves second and third contact by 2 to 3 seconds anywhere in the path and by tens of seconds near the edges [@limb-espenak-limb-page] [@limb-herald-1983].
- **Watts' 1963 charts gave way to laser altimetry.** Watts' datum is elliptical, offset from the centre of mass and libration-dependent, so it needs the Morrison and Appleby corrections of up to 0.4 arcseconds. Kaguya (SELENE) and LOLA heights are referenced to a 1737.4 km sphere centred on the centre of mass, so that correction disappears [@limb-morrison-appleby-1981] [@limb-lola-ldem128-label].
- **A limb profile belongs to one observer at one instant.** It is built by rotating the DEM point cloud into the observer's line of sight with the topocentric libration and keeping, in each position-angle bin, the point of largest angular radius [@limb-wright-young-2024] [@limb-svs-4517].
- **Corrected contact times are good to about 0.2 seconds** with LOLA or Kaguya profiles, against 0.5 seconds with corrected Watts data and 2 to 3 seconds with none [@limb-eclipsewise-limb] [@limb-occult-accuracy-2016].
- **Baily's beads are the same computation read at every position angle,** and timing them at the path edge is how IOTA has measured the apparent solar radius since 1979 [@limb-herald-1983] [@limb-fiala-dunham-sofia-1994].
:::

## What this topic covers

This topic covers the one input that separates a textbook eclipse prediction from one that matches a stopwatch: the shape of the Moon's silhouette. It traces the data from Watts' photographic charts through the laser-altimeter models of Kaguya (SELENE) and LRO, gives the geometry that turns a digital elevation model into a height-against-position-angle table for one observer at one instant, quotes the numbers each source reports for the effect on contact times and path edges, and describes how Baily's beads are predicted and how their timings are inverted for the solar radius.

## Notes in this topic

- [Limb profile methods](limb-profile-methods.md): history, the DEM-to-limb geometry with formulas, the effect on contact times and path limits, the software, and a worked pipeline.
- [Datasets: Watts, Kaguya, LOLA](datasets-watts-kaguya-lola.md): every dataset with its resolution, reference sphere, frame, accuracy, file format and download location.
- [Baily's beads](bailys-beads.md): how bead events are defined and predicted, and how IOTA uses them to measure the solar radius.

## What this topic changes for the pipeline

The pipeline gains a limb stage between local circumstances and the reported contacts, and a second limb stage inside the path-limit search. Both need the lunar orientation model and the observer vector in the Moon's body-fixed frame, which the Besselian stage does not otherwise compute, so the ephemeris layer must expose that frame. The path product changes shape as well: the umbra outline becomes a polygon that must be emitted as a polygon, and each limit line becomes a pair of lines, interior and exterior.
