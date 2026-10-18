---
title: Enumerating transits and their elements
seo_title: Transits of Mercury and Venus: Enumeration and Elements
description: How transits of Mercury and Venus are found and catalogued, their recurrence cycles, and the Besselian-style elements used to compute them.
order: 1
status: working
updated: 2026-10-17
tags: [transits, mercury, venus, besselian, catalogues, recurrence]
---

::: summary
- **A transit needs an inferior conjunction close to a node.** The Earth must be within a small heliocentric angle of the planet's node when the planet crosses the ecliptic. The 1961 Explanatory Supplement gives 238 arcminutes at Mercury's ascending node and 108 at its descending node, and 37 arcminutes at Venus's ascending node and 41 at its descending node [@tr-es1961].
- **Mercury transits fall near May 8 and November 10, Venus transits near June 7 and December 9.** November transits of Mercury are about twice as common as May transits. Espenak counts 94 Mercury transits from 1601 to 2300, 31 in May and 63 in November, and 81 Venus transits from 2000 BCE to 4000 CE [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog].
- **The cycles are near-commensurabilities.** Espenak gives 13 years as 54 orbits of Mercury less 2.01 days, 33 years as 137 orbits less 1.67 days, and 46 years as 191 orbits plus 0.34 days. He gives Venus a repeat after 8 years, or 13 orbits, with the planet arriving 2.45 days early, which gives the 8, 105.5, 8 and 121.5 year pattern and a 243-year series [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog].
- **The NASA catalogues rest on Meeus's elements.** Espenak's catalogues state that their Besselian elements and algorithms come from Meeus's *Transits* (Willmann-Bell, 1989). The ephemeris behind his individual predictions changed from DE200 (1999) through VSOP87 (2012) and DE406 (2016, 2019) to DE430 and DE431 for the 2018 Canon [@tr-nasa-catalog-key] [@tr-nasa-oh1999] [@tr-nasa-oh2012] [@tr-ew-tm2019] [@tr-ew-transit-index].
- **The almanac method is Bessel's eclipse theory with the planet in place of the Moon.** The 1961 Supplement works heliocentrically, puts the origin of the fundamental plane on the shadow axis, and gives contacts where the Earth's centre lies on the penumbral or umbral cone [@tr-es1961]. Stellarium computes geocentric elements in the solar-eclipse form, with the planet's radius as $k$ [@tr-stellarium-transits].
- **Grazing and partial transits are flagged by missing contacts.** The 1937 May Mercury transit has no geocentric interior contacts, the 1999 November one was a graze, and some Venus rows have no geocentric contacts at all [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog] [@tr-nasa-oh1999].
- **Light-time enters as a back-dating of the planet.** The planet's coordinates are taken at $T - \tau_2 + \tau_1$, with $\tau_2 - \tau_1 = 0.138439\,(R - r)$ hours in the 1961 Supplement and 0.138614 from 1968 [@tr-es1961].
:::

**The question.** How does a program find every [?tr-planetary-transit|transit of Mercury or Venus] in a span of centuries, what recurrence structure organises the list, and what intermediate quantities does a predictor compute before it solves for contact times? This note covers the enumeration stage and the elements. The contact solution, the local-circumstance formulas and the constants are in [Contacts and local circumstances](contacts-and-local-circumstances.md). The observations that test the predictions are in [Observations, the black drop and the solar radius](observations-black-drop-and-solar-radius.md). The solar-eclipse version of the same machinery is in [Besselian elements](../../10-shared/01-foundations/besselian-elements.md) and [Enumerating eclipses](../02-catalogs/enumerating-eclipses.md).

## The node condition

Both almanac supplements state the condition in the same words. Transits "can only occur when both the Earth and the planet are simultaneously very close to the same node of the planet's orbit on the ecliptic" [@tr-es1961] [@tr-es1992]. The 1961 Supplement adds the quantitative form: "In order that a geocentric transit should occur, the Earth must be within a range ±θ of the node of the planet's orbit, at the instant at which the planet crosses the ecliptic" [@tr-es1961]. It gives an approximate formula for θ in terms of the radii vectores $R$ and $r$ of the Earth and the planet, their daily motions, the inclination $i$ through $\csc i$, and the solar semidiameter $s_0$ at unit distance [@tr-es1961]. This note does not reproduce that formula. The evaluated limits below are the Supplement's own.

The same section tabulates the [?tr-node-limit|node limits] and the frequency each implies "assuming random distribution" [@tr-es1961]:

| Planet and node | Date of node passage | θ | Frequency |
|---|---|---|---|
| Mercury, ascending | about 16 November | 238′ | 9 per 100 years |
| Mercury, descending | about 8 May | 108′ | 4 per 100 years |
| Venus, ascending | about 9 December | 37′ | 0.6 per 100 years |
| Venus, descending | about 7 June | 41′ | 0.6 per 100 years |

Espenak's Venus catalogue agrees that the December transits occur at the ascending node and the June transits at the descending node [@tr-nasa-venus-catalog]. The reason the Mercury limits differ is orbital. "The highly eccentric orbit of Mercury thus means that the conditions, and limits, at the November transits are very different from those at the May transits" [@tr-es1961]. Espenak gives the physical picture. In November Mercury is near perihelion with a disc about 10 arcseconds across, and in May near aphelion with a disc about 12 arcseconds across. "The probability of a May transit is smaller by a factor of almost two" because "Mercury's slower orbital motion at aphelion makes it less likely to cross the node during the critical period" [@tr-nasa-transit-index].

The dates are not fixed. "Five thousand years ago, transits occurred around May 21 and November 19." Venus transits now fall "within a day of June 7 and December 9", and the dates migrate through the seasons in about 80,000 years [@tr-nasa-venus-catalog].

## Mercury: the 13, 33 and 46 year cycles

Espenak's Seven Century Catalogue lists 94 transits of Mercury from 1601 to 2300: 31 in May at the descending node and 63 in November at the ascending node [@tr-nasa-mercury-catalog]. Consecutive transits are separated by 3.5, 7, 9.5, 10 or 13 years. "The 13 year period is of particular note because it corresponds to nearly 54 orbits of Mercury around the Sun (it falls short of a perfect fit by just 2.01 days). A longer period of 33 years (10 + 10 + 13) produces an even better fit which corresponds to 137 orbits of Mercury minus 1.67 days. If one combines the 13 year and 33 year periods together, the 46 year total equals 191 orbits of Mercury plus only 0.34 days" [@tr-nasa-mercury-catalog]. November transits "recur at intervals of 7, 13, or 33 years while May transits recur only over the latter two intervals" [@tr-nasa-transit-index].

The 46-year period of 16,802 days defines a [?tr-transit-series|transit series], "quite analogous to the Saros series for solar and lunar eclipses" [@tr-nasa-mercury-catalog] [@tr-nasa-catalog-key]. The series lengths differ by node. In May the planet's position relative to the Sun "shifts by approximately 200 arc-seconds with each transit", so a May series lasts about 10 transits or 414 years. In November the shift is about 100 arcseconds and the series lasts about twice as long. Series 8 runs from 1776 to 2604 with 19 transits [@tr-nasa-mercury-catalog]. The catalogue key says the seven centuries hold twelve series [@tr-nasa-catalog-key], while the catalogue page itself says ten [@tr-nasa-mercury-catalog]. The table on the catalogue page numbers series up to 12, which supports the key.

The twentieth century had 14 transits, 10 in November and 4 in May, "including the grazing transits in May 1937 and November 1999" [@tr-es1961] [@tr-es1992]. The 1992 Supplement adds that the twenty-first century has "five transits in May and nine in November" [@tr-es1992].

## Venus: the 8, 105.5, 8 and 121.5 year pattern

Venus transits are governed by one resonance. "The orbital periods of Venus (224.701 days) and Earth (365.256 days) are in an 8 year (2922 days) resonance", with 13 Venus orbits in 8 Earth years, but "Venus arrives at the eight year rendezvous about 2.45 days earlier than Earth" [@tr-nasa-venus-catalog]. A pair of transits 8 years apart is therefore possible, but not a third. "After the third eight-year cycle, Venus arrives too early for a transit to occur. The next transit season occurs either 105.5 years or 121.5 years later at the opposite node" [@tr-nasa-venus-catalog]. The 1961 Supplement lists the historical intervals as 8, 121.5, 8, 105.5 and 8 years up to 1882, and states that "the accidental relationships ... between the periods of revolution of the Earth and Venus are dominant" [@tr-es1961].

The full cycle, 8 + 105.5 + 8 + 121.5 = 243 years or about 88,756 days, defines a Venus series. "Such transit series are quite long-lived and may last 5,000 years or more." Series 4 runs from −1763 to 2854 with 20 transits [@tr-nasa-venus-catalog]. The pairs are not permanent. "Occasionally, one of the eight year double-transits may disappear from the catalog for several centuries because one of them is a near miss", as in 1388, 1145, 902 and earlier [@tr-nasa-venus-catalog]. In the six millennia from 2000 BCE to 4000 CE there are 81 transits, 44 in June and 37 in December [@tr-nasa-venus-catalog]. The telescopic transits are 1631, 1639, 1761, 1769, 1874, 1882, 2004 and 2012, and the next pair is 2117 December 11 and 2125 December 8 [@tr-nasa-transit-index].

## Grazing, partial and topocentric-only transits

A transit can reach only part of the Earth. The catalogue shows this by dashes in the contact columns. The 1937 May 11 Mercury transit has contacts I and IV at 08:53 and 09:06 UT but no II or III, with a minimum separation of 955.5 arcseconds [@tr-nasa-mercury-catalog]. From the Earth's centre the planet never got wholly inside the disc. The 1999 November 15 transit is labelled "graze" with a minimum separation of 963.0 arcseconds [@tr-nasa-transit-index]. For it Espenak wrote that "the actual contact times may differ by tens of minutes depending on the observer's actual geographic coordinates" and that "as one approaches the southern limit of the total transit, contacts II and III will converge and vanish while the period between contacts I and IV decreases" [@tr-nasa-oh1999]. That is the transit analogue of a [?tr-grazing-transit|graze zone].

The Venus catalogue has rows with no geocentric contacts at all. The row for −0540 November 19 gives a minimum separation of 1012.3 arcseconds and dashes in all four contact columns [@tr-nasa-venus-catalog]. The row is kept because a transit is seen from part of the Earth even though none occurs at the geocentre. Rows −1763 and −0920 have contacts I and IV only [@tr-nasa-venus-catalog]. A catalogue built only from geocentric contacts would miss the −0540 event. The enumeration test must therefore use the penumbral cone and the Earth's radius, as Stellarium's $\gamma \le 0.9972 + L_1$ test does [@tr-stellarium-transits].

## How the catalogues were computed

### Espenak's NASA catalogues

The catalogues give, for each transit, the four geocentric contacts in UT to the minute, the time of [?tr-greatest-transit|greatest transit], the minimum separation in arcseconds, the Sun's right ascension and declination, Greenwich sidereal time at 0h UT, and the series number [@tr-nasa-catalog-key]. The key states the method and the ΔT recipe. "Transit predictions are based on algorithms and elements published in Transits by Jean Meeus (Willmann-Bell, 1989)." [?delta-t|ΔT] "was calculated from empirical expressions by Stephenson [1997]" before 1600, "obtained from published observations" from 1600 to the present, and "extrapolated from current values" for the future [@tr-nasa-catalog-key]. The catalogue pages add that the "Besselian elements for the transit predictions are from Transits by Jean Meeus" [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog]. Meeus's *Astronomical Algorithms* has no transit chapter. Its preface says that "elements and formulae about transits of Mercury and Venus across the Sun's disk are provided in our Transits (1989)" [@cat-meeus-1991-aa].

Espenak's individual transit articles name the ephemeris. They are not all the same:

| Prediction | Ephemeris stated | Algorithms stated |
|---|---|---|
| 1999 Mercury | JPL DE200 [@tr-nasa-oh1999] | Explanatory Supplement 1974 |
| 2012 Venus | VSOP87 [@tr-nasa-oh2012] | Meeus 1989, Explanatory Supplement 1974 |
| 2016 Mercury | JPL DE406 [@tr-ew-tm2016] | Meeus 1989, Explanatory Supplement 1974 |
| 2019 Mercury | JPL DE406 [@tr-ew-tm2019] | Meeus 1989, Explanatory Supplement 1974 |
| EclipseWise index and 2018 Canon | JPL DE430 and DE431 [@tr-ew-transit-index] | Explanatory Supplement 1974, Meeus 1989 |

The 2018 *Six Millennium Canon of Transits: −1999 to +4000* is a book from Astropixels Publishing [@tr-espenak-2018-canon]. No NASA Technical Publication on transits by Espenak and Meeus is listed on the NASA or EclipseWise transit pages. Jubier's database page describes its data as "provided by Fred Espenak and Jean Meeus (NASA Technical Publication)" without a report number [@tr-jubier-6mcst]. The web catalogues on eclipse.gsfc.nasa.gov carry no report number either [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog]. The catalogue's time columns are geocentric. The visibility page warns that this "may introduce an error in the actual contact times of up to 3 minutes for Mercury and up to 10 minutes for Venus" [@tr-nasa-visibility].

### IMCCE

For the 2004 predictions the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) used VSOP87 with Lieske precession, Wahr nutation and Aoki sidereal time, and the IAU 1976 constants. It states that "for these calculations, as for the making of our canons of transits of Mercury and Venus, we used formulae identical to that of the solar eclipses using the elements of Bessel" [@tr-eso-eis-b1].

### Stellarium

Stellarium's AstroCalc dialog has a "Transits across the Sun" table. Its `generateTransits` steps through inferior conjunctions from a reference Julian date with a fixed synodic period, 115.8774771 days for Mercury from JD 2451612.023 and 583.921361 days for Venus from JD 2451996.706 [@tr-stellarium-transits]. At each conjunction it computes geocentric elements, iterates the time of least $\sqrt{x^2+y^2}$, in a loop commented "0.1 second of accuracy", with `dt = -(x*xdot + y*ydot)/n2`, and accepts a transit when `gamma <= (0.9972+L1)` [@tr-stellarium-transits]. The threshold is the solar-eclipse test for a shadow touching the Earth, in which 0.9972 is the geocentric distance at which the axis grazes the ellipsoid (see [Besselian elements](../../10-shared/01-foundations/besselian-elements.md)).

### Swiss Ephemeris

The `swevents` utility lists "transit begin", "transit middle" and "transit end" for Mercury and Venus. It finds minimum elongation at inferior conjunction and then steps by $\sqrt{r^2 - e^2}$ divided by the relative motion, where $r$ is the sum of the semidiameters and $e$ the minimum elongation [@tr-swisseph-swevents]. This is a linear-motion estimate of contacts I and IV only, without interior contacts or parallax. Its constants are `SUN_RADIUS` 959.63 arcseconds, `VENUS_RADIUS` 8.34 and `MERCURY_RADIUS` 3.36 arcseconds at 1 au, cited to "AA96 E43" [@tr-swisseph-swevents].

## Elements: the Explanatory Supplement's heliocentric form

The 1961 Supplement computes transits of Mercury "according to an extension of the heliocentric method described by Simon Newcomb" (1882), with Mercury from Newcomb's *Tables of Mercury* and the Earth from his *Tables of the Sun* [@tr-es1961]. The 1992 Supplement says this method was used "prior to and including the 1986 transit of Mercury", and that later almanac work uses Chauvenet's method with "apparent geocentric ephemerides of the Sun and planet" computed from a modern ephemeris such as DE200 [@tr-es1992]. The geometry is that of a solar eclipse. "The heliocentric method of computing transits of Mercury is adapted from Bessel's theory of eclipses, in which the planet is substituted for the Moon. The exterior tangents to the Sun and the planet generate the cone of umbra, which has its vertex between Mercury and the Earth. The interior tangents form the cone of penumbra, with vertex between Mercury and the Sun." Exterior contacts occur when the observer is on the [?penumbral-cone|penumbral cone] and interior contacts when on the [?umbral-cone|umbral cone] [@tr-es1961].

![Contacts I and IV are external tangencies and II and III internal ones, so a larger solar semidiameter moves I and II earlier and III and IV later. The least separation $b$ is reached at greatest transit, and the position angle $P$ is counted from north through east [@tr-es1961] [@tr-nasa-catalog-key].](img/tr-contact-geometry.svg)

The [?fundamental-plane|fundamental plane] differs from the eclipse convention in its origin and axes. "As in the theory of eclipses, the fundamental plane ... is perpendicular to the axis of shadow and passes through the centre of the Earth. In the case of transits, however, the origin of coordinates is the intersection of the axis of shadow with the xy-plane; the x-axis is parallel to the plane of the ecliptic, positive in the direction opposite to the motion of Mercury around the Sun; the y-axis is positive towards the north" [@tr-es1961]. The axes are therefore ecliptic-aligned rather than equator-aligned, and the origin is on the shadow axis rather than at the Earth's centre.

With $l, b, r$ the heliocentric ecliptic longitude, latitude and radius vector of Mercury and $l_\oplus, b_\oplus, R$ those of the Earth, the Earth's centre has coordinates

$$
x = R\sin m\sin M = R\cos b_\oplus\sin(l - l_\oplus),\qquad
y = R\sin m\cos M = R\{\cos b\sin b_\oplus - \sin b\cos b_\oplus\cos(l - l_\oplus)\}
$$

where $m$ is "the angular distance of the planet from the Earth as seen from the centre of the Sun" and $M$ the position angle of the Earth's centre from the y-axis [@tr-es1961]. Since all angles except $M$ are small,

$$
m\sin M = l - l_\oplus = v,\qquad m\cos M = b_\oplus - b = u,\qquad u^2 + v^2 = m^2,
$$
$$
v' = l' - l'_\oplus = n\sin N,\qquad u' = b'_\oplus - b' = n\cos N,\qquad u'^2 + v'^2 = n^2,
$$

with primes for hourly variations [@tr-es1961]. These $u, v, m, n, M, N$ are heliocentric angles. They are not the solar-eclipse quantities of the same letters in [Contact times and magnitude](../04-local-circumstances/contact-times-and-magnitude.md), where $u = x - \xi$ is a distance in Earth radii. A program that implements both should name them apart.

The cone angles use the semidiameters at unit distance, $s$ for the planet and [?solar-semidiameter-s0|$s_0$] for the Sun, "their adopted values being 3".34 and 959".63 respectively" [@tr-es1961]. This note does not reproduce the Supplement's printed equation for the cone angles. The worked example evaluates $f_2 = 956''.29/r$ and notes that $s_0 - s = 956''.29$, so the umbral angle is $f_2 = (s_0 - s)/r$, with $f_1 = (s_0 + s)/r$ for the penumbra by symmetry [@tr-es1961]. The shadow radii on the fundamental plane, divided by $R$, are

$$
L_1 = \sec f_1\,(f_1\cos m - s_0/R),\qquad L_2 = \sec f_2\,(f_2\cos m - s_0/R)
$$

and "the geocentric contacts take place at the instants at which the distance $R\sin m = Rm$ of the centre of the Earth from the origin is equal to $R_1$ for exterior contacts or $R_2$ for interior contacts", that is when $m = L_1$ or $m = L_2$ [@tr-es1961]. Here $L_1, L_2$ are angles in arcseconds. They are not the eclipse radii $l_1, l_2$ in Earth radii.

### Light-time and aberration

"The contacts occur when the apparent positions of points on the limbs of Mercury and of the Sun coincide." The ray that reaches the observer at time $T$ "left the Sun at some previous time $T - \tau_2$ and grazed the planet at a time $T - \tau_2 + \tau_1$. Therefore ... the geometric coordinates of Mercury at time $T - \tau_2 + \tau_1$ must be combined with the geometric coordinates of the Earth at time $T$" [@tr-es1961]. The correction is

$$
\tau_2 - \tau_1 = 0.138439\,(R - r)\ \text{hours},
$$

"the factor being the time in hours for light to travel unit distance, as derived from the constant of aberration", replaced by 0.138614 "for 1968 onwards" [@tr-es1961]. The 1992 Supplement restates the same rule in its section on differential planetary aberration [@tr-es1992]. An implementation that takes apparent geocentric places from a modern ephemeris has [?light-time|light-time] built in, and must not apply this step again.

## Elements: the geocentric vector form in Stellarium

Stellarium's `TransitBessel::computeElements` cites the 1961 Supplement but uses the geocentric solar-eclipse construction. It takes the apparent equatorial places of the Sun and planet, forms the point Z, and computes $x, y, d, \mu, \tan f_1, \tan f_2, L_1, L_2$ in Earth equatorial radii [@tr-stellarium-transits]. The code reads:

```
const double b = pdistanceER / rss;
const double a = raSun - ((b * cos(dePlanet) * raDiff) / ((1 - b) * cos(deSun)));
besD = deSun - (b * (dePlanet - deSun) / (1 - b));
...
double k = object->getEquatorialRadius()/ssystem->getEarth()->getEquatorialRadius();
const double f1 = asin((SunEarth + k) / (rss * (1. - b)));
const double f2 = asin((SunEarth - k) / (rss * (1. - b)));
besL1 = z * bestf1 + (k / cos(f1));
besL2 = z * bestf2 - (k / cos(f2));
besMu = gast - a * M_180_PI;
```

Here `SunEarth` is 109.12278, the ratio 696000/6378.1366, and `rss` is the Sun's distance in Earth radii from 23454.7925 Earth radii per au [@tr-stellarium-transits]. The `k` of this code is the planet-to-Earth radius ratio. It uses the planet radius from `ssystem_major.ini`, 2440.53 km for Mercury and 6051.8 km for Venus [@tr-stellarium-ssystem]. It plays the role of the lunar $k$ in the eclipse formulas, but the value is 0.383 or 0.949, not 0.2725. Chauvenet used the same substitution in 1863, with "for Venus, k = 0.9975" and "for Mercury, k = 0.3897" in his eclipse formulae [@bes-chauvenet-1863]. The ratio $b$ of the planet's distance to the Sun's is about 0.28 for Venus and 0.55 to 0.68 for Mercury at the modern transits [@tr-jubier-mtc-js] [@tr-jubier-vtc-js]. For the Moon it is about 0.0026, so the terms in $b$ that are small corrections for an eclipse are large for a transit. Chauvenet noted that "since b is no longer a small quantity, it will be necessary to employ the exact formulae" [@bes-chauvenet-1863].

## Elements: Jubier's polynomial form

Jubier's transit calculators store one array per transit [@tr-jubier-mtc-js] [@tr-jubier-vtc-js]. Each array holds the date, a reference hour $t_0$ in TT, two ΔT values, cubic polynomials in $T$ (hours from $t_0$) for $X$ and $Y$ in arcseconds, quadratic polynomials for the declinations and Greenwich hour angles of the Sun and the planet in degrees, and quadratic polynomials for their geocentric distances in au. For 2019 November 11 the array begins:

```
2019, 11, 11, 15.0, 69.35, 69.35,
  -144.0777,    323.1807,     0.00713,    -0.001421,
    18.3080,    145.8275,    -0.08746,    -0.000927,
```

so $X = -144.0777 + 323.1807\,T + 0.00713\,T^2 - 0.001421\,T^3$ arcseconds and $Y = 18.3080 + 145.8275\,T - \ldots$ arcseconds, with $t_0 = 15$ h and ΔT = 69.35 s [@tr-jubier-mtc-js]. The relative motion at $t_0$ is $\sqrt{323.18^2 + 145.83^2} = 354.6$ arcseconds per hour. The Sun's distance polynomial starts at 0.9900365 au and the planet's at 0.6758643 au. Espenak credits Meeus's *Transits* for his elements [@tr-nasa-mercury-catalog], and none of the sources of this topic describes the Meeus element format. Whether Jubier's arrays copy that format is therefore not established. The contact solution that consumes them is quoted in [Contacts and local circumstances](contacts-and-local-circumstances.md).

## Elements: the yearbook form

The Astronomical Yearbook of the Institute of Applied Astronomy of the Russian Academy of Sciences (IAA RAS) prints the elements at the "Universal time of geocentric conjunction of the Sun and of Mercury in right ascension": the right ascensions, declinations, hourly motions, equatorial [?horizontal-parallax|horizontal parallaxes] and apparent semidiameters of the Sun and the planet, followed by linear expressions for each coordinate in $(T - t_0)$ hours of UT [@tr-iaa-2016] [@tr-iaa-2019]. For 2019 it gives conjunction at 15h 25m 35.1s UT, Sun parallax 8.88 and Mercury 13.01 arcseconds, apparent semidiameters 16 arcminutes 9.29 arcseconds and 4.98 arcseconds, and "TDT − UT1 = 70.0s" [@tr-iaa-2019]. This is the form of Chauvenet's method, which the 1992 Supplement names as the almanac method [@tr-es1992].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Explanatory Supplement 1961, section 9F [@tr-es1961] | The node limits by node with their dates and frequencies, Newcomb's heliocentric method with formulas, the transit fundamental plane, the light-time rule with its constant, a full worked example for 1960 November 7. Mercury only. |
| Explanatory Supplement 1992, sections 1.541, 3.257 and 8.5 [@tr-es1992] | The statement that the heliocentric method ended with 1986 and that Chauvenet's apparent-place method replaced it. No formulas of its own. |
| Chauvenet, *Manual*, Arts. 356 to 358 [@bes-chauvenet-1863] | The planet-for-Moon substitution with $k$ for Venus and Mercury, and Lagrange's method in Chauvenet's improved form. |
| Espenak, NASA transit catalogues [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog] [@tr-nasa-catalog-key] | The complete lists, the recurrence arithmetic, the series, the ΔT recipe and the dependence on Meeus 1989. |
| Espenak, individual transit articles [@tr-nasa-oh1999] [@tr-nasa-oh2012] [@tr-ew-tm2016] [@tr-ew-tm2019] | The ephemeris version for each event. |
| IMCCE for VT-2004 [@tr-eso-eis-b1] | A complete statement of the theories and constants behind one prediction. |
| IAA RAS yearbook [@tr-iaa-2016] [@tr-iaa-2019] | Almanac elements at conjunction with stated ΔT. |
| Stellarium source [@tr-stellarium-transits] | A public implementation of enumeration and geocentric transit elements. |
| Jubier's calculators [@tr-jubier-mtc-js] [@tr-jubier-vtc-js] | Polynomial elements with ΔT for each modern transit, in readable code. |
| Swiss Ephemeris `swevents` [@tr-swisseph-swevents] | A minimal exterior-contact finder with its constants. |

## What a developer should do

1. Enumerate by searching the ephemeris, not by the cycles. Step through inferior conjunctions, compute the least geocentric separation, and keep every event where the separation is below the sum of the solar and planetary semidiameters plus the solar and planetary parallax difference. Stellarium's $\gamma \le 0.9972 + L_1$ test in Earth radii is one implementation [@tr-stellarium-transits]. Use the 13, 33, 46, 8 and 243 year cycles only to label series and to check completeness against the catalogues [@tr-nasa-mercury-catalog] [@tr-nasa-venus-catalog].
2. Keep events with no geocentric interior contacts, and events with no geocentric contacts at all. The −0540 Venus row shows that the second kind exists [@tr-nasa-venus-catalog].
3. Use apparent geocentric places of the Sun and planet from a JPL ephemeris, so that light-time and aberration are included. Do not then apply the Supplement's $0.138439\,(R-r)$ back-dating [@tr-es1961].
4. Record the ephemeris, ΔT, $s_0$ and the planet's semidiameter with every element set. Espenak's predictions alone used four ephemerides between 1999 and 2018 [@tr-nasa-oh1999] [@tr-nasa-oh2012] [@tr-ew-tm2019] [@tr-ew-transit-index].
5. Read section 9F of the 1961 Supplement first and reproduce Example 9.26, whose interior egress for 1960 November 7 is 19h 10m 40.8s ET [@tr-es1961]. Then reproduce Espenak's catalogue minute values for 1601 to 2300 [@tr-nasa-mercury-catalog].

## What this changes

The enumeration stage of the pipeline generalises from the Moon to a list of bodies. The eclipse code's element generator can serve transits if the body radius $k$, the cone construction and the exact rather than small-$b$ formulas for the point Z are parameters. The catalogue schema needs a field for missing contacts and for events that are only topocentric.

## Open questions

- Meeus, *Transits* (Willmann-Bell, 1989): obtain the book and record its element format, its constants for $s_0$ and the planetary semidiameters, and its contact formulas, since the NASA catalogues depend on it [@tr-meeus-1989-transits].
- The 1961 Supplement's formula for the node limit θ: obtain a clean image of page 262 to transcribe it [@tr-es1961].
- Espenak's *Six Millennium Canon of Transits* (2018): obtain the book to record its ΔT model, constants and Mercury transit count for −1999 to +4000 [@tr-espenak-2018-canon].
- The Mercury catalogue page says ten series and the key says twelve. Obtain Espenak's series assignment table to settle the count [@tr-nasa-mercury-catalog] [@tr-nasa-catalog-key].
- Chapter 11 of the 2013 Explanatory Supplement: check whether it adds a transit section that replaces the 1992 pointer to Chauvenet [@tr-es1992].
