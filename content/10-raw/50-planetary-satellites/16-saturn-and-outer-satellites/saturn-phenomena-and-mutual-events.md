---
title: Phenomena and mutual events of Saturn's satellites
seo_title: Saturn's Moons: Eclipses, Transits and Mutual Events
description: How eclipses, occultations, transits, ring eclipses and mutual events of Saturn's satellites are predicted, when they occur, and what PHESAT observed.
order: 2
status: working
updated: 2026-10-17
tags: [saturn, mutual-events, phesat, titan, iapetus, ring-plane-crossing, eclipses]
---

::: summary
- **Most phenomena of Saturn's satellites are seasonal.** Transits, eclipses by the globe and [?mutual-event|mutual events] of Mimas to [Titan](https://en.wikipedia.org/wiki/Titan_(moon)) happen only near a [?sats-ring-plane-crossing]. Sun crossings came on 1995 November 19, 2009 August 10 and 2025 May 6, intervals of 13.72 and 15.74 years [@sats-rpx-dps-letter] [@sats-nasa-pia10563] [@sats-baa-2025-notes].
- **Iapetus is the exception.** Its orbit is inclined by about 15 degrees, so it is eclipsed by the globe and the rings only when Saturn is near one of its nodes, as in 1993 [@sats-soma-1992].
- **Published times refer to the satellite's centre.** The tables of the Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) give the instant the centre crosses the limb or shadow edge. Contact to contact takes 14 s for Mimas and 450 s for Titan on an equatorial track [@sats-imcce-1996-booklet].
- **An eclipse is computed as an occultation of the Sun seen from the eclipsed satellite,** with [light-time](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) from the Sun to that satellite, and contacts are taken with both the penumbral and umbral cones [@sats-arlot-2006-uranus] [@sats-arlot-thuillot-2008].
- **[Mutual events](../15-jupiter-satellites/mutual-events.md) are the most precise ground-based astrometry of these satellites.** The 2009 campaign gave 26 usable light curves and residuals of about 20 milliarcseconds, against 0.1 arcseconds, about 600 km, for direct imaging [@sats-arlot-2012-phesat09] [@sats-arlot-thuillot-2008].
- **Prediction accuracy is set by the ephemeris.** Times of maximum from TASS and from JPL's SAT252 differed by 10 to 30 s in 2009. For Iapetus's ring eclipse in 1993 two element sets differed by 11 to 32 minutes [@sats-arlot-thuillot-2008] [@sats-soma-1992].
- **Public tools simplify the planet.** [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) uses the equatorial radius with no oblateness or atmosphere and warns that satellite eclipse times may be off by a minute. None of Horizons, [SPICE](https://naif.jpl.nasa.gov/naif/) and [Stellarium](https://stellarium.org/) models the rings' optical depth [@sw-horizons-manual] [@sw-spice-gfoclt] [@sats-stellarium-planet].
:::

**The question.** Which phenomena of Saturn's satellites can be observed, when do they occur, how are their start and end instants defined and computed, and what accuracy do the published predictions and observations reach? The satellite theories behind these predictions are compared in [the theories note](saturn-theories-and-ring-geometry.md). The shared geometry with the Galilean satellites is in [the Jupiter satellite topic](../15-jupiter-satellites/_index.md).

## The phenomena

IMCCE's 1996 booklet lists the phenomena "similar to the well known phenomena of the Galilean satellites of Jupiter" [@sats-imcce-1996-booklet]:

- **Eclipses by Saturn**, when a satellite enters the planet's shadow. The booklet codes the start and end as Ed and Ef [@sats-imcce-1996-booklet].
- **Occultations by Saturn**, when a satellite passes behind the globe, coded Im for immersion and Em for emersion [@sats-imcce-1996-booklet].
- **Transits**, a satellite crossing in front of the disc, coded Pd and Pf [@sats-imcce-1996-booklet].
- **[?shadow-transit|Shadow transits]**, a satellite's shadow crossing the disc, coded Od and Of [@sats-imcce-1996-booklet].
- **Mutual occultations**, "the arrival of the disk of the occulting satellite on that of the occulted satellite" [@sats-arlot-thuillot-2008].
- **Mutual eclipses**, "the arrival of the eclipsed satellite in the shadow cone of the eclipsing satellite", which can be partial, annular or total [@sats-arlot-thuillot-2008].
- **Eclipses by the rings**, mainly of Iapetus, whose orbit lets it pass through the ring shadow away from the planet [@sats-soma-1992].

Arlot and Thuillot judge the science value of each type differently. Eclipses by the planet's shadow give positions whose accuracy is "similar to what is obtained with direct astrometric imaging". The planet's atmosphere degrades the timing, and the rings may pollute the photometry [@sats-arlot-thuillot-2008]. Occultations by the planet and transits "are difficult to analyze because it is impossible to model the figure of the planet with sufficient accuracy" [@sats-arlot-thuillot-2008]. Shadow transits "are not scientifically interesting but the transits of the shadow of Titan are spectacular" [@sats-arlot-thuillot-2008]. Mutual events are the valuable ones, because the satellites except Titan have no atmosphere [@sats-arlot-thuillot-2008].

## When they occur: ring-plane crossings and the equinox

The orbits of Mimas to Titan lie close to Saturn's equatorial plane. That plane is the ring plane. Mutual occultations therefore need the Earth near that plane, and mutual eclipses need the Sun near it [@sats-arlot-thuillot-2008]. "These planes correspond closely to the equatorial plane of Saturn. This occurrence takes place at the equinox on Saturn" [@sats-arlot-thuillot-2008]. The [?sats-planetary-equinox] is the Sun's crossing.

The Earth crosses the ring plane once or three times near each equinox. Seen from Saturn the Earth stays within a few degrees of the Sun. In 1995 to 1996 it was "up to 2.5 degrees above the ring plane while the sun is in or below the plane" [@sats-rpx-dps-letter]. The dates on record are [@sats-rpx-dps-letter] [@sats-arlot-thuillot-2008] [@sats-nasa-pia10563] [@sats-apod-2009-08-25] [@sats-baa-2025-notes] [@sats-imcce-phemu-campaign]:

| Season | Earth crossings | Sun crossing (equinox) |
|---|---|---|
| 1995 to 1996 | 1995 May 21, 1995 Aug 11, 1996 Feb 11 | 1995 Nov 19 |
| 2009 | 2009 Sep 4 | 2009 Aug 10 (Arlot and Thuillot predicted Aug 12) |
| 2025 | 2025 Mar 23 | 2025 May 6 (IMCCE gives May 7) |

NASA gives the 2009 Sun crossing as August 10 [@sats-nasa-pia10563] [@sats-apod-2009-08-25]. Arlot and Thuillot's 2008 prediction paper gives August 12 [@sats-arlot-thuillot-2008]. The intervals between Sun crossings are 13.72 years and 15.74 years, computed from the dates in the table's first position. Their sum, 29.46 years, is about one Saturnian year of 10,746.94 days, or 29.42 years [@sats-nssdc-saturn]. The two halves differ because Saturn's orbit is eccentric, with $e = 0.0520$ [@sats-nssdc-saturn]. IMCCE's own texts round both to "every 15 years" [@sats-arlot-2012-phesat09] [@sats-imcce-1996-booklet].

![Saturn's equinoxes alternate between a short and a long half of its orbit, 13.72 and 15.74 years apart, and the Earth crosses the ring plane once or three times near each [@sats-rpx-dps-letter] [@sats-nasa-pia10563] [@sats-arlot-thuillot-2008] [@sats-baa-2025-notes].](img/sats-crossing-timeline.svg)

The circumstances of a season depend on where Saturn is relative to the Sun. 1995 was favourable, with "the solar crossing and one of three earth crossings occuring within two months of opposition" [@sats-rpx-dps-letter]. In 2009 the equinox came "near the conjunction Saturn-Sun", so observations were possible "only before and after the equinox" [@sats-arlot-thuillot-2008]. In 2025 the Earth crossing came eleven days after the solar conjunction of March 12 [@sats-baa-2025-notes]. IMCCE predicted that the Saturnian mutual phenomena of this season would run from May 2024 to February 2026. It expected worse conditions than for Jupiter's 2026 equinox "due to the distance separating the equinox of the conjunction" [@sats-imcce-phemu-campaign].

Between an Earth crossing and a Sun crossing the two lie on opposite sides of the ring plane. The Earth then sees the unlit face, so the rings almost vanish. The 1995 periods were May 21 to August 11 and November 19 to February 11 [@sats-rpx-dps-letter]. The 2025 period was March 23 to May 6 [@sats-baa-2025-notes].

**Shadow transits of Titan.** Titan's orbit is inclined about 0.3 degrees to the equator [@sats-imcce-1996-booklet]. Its shadow therefore reaches the disc only for a year or so around each equinox. In 2009 shadow transits ran from 2009 February 24 to 2010 January 9 [@sats-arlot-thuillot-2008]. In 2025 observers of the British Astronomical Association (BAA) recorded Titan shadow transits on May 15 and 31, June 16, July 2 and 18, August 3 and 19, and September 4 and 20 [@sats-baa-2025-notes]. These are 16-day steps, Titan's period of 15.945 days [@sats-imcce-1996-booklet]. The May 15 shadow transit lasted from 09:34 to 15:42 UT [@sats-baa-2025-notes].

## Geometry of an event

### The shadows

The shadow cones of Saturn and of each satellite are built like the Moon's in a solar eclipse. An inner [?umbra] cone and an outer [?penumbra] cone come from the tangents to the Sun and the body (see [?shadow-cone] and [the fundamental plane note](../../10-shared/01-foundations/besselian-elements.md)). By similar triangles, the length of Saturn's umbra is $\ell_u = R_S\,d/(R_\odot - R_S)$, with $R_S$ Saturn's radius, $R_\odot$ the Sun's radius and $d$ the Sun-Saturn distance. With $R_S = 60{,}268$ km, $R_\odot = 696{,}000$ km and $d = 9.537$ au this is about $1.35\times 10^8$ km, or 2,240 Saturn radii [@sats-nssdc-saturn] [@sats-soma-1992]. Every satellite out to Iapetus at about 59 Saturn radii is far inside it [@sats-soniakeys-saturnmoons]. The Sun's angular radius at 9.54 au is 696,000 km divided by the distance, about 100.6 arcseconds. Over Titan's 1.22 million km from Saturn the penumbra is therefore about 1,190 km wide. These figures follow from the cited constants by the same similar-triangle construction.

Because Saturn is oblate, its shadow's cross-section is an ellipse whose shape depends on $B'$, the Sun's ring-opening angle from [the theories note](saturn-theories-and-ring-geometry.md#meeus-chapter-45-the-rings-aspect). Soma took Saturn's "size and shape" from Davies et al. (1989) and the ring dimensions from Esposito et al. (1984) [@sats-soma-1992].

### Light-time and the eclipse convention

Arlot, Lainey and Thuillot state the convention for mutual events: "For the eclipses, we do not consider that they are occultations as seen from the Sun because of the light-time, but that they are occultations of the Sun as seen from the eclipsed satellites. Therefore, we calculate the first and last contacts of the eclipsed satellite with the penumbral and umbral cones and the time of the minimum distance to the axis of the cones" [@sats-arlot-2006-uranus]. The relative positions are "calculated carefully taking the light-time into account" [@sats-arlot-2006-uranus].

For an occultation the [?light-time] runs from the satellites to the Earth. For an eclipse it runs from the Sun to the eclipsed satellite, and then the event is seen on the Earth one further light-time later. The difference matters. [Meeus](https://en.wikipedia.org/wiki/Jean_Meeus)'s light-time constant is 0.0057755183 days per au [@sats-soniakeys-saturnmoons]. Saturn is 1,205.5 to 1,658.6 million km, or 8.06 to 11.09 au, from the Earth [@sats-nssdc-saturn]. Light therefore takes 67 to 92 minutes, and Titan, at about 5.6 km/s, moves over 20,000 km in that time. The eclipse geometry must therefore use the eclipsing body's position at the instant the sunlight passed it, not at the Earth's reception time. NAIF documents how SPICE applies these corrections ([@moon-spice-abcorr]).

### Start, end and maximum

Two definitions are in use, and a product must state which it uses.

**Centre-based instants (phenomena by the planet).** IMCCE's booklet says: "These computations are made with no consideration of the diameter of the satellites but concern their center: these dates are the dates of the mid events" [@sats-imcce-1996-booklet]. It adds that on an equatorial apparent track the interval from first to last contact "is from 14s for Mimas (S1) up to 450s for Titan (S6)" [@sats-imcce-1996-booklet]. The 2009 tables of eclipses by Saturn give the instant of maximum and a "half-duration", "the time needed for the half-disappearance or reappearance of the satellite in seconds of time". For Titan in 2009 the half-duration ranged from 476 s to 1,440 s [@sats-arlot-thuillot-2008]. The long values arise when the track is oblique to the shadow edge.

**Contact-based instants (mutual events).** For each mutual eclipse the 2009 tables give [@sats-arlot-thuillot-2008]:

- the beginning of the eclipse by the penumbra,
- the beginning of the eclipse by the umbra, or of an occultation,
- the beginning of totality for total events,
- the maximum, from TASS and from the Do93 ephemeris,
- the end of totality, the end of the umbral eclipse or occultation, and the end of the penumbral eclipse,
- the [?sats-flux-drop] in V, with and without the satellites' albedos, and the magnitude drop,
- the duration in seconds, excluding the penumbral phase,
- the distance of the eclipsed satellite from Saturn's centre in Saturn radii,
- the [?impact-parameter] in arcseconds.

All times are in [?tt|Terrestrial Time] "since the UTC for this period is not yet available". The authors note TT − UTC "near 65 s in 2009" [@sats-arlot-thuillot-2008]. The 1996 booklet tells users to subtract 62 seconds to get UT [@sats-imcce-1996-booklet]. The flux drop runs from 0, no loss, to 1, total disappearance [@sats-arlot-thuillot-2008]. The albedos used for it were Morrison and Morrison's, with Mimas 0.77, Enceladus 1.04, Tethys 0.80, Dione 0.55, Rhea 0.65, Titan 0.20 and Hyperion 0.25 [@sats-arlot-thuillot-2008].

### Selecting events worth listing

Of 441 mutual events predicted for 2008 September 9 to 2010 June 18, Arlot and Thuillot printed 123 "easily observable" ones. Those occurred more than one Saturn radius from the limb, outside the ring, and had a magnitude drop over 10 per cent [@sats-arlot-thuillot-2008]. Eclipses by Saturn were listed only when more than 10 arcseconds from the limb and with Saturn more than 10 degrees from the Sun [@sats-arlot-thuillot-2008]. An event counted as observable from a site when the Sun was more than 10 degrees below the horizon and Saturn more than 15 degrees above it [@sats-arlot-thuillot-2008]. The 1996 booklet starred events within 30 degrees of the Sun or 5 degrees of the Moon, eclipses within 4 arcseconds of Saturn's limb, mutual events within 0.5 Saturn radius of the limb, and flux drops under 0.005 [@sats-imcce-1996-booklet].

Grazing events are uncertain by nature. "A difference of a few tenths of an arcsecond ... in the relative positions of the satellites may determine whether the event will occur or not" [@sats-arlot-thuillot-2008]. An event that is grazing in one ephemeris may be missing or deep in another. Its observation then tests the ephemeris directly.

## Eclipses by the rings and the Iapetus case

Iapetus's orbit is inclined "at about 15°" to Saturn's orbital plane, so "these events can take place only when Saturn is near one of the nodes of the satellite's orbit, i.e. the eclipses occur every 15 years" [@sats-soma-1992]. Soma's 1993 predictions give the sequence of a ring eclipse in full. On 1993 May 1 to 2, Iapetus was to enter ring A, leave it, enter ring B, enter ring C, leave C, enter Saturn's shadow, and then repeat the sequence in reverse after leaving the globe's shadow [@sats-soma-1992]. Barnard had observed the 1889 November 2 event visually. Reitsema recorded the 1977 October 19 event photometrically "from the immersion into the A ring to the passage of the Encke division" [@sats-soma-1992].

Soma's method follows Peters (1975) for mid-eclipse times, the "half-brightness points". It takes penumbral durations from the Sun's angular diameter seen from Iapetus with a [solar radius](../../20-solar-eclipses-and-transits/06-solar-radius/solar-radius-values.md) of 696,000 km, uses DE200 for Saturn and the Earth, and predicts in UT with TD − UT = +59 s for 1993 [@sats-soma-1992]. The two element sets used, Taylor and Shen (1988) and Dourneau (1987), gave mid-eclipse times 11 to 32 minutes apart. Soma noted that "the duration and magnitude drop especially for the ring eclipse of July 20-21 are sensitive to the difference of the orbital elements" [@sats-soma-1992].

**Ring transmission.** A ring is not an opaque disc. Ring occultation work converts the observed transmission $T$ of a ring into [?normal-optical-depth] with [@sats-afigbo-hedman-2025]:

$$
\tau_n = -\sin|B|\,\ln T,
$$

where $B$ is the ring opening angle to the light source. Inverting it for sunlight reaching a satellite through a ring gives $T = \exp(-\tau_n/\sin|B'|)$, with $B'$ the Sun's opening angle. This inversion is the same relation applied to the Sun as source, not a formula taken from an eclipse paper. With the fact sheet's $\tau$ of 0.4 to 2.5 for ring B and $B' = 5^{\circ}$, $T$ ranges from $e^{-4.6}$ to $e^{-28.7}$, which is effectively zero. With $\tau$ of 0.05 for the inner C ring, $T = e^{-0.57}$, or 0.56 [@sats-nssdc-rings]. A ring-eclipse predictor therefore needs the radial optical-depth profile, not only the edge radii. A satellite in the C ring's shadow loses part of its light, while in ring B's shadow it disappears.

**From a sky position to a ring radius.** A transmission needs the ring-plane radius at which the line of sight, or the sunlight, crosses the rings. The steps below are derived from the chapter 45 geometry, the fact-sheet edge radii and optical depths, and the transmission relation above. No source cited here prints them as one procedure [@sats-soniakeys-saturnring] [@sats-nssdc-rings] [@sats-afigbo-hedman-2025].

1. Take the offset of the star or satellite from Saturn's centre on the sky, $\Delta e$ towards the east and $\Delta n$ towards the north, in arcseconds. Rotate it by the ring position angle $P$, counted from north through east, so that $y$ runs along the projected northern semi-minor axis and $x$ along the major axis:
   $$
   x = \Delta e\cos P - \Delta n\sin P, \qquad y = \Delta e\sin P + \Delta n\cos P.
   $$
2. A ring-plane point at radius $r$ and azimuth $\theta$ projects to $(r\cos\theta,\ r\sin\theta\sin B)$. This is why the edges are ellipses with $b = a|\sin B|$, where $a$ and $b$ are Meeus's full axes and $r$ is half of $a$ for an edge. The line of sight through $(x, y)$ therefore meets the ring plane at
   $$
   r = \sqrt{x^2 + \left(\frac{y}{\sin B}\right)^2},
   $$
   which becomes kilometres at 725.27 km per arcsecond at 1 au, multiplied by $\Delta$ in au (see [the theories note](saturn-theories-and-ring-geometry.md#saturns-figure-and-the-rings-in-kilometres)).
3. The rings cover the body only when the body lies on the far side of the ring plane from the observer, so that its height above the ring plane has the opposite sign to $B$. Otherwise $T = 1$.
4. Find the edge crossings as the instants when $r(t)$ equals an edge radius from the fact sheet, by root-finding along the body's track. Between crossings take $\tau_n(r)$ from a radial optical-depth profile.
5. For a body seen through the rings from the Earth, $T = \exp(-\tau_n(r)/\sin|B|)$. For a ring shadow on a satellite, repeat steps 1 to 4 as seen from the Sun. Use offsets on the plane perpendicular to the Sun direction, the projected ring pole as the $y$ axis, and $B'$ in place of $B$, so that $T = \exp(-\tau_n(r)/\sin|B'|)$.

The thin-sheet relation fails as $B$ or $B'$ approaches zero. The slant path then grows without limit, and the ring's finite thickness, listed in the fact sheet, sets the geometry instead [@sats-nssdc-rings].

**The ring shadow on the globe.** The same $B'$ and $\Delta U$ from Meeus chapter 45 place the shadow of the rings on Saturn's disc and the shadow of the globe on the rings [@sats-soniakeys-saturnring]. Together these angles give the Sun's direction in the ring frame relative to the Earth's. Observers record both shadows: in 2025 the ring shadow on the globe in April and the globe's shadow on the rings by late May [@sats-baa-2025-notes]. When $B$ and $B'$ have opposite signs, the Earth sees the unlit face of the rings, as in 2025 between March 23 and May 6 [@sats-baa-2025-notes]. None of the sources cited here gives a closed formula for the ring-shadow outline on the oblate globe. It is a ray-ellipsoid intersection for each ring edge.

## What mutual events measure

The photometric reduction used for [?sats-phesat|PHESAT09] models the flux as [@sats-arlot-2012-phesat09]:

$$
E(t) = K\,\Phi\big(X(t), Y(t)\big),
$$

where $X(t)$ and $Y(t)$ are the differences of the two satellites' planetocentric coordinates projected on the tangent plane, $\Phi$ is a model of the phenomenon equal to 1 outside the event, and $K$ is the flux outside the event. The paper writes this model as S. It is renamed here because $S$ is the ellipsoid auxiliary elsewhere in this corpus. The theory gives $X_{\mathrm{th}}(t_i), Y_{\mathrm{th}}(t_i)$ for each photometric sample. The method solves, by linearised least squares [@sats-arlot-2012-phesat09]:

$$
E_i = K\,\Phi\big(X_{\mathrm{th}}(t_i) + D_x,\ Y_{\mathrm{th}}(t_i) + D_y\big), \qquad i = 1, \dots, m,
$$

for the offsets $D_x$, $D_y$ and $K$. The offsets are the O − C of the theory, here TASS 1.7 [@sats-arlot-2012-phesat09]. $\Phi$ integrates the reflected light over the visible hemisphere. It includes wavelength-dependent albedo, a rough-surface scattering law and solar limb darkening. It uses Buratti's combined photometric function [@sats-arlot-2012-phesat09]:

$$
(I/F)_c = A\,\frac{\mu_0}{\mu_0 + \mu}\,f(\alpha) + (1 - A)\,\mu_0,
$$

with $\mu_0$ and $\mu$ the cosines of the incidence and emission angles, $f(\alpha)$ the surface phase function and $A$ the weight between the two terms. The paper takes $A$ and $f(0)$ from Buratti (1984): for Mimas 0.7 and 1.1, for Dione 1.0 and 1.0 [@sats-arlot-2012-phesat09]. The result of each event is one relative position, the angular differences $\Delta\alpha\cos\delta$ and $\Delta\delta$ at the instant of closest apparent approach, which are heliocentric for eclipses [@sats-arlot-2012-phesat09].

The light curve does not fix two things. The albedo pattern of the satellites trades against position. The model therefore needs Voyager and ground-based photometry [@sats-arlot-2012-phesat09]. And the prediction's own impact parameter fixes the depth, so a missed grazing event is itself a measurement [@sats-arlot-thuillot-2008].

## The campaigns and their results

| Season | Predictions | Observations | Result |
|---|---|---|---|
| 1980 | Aksnes and Franklin (1978), nearly 300 events from October 1979 to August 1980, with ring eclipses [@sats-phemu-note09] | 14 observations [@sats-arlot-2012-phesat09] | Post-fit residuals of 80 km, about 0.01 arcseconds [@sats-rpx-dps-letter] |
| 1995 (PHESAT95) | Arlot and Thuillot (1993), 182 mutual events and 163 eclipses by Saturn. Aksnes and Dourneau (1995), 198 events [@sats-phemu-note09] | 66 observations [@sats-arlot-2012-phesat09] | Catalogue by Thuillot et al. 2001 and reduction by Noyelles et al. 2003, as cited in [@sats-arlot-2012-phesat09] |
| 2009 (PHESAT09) | Arlot and Thuillot (2008), 441 events, 123 easily observable, TASS and Do93 [@sats-arlot-thuillot-2008] | 33 observations, 26 light curves processed [@sats-arlot-2012-phesat09] | RMS O − C 48.5 and 21.7 mas against TASS 1.7, 16.4 and 20.7 against Lainey [@sats-arlot-2012-phesat09] |
| 2024 to 2026 | IMCCE web predictions for May 2024 to February 2026 [@sats-imcce-phemu-campaign] | Campaign under way at the page's last update, 2026 January 26 [@sats-imcce-phemu-campaign] | No published reduction found up to 2026 October |

Before 1980 only scattered visual records exist. Comrie published an algorithm for eclipses by Saturn in 1934. The BAA Handbook printed dates of Saturnian phenomena for favourable seasons [@sats-phemu-note09]. Dourneau's 1980 observations of two occultations showed O − C of one and three minutes against Aksnes and Franklin's predictions [@sats-phemu-note09]. That gap measures how poor the 1970s ephemerides were.

In 1995 Titan eclipsed Mimas, and the two shadows were seen to cross the rings. Hubbard, Consolmagno and colleagues used the shadow photometry to probe Titan's atmosphere [@sats-phemu-note09]. Titan is the one main satellite with an atmosphere, so its eclipse and occultation edges are soft [@sats-arlot-thuillot-2008]. An eclipse model that treats Titan as a sharp sphere of radius 2575 km [@sats-naif-pck00011] will misplace its contacts.

The 2009 season also showed how the planet hampers the observations. The ring "prevents us from observing the events close to the planet", and only relative photometry was generally possible [@sats-arlot-2012-phesat09]. The site table lists 19 site codes, from Greece and Spain to New Zealand, Chile and China [@sats-arlot-2012-phesat09].

## Published prediction products

| Product | What it lists | Theory | Source read |
|---|---|---|---|
| Bureau des longitudes annual supplement, for example the 1996 edition | Configuration curves good to 10 to 15 arcseconds, phenomena by the planet as centre-based instants, mutual events with type, flux drop and duration | Dourneau 1993 with VSOP82 | [@sats-imcce-1996-booklet] |
| Arlot and Thuillot 2008, A&A, with CDS tables | Mutual events, eclipses of Titan and Hyperion by Saturn, per-site visibility counts | TASS and Do93 | [@sats-arlot-thuillot-2008] |
| IMCCE PHEMU-PHESAT pages and the satellites-events form | Dates and local visibility, observing protocol, observation form | Not stated on the page | [@sats-imcce-phemu-campaign] |
| MULTI-SAT (Sternberg Astronomical Institute mirror) | Search for mutual events and eclipses by the planet | User's choice of five theories | [@sats-multisat-saturn] |
| PDS Ring-Moon Systems Node, 1995 RPX campaign | Arlot and Thuillot's classical-satellite predictions, Nicholson's small-satellite eclipse times | As supplied by the predictors | [@sats-pds-rpx-campaign] |
| BAA Saturn section apparition notes | Observations, not predictions: dated transits and shadow transits | Not applicable | [@sats-baa-2025-notes] |

Nicholson's predictions for the small inner satellites were revised after the May and August 1995 events, and "The Prometheus event times changed rather significantly" [@sats-pds-rpx-campaign]. Small satellites had ephemerides poor enough that the first observations of a season corrected the rest of its predictions. No primary source in this corpus states which theory Sky & Telescope's Saturn satellite tools and Titan transit tables use.

## What the public tools model

**JPL Horizons.** Observer quantity 12 gives a visibility code for a satellite against its primary: transiting, occulted, partial or total umbral eclipse, or occulted while eclipsed [@sw-horizons-manual]. The manual states its limits: "The radius of both primary and target body is taken to be the equatorial value ... Atmospheric effects and oblateness aspect are _NOT_ currently considered. Light-time is considered" [@sw-horizons-manual]. It adds that "Rise/set and satellite eclipse circumstances may not be accurate to less than a minute since factors such as the primarys' oblateness and atmosphere are not currently modelled" [@sw-horizons-manual]. Horizons therefore treats Saturn as a sphere of its equatorial radius, 60,268 km in the IAU value [@sats-naif-pck00011]. Near the poles its occultation contacts sit up to 5,904 km, the equatorial-polar difference, outside the true limb. It has no penumbral code and no ring.

**SPICE.** The occultation finder `gfoclt_c` handles finite discs as two ellipsoids, so it can use Saturn's triaxial radii from the PCK [@sw-spice-gfoclt] [@sats-naif-pck00011]. It has no ring model. A ring eclipse needs custom code.

**Stellarium.** Shadow casters for a body are its parent, its own satellites and its sibling satellites, each "with its equatorial radius" as a sphere. The shader takes at most four: "Our shader doesn't support more than 4 planets creating shadow" [@sats-stellarium-planet]. This code renders shadows. It does not compute [contact times](../../20-solar-eclipses-and-transits/04-local-circumstances/contact-times-and-magnitude.md).

**Cartes du Ciel (Skychart) and Miriade.** Cartes du Ciel computes positions with TASS and draws the system [@sats-skychart-plansat]. Miriade's ephemcc service returns positions with NOE. It does not list phenomena [@sats-miriade-ephemcc-output] [@sats-miriade-ephemcc-doc]. IMCCE's separate satellites-events form lists phenomena. It is a script-driven page whose theory is not stated on the page [@sats-imcce-phemu-campaign].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Arlot and Thuillot 2008 | The event types, column-by-column definitions of contacts and drops, selection criteria and the TASS versus Do93 timing spread |
| Arlot, Lainey and Thuillot 2006 | The light-time convention for eclipses, stated in words |
| IMCCE 1996 booklet | Centre-based timing convention and the 14 s to 450 s contact spans |
| Arlot et al. 2012 | The photometric model of a mutual event, the astrometric output, the campaign counts and O − C |
| Soma 1992 | A complete ring-eclipse sequence for Iapetus and the sensitivity to orbital elements |
| PDS RPX letter, BAA 2025 notes | Exact ring-plane crossing dates and modern dated shadow-transit observations |
| Horizons manual, Stellarium Planet.cpp | Documented simplifications in the most used public tools |

## What a developer should do

1. **Compute crossings first.** Find the dates when the saturnicentric latitudes of the Earth and the Sun, $B$ and $B'$, pass zero. Mutual events exist only within months of these dates, and globe phenomena of the inner satellites only within a year or so [@sats-arlot-thuillot-2008].
2. **Model Saturn as an oblate spheroid and its shadow as an elliptical cone** using $B'$. Do not copy Horizons's spherical simplification for contact times [@sw-horizons-manual] [@sats-naif-pck00011].
3. **Compute eclipses as occultations of the Sun seen from the eclipsed body,** with Sun-to-body light-time, and report both penumbral and umbral contacts [@sats-arlot-2006-uranus].
4. **State the timing convention.** Use either centre-based instants, as IMCCE's booklet does, or first and last contact. Give times in TT and UTC [@sats-imcce-1996-booklet] [@sats-arlot-thuillot-2008].
5. **For ring eclipses use a radial optical-depth profile** and $T = \exp(-\tau_n/\sin|B'|)$, with the ring-plane radius from the sky-plane offset as set out above, and present the result as a flux, not a yes-or-no event [@sats-afigbo-hedman-2025] [@sats-nssdc-rings].
6. **Carry two ephemerides,** for example SAT441 and TASS 1.7, and publish the difference in event times as the prediction's uncertainty, as Arlot and Thuillot did with TASS and Do93 [@sats-arlot-thuillot-2008].
7. **Treat Titan's edges as soft** and flag its contact times as approximate [@sats-phemu-note09].
8. **Read first:** Arlot and Thuillot 2008, then Arlot et al. 2012, then Soma 1992.

## What this changes

The solar-eclipse pipeline's shadow-cone machinery carries over to satellite eclipses, with three additions. The occulting body is oblate. A ring adds a partially transparent annulus to the shadow. The light-time convention changes, because the Sun-to-body and body-to-Earth legs are both long. The event-search layer gains a seasonal gate on $B$ and $B'$, which has no counterpart for the Earth and the Moon.

## Open questions

- **PHESAT95 catalogue.** Obtain Thuillot et al. 2001, A&A 371, 343, and Noyelles et al. 2003 for the 1995 O − C statistics, which this note cites only through the 2012 paper.
- **2024 to 2026 results.** Obtain the first reduction of the 2024 to 2026 Saturnian mutual events when IMCCE publishes it.
- **IMCCE satellites-events form.** Record which ephemeris the form at `ssp.imcce.fr/forms/satellites-events` uses for Saturn and how it defines contacts.
- **Ring-eclipse code.** Find a public implementation that predicts satellite eclipses by the rings with an optical-depth profile, or confirm that none exists, starting from Soma's method in Peters (1975), Celestial Mechanics 12, 99.
- **Titan's effective shadow radius.** Obtain Hubbard et al. 1996 (Lunar and Planetary Science 27, 569) for the radius at which Titan's shadow edge sits in eclipse photometry.
