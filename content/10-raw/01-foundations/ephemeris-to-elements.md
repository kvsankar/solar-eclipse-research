---
title: From ephemeris to elements
description: The ordered equations for producing a table of Besselian elements from geocentric Sun and Moon positions, what the almanacs and open-source codes do about frames, light-time and aberration, and how direct topocentric computation differs.
order: 2
status: working
updated: 2026-09-15
tags: [besselian, ephemeris, jpl-de, swiss-ephemeris, skyfield]
---

::: summary
- **Inputs are apparent geocentric places** of the Sun and Moon referred to the true equator and equinox of date, plus the Sun's distance and the Moon's parallax, at instants of TT. The 1961 Supplement names exactly these inputs [@bes-es1961]. Every implementation read for this note uses them, and none uses ICRF/J2000 directions without first rotating to the equator of date [@bes-swisseph-swecl] [@bes-solareclipses-formulas] [@bes-celestialprogramming-gen].
- **Fourteen equations, in order,** take those inputs to $x, y, d, \mu, l_1, l_2, \tan f_1, \tan f_2$. They are listed below with the constants each one needs [@bes-es1961] [@bes-es1992].
- **The almanacs computed elements at 10-minute steps and differentiated numerically.** NASA and Meeus publish a polynomial fitted to five samples over six hours. The polynomial is a publication format [@bes-es1992] [@bes-nasa-2024-elements].
- **No general-purpose open library generates elements from a JPL ephemeris as a documented, validated function.** Skyfield's maintainer says shadow projection "would require more sophisticated calculations than currently available" [@bes-skyfield-801]. The Swiss Ephemeris computes the geometry live but never exposes $x, y, l_1, l_2$ [@bes-swisseph-swecl]. Eclipse-Engine ships elements "fitted to the JPL DE440s ephemeris" but not the fitting code [@bes-eclipse-engine].
- **Direct topocentric computation** replaces the elements by the apparent topocentric separation of the two centres and their apparent semidiameters. The Swiss Ephemeris `eclipse_how()` and the USNO eclipse computer work this way, and Quaglia et al. extend it to the full limb profile [@bes-swisseph-swecl] [@bes-usno-eclipse-computer] [@bes-quaglia-2021].
:::

**The question.** Given a modern ephemeris such as JPL DE440, what sequence of equations produces a table of Besselian elements, which reference frame the inputs must be in, which of light-time, aberration, precession and nutation they must carry, how the published polynomial is fitted, and when a developer should skip the elements and compute topocentric circumstances directly. The definitions and constants are in [Besselian elements and the fundamental plane](besselian-elements.md) and are not repeated.

## What the inputs are

The 1961 Supplement is explicit: "The basic quantities from which the calculations of solar and lunar eclipses are derived are: the apparent right ascension $\alpha_\odot$, declination $\delta_\odot$, and radius vector $R$ of the Sun, and the right ascension $\alpha_\mathrm{m}$, declination $\delta_\mathrm{m}$, and horizontal parallax of the Moon, for every hour of E.T. during the eclipse; and the ephemeris sidereal time" [@bes-es1961]. An [?apparent-place|apparent place] is "the proper place of an object expressed with respect to the true (intermediate) equator and equinox of date", as opposed to a [?geometric-position|geometric position], which has no "corrections for light-time, aberration, etc." [@bes-usno-glossary]. The same Supplement notes that "Besselian elements, however, are rigorously independent of refraction" [@bes-es1961].

Three points follow for anyone starting from a JPL binary ephemeris, which delivers barycentric ICRF positions in TDB.

1. **Frame.** The fundamental system is defined through the equator and through $\mu$, an hour angle from a meridian. The x axis lies in the equatorial plane. Both need the true equator and equinox of date. A developer must apply precession and nutation to rotate GCRS vectors to the equator of date before forming $a$ and $d$. Current practice is IAU 2006/2000A [@bes-quaglia-2021]. The Swiss Ephemeris does this by requesting equatorial coordinates without the `SEFLG_J2000` flag [@bes-swisseph-swecl]. The solareclipses.com generator says "Use Equatorial Apparent of the Date coordinates" [@bes-solareclipses-formulas]. The Swiss Ephemeris comment "nutation need not be in lunar and solar positions, if mean sidereal time will be used" records the one consistent shortcut: nutation can be omitted from both the positions and the sidereal time, but not from one alone [@bes-swisseph-swecl].
2. **Light-time and aberration.** The almanac inputs are apparent places, so they carry light-time and annual aberration. The Swiss Ephemeris `eclipse_where()` calls `swe_calc()` with its default flags, which return apparent positions with light-time and aberration [@bes-swisseph-swecl] [@bes-swisseph-doc]. The solareclipses.com page states "Light-time already embedded in ephemeris data" [@bes-solareclipses-formulas]. Quaglia et al., who work topocentrically, apply "(a) light time to the body in question; (b) gravitational bending of the light path by the mass of the Sun; and (c) planetary aberration" [@bes-quaglia-2021]. Annual aberration displaces the Sun and the Moon by nearly the same angle, up to 20.5 arcseconds, so it moves the point Z but changes $x, y$ by only the differential part, of order the parallax factor times 20 arcseconds. Whether to use apparent or astrometric places is therefore a question of consistency with the sidereal time and the observer model rather than of shadow physics. None of the sources read for this note quantifies the difference. That is an open question below.
3. **Time.** Evaluate the ephemeris at instants of TT. The difference between TT and TDB, under 2 milliseconds, is negligible for the Moon's motion of 0.5 arcseconds per second. Do not evaluate at UT: ΔT belongs in the conversion of $\mu$ to longitude, not in the argument of the ephemeris [@bes-es1961] [@bes-aravpanwar].

Espenak's VSOP87/ELP2000-82 series are "referred to the mean equinox of the date" for the Sun [@bes-nasa-ephemeris], and his later series use JPL DE405 with the Moon's centre of mass [@bes-ew-de405]. The lunar theory was truncated at 0.0005 arcseconds and 1 metre, giving mean errors of "0.0006 second of time in right ascension and 0.006 arcsecond in declination" for the Moon and contact-time errors "of the order of 1/40 second" [@bes-nasa-ephemeris].

## The equations, in order

Symbols used below.

- $\alpha_\odot, \delta_\odot, R$: right ascension, declination and distance of the Sun, distance in au.
- $\alpha_\mathrm{m}, \delta_\mathrm{m}, \pi_\mathrm{m}$: right ascension, declination and equatorial horizontal parallax of the Moon.
- $\pi_0 = 8.794$ arcseconds: the solar parallax at 1 au.
- $s_0 = 959.63$ arcseconds: the solar semidiameter at 1 au.
- $k$: the lunar radius ratio, one value per cone.
- $\theta$: the Greenwich apparent sidereal time at the TT instant less ΔT.

All lengths are in Earth equatorial radii unless stated. Sources: the 1961 Supplement section 9B and the 1992 Supplement sections 8.322 and 8.323 [@bes-es1961] [@bes-es1992].

**Step 0. Positions.** From the ephemeris at TT instant $t$, obtain apparent geocentric $(\alpha_\odot, \delta_\odot, R)$ and $(\alpha_\mathrm{m}, \delta_\mathrm{m}, r_\mathrm{m})$ on the true equator and equinox of date. If the Moon's distance is given in km, form $\sin\pi_\mathrm{m} = a_e / r_\mathrm{m}$ with $a_e = 6378.137$ km, so that $r_\mathrm{m} = 1/\sin\pi_\mathrm{m}$ in Earth radii [@bes-es1992].

**Step 1. Scale.** The 1961 Supplement works with $g = G/R$ and $b = r_\mathrm{m}/R$, evaluated as
$$
b = \frac{\sin\pi_0}{R\sin\pi_\mathrm{m}}
$$
"where $\pi_0$, the horizontal parallax of the Sun at mean distance, is equal to 8".80 [8".794 for 1968 onwards] and $R$ is expressed in astronomical units as in the Ephemeris" [@bes-es1961]. With a modern ephemeris one may instead convert both distances to Earth radii using $1\ \mathrm{au} = 149\,597\,870.7$ km and $a_e = 6378.137$ km, so 1 au $= 23\,454.78$ Earth radii [@bes-solareclipses-formulas].

**Step 2. Direction of the axis (point Z).**
$$
g\cos d\cos a = \cos\delta_\odot\cos\alpha_\odot - b\cos\delta_\mathrm{m}\cos\alpha_\mathrm{m},\quad
g\cos d\sin a = \cos\delta_\odot\sin\alpha_\odot - b\cos\delta_\mathrm{m}\sin\alpha_\mathrm{m},\quad
g\sin d = \sin\delta_\odot - b\sin\delta_\mathrm{m}
$$
Solve for $a$ with a two-argument arctangent, then for $d$ and $g$ [@bes-es1961]. In vector form this is $\mathbf{g} = \mathbf{r}_s - \mathbf{r}_m$ normalised, equation 8.322-2 [@bes-es1992]. Chauvenet notes that "in many cases it will suffice to take the extremely simple forms $a = \alpha' - b(\alpha - \alpha')$, $d = \delta' - b(\delta - \delta')$", with an error below 0.09 arcseconds, but the exact form costs nothing on a computer [@bes-chauvenet-1863].

**Step 3. Moon in the fundamental system.**
$$
x = r_\mathrm{m}\cos\delta_\mathrm{m}\sin(\alpha_\mathrm{m} - a)
$$
$$
y = r_\mathrm{m}\left[\sin\delta_\mathrm{m}\cos d - \cos\delta_\mathrm{m}\sin d\cos(\alpha_\mathrm{m} - a)\right]
$$
$$
z = r_\mathrm{m}\left[\sin\delta_\mathrm{m}\sin d + \cos\delta_\mathrm{m}\cos d\cos(\alpha_\mathrm{m} - a)\right]
$$
[@bes-es1961] [@bes-chauvenet-1863]. Equivalently $\mathbf{r}_F = (1/\sin\pi_\mathrm{m})\,\mathbf{R}_1(90^{\circ} - d)\,\mathbf{R}_3(a + 90^{\circ})\,\mathbf{r}_G$ [@bes-es1992].

**Step 4. Hour angle.**
$$
\mu = \theta - a
$$
with $\theta$ the Greenwich apparent sidereal time [@bes-es1992]. To match NASA, evaluate $\theta$ at UT1 $= t - \Delta T$ with a stated ΔT and record that ΔT with the table [@bes-nasa-2024-elements] [@bes-aravpanwar]. To follow the 1961 convention instead, evaluate the sidereal time at the TT instant as if it were UT, call the result the ephemeris sidereal time, and let users shift their longitudes by $1.002738\,\Delta T$ [@bes-es1961].

**Step 5. Cone half-angles.**
$$
\sin f_1 = \frac{\sin s_0 + k_1\sin\pi_0}{gR},\qquad
\sin f_2 = \frac{\sin s_0 - k_2\sin\pi_0}{gR}
$$
[@bes-es1961] [@bes-es1992]. With $s_0 = 959.63$ arcseconds and $\pi_0 = 8.794$ arcseconds, $\sin s_0 = 0.0046524$ and $\sin\pi_0 = 4.2634\times10^{-5}$. Note the 1961 numerators for $k = 0.272281$: 0.0046640009 and 0.0046407920 [@bes-es1961]. Tabulate $\tan f_1$ and $\tan f_2$ from these.

**Step 6. Vertex heights.**
$$
c_1 = z + \frac{k_1}{\sin f_1},\qquad c_2 = z - \frac{k_2}{\sin f_2}
$$
[@bes-es1961] [@bes-es1992].

**Step 7. Shadow radii on the fundamental plane.**
$$
l_1 = c_1\tan f_1,\qquad l_2 = c_2\tan f_2
$$
$l_2 < 0$ total, $l_2 > 0$ annular [@bes-es1961].

**Step 8. Repeat** steps 0 to 7 at each sample instant. The 1992 Supplement used a 10-minute grid "but for some instances additional calculations at an interval of 30 seconds or less are necessary", and took derivatives numerically [@bes-es1992].

**Step 9. Fit.** For publication, sample at $t = -2, -1, 0, +1, +2$ hours about $t_0$ and fit $a_0 + a_1 t + a_2 t^2 + a_3 t^3$ by least squares to each of $x, y, d, \mu, l_1, l_2$. NASA describes "a least-squares fit to elements calculated at five uniformly spaced times over a six hour period centered at $t_0$" [@bes-nasa-2024-elements] [@bes-nasa-1998-elements]. Miller's page shows the normal equations solved by Gauss-Jordan elimination and reports that $\mu$ needs only first degree and $d, l_1, l_2$ only second [@bes-celestialprogramming-gen]. The NASA CSV confirms: $\mu$ has a zero quadratic coefficient in every row inspected, $d, l_1, l_2$ have three coefficients, $x, y$ have four [@bes-nasa-csv]. Five samples and a cubic leave one degree of freedom, so the fit is nearly an interpolation. Publish $\tan f_1, \tan f_2$ at $t_0$.

**Step 10. Record metadata.** Ephemeris and version, TT reference $t_0$, ΔT, $k_1$, $k_2$, $s_0$, $\pi_0$, ellipsoid, and whether the lunar position is centre of mass [@bes-nasa-2024-elements] [@bes-ew-de405].

A check for the developer: with the NASA 2024 April 8 elements, $x^2 + y^2$ at $t = 0$ gives $\sqrt{0.318244^2 + 0.219764^2} = 0.3868$, and the catalogue's gamma of 0.34314 is the minimum of that distance at 18:18:29 TDT, the catalogued time of greatest eclipse [@bes-nasa-csv].

## Vector shortcut used by the Swiss Ephemeris

The Swiss Ephemeris skips $a, d, \mu$ and works in au with the unit vector $\mathbf{e}$ from Sun to Moon. Its code variable `s0` is the almanac's $z$, not the almanac's $s_0$, and it forms the shadow diameters on the fundamental plane directly:

```c
/* distance of moon from fundamental plane */
s0 = -dot_prod(rm, e);
/* distance of shadow axis from geocenter */
r0 = sqrt(dm * dm - s0 * s0);
/* diameter of core shadow on fundamental plane */
d0 = (s0 / dsm * (drad * 2 - dmoon) - dmoon) / cosf1;
/* diameter of half-shadow on fundamental plane */
D0 = (s0 / dsm * (drad * 2 + dmoon) + dmoon) / cosf2;
```

Here `drad` is the solar radius, `dmoon` the lunar diameter, `dsm` the Sun-Moon distance, and `sinf1 = (drad - rmoon)/dsm`, `sinf2 = (drad + rmoon)/dsm`, so `f1` is the umbral angle and `f2` the penumbral, the reverse of the almanac subscripts [@bes-swisseph-swecl]. Algebraically `d0/2` equals $c_2\tan f_2$ of the almanac and `D0/2` equals $c_1\tan f_1$. The flattening is applied before this by `rm[2] /= earthobl; rs[2] /= earthobl;` with `earthobl = 1 - EARTH_OBLATENESS` and `EARTH_OBLATENESS = 1/298.25642` [@bes-swisseph-swecl] [@bes-swisseph-header]. That trick maps the ellipsoid to a sphere of equatorial radius and is exact for deciding whether the axis meets the surface, but it is not how the almanacs treat the observer, and a developer mixing the two must not apply the flattening twice. The constants are `DSUN = 1392000000.0 / AUNIT`, `DMOON = 3476300.0 / AUNIT`, `DEARTH = 6378140.0 * 2 / AUNIT`, `AUNIT = 1.49597870700e+11` [@bes-swisseph-swecl] [@bes-swisseph-header]. The library documentation says the northern and southern limits of the umbra and penumbra "are not implemented yet" [@bes-swisseph-doc].

## Open-source generators found

The full repository inventory and its comparison matrix are in [GitHub repositories](../09-software-and-repos/github-repositories.md). This section keeps only what each repository does about generating elements. Searches were run for "besselian elements" with python, javascript, fortran, rust and C, for Skyfield-based eclipse code, and for the Swiss Ephemeris, Occult, USNO and IMCCE. Findings:

| Code | Language | Generates elements? | Ephemeris and constants | Validation stated |
|---|---|---|---|---|
| Swiss Ephemeris `swecl.c` [@bes-swisseph-swecl] | C | Computes the geometry live, no table | its own DE-derived files, $k$ from 1738.15 km, Sun 696,000 km, $f = 1/298.25642$ | none against NASA in the file |
| celestialprogramming.com generator [@bes-celestialprogramming-gen] | JavaScript | Yes, with the least-squares fit | apparent geocentric places, $k = 0.2725076$, Sun $6.957\times10^8$ m | none stated |
| solareclipses.com formulas page [@bes-solareclipses-formulas] | prose with formulas | Yes, 13 samples at 30-minute steps | "Equatorial Apparent of the Date", $a_e = 6378.1366$ km, Sun 959.95 arcseconds, $k = 0.272399309$ | none stated. Its $c_2 = -k/\sin f_2$ omits $z$ and looks like a transcription error |
| Eclipse-Engine (eclipseradar.com) [@bes-eclipse-engine] | JavaScript | No. Ships `data/eclipses.json` "fitted to the JPL DE440s ephemeris". The fitting is in an unpublished Python chain | DE440s | reference values from its own Python chain |
| aravpanwar/besselian [@bes-aravpanwar] | Python | No. Consumes NASA elements | NASA, $k_1 = 0.272488$, $k_2 = 0.272281$ | Sun altitude 81.69 vs 81.7 degrees and duration 382.5 s vs 06m23s at greatest eclipse 2027 |
| libephemeris [@bes-libephemeris] | Python on Skyfield | Partial. "Eclipse searches combine JPL states with published shadow-cone/Besselian geometry and public physical radii" | JPL via Skyfield | "sub-arcsecond" agreement with a reference API for eclipses, per README |
| umbra-rs [@bes-umbra-rs] | Rust | Planned. "Milestone 1 ... in progress", "must not be used" | planned | none |
| Skyfield itself [@bes-skyfield-801] | Python | No. The maintainer states that projecting the shadow cone is not implemented | DE4xx | not applicable |
| Miller's 5MCSE mirror [@bes-miller-5mcse-repo] | data | No. Repackages NASA's CSV as JSON and JavaScript | NASA VSOP87/ELP2000 | not applicable |

Negative findings: no Fortran or C code that generates elements from a JPL ephemeris with documented validation against the almanac was found. Occult's public tutorial mentions solar eclipses only in its feature list [@bes-occult-tutorial]. No IMCCE page describing its own Besselian-element computation was located in the searches run. The USNO eclipse computer describes a topocentric method, not elements [@bes-usno-eclipse-computer]. Yuk Tung Liu's derivation page returned an access error and a JavaScript-only stub, and the Observable notebook by Yamahata returned rate-limit errors on two attempts, so neither was read.

## Elements versus direct topocentric computation

The Besselian method answers the global questions cheaply: where the axis meets the ellipsoid, the outline of the umbra, the limits of the penumbra, the duration on the central line, all from six polynomials [@bes-ew-beselm]. Espenak's reason for the method is that "using a full ephemeris is more computationally involved", and the elements "are basically an ephemeris valid only over a short period of time (usually about five hours), reduced to a few polynomials" [@bes-ew-beselm]. Local circumstances from elements need the observer's $\xi, \eta, \zeta$ and an iteration on the equations of condition, as in sections 8.33 to 8.36 of the 1992 Supplement [@bes-es1992].

Direct topocentric computation skips the plane. At each trial time one computes the apparent topocentric positions of the Sun and Moon for the observer, their apparent semidiameters, and the angular separation of their centres, then finds the times when the separation equals the sum or difference of the semidiameters. The Swiss Ephemeris `eclipse_how()` is a compact example:

```c
rmoon = asin(RMOON / lm[2]) * RADTODEG;
rsun = asin(drad / ls[2]) * RADTODEG;
rsplusrm = rsun + rmoon;
rsminusrm = rsun - rmoon;
...
dctr = acos(swi_dot_prod_unit(x1, x2)) * RADTODEG;
if (dctr < rsminusrm) retc = SE_ECL_ANNULAR;
else if (dctr < fabs(rsminusrm)) retc = SE_ECL_TOTAL;
else if (dctr < rsplusrm) retc = SE_ECL_PARTIAL;
...
attr[0] = lsunleft / rsun / 2;   /* magnitude = (rsun + rmoon - dctr) / (2 rsun) */
```

with the positions requested after `swe_set_topo()` for the observer and at TT $= $ UT $+ \Delta T$ [@bes-swisseph-swecl]. The USNO eclipse computer does the same: "The computation of Eclipse Local Circumstances is started by iteratively computing topocentric positions of the Sun and Moon to find the time of Maximum Eclipse", using IAU radii of 696,000 km and 1737.4 km and no limb profile [@bes-usno-eclipse-computer]. Quaglia et al. go furthest: "Our computational model does not depend, like the traditional method, on Besselian elements ... to compute nominal predictions and then on applying limb corrections ... Instead, it performs its computations directly with the solar limb and the lunar limb profile to find times of contact and other related quantities. No approximating adjustments are involved" [@bes-quaglia-2021].

When each is used:

- Use elements for catalogues, maps, path limits, and any product that must be reproducible from a published table, and for matching NASA or the Almanac, because their constants and fits are documented [@bes-nasa-2024-elements].
- Use direct topocentric computation when the ephemeris is at hand and the question is local: contact times at one site, Baily's beads, flash-spectrum timing, eclipse solar radius. It removes the polynomial truncation, the constant $\tan f$ approximation, the ellipsoid auxiliaries, and the split of $k$ into two values, and it lets a limb profile replace $k$ entirely [@bes-quaglia-2021].
- The two agree to well under a second when the same ephemeris, radii and ΔT are used. The observed differences between predictors come from those inputs, not from the method. Quaglia et al. report Occult's Baily's beads tool giving durations 2 s or more longer than their model at the same site, and Solar Eclipse Maestro 4 s or more, attributed to limb handling [@bes-quaglia-2021].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Explanatory Supplement 1961, section 9B [@bes-es1961] | The list of required inputs, explicitly apparent places at ET instants, and the $b = \sin\pi_0/(R\sin\pi_\mathrm{m})$ scaling with $\pi_0 = 8.794$ arcseconds. |
| Explanatory Supplement 1992, sections 8.322 to 8.325 [@bes-es1992] | The rotation-matrix form, unit vectors, and the statement that in practice elements were computed on a 10-minute grid with numerical derivatives. |
| Swiss Ephemeris `swecl.c` and `sweph.h` [@bes-swisseph-swecl] [@bes-swisseph-header] | Working C for both the fundamental-plane geometry and the direct topocentric method, with every constant visible. |
| Miller, celestialprogramming.com [@bes-celestialprogramming-gen] | The five-sample least-squares fit written out. |
| NASA element pages and CSV [@bes-nasa-2024-elements] [@bes-nasa-csv] | The target format and numbers to validate against. |
| Quaglia et al. 2021 [@bes-quaglia-2021] | The refereed description of a fully topocentric, limb-based alternative with IAU 2006 Earth orientation, DE430 and LOLA/Kaguya elevation models. |
| Skyfield discussion 801 [@bes-skyfield-801] | The maintainer's statement that Skyfield does not project the shadow. |

## What a developer should do

1. Build a function `elements_at(t_tt)` that returns $(x, y, d, \mu, l_1, l_2, \tan f_1, \tan f_2, z)$ from apparent geocentric places of date, following steps 0 to 7 above, with $k_1, k_2, s_0, \pi_0, a_e, \Delta T$ as parameters.
2. Validate it against the 1961 Supplement worked example (1961 February 15 08h ET) [@bes-es1961] and against the NASA 2024 April 8 polynomial at $t = 0$ [@bes-nasa-csv], expecting agreement at the $10^{-5}$ Earth-radius level once the same ephemeris, $k$ and ΔT are used. Differences larger than $10^{-4}$ Earth radii in $x, y$ (about 640 m) point to a frame or aberration inconsistency.
3. Only then add the polynomial fit as an export format, and keep the rigorous per-instant function as the computational path for local circumstances.
4. Implement the direct topocentric method as a second, independent path and use the agreement of the two as a regression test.

## What this changes

The pipeline gets two computational paths from one ephemeris layer: an elements path for global products and a topocentric path for local products. The ephemeris layer must expose apparent geocentric places of date, apparent topocentric places, and a sidereal-time function that is consistent in its treatment of nutation. Nothing else in the design changes.

## Open questions

- Quantify the effect of using astrometric versus apparent places for the Sun and Moon on $x, y$: obtain or write a test comparing both against the NASA 2024 elements with the same DE ephemeris and ΔT.
- Obtain Meeus's *Elements of Solar Eclipses 1951-2200* to confirm its sampling scheme and whether it applies nutation to $\mu$.
- Obtain the Python chain behind Eclipse-Engine's `data/eclipses.json`, or the author's description of it, to see how DE440s was reduced to elements and what $k$ and ΔT were used [@bes-eclipse-engine].
- Read libephemeris's eclipse module source to see whether it is a port of `swecl.c`. The provenance document names no file [@bes-libephemeris].
- Obtain the 1992 Supplement's section 8.35 (general solar eclipse phenomena) in a clean scan to check the equations for the axis-ellipsoid intersection, which the optical character recognition of the available scan garbles.
