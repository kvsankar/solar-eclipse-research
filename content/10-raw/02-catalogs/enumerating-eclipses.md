---
title: Enumerating eclipses
description: Three ways to list every solar eclipse in a period, the method and constants behind the NASA Five Millennium Canon, Saros and Inex numbering, and the accuracy ceiling set by ΔT.
order: 1
status: working
updated: 2026-09-15
tags: [enumeration, meeus, five-millennium-canon, saros, inex, delta-t]
---

::: summary
- **Meeus's approximate method finds every eclipse.** Chapter 52 of the 1991 *Astronomical Algorithms*, chapter 54 in the 1998 edition, steps through mean new moons, rejects a lunation when $|\sin F| > 0.36$, then computes $\gamma$ and $u$ from short trigonometric series. Against the NASA catalogue for 1951 to 2050 it finds all 221 eclipses, types all 221 correctly, and its times of greatest eclipse have a mean error of 0.36 min and a worst error of 1.11 min [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii].
- **A precise search is a minimum-distance search.** Ephemeris-based enumerators locate each new moon, then minimise the distance from Earth's centre to the Sun-Moon line, and test that distance against the penumbral radius plus an Earth radius. Astronomy Engine and the Swiss Ephemeris both do exactly this, with different constants [@cat-astronomy-engine] [@cat-swisseph-swecl].
- **The Five Millennium Catalogue, NASA/TP-2009-214174, used VSOP87D and a truncated ELP-2000/82.** Terms below 0.0005 arcseconds and 1 m were dropped, which costs about 1/40 s in eclipse phase times. The Moon's secular acceleration was $-25.858$ arcseconds per century squared from Chapront et al. 2002. Two lunar radii were used: $k = 0.2724880$ for penumbral contacts and $k = 0.272281$ for umbral and antumbral ones [@cat-espenak-meeus-2009-catalog].
- **$\Delta T$ dominates the error budget.** The canon states that 240 s of $\Delta T$ moves a path 1° in longitude, that the lunar ephemeris error is below map resolution even at $-1999$, and that the standard error in $\Delta T$ exceeds 265 s before +0001 and after +2300 [@cat-espenak-meeus-2006-canon].
- **Saros numbers follow van den Bergh and can be computed from the lunation number.** Kluepfel's 1985 algorithm reproduces the Saros number of all 11,898 catalogue eclipses. Odd series sit at the ascending node, even at the descending node [@cat-vangent-cycles] [@cat-espenak-meeus-2009-catalog].
- **Eclipse counts.** 11,898 solar eclipses in $-1999$ to $+3000$: 4,200 partial, 3,956 annular, 3,173 total, 569 hybrid. Per century the count runs from 222 to 255 with a mean of 238.0 [@cat-espenak-meeus-2009-catalog].
:::

**The question.** Given a start year and an end year, how does a program produce the complete, correctly typed list of solar eclipses, and how did the reference catalogue that everyone checks against do it? This note answers with the formulas and constants, the canon's own statement of its method and accuracy, and the numbering rules for [?saros|Saros] and [?inex|Inex] series. Type boundaries are detailed in [Types and classification](types-and-classification.md) and the downloadable products in [Canons and data products](canons-and-data-products.md).

## Three ways to enumerate

1. **Meeus's approximate method** uses closed-form series for the mean new moon and for two shadow quantities, $\gamma$ and $u$. It needs no ephemeris [@cat-meeus-1991-aa].
2. **An ephemeris search** iterates over new moons, finds the instant of minimum distance between the geocentre and the shadow axis, and classifies from the umbral radius at the geoid. Astronomy Engine, the Swiss Ephemeris and the open Skyfield pull request all follow this shape [@cat-astronomy-engine] [@cat-swisseph-swecl] [@cat-skyfield-pr-1076].
3. **A full Besselian computation** derives the [?besselian-elements|Besselian elements] for each candidate and reads $\gamma$, magnitude, path width and duration from them. This is what Espenak and Meeus did for the NASA [?canon|canon] and catalogue [@cat-espenak-meeus-2009-catalog].

Approach 1 decides *whether* and *which type*. Approach 3 is needed for every quantity a catalogue lists.

## Meeus's approximate method

The method is Chapter 52 in the 1991 first edition and Chapter 54 in the 1998 second edition of *Astronomical Algorithms*. The text below quotes the 1991 edition, which was read in full. The second-edition coefficients were read from a tested MIT-licensed port and from a worked example, and differ only in the polynomial constants for the mean new moon and $F$ [@cat-meeus-1991-aa] [@cat-soniakeys-meeus-go] [@cat-squarewidget-meeus].

### Step 1: mean new moon and the argument of latitude

Let $k$ be an integer for a new moon, with $k = 0$ at the new moon of 2000 January 6. An approximate $k$ for a decimal year is $k \approx (\text{year} - 2000) \times 12.3685$. With $T = k / 1236.85$ in Julian centuries from J2000.0, the second edition gives the instant of mean conjunction as

$$\text{JDE} = 2451550.09766 + 29.530588861\,k + 0.00015437\,T^2 - 0.000000150\,T^3 + 0.00000000073\,T^4$$

and the Moon's mean [?argument-of-latitude|argument of latitude] as

$$F = 160.7108^{\circ} + 390.67050284^{\circ}\,k - 0.0016118^{\circ}\,T^2 - 0.00000227^{\circ}\,T^3 + 0.000000011^{\circ}\,T^4 .$$

The other angles are the Sun's mean anomaly $M = 2.5534^{\circ} + 29.1053567^{\circ}\,k - 0.0000014^{\circ}\,T^2 - 0.00000011^{\circ}\,T^3$, the Moon's mean anomaly $M' = 201.5643^{\circ} + 385.81693528^{\circ}\,k + 0.0107582^{\circ}\,T^2 + 0.00001238^{\circ}\,T^3 - 0.000000058^{\circ}\,T^4$, the longitude of the ascending node $\Omega = 124.7746^{\circ} - 1.56375588^{\circ}\,k + 0.0020672^{\circ}\,T^2 + 0.00000215^{\circ}\,T^3$, and the eccentricity factor $E = 1 - 0.002516\,T - 0.0000074\,T^2$ [@cat-soniakeys-meeus-go] [@cat-squarewidget-meeus].

### Step 2: the eclipse-possibility test

Meeus 1991 states the rule in three tiers. "If $F$ differs from the nearest multiple of 180° by less than 13°.9, then there is certainly an eclipse; if the difference is larger than 21°.0, there is no eclipse; between these two values, the eclipse is uncertain at this stage and the case must be examined further. Use can be made of the following rule: there is no eclipse if $|\sin F| > 0.36$." He adds that "after one lunation, $F$ increases by 30°.6705" and that $F$ near 0° or 360° means the ascending node, $F$ near 180° the descending node [@cat-meeus-1991-aa].

The number 0.36 is $\sin 21.1^{\circ}$, so the single inequality carries the whole test. A program can therefore loop over $k$, evaluate $F$, and discard a lunation with one sine.

### Step 3: time of greatest eclipse

Compute $F_1 = F - 0^{\circ}.02665 \sin \Omega$ and $A_1 = 299^{\circ}.77 + 0^{\circ}.107408\,k - 0.009173\,T^2$. Then add to the mean-conjunction JDE the sum of the following terms in days [@cat-meeus-1991-aa]:

$$\begin{aligned}
&-0.4075 \sin M' + 0.1721\,E \sin M + 0.0161 \sin 2M' - 0.0097 \sin 2F_1 \\
&+ 0.0073\,E \sin(M'-M) - 0.0050\,E \sin(M'+M) - 0.0023 \sin(M'-2F_1) + 0.0021\,E \sin 2M \\
&+ 0.0012 \sin(M'+2F_1) + 0.0006\,E \sin(2M'+M) - 0.0004 \sin 3M' - 0.0003\,E \sin(M+2F_1) \\
&+ 0.0003 \sin A_1 - 0.0002\,E \sin(M-2F_1) - 0.0002\,E \sin(2M'-M) - 0.0002 \sin \Omega .
\end{aligned}$$

For lunar eclipses the first two coefficients become $-0.4065$ and $+0.1727$. Meeus states the accuracy: "For the 221 solar eclipses of the years A.D. 1951 to 2050, the method gives a mean error of 0.36 minute, and a greatest error of 1.1 minute in the times of maximum eclipse." He warns that "this algorithm should not be used, of course, if high accuracy is needed" [@cat-meeus-1991-aa].

### Step 4: gamma and the umbral radius

$$P = 0.2070\,E \sin M + 0.0024\,E \sin 2M - 0.0392 \sin M' + 0.0116 \sin 2M' - 0.0073\,E \sin(M'+M) + 0.0067\,E \sin(M'-M) + 0.0118 \sin 2F_1$$

$$Q = 5.2207 - 0.0048\,E \cos M + 0.0020\,E \cos 2M - 0.3299 \cos M' - 0.0060\,E \cos(M'+M) + 0.0041\,E \cos(M'-M)$$

$$W = |\cos F_1|, \qquad \gamma = (P \cos F_1 + Q \sin F_1)(1 - 0.0048\,W)$$

$$u = 0.0059 + 0.0046\,E \cos M - 0.0182 \cos M' + 0.0004 \cos 2M' - 0.0005 \cos(M + M')$$

Meeus defines the symbols: "$\gamma$ represents the least distance from the axis of the Moon's shadow to the center of the Earth, in units of the equatorial radius of the Earth. The quantity $\gamma$ is positive or negative, depending upon the axis of the shadow passing north or south of the Earth's center." And "$u$ denotes the radius of the Moon's umbral cone in the [?fundamental-plane|fundamental plane], again in units of the Earth's equatorial radius." The penumbral radius in that plane is $u + 0.5461$ [@cat-meeus-1991-aa].

### Step 5: classification

The rules, quoted from Meeus 1991 and reproduced verbatim in the Go port [@cat-meeus-1991-aa] [@cat-soniakeys-meeus-go]:

- "When $\gamma$ is between +0.9972 and −0.9972, the solar eclipse is central: there exists a line of central eclipse on the Earth's surface."
- "If $|\gamma|$ is between 0.9972 and 1.5433 + u, the eclipse is not central. In most cases, it is then a partial eclipse. However, when $|\gamma|$ is between 0.9972 and 1.0260, a part of the umbral cone may touch the surface of the Earth (within the polar regions), while the axis of the cone does not touch the Earth. These non-central total or annular eclipses occur when $0.9972 < |\gamma| < 0.9972 + |u|$."
- "If $|\gamma| > 1.5433 + u$, no eclipse is visible from the Earth's surface."
- For a central eclipse: "if $u < 0$, the eclipse is total; if $u > +0.0047$, the eclipse is annular; if $u$ is between 0 and +0.0047, the eclipse is either annular or annular-total." The ambiguity is removed by $\omega = 0.00464 \sqrt{1 - \gamma^2}$: "if $u < \omega$, the eclipse is annular-total; otherwise it is an annular one."
- For a partial eclipse the greatest magnitude on Earth is equation (52.2), $\dfrac{1.5433 + u - |\gamma|}{0.5461 + 2u}$.

The constant 0.9972 is the polar flattening of the Earth's cross-section seen from the shadow axis, 1.5433 is $0.9972 + 0.5461$, and 0.5461 is the difference between penumbral and umbral radii in the fundamental plane for a mean lunar distance. Meeus 1991 lists the seven [?non-central-eclipse|non-central] eclipses of 1950 to 2100: 1950 Mar 18, 1957 Apr 30, 2014 Apr 29 and 2043 Oct 03 annular, 1957 Oct 23, 1967 Nov 02 and 2043 Apr 09 total. The NASA catalogue gives the same seven dates as its examples [@cat-meeus-1991-aa] [@cat-espenak-meeus-2009-catalog].

### A check against the catalogue

The method above was implemented in about sixty lines of Python from the constants quoted here, run for $k$ from $-607$ to $+632$, and matched by time against the NASA ASCII catalogue for 1951 to 2050. Result: 221 eclipses found, 221 in the catalogue, no missing and no spurious event, zero type disagreements including the six [?hybrid-eclipse|hybrids] and the non-central cases, mean absolute time difference 0.36 min with a maximum of 1.11 min, and mean absolute difference in $\gamma$ of 0.0006 with a maximum of 0.0026 [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii]. Meeus's accuracy statement is reproduced exactly, and 0.0026 in $\gamma$ is small against the 0.0288 gap between 0.9972 and 1.0260.

## The precise method: ephemeris search

The precise method replaces the series with an ephemeris and the thresholds with geometry. The logic is the same: find the new moon, find the instant when the shadow axis is nearest the geocentre, compare that distance with the shadow radii.

### Astronomy Engine

`Astronomy_SearchGlobalSolarEclipse` in the C source loops over at most twelve consecutive new moons from `Astronomy_SearchMoonPhase(0.0, ...)`. It prunes with `const double PruneLatitude = 1.8; /* Moon's ecliptic latitude beyond which eclipse is impossible */`. For a surviving new moon `PeakMoonShadow` minimises the perpendicular distance `shadow.r` in kilometres from the Earth's centre to the Sun-Moon line, and the eclipse test is `if (shadow.r < shadow.p + EARTH_MEAN_RADIUS_KM)` with `EARTH_MEAN_RADIUS_KM 6371.0`. `CalcShadow` gives the umbral radius `shadow.k = +SUN_RADIUS_KM - (1.0 + shadow.u)*(SUN_RADIUS_KM - body_radius_km)` and the penumbral radius `shadow.p = -SUN_RADIUS_KM + (1.0 + shadow.u)*(SUN_RADIUS_KM + body_radius_km)`, where `shadow.u` is the fraction of the Sun-Moon distance beyond the Moon at which the closest point lies. The Moon's radius is `MOON_MEAN_RADIUS_KM 1737.4` for the search and `MOON_POLAR_RADIUS_KM 1736.0` at the geoid intersection. The type is `#define EclipseKindFromUmbra(k) (((k) > 0.014) ? ECLIPSE_TOTAL : ECLIPSE_ANNULAR)`, with the comment "HACK: I added a tiny bias (14 meters) to match Espenak test data." If the axis misses the oblate geoid the event is partial. The library claims ±1 arcmin and uses truncated VSOP87 [@cat-astronomy-engine].

Two consequences. Astronomy Engine has no hybrid class, since the type is the umbral radius at the one point where the axis meets the geoid at [?greatest-eclipse|greatest eclipse]. And it has no non-central class, so an eclipse whose axis misses the geoid is partial even when the umbra grazes the polar cap.

### Swiss Ephemeris

`swe_sol_eclipse_when_glob` in `swecl.c` begins from a lunation index `K = (int)((tjd_start - J2000) / 365.2425 * 12.3685)`, then refines the time of maximum by bracketing the quantity `dc = acos(dot(sun_unit, moon_unit)) - (rmoon + rsun)` with step `dt` starting at 1 day (5 days outside JD 2000000 to 2500000) and dividing by 4 until `dt < 0.0001` day, calling `find_maximum` at each level [@cat-swisseph-swecl]. Classification happens in `eclipse_where`. With `de = 6378140.0 / AUNIT`, `s0 = -dot_prod(rm, e)` the Moon's distance from the fundamental plane, `r0 = sqrt(dm*dm - s0*s0)` the distance of the shadow axis from the geocentre, `d0 = (s0/dsm*(drad*2 - dmoon) - dmoon)/cosf1` the umbral diameter on the fundamental plane and `D0` the penumbral diameter, the tests are:

```
if (de * cosf1 >= r0)                    retc |= SE_ECL_CENTRAL;
else if (r0 <= de * cosf1 + fabs(d0)/2)  retc |= SE_ECL_NONCENTRAL;
else if (r0 <= de * cosf2 + D0/2)        retc |= (SE_ECL_PARTIAL | SE_ECL_NONCENTRAL);
else                                     /* no solar eclipse */
```

Hybrids are found afterwards: the umbral core diameter is evaluated at maximum and at both ends of the central line, and "if (dc[0]*dc[1] < 0 || dc[0]*dc[2] < 0)" the flag becomes `SE_ECL_ANNULAR_TOTAL`, with the comment "the maximum is always total, and there is either one or two times before and after, when the core shadow becomes zero and totality changes into annularity or vice versa." The constants are `DSUN (1392000000.0 / AUNIT)`, `DMOON (3476300.0 / AUNIT)` and `DEARTH (6378140.0 * 2 / AUNIT)`, so the Moon's radius is 1738.15 km, or $k = 0.27252$ in units of the 6378.14 km equatorial radius [@cat-swisseph-swecl]. The documentation lists the return bits `SE_ECL_CENTRAL`, `SE_ECL_NONCENTRAL`, `SE_ECL_TOTAL`, `SE_ECL_ANNULAR`, `SE_ECL_PARTIAL`, `SE_ECL_ANNULAR_TOTAL` and a ten-element `tret[]` with maximum, local noon, begin, end, totality begin and end, central-line begin and end, and two unimplemented annular-total transition slots. Times in and out are UT [@cat-swisseph-doc].

### Skyfield

Skyfield's almanac has `skyfield.eclipselib.lunar_eclipses(t0, t1, eph)` and no solar equivalent, only `oppositions_conjunctions` plus `find_discrete` for new moons [@cat-skyfield-almanac]. Pull request 1076, prompted by issue 1078 of May 2025, adds a routine that "looks for minimum" of the Earth-Sun to Earth-Moon angle and tests the penumbra, umbra and antumbra against Earth. The author reports "the agreement of routine results with the official data for the last ~400 years is rather good", with misidentifications for "eclipses that last 0 seconds" and "low magnitude partial eclipses" where the choice of polar versus equatorial Earth radius decides. The pull request was still open when read [@cat-skyfield-pr-1076] [@cat-skyfield-issue-1078].

### From enumeration to Besselian elements

Once a lunation passes the test, a precise product computes the Besselian elements and takes $\gamma$ as the minimum of $\sqrt{x^2 + y^2}$ over the eclipse, signed by $y$ at that instant. The catalogue defines the instant: "The instant of greatest eclipse occurs when the distance between the axis of the Moon's shadow cone and the center of Earth reaches a minimum" [@cat-espenak-meeus-2009-catalog]. The Swiss Ephemeris `r0` and Astronomy Engine's `shadow.r` are that distance in kilometres. Every catalogued quantity and its derivation from the elements is in [Types and classification](types-and-classification.md).

## How Espenak and Meeus built the Five Millennium Canon

NASA/TP-2006-214141 is the canon of maps, NASA/TP-2009-214174 is the revised catalogue of tables. Both were read from the PDFs. The catalogue's Section 1 carries the method statement and is quoted here [@cat-espenak-meeus-2006-canon] [@cat-espenak-meeus-2009-catalog].

### Ephemerides

"The coordinates of the Sun used in these eclipse predictions have been calculated on the basis of the VSOP87 theory constructed by Bretagnon and Francou (1988) ... The complete set of periodic terms of version D of VSOP87 (this version provides the positions referred to the mean equinox of the date) were used." For the Moon, "use has been made of the theory ELP-2000/82 of Chapront-Touzé and Chapront (1983) ... The computer program used in the eclipse predictions neglects all periodic terms with coefficients smaller than 0.0005 arcsec in longitude and latitude, and smaller than 1 m in distance." The truncation error is "about 0.0006 s of time in right ascension, and about 0.006 arcsec in declination. The corresponding error in the calculated times of the phases of a solar eclipse is of the order of 1/40 s, which is considerably smaller than the uncertainties in predicted values of ΔT, and also much smaller than the error due to neglecting the irregularities (mountains and valleys) at the lunar limb" [@cat-espenak-meeus-2009-catalog].

"Improved expressions for the mean arguments L, D, M, M′, and F have been taken from Chapront, Chapront-Touzé, and Francou (2002)", bringing the [?secular-acceleration|secular acceleration] of the Moon's longitude, $-25.858$ arcseconds per century squared, "into good agreement with Lunar Laser Ranging (LLR) observations from 1972 to 2001." The almanac offices' centre-of-figure correction, "typically +0.50 arcsec in longitude and −0.25 arcsec in latitude", was not applied: "The authors have chosen to ignore this convention and have performed all calculations using the Moon's center of mass position" [@cat-espenak-meeus-2009-catalog].

### Lunar radius

Section 1.5 explains the two [?k-lunar-radius|k] values. "From 1968 to 1980, the Nautical Almanac Office used two separate values for k in their predictions. The larger value (k=0.2724880), representing a mean over topographic features, was used for all penumbral (exterior) contacts and for annular eclipses. A smaller value (k=0.272281), representing a mean minimum radius, was reserved exclusively for umbral (interior) contact calculations of total eclipses." The IAU 1982 value $k = 0.2725076$ "guarantees that some annular or hybrid eclipses will be misidentified as total. A case in point is the eclipse of 1986 Oct 03", listed in the Astronomical Almanac for 1986 as total for 3 s "when it was, in fact, a beaded annular eclipse." The choice: "The larger value (k=0.2724880) is utilized for all partial (penumbral) eclipses. ... the smaller value (k=0.272281) is used for all umbral and antumbral eclipses (total, annular, and hybrid)", giving shorter, narrower total paths and longer, wider annular paths than the IAU value [@cat-espenak-meeus-2009-catalog].

### ΔT

The ΔT models and their uncertainties are the subject of [ΔT and Earth rotation](../07-earth-and-time/delta-t-and-earth-rotation.md). This section keeps only the choices the catalogue itself made and states. The [?delta-t|ΔT] model has three regimes. Before 1950, "empirical fits to historical records derived by Morrison and Stephenson (2004)", whose cubic-spline table from $-500$ to $+1950$ is reproduced with standard errors from 430 s at $-500$ down to below 1 s after 1800. From 1955 to 2005, the observed values from the Astronomical Almanac for 2006, page K9. For the future, extrapolation "weighted by the long period trend from tidal braking of the Moon", giving estimates of +67 s in 2010, +93 s in 2050, +203 s in 2100 and +442 s in 2200 [@cat-espenak-meeus-2009-catalog] [@cat-morrison-stephenson-2004].

Outside the observed span the long-term parabola is $\Delta T = -20 + 32u^2$ s with $u = (\text{year} - 1820)/100$. Section 2.7 gives twelve polynomials in the decimal year $y = \text{year} + (\text{month} - 0.5)/12$ that cover $-1999$ to $+3000$. Two examples: between $-500$ and $+500$, with $u = y/100$, $\Delta T = 10583.6 - 1014.41u + 33.78311u^2 - 5.952053u^3 - 0.1798452u^4 + 0.022174192u^5 + 0.0090316521u^6$, and between 2005 and 2050, with $t = y - 2000$, $\Delta T = 62.92 + 0.32217t + 0.005589t^2$. The full set is on NASA's polynomial page and in the catalogue [@cat-nasa-deltatpoly] [@cat-espenak-meeus-2009-catalog].

The acceleration mismatch is corrected explicitly. "All values of ΔT, based on Morrison and Stephenson (2004), assume a value for the Moon's secular acceleration of −26 arcsec/cy². However, the ELP-2000/82 lunar ephemeris employed in the Catalog uses a slightly different value of −25.858 arcsec/cy². Thus, a small correction "c" must be added":

$$c = -0.000012932\,(y - 1955)^2 \text{ s}, \qquad \text{the general form being } c = -0.91072\,(-25.858 + 26.0)\,u^2,\ u = (\text{year} - 1955)/100 .$$

The correction is $-202$ s at $-2000$, $-49$ s at 0 and $-14$ s at $+3000$, and is zero for 1955 to 2005 because those values are independent of any lunar ephemeris [@cat-espenak-meeus-2009-catalog].

### The canon's own accuracy statement

Section 1.6 of the canon: "the lunar ephemeris is accurate to better than an arcsecond within several centuries of the present. Even for eclipses occurring in the year −1999 (2000 BCE), the Moon's position is correct to within a small fraction of a degree. Such positional discrepancies correspond to errors in predicted eclipse paths that are below the resolution threshold of the maps." Then: "A far greater source of error in the geographic position of eclipse paths is due to the uncertainty in ΔT. ... Because 1° in longitude corresponds to 4 min of time, a ΔT value of 240 s would shift the eclipse path 1° east of its TD position." Maps whose standard error exceeds 265 s, which is 1.1° of longitude, carry a "reference gore" of two dashed meridians at $\Delta T \pm \sigma$: "The years prior to +0001 and after +2300 have uncertainties of this magnitude or greater." The worked example is the total eclipse of $-1996$ Oct 04 at 23:24 TD with $\Delta T = 46{,}358$ s and $\sigma = \pm 3{,}712$ s, so the map may be rotated $\pm 15.5^{\circ}$ [@cat-espenak-meeus-2006-canon].

The standard error model is Morrison and Stephenson's $\sigma = 0.8\,t^2$ s with $t = (\text{year} - 1820)/100$, valid $-1000$ to $+1200$, giving 636 s at $-1000$, 265 s at 0 and 31 s at $+1200$. Outside that span the catalogue uses Huber's Brownian-drift model, $\sigma = 365.25\,N\,\sqrt{(N Q / 3)(1 + N/M)} / 1000$ s with $N$ years from the calibration year ($-500$ for the past, 2005 for the future), $M = 2500$ years and $Q = 0.058$ ms²/yr, giving 6,094 s at $-2000$ and 20,717 s at $-4000$ [@cat-espenak-meeus-2009-catalog] [@cat-nasa-uncertainty].

Stephenson, Morrison and Hohenkerk 2016 later revised the analysis: the length of day "increases at an average rate of +1.8 ms per century. This is significantly less than the rate predicted on the basis of tidal friction, which is +2.3 ms per century", with a long-term parabola $\Delta T = -320.0 + (32.5 \pm 0.6)\,((\text{year} - 1825)/100)^2$ s, "some indication of an oscillation in the lod with a period of roughly 1500 years", and the lunar acceleration implicit in JPL DE430 given as $-25.82$ arcseconds per century squared. Their method for untimed records: "a report that an eclipse was total or near-total at a known place fixes the rotational frame of the Earth" [@cat-stephenson-2016]. The NASA catalogue predates this and uses the 2004 splines and the $-20 + 32u^2$ parabola. A modern product should state which it adopts.

### Eclipse counts

The catalogue counts 11,898 solar eclipses in $-1999$ to $+3000$: 4,200 partial (35.3%), 3,956 annular (33.2%), 3,173 total (26.7%) and 569 hybrid (4.8%). Per century "the number of eclipses in any one century ranges from 222 to 255 with an average of 238.0", with a cycle "a little under six centuries" long, and the 20th and 21st centuries are poor with 228 and 224 eclipses. Two eclipses fall in 72.5% of calendar years, three in 17.5%, four in 9.5% and five in 0.5% [@cat-espenak-meeus-2009-catalog] [@cat-nasa-secatalog]. Parsing the ASCII catalogue gives, for 1901 to 2000, 78 partial, 73 annular, 71 total and 6 hybrid, and for 2001 to 2100, 77 partial, 72 annular, 68 total and 7 hybrid [@cat-nasa-5mkse-ascii].

![Partial, annular and total eclipses occur in comparable numbers over five millennia, within nine percentage points of one another, while hybrids are rarer than any of them by a factor of about six. A product that treats hybrids as a special case is therefore handling 4.8% of eclipses, and one that cannot classify them at all is wrong about 569 rows [@cat-espenak-meeus-2009-catalog].](img/catalogue-composition.svg)

## Saros, Inex and series numbering

### The periods

The catalogue gives the 2000 CE values: synodic month 29.530589 d, anomalistic month 27.554550 d, draconic month 27.212221 d. "One Saros is equal to 223 synodic months, however, 239 anomalistic months and 242 draconic months are also equal (within a few hours) to this same period": 223 synodic months = 6585.3223 d, 239 anomalistic = 6585.5375 d, 242 draconic = 6585.3575 d. The Inex is 358 synodic months = 10,571.9509 d against 388.5 draconic months = 10,571.9479 d, so consecutive Inex eclipses fall at opposite nodes. The node shifts 0.48° per Saros and 0.04° per Inex, which is why "a Saros series lasts 12 to 15 centuries, an Inex series typically lasts 225 centuries and contains about 780 eclipses". A Saros series "may last 1,226 to 1,551 years and is composed of 69 to 87 eclipses, of which 39 to 59 are umbral/antumbral". In 2008 there were 39 active series numbered 117 to 155 [@cat-espenak-meeus-2009-catalog] [@cat-nasa-sesaros]. Three Saros make an [?exeligmos|Exeligmos] of 669 lunations, after which a path returns to nearly the same longitudes. Each [?eclipse-season|eclipse season] lasts about 34.5 days and seasons recur every 173.3 days, with the Sun within 15.39° to 18.59° of a node at every solar eclipse [@cat-nasa-seperiodicity].

### Numbering

"The numbering system used for the Saros series was introduced by van den Bergh in his book *Periodicity and Variation of Solar (and Lunar) Eclipses* (1955). He assigned the number 1 to a pair of solar and lunar eclipse series that were in progress during the second millennium BCE based on an extrapolation from von Oppolzer's Canon der Finsternisse (1887)." The node rule: "The eclipses with an odd Saros number take place at the ascending node of the Moon's orbit; those with an even Saros number take place at the descending node." Gamma changes monotonically through a series, decreasing for odd and increasing for even series, with rare reversals near perihelion when Earth's eccentricity was larger, the extreme case being Saros 0 [@cat-espenak-meeus-2009-catalog] [@cat-van-den-bergh-1955].

### How a catalogue assigns the Saros number

Two methods are documented. The first is incremental: given the Saros number $s$ of one eclipse, the next eclipse 1 lunation later has $s + 38$, 5 lunations later $s - 33$, and 6 lunations later $s + 5$. The catalogue's Table 5-10 also lists 135 lunations (Tritos) $s + 1$, 235 (Metonic) $s + 10$, 358 (Inex) $s + 1$ and 669 (Exeligmos) $s$, attributing the relationships to Meeus, Grosjean and Vanderleen 1966 [@cat-espenak-meeus-2009-catalog].

The second is closed-form. Van Gent's catalogue of eclipse cycles states: "The Saros series number SNS of a solar eclipse (introduced by George van den Bergh in the 1950's) can be derived from the [?lunation-number|lunation number] LN with the following algorithm first given by Charles Kluepfel (1985):"

$$\begin{aligned}
ND &= LN + 105 \\
NS &= 136 + 38\,ND \\
NX &= -61\,ND \\
NC &= \lfloor NX/358 + 0.5 - ND/(12 \cdot 358 \cdot 358) \rfloor \\
SNS &= ((NS + 223\,NC - 1) \bmod 223) + 1
\end{aligned}$$

with "LN = Lunation number (0 on 6 January 2000)" and "LN = Brown Lunation Number − 953" [@cat-vangent-cycles]. The formula was run on all 11,898 rows of the NASA ASCII catalogue using its lunation column: it reproduced the Saros column in every case modulo 223. The modulus is needed because the catalogue's Saros numbers run from $-13$ to $194$ while the formula returns 1 to 223 [@cat-nasa-5mkse-ascii]. Since 223 and 358 are coprime, "any integer number of lunations (k) can thus be expressed as a combination of inex and saros cycles: k = m I + n S" [@cat-vangent-cycles].

### The Saros-Inex panorama

Van den Bergh "placed all 8,000 solar eclipses in von Oppolzer's Canon der Finsternisse (1887) into a large two-dimensional matrix. Each Saros series was arranged as a separate column containing every eclipse in chronological order. The individual Saros columns were then staggered so that the horizontal rows each corresponded to different Inex series." In this [?saros-inex-panorama|panorama] one step down is one Saros, one step right is one Inex, and any interval between two solar eclipses is $t = a\,i + b\,s$ days with $i = 10571.95$, $s = 6585.32$ and integers $a, b$. He used it to extend Oppolzer's canon back from $-1207$ to $-1600$ by arithmetic alone [@cat-espenak-meeus-2009-catalog]. NASA hosts a modern panorama by Luca Quaglia and John Tilley, "a Microsoft Excel file" that "shows 61775 solar eclipses from −11000 to +15000 organised by Saros and Inex Series" in 911 Saros columns computed with the Solex integrator [@cat-nasa-panorama]. The 5000-year catalogue contains eclipses from 204 Saros series, 121 of them complete [@cat-espenak-meeus-2009-catalog].

## Sources compared

| Source | Period | Ephemeris | ΔT | Lunar radius | What only it gives |
|---|---|---|---|---|---|
| Meeus AA ch. 52, 1991 edition [@cat-meeus-1991-aa] | any | none, series | none, JDE only | implicit in $u$ | Closed-form $\gamma$, $u$, type, partial magnitude with 0.9972, 1.5433, 0.0047, 0.00464 |
| Espenak and Meeus canon and catalogue [@cat-espenak-meeus-2009-catalog] | $-1999$ to $+3000$ | VSOP87D, ELP-2000/82 truncated, $\dot n = -25.858$ | M&S 2004 splines, polynomials, $-20 + 32u^2$, correction $c$ | 0.2724880 and 0.272281 | Standard-error gores, statistics, Saros tables, published Besselian elements |
| Astronomy Engine [@cat-astronomy-engine] | any | truncated VSOP87 | internal | 1737.4 km, 1736.0 km at geoid | Total or annular by 14 m umbra bias, no hybrid or non-central class |
| Swiss Ephemeris [@cat-swisseph-swecl] | any | DE or Moshier | internal, user-settable | 1738.15 km | Central, non-central, hybrid by sign change of core diameter, UT in and out |
| Skyfield [@cat-skyfield-almanac] | any | any SPK | IERS tables | not applicable | Lunar eclipses only, solar routine in open PR 1076 |
| Van Gent cycles [@cat-vangent-cycles] | not applicable | not applicable | not applicable | not applicable | Kluepfel closed-form Saros number from lunation number |
| Stephenson et al. 2016 [@cat-stephenson-2016] | $-720$ to $+2015$ | DE430 | new splines, $-320 + 32.5t^2$ | not applicable | Current ΔT and lod trend, 1.8 versus 2.3 ms/cy |

## What a developer should do

1. Enumerate with Meeus's series first. Implement Steps 1 to 5 as quoted, test against the 221 eclipses of 1951 to 2050 in the NASA ASCII catalogue, and expect zero type disagreements and a maximum time error near 1.1 min [@cat-meeus-1991-aa] [@cat-nasa-5mkse-ascii].
2. For each candidate, compute Besselian elements from a modern ephemeris and take $\gamma$ from the minimum of $\sqrt{x^2 + y^2}$. Keep the series value only as a sanity check within 0.003.
3. State $k$. The canon's pair, 0.2724880 penumbral and 0.272281 umbral and antumbral, is the only choice that reproduces its types and durations [@cat-espenak-meeus-2009-catalog].
4. Choose a $\Delta T$ model and print its standard error with every eclipse before +0001 or after +2300. Use NASA's polynomials and correction $c$ to match the catalogue, or Stephenson 2016 for the best current estimate, and say which [@cat-nasa-deltatpoly] [@cat-stephenson-2016].
5. Compute Saros numbers with Kluepfel's formula from the lunation number, subtracting 223 where needed to land in the catalogue's range [@cat-vangent-cycles].
6. Read first: catalogue Sections 1.3 to 1.5 and 2.6 to 2.8 [@cat-espenak-meeus-2009-catalog], canon Section 1.6 [@cat-espenak-meeus-2006-canon], Meeus 1991 Chapter 52 [@cat-meeus-1991-aa], and `swecl.c` lines 640 to 780 and 1185 to 1450 [@cat-swisseph-swecl].

## What this changes

The enumeration stage is solved and cheap, so the pipeline design should not spend effort on it beyond a Meeus pre-filter feeding a Besselian stage. Two things do change. First, the $k$ choice must be fixed before the final type is assigned, because it decides the type of near-hybrid events and not just their durations. The enumeration stage itself carries only a provisional Meeus type, and the decision is made in the Besselian stage, as set out in [Types and classification](types-and-classification.md). Second, the accuracy statement of any product covering years before +0001 or after +2300 must be a $\Delta T$ standard error, not an ephemeris error, because the canon shows the ephemeris contribution is below map resolution and the $\Delta T$ contribution reaches tens of degrees of longitude.

## Open questions

- Obtain Meeus, *Elements of Solar Eclipses 1951-2200* (Willmann-Bell 1989), for the formulas Espenak and Meeus used to derive path width and central duration from the Besselian elements. Only the catalogue's definitions were read.
- Obtain the 2020 addendum to Stephenson, Morrison and Hohenkerk (Proc. R. Soc. A 477, 20200776) to see whether the 1.8 ms/cy rate and the parabola were revised.
- Obtain the source of the NASA Besselian-element generator. The CSV headers show the columns `PNS`, `UNS`, `NCN`, `nSer`, `nSeq`, `nJLE` whose meaning is not documented on the site [@cat-nasa-besselian-csv].
- Obtain Kluepfel's 1985 note, cited by van Gent, to confirm the origin of the constants 105, 136, 38 and 61 in the Saros formula [@cat-vangent-cycles].
- Obtain the Swiss Ephemeris `swe_deltat` source to record which $\Delta T$ model it applies by default in 2026, since the documentation read did not state it [@cat-swisseph-doc].
