---
title: Software and repositories
description: Compare eclipse calculation software, web services, open-source libraries and datasets by methods, constants, licences and validation evidence.
order: 9
status: working
updated: 2026-09-30
tags: [software, repositories, datasets, survey]
seo_title: Solar Eclipse Calculation Software, Libraries and Data
---

::: summary
- **The surveyed products use several computational lineages.** [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak)'s NASA and EclipseWise tables, Jubier's calculator, Wright's [SVS](../../20-solar-eclipses-and-transits/11-svs-wright/_index.md) pipeline and Herald's Occult are prominent sources. Direct geometric engines and independently fitted element sets also appear in the survey [@sw-nasa-bessel-csv] [@sw-jubier-calc-js] [@sw-svs-5073] [@sw-occult4] [@sw-astronomy-engine-c] [@sw-repo-eclipse-engine].
- **Contact corrections and bead simulation are separate capabilities.** Jubier, Solar Eclipse Maestro, Occult, Eclipse Orchestrator and Kramer document limb corrections. Photo Ephemeris has smooth-Moon contact tables and a separate limb-aware bead simulator. The survey also includes public single-eclipse bead/profile implementations [@sw-jubier-calc-js] [@val-photoephemeris-technote] [@sw-repo-eclipse-2026-rojas]. See [corrections and code](../../20-solar-eclipses-and-transits/04-local-circumstances/corrections-and-code.md) for dataset choices.
- **Open-source code for the full Besselian pipeline exists** in [Stellarium](https://stellarium.org/)'s `SolarEclipseComputer.cpp` (C++, GPL) and NASA's `program.js` (JavaScript, GPL). [Swiss Ephemeris](https://www.astro.com/swisseph/) and Astronomy Engine compute eclipses geometrically from ephemerides without [Besselian elements](../01-foundations/besselian-elements.md) [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-swisseph-swecl] [@sw-astronomy-engine-c].
- **The surveyed general libraries supply smooth-Moon products.** The repository survey includes single-eclipse [LOLA](https://pds-geosciences.wustl.edu/missions/lro/lola.htm) bead work and a bundled limb-band file, but no general limb-corrected path-limit implementation [@sw-repo-eclipse-2026-rojas] [@sw-repo-sew] [@sw-github-api-search].
- **The reference datasets are all public**: NASA's 11,898-row CSV of polynomial Besselian elements, the SVS [shapefiles](https://en.wikipedia.org/wiki/Shapefile) and KML with 1-second umbra polygons, LOLA LDEM grids at 4 to 1024 pixels per degree, SLDEM2015, [SRTM](https://en.wikipedia.org/wiki/Shuttle_Radar_Topography_Mission) and Copernicus DEMs, and [USNO](https://en.wikipedia.org/wiki/United_States_Naval_Observatory) and [IERS](https://www.iers.org/) [ΔT](../07-earth-and-time/delta-t-and-earth-rotation.md) files [@sw-nasa-bessel-csv] [@sw-svs-5073] [@sw-lola-gdr-img].
:::

## What this topic covers

Which existing software, services and public code compute solar eclipse products, what exactly each one computes, from which inputs and constants, and where the method is documented well enough that a developer can reproduce or reuse it. The four notes cover institutional and commercial tools, general astronomy libraries, public GitHub repositories with a comparison matrix, and the datasets with download URLs and formats.

## Notes in this topic

- [Commercial and institutional tools](commercial-and-institutional-tools.md): NASA GSFC and EclipseWise, NASA SVS, Jubier, Occult 4, timeanddate, GreatAmericanEclipse, McGlaun, Eclipse Orchestrator, Solar Eclipse Timer, EclipseDroid, Totality, USNO.
- [Open-source libraries](open-source-libraries.md): Stellarium, Swiss Ephemeris, Astronomy Engine, [Skyfield](https://rhodesmill.org/skyfield/), PyEphem, libnova, NOVAS, SOFA, astropy, sunpy, [SPICE](https://naif.jpl.nasa.gov/naif/), [Horizons](https://ssd.jpl.nasa.gov/horizons/), [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) ports.
- [GitHub repositories](github-repositories.md): 30 repositories with a comparison matrix and the five most complete flagged.
- [Datasets](datasets.md): Besselian element tables, SVS GIS data, lunar DEMs, terrestrial DEMs, ΔT tables, ephemeris kernels.

## What this topic changes for the pipeline

Besselian elements are an interface for the classical pipeline. Direct topocentric calculations and SVS raster limb tests provide alternative routes. The validation plan uses NASA's JavaScript Solar Eclipse Explorer (JSEX) for smooth local circumstances, Jubier for limb-corrected contacts and SVS shapefiles as raster-method reference products [@sw-nasa-jsex-program-js] [@sw-svs-5073]. Predictor configuration is collected in [predictor disagreements](../../20-solar-eclipses-and-transits/10-validation/predictor-disagreements.md).
