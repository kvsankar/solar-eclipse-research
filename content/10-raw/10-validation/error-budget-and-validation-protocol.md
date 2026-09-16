---
title: Error budget and validation protocol
description: The contribution of each input to the error of a modern eclipse prediction, in seconds of contact time and metres of path edge, the record of ΔT model validation, and a test protocol with reference cases and tolerances for a new implementation.
order: 3
status: working
updated: 2026-09-15
tags: [validation, error-budget, delta-t, solar-radius, limb, terrain, protocol]
---

::: summary
- **Nobody has published a complete error budget.** Quaglia et al. state the accuracy of the ephemeris, Earth orientation and lunar topography inputs and conclude the solar radius is the only term that matters [@val-quaglia-2021]. Espenak states the limb and $\Delta T$ terms [@val-gsfc-2024-google] [@val-gsfc-uncertainty]. Wright and Young state the terrain rule [@val-wright-young-2024]. The table below assembles them.
- **For a present-day eclipse the budget is dominated by three terms of 0.6 to 3 km each at the edge.** Solar radius, 0.32 arcseconds or 600 m. The lunar limb if omitted, 1 to 3 km. Terrain if omitted, $h \cot a$ and up to 3 km. Everything else is below 100 m and 0.5 s once $\Delta T$ is refreshed, the umbral $k$ or a profile is used, and the profile is referenced to the centre of mass. The ephemeris is under 1 m [@val-quaglia-2021] [@val-gsfc-2024-google] [@val-svs-4517].
- **At the central line the same terms are seconds, not tens of seconds.** Radius 1.6 to 1.8 s, limb 1 to 3 s and up to 15 s in extreme geometry, $\Delta T$ realised errors 0.4 to 2.3 s in 2017 and 2024 [@val-quaglia-2021] [@val-photoephemeris-technote] [@val-usno-deltat-data].
- **ΔT model errors grow as the square of the distance from the present.** Morrison and Stephenson's rule $\sigma = 0.8\,t^2$ s with $t$ in centuries from 1820 gives 265 s at year 0 and 54 s at 1000, and Huber's model gives 1885 s at 3000 [@val-gsfc-uncertainty]. Total-eclipse records pin the rotational frame only to the width of the band, "a few minutes of time" [@val-stephenson-2016].
- **Successive ΔT analyses differ by more than their quoted sigmas.** The 1986 and 1997 Stephenson curves differ by 1294 s at AD 300, and 2026 work on Ming records bounds 1542 to $-328$ s $\le \Delta T \le 332$ s [@val-gsfc-deltat-hist] [@val-hayakawa-2026-china].
- **A validation protocol exists in pieces.** Hand-checkable examples in the 1961 Explanatory Supplement, the Lusaka limb-correction example in the 2001 NASA bulletin, the Vale and Stephenville edge records, and the IOTA/ES bead tables give reference cases at every level from Besselian elements to bead events [@val-es1961] [@val-tp2001-bulletin] [@val-quaglia-2021] [@val-besselian-maps-accuracy] [@val-guhl-tegtmeier-2018].
:::

**The question.** For a modern total eclipse, how many seconds of contact time and how many metres of path edge does each input contribute at a mid-path site and at the edge, who has published those numbers, and what tests with what tolerances would show that a new implementation is right?

## The budget

This table is the home of the sourced raw rows. The ranked version, which orders the same terms by size, is in [error budget](../../20-reports/error-budget.md). The table combines published statements with arithmetic from published constants. Rows marked "arithmetic" are this note's own conversions and are explained below the table. "Mid-path" means a site near the central line of a 2017-class eclipse with a shadow speed near 1 km/s. "Edge" means within a few hundred metres of a limit. The edge column is in metres of limit position or, where the source gives it, seconds of duration.

| Term | Mid-path contact time | Edge position or duration | Source |
|---|---|---|---|
| Lunar ephemeris (DE430 to DE440) | negligible, lunar distance residuals under 1 m against laser ranging | negligible | [@val-quaglia-2021] |
| Solar and Earth ephemeris | negligible at the present epoch, lunar position "better than an arcsecond within several centuries" | negligible | [@val-5mcse-tp2009] |
| Earth orientation (precession, nutation, polar motion), measured | under 1 mas, under 0.1 m on the ground | same | [@val-quaglia-2021] |
| UT1, measured after the fact | well under 1 ms, under 0.5 m | same | [@val-quaglia-2021] |
| $\Delta T$ prediction error, realised, 2017 | $-0.4$ s (the NASA eclipse site map at eclipse.gsfc.nasa.gov, 68.4 s against 68.84 s), $-0.04$ s (EclipseWise 68.8 s) | 150 m east-west at $40^{\circ}$ for 0.4 s, arithmetic | [@val-gsfc-2017-google] [@val-eclipsewise-2017-prime] [@val-usno-deltat-data] |
| $\Delta T$ prediction error, realised, 2024 | +1.4 s (NASA eclipse site map 70.6 s), +2.1 to +2.3 s (EclipseWise 71.3 to 71.5 s) against 69.20 s | 500 to 800 m east-west at $40^{\circ}$, arithmetic; 16.5 s for the 1987 canon, about 6 km | [@val-gsfc-2024-google] [@val-eclipsewise-2024-circ] [@val-usno-deltat-data] [@val-timeanddate-sanantonio] |
| $\Delta T$ prediction error, claimed a priori | under 0.5 s | under 180 m, arithmetic | [@val-jubier-map-help] |
| Solar radius, $959.63''$ versus $959.95''$ | 1.6 s of central-line duration (2017), 1.8 s for $960.00''$ | 600 m per limit, 19.3 s of duration a few hundred metres inside the Vale limit, 11 s at Stephenville | [@val-quaglia-2021] [@val-earthsky-2024-edges] [@val-besselian-maps-accuracy] |
| Solar radius, residual uncertainty $\pm 0.05''$ | 0.1 s | 100 m band | [@val-quaglia-2021] |
| Lunar limb profile, omitted | 1 to 3 s per Espenak, up to 2 s per contact per the Explanatory Supplement, up to about 15 s in extreme cases per The Photographer's Ephemeris (Photo Ephemeris) | 1 to 3 km per limit, 33 s of duration at Stephenville | [@val-gsfc-2024-google] [@val-es1992] [@val-photoephemeris-technote] [@val-besselian-maps-accuracy] |
| Lunar limb profile, Watts era | systematic errors reaching $0.4''$ at some position angles, predictions $\pm 0.3''$ | 600 to 750 m | [@val-tp2001-bulletin] |
| Lunar limb profile, LOLA era | topography better than 10 m, about 5 mas | under 20 m | [@val-quaglia-2021] |
| Limb sampling resolution | 18,000 elements at $0.02^{\circ}$ is 600 m on the Moon, coarser arrays miss valleys | not quantified, part of the 2 to 4 s implementation spread | [@val-wright-young-2024] [@val-quaglia-2021] |
| Centre of figure versus centre of mass | folded into any DEM tied to the DE421 mean-Earth frame, not applied by USNO, and the Watts datum was displaced. Up to 1.4 s of duration, derived in [lunar figure and libration](../08-lunar-and-solar-model/lunar-figure-and-libration.md) | 0.9 km, rising to 2.7 s and 1.9 km if the whole 1.935 km offset lay in the sky plane | [@moon-jones-2025] [@val-wright-young-2024] [@val-usno-2024] [@val-tp2001-bulletin] |
| Lunar radius constant $k$ (smooth-Moon products only) | $\Delta k = 0.0002266$ is 1.445 km of lunar radius, about 4 s of central duration (4.3 s by this arithmetic, and EclipseWise's 2017 Illinois comparison gives 4.0 s) | about 1.4 km per limit, arithmetic | [@val-gsfc-sepredictions] [@val-es1992] |
| Earth ellipsoid versus geoid | EGM96 undulations of tens of metres act like elevation | $h \cot a$, tens of metres, arithmetic | [@val-wright-young-2024] |
| Terrain, omitted | seconds where the Sun's azimuth is along the track | $h \cot a$; up to 3 km in the 2017 western states; 200 m for 1000 m at Elev Fact 0.20 | [@val-wright-young-2024] [@val-svs-4517] [@val-tp2001-bulletin] |
| Refraction | not applied by Jubier; matters only near sunrise and sunset | same | [@val-jubier-map-help] |
| Observer position, consumer GPS | none on time at mid-path | $\pm 100$ m | [@val-tp2001-bulletin] |
| Observer clock, GPS-stamped video | 0.05 s per bead at 25 frames per second | same | [@val-guhl-tegtmeier-2018] |
| Observer clock, visual with UTC timer | "a couple of seconds" on a duration | same | [@val-besselian-maps-accuracy] |
| Bead reduction, filtered 8-bit video | $\pm 0.1''$ per bead, $+0.2''$ systematic if overexposed | 200 to 400 m equivalent | [@val-guhl-tegtmeier-2018] |
| Implementation, same inputs | 2 s (Occult) to 4 s (Solar Eclipse Maestro) longer than Irwin's model at Vale | $0.03''$ to $0.07''$ of radius, 60 to 130 m | [@val-quaglia-2021] |

Arithmetic used. One arcsecond at the Moon's mean distance of 384,400 km is 1.864 km, so $0.32''$ is 0.60 km. One second of $\Delta T$ is $15.041''$ of longitude at the sidereal rate, which is 465 m at the equator and 356 m at $40^{\circ}$ latitude. The Five Millennium Canon, NASA/TP-2006-214141, states the same rule as 240 s per degree [@val-5mcse-tp2009]. The $k$ difference is $0.2725076 - 0.272281$ Earth radii of 6378.137 km [@val-gsfc-sepredictions] [@val-es1992]. The terrain shift is $h \cot a$ [@val-wright-young-2024].

The pattern is that a smooth-Moon, standard-radius, sea-level prediction carries three independent errors of 0.6 to 3 km at the limits, and a true-limb, terrain-corrected prediction with $s_0$ near $959.95''$ carries a residual of about 100 m from the radius uncertainty plus an implementation spread worth 60 to 130 m. Quaglia et al. put the residual as "fuzzy bands 100 m wide" [@val-quaglia-2021]. Dunham's practical margin of 2.0 km of umbral depth covers the instrumental sensitivity to faint beads that no computation can remove [@val-dunham-iota-2024].

## Who has published budgets

- Quaglia et al. 2021, section 1, states the accuracy of DE440, of the ITRS-GCRS orientation, of UT1 and of LOLA topography and concludes that "the solar radius is the most uncertain parameter of all these quantities" [@val-quaglia-2021].
- Espenak's map pages state the limb term for limits, durations and greatest-duration location, and the Canon states the ephemeris and $\Delta T$ terms with tables of $\sigma$ against year [@val-gsfc-2024-google] [@val-5mcse-tp2009] [@val-gsfc-uncertainty].
- The 2001 bulletin states the Watts-era limb term, the graze-zone accuracy, the terrain factor and the GPS term [@val-tp2001-bulletin].
- The 1992 Explanatory Supplement states the limb term for central-line contacts and refers to Herald 1983 for "the total effect and its components" [@val-es1992] [@val-herald-1983].
- Wright and Young state the terrain rule and the limb sampling requirement [@val-wright-young-2024].
- Dunham states the observational margin [@val-dunham-iota-2024].
- No SVS page, no Sigismondi paper and no Herald document read here gives a full table. Herald 1983 is the one artefact that may.

## Validation of ΔT models against historical eclipses

Stephenson, Morrison and Hohenkerk analysed 180 timed Babylonian eclipse observations from $-720$ to $-9$, 111 timed Chinese observations from 434 to 1280, 11 Greek and 54 Arab timings. They added a set of untimed total and annular eclipses from $-708$ to 1567 and about half a million telescopic lunar occultations from 1623 onward [@val-stephenson-2016]. The scatter of the timed records is 16 minutes for Babylonian observations after $-560$, 20 and 16 minutes for Chinese solar and lunar timings, about 14 minutes for Greek, and 5 and 13 minutes for Arab solar and lunar timings [@val-stephenson-2016]. Untimed records constrain differently: "a report that an eclipse was total or near-total at a known place fixes the rotational frame of the Earth to within the projected width of the band of totality parallel to the Earth's equator. This width is usually only a few minutes of time" [@val-stephenson-2016]. The long-term fit is

$$\Delta T = -320.0 + (32.5 \pm 0.6)\left(\frac{\text{year} - 1825}{100}\right)^2 \text{ s},$$

corresponding to a length-of-day increase of $+1.78 \pm 0.03$ ms per century, against $+2.3 \pm 0.1$ ms per century expected from tidal friction alone [@val-stephenson-2016]. The 2021 addendum extends the spline fits to 2025 and tabulates uncertainties in HMNAO Table S15.2020. It was not readable at the time of writing (2026 September) and is known only through the ytliu0 implementation and later citations [@val-morrison-2021] [@val-ytliu-deltat].

Espenak's uncertainty page gives the Morrison and Stephenson 2004 rule $\sigma = 0.8\,t^2$ s with $t = (\text{year} - 1820)/100$, valid from $-1000$ to 1200. Decade fluctuations give about 20 s from 1300 to 1600. The telescopic era gives 5 s at 1700, 1 s at 1800 and 0.1 s at 1900. Huber's Brownian-motion model covers the years outside the record [@val-gsfc-uncertainty]. The tabulated values are:

| Year | $\sigma(\Delta T)$ | Longitude |
|---|---|---|
| $-4000$ | 16,291 s (Huber) | $67.9^{\circ}$ |
| $-1000$ | 636 s | $2.65^{\circ}$ |
| $-500$ | 431 s | $1.79^{\circ}$ |
| 0 | 265 s | $1.10^{\circ}$ |
| 500 | 139 s | $0.58^{\circ}$ |
| 1000 | 54 s | $0.22^{\circ}$ |
| 1200 | 31 s | $0.13^{\circ}$ |
| 1700 | 5 s | $0.021^{\circ}$ |
| 1800 | 1 s | $0.004^{\circ}$ |
| 1900 | 0.1 s | $0.0004^{\circ}$ |
| 2500 | 612 s (Huber) | $2.6^{\circ}$ |
| 3000 | 1885 s (Huber) | $7.9^{\circ}$ |

Source: [@val-gsfc-uncertainty]. The Canon draws reference gores on every map whose $\sigma$ exceeds 265 s, which is every year before 1 and after 2300, and for $-1996$ shows the gore at $\pm 15.5^{\circ}$ of longitude for $\sigma = 3712$ s [@val-5mcse-tp2009].

Two checks show what these sigmas mean in practice. Espenak's table of Stephenson and Houlden 1986 against Stephenson 1997 values differs by 644 s at $-500$, $-752$ s at 0, $-1294$ s at 300 and 210 s at 1300 [@val-gsfc-deltat-hist], differences larger than the $\sigma$ rule at the same dates. Hayakawa et al. derived from Ming-dynasty records the bounds $-408 \le \Delta T \le 601$ s at 1361, $277 \le \Delta T \le 890$ s at 1514, $-328 \le \Delta T \le 332$ s at 1542 and $-1762 \le \Delta T \le 1091$ s at 1575. They state that these tighten the variations relative to the Morrison 2021 spline and require adjustments around 1361 and 1542 [@val-hayakawa-2026-china]. The lesson for a developer is that a past-eclipse product must carry the $\sigma$ and should draw it, as the Canon does.

For the present, the [?delta-t-realised|realised errors] are small. The measured values are 68.8373 s on 2017 August 1 and 69.1983 s on 2024 April 1 [@val-usno-deltat-data]. The 2017 predictions were within 0.4 s. The 2024 predictions made from the 2010s were 1.4 to 2.3 s high, because Earth's rotation sped up after 2016 and the extrapolations assumed continued slowing [@val-gsfc-2024-google] [@val-eclipsewise-2024-circ]. The Besselian Elements team frames the general rule: ephemerides, topography and the radius are fixed inputs, [?eop|EOP] are the only inputs that must be re-fetched, and $\Delta T = 32.184\text{ s} + \text{leap seconds} - \text{dUT1}$ [@val-besselian-updates].

## Accuracy statements by the predictors

Collected in the predictor-disagreements note and repeated here in one line each. Espenak: limits 1 to 3 km and durations 1 to 3 s from the limb, greatest-duration point 10 to 20 km, and full personal responsibility [@val-gsfc-2024-google] [@val-gsfc-sepredictions]. SVS: 100 m umbra shapes, 250 m path [@val-svs-4518]. Jubier: limb correction a few seconds, $\Delta T$ better than 0.5 s, refraction omitted [@val-jubier-map-help]. Besselian Elements: $959.95'' \pm 0.05''$, 1-sigma limit lines [@val-besselian-solar-radius] [@val-besselian-path-2024]. USNO: no limb, no centre-of-figure correction [@val-usno-2024]. Photo Ephemeris: smooth Moon, a few seconds and up to 15 s [@val-photoephemeris-technote]. Stellarium: 0.1 s iteration tolerance and no other statement [@val-stellarium-code] [@val-stellarium-changelog]. Occult and timeanddate: none found [@val-occult-page] [@val-besselian-maps-accuracy].

## Validation protocol for a new implementation

The protocol has five levels. Each level names a [?reference-case], the quantity compared, and a tolerance derived from the budget above. Times are given in the scale each source prints. [?tt|TT] appears as TDT or TD in NASA and EclipseWise tables and as ET before 1984. Times labelled UT are UT1 as published, observed times are UTC, and the difference is under 0.9 s and below every tolerance here.

### Level 1: Besselian elements and global circumstances

- Reproduce the 1961 Explanatory Supplement worked examples 9.2 to 9.9 for the eclipse of 1961 February 15: test for occurrence, Besselian and auxiliary elements, a point on the central line and its duration, and outline curves [@val-es1961]. These are hand calculations from tabulated elements, so agreement is to the last printed digit once the same elements are input.
- Reproduce EclipseWise's 2017 August 21 greatest eclipse at 18:26:40.3 TD, path width 114.7 km, central duration 02m40.12s, with DE405, $\Delta T = 68.8$ s, $k = 0.2725076$ and $0.2722810$ [@val-eclipsewise-2017-prime]. Tolerance: 0.1 s in time, 0.1 km in width.
- Reproduce the NASA eclipse site's 2024 greatest duration of 04m28.2s with the "VSOP87/ELP2000-85" the page names and $\Delta T = 70.6$ s, or the 2017 value of 2m40.2s with DE405 and 68.4 s [@val-gsfc-2024-google] [@val-gsfc-2017-google]. Tolerance: 0.2 s, since the ephemerides differ.

### Level 2: Local circumstances, smooth Moon

- The 2001 June 21 Lusaka case from the NASA bulletin with DE200/LE200: C2 13:09:19.3 UT at $P_2 = 118^{\circ}$, C3 13:12:32.8 UT at $P_3 = 247^{\circ}$ [@val-tp2001-bulletin]. $P$ is the [?position-angle-p|position angle] of the contact measured eastward from north, which the 1961 Supplement writes $Q$. Tolerance: 0.5 s, allowing for the ephemeris difference between DE200 and a modern DE.
- USNO's 2024 Solar Eclipse Computer, run for any city with height entered, as the check of a smooth-Moon solution using 696,000 km and 1737.4 km with no centre-of-figure correction [@val-usno-2024]. Tolerance: 0.5 s after matching $\Delta T$.
- Stellarium's AstroCalc contact times for the same sites, with the knowledge that it uses $959.63''$ and iterates to 0.1 s [@val-stellarium-code]. Tolerance: 0.5 s.

### Level 3: Limb corrections

- The Lusaka example: the bulletin's chart corrections of $+4.0$ s at C2 and $-1.2$ s at C3 give 13:09:23.3 and 13:12:31.6 UT, and the bulletin states these are within 0.2 s of a rigorous calculation with the actual limb profile [@val-tp2001-bulletin]. A LOLA-based implementation should land within 1 s of the corrected values, the difference being Watts against LOLA.
- Jubier's LC column at any site, read from the interactive map, as a second opinion [@val-jubier-map-help]. Tolerance: 1 s.

### Level 4: Edge sites against observation

- Vale, Oregon, 2017: $117^{\circ} 13' 09.8''$ W, $43^{\circ} 57' 10.9''$ N, 711 m. With $s_0 = 959.63''$ the reference contacts are 17:25:34.3 and 17:26:06.9 UTC, 32.6 s. Occult gives 2 s or more longer and Solar Eclipse Maestro 4 s or more. The limit distance should fall from 1200 m to under 400 m when $s_0$ is raised to $960.00''$, and the duration-versus-radius curve should bend at $960.15''$ [@val-quaglia-2021]. Tolerance: 2 s of duration and 100 m of limit distance.
- Stephenville, Texas, 2024: observed C2 18:39:06.6, C3 18:39:20.3 UTC, 13.7 s, error about 2 s [@val-besselian-maps-accuracy]. With a true limb, terrain and $959.95''$ the tolerance is 3 s. With $959.63''$ and a true limb the expected result is about 24 s. That run serves as a negative control.
- Cape Range, 2023 April 20, Site 1 of Quaglia et al.: totality should reach zero at $s_0 = 960.28''$ and the observed contacts support $959.90'' < s_0 < 960.02''$ [@val-quaglia-2023-joa].

### Level 5: Bead events

- Guhl and Tegtmeier's Table 1 for 2017USN1 at Thermopolis, Wyoming, 16 events from 17:39:59.9 to 17:40:42.9 UTC with axis angles [@val-guhl-tegtmeier-2018], and Guhl's Table 1 for 2023AUN1 with 16 events from 03:28:52.7 to 03:30:05.7 UTC [@val-guhl-2023]. A bead simulator with LOLA should reproduce each event's axis angle and time to within 1 s when run with the radius correction each paper derived, $+0.03''$ and $+0.38''$ respectively. Per-bead scatter of $\pm 0.1''$ is the floor.
- Photo Ephemeris lists eight sites across 2017 (Madras, Warrensburg), 2019 (Cerro Tololo) and 2023 (Bisti Badlands, Mentmore, Lamesa, Grand Vista Overlook, Kirtland, Kailis, Ned's Camp) for which it compared its simulation with recordings, but publishes no residuals [@val-photoephemeris-verification]. The site list is a starting point for obtaining videos.

### Data sets to obtain

USNO deltat.data and IERS bulletins for $\Delta T$ and polar motion [@val-usno-deltat-data] [@val-besselian-updates]. The LOLA LDEM and SLDEM2015 grids [@val-wright-young-2024]. The Journal for Occultation Astronomy issues 2018-3 and 2023-4 for bead tables [@val-guhl-tegtmeier-2018] [@val-guhl-2023]. Quaglia et al.'s flash-spectrum video, which the paper says is available on request [@val-quaglia-2021]. Dunham's 2023 and 2024 bead videos, linked from IOTA's graze pages [@val-dunham-nam23grz] [@val-dunham-iota-2024].

## Sources compared

| Source | Budget terms it provides | Reference cases it provides |
|---|---|---|
| Quaglia et al. 2021 [@val-quaglia-2021] | ephemeris, EOP, UT1, topography, radius sensitivity, implementation spread | Vale contacts and sensitivity curves |
| Espenak's NASA eclipse site and the Canon [@val-gsfc-2024-google] [@val-5mcse-tp2009] [@val-gsfc-uncertainty] | limb, $\Delta T$ sigma by year, ephemeris | greatest duration values with stated inputs |
| NASA 2001 bulletin [@val-tp2001-bulletin] | Watts limb error, terrain factor, GPS | Lusaka contacts and limb corrections |
| Explanatory Supplements [@val-es1992] [@val-es1961] | limb per contact, $k$ history | 1961 worked examples |
| Wright and Young 2024 [@val-wright-young-2024] | terrain rule, limb sampling | none |
| Stephenson et al. 2016 [@val-stephenson-2016] | $\Delta T$ record scatter and constraint rules | none |
| Besselian Elements [@val-besselian-maps-accuracy] [@val-besselian-updates] | EOP handling, visual timing error | Stephenville observation |
| IOTA/ES [@val-guhl-tegtmeier-2018] [@val-guhl-2023] | bead noise floor | bead tables |
| Dunham 2024 [@val-dunham-iota-2024] | observational margin | Solon site |

## What a developer should do

1. Implement the five-level protocol as an automated test suite, with the constants of each reference case pinned in the test and the tolerance stated beside it.
2. Emit a per-run error estimate that sums the budget rows in quadrature for the configuration actually used, and print it with the path limit as a band. A smooth-Moon run should report about 2 km at the limit. A true-limb run with $959.95''$ should report about 100 to 200 m.
3. Store $\Delta T$ with its source and date and warn when the eclipse is more than one year past the last measured value, or more than 300 years from the present, where the Canon's own maps switch to gores.
4. Read first: Quaglia et al. 2021 section 1 and section 4, Espenak's uncertainty page, Stephenson et al. 2016 section 2, and the 2001 bulletin's limb section.

## What this changes

The pipeline design gains an explicit uncertainty output and a test corpus. The solar radius moves from a constant to a configuration item with a stated uncertainty. Products for dates before 1600 or after 2300 must carry a longitude gore for the $\Delta T$ standard error. That threshold is this research's own recommendation and is stricter than the Five Millennium Canon, which draws gores only where $\sigma$ exceeds 265 s, before +0001 and after 2300. Between 1 and 1600 a product should at least print $\sigma$, which exceeds 20 s before 1600 [@val-5mcse-tp2009] [@val-gsfc-uncertainty]. Nothing else in the computational chain changes.

## Open questions

- Obtain Herald 1983, JBAA 93, 241, which the Explanatory Supplement says estimates the total limb effect and its components, so that measured components replace the derived centre-of-figure figures and the "not quantified" limb-sampling cell [@val-herald-1983].
- Obtain Morrison et al. 2021 and HMNAO Table S15.2020 to tabulate the current $\sigma(\Delta T)$ by year and replace the 2004 rule [@val-morrison-2021].
- Obtain the DE440 versus DE421 lunar position difference at the 2024 epoch, in metres, to close the ephemeris row with a number rather than "negligible".
- Obtain the per-site residuals behind Photo Ephemeris's eight-site verification, or the recordings themselves, to add bead-level cases from 2019 and 2023 October.
- Obtain Lamy et al. 2015 in full to record the limb data version and the per-site timing precision of the photometers, which would set the noise floor for a light-curve test.
