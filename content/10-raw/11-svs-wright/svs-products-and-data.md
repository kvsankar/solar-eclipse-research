---
title: SVS eclipse pages and datasets
description: Every SVS eclipse product by Ernie Wright with its ID, what it releases, the method statements on the page, and the exact shapefile schema a developer will load.
order: 2
status: working
updated: 2026-09-15
tags: [svs, shapefiles, kml, geojson, datasets, constants]
---

::: summary
- **Two data releases matter:** SVS 4518 for 2017 and SVS 5073 with 5123 and 5124 for the 2023 annular and 2024 total eclipses. Both release ESRI shapefiles in WGS 84 geographic coordinates [@svs-4518-2017-map-shapefiles] [@svs-5073-2023-2024-map-data].
- **The 2024 umbra_hi layer** has 6,741 polygons at 1 s intervals from 17:56:00 to 19:48:20 UTC with twelve attributes including centre longitude and latitude, duration, Sun altitude and azimuth, libration and Moon distance [@svs-2024-shapefiles-zip].
- **The constants** on the SVS pages: Earth radius 6378.137 km, WGS 84, EGM96, Moon radius 1737.4 km, Sun radius 696,000 km, DE421, and for 2017 $\Delta T$ = 68.917 s [@svs-4515-2017-path].
- **The cities file** gives contact times to the second for 32,174 US places [@svs-cities-2024-json].
- **No code, no 2019 to 2021 products.** No repository was found, and the archived SVS feeds show no limb-corrected products for the 2019, 2020 or 2021 eclipses.
- **Everything was read from Wayback snapshots** because svs.gsfc.nasa.gov refused connections at the time of writing (2026 September). Snapshot dates are in `refs.tsv`.
:::

**The question.** Which SVS pages carry Ernie Wright's eclipse calculations, what files do they release, what do the pages say about method, and what does a developer find inside the archives?

## The 2017 series

**SVS 4314, "2017 Total Solar Eclipse in the U.S."**, released 2015 September 9, is the smooth-model baseline and the most explicit constants table SVS ever published [@svs-4314-2017-usa]. Its "About Accuracy" section says the Earth "is neither smooth nor perfectly spherical, nor does it rotate at a perfectly constant, predictable speed", that "our knowledge of the size of the Sun is uncertain by a factor of about 0.2%, enough to affect the duration of totality by several seconds", and then lists:

| Quantity | Value on SVS 4314 |
|---|---|
| Earth radius | 6378.137 km |
| Earth flattening | 1/298.257 (WGS 84) |
| Moon radius | 1737.4 km ($k$ = 0.2723993) |
| Sun radius | 696,000 km (959.634 arcseconds at 1 au) |
| Ephemeris | DE 421 |
| Earth orientation | earth_070425_370426_predict.bpc ($\Delta T$ corrected) |
| Delta UTC | 68.184 s (TT minus TAI plus 36 leap seconds) |

The same page states that elevations and the limb "were ignored" for that animation, that the errors "tend to cancel out" because elevation lengthens totality while limb valleys shorten it, and that the Moon's centre of mass and [?centre-of-figure] differ by "about 0.5 kilometers". That figure is the sky-plane component. The full centre-of-mass to centre-of-figure vector from LOLA is 1.935 km, mostly along the Earth-Moon line, as [lunar figure and libration](../08-lunar-and-solar-model/lunar-figure-and-libration.md) sets out [@moon-jones-2025]. It also positions its lunar radius as "slightly larger than the one used by Fred Espenak and slightly smaller than the one used by the Astronomical Almanac" [@svs-4314-2017-usa]. The [?k-lunar-radius] value 0.2723993 is 1737.4/6378.137.

**SVS 4515, "2017 Path of Totality"**, and **SVS 4516, the oblique view**, both released 2016 December 13, are the first limb-and-terrain-corrected products. The text: "Elevations on the Earth's surface and the irregular lunar limb (the silhouette edge of the Moon's disk) are both fully accounted for." The constants table changes in two places from 4314 [@svs-4515-2017-path]:

| Quantity | Value on SVS 4515 and 4516 |
|---|---|
| Earth radius | 6378.137 km |
| Ellipsoid | WGS84 |
| Geoid | EGM96 |
| Moon radius | 1737.4 km |
| Sun radius | 696,000 km (959.645 arcseconds at 1 au) |
| Ephemeris | DE 421 |
| Earth orientation | earth_070425_370426_predict.bpc ($\Delta T$ corrected) |
| Delta UTC | 69.184 s (TT minus TAI plus 37 leap seconds) |
| $\Delta T$ | 68.917 s |

The Sun radius in kilometres is unchanged at 696,000 km. The arcsecond equivalent moved from 959.634 to 959.645, which is a change in the au or distance conversion rather than in the physical radius. The animation runs at 30 times real time, 10:12 am PDT to 2:52 pm EDT [@svs-4515-2017-path].

**SVS 4517, "Umbra Shapes"**, released 2016 December 13 and updated 2024 January 25, is the explainer page for the shape of the umbra [@svs-4517-umbra-shapes]. Its method statements, read in full:

- The umbra "is more like an irregular polygon with slightly curved edges. Each edge corresponds to a single valley on the lunar limb, the last (or first) spot on the limb that lets sunlight through." An observer at a cusp "will be treated to a double diamond ring."
- Over the Cascades, Rockies and Appalachians the edges "are scalloped by the peaks and valleys of the landscape", and western elevations "shift the umbra toward the southeast (in the direction of the Sun's azimuth) by as much as 3 kilometers."
- The animation compares three shapes: a red ellipse for smooth Moon and Earth, white for the limb effect, dark grey adding terrain.
- "The lunar limb in the present work is based on LRO laser altimetry and on a hybrid LRO/Kaguya dataset called SLDEM2015. To create a limb profile, each point in an elevation map is transformed into 3D cartesian coordinates in a Moon body-fixed frame. At each time step in the eclipse calculation, the point cloud is rotated into fundamental plane coordinates. The limb profile then comprises the set of points lying farthest from the shadow axis."
- Observer elevations "are taken from SRTM". The limb animation exaggerates the profile by 18. Watts "designed a machine that traced some 700 photographs of the Moon", an effort spanning 17 years.

This 2016 description rotates the point cloud into [?fundamental-plane] coordinates and picks the points farthest from the shadow axis. The 2024 paper rotates into the topocentric view of the shadow-axis observer and picks the largest angular radius per bin. These are the same construction stated in two frames.

**SVS 4518, "2017 Total Solar Eclipse Map and Shapefiles"**, released 2016 December 13, carries the printed map at 1:10,000,000 with 833 place names and umbra outlines at 10 minute intervals, plus two archives [@svs-4518-2017-map-shapefiles]. The page's own description of `eclipse2017_shapefiles.zip`, 5.0 MB, names eight layers:

- penum17, contours at 90, 75, 50, 25 and 0 per cent obscuration.
- penum17_1m, 1 minute steps from 17:00 to 19:15 UTC for 95 down to 75 per cent in 5 per cent steps.
- upath17 and w_upath17, the path at US and world scale, the US version limited to 96 degrees of longitude.
- umbra17 and w_umbra17, at 10 minute intervals.
- w_umbra17_1m, at 1 minute intervals from 16:49 to 20:02 UTC.
- center17 and w_center17, the central line.

"The projection for all of these shapefiles is WGS84, latitude-longitude, in degrees."

The second archive, `eclipse2017_shapefiles_1s.zip`, 139.2 MB, is described as holding four layers [@svs-4518-2017-map-shapefiles]:

- umbra17_1s, "6000 umbra shapes at one-second intervals from 17:12 to 18:52 UTC. These are high-resolution shapes with roughly 100-meter precision", with attributes for UTC time as a string and seconds past midnight as an integer.
- upath17_1s, covering 130 W to 76 W, "calculated at a precision of 250 meters".
- ucenter17_1s, points at 1 s.
- durations17_1s, at 30 s intervals, "truncated and invalid at the ends".

The 1 s archive has not been downloaded here, and the open questions say what it would settle.

The 5 MB archive was downloaded from the Wayback capture of 2020 October 19 and inspected [@svs-2017-shapefiles-zip]. Its DBF schemas:

| Layer | Records | Fields |
|---|---|---|
| penum17 | 5 | Name C24, Obscur N6.8 (values 0.8999, 0.7500, 0.5000, 0.2500, 0.0000) |
| umbra17 | 17 | Name C24, Time C6 (local), TZ C5 (PDT to EDT) |
| w_umbra17 | 20 | Name C24, Time C6 (UTC 16:50 to 20:00) |
| w_umbra17_1m | 194 | Name C24 (Umbra_1009 ...), UTCTime C6, UTCMin N5 (1009 to 1202) |
| penum17_1m | 680 | Name C24, UTCTime C5, UTCMin N5, Obscur N4.8 |
| upath17 | 1 | Name, Time0 17:00, Time1 19:50 |
| w_upath17 | 1 | Name, Time0 16:48:40, Time1 20:02:30 |
| center17 | 1 | Name, Time0 2017-08-21T17:00:02, Time1 2017-08-21T19:49:59 |
| w_center17 | 1 | Name, Time0 2017-08-21T16:49:10, Time1 2017-08-21T20:02:00 |

Every `.prj` is `GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]` [@svs-2017-shapefiles-zip].

**SVS 4552, "2017 Eclipse State Maps"**, released 2017 February 6, gives one map per state at 300 dpi with the umbra at 3 minute intervals and duration contours at 30 s. Its only method content is the claim that the path grazes Montana and Iowa, which "some sources" omit [@svs-4552-2017-state-maps]. Its datasets list adds the 2010 Census Gazetteer for place names.

**SVS 12412, "Tracing the 2017 Solar Eclipse"**, released 2016 December 14, is the narrated video. The caption file, retrieved from the Wayback capture of 2025 October 10, has Wright saying: "I used the Lunar Reconnaissance Orbiter, the laser altimetry data from that, which gives us a digital map of the elevations on the Moon. For the Earth I used something called SRTM ... For the positions of the Earth, the Moon, and the sun, I used a JPL ephemeris." And: "it hasn't actually been seen in exactly this way before where we calculate those circumstances for every point on the map and draw that shape" [@svs-12412-tracing-2017].

**SVS 4579, "Flying Around The Eclipse Shadow"**, released 2017 June 21, combines views from 4390, 4321 and 4314 and adds the LROC WAC mosaic. No method content beyond the datasets list [@svs-4579-flyaround-2017].

## 2019, 2020 and 2021

No SVS product for the 2019 July 2, 2020 December 14 or 2021 December 4 eclipses with limb or terrain corrections was found. The archived SVS atom feeds for `people=Ernie+Wright`, `keywords=Solar+Eclipse`, `keywords=Eclipse+2020`, `missions=LRO`, `series=2017+Solar+Eclipse` and `search=eclipse` were read from Wayback captures between 2024 and 2025. The `Eclipse 2020` feed contains one item, a Spanish-language safety video, SVS 13668. Each feed is truncated to ten entries, so absence in the feeds is not proof of absence on the site. The live SVS search API returned no results, because the host refused connections at the time of writing (2026 September).

## The 2023 annular and 2024 total eclipses

**SVS 5073, "The 2023 and 2024 Solar Eclipses: Map and Data"**, released 2023 March 8 and corrected 2023 March 15 for times in Mexico, is the combined data page [@svs-5073-2023-2024-map-data]. Its "Making the Map" statement is the canonical one: "The eclipse data were calculated by visualizer Ernie Wright using elevation information from SRTM, lunar topography from LRO, and planetary positions from the JPL DE421 ephemeris." The cartography is by Michala Garrison using Blue Marble Next Generation and Black Marble. The page explains that the irregular ovals are umbra or antumbra shapes labelled with times, that duration contours run "up to 4 minutes" for 2024, and that the outer contours are [?obscuration], "percentage of the Sun's area covered by the Moon".

Its downloads: `2023eclipse_shapefiles.zip`, `2023eclipse_kml.zip`, `cities-eclipse-2023.json`, `2024eclipse_shapefiles.zip`, `2024eclipse_kml.zip` and `cities-eclipse-2024.json`, all under `/vis/a000000/a005000/a005073/`. The page describes each zip as containing [@svs-5073-2023-2024-map-data]:

- center, "a high-resolution polyline tracing the path of the shadow center. Region limited."
- duration, "isocontours of maximum total or annular duration, at 30-second intervals."
- ppath, "contours of maximum partial obscuration ... at 5% intervals."
- ppath01, the same at 1 per cent intervals.
- umbra_hi, "high resolution umbra (or antumbra) polygons, at 1-second intervals. Region limited."
- umbra_lo, "lower resolution umbra (or antumbra) polygons, at 10-second intervals. Global."
- upath_hi and upath_lo, the path shape at region-limited and global resolution.

The cities JSON is described as covering "over 32k major cities in the US" with LON, LAT, ECLIPSE, NAME and STATE, where ECLIPSE is "an array of UTC times for the [0.01%, 50%, 100%, 50%, 0.01%] points of coverage (normalized with respect to the maximum coverage achieved)" [@svs-5073-2023-2024-map-data].

**SVS 5123, "The 2024 Total Solar Eclipse"**, released 2023 July 10 and updated 2024 April 7, is the 2024-only map with the same "Making the Map" text, the same shapefile list under `/vis/a000000/a005100/a005123/2024eclipse_shapefiles.zip`, and translations at SVS 5247, 5249, 5250, 5251, 5252 and 5253 [@svs-5123-2024-map]. **SVS 5124** is the 2023 annular equivalent, where the umbra_hi and umbra_lo layers hold antumbra polygons and the dark path "marks when 90% obscuration begins" [@svs-5124-2023-annular-map]. **SVS 5086** and **SVS 14474** are the narrated map tours, whose credits say "eclipse calculations by Ernie Wright, NASA Goddard Space Flight Center" [@svs-5086-map-tour] [@svs-14474-map-tour-2024].

**SVS 5219, "2024 Path of Totality"**, released 2024 February 13, is the flyover animation, 10:57 am PST to 4:47 pm ADT. Its method sentence: "the umbra and its path were calculated in a way that accounts for both elevations on the Earth's surface and the irregular lunar limb". It lists umbra-centre arrival times for cities, for example Kerrville and San Antonio 18:34:14 UTC, Dallas and Fort Worth 18:42:26 UTC, Carbondale 19:01:18 UTC, Cleveland 19:15:32 UTC and Montreal and Burlington 19:27:42 UTC [@svs-5219-2024-path].

**SVS 5212, "Path for Spherical Displays"**, released 2024 January 20, states the frame cadence of the global shadow rasters: "from 15:42:10 to 20:52:20 UTC with steps of 10 seconds between frames" [@svs-5212-2024-spherical]. **SVS 5248, "Insolation during the 2024 Eclipse"**, released 2024 March 25, releases the obscuration rasters behind it: "calculated at 10-second intervals from 15:42:10 to 20:52:20 UTC at a resolution of 360/8192 degrees per pixel (roughly 3.75 x 4.9 km at 40 N)", global equirectangular, white for 100 per cent obscuration, as a 194 MB zip [@svs-5248-insolation-2024]. That grid, 8192 by 4096 pixels, is the only stated raster resolution for any SVS eclipse product and is a plausible candidate for the global shadow grid.

**SVS 5186, "Flying Around The 2024 Eclipse Shadow"**, released 2023 November 13, is a narrated flyaround with the geometry to scale and the umbra speed given as "more than 1500 miles (2400 kilometers) per hour" [@svs-5186-flyaround-2024]. **The SVS Eclipse Explorer web app (SVS 5169)**, released 2023 October 2 by Alex Gurvich with Wright and Garrison credited, is the interactive map at go.nasa.gov/EclipseExplorer with per-city countdowns and SDO imagery [@svs-5169-eclipse-explorer]. It is a different product from NASA's JavaScript Solar Eclipse Explorer (JSEX), Espenak's local-circumstances calculator.

**SVS 5365 and 5366**, both released 2024 September 19 with the paper, are the broken-annular Baily's beads simulation for 2005 April 8 and the "Solar Eclipse Shadow Shape Explained" page. Both list the AJ paper under "Related papers" and both list LOLA DEM, DE421 and SLDEM2015 as datasets [@svs-5365-broken-annular] [@svs-5366-shadow-shape].

**SVS 5222, "5000 Years of Total Solar Eclipses"**, released 2024 February 20, is a different product: a heat map of 3,742 total and hybrid paths from the Five Millennium Canon drawn at 1/15 degree pixels, in Terrestrial Time, with DE441 listed as a dataset. It reports an average of 13.66 eclipses per pixel and 366 years between totalities at a place [@svs-5222-5000-years].

## After the paper

**SVS 5378, "Map of the October 2, 2024 Annular Solar Eclipse"**, released 2024 September 7, and **SVS 5510, "Map of the March 29, 2025 Partial Solar Eclipse"**, released 2025 February 25, are global maps with antumbra at 15 minute intervals, obscuration contours, isochrons and sunrise and sunset loops. Both list only Blue Marble and DE421 as datasets, with no LOLA or SLDEM entry, so they appear to be smooth-model products. Both carry the same caveat: "All of these lines are based on an idealized model of the eclipse geometry. The true situation at the ends of the shadow path is much messier. The apparent positions of the Sun and Moon relative to the horizon are affected by local terrain and atmospheric refraction." The 2025 page quotes gamma 1.0405 "as calculated by Fred Espenak" and a closest approach of about 215 km [@svs-5378-oct-2024-annular-map] [@svs-5510-mar-2025-partial-map].

## Inside the 2024 shapefile archive

`2024eclipse_shapefiles.zip` (78.6 MB) was downloaded from the Wayback capture of 2025 February 12 and the DBF headers were parsed directly [@svs-2024-shapefiles-zip]. All eight `.prj` files contain the WGS 84 geographic definition quoted above. Shape types are polygon, type 5, for umbra and path layers, and polyline, type 3, for the central line.

| Layer | Records | Fields and observed values |
|---|---|---|
| umbra_hi | 6,741 | UTCTime C8, UTCSec N5, CenterLon N10, CenterLat N10, CenterAlt N5, Duration N6, SunAlt N4, SunAz N5, MoonL N7, MoonB N7, MoonC N7, MoonDist N8. First record 17:56:00, UTCSec 64560, centre 109.84319 W, 19.15355 N, CenterAlt 0, Duration 262.24, SunAlt 66.3, SunAz 116.4, MoonL 2.192, MoonB minus 0.113, MoonC 339.240, MoonDist 353923.8. Last record 19:48:20, UTCSec 71300, 47.20313 W, 49.00295 N, Duration 162.67, SunAlt 19.1, SunAz 259.3, MoonDist 357783.6. |
| umbra_lo | 1,181 | Same twelve fields, 10 s steps from 16:38:50 to 19:55:30 UTC. Records before first contact of the umbra with the Earth repeat placeholder attribute values. |
| center | 1 | Name "Center Line", Time0 17:55:31, Time1 19:48:20. Polyline of 6,770 points starting at 109.97169 W, 19.01302 N. |
| duration | 8 | Duration N6, values 240, 210, 180 down to 30 seconds. |
| ppath | 26 | Obscuratio N6, from 0.9499 down to 0.0001 in 5% steps. |
| ppath01 | 106 | Obscuratio N6, from 0.9899 down to 0.0001 in 1% steps. |
| upath_hi | 1 | Name "Umbra Path Low Resolution" (the label is a quirk, the geometry is the high-resolution 38,938-vertex polygon). |
| upath_lo | 1 | Name "Umbra Path Low Resolution", 8,902 vertices. |

Interpretation of the umbra attributes, from the field names and values: CenterLon and CenterLat are the shadow-axis intersection in degrees, CenterAlt is height in metres and is 0 throughout, Duration is totality at the centre in seconds, SunAlt and SunAz are the Sun's altitude and azimuth in degrees at the centre, MoonL and MoonB are the [?libration] in longitude and latitude in degrees, MoonC is the [?axis-angle] in degrees (339.24, matching the $c$ of the paper's limb test) and MoonDist is the observer to Moon distance in kilometres, the $d$ of the limb test [@svs-2024-shapefiles-zip] [@svs-wright-young-2024]. The first umbra_hi polygons have 19, 83 and 112 vertices as the umbra rises over the Pacific. umbra_lo polygons in the middle of the path have 200 to 320 vertices at a coordinate quantisation of about 0.0049 degrees. umbra_hi coordinates are quantised at about 0.00049 degrees, roughly 50 m.

The 2024 umbra_hi centre at 17:56:00 UTC is 109.84 W, 19.15 N, and Espenak's central line table gives 20 19.2 N, 108 45.8 W at 18:00 UT [@svs-espenak-2024-path]. Four minutes of shadow motion at the stated speed accounts for the difference. A direct comparison of the two predictions at a common instant was not made here and is an open question below.

`2024eclipse_kml.zip`, 299 MB, read from the Wayback capture of 2025 February 12, contains center.kml, duration.kml, penumbra.kml, ppath.kml, ppath01.kml, umbra_hi.kml, umbra_lo.kml, upath_hi.kml and upath_lo.kml, read from the zip central directory with an HTTP range request [@svs-2024-kml-zip]. penumbra.kml has no shapefile counterpart. No GeoJSON is released. The cities file is the only JSON.

`cities-eclipse-2024.json`, 4.35 MB, read from the Wayback capture of 2025 February 12, is a list of 32,174 objects with keys STATE, NAME, LAT, LON and ECLIPSE. Places outside totality have five times and places inside have six, with the third and fourth being second and third contact [@svs-cities-2024-json]. Examples: Dallas, Texas: 17:23:40, 18:08:40, 18:40:47, 18:44:38, 19:17:10, 20:02:40 UTC, so totality lasts 3 min 51 s. Carbondale, Illinois: second contact 18:59:15, third contact 19:03:25, 4 min 10 s. Indianapolis: 19:06:06 to 19:09:53, 3 min 47 s. Partial-phase times are given to 10 s and contacts to 1 s, consistent with a 10 s global raster and a 1 s regional raster.

## Software, code and talks

No public implementation exists. GitHub holds no repository by Wright or by the Scientific Visualization Studio for the raster method, and no independent reimplementation of it, under any of the terms characteristic of the method: the umbra and the lunar limb, SPICE and limb profiles, the LOLA and SLDEM models, raster shadow maps over a digital elevation model, and the limb correction to Besselian elements. No GitHub account matches the author's name [@svs-github-api-search]. Semantic Scholar holds no author record linking Wright to other eclipse papers, and Crossref lists the AJ paper as his only eclipse publication [@svs-crossref-wright]. No personal site or blog is established as of 2026 September. The older SVS animator pages from 2009 and 2011 list his visualisations only, back to the Tycho skymap and LOLA footprint animations, with no biography [@svs-animator-page-2009].

What is documented about the stack: the paper's appendix prints C code against SPICE and names the kernels [@svs-wright-young-2024], the 2015 page says the Besselian method "was adapted to the routines available in NAIF's SPICE software library" [@svs-4314-2017-usa], and the 2017 shapefile page says the map "was rendered in animation software" [@svs-4518-2017-map-shapefiles]. No page and no part of the paper supports the sometimes repeated claim that Wright used Maya or RenderMan for the eclipse calculation itself. The only public talks found are the narrated SVS videos 12412 and 5186 and the map tours 5086 and 14474. No AAS or AGU abstract was found through Crossref, and ADS could not be queried without an API token.

## Sources compared

| Source | What it uniquely provides |
|---|---|
| SVS 4314 [@svs-4314-2017-usa] | The only page with $k$, flattening and the mass-versus-figure offset stated. |
| SVS 4515 [@svs-4515-2017-path] | The only page with $\Delta T$, the geoid and the EOP kernel stated. |
| SVS 4517 [@svs-4517-umbra-shapes] | The point-cloud description of the limb profile and the 3 km terrain shift. |
| SVS 4518 [@svs-4518-2017-map-shapefiles] | The 100 m and 250 m precision statements for the 1 s archive. |
| SVS 5073 [@svs-5073-2023-2024-map-data] | The layer descriptions and the cities JSON schema for 2023 and 2024. |
| SVS 5248 [@svs-5248-insolation-2024] | The only stated raster grid, 360/8192 degrees per pixel at 10 s. |
| The zip archives [@svs-2024-shapefiles-zip] [@svs-2017-shapefiles-zip] | The actual DBF field names and time coverage. |
| SVS 12412 captions [@svs-12412-tracing-2017] | Wright's own words on the datasets. |

## What a developer should do

Download `2024eclipse_shapefiles.zip` from SVS 5123 or 5073, or from the Wayback capture if SVS is down. Load umbra_hi with any shapefile reader. Use UTCSec as the key, CenterLon and CenterLat as the shadow-axis track, and MoonL, MoonB, MoonC and MoonDist as a free per-second table of the libration and distance inputs to the limb test in [wright-2024-paper.md](wright-2024-paper.md). Treat upath_hi as the reference path outline for regression tests, with the understanding that its edge is limb-corrected, terrain-corrected and computed with a 696,000 km Sun. Use the cities JSON as a contact-time test set with 1 s resolution. Do not rely on the 2019 to 2021 eclipses for SVS reference data.

## What this changes

The SVS archives become the validation set for the pipeline. They fix the target constants, which are DE421 or DE440, 1737.4 km, 696,000 km, WGS 84, EGM96 and SRTM. They fix the target resolutions, 1 s and 10 s in time and about 50 m and 500 m in position. They fix the target outputs: umbra polygons, path polygon, centre polyline, duration and obscuration contours, and city contact times.

## Open questions

- **The 1 s archive for 2017**, `eclipse2017_shapefiles_1s.zip` at SVS 4518, was not downloaded. Fetch it and confirm the attribute schema matches the 2024 umbra_hi schema.
- **The 2023 annular archive**, `2023eclipse_shapefiles.zip`, has not been downloaded, because the CDX query timed out. Its umbra_hi layer holds antumbra polygons and would test the reversed limb test.
- **The obscuration raster zip** at SVS 5248 (194 MB) would show whether the global grid is 8192 by 4096 and whether obscuration is computed with the limb.
- **The SVS API JSON for 5123** may list software or funding fields that the HTML omits. Fetch `https://svs.gsfc.nasa.gov/api/5123` when the host is reachable.
- **A same-instant comparison** of umbra_hi centre coordinates with Espenak's central-line table would quantify the ephemeris and $\Delta T$ difference in kilometres.
