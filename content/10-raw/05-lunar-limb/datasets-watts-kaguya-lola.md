---
title: "Datasets: Watts, Kaguya, LOLA"
description: Every limb dataset with its resolution, reference sphere, frame, accuracy, file format and download location, and the centre-of-figure offset that separates the old data from the new.
order: 2
status: working
updated: 2026-09-15
tags: [watts, kaguya, lalt, lola, ldem, sldem2015, datasets]
---

::: summary
- **Three generations of data**: Watts' 1963 photographic charts, Kaguya (SELENE) LALT laser altimetry from 2009, and LRO LOLA altimetry from 2010 onward, the last two merged with Kaguya Terrain Camera stereo as SLDEM2015 [@limb-vizier-vi122] [@limb-lalt-ggt-map-label] [@limb-ode-sldem].
- **All modern grids share one datum**: heights above a sphere of radius 1737.4 km centred on the Moon's centre of mass, in the mean Earth/polar axis frame of DE421 [@limb-lola-ldem128-label] [@limb-lalt-ggt-map-label] [@limb-sldem2015-label].
- **Resolutions**: the Kaguya LALT grid is 16 pixels per degree, 1.895 km. LOLA LDEM runs from 4 to 1024 pixels per degree, with 128 pixels per degree at 236.9 m. SLDEM2015 is 512 pixels per degree, about 60 m [@limb-lola-gdr-dscat] [@limb-pgda-sldem2015].
- **Accuracy**: LOLA vertical precision is about 10 cm and accuracy about 1 m per shot. SLDEM2015 has a typical vertical accuracy of 3 to 4 m. Watts heights are good to about 0.2 arcseconds, about 370 m, with systematic errors to 0.4 arcseconds [@limb-pgda-sldem2015] [@limb-ode-sldem] [@limb-sigismondi-thesis-2011] [@limb-morrison-appleby-1981].
- **The centre-of-figure offset** is about 1.9 km and points mostly away from Earth. It mattered for Watts, whose datum was a centre-of-figure surface, and does not matter for DEMs, which are referenced to the centre of mass [@limb-morrison-appleby-1981] [@limb-smith-2010-lola].
- **Files to download** are named below with their PDS and DARTS URLs. LDEM_128 is 2.12 GB and LDEM_16 is 33.2 MB [@limb-lola-gdr-dir].
:::

**The question.** Which limb datasets exist, what exactly do their numbers mean, where are they downloaded, and how are they related to the point that the lunar ephemeris tracks?

## Watts 1963: The Marginal Zone of the Moon

**What it is.** Charts of the height of the lunar limb above a smooth datum, drawn from a photographic survey of 503 sequences taken 1927 to 1956 at Washington, Johannesburg and Flagstaff, published in 1963 in Astronomical Papers of the American Ephemeris Vol. XVII [@limb-vizier-vi122] [@limb-watts-1963]. There are 1800 charts, one per 0.2 degrees of [?watts-angle|Watts angle] measured from the Moon's north pole, with a contour interval of 0.2 arcseconds, covering librations $L$ from $-9^{\circ}$ to $+9^{\circ}$ and $B$ from $-8^{\circ}$ to $+8^{\circ}$ [@limb-vizier-vi122].

**Digital form.** VizieR catalogue VI/122 holds the HMNAO digitisation reformatted by USNO. `WATTS.TXT` is 79,606,800 bytes of fixed 6-byte records: a sign byte, a three-digit height in units of 0.01 arcseconds, and two accuracy codes $a$ and $b$ from 0 to 7. Records are indexed by $729000(9.0-L) + 9000(8.0-B) + 5\,\mathrm{WA} + 1$ over a 0.2 degree libration grid and 1800 Watts angles [@limb-vizier-vi122]. Code $b$ says whether contours were interpolated, extrapolated, too sparse, or missing. Code $a/2$ is the contour density per degree or the extrapolation distance in degrees depending on $b$ [@limb-vizier-vi122]. Chart 36.0 was corrected by hand from the paper chart, and the Cassini regions lack contours, with grazing observations showing systematic deviations there at positive latitude librations on the northern limb [@limb-vizier-vi122].

**Angle conventions.** "It is necessary to add 0.21 deg. to a computed Axis Angle to obtain the corresponding Watts Angle," plus $-0.022\cos(L-W)$ degrees for the inclination Watts used, 1.564 degrees, against the almanac's 1.542 degrees [@limb-vizier-vi122]. Morrison and Appleby used $Q + 0.25^{\circ}$ [@limb-morrison-appleby-1981]. Solar Eclipse Maestro corrects 0.241 degrees [@limb-jubier-sem-limb-window].

**Datum.** The [?watts-datum|datum] is a centre-of-figure surface. Morrison and Appleby's reduction assumed a datum radius of 1737.97 km, 932.58 arcseconds at mean distance [@limb-morrison-appleby-1981]. Later occultation solutions for the effective Watts radius, collected by Sigismondi, run from 1738.05 ± 0.02 km (Morrison and Appleby 1981) through 1738.09 km (Newhall et al. 1983) to 1738.103 ± 0.002 km (Rosselló and Jordi 1991), all larger than the 1737.4 km Kaguya sphere [@limb-sigismondi-thesis-2011]. Corrections to a spherical datum at the centre of mass are given in [Limb profile methods](limb-profile-methods.md) and reach 0.4 arcseconds [@limb-morrison-appleby-1981].

**Accuracy.** Individual heights are good to about 0.20 arcseconds, treated as random [@limb-sigismondi-thesis-2011]. Herald's 1983 error budget puts the uncertainty of the actual limb relative to the datum at ±0.2 arcseconds at any point and notes occasional missing features [@limb-herald-1983]. At 1.863 km per arcsecond [@limb-espenak-limb-page] the random error is about 370 m in height.

## Kaguya (SELENE) LALT

**Instrument and mission.** The Laser Altimeter on the Japanese Kaguya (SELENE) orbiter, launched 2007, produced the first complete polar topography and a global shape model complete to degree and order 359 on a quarter-degree grid, published by Araki et al. in Science in 2009 [@limb-araki-2009]. The paper was not read for this note, and the numbers are from search summaries.

**Products at JAXA DARTS.** The PDS3 dataset `SLN-L-LALT-5-TOPO-GGT-MAP-V2.0` at `https://data.darts.isas.jaxa.jp/pub/pds3/sln-l-lalt-5-topo-ggt-map-v2.0/` contains `LALT_GGT_MAP.IMG` (63 MB) with label `LALT_GGT_MAP.lbl` [@limb-darts-kaguya-faq] [@limb-ltvt-kaguya-wiki]. The label states: MAP_RESOLUTION 16 pixel/degree, MAP_SCALE 1.8952094015 km/pixel, A_AXIS_RADIUS 1737.400 km, 32-bit PC_REAL samples in km, OFFSET 0, SCALING_FACTOR 1, COORDINATE_SYSTEM_NAME "MEAN EARTH/POLAR AXIS OF DE421", version 2.0, and that the altitudes are relative to a 1737.4 km sphere centred on the centre of mass, interpolated with the GMT `sphinterpolate` routine on a 0.0625 degree grid [@limb-lalt-ggt-map-label]. Sibling datasets hold the numeric table `LALT_GGT_NUM`, the polar grids `LALT_GT_NP` and `LALT_GT_SP` at 64 points per degree out to 10 degrees from each pole, and the spherical harmonic coefficients `LALT_SH` [@limb-ltvt-kaguya-wiki] [@limb-darts-kaguya-faq].

**Resolution at the limb.** 1.895 km per pixel is about one arcsecond at the Moon. The raw LALT tracks that Occult and Eclipse Orchestrator used are sampled about every 1.5 km along track with a height accuracy of ±1 m [@limb-sigismondi-thesis-2011] [@limb-eclipse-orchestrator-lro]. The Terrain Camera's SLDEM2013 is a separate 4096 pixels per degree, about 7.4 m, stereo DEM at DARTS [@limb-darts-kaguya-faq].

**Mean radius.** The LALT shape model gives a mean radius of 1737.15 km. That value is reported secondhand from the DARTS material and is not confirmed in the FAQ itself [@limb-darts-kaguya-faq]. SLDEM2015's own mean radius from its $C_{00}$ term is given as 1737.1512 km, 248.8 m below the 1737.4 km reference, on a secondary report of Barker et al. rather than the paper [@limb-barker-2016-sldem]. Both say the same thing: the reference sphere is 250 m larger than the actual mean radius, so the average limb height in a DEM-derived profile is about $-0.13$ arcseconds.

## LRO LOLA: the LDEM series

**Archive.** The Gridded Data Record of the LOLA RDR archive at the PDS Geosciences Node, dataset `LRO-L-LOLA-4-GDR-V1.0`, directory `https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/` with subdirectories `cylindrical` and `polar` [@limb-lola-gdr-dscat]. The data set catalogue states that the GDR "consists primarily of raster Digital Elevation Models formatted as binary images with detached labels" at 4, 16, 64, 128, 256 and 512 pixels per degree in equidistant cylindrical projection, plus sparse 1024 pixels per degree maps and polar stereographic maps from 240 m down to 5 m per pixel [@limb-lola-gdr-dscat].

**Files.** In `cylindrical/img/`: `ldem_4` (2.07 MB), `ldem_16` (33.2 MB), `ldem_64` (530.8 MB), `ldem_128` (2.12 GB), `ldem_256`, `ldem_512`, and `ldem_1024_*` tiles of 30 by 15 degrees at 943.7 MB each, every file with a `.lbl` and `.xml` label; `float_img/` and `jp2/` hold floating-point and JPEG2000 versions [@limb-lola-gdr-dir].

**The LDEM_128 label, verbatim fields.** MAP_RESOLUTION 128 pix/deg; MAP_SCALE 236.901 m/pix; A_AXIS_RADIUS 1737.4 km; OFFSET 1737400; SCALING_FACTOR 0.5; SAMPLE_BITS 16; UNIT METER; COORDINATE_SYSTEM_NAME "MEAN EARTH/POLAR AXIS OF DE421"; PRODUCT_VERSION_ID V3.0; START_TIME 2009-07-13T17:33:17; STOP_TIME 2016-11-29T05:48:19; "Each sample represents height relative to a reference radius (OFFSET) and is generated using geolocated LOLA data produced by the LOLA team" [@limb-lola-ldem128-label]. The radius of a pixel is therefore $1737400 + 0.5 \times \mathrm{DN}$ metres.

**Accuracy.** LOLA's vertical precision is about 10 cm and its accuracy about 1 m per shot [@limb-pgda-sldem2015]. The LOLA team's geodetic grid is accurate to about 10 m radially and 100 m spatially with respect to the centre of mass, a figure taken secondhand from Smith et al. 2010 and still to be confirmed against the paper [@limb-smith-2010-lola]. No accuracy statement appears in the LDEM_128 label or the GDR catalogue [@limb-lola-ldem128-label] [@limb-lola-gdr-dscat].

**Frame.** The [?moon-me-frame|mean Earth/polar axis frame] of DE421. Wright and Young note that the latitude and longitude origin of Moon ME is the mean sub-Earth point [@limb-wright-young-2024]. They load the DE440 lunar orientation kernels for their computation, a different ephemeris from the DE421 named in the label. JPL DE421 is what every SVS product page lists, while the paper's appendix uses DE440, and the difference is under a metre at the Moon [@limb-wright-young-2024]. The difference between the two ME realisations is at the level of metres on the surface and is not a concern at limb-profile resolution.

## SLDEM2015

**What it is.** A co-registration of about 4.5 billion LOLA heights with 43,200 SELENE Terrain Camera stereo DEMs, covering 60 S to 60 N, with an effective resolution of about 60 m at the equator and a typical vertical accuracy of 3 to 4 m, published by Barker et al. in Icarus 273, 346 (2016) [@limb-ode-sldem] [@limb-barker-2016-sldem]. The paper was not read. The PGDA page describes the two-step method, first a five-parameter transformation of each TC tile onto the full-resolution LOLA point cloud in that tile, then a three-dimensional offset fitted to each LOLA profile segment [@limb-pgda-sldem2015].

**Files.** PDS: `https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/sldem2015/` with `global/` and `tiles/`. The global float image at 128 pixels per degree is `sldem2015_128_60s_60n_000_360_float.img` (2.83 GB) with label [@limb-sldem2015-label]. PGDA: `http://imbrium.mit.edu/DATA/SLDEM2015/GLOBAL/` and `TILES/`, with 512, 256 and 128 pixels per degree JPEG2000 and 256 and 128 float versions [@limb-pgda-sldem2015]. The file naming rule is `SLDEM2015_PPP_NNND_SSSD_MMM_OOO_FLOAT.IMG` with PPP the pixels per degree and the latitude and longitude bounds following [@limb-ode-sldem].

**The label, verbatim fields.** MAP_RESOLUTION 128 pix/deg; MAP_SCALE 0.236901 km/pix; A_AXIS_RADIUS 1737.4 km; PC_REAL 32-bit samples in km; SCALING_FACTOR 1; COORDINATE_SYSTEM_NAME "MEAN EARTH/POLAR AXIS OF DE421"; PRODUCT_VERSION_ID V2.0; heights from $-8.717$ to $+10.778$ km; geolocated with the GRGM900B gravity field [@limb-sldem2015-label].

**Use.** [SVS used SLDEM2015](../11-svs-wright/svs-products-and-data.md) for the 2017 and 2024 eclipse maps and for the 2005 broken-annular bead simulation, with the polar stereographic LDEM from LOLA covering the poles beyond 60 degrees, as [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md) confirms [@limb-svs-4517] [@limb-svs-5073] [@limb-svs-5365]. Wright and Young subsample SLDEM to 256 and 128 pixels per degree and recommend the 240 m level paired with 18,000 profile bins [@limb-wright-young-2024].

## Centre of figure and centre of mass

The lunar ephemeris gives the position of the centre of mass. Watts' datum was, by construction, centred near the centre of figure, and occultation reductions had to move it. Morrison and Appleby summarise the evidence available in 1981 [@limb-morrison-appleby-1981]. Occultations give a displacement of 0.72 ± 0.08 arcseconds with the centre of figure leading the centre of mass in orbital longitude. Mulholland's occultation-plus-laser-ranging analysis gives 2.5 ± 0.5 km. Apollo 15 to 17 laser altimetry gives about 1 km, or 0.5 arcseconds. They adopt a $+0.50'' \sin Q$ correction uncertain by 0.2 arcseconds [@limb-morrison-appleby-1981]. LOLA's global solution gives the centre-of-mass to centre-of-figure vector as $(-1.7752, -0.7311, 0.2399)$ km in the mean Earth/polar axis frame, a displacement of 1.9347 km toward 7.12 N, 202.38 E [@limb-smith-2010-lola]. The centre of figure therefore lies about 1.9 km from the centre of mass on the far-side hemisphere. This too is secondhand from Smith et al. 2010 and remains unconfirmed. In the sky, an offset along the Earth-Moon line is invisible at the limb to first order, and its transverse components of about 0.7 km and 0.2 km correspond to 0.4 and 0.1 arcseconds, consistent with the occultation-era values.

The practical consequence: a DEM height is a distance from the centre of mass, so the profile built from it is already in the frame of the ephemeris and no $\delta x \sin Q + \delta y \cos Q$ term is applied. The Sigismondi Hao 2010 table shows what happens when this is done inconsistently, with the IMCCE Kaguya computation differing by 1.9 s at C2 between an optical-centre and a centre-of-mass reduction [@limb-sigismondi-thesis-2011].

## Sources compared

| Dataset | Resolution at limb | Datum | Frame | Accuracy | Where |
|---|---|---|---|---|---|
| Watts 1963 [@limb-vizier-vi122] | 0.2° in Watts angle, 0.01″ height units | Centre-of-figure surface, radius 1737.97 km assumed [@limb-morrison-appleby-1981] | Watts angle from lunar pole, offset 0.21 to 0.25° | 0.2″ random, 0.4″ systematic | VizieR VI/122 |
| Kaguya LALT_GGT_MAP [@limb-lalt-ggt-map-label] | 16 ppd, 1.895 km, about 1″ | 1737.4 km sphere, centre of mass | ME/PA of DE421 | ±1 m height per shot | DARTS PDS3 |
| LOLA LDEM_128 [@limb-lola-ldem128-label] | 128 ppd, 236.9 m, 0.13″ | 1737.4 km sphere, centre of mass | ME/PA of DE421 | about 1 m vertical per shot, 10 m radial grid | PDS GDR |
| LOLA LDEM_512 and 1024 tiles [@limb-lola-gdr-dir] | 59 m and 30 m | same | same | same, sparse at 1024 | PDS GDR |
| SLDEM2015 [@limb-sldem2015-label] [@limb-ode-sldem] | 512 ppd, about 60 m, 0.03″ | 1737.4 km sphere, centre of mass | ME/PA of DE421 | 3 to 4 m vertical | PDS and PGDA |

## What a developer should do

Take `ldem_128.img` and its label as the development dataset: it is one file, 2.12 GB, global including the poles, and its 0.13 arcsecond cell is below the 0.2 s timing target. Move to SLDEM2015 at 256 or 512 pixels per degree only when a bead-level simulation is wanted, and then stitch LDEM polar tiles above 60 degrees. Decode LDEM heights as $0.5\times\mathrm{DN}$ metres and SLDEM heights as kilometres, both above 1737.4 km. Keep the Watts data only for reproducing historical bulletins, and when doing so apply the Morrison and Appleby harmonic correction and the Watts-angle offset explicitly.

## What this changes

The datum choice removes the centre-of-figure stage from the pipeline. The 0.69 km gap between the 1737.4 km DEM sphere and the 1738.09 km sphere of $k = 0.2725076$ becomes a constant that must be added when profile heights are quoted against the almanac mean limb [@limb-jubier-sem-limb-window]. Nothing else in the Besselian stages changes.

## Open questions

- Obtain Barker et al. 2016 to confirm the SLDEM2015 mean radius and horizontal accuracy [@limb-barker-2016-sldem].
- Obtain Smith et al. 2010 to confirm the COM/COF vector and the 10 m radial grid accuracy [@limb-smith-2010-lola].
- Obtain the LOLA GDR `dsmap.cat` and the polar `ldem_*` labels to document the polar stereographic products a global profile needs above 60 degrees [@limb-lola-gdr-dscat].
- Obtain the DARTS `lalt_ds.cat` and the LALT_GGT_NUM label to document the numeric table and the polar 64 points per degree grids [@limb-ltvt-kaguya-wiki].
- Obtain Rosselló, Jordi and Salazar 1991 to document the 1738.103 km Watts datum radius used by Solar Eclipse Maestro [@limb-sigismondi-thesis-2011].
