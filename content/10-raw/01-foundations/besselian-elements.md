---
title: Besselian elements and the fundamental plane
description: The eight elements, the fundamental-plane geometry, sign conventions, units, time scales, the constants k and s0, and the polynomial form NASA and Meeus publish.
order: 1
status: working
updated: 2026-09-15
tags: [besselian, fundamental-plane, constants, delta-t]
---

::: summary
- **The fundamental plane** is the plane through the Earth's centre perpendicular to the axis of the Moon's shadow. The x axis is its intersection with the equator, positive east. The y axis is positive north. The z axis is parallel to the shadow axis, positive toward the Moon [@bes-es1961] [@bes-es1992].
- **Eight elements** describe the shadow in that plane. $x, y$ are the axis position in Earth equatorial radii, $d, \mu$ the declination and hour angle of the axis direction in degrees, $l_1, l_2$ the penumbra and umbra radii on the plane in Earth equatorial radii, and $\tan f_1, \tan f_2$ the cone half-angles [@bes-nasa-beselm] [@bes-es1992].
- **$l_2$ is negative for a total eclipse** and positive for an annular one. $l_1$ is always positive. The sign comes from $c_2 = z - k\,\mathrm{cosec} f_2$, the height of the umbral vertex above the plane [@bes-es1961] [@bes-es1992].
- **Two lunar radius ratios are in use.** The IAU adopted $k = 0.2725076$ in 1982. Espenak's bulletins and EclipseWise use it for penumbral contacts. The Five Millennium Canon and the NASA element pages derived from it use 0.2724880. All of them use $k = 0.272281$ for umbral contacts, because the smaller value reproduces observed totality durations and avoids misclassifying beaded annular eclipses as total [@bes-nasa-radius] [@bes-ew-2024-prime].
- **The solar radius is Auwers' 959.63 arcseconds at 1 au** (696,000 km) in every published prediction, although eclipse observations give about 959.95 arcseconds and the IAU 2015 nominal value is 959.22 arcseconds by arctangent, 959.23 by arcsine [@bes-quaglia-2021].
- **NASA publishes the elements as polynomials in $t = t_1 - t_0$** in decimal hours of TDT, third order for $x, y$, second order for $d, l_1, l_2, \mu$, fitted by least squares to five rigorous evaluations over six hours and valid for $t_0 \pm 3$ hours [@bes-nasa-2024-elements] [@bes-nasa-1998-elements].
- **Time scale is TT (TDT) throughout.** ΔT enters only when $\mu$, a Greenwich hour angle, is turned into a geographic longitude. Changing ΔT by one second shifts every longitude by 15.041 arcseconds of rotation [@bes-es1961] [@bes-lasteclipse] [@bes-aravpanwar].
:::

**The question.** What exactly are the Besselian elements of a solar eclipse, what geometry and sign conventions define them, what constants and time scales do the almanacs and NASA build into them, and in what form are they published? This note answers those questions from the almanac chapters and NASA's own pages so that a developer can read a published table of elements and know what every number means. The companion note [From ephemeris to elements](ephemeris-to-elements.md) gives the equations for producing such a table from a JPL ephemeris.

## Origin and lineage of the method

Bessel introduced the method in *Astronomische Nachrichten* No. 50 (1824) for stellar occultations, generalised it to solar eclipses and planetary occultations in No. 145 (1829, "Ueber die Vorausberechnung der Sternbedeckungen"), and collected the theory as the four-part "Analyse der Finsternisse" in volume 2 of his *Astronomische Untersuchungen* (1842) [@bes-bessel-history]. Chauvenet's *Manual of Spherical and Practical Astronomy* (1863) recast the method into the form the almanacs still use [@bes-chauvenet-1863]. Buchanan, who computed the eclipses for the American Ephemeris for 23 years, wrote in 1904 that Chauvenet's chapter "is taken as the standard authority for the methods of computation by both the English and the American Nautical Almanacs", and that Chauvenet's formulas "are not given in the order they are to be used" [@bes-buchanan-1904]. The Explanatory Supplement of 1961 (section 9B) and of 1992 (chapter 8, sections 8.31 to 8.36) give the same formulas in almanac notation, and the 2013 third edition describes its chapter 11 as "an update of the material contained in the 1992 Explanatory Supplement" [@bes-es1961] [@bes-es1992] [@bes-usno-expsupp].

The key idea, in Espenak's words, is "the expression of the ephemerides of the Sun and Moon in terms of the Moon's shadow with respect to Earth's center", which reduces the three-body geometry to the motion of two concentric circles across a plane [@bes-ew-beselm].

## The fundamental plane and the point Z

![The umbral cone narrows to a vertex, and an eclipse is total wherever that vertex falls beyond the Earth's surface rather than short of it. Both shadow radii, $l_1$ and $l_2$, are measured on the fundamental plane rather than on the ground, which is what makes them independent of the observer.](img/fundamental-plane.svg)

The 1961 Supplement defines the geometry in one paragraph, quoted here because every later source paraphrases it. "The exterior tangents to the surfaces of the Sun and the Moon form the umbral cone, the interior tangents the penumbral cone. The common axis of the two cones is the axis of the shadow. The geocentric plane perpendicular to the axis of the shadow is called the [?fundamental-plane|fundamental plane], and is taken as the xy-plane of a system of geocentric rectangular coordinates. The x-axis is the intersection of the fundamental plane with the plane of the equator and is directed positively towards the east; the y-axis is directed positively towards the north. The z-axis is parallel to the axis of the shadow and is positive towards the Moon" [@bes-es1961].

The direction of the axis is fixed by the [?point-z|point Z] on the celestial sphere, with right ascension $a$ and declination $d$. Chauvenet defines Z as the point "in which the sun would be projected upon the sphere by an observer at the centre of the moon" [@bes-chauvenet-1863]. In vector terms, with $\mathbf{R}_s$ and $\mathbf{R}_m$ the geocentric equatorial position vectors of the Sun and Moon, $\mathbf{G} = \mathbf{R}_s - \mathbf{R}_m$ is collinear with the shadow axis and

$$
G \cos d \cos a = R\cos\delta_\odot\cos\alpha_\odot - r_\mathrm{m}\cos\delta_\mathrm{m}\cos\alpha_\mathrm{m},\quad
G \cos d \sin a = R\cos\delta_\odot\sin\alpha_\odot - r_\mathrm{m}\cos\delta_\mathrm{m}\sin\alpha_\mathrm{m},\quad
G \sin d = R\sin\delta_\odot - r_\mathrm{m}\sin\delta_\mathrm{m}
$$

where $R$ is the Sun's radius vector and $r_\mathrm{m}$ the Moon's geocentric distance in the same unit [@bes-es1961] [@bes-es1992]. The 1992 Supplement writes the same thing as $\mathbf{g} = \mathbf{r}_s - \mathbf{r}_m = g\,(\cos d\cos a, \cos d\sin a, \sin d)^T$, equation 8.322-2, and gives the unit vectors of the fundamental system as $\mathbf{i} = (-\sin a, \cos a, 0)$, $\mathbf{j} = (-\cos a\sin d, -\sin a\sin d, \cos d)$ and $\mathbf{k} = (\cos d\cos a, \cos d\sin a, \sin d)$, equations 8.322-4 and 8.322-5 [@bes-es1992]. Chauvenet's x axis is "positive towards that point whose right ascension is $90^{\circ} + a$". That is the same east-pointing axis [@bes-chauvenet-1863].

Espenak's summary of the same convention: "north is positive Y, east is positive X, and the Z axis is perpendicular to this plane and parallel to the shadow axis", and "the outline of the shadow on it is always a circle with no perspective distortion" [@bes-ew-beselm].

## The eight elements

Espenak lists "eight parameters" that "characterize a solar eclipse" and that "may be tabulated at hourly intervals or expressed as third order polynomials over the several hour period of the eclipse" [@bes-nasa-beselm] [@bes-ew-beselm]. The 1992 Supplement is slightly broader: "the quantities $x, y, \sin d, \cos d, \mu, l_1, l_2, \tan f_1, \tan f_2, \mu', d'$ are conventionally designated as Besselian elements ... the first seven quantities are tabulated as a function of time at a short interval, or may also be given as a low-order polynomial as a function of time. The remaining four quantities, to the precision required, are constant for the entire eclipse and are given at the conjunction value" [@bes-es1992].

| Element | Meaning | Unit in NASA tables |
|---|---|---|
| $x, y$ | coordinates of the intersection of the shadow axis with the fundamental plane | Earth equatorial radii |
| $d$ | declination of the point Z, the shadow axis direction | degrees |
| $\mu$ | hour angle of the point Z, measured from the Greenwich or ephemeris meridian | degrees |
| $l_1$ | radius of the penumbra on the fundamental plane | Earth equatorial radii |
| $l_2$ | radius of the umbra (or antumbra) on the fundamental plane | Earth equatorial radii |
| $\tan f_1$ | tangent of the penumbral cone half-angle | dimensionless |
| $\tan f_2$ | tangent of the umbral cone half-angle | dimensionless |

![Looking down the axis, the elements are two concentric circles crossing a disc of unit radius: $x$ and $y$ carry the shadow centre across the plane, $l_1$ and $l_2$ are the radii of the two circles there, and $\gamma$ is the least distance $\sqrt{x^2+y^2}$ reaches. The umbral circle is the small one, and its radius is about one fiftieth of the penumbral radius at true scale.](img/besselian-xy.svg){.fig3d scene="fundamental-plane"}

The units are stated on the NASA explanation page: $x, y$ and $L_1, L_2$ are "in units of the equatorial radius of Earth" [@bes-nasa-beselm]. The 1961 Supplement adds that the derivatives $\mu'$ and $d'$ "are expressed in their natural units of radians per hour" and that $x', y', l_2'$ "may be obtained with sufficient precision by multiplying by six the first differences of the tabular values at intervals of 10 minutes" [@bes-es1961].

### $x$, $y$, $z$ of the Moon

With $a, d$ known, the Moon's coordinates in the fundamental system, "in units of the equatorial radius of the Earth", are

$$
x = r_\mathrm{m}\cos\delta_\mathrm{m}\sin(\alpha_\mathrm{m} - a),\qquad
y = r_\mathrm{m}\left[\sin\delta_\mathrm{m}\cos d - \cos\delta_\mathrm{m}\sin d\cos(\alpha_\mathrm{m} - a)\right],
$$
$$
z = r_\mathrm{m}\left[\sin\delta_\mathrm{m}\sin d + \cos\delta_\mathrm{m}\cos d\cos(\alpha_\mathrm{m} - a)\right],\qquad r_\mathrm{m} = 1/\sin\pi_\mathrm{m}
$$

where $\pi_\mathrm{m}$ is the Moon's equatorial [?horizontal-parallax|horizontal parallax] [@bes-es1961]. "The coordinates $x, y$ are also those of the intersection of the axis of shadow with the fundamental plane" [@bes-es1961]. These are Chauvenet's equations (482) unchanged [@bes-chauvenet-1863]. The 1992 Supplement writes them as a rotation, equation 8.322-3, $\mathbf{r}_\mathrm{Fund} = \frac{1}{\sin\pi_\mathrm{m}}\,\mathbf{R}_1(90^{\circ} - d)\,\mathbf{R}_3(a + 90^{\circ})\,\mathbf{r}_\mathrm{Geoc}$, "in units of earth radii" [@bes-es1992]. The Sun's $x, y$ in this system are the same as the Moon's and its $z$ is $z + G$, but "the method of investigation which we are here following does not require their use" [@bes-chauvenet-1863].

### $\mu$: hour angle instead of right ascension

"In the tabulation of Besselian elements of eclipses, the right ascension $a$ of the point Z is conventionally replaced for practical use by the [?ephemeris-hour-angle|ephemeris hour angle] $\mu$ of that point, given by $\mu$ = ephemeris sidereal time $- a$" [@bes-es1961]. The 1992 edition drops the ephemeris meridian: "$\mu$ = Greenwich apparent sidereal time $- a$. In practical calculation, the Greenwich sidereal time is evaluated according to the precepts given in Chapter 2" [@bes-es1992]. Which meridian is used decides where ΔT enters, and that is treated below.

### The cone angles $f_1$, $f_2$

With subscript 1 for the penumbra and 2 for the umbra, and $g = G/R$ so that $gR$ is the Sun-Moon distance in astronomical units,

$$
\sin f_1 = \frac{\sin s_0 + k\sin\pi_0}{gR},\qquad
\sin f_2 = \frac{\sin s_0 - k\sin\pi_0}{gR}
$$

where $s_0$ is "the adopted value of the semi-diameter (15' 59".63)" of the Sun at unit distance and $\pi_0$ its horizontal parallax at unit distance, 8".80 in 1961 and 8".794 "for 1968 onwards" [@bes-es1961]. The 1992 edition derives the same expression as equation 8.323-5 from $\sin f_1 = (d_s + d_m)/(gR)$ and $\sin f_2 = (d_s - d_m)/(gR)$, with $d_s = \sin s_0/\sin\pi_0$ the solar radius and $d_m = k$ the lunar radius, both in Earth equatorial radii [@bes-es1992]. In the 1961 Supplement the numerators are tabulated constants: for $k = 0.272281$ (1968 onwards) the numerator of $\sin f_1$ is 0.0046640009 and of $\sin f_2$ is 0.0046407920 [@bes-es1961]. The same structure appears in Chauvenet as $\sin f = (s + k\,\pi)/(r'g)$ with $\log k = 9.435000$, so his $k = 0.27227$ [@bes-chauvenet-1863].

### The vertices $c_1$, $c_2$ and the radii $l_1$, $l_2$

"The distances $c_1, c_2$ of the vertices of the penumbral and umbral cones above the fundamental plane are thus, in units of the equatorial radius of the Earth:"

$$
c_1 = z + k\,\mathrm{cosec} f_1,\qquad c_2 = z - k\,\mathrm{cosec} f_2
$$

and "the radii $l_1, l_2$ of the penumbra and umbra on the fundamental plane are obtained from"

$$
l_1 = c_1\tan f_1,\qquad l_2 = c_2\tan f_2 .
$$

"The convention of signs introduced in the formulae for $c$ makes $l_2$ negative for total eclipses, positive for annular eclipses, while $l_1$ is always positive" [@bes-es1961]. The 1992 edition adds the geometric reading: negative $l_2$ means "the vertex is below the fundamental plane" [@bes-es1992]. The penumbral vertex lies between Sun and Moon, so $c_1 > z$ always. The umbral vertex lies beyond the Moon toward Earth, so $c_2 < z$, and $l_2$ changes sign exactly when the vertex crosses the fundamental plane. That crossing is the boundary between a total and an annular eclipse at the geocentre.

At the Earth's surface the radii shrink or grow with the observer's height $\zeta$ above the plane: $L_1 = l_1 - \zeta\tan f_1$ and $L_2 = l_2 - \zeta\tan f_2$ [@bes-lasteclipse]. That step belongs to local circumstances and is only mentioned here because it is why $\tan f_1$ and $\tan f_2$ must be published with the other elements.

### What is held constant

"Although the values of $\tan f_1$ and $\tan f_2$ must be calculated for each hour for the accurate evaluation of $l_1$ and $l_2$, it is always sufficient to use the constant values of $\tan f_1$ and $\tan f_2$ for the integral hour nearest conjunction in the calculation of local circumstances and eclipse curves" [@bes-es1961]. NASA follows this: each table gives one $\tan f_1$ and one $\tan f_2$ [@bes-nasa-2024-elements].

## The constants

### Earth: the unit of length and the flattening

The unit of $x, y, z, l_1, l_2, c_1, c_2$ and $k$ is the Earth's equatorial radius [@bes-es1961] [@bes-es1992]. The 1992 Supplement's reference ellipsoid is $a = 6378.137$ km and $f = 1/298.257$ (its equation 3.244-1) [@bes-es1992]. The flattening does not enter the elements themselves. It enters when an observer's geodetic latitude $\phi$ is converted to $\rho\sin\phi' = S\sin\phi$ and $\rho\cos\phi' = C\cos\phi$ with $C = (1 - e^2\sin^2\phi)^{-1/2}$, $S = (1 - e^2)C$ and $e^2 = 1 - b^2/a^2$ (equations 8.333-1 to 8.333-3) [@bes-es1992]. The Swiss Ephemeris instead scales the $z$ coordinates of the Sun and Moon by $1/(1-f)$ with $f = 1/298.25642$ before forming the shadow axis, "Instead of flattening the earth" [@bes-swisseph-swecl] [@bes-swisseph-header]. Third-party guides use WGS 84, whose $e^2$ is about 0.006694 [@bes-lasteclipse]. Which ellipsoid is used matters at the hundred-metre level for path edges and should be recorded with every table.

### The Sun: $s_0 = 959.63$ arcseconds

Every almanac and NASA prediction uses the Auwers (1891) semidiameter of 15' 59".63 = 959.63 arcseconds at 1 au [@bes-es1961] [@bes-quaglia-2021]. Quaglia et al. (2021) state that this value "has remained unchanged for more than a century" and "is used in all published eclipse predictions; for example in The Astronomical Almanac", and that the IAU's 2015 nominal radius corresponds to 959.22 arcseconds by arctangent and 959.23 by arcsine, while their flash-spectrum analysis of the 2017 August 21 eclipse gives $959.95 \pm 0.05$ arcseconds at 1 au [@bes-quaglia-2021]. In linear units 959.63 arcseconds at 1 au is 696,000 km. The USNO eclipse computer quotes that value as "adopted by the International Astronomical Union (Sun 696000 km; Moon 1737.4 km)" [@bes-usno-eclipse-computer]. The Swiss Ephemeris hard-codes a solar diameter of 1,392,000,000 m and carries a commented-out alternative of 1,391,978,489.9 m annotated "consistent with 959.63 arcsec at AU distance (Astr. Alm.)" [@bes-swisseph-swecl]. Greg Miller's generator instead uses the IAU 2015 nominal $6.957\times10^8$ m, which is 0.3 arcseconds smaller [@bes-celestialprogramming-gen]. The 0.3 arcsecond difference between 959.63 and 959.95 arcseconds moves the umbral path edges and changes the duration of totality by about one second per edge. The measurements and their effect are in [solar radius](../06-solar-radius/_index.md).

### The Moon: two values of $k$

$k$ is the ratio of the Moon's radius to the Earth's equatorial radius. Its history, from the NASA reference page and the identical EclipseWise page [@bes-nasa-radius] [@bes-ew-radius]:

- From 1968 through 1980 the Nautical Almanac Office used two values: $k = 0.2724880$, "a mean over topographic features", for all penumbral (exterior) contacts and for annular eclipses, and $k = 0.272281$, "a mean minimum radius", for the umbral (interior) contacts of total eclipses. The 1961 Supplement's footnotes record the changeover: $k = 0.272274$ for 1961, $k = 0.2724807$ "for use after 1962", and "for 1968 onwards: $k = 0.272281$, $k = 0.2724880$" [@bes-es1961].
- "In August 1982, the International Astronomical Union (IAU) General Assembly adopted a value of $k = 0.2725076$ for the mean lunar radius", meant as the best mean radius averaging mountain peaks and valleys along the limb. Using one value for everything removed a discontinuity in hybrid eclipses but "tends to misclassify certain eclipse types": the 1986 October 3 eclipse was labelled total when it was a beaded annular eclipse.
- Espenak's compromise is $k = 0.272281$ for all umbral and antumbral contacts, because the smaller value "predicts central durations which are closer to the actual durations at total eclipses" and gives shorter totalities, narrower total paths, longer annularities and wider annular paths. For penumbral contacts the NASA bulletins and EclipseWise use the IAU $k = 0.2725076$. The Five Millennium Canon, NASA/TP-2006-214141, and the NASA catalogue, CSV and element pages generated from it use $k = 0.2724880$, the older Nautical Almanac Office value [@bes-nasa-tp2007] [@bes-nasa-radius] [@bes-nasa-2024-elements].

The published tables therefore do not all agree on the penumbral value. The NASA element pages generated from the Five Millennium Canon print "k1 (Penumbra) = 0.272488, k2 (Umbra) = 0.272281" for 2024 April 8 [@bes-nasa-2024-elements] [@bes-nasa-2024-sedata], whereas the EclipseWise DE405 page for the same eclipse prints $k = 0.2725076$ (penumbra) and $0.2722810$ (umbra) [@bes-ew-2024-prime], and the NASA technical publication for 2008 August 1 states the IAU value for penumbral contacts [@bes-nasa-tp2007]. The Canon's own text says which is which, and it is quoted in [Enumerating eclipses](../02-catalogs/enumerating-eclipses.md). The difference between 0.2724880 and 0.2725076 is $2\times10^{-5}$ Earth radii, about 125 m in the penumbral radius, and it does not change $\tan f_1$ at the seven decimals published. The umbral value is the one that matters and it is 0.272281 in all of Espenak's tables.

The Swiss Ephemeris uses a single lunar diameter of 3 476 300 m, so its implied $k$ is $1738.15/6378.14 = 0.27251$ for both cones [@bes-swisseph-swecl]. Miller's generator uses 0.2725076 for both [@bes-celestialprogramming-gen]. A page at solareclipses.com uses 0.272399309, which is the 1737.4 km LOLA datum radius over the WGS 84 equatorial radius, the same $k$ that NASA SVS product 4314 prints [@bes-solareclipses-formulas]. A developer must therefore never assume that two tables of elements share a $k$.

### Centre of mass, not centre of figure

NASA's elements are computed for the Moon's centre of mass: "The lunar coordinates have been calculated with respect to the Moon's Center of Mass. They DO NOT include a correction to the Center of Figure, or the effects of mountains and valleys along the edge of the Moon" [@bes-nasa-2024-elements]. The same choice is stated for the DE200/LE200 bulletins ("no corrections made for center of figure, lunar limb profile or atmospheric refraction") [@bes-nasa-explain] and for the DE405 and VSOP87 series [@bes-ew-de405] [@bes-ew-ve82]. Limb corrections are applied later, in local circumstances, and belong to [limb profile methods](../05-lunar-limb/limb-profile-methods.md).

## Time scale and ΔT

The elements are functions of a uniform time. In 1961 that was Ephemeris Time (E.T.), and the basic inputs were "the apparent right ascension $\alpha_\odot$, declination $\delta_\odot$, and radius vector $R$ of the Sun, and the right ascension $\alpha_\mathrm{m}$, declination $\delta_\mathrm{m}$, and horizontal parallax of the Moon, for every hour of E.T. during the eclipse; and the ephemeris sidereal time" [@bes-es1961]. NASA's tables say "Note that all times are expressed in Terrestrial Dynamical Time (TDT)" [@bes-nasa-2024-elements], and EclipseWise gives "UT1 = TD $-$ ΔT" [@bes-ew-2024-prime]. [?tt|TT] is printed as TDT or TD in NASA tables and was called ET before 1984. All are the same scale, $TT = TAI + 32.184$ s, and [?delta-t|ΔT] $= TT - UT1$ [@bes-usno-glossary].

Where ΔT enters is the one place the two Supplements differ. The 1961 edition measures $\mu$ from the ephemeris meridian, which lies $1.002738\,\Delta T$ east of Greenwich, so that an observer's "ephemeris longitude" is his geographic longitude shifted by that amount and the Besselian elements themselves are free of ΔT [@bes-es1961]. The 1992 edition measures $\mu$ from Greenwich, using Greenwich apparent sidereal time, and says of the observer's longitude that it "is not now corrected for ΔT" [@bes-es1992]. In the 1992 convention, which NASA follows, the tabulated $\mu$ is a Greenwich hour angle carried against a TT argument, so the ΔT shift is applied downstream rather than built into $\mu_0$. A recent implementation states the consequence: "mu is tabulated against TDT but expresses a Greenwich hour angle, a UT quantity. The frames differ by delta T, so it must be subtracted in the hour angle" [@bes-aravpanwar]. The correction is $\mu_\mathrm{UT} = \mu_\mathrm{TT} - \Delta T \times 0.004178074^{\circ}/\mathrm{s}$, that is 15.041067 degrees per hour of ΔT [@bes-lasteclipse]. For the 2027 August 2 eclipse, omitting the 76.0 s of ΔT from the hour angle altogether shifts every longitude by about 32 km at the latitude of Egypt. The 4.3 s difference between NASA's 71.7 s and the repository's 76.0 s is worth about 1.8 km [@bes-aravpanwar].

The ΔT values printed with NASA's 2024 April 8 elements illustrate the versioning problem: 70.6 s on the element page [@bes-nasa-2024-elements], 74.0 s in the catalogue CSV and on the database page [@bes-nasa-csv] [@bes-nasa-2024-sedata], and 71.5 s on the EclipseWise DE405 page [@bes-ew-2024-prime]. The two NASA pages also carry different coefficients: the SEbeselm page gives $x_0 = -0.318157$, the Canon CSV and SEdata page $-0.318244$, a 550 m difference from the two ephemeris runs [@bes-nasa-2024-elements] [@bes-nasa-csv]. A table of elements is therefore incomplete without its ΔT, its ephemeris and its $k$ values.

## The polynomial form

NASA's tables give, for each of $x, y, d, l_1, l_2, \mu$, coefficients $a_0 \ldots a_3$ of

$$
a = a_0 + a_1 t + a_2 t^2 + a_3 t^3,\qquad t = t_1 - t_0
$$

"(decimal hours)", with $t_0$ an integral hour of TDT near greatest eclipse. "The Besselian elements were derived from a least-squares fit to elements calculated at five uniformly spaced times over a six hour period centered at $t_0$" and "are valid over the period $t_0 - 3 \le t_1 \le t_0 + 3$" [@bes-nasa-2024-elements] [@bes-nasa-1998-elements]. The Five Millennium Canon catalogue CSV has the same structure: columns `t0, x0..x3, y0..y3, d0..d2, mu0..mu2, l10..l12, l20..l22, tan_f1, tan_f2, tmin, tmax`, with `tmin = -3` and `tmax = 3` for every row, and `mu2` is zero in every row inspected, so $\mu$ is effectively linear [@bes-nasa-csv]. For 2024 April 8 the CSV row gives $t_0 = 18$, $x = -0.318244 + 0.5117116\,t + 0.0000326\,t^2 - 0.00000842\,t^3$, $y = 0.219764 + 0.2709589\,t - 0.0000595\,t^2 - 0.00000466\,t^3$, $d = 7.58620 + 0.014844\,t - 0.000002\,t^2$, $\mu = 89.59122 + 15.00408\,t$, $l_1 = 0.535814 + 0.0000618\,t - 0.0000128\,t^2$, $l_2 = -0.010272 + 0.0000615\,t - 0.0000127\,t^2$, $\tan f_1 = 0.0046683$, $\tan f_2 = 0.0046450$ [@bes-nasa-csv]. The negative $l_2$ says total. The coefficient $\mu_1 \approx 15.004$ degrees per hour is the Earth's rotation rate relative to the slowly moving point Z.

Miller's independent generator reproduces this scheme from five samples at $t = -2, -1, 0, 1, 2$ hours, solves the normal equations by Gauss-Jordan elimination, and notes that "x, y typically third-degree; d, l1, l2 typically second-degree; μ first-degree" while $\tan f_1, \tan f_2$ are taken at $T_0$ only [@bes-celestialprogramming-gen]. The 1992 Supplement's practice was different: elements "are calculated from the ephemeris entries and carried as an array; none is assumed to be constant. Derivatives are taken numerically", at a 10-minute interval refined to 30 seconds where needed [@bes-es1992]. The polynomial is a compact publication format, not the computation method.

Meeus's *Elements of Solar Eclipses 1951-2200* (1989) publishes the 570 eclipses of that interval in the same polynomial form, computed from the Bureau des Longitudes theories, with worked examples for local circumstances and path points [@bes-meeus-1989]. The earlier Mucke and Meeus *Canon of Solar Eclipses -2003 to +2526* (1983) gave Besselian elements and maps for 10,774 eclipses computed from Newcomb's solar tables and Brown's lunar theory as modified in the Improved Lunar Ephemeris of 1954 [@bes-5mcse2-preface] [@bes-mucke-meeus-1983]. Those canons were superseded by the Five Millennium Canon, which is "based on modern theories of the Sun and the Moon constructed at the Bureau des Longitudes of Paris" with "ephemerides and eclipse predictions performed in Terrestrial Dynamical Time" [@bes-5mcse2-preface].

## Gamma and the classification of an eclipse

[?gamma|Gamma] is the value of $\sqrt{x^2 + y^2}$, with the sign of $y$, at the instant of greatest eclipse: "the distance of the Moon's shadow axis from Earth's center in units of equatorial Earth radii ... defined at the instant of greatest eclipse when its absolute value is at a minimum" [@bes-nasa-glossary]. It is therefore a derived quantity of the elements, not an element. Meeus's approximation in chapter 52 of the 1991 *Astronomical Algorithms*, chapter 54 in the 1998 edition, is used for enumerating eclipses rather than for circumstances. The thresholds are the subject of [Enumerating eclipses](../02-catalogs/enumerating-eclipses.md), and the series computes $\gamma = (P\cos F_1 + Q\sin F_1)(1 - 0.0048\,W)$ and $u = 0.0059 + 0.0046\,E\cos M - 0.0182\cos M' + 0.0004\cos 2M' - 0.0005\cos(M + M')$. It then classifies: no eclipse if $|\gamma| > 1.5433 + u$, central if $|\gamma| < 0.9972$, total if $u < 0$, annular if $u > 0.0047$, otherwise annular-total [@bes-soniakeys-meeus] [@bes-squarewidget]. Here $u$ is the umbral radius on the fundamental plane, the same quantity as $l_2$, and 0.9972 is the geocentric distance at which the axis grazes the ellipsoid [@bes-gamma-wikipedia]. Meeus's own text was not read. The formulas are quoted from an open-source implementation that cites chapter 54 line by line [@bes-soniakeys-meeus].

## The Swiss Ephemeris variant of the geometry

The Swiss Ephemeris does not tabulate elements. Its `eclipse_where()` in `swecl.c` computes the same geometry in astronomical units at each call, with the umbral and penumbral subscripts reversed relative to the almanac convention and the flattening applied by scaling the $z$ coordinates of the Sun and Moon [@bes-swisseph-swecl]. The code is quoted and mapped onto the almanac symbols in [From ephemeris to elements](ephemeris-to-elements.md).

## Sources compared

| Source | Year | What it gives that the others do not |
|---|---|---|
| Chauvenet, *Manual*, Vol. I, Arts. 288-296 [@bes-chauvenet-1863] | 1863 | The original derivation in Bessel's notation, with the point Z defined as the Sun seen from the Moon's centre and $\log k = 9.435000$. Formulas are scattered, as Buchanan complained. |
| Buchanan, *Mathematical Theory of Eclipses* [@bes-buchanan-1904] | 1904 | Chauvenet's formulas re-ordered into computing sequence by the Nautical Almanac Office's eclipse computer. |
| Explanatory Supplement 1961, section 9B [@bes-es1961] | 1961 | Complete almanac formulation with the tabulated numerators of $\sin f_1, \sin f_2$ for each $k$, the ephemeris-meridian treatment of ΔT, and a worked example (1961 February 15). |
| Explanatory Supplement 1992, chapter 8, by Alan D. Fiala and John A. Bangert [@bes-es1992] | 1992 | Rotation-matrix form (8.322-3), unit vectors of the fundamental system, the flattening auxiliaries $C, S$ (8.333), the Greenwich-based $\mu$, and the note on practical calculation (8.325). |
| Explanatory Supplement 2013, chapter 11 [@bes-usno-expsupp] | 2013 | Described by USNO as an update of the 1992 chapter. Not read for this note. |
| NASA GSFC element pages and CSV [@bes-nasa-2024-elements] [@bes-nasa-csv] | 2006-2024 | The published polynomial form, $t_0$, validity window, $k_1, k_2$, ΔT and ephemeris for every eclipse from -1999 to +3000. |
| NASA mean lunar radius page [@bes-nasa-radius] | 1990s | The documented history of $k$ and the rationale for 0.272281 at umbral contacts. |
| EclipseWise DE405 pages [@bes-ew-2024-prime] [@bes-ew-de405] | 2014-2024 | Espenak's elements recomputed from JPL DE405 with $k = 0.2725076/0.2722810$ and a later ΔT. |
| Swiss Ephemeris `swecl.c` [@bes-swisseph-swecl] | 1997-2024 | A live vector formulation in au with the flattening applied by scaling $z$, and reversed $f_1/f_2$ naming. |
| Miller, celestialprogramming.com [@bes-celestialprogramming-gen] | 2020s | The only page found that shows the least-squares fit explicitly, with five samples and Gauss-Jordan elimination. |
| Quaglia et al., ApJS [@bes-quaglia-2021] | 2021 | A refereed statement of which constants published predictions use (959.63 arcseconds, Auwers 1891) and a method that avoids Besselian elements entirely. |

## What a developer should do

1. Read section 9B of the 1961 Supplement first [@bes-es1961]. It is the shortest complete statement of the formulas, and its worked example for 1961 February 15 08h ET gives numbers to test against. Then read sections 8.32 and 8.33 of the 1992 Supplement for the rotation-matrix form and the flattening auxiliaries [@bes-es1992]. Both are free on archive.org.
2. Treat a table of elements as a record with mandatory metadata: ephemeris, ΔT, $k_1$, $k_2$, $s_0$, ellipsoid, $t_0$, time scale. NASA's CSV [@bes-nasa-csv] carries ΔT and $t_0$ but not $k$ or the ephemeris, which must be taken from the accompanying pages.
3. Use $k_2 = 0.272281$ for umbral contacts. For penumbral contacts use $k_1 = 0.2724880$ to match the Five Millennium Canon, the NASA catalogue, CSV and element pages, and $k_1 = 0.2725076$ to match the NASA bulletins and EclipseWise. Say which. Use $s_0 = 959.63$ arcseconds if the goal is to match published predictions, and keep it a parameter because the measured value is about 959.95 arcseconds [@bes-quaglia-2021].
4. Keep $\mu$ in TT with the ΔT of the table, and apply $\mu_\mathrm{UT} = \mu_\mathrm{TT} - 15.041067^{\circ}\,\Delta T/3600$ only when converting to geographic longitude with a different ΔT [@bes-lasteclipse].
5. Publish $l_2$ with its sign. Do not take an absolute value anywhere before the classification step.

## What this changes

For the pipeline design this fixes the interface between the ephemeris stage and everything downstream: the product of the ephemeris stage is a table of $(x, y, d, \mu, l_1, l_2)$ against TT plus the two constants $\tan f_1, \tan f_2$, and the metadata listed above. Global and local circumstances consume only that table. It also fixes two design decisions: the umbral $k$ must be an input, not a constant, and ΔT must be carried as metadata of the element set rather than applied inside it.

## Open questions

- Chapter 11 of the 2013 Explanatory Supplement: obtain the chapter and check whether it changes the $\mu$ convention, the ellipsoid, or the recommended $k$, and record its authors. The USNO page describes it only as an update of the 1992 material [@bes-usno-expsupp].
- Meeus, *Astronomical Algorithms*, chapter 52 in the 1991 edition and chapter 54 in the 1998 edition, and *Elements of Solar Eclipses 1951-2200*: obtain the books and verify the thresholds 0.9972, 1.5433 and 0.0047 and the stated $k$ and ephemeris against the values quoted here from secondary implementations.
- Bessel's 1829 paper in *Astronomische Nachrichten* No. 145 and the 1842 *Analyse der Finsternisse*: obtain scans to confirm the original sign conventions. ADS holds Astronomische Nachrichten.
- Jubier's 2024 page and its statement of ephemeris and $k$: the live page refused connection and the Wayback snapshot of 2025-12-30 is a JavaScript stub. Obtain the page source directly.
