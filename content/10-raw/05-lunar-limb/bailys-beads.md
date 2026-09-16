---
title: Baily's beads
description: How bead events are defined and predicted from the limb profile, how IOTA has used them since 1979 to measure the solar radius, and what the solar-limb definition does to the result.
order: 3
status: working
updated: 2026-09-15
tags: [bailys-beads, solar-radius, iota, occult, limb-profile]
---

::: summary
- **A bead is a valley on the limb profile that the Sun's limb has not yet cleared.** Its appearance or disappearance is the instant the solar limb, drawn with Herald's curve $h = 960''(M-1)(1-\cos C)$, passes the valley floor. Here $C$ is the angle from the contact point, Espenak's symbol. Herald writes $P$, which is not the position angle [@limb-herald-1983].
- **Prediction is a by-product of the contact-time correction**: the same tangency search that gives C2 and C3 gives, for each bin of the profile, the time the Sun's limb reaches it, and Occult, Solar Eclipse Maestro and the SVS raster method all produce bead sequences this way [@limb-espenak-tp2001] [@limb-jubier-sem-beads-window] [@limb-svs-5365].
- **IOTA's edge method (1979 onward)** stations observers 1 to 3 km inside each path limit, where beads last a minute or more, times each bead to 0.5 s, identifies it with a limb feature, and solves for the apparent solar radius and the Moon's position, needing both edges to separate the two [@limb-fiala-dunham-sofia-1994] [@limb-eclipsetours-edge].
- **Results** are corrections to the 959.63 arcsecond standard radius of a few hundredths to a few tenths of an arcsecond per eclipse, for example $+0.48 \pm 0.2''$ for 1715 and $-0.11 \pm 0.05''$ for 1979, with the reductions depending on the limb data used [@limb-fiala-dunham-sofia-1994].
- **The Kaguya (SELENE) and LOLA profiles moved the limiting error from the Moon to the Sun**: with a 1 m limb the open question is where the photospheric edge is, and bead light curves show light at least 0.65 arcseconds beyond the limb-darkening inflection point [@limb-raponi-sigismondi-2011-ldf].
- **Beaded and broken annular phases** exist wherever the limb's range of heights exceeds the Sun-Moon size difference. Wright and Young map them with the criterion $\max(L) - \min(L) > \delta$ and simulate one in real time for 2005 April 8 [@limb-wright-young-2024] [@limb-svs-5365].
:::

**The question.** How is a Baily's bead event defined in terms of the limb profile and the solar radius, how do the implementations predict bead sequences, and how has the reverse problem, using observed beads to measure the Sun, been done?

## The definition of a bead event

Espenak describes the phenomenon at the path limits: "an observer positioned here will witness a slender solar crescent that is fragmented into a series of bright beads and short segments whose morphology changes quickly with the rapidly varying geometry between the limbs of the Moon and the Sun. These beading phenomena are caused by the appearance of photospheric rays that alternately pass through deep lunar valleys and hide behind high mountain peaks as the Moon's irregular limb grazes the edge of the Sun's disk. The geometry is directly analogous to the case of grazing occultations of stars by the Moon" [@limb-espenak-tp2001]. SVS puts it in one sentence: "bright pinpoints of sunlight peeking through lunar valleys along the silhouette edge of the Moon during a solar eclipse" [@limb-svs-5365].

In profile terms, on an exaggerated radial chart the Sun's limb near the contact point is the curve $h = 960''(M-1)(1-\cos C)$ above the mean lunar limb, with $M$ the magnitude and $C$ the angle from the nominal contact, Espenak's symbol. Herald writes that angle $P$, which is not the position angle [@limb-herald-1983]. A bead exists at position angle $\theta$ at time $t$ when the limb height $\Delta(\theta)$ is below the solar limb curve displaced to its position at $t$, that is, when the valley floor is inside the Sun's disk while its neighbouring peaks are outside. The bead disappears when the moving solar limb drops below the valley floor, and reappears at third contact in the reverse sense. Second contact of a total eclipse is the disappearance of the last bead, and Herald's "operation may be used for predicting the formation and location of Baily's beads" as well as the contacts [@limb-espenak-tp2001]. Wright and Young formalise the same test at every time step: a limb element at angular radius $a$ and position angle $\theta$ is inside the solar disk of unit radius when $\rho = a^2 + \delta^2 - 2a\delta\cos(\theta - \varphi) < 1$, and any element with $\rho < 1$ is a bead [@limb-wright-young-2024].

![A bead is the gap between the Sun's limb curve and a valley floor, so the beads go out one by one as that curve sinks, and second contact is the instant the last of them closes [@limb-herald-1983] [@limb-espenak-tp2001].](img/bailys-beads.svg)

The depth of the valley sets the bead's size and lifetime. IOTA's field guide states that large beads come from valleys 1 to 2 km deep and small ones from 50 to 200 m features, and that at the path edge beads persist "a full minute or more" against seconds near the central line [@limb-eclipsetours-edge]. Espenak notes that "the most dynamic beading phenomena occurs within 1.5 arc-seconds of the Moon's limb," about 3 km inside the interior limit [@limb-espenak-tp2001].

## Predicting beads

**Occult 4.** Herald's program computes bead sequences from the Watts, Kaguya (SELENE) or LOLA profile. Sigismondi's group used its "Baily's beads software" to script the observing sequence for an annular eclipse, and reduced the 2005 to 2008 bead atlas with the Watts profile in Occult 4, identifying each event by Watts angle [@limb-sigismondi-thesis-2011] [@limb-sigismondi-beads-atlas-2009]. The Sri Lankan 2010 reduction states that "the limb profile used in Occult 4 software is updated from Kaguya lunar explorer data" [@limb-gunasekera-2011-ipsl]. Occult's documentation of the bead algorithm itself was not found online. The graze-profile machinery, which selects the LOLA HiRes profile and plots events against distance from the limit line, is the documented part [@limb-iota-2026-predictions].

**Solar Eclipse Maestro.** The Baily's Beads Study window draws the LRO profile with the Sun behind it as seen from the observer at second contact, maximum or third contact [@limb-jubier-sem-beads-window]. A time slider moves the Sun's limb across the terrain. Heights are in arcseconds against the IAU mean radius 1738.091 km, corrected contacts are marked C2' and C3', and the profile for the current topocentric libration can be exported as text [@limb-jubier-sem-beads-window]. The program's eclipse simulation includes the beads [@limb-jubier-sem-limb-window].

**NASA SVS.** The 2024 simulation of beads for the 2005 April 8 hybrid eclipse, from 94.02587 W, 6.45677 N between 21:55:20.5 and 21:55:35.5 UTC, is the raster method run in real time at one site with SLDEM2015 and DE421 [@limb-svs-5365]. The paper adds a map criterion for the broken annular phase. Where $\max(L) - \min(L) > \delta$, the spread of limb heights exceeds the separation of the two disks in solar radii, so no complete ring and no complete totality is possible [@limb-wright-young-2024]. It finds the 2005 hybrid "flanked by more than 1300 and 730 km of broken annularity" and the 1894 April 6 eclipse broken annular for about two hours over nearly 5400 km [@limb-wright-young-2024]. Herald had described the same phase in 1983 as "partial annularity," with an interior locus for an eclipse of magnitude $2 - M$ bounding it, and reported that observers near but inside the 1981 February 4 limits confirmed the approach [@limb-herald-1983].

## IOTA's use of beads for the solar radius

The idea is that at the edge of the path the geometry is a grazing occultation of an extended source. Fiala, Dunham and Sofia describe it: "Observers station themselves along the predicted edges of the track of the umbra at a solar eclipse. The observations consist of timings of the formation and disappearance of individual Baily's Beads. Each timing is actually a measurement of the direction in space of a point on the apparent limb of the Sun. It is compared to a predicted sequence of Bead phenomena based on the calculated limb of the Moon for that instant as seen from each site, and identification made with a known limb feature (mountain peak or valley). As long as the position of each observing site is known to an accuracy within 50 feet, the only adjustable parameters in the calculation that affect the predicted times are the apparent diameter of the Sun, and the Sun's position relative to the Moon. ... Timings from both edges of the predicted path are required in order to separate the effects of a change in the width of the path from a shift in its longitude" [@limb-fiala-dunham-sofia-1994]. Herald 1983 makes the same point: near the limits "the number of Baily beads present at maximum eclipse will be very sensitive to the location of the observer relative to the shadow axis, thus providing a sensitive measurement of the location of the eclipse limit" [@limb-herald-1983].

The programme began in 1979 [@limb-fiala-dunham-sofia-1994], with the first result in Science in 1980 [@limb-dunham-1980-science]. Equipment progressed from 8 mm film and audio tape to video, positions from topographic maps to GPS, and time signals from radio broadcasts corrected for ΔT with USNO data [@limb-fiala-dunham-sofia-1994]. Current practice: video with a GPS or shortwave time base, timing to 0.5 s, site position to 30 m horizontally and 20 m in elevation, stations 1 to 3 km inside the path limit [@limb-eclipsetours-edge].

The reduction plots, for each bead, the Watts angle against the residual in arcseconds between the solar limb and the lunar limb, as in Fiala's Figure 1 for 1984 May 30, where "Bead forms" is marked where the two curves meet [@limb-fiala-dunham-sofia-1994]. Table II of that paper lists, per eclipse, the solar radius correction to the standard 959.63 arcseconds together with corrections to the Moon's ecliptic longitude and latitude [@limb-fiala-dunham-sofia-1994]. The radius corrections are:

- 1715 May 3, $+0.48 \pm 0.2''$ from 3 observations
- 1925 Jan 24, $+0.51 \pm 0.08''$ from 8
- 1976 Oct 23, $+0.04 \pm 0.07''$ from 43
- 1979 Feb 26, $-0.11 \pm 0.05''$ from 47
- 1980 Feb 16, $-0.03 \pm 0.03''$ from 232
- 1981 Feb 4, $-0.02 \pm 0.03''$ from 153
- 1983 Jun 11, $+0.09 \pm 0.02''$ from 201
- 1984 May 30, $+0.23 \pm 0.04''$ in the old analysis and $+0.09 \pm 0.04''$ re-reduced with DE200/LE200, from 51
- 1987 Sep 23, $-0.11 \pm 0.03''$ from 123

The re-reduction changed about a third of the feature identifications and moved the correction "from the ephemeris to the solar diameter" [@limb-fiala-dunham-sofia-1994]. The paper states that "the precision and accuracy of the observations depends upon Watts' limb profile data" [@limb-fiala-dunham-sofia-1994].

With the Kaguya profile, Gunasekera et al. reduced southern-limit beads of the 2010 January 15 annular eclipse in Sri Lanka to a correction of $+0.26 \pm 0.18''$, giving 959.89 ± 0.18 arcseconds [@limb-gunasekera-2011-ipsl]. Sigismondi's guidelines paper describes two reduction procedures, one on limb heights and one on times, for beads read from central-eclipse video with a known limb profile. The paper was not read and this description is from its abstract [@limb-sigismondi-2009-guidelines].

## The solar-limb definition

Once the lunar profile is known to a metre, the radius result depends on what "the edge of the Sun" means. Herald's 1983 error budget already listed "uncertainty in the definition of the actual surface of the Sun," quoting a maximum radial brightness gradient of 7.0 magnitudes per arcsecond at the limb and estimating a probable error under 0.3 s on the central line from this cause [@limb-herald-1983]. Raponi and Sigismondi adopt the [?ldf-inflection|inflection point of the limb darkening function] as the limb [@limb-raponi-sigismondi-2012]. They use the light curve of a single bead together with the Kaguya profile to reconstruct the outer part of that function. Their 2010 January 15 videos show "light from solar limb detected at least 0.65 arcsec beyond the LDF inflection point," and they say this requires re-evaluation of naked-eye historical eclipse timings [@limb-raponi-sigismondi-2011-ldf]. This is why Jubier's tools state both the IAU 1976 value of 959.63 arcseconds that the computation uses and the 959.98 ± 0.02 arcsecond "true photospheric" value [@limb-jubier-map-help], and why Wright and Young note that recent eclipse observations put the radius between 959.95 and 960.01 arcseconds while their maps use 959.63 [@limb-wright-young-2024]. A bead prediction is only as good as the radius it assumes. Near a path limit 0.03 arcseconds is one second of duration, and on the central line about 0.2 arcseconds is one second, as [Effect of the radius on eclipse products](../06-solar-radius/effect-on-eclipse-products.md) sets out [@limb-wright-young-2024].

## Sources compared

| Source | Bead definition | Profile used | Unique content |
|---|---|---|---|
| Herald 1983 [@limb-herald-1983] | Solar limb curve tangent to valley | Watts via Duncombe | The chart method, partial annularity, sensitivity of bead count to position |
| Espenak TP 2001 [@limb-espenak-tp2001] | Photospheric rays through valleys | Corrected Watts | Interior limit as no beads over ±30°, exterior as 60° crescent, 1.5" dynamic zone |
| Fiala, Dunham, Sofia 1994 [@limb-fiala-dunham-sofia-1994] | Timed formation and disappearance | Watts | The IOTA method statement, Table II results 1715 to 1987, 50 ft site accuracy |
| Wright and Young 2024 [@limb-wright-young-2024] | Limb element with ρ < 1 | SLDEM2015 | Broken-annular criterion and extents, real-time simulation |
| Solar Eclipse Maestro [@limb-jubier-sem-beads-window] | Sun drawn behind LRO profile | LRO | Interactive time slider, profile export |
| Raponi and Sigismondi [@limb-raponi-sigismondi-2011-ldf] | Bead light curve versus LDF | Kaguya | 0.65" excess beyond the inflection point |
| Gunasekera et al. 2011 [@limb-gunasekera-2011-ipsl] | Occult 4 bead times | Kaguya in Occult 4 | A Kaguya-era radius result, +0.26 ± 0.18" |

## What a developer should do

Generate beads from the same limb table and the same time-stepped test used for the contacts, and report each bead with its position angle, its valley depth in arcseconds, and its formation and disappearance times for the assumed solar radius. Make the solar radius a parameter and expose the sensitivity, which is one second per 0.03 arcseconds at a path limit and one second per about 0.2 arcseconds on the central line [@limb-wright-young-2024]. For an IOTA-style reduction, invert the same model: hold the profile fixed, fit the solar radius and a two-component shift of the Moon, and require observations from both limits. Read Fiala, Dunham and Sofia 1994 for the method statement and Herald 1983 for the error budget before designing the fit.

## What this changes

Bead prediction adds no new data or geometry to the pipeline beyond the limb stage already required for contacts. It does force the solar radius to be an explicit input, because bead timing is where the almanac value and the observed value disagree by more than the limb error.

## Open questions

- Obtain Sigismondi 2009 and the 2005 to 2008 bead atlas to document the two reduction procedures and the Watts-angle identification scheme in detail [@limb-sigismondi-2009-guidelines] [@limb-sigismondi-beads-atlas-2009].
- Obtain Dunham et al. 1980 Science for the original edge-observation reduction [@limb-dunham-1980-science].
- Obtain a bead sequence exported from Occult 4 and one from Solar Eclipse Maestro for the same site and eclipse, to compare their event definitions and their assumed solar radius.
- Obtain the SVS 5365 frame set and reproduce the 2005 April 8 bead sequence from SLDEM2015 with the ρ test as a validation case [@limb-svs-5365].
- Obtain a post-2010 IOTA solar-radius solution reduced with a LOLA profile rather than Kaguya (SELENE) or Watts, for example a Journal for Occultation Astronomy paper on the 2023 or 2024 bead campaigns. None was found in the searches run for this note.
