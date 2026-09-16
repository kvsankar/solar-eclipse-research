---
title: Data products and code
description: The published path products (NASA tables, SVS shapefiles, Jubier KML, NOAA releases, GreatAmericanEclipse, Irwin), which of them carry limb and terrain corrections, the open-source code that computes paths, and a worked pipeline from Besselian polynomials to GeoJSON.
order: 3
status: working
updated: 2026-09-15
tags: [shapefiles, geojson, kml, svs, stellarium, swiss-ephemeris, github, pipeline]
---

::: summary
- **NASA's path tables are the reference product but are smooth-Moon and sea-level.** The columns are UT, northern and southern limit, central line, Moon/Sun diameter ratio, Sun altitude and azimuth, path width in km and central duration, in 2-minute rows for 2024 with $\Delta T = 70.6$ s. There is no limb correction, and the edges are good to 1 to 2 km [@glob-nasa-path-2024] [@glob-nasa-google-ack].
- **SVS shapefiles are the only public product with limb-profiled, terrain-corrected umbra polygons.** For 2017 the umbra comes at 10 min, 1 min and 1 s, the last as 6000 shapes at about 100 m precision, with path, central line and penumbra contours. For 2024 there are `umbra_hi` at 1 s, `umbra_lo` at 10 s, `upath`, `center`, `duration` at 30 s and `ppath` at 5 and 1 per cent obscuration. All are WGS 84 lat-lon, built from SRTM, LRO LOLA and SLDEM2015, and JPL DE421 on every SVS product page, with DE440 in the paper's appendix [@glob-svs-4518] [@glob-svs-5123].
- **Jubier's KML and GreatAmericanEclipse's maps are limb-corrected.** Jubier publishes KML/KMZ per eclipse and a per-location limb correction. Zeiler's maps use Espenak's elements through Jubier's software, "corrected for the precise shape of the Moon's limb" [@glob-jubier-maps] [@glob-gae-about].
- **NOAA and USGS redistribute, they do not compute.** NOAA's Science On a Sphere dataset and ArcGIS Hub shapefiles are SVS data processed in ArcGIS Pro. No USGS computation was found [@glob-noaa-sos] [@glob-noaa-hub].
- **Open source: Stellarium is the complete reference, the Swiss Ephemeris gives the centre only.** Stellarium computes every classic curve and writes KML. `swe_sol_eclipse_where` returns the central point and umbra diameter, not the limits. GitHub engines exist in JavaScript, Python and Rust. Skyfield has no path routine [@glob-stellarium-sec] [@glob-swisseph-doc] [@glob-skyfield-801].
- **No open-source implementation of limb-corrected path edges was found.** The searches are described below. Irwin's and Wright's code is not public.
:::

**The question.** Which published data products describe the path on a world map, in what formats, with what corrections, and what open-source code exists that computes the path from Besselian elements? What steps turn a polynomial set and a time step into central line, limits and umbra outlines as GeoJSON?

## NASA path tables and bulletins

The web path table for 2024 April 8 lists rows at 120-second intervals with the columns "Universal Time | Northern Limit (Latitude, Longitude) | Southern Limit | Central Line | M:S Diam. Ratio | Sun Alt | Sun Azm | Path Width | Central Line Durat.", coordinates to 0.1 arcminute, a first row labelled "Limits" giving the extreme points, and the footnote "ΔT = 70.6 seconds". The first rows read

```
 Limits  07 11.6S 158 43.9W  08 27.2S 158 20.1W  07 49.5S 158 31.9W  1.040   0   -  144  02m06.3s
 16:40      -         -      07 36.2S 152 54.5W  07 38.1S 157 11.2W  1.040   1  82  146  02m08.8s
 16:42   05 30.6S 149 47.6W  06 11.7S 146 38.0W  05 50.2S 148 07.8W  1.043  11  81  159  02m27.5s
```

[@glob-nasa-path-2024]. The 2017 table has the same layout with $\Delta T = 68.4$ s, and at 18:00 UT gives central line 40°50.3'N 98°18.3'W, ratio 1.030, width 112 km, duration 2m35.7s [@glob-nasa-path-2017]. The tables carry no "Δ" columns. The bulletins' Table 2 lists the shadow contacts P1 to U4 "with and without corrections for ΔT" [@glob-nasa-tp2001]. NASA's explanation page defines the columns: limits and central line "to the nearest tenth of an arc-minute (~185 m at the Equator)", the "topocentric ratio of the apparent diameters of the Moon and Sun", the central path width with "the umbral shadow's major and minor axes", and "the central line duration of the umbral phase" [@glob-nasa-explain]. The bulletins add four tables that the web pages do not carry [@glob-nasa-tp2001] [@glob-nasa-tp2008-sec1]:

- Table 4, the physical ephemeris: topocentric diameter ratio, obscuration, altitude, azimuth, width, major and minor axes, velocity and duration.
- Table 6, topocentric data and limb corrections to the limits.
- Table 7, limits and central line at 1 degree of longitude, to 0.01 arcminute.
- Table 8, graze-zone coordinates every 30 arcminutes of longitude, with time, path azimuth, Elev Fact and scale factor.

The bulletins' generating constants are $k = 0.2725076$ for penumbral and $k = 0.272281$ for umbral contacts, centre-of-mass lunar positions, no refraction, and "the best value of ΔT available at the time of preparation" [@glob-nasa-tp2001]. The Five Millennium Canon, NASA/TP-2006-214141, and the web path tables generated from it use $k = 0.2724880$ for penumbral contacts instead, as [Besselian elements and the fundamental plane](../01-foundations/besselian-elements.md) sets out. The acknowledgement page for the Google maps states the elements were "generated for the Moon's center of mass using the VSOP87/ELP2000-82 ephemerides" and that "the accuracy of the northern and southern edges of the eclipse path are limited to approximately 1-2 kilometers due to the lunar limb profile" [@glob-nasa-google-ack]. EclipseWise, Espenak's own site, repeats the two-$k$ policy and its rationale: the smaller umbral value "ensures that an eclipse is truly total" and yields "shorter durations and narrower paths for total eclipses compared to IAU calculations" [@glob-eclipsewise-radius].

## NASA SVS shapefiles (Ernie Wright)

The 2017 release `eclipse2017_shapefiles.zip` contains nine shapefiles: `penum17` (maximum obscuration contours at 90, 75, 50, 25 per cent and the penumbra edge at 0 per cent), `penum17_1m` (penumbra outlines each minute 17:00–19:15 UTC for 95 to 75 per cent in 5 per cent steps), `upath17` and `w_upath17` (path of totality, U.S. high resolution and world), `umbra17` and `w_umbra17` (umbra shapes every 10 minutes), `w_umbra17_1m` (umbra each minute 16:49–20:02 UTC), `center17` and `w_center17`. "The projection for all of these shapefiles is WGS84, latitude-longitude, in degrees." A second archive `eclipse2017_shapefiles_1s.zip` (139 MB) holds `umbra17_1s` with "6000 umbra shapes at one-second intervals from 17:12 to 18:52 UTC... with roughly 100-meter precision", attributes with the UTC string and seconds past midnight, `upath17_1s` "calculated at a precision of 250 meters" over 130°W to 76°W, `ucenter17_1s` as a polyline with one-second points, and `durations17_1s` at 30-second intervals, "truncated and invalid at the ends" [@glob-svs-4518]. Wright's page says the lunar topography "is from NASA LRO laser altimetry and JAXA Kaguya stereo imaging", positions "from the JPL DE421 ephemeris", and "the lunar limb profile and eclipse calculations are by the visualizer" [@glob-svs-4518]. Kaguya is the SELENE mission. DE421 is named on every SVS product page, while the paper's appendix uses DE440, a difference of under a metre at the Moon, as [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md) sets out.

The 2024 release `2024eclipse_shapefiles.zip` contains `center.shp` (high-resolution polyline, region limited), `duration.shp` (isocontours of maximum total duration at 30-second intervals), `ppath.shp` and `ppath01.shp` (maximum partial obscuration at 5 per cent and 1 per cent), `umbra_hi.shp` (umbra polygons at 1-second intervals, region limited), `umbra_lo.shp` (10-second intervals, global), `upath_hi.shp` and `upath_lo.shp`. The data were "calculated by visualizer Ernie Wright using elevation information from SRTM, lunar topography from LRO, and planetary positions from the JPL DE421 ephemeris" [@glob-svs-5123]. The combined 2023/2024 map page (SVS 5073) lists the same datasets and is the source NOAA cites [@glob-svs-5073] [@glob-noaa-sos]. None of the SVS pages read names a file containing "ducks". The penumbra products are `penum17`, `penum17_1m`, `ppath` and `ppath01`. The pages were read from Wayback Machine snapshots dated 2025-12-09 (5123), 2025-12-20 (4518), 2026-01-02 (5073), 2025-12-10 (4517), 2026-03-06 (5366) and 2025-12-12 (5219) because svs.gsfc.nasa.gov refused connections at fetch time.

These are the only public products in which the umbra polygons carry the lunar limb profile and Earth terrain. The method, described on the Umbra Shapes page and in Wright and Young 2024, is covered in [Path and limits](path-and-limits.md) [@glob-svs-4517] [@glob-wright-young-2024].

## NOAA and USGS

NOAA's Science On a Sphere dataset "Solar Eclipse Paths: 2023 & 2024" states that "shape files were obtained from NASA's Scientific Visualization Studio" (SVS 5073) "and subsequently processed using ArcGIS Pro", with labels added in Photoshop, credited to the NOAA Office of Education and CIRES [@glob-noaa-sos]. NOAA's ArcGIS Hub item "2024 Eclipse Shapefiles" is summarised in search results as "NASA Data for the Solar Eclipse on April 8th, 2024. Shapefile includes center, path, duration and more". The page itself rendered only its title when fetched [@glob-noaa-hub]. NCEI's contribution was a cloud-climatology map, not a path computation. No USGS eclipse path release was found in the searches "NOAA NCEI OR USGS 2024 total solar eclipse path shapefile GIS data release".

## Jubier, GreatAmericanEclipse, Irwin, Photo Ephemeris, Radiant Drift

Xavier Jubier's interactive maps draw "the umbral or antumbral northern and southern limits... in pink while the central line is blue", offer "the Google Earth files (kml, kmz) for each eclipses", and add "special Google Maps showing the grazing zones" [@glob-jubier-maps]. The help page lists the full colour code (orange 10-minute maximum lines, green penumbral limits, maximum on the horizon and equal magnitude, yellow maximum at sunrise and sunset, violet 30-minute maximum curves), a tooltip with umbral depth, path width, obscuration, magnitude, size ratio and umbral velocity, and an "LC" column giving the limb correction in seconds, available "only when you are online". It states that "the computations are executed using the standard IAU 1976 solar radius, that is 959.63 arc-seconds at one astronomical unit, and not the true photospheric solar radius that is closer to 959.98 arc-seconds", that refraction is not applied, and that an elevation tool re-evaluates the local circumstances at the terrain height [@glob-jubier-help]. The Solar Eclipse Maestro help describes the limb datasets: Watts corrected by Morrison and Appleby (1981) and Rosselló and Jordi (1991), Kaguya, and LRO, the last two "much more accurate than the Watts even after correction", plotted against the reduced radius $k_2$ "usually used to compute the uncorrected second and third contacts and the umbral or ant-umbral path" and the IAU mean radius 1738.091 km, $k = 0.2725076$ [@glob-jubier-sem-limb]. NASA's own Google maps were built on Jubier's code: "Xavier's assistance in updating and improving these maps has been invaluable" [@glob-nasa-google-ack].

GreatAmericanEclipse (Michael Zeiler) states that its maps rest on Fred Espenak's Besselian elements adapted through Xavier Jubier's software, "corrected for the precise shape of the Moon's limb as lunar mountains and valleys affect the onset and egress of totality by up to several seconds", and are produced with ArcGIS. The about page does not offer shapefiles for download [@glob-gae-about]. The search for "greatamericaneclipse.com shapefiles GIS 2024" returned no data page, and the site's `/eclipse-data` URL returned 404.

John Irwin's besselianelements.com publishes a "true limb" 2024 path whose limits "account for the topographic elevation, both around the limb of the Moon and on the surface of the Earth", drawn for solar radii of 959.90 and 960.00 arcseconds around $959.95'' \pm 0.05''$ and using "the most recent determinations of... the Earth's orientation parameters". The limb dataset and formats are not named on the pages read, and the technical-details page shows its parameters as an image [@glob-besselianelements-2024] [@glob-besselianelements-tech] [@glob-besselianelements-jagged].

The Photographer's Ephemeris (Photo Ephemeris) documents a vendor implementation: elements "provided by Fred Espenak and published by NASA", local circumstances and paths after "Jean Meeus, Elements of Solar Eclipses 1951–2200; The Astronomical Almanac 2023", paths at "0.1 degrees in longitude calculated for an observer at sea level", "no correction is made for the lunar limb profile", path accuracy "±1–2 km", and elevation from SRTM3, ASTER GDEM and Google. Its $\Delta T$ comes from Meeus's table to 2006, USNO `deltat.data` to 2024, USNO predictions to 2034 and polynomials beyond, with the USNO values overriding NASA's per-eclipse values. For 2017 NASA's 70.3 s was replaced by 68.8373 s [@glob-photoephemeris]. Radiant Drift's API returns GeoJSON for the central path, northern and southern limits of totality and of partial eclipse, lines of equal magnitude and a totality polygon, with point spacing from 1° down to 0.025°, and lists open issues at extreme latitudes and the antimeridian. It does not describe its algorithm [@glob-radiantdrift].

## Occult and USNO

Occult 4 (David Herald) covers "solar and lunar eclipses, transits of Mercury and Venus" and, per Steve Preston's tutorial, downloads LOLA lunar limb data, offers "Show LOLA high resolution limb" and Kaguya options for graze profiles, references paths to WGS84 with altitude above mean sea level, and exports occultation paths to Google Earth KMZ [@glob-occult4] [@glob-occult-tutorial]. The tutorial does not describe the solar-eclipse global-circumstances output, so what Occult writes for eclipse limits remains an open item. USNO's Solar Eclipse Computer gives local circumstances only, "iteratively computing topocentric positions of the Sun and Moon", with IAU radii of 696,000 km and 1737.4 km and no limb profile [@glob-usno-sec].

## Stellarium

Stellarium's `src/core/SolarEclipseComputer.cpp` (the class is `SolarEclipseComputer`, found by searching the repository) computes Besselian elements at run time from its own Sun and Moon positions, with derivatives from $\pm 5$-minute differences, and provides `generateEclipseMap`, which classifies the eclipse by $\gamma$ against 0.9972 and $1.5433 + L_2$, finds P1 to P4 by `getJDofContact`, computes the greatest-eclipse point, the penumbral and umbral limits by `computeNSLimitsOfShadow`, the rise/set curves between P1–P2 and P3–P4 at one-minute steps, the maximum-at-horizon curve, the central line and umbral outlines. It writes a PNG map and a KML document with placemarks for greatest eclipse and first and last contact with Earth, and styled `LineString` and polygon features for the total, annular, hybrid and penumbral limits [@glob-stellarium-sec]. Its constants are 6378.1366 km, 696,000 km, $k = 0.2725076$ and the code constant `s` = 0.272281. The source comments that "durations seem to agree with NASA" with the two-$k$ choice [@glob-stellarium-sec].

## Swiss Ephemeris

`swe_sol_eclipse_where` returns in `geopos[0..1]` the "geographic longitude of central line" and latitude, and in `attr` the fraction of diameter covered, the diameter ratio, the obscuration and the core-shadow diameter in km [@glob-swisseph-doc]. The implementation, `eclipse_where` in `swecl.c`, does not use Besselian elements. It forms the Sun–Moon unit vector $\mathbf{e}$, the Moon's distance from the fundamental plane `s0` $= -\mathbf{r}_m\cdot\mathbf{e}$, which is the almanac's $z$ and not the almanac's $s_0$, the axis distance `r0` $= \sqrt{d_m^2 - \mathtt{s0}^2}$, the umbra and penumbra diameters on the plane `d0` $= (\mathtt{s0}(2 r_\odot - d_{moon})/d_{sm} - d_{moon})/\cos f_1$ and `D0` $= (\mathtt{s0}(2r_\odot + d_{moon})/d_{sm} + d_{moon})/\cos f_2$, tests centrality by $R_\oplus\cos f_1 \ge$ `r0`, finds the surface point at $\mathbf{r}_m + (\mathtt{s0} - \sqrt{\mathtt{s0}^2 + R_\oplus^2 - d_m^2})\mathbf{e}$, and treats oblateness by dividing the $z$ coordinates by $(1 - f)$ and iterating once on the latitude found. Constants: `DMOON 3476300.0 m`, `DSUN 1392000000.0 m` (alternatively 1391978489.9 m, "consistent with" the IAU 1976 angular radius), Earth radius 6378140 m. The umbra diameter at the surface is `(s/dsmt*(2*drad - dmoon) - dmoon)*cosf1`, positive meaning annular [@glob-swisseph-swecl]. There is no function for limits or outlines. A caller must construct them by sampling `swe_sol_eclipse_how` on a grid.

## GitHub implementations

The full repository inventory and its comparison matrix are in [GitHub
repositories](../09-software-and-repos/github-repositories.md). This section
keeps only what each repository does for a path product. The searches were "github besselian elements eclipse path central line umbra limits python", "Stellarium source SolarEclipseComputation", "skyfield solar eclipse path totality Besselian OR umbra github notebook Rhodes", and "eclipse GeoJSON OR KML path totality generator open source github Besselian". They found:

- `enrique7mc/solar-eclipse-2027` (JavaScript, `src/eclipse.js`): elements from NASA GSFC for 2027 August 2, $f = 1/298.257$, $k_2 = 0.272281$, $\Delta T = 71.7$ s. It uses a line–ellipsoid quadratic, limits by a sweep envelope perpendicular to the ground-relative motion, outlines at 90 angles and durations by bisection. `scripts/check-elements.mjs` compares with the NASA path table, "positions agree to about 1 km and durations to 0.1 s" [@glob-enrique7mc].
- `RHerAle/Eclipse-Engine` (JavaScript, `js/besselian.js`, AGPL): elements "fitted to JPL DE440s" in `data/eclipses.json`, WGS84 flattening, central line at 6-second steps over $\pm 4$ h, limits with five iterations on ground-relative velocity, outlines at 181 angles to convergence, obscuration grid and contours. Validation is against the project's own Python chain [@glob-rherale].
- `aravpanwar/besselian` (Python): $k_1 = 0.272488$, $k_2 = 0.272281$, $\Delta T = 76.0$ s for 2027, exact central-line solve, greatest eclipse versus greatest duration 215 km apart, checks against NASA (greatest-eclipse position to $10^{-5}$ Earth radii, duration 382.5 s against 6m23s) [@glob-aravpanwar].
- `SR123/eclipse-2026` (JavaScript, `eclipse.js`): NASA elements with $t_0 = $ 18:00 [?tt|TDT], $\Delta T = 71.4$ s, Meeus *Astronomical Algorithms* ch. 54 for the classification, per-location circumstances by contact bisection. It warns of edge sensitivity [@glob-sr123].
- `RyuuNeko1107/umbra-rs` (Rust): six crates, `umbra-geo` for central line and limits, all marked work in progress with precision targets "not published as guarantees until validated against JPL DE" [@glob-umbra-rs].
- `plhery/umbra-eclipse-atlas` (TypeScript): elements from the Five Millennium Canon through `@astronomy-bundle/solar-eclipse`, exports GeoJSON, KML/KMZ, GPX and CSV. It calls itself "a planning aid, not an official prediction service" [@glob-plhery].
- `Frencil/eclipsetracks` issue 9: the Cesium app uses NASA surface-track tables and the issue to move to Besselian elements "remains open" [@glob-eclipsetracks-issue9].
- Skyfield: discussion 801 has Brandon Rhodes explaining that the subpoint of the Sun is not the shadow, that a line–ellipsoid intersection "would be needed" and that Skyfield "lacks a built-in routine for calculating eclipse shadow paths". Issue 1078 and PR 1076 add detection and classification of solar eclipses by the lunar-eclipse minimum-angle method, not paths [@glob-skyfield-801] [@glob-skyfield-1078].
- celestialprogramming.com: JavaScript for generating Besselian polynomial coefficients from DE405 at five times by Gauss–Jordan fit, with $k = 0.2725076$, solar radius $6.957\times10^8$ m and Earth radius $6.3781\times10^6$ m per IAU 2015 Resolution B3, citing Chauvenet, Green, Smart and the 2013 Supplement [@glob-celestialprogramming].
- MATLAB: David Eagle's implementation of Meeus's Elements requires the `ECLIPSE.ELS` file sold by Willmann-Bell [@glob-matlab-meeus].

No repository found implements limb-profiled limits or a terrain-corrected umbra. The 2027 visualiser, Eclipse-Engine and `besselian` all state that they use a smooth Moon. `besselian` notes that NASA's limb corrections "shifting path limits 1-2 km" appear 12 to 18 months before an event [@glob-aravpanwar]. This is a negative finding: as of the searches above, no open-source implementation of the limb-corrected path edge exists in Python, JavaScript, Rust or C.

## A worked pipeline: polynomials to GeoJSON

The inputs are a set of NASA polynomial elements and a time step $\delta t$. The elements are $x, y, d, \mu, l_1, l_2$ as cubics in $t$ hours from $t_0$ in TDT, the constants $\tan f_1$ and $\tan f_2$, and the ΔT the table was made with. TDT, TD and TT are one scale, and ET is the pre-1984 name for it.

1. **Evaluate elements and rates.** $a(t) = \sum a_n t^n$, $a'(t) = \sum n a_n t^{n-1}$ per hour. Convert $d$ and $\mu$ to radians, so that $\mu'$ is in radians per hour [@glob-nasa-tp2001].
2. **Shift $\mu$ for $\Delta T$.** $\mu_{UT} = \mu - 1.002738 \times 15\,\Delta T$ arcseconds, so that longitudes come out in UT while the geometry stays in TT [@glob-rherale].
3. **Earth constants.** Choose $e^2$ (WGS84: $f = 1/298.257223563$). Compute $\rho_1$, $\rho_2$, $\sin d_1$, $\cos d_1$, $\sin(d_1 - d_2)$, $\cos(d_1 - d_2)$ once per time [@glob-es1961].
4. **Central line.** $\xi = x$, $\eta_1 = y/\rho_1$, $p = 1 - \xi^2 - \eta_1^2$. If $p < 0$ skip the time. Else $\zeta_1 = \sqrt p$, $\zeta = \rho_2[\zeta_1\cos(d_1 - d_2) - \eta_1\sin(d_1 - d_2)]$, then $\theta = \operatorname{atan2}(\xi, -\eta_1\sin d_1 + \zeta_1\cos d_1)$, $\lambda_E = \theta - \mu_{UT}$, $\phi = \arctan[\tan\phi_1/\sqrt{1 - e^2}]$ with $\sin\phi_1 = \eta_1\cos d_1 + \zeta_1\sin d_1$ [@glob-es1961] [@glob-stellarium-sec].
5. **Duration, ratio, width at the central point.** $L_2 = l_2 - \zeta\tan f_2$, $L_1 = l_1 - \zeta\tan f_1$, $\xi' = \mu'(-y\sin d + \zeta\cos d)$, $\eta' = \mu' x\sin d - d'\zeta$, $n = |(x' - \xi', y' - \eta')|$, duration $= 2L_2/n$ hours, magnitude $L_1/(L_1 + L_2)$, ratio $= 1 + 2(\text{mag} - 1)$, width by Mikhailov's formula [@glob-es1992] [@glob-stellarium-sec].
6. **Limits.** For each cone, start $\zeta = 0$, $L = l$, $\tan Q = b'/c'$ with $b' = -y' + \mu' x\sin d$, $c' = x' + \mu' y\sin d + \mu' l\tan f\cos d$. Scan $Q$ for the two roots of the conditional equation, then iterate $\xi = x - L\sin Q$, $\eta_1 = (y - L\cos Q)/\rho_1$, $\zeta_1 = \sqrt{1 - \xi^2 - \eta_1^2}$, $\zeta$, $L$, $Q$ until $\zeta$ changes by less than $10^{-5}$. Assign north or south by the sign of $L\cos Q$. Drop points with $\zeta_1^2 < 0$ or $\zeta_1 < 0$ [@glob-es1961] [@glob-es1992].
7. **Outline at each time.** For $Q$ from 0 to 360 in 1 to 4 degree steps, iterate $L = l - \zeta\tan f$ as in step 6 to convergence. Where $1 - \xi^2 - \eta_1^2 < 0$ either break the ring (Eclipse-Engine) or substitute the terminator point in that direction (2027 visualiser) [@glob-rherale] [@glob-enrique7mc].
8. **Assemble GeoJSON.** Write `LineString` features for `center`, `north_limit` and `south_limit` with `time` arrays. Write one `Polygon` per time step for `umbra` with `properties.utc`. Write a `Polygon` for the path formed by the northern limit forward and the southern limit backward, closed at the extreme points from the $\zeta_1 = 0$ solution. Split any feature crossing the antimeridian, and near the poles test longitude jumps as well as distance, as Eclipse-Engine does [@glob-rherale]. Use the SVS attribute convention of a UTC string and integer seconds past midnight per polygon [@glob-svs-4518].
9. **Validate.** Compare three central-line rows and the "Limits" row against the NASA path table for the eclipse, expecting 1 km and 0.1 s [@glob-nasa-path-2024] [@glob-enrique7mc].
10. **Label the product.** State the $k$ values, $\Delta T$, ellipsoid, and that the Moon is smooth and the observer at sea level. Keep any limb-corrected product in a separate file.

## Sources compared

| Product or code | Curves and formats | Limb | Terrain | Grade |
|---|---|---|---|---|
| NASA path tables [@glob-nasa-path-2024] | HTML tables, 2-min rows, limits and centre, width, duration | No (1–2 km) | Sea level | primary |
| NASA bulletins [@glob-nasa-tp2001] | Tables 3–8, graze zones at 30' longitude, Elev Fact | Yes, in Tables 6 and 8 (Watts) | Via Elev Fact | primary |
| SVS 2017 and 2024 [@glob-svs-4518] [@glob-svs-5123] | Shapefiles: umbra 1 s/10 s/1 min/10 min, path, centre, duration, obscuration contours | Yes (LOLA, SLDEM2015) | Yes (SRTM) | primary |
| NOAA SOS and Hub [@glob-noaa-sos] [@glob-noaa-hub] | Repackaged SVS shapefiles | As SVS | As SVS | primary |
| Jubier [@glob-jubier-maps] [@glob-jubier-help] | Google Maps, KML/KMZ, grazing-zone maps | Yes (online LC) | Elevation tool | company |
| GreatAmericanEclipse [@glob-gae-about] | ArcGIS maps, no data download found | Yes, via Jubier | Not stated | company |
| Irwin [@glob-besselianelements-2024] | Map images of true-limb limits | Yes | Yes | trade |
| Photo Ephemeris [@glob-photoephemeris] | Paths at 0.1° longitude | No | Sea level, DEM for local | company |
| Stellarium [@glob-stellarium-sec] | PNG and KML, all classic curves | No | No | company |
| Swiss Ephemeris [@glob-swisseph-swecl] | Central point and umbra diameter only | No | Height in `_how` only | company |
| 2027 visualiser, Eclipse-Engine, besselian [@glob-enrique7mc] [@glob-rherale] [@glob-aravpanwar] | In-browser polygons, GeoJSON-ready arrays, CSV/JSON | No | Local only | company / unsourced |

## What a developer should do

1. Download `eclipse2017_shapefiles_1s.zip` and `2024eclipse_shapefiles.zip` from SVS and use them as the ground truth for any limb-corrected product. Compare a smooth-Moon umbra outline against `umbra17_1s` at the same second to measure the limb and terrain effect directly [@glob-svs-4518] [@glob-svs-5123].
2. Use the NASA path table as the ground truth for the smooth-Moon product and reproduce it to 1 km before adding anything [@glob-nasa-path-2024].
3. Read `SolarEclipseComputer.cpp` for the classic curves and `src/eclipse.js` of the 2027 visualiser for the compact ellipsoid formulation. Read Eclipse-Engine's comments for the antimeridian, pole and convergence pitfalls [@glob-stellarium-sec] [@glob-enrique7mc] [@glob-rherale].
4. Do not build on the Swiss Ephemeris for global circumstances. It gives the centre only [@glob-swisseph-doc].

## What this changes

The pipeline gains a validation contract: smooth-Moon output must match NASA tables, and limb-corrected output must be compared against SVS 1-second umbra polygons. It also fixes the product split: NASA-style tables and classic curves from Besselian polynomials on one side, limb-profiled polygons from the lunar DEM on the other.

## Open questions

- The contents and attribute schema of NOAA's ArcGIS Hub "2024 Eclipse Shapefiles" item, which rendered only its title [@glob-noaa-hub].
- Whether Occult 4 exports solar-eclipse limits with LOLA limb corrections, and in what format. The tutorial covers occultations only [@glob-occult-tutorial].
- The limb dataset, terrain DEM and export formats behind Irwin's true-limb 2024 path, shown only as an image table on the technical page [@glob-besselianelements-tech].
- Jubier's KML file structure for a specific eclipse (which curves, at what sampling), which requires downloading a KMZ from his site [@glob-jubier-maps].
- The timeanddate map methodology, unreachable at fetch time [@glob-timeanddate-magnitude].
- A copy of the SVS 2024 `umbra_hi.shp` attribute table to confirm the one-second sampling and the time fields match the 2017 convention [@glob-svs-5123].
