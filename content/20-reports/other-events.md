---
title: Lunar eclipses, occultations and transits
description: How one shadow geometry serves lunar eclipses, occultations by the Moon and minor bodies, planetary transits and satellite phenomena, and what each event adds.
order: 6
status: working
updated: 2026-10-17
seo_title: Lunar Eclipse, Occultation and Transit Calculation Compared
---

::: summary
- **Every event in this corpus is one body hiding another from a third.** A source, an occulter and a receiver define a [?fundamental-plane] perpendicular to the source direction. The contacts are the roots of one quadratic in time on that plane [@bes-es1961] [@bes-chauvenet-1863].
- **The shadow is a cone for an extended source and a cylinder for a star.** Solar eclipses, transits and satellite eclipses use cones. Lunar and minor-body occultations of stars use a cylinder whose radius is the occulter's radius [@occ-es1961] [@mb-gomes-junior-2022-sora].
- **Each event has one dominant input that is a convention or a model, not a constant of nature.** It is the shadow enlargement rule for lunar eclipses, the lunar limb for grazes, the solar and planetary radii for transits, the satellite ephemeris for Jupiter and Saturn, and the orbit of the body for asteroid occultations [@lun-herald-sinnott-2014] [@limb-occult-accuracy-2016] [@tr-eso-eis-b1] [@sats-arlot-2012-phesat09] [@mb-ferreira-2022].
- **The published instant means different things.** Lunar eclipse contacts are geocentric. Transit contacts are tangencies of two discs. IMCCE's satellite phenomena are mid-events in TT. An occultation of a star is a single disappearance at one site [@lun-5mcle-tp2009] [@bes-es1961] [@jup-imcce-phenjupiter-readme] [@occ-es1961].
- **A general pipeline needs four additions to the solar one.** These are a star-catalogue stage, a satellite-ephemeris layer, a body model that can be oblate, ringed or partly transparent, and a reduction stage that turns an observed time into a residual.
:::

## The question

The solar pipeline in [pipeline design](pipeline-design.md) computes one
event: the Moon hiding the Sun from a place on the Earth. This page asks which
parts of that pipeline carry over to the other events of the same family, and
what each event adds. The raw research is in six topics:
[lunar eclipses](../10-raw/12-lunar-eclipses/_index.md),
[lunar occultations](../10-raw/13-lunar-occultations/_index.md),
[transits of Mercury and Venus](../10-raw/14-transits/_index.md),
[Jupiter's satellites](../10-raw/15-jupiter-satellites/_index.md),
[Saturn and the outer satellites](../10-raw/16-saturn-and-outer-satellites/_index.md) and
[occultations by planets and minor bodies](../10-raw/17-occultations-by-planets-and-minor-bodies/_index.md).

## One geometry

Bessel's construction needs three bodies. The **source** gives light. The
**occulter** casts the shadow. The **receiver** is where the observer stands.
The fundamental plane passes through the receiver's centre perpendicular to
the line from the source through the occulter. On that plane the occulter's
shadow is a circle of radius $L$, and the observer is a point $(\xi, \eta)$.
A contact is an instant at which the distance between the two equals $L$. For
a lunar eclipse the roles turn round: the Moon is the moving point and $L$ is
a limiting separation between the Moon's centre and the shadow axis
[@bes-es1961].
With relative position $(u, v)$ and relative motion $(u', v')$, the 1961
Explanatory Supplement solves this as

$$
t = \frac{L\cos\psi}{n} - \frac{uu' + vv'}{n^2}, \qquad \sin\psi = \frac{uv' - u'v}{nL},
$$

with $n^2 = u'^2 + v'^2$ and $\cos\psi$ negative at ingress [@bes-es1961]. The
Supplement's occultation section solves the same quadratic by iteration, and
Chauvenet gives the same geometry [@occ-es1961] [@bes-chauvenet-1863].

The events differ in four places:

1. **What the source is.** The Sun is an extended disc, so the shadow is a
   cone with an umbra and a penumbra. A star is a point at infinity, so the
   shadow is a cylinder of the occulter's radius. For lunar occultations the
   cylinder radius is $k$, the Moon's radius in Earth equatorial radii
   [@occ-es1961].
2. **What the occulter is.** The Moon has a limb profile. Jupiter and Saturn
   are oblate, and Saturn has rings that pass part of the light. A minor body
   has an unknown shape that the occultation measures [@jup-thuillot-1983]
   [@sats-nssdc-rings] [@mb-herald-2020].
3. **Where the receiver is.** For a solar eclipse, a transit or an occultation
   the receiver is an observer on the Earth, so the time depends on the site.
   For a lunar eclipse the receiver is the Moon, and every observer sees the
   same instant. For a satellite eclipse the receiver is the satellite, and
   the Earth sees the result after a light-time [@lun-5mcle-tp2009]
   [@jup-thuillot-1983]. The receiver can also be a spacecraft or a rover.
   Its state vector then comes from its own SPICE kernel, and SPICE's
   occultation search accepts any observer [@sw-spice-gfoclt]. Transit
   timings from the SOHO and SDO spacecraft [@tr-emilio-2012] therefore
   need predictions for the spacecraft's position, not the Earth's centre.
4. **What the reported instant is.** See
   [the event definitions](#what-the-published-instant-means).

## The events compared

| Event | Source | Occulter | Shadow | Receiver | Dominant input | Achievable accuracy | Topic |
|---|---|---|---|---|---|---|---|
| Solar eclipse | Sun | Moon | Cone | Observer | Lunar limb and solar radius | About 0.2 s for contacts with a modern limb profile | [Lunar limb](../10-raw/05-lunar-limb/_index.md) |
| Lunar eclipse | Sun | Earth with atmosphere | Cone, enlarged | Moon | Enlargement rule | Umbral contacts to a few seconds against many observers, tens of seconds against one | [Lunar eclipses](../10-raw/12-lunar-eclipses/_index.md) |
| Lunar occultation of a star | Star | Moon | Cylinder of radius $k$ | Observer | Limb and event position angle | Most predictions within 0.3 s of video timings | [Lunar occultations](../10-raw/13-lunar-occultations/_index.md) |
| Lunar occultation of a planet | Planet disc | Moon | Cone with a small source | Observer | Planet outline and phase | Not quantified in the sources read | [Lunar occultations](../10-raw/13-lunar-occultations/planets-catalogues-and-reduction.md) |
| Transit of Mercury or Venus | Sun | Planet | Cone | Observer | Solar and planetary radii | Predictors agree to about 2 s | [Transits](../10-raw/14-transits/_index.md) |
| Galilean satellite phenomena | Sun or Jupiter | Jupiter or a satellite | Cone, oblate occulter | Satellite or observer | Satellite ephemeris | Mutual events give 5 to 50 mas | [Jupiter's satellites](../10-raw/15-jupiter-satellites/_index.md) |
| Saturnian satellite phenomena | Sun or Saturn | Saturn, rings or a satellite | Cone, oblate and ringed | Satellite or observer | Satellite ephemeris and ring transmission | Mutual events give about 20 mas | [Saturn and outer satellites](../10-raw/16-saturn-and-outer-satellites/_index.md) |
| Occultation of a star by a minor body | Star | Asteroid or TNO | Cylinder of the body's size | Observer | Body orbit and star position | About 10 mas with Gaia EDR3 | [Planets and minor bodies](../10-raw/17-occultations-by-planets-and-minor-bodies/_index.md) |
| Mutual events at Uranus and Pluto | Sun or satellite | Satellite or Pluto | Cone | Satellite or observer | Satellite ephemeris and light-curve model | Formal uncertainties below 0.01 arcseconds at Uranus in 2007 | [Saturn and outer satellites](../10-raw/16-saturn-and-outer-satellites/uranus-pluto-and-others.md) |
| Occultation of one planet by another | Farther planet | Nearer planet | Cone | Observer | Planet radii and ephemeris | Published times for 2065 disagree by more than two minutes | [Planets and minor bodies](../10-raw/17-occultations-by-planets-and-minor-bodies/planets-satellites-and-mutual-planetary-occultations.md) |

The accuracy column quotes each topic's own figures. For solar eclipses the
figure is the limb-corrected contact accuracy [@limb-eclipsewise-limb]. For
lunar eclipses it is the scatter of crater timings about a given enlargement
rule, which falls with the number of observers [@lun-herald-sinnott-2014]. For
lunar occultations it is Herald's comparison with video timings
[@limb-occult-accuracy-2016]. For transits it is the agreement between
Espenak and the IAA for the 2016 and 2019 Mercury transits
[@tr-ew-tm2016] [@tr-iaa-2016]. For the satellites it is the rms O−C of
mutual-event astrometry [@jup-saquet-2018] [@sats-arlot-2012-phesat09]. For
minor bodies it is the astrometric precision of a fitted occultation
[@mb-ferreira-2022]. For Uranus it is the mutual-event astrometry of 2007
[@sats-christou-2009]. For planet-planet occultations it is the spread
between published lists for the 2065 Venus and Jupiter event
[@mb-gray-mutual] [@mb-bogan-mutual]. These numbers measure different things and cannot be
ranked against each other.

## What the published instant means

A pipeline that compares its output with a published table must use the same
definition of the instant.

- **Solar eclipse and transit contacts** are tangencies of two discs, external
  or internal [@bes-es1961].
- **Lunar eclipse contacts** P1, U1, U2, U3, U4 and P4 are tangencies of the
  Moon's disc with the enlarged penumbra or umbra, computed at the Earth's
  centre. They are the same instant for every observer
  [@lun-5mcle-tp2009].
- **A lunar occultation of a star** is the instant the star's direction meets
  the limb, at one site. A smooth-limb prediction and a limb-corrected
  prediction differ by the limb height divided by the limb rate
  $kn\cos\psi$ [@occ-es1961].
- **Galilean satellite phenomena in IMCCE's tables** are mid-events in TT.
  An eclipse is timed at half flux. Occultations, transits and shadow transits
  are timed when the satellite or its shadow is bisected by the limb
  [@jup-imcce-phenjupiter-readme]. The first or last visible part of the
  satellite can be 1 to 15 minutes away, depending on the satellite
  [@jup-westfall-alpo].
- **Phenomena of Saturn's satellites** in the 1996 Bureau des longitudes
  booklet are timed at the satellite's centre [@sats-imcce-1996-booklet]. The
  2009 tables of eclipses by Saturn give a maximum and a half-duration, and
  the mutual-event tables give contacts [@sats-arlot-thuillot-2008].
- **A stellar occultation by a minor body** is a pair of disappearance and
  reappearance times per chord, with Fresnel diffraction and the star's
  diameter in the light curve [@mb-gomes-junior-2022-sora].

## What generalises in the pipeline

The [pipeline design](pipeline-design.md) has nine stages. All nine carry over
in some form, and the other events add a tenth.

1. **Stage 1, ephemeris, orientation and time.** The planetary ephemeris and
   the time scales stay. Compute in TT and convert to UT1 only at output. Two
   layers join the ephemeris: a star catalogue with epoch propagation of Gaia
   DR3 positions, and satellite ephemerides delivered as SPICE kernels
   consistent with DE440, such as JUP365 for Jupiter and SAT441 for Saturn
   [@occ-gaia-dr3-propagation] [@jup-naif-jup365-cmt] [@sats-naif-sat441-cmt].
   Record the kernel pair with every result. The body model grows as well. The
   occulter can be an oblate spheroid, a body with rings, or a body whose
   atmosphere sets the edge. Saturn's ring B is close to opaque and ring C is
   not [@sats-nssdc-rings]. JPL Horizons models the planet as a sphere of the
   equatorial radius for these events [@sw-horizons-manual].
2. **Stage 2, enumeration and provisional type.** The same search for a
   syzygy near a node finds lunar eclipses and transits. Lunar eclipses use
   Meeus's closed form with changed coefficients [@cat-meeus-1991-aa].
   Transits need an inferior conjunction near the planet's node [@tr-es1961].
   Satellite phenomena need a seasonal gate on the planetocentric latitudes of
   the Earth and the Sun [@sats-arlot-thuillot-2008].
3. **Stage 3, Besselian elements.** The cone code takes a cylinder as a limit,
   with $l_1 = l_2 = k$ and both cone angles zero for a star [@occ-es1961]. For
   a lunar eclipse the elements shrink to $x$, $y$ and three limiting
   separations $L_1$, $L_2$ and $L_3$, which are set by an atmospheric
   enlargement rule [@bes-es1961]. Chauvenet, Danjon and Herald and Sinnott
   give different values, and the choice moves umbral contacts by 20 to
   30 seconds and penumbral contacts by about 1.5 minutes
   [@lun-herald-sinnott-2014] [@lun-nasa-shadow-page]. One contact solver
   serves every event if $L$ is an input built from explicit radii: $k$, the
   solar semidiameter, the planet's semidiameter, the occulter's radius or the
   lunar-eclipse separation [@bes-es1961].
4. **Stage 4, global circumstances.** Paths and limit lines carry over to
   occultations of stars, where the limit is a graze line, and to minor-body
   occultations, where the path width is the body's diameter
   [@bes-chauvenet-1863] [@mb-gomes-junior-2022-sora]. A lunar eclipse has no
   path.
5. **Stage 5, partial-eclipse maps.** For a lunar eclipse the map is a
   horizon map of where the Moon is up at each contact. ΔT moves it by
   1 degree of longitude per 240 seconds of ΔT [@lun-5mcle-tp2009].
6. **Stage 6, local circumstances.** Site-dependent for transits and
   occultations as for solar eclipses. Transit tables also publish a
   three-constant reduction formula per contact [@tr-iaa-2019].
7. **Stage 7, terrain.** Shared with lunar occultations, where the observer's
   height shifts a graze line by $h\tan z$ toward the Moon's azimuth
   [@occ-iota-manual-2007].
8. **Stage 8, lunar limb.** Shared unchanged between solar eclipses and lunar
   occultations. A graze uses the same limb test, and Morrison required the
   event position angle to 0.01 degrees [@occ-morrison-1979]. An error of
   about 0.2 degrees in Occult's position angle once degraded its graze
   profiles [@limb-occult-accuracy-2016].
9. **Stage 9, products and uncertainty.** Each product gains the conventions
   in the next section. Minor-body paths gain a cross-track uncertainty from
   the orbit covariance [@mb-tanga-delbo-2007].
10. **A new stage, reduction.** An observed time becomes a residual against
    the prediction. Occultation residuals measure ΔT, lunar-eclipse crater
    timings measure the shadow layer, and chord timings measure an asteroid's
    size and position [@cat-stephenson-2016] [@lun-herald-sinnott-2014]
    [@mb-herald-2020].

## Conventions to carry as metadata

Each of these choices changes the output and none of them is fixed by
nature. A result without them cannot be compared.

| Convention | Events | Values in use | Effect |
|---|---|---|---|
| Shadow enlargement | Lunar eclipses | Chauvenet 1.02, Danjon 1.01 on the lunar parallax, Herald and Sinnott 87 km | 0.005 in umbral magnitude, 20 to 90 seconds in contacts [@lun-herald-sinnott-2014] |
| Lunar radius $k$ | Solar eclipses, lunar eclipses, occultations | 0.272281 for umbral contacts and 0.2724880 or 0.2725076 for penumbral contacts in NASA's solar tables, 0.2724880 in the lunar Canon, 0.2725 for occultation prediction, 0.2725076 adopted by the IAU in 1982 | Smooth-limb times and durations [@bes-nasa-radius] [@lun-5mcle-tp2009] [@occ-es1961] [@occ-es1992] |
| Solar radius $s_0$ | Solar eclipses, transits | 959.63 and 959.95 arcseconds | 3.3 to 6.5 seconds per transit contact for that gap, computed from the Supplement's solution with published elements [@tr-es1961] [@tr-eso-eis-b1] [@tr-ew-tm2019] |
| Venus semidiameter | Venus transits | 8.34 and 8.41 arcseconds at 1 au | About 5 seconds per contact [@tr-eso-eis-b1] [@cat-meeus-1991-aa] |
| Satellite theory | Planetary satellites | Lieske E5, Lainey L1 and NOE, JPL JUP365 and SAT441, TASS 1.7 | Tens of milliarcseconds, and grazing events can appear or vanish between theories [@sats-arlot-2012-phesat09] [@sats-arlot-2006-uranus] [@sats-arlot-thuillot-2008] |
| Event definition | Satellite phenomena | Mid-event, satellite centre, first or last light | Minutes [@jup-westfall-alpo] |
| Longitude sign | Transits, occultations | West-positive in the 1961 Supplement, east-positive in the IAA and RASC tables | Inverts the local correction if mixed [@tr-iaa-2016] [@limb-dunham-rasc-2026] |
| Uncertainty level | Minor-body paths | JPL Horizons gives 3-sigma | Divide by 3 for 1-sigma path lines [@sw-horizons-manual] |

## What a developer should do

Build the contact solver once, with $L$ and the shadow shape as inputs, and
test it on the 1961 Explanatory Supplement's worked examples for eclipses,
transits and occultations [@bes-es1961] [@tr-es1961] [@occ-es1961]. Then add the events in
the order of how much new machinery each needs:

1. **Transits** need only a planet radius and a second semidiameter. Test
   against the Supplement's 1960 examples and the IAA city tables
   [@tr-es1961] [@tr-iaa-2019].
2. **Lunar eclipses** need an enlargement rule and a horizon map. Test against
   the NASA catalogue with Danjon's rule, then against crater timings in
   VizieR VI/140 with Herald and Sinnott's rule [@lun-5mcle-tp2009]
   [@lun-vizier-vi140].
3. **Lunar occultations** need a star catalogue and the cylinder mode. Grazes
   reuse the limb stage. Test against the VI/132C archive
   [@occ-vizier-vi132c].
4. **Satellite phenomena** need satellite kernels, an oblate occulter and
   separate light-time paths from the Sun and to the Earth
   [@jup-thuillot-1983]. Test against IMCCE's published tables with the same
   event definition [@jup-imcce-phenjupiter-readme].
5. **Minor-body occultations** need orbit covariance mapped to a cross-track
   uncertainty, and a diffraction light-curve model for reduction. SORA is the
   documented open implementation [@mb-sora-code].

## Open questions

- Occult's help file is the missing source in four topics: its lunar eclipse
  enlargement rule, its graze binning, its treatment of planet phase in lunar
  occultations, and its asteroid elements. The program is closed source and
  its help is distributed only with the installer [@sw-occult4].
- Meeus's *Transits* (1989) underlies the NASA transit catalogues and was not
  read [@tr-nasa-mercury-catalog].
- The current Astronomical Almanac sections on lunar eclipses, occultations
  and satellite phenomena would establish its present enlargement rule and
  satellite theory.
- The altitude in Jupiter's atmosphere at which a satellite eclipse reaches
  half flux is not stated in any source read [@jup-imcce-phenjupiter-readme].
- No public tool examined models the transmission of Saturn's rings in
  satellite eclipses [@sats-nssdc-rings].
