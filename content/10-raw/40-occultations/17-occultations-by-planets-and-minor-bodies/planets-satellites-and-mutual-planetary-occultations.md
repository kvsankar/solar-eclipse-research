---
title: Planets, satellites and mutual planetary occultations
seo_title: Occultations by Planets and Planet-Planet Occultations
description: How occultations of stars by the giant planets, Titan, Triton and the Galilean moons are predicted, and how planet-planet occultations are found.
order: 3
status: working
updated: 2026-10-17
tags: [stellar-occultation, planets, titan, triton, galilean-moons, mutual-occultation, spice]
---

::: summary
- **Planetary predictions use SPICE kernels and Gaia DR3.** French and Souami's list for 2023 to 2050 covers Jupiter, Saturn, Uranus, Neptune, Titan and Triton. It uses DE440 with jup365, sat440l, ura161 and nep097, matches 2MASS K-band stars to Gaia DR3, and agrees with SORA (Stellar Occultation Reduction and Analysis) to a few seconds and a few kilometres [@mb-french-souami-2023].
- **Bright events are rare and clustered.** Between 2023 and 2050 Jupiter has about one event a year with K ≤ 7 and Saturn two with K ≤ 5. Uranus has ten ring occultations with K ≤ 10, and Triton only 22 events with K ≤ 15 [@mb-french-souami-2023].
- **A planet's limb is an atmosphere, not an edge.** Refraction spreads the star's disappearance and can produce a central flash, so planetary occultations probe stratospheres and give ring orbits rather than sizes [@mb-french-souami-2023] [@mb-meza-2019].
- **Satellite occultations give the best ground-based satellite astrometry.** For the Galilean moons, a 3D shape fit to the chords gives positions near 1 milliarcsecond, about 3 km at Jupiter at opposition, against 100 to 150 milliarcseconds from conventional imaging [@mb-morgado-2022-galilean].
- **Planet-planet occultations are eclipse geometry.** The farther planet plays the Sun and the nearer one plays the Moon, so the fundamental plane, the cone condition and the total, annular and partial classes carry over. The last event was Venus and Jupiter on 1818 January 3, and the next is the same pair on 2065 November 22 [@mb-gray-mutual] [@mb-bogan-mutual].
- **The lists disagree in detail.** Albers 1979 found 21 events in 1557 to 2230. Gray's VSOP search gives about one per 35 years. Event times for 2065 differ between lists by more than two minutes [@mb-albers-1979] [@mb-gray-mutual] [@mb-bogan-mutual].
:::

**The question.** How are occultations of stars by the major planets and their satellites predicted and reduced, how does this differ from the minor-body case, and how are occultations of one planet by another found and classified? The minor-body geometry is in [Prediction geometry and astrometry](prediction-geometry-and-astrometry.md), and the Moon as occulter is in [Lunar occultations](../13-lunar-occultations/_index.md).

## Occultations of stars by the giant planets

### Prediction

French and Souami compute their predictions with their occultation code RINGFIT. It works in a solar-system-barycentric inertial frame and evaluates geocentric apparent positions of the targets with [?spk-kernel|SPICE kernels] from NASA's Navigation and Ancillary Information Facility (NAIF) [@mb-french-souami-2023]. The kernels are `de440.bsp` for the planets except in Uranus events, `jup365.bsp` for Jupiter, `sat440l.bsp` for Saturn and Titan, `ura161.bsp` with `peph.ura160.bsp` for Uranus events, and `nep097.bsp` and `nep101.bsp` for Neptune and Triton. Earth orientation comes from ITRF binary kernels, and pole directions and radii from `pck00010.tpc` [@mb-french-souami-2023].

The star search runs in two catalogues. French and Souami first take 2MASS stars brighter than the K-band limit "within 4$''$ of each target's path" at the 2MASS epoch 1996.0. They state that this generous margin covers the 0.5 arcsecond 2MASS accuracy, the planets' and rings' extent, the Earth's angular size from the target, ephemeris errors and proper motion [@mb-french-souami-2023]. They then match each candidate to Gaia DR3 within 1 arcsecond after propagating proper motion. They apply the Cantat-Gaudin and Brandt correction and propagate the position errors after Butkevich and Lindegren 2014 [@mb-french-souami-2023]. K-band limits are K ≤ 10 for Jupiter and Saturn and K ≤ 15 for Uranus, Neptune, Titan and Triton. The infrared band is used because methane absorption near 2.2 µm darkens the planet relative to the star [@mb-french-souami-2023].

Observability is decided per site. Events with a Sun-geocentre-target angle below 45 degrees are dropped. An event is observable when the Sun is more than 5 degrees below and the target more than 5 degrees above the horizon, at 13 listed observatories and at the geocentre [@mb-french-souami-2023]. Each event gets a planet type and, for Saturn, Uranus and Neptune, a ring type. These record whether ingress or egress is visible from Earth, from the geocentre, from a listed site, or not at all [@mb-french-souami-2023]. As a cross-check, SORA with the same kernels "returned virtually identical sets of candidate occultations". Closest-approach times agreed "to within a few seconds" and sky-plane separations "to within a few km" [@mb-french-souami-2023].

The resulting frequencies, for 2023 to 2050 [@mb-french-souami-2023]:

| Target | Limit | Events |
|---|---|---|
| Jupiter | K ≤ 7 | about one per year, more in 2031 and 2043 |
| Saturn | K ≤ 5 | two, in 2032 and 2047 |
| Uranus rings | K ≤ 10 | ten |
| Neptune | K ≤ 12 | thirteen, star-poor fields until 2068 |
| Titan | K ≤ 15 | 1 769, several bright in 2029 to 2031 |
| Triton | K ≤ 15 | 22 |

Pluto is excluded "because its long-term ephemeris is much less accurate than Titan's and Triton's" [@mb-french-souami-2023]. For Triton, a recent orbit differs from the JPL ephemerides NEP081 and NEP097 by less than 300 km, about 15 milliarcseconds [@mb-french-souami-2023].

### What the light curve measures

A planet does not have a sharp limb at the star's level. The star is dimmed by refractive defocusing in the upper atmosphere, so the light curve encodes a profile of density, pressure and temperature. French and Souami list the stratospheric results for Jupiter, Saturn, Uranus and Neptune that came from such events [@mb-french-souami-2023]. Near the central line, refraction around the whole limb focuses light into a [?mb-central-flash|central flash]. It was seen in Saturn's 1989 event, and in recent dense campaigns on Triton and Pluto [@mb-french-souami-2023]. The same physics is the basis of the Pluto pressure record of [Light curves, chords and results](light-curves-chords-and-results.md#trans-neptunian-objects-and-centaurs) [@mb-meza-2019].

The rings are sharp-edged absorbers and give precise timings. Uranus's rings were found in the 1977 March 10 occultation of SAO 158687 [@mb-elliot-1977]. French and Souami cite eight papers on that event, and describe how later occultations showed the rings to be "eccentric and inclined, precessing under the gravitational influence of the oblate central planet" [@mb-french-souami-2023]. Concerted Neptune campaigns then found its incomplete ring arcs [@mb-french-souami-2023]. The prediction for planetary ring occultations therefore needs the ring geometry. French and Souami tabulate the radii and widths they assume for each ring of Saturn, Uranus and Neptune [@mb-french-souami-2023]. An occultation of a star by Saturn's rings uses those radii with the ring geometry of [Saturn theories and ring geometry](../../50-planetary-satellites/16-saturn-and-outer-satellites/saturn-theories-and-ring-geometry.md). The star's sky-plane offset from Saturn's centre is mapped to a ring-plane radius and compared with the tabulated ring edges.

### Historical events

French and Souami give the event histories [@mb-french-souami-2023]:

- **Jupiter.** Five photometric events: $\sigma$ Arietis on 1952 November 20, $\beta$ Scorpii on 1971 May 13, SAO 78505 on 1989 December 13, HIP 9369 on 1999 October 10 and an event of 2009 August 3 to 4. The 1971 event was also an occultation by Io, in the paper title "The occultation of Beta Scorpii by Jupiter and Io".
- **Saturn and Titan.** 28 Sgr on 1989 July 3, at K = 1.48, was "predicted by Taylor (1983)". It probed Saturn's rings and stratosphere, showed a central flash, and gave Titan's atmosphere between 290 and 500 km altitude.
- **Neptune.** First modern event on 1968 April 7.
- **Triton.** Voyager 2 radio occultation in 1989, ground events in 1993, 1995 and 1997. On 2017 October 5, 90 European stations recorded the event, with 42 central-flash detections.

The 2022 October 6 Triton occultation gave a pressure of 1.211 ± 0.039 microbar at 1 400 km radius and a surface pressure of 14.54 ± 0.47 microbar, the same within error bars as in 2017 [@mb-sicardy-2024-triton].

## Occultations of stars by planetary satellites

A planetary satellite is reduced like an asteroid: the chords fix its outline and centre on the [?fundamental-plane|fundamental plane] [@mb-morgado-2022-galilean]. Two things differ. The satellite's position is relative to its planet, so its ephemeris is a satellite theory such as `jup365` or `sat440l` on top of the planetary one [@mb-french-souami-2023]. The planet's glare also spoils direct astrometry. Morgado et al. state that for the Galilean moons conventional CCD positions carry 100 to 150 milliarcseconds because "Jupiter's brightness in the Field of View (FoV) would quickly saturate the CCD" [@mb-morgado-2022-galilean].

Morgado et al. observed occultations by Io in 2021, Ganymede in 2020 and Europa in 2019, and re-analysed events by Europa in 2016 and Ganymede in 2017 [@mb-morgado-2022-galilean]. They fitted each satellite's known 3D shape to the chords to locate its centre of figure. The resulting positions have uncertainties "in the order of 1 mas (∼3 km at Jupiter distance during opposition)", about ten times better than other methods [@mb-morgado-2022-galilean]. They name the alternatives as mutual phenomena, mutual approximations, radar astrometry and stellar occultations [@mb-morgado-2022-galilean].

Herald's data set keeps planetary and satellite events in separate files from asteroid events, `occsatlist` and `occsattimings` [@mb-herald-2020]. Occult computes occultations of stars by planets and planetary satellites. It also computes eclipses and transits of satellites against their planet, mutual eclipses and occultations of satellites, and mutual conjunctions of planets [@sw-occult4]. For satellites of TNOs, the Lucky Star predictions take ephemerides from the Genoid project [@mb-lucky-star-predictions].

## Mutual planetary occultations

### The geometry is eclipse geometry

A [?mb-mutual-planetary-occultation|mutual planetary occultation] is a solar eclipse with the Sun replaced by the farther planet and the Moon by the nearer one. Both have finite angular size, so the shadow of the nearer planet in the farther planet's light has an umbral and a penumbral cone. The plane perpendicular to the line joining them is a fundamental plane exactly as in [Besselian elements](../../10-shared/01-foundations/besselian-elements.md). This correspondence is a derivation from the eclipse geometry, not a statement found in the mutual-occultation lists. The lists do use the eclipse vocabulary. The Wikipedia list classifies events as total, annular or partial, and treats an annular event as a transit [@mb-wiki-mutual].

A geocentric screening condition follows from that geometry. Let $s$ be the geocentric angular separation of the centres, $\sigma_n$ and $\sigma_f$ the angular semidiameters of the nearer and farther planet, and $\pi_n$ and $\pi_f$ their [?horizontal-parallax|horizontal parallaxes]. The topocentric separation differs from $s$ by at most about $\pi_n - \pi_f$. Somewhere on Earth the discs can then overlap only if

$$
s < \sigma_n + \sigma_f + (\pi_n - \pi_f).
$$

The event is an occultation in the strict sense where $\sigma_n > \sigma_f$ and the nearer disc covers the farther. It is a transit where $\sigma_n < \sigma_f$. Gray's list applies the equivalent test: "An event is listed if, at some point on the earth, the disk of one planet overlaps another" [@mb-gray-mutual]. Because the two planets lie at different distances, each apparent position must carry its own [?light-time|light-time] to the Earth at the same reception instant.

### The lists

Steven Albers published the first dedicated table in 1979 [@mb-wiki-mutual]. Bogan reports that Albers "wrote a high precision computer program to search for mutual occultations of planets". Albers "found 21 such events in the period from 1557 to 2230 with none in the 20th century and only 2 in the 19th century" [@mb-bogan-mutual] [@mb-albers-1979]. The Wikipedia list states that Meeus and Walch had found the 1522 and 1570 events in a manual search of conjunctions published in 1970. It adds that De Meis 1993 and Meeus 1998 extended and recomputed the table [@mb-wiki-mutual]. Gray computed events from -1000 to +6000 with the VSOP theory. His times are in TD and his dates Gregorian even before 1582. He finds an average rate of "about one every 35 years" and warns that distant events are "slightly more doubtful" [@mb-gray-mutual].

The Venus-Jupiter pairs as listed:

| Date | Gray (TD) [@mb-gray-mutual] | Bogan (UT) [@mb-bogan-mutual] | Bogan: elongation, diameters, geocentric separation |
|---|---|---|---|
| 1570 February 15 (Gray), February 5 (Bogan) | 7:48, separation 0.005° | 7:47 | 25° W, 11″ and 31″, 18″ |
| 1818 January 3 | 21:52, separation 0.004° | 21:51 | 16° W, 10″ and 30″, 12″ |
| 2065 November 22 | 12:45, separation 0.004° | 12:47 | 8° W, 10″ and 29″, 14″ |
| 2123 September 14 | 15:28, separation 0.002° | 15:26 | 16° E, 10″ and 29″, 6″ |

Four points follow from these numbers. First, Venus's disc is smaller than Jupiter's in every case, so in the strict sense these are transits of Venus across Jupiter. Bogan calls them occultations of Jupiter by Venus [@mb-bogan-mutual], while the Wikipedia list classes 1818 as annular [@mb-wiki-mutual]. Second, with Bogan's 1818 values the geocentric separation of 12 arcseconds plus Venus's 5 arcsecond semidiameter exceeds Jupiter's 15 arcsecond semidiameter. A central, annular phase therefore needs topocentric parallax, which is consistent with the Wikipedia list placing annular visibility only in Sakhalin, the Kurils and Kamchatka [@mb-wiki-mutual]. Third, the 2065 times disagree. Bogan's UT is two minutes later than Gray's TD, although UT runs behind TD by ΔT. The lists therefore differ by more than two minutes. The sources do not give enough detail to say which is right. Fourth, the 1570 dates differ by ten days. Gray states that his dates are Gregorian even before 1582, so Bogan's date is presumably Julian, although his table does not say so for that event [@mb-gray-mutual] [@mb-bogan-mutual].

The 2065 event occurs 8 degrees from the Sun, and Bogan describes it as essentially unobservable [@mb-bogan-mutual]. The 1737 May 28 occultation of Mercury by Venus is the one Bogan describes as observed, by Bevis [@mb-bogan-mutual].

## Sources compared

| Source | Kind | Ephemeris | Star or event data | Unique content |
|---|---|---|---|---|
| French and Souami 2023 [@mb-french-souami-2023] | Prediction survey | DE440 and satellite kernels | 2MASS K matched to Gaia DR3 | Kernel list, event types, frequencies to 2050, event histories |
| Morgado et al. 2022 [@mb-morgado-2022-galilean] | Satellite astrometry | Not stated in the abstract or introduction | Gaia | 1 mas Galilean positions, glare limit of imaging |
| Sicardy et al. 2024 [@mb-sicardy-2024-triton] | Atmosphere | Not stated in the abstract | Not stated in the abstract | 2022 Triton pressure |
| Gray, Project Pluto [@mb-gray-mutual] | Event list | VSOP | Not applicable | -1000 to +6000, TD, overlap criterion |
| Bogan [@mb-bogan-mutual] | Event list | Guide 7 for added events | Not applicable | Elongations, diameters and separations |
| Albers 1979 [@mb-albers-1979] | Event list | Not known | Not applicable | First dedicated table, known only secondhand |
| Wikipedia list [@mb-wiki-mutual] | Compilation | Not stated | Not applicable | Total, annular and partial classes, list history |

## What a developer should do

1. For planetary and satellite events, take positions from the NAIF kernels that French and Souami list, and stars from Gaia DR3 with proper-motion correction and propagated errors [@mb-french-souami-2023].
2. Model the planet's limb as an atmosphere and its rings as geometric bands with tabulated radii and widths. Do not use the minor-body diffraction model for these targets [@mb-french-souami-2023]. None of the sources cited here prints a refractive light-curve formula. French and Souami cite Baum and Code 1953 for the first photometric occultation by Jupiter, of 1952, and for Jupiter's stratospheric thermal structure [@mb-french-souami-2023].
3. For satellites, fit a 3D shape model to chords, as Morgado et al. do [@mb-morgado-2022-galilean].
4. For planet-planet events, reuse the Besselian code with the farther planet as source. Screen geocentrically with $s < \sigma_n + \sigma_f + (\pi_n - \pi_f)$, apply separate light-times, and classify the result as total, annular or partial on the same plane.
5. Validate against Gray's and Bogan's lists, and expect minute-level disagreement for the 2065 event [@mb-gray-mutual] [@mb-bogan-mutual].

## What this changes

The planet-planet case needs no new geometry: the solar-eclipse Besselian stage, parameterised by source and occulter, computes it. Planetary and satellite occultations of stars need two additions to the minor-body pipeline: a satellite-ephemeris layer on top of the planetary ephemeris, and a refractive light-curve model in place of the diffraction model.

## Open questions

- Obtain Albers 1979 in Sky & Telescope 57, 220 to read its method, its ephemeris and the full list of 21 events [@mb-albers-1979].
- Obtain Meeus, Mathematical Astronomy Morsels III, for the chapter on mutual occultations of planets and its light-time discussion.
- Obtain the full Gray list as a file and compute the 1818 and 2065 events with DE440 to settle the time disagreement between lists [@mb-gray-mutual].
- Obtain Baum and Code 1953, "A photometric observation of the occultation of σ Arietis by Jupiter" (AJ 58, 108). Quote its light-curve relation for a refracting atmosphere, with its constants [@mb-french-souami-2023].
- Obtain French and Souami's supplementary material to read RINGFIT's treatment of refraction and planetary oblateness in the predicted chords [@mb-french-souami-2023].
- Obtain Taylor 1983 for the 28 Sgr prediction, an early example of a planetary prediction made before Hipparcos [@mb-french-souami-2023].
