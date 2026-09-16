---
title: Software and repositories
description: Survey of the programs, web services, libraries, public repositories and datasets that compute solar eclipse products, with their inputs, constants, licences and documented validation.
order: 9
status: working
updated: 2026-09-15
tags: [software, repositories, datasets, survey]
---

::: summary
- **Four production lineages** produce almost every published eclipse number: Espenak's NASA and EclipseWise tables, Xavier Jubier's JavaScript calculator and Solar Eclipse Maestro, Ernie Wright's NASA SVS pipeline, and Dave Herald's Occult 4. Every consumer app surveyed either embeds one of these or embeds NASA's Besselian elements [@sw-nasa-bessel-csv] [@sw-jubier-calc-js] [@sw-svs-5073] [@sw-occult4].
- **Only the closed programs apply a lunar limb profile to contact times**, and only SVS applies one to the umbra shape. Jubier's maps and Solar Eclipse Maestro, Occult 4, Eclipse Orchestrator, Kramer's calculator and the Photo Ephemeris bead simulator all correct contacts. Maestro and Jubier's limb-correction column use LRO LOLA and Kaguya (SELENE) as well as corrected Watts charts. The list is in [corrections and code](../04-local-circumstances/corrections-and-code.md) [@sw-jubier-calc-js] [@sw-svs-5073].
- **Open-source code for the full Besselian pipeline exists** in Stellarium's `SolarEclipseComputer.cpp` (C++, GPL) and NASA's `program.js` (JavaScript, GPL). Swiss Ephemeris and Astronomy Engine compute eclipses geometrically from ephemerides without Besselian elements [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-swisseph-swecl] [@sw-astronomy-engine-c].
- **No open-source implementation of a limb-corrected path edge or of Baily's beads from LOLA was found in a general library.** Two recent repositories, tomasrojasc/eclipse-2026 and AstroWimSara/SolarEclipseWorkbench, do it for single eclipses [@sw-repo-eclipse-2026-rojas] [@sw-repo-sew].
- **The reference datasets are all public**: NASA's 11,898-row CSV of polynomial Besselian elements, the SVS shapefiles and KML with 1-second umbra polygons, LOLA LDEM grids at 4 to 1024 pixels per degree, SLDEM2015, SRTM and Copernicus DEMs, and USNO and IERS ΔT files [@sw-nasa-bessel-csv] [@sw-svs-5073] [@sw-lola-gdr-img].
:::

## What this topic covers

Which existing software, services and public code compute solar eclipse products, what exactly each one computes, from which inputs and constants, and where the method is documented well enough that a developer can reproduce or reuse it. The four notes cover institutional and commercial tools, general astronomy libraries, public GitHub repositories with a comparison matrix, and the datasets with download URLs and formats.

## Notes in this topic

- [Commercial and institutional tools](commercial-and-institutional-tools.md): NASA GSFC and EclipseWise, NASA SVS, Jubier, Occult 4, timeanddate, GreatAmericanEclipse, McGlaun, Eclipse Orchestrator, Solar Eclipse Timer, EclipseDroid, Totality, USNO.
- [Open-source libraries](open-source-libraries.md): Stellarium, Swiss Ephemeris, Astronomy Engine, Skyfield, PyEphem, libnova, NOVAS, SOFA, astropy, sunpy, SPICE, Horizons, Meeus ports.
- [GitHub repositories](github-repositories.md): 30 repositories with a comparison matrix and the five most complete flagged.
- [Datasets](datasets.md): Besselian element tables, SVS GIS data, lunar DEMs, terrestrial DEMs, ΔT tables, ephemeris kernels.

## What this topic changes for the pipeline

Nothing in the stage design. The survey confirms that the Besselian element formulation is the common interface between the ephemeris stage and the product stage, and that limb and terrain corrections are applied downstream of it by every tool that applies them. It fixes the validation plan instead: NASA's JavaScript Solar Eclipse Explorer for local circumstances without a limb, Jubier's map for limb-corrected contacts, and the SVS shapefiles for the umbra outline. Which predictor uses which ephemeris, ΔT, radius, limb and terrain is tabulated once, in [predictor disagreements](../10-validation/predictor-disagreements.md).
