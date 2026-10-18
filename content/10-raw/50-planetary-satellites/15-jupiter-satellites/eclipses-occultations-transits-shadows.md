---
title: Eclipses, occultations, transits and shadow transits
seo_title: Jupiter's Moons: Eclipse, Occultation and Transit Times
description: How the four satellite-Jupiter phenomena are computed, from shadow cones and Jupiter's flattening to light-time, timing conventions, published tables and accuracy.
order: 2
status: working
updated: 2026-10-17
tags: [jupiter, galilean-satellites, eclipses, occultations, transits, light-time, romer]
---

::: summary
- **Four phenomena, two viewpoints.** An eclipse and a shadow transit are decided by the satellite's position as seen from the Sun. An occultation and a transit are decided by its position as seen from the Earth. The two views differ by Jupiter's phase angle, at most about 12 degrees [@jup-nsdc-guide] [@jup-thuillot-1983].
- **The classical computation is two cones and an ellipsoid.** Thuillot (1983) puts a point Sun or a point Earth at the vertex of a cone tangent to an oblate Jupiter, $x^2 + y^2 + (1-\varepsilon)^{-2}z^2 = a^2$. An event is the instant the satellite centre crosses the cone, solved by iteration with separate light-time rules for each phenomenon [@jup-thuillot-1983].
- **Published times are mid-events in TT.** The Institut de mécanique céleste et de calcul des éphémérides (IMCCE) times an eclipse at half the satellite's light and the other events at bisection of the satellite. A visual observer sees the last or first speck instead, 1 to 2 minutes away for Io and Europa and up to 15 minutes for Callisto [@jup-imcce-phenjupiter-readme] [@jup-westfall-alpo].
- **Jupiter's penumbra at the satellites is 750 to 3400 km wide.** That width is $2dR_\odot/r$. It reproduces Westfall's table, as do the ingress durations of 4.2 minutes for Io to 16.6 minutes for Callisto that follow from it [@jup-westfall-alpo] [@sats-naif-pck00011].
- **Jupiter's atmosphere blurs the eclipse.** Refracted and scattered light makes a "refractive tail" lasting minutes in the red. The cloud tops cut the light off at about 9 magnitudes of darkening. The height of the half-light level is not established in the eclipse literature cited here, and Horizons and Thuillot both leave the atmosphere out [@jup-shorthill-1974] [@sw-horizons-manual].
- **The phase correction is minutes, not seconds.** Taking the limb or terminator instead of the ellipsoid shifts shadow and transit contacts by up to 3 minutes for Io and 6 minutes for Callisto near quadrature [@jup-thuillot-1983].
- **Eclipses of Io gave the first finite speed of light.** Cassini announced a delay of "ten or eleven minutes" across half the Earth's orbit on 22 August 1676. Rømer explained it as light's travel time in the Journal des Sçavans on 7 December 1676 [@jup-bobis-lequeux-2008].
:::

**The question.** How are the start and end of an eclipse, an occultation, a transit and a shadow transit of a Galilean satellite computed? Which geometry is used for the shadow and for Jupiter's disc, how do light-time and Jupiter's phase enter, what instant does a published time refer to, and how accurate are the published tables?

## Four phenomena and two viewpoints

The observing guide of IMCCE's Natural Satellites Data Center (NSDC) defines the satellite-planet phenomena by viewpoint. "When the Sun passes through the orbital plane of a satellite, the shadow of the planet may eclipse the satellite and the umbra of the satellite may pass on the disk of the planet." These are the [?jup-satellite-eclipse|eclipse] and the [?shadow-transit|transit of the umbra] (shadow transit), and they "are observable independantly of the observer". When the Earth passes through the orbital plane, the observer sees an [?jup-occultation|occultation] or a [?jup-transit|transit] of the satellite, which "depend on the observer" [@jup-nsdc-guide].

![The two Sun-fixed zones and the two Earth-fixed zones of one orbit are separated by Jupiter's phase angle, so an eclipse and an occultation of the same satellite are distinct events at distinct times [@jup-nsdc-guide] [@jup-thuillot-1983].](img/jup-phenomena.svg)

IMCCE's prediction files use eight codes. EC D and EC R are the disappearance and reappearance of an eclipse. OC D and OC R are those of an occultation. TR I and TR E are the ingress and egress of a transit, and SH I and SH E those of a shadow transit [@jup-imcce-phenjupiter-readme]. The French files write E. c., E. f., Im., Em., P. c., P. f., O. c. and O. f. [@jup-imcce-phenjupiter-readme].

The phase angle is the angle Sun-Jupiter-Earth. Its maximum is $\arcsin(R/r)$ for an Earth-Sun distance $R$ and a Jupiter-Sun distance $r$. Jupiter's perihelion distance is about 4.957 au, the minimum of Meeus's $r = 5.20872 - 0.25208\cos N$ [@jup-soniakeys-jupitermoons]. With $R = 1$ au that gives 11.6 degrees. With the Earth also at aphelion, $R = 1.0167$ au, it gives 11.8 degrees, the largest value. The separation between the Sun zones and the Earth zones has two consequences. Before opposition only Io's disappearances into the shadow can be seen, and after opposition only its reappearances, because Jupiter hides the other end [@jup-westfall-alpo]. For Ganymede and Callisto both ends are often visible within a few hours [@jup-westfall-alpo].

## Jupiter's shadow at the satellites

Jupiter's [?jup-jovian-shadow|shadow] has the same construction as the Moon's in the [Besselian elements](../../10-shared/01-foundations/besselian-elements.md). A cone of exterior tangents to the Sun and Jupiter bounds the umbra. A cone of interior tangents bounds the penumbra. For a satellite at distance $d$ behind Jupiter, measured along the shadow axis, with Jupiter at distance $r$ from the Sun, the small-angle radii are

$$
\rho_u = R_J - d\,\frac{R_\odot - R_J}{r}, \qquad
\rho_p = R_J + d\,\frac{R_\odot + R_J}{r}, \qquad
w = \rho_p - \rho_u = \frac{2\,d\,R_\odot}{r}.
$$

The cone with its vertex at the Sun's centre, Thuillot's "Soleil ponctuel" [@jup-thuillot-1983], has the radius

$$
\rho_c = R_J\left(1 + \frac{d}{r}\right),
$$

which is the mid-line of the penumbra. This follows from the small-angle forms above, since $(\rho_u + \rho_p)/2 = R_J(1 + d/r) = \rho_c$ exactly. It is a derivation, not a statement of the cited sources. A small satellite on that line sees Jupiter's limb pass through the Sun's centre, so about half the Sun's light reaches it. That is why a computation for the satellite's centre and a point Sun approximates the half-flux instant that IMCCE publishes [@jup-imcce-phenjupiter-readme].

The umbral cone is about 1250 Jupiter radii long, so all four satellites pass through the full shadow. The table evaluates the formulas with $R_\odot = 695{,}700$ km and $R_J = 71{,}492$ km from the IAU 2015 values in NAIF's PCK [@sats-naif-pck00011]. It uses $r = 5.20872$ au, the constant term of Meeus's Jupiter-Sun distance [@jup-soniakeys-jupitermoons], and the orbital radii, speeds and diameters of the Association of Lunar and Planetary Observers (ALPO) instructions by Westfall [@jup-westfall-alpo]. The solar radius is the IAU 2015 nominal value. The rest of this corpus predicts solar eclipses with 696,000 km. That value would widen each $w$ by 0.04 per cent, less than 2 km for Callisto.

| Satellite | $d$ (km) | $\rho_u$ (km) | $\rho_p$ (km) | $w$ (km) | Westfall penumbra (km) | Central ingress $(D + w)/v$ (min) | Westfall ingress (min) | Central eclipse $2\rho_c/v$ (min) | Westfall eclipse (min) |
|---|---|---|---|---|---|---|---|---|---|
| Io | 421,800 | 71,154 | 71,907 | 753 | 754 | 4.2 | 4.2 to 4.5 | 137.6 | 128 to 138 |
| Europa | 671,100 | 70,954 | 72,153 | 1198 | 1200 | 5.3 | 5.2 to 6.4 | 173.6 | 135 to 174 |
| Ganymede | 1,070,400 | 70,635 | 72,546 | 1911 | 1915 | 11.0 | 10.9 to 18.2 | 219.3 | 126 to 220 |
| Callisto | 1,882,700 | 69,984 | 73,346 | 3362 | 3367 | 16.6 | 16.8 to 134.8 | 291.0 | 0 to 290 |

Here $D$ is the satellite's diameter and $v$ its orbital speed. The formulas give the lower bound of each ingress range and the upper bound of each eclipse range. Those are the central, perpendicular crossings, and Westfall's ranges cover oblique ones [@jup-westfall-alpo]. Callisto's long ingress and zero-length eclipses are grazing passages. Callisto's centre enters the shadow only when $|D_S| < \arcsin(R_J/d) = 2.2^{\circ}$ with the equatorial radius, or $2.0^{\circ}$ with the polar radius. Jupiter's equator is inclined $3.12^{\circ}$ to its orbit [@jup-soniakeys-jupitermoons]. Callisto therefore "has eclipses only half the time", for three-year periods separated by three years [@jup-westfall-alpo].

## Jupiter's figure in the test

Jupiter is an oblate spheroid with radii 71,492, 71,492 and 66,854 km in the IAU 2015 values [@sats-naif-pck00011]. Its [?jup-flattening|flattening] is $(71492 - 66854)/71492 = 0.0649$, and $71492/66854 = 1.0694$. JPL's satellite kernels adopt the same equatorial radius [@jup-naif-jup365-cmt] [@jup-naif-jup310-cmt].

Thuillot's formulation keeps the spheroid exact. In a jovicentric equatorial frame Jupiter is

$$
X^{t} M X - a^2 = 0, \qquad M = \begin{pmatrix}1 & 0 & 0\\ 0 & 1 & 0\\ 0 & 0 & \varrho\end{pmatrix}, \qquad \varrho = (1 - \varepsilon)^{-2},
$$

with $a$ the equatorial radius and $\varepsilon$ the geometric flattening [@jup-thuillot-1983]. A satellite at $Q$ lies on the cone with vertex at the Sun's centre $S$, tangent to the spheroid, when

$$
\Delta_S = (S^{t}MQ - a^2)^2 - (S^{t}MS - a^2)(Q^{t}MQ - a^2) = 0 .
$$

The cone of visibility from the Earth's centre $T$ is the same expression with $T$ for $S$, $\Delta_T = 0$ [@jup-thuillot-1983]. $\Delta_S > 0$ means the satellite is inside the shadow cone. $\Delta_T > 0$ means it is inside the cone of visibility, that is, behind or in front of the disc [@jup-thuillot-1983]. Which of the two depends on whether the satellite is beyond Jupiter or between Jupiter and the Sun or Earth. Thuillot takes the pole of Jupiter from Null (1976) and solves the equations by successive approximation [@jup-thuillot-1983].

Simpler implementations stretch Y. PyMeeus multiplies the $Y$ coordinate by 1.071374 and tests $\sqrt{X^2 + Y^2} \le 1$. It uses the Earth-view coordinates for occultations and the Sun-view coordinates for eclipses, and the sign of $Z$ for which side of Jupiter the satellite is on [@jup-pymeeus-jupitermoons]. The factor 1.071374 does not equal the IAU 2015 ratio 1.069375. The code does not say where it comes from [@jup-pymeeus-jupitermoons] [@sats-naif-pck00011]. The test also uses a cylinder of radius 1. It ignores both the converging umbra and the half-flux cone $\rho_c$. Its event times therefore refer to neither the half-flux instant nor the umbra contact. Horizons ignores the flattening altogether. Its visibility codes take "the equatorial value" for both the primary and the satellite, and "Atmospheric effects and oblateness aspect are _NOT_ currently considered" [@sw-horizons-manual].

A rigorous program applies the flattening to the projected disc. A spheroid seen from a direction at jovicentric latitude $D$ projects to an ellipse with semi-major axis $a$ and semi-minor axis $\sqrt{a^2\sin^2 D + b^2\cos^2 D}$, where $b$ is the polar radius. Use $D = D_E$ for the disc and $D = D_S$ for the shadow. Thuillot's cone equation contains this projection implicitly [@jup-thuillot-1983].

## Light-time: two clocks

The phenomena mix two light paths. Thuillot gives the rules for a time $t$ in Ephemeris Time, with $TQ$ and $TJ$ the Earth-satellite and Earth-Jupiter distances and $C$ the speed of light. For occultations and transits the paper prints that "le satellite doit être considéré dans sa position à t − TQ/C et la Terre dans sa position à t − TJ/C". The date $t$ that satisfies the equations is "la date du phénomène perçu sur Terre" [@jup-thuillot-1983]. As printed, the second clause delays the Earth. Since $t$ is the date of reception at the Earth, the physically consistent reading delays Jupiter, the occulting body, to $t - TJ/C$ and keeps the Earth at $t$. This note takes that reading, as its own correction of the printed text. For eclipses and shadow transits, the Sun is taken at $t - QS/C$. The date seen from the Earth is then $t + TQ/C$ for an eclipse and $t + TJ/C$ for a shadow transit [@jup-thuillot-1983]. With a phase correction, the terminator is set by the Sun at $t - (TJ + JS)/C$, and the limb that bounds a shadow is the one seen from the Earth at $t + JT/C$ [@jup-thuillot-1983].

With the Earth-Jupiter distance $\Delta$ between about 4.0 and 6.4 au, the [?light-time] $\Delta/173$ days is 33 to 53 minutes [@jup-soniakeys-jupitermoons]. That full span needs several apparitions, because Jupiter's distance from the Sun runs from about 4.96 to 5.46 au over its 12-year orbit. Within one synodic period $\Delta$ changes by about 2 au, the diameter of the Earth's orbit, so the light-time changes by about 16 minutes. That drift was the first evidence for a finite speed of light. Within the satellite system, Meeus's high-accuracy method applies the [?jup-differential-light-time|differential light-time] $|Z|/K_i$ to X, where Z is the satellite's distance along the line of sight in Jupiter radii [@jup-soniakeys-jupitermoons]. For Io at $Z = 6$ Jupiter radii it is about $6/17295$ Jupiter radii, or 25 km. That is 1.4 seconds of Io's motion. [Refraction, light-time and frames](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) covers the observer-side corrections, which are the same as for the Sun and Moon.

The IMCCE tables give the instants in TT. To convert to UT, subtract TT − UT [@jup-imcce-phenjupiter-readme]. Their table of TT − UT runs from 61 s in 1994 to 69 s from 2017 on, and the 2026 UT edition uses 69 s [@jup-imcce-phenjupiter-readme] [@jup-imcce-phen-2026]. The difference is [?delta-t|ΔT].

## The phase correction

Thuillot's basic cones rest on the spheroid. They give the right answer when the satellite and the Sun, or the satellite and the Earth, are on opposite sides of the Sun-Earth-Jupiter line. In the other cases the cone must rest "non plus sur l'ellipsoïde mais sur le limbe dans le cas des ombres, ou sur le terminateur dans le cas des passages" [@jup-thuillot-1983]. Thuillot lists the affected events. Before opposition they are the beginnings of shadow transits and the ends of transits. After opposition they are the ends of shadow transits and the beginnings of transits [@jup-thuillot-1983]. For those cases he replaces $\Delta_S$ and $\Delta_T$ by $\Delta'_S$ and $\Delta'_T$ [@jup-thuillot-1983].

The limb seen from the Earth is the intersection of the ellipsoid $X^{t}MX - a^2 = 0$ with the plane $T^{t}MX - a^2 = 0$. Thuillot substitutes the generator of the Sun's cone, $X = (Q + \lambda S)/(1 + \lambda)$, and eliminates the parameter $\lambda$. The result, his equation 4, replaces equation 2 for shadow transits with a phase correction [@jup-thuillot-1983]:

$$
\Delta'_S = (S^{t}MS - a^2)(a^2 - T^{t}MQ)^2 + 2(S^{t}MQ - a^2)(a^2 - T^{t}MQ)(T^{t}MS - a^2) + (Q^{t}MQ - a^2)(T^{t}MS - a^2)^2 = 0 .
$$

His equation 5 is the same construction for transits, with the cone from the Earth resting on the terminator, the plane $S^{t}MX - a^2 = 0$ [@jup-thuillot-1983]:

$$
\Delta'_T = (T^{t}MT - a^2)(a^2 - S^{t}MQ)^2 + 2(T^{t}MQ - a^2)(a^2 - S^{t}MQ)(S^{t}MT - a^2) + (Q^{t}MQ - a^2)(S^{t}MT - a^2)^2 = 0 .
$$

Here $S$, $T$ and $Q$ are the column vectors of the Sun's centre, the Earth's centre and the satellite in the jovicentric equatorial frame, and $M$ and $a$ are as above. The sign convention is reversed from $\Delta_S$ and $\Delta_T$. $\Delta'_S < 0$ means the satellite is inside the phase-corrected shadow cone, and $\Delta'_T < 0$ means it is inside the phase-corrected cone of visibility [@jup-thuillot-1983].

The [?jup-phase-correction|phase correction] "atteint près de la quadrature 3 min de temps pour le satellite 1 et 6 min pour le satellite 4" [@jup-thuillot-1983]. A shadow seen against the unlit part of the disc beyond the terminator is invisible. A satellite crossing the terminator is still in front of the disc. A program that tests only the sky-plane disc gets these events wrong by minutes near quadrature.

## What "start" and "end" mean

Four conventions are in use:

| Convention | Used by | Instant |
|---|---|---|
| Half flux for eclipses, bisection by the limb or shadow edge for the others | IMCCE phenomena files and the Connaissance des Temps | satellite centre on the point-Sun cone or on the limb [@jup-imcce-phenjupiter-readme] |
| Half flux, or the instant computed from first or last speck | IMCCE's archive of observed eclipses 1652 to 1983 | mid-event, with the semi-duration TQ to the last or first speck recorded [@jup-nsdc-eclipse-readme] |
| Centre of the satellite touching the limb | Juptool (Nagoya) | centre contact [@jup-juptool-nagoya] |
| Limb-to-limb with equatorial radii | Horizons observer tables, quantity 12 | first and last contact, no flattening [@sw-horizons-manual] |

IMCCE states the convention twice. "The dates t of the mid event (the satellite or its umbra is bissected) are given in the TT time scale". "Each event is computed for the center of the satellites: for the eclipses these dates are approximately the half brightness (or mid event), for the other phenomena they correspond to the bissection of the satellites" [@jup-imcce-phenjupiter-readme]. The NSDC guide adds that published eclipse times are "commonly the time of the mid-extinction or mid-reappartion of the satellite (half flux of the satellite visible unless another specification in the comments)" [@jup-nsdc-guide]. This is the [?jup-mid-event|mid-event convention].

A visual observer does not see the mid-event. Westfall's instructions say to time "the 'last speck'" at disappearance and the "first speck" at reappearance. They warn that "Io and Europa typically reappear about 1-2 minutes 'early' and disappear the same amount 'late.' Ganymede's time difference is more like 4-8 minutes, and can be up to about 15 minutes for Callisto" [@jup-westfall-alpo]. Juptool's manual makes the same point for centre contacts: "the real starting or ending time may be a few minutes earlier/later than the center contact time" [@jup-juptool-nagoya].

Horizons reports a visibility code per output step, not event times. The codes are /t transiting, /O occulted, /p partial umbral eclipse, /P occulted partial umbral eclipse, /u total umbral eclipse, /U occulted total umbral eclipse and /* free and clear. They refer to "limb-to-limb" contact, and "Light-time is considered" [@sw-horizons-manual]. The list has no code for a shadow transit, and no code for a penumbral-only eclipse [@sw-horizons-manual].

## Simultaneous events

Thuillot warns that the end or the start of an eclipse or an occultation can be invisible when the satellite is already occulted or eclipsed. All four phases, OC.D and OC.F, EC.D and EC.F in Thuillot's notation, must therefore be computed before any one is declared visible [@jup-thuillot-1983]. The combined events that observers look for follow by the same logic. Each phenomenon is a time interval, from its start event to its end event in the per-satellite lists. A double or triple shadow transit is the overlap of two or three SH I to SH E intervals. A satellite in transit with its own shadow on the disc is the overlap of its TR and SH intervals. Jupiter with no Galilean satellite visible beside it is the time when each of the four satellites is inside one of its own OC, EC or TR intervals. That is the intersection, over the four satellites, of each satellite's union of those intervals. These rules are derived here from the interval structure of the published lists, not quoted from a source.

## Jupiter's atmosphere and the eclipse light curve

The shadow edge is not sharp, and not only because of the penumbra. Shorthill, Greene and Smith observed twelve eclipse light curves at 30 wavelengths with the 200-inch Hale telescope. "Sun light is refracted and scattered into the geometric shadow resulting in a 'refractive-tail'" [@jup-shorthill-1974]. At 7300 Å the [?jup-refractive-tail|refractive tail] lasts several minutes. At 11000 Å it lasts longer. At 5000 Å the light curve "falls very rapidly and may show no refractive-tail at all" [@jup-shorthill-1974]. "At some point (mv≈9) a ray passing tangentially through the atmosphere will be cut off by the cloud tops" [@jup-shorthill-1974]. Eclipses probe the atmosphere "to greater depths ... in some cases, to the cloud deck" than stellar occultations do [@jup-shorthill-1974]. Even in totality the satellites are not dark. Tsumura et al. measured Europa, Ganymede and Callisto at $10^{-6}$ to $10^{-7}$ of their uneclipsed brightness near 1.5 micrometres [@jup-tsumura-2014].

The altitude above the 1-bar level, or the radius in km, at which the half-flux point of a Galilean eclipse falls is not stated by Shorthill et al., Thuillot, IMCCE or the Horizons manual. Thuillot's predictions are made "sans considérer l'influence de l'atmosphère de Jupiter" [@jup-thuillot-1983]. Horizons does not model it [@sw-horizons-manual]. So the published instants are geometric half-flux instants for a solid spheroid. The observed half-flux instant differs from them by an amount that depends on the wavelength band. The size and sign of that offset are an open question.

## Published products

**IMCCE phenomena files.** IMCCE publishes yearly prediction files for all four phenomena [@jup-imcce-phenjupiter-readme]. They are computed by V. Lainey, M. Gastineau and J. Nepper from 2023 and by W. Thuillot from 1996 to 2022 [@jup-imcce-phenjupiter-readme]. The `phenE.yyyy` file lists each month's events in four columns in TT. Eclipse times are given to 0.1 minute and other events to the minute, for example "26 1  1 1546.3   I EC D" [@jup-imcce-phen-2026]. The `xyE.yyyy` file gives "the differential coordinates X and Y of the Galilean satellites (X towards the East and Y towards the North) during an eclipse at a date near the middle of each month" [@jup-imcce-phenjupiter-readme]. The `JovianEventsUTyyyy.txt` file gives UT rounded to the minute, the conjunctions and the dates when Jupiter is not observable [@jup-imcce-phenjupiter-readme]. In 2026 that period runs from July 2 to August 25 (TT) [@jup-imcce-phen-2026].

**Connaissance des Temps.** IMCCE also distributes the phenomena "under the form of Chebychev polynomials as published in the ephemeris Connaissance des Temps" [@jup-imcce-phenjupcdt]. Thuillot designed that form. For each satellite and each phenomenon, 15 [?chebyshev|Chebyshev] coefficients represent the residual $\tau_N = t_N - (T_B + N T_P)$ after removing the synodic period $T_P$. That residual is mostly the light-time variation [@jup-thuillot-1983]. The date of the next event is $t = T_B + N T_P + \tau/24$ with $\tau = \sum_{n=0}^{14} C_n \cos(n\Theta)$ and $\Theta = \arccos(2(t^{(0)} - T_B)/T_I - 1)$. Iterating once more makes the date converge to about a second [@jup-thuillot-1983]. Against the full computation the maximum error was 51 s, for Ganymede in 1985 [@jup-thuillot-1983]. The 1984 coefficients were computed from G-5 [@jup-thuillot-1983].

**Almanacs and magazines.** Westfall lists The Astronomical Almanac, the Handbook of the British Astronomical Association (BAA), the Handbook of the Royal Astronomical Society of Canada (RASC) and the Sky & Telescope website as sources of predictions [@jup-westfall-alpo]. Sky & Telescope's tables are reported to be computed by the Bureau des Longitudes. That is reported secondhand and unconfirmed [@jup-snt-erratum-2008]. The Astronomical Almanac's theory and accuracy statement for its satellite phenomena are not established in the sources cited here.

**Open software.** Stellarium's AstroCalc tool has a "Shadows" mode. It finds the minimum of the heliocentric angle between a moon and its planet and labels the instant "Shadow transit", or "Eclipse" when the moon is the farther body [@sw-stellarium-astrocalc]. Its conjunction mode labels a geocentric close approach "Transit" or "Occultation" from the two discs' sizes [@sw-stellarium-astrocalc]. Both report one central instant, not the start and end. PyMeeus returns, for one instant, a signed distance from Jupiter's centre in the Y-stretched metric [@jup-pymeeus-jupitermoons]. A caller must search that function for its crossings of ±1 to get contact times.

**SPICE.** NAIF's `gfoclt_c` finds occultation intervals between two bodies modelled as ellipsoids, of type FULL, ANNULAR, PARTIAL or ANY [@sw-spice-gfoclt]. Placed at a satellite with the Sun as the back body and Jupiter as the front body, it returns the satellite centre's passage through the penumbra (PARTIAL) and the umbra (FULL). That set-up follows from the routine's definition. The routine does not model the atmosphere, and it does not return the half-flux instant. An occultation of the satellite is the same call from the Earth with the satellite as a point target and type ANY [@sw-spice-gfoclt].

## Accuracy of the predictions

| Product | Error stated | Source |
|---|---|---|
| Thuillot's Chebyshev form against his full computation | 51 s maximum (1984 to 1987) | [@jup-thuillot-1983] |
| Horizons satellite eclipse circumstances | "may not be accurate to less than a minute" | [@sw-horizons-manual] |
| Juptool event times | "3-4 minutes off" accurate tables | [@jup-juptool-nagoya] |
| Visual timing against mid-event | 1 to 2 min (Io, Europa), 4 to 8 min (Ganymede), up to 15 min (Callisto) | [@jup-westfall-alpo] |
| Seventeenth-century timings | Cassini claimed 15 s; observers differed by half a minute | [@jup-bobis-lequeux-2008] |

The theory error is now small against these. A satellite moving at about 10 km/s covers 10 km in one second of time, so "an error of one second of time corresponds ... to 10km" [@jup-nsdc-guide]. A JUP365 position good to tens of km therefore times an eclipse to a few seconds [@jup-catani-2023]. The remaining error of a geometric prediction comes from the atmosphere and from the definition of the instant, not from the orbit. IMCCE's archive holds 16,802 eclipse observations from 1652 to 1983 from 426 observatories, each with its [?o-minus-c|O − C], its a priori uncertainty and its semi-duration TQ. These are the data that test such definitions [@jup-nsdc-eclipse-readme].

## Longitude and the speed of light

Galileo proposed the satellites as a clock soon after he discovered them. Cassini wrote in 1692 that astronomers observed Jupiter "in order to obtain an exact knowledge of longitudes". He meant a rapid phenomenon seen at the same instant from distant places [@jup-bobis-lequeux-2008]. With clocks synchronised by an eclipse, the difference in the local times of a star's meridian transit gave the difference in longitude. That corrected "a large quantity of errors" in the maps [@jup-bobis-lequeux-2008]. Cassini claimed 15 s accuracy for an immersion or emersion. A study by Débarbat found that observers could differ by half a minute, even for Io [@jup-bobis-lequeux-2008].

The same timings showed an anomaly. On 22 August 1676 Cassini announced a new inequality, "the same for all the satellites", that could reach a quarter of an hour. He predicted that Io's emersion of 16 November would be about 10 minutes late. He also wrote that light seemed to take "ten or eleven minutes [to cross] a distance equal to the half-diameter of the annual orbit" [@jup-bobis-lequeux-2008]. An emersion observed on 9 November 1676 was 10 minutes late. Rømer read his account to the Academy on 21 November, and the Journal des Sçavans published it on 7 December 1676 [@jup-bobis-lequeux-2008]. Bobis and Lequeux argue from a Paris Observatory manuscript that Cassini first proposed the "successive motion" of light and later abandoned it [@jup-bobis-lequeux-2008]. The light-time term in every modern prediction is the effect that these two astronomers measured.

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Thuillot (1983) [@jup-thuillot-1983] | The cone equations with an oblate Jupiter, the phase correction, the light-time rules, the Chebyshev form and its error |
| IMCCE phenjupiter README and files [@jup-imcce-phenjupiter-readme] [@jup-imcce-phen-2026] | Event codes, TT, the mid-event convention, the precision of the published times, the theory used |
| NSDC guide and eclipse README [@jup-nsdc-guide] [@jup-nsdc-eclipse-readme] | Viewpoint definitions, half-flux convention, the 1652 to 1983 eclipse archive |
| Westfall (ALPO) [@jup-westfall-alpo] | Penumbral widths, durations, the visual-timing offsets |
| Shorthill et al. (1974) [@jup-shorthill-1974] | The atmosphere's effect on the eclipse light curve |
| Horizons manual [@sw-horizons-manual] | What the most used online service models and omits |
| Stellarium, PyMeeus, Juptool code and manuals [@sw-stellarium-astrocalc] [@jup-pymeeus-jupitermoons] [@jup-juptool-nagoya] | What hobby software reports and with which convention |
| Bobis and Lequeux (2008) [@jup-bobis-lequeux-2008] | The documented history of the longitude method and of the 1676 discovery |

## What a developer should do

1. **Compute two sets of satellite coordinates.** Use the Earth-view coordinates, with light-time to the Earth, for occultations and transits. Use the Sun-view coordinates, with light-time from the Sun, for eclipses and shadow transits. Then add the satellite-to-Earth or Jupiter-to-Earth light-time to the eclipse or shadow instant, as Thuillot does [@jup-thuillot-1983].
2. **Model Jupiter as the IAU spheroid**, 71,492 by 66,854 km, and project it with $D_E$ for the disc and $D_S$ for the shadow [@sats-naif-pck00011] [@jup-thuillot-1983].
3. **Publish the mid-event in TT and say so.** Use the point-Sun cone $\rho_c$ for eclipse half-flux and the bisection of the satellite for the other events, to match IMCCE [@jup-imcce-phenjupiter-readme]. If a product shows first and last contact as well, compute them from $\rho_p$, $\rho_u$ and the satellite radius, and label them separately.
4. **Apply the phase correction** for shadow-transit and transit contacts on the terminator side, or accept errors of up to 6 minutes near quadrature [@jup-thuillot-1983].
5. **Validate against the IMCCE files** for the same year, and record which theory those files used [@jup-imcce-phenjupiter-readme]. Expect agreement within a minute for eclipses if the ephemeris is modern and the conventions match. Check the sign of X before comparing positions. The `xyE` files give "X towards the East and Y towards the North" [@jup-imcce-phenjupiter-readme]. Meeus's X is positive to the west. That follows from his low-accuracy formulas: $u = 0$ gives $Y = -r\sin D_E$, the near side of the orbit, so $X = r\sin u$ grows along the satellite's prograde motion across the disc, which is westward [@jup-soniakeys-jupitermoons].
6. **Do not use Horizons visibility codes as event times.** They are per-step flags with equatorial radii and no flattening [@sw-horizons-manual].

Read first: Thuillot (1983), the IMCCE phenjupiter README, Westfall's ALPO instructions.

## What this changes

The pipeline's shadow-cone and contact machinery carries over from solar eclipses with three changes. The body casting the shadow is an oblate spheroid whose projection depends on the jovicentric declination. Two light-time paths must be kept separately, one for the shadow and one for the disc. And the published instant is a mid-event, not a first contact. The contact solver in [the local circumstances topic](../../20-solar-eclipses-and-transits/04-local-circumstances/contact-times-and-magnitude.md) needs a mode that reports bisection or half-flux instants.

## Open questions

- **The Astronomical Almanac's satellite phenomena section.** Obtain the explanatory text that states the theory, the conventions and the accuracy of its tables.
- **Half-flux altitude.** Find a paper that fits CCD eclipse light curves with a Jovian atmosphere model and states the radius of the half-flux level. Candidates are the 1970s eclipse studies that Shorthill et al. cite and the eclipse-astrometry papers cited by Tsumura et al.
- **Meeus's flattening factor.** Check whether 1.071374 in PyMeeus is printed in Meeus chapter 44 or is a transcription error for 1.069374.
- **Sky & Telescope's tables.** Confirm from the magazine which institution and theory compute the current "Jupiter's Moons" tables and app.
- **Explanatory Supplement (2013), satellites chapter.** Obtain its treatment of satellite phenomena for the almanac's adopted conventions.
