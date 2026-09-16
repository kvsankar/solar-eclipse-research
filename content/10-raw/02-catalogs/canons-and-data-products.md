---
title: Canons and data products
description: Where the eclipse lists live, in what format, with which ephemeris and ΔT, which open-source code enumerates eclipses, and what the older canons from Oppolzer to Mucke and Meeus contain.
order: 3
status: working
updated: 2026-09-15
tags: [canon, catalogue, nasa-gsfc, imcce, hmnao, jubier, occult, data-products, open-source]
---

::: summary
- **NASA GSFC is the machine-readable reference.** One ASCII catalogue of 11,898 rows and one CSV of Besselian polynomial elements for the same eclipses, both derived from the Five Millennium Canon with VSOP87D and ELP-2000/82, are downloadable without registration and reproducible with the credit line "Eclipse Predictions by Fred Espenak, NASA's GSFC" [@cat-nasa-5mkse-ascii] [@cat-nasa-besselian-csv] [@cat-gmiller-besselian].
- **IMCCE has its own six-millennium canon.** 14,155 solar eclipses from $-2999$ to $+3000$ computed with ELP2000, VSOP82, Chebyshev ephemerides SLP98, Stephenson 1984 for TT−UT, $k = 0.2725076$ and a solar semidiameter of 15′59.63″ at 1 au [@cat-imcce-theories] [@cat-imcce-parametres] [@cat-imcce-resultats].
- **EclipseWise extends the count to 14,261.** Espenak's later six-millennium catalogue lists 5,042 partial, 4,761 annular, 3,820 total and 638 hybrid eclipses. Van Gent reports it was computed from JPL DE406 [@cat-eclipsewise-catalog] [@cat-vangent-tables].
- **Only two mainstream libraries enumerate solar eclipses.** Astronomy Engine and the Swiss Ephemeris. Skyfield has lunar eclipses only, libnova has no eclipse header at all, and no astropy eclipse finder was found [@cat-astronomy-engine] [@cat-swisseph-doc] [@cat-skyfield-almanac] [@cat-libnova-headers].
- **The older canons set the numbering and the baselines.** Oppolzer 1887 covers 8,000 solar eclipses from $-1207$ to $+2161$ with hand-computed circular-arc paths. Mucke and Meeus 1983 covers 10,774 eclipses from $-2003$ to $+2526$ with Besselian elements. Meeus 1989 gives elements for 570 eclipses from 1951 to 2200 [@cat-espenak-meeus-2009-catalog] [@cat-meeus-1989-elements].
:::

**The question.** Where should a developer obtain a trustworthy list of eclipses with their elements, what does each product state about its ephemeris, $\Delta T$ model and lunar radius, which code can regenerate such a list, and what are the older canons that the modern ones cite? Method and type rules are in [Enumerating eclipses](enumerating-eclipses.md) and [Types and classification](types-and-classification.md).

## NASA GSFC eclipse site

The site publishes the Five Millennium Canon (NASA/TP-2006-214141) and the revised Five Millennium Catalog (NASA/TP-2009-214174) and everything derived from them. The catalogue itself says the tables are "available via the Web at http://eclipse.gsfc.nasa.gov/SEcat5/catalog.html. Organized into 100-year intervals, the tables have individual links to eclipse maps and Saros series tables" [@cat-espenak-meeus-2009-catalog] [@cat-nasa-catalog-index]. The site was intermittently unreachable on 2026-09-15; unless a reference note says otherwise, every page cited from it is as of that date.

**Publications.** The canon text is `5MCSE/5MCSE-Text11.pdf` (the `Text10` link on the publication page returns 404) with twelve map PDFs of 19.5 to 21.8 MB each. The catalogue is `5MCSE/TP2009-214174.pdf`, 13.2 MB [@cat-nasa-5mcse-page] [@cat-nasa-5mkse-page].

**ASCII catalogue.** `https://eclipse.gsfc.nasa.gov/5MCSE/5MKSEcatalog.txt`, 1.38 MB, 11,908 lines, dated 2008 Oct 07 and headed "NASA Technical Publication NASA/TP-2008-214170". Fixed-width columns: catalogue number, canon plate, calendar date, [?tt|TD] of greatest eclipse, ΔT in seconds, lunation number, Saros number, type code, QLE, gamma, magnitude, latitude, longitude, Sun altitude, Sun azimuth, path width in km, central duration. Row 1 reads `1 001 -1999 Jun 12 03:14:51 46438 -49456 5 T -n -0.2701 1.0733 6.0N 33.3W 74 344 247 06m37s` [@cat-nasa-5mkse-ascii]. A regular expression over the type field and the numeric columns parses all 11,898 rows. TD, TDT and TT are one scale, printed as TDT or TD in NASA tables and called ET before 1984.

**Besselian elements CSV.** `https://eclipse.gsfc.nasa.gov/eclipse_besselian_from_mysqldump2.csv`, 5.95 MB, 11,899 lines including the header. Columns: `year, month, day, td_ge, dt, luna_num, saros, eclipse_type, gamma, magnitude, lat_ge, lng_ge, lat_dd_ge, lng_dd_ge, sun_alt, sun_azm, path_width, central_duration, duration_secs, cat_no, canon_plate, julian_date, t0, x0, x1, x2, x3, y0, y1, y2, y3, d0, d1, d2, mu0, mu1, mu2, l10, l11, l12, l20, l21, l22, tan_f1, tan_f2, tmin, tmax, etype, PNS, UNS, NCN, nSer, nSeq, nJLE`. The elements are cubic in $x$ and $y$, quadratic in $d$, $\mu$, $l_1$ and $l_2$, referred to `t0` in TDT hours and valid for `tmin` −3 to `tmax` +3 hours. The last six columns are undocumented on the site [@cat-nasa-besselian-csv]. The publication page links this file next to the ASCII catalogue [@cat-nasa-5mcse-page]. The same data are mirrored as CSV, JSON and JavaScript in a GitHub repository whose README quotes NASA's permission: "Permission is freely granted to reproduce this data when accompanied by an acknowledgment: 'Eclipse Predictions by Fred Espenak, NASA's GSFC'" [@cat-gmiller-besselian].

**Per-eclipse pages.** `SEsearch/SEdata.php?Ecl=YYYYMMDD` returns the polynomial elements, the circumstances at greatest eclipse and the statement that the predictions use "VSOP87/ELP2000-82 solar and lunar ephemerides". The 2024 Apr 08 page gives $t_0 = 18.000$ TDT, $\gamma = 0.3431$, magnitude 1.0566, Saros 139, ΔT 74.0 s, path width 197.5 km and central duration 04m28s [@cat-nasa-sedata-2024]. The explanatory page for the elements defines the eight parameters and their tabulation "often at hourly intervals" [@cat-nasa-beselm].

**Saros products.** A catalogue of Saros series 0 to 180 with the count, span and first and last date of each, the per-series tables, and the Quaglia and Tilley Saros-Inex panorama as an Excel file of 61,775 eclipses [@cat-nasa-saroscat] [@cat-nasa-sescatkey] [@cat-nasa-panorama].

**ΔT pages.** The polynomial page, the historical-values page and the uncertainty page reproduce Sections 2.6 to 2.8 of the catalogue, including the $\sigma = 0.8t^2$ and Huber formulas and the table of longitude uncertainties from 2.65° at $-1000$ to 0.0004° at $+1900$ [@cat-nasa-deltatpoly] [@cat-nasa-deltat] [@cat-nasa-uncertainty].

## EclipseWise

Espenak's own site carries a six-millennium catalogue, $-2999$ to $+3000$, with 14,261 eclipses: 5,042 partial, 4,761 annular, 3,820 total, 638 hybrid. The page states that "some of the data presented in the Catalog of Solar Eclipses were previously published in the Five Millennium Canon" and carries the credit "Eclipse Predictions by Fred Espenak, www.EclipseWise.com", but the pages read do not name the ephemeris, the $\Delta T$ model or $k$ [@cat-eclipsewise-catalog] [@cat-eclipsewise-catkey]. Van Gent's bibliography states the six-millennium catalogues were "calculated by Fred Espenak and Jean Meeus from the DE406 solar system ephemeris"; this is a third-party statement and was not confirmed on EclipseWise [@cat-vangent-tables]. The EclipseWise catalogue key adds a "ΔT Sigma" column absent from the NASA catalogue [@cat-eclipsewise-catkey]. Its $\Delta T$ polynomial page, last updated 2020 Jan 27, replaces the NASA 2005-to-2050 expression with one covering "Between years 2015 and 3000" described as "an extrapolation based on recent values of ΔT combined with the long term trend obtained by fitting a quadratic function to the values of ΔT from the historic records" [@cat-eclipsewise-deltatpoly2014]. The second edition of the canon is sold as two volumes, $-1999$ to 0 and 1 to 3000, and the sales page does not list technical changes [@cat-eclipsewise-5mcse2].

## IMCCE

The Observatoire de Paris teaching pages describe the IMCCE canon: "une période de 6000 ans (de l'an −2999 à 3000)", built "avec les dernières théories planétaires et lunaire élaborées à l'IMCCE" [@cat-imcce-canons]. The theories: "Théorie de la Lune : ELP2000 de Michèle Chapront-Touzé et J. Chapront", "Théorie du barycentre Terre-Lune : VSOP82 de P. Bretagnon", "Éphémérides sous forme de polynômes de Tchebycheff : SLP98 de G. Francou", "TT-TU : valeurs de R. Stephenson (1984) modifiées et adaptées à la théorie de la Lune utilisée", precession of Lieske 1977, nutation of Wahr 1981, sidereal time of Aoki 1992 [@cat-imcce-theories]. The physical parameters: "le demi-diamètre solaire = 15′ 59.63″", "le rapport du rayon lunaire sur le rayon équatorial terrestre : k = 0,2725076", "le rayon équatorial terrestre = 6 378 140 m", "le carré de l'ellipticité de l'ellipsoïde terrestre = 0,00669438 ; 1/f = 1/298.257 IERS (1992)" [@cat-imcce-parametres]. The result: "Nous avons trouvé sur cette période de 6000 ans, 14 155 éclipses de Soleil" with the remark that annular eclipses outnumber total ones; the per-type table did not render in the page as fetched [@cat-imcce-resultats]. The IMCCE canon therefore uses the single IAU $k$ that Espenak and Meeus rejected, and 14,155 versus EclipseWise's 14,261 for the same span is the difference to investigate.

The live IMCCE service at `ssp.imcce.fr/forms/solar-eclipses` is a JavaScript application that serves no content in its document body, so its parameters cannot be read from the page. It is an online calculator for general and local circumstances, with a page per eclipse such as `/forms/solar-eclipses/2026-08-12` [@cat-imcce-ssp-forms]. Its ephemeris version is unestablished.

## HMNAO

The portal at `astro.ukho.gov.uk/eclipse/` returned HTTP 503 on every attempt on 2026-09-15 and no archive snapshot was retrievable. Search summaries state it covers "1501 CE to 2100 CE inclusive, with a total of 2,881 eclipses made up of 1,421 solar and 1,460 lunar eclipses" and that "the mapping information is based on data derived from solar and lunar eclipse software used in the production of The Astronomical Almanac". This is search-summary provenance only [@cat-hmnao-portal].

## Xavier Jubier

The Five Millennium Canon database page states: "All the data accessed through this interface is provided by Fred Espenak and Jean Meeus (NASA Technical Publication TP-2006-214141)." It offers on-the-fly Google Maps and Google Earth kmz files for each of the 11,898 eclipses, filters by year, type, duration and Saros ($-13$ to 194), and warns that "the uncertainty in Earth's rotational period expressed in the parameter ΔT has an impact on the geographic visibility of eclipses in the past and future", linking to a page on the 5MCSE ΔT model. The page footer reads "Powered by eEclipser ©2006-2024" and "Last page update on February 2, 2007" [@cat-jubier-5mcse]. The page requires JavaScript, so nothing beyond the header text is present in the document itself.

## Occult 4

Dave Herald's page lists among Occult's capabilities "Solar and lunar eclipses, transits of Mercury and Venus", states it "has been written in the language C#, and runs in the .NET framework V4.5", and describes installation via `OccultInstaller.zip` with data downloads [@cat-occult4]. That eclipse paths from Occult version 4.2023.11.30 used JPL DE441 is reported on a third-party map page and is not confirmed in Occult's own documentation [@cat-occult4]. Occult's eclipse listing, and its use of a lunar limb profile in eclipse predictions, fall outside the scope of this note.

## timeanddate

The site blocked all automated fetches. Search summaries of its help pages state that its eclipse calculations "account for changes in the speed of Earth's rotation using a value called Delta T", quote ΔT values near 69 to 75 s for current eclipses, and describe magnitude as computed from Besselian elements [@cat-timeanddate-accuracy]. No ephemeris or $k$ statement was found. Search-summary provenance only.

## Open-source code that enumerates eclipses

The full repository inventory and its comparison matrix are in [GitHub
repositories](../09-software-and-repos/github-repositories.md). This section
keeps only what each project does about enumeration.

**Astronomy Engine** (MIT, C, C#, JavaScript, Python, Kotlin). `SearchGlobalSolarEclipse` and `NextGlobalSolarEclipse` return kind (partial, annular, total), obscuration, distance of the shadow axis from Earth's centre, and the latitude and longitude of the peak. The kind logic and constants are quoted in [Enumerating eclipses](enumerating-eclipses.md). It uses truncated VSOP87 and claims ±1 arcmin [@cat-astronomy-engine].

**Swiss Ephemeris** (AGPL or commercial, C with many bindings). `swe_sol_eclipse_when_glob` with type flags, `swe_sol_eclipse_where` and `swe_sol_eclipse_how`. The DE-based or Moshier ephemeris is selected by flag. The type logic is quoted in the two companion notes [@cat-swisseph-doc] [@cat-swisseph-swecl].

**Skyfield** (MIT, Python). `skyfield.eclipselib.lunar_eclipses` only. New moons can be found with `almanac.oppositions_conjunctions` and `find_discrete`. Pull request 1076, still open, adds a solar routine tested against "the official data for the last ~400 years" [@cat-skyfield-almanac] [@cat-skyfield-pr-1076] [@cat-skyfield-issue-1078].

**Meeus ports.** `soniakeys/meeus` (Go, MIT) implements Chapter 54 as `eclipse.Solar(year)` returning type, central flag, JDE of maximum, $\gamma$, $u$, penumbral radius and partial magnitude, with the book's constants verbatim [@cat-soniakeys-meeus-go]. A C# walkthrough of the same chapter exists on squarewidget.com [@cat-squarewidget-meeus].

**Small projects found by GitHub search** (queries "solar eclipse catalog", "eclipse finder", "saros", "besselian elements", "solar eclipse prediction", "eclipse calculator meeus" on 2026-09-15). "solar eclipse catalog" and "eclipse calculator meeus" returned no repositories. Others:

- `erikbern/eclipse-finder` (Python): "Simple Modal script that uses Astropy to find eclipses in the 2020-2030 period" by brute-force separation search. That a user had to write it is the evidence that astropy itself has no eclipse function [@cat-erikbern-eclipse-finder].
- `cjwinchester/full-moons-solstices-equinoxes-eclipses` (Python): 23,289 events 1550 to 2649, lunar eclipses from Skyfield with DE440, and "Solar eclipse data comes from NASA's Five Millenium Catalog of Solar Eclipses", output as CSV [@cat-cjwinchester-almanac].
- `i230010/sedategenerator_v2` (Python): generates a CSV with UT1 and TT datetimes, ΔT and the Besselian polynomial coefficients $x_0..x_3$, $y_0..y_3$, $d_0..d_3$, $l_{10}..l_{13}$, $l_{20}..l_{23}$, $\mu_0..\mu_3$, $\tan f_1$, $\tan f_2$ over a year range with a time step in seconds; no method or validation is documented [@cat-sedategenerator].
- `RyuuNeko1107/umbra-rs` (Rust): an AI-authored experiment with design documents targeting ±1 to 2 s in greatest-eclipse time and sub-km central lines, explicitly "not ready for use" and not validated against JPL DE [@cat-umbra-rs].
- `RHerAle/Eclipse-Engine` (JavaScript, AGPL-3.0): the engine behind eclipseradar.com, using "Besselian elements, fitted to the JPL DE440s ephemeris" for 2026 to 2050; it consumes elements rather than enumerating [@cat-rherale-eclipse-engine].
- `gmiller123456/FiveMillenniumCanonOfSolarEclipses-Besselian-Elements`: the NASA CSV re-served as JSON and JavaScript [@cat-gmiller-besselian].

**libnova** (LGPL, C). The `src/libnova` header directory contains `solar.h`, `lunar.h`, `rise_set.h`, `parallax.h` and thirty others, none for eclipses, and a code search for "eclipse" in the repository returned zero hits [@cat-libnova-headers].

No Zenodo dataset of solar eclipse catalogues or Besselian elements was found in searches for "Zenodo solar eclipses catalog CSV JSON Besselian elements". The NASA CSV and its GitHub mirror are the only machine-readable element sets located.

## The older canons

The catalogue's introduction is the best short history and is quoted here [@cat-espenak-meeus-2009-catalog].

**Oppolzer 1887, Canon der Finsternisse.** "It stands as one of the greatest achievements in computational astronomy of the 19th century and contains the elements of all 8,000 solar eclipses (and 5,200 lunar eclipses) occurring between the years −1207 and +2161 ... together with maps showing the approximate positions of the central lines. To accomplish this remarkable feat, a number of approximations were used in the calculations and maps. Consequently, the eclipse paths often differ by hundreds of miles compared to rigorous predictions generated with modern ephemerides. Furthermore, the 1887 Canon took no account of the shifts imparted to ancient eclipse paths as a consequence of Earth's variable rotation rate and the secular acceleration of the Moon." Search coverage adds that ten human computers shared the work and that each path was drawn as a circular arc through three computed points, begin, middle and end [@cat-oppolzer-1887]. Gingerich's 1962 translation is on the Internet Archive [@cat-oppolzer-1887].

**Meeus, Grosjean and Vanderleen 1966, Canon of Solar Eclipses.** "Contains the Besselian elements of all solar eclipses from +1898 to +2510, together with central line tables and maps. The aim of this work was to provide data on future eclipses." It is also the source of the Saros-number increments in Table 5-10 and of the statement that a total eclipse cannot occur "so long as any photospheric rays are visible through deep valleys along the Moon's limb" [@cat-espenak-meeus-2009-catalog].

**Mucke and Meeus 1983, Canon of Solar Eclipses −2003 to +2526.** "Intended primarily for historical research, serving as the modern day successor of Oppolzer's great canon. The Mucke-Meeus publication included Besselian elements and maps of all 10,774 solar eclipses during this time interval. Each orthographic map was oriented to show the day-side hemisphere of Earth. In this projection, the path of the Moon's penumbra and the central axis of the shadow cone could be approximated by straight lines." Meeus 1991 refers readers to it for elements and formulas [@cat-espenak-meeus-2009-catalog] [@cat-meeus-1991-aa] [@cat-mucke-meeus-1983].

**Meeus 1989, Elements of Solar Eclipses 1951-2200.** Besselian elements for the 570 solar eclipses of 1951 to 2200 "calculated using highly accurate modern theories of the Sun and Moon developed at the Bureau des Longitudes of Paris", with formulas for local circumstances, central line and limits, and worked examples. Meeus 1991 calls these "accurate Besselian elements" [@cat-meeus-1989-elements] [@cat-meeus-1991-aa]. Not read directly.

**Espenak 1987, Fifty Year Canon of Solar Eclipses 1986-2035.** Individual maps and central path data. The five-millennium catalogue states its smaller $k$ "is consistent with predictions in Fifty Year Canon of Solar Eclipses" [@cat-espenak-meeus-2009-catalog].

**Stephenson and Houlden 1986, Atlas of Historical Eclipse Maps, East Asia 1500 BC to AD 1900.** Path maps of total and annular eclipses visible from China, and the source of the telescopic-era ΔT uncertainties in the catalogue's Table 2-4 [@cat-espenak-meeus-2009-catalog].

**Van den Bergh 1955, Periodicity and Variation of Solar (and Lunar) Eclipses.** The source of the Saros and Inex numbering and of the panorama [@cat-van-den-bergh-1955] [@cat-espenak-meeus-2009-catalog].

The catalogue notes that "Without exception, all solar eclipse canons produced during the latter half of the 20th century were based on Newcomb's tables of the Sun (1895) and Brown's lunar theory (1905), subject to later modifications in the Improved Lunar Ephemeris (1954)", and the 2006 canon was the first based on the Bureau des Longitudes theories with predictions in Terrestrial Dynamical Time [@cat-espenak-meeus-2009-catalog].

## Sources compared

| Product | Span | Eclipses | Ephemeris | ΔT | $k$ | Machine-readable |
|---|---|---|---|---|---|---|
| NASA 5MCSE catalogue [@cat-nasa-5mkse-ascii] | $-1999$ to $+3000$ | 11,898 | VSOP87D, ELP-2000/82 | M&S 2004 + polynomials + $c$ | 0.2724880 / 0.272281 | ASCII, CSV of elements |
| EclipseWise six millennium [@cat-eclipsewise-catalog] | $-2999$ to $+3000$ | 14,261 | DE406 per van Gent, unconfirmed | 2020 polynomials | not stated | HTML tables |
| IMCCE canon [@cat-imcce-theories] | $-2999$ to $+3000$ | 14,155 | ELP2000, VSOP82, SLP98 | Stephenson 1984 adapted | 0.2725076 | not found |
| HMNAO portal [@cat-hmnao-portal] | 1501 to 2100 | 1,421 solar | Astronomical Almanac software | not stated | not stated | unknown, site down |
| Jubier 5MCSE [@cat-jubier-5mcse] | $-1999$ to $+3000$ | 11,898 | NASA data | NASA model | NASA | kmz, maps |
| Mucke and Meeus 1983 [@cat-mucke-meeus-1983] | $-2003$ to $+2526$ | 10,774 | Newcomb, Brown ILE | of its day | not stated here | print |
| Oppolzer 1887 [@cat-oppolzer-1887] | $-1207$ to $+2161$ | 8,000 | 19th-century tables | none | not applicable | print, scanned |

## What a developer should do

1. Download `5MKSEcatalog.txt` and `eclipse_besselian_from_mysqldump2.csv` from NASA and treat them as the acceptance test set. Keep the credit line in any redistribution [@cat-nasa-5mkse-ascii] [@cat-nasa-besselian-csv].
2. Use the Swiss Ephemeris or Astronomy Engine as a second, independent enumerator and diff the three lists. Differences will concentrate in the non-central band and in near-hybrid events, which is where $k$ and the surface-versus-plane umbral radius matter [@cat-swisseph-swecl] [@cat-astronomy-engine].
3. Record the ephemeris, the $\Delta T$ model and the $k$ pair as metadata on every exported row. The NASA CSV does not carry them, and the IMCCE and EclipseWise products differ from NASA on all three.
4. For historical work compare with IMCCE's 14,155 and EclipseWise's 14,261 for $-2999$ to $+3000$ and explain the 106-eclipse difference before trusting either at the margins.

## What this changes

Nothing in the pipeline design. The NASA files are sufficient as a reference set and no product examined offers a documented improvement over them for enumeration. The data-products stage should add a provenance record, because the only widely mirrored element set carries no statement of its own constants.

## Open questions

- Obtain the IMCCE canon's per-type counts and its statement of the Earth-rotation series, from the pages `stlp-canon-imcce-resultats.html` whose table did not render, or from IMCCE's *Le manuel des éclipses* (2005) [@cat-imcce-resultats].
- Obtain a confirmed statement of the ephemeris behind the EclipseWise six-millennium catalogue, either from EclipseWise or from Espenak's *Thousand Year Canon of Solar Eclipses 1501 to 2500* [@cat-eclipsewise-catalog].
- Obtain the HMNAO Eclipse Portal pages when the server is up, in particular whether Besselian elements are exported and which ephemeris the Astronomical Almanac software used for 1501 to 2100 [@cat-hmnao-portal].
- Obtain Occult 4's help topic on solar eclipses to record its ephemeris, $k$ and limb usage from the author's own text [@cat-occult4].
- Obtain the Skyfield pull request 1076 test file to see which reference list it compares with [@cat-skyfield-pr-1076].
