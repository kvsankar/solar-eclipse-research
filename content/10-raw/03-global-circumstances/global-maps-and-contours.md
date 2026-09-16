---
title: Global maps and contours
description: How the curves of the partial-eclipse world map are computed: rise and set curves, maximum eclipse at sunrise and sunset, curves of maximum eclipse at stated times, outline (contact-time) curves, and contours of equal magnitude and equal obscuration.
order: 2
status: working
updated: 2026-09-15
tags: [rise-set-curves, maximum-eclipse, magnitude-contours, obscuration, world-map]
---

::: summary
- **Five curve families make the classic map.** Penumbral limits, the rising and setting curve, the curve of maximum eclipse at sunrise and sunset, curves of maximum eclipse at stated times, and outline curves of the penumbra at stated times. The 1961 and 1992 Explanatory Supplements give a closed procedure for each [@glob-es1961] [@glob-es1992].
- **The rising and setting curve is the terminator condition.** Set $\zeta = 0$ and intersect the penumbral circle with the unit circle: $\cos(\gamma - M) = (m^2 + 1 - l_1^2)/(2m)$, two points per instant, traced over time from P1 to P4 [@glob-es1961].
- **Maximum eclipse is a dynamic condition, not a geometric one.** It fixes the position angle by $\tan Q = -(y' - \eta')/(x' - \xi')$ and then sweeps $\zeta$ as the parameter. At $\zeta = 0$ it gives the maximum-at-horizon curve [@glob-es1961].
- **Equal magnitude and equal obscuration are not computed directly.** The Supplements obtain them "by inverse interpolation on the curves of maximum eclipse". SVS and Eclipse-Engine instead rasterise the maximum obscuration on a latitude–longitude grid and contour it [@glob-es1961] [@glob-svs-5123] [@glob-rherale].
- **Obscuration is a two-circle overlap.** With Sun radius 1, Moon radius $\rho$ and separation $s = 1 + \rho - 2m$ for magnitude $m$, the covered fraction is $[\rho^2\arccos\frac{s^2 + \rho^2 - 1}{2s\rho} + \arccos\frac{s^2 + 1 - \rho^2}{2s} - \tfrac12\sqrt{(-s+1+\rho)(s+1-\rho)(s-1+\rho)(s+1+\rho)}]/\pi$ [@glob-enrique7mc].
- **Jubier and NASA draw the same set.** Jubier's map: limits in pink, central line blue, maximum eclipse lines at 10-minute steps orange, penumbral limits and equal-magnitude curves green, maximum at sunrise and sunset yellow, 30-minute maximum curves violet [@glob-jubier-help].
:::

**The question.** How are the curves of a partial-eclipse world map computed from Besselian elements, in particular the rise and set loops, the curve of maximum eclipse at sunrise and sunset, the curves of maximum eclipse at stated times, the contact-time (outline) curves, and the contours of equal magnitude and equal obscuration that NASA, Jubier, timeanddate and SVS draw?

## What is on the map

NASA's explanation of its eclipse maps lists the elements [@glob-nasa-map-explain]:

- The northern and southern limits of the penumbra, which "define the region of visibility of the partial eclipse".
- The umbral path, which "bisects the penumbral path from west to east".
- P1 and P4, where the penumbra first and last touches the Earth, and P2 and P3, the interior tangencies when the penumbra "falls completely within Earth's disk".
- The rise and set loops at the eastern and western extremes.
- The curves of maximum eclipse at sunrise and sunset that bisect those loops.
- Curves of maximum eclipse "at half-hour intervals", which for central eclipses cross umbral outlines "at ten-minute intervals".
- "The curves of constant eclipse magnitude" at 0.2, 0.4, 0.6 and 0.8, which "parallel the penumbral and umbral limits".

The Five Millennium Canon, NASA/TP-2006-214141, shows only the 0.5 magnitude curve and adds the subsolar point and $\Delta T$ with its standard error expressed as a longitude shift [@glob-nasa-mapkey] [@glob-5mcse-text]. The Canon's text notes that Oppolzer's 1887 canon computed each central line "for only three positions: sunrise, mid-point, and sunset" and fitted a circular arc, so its lines "often differ by hundreds of miles" from rigorous predictions [@glob-5mcse-text].

The 1992 Supplement says the Almanac map "is a plot of the curves described in Section 8.355, except that outline curves are limited to those of the penumbra every half hour", drawn with the leading edge in short dash and the trailing edge in long dash so that first and last contact "may be estimated from the map to within a few minutes" [@glob-es1992]. Those outline curves are the contact-time contours.

## Rising and setting curve

The [?rise-set-curve] is "the locus of the end points of the outline curves". If the penumbra has both a northern and a southern limit the curve "forms two separate loops". Otherwise it "assumes the shape of a distorted figure eight", and the Supplement warns that the break into loops "does not occur at the node of the figure eight, but at a short distance from it" [@glob-es1961]. Neglecting flattening and refraction, points on the curve at each time satisfy $\zeta = 0$ and

$$\xi = x - l_1\sin Q, \qquad \eta = y - l_1\cos Q, \qquad \xi^2 + \eta^2 = 1$$

With $\xi = \sin\gamma$, $\eta = \cos\gamma$ and $x = m\sin M$, $y = m\cos M$, eliminating $Q$ gives

$$\cos(\gamma - M) = \frac{m^2 + 1 - l_1^2}{2m}$$

with two roots $\gamma$ per instant. With flattening, $\xi^2 + \eta^2 = \rho^2$ and

$$\cos(\gamma - M) = \frac{m^2 + \rho^2 - l_1^2}{2m\rho}, \qquad \eta_1 = \eta/\rho_1, \qquad \zeta_1 = 0$$

and "two approximations are necessary" because $\rho$ depends on the unknown latitude [@glob-es1961]. The 1992 edition supplies the iteration: assume $|\rho| = 1$, compute $\sin\gamma = \xi/\rho$, $\cos\gamma = \eta/\rho$, then $\tan\gamma' = \rho_1\tan\gamma$ and $\rho = \sin\gamma'/\sin\gamma$, "three or more times, until convergence". Afterwards $\xi = \sin\gamma'$, $\eta_1 = \cos\gamma'$ [@glob-es1992]. The 1992 text also states the topology rule: "if both the northern and southern limits exist for an interval of time (i.e., the central path is in equatorial regions), then during that interval the rising and setting curve does not exist", which produces the two teardrop loops [@glob-es1992].

Stellarium takes a different route. It parametrises the Earth's border in the fundamental plane as the ellipse $\xi = \cos t$, $\eta = k\sin t$ with semi-minor axis $k = 1/\sqrt{\sin^2 d + \cos^2 d/(1 - e^2)}$, substitutes into $(\xi - x)^2 + (\eta - y)^2 = L^2$, and solves the single equation in $t$ by Newton's method with root deflation, up to two roots. The author notes "the computation of the intersection is my own derivation, I haven't found it in the book" [@glob-stellarium-sec]. The curve is traced at one-minute steps from P1 to P2 and from P3 to P4 when both interior contacts exist, and from P1 to P4 otherwise [@glob-stellarium-sec].

The first and last contacts of the penumbra are the extreme times of the curve, where $\cos(\gamma - M) = 1$, $\gamma = M$, and the cone is tangent to the Earth: $x^2 + y^2 = (l_1 + \rho)^2$, solved by Newton's method in time from $(x + x't)^2 + (y + y't)^2 = (l_1 + \rho)^2$ [@glob-es1961]. The 1992 edition uses discriminants $D = x^2 + y_1^2 - (l_1 \pm \rho)^2$ for the exterior and interior contacts of each cone and finds the times by inverse interpolation [@glob-es1992].

## Curve of maximum eclipse at sunrise and sunset

This curve is the locus of points on the curves of maximum eclipse for which $\zeta = 0$. Ignoring flattening,

$$c = 1, \qquad \tan Q = b'/c_1', \qquad \sin(\gamma - Q) = x\cos Q - y\sin Q$$

with the requirement $\Delta^2 \le L_1^2$. With flattening, $c = \rho$ and $\rho\sin(\gamma - Q) = x\cos Q - y\sin Q$, iterated as for the rise and set curve. The curve "has two sections if the rising and setting curve has two separate loops; it is one continuous curve if the rising and setting curve has the shape of a distorted figure eight", in which case it "passes between the node and nearer pole" [@glob-es1961]. The 1992 edition writes the condition as its 8.3552-1, $a_1 - b_1\cos Q + c_1\sin Q = 0$, and 8.3552-2, $\rho\sin(\gamma - Q) = x\cos Q - y\sin Q$, with the existence tests $|\sin(\gamma - Q)| \le 1$ and $(x - \xi)^2 + (y - \eta_1\rho_1)^2 \le l_1^2$ [@glob-es1992]. Stellarium's `getMaximumEclipseAtRiseSet` sets $Q = \operatorname{atan2}(\dot b, \dot c)$, adds $\pi$ for the second branch, and runs three iterations "as described in equations (11.89) and (11.94)" of the 2013 edition, computing $\rho$ from $\gamma$ each time, then rejects the point if $(x - \xi)^2 + (y - \eta)^2 > L_1^2$ [@glob-stellarium-sec] [@glob-es2013].

## Curves of maximum eclipse at stated times

A [?curve-of-maximum-eclipse] is "the locus of all points at which the eclipse is at maximum at a given time". The Supplement prefers it to the curve of middle eclipse because it "corresponds to a definite geometric condition" and "may be obtained by a simple computation". The observer is written $\xi = x - \Delta\sin Q$, $\eta = y - \Delta\cos Q$ with $Q$ fixed by the maximum condition, which neglecting flattening and the small $(l' - \zeta'\tan f)$ term is

$$\tan Q = -\frac{y' - \eta'}{x' - \xi'}$$

The parameter of the curve is $\zeta$ rather than $\Delta$. With $c^2 = 1 - \zeta^2$, $\xi = c\sin\gamma$, $\eta = c\cos\gamma$,

$$\sin(\gamma - Q) = \frac{1}{c}(x\cos Q - y\sin Q)$$

taking $\cos(\gamma - Q)$ positive. For each $\zeta$ there are two values of $Q$ differing by 180 degrees, and the one outside the penumbra is discarded by $(x - \xi)^2 + (y - \eta)^2 \le L_1^2$. The starting $\zeta$ is zero if the curve has a point on the horizon, otherwise the smaller of the two penumbral-limit values, and it is increased "until $(\gamma - Q)$ becomes imaginary". Flattening is restored by $\rho^2 = \xi^2 + \eta^2 + \zeta^2$ with $\eta_1 = \eta/\rho_1$, "two approximations" being needed [@glob-es1961]. The Supplement records that the difference between maximising $L - \Delta$ and minimising $\Delta$ "can be significant for precise calculations", citing Gossner's 1955 correction to the time of maximum obscuration [@glob-es1961].

At each point the semi-duration of the partial phase and the magnitude follow:

$$\text{semi-duration} = \frac{L_1\cos\psi}{n}, \quad \sin\psi = \Delta/L_1, \quad n^2 = (x' - \xi')^2 + (y' - \eta')^2$$
$$\text{magnitude} = \frac{L_1 - \Delta}{L_1 + L_2}$$

with $\xi' = \mu'\rho\cos\phi'\cos\theta$, $\eta' = \mu'\xi\sin d$, and $L_1 + L_2$ replaceable by $2L_1 - 0.5459$ (0.5464 from 1963) [@glob-es1961]. The 1992 edition defines magnitude as "the fraction of the linear diameter of the Sun covered by the Moon" and obscuration as "the fraction of the area of the solar disk obscured by the Moon" and warns that the two are "commonly confused" [@glob-es1992].

NASA draws these curves every 30 minutes. Inside the path the 2001 bulletin's detailed maps show them at two-minute steps as "lines of maximum eclipse", each representing "the projection diameter of the umbral shadow at the given time", so that "any point on one of these lines will witness maximum eclipse (i.e., mid-totality) at the same instant" [@glob-nasa-map-explain] [@glob-nasa-tp2001]. Jubier's map draws the in-path lines at 10-minute steps in orange and the global curves at 30-minute steps in violet [@glob-jubier-help].

## Outline curves as contact-time contours

The outline curves of the penumbra at stated times, computed as in [Path and limits](path-and-limits.md) with $Q$ as the independent variable, are the loci where the partial phase begins (leading edge) or ends (trailing edge) at that time [@glob-es1961] [@glob-es1992]. They are the "eclipse begins at" and "eclipse ends at" contours of a contact-time map. SVS publishes the equivalent as `penum17_1m`, "a time sequence of penumbra outlines at 1-minute intervals from 17:00 to 19:15 UTC, for 95% to 75% obscuration in 5% steps", which are outline curves of nested cones rather than of the penumbral edge alone [@glob-svs-4518]. The 1961 Supplement says the Almanac replaced outline curves after 1960 by "curves giving the times of middle and the semi-duration of the eclipse", and that those were "constructed graphically from the intersections of a network of outline curves", extending the outlines below the horizon "by using the negative solutions for $\zeta$" [@glob-es1961]. The 1992 edition confirms that for 1960 to 1980 such curves existed and that "there is no way to calculate them directly" [@glob-es1992].

## Contours of equal magnitude and equal obscuration

The Supplements do not compute [?equal-magnitude-curve] contours directly. "A direct computation of the curves of equal semi-duration is extremely laborious because both $\Delta$ and $\zeta$ are unknown, and successive approximations based on the above relations do not always converge." The curves of equal magnitude "may also be obtained by inverse interpolation on the curves of maximum eclipse" once the magnitude has been evaluated at enough points along each curve [@glob-es1961]. The Canon calls the penumbral limits "curves of eclipse magnitude of 0.0" and the umbral limits "curves of eclipse magnitude of 1.0", and states that the 0.5 curves "run exclusively between the curves of maximum eclipse at sunrise and sunset" [@glob-5mcse-text].

Two modern methods replace the interpolation with a raster. Wright's SVS maps show "contours of obscuration, or percentage of the Sun's area covered by the Moon" at 5 per cent and 1 per cent steps (`ppath.shp`, `ppath01.shp` for 2024; `penum17` at 90, 75, 50, 25 and 0 per cent for 2017), produced by the raster method of Wright and Young 2024, which renders "eclipse maps one pixel at a time, the same way 3D animation software creates images" [@glob-svs-5123] [@glob-svs-4518] [@glob-usra-2024]. Eclipse-Engine's `obscurationGrid` evaluates the maximum obscuration on a 640 by 320 latitude–longitude grid over 121 time steps spanning the eclipse, stores the time of each cell's maximum so that contour vertices can be refined by looking "at a few instants around it rather than sweeping the six hours again", and keeps a second field, the visibility margin, from which the dashed outer limit is drawn. `contours` then traces levels on a lattice padded with real values at the map edge and refines rings to a 0.5 km tolerance over up to ten passes [@glob-rherale]. The Radiant Drift API offers "lines of equal magnitude (configurable count)" as GeoJSON but does not state its method [@glob-radiantdrift].

The obscuration at a point with magnitude $m$ and Moon/Sun apparent diameter ratio $\rho$ follows from the overlap of two circles. In the 2027 visualiser's `obscuration(m, rho)`, with the Sun of radius 1, $s = 1 + \rho - 2m$ the centre separation, the covered area is

$$A = \rho^2\arccos\frac{s^2 + \rho^2 - 1}{2s\rho} + \arccos\frac{s^2 + 1 - \rho^2}{2s} - \frac12\sqrt{(-s + 1 + \rho)(s + 1 - \rho)(s - 1 + \rho)(s + 1 + \rho)}$$

and the obscuration is $A/\pi$, with the special cases $\rho^2$ (annular, $s \le |1 - \rho|$ and $\rho < 1$), 1 (total) and 0 ($s \ge 1 + \rho$) [@glob-enrique7mc]. The timeanddate magnitude page distinguishes the same two quantities, which the search index summarised as "magnitude relates to diameter ratios while obscuration relates to area coverage". Its map page itself could not be fetched, returning HTTP 403, and the archive copy returned only navigation, so its contouring method is unrecorded here [@glob-timeanddate-magnitude]. The Swiss Ephemeris returns both quantities per location in `attr[0]` (fraction of diameter) and `attr[2]` (obscuration) [@glob-swisseph-doc].

The magnitude and obscuration contours are computed for maximum eclipse at each point, so a contour map must hold the time free per cell. That is why SVS's `penum17_1m` product, which fixes the time, and `penum17`, which fixes the level, are different datasets [@glob-svs-4518]. NASA's remark that the magnitude curves "parallel the penumbral and umbral limits" is the geometric reason the raster approach works well: the field is smooth away from the terminator [@glob-nasa-map-explain].

## Time and $\Delta T$ on the map

All curves are computed in ephemeris time and labelled in Universal Time through $\Delta T$ [@glob-es1961]. NASA's rotation page explains that predicted paths for ancient eclipses "were shifted with respect to the historical records" until $\Delta T$ was applied, and gives the longitude shift per epoch as a table with no formula. The Canon adds the standard error of $\Delta T$ "both in seconds, and in the equivalent shift in longitude east or west" to each map page [@glob-nasa-rotation] [@glob-5mcse-text]. For a modern eclipse the uncertainty is small: Jubier says the extrapolated value "should be good to better than 0.5 seconds" [@glob-jubier-help].

## Sources compared

| Source | Curves it computes | Method for magnitude or obscuration contours | Grade |
|---|---|---|---|
| Explanatory Supplement 1961 [@glob-es1961] | Rise/set, max at horizon, max at stated times, outlines, semi-duration, magnitude at points | Inverse interpolation on maximum-eclipse curves; equal semi-duration graphically from outlines | peer-reviewed |
| Explanatory Supplement 1992 [@glob-es1992] | Same set with $\gamma$ iteration for flattening and discriminants for contacts | None direct; "no way to calculate them directly" for equal semi-duration | peer-reviewed |
| NASA maps and Canon [@glob-nasa-map-explain] [@glob-5mcse-text] | All classic curves; magnitude 0.2–0.8 or 0.5 | Not stated | primary |
| Stellarium [@glob-stellarium-sec] | Limits, rise/set by ellipse–circle Newton solve, max at rise/set, outlines, central line, greatest eclipse; no magnitude contours | None | company |
| SVS / Wright [@glob-svs-5123] [@glob-wright-young-2024] | Obscuration contours 1% and 5%, penumbra outlines per minute, duration contours 30 s | Raster per pixel with terrain and limb | primary |
| Eclipse-Engine [@glob-rherale] | Obscuration bands and outer limit | 640×320 grid × 121 times, refined contours to 0.5 km | unsourced |
| Jubier [@glob-jubier-help] | Full classic set in colour code, equal magnitude in green | Not stated | company |

## What a developer should do

1. Compute the classic curves from the Supplement formulas, using $\zeta$ as the sweep parameter for the maximum-eclipse curves and $Q$ for the outlines. Keep the below-horizon roots when the map needs closed contours.
2. For magnitude and obscuration contours, rasterise: for each grid cell find the time of maximum by bracketing the derivative condition $\tan Q = -(y' - \eta')/(x' - \xi')$ or by direct minimisation of $\Delta - L_1$, evaluate $m$ and the two-circle obscuration, and contour with marching squares. Follow Eclipse-Engine's practice of padding the grid edge with real values and refining vertices near the time of maximum [@glob-rherale].
3. Compute obscuration with the exact two-circle formula and the annular special case, never from magnitude alone [@glob-enrique7mc].
4. Label every curve with the time system used and the $\Delta T$ adopted.

## What this changes

Nothing in the architecture beyond confirming that the partial-eclipse map is a separate product from the path: it needs a per-cell maximisation in time and a contouring step, while the path curves are per-time root finds. The two share only the observer transformation.

## Open questions

- The NASA method for the magnitude curves on the SEmono maps: no page read states whether they are interpolated or rasterised [@glob-nasa-map-explain].
- Gossner, S. D., "A correction to the time of maximum obscuration in solar eclipses", AJ 60, 383 (1955), cited by the 1961 Supplement for the difference between the two maximum conditions [@glob-es1961].
- The timeanddate map methodology page, blocked at fetch time. A copy is needed to say how its magnitude animation is computed [@glob-timeanddate-magnitude].
- The Explanatory Supplement 2013 equations 11.89 and 11.94, to confirm Stellarium's three-pass iteration for the maximum-at-horizon curve [@glob-es2013].
