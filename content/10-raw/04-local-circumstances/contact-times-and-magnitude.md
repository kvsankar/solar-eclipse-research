---
title: Contact times, magnitude and position angles from Besselian elements
description: The Explanatory Supplement reduction from Besselian elements to one observer's contacts, magnitude, obscuration, P and V angles, altitude, azimuth and duration, checked line by line against NASA's JavaScript Solar Eclipse Explorer.
order: 1
status: working
updated: 2026-09-15
tags: [local-circumstances, besselian, contacts, magnitude, obscuration, position-angle]
---

::: summary
- **The whole reduction is eight formulas.** Project the observer onto the [?fundamental-plane] as $(\xi,\eta,\zeta)$ and subtract from the shadow-axis coordinates $(x,y)$ to get $(u,v)$. Shrink the shadow radii to the observer's plane with $L' = L - \zeta\tan f$. Solve $u^2+v^2 = L'^2$ for the contacts and $uu'+vv'=0$ for maximum eclipse. The 1961 Explanatory Supplement gives every one of them [@loc-es1961-local].
- **NASA's JavaScript Solar Eclipse Explorer (JSEX) is that method in 1200 lines of GPL code.** Its `program.js` computes $\rho\sin\phi'$ with $b/a = 0.99664719$ and $a = 6378140$ m, and the hour angle as $\mu - \lambda_W - \Delta T/13713.44$. It iterates each contact with a Newton step until the correction is below $10^{-6}$ h, and reports P, V, altitude, azimuth, magnitude, obscuration and duration [@loc-jsex-program-js].
- **Magnitude has two branches.** In the penumbra it is $(L_1'-m)/(L_1'+L_2')$, the fraction of the solar diameter covered. Inside the umbra or antumbra it is $(L_1'-L_2')/(L_1'+L_2')$, the ratio of the apparent diameters. NASA tables and every code read here switch branches at $m = |L_2'|$ [@loc-es1961-local] [@loc-nasa-locirc-2001].
- **Obscuration is a lens area, never a linear function of magnitude.** With the solar radius as unit and $s$ the lunar radius, $S' = (s^2 A + B - s\sin C)/\pi$ where $A$, $B$, $C$ are the angles of the triangle formed by the two centres and an intersection point [@loc-es1961-local]. A 0.5 magnitude with equal radii hides about 39 per cent of the disc.
- **The position angle $P$ of a contact is $\tan P = u/v$ at the contact instant,** measured eastward from the north point, with the sign of $\sin P$ reversed for the interior contacts of a total eclipse because $L_2 < 0$. The 1961 Supplement writes this angle $Q$. The vertex angle is $V = P - C$ with $\tan C = \xi/\eta$ the parallactic angle [@loc-es1961-local] [@loc-buchanan-1904].
- **The direct numerical alternative needs no auxiliary angles.** Tabulate $u^2+v^2-L^2$ at equal time steps and inverse-interpolate its zero. The 1992 Explanatory Supplement recommends it as simpler and free of the constant-velocity assumption [@loc-es1992-ch8].
- **Nothing in this reduction knows about the lunar limb, refraction or the solar radius choice.** Those enter through the elements ($k$, the solar radius in $L_1$, $L_2$) and through post-corrections described in [corrections-and-code.md](corrections-and-code.md).
:::

**The question.** Given a published set of Besselian elements for one eclipse and an observer's geodetic latitude, longitude and height, what is the exact sequence of formulas for the site? The outputs wanted are the times of the four contacts and of maximum eclipse, the magnitude, the obscuration, the position and vertex angles of each contact, the Sun's altitude and azimuth, and the duration of totality or annularity. Which constants does each formulation fix, and where do the published implementations differ from the almanac text?

## The pipeline for one observer

Given Besselian elements $x, y, d, \mu, L_1, L_2, \tan f_1, \tan f_2$ as polynomials in $t$ about $t_0$ in [?tt], the $\Delta T$ they were computed with, and an observer $(\phi, \lambda, h)$:

1. **Observer constants.** $\rho\sin\phi'$ and $\rho\cos\phi'$ from the geodetic latitude, the spheroid and the height [@loc-es1961-local].
2. **Hour angle.** $\theta = \mu(t) - \lambda - 1.002738\,\Delta T$ with west longitude positive [@loc-es1961-local].
3. **Fundamental-plane position.** $\xi$, $\eta$, $\zeta$ and their rates $\xi'$, $\eta'$ [@loc-es1961-local].
4. **Relative coordinates.** $u = x - \xi$, $v = y - \eta$, their rates, $m$, $n$, and the observer's-plane radii $L_1' = L_1 - \zeta\tan f_1$, $L_2' = L_2 - \zeta\tan f_2$ [@loc-es1961-local].
5. **Maximum eclipse.** Iterate $t \leftarrow t - (uu' + vv')/n^2$ to convergence [@loc-jsex-program-js].
6. **Eclipse type at the site.** None if $m \ge L_1'$. Partial if $m < L_1'$. Central if $m < |L_2'|$, total when $L_2' < 0$ and annular when $L_2' > 0$ [@loc-jsex-program-js].
7. **Contacts.** Roots of $m(t) = L_1'(t)$ for C1 and C4 and of $m(t) = |L_2'(t)|$ for C2 and C3, by the auxiliary-angle Newton step $t \leftarrow t - D/n^2 \pm L'\cos\psi/n$ or by bracketing and inverse interpolation [@loc-es1961-local] [@loc-es1992-ch8].
8. **Magnitude.** $(L_1' - m)/(L_1' + L_2')$ in the penumbra, $(L_1' - L_2')/(L_1' + L_2')$ inside the umbra or antumbra [@loc-es1961-local] [@loc-nasa-locirc-2001].
9. **Obscuration.** Lens area with $s = (L_1' - L_2')/(L_1' + L_2')$, $S' = (s^2A + B - s\sin C)/\pi$, or $s^2$ for annular and 1 for total [@loc-es1961-local].
10. **Position angles.** At each contact $P = \text{atan2}(u, v)$ with the sign reversed for the interior contacts of a total eclipse, and $V = P - C$ with $\tan C = \xi/\eta$ [@loc-es1961-local].
11. **Altitude and azimuth** from $d$, $\theta$, $\phi$. Flag or replace contacts below the horizon by sunrise or sunset [@loc-jsex-program-js].
12. **Duration** $t_{C3} - t_{C2}$, and **UT** by subtracting $\Delta T$ from every time [@loc-es1961-local].
13. **Corrections**, reported separately: solar radius, limb profile at C2 and C3, current $\Delta T$, height, refraction flag. Their sizes are in [corrections and code](corrections-and-code.md) [@loc-nasa-limb-help].

The rest of this note is those steps with their symbols, constants and the JSEX code.

![Every symbol in the reduction is a length in one of two planes. The observer's height ζ above the fundamental plane fixes how far the two shadow radii shrink, and the in-plane difference $(u, v)$ between the observer and the shadow axis fixes everything else.](img/observer-reduction.svg)

## The observer on the fundamental plane

### Geocentric coordinates of the site

The 1961 Explanatory Supplement, section 9D, starts from the geodetic latitude $\phi$, the longitude $\lambda$ and the height $H$ above the spheroid [@loc-es1961-local]:

$$\rho\sin\phi' = (S + H)\sin\phi, \qquad \rho\cos\phi' = (C + H)\cos\phi,$$

$$C = (1 - e^2\sin^2\phi)^{-1/2}, \qquad S = (1 - e^2)\,C.$$

Here $\rho$ is the geocentric distance in units of the Earth's equatorial radius and $\phi'$ is the geocentric latitude. The 1961 text uses $e^2 = 0.00672267$ and converts height in metres to Earth radii with the factor $0.1567794\times10^{-6}$, that is the Hayford radius 6378388 m. A footnote replaces both from 1968 with $e^2 = 0.00669454$ and $0.1567850\times10^{-6}$ per metre, the IAU 1964 radius 6378160 m [@loc-es1961-local]. The choice of spheroid moves $\rho\sin\phi'$ by parts in $10^{5}$, which is below the level at which contact times change by a tenth of a second.

The NASA JavaScript Solar Eclipse Explorer uses the reduced-latitude form instead, in `readform()` [@loc-jsex-program-js]:

```
tmp = Math.atan(0.99664719*Math.tan(obsvconst[0]))
obsvconst[4] = 0.99664719*Math.sin(tmp) + (obsvconst[2]/6378140.0)*Math.sin(obsvconst[0])
obsvconst[5] = Math.cos(tmp) + (obsvconst[2]/6378140.0*Math.cos(obsvconst[0]))
```

so that with $u = \arctan(0.99664719\tan\phi)$ and $h$ the height in metres,

$$\rho\sin\phi' = 0.99664719\sin u + \frac{h}{6378140}\sin\phi, \qquad \rho\cos\phi' = \cos u + \frac{h}{6378140}\cos\phi.$$

The constant $0.99664719 = 1 - 1/298.257$ is the IAU 1976 polar-to-equatorial ratio and 6378140 m the IAU 1976 equatorial radius. Both forms are the same ellipsoid geometry. Height enters along the local normal in both. The Eclipse-Engine code uses the $C$ and $S$ form with $N = 1/\sqrt{1-e^2\sin^2\phi}$ and a 6378.1366 km radius [@loc-eclipse-engine]. Stellarium takes the rectangular geocentric coordinates of the site from its own Earth model and divides by the equatorial radius [@loc-stellarium-astrocalc].

### Hour angle, longitude and $\Delta T$

Besselian elements are tabulated against Terrestrial (formerly Ephemeris) Time, and $\mu$ is the Greenwich hour angle of the shadow axis at that time scale. The observer's longitude is a Universal Time quantity, so the Supplement converts it to an [?ephemeris-longitude]: "The longitude $\lambda$ must be converted to the ephemeris longitude $\lambda^*$ by increasing it by $1.002738\,\Delta T$, the sidereal equivalent of $\Delta T$" [@loc-es1961-local]. The local hour angle of the axis is then

$$\theta = \mu - \lambda - 1.002738\,\Delta T,$$

with west longitude positive and $\Delta T$ expressed as an angle at 15 arcseconds per second.

The JSEX code is the same statement in radians per second [@loc-jsex-program-js]:

```
circumstances[16] = circumstances[7] - obsvconst[1] - (elements[index+5] / 13713.44)
```

where `elements[index+5]` is $\Delta T$ in seconds from the element table and $13713.44 = 1/(1.002738 \times 15'' \text{ in radians})$, that is one over $7.2921\times10^{-5}$ rad s$^{-1}$. Eclipse-Engine writes the same term as `1.002738 * delta_t_s * 15 / 3600 * D2R` [@loc-eclipse-engine]. Stellarium omits the term because it evaluates $\mu$ from Greenwich apparent sidereal time at the UT of the requested instant, so $\Delta T$ is already inside its elements [@loc-stellarium-astrocalc]. The JSEX element files carry $\Delta T$ per eclipse. Each eclipse is 28 numbers: the JD and hour of $t_0$ in TDT, the validity window, $\Delta T$ in seconds, then the polynomial coefficients of $x$ and $y$ (cubic), $d$, $\mu$, $L_1$ and $L_2$ (quadratic), and $\tan f_1$ and $\tan f_2$ [@loc-jsex-data-2001].

### The coordinates $\xi$, $\eta$, $\zeta$ and their hourly variations

With $d$ the declination of the shadow axis [@loc-es1961-local]:

$$\xi = \rho\cos\phi'\sin\theta,$$
$$\eta = \rho\sin\phi'\cos d - \rho\cos\phi'\sin d\cos\theta,$$
$$\zeta = \rho\sin\phi'\sin d + \rho\cos\phi'\cos d\cos\theta,$$

and the hourly variations, with $\mu'$ and $d'$ the hourly rates of $\mu$ and $d$ in radians:

$$\xi' = \mu'\,\rho\cos\phi'\cos\theta, \qquad \eta' = \mu'\,\xi\sin d - \zeta\,d', \qquad \zeta' = -\mu'\,\xi\cos d + \eta\,d'.$$

The Supplement adds that "$\zeta'$ is not needed" in most cases and that "if predictions to the nearest second are acceptable, the terms $\zeta d'$ and $\eta d'$ may be omitted" [@loc-es1961-local]. JSEX keeps the $\zeta\,dd$ term in `deta` and never forms $\zeta'$ [@loc-jsex-program-js]. The elements "must always be interpolated to the time assumed in the calculation", which the polynomial form makes automatic [@loc-es1961-local].

### Shadow radii at the observer's plane

The tabulated $L_1$ and $L_2$ are the penumbral and umbral radii on the fundamental plane. The observer sits at height $\zeta$ above it along the axis, so the radii there are

$$L_1' = L_1 - \zeta\tan f_1, \qquad L_2' = L_2 - \zeta\tan f_2,$$

where $f_1$ and $f_2$ are the half-angles of the penumbral and umbral cones. JSEX stores these as `l1'` and `l2'` in slots 28 and 29 [@loc-jsex-program-js]. Stellarium writes `L1 = L1 - zeta * tf1` [@loc-stellarium-astrocalc]. $L_2'$ is negative when the observer is inside the umbral cone beyond its vertex, the total case, and positive in the antumbral, annular case [@loc-es1961-local].

Two identities that every code read here relies on follow from the cone geometry: $(L_1' + L_2')/2$ is the apparent solar radius and $(L_1' - L_2')/2$ the apparent lunar radius, both in Earth radii projected on the observer's plane. Eclipse-Engine sets `rSun = (gm.L1 + gm.L2) / 2, rMoon = (gm.L1 - gm.L2) / 2` [@loc-eclipse-engine], and the SR123 simulator does the same [@loc-sr123-eclipse-2026].

## Greatest phase and the contacts

### The relative coordinates

Define [@loc-es1961-local]

$$u = x - \xi, \quad v = y - \eta, \quad u' = x' - \xi', \quad v' = y' - \eta',$$
$$m^2 = u^2 + v^2, \qquad n^2 = u'^2 + v'^2,$$

with $m$ and $n$ positive. $m$ is the distance from the observer to the shadow axis in the observer's plane and $n$ the relative speed in Earth radii per hour. The 1992 Supplement phrases the whole problem as "an observer sees an eclipse as two disks of fixed size, one crossing the other in a straight line at constant speed" [@loc-es1992-ch8].

![A contact is a tangency of the two discs, which is why C1 and C4 are roots of $m = L_1'$ and C2 and C3 roots of $m = |L_2'|$. The position angle $P$ locates the point of tangency on the solar limb, and is what the tables print beside each time.](img/contact-configurations.svg)

### Maximum eclipse

Greatest phase is when $(L_1 - m)/(L_1 + L_2)$ is a maximum. Because $L$ varies very slowly, this is when $m^2$ is a minimum, $uu' + vv' = 0$. With $T = T_0 + t$ and the velocities held constant over $t$,

$$t = -\frac{D}{n^2}, \qquad D = u_0 u' + v_0 v',$$

in hours [@loc-es1961-local]. JSEX `getmid()` starts at $t = 0$ and repeats `tmp = (u*a + v*b)/n2; t -= tmp` until $|\mathrm{tmp}| < 10^{-6}$ h or 50 iterations, re-evaluating everything at each step [@loc-jsex-program-js]. Eclipse-Engine instead scans a 4 hour window at 4000 steps and golden-sections the magnitude [@loc-eclipse-engine].

### Penumbral contacts (first and fourth)

At beginning or end of the partial phase $u^2 + v^2 = L_1^2$. Substituting $u = u_0 + tu'$, $v = v_0 + tv'$ gives the quadratic

$$n^2 t^2 + 2Dt + (m_0^2 - L_1^2) = 0.$$

The Supplement solves it through an auxiliary angle. Setting

$$\Delta = \frac{u_0 v' - u' v_0}{n}, \qquad \sin\psi = \frac{\Delta}{L_1},$$

the solution is

$$t = \frac{L_1\cos\psi}{n} - \frac{D}{n^2}.$$

"The term $-D/n^2$ is the correction that would be applied to $T_0$ to give the time of greatest phase ... the term $L_1\cos\psi/n$ thus represents approximately the semi-duration of the partial phase which must be subtracted to obtain the time of beginning, or added to obtain the time of end. In other words, $\cos\psi$ must be taken as negative for the beginning and positive for the end, since $L_1$ is always positive" [@loc-es1961-local]. $\Delta$ is the perpendicular distance from the observer to the relative path of the axis, so $|\Delta| > L_1$ means the site is never in the penumbra.

### Umbral contacts (second and third) and the sign rules

The umbral contacts use $L_2$ in the same formula:

$$t = \frac{L_2\cos\psi}{n} - \frac{D}{n^2}, \qquad \sin\psi = \frac{\Delta}{L_2}.$$

"Because $L_2$ is negative for total eclipses and positive for annular eclipses, $\cos\psi$ must be taken as positive for the beginning of the total phase and the end of the annular phase, and as negative for the end of the total phase and the beginning of the annular phase. The semi-duration of the umbral phase is given by $\pm L_2\cos\psi/n$" [@loc-es1961-local]. A second approximation from the improved times is recommended, and $\Delta T$ is subtracted at the end to convert to Universal Time.

JSEX encodes exactly this. In `c2c3iterate()` the sign is $-1$ for C2 and $+1$ for C3 and is reversed when `mid[29] < 0`, that is when $L_2' < 0$. The loop body is [@loc-jsex-program-js]:

```
n = Math.sqrt(circumstances[30])
tmp = circumstances[26]*circumstances[25] - circumstances[24]*circumstances[27]
tmp = tmp / n / circumstances[29]
tmp = sign * Math.sqrt(1.0 - tmp*tmp) * circumstances[29] / n
tmp = (circumstances[24]*circumstances[26] + circumstances[25]*circumstances[27]) / circumstances[30] - tmp
circumstances[1] = circumstances[1] - tmp
```

The first `tmp` is $(u'v - uv')/(nL_2') = -\sin\psi$, the second is $\pm L_2'\cos\psi/n$, and the update is $t \leftarrow t - D/n^2 \pm L_2'\cos\psi/n$, a Newton step on the contact condition with the velocities re-evaluated each pass. The initial guesses come from the mid-eclipse solution: `c2[1] = mid[1] - tmp` and `c3[1] = mid[1] + tmp` for the annular case and the reverse when $L_2' < 0$. Convergence is to $10^{-6}$ h, about 4 ms, in at most 50 passes. Stellarium's `localSolarEclipse` returns the same increment in one line, `dt = (L * cfi / sqrt(udot*udot + vdot*vdot)) - (u*udot + v*vdot)/n2` with `cfi = contact * sqrt(1 - (delta/L)^2)` [@loc-stellarium-astrocalc].

### Is the site inside the umbra?

The site sees a central phase when, at greatest phase, $m < |L_2'|$. It is total when $L_2' < 0$ and annular when $L_2' > 0$. JSEX `getall()` tests `if ((mid[36] < mid[29]) || (mid[36] < -mid[29]))` and then sets the type from the sign of `mid[29]` [@loc-jsex-program-js]. Eclipse-Engine solves the inner contacts on $m - |L_2'|$ and notes why the absolute value matters: "L2 is negative inside an umbra and POSITIVE inside an antumbra, so the m + L2 form that holds for a total eclipse has no root for an annular one" [@loc-eclipse-engine]. A partial eclipse at the site requires only $m < L_1'$ at greatest phase, which JSEX expresses as a positive magnitude.

### The direct numerical alternative

Both Supplements offer a second method. "Times and position angles of contacts may be obtained by direct numerical solution of the equation $u^2 + v^2 - L^2 = 0$. For four, or more, times at equal intervals surrounding the phase required, a small table is made of the quantities $u$, $v$, $L$, $u^2+v^2-L^2$. The time $T$ of contact is then found, by the standard techniques of inverse interpolation" [@loc-es1961-local]. The 1992 edition prefers it: "There are methods for finding the times of these phenomena by successive iteration, using approximations and auxiliary angles. However, it is simpler to tabulate $u$, $v$, $L$ ... and also the discriminant $u^2+v^2-L^2$. When the discriminant goes to zero, inverse interpolation gives the time of the local contact" [@loc-es1992-ch8]. Its advantages listed in 1961 are "no auxiliary formulae and angles; ... no theoretical approximations are necessary (there is no need to assume that $u'$, $v'$ and $L$ are constant)" [@loc-es1961-local]. Eclipse-Engine is the code that follows this route. It brackets sign changes of $m - L_1'$ and $m - |L_2'|$ on a grid and bisects. It names contacts "by which way the curve crosses zero, never by the order the roots came out", so that a window containing only a last contact is not mislabelled as a first one [@loc-eclipse-engine].

## Magnitude

The Supplement's definition: "The magnitude of the eclipse is by definition the fraction of the solar diameter covered by the Moon at the time of greatest phase, expressed in units of the solar diameter" [@loc-es1961-local]. Two cases follow from the figure of the two cones cut by the observer's plane.

An observer in the penumbra at distance $m$ from the axis:

$$M_1 = \frac{L_1' - m}{L_1' + L_2'}.$$

An observer inside the umbra or antumbra sees the whole lunar disc projected on the Sun:

$$M_2 = \frac{L_1' - L_2'}{L_1' + L_2'},$$

and "identical results are obtained for a total eclipse, provided it is noted that in the latter case $OA = -L_2$" [@loc-es1961-local]. The 1992 edition adds: "Note also that this is the diameter of the lunar disk in units of the diameter of the solar disk" [@loc-es1992-ch8]. NASA's local circumstances tables state the same convention: "For umbral eclipses (both annular and total), the eclipse magnitude is identical to the topocentric ratio of the Moon's and Sun's apparent diameters" [@loc-nasa-locirc-2001].

JSEX computes both and switches at the end of `getall()` [@loc-jsex-program-js]:

```
mid[36] = Math.sqrt(mid[24]*mid[24] + mid[25]*mid[25])      // m
mid[37] = (mid[28] - mid[36]) / (mid[28] + mid[29])          // magnitude, penumbral form
mid[38] = (mid[28] - mid[29]) / (mid[28] + mid[29])          // moon/sun ratio
...
if ((mid[39] == 2) || (mid[39] == 3)) { mid[37] = mid[38] }  // umbral: ratio
```

$M_1$ continues smoothly into $M_2$ at $m = |L_2'|$ in the total case, since there $L_1' - m = L_1' + L_2'$ only when $L_2' = -m$. In the annular case $M_1 < 1$ at second contact and $M_2 < 1$ throughout, so the reported "magnitude" of an annular eclipse is the diameter ratio, below one. Swiss Ephemeris reports both numbers, `attr[0]` the diameter fraction and `attr[8]` "magnitude acc. to NASA; = attr[0] for partial and attr[1] for annular and total eclipses" [@loc-swephprg].

## Obscuration

"In the reduction of certain types of eclipse observations, it is necessary to evaluate the fraction of the surface of the solar disk obscured by the Moon" [@loc-es1961-local]. With the solar radius as the unit, the lunar radius is

$$s = \frac{L_1' - L_2'}{L_1' + L_2'},$$

the centre separation is $1 + s - 2M_1 = 2m/(L_1' + L_2')$, and the triangle formed by the two centres $A$ (Moon), $B$ (Sun) and one intersection point $C$ of the two circles has angles

$$\cos C = \frac{L_1'^2 + L_2'^2 - 2m^2}{L_1'^2 - L_2'^2}, \qquad \cos B = \frac{L_1' L_2' + m^2}{m\,(L_1' + L_2')}, \qquad A = \pi - (B + C),$$

with $0 \le C \le \pi$ and $0 \le B \le \pi$. The obscured fraction is

$$S' = \frac{s^2 A + B - s\sin C}{\pi}.$$

"During the annular phase, $S'$ is equal to $s^2$, while it is equal to unity in the case of the total phase" [@loc-es1961-local]. The derivation is two circular segments: $S = (s^2 A + B) - (s^2\sin A\cos A + \sin B\cos B)$, and the half-chord $CE = s\sin A = \sin B$ collapses the second bracket to $s\sin C$. JSEX `getcoverage()` is a transcription [@loc-jsex-program-js]:

```
c = Math.acos((mid[28]*mid[28] + mid[29]*mid[29] - 2.0*mid[36]*mid[36]) / (mid[28]*mid[28] - mid[29]*mid[29]))
b = Math.acos((mid[28]*mid[29] + mid[36]*mid[36])/mid[36]/(mid[28]+mid[29]))
a = Math.PI - b - c
c = ((mid[38]*mid[38]*a + b) - mid[38]*Math.sin(c))/Math.PI
```

with the annular branch `c = mid[38]*mid[38]` and clamps at 0 and 1.

The same area written for two discs of angular radii $r_s$ and $r_m$ at separation $\delta$, the form used by the topocentric codes, is

$$\text{Obs} = \frac{r_m^2\alpha + r_s^2\beta - \tfrac12\sqrt{(-\delta+r_s+r_m)(\delta+r_s-r_m)(\delta-r_s+r_m)(\delta+r_s+r_m)}}{\pi r_s^2},$$

$$\alpha = \arccos\frac{\delta^2 + r_m^2 - r_s^2}{2\delta r_m}, \qquad \beta = \arccos\frac{\delta^2 + r_s^2 - r_m^2}{2\delta r_s},$$

which is Eclipse-Engine's `obscuration(sep, rs, rm)` [@loc-eclipse-engine] and, with the square root written as $r_m^2\sin\alpha\cos\alpha + r_s^2\sin\beta\cos\beta$, Swiss Ephemeris' `sc1 + sc2` [@loc-swecl-c]. In terms of magnitude and the radius ratio $r = r_m/r_s$ the separation is $\delta/r_s = 1 + r - 2M_1$. With that substitution solareclipses.com writes obscuration as a function of $M$ and $r$ alone, building on the image-analysis derivation of Sridhar and others and correcting a sign error in it [@loc-solareclipses-obscuration] [@loc-sridhar-2012].

Obscuration is smaller than magnitude through the partial phase because the covered region is a lens, not a rectangle. Espenak's glossary keeps the two apart: magnitude "is strictly a ratio of diameters and should not be confused with eclipse obscuration, which is a measure of the Sun's surface area occulted by the Moon" [@loc-eclipsewise-glossary]. The 1992 Supplement opens its section with "Magnitude is commonly confused with obscuration" [@loc-es1992-ch8].

![Obscuration runs below magnitude at every magnitude short of one. With equal apparent discs a magnitude of 0.50 covers 0.391 of the solar area. The curve is computed from the lens-area formula quoted above, section 9D of the 1961 Explanatory Supplement [@loc-es1961-local].](img/magnitude-obscuration.svg)

## Position angle $P$ and vertex angle $V$

This note writes the position angle of a contact $P$, as NASA's tables do. The 1961 Supplement writes the same angle $Q$, and the quotations below keep its letter.

At a contact the point of tangency lies on the line of centres, so [@loc-es1961-local]

$$u = L\sin Q, \qquad v = L\cos Q, \qquad \tan Q = \frac{u}{v},$$

"where the appropriate value of $L$ is used. The angle $Q$ is the position angle of the point of contact, measured eastwards from the north point of the solar limb. The quadrant of $Q$ is determined by noting that $\sin Q$ has the sign of $u$, except for the contacts of the total phase for which $\sin Q$ has the opposite sign to $u$ since $L_2$ is negative for total eclipses" [@loc-es1961-local]. JSEX applies the sign through a multiplier [@loc-jsex-program-js]:

```
if ((mid[39] == 3) && ((circumstances[0] == -1) || (circumstances[0] == 1))) contacttype = -1.0
circumstances[31] = Math.atan2(contacttype*circumstances[24], contacttype*circumstances[25])
```

The Supplement also gives $Q = N + \psi$ with $\tan N = u'/v'$, useful when only one approximation has been made, and the 1992 edition restates the angle as the direction of the vector $(u, v)$ because "the projected shadow is a reflection of what the observer sees in the sky" [@loc-es1992-ch8]. NASA's local circumstances tables define $P$ and $V$ as "measured counter-clockwise (i.e., eastward) from the north and zenith points, respectively" [@loc-nasa-locirc-2001].

The vertex angle subtracts the [?parallactic-angle] $C$:

$$V = P - C, \qquad \tan C = \frac{\xi}{\eta},$$

"$\sin C$ having the same algebraic sign as $\xi$" [@loc-es1961-local]. The same relation appears in the differential-correction section as $\tan C = (\xi + \xi'\sigma)/(\eta + \eta'\sigma)$ for the contacts at semi-duration $\sigma$ from maximum [@loc-es1961-local]. Chauvenet's formulation, as transmitted by Buchanan, is equation (385) $V = Q - C$ with $C$ from $p\sin P = \sin\phi$, $p\cos P = \cos\phi\cos\theta$, $c\sin C = \cos P\tan\theta$, $c\cos C = \sin(P - d')$, where $d'$ is the Sun's declination [@loc-buchanan-1904]. JSEX computes $C$ as the parallactic angle from the altitude [@loc-jsex-program-js]:

```
circumstances[33] = Math.asin(coslat * circumstances[17] / Math.cos(circumstances[32]))
if (circumstances[20] < 0.0) { circumstances[33] = Math.PI - circumstances[33] }
circumstances[34] = circumstances[31] - circumstances[33]
```

that is $\sin C = \cos\phi\sin\theta/\cos a$, placed in the second quadrant when $\eta < 0$, and $V = P - C$. Jubier's calculator reports $V$ as an o'clock value and notes that this differs from the NASA bulletins, where $V$ is counter-clockwise in degrees [@loc-jubier-calc-instr].

## Altitude, azimuth and visibility

The direction of the shadow axis is the direction to the Sun to within the solar parallax, so the Sun's altitude and azimuth follow from $d$, $\theta$ and $\phi$. JSEX [@loc-jsex-program-js]:

$$\sin a = \sin d\sin\phi + \cos d\cos\phi\cos\theta,$$
$$\tan A = \frac{-\sin\theta\cos d}{\sin d\cos\phi - \cos\theta\sin\phi\cos d},$$

with $A$ from north through east via `atan2`. Stellarium uses $\sin a = \zeta$ directly, the same expression in fundamental-plane terms [@loc-stellarium-astrocalc]. JSEX marks an event as below the horizon when $a < -0.00524$ rad, that is $-0.3^{\circ}$, the comment calling it a "crude correction for refraction (and for consistency's sake)", and it prints such altitudes as 0 [@loc-jsex-program-js]. The header comment records what a real refraction treatment would need: "correcting for refraction will involve creating a 'virtual' altitude for each contact, and hence a different value of rho and O' for each contact" [@loc-jsex-program-js].

When a contact falls below the horizon but maximum is above it, JSEX replaces the contact by sunrise or sunset. `getsunriset()` iterates at most three times on

$$h_0 = \arccos\frac{\sin(-0.00524) - \sin\phi\sin d}{\cos\phi\cos d}, \qquad t \leftarrow t + \frac{\pm h_0 - \theta}{\mu'},$$

and the row is flagged (r) or (s) [@loc-jsex-program-js] [@loc-jsex-key]. The bit pattern of which of C1, C2, mid, C3, C4 are above the horizon selects one of ten handled cases, and the code admits "There are other patterns, but those are the only ones we're covering!" [@loc-jsex-program-js].

## Duration and time output

Duration of the central phase is $t_{C3} - t_{C2}$ in hours, printed as minutes and seconds after adding $0.05/60$ h so that the floor rounds to the nearest 0.1 s. If C2 or C3 is below the horizon the duration is measured from maximum instead [@loc-jsex-program-js]. The Supplement's semi-duration $\pm L_2\cos\psi/n$ gives the same number in one evaluation when the velocities are constant [@loc-es1961-local].

Times come out in hours of TDT relative to $t_0$. JSEX converts to local time as `t + t0 - tz - (deltaT - 0.5)/3600`, subtracting $\Delta T$ and half a second so that the truncating formatter rounds to the nearest second [@loc-jsex-program-js]. Every other time in the table is rounded the same way.

## What the JSEX program does, in order

For one eclipse and one site, `calculatefor()` runs `getall()` [@loc-jsex-program-js]:

1. `readform()` builds the observer constants: $\phi$, $\lambda_W$, height, time zone, $\rho\sin\phi'$, $\rho\cos\phi'$.
2. `getmid()` iterates $t \leftarrow t - D/n^2$ from $t = 0$, each pass calling `timelocdependent()` which evaluates the polynomials and their derivatives (`timedependent()`), then $\theta$, $\xi$, $\eta$, $\zeta$, $\xi'$, $\eta'$, $u$, $v$, $u'$, $v'$, $L_1'$, $L_2'$ and $n^2$.
3. `midobservational()` computes $P$, altitude, $C$, $V$, azimuth, visibility, then $m$, magnitude and the diameter ratio.
4. If the magnitude is positive, `getc1c4()` seeds C1 and C4 at $t_\mathrm{mid} \mp L_1'\cos\psi/n$ and iterates each with `c1c4iterate()`.
5. If $m < |L_2'|$, `getc2c3()` seeds and iterates C2 and C3 with the sign rule for $L_2' < 0$, and sets the type to total or annular. `observational()` is then run for every contact.
6. The horizon pattern is examined and sunrise or sunset substituted where a contact is below the horizon.
7. For central eclipses the magnitude is replaced by the diameter ratio. `getcoverage()` computes obscuration, `getduration()` the central duration.

The code carries no limb profile, no refraction beyond the $-0.3^{\circ}$ threshold, no centre-of-figure offset and no choice of $k$ or solar radius. Those are frozen inside the element files, the values of the Five Millennium Canon, NASA/TP-2006-214141, with its $\Delta T$ [@loc-jsex-index].

## Chauvenet and Meeus

Chauvenet's chapter X is a transformation of Bessel's method with the same fundamental-plane quantities. Buchanan's 1904 exposition of it gives the angles of position as $Q = N + \psi$ and $V = Q - C$ (equations 276 to 279). It also keeps the old expression of magnitude in "digits", twelfths of the solar diameter, and says it becomes the modern fraction "by omitting the constant 12" [@loc-buchanan-1904]. The USNO reference list still names Chauvenet volume 1 chapter X and Green (1985) chapter 18 as the treatments of Bessel's formulation [@loc-usno-eclipse-ref].

Meeus's "Elements of Solar Eclipses 1951-2200" (1989) is the source the calculator authors cite. Jubier credits it and "Astronomical Algorithms" as having "provided the algorithms for this page" [@loc-jubier-calc-instr], and The Photographer's Ephemeris bases its local circumstances on it together with the 2013 Explanatory Supplement [@loc-tpe-technote]. Bill Gray's review describes its heart as "a discussion of the use of Besselian elements" that "contained everything I needed to know to implement eclipse/occultation computations", with no treatment of how to generate the elements [@loc-projectpluto-books]. The book was not obtained for this note. "Astronomical Algorithms" chapter 54 was not obtained either. As far as this project has established, that chapter derives $\gamma$, $u$ and the magnitude at greatest eclipse from the lunar phase theory and does not carry the observer-level reduction. That is why the USNO list and the calculator authors point to "Elements" for site-level work [@loc-usno-eclipse-ref] [@loc-meeus-aa-1998]. Confirming that from the text itself is an open question below.

## Sources compared

| Source | Formulation | Observer model | Contact solver | What it has that the others do not |
|---|---|---|---|---|
| Explanatory Supplement 1961, 9D [@loc-es1961-local] | Closed formulas with auxiliary angle $\psi$ | $C$, $S$, $H$ in Earth radii, $e^2 = 0.00672267$ then $0.00669454$ | $t = L\cos\psi/n - D/n^2$, second approximation | Differential corrections $\partial t/\partial\lambda, \partial\phi, \partial H, \partial\Delta T$; three worked examples; ionosphere heights |
| Explanatory Supplement 1992, 8.36 [@loc-es1992-ch8] | Vector restatement | Same | Inverse interpolation on $u^2+v^2-L^2$ recommended | Explicit warning list: ephemeris consistency, rotation, centre of figure, limb, refraction |
| Chauvenet via Buchanan [@loc-buchanan-1904] | Bessel's method transformed | Same quantities | Successive approximation | $Q = N + \psi$ form, $V$ from $P$, $C$ auxiliaries, magnitude in digits |
| NASA JSEX program.js [@loc-jsex-program-js] | 1961 formulas | $0.99664719$, 6378140 m | Newton iteration to $10^{-6}$ h | Sunrise/sunset substitution, obscuration, (r)/(s) flags, full source |
| Stellarium AstroCalc [@loc-stellarium-astrocalc] | 1961 formulas | Site rectangular coordinates from its Earth model | Same increment, elements computed on the fly | No published elements needed; $k = 0.2725076$ and $0.272281$, Sun 696000 km |
| Eclipse-Engine [@loc-eclipse-engine] | 1961 coordinates, numerical contacts | $N$, $e^2$, 6378.1366 km | Grid plus bisection, golden section for maximum | Root naming by crossing direction; lens obscuration in $r_s$, $r_m$ |

## What a developer should do

Implement the 1961 Explanatory Supplement section 9D formulas exactly as quoted above and test against `program.js`, which is GPL and self-contained [@loc-es1961-local] [@loc-jsex-program-js]. Use the NASA element files as the first test data because their $\Delta T$ is embedded and the JSEX output for any city is published, so a match to the second is a full regression test [@loc-jsex-index] [@loc-jsex-key]. Solve the contacts by the direct root-finding of the 1992 edition rather than the auxiliary angle, because it makes no constant-velocity assumption and handles windows containing a single contact cleanly [@loc-es1992-ch8] [@loc-eclipse-engine]. Report magnitude in NASA's two branches and obscuration from the lens area, and label the branch. Compute $P$ from $\text{atan2}(\pm u, \pm v)$ with the total-eclipse sign reversal and $V$ from the parallactic angle $\tan C = \xi/\eta$. Keep every time in TT internally and subtract $\Delta T$ once at output. Read the 1961 text first, then the 1992 section 8.36, then the JSEX code.

## What this changes

Nothing in the global-circumstances pipeline. The local reduction consumes the same elements and the same $\Delta T$. It adds one requirement upstream: the element generator must publish $\tan f_1$, $\tan f_2$ and $\Delta T$ with the elements, because $L_1'$, $L_2'$ and $\theta$ cannot be formed without them.

## Open questions

- Obtain "Elements of Solar Eclipses 1951-2200" (Meeus 1989) and record its local-circumstances chapter formula by formula, in particular whether it uses the auxiliary angle $\psi$ or direct root finding and which spheroid constants it fixes [@loc-meeus-elements-1989].
- Obtain "Astronomical Algorithms" chapter 54 and confirm from the text that it stops at $\gamma$, $u$ and greatest-eclipse magnitude and refers site-level work to "Elements" [@loc-meeus-aa-1998].
- Obtain the 2013 Explanatory Supplement chapter 11 and note whether section 8.36 of 1992 was carried over unchanged, including the inverse-interpolation recommendation [@loc-es2013-ch11].
- Obtain the Sky and Telescope BASIC listing `solarecl.bas` (Sinnott's "Astronomical Computing" column), which the search index describes as "Local circumstances of a solar eclipse". The download returned a Cloudflare challenge and the Wayback copy an error page.
- Retrieve the Wayback snapshot of Chris O'Byrne's original "Eclipse Calculator" (chris.obyrne.com/Eclipses/calculator.html). The live host now serves a parking page and the 2016 snapshot fetched contains only site assets.
