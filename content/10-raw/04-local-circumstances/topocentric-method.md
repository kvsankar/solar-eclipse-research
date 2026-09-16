---
title: The direct topocentric method
description: Finding contacts as the instants when the topocentric angular separation of Sun and Moon equals the sum or difference of their apparent semidiameters, and how USNO, Swiss Ephemeris, sunpy, Skyfield, astropy, PyEphem, Stellarium, Horizons and SPICE support it.
order: 2
status: working
updated: 2026-09-15
tags: [local-circumstances, topocentric, swiss-ephemeris, spice, skyfield, astropy]
---

::: summary
- **The method is one equation.** With $\delta(t)$ the topocentric angular separation of the centres and $r_s$, $r_m$ the apparent semidiameters, the exterior contacts are the roots of $\delta = r_s + r_m$, the interior contacts the roots of $\delta = |r_s - r_m|$, and maximum eclipse the minimum of $\delta$. USNO's Solar Eclipse Computer and Swiss Ephemeris both work this way [@loc-usno-sec] [@loc-swecl-c].
- **USNO iterates topocentric positions with IAU radii,** Sun 696000 km and Moon 1737.4 km, finds maximum first and then searches backwards and forwards for the contacts, and corrects the reported altitude for standard refraction [@loc-usno-sec].
- **Swiss Ephemeris `eclipse_when_loc` brackets the minimum separation with a shrinking three-point search.** It then finds the exterior contacts as zeros of $(r_s + r_m) - \delta$ over $\pm 2$ h and the interior contacts as zeros of $|r_s - r_m| - \delta$ over $\pm 2$ min. For the interior contacts the lunar radius is scaled by 0.99916, and that factor is $k = 0.272281$ in disguise [@loc-swecl-c].
- **The general-purpose libraries give the ingredients, not the product.** Skyfield's `separation_from()` on apparent topocentric positions, astropy's `get_body` plus `separation`, PyEphem's `separation()` and `radius`, Horizons' observer tables and SPICE's `gfsep_c` all yield $\delta(t)$ and the radii. None of them ships a solar-eclipse contact routine [@loc-skyfield-examples] [@loc-pyephem-quick] [@loc-horizons-manual] [@loc-spice-gfsep].
- **Two exceptions ship something.** sunpy's `eclipse_amount()` returns obscuration at an observer with a selectable lunar radius, and SPICE's `gfoclt_c` finds FULL, ANNULAR and PARTIAL occultation intervals for ellipsoid or DSK-shaped bodies from any observer defined as an SPK object [@loc-sunpy-eclipse-amount] [@loc-spice-gfoclt].
- **Frame mistakes are the usual bug.** astropy's `separation()` is evaluated in the frame of the first coordinate, so an ICRS separation is barycentric, not topocentric [@loc-astropy-common-errors]. Stellarium turns topocentric coordinates off to form Besselian elements and never uses the separation method for eclipses [@loc-stellarium-sec].
:::

**The question.** Instead of reducing published Besselian elements, a program with an ephemeris can compute the apparent topocentric positions of the Sun and Moon directly and find the instants at which their discs touch. What exactly does that computation consist of, which radii and corrections does each implementation use, and which libraries and services offer the pieces?

## The equation and its ingredients

At time $t$ the observer at geodetic position $(\phi, \lambda, h)$ sees the Sun's centre at apparent topocentric direction $\hat{s}$ and the Moon's at $\hat{m}$, with distances $D_s$ and $D_m$. The apparent semidiameters are $r_s = \arcsin(R_s/D_s)$ and $r_m = \arcsin(R_m/D_m)$ and the separation is $\delta = \arccos(\hat{s}\cdot\hat{m})$. Then

- first and fourth contact: $\delta = r_s + r_m$,
- second and third contact: $\delta = |r_s - r_m|$, total if $r_m > r_s$, annular if $r_m < r_s$,
- maximum eclipse: $\delta$ minimal,
- magnitude (partial): $(r_s + r_m - \delta)/(2r_s)$, and ratio $r_m/r_s$ once the discs nest,
- obscuration: the lens area of the two discs divided by $\pi r_s^2$, whose closed form is in [contact times, magnitude and position angles](contact-times-and-magnitude.md).

"Apparent topocentric" means the positions include light time for the Moon and Sun, aberration, and the diurnal parallax of the site with its height. Refraction is optional and, if applied, must be applied to both bodies before the separation is formed. The Besselian and the topocentric method agree to the extent that the ephemeris, the radii and $\Delta T$ agree: the Besselian elements are themselves a compressed geocentric ephemeris of the two bodies [@loc-es1992-ch8].

## USNO Solar Eclipse Computer

The USNO service describes its algorithm in three sentences: "The computation of Eclipse Local Circumstances is started by iteratively computing topocentric positions of the Sun and Moon to find the time of Maximum Eclipse", after which "another series of position computations is performed going backwards and forwards from the time of Maximum Eclipse to find the times of contacts", and "the solar and lunar angular diameters are calculated at each position using radius values adopted by the International Astronomical Union (Sun 696000 km; Moon 1737.4 km) to determine if contact conditions have occurred" [@loc-usno-sec]. The output gives "the time of each contact point, the Sun's topocentric position at that time, and its Position and Vertex Angles", with duration, magnitude and obscuration, and "the altitude is corrected for refraction assuming standard atmospheric conditions" [@loc-usno-sec]. The lunar radius 1737.4 km is $k = 1737.4/6378.137 = 0.27240$, between the IAU $0.2725076$ and the umbral $0.272281$ that NASA uses, so USNO durations differ from NASA's by construction. The page does not state the JPL ephemeris version or $\Delta T$ source [@loc-usno-sec].

## Swiss Ephemeris `swe_sol_eclipse_how` and `swe_sol_eclipse_when_loc`

The file swecl.c is the most complete open implementation of the topocentric method and was read in full [@loc-swecl-c].

**Constants.** `DSUN = 1392000000.0 / AUNIT`, `DMOON = 3476300.0 / AUNIT`, `RSUN = DSUN/2`, `RMOON = DMOON/2`, so the Sun's radius is 696000 km and the Moon's 1738.15 km ($k = 0.27252$) [@loc-swecl-c].

**Positions.** `eclipse_when_loc` sets `iflag = SEFLG_EQUATORIAL | SEFLG_TOPOCTR | ifl` and calls `swe_set_topo(geopos[0], geopos[1], geopos[2])`, so Sun and Moon are apparent topocentric equatorial vectors including the site height [@loc-swecl-c].

**Separation, radii and type**, from `eclipse_how` [@loc-swecl-c]:

```
rmoon = asin(RMOON / lm[2]) * RADTODEG;
rsun = asin(drad / ls[2]) * RADTODEG;
rsplusrm = rsun + rmoon;
rsminusrm = rsun - rmoon;
dctr = acos(swi_dot_prod_unit(x1, x2)) * RADTODEG;
if (dctr < rsminusrm)            retc = SE_ECL_ANNULAR;
else if (dctr < fabs(rsminusrm)) retc = SE_ECL_TOTAL;
else if (dctr < rsplusrm)        retc = SE_ECL_PARTIAL;
```

**Magnitude and obscuration** [@loc-swecl-c]:

```
attr[1] = rmoon / rsun;                       /* ratio of diameters */
lsunleft = (-dctr + rsun + rmoon);
attr[0] = lsunleft / rsun / 2;                /* fraction of solar diameter covered */
...
attr[2] = (sc1 + sc2) * 2 / PI / lsun / lsun; /* obscuration, partial case */
attr[8] = attr[0]; if (retc & (SE_ECL_TOTAL | SE_ECL_ANNULAR)) attr[8] = attr[1];  /* NASA magnitude */
```

where `sc1 = a*lmoon^2/2 - cos(a)sin(a)*lmoon^2/2` and `sc2 = b*lsun^2/2 - cos(b)sin(b)*lsun^2/2` with `a = acos((lctr^2 + lmoon^2 - lsun^2)/(2 lctr lmoon))` and `b = acos((lctr^2 + lsun^2 - lmoon^2)/(2 lctr lsun))`, clamped to $[-1, 1]$; total and annular return `lmoon^2/lsun^2` or 1 [@loc-swecl-c]. The programmer's manual documents `attr[0]` as "fraction of solar diameter covered by moon; with total/annular eclipses, it results in magnitude acc. to IMCCE" and `attr[8]` as "magnitude acc. to NASA; = attr[0] for partial and attr[1] for annular and total eclipses" [@loc-swephprg].

**Maximum.** A first guess comes from the Meeus lunar-phase polynomial for new Moon. It is then refined by a bracketing loop, `for (dt = dtstart; dt > 0.00001; dt /= dtdiv)`. Each pass evaluates the separation at $t - dt$, $t$ and $t + dt$, calls `find_maximum` on the parabola through the three points, and moves $t$ to the fitted extremum [@loc-swecl-c].

**Contacts.** For the exterior contacts the quantity $(r_s + r_m) - \delta$ is evaluated at $t - 2$ h, $t$ and $t + 2$ h. `find_zero(dc[0], dc[1], dc[2], twohr, &dt1, &dt2)` returns the two roots of the parabola through the three points. Those roots are then re-refined with `tensec = 10/(24*3600)` brackets. Interior contacts use $|r_s - r_m| - \delta$ with `twomin = 2/(24*60)` brackets, and before forming them the code does [@loc-swecl-c]:

```
rmoon = asin(RMOON / dm) * RADTODEG;
rmoon *= 0.99916; /* gives better accuracy for 2nd/3rd contacts */
```

$0.99916 \times 1738.15\ \text{km} = 1736.69\ \text{km}$, and $0.272281 \times 6378.137\ \text{km} = 1736.65\ \text{km}$, 40 m from the scaled value. The scale factor is the NASA umbral $k$ applied to the interior contacts only, the same convention as the Five Millennium Canon, NASA/TP-2006-214141 [@loc-5mcse-text] [@loc-eclipsewise-radius].

**Refraction and visibility.** `swe_azalt` returns true and apparent altitude, stored as `attr[5]` and `attr[6]`. The visibility flag uses an approximate minimum apparent height, `hmin_appr = -(34.4556 + (1.75 + 0.37) * sqrt(geohgt)) / 60`. The first term is horizon refraction from Bennett's formula. The other two are the dip of the horizon and the refraction between horizon and observer, both scaling with the square root of the height [@loc-swecl-c]. Refraction is never applied to the separation itself, so contact times are unrefracted. `tret[5]` and `tret[6]` carry sunrise and sunset between first and fourth contact when they occur [@loc-swephprg].

**Output.** `tret[0]` maximum, `tret[1]` to `tret[4]` the four contacts, `attr[3]` the core-shadow diameter from `eclipse_where`, `attr[4]` azimuth, `attr[7]` the separation [@loc-swephprg] [@loc-swecl-c].

## sunpy `eclipse_amount`

sunpy provides `sunpy.coordinates.sun.eclipse_amount(observer, *, moon_radius='IAU')`, which returns the obscuration at an observer `SkyCoord` for its time, "using the simplifying assumption that the Moon has a constant radius". The `'IAU'` option is $R_\mathrm{moon}/R_\mathrm{earth} = 0.2725076$ and `'minimum'` is $0.272281$, the latter "more accurate for total eclipse contact predictions but less accurate for partial eclipse measurements" in the documentation's paraphrase. Light travel time is included. The docstring recommends a JPL ephemeris because astropy's built-in lunar position "is appreciably inaccurate" [@loc-sunpy-eclipse-amount]. Contact times are not returned. A root finder on this function against 0, and on $1 - \mathrm{amount}$, reproduces them.

## Skyfield

Skyfield has no eclipse function. Issue #807 proposes the detector [@loc-skyfield-807]:

```python
bluffton = eph['earth'] + wgs84.latlon(40.197303, -89.626094 * E, elevation_m=0)
sun = bluffton.at(time).observe(eph['sun']).apparent()
moon = bluffton.at(time).observe(eph['moon']).apparent()
elongation_degrees = sun.separation_from(moon).degrees
```

The `.apparent()` call applies light time, aberration and deflection, and `wgs84.latlon` with `elevation_m` gives the topocentric origin. Apparent radii come from the documented pattern `Angle(radians=np.arcsin(radius_km / distance.km) * 2.0)` for the angular diameter [@loc-skyfield-examples]. The documentation's `find_discrete` and `find_minima` almanac searchers can then locate the roots of $\delta - (r_s \pm r_m)$ and the minimum of $\delta$. Skyfield's examples page has lunar-eclipse support but no solar-eclipse example and no contact-time function [@loc-skyfield-examples].

## astropy

astropy gives `get_body("moon", time, loc)` and `get_body("sun", time, loc)` for an `EarthLocation`, and `moon.separation(sun)`. Erik Bernhardsson's 2024 note uses exactly that pair and minimises the separation with scipy's Nelder-Mead to find where on Earth the eclipse is central, without computing contacts or obscuration [@loc-erikbern-2024]. The astropy documentation's "Common mistakes" page warns that `separation()` is computed in the frame of the coordinate it is called on, so `star.separation(moon)` in ICRS is a barycentric separation while `moon.separation(star)` from a geocentric or topocentric frame is the observed one [@loc-astropy-common-errors]. No open astropy issue proposing a solar-eclipse contact routine was found in the searches run for this note. The feature lives in sunpy instead [@loc-sunpy-eclipse-amount].

## PyEphem

PyEphem bodies expose `radius` ("size (radius as an angle)") and `size` in arcseconds, `separation()` gives the angle between two positions, and `Observer` carries `elevation`, `pressure` and `temperature` so that apparent positions "include an adjustment to simulate atmospheric refraction". There is no eclipse function [@loc-pyephem-quick]. Setting `pressure = 0` removes refraction, as a contact computation requires.

## JPL Horizons

Horizons has no eclipse or occultation product. Its observer tables, from a topocentric site with an optional refraction model, list apparent RA and Dec, the angular diameter, elongation and range rates for one target at a time, from which two tables yield $\delta(t)$ and the radii, one for the Sun and one for the Moon at identical times [@loc-horizons-manual]. Horizons is therefore a validation oracle for a local ephemeris rather than a contact calculator.

## SPICE `gfoclt_c` and `gfsep_c`

`gfoclt_c` "determines time intervals when an observer sees one target body occulted by, or in transit across, another". Occultation types are FULL ("the full occultation of the body designated by back by the body designated by front"), ANNULAR ("front blocks part of, but not the limb of, back"), PARTIAL ("front blocks part, but not all, of the limb of back") and ANY, which "must be used if either the front or back target body is modeled as a point". Shapes are ELLIPSOID from the kernel-pool radii, POINT, and DSK for topographic models. Aberration corrections are NONE, LT, CN, XLT and XCN. "The step size should be shorter than the shortest occultation duration and the shortest time interval between two occultation events", and roots are accepted when bracketed within `SPICE_GF_CNVTOL`. The first documented example finds the December 2001 solar eclipse as an 85 minute interval of Moon occulting Sun as seen from Earth's centre [@loc-spice-gfoclt]. To use a surface site as the observer, the site must exist as an SPK object, which NAIF's `pinpoint` utility produces from a body-fixed position; the documentation does not spell this out but the observer argument is a body name. With DSK shapes the Moon's actual limb is used. That is the only library route found in this topic that folds a limb model into contact times without a separate post-correction.

`gfsep_c` complements it: "determine time intervals when the angular separation between the position vectors of two target bodies relative to an observer satisfies a numerical relationship", with shapes SPHERE and POINT and relations `=`, `<`, `>`, `LOCMIN`, `LOCMAX`, `ABSMIN`, `ABSMAX`. A SPHERE takes its radius as the maximum of `BODYnnn_RADII`. With SPHERE the separation is measured between the limbs rather than the centres, so `= 0` with SPHERE for both bodies is the exterior contact condition and `ABSMIN` gives maximum eclipse [@loc-spice-gfsep].

## Stellarium

Stellarium does not use the separation method for its eclipse tables. `calcSolarEclipseBessel()` switches topocentric coordinates off and takes the geocentric apparent RA and Dec of Sun and Moon. From them it forms $x$, $y$, $d$, $\mu$, $L_1$, $L_2$, $\tan f_1$ and $\tan f_2$ with `SunEarth = 109.12278` (696000/6378.1366), `k = 0.2725076` and `s = 0.272281`. The comment reads "we will use two values (same with NASA), because durations seem to agree with NASA" [@loc-stellarium-sec]. The local circumstances then follow the Besselian route in `localSolarEclipse` [@loc-stellarium-astrocalc]. The maintainers described the feature in 2022 as new, with contact times for lunar eclipses and solar eclipse maps as later enhancements [@loc-stellarium-disc-2370]. The on-screen rendering, by contrast, is topocentric by default, so what the user sees in the sky view and what the AstroCalc table reports are computed by two different methods.

## Sources compared

| Implementation | Positions | Radii | Contact search | Refraction | Ships contacts |
|---|---|---|---|---|---|
| USNO Solar Eclipse Computer [@loc-usno-sec] | Topocentric, JPL (version unstated) | 696000 km, 1737.4 km | Iterate to maximum, then step out | Altitude only | Yes, with P, V |
| Swiss Ephemeris [@loc-swecl-c] | Topocentric apparent, `SEFLG_TOPOCTR` | 696000 km, 1738.15 km, x0.99916 inside | Parabolic bracketing, 10 s then finer | Visibility only | Yes, plus sunrise/sunset |
| sunpy [@loc-sunpy-eclipse-amount] | astropy topocentric with light time | 0.2725076 or 0.272281 | None (user root-finds) | None | Obscuration only |
| Skyfield [@loc-skyfield-807] | Apparent topocentric | User supplies | User uses `find_discrete` | Optional via altaz | No |
| astropy [@loc-erikbern-2024] | `get_body` at EarthLocation | User supplies | User | None in separation | No |
| PyEphem [@loc-pyephem-quick] | Topocentric with refraction by default | `radius` attribute | User | On unless pressure = 0 | No |
| Horizons [@loc-horizons-manual] | Topocentric tables | Angular diameter column | User | Optional model | No |
| SPICE gfoclt [@loc-spice-gfoclt] | Any SPK observer, LT or CN | Ellipsoid or DSK | Built-in interval search | None | Intervals of FULL, ANNULAR, PARTIAL |

## What a developer should do

Build the topocentric method as the independent check of the Besselian reduction, not as a replacement. Use a JPL ephemeris through Skyfield or sunpy, with apparent topocentric positions that include light time and aberration and exclude refraction. Fix the radii at $R_s = 696000$ km and $R_m = 0.2725076\,R_e$ for exterior contacts and $0.272281\,R_e$ for interior contacts to match NASA. Find the contacts with a bracketed root finder on $\delta - (r_s \pm r_m)$ seeded from the minimum of $\delta$ [@loc-usno-sec] [@loc-swecl-c] [@loc-sunpy-eclipse-amount]. Agreement with the Besselian result should be within 0.1 s when the same ephemeris and $\Delta T$ feed both. Read swecl.c `eclipse_when_loc` for the search structure and `eclipse_how` for the obscuration code, and gfoclt_c's documentation for the DSK route to a limb-aware contact.

## What this changes

Nothing in the pipeline's data flow. It adds a second, cheaper validation path. Any site-level number from the Besselian path can be reproduced from the raw ephemeris in a few dozen lines. That is the test to run whenever the element generator changes.

## Open questions

- Obtain the JPL ephemeris version and $\Delta T$ source behind the USNO Solar Eclipse Computer, which the service page does not state [@loc-usno-sec].
- Run gfoclt_c with a `pinpoint`-defined surface site, ELLIPSOID for the Sun and a DSK Moon from LOLA, and record how its FULL interval compares with a limb-corrected C2 to C3 from Occult or Solar Eclipse Maestro.
- Locate the astropy or astroplan issue tracker entry, if any, that proposes solar-eclipse contact support. None surfaced in this note's searches.
