---
title: Commercial and institutional tools
description: What NASA GSFC, EclipseWise, NASA SVS, Jubier, Occult 4, timeanddate, GreatAmericanEclipse, McGlaun, Eclipse Orchestrator, the phone apps and USNO compute, from which inputs, and what each documents.
order: 1
status: working
updated: 2026-09-15
tags: [software, nasa, eclipsewise, jubier, occult, svs, timeanddate, apps]
---

::: summary
- **NASA GSFC publishes the elements everyone else consumes**: polynomial Besselian elements from VSOP87 and ELP2000, with $k_1 = 0.272488$ for penumbral contacts and $k_2 = 0.272281$ for umbral contacts, and ΔT from the Canon polynomials. NASA's JavaScript Solar Eclipse Explorer (JSEX) is GPL code that computes local circumstances from those elements with no limb correction and a crude refraction rule.
- **EclipseWise departs from NASA on one constant**: it uses the IAU value $k = 0.2725076$ for penumbral contacts while keeping $k = 0.272281$ for umbral contacts, and documents why with a 2017 duration comparison.
- **Jubier's maps run Espenak's elements in the browser** and add three things nobody else offers in a web page: Watts-chart and Kaguya (SELENE) DEM limb corrections fetched from his server, refraction applied to the displayed altitude and horizon at the observer's elevation on the WGS 84 ellipsoid with no correction to contact times, and Baily's beads diagrams. His 2024 page ships Espenak's elements with its own ΔT = 69.1 s.
- **NASA SVS (Wright) is the only lineage that publishes limb-corrected umbra polygons** as GIS data, computed from SRTM and LRO LOLA plus Kaguya (SELENE), at 1-second intervals for 2017, 2023 and 2024. Every SVS product page names JPL DE421, while the paper's appendix uses DE440.
- **Occult 4 is the reference for Baily's beads** in the occultation community but is a closed Windows C# binary whose eclipse documentation lives in its help file.
- **timeanddate and USNO state their simplifications**: sea-level observers, mean lunar radius, no limb profile. Consumer apps (Totality, EclipseDroid, Solar Eclipse Timer) embed Jubier's or O'Byrne's code and publish no method of their own.
:::

**The question.** For each institutional or commercial eclipse product, what does it compute, which ephemeris, lunar radius, solar radius, limb dataset, elevation model and ΔT source does it use, in what language and under what licence, and where is the method written down?

## NASA GSFC Eclipse Web Site (Espenak)

**Products.** The site publishes the Five Millennium Catalog of Solar Eclipses, NASA/TP-2009-214174, for -1999 to +3000 [@sw-nasa-5mcse-catalog], a Besselian elements page per eclipse, a path table per central eclipse, and the JavaScript Solar Eclipse Explorer. The catalogue states that "The coordinates of the Sun used in these predictions are based on the VSOP87 theory" and "The Moon's coordinates are based on the ELP-2000/82 theory" [@sw-nasa-5mcse-catalog]. The catalogue key defines [?gamma] as "Distance of the shadow cone axis from the center of Earth (units of equatorial radii) at the instant of greatest eclipse" and [?eclipse-magnitude] as "the fraction of the Sun's diameter obscured by the Moon" [@sw-nasa-5mcse-key].

**Besselian elements.** The 2024 April 8 page gives the [?besselian-elements] as cubic polynomials in $t$, decimal hours from $t_0$ = 18:00:00.0 TDT: $a = a_0 + a_1 t + a_2 t^2 + a_3 t^3$, derived from "a least-squares fit to elements calculated at five uniformly spaced times over a six hour period" and valid from 15:00 to 21:00 TDT [@sw-nasa-bessel-2024]. The stated constants are $k_1 = 0.272488$ for the penumbra, $k_2 = 0.272281$ for the umbra, ΔT = 70.6 s, and a solar semidiameter of 959.63″ at 1 au, printed as the apparent value 15′58.2″ on the date [@sw-nasa-bessel-2024]. The ephemeris is labelled "VSOP87/ELP2000-85" on that page, while the Five Millennium Catalog text describes ELP-2000/82 [@sw-nasa-bessel-2024] [@sw-nasa-5mcse-catalog]. The history of the two $k$ values, and which table prints which, is in [Besselian elements](../01-foundations/besselian-elements.md).

**ΔT.** The Canon's [?delta-t] comes from piecewise polynomials, for example before -500: $\Delta T = -20 + 32u^2$ with $u = (y - 1820)/100$, and for -500 to +500: $\Delta T = 10583.6 - 1014.41u + 33.78311u^2 - 5.952053u^3 - 0.1798452u^4 + 0.022174192u^5 + 0.0090316521u^6$ [@sw-nasa-deltatpoly]. A correction $c = -0.000012932(y - 1955)^2$ is added outside 1955 to 2005 to move the polynomials to the Canon's lunar secular acceleration of $\dot n = -25.858$ arcseconds per century squared [@sw-nasa-deltatpoly] [@sw-nasa-5mcse-catalog]. The models themselves, their uncertainty and the per-predictor values are in [ΔT and Earth rotation](../07-earth-and-time/delta-t-and-earth-rotation.md).

**Path tables.** The path page lists northern limit, southern limit and central line in WGS 84 at 120-second intervals with the diameter ratio, Sun altitude and azimuth, [?path-width] in kilometres and central duration [@sw-nasa-path-2024].

**JavaScript Solar Eclipse Explorer.** Version 1 by Chris O'Byrne and Fred Espenak (2007) builds on the 2003 "Eclipse Calculator" by O'Byrne and Stephen McCann, and the file header releases it under the GNU GPL version 2 or later [@sw-nasa-jsex-program-js]. The index page states that "Besselian elements and values of ΔT used in Solar Eclipse Explorer are the same as those used by Five Millennium Canon of Solar Eclipses" and restricts use to -1499 to 3000 because the ΔT uncertainty grows beyond that [@sw-nasa-jsex-index]. The code computes the observer's geocentric constants with flattening factor 0.99664719 and radius 6378140 m:

$$\rho\sin\phi' = 0.99664719\sin u + \frac{h}{6378140}\sin\phi,\quad \rho\cos\phi' = \cos u + \frac{h}{6378140}\cos\phi,\quad u = \arctan(0.99664719\tan\phi)$$

where $\phi$ is geodetic latitude and $h$ is height in metres [@sw-nasa-jsex-program-js]. The hour angle is $h = \mu - \lambda_W - \Delta T/13713.44$ where 13713.44 converts seconds of ΔT to radians of Earth rotation, and the [?fundamental-plane] coordinates are

$$\xi = \rho\cos\phi'\sin h,\quad \eta = \rho\sin\phi'\cos d - \rho\cos\phi'\cos h\sin d,\quad \zeta = \rho\sin\phi'\sin d + \rho\cos\phi'\cos h\cos d$$

with $u = x - \xi$, $v = y - \eta$, $l_1' = l_1 - \zeta\tan f_1$, $l_2' = l_2 - \zeta\tan f_2$ [@sw-nasa-jsex-program-js]. Contacts C1 and C4 are found by iterating on $l_1'$ and C2 and C3 on $l_2'$ [@sw-nasa-jsex-program-js]. [?obscuration] is computed from the lens-area formula using $l_1'$, $l_2'$ and the separation $m$ at maximum [@sw-nasa-jsex-program-js]. There is no limb correction, and the code comment says a full refraction correction "will involve creating a 'virtual' altitude for each contact"; the implemented rule only treats altitudes between 0 and -0.00524 rad as on the horizon [@sw-nasa-jsex-program-js].

## EclipseWise.com (Espenak)

The help page on the mean lunar radius states the convention: "Solar eclipse predictions appearing on EclipseWise.com use the IAU's accepted value of k (k=0.2725076) for all penumbral (exterior) contacts. However, the predictions here depart from IAU convention by adopting the smaller value for k (k=0.272281) for all central (interior) contacts" [@sw-eclipsewise-radius]. It explains the USNO 1968 to 1980 practice of $k = 0.2724880$ for penumbral and $k = 0.272281$ for umbral contacts, the IAU 1982 adoption of 0.2725076, and the misidentification of the 1986 Oct 03 eclipse as total [@sw-eclipsewise-radius]. Its comparison for the 2017 central line in Shawnee National Forest gives 2m44.3s from USNO with the IAU $k$, 2m40.3s from EclipseWise with $k = 0.272281$, 2m41.5s from the Eclipse Bulletin using the actual limb profile, and 2m41.4s from Jubier's map using the limb profile [@sw-eclipsewise-radius]. The 2024 page advertises the Eclipse Bulletin extras: libration values, penumbral and umbral shadow contact data, central line data, polynomial Besselian elements and a lunar limb profile from the central line at 19:15 UTC [@sw-eclipsewise-2024]. The site's general calculation help page (`SEcalc.html`) returned 403 live and is not in the Wayback Machine, so the ephemeris behind EclipseWise's own tables is not documented in this note.

## NASA Scientific Visualization Studio (Wright)

This note inventories the products only. The methodology is covered by [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md).

**Data sources.** SVS 5073 states: "The eclipse data were calculated by visualizer Ernie Wright using elevation information from SRTM, lunar topography from LRO, and planetary positions from the JPL DE421 ephemeris" [@sw-svs-5073]. The dataset list on that page names SRTM from SIR-C, the LRO LOLA DEM, and SLDEM2015 from LOLA and the SELENE Terrain Camera [@sw-svs-5073]. DE421 is what the product pages name. The paper's appendix uses DE440, and the difference is under a metre at the Moon [@sw-svs-5073]. The 2017 page adds that "Lunar topography, used for precise shadow calculations, is from NASA LRO laser altimetry and JAXA Kaguya stereo imaging" and that "The lunar limb profile and eclipse calculations are by the visualizer" [@sw-svs-4518].

**Released files.** For 2023 and 2024: `2023eclipse_shapefiles.zip`, `2023eclipse_kml.zip`, `cities-eclipse-2023.json`, `2024eclipse_shapefiles.zip`, `2024eclipse_kml.zip`, `cities-eclipse-2024.json` [@sw-svs-5073]. Each zip contains `center` (high-resolution centre polyline, region limited), `duration` (isocontours of maximum total or annular duration at 30-second intervals), `ppath` and `ppath01` (contours of maximum obscuration at 5 per cent and 1 per cent), `umbra_hi` (umbra or antumbra polygons at 1-second intervals, region limited), `umbra_lo` (10-second intervals, global), `upath_hi` and `upath_lo` (path shapes) [@sw-svs-5073]. The city JSON gives, for over 32,000 US cities, `LON`, `LAT`, `NAME`, `STATE` and `ECLIPSE`, "An array of UTC times for the [0.01%, 50%, 100%, 50%, 0.01%] points of coverage (normalized with respect to the maximum coverage achieved)" [@sw-svs-5073]. For 2017 the files are `eclipse2017_shapefiles.zip` and `eclipse2017_shapefiles_1s.zip` [@sw-svs-4518]. SVS 5123 repeats the 2024 shapefile link [@sw-svs-5123].

**The SVS Eclipse Explorer web app.** The SVS Eclipse Explorer web app (SVS 5169) is served at eclipse-explorer.smce.nasa.gov and is script-rendered, so only its HTML shell was retrievable [@sw-nasa-eclipse-explorer-app]. It is a different product from the JavaScript Solar Eclipse Explorer above. No code release from SVS was found on the product pages [@sw-svs-5073] [@sw-svs-4518].

## Xavier Jubier

**Interactive Google Maps.** The 2024 map page embeds an element array (`elements`) with $t_0$ at JD 2460409.26284, 18.0 h, ΔT = 69.1 s, and coefficients $x_0 = -0.31824401$, $x_1 = 0.51171160$, $y_0 = 0.21976399$, $d_0 = 7.58620024$, $\mu_0 = 89.59121704$, $l_{1,0} = 0.53581399$, $l_{2,0} = -0.01027200$, $\tan f_1 = 0.00466830$, $\tan f_2 = 0.00464500$, and a header stating "ΔT: 69.1s, σ = ±4s" [@sw-jubier-2024-map]. These agree with NASA's 2024 page to the six decimals NASA prints, and they are the Five Millennium Catalog coefficients to every printed digit. Only the ΔT is Jubier's own, 69.1 s against 70.6 s on NASA's separately computed element page, so Jubier uses Espenak's elements with his own ΔT [@sw-jubier-2024-map] [@sw-nasa-bessel-2024]. The page loads `EclipseCalculatorGM3_xSE.js`, `GoogleMap3_TSE_2024.js`, `GoogleMap3_DayNight.js` and `GoogleMap3_Geolocation.js` [@sw-jubier-2024-map].

**The calculator code.** The calculator's change log records the capabilities in order: "2008-01-18 Added altitude with refraction (no time correction)", "2009-01-05 Moon libration calculation for Watts chart", "2009-01-29 Lunar limb corrections with Watts chart", "2009-11-20 Lunar limb corrections with Kaguya's DEM", "2010-06-31 Added elevation profile at click location", "2013-01-31 Solar mesosphere 0.5" correction (add &Mes=1 to URL)", "2016-01-03 (Ant-)Umbral shadow outline at maximum eclipse, c1, c2, c3 and c4" [@sw-jubier-calc-js]. The Earth model is WGS 84: equatorial radius 6378137.0 m, polar radius 6356752.314245 m, $e^2 = 0.00669437999014$ [@sw-jubier-calc-js]. The solar radius the help page states is 959.63″. The client code carries a rounded 0.26667°, which is 16′, for drawing [@sw-jubier-calc-js]. The lunar radius ratio is switchable: `lambdak1k2 = 1.00076024401` for $k_1 = 0.2724880$ and $k_2 = 0.2722810$ (the default when `gVSOP == 1`), or `1.00083222847` for $k_1 = 0.2725076$ and $k_2 = 0.2722810$ (IAU 1982, when `gVSOP == 0`) [@sw-jubier-calc-js]. Limb corrections are not computed in the browser. The client calls `/php/php85/WattsChartCorrections.php` with the Moon's distance, libration in longitude and latitude, position angles of C2 and C3 and the duration, and `/php/php85/WattsChartBailyBeads.php` for the beads diagram. The link title chooses "Watts" when the libration in latitude exceeds 1.6° in absolute value and "Kaguya" otherwise [@sw-jubier-calc-js]. The refraction constant is `gRefractionHeight = -0.01454` rad for standard refraction at the horizon, and `elevationRefraction()` adjusts the horizon for the observer's elevation [@sw-jubier-calc-js]. The index page describes the map icons for the terrain elevation profile and shows a "Lunar limb profile and Baily's beads screenshot" [@sw-jubier-gm-index]. The 5MCSE interface generates maps and KMZ on the fly for all 11,898 eclipses from data "provided by Fred Espenak and Jean Meeus" [@sw-jubier-5mcse].

**Solar Eclipse Maestro.** Version 1.9.0v1 (2019-06-09), macOS only, donationware, runs on MacOS X 10.4 to 10.14 and "will not be compatible with macOS Catalina" [@sw-jubier-sem]. It "can handle any solar eclipse, provide you Baily's beads preview and animation, simulate an all-sky view or weather statistics" and controls up to four cameras with optional Garmin GPS input [@sw-jubier-sem]. The page does not name the limb dataset behind the beads preview. The Maestro help pages do, and they are quoted in [limb profile methods](../05-lunar-limb/limb-profile-methods.md).

## Occult 4 (Herald, IOTA)

Occult v4.2024.x.x by David Herald computes "Solar and lunar eclipses, transits of Mercury and Venus" alongside occultations by asteroids, the Moon and planetary satellites [@sw-occult4]. It is written in C# on .NET Framework 4.5, Windows only, distributed as `OccultInstaller.zip` (12.9 MB) plus `InstallResources.zip` (57 MB), and downloads 42 separately revised data files including planetary ephemerides and star catalogues [@sw-occult4]. The program is free and the author asks that contributed occultation data be acknowledged [@sw-occult4]. The IOTA page lists tutorials by Dave Gault and David Dunham but no eclipse method statement [@sw-iota-occult]. The eclipse and limb-profile topics are inside `Occult.chm`, which was not read [@sw-occult4]. Occult's ephemeris is named by version across the corpus: DE441 for version 4.2023, DE435 and DE422 for occultations, and DE423 for version 4.0.8.6. Those per-version readings are collected in [predictor disagreements](../10-validation/predictor-disagreements.md) [@sw-occult4].

## timeanddate.com

The accuracy page states: "Our calculations do not take elevation into account; they are based on sea level for each location" and "There are mountains and valleys on the Moon, so its shadow has a slightly rugged edge. Solar eclipse predictions usually do not take this factor into account" [@sw-timeanddate-accuracy]. It attributes remaining uncertainty to ΔT, the shapes of Earth and Moon, and the solar diameter, whose "margin of error is only about 0.03%, but that it is enough to influence the times for a solar eclipse by a few seconds" [@sw-timeanddate-accuracy]. It claims consistency with NASA and the Astronomical Almanac but names no ephemeris, $k$ or ΔT source [@sw-timeanddate-accuracy].

## GreatAmericanEclipse.com (Zeiler)

The home page credits "Eclipse predictions by Fred Espenak, and eclipse computations by Xavier Jubier", says "The Moon's shadow reflects the true shape of the Moon as influenced by the many craters and mountains on the lunar limb", and that the team "used detailed terrain data from the NASA Lunar Reconnaissance Orbiter" with frames "composed in ArcGIS Pro and Adobe Illustrator with additional specialized Python and Javascript code" [@sw-gae-home]. The 2024 page and FAQ add only the ArcGIS attribution [@sw-gae-2024] [@sw-gae-faq]. No downloadable path data was found on the site.

## Eclipse2024.org simulator (McGlaun)

eclipse2024.org now redirects to solareclipses.com, run by 5th Contact LLC, which lists a simulator, state map views and simulation videos for over 2,200 cities [@sw-solareclipses-2024]. The simulator page describes itself as "detailed and accurate" but states no method, element source, limb data or ΔT [@sw-solareclipses-sim]. This is a negative finding after reading both pages.

## Eclipse Orchestrator (Bruenjes)

Windows software, version 3.9.3 released 2024-03-28, Free and Pro ($109) editions, first written for the 2002 eclipse [@sw-eo-index]. It computes local circumstances from entered coordinates and supports "Refraction, limb effects, and delta-T correction" with "UTC event times for subsecond accuracy", a Pro-only "Baily's Beads simulation", GPS NMEA input and 1 PPS timing [@sw-eo-features]. The author's 2024 advice was to "Use the new 959.98" solar radius (Setup | Solar Radius...) and make sure refraction and limb correction are turned ON" [@sw-eo-index]. The limb dataset is not named on either page.

## Solar Eclipse Timer (Telepun)

The site advertises "Automatic geolocation. Automatic calculation of the contact times" and a talking countdown, and states nothing about the elements, limb, elevation or ΔT [@sw-set-home]. Negative finding.

## EclipseDroid (Strickling)

Android app from version 2.0 upward, version 7 current. The page states: "The eclipse algorithms came from Deirdre O'Byrne's Java Script Eclipse Calculator" and that a database of eclipses from 3000 BC to 3000 AD is downloadable, credited to O'Byrne [@sw-eclipsedroid]. The local circumstances screen shows "the assumed value of delta T and the altitude above sea level" [@sw-eclipsedroid]. This is therefore the same Besselian local-circumstance algorithm as NASA's JSEX, without limb correction.

## Totality (Big Kid Science)

Free iOS and Android app by Jeffrey Bennett with Rick Fienberg as scientific advisor, covering all total eclipses through 2050, with "Eclipse code by Xavier Jubier" and "Maps based on eclipse code graciously provided by Xavier Jubier" [@sw-totality-app].

## USNO Solar Eclipse Computer

The USNO service covers 2017 to 2026, computes "topocentric positions of the Sun and Moon" iteratively to find maximum eclipse and then the contacts, reports magnitude, obscuration and durations, uses "radius values adopted by the International Astronomical Union", does not apply "lunar limb profiles and center of mass/center of figure corrections", and offers a JSON API [@sw-usno-sec].

## Sky & Telescope and other calculator apps

No page describing a Sky & Telescope eclipse calculator or a generic "Eclipse Calculator" app's method was reached at the time of writing (2026 September). This is an unresolved item rather than a negative finding, and it is recorded as an open question below.

## Sources compared

Which predictor uses which ephemeris, ΔT, radius, limb and terrain is tabulated once, in [predictor disagreements](../10-validation/predictor-disagreements.md). This table keeps the product, licence and documentation columns this note owns, with the constants repeated for convenience.

| Tool | Computes | Ephemeris | $k$ | Solar radius | Limb | Elevation and refraction | ΔT | Language, licence | Method documented |
|---|---|---|---|---|---|---|---|---|---|
| NASA GSFC tables [@sw-nasa-bessel-2024] | Catalogue, elements, paths | VSOP87, ELP2000 | 0.272488 / 0.272281 | 959.63″ at 1 au, printed as 15′58.2″ apparent on the date | No | No | Canon polynomials | Static HTML | Yes |
| NASA JSEX [@sw-nasa-jsex-program-js] | Local circumstances | Canon elements | Canon | Canon | No | Crude horizon rule | Canon | JavaScript, GPL 2+ | Code |
| EclipseWise [@sw-eclipsewise-radius] | Catalogue, elements, bulletins | Not read | 0.2725076 / 0.272281 | Not stated | Bulletins | Not stated | Not stated | Static HTML | Partly |
| NASA SVS [@sw-svs-5073] | Umbra polygons, paths, city times | JPL DE421 on the product pages, DE440 in the paper | Not stated | Not stated | LOLA, Kaguya | SRTM | Not stated | None released | Product pages |
| Jubier maps [@sw-jubier-calc-js] | Local circumstances, outlines, beads | Espenak's Canon elements | 0.2724880 / 0.2722810 default | 959.63″ per the help page, with a rounded 0.26667° (16′) in the client code for drawing | Watts, Kaguya | WGS 84, elevation, refraction on the displayed altitude only | Own (69.1 s for 2024) | JavaScript, unlicensed | Code |
| Maestro [@sw-jubier-sem] | Local circumstances, beads, camera control | Not stated | Not stated | Not stated | Yes | Not stated | Not stated | macOS binary | No |
| Occult 4 [@sw-occult4] | Eclipses, occultations, beads | JPL DE files | Not stated | Not stated | Yes | Not stated | Not stated | C# binary, free | Help file |
| timeanddate [@sw-timeanddate-accuracy] | Local times, maps | Not stated | Mean radius | Not stated | No | Sea level | Yes, unnamed | Web service | Caveats only |
| USNO [@sw-usno-sec] | Local circumstances, JSON | Not stated | IAU | IAU | No | Not stated | Not stated | Web API | Partly |
| Eclipse Orchestrator [@sw-eo-features] | Local circumstances, beads simulation | Not stated | Not stated | 959.98″ advised | Yes | Refraction | Yes | Windows, $109 Pro | Feature list |
| EclipseDroid [@sw-eclipsedroid] | Local circumstances | O'Byrne database | O'Byrne | O'Byrne | No | Altitude entered | Shown | Android, paid and free | Attribution |
| Totality [@sw-totality-app] | Maps, times | Jubier | Jubier | Jubier | Jubier | Jubier | Jubier | iOS, Android, free | Attribution |

## What a developer should do

Take the Besselian elements from NASA's CSV [@sw-nasa-bessel-csv] and reproduce NASA's JSEX local circumstances first, because that code is GPL and short [@sw-nasa-jsex-program-js]. Then match Jubier's 2024 elements and ΔT [@sw-jubier-2024-map] to learn how much the element source alone moves contact times. Use EclipseWise's $k$ discussion [@sw-eclipsewise-radius] to decide the penumbral and umbral radius convention and record it in the product. Treat SVS umbra polygons [@sw-svs-5073] as the target for any limb-corrected shadow outline.

## What this changes

Nothing in the pipeline stages. It fixes the validation plan: NASA JSEX for local circumstances without limb, Jubier's map for limb-corrected contacts, SVS shapefiles for the umbra outline.

## Open questions

- Obtain `Occult.chm` from an Occult 4 installation and read the "Solar eclipses" and "Lunar limb profile" topics to record which limb dataset Occult ships [@sw-occult4].
- Obtain a method page for a Sky & Telescope eclipse calculator, or establish that no such product exists.
- Obtain Jubier's `WattsChartCorrections.php` output for one location and compare the C2 and C3 corrections against an independent LOLA-based computation [@sw-jubier-calc-js].
- Obtain EclipseWise's `SEcalc.html` (403 live, not archived) to confirm the ephemeris and ΔT behind its tables.
- Obtain the Eclipse Orchestrator user guide PDF to identify the limb dataset behind its "limb effects" option [@sw-eo-features].
