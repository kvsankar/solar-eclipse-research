---
title: Uranus, Neptune, Pluto and Mars satellite events
seo_title: Uranus and Pluto-Charon Mutual Events
description: How the 2007 Uranian mutual events and the 1985 to 1990 Pluto-Charon events were predicted and observed, with notes on Triton, Phobos and Deimos.
order: 3
status: working
updated: 2026-10-17
tags: [uranus, pheura07, gust86, pluto, charon, triton, phobos, mutual-events]
---

::: summary
- **Uranus's satellites have [mutual events](../15-jupiter-satellites/mutual-events.md) every 42 years,** at Uranus's equinox. The 2007 season was the first observed. The Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) predicted it with two models, GUST86 and LA06, and published both [@sats-arlot-2006-uranus].
- **The models disagreed by up to 500 km, or 0.04 arcseconds.** Mid-times mostly agreed within 5 minutes, but one event differed by 30 minutes, and 11 main events predicted by LA06 did not occur in GUST86 [@sats-arlot-2006-uranus].
- **The reason was the viewing geometry.** Most earlier observations saw the system nearly pole-on, so the orbital inclinations were poorly fitted. The mutual events constrained them directly [@sats-arlot-2006-uranus].
- **Observations reached formal uncertainties below 0.01 arcseconds.** The first event, Oberon occulting Umbriel on 2007 May 4, gave a mid-time to 4 s. Eight events seen with telescopes of 0.4 to 10 m showed observed mid-times systematically later than predicted [@sats-hidas-2008] [@sats-christou-2009].
- **[Pluto](https://en.wikipedia.org/wiki/Pluto) and [Charon](https://en.wikipedia.org/wiki/Charon_(moon)) eclipsed each other from 1985 to 1990** at 3.2-day intervals. The light curves gave radii, albedo maps and the orbit, and this happens only about once every 124 years [@sats-binzel-1985] [@sats-phemu-note09].
- **The same software stack covers these systems unevenly.** JPL uses URA182, NEP097, PLU060 and MAR099. [Stellarium](https://stellarium.org/) uses GUST86 and Lainey's MarsSat and has no dedicated [Triton](https://en.wikipedia.org/wiki/Triton_(moon)) or Charon theory. Miriade lists no Charon ephemeris [@sats-jpl-sat-ephem-table] [@sats-stellarium-ephemwrapper] [@sats-miriade-ephemcc-output].
:::

**The question.** Beyond Saturn, which satellite systems produce observable eclipses, occultations and mutual events, how were the classic seasons predicted and observed, and which theories do current programs use for them? The geometry and timing conventions are the same as in [the Saturn phenomena note](saturn-phenomena-and-mutual-events.md). The theory versions for Saturn are in [the theories note](saturn-theories-and-ring-geometry.md).

## Uranus: the 2007 equinox and PHEURA07

### Why every 42 years

"Every 42 years, the Earth and the Sun pass through the equatorial plane of Uranus allowing observations of mutual occultations and eclipses of the main satellites" [@sats-arlot-2006-uranus]. The satellites orbit close to Uranus's equatorial plane, so the events need the Earth or the Sun in that plane, at the "equinox" on Uranus [@sats-arlot-2006-uranus]. Away from equinox the Earth sees the system from near its pole, and the satellites do not pass in front of each other.

That geometry made the predictions hard. "The orbits of the Uranian satellites have little known inclinations due to a geocentric polar view of the system from Earth most of the time" [@sats-arlot-2006-uranus]. A model fitted to pole-on astrometry constrains the satellites' positions in the sky plane well and their heights above Uranus's equator poorly. Those heights are exactly what decides whether an event occurs.

For 2006 to 2008 the paper tabulates the uranocentric declinations of the Earth and the Sun by month. The best period for deep events was May 2007 to February 2008 [@sats-arlot-2006-uranus]. Uranus was at declination −4 to −8 degrees, so both hemispheres could observe. Its opposition fell in September, in the middle of the season [@sats-arlot-2006-uranus].

### Two models, published side by side

IMCCE computed every event with two ephemerides [@sats-arlot-2006-uranus]:

| Model | Kind | Observations fitted | Internal error | External accuracy |
|---|---|---|---|---|
| [?sats-gust86] (Laskar and Jacobson 1987) | Analytical theory | 1911 to 1986 | 10 to 100 km over a ten-year period | about 0.1 arcseconds, from Stone and Harris (2000) |
| LA06 (Lainey and Arlot 2006) | Numerical integration with NOE | 11,359 observations, 1948 to 2003 | around 10 m | around 0.05 arcseconds for recent observations |

LA06 includes Uranus's gravity field through $C_{20}$ and $C_{40}$ from French et al. (1988), solar perturbation from DE406, masses from Jacobson et al. (1992) and the IAU 2000 precession of Uranus [@sats-arlot-2006-uranus]. Only the initial positions and velocities were fitted in that preliminary version [@sats-arlot-2006-uranus].

The comparison was the prediction's error estimate [@sats-arlot-2006-uranus]:

- "the deviation between LA06 and GUST86 may reach 500 km (0.04 arcsec) either in longitude (change in the midtime of the event) or in latitude (change in the magnitude drop of the event)";
- "most of the events have their midtimes predicted within 5 min of time", with exceptions such as "30 min of time for the occultation of U-2 by U-1 on August 25, 2007";
- "among the main events, 11 events predicted using LA06 are not seen using GUST86 and many events have a difference of 50% for their flux drop".

The tables therefore list events from both models, and further tables list events that "may not occur since they are not predicted by both ephemerides" [@sats-arlot-2006-uranus]. An independent prediction set was published by Christou (2005) [@sats-christou-2005].

### How the events were computed and listed

The paper states the eclipse convention used for every IMCCE mutual-event prediction since. Eclipses are not treated as occultations seen from the Sun "because of the light-time". They are treated as "occultations of the Sun as seen from the eclipsed satellites" [@sats-arlot-2006-uranus]. Contacts are computed with both the penumbral and umbral cones, together with "the time of the minimum distance to the axis of the cones" [@sats-arlot-2006-uranus]. The positions of the cones and the satellites "are calculated carefully taking the light-time into account" [@sats-arlot-2006-uranus].

The tables give the time of maximum in TT, the event type, the start of the occultation or penumbral eclipse, and the duration in seconds [@sats-arlot-2006-uranus]. They also give the distance from Uranus's limb in Uranian radii, the flux drop in R, magnitude drops in R and V, and the [?impact-parameter] in arcseconds [@sats-arlot-2006-uranus]. The event type is P for partial, A for annular, T for total, p for penumbral and c for a conjunction without an event [@sats-arlot-2006-uranus]. The albedos used are Miranda 0.307, Ariel 0.350, Umbriel 0.189, Titania 0.232 and Oberon 0.205 in V. The paper notes "the strong difference between Ariel and Umbriel" in their effect on the flux drop [@sats-arlot-2006-uranus].

An event was counted as observable from a site when the Sun was more than 10 degrees below the horizon, Uranus more than 15 degrees above it, and the satellites more than one Uranian radius from the limb [@sats-arlot-2006-uranus]. The predicted times were in TT, and observers were told to subtract about 66 s to get UTC and to "start at least 15 min before the beginning of the event" because of the ephemeris uncertainties [@sats-arlot-2006-uranus].

The paper also notes events by the planet: occultations by Uranus, eclipses by its shadow, transits and shadow transits. Only the eclipses, and perhaps the shadow transits, are easily observable, and IMCCE used their dates to remove mutual events hidden by the planet [@sats-arlot-2006-uranus].

### What was observed

The satellites are faint and close to a bright planet. Observers worked in the near-infrared and modelled and subtracted the planet's light from each frame [@sats-christou-2009].

- **First detection.** Hidas, Christou and Brown observed "the occultation of Umbriel by Oberon on 4 May, 2007", which they believed "is the first observed mutual event between satellites of Uranus". A geometric fit gave the mid-event time "with a precision of 4 seconds" and an impact parameter of "500 +/- 80 km", "more precise than estimates based on current ephemerides" [@sats-hidas-2008].
- **Eight events with five instruments.** Christou and colleagues observed with telescopes "ranging in aperture from 0.4m to 10m", in the near-infrared "to mitigate the glare from the planet". Of fifteen [?sats-light-curve|light curves], "eight of which show a clear drop", giving relative positions "with typical formal uncertainties of <0.01 arcsec" [@sats-christou-2009]. Their mid-times showed "a systematic lag, with the observations later than predictions". Two predicted partial eclipses of Miranda showed no significant drop [@sats-christou-2009].
- **VLT adaptive optics.** Arlot, Dumas and Sicardy recorded an eclipse of Titania by Umbriel on 2007 December 8 in K band with the ESO VLT and the NACO adaptive-optics camera, to assess "the quality of the available dynamical models" [@sats-arlot-2008-titania].

These results agree with the Saturnian experience. A mutual event gives a relative position an order of magnitude better than direct astrometry of the same satellites, and it tests the out-of-plane part of the orbit that pole-on astrometry misses. The next Uranian season falls 42 years after 2007, in the late 2040s.

### Current ephemerides for Uranus's satellites

JPL's table assigns URA182 to Ariel, Umbriel, Titania, Oberon and Miranda. Its reference is Jacobson and Park (2025), "The Orbits of Uranus, Its Satellites and Rings, the Gravity Field of the Uranian System, and the Orientation of the Poles of Uranus and Its Satellites", AJ 169, 65 [@sats-jpl-sat-ephem-table]. Miriade labels its Ariel positions "INPOP19 + LTE-NOE" [@sats-miriade-ephemcc-output]. LTE stands for Laboratoire Temps Espace, the name that IMCCE's campaign page carries [@sats-imcce-phemu-campaign]. Stellarium uses GUST86 "version 0.1 (1988,1995)" by Laskar and Jacobson, rearranged by Gajdosik [@sats-stellarium-gust86] [@sats-stellarium-ephemwrapper]. Cartes du Ciel (Skychart) also uses GUST86, translated from the IMCCE Fortran [@sats-skychart-plansat]. The two open-source planetaria therefore carry the model whose inclinations the 2007 events were designed to test.

## Neptune and Triton

No mutual-event campaign for Neptune's satellites appears in the IMCCE campaign pages or the PHEMU technical notes, which cover Jupiter, Saturn, Uranus and Pluto-Charon [@sats-imcce-phemu-campaign] [@sats-phemu-note09]. Eclipses of satellites by their planet have been modelled for the Neptunian system by Mallama. This work is known here only through Arlot and Thuillot's citation of it [@sats-arlot-thuillot-2008].

For positions, JPL assigns NEP097 to Triton [@sats-jpl-sat-ephem-table]. Miriade labels Triton "INPOP19 + LTE-SAI" [@sats-miriade-ephemcc-output]. The MULTI-SAT server is run by IMCCE and the Sternberg Astronomical Institute (SAI) [@sats-multisat-saturn]. Cartes du Ciel uses Jacobson (1990), A&A 231, 241 [@sats-skychart-plansat]. Stellarium's ephemeris wrapper has no dedicated Triton theory function at commit 77d52ea, so Triton falls back to the generic orbit handling [@sats-stellarium-ephemwrapper]. The NAIF constants kernel gives Triton a radius of 1352.6 km [@sats-naif-pck00011].

## Pluto and Charon, 1985 to 1990

The Pluto-Charon events are the classic demonstration of what mutual events measure. "The first eclipses between Pluto and its satellite ("Charon") were detected in January and February 1985, confirming the satellite's existence" [@sats-binzel-1985]. Binzel and colleagues predicted that "Eclipses lasting a few hours will now occur at 3.2-day intervals for the next 5 to 6 years and then will cease for about 120 years" [@sats-binzel-1985]. They listed the parameters to be measured: "the diameters of the planet and satellite, the surface albedo distribution on one hemisphere of the planet, the orbit of the satellite, and the mass of the planet and hence its density" [@sats-binzel-1985].

The 3.2-day spacing is half of Charon's 6.387-day orbital period, which Cartes du Ciel's Charon model uses [@sats-skychart-plansat]. Each orbit then gives two events, one with Charon in front of Pluto and one with Charon behind it. PHEMU Technical Note 9 gives the recurrence as "only once every 124 years", half of Pluto's orbital period [@sats-phemu-note09].

The following account of the season is reported secondhand from that technical note. The original papers are not quoted here [@sats-phemu-note09]:

- **Predictions.** Mulholland and Binzel (1984) computed the first predictions and showed that the events had not begun by early 1983. Tholen (1985) predicted 81 events for 1986, with a largest drop of about 0.15. Tholen and colleagues tabulated 89 events for 1988.
- **Optics.** Mulholland and Gustafson (1987) suggested diffraction might make the light curves depend on wavelength and aperture. Tholen and Hubbard (1988) showed the effect absent, so simple geometrical optics suffice.
- **Maps.** Buie, Tholen and Horne (1992) inverted the light curves by maximum entropy onto a 59 by 29 grid for Pluto and Charon and found a bright south polar cap on Pluto [@sats-buie-1992]. Young and Binzel (1993) and Reinsch, Burwitz and Festou (1994) produced independent albedo maps of Pluto's sub-Charon hemisphere. Reinsch and colleagues used 18 transits and 15 eclipses and occultations of Charon from 1982 to 1990.
- **Radii.** Young and Binzel (1994) examined a discrepancy of about 4 per cent between Pluto's radius from the mutual events and from the 1988 [stellar occultation](../../40-occultations/17-occultations-by-planets-and-minor-bodies/prediction-geometry-and-astrometry.md). They attributed it to limb darkening neglected in the event models, which leads to underestimated radii [@sats-young-binzel-1994].
- **Orbit.** Tholen and Buie (1997) refined Charon's orbit from HST images and found its semi-major axis in good agreement with the values used to derive the radii from the mutual events.

The radii lesson carries over to every mutual-event reduction. The model of the occulting and occulted discs, including limb darkening and albedo pattern, biases the geometry recovered from the light curve. The PHESAT09 reduction addresses the same issue with its scattering-law model [@sats-arlot-2012-phesat09].

**Current ephemerides.** JPL's PLU060 covers Charon, Nix, Hydra, Kerberos and Styx from 1800 to 2199 relative to the Pluto system barycentre [@sats-naif-aa-summaries] [@sats-jpl-sat-ephem-table]. The NAIF constants kernel gives Pluto a radius of 1188.3 km and Charon 606 km [@sats-naif-pck00011]. Cartes du Ciel's Charon is Tholen's 1985 model. It uses a 19,130 km semi-major axis, a period of 6.38723 days, an inclination of 94.3 degrees and a node of 223.7 degrees [@sats-skychart-plansat]. Miriade lists no Charon ephemeris (2026 October) [@sats-miriade-ephemcc-output].

## Mars: Phobos and Deimos

From the surface of Mars, [Phobos](https://en.wikipedia.org/wiki/Phobos_(moon)) and Deimos transit the Sun. The Mars Exploration Rovers recorded such events, reported by Bell and colleagues in 2005 [@sats-bell-2005]. No result from that paper is quoted here. IMCCE's campaign pages list no campaign for mutual events of Phobos and Deimos [@sats-imcce-phemu-campaign].

Positions come from four different models. JPL assigns MAR099, which covers 1600 to 2600 on [DE440](../../10-shared/08-lunar-and-solar-model/ephemerides.md) [@sats-jpl-sat-ephem-table] [@sats-naif-aa-summaries]. Stellarium uses Lainey's "Ephemerides of the Martian satellites (adjustement from 1877 to 2005, Version 1.0)" [@sats-stellarium-marssat]. Cartes du Ciel uses Sinclair (1989), A&A 220, 321 [@sats-skychart-plansat]. Miriade labels Phobos "INPOP19 + LTE-SAI" [@sats-miriade-ephemcc-output].

## Theories by system and program

| System | JPL ([Horizons](https://ssd.jpl.nasa.gov/horizons/), [SPICE](https://naif.jpl.nasa.gov/naif/)) | IMCCE Miriade | Stellarium | Cartes du Ciel |
|---|---|---|---|---|
| Mars | MAR099 | LTE-SAI | Lainey MarsSat 1.0 | Sinclair 1989 |
| Saturn | SAT441, SAT415 | LTE-NOE | TASS 1.7 | TASS |
| Uranus | URA182 | LTE-NOE | GUST86 | GUST86 |
| Neptune (Triton) | NEP097 | LTE-SAI | none dedicated | Jacobson 1990 |
| Pluto (Charon) | PLU060 | not found | none dedicated | Tholen 1985 |

Sources: [@sats-jpl-sat-ephem-table] [@sats-miriade-ephemcc-output] [@sats-stellarium-ephemwrapper] [@sats-skychart-plansat]. Jupiter's Galilean satellites are covered in [the Jupiter satellite topic](../15-jupiter-satellites/_index.md).

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Arlot, Lainey and Thuillot 2006 | The 2007 prediction method, the two-model error estimate, and the eclipse [light-time](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) convention |
| Hidas et al. 2008, Christou et al. 2009 | Observed results of the 2007 season: precision and a systematic lag against predictions |
| Arlot, Dumas and Sicardy 2008 | An adaptive-optics observation on an 8 m class telescope |
| Binzel et al. 1985 | The detection of the Pluto-Charon events and the list of quantities they determine |
| PHEMU Technical Note 9 | A compact history of the Pluto-Charon season and of the Saturnian events before 1997 |
| JPL satellite ephemeris table | The current JPL file per satellite with its published reference |
| Stellarium and Cartes du Ciel sources, Miriade headers | Which theory each program actually evaluates |

## What a developer should do

1. **Use the JPL file per system through SPICE:** URA182, NEP097, PLU060, MAR099, with DE440. Check the file's span against the dates needed [@sats-jpl-sat-ephem-table] [@sats-naif-aa-summaries].
2. **Do not rely on GUST86 for Uranian event prediction.** Its inclinations are the quantity the 2007 events tested, and they disagreed with a newer fit by up to 500 km [@sats-arlot-2006-uranus].
3. **Publish predictions from two independent ephemerides** and show their difference, as IMCCE did for Uranus in 2007 and for Saturn in 2009 [@sats-arlot-2006-uranus] [@sats-arlot-thuillot-2008].
4. **Include limb darkening and an albedo model** when reducing mutual-event light curves, or expect radius and position biases of the Pluto-Charon kind [@sats-young-binzel-1994] [@sats-arlot-2012-phesat09].
5. **Read first:** Arlot, Lainey and Thuillot 2006, then Christou et al. 2009.

## What this changes

Nothing in the solar-eclipse pipeline. For the extended corpus, the Uranian and Pluto-Charon cases add one requirement: an event predictor must carry the uncertainty of the satellite ephemeris through to the event list, because whole events can appear or vanish between models.

## Open questions

- **PHEURA07 results paper.** Obtain IMCCE's consolidated reduction of the 2007 Uranian mutual events with O − C against GUST86, LA06 and a JPL ephemeris, if published.
- **Bell et al. 2005.** Read Nature 436, 55 for the rover-observed transit timings of Phobos and Deimos and the orbit offsets they implied.
- **Pluto-Charon originals.** Obtain Young and Binzel 1994 (Icarus 108, 219) and Buie, Tholen and Horne 1992 (Icarus 97, 211) to replace the secondary account with the papers' own numbers.
- **Mallama's satellite-eclipse models.** Obtain the papers Arlot and Thuillot cite as Mallama (2000, 2007a, 2007b) for the Neptunian and Uranian eclipse models.
