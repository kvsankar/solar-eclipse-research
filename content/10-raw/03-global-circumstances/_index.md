---
title: Global circumstances
description: How the central line, the umbral and penumbral limits, the shadow outlines, the rise and set curves, the magnitude contours and the path products on a world map are computed from Besselian elements.
order: 3
status: working
updated: 2026-09-15
tags: [global-circumstances, path, limits, besselian]
---

::: summary
- **One algorithm, many implementations.** Every world-map product is derived from the eight Besselian elements by the method Bessel set out and Chauvenet, the 1961 Explanatory Supplement and its 1992 and 2013 revisions formalised. Stellarium is the closest thing to a complete open reference implementation [@glob-es1961] [@glob-stellarium-sec].
- **The oblate Earth is handled by Bessel's substitution.** Two auxiliary radii and a rotated declination turn the ellipsoid into a unit sphere, so the central line, limits and outlines all become root finds in one angle or one height [@glob-es1961] [@glob-es1992].
- **Constants matter more than the algebra.** The lunar radius ratio $k$, the solar radius, the ellipsoid and ΔT move the path edges by kilometres. A ΔT shift is 15.041 arcseconds of longitude per second [@glob-nasa-tp2001] [@glob-rherale].
- **Smooth-Moon limits are wrong by 1 to 3 km.** NASA, Jubier and SVS all say so. Only the SVS shapefiles publish a limb-profiled, terrain-corrected umbra polygon, and no open-source implementation of a limb-corrected path edge was found [@glob-nasa-google-2024] [@glob-svs-4518].
- **Magnitude and obscuration contours are rasterised, not solved.** The Supplements obtain them by inverse interpolation on the curves of maximum eclipse. SVS and Eclipse-Engine evaluate maximum obscuration per grid cell and contour the field [@glob-es1961] [@glob-svs-5123] [@glob-rherale].
:::

## What this topic covers

Everything that goes on a world map, computed from a table of Besselian
elements: the central line, the northern and southern limits of the umbra and
of the penumbra, the outline of the shadow at an instant, duration, path width,
greatest eclipse and greatest duration, the ground speed of the umbra, the
rise and set curves, the curves of maximum eclipse, the magnitude and
obscuration contours, and the observer-height and terrain treatment. It also
covers the published products that carry these curves, which of them are limb
and terrain corrected, and the open-source code that computes them.

## Notes in this topic

- [Path and limits](path-and-limits.md): the central line, northern and
  southern limits, outline curves, duration, path width, greatest eclipse,
  ground speed, umbra shape.
- [Global maps and contours](global-maps-and-contours.md): rise and set curves,
  curves of maximum eclipse, equal magnitude and equal obscuration contours,
  contact-time contours.
- [Data products and code](data-products-and-code.md): NASA path tables, SVS
  shapefiles, Jubier KML, NOAA releases, Stellarium, Swiss Ephemeris, GitHub
  implementations, and a pipeline to GeoJSON.

## What this topic changes for the pipeline

The global stage is one routine that maps a time, a position angle and a cone
to a surface point through Bessel's substitution. The central line, limits,
outlines, rise and set curves and maximum-eclipse curves are all constraints on
that routine, and width and duration are by-products of it. The partial-eclipse
map is a separate product, because magnitude and obscuration contours need a
per-cell maximisation in time and a contouring step rather than a per-time root
find. The smooth-Moon path and the limb-profiled polygon are two distinct
products and must never share a file without a label. Validation is contractual:
smooth-Moon output must match the NASA path table to 1 km and 0.1 s, and
limb-corrected output is compared against the SVS one-second umbra polygons.
