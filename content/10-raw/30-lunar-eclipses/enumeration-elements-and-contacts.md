---
title: Enumeration, elements and contacts
seo_title: Lunar Eclipse Calculation: Elements and Contact Times
description: How lunar eclipses are found and classified, and how gamma, magnitudes, contact times, durations and visibility maps are computed.
order: 1
status: working
updated: 2026-10-17
tags: [lunar-eclipse, gamma, saros, meeus, besselian-elements, contacts, visibility, delta-t]
---

::: summary
- **A [lunar eclipse](_index.md) is one instant for the whole Earth.** The contacts are geocentric, so a prediction is a list of times plus a map of where the Moon is above the horizon at each contact. There is no path and no local contact time [@lun-es1961] [@lun-es1992].
- **The elements are two coordinates and three radii.** The Explanatory Supplement takes the antisolar point as the axis and computes the Moon's offsets $x$ and $y$ from it in arcseconds. Each contact solves $(x + x't)^2 + (y + y't)^2 = L^2$ for $L_1$, $L_2$ or $L_3$ [@lun-es1961] [@lun-es1992].
- **Lunar gamma is the Moon's least distance from the shadow axis**, in Earth equatorial radii, positive when the Moon passes north. It is not the solar-eclipse gamma, which measures the Moon's shadow axis from the Earth's centre [@lun-5mcle-tp2009] [@lun-nasa-lecatkey].
- **[Meeus](https://en.wikipedia.org/wiki/Jean_Meeus)'s closed form needs only the full-moon index.** The solar method of chapter 54 changes two coefficients, then $\rho = 1.2848 + u$, $\sigma = 0.7403 - u$, the magnitudes and the semidurations $\tfrac{60}{n}\sqrt{L^2-\gamma^2}$ minutes follow [@cat-meeus-1991-aa] [@cat-soniakeys-meeus-go].
- **The NASA Five Millennium Canon of Lunar Eclipses (NASA/TP-2009-214172) lists 12,064 eclipses from −1999 to +3000**: 4,378 penumbral, 4,207 partial and 3,479 total, computed with VSOP87, ELP-2000/82, $k = 0.2724880$ and [Danjon](https://en.wikipedia.org/wiki/Andr%C3%A9_Danjon)'s enlargement [@lun-5mcle-tp2009].
- **ΔT moves only the map.** Greatest eclipse and the contacts are computed in TT. Subtracting ΔT gives UT1 and shifts every visibility curve by 1 degree of longitude per 240 seconds of ΔT [@lun-5mcle-tp2009].
:::

**The question.** How are lunar eclipses found in a period and classified, how are gamma, the magnitudes, the six contacts and the durations computed, and how do the visibility maps and the time scales enter the product?

## What a lunar eclipse prediction contains

The 1961 Explanatory Supplement states the simplification that sets lunar eclipses apart: "the times and circumstances are the same for all parts of the Earth from which the Moon is visible" [@lun-es1961]. The 1992 edition adds that "since the observer is on the body that is casting the shadow, the circumstances are the same for all parts of the Earth from which the Moon is visible", and that of the solar coordinates "only (x,y) in the fundamental plane are used" [@lun-es1992]. A product therefore has three parts: the instants of the contacts and of greatest eclipse, the magnitudes and durations, and a map of visibility.

There are three types. A [?lun-penumbral-eclipse|penumbral eclipse], also called an appulse, is one in which the Moon enters only the Earth's penumbra. The Canon states that penumbral eclipses "cannot be detected visually" unless the penumbral magnitude "is greater than ~0.6" [@lun-5mcle-tp2009]. In a partial eclipse it enters the umbra without being wholly immersed. In a total eclipse it is entirely inside the umbra [@lun-es1961]. A penumbral eclipse in which the whole Moon is inside the penumbra is a [?lun-total-penumbral|total penumbral eclipse] [@lun-5mcle-tp2009]. A central total eclipse is one in which "some portion of the Moon passes directly through the center of Earth's umbral shadow". The NASA canon marks it "+" or "−" as the Moon's centre passes north or south of the axis [@lun-5mcle-tp2009] [@lun-nasa-le2001].

The contacts carry their own names. In the NASA convention P1 and P4 are the first and last exterior tangencies with the penumbra. U1 and U4 are the first and last exterior tangencies with the umbra, and U2 and U3 the first and last interior tangencies with it [@lun-5mcle-tp2009]. These are the [?lun-contacts|lunar contacts]. They replace the C1 to C4 of a solar eclipse. NASA notes that P1 and P4 are not observable [@lun-5mcle-tp2009].

![The six contacts are the instants when the Moon's track meets the circles at distances $\rho + k$, $\sigma + k$ and $\sigma - k$ from the shadow axis, and gamma is the perpendicular from the axis to the track [@lun-es1992] [@cat-meeus-1991-aa]. Schematic, to scale for Meeus's Danjon radii at $u = 0$.](img/lunar-contacts.svg)

## Classification and the catalogue codes

The Canon's distribution over 5,000 years is 12,064 eclipses: 4,378 penumbral (36.3 per cent), 4,207 partial (34.9 per cent) and 3,479 total (28.8 per cent) [@lun-5mcle-tp2009]. Of the penumbral eclipses, 141 or 3.2 per cent are total penumbral [@lun-5mcle-tp2009]. The 21st century has 228 lunar eclipses: 86 penumbral, 57 partial and 85 total [@lun-nasa-le2001].

Total penumbral eclipses are rare for a geometric reason. The Moon's apparent diameter ranges from 1763.0 arcseconds at apogee to 2011.8 arcseconds at perigee. The penumbral annulus between the edges of the penumbra and umbra ranges from 1887.7 arcseconds at aphelion to 1951.9 arcseconds at perihelion. "The Moon cannot fit entirely within the penumbral annulus when it is near perigee" [@lun-5mcle-tp2009].

The catalogue type field has a second character. "m" marks the middle eclipse of a Saros series, "+" and "−" central total eclipses, "*" a total penumbral eclipse, and "b" and "e" the first and last penumbral eclipse of a series [@lun-nasa-lecatkey]. The ASCII catalogue file prints a total penumbral eclipse as `Nx`, for example 2006 March 14 and 1988 March 3 [@lun-5mkle-ascii]. The Quincena Solar Eclipse field, QSE, gives the type of the [?lun-quincena|solar eclipse a fortnight] before or after the lunar eclipse [@lun-nasa-lecatkey].

## Gamma and greatest eclipse

NASA defines lunar gamma as "the minimum distance from the center of the Moon to the axis of Earth's umbral shadow cone, in units of Earth's equatorial radius", positive or negative "depending on whether the Moon passes north or south of the shadow cone axis" [@lun-5mcle-tp2009]. Meeus uses the same definition [@cat-meeus-1991-aa]. This is the [?lun-gamma|lunar gamma]. It shares a name with the solar [?gamma|gamma] but measures a different distance in a different plane.

[?greatest-eclipse|Greatest eclipse] is "the instant when the center of the Moon passes closest to the axis of Earth's umbral shadow" [@lun-nasa-lecatkey]. The Canon notes that "because of Earth's flattening, the instant of greatest eclipse differs slightly from the instant of greatest magnitude", a difference that cannot be distinguished observationally [@lun-5mcle-tp2009]. Greatest eclipse coincides neither with opposition in longitude, which is the full moon, nor with opposition in right ascension, unless the eclipse is perfectly central [@lun-5mcle-tp2009].

Gamma changes steadily along a Saros series. "For odd numbered series (descending node), gamma increases, while for even numbered series (ascending node), gamma decreases" [@lun-5mcle-tp2009]. The step is larger near aphelion. Saros 129, with eclipses in June and July, steps by 0.0802 to 0.0882 per Saros between 1928 and 2054. Saros 134, in December and January, steps by only −0.0036 to −0.0093 [@lun-5mcle-tp2009]. When the Earth's orbital eccentricity was larger, gamma sometimes reversed for a few eclipses. Saros 13 is the extreme case, and the most recent reversal was on 1648 January 10 in Saros 138 [@lun-5mcle-tp2009].

[Stellarium](https://stellarium.org/) computes gamma from the angular separation $m$ at greatest eclipse in arcseconds as `gamma = m*0.2725076/mSD`, with `mSD` the Moon's semidiameter in arcseconds, and gives it the sign of $y$ [@sw-stellarium-astrocalc]. This converts an angle at the Moon into Earth radii through the [?k-lunar-radius|lunar radius ratio] $k$.

## Saros, Inex and the other series

Lunar eclipses use the same series as solar eclipses. The [?saros|Saros] is 223 synodic months, 6585.3223 days, which is within hours of 239 anomalistic months, 6585.5375 days, and 242 draconic months, 6585.3575 days [@lun-5mcle-tp2009]. Lunar Saros numbering follows van den Bergh's 1955 scheme. "The eclipses with an odd Saros number take place at the descending node of the Moon's orbit, while those with an even Saros number take place at the ascending node" [@lun-5mcle-tp2009]. The Canon spans 204 series [@lun-5mcle-tp2009].

Successive Saros members shift about 120 degrees west in visibility, because the Saros exceeds a whole number of days by about a third. Three Saros, the [?exeligmos|Exeligmos], return an eclipse to roughly the same region [@lun-5mcle-tp2009]. The [?inex|Inex] is 358 synodic months, 10,571.9509 days, close to 388.5 draconic months, so successive Inex members occur at opposite nodes. The node shift after one Inex is about +0.04 degrees, against about −0.48 degrees for the Saros [@lun-5mcle-tp2009].

The interval between two successive lunar eclipses is 1, 5 or 6 lunations. Over the Canon these occur 1,527, 2,909 and 7,627 times [@lun-5mcle-tp2009]. The Canon's Table 5-9 gives the Saros number of the next eclipse from the interval: $s + 38$ after one month, $s - 33$ after five and $s + 5$ after six [@lun-5mcle-tp2009]. Stellarium computes the Saros number from the Brown lunation number with a closed form "adapted from Saros calculations for solar eclipses in Sky & Telescope (October 1985)" [@sw-stellarium-astrocalc]. For the solar side of the numbering and the Saros-Inex panorama, see [Enumerating eclipses](../20-solar-eclipses-and-transits/02-catalogs/enumerating-eclipses.md).

## Eclipse limits at opposition

A lunar eclipse is possible only near a node. The Canon puts the zone at "within about 17° of a node", which the Sun and the antisolar shadow take 34.5 days to cross, so each [?eclipse-season|eclipse season] contains at least one full moon [@lun-5mcle-tp2009].

The 1961 Supplement gives the occurrence tests on the Moon's latitude $\beta$ at opposition. Here $\beta \cos I'$ is the least true angular distance of the centres. A penumbral eclipse needs $\beta\cos I' < 1.02(\pi_1 + s_\odot + \pi_\odot) + s_m$ [@lun-es1961]. An umbral eclipse needs $\beta\cos I' < 1.02(\pi_1 - s_\odot + \pi_\odot) + s_m$ [@lun-es1961]. With numbers substituted it tabulates [@lun-es1961]:

- $|\beta| > 1^{\circ}36'38''$: no penumbral eclipse;
- $1^{\circ}26'19'' < |\beta| < 1^{\circ}36'38''$: penumbral eclipse possible;
- $1^{\circ}03'46'' < |\beta| < 1^{\circ}26'19''$: penumbral eclipse certain, no umbral eclipse;
- $0^{\circ}53'26'' < |\beta| < 1^{\circ}03'46''$: penumbral eclipse certain, umbral eclipse possible;
- $|\beta| < 0^{\circ}53'26''$: umbral eclipse certain.

[Chauvenet](https://en.wikipedia.org/wiki/William_Chauvenet)'s 1863 limit for an umbral eclipse is 63 arcminutes 53 arcseconds [@bes-chauvenet-1863]. Astronomy Engine prunes any full moon whose ecliptic latitude exceeds 1.8 degrees before searching for the shadow [@sw-astronomy-engine-c].

## Meeus's closed form

Meeus treats lunar eclipses in the same chapter as solar eclipses. That is chapter 52 in the 1991 edition and chapter 54 in the 1998 edition [@cat-meeus-1991-aa]. The mean phase, the arguments $F$, $M$, $M'$, $\Omega$ and $E$, the test $|\sin F| > 0.36$ and the sixteen-term correction to the time of maximum are those of the solar method, set out in [Enumerating eclipses](../20-solar-eclipses-and-transits/02-catalogs/enumerating-eclipses.md#meeuss-approximate-method). Meeus counts lunations with an index he calls $k$. That $k$ is not the lunar radius ratio, so this topic calls it the lunation index. For a full moon the lunation index is an integer plus 0.5, and the first two coefficients of the time correction change from −0.4075 and +0.1721 to −0.4065 and +0.1727 [@cat-meeus-1991-aa] [@cat-soniakeys-meeus-go]. Gamma and $u$ come from the same expressions, through the auxiliaries that Meeus calls P, Q and W. These letters are Meeus's intermediate sums, not the position angle $P$ or the shadow-edge angle $Q$ of the corpus.

For a lunar eclipse Meeus gives, "again in equatorial Earth radii", the radii at the distance of the Moon [@cat-meeus-1991-aa]:

$$\rho = 1.2848 + u \ \ \text{(penumbra)}, \qquad \sigma = 0.7403 - u \ \ \text{(umbra)}.$$

The magnitudes are [@cat-meeus-1991-aa]

$$\text{penumbral} = \frac{1.5573 + u - |\gamma|}{0.5450}, \qquad \text{umbral} = \frac{1.0128 - u - |\gamma|}{0.5450},$$

and "if the magnitude is negative, this indicates that there is no eclipse". The denominator 0.5450 is the Moon's diameter in Earth radii, $2k$. Meeus names three limiting distances P, T and H. This topic writes them $L_\mathrm{par} = 1.0128 - u$ for the partial phase, $L_\mathrm{tot} = 0.4678 - u$ for totality and $L_\mathrm{pen} = 1.5573 + u$ for the penumbral phase, because $P$ is the position angle in the corpus. With $n = 0.5458 + 0.0400\cos M'$, the semiduration of each phase in minutes is $\tfrac{60}{n}\sqrt{L^2 - \gamma^2}$ with the matching $L$ [@cat-meeus-1991-aa]. The Go port computes the same quantities in hours as `math.Sqrt(t*t-γ2) / n` [@cat-soniakeys-meeus-go]. In Meeus's notation $n$ is the Moon's speed relative to the shadow in Earth radii per hour. In the corpus $n$ is also the speed on the [fundamental plane](../10-shared/01-foundations/besselian-elements.md) in the solar method, so the meaning carries over.

These constants include Danjon's enlargement. Meeus states that "instead of the traditional rule consisting of increasing by 1/50 the theoretical radii, we have preferred the method used since 1951 by the Connaissance des Temps", and he gives the constants for the traditional rule [@cat-meeus-1991-aa]. The comparison of the rules is in [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md).

Meeus's worked example is the eclipse after 1997 July 1. With lunation index −28.5 it finds the maximum at 1997 September 16, 18h 48.2m TD, or 18h 47m UT for ΔT = +63 seconds. It gives $\gamma = -0.3791$, $u = -0.0131$ and umbral magnitude 1.187. The semidurations are 98 minutes for the partial phase, 30 minutes for totality and 153 minutes for the penumbral phase. The contacts follow as P1 16h 14m, U1 17h 09m, U2 18h 17m, U3 19h 17m, U4 20h 25m and P4 21h 20m UT [@cat-meeus-1991-aa]. On accuracy, Meeus writes that "for lunar eclipses the results will generally be precise enough for historical research, or when high accuracy is not needed". He gives the counter-example of 1890 November 26, for which the method returns umbral magnitude −0.007 although "it was a very small partial eclipse in the umbra" [@cat-meeus-1991-aa]. A check of the method against the NASA catalogue is in [Observation, brightness and validation](observation-brightness-and-validation.md).

## Besselian elements for a lunar eclipse

The Explanatory Supplement uses a [?fundamental-plane|fundamental plane] through the Moon perpendicular to the shadow axis. The axis points to the antisolar point, $a = \alpha_\odot + 12^{h}$ and $d = -\delta_\odot$ [@lun-es1961]. The Moon's coordinates in this frame are [@lun-es1961]

$$x = \cos\delta_m \sin(\alpha_m - a), \qquad y = \cos d\,\sin\delta_m - \sin d\,\cos\delta_m\cos(\alpha_m - a),$$

"usually expressed in seconds of arc". The 1992 edition writes the same rotation in vector form and states that only $(x, y)$ are used [@lun-es1992]. Stellarium's `LunarEclipseBessel::computeElements` evaluates these two lines from geocentric apparent positions, citing the 1961 Supplement [@sw-stellarium-astrocalc].

The separation of the centres is $m = (x^2 + y^2)^{1/2}$. At the contacts it takes the values [@lun-es1961] [@lun-es1992]

$$L_1 = R_p + s_m, \qquad L_2 = R_u + s_m, \qquad L_3 = R_u - s_m,$$

for the beginning and end of the penumbral, partial and total phases. Here $R_p$ and $R_u$ are the enlarged shadow radii and $s_m$ is the Moon's geocentric semidiameter. The Moon's semidiameter follows from its horizontal parallax and the lunar radius ratio $k$ as $\sin s_m = k\,\sin\pi_m$, so that $s_m \approx k\,\pi_m$. The 1961 Supplement adopts "sin s = 0.2724880 sin π" for 1968 onwards and gives the working form "s″ = 0.0799 + 0.272453 π″" [@lun-es1961]. The products choose different $k$. Meeus's magnitude denominator 0.5450 is $2k$ with $k = 0.2725$ [@cat-meeus-1991-aa]. The NASA Canon uses $k = 0.2724880$ [@lun-5mcle-tp2009]. Stellarium forms the semidiameter from the Moon's equatorial radius and distance as `atan(moon->getEquatorialRadius()/dist)`, and uses 0.2725076 only to convert gamma to Earth radii [@sw-stellarium-astrocalc]. In the corpus $L_1'$ and $L_2'$ are the solar shadow radii on an observer's plane, so these lunar $L_i$ are limiting separations, not radii. The 1992 Supplement lists the elements as $x$, $y$, $\dot x$, $\dot y$, $m$, $L_1$, $L_2$, $L_3$ and the two radii. It adds that "there is no widely accepted convention, however, and the elements are not published in The Astronomical Almanac" [@lun-es1992].

### Contacts

With $x_0$, $y_0$ at a time $T$ near opposition and hourly rates $x'$, $y'$, a contact at $T + t$ satisfies [@lun-es1961]

$$(x_0 + x't)^2 + (y_0 + y't)^2 = L^2 .$$

The 1961 Supplement solves it by setting $n^2 = x'^2 + y'^2$ and $\Delta = \pm(x_0 y' - y_0 x')/n$, with the sign chosen so that $\Delta > 0$. Then

$$t = -\frac{x_0x' + y_0y'}{n^2} \mp \frac{\sqrt{L^2 - \Delta^2}}{n},$$

"the upper sign being used for first contact and the lower sign for last contact". The calculation may be repeated from the times found [@lun-es1961]. Stellarium implements the same algorithm with `delta = (x*ydot-y*xdot)/sqrt(n2)` and `semiDuration = sqrt((L*L-delta*delta)/n2)` [@sw-stellarium-astrocalc]. The type follows from the same quantities: no eclipse if $L_1^2 - \Delta^2 < 0$, penumbral if $L_2^2 - \Delta^2 < 0$, partial if $L_3^2 - \Delta^2 < 0$, and total otherwise [@lun-es1961].

The 1992 Supplement gives a second method. It tabulates the discriminants $L_1 - m$, $L_2 - m$ and $L_3 - m$ at a fixed step, usually 10 minutes. It finds each sign change by inverse interpolation and checks that the events occur in the order of its Table 8.422.1 [@lun-es1992]. "No approximations or manipulations are necessary" [@lun-es1992]. Before tabulating, it corrects the lunar ephemeris "for the offset of the center of figure from the center of mass" and changes the argument to UT by applying ΔT [@lun-es1992]. The 1961 worked example for 1960 March 13 applies $\Delta\alpha = -0.20''$ for that offset [@lun-es1961].

### Greatest eclipse, magnitude and position angle

Greatest eclipse is the minimum of $m$, where $x\dot x + y\dot y = 0$. The correction to a trial time is $t = -(x_0x' + y_0y')/n^2$ [@lun-es1961] [@lun-es1992]. Stellarium iterates this step from the mean full moon until it changes by less than 0.1 seconds, using rates from positions 5 minutes either side [@sw-stellarium-astrocalc].

The magnitude is [@lun-es1992]

$$\text{magnitude} = \frac{L_i - m}{2 s_m}, \qquad i = 1, 2,$$

with $L_1$ for the penumbral and $L_2$ for the [?lun-umbral-magnitude|umbral magnitude]. The 1992 Supplement states that the magnitude "may be greater than unity, but not negative" [@lun-es1992]. NASA instead prints a negative umbral magnitude for penumbral eclipses, as "a measure of the distance of the Moon's limb to the edge of the umbral shadow in units of the Moon's diameter" [@lun-5mcle-tp2009]. NASA's verbal definition is $M_p = x_p/d_m$, the penetration of the Moon's deepest limb divided by its diameter [@lun-5mcle-tp2009]. Stellarium computes `pMag = (L1 - m) / (2. * mSD)` and `uMag = (L2 - m) / (2. * mSD)` [@sw-stellarium-astrocalc].

The [?position-angle|position angle] of a contact on the Moon's limb is $P = M$ for interior and $P = M + 180^{\circ}$ for exterior contacts, with $\tan M = x/y$ measured eastward from north [@lun-es1992]. The Institut de mécanique céleste et de calcul des éphémérides ([IMCCE](https://www.imcce.fr/)) quotes an "angle au pôle" counted positive towards the west, which is the opposite sense [@lun-imcce-2023-may].

### Durations

The durations are differences of contacts: penumbral P4 − P1, partial U4 − U1 and total U3 − U2 [@lun-nasa-lecatkey]. The Canon figures round them to the nearest minute, and the catalogue prints tenths of a minute [@lun-5mcle-tp2009] [@lun-nasa-le2001]. Totality lasts longest near aphelion with the Moon near apogee, when the umbra is largest and the Moon is small and slow. Eighteen eclipses in the Canon exceed 106 minutes [@lun-5mcle-tp2009]. The longest of the 21st century is 2018 July 27 at 1h 42m 57s, and the shortest total eclipse is 2015 April 4 at 4m 43s [@lun-nasa-le2001].

## The NASA catalogue and canon

The Five Millennium Canon of Lunar Eclipses (NASA/TP-2009-214172) gives a diagram and a visibility map for each eclipse. The Five Millennium Catalog of Lunar Eclipses (NASA/TP-2009-214173) lists the same eclipses with additional fields [@lun-5mcle-tp2009] [@lun-5mkle-tp2009]. Their inputs are [@lun-5mcle-tp2009]:

- the Sun from VSOP87 version D, with "the complete set of periodic terms";
- the Moon from ELP-2000/82, truncated below 0.0005 arcseconds and 1 m, which gives "a mean error ... of about 0.0006 s of time in right ascension, and about 0.006 arcsec in declination" and an error in [contact times](../20-solar-eclipses-and-transits/04-local-circumstances/contact-times-and-magnitude.md) "of the order of 1/40 s";
- mean arguments from Chapront, Chapront-Touzé and Francou 2002, with a secular acceleration of the Moon of −25.858 arcseconds per century squared;
- the lunar radius $k = 0.2724880$, "a mean over the Moon's topographic features";
- the centre-of-figure offset of about 0.5 arcseconds ignored, as "much smaller than the uncertainty in the edges of the penumbral and umbral shadows";
- Danjon's enlargement.

The key page adds that "Jean Meeus" provided "the Besselian elements used in the lunar eclipse predictions", and that ΔT came from Morrison and Stephenson 2004 before the 1950s, from observations for 1955 to 2006, and from extrapolation afterwards [@lun-nasa-lecatkey]. The ASCII file `5MKLEcatalog.txt` is dated 2011 May 23 and has 12,064 data rows in fixed-width columns: catalogue number, date, TD of greatest eclipse, ΔT, lunation number, Saros number, type, QSE, gamma, penumbral and umbral magnitudes, the three durations in minutes, and the latitude and longitude of the [?lun-sublunar-point|sublunar point] at greatest eclipse [@lun-5mkle-ascii]. For the catalogues of the solar side and their file formats, see [Canons and data products](../20-solar-eclipses-and-transits/02-catalogs/canons-and-data-products.md).

EclipseWise publishes newer pages for individual eclipses. The page for 2025 March 14 lists P1 at 03:57:09.4 UT1, U1 05:09:22.6, U2 06:25:57.5, greatest eclipse 06:58:44.5, U3 07:32:01.5, U4 08:48:18.5 and P4 10:00:31.9. It gives penumbral magnitude 2.26146, umbral magnitude 1.18038, gamma 0.34846, ΔT 71.7 seconds, the Jet Propulsion Laboratory (JPL) ephemeris [DE430](../10-shared/08-lunar-and-solar-model/ephemerides.md) and the Herald and Sinnott shadow rule, last updated 2022 February 27 [@lun-ew-2025mar14]. The NASA catalogue gives this eclipse at 06:59:56 TD with ΔT 75 seconds, a value extrapolated before 2009 [@lun-nasa-le2001].

## Local circumstances: visibility, not timing

Because the contacts are the same everywhere, local circumstances reduce to the Moon's altitude at each contact. The Supplement computes the sublunar point at each instant as $\varphi = \delta_m$ and a longitude equal to "Greenwich apparent sidereal time − $\alpha_m$" [@lun-es1992]. That longitude is the Greenwich hour angle, a west longitude. Stellarium computes the east longitude as `raMoon - gast` [@sw-stellarium-astrocalc]. The horizon circle around a sublunar point $(\varphi_0, \lambda_0)$ is the great circle [@lun-es1992]

$$\tan\varphi = -\cot\varphi_0\cos(\lambda_0 - \lambda),$$

and "the hemisphere defined by this central point and horizon circle is where the Moon is above the horizon at the instant" [@lun-es1992].

The NASA Canon draws, for each contact, the curve where the Moon rises or sets at that instant [@lun-5mcle-tp2009]. It shades the map by how much of the eclipse is visible, with the whole eclipse visible in the unshaded zone and none in the darkest [@lun-5mcle-tp2009]. A vertical line marks the meridian the Moon crosses at greatest eclipse, with a dot at the sublunar point [@lun-5mcle-tp2009]. IMCCE's maps follow the same plan, with moonrise curves in red, moonset curves in blue and a curve for each phase [@lun-imcce-2023-may].

The Supplement's horizon is geocentric. Apparent moonrise is not. Meeus gives the geocentric altitude of the Moon's centre at apparent rising or setting as $h_0 = 0.7275\,\pi - 0^{\circ}34'$, about +0.125 degrees on average [@cat-meeus-1991-aa]. The term $0.7275\,\pi = \pi - k\pi$ removes the parallax and adds the semidiameter, and 34 arcminutes is the standard horizontal [?earth-refraction|refraction]. A curve drawn at $h_0$ instead of at zero altitude moves by about 0.125 degrees of arc, or 14 km on the ground. This offset is derived here from Meeus's $h_0$. Neither the Canon nor the IMCCE notes say which altitude their curves use. Stellarium grades visibility at greatest eclipse as "Perfect" above 45 degrees of lunar altitude, "Good" above 30 degrees, "Bad" below and "Invisible" below the horizon [@sw-stellarium-astrocalc].

## Time scales and ΔT

The Canon gives greatest eclipse in Terrestrial Dynamical Time, the [?tt|TT] of the corpus, and states that "to determine the geographic visibility of an eclipse, TD is converted to Universal Time ... using the parameter ΔT" [@lun-5mcle-tp2009]. Because the geometry is geocentric, [?delta-t|ΔT] does not change the eclipse. It changes only the [?earth-ut1|UT1] clock reading of each contact and the longitude of every visibility curve. "Because 1° in longitude corresponds to 4 min of time, a ΔT value of 240 s would shift the visibility zones 1° east of their TD positions" [@lun-5mcle-tp2009].

Where ΔT is uncertain, the Canon draws the uncertainty. For years before −630 and after +2428 the standard error exceeds 480 seconds, or 2 degrees of longitude, and the maps add two dashed meridians at ΔT ± σ [@lun-5mcle-tp2009]. The worked example is the partial eclipse of −1987 April 16 at 12:21 TD. With ΔT = 46,150 seconds the instant is 23:32 UT on April 15. With the standard error of ±3,676 seconds the map shifts by ±15.3 degrees [@lun-5mcle-tp2009].

The Canon also corrects published ΔT values for its choice of lunar secular acceleration. Values derived with −26 arcseconds per century squared are adjusted by

$$c = -0.91072\,(-25.858 + 26.0)\,u^2, \qquad u = (\text{year} - 1955)/100,$$

which is −202 seconds at −2000 and −14 seconds at +3000 [@lun-5mcle-tp2009]. The physics and the models of ΔT are in [ΔT and Earth rotation](../10-shared/07-earth-and-time/delta-t-and-earth-rotation.md). The use of historical lunar eclipses to measure ΔT is in [Observation, brightness and validation](observation-brightness-and-validation.md).

## How the open-source programs enumerate

**[Skyfield](https://rhodesmill.org/skyfield/).** `eclipselib.lunar_eclipses()` finds the maxima of the angle between the Earth–Sun and Earth–Moon vectors with a 5-day step. It applies aberration to the Sun and neglects [light-time](../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) to the Moon, then tests the closest approach against Danjon radii [@sw-skyfield-eclipselib]. It returns the time of greatest eclipse, a code 0, 1 or 2 for penumbral, partial or total, and the closest approach, the radii and both magnitudes. It returns no contact times and no gamma [@sw-skyfield-eclipselib]. The docstring cites section 11.2.3 of the 2013 Explanatory Supplement [@sw-skyfield-eclipselib] [@earth-es2013].

**Stellarium.** The Astronomical Calculations dialog steps through mean full moons from JD 2451550.09765 at 29.530588853 days. It iterates each to the minimum of $m$, computes the magnitudes, gamma and Saros number, and lists P1 to P4 with position angles [@sw-stellarium-astrocalc]. It switches topocentric coordinates off for the computation [@sw-stellarium-astrocalc].

**Astronomy Engine.** `Astronomy_SearchLunarEclipse` searches each full moon, prunes by latitude, finds the minimum distance of the Moon from the Sun–Earth axis in km and compares it with the shadow radii at the Moon's distance. It returns the kind, the peak time, semidurations in minutes and an obscuration [@sw-astronomy-engine-c]. Its obscuration is the fraction of the Moon's disk area inside the umbra, not a magnitude, and it is set to 1.0 for total eclipses [@sw-astronomy-engine-c].

**Meeus ports.** The Go package `eclipse.Lunar(year)` returns the type, time of maximum, $\gamma$, $\rho$, $\sigma$, magnitude and the three semidurations [@cat-soniakeys-meeus-go].

## Sources compared

| Source | Method | Outputs | Unique content |
|---|---|---|---|
| Explanatory Supplement 1961 [@lun-es1961] | $x$, $y$ in arcseconds about the antisolar point, quadratic for contacts | contacts, magnitude, P, sublunar point | Latitude limits at opposition, 1960 March 13 worked example |
| Explanatory Supplement 1992 [@lun-es1992] | same, plus discriminant tabulation | as above | Least-separation derivation, statement that no element convention exists |
| Meeus 1991 [@cat-meeus-1991-aa] | closed form from the full-moon index | γ, magnitudes, semidurations | Danjon constants with Chauvenet alternatives, 1997 example |
| NASA Canon and Catalogue 2009 [@lun-5mcle-tp2009] [@lun-5mkle-tp2009] | full ephemeris, Danjon | 12,064 eclipses with maps | ΔT uncertainty zones, statistics, series behaviour |
| EclipseWise [@lun-ew-2025mar14] | DE430, Herald and Sinnott | contacts to 0.1 s in UT1 | Current predictions under the new shadow rule |
| IMCCE note 2023 [@lun-imcce-2023-may] | Danjon by reduction | contacts, cone diameters, maps | Current French product format |
| Stellarium [@sw-stellarium-astrocalc] | ES 1961 elements, numeric rates | contacts, γ, Saros, visibility grade | Open code for the whole chain |
| Skyfield [@sw-skyfield-eclipselib] | maximum of Sun–Moon elongation | time, type, radii, magnitudes | Validated against the NASA catalogue |
| Astronomy Engine [@sw-astronomy-engine-c] | shadow distance in km | kind, peak, semidurations, obscuration | Area obscuration instead of magnitude |

## What a developer should do

Compute the elements as the Supplement does. Take apparent geocentric positions in TT, form $x$ and $y$ about the antisolar point, and fit low-order polynomials over about six hours. Find greatest eclipse from $x\dot x + y\dot y = 0$ and the six contacts from the quadratic, iterated twice. Take $R_p$ and $R_u$ from a named enlargement rule as described in [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md). Report gamma in Earth radii, both magnitudes with the NASA sign convention, the position angle of each contact and the durations. Convert to UT1 only at the output, and draw each visibility curve as the locus of geocentric lunar altitude $h_0 = 0.7275\,\pi_m - 34'$. Use Meeus's closed form only to seed the search and to cross-check types. Read the 1992 Supplement section 8.4 and the NASA Canon section 1 first.

## What this changes

The pipeline's ephemeris and time stages serve lunar eclipses unchanged. The Besselian stage gains a lunar variant with only $x$, $y$ and three limiting separations, and the local-circumstances stage becomes a horizon-circle and moonrise computation. The output gains a visibility map per contact and loses the path. A separate enlargement-rule input is required.

## Open questions

- Obtain the 2013 Explanatory Supplement, chapter 11, to see whether its lunar eclipse section defines elements or a contact method beyond the 1992 text [@earth-es2013].
- Obtain the NASA Canon's map-generation code, or a statement from [Espenak](https://en.wikipedia.org/wiki/Fred_Espenak), giving the lunar altitude used for the moonrise and moonset curves [@lun-5mcle-tp2009].
- Obtain Meeus and Mucke's *Canon of Lunar Eclipses −2002 to +2526* (1979) to compare its Besselian elements with the 2009 Catalogue [@lun-meeus-mucke-1979].
- Obtain the EclipseWise *21st Century Canon of Lunar Eclipses* to learn its ΔT model and whether its contact times include the centre-of-figure offset.
