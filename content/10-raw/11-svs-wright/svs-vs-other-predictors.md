---
title: SVS versus Espenak, Jubier and Irwin
description: Where the NASA SVS path differs from the NASA eclipse site, EclipseWise, Jubier's maps and the Besselian Elements map, by how much, and which constant is responsible.
order: 3
status: working
updated: 2026-09-15
tags: [svs, espenak, jubier, irwin, solar-radius, delta-t, comparison]
---

::: summary
- **Two NASA maps disagree** for 2024 because Espenak's eclipse.gsfc.nasa.gov predictions use a smooth Moon and a sea-level Earth, and SVS uses the LOLA limb and SRTM terrain. Espenak's site says limb corrections "may shift the limits ... by ~1-3 kilometers, and change the eclipse duration by ~1-3 seconds" [@svs-espenak-2024-path].
- **The solar radius** is the other axis of disagreement. SVS and Espenak use 696,000 km (959.63 arcseconds). Irwin and Quaglia use 959.95 plus or minus 0.05 arcseconds (696,221 km). The larger Sun narrows the path by "several city blocks" at each limit [@svs-irwin-quaglia-2024-technical] [@svs-wright-young-2024].
- **The ephemerides differ but do not matter** at this level: the "VSOP87/ELP2000-85" the NASA eclipse site's 2024 element page names, with $\Delta T$ = 70.6 s, DE405 with $\Delta T$ = 71.5 s on EclipseWise, DE421 or DE440 with $\Delta T$ from IERS kernels at SVS, DE440 with TT minus UT1 = 69.2015 s at Besselian Elements [@svs-espenak-2024-besselian] [@svs-eclipsewise-2024-prime] [@svs-irwin-quaglia-2024-technical].
- **Jubier and Zeiler** produced limb-corrected umbra shapes before SVS, and Zeiler reports "good agreement despite a different computational process" when compared with Wright's 2017 results [@svs-zeiler-double-diamond].
- **NASA did not revise its 2024 map.** Its statement said "a few city blocks one way or the other could mean 20, 10, or 0 seconds of totality" [@svs-cnn-wattles-2024].
:::

**The question.** When the SVS path, the NASA eclipse site path, EclipseWise, Jubier's interactive maps and the Besselian Elements map disagree for the same eclipse, which input explains the difference and how large is it?

## The predictors and their inputs

The full side-by-side of which predictor uses which ephemeris, ΔT, radius, limb and terrain is in [predictor disagreements](../10-validation/predictor-disagreements.md). This table keeps the SVS and Irwin rows, whose parameter sets are transcribed here and nowhere else.

| Predictor | Ephemeris | $\Delta T$ or EOP for 2024 | Solar radius | Lunar radius or limb | Earth model |
|---|---|---|---|---|---|
| NASA eclipse site, Espenak [@svs-espenak-2024-besselian] [@svs-espenak-2024-path] | "VSOP87/ELP2000-85" as the page labels it | 70.6 s | 959.63 arcseconds, implied by the $k$ convention | $k_1$ = 0.272488 penumbra, $k_2$ = 0.272281 umbra, no limb | ellipsoid, sea level |
| EclipseWise, Espenak [@svs-eclipsewise-2024-prime] | JPL DE405 | 71.5 s | not stated on the page | $k$ = 0.2725076 penumbra, 0.2722810 umbra, no limb | ellipsoid, sea level |
| NASA SVS, Wright [@svs-4515-2017-path] [@svs-wright-young-2024] | DE421 on product pages, DE440 in the paper's appendix | IERS EOP kernel, 68.917 s in 2017, unstated for 2024 | 696,000 km, 959.645 arcseconds | 1737.4 km datum plus SLDEM2015 and the polar LDEM limb profile | WGS 84, EGM96, SRTM terrain |
| Besselian Elements, Irwin and Quaglia [@svs-irwin-quaglia-2024-technical] | JPL DE440 | IAU2006A with EOP, TT minus UT1 = 69.2015 s, UT1 minus UTC = minus 0.0175 s, polar motion (minus 0.015, plus 0.359) arcseconds | 696,221 plus or minus 36 km, 959.95 plus or minus 0.05 arcseconds | 1738.091 km mean plus SLDEM2015 and the LOLA LDEM at 256 and 128 pixels per degree, ME421 orientation relative to PA440 | WGS 84 at 6378.137 and 6356.752 km, Earth2014 at 60 pixels per degree plus EGM96 |
| Jubier, interactive maps and Solar Eclipse Maestro [@svs-jubier-google-maps] | not stated on the pages read | not stated | not stated | limb profile and Baily's beads simulation offered per site | terrain elevation profile offered per site |

The Irwin and Quaglia row is transcribed from the parameter table image on their technical page, which also lists the astrometric method as "light-time + gravitational light deflection + planetary aberration", the origin as "hybrid (topocentric & geocentric)", and the software as "EclipseView, LimbView & SkyWare (proprietary)" [@svs-irwin-quaglia-2024-technical].

Jubier's constants are not published in any retrievable form: the interactive pages build themselves in the browser, and the Internet Archive capture of the 2024 map holds only the loader. His site index describes per-click "lunar limb profile and Baily's beads" and "terrain elevation profile" features without naming datasets [@svs-jubier-google-maps]. The paper credits Jubier's software as the engine behind Zeiler's limb-corrected maps since 2012 and cites Jubier et al. 2021 for a solar radius of 959.98 arcseconds, from a presentation whose PDF link now returns 404 [@svs-wright-young-2024].

## The limb and terrain difference

Espenak's own caveat sets the scale. The 2024 path page states that the predictions "DO NOT include the effects of mountains and valleys along the edge of the Moon. Such corrections ... may shift the limits of the eclipse path north or south by ~1-3 kilometers, and change the eclipse duration by ~1-3 seconds" [@svs-espenak-2024-path]. Espenak's reference page on the lunar radius explains why he uses two values: the IAU 1982 $k$ = 0.2725076 is "the best mean radius, averaging mountain peaks and low valleys", while $k$ = 0.272281 is "a mean minimum radius" used for umbral contacts so that beaded annular eclipses are not misidentified as total [@svs-espenak-radius-reference]. This two-$k$ device is the Besselian tradition's proxy for the limb, and it is exactly what the SVS limb test replaces.

The terrain term is SVS's addition. On 2017 August 21 western elevations shifted the umbra "toward the southeast (in the direction of the Sun's azimuth) by as much as 3 kilometers" [@svs-4517-umbra-shapes], and the paper's Figure 1 shows a 1.5 km shift west of Idaho Falls [@svs-wright-young-2024]. The paper's rule of thumb is a shift of $h\cot a$: at 1500 m elevation and 45 degrees solar altitude the shift is 1.5 km, and at 20 degrees altitude it is 4.1 km. None of the Espenak products model this. Irwin's map does, with Earth2014 at 60 pixels per degree [@svs-irwin-quaglia-2024-technical].

Zeiler's account of the 2017 comparison is the only published cross-check between independent limb-corrected implementations: Wright "independently produced similar lunar limb corrected umbral figures", and when Zeiler and Wright compared results they "found good agreement despite a different computational process" [@svs-zeiler-double-diamond]. No number is given.

## The solar radius difference

The 2024 dispute was entirely about the solar radius. Irwin's map, published on the Besselian Elements site in March 2024, "incorporates adjustments that account for the topographic elevation, both around the limb of the Moon and on the surface of the Earth", and draws "true limb eclipse limits" in orange with error bars against "traditional smooth limits" in red [@svs-irwin-2024-path]. The technical page explains the difference from NASA: it uses "an improved solar radius S equivalent to 959.95 arcseconds at 1 a.u. This is a better value to use than the 'standard' solar radius S = 959.63 arcseconds usually used in eclipse maps", backed by "recent determinations collected during solar eclipses, some by us", plus "the most recent determinations of certain other parameters ... mainly the Earth's orientation parameters" [@svs-irwin-quaglia-2024-technical]. The measurement behind 959.95 is Quaglia, Irwin, Emmanouilidis and Pessi 2021, from flash-spectrum video at the southern limit of the 2017 path [@svs-quaglia-2021-apjs].

The size of the effect, stated by the parties:

- Wright and Young: Irwin's radius "had the effect of shifting the northern limit of the path to the southeast by several city blocks compared to maps calculated with the conventional radius" [@svs-wright-young-2024].
- NASA's statement, through spokesperson Karen Fox: "Calculations that use a slightly larger radius for the size of the Sun yield an eclipse path that is slightly narrower. This difference would only affect cities on the very edge of the path of totality, where blanket predictions are difficult regardless: a few city blocks one way or the other could mean 20, 10, or 0 seconds of totality." NASA also said "precise eclipse prediction has brought new attention to a tiny but real uncertainty about the size of the Sun" and that "uncertainty in the Earth's rotation can also affect eclipse predictions on this level" [@svs-cnn-wattles-2024].
- Edward Guinan, quoted by CNN: "even if the NASA map is wrong, Irwin's calculations indicate it's only off by a couple thousand feet on the edges" [@svs-cnn-wattles-2024].

A back-of-envelope check, which is this note's arithmetic and not a source's: the difference of 0.32 arcseconds in solar radius is $1.55 \times 10^{-6}$ radians. At the Moon's distance of about 360,000 km that is about 0.56 km of umbra radius, so each limit moves inward by roughly 0.6 km divided by the cosine of the angle between the shadow axis and the local vertical. Near the middle of the 2024 path that is 0.6 to 0.8 km per limit, which matches "several city blocks" and "a couple thousand feet". The paper's sensitivity statement gives the same order from the other direction: 0.03 arcseconds per second of duration at the limits, so 0.32 arcseconds is about 10 s of duration lost or gained by an observer right at a limit [@svs-wright-young-2024].

The one timed test of this difference is the 2024 Stephenville experiment, where 13.7 s was observed against 12.9 s from Irwin's true-limb model with 959.95 arcseconds and up to 65 s from smooth-Moon products with the conventional radius. It is reported in [observed versus predicted](../10-validation/observed-vs-predicted.md) [@val-besselian-maps-accuracy].

The paper's Table of recent eclipse-derived radii (959.99, 959.95, 959.98, 960.01 arcseconds) and its remark that "the need for an authoritative consensus is becoming acute" are the closest thing to a position SVS has taken. The SVS products themselves stayed at 696,000 km through the March 2025 map [@svs-5510-mar-2025-partial-map]. Guhl's 2023 value of 960.01 plus or minus 0.12 arcseconds, which cites 959.63 as the value in the reduction software it corrects, reinforces that the community's working values are all about 0.3 to 0.4 arcseconds above the conventional one [@svs-guhl-2023-joa].

## The ephemeris and time difference

The four predictors use four ephemeris and time combinations, and none of the sources attribute any visible path difference to them. [?tt|TT] is the scale of the elements, printed as TDT or TD in NASA and EclipseWise tables and as ET before 1984. The NASA eclipse site's Besselian elements page for 2024 gives $t_0$ = 18:00:00 TDT, $x_0$ = minus 0.318157, $y_0$ = 0.219747, $d_0$ = 7.58620 degrees, $l_1$ = 0.535813, $l_2$ = minus 0.010274, $\mu_0$ = 89.59122 degrees, rates $x_1$ = 0.5117105, $y_1$ = 0.2709586, $\mu_1$ = 15.004084, with $\Delta T$ = 70.6 s and the ephemerides it labels "VSOP87/ELP2000-85" [@svs-espenak-2024-besselian]. NASA labels its 2024 element page "VSOP87/ELP2000-85", while the Five Millennium Canon text describes ELP-2000/82, so the two are different runs [@svs-espenak-2024-besselian]. EclipseWise for the same eclipse uses DE405 and $\Delta T$ = 71.5 s, with greatest eclipse at 18:18:29.4 TD, 18:17:17.9 UT1, duration 4 min 28.13 s and width 197.5 km [@svs-eclipsewise-2024-prime]. The NASA eclipse site gives greatest eclipse at 18:17:18.3 UT, 4 min 28.1 s and 197.5 km [@svs-espenak-2024-path].

The actual TT minus UT1 in April 2024 was about 69.2 s, which is what Irwin's table states [@svs-irwin-quaglia-2024-technical] and what an IERS-based SPICE kernel would encode for SVS. Espenak's 70.6 s and 71.5 s are predictions made years earlier. A $\Delta T$ error of 1.4 to 2.3 s displaces the whole path in longitude by the Earth's rotation over that interval, 0.4 to 0.7 km at 40 degrees latitude, without changing its width or its latitude. That is the same order as the solar-radius effect but in a different direction, and unlike the radius effect it is fully correctable before the event.

SVS's own 2017 pages show the same mechanism: $\Delta T$ = 68.917 s and Delta UTC 69.184 s with 37 leap seconds [@svs-4515-2017-path], versus the predicted value used in the 2015 smooth animation, Delta UTC 68.184 s with 36 leap seconds [@svs-4314-2017-usa].

## Where the SVS product differs from the NASA eclipse site, by cause

| Cause | Direction and size | Source |
|---|---|---|
| Lunar limb | Limits move 1 to 3 km, duration changes 1 to 3 s, edges become polygonal | [@svs-espenak-2024-path] [@svs-wright-young-2024] |
| Terrain | Umbra shifts toward the Sun's azimuth by $h\cot a$, up to 3 km in the 2017 west | [@svs-4517-umbra-shapes] |
| Solar radius | None between SVS and Espenak, both 696,000 km. Irwin's 959.95 narrows the path by about 0.6 km per limit | [@svs-irwin-quaglia-2024-technical] [@svs-cnn-wattles-2024] |
| $\Delta T$ | Longitude shift of order 0.5 km between predicted and observed values | [@svs-espenak-2024-besselian] [@svs-irwin-quaglia-2024-technical] |
| Ephemeris | Negligible at the 600 m limb-profile resolution | [@svs-wright-young-2024] |
| Lunar radius convention | Espenak's two $k$ values approximate the limb, SVS uses the DEM directly | [@svs-espenak-radius-reference] |

## Sources compared

| Source | What it uniquely provides |
|---|---|
| Espenak 2024 path page [@svs-espenak-2024-path] | The 1 to 3 km and 1 to 3 s limb caveat in NASA's own words. |
| Espenak Besselian elements [@svs-espenak-2024-besselian] | The polynomial elements, $\Delta T$ = 70.6 s and the two $k$ values. |
| Espenak radius reference [@svs-espenak-radius-reference] | The rationale for $k$ = 0.272281 on umbral contacts. |
| EclipseWise [@svs-eclipsewise-2024-prime] | DE405 and $\Delta T$ = 71.5 s, showing Espenak's two sites differ from each other. |
| Irwin and Quaglia technical table [@svs-irwin-quaglia-2024-technical] | The only fully itemised parameter set of any predictor, including EOP values and DEM resolutions. |
| CNN, Wattles [@svs-cnn-wattles-2024] | NASA's official response and Guinan's "couple thousand feet". |
| Zeiler [@svs-zeiler-double-diamond] | The 2017 cross-check between Wright and Jubier-based maps. |
| Wright and Young [@svs-wright-young-2024] | The 0.03 arcseconds per second sensitivity and the list of measured radii. |

## What a developer should do

Make the solar radius a named parameter with a default and a documented alternative: 696,000 km (959.63 arcseconds) to reproduce SVS and Espenak, 959.95 arcseconds to reproduce Irwin. Report both limits on any map intended for observers near the edge. Take $\Delta T$ from IERS Bulletin A or a SPICE EOP kernel rather than a long-range prediction, and state the value used. Implement the limb from the DEM rather than through a second $k$. Do not expect ephemeris choice among DE421, DE430, DE440 to change anything at the 100 m level. For validation, compare your umbra polygons with SVS umbra_hi, your smooth-model limits with Espenak's path table, and your limb-corrected limits with Irwin's orange lines, in that order.

## What this changes

It fixes the error budget for the pipeline. At the path limits the limb contributes 1 to 3 km, terrain up to a few kilometres at low Sun, the solar radius about 0.6 km per limit per 0.3 arcseconds, and $\Delta T$ about 0.5 km per 2 s. A pipeline that resolves the first two and parameterises the last two is at the state of the art. Nothing else changes.

## Open questions

- **A quantitative SVS versus Irwin comparison.** Obtain Irwin's 2024 limit polylines, or the Besselian Elements app's output, and difference them against SVS upath_hi at fixed longitudes.
- **Jubier's constants.** Read the Solar Eclipse Maestro help pages or the interactive map's info panel in a browser to record his ephemeris, $\Delta T$, solar radius and limb dataset.
- **Espenak's solar radius.** Neither page read here states the arcsecond value. The open question is kept in [solar radius values](../06-solar-radius/solar-radius-values.md), which is the home for the radius question.
- **The 2017 Zeiler and Wright comparison.** Ask either party for the numerical residuals.
- **Observed 2024 limits.** The Quaglia and Irwin team collected limit observations in 2024. Their published reduction would settle which radius the 2024 path actually followed.
