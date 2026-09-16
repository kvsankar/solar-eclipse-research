---
title: Observed versus predicted
description: Published comparisons of timed contacts and Baily's bead events with predictions, from the IOTA edge campaigns to the 2024 edge experiments, with the measured offsets in seconds and metres.
order: 1
status: working
updated: 2026-09-15
tags: [validation, bailys-beads, solar-radius, path-edge, iota]
---

::: summary
- **Every quantitative test of an eclipse prediction against observation has been made at or near a path limit.** Mid-path contact timings are too insensitive: a 0.37 arcsecond change in solar radius moves a 2017 central-line duration by 1.8 s but moves the duration a few hundred metres inside the southern limit by 19.3 s [@val-quaglia-2021].
- **Predictions that use the standard solar radius of 959.63 arcseconds place the path limit too far out by roughly 600 m.** Four independent campaigns since 2010 give an [?eclipse-solar-radius] between 959.95 and 960.01 arcseconds [@val-lamy-2015] [@val-quaglia-2021] [@val-guhl-2023] [@val-wright-young-2024]. The difference of 0.32 arcseconds at the Moon's distance is 610 m on the ground [@val-earthsky-2024-edges].
- **The cleanest 2024 edge test observed 13.7 s of totality where six public predictions said 12.9 s to 65 s.** At Stephenville, Texas, Irwin's true-limb model with the larger radius came within one second. timeanddate, eclipse2024.org and Jubier's uncorrected duration were 40 to 50 s too long [@val-besselian-maps-accuracy].
- **Bead-by-bead residuals from good video are at the 0.1 arcsecond level.** IOTA/ES reduced 16 beads from 700 m inside the 2017 northern limit to a mean radius correction of +0.03 arcseconds, with individual beads scattered between minus 0.10 and +0.14 arcseconds [@val-guhl-tegtmeier-2018].
- **IOTA has withdrawn its earlier claim of a varying solar radius.** Dunham now attributes the eclipse-to-eclipse scatter of the 1980s and 1990s campaigns to observational error larger than the formal estimates, and recommends sites at least 2.0 km inside the corrected limit [@val-dunham-iota-2024].
- **No published report from the 2023 annular edges gives an observed-minus-predicted number.** Dunham recorded about 3 minutes of beads near Mentmore, New Mexico, and the IOTA/ES station at Cape Range gave +0.38 arcseconds, but no site reported a timed offset of the antumbral limit [@val-dunham-nam23grz] [@val-guhl-2023].
- **Kentucky, Nebraska and 2017 crowd-sourced edge stations produced no usable timings.** Nugent's summary of the 2018 IOTA meeting records that too few volunteers were obtained, and Dunham notes the best amateur edge recording of 2017 was not accurately timed [@val-iota-meeting-2018] [@val-dunham-iota-2024].
:::

**The question.** When someone has stood at a known position with a GPS-stamped clock and recorded second and third contact, or the beads around them, how far were the published predictions off, in seconds of time and in metres of path edge, and which input explains the offset?

Times labelled UT below are UT1 as published, and observed times are UTC. The difference is under 0.9 s and below every tolerance quoted here.

## Why only edge observations count

The duration of totality at the central line depends weakly on the inputs. Quaglia et al. computed, for the 2017 August 21 eclipse, the effect of raising the solar radius from the standard $s_0 = 959.63''$ to $960.00''$ at 1 au. On the central line the duration dropped by 1.8 s. At their site a few hundred metres inside the southern limit near Vale, Oregon, it dropped by 19.3 s. The distance from the site to the limit went from 1200 m to under 400 m [@val-quaglia-2021]. Wright and Young state the same sensitivity the other way round: very close to the limit, a discrepancy of 1 s in duration corresponds to an error as small as 20 km, or $0.03''$, in solar radius [@val-wright-young-2024]. Every test with a measurable residual therefore comes from an [?edge-observation] near a [?path-limit].

The second reason is that only the edge separates the inputs. Maley's description of the IOTA method states that the difference of the northern and southern limit residuals removes the ephemeris error and leaves the solar radius residual [@val-eclipsetours-edge]. A mid-path contact time mixes ephemeris, $\Delta T$, radius and limb into one number that cannot be decomposed.

## IOTA and IOTA/ES campaigns, 1973 to 2017

Maley lists edge expeditions from Acapulco in 1973 through Papua New Guinea in 1984, Gabon in 1987, India in 1995, Curaçao in 1998, Uganda in 2010 and Minden, Nebraska in 2017. Observers stood 1 to 3 km inside the edge. IOTA required a timing precision of 0.5 s or better [@val-maley-edge] [@val-eclipsetours-edge]. The reductions of this era used the Watts limb charts and the DE200 ephemeris, which Maley describes as in error by less than $0.2''$ [@val-eclipsetours-edge]. Fiala, Dunham and Sofia collected every usable eclipse timing from 1715 to 1991 and found that re-reducing the 1984 observations with newer ephemerides shrank the component of the residuals caused by the ephemeris [@val-fiala-1994].

The results of that programme were radius corrections relative to $959.63''$. Nugent's summary of Dunham's 2018 talk gives the 1998 February 26 result as a reduction averaging $0.20'' \pm 0.04''$ [@val-iota-meeting-2018]. Quaglia et al. summarise the 1990s IOTA values (Dunham et al. 2016) as a range whose printed digits read $956''.40$ to $956''.80$. The 1998 figure implies the intended range is $959.40''$ to $959.80''$, and the printed value is taken here as a typographical slip [@val-quaglia-2021] [@val-dunham-2016-iau]. The 2005 to 2008 campaigns coordinated by Sigismondi produced 598 bead data points from 23 observers at 28 stations [@val-sigismondi-2009-atlas]. Raponi et al. tied the bead light curve to the limb darkening function and found, for 2010 January 15, light at least $0.85''$ beyond the inflection point in the Solar Physics reduction, against at least $0.65''$ in the earlier arXiv analysis of the same eclipse [@val-raponi-2012] [@sun-raponi-sigismondi-2011]. The solar-radius topic is the home of that comparison, in [solar radius values](../06-solar-radius/solar-radius-values.md).

IOTA no longer defends the radius variations these campaigns reported. Dunham's 2024 page states that the real errors of the observations were larger than the earlier formal estimates, as determined from different pairs of observations made near each limit of the same well-observed path, and larger than the variations from eclipse to eclipse found earlier. The page concludes that the solar radius is constant or nearly so, and that IOTA "came to realize the difficulty in deriving such information from such recordings" [@val-dunham-iota-2024].

## 2017 August 21: three quantitative tests

### Quaglia et al., flash spectrum at the southern limit

Site: WGS84 $117^{\circ} 13' 09.8''$ W, $43^{\circ} 57' 10.9''$ N, 711 m, just south of Vale, Oregon, a few hundred metres inside the southern limit [@val-quaglia-2021]. A Canon EOS 6D with a 235 lines/mm grating recorded the [?flash-spectrum] at 23.976 frames per second. Light curves of the last and first beads were matched by [?light-curve-matching] to simulations that integrate the limb-darkening function over the exposed photosphere, using DE430 positions, the IAU 2006 Earth orientation model with measured EOP, and LOLA topography in the DE421 mean-Earth frame [@val-quaglia-2021]. The result is

$$s_0 = 959.95'' \pm 0.05''$$

at 1 au with no significant wavelength dependence between 480 and 640 nm [@val-quaglia-2021]. The paper's stated inputs accuracies are a lunar distance residual against laser ranging below 1 m for DE440, ITRS-to-GCRS orientation better than 1 mas, UT1 determined to well below 1 ms, and lunar topography better than 10 m, which is about 5 mas at the Moon's mean distance [@val-quaglia-2021].

The consequences for a 2017 prediction at the central line: totality of 2m10.0s with the Auwers radius becomes 2m08.4s with the new one, a change of 1.6 s. The authors note this matters for scripted cameras [@val-quaglia-2021]. Treating the photospheric edge as a layer $0.05''$ thick makes the duration a range, 2m08.3s to 2m08.5s, and turns the path limits into fuzzy bands 100 m wide [@val-quaglia-2021].

The same paper contains the only published cross-check of three implementations at a single edge site. All were run with $s_0 = 959.63''$. Irwin's model gave C2 17:25:34.3 and C3 17:26:06.9 UTC, a duration of 32.6 s. For the same radius, Occult's Baily's beads tool gave durations 2 s or more longer, and Solar Eclipse Maestro 4 s or more longer. Equivalently, for a given observed duration Occult would infer a radius $0.03''$ higher than Irwin's model and Solar Eclipse Maestro $0.07''$ higher. A bend in the duration-versus-radius curve at $960.15''$, caused by third contact jumping to a different valley, appears in neither application [@val-quaglia-2021].

### Guhl and Tegtmeier, IOTA/ES at both limits

The northern station 2017USN1 (Elke and Konrad Guhl) was at $43^{\circ} 40' 23.5''$ N, $108^{\circ} 12' 18.4''$ W, 1320 m, in Thermopolis, Wyoming, 700 m inside the totality zone with a predicted duration of 16 s. A 100/1000 mm Maksutov, a 535 nm filter and a GPS time inserter were used. Beads were reduced with Occult 4.5.3.0 using LOLA and Kaguya (SELENE) data. Table 1 of the paper lists 16 [?bead-residual|bead residuals] as events between 17:39:59.9 and 17:40:42.9 UTC with per-bead radius variations from $-0.10''$ to $+0.14''$ and a mean of $+0.029''$, giving $959.66''$ [@val-guhl-tegtmeier-2018].

The southern station 2017USS1 (Carmen and Andreas Tegtmeier) was at $37^{\circ} 13' 6.20''$ N, $89^{\circ} 40' 49.26''$ W, 106 m, about 15 km south-west of Cape Girardeau, Missouri, which the authors describe as approximately 1100 m outside the totality zone. Beads were recorded but the video was overexposed, and the per-bead corrections were all between $+0.17''$ and $+0.33''$ with a mean of $+0.25''$. The authors treat the southern result as showing "the limits of the method with the 8 bit video signal" and report the northern station alone as their result, while noting that the two-station average would be $959.88''$ [@val-guhl-tegtmeier-2018]. The paper also records that the IOTA/ES bead programme ended with 2017 because spacecraft measurements were judged better after 2012 [@val-guhl-tegtmeier-2018].

The southern station's overexposed $+0.25''$ is close to the later consensus value, and the northern station's $+0.03''$ is not. Nothing in the paper resolves this. Overexposure makes faint beads appear earlier at disappearance and later at reappearance, which mimics a larger Sun, so the authors' decision to discard the southern value is defensible on its own terms. Whether the 700 m northern site was affected by a specific valley is not discussed.

### The NASA limb-corrected greatest duration

Espenak's 2017 interactive map states that the smooth-Moon greatest duration is 2m40.2s and that detailed predictions using the limb profile give 2m41.7s [@val-gsfc-2017-google]. This 1.5 s difference compares two predictions and no observation. It is the only place where NASA quantified the limb effect for that eclipse on the public map.

### Crowd-sourced stations

Maley and Lisa Clapper set up student stations near Minden, Nebraska, at the southern edge, to determine "the true vs predicted edge of an eclipse path" [@val-maley-edge]. A search-engine summary of an EclipseWise page describes 15 stations using smartphones. Nugent's summary of the 2018 IOTA meeting records that "there weren't enough volunteers to reach the goals of determining historical accuracies of the solar diameter" [@val-iota-meeting-2018]. Dunham singles out Fred Bruenjes's recording from his home about 2 km north of the southern limit as the best portrayal of edge phenomena in 2017 but states that it "was not timed accurately" [@val-dunham-iota-2024]. No numeric result from any Kentucky, Nebraska or Oregon crowd station was found in IOTA's journal, on IOTA's web pages or in the meeting summary. That absence is a finding: the 2017 citizen edge programme produced no published offsets.

## 2019 and the pre-2024 radius consensus

The measured values and their provenance are collected in [solar radius values](../06-solar-radius/solar-radius-values.md). This section keeps the rows that come from timed edge observations. Guhl's 2023 paper tabulates the IOTA/ES station results as $-0.04''$ for 2016 September 1, $+0.03''$ for 2017 August 21, and $-0.08''$ for 2019 July 2 [@val-guhl-2023]. Lamy et al. obtained 17 photometer determinations across the 2010, 2012, 2013 and 2015 eclipses, with Kaguya limb data, of $959.94'' \pm 0.02''$, $960.02'' \pm 0.04''$, $959.99'' \pm 0.09''$ and $960.01'' \pm 0.09''$, average $959.99'' \pm 0.06''$ at 540 nm, equivalent to $696{,}246 \pm 45$ km [@val-lamy-2015]. Wright and Young list the modern eclipse values as $959.99'' \pm 0.06''$ (Lamy), $959.95'' \pm 0.05''$ (Quaglia), $959.98''$ (Jubier et al. 2021) and $960.01''$ (Guhl 2023) [@val-wright-young-2024]. Jubier's own map help states that the true photospheric radius is "closer to 959.98 arc-seconds at one astronomical unit ($\pm 0.02$ arc-second)" while the map computes with $959.63''$ [@val-jubier-map-help]. The IOTA/ES filtered-video results sit below this consensus and the light-curve results sit on it.

## 2023 April 20 and October 14

The hybrid eclipse of 2023 April 20 was observed at the northern limit of its total segment in Cape Range National Park, Western Australia, by both an IOTA/ES station and the Besselian Elements team. Guhl's station 2023AUN1 timed 16 beads between 03:28:52.7 and 03:30:05.7 UTC by photometry of FITS frames, reduced with Occult including LOLA data, with per-bead corrections from $+0.24''$ to $+0.61''$ and a mean of $+0.38''$, giving

$$959.63'' + 0.38'' = 960.01'' \pm 0.12''$$

at 535 nm [@val-guhl-2023]. Quaglia et al. placed three photodiode loggers at sites less than a couple of hundred metres inside the northern limit, at heights of $-1$, $-8$ and $-9$ m. Visual timing of the flash spectrum through grating spectacles supports $959.90'' < s_0 < 960.02''$. The photodiode ambient-light curves gave $960.25'' \pm 0.04''$, $960.23'' \pm 0.04''$ and $960.25'' \pm 0.05''$, which the authors reject as a limitation of ambient-light curves. The paper also shows that for $s_0 = 960.28''$ second and third contact coincide at Site 1, so the northern limit passes through the site [@val-quaglia-2023-joa]. The 2023 April limit was therefore fixed by observation to a band a few hundred metres wide, and the two teams agree at the $0.1''$ level.

For the 2023 October 14 annular eclipse Dunham recorded from $35.50030^{\circ}$ N, $108.85797^{\circ}$ W, 1966 m, near Mentmore, New Mexico, a site chosen on Jubier's map near the southern limit, and obtained about 3 minutes of beads through the annular phase [@val-dunham-nam23grz]. No observed-minus-predicted time or distance was published for that site, and no other 2023 October edge report with numbers was found in the IOTA pages or the Journal for Occultation Astronomy issues read.

## 2024 April 8: the Stephenville experiment and the Maine graze

### Stephenville, Texas

The Besselian Elements team stood in Stephenville City Park, very close to the predicted northern limit, with a GPS-disciplined Arduino "UTC Event Timer", and timed the vanishing and return of the photospheric continuum seen through diffraction-grating spectacles. Observed: C2 18:39:06.6 UTC, C3 18:39:20.3 UTC, duration 13.7 s, with an estimated error on the duration "of the order of just a couple of seconds, no more" [@val-besselian-maps-accuracy]. The predictions for that site were:

| Source | Predicted duration |
|---|---|
| timeanddate.com | 65 s |
| eclipse2024.org (local circumstances) | 62 s |
| xjubier.free.fr, uncorrected | 57.4 s |
| eclipse2024.org simulator | about 36 s |
| xjubier.free.fr, lunar-limb corrected | 24.5 s |
| Besselian Elements (Irwin), true limb, $959.95''$ | 12.9 s |
| **Observed** | **13.7 s** |

The team notes that the differences between the predicted northern limits "can be of the order of a couple kilometers" and that all predictions other than Irwin's differ from the observation by "several tens of seconds, well beyond the level of experimental uncertainty" [@val-besselian-maps-accuracy]. The experiment is the team's own test of its own model, and the grading here reflects that. It nevertheless separates the inputs cleanly. The smooth-limb, standard-radius products are 40 to 50 s too long. Those are timeanddate, eclipse2024.org and Jubier uncorrected. Adding the limb profile, which is Jubier's corrected column, removes about 33 s. Adding the larger radius removes the remaining 11 s.

### Solon, Maine

Dunham and Joan Dunham observed from $44^{\circ} 58' 38.6''$ N, $69^{\circ} 52' 03.7''$ W, 114 m by GPS (121 m by Google Earth), 3 km north of the predicted southern limit. They recorded over a minute of beads before second contact and another minute after third, and about 43 s of totality [@val-dunham-iota-2024]. The page does not state which prediction the 43 s is to be compared with. Dunham's pre-eclipse guidance is more useful as a measurement. On Jubier's map, a site exactly on Irwin's northern limit shows a limb-corrected duration of 13 s where Irwin gives zero or a fraction of a second. Jubier's corrected duration goes to zero about 0.7 km farther north-west, "consistent with the difference in the values for the solar radius used" [@val-dunham-iota-2024]. Dunham also judged Irwin's stated one-sigma limit error of less than 90 m too small, given the varying sensitivity of telescopes and cameras to faint beads, and recommended an [?umbral-depth] of at least 2.0 km on Jubier's map, expecting actual durations up to 10 s shorter than Jubier's corrected values [@val-dunham-iota-2024].

### Public reaction and NASA's position

Irwin's 2024 map, with true-limb limits and $959.95''$, moved the northern limit "to the southeast by several city blocks compared to maps calculated with the conventional radius" [@val-wright-young-2024]. EarthSky quantified the shift as about 2,000 feet (610 m) along most of the northern and southern edges and quoted C. Alex Young of NASA Goddard that "some of this was noticed in 2017" [@val-earthsky-2024-edges]. Space.com reported the same work with the caution that it was not peer reviewed and that Young would publish a paper showing the Sun slightly larger than expected [@val-space-edge-report-2024]. NASA did not revise its map. Wright and Young's paper, published 2024 September 19, calls for "an authoritative consensus" on the eclipse radius and states that nearly all eclipse calculations still use $959.63''$ [@val-wright-young-2024]. The 610 m figure is consistent with the arithmetic: $0.32''$ at the Moon's mean distance of 384,400 km is 0.60 km.

No forum or mailing-list report from an observer who stood between the two 2024 limits and saw no totality has been read here. The artefact that would close the gap is named in the open questions.

## Historical edge anecdotes

Rao collects three. The 1925 January 24 eclipse had its southern limit along 96th Street in Manhattan, with the corona briefly visible south of it. A 1970 March 7 observer at Chatham, Massachusetts, about 7 km outside totality, saw the corona for a few seconds in a 4-inch telescope. Edge reports from 1970 describe beads lasting nearly a minute before and after totality, roughly ten times the central-line duration [@val-space-rao-edge-history]. These are qualitative and predate any GPS timing, but the 1970 bead durations agree with the 2024 Maine recording and give the developer a sanity check on any bead simulator.

## What the offsets say about each input

Collecting the numbers above by cause:

| Cause | Evidence | Size |
|---|---|---|
| Solar radius $959.63''$ instead of about $959.95''$ | Quaglia 2017, Stephenville 2024, EarthSky | 600 m per limit, 1.6 to 1.8 s at central line, 10 to 20 s within a few hundred metres of a limit |
| Smooth Moon instead of limb profile | Stephenville 2024 (57.4 s to 24.5 s), NASA 2017 greatest duration (+1.5 s) | 1 to 3 s typical at centre, tens of seconds at the edge |
| Implementation differences at the same inputs | Irwin versus Occult versus Solar Eclipse Maestro at Vale | 2 to 4 s of duration, or $0.03''$ to $0.07''$ of radius |
| Bead timing noise, filtered video, 8 bit | 2017USN1, 2023AUN1 | $\pm 0.1''$ per bead, systematic $+0.2''$ when overexposed |
| Observer clock, visual contacts | Stephenville UTC timer | about 2 s on a duration |
| Site position | Dunham on Irwin's 90 m sigma | 90 m to 2 km of recommended margin |

Ephemeris and $\Delta T$ do not appear because no edge report has attributed a residual to them since the DE200 era. The 2024 realised $\Delta T$ errors are treated in the error-budget note.

## Sources compared

| Source | Eclipse and site | What it measures | What it uniquely provides |
|---|---|---|---|
| Quaglia et al. 2021 [@val-quaglia-2021] | 2017, Vale OR, southern limit | Radius from flash-spectrum light curves | Sensitivity curves, three-implementation comparison, fuzzy-band interpretation |
| Guhl and Tegtmeier 2018 [@val-guhl-tegtmeier-2018] | 2017, Thermopolis WY and Cape Girardeau MO | Bead residuals with Occult, LOLA and Kaguya | Per-bead table with times and residuals |
| Guhl 2023 [@val-guhl-2023] | 2023 April, Cape Range | Bead residuals by FITS photometry | $960.01'' \pm 0.12''$ and the IOTA/ES series 2016 to 2023 |
| Quaglia et al. 2023 [@val-quaglia-2023-joa] | 2023 April, Cape Range | Visual flash spectrum and photodiodes | Shows ambient-light curves overestimate the radius |
| Besselian Elements 2024 [@val-besselian-maps-accuracy] | 2024, Stephenville TX | Timed C2 and C3 against six predictors | The only side-by-side test of public products |
| Dunham 2024 [@val-dunham-iota-2024] | 2024, Solon ME | Beads and totality at 3 km inside | IOTA's retraction of radius variability, the 2 km margin |
| Lamy et al. 2015 [@val-lamy-2015] | 2010 to 2015 | Photometer light curves | The largest consistent radius data set |
| Maley [@val-maley-edge] [@val-eclipsetours-edge] | 1973 to 2017 | Edge expedition method | Timing requirement, residual differencing |
| Rao 2024 [@val-space-rao-edge-history] | 1925, 1970 | Anecdotes | Bead durations at the edge before GPS |

## What a developer should do

1. Use the Stephenville 2024 record as the primary end-to-end test: site in Stephenville City Park, C2 18:39:06.6 UTC, C3 18:39:20.3 UTC, tolerance about 2 s. A smooth-Moon implementation with $959.63''$ will fail by 40 to 50 s, a limb-corrected one with $959.63''$ by about 11 s, and a limb-corrected one with $959.95''$ should pass [@val-besselian-maps-accuracy].
2. Use the Vale 2017 site as the second test. With $s_0 = 959.63''$ the reference contacts are C2 17:25:34.3 and C3 17:26:06.9 UTC from Irwin's model, and Occult and Solar Eclipse Maestro are 2 s and 4 s longer. Any implementation should land within that 4 s spread, and should reproduce the drop of the limit distance from 1200 m to under 400 m when the radius is raised to $960.00''$ [@val-quaglia-2021].
3. Reproduce the per-bead tables of Guhl and Tegtmeier for 2017USN1 and of Guhl for 2023AUN1 with a bead simulator using LOLA. The residual scatter of $\pm 0.1''$ is the noise floor of filtered video, so a simulator that matches the event list to within a second per bead is doing as well as the data allow [@val-guhl-tegtmeier-2018] [@val-guhl-2023].
4. Read Quaglia et al. 2021 in full before choosing a radius, then Wright and Young 2024 section 6.4, then Dunham's 2024 page for the practical margin.

## What this changes

The pipeline must carry the solar radius as a parameter and expose it to the user, with $959.95''$ or a value near it as the default for edge products and $959.63''$ available for reproducing NASA and Espenak tables. Limb-corrected contacts are mandatory for anything within 5 km of a limit. The path limit should be drawn as a band of at least 100 m and preferably with the 1-sigma lines Irwin uses, not as a line.

## Open questions

- Obtain Dunham et al. 2016, IAU Symposium 320, to resolve the printed IOTA radius range and to get the per-eclipse values and uncertainties of the 1990s campaign [@val-dunham-2016-iau].
- Obtain Jubier, Koutchmy, Daniel et al. 2021 and its method. That is the source of the $959.98''$ value cited by Wright and Young [@val-wright-young-2024].
- Obtain the promised Journal for Occultation Astronomy article on the Solon, Maine recording with its bead timings, and the separate US IOTA report on 2017 that Guhl and Tegtmeier said was expected [@val-dunham-iota-2024] [@val-guhl-tegtmeier-2018].
- Obtain the Forbes articles of 2024 March 30 and 31 by Carter that listed the 15 places whose status changed, to build a list of 2024 sites with observer reports [@val-wright-young-2024].
- Obtain a dated SEML, Cloudy Nights or Reddit post by a 2024 observer positioned between the Jubier and Irwin northern limits who reports no totality, with coordinates, and the equivalent for 2017 observers near Vale and Thermopolis.
- Obtain the SunSketcher 2024 results, which timed beads with thousands of smartphones along the whole path, to see whether a crowd data set can constrain the radius or the limb profile.
