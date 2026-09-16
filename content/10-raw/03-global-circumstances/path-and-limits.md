---
title: Path and limits
description: The formulas for the central line, the umbral and penumbral limits, the shadow outline, duration, path width, greatest eclipse and umbra speed, with the oblate-Earth treatment and the limb and terrain corrections that the main implementations apply.
order: 1
status: working
updated: 2026-09-15
tags: [central-line, limits, outline, path-width, duration, oblate-earth, besselian]
---

::: summary
- **The central line is a square root.** At time $t$ the shadow axis meets the ellipsoid where $\xi = x$, $\eta_1 = y/\rho_1$ and $\zeta_1 = \sqrt{1 - x^2 - \eta_1^2}$, in a frame where the flattened Earth is a unit sphere. Everything else on the map is a variation on this step [@glob-es1961].
- **The limits are a root-finding problem in one angle.** A point is on a limit when the eclipse begins and ends at the same instant. That gives one condition on the position angle $Q$ of the shadow edge, $\tan Q = (b' - \zeta d' - a'\sec Q)/(c' - \zeta\mu'\cos d)$, and an iteration on $\zeta$ because the height above the fundamental plane is not known until the point is found [@glob-es1961] [@glob-es1992].
- **Duration and width are local ratios.** Central duration is $2L_2/n$ with $L_2 = l_2 - \zeta\tan f_2$ and $n$ the shadow speed relative to the rotating observer. Path width follows Mikhailov's 1931 formula, $2L_2\,[\zeta^2 + ((x(x'-\xi') + \eta_1(y'-\eta'))/n)^2]^{-1/2}$ [@glob-es1992] [@glob-stellarium-sec].
- **The oblate Earth is handled by Bessel's substitution.** Two auxiliary radii $\rho_1 = \sqrt{1 - e^2\cos^2 d}$ and $\rho_2 = \sqrt{1 - e^2\sin^2 d}$ and a rotated declination $d_1$ turn the ellipsoid into a unit sphere in $(\xi, \eta_1, \zeta_1)$ coordinates. Some codes skip this and intersect a line with the ellipsoid directly by solving a quadratic [@glob-es1961] [@glob-enrique7mc].
- **The constants decide the edges.** All NASA products use $k = 0.272281$ for umbral contacts, a solar radius of 959.63 arcseconds at 1 au, and a published $\Delta T$ per eclipse. For penumbral contacts the bulletins and EclipseWise use $k = 0.2725076$, while the Five Millennium Canon and the path tables and element pages generated from it use $k = 0.2724880$. Stellarium copies the bulletin pair. The Swiss Ephemeris uses its own vector method with a lunar diameter of 3476.3 km [@glob-nasa-tp2001] [@glob-stellarium-sec] [@glob-swisseph-swecl].
- **Smooth-Moon limits are wrong by 1 to 3 km.** NASA, Jubier and SVS all say so. SVS (Ernie Wright) replaces the ellipse with a limb-profiled polygon built from LRO LOLA and SLDEM2015 with SRTM terrain, and reports 2017 umbra shifts of up to 3 km from observer elevation alone [@glob-svs-4517] [@glob-nasa-google-2024].
:::

**The question.** Given the Besselian elements of a solar eclipse as polynomials in time, how are the curves that go on a world map computed: the central line, the northern and southern limits of the umbra or antumbra and of the penumbra, the outline of the shadow at an instant, the duration of totality or annularity, the path width, the instant and point of greatest eclipse, the point of greatest duration, the ground speed of the umbra, and the true shape of the umbra on the ground? Which formulas do the Explanatory Supplement, Chauvenet, Meeus and Espenak use, what constants do they adopt, how is the oblate Earth treated, and what do the implementations that add lunar limb and terrain corrections do differently?

## The frame and the elements

Every source here works in Bessel's [?fundamental-plane], with lengths in units of the Earth's equatorial radius and the [?besselian-elements] $x, y, d, \mu, l_1, l_2, \tan f_1, \tan f_2$ as the only input. The geometry, the sign conventions, the cone equations and the constants behind those eight numbers are in [Besselian elements and the fundamental plane](../01-foundations/besselian-elements.md), and are used here without re-derivation [@glob-es1961] [@glob-eclipsewise-beselm].

Two details are needed below. The 1961 Supplement tabulates the numerators of $\sin f_1$ and $\sin f_2$ as constants for each lunar radius ratio: 0.0046640 09 and 0.0046407 92 when $k = 0.272281$, and 0.0046640 18 and 0.0046407 83 when $k = 0.2724880$, both from 1968 [@glob-es1961]. And $l_2$ is negative for a total eclipse, positive for an annular one, while $l_1$ is always positive [@glob-es1961].

Stellarium computes the elements at run time with a Sun/Earth radius ratio of 109.12278, from 696,000 km over 6378.1366 km, the latter from IERS Conventions 2003, and uses $k = 0.2725076$ for the penumbra and the code constant `s` $= 0.272281$ for the umbra, commenting that the 696,000 km value is "calculated from arctan of IAU 1976 solar radius (959.63 arcsec at 1 au)" [@glob-stellarium-sec].

NASA's bulletins publish the elements as cubic polynomials in $t = t_1 - t_0$, in decimal hours from the hour $t_0$ nearest greatest eclipse in [?tt|Terrestrial Dynamical Time]. The form is $a = a_0 + a_1 t + a_2 t^2 + a_3 t^3$ for $a \in \{x, y, d, l_1, l_2, \mu\}$, fitted by least squares to elements "rigorously calculated at five separate times over a six hour period centered at $t_0$", so the fit is valid for $t_0 \pm 3$ h [@glob-nasa-tp2001] [@glob-nasa-tp2008-sec1]. TDT, TD and TT are one scale, and ET is the pre-1984 name for it. $\tan f_1$ and $\tan f_2$ are given as constants for the eclipse.

The ephemeris differs by product. The 2001 bulletin used DE200/LE200. The 2017 pages state JPL DE405 with $\Delta T = 68.4$ s and the 2024 pages VSOP87 and ELP2000-85 with $\Delta T = 70.6$ s [@glob-nasa-tp2001] [@glob-nasa-path-2017] [@glob-nasa-path-2024]. The Five Millennium Canon, NASA/TP-2006-214141, uses VSOP87D and ELP-2000/82 truncated at 0.0005 arcseconds, with centre-of-mass lunar positions and no centre-of-figure offset [@glob-5mcse-text]. NASA labels its 2024 element page "VSOP87/ELP2000-85", while the Canon text describes ELP-2000/82, so the two labels belong to different runs.

## The observer and the oblate Earth

An observer at west longitude $\lambda$, geocentric latitude $\phi'$ and geocentric distance $\rho$ has coordinates in the fundamental frame

$$\xi = \rho\cos\phi'\sin\theta, \quad \eta = \rho\sin\phi'\cos d - \rho\cos\phi'\sin d\cos\theta, \quad \zeta = \rho\sin\phi'\sin d + \rho\cos\phi'\cos d\cos\theta$$

with $\theta = \mu - \lambda$ the local hour angle of the shadow axis [@glob-es1961]. Their hourly rates, with $\mu'$ and $d'$ in radians per hour, are

$$\xi' = \mu'(-\eta\sin d + \zeta\cos d), \qquad \eta' = \mu'\xi\sin d - d'\zeta, \qquad \zeta' = -\mu'\xi\cos d + d'\eta$$

The [?rho-sin-phi] pair for geodetic latitude $\phi$ is

$$\rho\sin\phi' = \frac{(1-e^2)\sin\phi}{\sqrt{1 - e^2\sin^2\phi}} = S\sin\phi, \qquad \rho\cos\phi' = \frac{\cos\phi}{\sqrt{1 - e^2\sin^2\phi}} = C\cos\phi$$

The 1961 edition uses Hayford's spheroid, $e^2 = 0.00672267$, flattening 1/297, and notes $e^2 = 0.00669454$ from 1968 [@glob-es1961]. Modern codes use WGS84: Eclipse-Engine hard-codes $F = 1/298.257223563$, the 2027 visualiser $1/298.257$, and Stellarium takes the flattening from its Earth model [@glob-rherale] [@glob-enrique7mc] [@glob-stellarium-sec].

The difficulty for global curves is that $\rho$ depends on the latitude of a point that has not yet been found. Bessel's substitution removes the iteration. Introduce the [?parametric-latitude] $\phi_1$ with $\sin\phi_1 = \rho\sin\phi'/\sqrt{1-e^2}$ and $\cos\phi_1 = \rho\cos\phi'$, and the auxiliary quantities

$$\rho_1 = \sqrt{1 - e^2\cos^2 d}, \qquad \rho_2 = \sqrt{1 - e^2\sin^2 d}$$
$$\rho_1\sin d_1 = \sin d, \quad \rho_1\cos d_1 = \sqrt{1-e^2}\cos d, \quad \rho_1\rho_2\sin(d_1 - d_2) = e^2\sin d\cos d, \quad \rho_1\rho_2\cos(d_1 - d_2) = \sqrt{1-e^2}$$

Then with $\eta_1 = \eta/\rho_1$ and $\zeta_1 = \zeta/\rho_2$ the observer satisfies

$$\xi = \cos\phi_1\sin\theta, \quad \eta_1 = \sin\phi_1\cos d_1 - \cos\phi_1\sin d_1\cos\theta, \quad \zeta_1 = \sin\phi_1\sin d_1 + \cos\phi_1\cos d_1\cos\theta$$

so that $\xi^2 + \eta_1^2 + \zeta_1^2 = 1$: the ellipsoid has become a unit sphere. The true height above the plane is recovered from

$$\zeta = \rho_2\left[\zeta_1\cos(d_1 - d_2) - \eta_1\sin(d_1 - d_2)\right]$$

The Supplement notes that $\rho_1$, $\rho_2$ and $d_1 - d_2$ are nearly constant over an eclipse and can be evaluated once for the hour nearest conjunction [@glob-es1961]. The inverse transformation to geographic coordinates is

$$\cos\phi_1\sin\theta = \xi, \quad \cos\phi_1\cos\theta = -\eta_1\sin d_1 + \zeta_1\cos d_1, \quad \sin\phi_1 = \eta_1\cos d_1 + \zeta_1\sin d_1$$
$$\lambda = \mu - \theta, \qquad \tan\phi = \frac{\tan\phi_1}{\sqrt{1-e^2}}$$

with $(1-e^2)^{-1/2} = 1.003378$ for Hayford and 1.003364 from 1968 [@glob-es1961]. Stellarium's `computeTimePoint` and `calcSolarEclipseData` implement exactly these lines: `rho1 = sqrt(1-e2*sqr(cosd))`, `sd1 = sind/rho1`, `cd1 = sqrt(1-e2)*cosd/rho1`, `sdd = e2*sind*cosd/(rho1*rho2)`, `zeta1 = (zeta/rho2 + eta1*sdd)/cdd`, `theta = atan2(xi, -eta1*sd1 + zeta1*cd1)`, `lng = theta - mu`, `tanLat = sfn1/((1-f)*cfn1)` [@glob-stellarium-sec].

A second treatment avoids the substitution. The 2027 visualiser expresses the fundamental-plane basis vectors in Earth-fixed coordinates, $\hat\xi = (\sin\mu, \cos\mu, 0)$, $\hat\eta = (-\sin d\cos\mu, \sin d\sin\mu, \cos d)$, $\hat\zeta = (\cos d\cos\mu, -\cos d\sin\mu, \sin d)$, and intersects the line $\mathbf{a} + \zeta\hat\zeta$ with the ellipsoid by solving the quadratic $g(\hat\zeta,\hat\zeta)\zeta^2 + 2g(\mathbf{a},\hat\zeta)\zeta + g(\mathbf{a},\mathbf{a}) - 1 = 0$ where $g$ is the ellipsoid metric with $z$ scaled by $1/(1-f)^2$, and takes the root nearest the Moon [@glob-enrique7mc]. The Swiss Ephemeris does the same in a cruder way: it divides the $z$ coordinates of Sun and Moon by $(1 - f)$, computes the intersection as if the Earth were a sphere, then recomputes the scale factor from the latitude found and repeats once [@glob-swisseph-swecl]. Both are algebraically equivalent to Bessel's substitution for a point on the surface. They differ when an observer height must be included. That case is discussed below.

The time system is ephemeris time (now TT) throughout the Supplement, and the map curves are converted to Universal Time only through $\Delta T$ [@glob-es1961]. In practice the hour angle $\mu$ tabulated against TT is shifted by the rotation of the Earth in $\Delta T$ seconds: the 2027 visualiser evaluates `mu = poly(E.mu, t) - 0.00417807 * deltaT` degrees, and Eclipse-Engine uses `1.002738 * delta_t_s * 15 / 3600` degrees, both 15.041 arcseconds of longitude per second of $\Delta T$ [@glob-enrique7mc] [@glob-rherale]. Omitting it leaves latitude right and shifts longitude by about 32 km for $\Delta T = 76$ s at the latitude of Egypt [@glob-aravpanwar]. NASA's page on Earth rotation tabulates the same effect for historical eclipses, for example 9,848 s of $\Delta T$ at 1 BCE giving a 41.0 degree longitude shift [@glob-nasa-rotation].

## Central line

The [?central-line] is the locus where the shadow axis meets the surface. At each time,

$$\xi = x, \qquad \eta_1 = y/\rho_1, \qquad \zeta_1 = \sqrt{1 - x^2 - \eta_1^2}$$

There are two roots. The negative $\zeta_1$ is the point below the horizon and is "usually omitted in the ephemerides" [@glob-es1961]. Where $1 - x^2 - \eta_1^2 < 0$ the axis misses the Earth: the eclipse is non-central at that instant. The 1992 edition writes the same three lines as its equation 8.3553-1 and adds $\zeta = \rho_2[\zeta_1\cos(d_1-d_2) - \eta_1\sin(d_1-d_2)]$ as 8.3553-2 [@glob-es1992]. Stellarium's `calcSolarEclipseData` tests `p = 1 - x*x - eta1*eta1` and takes the partial-eclipse branch when it is negative, in which case it computes the point on the limb closest to the axis by normalising $(x, y/\rho_1)$ [@glob-stellarium-sec].

The ends of the central line are the first and last contacts of the umbra, where $\zeta_1 = 0$ and $x^2 + \eta_1^2 = 1$. The Supplement finds the time by Newton's correction $t = -(xx' + yy')/n_1^2$ with $n_1^2 = x'^2 + y'^2$ at an approximate time, and the 1992 edition uses the discriminant $D = x^2 + y_1^2 - 1$ with inverse interpolation [@glob-es1961] [@glob-es1992].

## Duration on the central line

The 1961 Supplement gives the semi-duration of the total or annular phase as

$$s = \frac{L_2}{n}, \qquad L_2 = l_2 - \zeta\tan f_2, \qquad n^2 = (x' - \xi')^2 + (y' - \eta')^2$$

with $\xi' = \mu'(-y\sin d + \zeta\cos d)$ and $\eta' = \mu' x\sin d - d'\zeta$ evaluated at the central-line point. The units are hours when hourly variations are used [@glob-es1961]. The 1992 edition gives the full duration as $2L_2/n$ "with appropriate sign" and remarks that this disregards vertical motion, and that in local circumstances the accurate duration is the difference of the two contact times [@glob-es1992]. Stellarium writes `duration = L2a*120./n` minutes with $n$ in Earth radii per hour and the sign distinguishing annular (positive) from total (negative) [@glob-stellarium-sec]. The 2027 visualiser instead bisects the two times at which the fixed surface point crosses the umbra edge, $|(\xi - x, \eta - y)| = |l_2 - \zeta\tan f_2|$. That is the local-circumstance definition of duration [@glob-enrique7mc].

Off the central line the NASA bulletins give the interpolation

$$d = D\sqrt{1 - (2a/W)^2}$$

with $D$ the central duration, $a$ the perpendicular distance from the central line and $W$ the path width, all in seconds and kilometres, together with $t_2 = t_m - d/2$ and $t_3 = t_m + d/2$ [@glob-nasa-tp2001].

## Northern and southern limits

![A limit is the envelope of the moving umbra. Every point on it is touched by the shadow's edge at one instant only, which is why the condition solved for it is that the eclipse begins and ends at the same moment, and not a separate curve fitted to the map.](img/path-and-limits.svg)

At a point on a limit the eclipse begins and ends at the same instant, so the distance $\Delta$ from the observer to the axis equals the shadow radius $L$ and its time derivative vanishes. Writing $x - \xi = \Delta\sin Q$, $y - \eta = \Delta\cos Q$ with $Q$ the [?position-angle-q] of the axis from the observer, the condition is

$$(x' - \xi')\sin Q + (y' - \eta')\cos Q - (l' - \zeta'\tan f) = 0$$

The Supplement introduces the [?auxiliary-elements]

$$a' = -l' - \mu' x\tan f\cos d, \qquad b' = -y' + \mu' x\sin d, \qquad c' = x' + \mu' y\sin d + \mu' l\tan f\cos d$$

and, omitting terms in $d'\tan f$ and setting $\sec^2 f = 1$, obtains

$$\tan Q = \frac{b' - \zeta d' - a'\sec Q}{c' - \zeta\mu'\cos d}$$

For the umbra, $\xi = x - L_2\sin Q$ and $\eta_1 = (y - L_2\cos Q)/\rho_1$. The sign of $\cos Q$ is positive for the northern limit of a total eclipse and the southern limit of an annular eclipse, negative for the other two [@glob-es1961]. The 1992 edition writes the same condition with the $\tan^2 f$ factor kept, its equation 8.353-2,

$$a_i - b_i\cos Q + c_i\sin Q + \zeta(1 + \tan^2 f_i)(d'\cos Q - \mu'\cos d\sin Q) = 0, \qquad i = 1, 2$$

with dots on $a$, $b$, $c$ that the scan dropped, and assigns a converged point to the northern limit when $L_i\cos Q < 0$ and to the southern when $L_i\cos Q > 0$ [@glob-es1992]. The 2013 edition's equation 11.81 is the same relation solved for $\zeta$, which Stellarium implements as

$$\zeta = \frac{-\dot a + \dot b\cos Q - \dot c\sin Q}{(1 + \tan^2 f)(\dot d\cos Q - \dot\mu\cos d\sin Q)}$$

with $\dot a = -\dot l - \dot\mu x\tan f\cos d + y\dot d\tan f$, $\dot b = -(\dot y - \dot\mu x\sin d)$ and $\dot c = \dot x + \dot\mu y\sin d + \dot\mu L\tan f\cos d$ [@glob-stellarium-sec] [@glob-es2013]. Note the extra $y\dot d\tan f$ term that 1961 dropped. Chauvenet's original, reproduced in Buchanan's 1904 exposition, is the same condition in logarithmic form: $\tan(Q - \tfrac{1}{2}E) = \tan(45^{\circ} + v')\tan\tfrac{1}{2}E$ with $\tan v' = (f/e)\cos\beta$, where $e$, $E$ and $f$ are Chauvenet's auxiliaries and $\cos\beta$ is taken from the central line because it "is not known" on the limit curve, which Buchanan admits makes the umbral formulae "not rigorously exact" near the ends [@glob-buchanan-1904].

The iteration in the 1961 Supplement is:

1. Start with $L_2$ from the central-line duration computation at the same time and $\tan Q_0 = b'/(c_2' - \zeta\mu'\cos d)$ from the same computation. If there is no central line, start with $\zeta = 0$, $L_2 = l_2$, $\tan Q = b'/c_2'$.
2. Compute $\xi$, $\eta_1$, then $\zeta_1 = \sqrt{1 - \xi^2 - \eta_1^2}$ and $\zeta = \rho_2[\zeta_1\cos(d_1-d_2) - \eta_1\sin(d_1-d_2)]$.
3. Recompute $\tan Q$ from the accurate formula, using $\sec Q$ from the previous approximation because the $a'\sec Q$ term is small.
4. Re-evaluate $L_2 = l_2 - \zeta\tan f_2$, $\xi$, $\eta_1$, $\zeta_1$ and convert to $\lambda$, $\phi$.

The procedure "converges rapidly and rarely requires more than two approximations", but "near the ends of the path it may be advisable to carry through one more approximation" [@glob-es1961]. The 1992 edition scans $Q$ a degree at a time from a first guess with $a_i = 0$ until the discriminant changes sign twice, inverse-interpolates each zero, then iterates $\zeta$ to $10^{-5}$ Earth radii, and, where the iteration "may begin oscillating about some mean value", takes the mean [@glob-es1992].

For the penumbral limits the flattening may be neglected: $L_1 = l_1 - \zeta\tan f_1$, $\xi = x - L_1\sin Q$, $\eta = y - L_1\cos Q$, $\zeta = \sqrt{1 - \xi^2 - \eta^2}$, $\tan Q = b'/(c_1' - \zeta\mu'\cos d)$ with the $\zeta d'$ and $a'\sec Q$ terms omitted, and the sign of $\cos Q$ positive for the southern limit and negative for the northern [@glob-es1961]. The penumbra "often has only one" limit on the surface, the umbra "nearly always has both" [@glob-es1992].

Stellarium takes a different route to the same condition. Its `getShadowLimitQs` substitutes $\zeta(Q)$ from the 2013 equation 11.81 into the unit-sphere identity $\xi^2 + \eta_1^2 + \zeta_1^2 = 1$ and the $\zeta$ relation 11.60, multiplies through, and obtains a single polynomial in $\sin Q$ and $\cos Q$ whose coefficients the source lists term by term. It solves that with Newton's method over the full circle, keeps only sets with an even number of roots, samples every minute from P1 to P4, and bisects in time wherever the number of roots changes or $\zeta$ changes sign, dropping points with negative $\zeta$ as below the horizon [@glob-stellarium-sec].

Two open-source engines replace the derivative condition with a geometric one. The 2027 visualiser computes the ground velocity of the shadow centre, $\mathbf{v} = \omega\hat z \times \mathbf{P}$ projected on the $\xi$ and $\eta$ axes, forms the direction of travel relative to the ground $Q_{dir} = \operatorname{atan2}(\dot x - v_\xi, \dot y - v_\eta)$, and places the two limits at $Q_{dir} \pm 90^{\circ}$, iterating four times on $L = |l_2 - \zeta\tan f_2|$ [@glob-enrique7mc]. Eclipse-Engine does the same with five iterations and records why the ground-relative velocity matters: "the observer's own eastward speed is a few hundred m/s against an umbra doing a few km/s. Ignoring it narrows the drawn band by up to 5 km on each side at low latitude", a 4 per cent error on a 130 km half-width. It also returns the two curves as left and right of the motion instead of north and south, because the labels swap at "some 170 of 6200 sampled epochs" in its catalogue [@glob-rherale]. This perpendicular-offset construction is the small-$l'$, small-$d'$ limit of the Supplement's condition and is the reason NASA's bulletins describe the limits as tangent to the path of the shadow.

## Outline of the shadow at an instant

An [?outline-curve] is the locus of points where the eclipse is beginning or ending at the given time. Neglecting flattening and using $l_1$ for $L_1$,

$$\xi = x - l_1\sin Q, \qquad \eta = y - l_1\cos Q, \qquad \xi^2 + \eta^2 + \zeta^2 = 1$$

with $Q$ as the independent variable at 5 or 10 degree steps. If the penumbra has both limits on the surface, $Q$ runs through the full circle. Otherwise the end points are where $\zeta = 0$: with $x = m\sin M$, $y = m\cos M$,

$$\cos(Q - M) = \frac{m^2 + l_1^2 - 1}{2 m l_1}$$

and the two roots bound the visible arc; which arc is found by testing a trial $Q$. For a large-scale map the flattening is restored, $\xi = x - L_1\sin Q$, $\eta_1 = (y - L_1\cos Q)/\rho_1$, $\zeta_1 = \sqrt{1 - \xi^2 - \eta_1^2}$, iterating $L_1 = l_1 - \zeta\tan f_1$ from the spherical value [@glob-es1961]. The 1992 edition uses one-degree steps in $Q$ and points already computed on the limit curves as the end points [@glob-es1992]. The umbral outline is the same with $l_2$, $f_2$, and the Supplement notes that outline curves of the umbra "are not published" in the Almanac [@glob-es1992].

Stellarium's `getShadowOutlineCoordinates` runs three fixed iterations of $L = l - \zeta_1\tan f$ for each of 60 angles and returns nothing where $1 - \xi^2 - \eta_1^2 < 0$ [@glob-stellarium-sec]. The 2027 visualiser uses 90 angles and four iterations and, where the cone misses the Earth, substitutes the point on the terminator in that direction so the polygon stays closed [@glob-enrique7mc]. Eclipse-Engine uses 181 angles, iterates to convergence instead of a fixed count because "at grazing incidence the radius depends ever more steeply on zeta and four rounds leave the vertex kilometres out", and breaks the ring into runs where the cone leaves the ground [@glob-rherale].

## Path width

The 1992 Supplement gives the width perpendicular to the direction of motion by "a formula derived by Mikhailov (1931)", its equation 8.3553-5, which the scan garbled. Stellarium's transcription of it reads

$$W = \left|\, 2 R_\oplus L_2 \left[\zeta^2 + \left(\frac{x(x' - \xi') + \eta_1(y' - \eta')}{n}\right)^2\right]^{-1/2}\right|$$

with `p1 = zeta*zeta`, `p2 = x*(xdot-xidot)/n`, `p3 = eta1*(ydot-etadot)/n`, `pathWidth = abs(earthRadius*2.*L2a/sqrt(p1+(p2+p3)*(p2+p3)))` [@glob-es1992] [@glob-stellarium-sec]. The term in the bracket is the cosine of the angle between the surface normal and the direction of motion resolved on the fundamental plane. When the motion is along the tilt of the surface the width is $2L_2$, and when the motion is across the tilt it is $2L_2/\zeta$. Stellarium's comment warns that the formula "could give a false impression" where only part of the umbra touches the Earth, citing the 2003 May 31 annular eclipse, and that width should not be shown unless both limits exist [@glob-stellarium-sec]. NASA's path tables give width in kilometres at the central-line point together with the umbra's major and minor axes and its "instantaneous velocity with respect to Earth's surface" in the physical-ephemeris table [@glob-nasa-tp2001]. A simple cone-geometry approximation, $W = 2(d_{umbra} - (d_{moon} - r_\oplus))\tan\alpha$ with $\alpha = \arcsin((r_\odot - r_{moon})/(d_\odot - d_{moon}))$, reproduces the 2017 NASA value of 114.7 km as 116 km but ignores the surface tilt [@glob-mathscinotes].

## Ground speed of the umbra

No source read here prints a formula for the speed of the umbra over the ground. The Supplement's $n$ is the speed of the shadow relative to the observer in the plane through the observer parallel to the fundamental plane [@glob-es1961]. NASA bulletins tabulate the velocity and describe it in the narrative: 0.554 km/s at greatest eclipse in 2001, 0.63 km/s at the Angolan coast and 1.7 km/s leaving Mozambique [@glob-nasa-tp2001]. Jubier's map reports "Umbral/Antumbral velocity" in its tooltip [@glob-jubier-help]. A geometric derivation, given here because it is not quoted from any source, follows from the same projection as Mikhailov's width. A lateral displacement $\boldsymbol\delta$ of the axis in the fundamental plane moves the surface intersection by $\boldsymbol\delta_s = \boldsymbol\delta - \hat z\,(\boldsymbol\delta\cdot\mathbf{N})/(\hat z\cdot\mathbf{N})$, where $\mathbf{N}$ is the surface normal, so that

$$v_{ground} = n R_\oplus\sqrt{1 + \frac{(\hat v\cdot\mathbf{N})^2}{\zeta^2}}$$

with $\hat v$ the unit direction of $(x' - \xi', y' - \eta')$ and $\hat z\cdot\mathbf{N} = \zeta$ for a sphere. This is why the shadow speed rises without bound toward the ends of the path where $\zeta \to 0$, and why the satellite-derived 2017 estimates of 2,382 to 2,929 km/h over Wyoming and Nebraska sit close to $n R_\oplus$ where the Sun was high [@glob-helioclipse].

## Greatest eclipse and greatest duration

The [?greatest-eclipse] is the instant when the shadow axis passes closest to the centre of the Earth. The Supplement minimises $m^2 = x^2 + y^2$: at an approximate time $T$ the correction is $t = -(xx' + yy')/n_1^2$ with $n_1^2 = x'^2 + y'^2$, and the 1992 edition uses the discriminant $xx' + yy' = 0$ [@glob-es1961] [@glob-es1992]. For a partial eclipse the point of greatest magnitude is on the terminator, $\zeta = 0$, at $\xi = x/m$, $\eta_1 = y_1/m_1$, with distance to the axis $\Delta = m - \rho$ and magnitude $(l_1 - \Delta)/(l_1 + l_2)$, where $l_1 + l_2$ may be replaced by $2l_1 - 0.5459$ (0.5464 from 1963) when $l_2$ is unavailable [@glob-es1961]. The 2001 bulletin defines greatest eclipse the same way and adds that it "differs slightly from the instants of greatest magnitude and greatest duration (for total eclipses)", and that "the differences are usually quite small" [@glob-nasa-tp2001]. NASA's map key marks the point with an asterisk and the minimum distance as [?gamma] [@glob-nasa-mapkey].

The point of [?greatest-duration] has no closed formula in any source read. It is the maximum of $2L_2(t)/n(t)$ along the central line, which trades the growth of $|L_2|$ toward the subsolar point against the growth of $n$ where the Earth's rotation contributes least. The `besselian` repository reports that for 2027 August 2 the two points differ by about 215 km and 0.6 s, and that its "exact centerline solve" dominates a seven-minute build [@glob-aravpanwar]. The NASA Google map for 2024 states that limb corrections "shift the exact location of Greatest Duration by ~10-20 kilometers" [@glob-nasa-google-2024].

## Observer height, terrain and the ends of the path

The Supplement's formulas put every point on the spheroid. Height enters only through $\rho$, which the 1992 edition says "is usually not unity; it contains flattening and height above the geoid" [@glob-es1992]. NASA's bulletins handle height in the graze-zone tables with a multiplicative "Elev Fact": the path must be shifted perpendicular to itself by the elevation times the factor, so an observer at 1000 m with a factor of +0.20 shifts the limit by 200 m northward [@glob-nasa-tp2001]. The 2008 bulletin states the factor as $\tan(90^{\circ} - A)\sin D$ with $A$ the Sun's altitude and $D$ the difference between the Sun's azimuth and the azimuth of the limit line [@glob-nasa-tp2008-sec1]. The Photographer's Ephemeris (Photo Ephemeris) quotes the same rule of thumb as "of the order of ~500 m per 1,000 m of elevation" and computes its paths "for an observer at sea level" at 0.1 degree longitude steps [@glob-photoephemeris]. NASA's local-circumstance tables use a location's elevation when known and otherwise sea level, and say elevation "does not play a significant role in the predictions unless the location is near the umbral path limits and the Sun's altitude is relatively small (<10°)" [@glob-nasa-tp2001].

The direct line–ellipsoid approach handles height naturally: the 2027 visualiser's `surfacePoint` intersects the axis with an ellipsoid of any semi-axes, and its local circumstances accept an observer above the surface [@glob-enrique7mc]. Ernie Wright's SVS method goes further and takes observer elevations from SRTM at every pixel, so that "higher elevations can lift the observer either into or out of the umbra cone. The overall effect is to shift the umbra toward the Sun", by up to 3 km to the southeast in the western United States in 2017 [@glob-svs-4517].

At the ends of the path all the formulas degrade. The central line ends where $\zeta_1 = 0$, the limit iteration needs an extra pass, the limit curves continue past the end of the central line to the extreme points where $\xi = x - l_2\sin Q$, $\eta_1 = (y - l_2\cos Q)/\rho_1$, $\xi^2 + \eta_1^2 = 1$ and $\tan Q = (b' - a_2'\sec Q)/c_2'$, and the width formula blows up as $\zeta \to 0$ [@glob-es1961] [@glob-es1992]. Chauvenet's umbral-limit formulae have $\cos\beta$ as a divisor and become infinite at the extreme points [@glob-buchanan-1904]. NASA's 2001 bulletin says the time interpolation between lines of maximum eclipse "is valid along most of the path with the exception of the extreme ends, where the shadow experiences its largest acceleration", and that refraction corrections near the horizon "are uncertain since they depend on the atmospheric temperature-pressure profile" [@glob-nasa-tp2001]. SVS notes that its duration and path shapefiles "are truncated and invalid at the ends" [@glob-svs-4518]. The polynomial elements add their own edge problem: the 2026 simulator warns that at "the very edge of the path of totality (where duration → 0)" the cubic fit can shift contact times by tens of seconds against full-ephemeris sources [@glob-sr123].

## The shape of the umbra: ellipse or polygon

On the smooth-Moon model the umbra on the ground is the projection of a circle along the shadow axis onto a tilted surface, an ellipse with semi-axes $|L_2|$ and $|L_2|/\zeta$ in the small-cone limit, and the [?outline-curve] iteration above traces it exactly on the spheroid [@glob-es1961]. NASA's physical-ephemeris tables print the major and minor axes [@glob-nasa-tp2001].

Wright's SVS visualisations replace this with what the 2017 animation calls "an irregular polygon with slightly curved edges. Each edge corresponds to a single valley on the lunar limb, the last (or first) spot on the limb that lets sunlight through." The limb profile is built by transforming each point of a lunar elevation map into body-fixed Cartesian coordinates, rotating the point cloud into fundamental-plane coordinates at each time step, and taking "the set of points lying farthest from the shadow axis" as the limb. The lunar data are LRO laser altimetry and the hybrid LRO/Kaguya (SELENE) SLDEM2015 model. Earth elevations are SRTM. Positions are JPL DE421 on every SVS product page, while the paper's appendix uses DE440. The difference is under a metre at the Moon, and the question is treated in [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md). The 2024 path animation states that "the umbra and its path were calculated in a way that accounts for both elevations on the Earth's surface and the irregular lunar limb" [@glob-svs-5219]. The animation shows three shapes: the red smooth ellipse, the white limb-corrected polygon and the dark grey polygon with Earth terrain added [@glob-svs-4517]. The 2024 follow-up explains the geometry as valleys acting "like pinholes projecting images of the Sun onto the surface of the Earth", the umbra being the hole in the middle of the resulting flower pattern, and reports that in 2017 "only 49 valleys made significant contributions to the umbra shape" [@glob-svs-5366]. The method paper is Wright and Young, "A Raster-oriented Method for Creating Eclipse Maps", Astronomical Journal 168:163 (2024), whose abstract states that ignoring the terrain of both bodies "introduces errors on the order of kilometers in the ground track of the umbra and seconds in the duration and contact times of totality" [@glob-wright-young-2024] [@glob-usra-2024].

NASA's own path tables do not include this. The 2024 Google map page says its data "DO NOT include the effects of mountains and valleys along the edge of the Moon", that such corrections "shift the limits of the eclipse path north or south by ~1-3 kilometers, and change the eclipse duration by ~1-3 seconds", and that limb-corrected predictions "are normally posted 12-18 months before each eclipse" [@glob-nasa-google-2024]. NASA's and EclipseWise's limb pages put the uncorrected timing error at "2 to 3 seconds (and more near the path limits where the geometry is far more critical)", reduced to 0.5 s with Watts data and 0.2 s with Kaguya or LRO data [@glob-nasa-limb] [@glob-eclipsewise-limb]. The bulletins tabulate corrections to the limits as interior and exterior components that define a [?graze-zone] "typically five to ten kilometers wide", computed by "an algorithm which searches the path limits for the extreme positions where no photospheric beads are visible along a ±30° segment of the Moon's limb, symmetric about the extreme contact points at the instant of maximum eclipse", with the exterior boundary "somewhat arbitrarily defined" as where "an unbroken photospheric crescent of 60° in angular extent is visible at maximum eclipse". The limb data were Watts's 1963 charts corrected to a centre-of-mass sphere after Morrison and Appleby (1981), accurate to about 0.3 arcseconds [@glob-nasa-tp2001] [@glob-nasa-tp2008-sec1]. Jubier's maps display a per-location limb correction "LC" in seconds, fetched online, and his Solar Eclipse Maestro compares Watts, Kaguya and LRO profiles against the reduced radius $k_2$ used for the uncorrected path [@glob-jubier-help] [@glob-jubier-sem-limb]. John Irwin's besselianelements.com publishes "true limb" limits for 2024 that account for lunar and terrestrial topography and are drawn for two solar radii, 959.90 and 960.00 arcseconds, around an estimate of $959.95'' \pm 0.05''$; the lines are jagged because the terrain is [@glob-besselianelements-jagged] [@glob-besselianelements-2024].

## Sources compared

| Source | What it gives that the others do not | Constants and data | Grade |
|---|---|---|---|
| Explanatory Supplement 1961, ch. 9 [@glob-es1961] | The complete algebra, worked examples for 1961 Feb 15, the auxiliary elements $a'$, $b'$, $c'$, the two-step iteration for limits, the $Q$-range test for outlines | $k = 0.272274$ then 0.272281 and 0.2724880, $s_\odot = 959''.63$, Hayford $e^2 = 0.00672267$ | peer-reviewed |
| Explanatory Supplement 1992, ch. 8 [@glob-es1992] | The discriminant scan in $Q$, the $10^{-5}$ Earth-radius tolerance, the oscillation rule, Mikhailov's width formula, the flattening iteration in $\gamma$ | Refers to IAU $k$ of 1982 | peer-reviewed |
| Explanatory Supplement 2013, ch. 11 [@glob-es2013] | The $\zeta(Q)$ closed form (eq. 11.81) and rise/set iteration (11.89, 11.94) that Stellarium implements; not read directly | via Stellarium | peer-reviewed |
| Chauvenet 1863 via Buchanan 1904 [@glob-buchanan-1904] | The logarithmic auxiliaries $e$, $E$, $f$, $v$ and the admission that the umbral limits borrow $\cos\beta$ from the central line | pre-IAU | survey |
| Meeus 1989, Elements of Solar Eclipses [@glob-meeus-1989] | Elements for 570 eclipses 1951–2200 with algorithms for central line and limits and numerical checks; not read | ELP/VSOP era, not verified | peer-reviewed |
| NASA bulletins and path tables [@glob-nasa-tp2001] [@glob-nasa-tp2008-sec1] [@glob-nasa-path-2024] | The tabulated product, the graze-zone algorithm, Elev Fact, the off-axis duration interpolation | $k = 0.2725076$ penumbral, 0.272281 umbral, DE200 then VSOP87/ELP2000, $\Delta T$ per eclipse | primary |
| Stellarium [@glob-stellarium-sec] | A complete open implementation with every curve, Newton solve of the limit polynomial, PNG and KML output | 6378.1366 km, 696,000 km, $k$ and $s$ as NASA | company |
| Swiss Ephemeris [@glob-swisseph-swecl] | Vector method without Besselian elements; central point and umbra diameter only, no limits | DMOON 3476.3 km, DSUN 1,392,000 km (or 1,391,978.5 km), Earth 6378.14 km | company |
| SVS / Wright [@glob-svs-4517] [@glob-wright-young-2024] | Raster method with limb polygon and terrain; the only source that publishes the true shape | LRO LOLA, SLDEM2015, SRTM, DE421 | primary, peer-reviewed |
| Open-source JS engines [@glob-enrique7mc] [@glob-rherale] | Line–ellipsoid quadratic, ground-relative sweep for limits, convergence notes | WGS84, $k_2 = 0.272281$, $\Delta T$ from NASA | company, unsourced |

## What a developer should do

1. Implement the 1961 Supplement's equations exactly as quoted above, in the $(\xi, \eta_1, \zeta_1)$ frame, and check against Example 9.6 and 9.7 for 1961 February 15 08h ET ($x = -0.403040$, $y = +0.808354$, $\sin d = -0.220112$, giving $\phi = +44^{\circ} 18'.3$, $\lambda = -29^{\circ} 20'.9$ west, duration 158.6 s) [@glob-es1961]. Read `SolarEclipseComputer.cpp` in Stellarium alongside it. It is the closest thing to a reference implementation with citations [@glob-stellarium-sec].
2. Use the 1992 edition's limit procedure (scan $Q$, inverse-interpolate, iterate $\zeta$ to $10^{-5}$, assign by the sign of $L\cos Q$) rather than the two-pass 1961 recipe when generating whole curves, because it is robust at the ends [@glob-es1992].
3. Adopt NASA's constants when the goal is to reproduce NASA tables: $k_1 = 0.2724880$ for the NASA path tables and catalogue and $0.2725076$ for the bulletins and EclipseWise, $k_2 = 0.272281$ in both cases, solar radius 959.63 arcseconds at 1 au, and the $\Delta T$ printed with each eclipse. Validate against the path table at three times, as the 2027 visualiser does, expecting agreement at 1 km and 0.1 s [@glob-nasa-path-2024] [@glob-enrique7mc].
4. Apply the $\Delta T$ shift to $\mu$ at 15.041 arcseconds per second, not 15.0 [@glob-rherale].
5. Treat limb and terrain corrections as a separate stage, and read Wright and Young 2024 before designing it [@glob-wright-young-2024].

## What this changes

The pipeline's global-circumstances stage should be a single routine that maps $(t, Q, \text{cone})$ to a surface point through the Bessel substitution, with the central line, limits, outlines, rise/set curves and maximum-eclipse curves all expressed as constraints on $Q$ or $\zeta$. The width and duration are by-products of that routine. The smooth-Moon path is a first-order product. The limb-profiled polygon is a distinct product that needs the lunar DEM and a raster or ray method, and the two should never be mixed in one file without labelling.

## Open questions

- The exact text of Explanatory Supplement 2013 equations 11.56, 11.60, 11.65, 11.78, 11.81, 11.82, 11.89 and 11.94, to confirm Stellarium's transcription of the $\zeta(Q)$ formula and the rise/set iteration [@glob-es2013].
- Mikhailov 1931 as cited in the 1992 Supplement for the path-width formula, to verify the scan-damaged equation 8.3553-5 against the Stellarium code [@glob-es1992].
- The full text of Wright and Young 2024 (AJ 168:163), for the solar radius adopted, the limb-point selection criterion and the pixel resolution of the raster [@glob-wright-young-2024].
- Meeus's Elements of Solar Eclipses 1951–2200, for its limit algorithm and the numerical examples that the Photo Ephemeris and MATLAB implementations rely on [@glob-meeus-1989] [@glob-matlab-meeus].
- The NASA source code or a written statement of how the bulletins compute the "instantaneous velocity with respect to Earth's surface" in the physical-ephemeris tables [@glob-nasa-tp2001].
