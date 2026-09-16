---
title: GitHub repositories
description: Thirty public repositories that compute solar eclipse products, with language, stars, last commit, method, constants, limb and terrain handling, and a comparison matrix flagging the five most complete.
order: 3
status: working
updated: 2026-09-15
tags: [software, github, repositories, besselian, limb, terrain]
---

::: summary
- **Thirty repositories were inventoried** from GitHub API searches on 2026-09-15 across Python, JavaScript, TypeScript, Rust, Go, Java, C++ and Julia. Most are small (0 to 3 stars) and recent (2024 to 2026). Star counts measure popularity, not correctness.
- **Three method families.** Consumers of NASA's Canon Besselian elements are tahze0, aravpanwar, Absolute-Eclipse, johnarban, umbra-atlas and Eclipse-Engine. Geometric computation on Astronomy Engine or Skyfield is used by angristan, mf4633, eclipsite, eclipse-3d-sim, jpatka and eclipse-2026. Meeus and textbook ports are astronomia, soniakeys/meeus, Starainrt/astro and johanley.
- **Only tomasrojasc/eclipse-2026 builds Baily's beads from LOLA**, using `ldem_16.img` with `moon_pa_de421_1900-2050.bpc` orientation. Only SolarEclipseWorkbench ships a limb band file. Nobody derives path limits from a limb profile.
- **Terrain is handled by four.** Eclipse-Engine uses a DEM plus OpenStreetMap buildings, eclipsite uses EU-DEM at 25 m, eclipse-3d-sim ray-casts Copernicus at 30 m, and umbra-eclipse-atlas reads Copernicus through Open-Meteo.
- **Documented validation is rare**: Absolute-Eclipse reports 1 to 5 s residuals against Espenak, eclipsite 0.36 s mean against NASA elements and 0.60 s RMS against IGN durations, tahze0 a 0.26 per cent median path-width error over 300 eclipses, Starainrt/astro second-level global agreement with NASA.
- **Five most complete**: Stellarium, covered in [open-source libraries](open-source-libraries.md), then RHerAle/Eclipse-Engine, tahze0/solar-eclipse-explorer, tomasrojasc/eclipse-2026, Xeratec/eclipsite. NASA's JSEX and its ports remain the cleanest minimal reference.
:::

**The question.** Which public repositories contain substantive solar eclipse computation, what do they implement, from which formulas and elements, with which constants, and do any of them handle limb profiles, terrain or catalogue generation?

## How the inventory was built

The GitHub repository search API was queried for "besselian elements", "solar eclipse calculator", "solar eclipse path", "eclipse circumstances", "solar eclipse besselian", "eclipse limb profile" (zero results), "baily beads", "eclipse explorer", "eclipse predictor", "pyeclipse", "eclipsecalc", and "solar eclipse" restricted to Rust, Go, Julia, Java and C++, each sorted by stars, on 2026-09-15 [@sw-github-api-search]. Metadata for language, stars, last push and licence comes from the repos endpoint on the same day [@sw-github-api-search]. READMEs were then read for every repository below. Repositories that only process eclipse photographs, such as timelapse aligners and corona processing, were excluded, as was unrelated software named "Eclipse". The plausible project names "eclipsecalc", "SolarEclipseCalc", "pyeclipse", "solareclipse.js", "Eclipse-Path", "moon-shadow" and "eclipse_predictor" matched no substantive eclipse-computation repository except those listed.

## Repositories

### Elements consumers (NASA Canon Besselian elements)

**RHerAle/Eclipse-Engine**. JavaScript, AGPL-3.0, 0 stars, last push 2026-09-14. The engine behind eclipseradar.com for 2026 to 2050: "Besselian shadow geometry: contacts, obscuration, magnitude, central line, limits, shadow outline, and obscuration bands", plus spectral irradiance with limb darkening and ICNIRP exposure limits, "Terrain analysis: skyline toward the Sun from elevation models and OpenStreetMap building data", and solar-limb video stabilisation. Its `data/eclipses.json` is "the catalogue of Besselian elements, fitted to the JPL DE440s ephemeris", so it generates elements rather than copying NASA's. No dependencies. Data CC-BY-SA-4.0 [@sw-repo-eclipse-engine].

**tahze0/solar-eclipse-explorer**. Python, MIT code, 0 stars, last push 2026-09-08. Reconstructs all 11,898 Canon eclipses "computed locally from NASA Five Millennium Canon Besselian elements" from `eclipse_besselian_from_mysqldump2.csv`, with umbra and penumbra modules, a 14-step build pipeline and reported "median 0.26% error" in path width against catalogue values on 300 reference eclipses [@sw-repo-tahze0].

**aravpanwar/besselian**. Python, AGPL-3.0, 0 stars, last push 2026-09-14. Local circumstances from NASA elements intersected with OpenStreetMap populated places for 2027 August 2 in Egypt. States $k_1 = 0.272488$ for penumbral and $k_2 = 0.272281$ for umbral contacts, ΔT = 76.0 s, and that omitting ΔT in the hour angle "introduces ~32 km longitude error". Validates Sun altitude 81.69° and duration 382.5 s at greatest eclipse against published values [@sw-repo-aravpanwar-besselian].

**Absolute-Eclipse/eclipse-data**. JavaScript, MIT code and CC-BY-4.0 data, 0 stars, last push 2026-06-17. Local circumstances for 9,438 European cities for 2026 and 2027 from "Besselian elements sourced from F. Espenak (NASA/EclipseWise)", with ΔT, lunar-limb adjustments and refraction documented, elevation from Copernicus, NASA and ASTER, "accuracy within 1–5 seconds for greatest eclipse and 0.05 percentage points for partial phases" against NASA and Espenak, residuals published, and near-limit cities flagged [@sw-repo-absolute-eclipse].

**johnarban/eclipse_explorer**. TypeScript, GPL-3.0, 0 stars, last push 2026-07-15. A TypeScript port of NASA's JavaScript Solar Eclipse Explorer (JSEX) with `SE2001.ts` and `SE2024.ts` element files and a test file [@sw-repo-johnarban]. **ebradyjobory/eclipse-explorer**. JavaScript, GPL-2.0, 16 stars, one commit in 2010. It mirrors NASA's JSEX and JLEX unchanged [@sw-repo-eclipse-explorer-mirror].

**plhery/umbra-eclipse-atlas**. TypeScript, MIT, 0 stars, last push 2026-09-08. Browses 11,898 eclipses using "Besselian elements from NASA's Five Millennium Canon via the `@astronomy-bundle/solar-eclipse` library", Copernicus DEM skyline via Open-Meteo, and states it is "a planning aid, not an official prediction service" [@sw-repo-umbra-atlas].

**gmiller123456/FiveMillenniumCanonOfSolarEclipses-Besselian-Elements**. Python, 3 stars, last push 2023-03-10. Repackages NASA's elements as CSV, JS and JSON with condensing scripts. Data use requires the Espenak acknowledgment [@sw-gmiller-5mcse-repo]. Greg Miller's site also documents generating polynomial elements from a DE405 extract with $k = 0.2725076$ and $R_\odot = 6.957\times10^8$ m, fitting five points at $t_0 \pm 2$ h with Gauss-Jordan elimination, and matching Espenak "to approximately seven decimal places" [@sw-celestialprogramming-bessel], and a prediction article citing the Explanatory Supplement, Meeus, Chauvenet, Green and Smart [@sw-celestialprogramming-pred] [@sw-celestialprogramming-home].

**Frencil/eclipsetracks**. Python and JavaScript, Apache-2.0, 31 stars, last push 2024-02-20. Scrapes NASA path tables into CZML for a Cesium globe and does not compute the umbra itself [@sw-repo-eclipsetracks].

### Geometric computation on Astronomy Engine or Skyfield

**Xeratec/eclipsite**. Python, MIT, 2 stars, last push 2026-08-12. Ranks observing sites by "P(clear line of sight) × eclipse depth × terrain gate × model-agreement discount × drive-time discount". Local circumstances from JPL DE421 via Skyfield, cross-checked against NASA Besselian elements to "0.36s mean difference". It adds an EU-DEM 25 m skyline via OpenTopoData and cloud ensembles. Validation gives "RMS 0.60s" against IGN and Generalitat de Catalunya durations, which "caught a solar-radius convention error worth 1.3 seconds per site" [@sw-repo-eclipsite].

**tomasrojasc/eclipse-2026**. Python and TypeScript, no licence stated, 0 stars, last push 2026-08-12. Contact times for Spain via Skyfield and DE421, and beads "computed from the Moon's actual shape. The app builds a limb profile from LOLA laser altimetry for the Moon's libration at your contact time, then slides that jagged limb across the Sun's edge". It uses LRO LOLA `ldem_16.img` at 16 pixels per degree, about 1.9 km at the limb, with the NAIF `moon_pa_de421_1900-2050.bpc` kernel. There are 84 tests, including totality-band checks for 11 cities [@sw-repo-eclipse-2026-rojas].

**angristan/eclipse**. TypeScript, MIT, 1 star, last push 2026-09-09. Paths by intersecting the Sun-Moon axis with the WGS84 ellipsoid using astronomy-engine's `SearchGlobalSolarEclipse` and `SearchLocalSolarEclipse`, umbra radius by similar triangles, "no database and no data files", and "Overall accuracy is a few kilometers: great for a map, not for planning an expedition to the edge" [@sw-repo-angristan].

**mf4633/eclipse-predictor**. HTML single file, MIT, 0 stars, last push 2026-09-08. Catalogue of 1900 to 2200, about 690 events, from astronomy-engine, "Besselian elements derived from position data" to trace the path, claims "±1–2 km ground accuracy" and local contacts "to a few seconds" against NASA [@sw-repo-mf4633].

**carlok/eclipse-3d-sim**. Python and React, no licence stated, 1 star, last push 2026-07-25. Astronomy Engine circumstances compared against terrain by ray-casting a WGS84 GeoTIFF DEM, optionally Copernicus 30 m from OpenTopography, plus a manual obstacle editor [@sw-repo-eclipse-3d-sim].

**jpatka/Eclipse-Explorer**. Python, MIT, 0 stars, last push 2026-08-14. Skyfield with DE421, refraction, and CSV and iCalendar output. No validation is stated, and it was developed with an LLM assistant [@sw-repo-jpatka].

**pmisson/pyeclipsesimulator**. Python, MIT, 4 stars, last push 2025-09-07. Astropy-based contacts with refraction libraries and Open-Meteo elevation, "compared with xjubier.free.fr" with discrepancies of a few seconds, "purely demonstrative", mostly LLM-generated [@sw-repo-pyeclipsesimulator].

**AstroWimSara/SolarEclipseWorkbench**. Python 3.11, GPL-3.0, 20 stars, last push 2026-08-07. Camera-control workbench computing C1, C2, MAX, C3, C4, sunrise and sunset. "Astropy/IERS is used to compute Delta T (TT − UT1)", solar radius "959.95 ±0.05 arcseconds", a bundled `lunar_limb_band_v1.bin`, and SPICE kernels for the Moon [@sw-repo-sew].

**sPaMFouR/SolarEclipse**. Jupyter, 2 stars, 2021. It uses astropy and astroplan, is "under development", and documents no method [@sw-repo-spamfour].

### Element generators and textbook ports

**i230010/sedategenerator_v2**. Python, MIT, 2 stars, last push 2026-09-15. Emits eclipse dates with polynomial elements x0..x3, y0..y3, d0..d3, l10..l13, l20..l23, mu0..mu3, tan f1, tan f2, and ΔT, from a bundled `ephem` folder whose source is not documented [@sw-repo-sedategenerator].

**RyuuNeko1107/umbra-rs**. Rust, Apache-2.0 or MIT provisional, 0 stars, last push 2026-09-15. "Experimental pure-Rust solar eclipse prediction engine" with VSOP87, ELP-MPP02 and IERS EOP inputs, mean limb, precision targets of ±1 to 2 s, and the statement that it is "not ready for use" [@sw-repo-umbra-rs].

**johanley/custom-solar-eclipse-viewer**. Java, no licence stated, 2 stars, last push 2024-06-03. Local circumstances with Meeus's *Elements of Solar Eclipses*, 1989, as "my main reference" and the 1961 Explanatory Supplement [@sw-repo-johanley].

**Starainrt/astro**, Go, Apache-2.0, 157 stars, last push 2026-08-06; **commenthol/astronomia**, JavaScript, MIT, 180 stars; **soniakeys/meeus**, Go, MIT, 376 stars, 2019; and **andrmoel/astronomy-bundle**, PHP, MIT, 12 stars, are covered in [open-source libraries](open-source-libraries.md) [@sw-astro-go] [@sw-astronomia-eclipse] [@sw-meeus-go-eclipse] [@sw-astronomy-bundle-php].

**curiousleo/twilight**, C++, 2013, integrates Sun, Earth and Moon numerically and tests eclipse geometry with tangent lines [@sw-repo-twilight]. **fizyk20/eclipse-predictor**, Rust, 2022, has 8 commits and no README detail [@sw-repo-fizyk20]. **ArctynFox/SunSketcher**, Java, 2 stars, is the NASA-partnered Android app for crowd-sourced Baily's beads imagery. Its README covers the build only [@sw-repo-sunsketcher].

## Comparison matrix

| Repository | Language | Stars | Last push | Elements source | Global path | Local contacts | Limb | Terrain | Catalogue | Validation stated | Licence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Stellarium [@sw-stellarium-sec-cpp] | C++ | 9,987 | 2026-09-15 | Computed, own ephemeris | Yes | Yes | No | No | Yes | No | GPL-2.0 |
| cosinekitty/astronomy [@sw-astronomy-engine-repo] | C, JS, Py, C#, Kotlin | 1,016 | 2025-01-27 | Geometric | Peak only | Yes | No | No | Yes | Against NOVAS | MIT |
| aloistr/swisseph [@sw-swisseph-swecl] | C | 726 | 2026-09-14 | Geometric | Central line | Yes | No | No | Yes | Error budget | AGPL or paid |
| soniakeys/meeus [@sw-meeus-go-eclipse] | Go | 376 | 2019-03-01 | Meeus ch. 54 | No | No | No | No | Yes | No | MIT |
| commenthol/astronomia [@sw-astronomia-eclipse] | JavaScript | 180 | 2025-08-30 | Meeus ch. 54 | No | No | No | No | Yes | No | MIT |
| Starainrt/astro [@sw-astro-go] | Go | 157 | 2026-08-06 | VSOP87, ELP2000 | Yes | Yes | No | No | Yes | NASA, seconds | Apache-2.0 |
| Frencil/eclipsetracks [@sw-repo-eclipsetracks] | Python, JS | 31 | 2024-02-20 | NASA tables | Imported | No | No | No | No | No | Apache-2.0 |
| AstroWimSara/SolarEclipseWorkbench [@sw-repo-sew] | Python | 20 | 2026-08-07 | SPICE, astropy | No | Yes | Band file | No | No | No | GPL-3.0 |
| ebradyjobory/eclipse-explorer [@sw-repo-eclipse-explorer-mirror] | JavaScript | 16 | 2010-12-22 | NASA Canon | No | Yes | No | No | No | NASA code | GPL-2.0 |
| andrmoel/astronomy-bundle [@sw-astronomy-bundle-php] | PHP | 12 | active | VSOP87, Meeus | No | Yes | No | No | No | No | MIT |
| pmisson/pyeclipsesimulator [@sw-repo-pyeclipsesimulator] | Python | 4 | 2025-09-07 | astropy | No | Yes | No | Elevation | No | vs Jubier, seconds | MIT |
| gmiller123456 Besselian [@sw-gmiller-5mcse-repo] | Python | 3 | 2023-03-10 | NASA Canon | No | No | No | No | Data only | No | NASA terms |
| i230010/sedategenerator_v2 [@sw-repo-sedategenerator] | Python | 2 | 2026-09-15 | Own ephem | No | No | No | No | Elements | Tests | MIT |
| Xeratec/eclipsite [@sw-repo-eclipsite] | Python | 2 | 2026-08-12 | Skyfield DE421 plus NASA | No | Yes | No | EU-DEM 25 m | No | 0.36 s, 0.60 s RMS | MIT |
| johanley/custom-solar-eclipse-viewer [@sw-repo-johanley] | Java | 2 | 2024-06-03 | Meeus 1989 | No | Yes | No | No | No | No | None |
| sPaMFouR/SolarEclipse [@sw-repo-spamfour] | Jupyter | 2 | 2021-06-09 | astropy | No | Yes | No | No | No | No | None |
| curiousleo/twilight [@sw-repo-twilight] | C++ | 2 | 2013-02-02 | Integration | No | No | No | No | Dates | No | None |
| ArctynFox/SunSketcher [@sw-repo-sunsketcher] | Java | 2 | 2025-09-01 | Not stated | No | App | Imagery | No | No | No | None |
| angristan/eclipse [@sw-repo-angristan] | TypeScript | 1 | 2026-09-09 | astronomy-engine | Yes | Yes | No | No | 2023 to 2035 | few km | MIT |
| carlok/eclipse-3d-sim [@sw-repo-eclipse-3d-sim] | Python, React | 1 | 2026-07-25 | astronomy-engine | No | Yes | No | Copernicus 30 m | No | No | None |
| fizyk20/eclipse-predictor [@sw-repo-fizyk20] | Rust | 1 | 2022-11-26 | Not stated | No | No | No | No | Dates | No | None |
| RHerAle/Eclipse-Engine [@sw-repo-eclipse-engine] | JavaScript | 0 | 2026-09-14 | Own, fitted to DE440s | Yes | Yes | No | DEM plus OSM | 2026 to 2050 | Not stated | AGPL-3.0 |
| tahze0/solar-eclipse-explorer [@sw-repo-tahze0] | Python | 0 | 2026-09-08 | NASA CSV | Yes | No | No | No | 11,898 | 0.26 per cent width | MIT |
| aravpanwar/besselian [@sw-repo-aravpanwar-besselian] | Python | 0 | 2026-09-14 | NASA | No | Yes | No | No | No | Published values | AGPL-3.0 |
| Absolute-Eclipse/eclipse-data [@sw-repo-absolute-eclipse] | JavaScript | 0 | 2026-06-17 | Espenak | No | Yes | Adjustment | Elevation | 2026, 2027 | 1 to 5 s | MIT, CC-BY |
| tomasrojasc/eclipse-2026 [@sw-repo-eclipse-2026-rojas] | Python, TS | 0 | 2026-08-12 | Skyfield DE421 | Band | Yes | LOLA beads at 16 pixels per degree | No | 2026 only | 84 tests | None |
| johnarban/eclipse_explorer [@sw-repo-johnarban] | TypeScript | 0 | 2026-07-15 | NASA Canon | No | Yes | No | No | No | Tests | GPL-3.0 |
| plhery/umbra-eclipse-atlas [@sw-repo-umbra-atlas] | TypeScript | 0 | 2026-09-08 | NASA Canon via library | Yes | Yes | No | Copernicus | 11,898 | Disclaimer | MIT |
| mf4633/eclipse-predictor [@sw-repo-mf4633] | HTML | 0 | 2026-09-08 | astronomy-engine | Yes | Yes | No | No | 1900 to 2200 | 1 to 2 km | MIT |
| RyuuNeko1107/umbra-rs [@sw-repo-umbra-rs] | Rust | 0 | 2026-09-15 | VSOP87, ELP-MPP02 | Planned | Planned | Mean | No | Planned | Not yet | Provisional |
| jpatka/Eclipse-Explorer [@sw-repo-jpatka] | Python | 0 | 2026-08-14 | Skyfield DE421 | No | Yes | No | No | No | No | MIT |

## The five most complete

1. **Stellarium `SolarEclipseComputer.cpp`**: elements, limits, outlines, rise-set curves, contacts and maps with cited equations [@sw-stellarium-sec-cpp].
2. **RHerAle/Eclipse-Engine**: elements fitted to DE440s, full Besselian product set, terrain skyline, radiometry [@sw-repo-eclipse-engine].
3. **tahze0/solar-eclipse-explorer**: full 5,000-year catalogue reconstruction from the NASA CSV with a measured path-width error [@sw-repo-tahze0].
4. **tomasrojasc/eclipse-2026**: the only repository that computes Baily's beads from a LOLA DEM with a lunar orientation kernel, in its case the DE421 one [@sw-repo-eclipse-2026-rojas].
5. **Xeratec/eclipsite**: local contacts from two independent methods with published residuals and a DEM skyline gate [@sw-repo-eclipsite].

## Negative findings

No repository was found that derives the northern and southern umbral limits from a lunar limb profile, which is what SVS's `umbra_hi` polygons encode [@sw-svs-5073]. No repository was found that reads Watts charts. No general-purpose library ships a LOLA-derived limb profile as a reusable function. The GitHub query "eclipse limb profile" returned zero repositories [@sw-github-api-search].

## Sources compared

| Method family | Representative | Strength | Gap |
|---|---|---|---|
| NASA elements consumer | tahze0, aravpanwar, Absolute-Eclipse | Reproduces Espenak to seconds, cheap | Inherits NASA's $k$, ΔT and no limb |
| Own elements from JPL kernels | Eclipse-Engine, Celestial Programming | Independent of NASA, current ephemeris | Element accuracy unverified except Miller's seven-decimal match |
| Geometric on Astronomy Engine | angristan, mf4633 | No data files, multi-language | Few-kilometre paths, mean lunar radius |
| Skyfield plus DEM or LOLA | eclipsite, eclipse-2026 | Terrain and beads, published residuals | Single-eclipse scope |

## What a developer should do

Clone Stellarium sparsely (`src/core`, `src/gui`) and read `SolarEclipseComputer.cpp` end to end [@sw-stellarium-sec-cpp]. Read `program.js` from NASA for the minimal local-circumstance loop [@sw-nasa-jsex-program-js]. Read tomasrojasc/eclipse-2026's bead code for a worked LOLA limb construction with the correct orientation kernel [@sw-repo-eclipse-2026-rojas]. Use tahze0's pipeline as a template for catalogue-scale validation against the NASA CSV [@sw-repo-tahze0]. Avoid the LLM-generated repositories for anything but ideas, since they state so themselves [@sw-repo-pyeclipsesimulator] [@sw-repo-jpatka].

## What this changes

Nothing in the stage design. It establishes that a limb-corrected limit computation has to be written, not imported, and that LOLA-based bead prediction has a small worked precedent.

## Open questions

- Obtain `data/eclipses.json` and the fitting script from RHerAle/Eclipse-Engine and compare its 2026 elements against NASA's page [@sw-repo-eclipse-engine].
- Obtain tomasrojasc/eclipse-2026's limb-profile module and test it against Jubier's 2026 Baily's beads diagram for one site [@sw-repo-eclipse-2026-rojas] [@sw-jubier-calc-js].
- Obtain SolarEclipseWorkbench's `lunar_limb_band_v1.bin` format description [@sw-repo-sew].
- Obtain the `@astronomy-bundle/solar-eclipse` npm package source (the fetch of its npm page returned 404) to see which element set it bundles [@sw-repo-umbra-atlas].
