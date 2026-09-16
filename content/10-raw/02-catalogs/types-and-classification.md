---
title: Types and classification
description: The inequalities in gamma and the umbral radius that separate partial, annular, total, hybrid, central and non-central eclipses, and the definition and derivation of every quantity a catalogue lists per eclipse.
order: 2
status: working
updated: 2026-09-15
tags: [eclipse-types, gamma, hybrid, non-central, magnitude, greatest-eclipse]
---

::: summary
- **Four types, one geometric rule.** Partial: the penumbra touches Earth but the umbra and antumbra miss. Annular: the antumbra crosses Earth. Total: the umbra crosses Earth. Hybrid: both do along different parts of one path [@cat-espenak-meeus-2009-catalog].
- **Central means $|\gamma| < 0.997$.** "If gamma is between +0.997 and −0.997, the eclipse is a central one. ... The limiting value 0.997 differs from unity because of the flattening of Earth." Meeus's series uses 0.9972 [@cat-espenak-meeus-2009-catalog] [@cat-meeus-1991-aa].
- **Total versus annular is the sign of the umbral radius.** In Meeus's units $u < 0$ is total and $u > 0.0047$ is annular. Between, $\omega = 0.00464\sqrt{1-\gamma^2}$ decides hybrid. In Astronomy Engine the umbral radius at the geoid must exceed 0.014 km for total [@cat-meeus-1991-aa] [@cat-astronomy-engine].
- **Non-central umbral eclipses exist and are rare.** 94 of 7,698 umbral and antumbral eclipses in the 5000-year catalogue have an axis that misses Earth while one edge of the umbra or antumbra grazes it. Their $|\gamma|$ runs from 0.9972 to 1.0242 in the catalogue [@cat-espenak-meeus-2009-catalog] [@cat-nasa-5mkse-ascii].
- **Hybrids come in three classes.** 519 of 569 begin annular, become total and end annular. 24 begin total and end annular (H2). 26 begin annular and end total (H3). No non-central hybrid occurs in five millennia [@cat-espenak-meeus-2009-catalog].
- **Every catalogue column is defined at one instant.** Greatest eclipse is the minimum distance between shadow axis and geocentre. Magnitude, latitude, longitude, altitude, path width and duration are all evaluated there, and for partial eclipses at the surface point nearest the axis, where the Sun's altitude is 0° [@cat-espenak-meeus-2009-catalog].
:::

**The question.** What exact inequalities turn a $\gamma$ and an umbral radius into "partial", "annular", "total", "hybrid", "central" or "non-central", how often each type occurs, and what does every number in a catalogue row mean and how is it computed? This note collects the definitions from the NASA catalogue, the thresholds from Meeus and from two open implementations, and observed ranges from the catalogue file itself. Enumeration is in [Enumerating eclipses](enumerating-eclipses.md).

## The four types and the shadow cones

The catalogue's definitions, Section 1.2.8 [@cat-espenak-meeus-2009-catalog]:

1. "P = Partial Solar Eclipse (Moon's penumbral shadow traverses Earth; Moon's umbral and antumbral shadows completely miss Earth)"
2. "A = Annular Solar Eclipse (Moon's antumbral shadow traverses Earth; Moon is too far from Earth to completely cover the Sun)"
3. "T = Total Solar Eclipse (Moon's umbral shadow traverses Earth (Moon is close enough to Earth to completely cover the Sun)"
4. "H = Hybrid Solar Eclipse (Moon's umbral and antumbral shadows traverse different parts of Earth; eclipse appears either total or annular along different sections of its path. Hybrid eclipses are also known as annular-total eclipses.)" This is the [?hybrid-eclipse|hybrid eclipse] and the catalogue's [?non-central-eclipse|non-central] class is defined below.

![One quantity separates the four types: where the vertex of the umbral cone falls relative to the Earth's surface. It falls short for an annular eclipse, so the widening antumbra lands; it falls beyond for a total one, so the umbra itself lands; and for a hybrid it falls between the two, so the same eclipse changes type along its own path. The dashed arc in the fourth panel carries every point as far from the Moon as the vertex is: the middle of the path lies inside it and is total, the ends lie outside it and are annular. A partial eclipse is the case where the axis misses the Earth and only the penumbra lands.](img/eclipse-types.svg){.fig3d scene="eclipse-types"}

The NASA glossary defines the cones: the [?umbra|umbra] is "the darkest part of the Moon's shadow. From within the umbra, the Sun is completely blocked by the Moon"; the [?antumbra|antumbra] is "that part of the Moon's shadow that extends beyond the umbra"; the [?penumbra|penumbra] is "the weak or pale part of the Moon's shadow" [@cat-nasa-glossary]. In [?besselian-elements|Besselian elements] the umbral radius on the [?fundamental-plane|fundamental plane] is $l_2$, negative when the umbral vertex lies above the plane, and the penumbral radius is $l_1$. Whether a given surface point sees the umbra or the antumbra is the sign of the umbral radius projected to that point.

## Central and non-central

The catalogue's footnotes to the type codes define the [?central-eclipse|central eclipse] and its [?one-limit-eclipse|one-limit] variant: "A central eclipse is an annular, total or hybrid eclipse in which the central axis of the Moon's shadow traverses Earth, thereby producing a central line in the eclipse track. The paths of most central eclipses have both a northern and southern limit. On rare occasions when the umbral or antumbral shadow grazes Earth, the resulting eclipse track may have only one limit." And: "A non-central eclipse is an annular, total or hybrid eclipse in which the central axis of the Moon's shadow misses Earth, while one edge of the umbra or antumbra grazes Earth producing a ground track with one limit and no central line" [@cat-espenak-meeus-2009-catalog].

Section 3.1 turns this into three categories for umbral and antumbral eclipses: central with two limits, central with one limit, non-central with one limit. The statistics [@cat-espenak-meeus-2009-catalog]:

| Class | Annular | Total | Hybrid |
|---|---|---|---|
| All | 3,956 | 3,173 | 569 |
| Central, two limits | 3,827 (96.7%) | 3,121 (98.4%) | 569 (100%) |
| Central, one limit | 61 (1.5%) | 26 (0.8%) | 0 |
| Non-central, one limit | 68 (1.7%) | 26 (0.8%) | 0 |

"An estimate of the mean frequency of non-central hybrid eclipses is one out of every 600 million eclipses or once every 250 million years (Meeus, 2002a)" [@cat-espenak-meeus-2009-catalog].

### The inequalities

Three sources give the inequalities in three different units. They agree on the geometry.

**Meeus, units of Earth's equatorial radius** [@cat-meeus-1991-aa]. With [?gamma|$\gamma$] the least distance of the axis from the geocentre and $u$ the umbral radius in the fundamental plane:

- central: $|\gamma| < 0.9972$
- non-central total or annular: $0.9972 < |\gamma| < 0.9972 + |u|$ (always inside $|\gamma| < 1.0260$)
- partial: $0.9972 + |u| \le |\gamma| \le 1.5433 + u$
- no eclipse: $|\gamma| > 1.5433 + u$

Here $0.9972$ is the semi-minor axis of the Earth's cross-section for a shadow axis inclined to the equator, expressed in equatorial radii, and $0.5461 = (1.5433 - 0.9972)$ is the mean difference between the penumbral and umbral radii in the fundamental plane. The penumbral radius is $u + 0.5461$, so the no-eclipse condition is $|\gamma| > 0.9972 + l_1$: the axis is farther than an Earth radius plus a penumbral radius.

![Two of the six regions are thin, which is why the classification is delicate. Every boundary drawn is one of Meeus's inequalities: the non-central umbral band is only $|u|$ thick, at most about 0.02 Earth radii, and the hybrid wedge closes to nothing as $|\gamma|$ approaches 1 because the curve $u = 0.00464\sqrt{1-\gamma^2}$ is the amount by which the umbral radius shrinks between the fundamental plane and the surface [@cat-meeus-1991-aa].](img/gamma-u-classification.svg)

**Swiss Ephemeris, astronomical units** [@cat-swisseph-swecl]. With $r_0$ the axis distance from the geocentre, $d_e$ the equatorial radius, $\cos f_1$ and $\cos f_2$ the cosines of the umbral and penumbral cone half-angles, $d_0$ the umbral diameter and $D_0$ the penumbral diameter on the fundamental plane:

- central: $d_e \cos f_1 \ge r_0$
- non-central: $r_0 \le d_e \cos f_1 + |d_0|/2$
- partial: $r_0 \le d_e \cos f_2 + D_0/2$
- otherwise no eclipse

The factor $\cos f_1$ plays the role of Meeus's 0.9972 and the code omits flattening in this test, though it applies `earthobl = 1 - EARTH_OBLATENESS` when it intersects the axis with the surface.

**Astronomy Engine, kilometres** [@cat-astronomy-engine]. An eclipse exists when `shadow.r < shadow.p + EARTH_MEAN_RADIUS_KM` with the mean radius 6371.0 km. It is central when the axis intersects the oblate geoid, which `GeoidIntersect` tests directly. There is no non-central class.

The observed catalogue ranges confirm the thresholds. Parsing the 11,898 rows of the NASA ASCII catalogue: central eclipses (codes without + or −) reach a maximum $|\gamma|$ of 0.9972, non-central eclipses span 0.9972 to 1.0242, the 87 one-limit central eclipses (codes n and s) span 0.9719 to 0.9972, and partial eclipses span 0.9985 to 1.5706 [@cat-nasa-5mkse-ascii]. The partial minimum 0.9985 exceeding 0.9972 shows the umbra-graze band in practice: between 0.9972 and about 1.024 an eclipse can be either partial or non-central umbral depending on $|u|$.

## Total, annular and hybrid

For a central eclipse Meeus's rule is: "if $u < 0$, the eclipse is total; if $u > +0.0047$, the eclipse is annular; if $u$ is between 0 and +0.0047, the eclipse is either annular or annular-total." The tie-break: compute $\omega = 0.00464\sqrt{1 - \gamma^2}$ and "if $u < \omega$, the eclipse is annular-total; otherwise it is an annular one" [@cat-meeus-1991-aa]. The reasoning is that $u$ is the umbral radius on the fundamental plane through the geocentre, while the surface at the sub-shadow point lies $\sqrt{1-\gamma^2}$ Earth radii closer to the Moon, where the umbral radius is smaller by that height times $\tan f_2$. The constant 0.00464 is $\tan f_2$ for a mean geometry, so $\omega$ is the amount by which the umbral radius shrinks between the fundamental plane and the surface. If the umbra is annular at the geocentre plane but total at the surface, the eclipse is hybrid.

Rigorous implementations replace the constant with the actual value along the path. The Swiss Ephemeris evaluates the umbral core diameter at the surface at three instants, maximum, central-line start and central-line end, and flags `SE_ECL_ANNULAR_TOTAL` when the sign differs between the maximum and either end [@cat-swisseph-swecl]. This also yields the catalogue's three hybrid classes: "Most hybrid eclipses are of class 1 in which the central path begins annular, changes to total, and then reverts back to annular (ATA). In class 2 hybrids, the eclipse begins as total and end as annular (TA). Finally, class 3 hybrid eclipses begin as annular and end as total (AT). ... Asymmetric hybrids always occur when the vertex of the Moon's umbral shadow passes through Earth's fundamental plane during the eclipse." Class 1 occurs in 519 of 569, class 2 in 24 and class 3 in 26. The catalogue lists class 1 as H and the others as H2 and H3 [@cat-espenak-meeus-2009-catalog]. Recent examples: ATA 2005 Apr 08 and 2023 Apr 20, AT 2013 Nov 03, TA 1825 Dec 09 [@cat-espenak-meeus-2009-catalog].

Hybrid frequency is not uniform. "Their frequency is modulated by a sinusoidal cycle lasting approximately seventeen centuries. During some periods (e.g., 1001 to 1800 CE), there are 15 to 24 hybrid eclipses per century. At other epochs (e.g., 2201 to 2800 CE), the number of hybrids can drop below 5 eclipses per century" [@cat-espenak-meeus-2009-catalog].

Astronomy Engine collapses all of this to one test at greatest eclipse, `EclipseKindFromUmbra(k)` returning total when the umbral radius at the geoid exceeds 0.014 km and annular otherwise, "to match Espenak test data" [@cat-astronomy-engine]. A hybrid that is total at greatest eclipse therefore reports as total, one that is annular there as annular.

## The catalogue codes

The second character of the type field [@cat-espenak-meeus-2009-catalog] [@cat-nasa-secatkey]:

| Code | Meaning | Count in catalogue |
|---|---|---|
| m | Middle eclipse of Saros series | Am 72, Tm 72, Hm 17 |
| n | Central eclipse with no northern limit | An 36, Tn 14 |
| s | Central eclipse with no southern limit | As 25, Ts 12 |
| + | Non-central eclipse with no northern limit | A+ 34, T+ 9 |
| − | Non-central eclipse with no southern limit | A− 34, T− 17 |
| 2 | Hybrid path begins total and ends annular | H2 24 |
| 3 | Hybrid path begins annular and ends total | H3 26 |
| b | Saros series begins | Pb 163 |
| e | Saros series ends | Pe 162 |

The counts were tallied from the ASCII file [@cat-nasa-5mkse-ascii]. "Qualifiers 1 through 5 are used with annular, total or hybrid eclipses but not partial eclipses. Qualifiers 6 and 7 apply only to special classes of hybrid eclipses while qualifiers 8 and 9 are used exclusively with partial eclipses" [@cat-espenak-meeus-2009-catalog].

## Numbers per century

From the catalogue's Table 3-5 and text: 222 to 255 eclipses per century, mean 238.0, mean 238.9 over 1501 to 2500, with the 20th century at 228 and the 21st at 224. From the ASCII file: 1901 to 2000 has 78 P, 73 A, 71 T, 6 H with 5 non-central; 2001 to 2100 has 77 P, 72 A, 68 T, 7 H with 3 non-central; 2101 to 2200 has 79 P, 87 A, 65 T, 4 H with 5 non-central [@cat-espenak-meeus-2009-catalog] [@cat-nasa-5mkse-ascii]. Over five millennia the shares are 35.3% partial, 33.2% annular, 26.7% total and 4.8% hybrid [@cat-nasa-secatalog].

## The quantities catalogued per eclipse

Each row of the catalogue holds the following. Definitions are quoted from Section 1.2 of the catalogue and from the catalogue key [@cat-espenak-meeus-2009-catalog] [@cat-nasa-secatkey]. The derivation column says how the number follows from the Besselian elements $x, y, d, \mu, l_1, l_2, \tan f_1, \tan f_2$ as functions of time.

**Calendar date and [?tt|TD] of greatest eclipse.** TD, TDT and TT are one scale, printed as TDT or TD in NASA tables and called ET before 1984. "The instant of greatest eclipse occurs when the distance between the axis of the Moon's shadow cone and the center of Earth reaches a minimum. For partial eclipses, the instant of greatest eclipse differs slightly from the instant of greatest magnitude primarily because of Earth's flattening. For total eclipses, the instant of greatest eclipse differs slightly from the instant of greatest duration." Julian calendar before 1582 Oct 04, Gregorian from 1582 Oct 15, astronomical year numbering with a year 0. Derivation: minimise $m(t) = \sqrt{x(t)^2 + y(t)^2}$. With cubic polynomials in $t$ this is a one-dimensional root of $x x' + y y' = 0$. The catalogue states greatest eclipse "does not coincide with that of apparent ecliptic conjunction (i.e., New Moon), nor with the time of conjunction in Right Ascension" because the Moon crosses the ecliptic at about 5° [@cat-espenak-meeus-2009-catalog].

**ΔT.** "The arithmetic difference, in seconds, between Terrestrial Dynamical Time and Universal Time." UT of greatest eclipse is TD minus ΔT. The catalogue lists the adopted value, from the polynomials of its Section 2.7 with correction $c$ [@cat-espenak-meeus-2009-catalog].

**Lunation number.** "The number of synodic months or lunations since New Moon on 2000 Jan 06. The Brown Lunation Number can be calculated from it by adding 953." Derivation: the integer $k$ of the mean new moon [@cat-espenak-meeus-2009-catalog].

**Saros number.** Van den Bergh numbering, odd at the ascending node, even at the descending node. Derivation: Kluepfel's formula from the lunation number, verified on all rows [@cat-espenak-meeus-2009-catalog] [@cat-vangent-cycles] [@cat-nasa-5mkse-ascii].

**Type and qualifier.** As above.

**QLE.** A two-character code for the lunar eclipse preceding and succeeding the solar eclipse within about 15 days: n penumbral, p partial, t total, − none [@cat-espenak-meeus-2009-catalog].

**Gamma.** "The minimum distance from the axis of the lunar shadow cone to the center of Earth, in units of Earth's equatorial radius. This distance is positive or negative, depending on whether the axis of the shadow cone passes north or south of Earth's center." Derivation: $\gamma = \pm\min m(t)$ with the sign of $y$ at that instant. Table 1-1 of the catalogue shows the Saros-to-Saros change in $\gamma$ is larger near aphelion (June and July, steps of about 0.074) than near perihelion (December and January, steps of about 0.008) [@cat-espenak-meeus-2009-catalog].

**Eclipse magnitude.** "The fraction of the Sun's diameter occulted by the Moon. For partial eclipses, the eclipse magnitude at the instant of greatest eclipse is given for the geographic position closest to the axis of the Moon's shadow cone. For central eclipses (total, annular, and hybrid), the eclipse magnitude listed is actually the ratio of the topocentric apparent diameters of the Moon and Sun at greatest eclipse." Partial and annular magnitudes are below 1.0, total and hybrid at or above 1.0 [@cat-espenak-meeus-2009-catalog]. Derivation for a partial eclipse: with $\Delta$ the distance from the axis to the nearest surface point in the fundamental plane, the [?eclipse-magnitude|magnitude] is $(l_1 - \Delta)/(l_1 + l_2)$, the standard Besselian expression for the fraction of the diameter covered at a point at distance $\Delta$ inside the penumbra. Meeus's approximate equation is the same expression in mean units, $(1.5433 + u - |\gamma|)/(0.5461 + 2u)$, because $1.5433 + u - |\gamma| = l_1 - (|\gamma| - 0.9972)$ and $0.5461 + 2u = l_1 + l_2$ when $l_1 = u + 0.5461$ and $l_2 = u$ [@cat-meeus-1991-aa]. For central eclipses the ratio of topocentric semidiameters is computed at the surface point on the axis. The Swiss Ephemeris returns both in `swe_sol_eclipse_where`: "attr[0] fraction of solar diameter covered by the moon" and "attr[2] fraction of solar disc covered by moon (obscuration)", with `attr[1] = rmoon / rsun` the diameter ratio [@cat-swisseph-doc] [@cat-swisseph-swecl].

**Latitude and longitude.** "The position of greatest eclipse." For central eclipses this is where the axis meets the surface at that instant. "For both partial and non-central umbral/antumbral eclipses, the latitude and longitude correspond to the point closest to the shadow cone axis at greatest eclipse. The Sun's altitude is always 0° at this location." Derivation: intersect the line $(x, y)$ parallel to the $z$ axis with the ellipsoid, using $d$ and $\mu$ minus the Greenwich hour angle offset from ΔT to rotate into geographic coordinates. Longitude therefore carries the full ΔT uncertainty [@cat-espenak-meeus-2009-catalog].

**Sun altitude and azimuth.** "The Sun's altitude at the geographic position intersected by the axis of the lunar shadow cone is given at the instant of greatest eclipse. For partial eclipses, the Sun's altitude is always 0° because the shadow axis misses Earth." Azimuth is 0° north, 90° east [@cat-espenak-meeus-2009-catalog]. Derivation: the altitude is $\arcsin$ of the $z$ component of the surface point in the fundamental frame, since the axis direction is the direction to the Sun.

**Path width.** "For central eclipses (total, annular, or hybrid), the width of the path of totality or annularity (kilometers) is given at the geographic position intersected by the axis of the lunar shadow cone at the instant of greatest eclipse." Derivation: the umbral radius at the surface, $L_2 = l_2 - \zeta \tan f_2$ with $\zeta$ the height of the surface point above the fundamental plane, doubled and divided by the cosine of the angle between the axis and the local vertical. The Swiss Ephemeris computes the core diameter at the surface as `*dcore = (s/dsmt*(drad*2 - dmoon) - dmoon)*cosf1` and the outline width from it [@cat-espenak-meeus-2009-catalog] [@cat-swisseph-swecl]. The catalogue's two $k$ values make the umbral width narrower for total and wider for annular eclipses than the IAU value would.

**Central line duration.** "The central line duration of the total or annular phase (in minutes and seconds) is given at the geographic position intersected by the axis ... at the instant of greatest eclipse. In the case of a total or hybrid eclipse, this duration is very nearly, but not exactly, the maximum duration of the total phase along the entire umbral path. For an annular eclipse, the duration at greatest eclipse may be near either the minimum or maximum duration of the annular phase along the path. If the annular phase duration exceeds approximately 2.3 min, then it corresponds to the near maximum duration along the central line track. If the annular phase duration is less, however, then it corresponds to a near minimum and the annular duration increases towards the ends of the central path" [@cat-espenak-meeus-2009-catalog]. Derivation: twice the surface umbral radius divided by the speed of the shadow across the surface, which is the derivative of $(x, y)$ minus the rotational velocity of the surface point projected on the fundamental plane. The 2.3 min rule follows from the shadow speed being lowest near greatest eclipse while the antumbral radius is largest at the path ends where the surface is farther from the Moon.

**Catalogue and plate number.** Sequence 1 to 11,898 and the canon plate, 20 maps per plate on 595 plates [@cat-espenak-meeus-2009-catalog].

The Besselian CSV that NASA publishes adds `t0`, the polynomial coefficients `x0..x3`, `y0..y3`, `d0..d2`, `mu0..mu2`, `l10..l12`, `l20..l22`, `tan_f1`, `tan_f2`, the validity window `tmin` and `tmax` of −3 to +3 hours, and a `julian_date` column [@cat-nasa-besselian-csv]. The per-eclipse NASA page for 2024 Apr 08 shows the format: $t_0 = 18.000$ TDT, $x = -0.3182440 + 0.5117116t + 0.0000326t^2$, $y = 0.2197640 + 0.2709589t - 0.0000595t^2$, $d = 7.5862002 + 0.0148440t - 0.0000020t^2$, $l_1 = 0.5358140 + 0.0000618t - 0.0000128t^2$, $l_2 = -0.0102720 + 0.0000615t - 0.0000127t^2$, $\mu = 89.591217 + 15.004080t$, $\tan f_1 = 0.0046683$, $\tan f_2 = 0.0046450$, with greatest eclipse 18:18:29 TDT, $\gamma = 0.3431$, magnitude 1.0566, Saros 139, ΔT 74.0 s [@cat-nasa-sedata-2024].

## Sources compared

| Source | Central test | Total versus annular | Hybrid | Non-central | Units |
|---|---|---|---|---|---|
| Meeus 1991 [@cat-meeus-1991-aa] | $|\gamma| < 0.9972$ | $u < 0$, $u > 0.0047$ | $u < 0.00464\sqrt{1-\gamma^2}$ | $0.9972 < |\gamma| < 0.9972 + |u|$ | Earth equatorial radii |
| NASA catalogue [@cat-espenak-meeus-2009-catalog] | $|\gamma| < 0.997$ | sign of umbral radius at surface with $k = 0.272281$ | path changes sign along track, classes ATA, TA, AT | axis misses, edge grazes | Earth equatorial radii, km |
| Swiss Ephemeris [@cat-swisseph-swecl] | $d_e \cos f_1 \ge r_0$ | sign of core diameter at maximum | sign change at maximum versus central-line ends | $r_0 \le d_e\cos f_1 + |d_0|/2$ | AU internally, km out |
| Astronomy Engine [@cat-astronomy-engine] | axis meets geoid | umbral radius at geoid > 0.014 km | not classified | not classified | km |
| Skyfield PR 1076 [@cat-skyfield-pr-1076] | penumbra, umbra, antumbra versus Earth | umbra versus antumbra | grouped with total | not stated | km |

## What a developer should do

1. Implement the type decision on the umbral radius at the *surface* point under the axis, not on the fundamental plane, and evaluate it at three instants at least, greatest eclipse and the two ends of the central line, so that hybrids and their classes fall out. The Swiss Ephemeris code is the reference pattern [@cat-swisseph-swecl].
2. Keep a non-central class. Ninety-four eclipses in five millennia, and three in the 21st century (2014 Apr 29, 2043 Apr 09, 2043 Oct 03), have a one-limit umbral or antumbral track with no central line. Products that only test "axis meets geoid" call them partial [@cat-espenak-meeus-2009-catalog] [@cat-nasa-5mkse-ascii].
3. Use the catalogue's $k$ pair if the target is agreement with NASA types. The catalogue documents 1986 Oct 03 as the case where $k = 0.2725076$ gives the wrong type [@cat-espenak-meeus-2009-catalog].
4. Compute every catalogued quantity at the instant of minimum $\sqrt{x^2+y^2}$, and for partial eclipses report the surface point nearest the axis with altitude 0°, exactly as the catalogue does, so that rows are comparable.
5. Validate against the ASCII catalogue: types for all 11,898 rows, $\gamma$ to 0.0005, magnitude to 0.001, and the type-code letters n, s, +, −, 2, 3 [@cat-nasa-5mkse-ascii].

## What this changes

Classification is not a post-processing label. It depends on the $k$ constant and on where along the path the umbral radius is evaluated, so the type decision belongs inside the Besselian stage of the pipeline, after path limits are known, not in the enumeration stage. The enumeration stage should only carry a provisional Meeus type.

## Open questions

- Obtain the *Explanatory Supplement to the Astronomical Almanac* (1992 or 2013 edition), chapter on eclipses, to quote the standard formulas for path width and central duration from the elements. The derivations above are stated from the geometry and from the Swiss Ephemeris code, not from the almanac text.
- Obtain Meeus 2002, cited as "Meeus, 2002a" in the catalogue, for the derivation of the one-in-600-million estimate for non-central hybrids.
- Obtain the Astronomy Engine test fixtures that motivated the 0.014 km bias, to see which Espenak eclipses were the marginal cases [@cat-astronomy-engine].
- Obtain the source or documentation for the NASA CSV columns `PNS`, `UNS`, `NCN`, `nSer`, `nSeq`, `nJLE`, which appear to encode limits and Saros sequence but are undocumented [@cat-nasa-besselian-csv].
