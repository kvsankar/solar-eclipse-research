---
title: Datasets
description: Where to download the Besselian element tables, SVS GIS products, lunar DEMs, terrestrial DEMs, ΔT tables and ephemeris kernels an eclipse pipeline needs, with formats verified on 2026-09-15.
order: 4
status: working
updated: 2026-09-15
tags: [datasets, besselian, lola, sldem2015, srtm, deltat, de440]
---

::: summary
- **NASA's machine-readable Besselian elements** are one 5.95 MB CSV with 11,898 rows and 54 columns covering -1999 to +3000, including the cubic polynomial coefficients, $\tan f_1$, $\tan f_2$, $t_0$ and ΔT per eclipse.
- **SVS GIS products** for 2017, 2023 and 2024 are zipped shapefiles and KML with central line, duration contours, obscuration contours, umbra polygons at 1-second and 10-second cadence, and a city-times JSON. The SVS host refused connections at the time of writing (2026 September), and the Wayback Machine served the pages.
- **Lunar topography**: LOLA LDEM cylindrical grids at 4, 16, 64 and 128 pixels per degree as single IMG files of 2 MB to 2.1 GB, 256 pixels per degree in four hemisphere files, and 1024 pixels per degree in tiles of about 944 MB, plus SLDEM2015 in global and tiled forms. Kaguya (SELENE) LALT is at JAXA DARTS.
- **Terrestrial topography**: SRTMGL1 (1 arcsecond) from LP DAAC and Copernicus GLO-30 from the AWS Open Data Registry.
- **ΔT**: USNO `deltat.data` (observed) and `deltat.preds` (predicted), IERS `finals.all.iau2000.txt` for UT1-UTC and polar motion, and NASA's Canon polynomials for long-range values.
- **Ephemerides**: JPL DE440 SPK (`de440.bsp`) and the NAIF lunar orientation kernel matching the ephemeris, `moon_pa_de440_200625.bpc` with frame kernel `moon_de440_250416.tf` for DE440, which is needed to orient a limb profile. tomasrojasc/eclipse-2026 pairs the older `moon_pa_de421_1900-2050.bpc` with DE421. The choice is argued in [lunar figure, radius ratio k, and libration](../08-lunar-and-solar-model/lunar-figure-and-libration.md).
:::

**The question.** For each dataset that the surveyed tools consume, what is the URL, the format and the version, and was it reachable?

## Besselian element tables

**NASA CSV.** `https://eclipse.gsfc.nasa.gov/eclipse_besselian_from_mysqldump2.csv`, linked from the Five Millennium Catalog page as "Catalog of Solar Eclipse Besselian elements in CSV format" [@sw-nasa-5mcse-catalog]. Downloaded 2026-09-15: 5,952,576 bytes, 11,898 data rows plus header [@sw-nasa-bessel-csv]. Columns: `year, month, day, td_ge, dt, luna_num, saros, eclipse_type, gamma, magnitude, lat_ge, lng_ge, lat_dd_ge, lng_dd_ge, sun_alt, sun_azm, path_width, central_duration, duration_secs, cat_no, canon_plate, julian_date, t0, x0, x1, x2, x3, y0, y1, y2, y3, d0, d1, d2, mu0, mu1, mu2, l10, l11, l12, l20, l21, l22, tan_f1, tan_f2, tmin, tmax, etype, PNS, UNS, NCN, nSer, nSeq, nJLE` [@sw-nasa-bessel-csv]. The first row (-1999 June 12, type T) has `dt` = 46438.2 s, `t0` = 3.0, `x0` = -0.056331, `x1` = 0.5538768, `tan_f1` = 0.0046008, `tan_f2` = 0.0045779, `tmin` = -3, `tmax` = 3 [@sw-nasa-bessel-csv]. The $d$ and $\mu$ polynomials are quadratic and $x$ and $y$ cubic in this file, matching the per-eclipse HTML pages [@sw-nasa-bessel-2024]. The elements were computed with VSOP87 and ELP-2000/82 and the Canon ΔT [@sw-nasa-5mcse-catalog].

**Per-eclipse HTML pages.** `https://eclipse.gsfc.nasa.gov/SEbeselm/SEbeselm2001/SE2024Apr08Tbeselm.html` and siblings give the same polynomials with $k_1$, $k_2$, ΔT and the solar semi-diameter [@sw-nasa-bessel-2024].

**Path tables.** `https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2024Apr08Tpath.html` gives limits and central line at 120-second intervals as preformatted text in WGS 84 [@sw-nasa-path-2024].

**Derived repackagings.** gmiller123456's repository offers the same data as CSV, JS and JSON [@sw-gmiller-5mcse-repo]. Jubier's 5MCSE interface generates per-eclipse KMZ on demand [@sw-jubier-5mcse]. EclipseWise's 2024 bulletin extras include libration values, shadow contact data, central line data and polynomial elements as web pages [@sw-eclipsewise-2024].

**Jubier's elements.** Each interactive map page embeds its own element array in the HTML, with its own ΔT (69.1 s for 2024) [@sw-jubier-2024-map].

## SVS GIS products

| Eclipse | Page | Files | Contents |
|---|---|---|---|
| 2017 Aug 21 | SVS 4518 | `eclipse2017_shapefiles.zip`, `eclipse2017_shapefiles_1s.zip` under `/vis/a000000/a004500/a004518/` | Path and umbra shapes; the `_1s` set is at 1-second cadence [@sw-svs-4518] |
| 2023 Oct 14 | SVS 5073 | `2023eclipse_shapefiles.zip`, `2023eclipse_kml.zip`, `cities-eclipse-2023.json` under `/vis/a000000/a005000/a005073/` | See layer list below [@sw-svs-5073] |
| 2024 Apr 8 | SVS 5073, SVS 5123 | `2024eclipse_shapefiles.zip`, `2024eclipse_kml.zip`, `cities-eclipse-2024.json` | See layer list below [@sw-svs-5073] [@sw-svs-5123] |

Each 2023 and 2024 zip contains `center`, `duration` (30-second isocontours), `ppath` (5 per cent obscuration contours), `ppath01` (1 per cent), `umbra_hi` (1-second umbra polygons, region limited), `umbra_lo` (10-second, global), `upath_hi` and `upath_lo` [@sw-svs-5073]. The city JSON has `LON`, `LAT`, `NAME`, `STATE` and an `ECLIPSE` array of UTC times at 0.01, 50, 100, 50 and 0.01 per cent of maximum coverage for over 32,000 US cities [@sw-svs-5073]. Inputs were SRTM and LRO LOLA plus Kaguya (SELENE), with JPL DE421 on the product pages and DE440 in the paper's appendix, as set out in [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md) [@sw-svs-5073] [@sw-svs-4518]. At the time of writing (2026 September) svs.gsfc.nasa.gov refused TCP connections, so the zip URLs could not be verified live and the pages were read from Wayback Machine snapshots dated 2025 [@sw-svs-5073].

## Lunar limb and topography data

Which of these grids to use, and what each costs in contact time, is settled in [datasets: Watts, Kaguya, LOLA](../05-lunar-limb/datasets-watts-kaguya-lola.md). This section keeps the URLs, sizes and formats.

**LOLA GDR.** `https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/` with `cylindrical` and `polar` subdirectories [@sw-lola-gdr]. The cylindrical IMG directory holds `ldem_4.img` (2,073,600 bytes), `ldem_16.img` (33,177,600), `ldem_64.img` (530,841,600), `ldem_128.img` (2,123,366,400), four `ldem_256_*` hemisphere files (1,061,683,200 each) and `ldem_1024_<lat>_<lon>.img` tiles of about 943,718,400 bytes in 15-degree latitude bands and 30-degree longitude segments, each with `.lbl` and `.xml` labels [@sw-lola-gdr-img]. The number in the name is pixels per degree, so `ldem_16.img` is at 16 pixels per degree, which tomasrojasc/eclipse-2026 quotes as about 1.9 km at the limb [@sw-repo-eclipse-2026-rojas]. Format is PDS3 IMG with detached label.

**SLDEM2015.** `https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/sldem2015/` with `global` and `tiles` subdirectories [@sw-sldem2015]. SVS names this product (LOLA merged with SELENE Terrain Camera) among its inputs [@sw-svs-5073].

**Kaguya (SELENE) LALT.** The JAXA DARTS SELENE archive is at `https://darts.isas.jaxa.jp/planet/pdap/selene/` and was reachable, though its product pages were not read [@sw-darts-selene]. SVS 4518 cites "JAXA Kaguya stereo imaging" and Jubier's calculator cites "Kaguya's DEM" for limb corrections [@sw-svs-4518] [@sw-jubier-calc-js].

**Lunar orientation.** The NAIF PCK directory at `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/` was reachable. `moon_pa_de440_200625.bpc` with frame kernel `moon_de440_250416.tf` is the pairing for DE440. `moon_pa_de421_1900-2050.bpc` is the older binary PCK, and it is what tomasrojasc/eclipse-2026 uses to orient the LOLA profile for the libration at contact time [@sw-naif-moon-pa] [@sw-repo-eclipse-2026-rojas].

**Watts charts and Occult limb data.** Jubier's Watts-chart corrections are served by his PHP back end and are not downloadable [@sw-jubier-calc-js]. Occult 4 distributes its limb data among 42 downloadable data files installed by the program, not as a standalone dataset [@sw-occult4]. SolarEclipseWorkbench bundles `lunar_limb_band_v1.bin` of undocumented format [@sw-repo-sew].

## Terrestrial elevation

- SRTMGL1 v003 (1 arcsecond, about 30 m) at LP DAAC: `https://lpdaac.usgs.gov/products/srtmgl1v003/` (reachable) [@sw-srtmgl1]. SVS used SRTM (SIR-C) [@sw-svs-5073].
- Copernicus DEM GLO-30 and GLO-90 on the AWS Open Data Registry: `https://registry.opendata.aws/copernicus-dem/` (reachable) [@sw-copernicus-dem]. Used by carlok/eclipse-3d-sim via OpenTopography and by umbra-eclipse-atlas via Open-Meteo [@sw-repo-eclipse-3d-sim] [@sw-repo-umbra-atlas].
- EU-DEM 25 m via OpenTopoData is used by eclipsite [@sw-repo-eclipsite].

## ΔT and Earth orientation

- USNO observed ΔT: `https://maia.usno.navy.mil/ser7/deltat.data` (text/plain, reachable) [@sw-usno-deltat-data].
- USNO predicted ΔT: `https://maia.usno.navy.mil/ser7/deltat.preds` (text/plain, reachable) [@sw-usno-deltat-preds].
- IERS `finals.all.iau2000.txt`: `https://datacenter.iers.org/data/latestVersion/finals.all.iau2000.txt` (text/plain, reachable), giving UT1-UTC and polar motion [@sw-iers-finals]. Stellarium's default ΔT interpolates IERS values for 2015 to 2033 on top of the Espenak and Meeus polynomial [@sw-stellarium-stelcore].
- NASA Canon polynomials with the $-0.000012932(y-1955)^2$ secular-acceleration correction: `https://eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html` [@sw-nasa-deltatpoly].
- Swiss Ephemeris since 2.06 uses Stephenson, Morrison and Hohenkerk 2016 for historical ΔT [@sw-swisseph-gendoc].

## Ephemerides

- JPL DE440 SPK: `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440.bsp` (binary, reachable) [@sw-jpl-de440]. sunpy's example uses `de440s` [@sw-sunpy-gallery-eclipse]. Eclipse-Engine fits elements to DE440s [@sw-repo-eclipse-engine].
- DE421 is what eclipsite, eclipse-2026 and jpatka use, and it is what every SVS product page names, with DE440 in the SVS paper's appendix [@sw-svs-5073] [@sw-repo-eclipsite] [@sw-repo-eclipse-2026-rojas] [@sw-repo-jpatka]. The NAIF path `generic_kernels/spk/planets/de421.bsp` returned 404 at the time of writing (2026 September), so the current location of that file was not verified.
- Swiss Ephemeris files are compressed from DE431 [@sw-swisseph-gendoc].
- NASA's Canon uses VSOP87 and ELP-2000/82 analytic theories rather than a JPL kernel [@sw-nasa-5mcse-catalog].

## Sources compared

| Dataset | Owner | Format | Resolution or cadence | Reachable 2026-09-15 |
|---|---|---|---|---|
| Besselian elements CSV [@sw-nasa-bessel-csv] | NASA GSFC | CSV, 54 columns | One row per eclipse, cubic polynomials | Yes |
| SVS 2023 and 2024 GIS [@sw-svs-5073] | NASA SVS | Shapefile, KML, JSON | 1 s and 10 s umbra polygons | Pages via archive only |
| SVS 2017 GIS [@sw-svs-4518] | NASA SVS | Shapefile | 10 s and 1 s | Pages via archive only |
| LOLA LDEM [@sw-lola-gdr-img] | NASA PDS | PDS3 IMG plus LBL | 4 to 1024 pixels per degree | Yes |
| SLDEM2015 [@sw-sldem2015] | NASA PDS | PDS3 IMG | Global and tiles | Yes |
| Kaguya LALT [@sw-darts-selene] | JAXA DARTS | Not read | Not read | Root page yes |
| SRTMGL1 [@sw-srtmgl1] | NASA LP DAAC | HGT or GeoTIFF | 1 arcsecond | Yes |
| Copernicus DEM [@sw-copernicus-dem] | ESA via AWS | Cloud-optimised GeoTIFF | 30 m and 90 m | Yes |
| deltat.data, deltat.preds [@sw-usno-deltat-data] [@sw-usno-deltat-preds] | USNO | Text | Observed and predicted | Yes |
| finals.all [@sw-iers-finals] | IERS | Fixed-width text | Daily | Yes |
| DE440 [@sw-jpl-de440] | JPL SSD | SPK | Continuous | Yes |
| `moon_pa_de440_200625.bpc`, `moon_pa_de421_1900-2050.bpc` [@sw-naif-moon-pa] | NAIF | Binary PCK | 1549 to 2650 and 1900 to 2050 | Yes |

## What a developer should do

Download the NASA CSV once and treat it as the regression fixture for the elements stage [@sw-nasa-bessel-csv]. Fetch the three SVS zips through an archive mirror if the live host stays unreachable and keep them as the fixture for limb-corrected umbra shapes [@sw-svs-5073]. Start limb work with `ldem_128.img` (2.12 GB). `ldem_16.img` (33 MB) serves only for smoke tests, since one cell at 16 pixels per degree is worth 2 to 3 s of contact time, as shown in [datasets: Watts, Kaguya, LOLA](../05-lunar-limb/datasets-watts-kaguya-lola.md) [@sw-lola-gdr-img]. Pair every LOLA use with the PCK of the ephemeris in use, `moon_pa_de440_200625.bpc` for DE440 [@sw-naif-moon-pa]. Pull `deltat.data`, `deltat.preds` and `finals.all` on a schedule and record the fetch date in every product [@sw-usno-deltat-data] [@sw-usno-deltat-preds] [@sw-iers-finals].

## What this changes

Nothing in the stage design. It confirms that every input the SVS pipeline used is publicly downloadable, so the SVS products can be reproduced in principle.

## Open questions

- Obtain the SVS shapefile zips themselves and record their coordinate reference system and attribute schema (the pages describe layers but not attributes) [@sw-svs-5073].
- Obtain the Kaguya LALT product listing and label format from DARTS [@sw-darts-selene].
- Obtain the current NAIF location of `de421.bsp`, since the standard generic-kernel path returned 404.
- Obtain the format of SolarEclipseWorkbench's `lunar_limb_band_v1.bin` and its provenance [@sw-repo-sew].
