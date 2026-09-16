---
title: Pipeline design
description: Nine stages from ephemeris kernels to limb-corrected umbra polygons, with the formulas, constants, outputs and validation case for each.
order: 2
status: working
updated: 2026-09-16
---

::: summary
- **Nine stages, one configuration record.** Ephemeris and time, enumeration, Besselian elements, global circumstances, partial-eclipse maps, local circumstances, terrain, lunar limb, and products with uncertainty. Every product carries the record of constants and data versions that produced it, set out before stage 1.
- **Two computational paths from one ephemeris layer.** An elements path for catalogues, maps and anything that must be reproducible from a published table, and a direct topocentric path for site-level work and limb tests. They must agree to 0.1 s on the same inputs [@bes-quaglia-2021] [@loc-usno-sec].
- **The smooth-Moon stages are textbook and have reference implementations.** The 1961 Explanatory Supplement for the formulas, Stellarium for the global curves, NASA's `program.js` for local circumstances [@bes-es1961] [@sw-stellarium-sec-cpp] [@loc-jsex-program-js].
- **The limb and terrain stages follow Wright and Young 2024** and have no open implementation. They replace the circular shadow with a per-pixel test against an 18,000-element profile [@svs-wright-young-2024].
- **Each stage has a named validation case** with a tolerance drawn from the [error budget](error-budget.md).
:::

![Two computational paths leave the same ephemeris layer, and the design's only true cross-check is that they meet again at local circumstances within 0.1 s. Almanac mode ends at stage 6, and terrain and the lunar limb are what edge mode adds.](img/pipeline-stages.svg)

## The configuration record

Every run starts by fixing, and every output ends by printing, the following.
Predictors state some of these and none states all of them, and the
differences between predictors reduce to differences here [@val-quaglia-2021] [@svs-irwin-quaglia-2024-technical].

| Item | Almanac mode | Edge mode |
|---|---|---|
| Ephemeris | DE440 via `de440s.bsp` (or the ephemeris of the table being reproduced) | DE440 |
| Lunar orientation | not needed | `moon_pa_de440_200625.bpc` with the current NAIF frame kernel, frame `MOON_ME_DE440_ME421` |
| Earth figure | WGS84, $a = 6378.137$ km, $1/f = 298.257223563$ | same, plus EGM96 or EGM2008 geoid |
| Solar radius $s_0$ | 959.63″ at 1 au | 959.95″ ± 0.05″, with 959.63″ as a preset |
| Lunar radius | $k_1 = 0.2724880$ penumbral to match the NASA GSFC tables, 0.2725076 to match EclipseWise and the bulletins; $k_2 = 0.272281$ umbral | LOLA profile on a 1737.4 km datum; $k$ only for penumbral products |
| Terrain | sea level | SRTM GL1 or Copernicus GLO-30, converted to ellipsoidal height |
| ΔT | value printed with the table being matched | latest USNO `deltat.data` or `deltat.preds`, with its date |
| Refraction | none, stated | none, stated; optional flagged C1 and C4 adjustment below 5°, and a warning flag on any contact with the Sun below 10° |
| Time scale internal | TT | TT |

Sources for each choice are in the stage notes below and in
[Earth model and time](../10-raw/07-earth-and-time/_index.md) and
[lunar and solar model](../10-raw/08-lunar-and-solar-model/_index.md).
The default solar radius is contested: the evidence from the solar radius and
from validation favours 959.95″, while the foundations, local-circumstances
and limb practice favour 959.63″ with the measured value available. The two
modes satisfy both. The frame kernel is named `moon_de440_200625.tf` in Wright and
Young's appendix; NAIF now serves the 2025 revision of the same frame as
`moon_de440_250416.tf` [@svs-wright-young-2024] [@moon-naif-moon-fk-de440].

## Stage 1: ephemeris, orientation and time

**Inputs.** `de440s.bsp` (1849 to 2150, 31 MB) for the Sun, Earth and Moon;
the DE440 lunar PCK and frame kernel; IERS `finals.all` or USNO `deltat.data`
and `deltat.preds`; a leap-second table [@moon-naif-summaries]
[@moon-jpl-bsp-readme] [@earth-iers-bulletin-a] [@earth-usno-deltat-preds].

**Contract.** The layer exposes, at a TT instant: apparent geocentric places
of the Sun and Moon on the true equator and equinox of date, with light-time
and aberration applied to both; apparent topocentric places for a site;
Greenwich apparent sidereal time; the observer-to-Moon vector in the Moon
mean-Earth frame. The Moon is read as body 301 relative to 399 and the Sun as
body 10, never the barycentre, since the Sun wanders up to 1.6 solar radii
from it [@moon-folkner-2014]. TT may stand in for TDB, the difference being
under 2 m on the shadow [@earth-circ179].

**The trap.** Mixing a geometric Sun with an apparent Moon displaces the
shadow axis by 20″, which is 38 km on the ground. Using TT where UT belongs
displaces it by 32 km. These two errors dwarf everything else in the budget
and are the first things to test [@earth-es1992] [@moon-skyfield-positions].

**ΔT.** Three regimes: measured IERS or USNO values for 1962 onward,
`deltat.preds` with its error column for a few years ahead, and the
Stephenson, Morrison and Hohenkerk 2016 spline and parabola beyond that, with
the tidal-acceleration adjustment matched to the ephemeris
[@earth-smh2016] [@earth-swisseph-swephlib]. ΔT is stored as metadata and
applied once, when μ is converted to a longitude in stage 4 or to a local
hour angle in stage 6, at 15.041″ of rotation per second [@bes-es1961]
[@glob-rherale].

## Stage 2: enumeration and provisional type

**Method.** Step through mean new moons. Reject a lunation when
$|\sin F| > 0.36$. Compute [?gamma] and $u$ from Meeus's short series. Classify:
central if $|\gamma| < 0.9972$; no eclipse if $|\gamma| > 1.5433 + u$;
non-central umbral if $0.9972 < |\gamma| < 0.9972 + |u|$; total if $u < 0$;
annular if $u > 0.0047$; for $0 \le u \le 0.0047$, hybrid if
$u < 0.00464\sqrt{1 - \gamma^2}$ and otherwise annular; partial
magnitude $(1.5433 + u - |\gamma|)/(0.5461 + 2u)$ [@cat-meeus-1991-aa].

**Then refine.** For each candidate, compute the elements of stage 3 and take
γ as the minimum of $\sqrt{x^2 + y^2}$. Decide the final type on the umbral
radius at the surface point under the axis, at greatest eclipse and at both
ends of the central line, so that hybrids and their three classes fall out.
Keep a non-central class: 94 eclipses in five millennia have a one-limit
track and no central line [@cat-espenak-meeus-2009-catalog]
[@cat-swisseph-swecl].

**Saros.** Kluepfel's closed form from the lunation number reproduces the
Saros number of all 11,898 catalogued eclipses [@cat-vangent-cycles].

**Validation.** The 221 eclipses of 1951 to 2050 in NASA's ASCII catalogue:
zero type disagreements, greatest-eclipse times within 1.2 min from the
series, then within 0.1 s from the elements [@cat-nasa-5mkse-ascii].

## Stage 3: Besselian elements

**Inputs.** Apparent geocentric places from stage 1, $k_1$, $k_2$, $s_0$,
$\pi_0 = 8.794″$, $a_e$, ΔT.

**Equations, in order** [@bes-es1961] [@bes-es1992]. With $b = r_m / R$, both
distances in the same unit, the shadow axis direction $(a, d)$ and scale $g$ come from
$g\cos d\cos a = \cos\delta_\odot\cos\alpha_\odot - b\cos\delta_m\cos\alpha_m$
and its two companions. The Moon's coordinates in the fundamental system are

$$x = r_m\cos\delta_m\sin(\alpha_m - a),\qquad
y = r_m[\sin\delta_m\cos d - \cos\delta_m\sin d\cos(\alpha_m - a)],$$

$$z = r_m[\sin\delta_m\sin d + \cos\delta_m\cos d\cos(\alpha_m - a)].$$

The hour angle is $\mu = \theta - a$ with θ the apparent sidereal time
evaluated at the TT instant as if it were UT, the ephemeris sidereal time of
the 1961 Supplement. NASA's tables, its JavaScript calculator, Eclipse-Engine
and the 2027 visualiser all tabulate μ this way, so a table's μ is free of ΔT
and the shift is applied downstream [@bes-es1961] [@loc-jsex-program-js]
[@glob-rherale]. The cone half-angles are

$$\sin f_1 = \frac{\sin s_0 + k_1\sin\pi_0}{gR},\qquad
\sin f_2 = \frac{\sin s_0 - k_2\sin\pi_0}{gR},$$

the vertex heights $c_1 = z + k_1/\sin f_1$ and $c_2 = z - k_2/\sin f_2$, and
the shadow radii on the plane $l_1 = c_1\tan f_1$ and $l_2 = c_2\tan f_2$.
$l_2 < 0$ is total, $l_2 > 0$ annular. Publish $l_2$ with its sign.

**Output.** A function `elements_at(t_tt)` returning $(x, y, d, \mu, l_1,
l_2, \tan f_1, \tan f_2, z)$, and for export the NASA polynomial form: cubic
in $x$ and $y$, quadratic in $d$, $l_1$, $l_2$, linear in μ, fitted to five
samples over six hours about $t_0$ [@bes-nasa-2024-elements]. Metadata:
ephemeris, $t_0$, ΔT, $k_1$, $k_2$, $s_0$, ellipsoid.

**Validation.** The 1961 Supplement's worked example for 1961 February 15
08h ET, and the NASA 2024 April 8 polynomial at $t = 0$, expecting agreement
at $10^{-5}$ Earth radii once ephemeris, $k$ and ΔT match. A difference above
$10^{-4}$ Earth radii in $x$ or $y$, about 640 m, means a frame or aberration
inconsistency [@bes-es1961] [@bes-nasa-csv].

## Stage 4: global circumstances, smooth Moon

**Frame.** Bessel's substitution turns the ellipsoid into a unit sphere with
$\rho_1 = \sqrt{1 - e^2\cos^2 d}$, $\rho_2 = \sqrt{1 - e^2\sin^2 d}$ and a
rotated declination $d_1$. In that frame the central line at time $t$ is
$\xi = x$, $\eta_1 = y/\rho_1$, $\zeta_1 = \sqrt{1 - x^2 - \eta_1^2}$
[@glob-es1961]. Longitudes follow from $\lambda = \theta - \mu_{UT}$ with
$\mu_{UT} = \mu - 1.002738 \times 15\,\Delta T$ arcseconds, which is where ΔT
enters the map [@glob-rherale].

**Limits.** A point is on a limit when the eclipse begins and ends at the same
instant, which gives $\tan Q = (b' - \zeta d' - a'\sec Q)/(c' - \zeta\mu'\cos d)$
for the position angle $Q$ of the shadow edge, iterated on ζ. Use the 1992
procedure for whole curves: scan $Q$ by degrees, inverse-interpolate, iterate
ζ to $10^{-5}$ Earth radii, assign north or south by the sign of $L\cos Q$
[@glob-es1961] [@glob-es1992].

**Duration and width.** Central duration $2L_2/n$ with
$L_2 = l_2 - \zeta\tan f_2$; path width by Mikhailov's formula as transcribed
in Stellarium [@glob-es1992] [@glob-stellarium-sec]. Rise and set curves from
$\cos(\gamma - M) = (m^2 + 1 - l_1^2)/(2m)$ at $\zeta = 0$; curves of maximum
eclipse from $\tan Q = -(y' - \eta')/(x' - \xi')$ sweeping ζ [@glob-es1961].

**Output.** Central line, limits, outlines at stated instants, rise and set
curves, maximum-eclipse curves, greatest eclipse, greatest duration, ground
speed, as GeoJSON with the time system and ΔT in the properties.

**Validation.** The 1961 examples 9.6 and 9.7 ($\phi = +44^{\circ} 18'.3$,
$\lambda = -29^{\circ} 20'.9$, duration 158.6 s at 08h ET). Then NASA's 2024 path
table at three times, expecting 1 km and 0.1 s [@glob-es1961]
[@glob-nasa-path-2024].

## Stage 5: partial-eclipse maps

Equal-magnitude and equal-obscuration curves are not solved directly. The
Supplements interpolate on the maximum-eclipse curves; SVS and the open
Eclipse-Engine rasterise instead. For each grid cell find the time of maximum
by minimising $\Delta - L_1$, evaluate magnitude and the two-circle obscuration
with the exact lens formula, and contour with marching squares, padding the
grid edge and refining vertices near the time of maximum
[@glob-es1961] [@glob-rherale] [@glob-enrique7mc].

## Stage 6: local circumstances, smooth Moon

**Observer.** $\rho\sin\phi' = (S + h/a)\sin\phi$, $\rho\cos\phi' = (C + h/a)\cos\phi$
with $C = (\cos^2\phi + (1 - f)^2\sin^2\phi)^{-1/2}$ and $S = (1 - f)^2 C$,
$h$ the ellipsoidal height. Hour angle $\theta = \mu(t) - \lambda - 1.002738\,\Delta T$
with west longitude positive [@earth-es1992] [@loc-es1961-local].

**Reduction.** Form $(\xi, \eta, \zeta)$ and their rates, $u = x - \xi$,
$v = y - \eta$, $m = \sqrt{u^2 + v^2}$, and the observer's-plane radii
$L_1' = L_1 - \zeta\tan f_1$, $L_2' = L_2 - \zeta\tan f_2$. Maximum eclipse
iterates $t \leftarrow t - (uu' + vv')/n^2$. Contacts are the roots of
$m = L_1'$ (C1, C4) and $m = |L_2'|$ (C2, C3), found by the 1992 edition's
direct inverse interpolation on $u^2 + v^2 - L^2$ rather than the auxiliary
angle [@loc-es1961-local] [@loc-es1992-ch8].

**Magnitude and obscuration.** Magnitude $(L_1' - m)/(L_1' + L_2')$ in the
penumbra and $(L_1' - L_2')/(L_1' + L_2')$ inside the umbra or antumbra,
switching at $m = |L_2'|$. Obscuration is the lens area
$S' = (s^2 A + B - s\sin C)/\pi$ with $s = (L_1' - L_2')/(L_1' + L_2')$ the
ratio of the lunar to the solar radius, $B$ and $C$ the angles at the solar
and lunar centres of the triangle formed with an intersection point, and
$A = \pi - B - C$; never a function of magnitude alone.
Position angle $P$ from $\text{atan2}(\pm u, \pm v)$ with the sign reversal for
interior contacts of a total eclipse; vertex angle $V = P - C$ with
$\tan C = \xi/\eta$ [@loc-es1961-local] [@loc-nasa-locirc-2001].

**Second path.** The direct topocentric method: root-find
$\delta(t) = r_s \pm r_m$ on apparent topocentric positions from stage 1, as
USNO and the Swiss Ephemeris do. Agreement with the Besselian result within
0.1 s on the same inputs is the regression test for the element generator
[@loc-usno-sec] [@loc-swecl-c].

**Validation.** NASA's `program.js` output for any city, which is GPL and
self-contained, to the second; the Lusaka 2001 case (C2 13:09:19.3 UT,
C3 13:12:32.8 UT before limb correction) to 0.5 s [@loc-jsex-program-js]
[@val-tp2001-bulletin].

## Stage 7: terrain

**Why.** A limit shifts perpendicular to the path by about $h\cot A\sin D$:
577 m per 1000 m of elevation at a 60° Sun, 1.7 km at 30°, 5.7 km at 10°.
SVS measured up to 3 km over the 2017 western states. The umbra widens only by
$2h\tan f_2$, 82 m at Everest [@earth-espenak-tp2001] [@earth-svs-4517]
[@earth-timeanddate-accuracy].

**Method.** Look up orthometric height $H$ in SRTM GL1 (EGM96) or Copernicus
GLO-30 (EGM2008) and add the geoid undulation $N$ to get ellipsoidal $h$. The
geoid sits between 106 m below and 85 m above WGS84 and is worth up to 170 m
of path at a 30° Sun. Intersect the shadow with the terrain surface rather
than shifting a sea-level limit by the elevation factor; keep the factor as a
check [@earth-srtm-guide] [@earth-copdem] [@svs-wright-young-2024].

## Stage 8: lunar limb

**Profile construction** [@svs-wright-young-2024]. For an observer at
distance $d$ from the Moon's centre: convert each DEM pixel to rectangular
coordinates on the 1737.4 km datum; rotate by the topocentric libration from
stage 1; take polar $(r, \theta)$ of the transformed $(y, z)$; replace $r$ by
the angular radius $\alpha = \tan^{-1}(r/(d - x))$; bin θ into 18,000 elements
at 0.02°; keep the maximum α per bin. Rebuild when a libration angle moves by
0.01°. Only DEM longitudes between 75° and 105° east and west and a 450 km polar
swath need processing. SLDEM2015 at 128 pixels per degree (240 m) pairs with
this resolution. LDEM_128 is the one-file development dataset; the 33 MB
LDEM_16 is fit only for a smoke test, since a 16 pixel-per-degree cell is
about one arcsecond at the limb, 2 to 3 s of contact time
[@limb-lola-ldem128-label] [@limb-sldem2015-label].

**Limb test.** Symbols: $n$ the number of elements in $L$, $d_0$ the
observer-to-Moon distance at which $L$ was built, $d$ the current observer's
distance, $c$ the position angle of the Moon's axis, $\delta$ the Sun-to-Moon
apparent distance in solar radii, $\phi$ the position angle of the Sun with
respect to the Moon, $r$ the Sun's apparent radius in radians. With
$s = (d_0/d)/r$, $a = sL_i$, $\theta = 2\pi i/n + c$,
$\rho = a^2 + \delta^2 - 2a\delta\cos(\theta - \phi)$: the eclipse is not
total if any $\rho < 1$. Trivial exclusions: outside the umbra if
$s\max(L) - \delta < 1$, inside if $s\min(L) - \delta \ge 1$. Reverse the sense
for annularity. Antialias with $\epsilon = A(p)/10$. The broken-annular locus
is $\max(L) - \min(L) > \delta$ where both tests fail
[@svs-wright-young-2024].

**Contacts and beads.** C2 and C3 at a site are the first and last time steps
at which the test passes. Baily's beads are the same test per limb element:
each event is the instant the solar limb, drawn with Herald's curve
$h = 960″(M - 1)(1 - \cos P)$, clears a valley floor, reported with its
position angle and depth. Keep Herald's tangency construction as a
cross-check because the bulletins' examples are stated in its terms
[@limb-herald-1983] [@limb-espenak-tp2001].

**Path products.** The umbra is emitted as the polygon the raster produces,
not as an ellipse. A limit line becomes an interior and an exterior line with
a [?graze-zone] between them, 5 to 10 km wide [@limb-espenak-tp2001].

**What the profile replaces.** The centre-of-figure correction of the almanacs
is retired: LOLA products are referenced to the centre of mass in the DE421
mean-Earth frame, which is the frame the ephemeris orients. The 0.69 km gap
between the 1737.4 km datum and the 1738.09 km sphere of $k = 0.2725076$ is a
constant to add only when quoting heights against the almanac mean limb
[@limb-lola-ldem128-label] [@moon-naif-moon-fk-de440].

**Validation.** The Lusaka corrections of +4.0 s at C2 and −1.2 s at C3,
within 1 s allowing for Watts against LOLA. The SVS 2024 `umbra_hi` polygon at
one second, reproduced from SLDEM2015. The IOTA bead tables for 2017 at
Thermopolis and 2023 at Cape Range, each event within 1 s at the radius
correction each paper derived [@val-tp2001-bulletin] [@svs-2024-shapefiles-zip]
[@val-guhl-tegtmeier-2018] [@val-guhl-2023].

## Stage 9: products and uncertainty

Every product carries the stage 0 record and a per-run error estimate that
sums the [error budget](error-budget.md) rows in quadrature for the
configuration used. A smooth-Moon run reports about 2 km at a limit; a
true-limb run with 959.95″ reports 100 to 200 m. Limits are drawn three times,
at $s_0$ and $s_0 \pm \sigma$. Products for dates before 1600 or after 2300
carry a longitude gore for the ΔT standard error. This is stricter than the
Five Millennium Canon, which draws gores only where σ exceeds 265 s, before
the year 1 and after 2300 [@val-quaglia-2021] [@val-gsfc-uncertainty]
[@cat-espenak-meeus-2006-canon].

| Product | Stages | Reference to match |
|---|---|---|
| Eclipse list with type, γ, magnitude, Saros | 1, 2, 3 | NASA ASCII catalogue, 11,898 rows [@cat-nasa-5mkse-ascii] |
| Besselian element tables | 1, 3 | NASA CSV [@cat-nasa-besselian-csv] |
| Path map, smooth Moon | 3, 4 | NASA path tables [@glob-nasa-path-2024] |
| Partial-eclipse magnitude and obscuration map | 3, 5 | SVS 1% and 5% obscuration contours [@sw-svs-5073] |
| Site table: contacts, magnitude, obscuration, P, V, altitude | 3, 6 | NASA JavaScript Explorer, USNO computer [@loc-jsex-program-js] [@val-usno-2024] |
| Limb-corrected contacts and beads | 1, 6, 8 | Jubier's LC column, IOTA bead tables [@val-guhl-tegtmeier-2018] |
| Umbra polygons and true limits | 1, 4, 7, 8 | SVS `umbra_hi` and `upath_hi` [@svs-2024-shapefiles-zip] |
| City contact times at scale | 7, 8 | SVS cities JSON, 32,174 places [@svs-cities-2024-json] |

## What this does not cover

Refraction is left out of contacts and limits by every predictor and by this
design, with the reason stated in the output: it cancels to first order in a
relative-angle condition and is unpredictable below 5° [@earth-espenak-tp2001].
Lunar eclipses, transits and occultations reuse stages 1 and 8 but are out of
scope.
