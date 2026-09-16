---
title: Predictor disagreements
description: Where the NASA SVS, Espenak, Jubier, Irwin, USNO, timeanddate, Occult, Stellarium and Photo Ephemeris products differ in inputs, and by how many metres and seconds at the path edge in 2017 and 2024.
order: 2
status: working
updated: 2026-09-15
tags: [validation, svs, espenak, jubier, irwin, solar-radius, delta-t, path-edge]
---

::: summary
- **The predictors differ by up to 2 km at the 2024 path limits and by up to 50 s in edge durations.** At Stephenville, Texas, six public products predicted 12.9 s to 65 s of totality at one point [@val-besselian-maps-accuracy]. Jubier's limb-corrected limit and Irwin's true-limb limit are about 0.7 km apart, which Dunham attributes to the solar radius [@val-dunham-iota-2024].
- **Three inputs explain almost all of it: solar radius, lunar limb, terrain.** The standard $959.63''$ against about $959.95''$ is 610 m per limit [@val-earthsky-2024-edges]. Omitting the limb profile shifts limits by 1 to 3 km and durations by 1 to 3 s on Espenak's own statement [@val-gsfc-2024-google]. Terrain shifted the 2017 umbra south-east by up to 3 km in the western states [@val-svs-4517].
- **The 2017 "shifted path" story was terrain and limb, not a different ephemeris.** SVS computed umbra shapes at roughly 100 m precision with JPL DE421 on every SVS product page, LRO and Kaguya (SELENE) topography and SRTM, while Espenak's map used DE405 with a smooth Moon and no terrain. The paper's appendix uses DE440, and the difference is under a metre at the Moon, as set out in [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md) [@val-svs-4518] [@val-gsfc-2017-google].
- **ΔT choices differ by a few seconds and matter less than the radius.** For 2024 the NASA eclipse site map used 70.6 s, EclipseWise 71.3 to 71.5 s, and the measured value was 69.20 s [@val-gsfc-2024-google] [@val-eclipsewise-2024-circ] [@val-usno-deltat-data]. One second of $\Delta T$ is 15.041 arcseconds of longitude, about 356 m east-west at 40 degrees latitude [@val-5mcse-tp2009].
- **Implementations given identical inputs still disagree by seconds at the edge.** Irwin's model, Occult and Solar Eclipse Maestro differ by 2 to 4 s of duration at the Vale 2017 site for the same radius [@val-quaglia-2021].
- **USNO, Stellarium and The Photographer's Ephemeris (Photo Ephemeris) publish contacts for a smooth Moon.** USNO states it uses IAU radii and no limb or centre-of-figure correction [@val-usno-2024]. Stellarium iterates contacts to 0.1 s with $959.63''$ [@val-stellarium-code]. Photo Ephemeris states the limb effect it omits is a few seconds and up to about 15 s [@val-photoephemeris-technote].
:::

**The question.** When two reputable products give different path edges or contact times for the same eclipse, which input differs, how large is the resulting difference in metres and seconds, and which product should a developer treat as the reference for which quantity?

## The inputs each predictor states

| Predictor | Ephemeris | $\Delta T$ 2017 / 2024 | Solar radius | Lunar radius or limb | Terrain | Source |
|---|---|---|---|---|---|---|
| NASA eclipse site interactive maps, eclipse.gsfc.nasa.gov (Espenak) | DE405 on the 2017 Google-map page, "VSOP87/ELP2000-85" as the 2024 pages label theirs | 68.4 s / 70.6 s | not stated on page | smooth Moon, $k = 0.272281$ for the umbra | none | [@val-gsfc-2017-google] [@val-gsfc-2024-google] [@val-gsfc-sepredictions] |
| EclipseWise (Espenak) | DE405 prime pages, DE406 circumstances | 68.8 s / 71.5 s (prime), 71.3 s (circumstances) | not stated | $k = 0.2725076$ penumbra, $0.2722810$ umbra | none | [@val-eclipsewise-2017-prime] [@val-eclipsewise-2024-prime] [@val-eclipsewise-2024-circ] |
| NASA SVS (Wright) | DE421 on the product pages, DE440 in the paper's appendix | not stated | $959.63''$ by the paper's own account of "nearly all" calculations | LOLA LDEM and SLDEM2015 limb, 18,000 elements | SRTM | [@val-svs-4518] [@val-svs-5123] [@val-wright-young-2024] |
| Jubier interactive maps | Espenak's elements | extrapolated, "better than 0.5 seconds". The 2024 map page prints 69.1 s, read from the calculator source in [commercial and institutional tools](../09-software-and-repos/commercial-and-institutional-tools.md) | $959.63''$, with the note that the true value is nearer $959.98'' \pm 0.02''$ | Kaguya and LRO corrections as an LC column | elevation from a click | [@val-jubier-map-help] [@val-jubier-calc-instr] |
| Solar Eclipse Maestro (Jubier) | not stated | not stated | $959.63''$ standard | LRO, Kaguya and corrected Watts profiles, IAU mean radius 1738.091 km | yes | [@val-jubier-sem-limb] |
| Besselian Elements (Irwin, Quaglia) | DE430 or later | measured EOP, final 2026 value 69.15 s | $959.95'' \pm 0.05''$ | LOLA in the DE421 mean-Earth frame | yes, jagged limits | [@val-quaglia-2021] [@val-besselian-updates] [@val-besselian-technical] |
| USNO Astronomical Applications | not stated | not stated | 696,000 km | 1737.4 km, no limb, no centre-of-figure correction | height entered by user | [@val-usno-2024] |
| Occult (Herald) | DE435 and DE422 for occultations | not stated | user-set, IOTA/ES use $959.63''$ plus correction | Kaguya and LOLA, 1800 points at $0.2^{\circ}$ | yes | [@val-guhl-tegtmeier-2018] [@val-photoephemeris-verification] |
| Stellarium | its own planetary ephemeris choice | its own $\Delta T$ model | $959.63''$ | its constants `k` = 0.2725076 penumbral and `s` = 0.272281 umbral | none | [@val-stellarium-code] |
| Photo Ephemeris | Meeus elements | USNO to 2034, then NASA polynomials | $959.95''$ in the simulator only | Kaguya/Herald in the simulator, smooth Moon for contacts | none stated | [@val-photoephemeris-technote] [@val-photoephemeris-verification] |
| timeanddate.com | not found | not found | not found | not found | not found | [@val-besselian-maps-accuracy] |

timeanddate's method page could not be read (HTTP 403 on every attempt). Its only documented number here is the 65 s Stephenville prediction, which places it with the smooth-Moon, standard-radius group [@val-besselian-maps-accuracy].

## 2017: SVS versus Espenak versus Jubier

Wright's 2017 map computed the umbra at one-second intervals as polygons with roughly 100 m precision and the path at 250 m precision, from DE421 positions, LRO laser altimetry and Kaguya stereo topography, and SRTM elevations [@val-svs-4518]. The companion page states that the higher elevations of the western states shifted the umbra toward the south-east, in the direction of the Sun's azimuth, by as much as 3 km, and that the true umbra is an irregular polygon whose every edge corresponds to one limb valley [@val-svs-4517]. NASA's press release gave the timing effect as "several seconds" [@val-nasa-2017-lro-path]. A search-engine summary of NASA coverage stated that the SVS lunar radius was slightly larger than Espenak's and slightly smaller than the Astronomical Almanac's. That sentence was not found in any page read here and is recorded as unverified.

Espenak's 2017 interactive map states that it does not include the limb profile. It states that limb corrections may shift the limits north or south by 1 to 3 km and change durations by 1 to 3 s, and that the location of greatest duration may move by 10 to 20 km. It gives the limb-corrected greatest duration as 2m41.7s against the smooth-Moon 2m40.2s [@val-gsfc-2017-google]. So the two NASA products differed by design in exactly the terms the press described as a "shifted path". The two used the same solar radius, so the difference was terrain plus limb, of order 1 to 3 km at the limits.

Jubier's map applied Espenak's elements with [?limb-correction|limb corrections] and offered a terrain-elevation click, and warned that the corrected duration is shown only inside the path and that the correction can be "a few seconds" [@val-jubier-map-help] [@val-jubier-calc-instr]. Jubier's product therefore sat between the two NASA ones in 2017.

Wright and Young's abstract summarises the general size of the effects. Ignoring the terrain of both bodies "introduces errors on the order of kilometers in the ground track of the umbra and seconds in the duration and contact times of totality". The elevation shift is roughly $h \cot a$, where $h$ is the elevation and $a$ is the Sun's altitude [@val-wright-young-2024]. The 2001 NASA bulletin gave the same rule as an "Elev Fact" factor $\tan(90^{\circ} - A)\,\sin D$, where $A$ is the Sun's altitude and $D$ the difference between the Sun's azimuth and the limit line's azimuth, so 1000 m of elevation with a factor of 0.20 shifts the limit 200 m [@val-tp2001-bulletin].

## 2024: the radius controversy

Irwin's map for 2024 April 8 drew true-limb limits in orange with 1-sigma error lines and the smooth limits in red, using $959.95''$ [@val-besselian-path-2024]. Wright and Young describe the effect as shifting the northern limit "to the southeast by several city blocks compared to maps calculated with the conventional radius", and record that dozens of journalists asked whether NASA would revise its map [@val-wright-young-2024]. EarthSky put the shift at about 2,000 feet (610 m) on most of both edges [@val-earthsky-2024-edges]. The arithmetic supports this: $0.32''$ at the Moon's mean distance is 0.60 km, and more where the shadow cone meets the ground obliquely.

Dunham's comparison of the two edge products is the most precise available. On Jubier's map, a point exactly on Irwin's northern limit shows 13 s of limb-corrected totality. Jubier's corrected duration reaches zero about 0.7 km farther north-west [@val-dunham-iota-2024]. Both use LRO-class limb data, so the 0.7 km is the radius difference plus any terrain and implementation differences. Dunham also expected Jubier's corrected durations near the limits to be up to 10 s longer than reality [@val-dunham-iota-2024], which the Stephenville measurement confirmed: Jubier corrected 24.5 s, Irwin 12.9 s, observed 13.7 s [@val-besselian-maps-accuracy].

NASA's 2024 SVS map continued with LOLA, SRTM and the DE421 its product pages name [@val-svs-5123] [@val-svs-5219], and Wright and Young's paper, published after the eclipse, treats the radius as an open standardisation problem and lists the four modern determinations without adopting one [@val-wright-young-2024]. The NASA eclipse site's interactive map for 2024 was produced with the Five Millennium Canon machinery and carries the same 1 to 3 km caveat. Its stated inputs are the "VSOP87/ELP2000-85" label the page prints, $\Delta T$ = 70.6 s and no limb [@val-gsfc-2024-google].

## Solar radius choices in one table

The measurements themselves, their papers and the two-mode default are in [solar radius values](../06-solar-radius/solar-radius-values.md). This table keeps only which predictor adopts which value.

| Value at 1 au | Who uses it | Origin |
|---|---|---|
| $959.22''$ (695,700 km) | nobody for eclipses | IAU 2015 nominal, helioseismic, "conversion factors only" [@val-wright-young-2024] [@val-guhl-2023] |
| $959.63''$ (696,000 km) | the NASA eclipse site, EclipseWise, SVS, Jubier maps, Solar Eclipse Maestro, USNO, Stellarium, Occult default, IOTA/ES reductions | Auwers 1891 [@val-quaglia-2021] [@val-usno-2024] [@val-stellarium-code] |
| $959.95'' \pm 0.05''$ | Besselian Elements, Photo Ephemeris simulator | Quaglia et al. 2021 [@val-quaglia-2021] [@val-photoephemeris-technote] |
| $959.98'' \pm 0.02''$ | quoted by Jubier as the true value | Jubier et al. 2021 [@val-jubier-map-help] [@val-wright-young-2024] |
| $959.99'' \pm 0.06''$ | none as a default | Lamy et al. 2015 [@val-lamy-2015] |
| $960.01'' \pm 0.12''$ | Photo Ephemeris option | Guhl 2023 [@val-guhl-2023] [@val-photoephemeris-verification] |

## Lunar radius choices

The history of the two $k$ values, and which table prints which, is in [Besselian elements](../01-foundations/besselian-elements.md). This section keeps the per-predictor choices. Espenak uses $k = 0.272281$ for the umbra and $0.2725076$ for the penumbra, and states that the smaller value "results in a better approximation of Moon's minimum diameter and a slightly shorter total or longer annular eclipse" [@val-gsfc-sepredictions] [@val-eclipsewise-2024-prime]. The 1992 Explanatory Supplement explains that before 1982 a smaller $k$ was used solely for central-line durations as an approximate limb correction, that the IAU adopted $0.2725076$ in 1982, and that it was then "agreed implicitly that limb effects are no longer accounted for, but are averaged" [@val-es1992]. USNO uses 1737.4 km [@val-usno-2024], Stellarium carries both constants with a comment crediting Espenak [@val-stellarium-code], and Solar Eclipse Maestro uses 1738.091 km ($k = 0.2725076$) as the datum for its profiles [@val-jubier-sem-limb].

The size of this choice, by arithmetic from the constants: $\Delta k = 0.2725076 - 0.272281 = 0.0002266$ Earth radii, which is 1.445 km of lunar radius, $0.78''$ at the Moon's mean distance, and about 1.4 km at each umbral limit or 2.9 km of path width. USNO's 1737.4 km sits 0.75 km above Espenak's umbral radius and 0.69 km below the IAU datum. Any product that uses a true limb profile makes the choice irrelevant, because the profile replaces the sphere.

## ΔT choices

| Product | 2017 value | 2024 value |
|---|---|---|
| NASA eclipse site interactive map | 68.4 s [@val-gsfc-2017-google] | 70.6 s [@val-gsfc-2024-google] |
| EclipseWise prime page | 68.8 s [@val-eclipsewise-2017-prime] | 71.5 s [@val-eclipsewise-2024-prime] |
| EclipseWise circumstances | not read | 71.3 s [@val-eclipsewise-2024-circ] |
| "NASA" value cited by Photo Ephemeris | 70.3 s [@val-photoephemeris-technote] | not stated |
| Espenak 1987 Fifty Year Canon, reported secondhand by timeanddate | not stated | 85.7 s [@val-timeanddate-sanantonio] |
| Measured (USNO) | 68.8373 s on 2017 Aug 1 | 69.1983 s on 2024 Apr 1 [@val-usno-deltat-data] |

Jubier's help states that the extrapolated $\Delta T$ "should be good to better than 0.5 seconds" [@val-jubier-map-help]. The Besselian Elements team states that [?eop|EOP] are the only inputs that change in practice and quotes final 2026 August 12 values of dUT1 = +0.03 s and $\Delta T$ = +69.15 s [@val-besselian-updates]. The Five Millennium Canon states the conversion: 240 s of $\Delta T$ shifts a path one degree of longitude, eastward for positive $\Delta T$ [@val-5mcse-tp2009]. One second is therefore $15.041''$ of longitude at the sidereal rate, 465 m at the equator and 356 m at $40^{\circ}$ latitude, east-west. The across-track component is that number times the sine of the angle between the path and the parallel. For 2024, the NASA eclipse site map's 1.4 s excess is about 500 m east-west and the EclipseWise circumstances page's 2.3 s excess about 800 m, both smaller than the 610 m radius effect only at low latitude and only after projection across the track. The 16.5 s error of the 1987 canon would be about 6 km.

## Implementation differences at identical inputs

At the Vale 2017 site with $s_0 = 959.63''$, Irwin's model gave a duration of 32.6 s, Occult's Baily's beads tool 2 s or more longer, and Solar Eclipse Maestro 4 s or more longer. In radius terms Occult would infer $0.03''$ more and Solar Eclipse Maestro $0.07''$ more than Irwin's model for the same observed duration, and neither application reproduces the bend at $960.15''$ where third contact moves to another valley [@val-quaglia-2021]. This is the only published three-way comparison at fixed inputs. Possible causes named or implied in that paper are the limb-profile resolution, the treatment of the observer's height, and the definition of contact against a profile. Wright and Young note that a limb array of 18,000 elements has a resolution of $0.02^{\circ}$, roughly 600 m on the Moon, and that too coarse an array misses small valleys [@val-wright-young-2024]. Photo Ephemeris states that the Kaguya/Herald data it uses has 1800 points at $0.2^{\circ}$ spacing [@val-photoephemeris-verification], ten times coarser.

Besselian Elements has also shown that true-limb limits are jagged rather than smooth, following terrain and limb valleys, and that near Elorrio, Spain, for 2026 August 12 they lie at times more than 1 km from Jubier's smooth limit [@val-besselian-jagged].

## Stated accuracies, product by product

- **Espenak, the NASA eclipse site.** "All eclipse calculations are by Fred Espenak, and he assumes full responsibility for their accuracy." Limits may move 1 to 3 km and durations 1 to 3 s with the limb profile. The point of greatest duration may move 10 to 20 km [@val-gsfc-2017-google] [@val-gsfc-2024-google] [@val-gsfc-sepredictions]. The Canon states the lunar ephemeris is accurate to better than an arcsecond within several centuries and that $\Delta T$ dominates path error in the past [@val-5mcse-tp2009]. The 2001 bulletin states [?graze-zone] predictions are accurate to $\pm 0.3''$ given the Watts data and advises observers to stay at least 1 km inside the interior limits [@val-tp2001-bulletin].
- **NASA SVS.** Umbra shapes at roughly 100 m precision, path at 250 m [@val-svs-4518]. The paper gives no formal error, but states the terrain rule $h \cot a$ and the 600 m limb-element resolution [@val-wright-young-2024].
- **Jubier.** Limb corrections change totality by "a few seconds", refraction is not applied, $\Delta T$ is good to better than 0.5 s, and the radius used is $959.63''$ against a true value near $959.98''$ [@val-jubier-map-help].
- **Besselian Elements.** Radius $959.95'' \pm 0.05''$, limits drawn with 1-sigma lines that Dunham read as under 90 m, and a stated experimental confirmation to about 1 s at Stephenville [@val-besselian-solar-radius] [@val-dunham-iota-2024] [@val-besselian-maps-accuracy].
- **USNO.** No accuracy statement. IAU radii, no limb, no centre-of-figure correction, contacts by iteration of topocentric positions [@val-usno-2024].
- **Occult.** No accuracy statement on the program page [@val-occult-page]. Its bead tool is the reduction standard of IOTA/ES [@val-guhl-tegtmeier-2018] [@val-guhl-2023].
- **Stellarium.** No accuracy statement in the release notes. Version 0.22.0 added the Eclipse Finder and 1.0 added global contact times and KML maps [@val-stellarium-changelog]. The code stops iterating a contact when the correction is under 0.1 s [@val-stellarium-code].
- **Photo Ephemeris.** "Contact times are calculated assuming a smooth spherical Moon. No correction is made for the lunar limb profile, which typically affects the timing of C2 and C3 by a few seconds, but up to ~15 s in extreme cases." It refers users to Jubier, Espenak and IOTA software for edge planning [@val-photoephemeris-technote].
- **timeanddate.** No statement found.

## Sources compared

| Source | What it contributes that others do not |
|---|---|
| Besselian Elements accuracy test [@val-besselian-maps-accuracy] | Six products at one point with an observed value |
| Dunham 2024 [@val-dunham-iota-2024] | The 0.7 km Jubier-to-Irwin offset and the 2 km margin |
| Wright and Young 2024 [@val-wright-young-2024] | SVS inputs, terrain rule, radius survey, and the account of the 2024 controversy |
| Quaglia et al. 2021 [@val-quaglia-2021] | Irwin versus Occult versus Solar Eclipse Maestro at fixed inputs |
| NASA eclipse site map pages [@val-gsfc-2017-google] [@val-gsfc-2024-google] | Espenak's own 1 to 3 km and 1 to 3 s caveats and his $\Delta T$ values |
| EclipseWise pages [@val-eclipsewise-2017-prime] [@val-eclipsewise-2024-prime] [@val-eclipsewise-2024-circ] | DE405/DE406, $k$ values, $\Delta T$ 68.8 s and 71.3 to 71.5 s |
| USNO [@val-usno-2024] | The one official product that states it applies no limb or centre-of-figure correction |
| Explanatory Supplement 1992 [@val-es1992] | Why two $k$ values exist |
| Photo Ephemeris [@val-photoephemeris-technote] | The 15 s extreme limb figure and the $\Delta T$ revision from 70.3 s to 68.8373 s |
| Stellarium code [@val-stellarium-code] | Constants and convergence criterion of an open-source implementation |

## What a developer should do

1. Treat the differences as parameter choices, not bugs, and make each one explicit in the output: ephemeris version, $\Delta T$ value and source date, $s_0$, $k$ or profile source, terrain source, refraction on or off.
2. For reproducing NASA and EclipseWise tables, set $s_0 = 959.63''$, $k = 0.272281$ for the umbra, no limb, no terrain, and the page's $\Delta T$. Agreement should be within 0.1 s for contacts and within the map precision for limits.
3. For edge products, use a LOLA-derived profile with at least 18,000 elements, terrain, and $s_0$ near $959.95''$, then check against Stephenville (13.7 s) and the Vale site (Irwin 32.6 s at $959.63''$).
4. Update $\Delta T$ from USNO or IERS bulletins until the eclipse and record the value used. The realised 2024 errors of published predictions were 1.4 to 2.3 s.
5. Read in this order: Wright and Young 2024 sections 3 to 6, Quaglia et al. 2021 section 4 and appendix, the NASA eclipse site's 2024 map page notes, Dunham's 2024 page.

## What this changes

The pipeline needs a configuration record that travels with every product so that two runs can be compared term by term. The path-edge product must be a separate mode from the almanac-reproduction mode, because their constants differ by design. Nothing changes in the Besselian core.

## Open questions

- Obtain timeanddate's method description, or an email from the site, to learn its ephemeris, $\Delta T$, radius and limb treatment.
- Obtain the parameter table image from the Besselian Elements technical page, which was not extracted, to record Irwin's ephemeris version, EOP source and DEM resolutions [@val-besselian-technical].
- Obtain Occult's help file text on the Baily's beads tool, to learn its profile resolution and contact definition, which would explain the 2 s offset from Irwin's model.
- Obtain the Solar Eclipse Maestro documentation on how observer height and the limb profile enter the contact solution, to explain the 4 s offset.
- Verify or discard the search-summary sentence about the SVS lunar radius relative to Espenak's and the Almanac's by locating the NASA or USRA page that contains it.
