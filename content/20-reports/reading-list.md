---
title: Reading list and reference matrix
description: The papers, code and datasets a developer should take in order, and what each one uniquely provides.
order: 4
status: working
updated: 2026-09-16
---

::: summary
- **Read four documents first**: Wright and Young 2024 for the state of the art, section 9 of the 1961 Explanatory Supplement for the formulas, Quaglia and colleagues 2021 for the solar radius and the edge sensitivity, and Herald 1983 for the limb correction [@svs-wright-young-2024] [@bes-es1961] [@val-quaglia-2021] [@limb-herald-1983].
- **Read three source files**: Stellarium's `SolarEclipseComputer.cpp`, NASA's `program.js`, and the Swiss Ephemeris `swecl.c`. Together they cover elements, every global curve, local circumstances and the geometric alternative [@sw-stellarium-sec-cpp] [@sw-nasa-jsex-program-js] [@sw-swisseph-swecl].
- **Download eight datasets**: NASA's element CSV and ASCII catalogue, the SVS shapefiles, LDEM_128 and SLDEM2015, a terrestrial DEM with its geoid, DE440 with its lunar PCK, and the USNO ΔT files.
- **The Explanatory Supplements and the NASA technical publications are free** on archive.org and eclipse.gsfc.nasa.gov. Meeus's *Elements of Solar Eclipses* and the 2013 Supplement are not, and are cited only through implementations that transcribe them.
:::

## Papers and books, in reading order

| Order | Source | Grade | What it uniquely provides | Note |
|---|---|---|---|---|
| 1 | Wright and Young 2024, AJ 168:163 [@svs-wright-young-2024] | peer-reviewed | The raster method, the limb-profile construction with bin count and refresh rule, the limb test, the broken-annular criterion, the SPICE calls, the radius survey | Open access, CC BY. Sections 4 and 5 are implementable as written |
| 2 | Explanatory Supplement 1961, chapter 9 [@bes-es1961] | peer-reviewed | Every formula for elements, global circumstances and local circumstances, with worked examples for 1961 February 15 | Free OCR on archive.org; the shortest complete statement |
| 3 | Explanatory Supplement 1992, chapter 8 [@bes-es1992] | peer-reviewed | The vector restatement, the flattening auxiliaries, the recommendation of direct root-finding, the warning list on ephemeris consistency, rotation, centre of figure, limb and refraction | Free on archive.org; OCR garbles some equations |
| 4 | Quaglia, Irwin, Emmanouilidis and Pessi 2021, ApJS 256:36 [@val-quaglia-2021] | peer-reviewed | The eclipse solar radius 959.95″ ± 0.05″, duration-versus-radius curves at the central line and at a limit, the comparison of Irwin's model with Occult and Solar Eclipse Maestro, a fully topocentric limb-based method | arXiv 2107.09416 |
| 5 | Herald 1983, JBAA 93:241 [@limb-herald-1983] | peer-reviewed | The contact-time correction from a limb profile, the limit displacement factor, the error budget of the Watts era | ADS scan |
| 6 | Espenak and Meeus 2009, Five Millennium Catalog, NASA/TP-2009-214174 [@cat-espenak-meeus-2009-catalog] | primary | The enumeration method, the ephemerides and truncation, the two $k$ values, the ΔT model with its correction, the type classification with counts, Saros tables | With the 2006 Canon, NASA/TP-2006-214141 [@cat-espenak-meeus-2006-canon] |
| 7 | Espenak and Anderson 2001 bulletin, NASA/TP-1999-209484 [@limb-espenak-tp2001] | primary | The lunar limb profile and graze zone sections, the $k$ history, the elevation factor, the Lusaka worked correction | Any bulletin from 1994 to 2009 has the same sections |
| 8 | Meeus, *Astronomical Algorithms*, chapter 54 [@cat-meeus-1991-aa] | trade | The approximate enumeration and classification with the thresholds 0.36, 0.9972, 1.5433, 0.0047, 0.00464 | 1991 edition free on archive.org as chapter 52 |
| 9 | Stephenson, Morrison and Hohenkerk 2016, Proc. R. Soc. A [@earth-smh2016] | peer-reviewed | The current ΔT spline and parabola, the lengthening-of-day rate, the historical record's scatter | Open access |
| 10 | Park, Folkner, Williams and Boggs 2021, AJ 161:105 [@moon-park-2021] | peer-reviewed | DE440 and DE441: LLR residuals, frame, the recommendation of DE440 for 1550 to 2650 | With Williams, Boggs and Folkner 2013 for the PA and ME frames [@moon-williams-2013] |
| 11 | Morrison and Appleby 1981, MNRAS 196:1013 [@limb-morrison-appleby-1981] | peer-reviewed | The systematic corrections to Watts' datum, needed only to reproduce historical bulletins | ADS scan |
| 12 | Lamy and colleagues 2015, Solar Physics 290:2617 [@sun-lamy-2015] | peer-reviewed | The largest homogeneous eclipse radius dataset, 959.99″ ± 0.06″ from 17 light curves | |
| 13 | Haberreiter, Schmutz and Kosovichev 2008, ApJ 675:L53 [@sun-haberreiter-2008] | peer-reviewed | Why the inflection-point radius exceeds the seismic radius by 0.33 Mm, the basis of the IAU nominal value | arXiv 0711.2392 |
| 14 | Prša and colleagues 2016, AJ 152:41 [@sun-prsa-2016] | peer-reviewed | What the IAU 2015 nominal radius is and is not | The reason not to use astropy's constant |
| 15 | Fiala, Dunham and Sofia 1994 [@limb-fiala-dunham-sofia-1994] | peer-reviewed | The IOTA edge method for solar radius from beads, results 1715 to 1987 | |
| 16 | Guhl and Tegtmeier 2018 and Guhl 2023, Journal for Occultation Astronomy [@val-guhl-tegtmeier-2018] [@val-guhl-2023] | trade | Per-bead residual tables for 2017 and 2023 with Occult, LOLA and Kaguya | The bead-level validation cases |
| 17 | Rozelot and Kosovichev 2026, arXiv 2605.23794 [@sun-rozelot-kosovichev-2026] | preprint | The only review tabulating canonical, nominal, seismic and eclipse radii side by side | |

## Code, in reading order

| Order | Code | Licence | What to read it for | Constants |
|---|---|---|---|---|
| 1 | Stellarium `src/core/SolarEclipseComputer.cpp` [@sw-stellarium-sec-cpp] | GPL-2.0 | Elements from an ephemeris, central line, limits, outlines, rise and set curves, KML export, with 2013 Supplement equation numbers in comments | $k$ 0.2725076 and 0.272281, Sun 696,000 km, Earth 6378.1366 km |
| 2 | NASA JavaScript Solar Eclipse Explorer `program.js` [@sw-nasa-jsex-program-js] | GPL-2+ | The 1961 local-circumstances method in 1,200 lines: observer constants, hour angle with ΔT, Newton iteration for contacts, magnitude branches, lens obscuration, P and V | $b/a = 0.99664719$, $a = 6378140$ m, ΔT/13713.44 |
| 3 | Swiss Ephemeris `swecl.c` [@sw-swisseph-swecl] | AGPL or paid | The geometric alternative: `eclipse_where` for the central point, `eclipse_how` and `eclipse_when_loc` for topocentric contacts with a bracketed search, an explicit error budget in the comments | Moon 3476.3 km, Sun 1,392,000 km, factor 0.99916 for interior contacts |
| 4 | Astronomy Engine [@cat-astronomy-engine] | MIT | A second independent enumerator in five languages, shadow axis against a dilated sphere | Sun 695,700 km, Moon 1737.4 km |
| 5 | Eclipse-Engine [@sw-repo-eclipse-engine] | AGPL-3.0 | Rasterised obscuration contours, antimeridian and pole pitfalls, the 15.041″/s ΔT rule | Elements fitted to DE440s, fitting code unpublished |
| 6 | tomasrojasc/eclipse-2026 [@sw-repo-eclipse-2026-rojas] | none stated | The only open LOLA bead construction, with the correct orientation kernel, for one eclipse | LDEM_16, `moon_pa_de421` |
| 7 | tahze0/solar-eclipse-explorer [@sw-repo-tahze0] | MIT | A template for catalogue-scale validation against the NASA CSV | 0.26 percent median width error over 300 eclipses |
| 8 | Eclipse-Engine, 2027 visualiser and `besselian` [@glob-rherale] [@glob-enrique7mc] [@glob-aravpanwar] | mixed | Compact ellipsoid formulations in JavaScript and Python, three-time validation against NASA tables | WGS84, $k_2 = 0.272281$ |

## Datasets

| Dataset | Owner | Format and size | Use | Source |
|---|---|---|---|---|
| Besselian elements CSV, 11,898 rows, 54 columns | NASA GSFC | CSV, 5.95 MB | Regression fixture for stage 3; carries $t_0$ and ΔT but not $k$ or the ephemeris | [@cat-nasa-besselian-csv] |
| Five Millennium ASCII catalogue | NASA GSFC | text, 11,898 rows | Fixture for stages 2 and 3: types, γ, magnitude, Saros | [@cat-nasa-5mkse-ascii] |
| SVS 2017, 2023 and 2024 shapefiles and cities JSON | NASA SVS | zipped shapefiles, KML, JSON | Ground truth for limb-and-terrain umbra polygons at 1 s and for city contact times | [@sw-svs-5073] [@svs-2024-shapefiles-zip] |
| LOLA LDEM_128 | NASA PDS | PDS3 IMG, 2.12 GB, 128 ppd, 237 m | Development limb dataset; 0.13″ per cell | [@limb-lola-ldem128-label] |
| SLDEM2015 and polar LDEM tiles | NASA PDS | PDS3 IMG, 512 ppd, 60 m, 3 to 4 m vertical | Production limb dataset with polar coverage above 60° | [@limb-sldem2015-label] |
| SRTM GL1 or Copernicus GLO-30, with EGM96 or EGM2008 | NASA LP DAAC, ESA | HGT or cloud-optimised GeoTIFF | Terrain stage; orthometric heights need the geoid | [@earth-srtm-guide] [@earth-copdem] |
| `de440s.bsp`, `moon_pa_de440_200625.bpc`, `moon_de440_250416.tf` (the 2025 revision of the `moon_de440_200625.tf` the paper cites) | NAIF | SPK 31 MB, binary PCK, frame kernel | Ephemeris and lunar orientation in the ME frame | [@moon-naif-summaries] [@moon-naif-moon-fk-de440] |
| `deltat.data`, `deltat.preds`, `finals.all` | USNO, IERS | text | ΔT measured and predicted with errors, UT1 and polar motion | [@earth-usno-deltat-data] [@earth-usno-deltat-preds] [@earth-iers-bulletin-a] |
| Watts charts, VizieR VI/122 | CDS | table | Only to reproduce pre-2009 bulletins, with the Morrison and Appleby corrections | [@limb-vizier-vi122] |

## Reference products for validation

| Level | Case | Values | Tolerance | Source |
|---|---|---|---|---|
| 1 | 1961 February 15, 08h ET | $\phi = +44^{\circ} 18'.3$, $\lambda = −29^{\circ} 20'.9$, duration 158.6 s | last printed digit on the same elements | [@val-es1961] |
| 1 | 2017 August 21 greatest eclipse, EclipseWise | 18:26:40.3 TD, width 114.7 km, duration 2m40.12s, DE405, ΔT 68.8 s | 0.1 s, 0.1 km | [@val-eclipsewise-2017-prime] |
| 2 | Lusaka 2001 June 21, smooth Moon | C2 13:09:19.3 UT, C3 13:12:32.8 UT | 0.5 s | [@val-tp2001-bulletin] |
| 3 | Lusaka with limb corrections | +4.0 s at C2, −1.2 s at C3 | 1 s (Watts against LOLA) | [@val-tp2001-bulletin] |
| 4 | Vale, Oregon, 2017, 711 m | C2 17:25:34.3, C3 17:26:06.9 UTC at 959.63″; limit distance 1200 m falling under 400 m at 960.00″ | 2 s, 100 m | [@val-quaglia-2021] |
| 4 | Stephenville, Texas, 2024 | observed C2 18:39:06.6, C3 18:39:20.3 UTC, 13.7 s | 3 s with true limb and 959.95″; about 24 s expected at 959.63″ as a negative control | [@val-besselian-maps-accuracy] |
| 5 | Thermopolis 2017 and Cape Range 2023 bead tables | 16 events each with axis angles and times | 1 s per event at the derived radius correction | [@val-guhl-tegtmeier-2018] [@val-guhl-2023] |

## Where the raw notes go deeper

Each topic folder ends with a "Sources compared" table and a "What a
developer should do" section. The [foundations](../10-raw/01-foundations/_index.md)
and [local circumstances](../10-raw/04-local-circumstances/_index.md) notes
quote the formulas; the [lunar limb](../10-raw/05-lunar-limb/_index.md) and
[SVS](../10-raw/11-svs-wright/_index.md) notes quote the algorithm; the
[software](../10-raw/09-software-and-repos/_index.md) note has the thirty-row
repository matrix; the [validation](../10-raw/10-validation/_index.md) note
has the five-level protocol in full.
