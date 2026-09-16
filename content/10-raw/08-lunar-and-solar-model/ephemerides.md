---
title: Lunar and solar ephemerides
description: Which ephemeris to feed an eclipse computation, what each JPL DE release changed for the Moon, how INPOP, EPM, ELP and VSOP compare, and where the errors land on the ground.
order: 1
status: working
updated: 2026-09-15
tags: [ephemeris, jpl-de, de440, inpop, elp, vsop87, spk, tdb]
---

::: summary
- **The Moon's orbit is known to centimetres, the eclipse path to metres.** DE440 fits lunar laser ranging with a recent rms residual of about 1.3 cm, and the DE430 to DE421 change in the Moon's sky position was under 0.5 milliarcseconds, which is under 1 m of shadow displacement on the ground [@moon-park-2021] [@moon-williams-2013].
- **Use DE440 for any 2020s product**, or the 1849 to 2150 excerpt `de440s.bsp` at 31 MB. DE441 is the same fit without the lunar core-mantle damping term and is only for dates outside 1550 to 2650 [@moon-naif-summaries] [@moon-jpl-eph-export].
- **The `t` variants carry TT minus TDB as a pseudo-body.** TT is printed as TDT or TD in NASA tables and was called ET before 1984. de440t.bsp exposes body 1000000001 relative to 1000000000 with TT minus TDB in seconds as the x component. The lunar libration Euler angles ship separately as the binary PCK moon_pa_de440_200625.bpc [@moon-jpl-bsp-readme] [@moon-naif-pck-dir].
- **ELP-2000/82 and VSOP87 remain adequate for path products but not for limb work.** The Five Millennium Catalog, NASA/TP-2009-214174, truncates ELP-2000/82 at 0.0005 arcseconds and reports a resulting timing error near 1/40 s, far below ΔT and limb uncertainty [@moon-espenak-meeus-canon].
- **INPOP21a and EPM2021 are independent integrations of the same class.** INPOP21a fits 27,899 LLR normal points to 2020 with recent station residuals of 1.0 to 1.3 cm. All three families ship SPICE kernels [@moon-fienga-2021] [@moon-iaa-epm].
- **The Sun's own position matters at the arcminute level.** The Sun wanders up to about 1.6 solar radii from the solar-system barycentre. Elements must use the Sun's centre (SPICE body 10), not the barycentre (body 0) [@moon-folkner-2014].
- **Mixing time scales or reduction levels is the usual bug.** ΔT of 69 s mistaken between TT and UT moves the path 32 km in longitude at the equator. A geometric Sun paired with an apparent Moon is a 20.5 arcsecond error and a 38 km path shift [@moon-es-1992] [@moon-skyfield-positions].
:::

**The question.** An eclipse computation needs the geocentric position of the Moon and of the Sun, in a known frame and time scale, at the level of a few metres on the ground. This note records which ephemerides supply that, what each JPL Development Ephemeris (DE) release changed for the Moon, what the independent French (INPOP) and Russian (EPM) integrations offer, how far the semi-analytical theories ELP and VSOP87 that Meeus and the Five Millennium Catalog use fall behind, and how each choice lands in arcseconds on the sky, seconds of contact time and kilometres of path.

## What an ephemeris supplies and how it is built

A modern planetary and lunar [?ephemeris] is a numerically integrated orbit fitted to observations. For DE430 and DE431 JPL states that "the present-day lunar orbit is known to submeter accuracy through fitting lunar laser ranging data with an updated lunar gravity field from the Gravity Recovery and Interior Laboratory (GRAIL) mission" [@moon-folkner-2014]. The Moon is the best-determined body in the file. The inner planets are known to sub-kilometre accuracy, and the ephemeris orientation is "tied to the International Celestial Reference Frame with an accuracy of 0.0002" arcseconds through VLBI of Mars orbiters [@moon-folkner-2014].

The coordinate frame is the [?icrf|ICRS realised by the ICRF]. The DE430 report says the axes are "aligned with the International Celestial Reference System (ICRS), with the XY plane close to the mean equator of epoch J2000.0 and the X axis close to the intersection of the mean equator of J2000.0 with the mean ecliptic plane", realised by ICRF2 [@moon-folkner-2014]. DE440 moved to ICRF3 [@moon-park-2021]. The ICRS axes differ from the old J2000 dynamical axes by a constant frame bias of about 0.02 arcseconds, which Skyfield documents as the reason "many scripts simply treat J2000 coordinates as modern ICRS coordinates" [@moon-skyfield-positions]. For eclipse work 0.02 arcseconds is 37 m on the ground and can be ignored unless the rest of the chain is at that level.

The independent variable is [?tdb|Barycentric Dynamical Time]. "The coordinate time scale used for DE430 and DE431 is Barycentric Dynamical Time (TDB) as defined in terms of Barycentric Coordinate Time (TCB)" with "TT = TAI + 32.184 s" as the intermediate scale [@moon-folkner-2014]. The IAU definition is a linear transformation of TCB,

$$\mathrm{TDB} = \mathrm{TCB} - L_B \,(\mathrm{JD}_{\mathrm{TCB}} - T_0)\, 86400\ \mathrm{s} + \mathrm{TDB}_0,$$

with $L_B = 1.550519768 \times 10^{-8}$ and $\mathrm{TDB}_0 = -6.55 \times 10^{-5}$ s [@moon-iers-2010-ch10]. The DE430 report gives the full integrated expression for TDB minus TT as a function of the Earth's velocity and the gravitational potential at the geocentre, and notes that only the Sun's oblateness is included among figure effects [@moon-folkner-2014]. The periodic part has an amplitude near 1.7 ms. The Moon moves about 0.5 arcseconds per second against the stars, so ignoring TT minus TDB altogether costs under 1 milliarcsecond, which is negligible for eclipses. Confusing [?tt|Terrestrial Time] with Universal Time is not negligible and is covered under pitfalls below.

## The JPL DE series: what each release changed for the Moon

### DE200 (1981)

DE200 and its lunar part LE200 were the basis of the Astronomical Almanac from 1984 and of the NASA eclipse bulletins through the 2001 eclipse: "The solar and lunar ephemerides were generated from the JPL DE200 and LE200, respectively" [@moon-espenak-2001-bulletin]. DE200 is referred to the dynamical equinox of J2000 rather than to the ICRS. Espenak's older long-range predictions for 1991 to 2030 used even earlier sources, "j=2 ephemerides for the Sun [Newcomb, 1895] and Moon [Brown, 1919, and Eckert, Jones and Clark, 1954]" with a secular acceleration of −26 arcseconds per century squared and a −0.6 arcsecond latitude correction for the centre of figure [@moon-espenak-2001-bulletin].

### DE405 and DE406 (1997)

DE405 was the first release aligned to the ICRF and covers 1600 to 2200. DE406 is the long version, −3000 to +3000, at reduced precision [@moon-skyfield-planets]. Standish's DE405 memo exists only as a scanned PDF at JPL and could not be text-extracted at the time of writing (2026 September). The DE421 memo characterises DE405's weakness: "For DE 405 the lunar orbit was not fit in a way consistent with the other planets", and "the error in the Earth and Mars orbits in DE 405, is now known to be about 2 km" [@moon-folkner-2009]. Espenak's EclipseWise predictions for 2024 April 8 still state "Predictions for the Total Solar Eclipse of 2024 Apr 08 were generated using the JPL DE405 solar and lunar ephemerides" [@moon-eclipsewise-2024]. Swiss Ephemeris quotes its Moshier fallback as accurate to "0.5 arc second relative to DE404" [@moon-swisseph].

### DE421 (2008)

DE421 was "integrated over the time period 1900 to 2050" and was "a combined fit of lunar laser ranging (LLR) and planetary measurements", described as "a major improvement over the widely distributed DE 405" for the Moon, with the lunar orbit "known to sub-meter accuracy" [@moon-folkner-2009]. The lunar memo puts the DE421 minus DE403 position difference at "about 6 m in 2008, increasing to ~8 m in 2012, ~11 m in 2015, and ~16 m in 2020", or "about 3, 4, 6, and 9 milliseconds of arc" [@moon-williams-2008]. The IAU Working Group on Cartographic Coordinates adopted DE421 as "the best currently available lunar ephemeris" in its 2009 report [@moon-archinal-2011]. The de421.bsp kernel is 17 MB [@moon-skyfield-planets].

### DE430 and DE431 (2013)

DE430 covers 1550 to 2650 and DE431 covers −13,200 to +17,191 [@moon-folkner-2014]. The two share one fit and differ in the lunar dynamical model: "The dynamical model for DE430 included a damping term between the Moon's liquid core and solid mantle that gives the best fit to lunar laser ranging data but that is not suitable for backward integration of more than a few centuries" [@moon-folkner-2014]. Because "the initial conditions of the lunar core cannot be determined perfectly, error grows in backward integrations", so "the DE430 time span has been limited to the years 1550 to 2650" [@moon-folkner-2014]. The lunar orbits of the two "differ by less than 1 m during the time span of the LLR data, 1970 to 2012" [@moon-folkner-2014].

The LLR fit used "18,548 ranges extending from March 16, 1970 to December 18, 2012", with "weighted rms 1.9 cm for the past 4 yr" [@moon-williams-2013]. Compared with DE421, "the right ascension and declination differences reach up to ~1 m perpendicular to the radius, or up to ~1/2 milliarcsecond (mas) in angle" [@moon-williams-2013]. DE430 was the first release to ship an integrated TT minus TDB in the SPICE kernels, "starting with DE430 released March 2013" [@moon-jpl-bsp-readme].

### DE440 and DE441 (2020)

DE440 keeps the 1550 to 2650 span and DE441 the −13,200 to +17,191 span [@moon-park-2021]. The lunar changes were that "the effect of geodetic precession on lunar librations has been added as well as the solar radiation pressure force on the Earth–Moon system orbits", with LLR "extended through 2020 March" [@moon-park-2021]. Residuals: "The rms residual of the early LLR data (~1970–1980) is about 20 cm while the rms residual of the recent LLR data is about 1.3 cm" [@moon-park-2021]. The frame is ICRF3 [@moon-park-2021]. The recommendation is explicit: "DE440 is recommended for analyzing modern data while DE441 is recommended for analyzing historical data earlier than the modern range data" [@moon-park-2021]. JPL's export page quantifies the divergence: "DE441 differs from DE440 mainly in the estimated tidal damping term causing a difference in along-track position of the Moon of ~10 meters 100 years from the present" [@moon-jpl-eph-export].

### DE442 (2024)

DE442 "was created in May 2024 with the primary purpose of updating the ephemeris of the Uranus barycenter to support the development of the Uranus satellite ephemeris URA182", and "is essentially an update of the planetary ephemeris DE440, incorporating Uranus occultation data as well as additional Mars orbiter ranging data and Juno ranging data spanning an additional four years" [@moon-naif-de442-comments]. The comments do not describe any lunar change. No separate lunar orientation PCK for DE442 is listed at NAIF, and the DE440 PA kernel remains the current lunar orientation product [@moon-naif-pck-dir]. Treat DE442 as DE440 for the Moon until JPL says otherwise.

## Files, formats and readers

JPL exports each DE in three forms: ASCII blocks "created in blocks of 20 or more years", machine-dependent binaries, and "machine-independent binary format (kernels)" for SPICE. Directories are https://ssd.jpl.nasa.gov/ftp/eph/planets/ascii/, https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/, https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/ and https://ssd.jpl.nasa.gov/ftp/eph/planets/SunOS/ [@moon-jpl-eph-export]. The [?spk-kernel|SPK kernels] and their validity spans as listed by NAIF are:

| Kernel | Span | Size | Note |
|---|---|---|---|
| de405.bsp | 1600 to 2200 | 63 MB | ICRF-aligned, superseded [@moon-skyfield-planets] |
| de421.bsp | 1900 to 2050 | 17 MB | 2008 fit [@moon-skyfield-planets] |
| de430.bsp | 1549 Dec 31 to 2650 Jan 25 | 128 MB (de430t) | first with TT−TDB in `t` file [@moon-naif-summaries] [@moon-skyfield-planets] |
| de430_1850-2150.bsp | 1850 to 2150 | 31 MB | excerpt [@moon-skyfield-planets] |
| de431_part-1/2.bsp | 13201 BC to 17191 AD | 3.5 GB | long span, no core damping [@moon-naif-summaries] |
| de440.bsp | 1549 Dec 31 to 2650 Jan 25 | 114 MB | recommended [@moon-naif-summaries] [@moon-naif-planets-dir] |
| de440s.bsp | 1849 Dec 26 to 2150 Jan 22 | 31 MB | recommended excerpt [@moon-naif-summaries] |
| de440t.bsp | 1550 to 2650 | 146 MB | adds TT−TDB segment [@moon-jpl-bsp-dir] |
| de441_part-1/2.bsp | 13201 BC to 17191 AD | 3.1 GB | historical eclipses [@moon-naif-summaries] |
| de442.bsp, de442s.bsp | as DE440 | 114 MB, 31 MB | Uranus update, 2025-02 [@moon-naif-planets-dir] |

Skyfield's guidance is to "choose the shortest ephemeris that will cover the dates your project needs", because "the most recent short-term ephemerides DE430 and DE440 are more accurate than their long-term counterparts DE431 and DE441 because the shorter files include the effect of the Moon's liquid core", and it singles out de440s as "only twice the size of DE421 while delivering higher accuracy plus an extra century of data" [@moon-skyfield-planets]. Skyfield can also build an excerpt of a larger file over HTTP range requests [@moon-skyfield-planets].

Every DE kernel stores the Moon as segment 3 to 301 (Earth-Moon barycentre to Moon) and the Earth as 3 to 399. jplephem exposes exactly this: "Earth Barycenter (3) -> Moon (301)" and "Earth Barycenter (3) -> Earth (399)", evaluated as `kernel[center, target].compute(jd)` in kilometres with the time given as a TDB Julian date [@moon-jplephem-pypi]. Positions are stored as [?chebyshev|Chebyshev polynomials] (SPK type 2) with velocity from the derivative [@moon-jplephem-pypi]. The geocentric Moon is therefore (3→301) minus (3→399). Skyfield's remark that "only the Earth and Pluto have such massive moons that their system barycenters are poor approximations for the position of the planets themselves" is the reason the subtraction must be done rather than treating segment 3 as the Earth [@moon-skyfield-planets].

TT minus TDB: "This may be accessed by requesting the state (position and velocity) of body 1000000001 with respect to center 1000000000, with the value of TT-TDB in seconds returned as the 'x' component, and the rate of change, d(TT-TDB)/d(TDB) in seconds/second returned as the 'Vx' component" [@moon-jpl-bsp-readme]. A higher-order refit for DE430 exists as TTmTDB.de430.19feb2015.bsp [@moon-jpl-bsp-readme].

Lunar orientation: the SPK holds no libration. The DE440 [?lunar-euler-angles|Euler angles] are published as the binary PCK moon_pa_de440_200625.bpc (12 MB, 1549 Dec 31 to 2650 Jan 25), which "contains high-accuracy lunar orientation data from the JPL Solar System Dynamics Group's planetary ephemeris DE440" and gives "the orientation of the lunar Principal Axes (PA) reference frame defined by DE440, relative to the ICRF" [@moon-naif-moon-pa-de440-cmt] [@moon-naif-pck-dir]. Earlier PCKs are `moon_pa_de421_1900-2050.bpc` at 1.7 MB and `moon_pa_de403_1950-2198.bpc` [@moon-naif-pck-dir]. The matching frame kernel is named two ways in the literature. Wright and Young's paper cites `moon_de440_200625.tf`, the 2020 release, and NAIF now serves `moon_de440_250416.tf`, the 2025 revision of the same DE440 frame [@moon-naif-moon-fk-de440] [@moon-naif-pck-dir]. The ASCII and raw-binary DE distributions do include the libration angles inline, which is what the IAU working group meant when it wrote that "polynomial representations of the (Euler) lunar libration angles and their rates in the PA system are stored in the ephemeris file" [@moon-archinal-2011]. The frames themselves are in [lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md).

## INPOP (IMCCE, Paris)

INPOP is the French integration. INPOP19a "includes orbital solutions of the Sun, the eight planets, the dwarf planet Pluto and the Moon, the libration of the Moon", in kilometres relative to the ICRF, plus "the time scale transformations TT‑TDB and TCG‑TCB", and is distributed in four formats: extended JPL-style binaries with the time transformations, ASCII Chebyshev files, SPICE kernels, and JPL-compatible binaries without the time transformations [@moon-imcce-inpop19a] [@moon-imcce-inpop]. Spans offered are ±100 and ±1000 years from J2000 [@moon-imcce-inpop19a].

INPOP21a, published as IMCCE Notes Scientifiques et Techniques S110 in June 2021, extended LLR "to 2020/06/01 totaling 27899 normal points" [@moon-fienga-2021]. Its post-fit LLR residuals (one-way weighted rms) are 1.06 to 1.75 cm for APOLLO 2006 to 2016 and 1.01 to 1.33 cm for Grasse 2009 to 2020, against 14 to 55 cm for 1969 to 1986 stations [@moon-fienga-2021]. INPOP's lunar solution is documented separately by Viswanathan et al. for INPOP17a, "obtained through the numerical integration of the equations of motion and of rotation of the Moon, fitted over 48 years of Lunar Laser Ranging (LLR) data" [@moon-viswanathan-2018]. INPOP21a reports its planetary differences from DE440 (for Jupiter "from about 180 m between DE438 and INPOP19a to 70 m from DE440 and INPOP21a over the period 1980:2040") but the document read here gives no Moon-versus-DE440 figure in metres [@moon-fienga-2021]. Given that both fit the same LLR set to about 1 cm, the lunar difference is at the metre level and irrelevant to eclipses.

## EPM (IAA RAS, St Petersburg)

EPM2021 covers "more than 400 years (1787–2214)", includes "TT-TDB and Euler angles for lunar physical libration", and is supplied "in SPK and PCK formats, also known as the SPICE formats" from http://ftp.iaaras.ru/pub/epm/EPM2021. EPM2021H is the same over "13199 BC to AD 17191" [@moon-iaa-epm]. No accuracy comparison with DE was found on the IAA page.

## Semi-analytical theories: ELP and VSOP87

The Five Millennium Catalog, NASA/TP-2009-214174, states its sources. "The coordinates of the Sun used in these eclipse predictions have been calculated on the basis of the VSOP87 theory constructed by Bretagnon and Francou (1988)", using "version D of VSOP87 (this version provides the positions referred to the mean equinox of the date)". For the Moon "use has been made of the theory ELP-2000/82 of Chapront-Touzé and Chapront (1983)", with "37,862 periodic terms, namely 20,560 for the Moon's longitude, 7,684 for the latitude, and 9,618 for the distance" [@moon-espenak-meeus-canon]. The Catalog program "neglects all periodic terms with coefficients smaller than 0.0005 arcsec in longitude and latitude, and smaller than 1 m in distance", giving "a mean error (as compared to the full ELP theory) of about 0.0006 s of time in right ascension, and about 0.006 arcsec in declination" and "error in the calculated times of the phases of a solar eclipse ... of the order of 1/40 s" [@moon-espenak-meeus-canon]. The Catalog also adopts improved mean arguments from Chapront, Chapront-Touzé and Francou (2002) so that the secular acceleration is −25.858 arcseconds per century squared, consistent with LLR, and it corrects Morrison and Stephenson's ΔT (which assumed −26 arcseconds per century squared) by $c = -0.000012932\,(y-1955)^2$ seconds [@moon-espenak-meeus-canon].

ELP2000-82B is the version whose "constants of the subsequent lunar ephemeris are fitted to the numerical integration DE200/LE200" [@moon-imcce-elp82b-readme]. The files ELP1 to ELP36 and the notice elp82b.ps are at https://ftp.imcce.fr/pub/ephem/moon/elp82b/ [@moon-imcce-elp82b-readme]. ELP/MPP02, published by Chapront and Francou in A&A 404, 735, 2003, reworked the planetary perturbations and is distributed with two constant sets, one fitted to LLR and one to DE405, which the third-party Python port exposes as "LLR (mode=0; default) or DE405 (mode=1; 'historical')" [@moon-chapront-francou-2003] [@moon-elp-mpp02-pypi]. The A&A abstract with its accuracy figures could not be fetched, because the publisher and ADS both refused, so no ELP/MPP02-versus-DE number is quoted here. Meeus's Astronomical Algorithms chapter 47 uses a heavily truncated ELP-2000/82 and states an accuracy of about 10 arcseconds in longitude and 4 arcseconds in latitude. That statement is transcribed from the printed book, not from a fetched artefact [@moon-meeus-1998].

VSOP87's own notice gives the accuracy: the inner-planet series carry "a precision of 1\" for 4000 years before and after J2000", with a relative precision for the Earth of $2.5 \times 10^{-8}$ [@moon-imcce-vsop87-doc]. Version D is in spherical variables referred to the equinox and ecliptic of date, versions A, B and E to J2000 [@moon-imcce-vsop87-doc].

Translating these into eclipse error uses one lever arm. A direction error $\theta$ in either the Sun or the Moon tilts the shadow axis about the Moon and moves its intersection with the Earth by $\theta \times D_\mathrm{Moon}$, where $D_\mathrm{Moon} \approx 384{,}400$ km, so 1 arcsecond is 1.86 km on the ground. At a typical relative angular rate of the Moon against the Sun of 0.364 arcseconds per second [@moon-espenak-2001-bulletin], 1 arcsecond is also 2.7 s of contact time. The 10 arcseconds Meeus truncation is therefore about 19 km of path and 27 s of contact time. The Catalog's 0.006 arcseconds is 11 m and 0.02 s. VSOP87's 1 arcsecond over ±4000 years is 1.9 km at the extremes and far less in the present century.

## The Sun: heliocentre, barycentre, light-time, oblateness

Eclipse elements need the direction and distance of the Sun's centre from the Earth. The [?ssb|solar-system barycentre] is the origin of the ICRS and of every DE integration [@moon-folkner-2014]. The Sun is a separate body (SPICE ID 10) whose offset from the barycentre is set mainly by Jupiter and Saturn. With the DE430 mass ratios Sun/Jupiter 1047.348625 and Sun/Saturn 3497.901768 [@moon-folkner-2014], Jupiter at 5.2 au displaces the Sun by 5.2/1047.35 = 0.0050 au, about 743,000 km or 1.07 solar radii, and Saturn adds up to 9.5/3497.9 = 0.0027 au, so the Sun can sit about 1.6 solar radii, 0.0077 au, from the barycentre. This arithmetic is the note's own. Seen from Earth 0.0077 au is 0.44 degrees, so using the barycentre as the Sun is not a subtle bug. All software listed below returns the Sun's centre when asked for the Sun.

Light-time. The astronomical unit is defined as 149,597,870.700 km [@moon-folkner-2014], so light from the Sun takes 499.005 s, 8.32 min, to reach the Earth, and light from the Moon about 1.28 s. The Sun's direction at emission differs from its geometric direction at reception by roughly 499 s times the Earth's orbital rate, 0.041 arcseconds per second, about 20.5 arcseconds, which is numerically the same size as annual aberration. Because annual aberration displaces the Sun and the Moon by the same vector to first order, it cancels in the Sun-Moon relative geometry, whereas the light-time asymmetry does not. The Explanatory Supplement's eclipse chapter therefore builds elements from apparent places of both bodies [@moon-es-1961]. Skyfield's definitions match the almanac's: an astrometric position "applies the effect of light travel time", and `.apparent()` adds "the aberration of light produced by the observer's own motion through space, and the gravitational deflection of light" [@moon-skyfield-positions]. Whichever level is chosen, both bodies must be reduced the same way.

Oblateness. RHESSI measured "a total oblateness of 10.77 +/- 0.44 milli-arc seconds" including magnetic contributions and "the corrected oblateness of the nonmagnetic Sun is 8.01 +/- 0.14 milli-arc seconds, which is near the value expected from rotation" of 7.8 mas [@moon-fivian-2008]. SDO/HMI found the oblate shape "distinctly constant" and "significantly lower than theoretical expectations" [@moon-kuhn-2012]. Eight milliarcseconds is 5.8 km of equator-to-pole radius difference, against a photospheric radius near 696,000 km whose adopted eclipse value is itself uncertain by hundreds of kilometres. Solar oblateness is negligible for eclipse geometry. The solar radius constant and its interplay with the lunar radius ratio $k$ are treated in [solar radius](../06-solar-radius/_index.md).
Here it is enough that both semidiameters enter the umbral cone the same way, so a 0.3 arcseconds error in either has the same effect on totality duration.

## Software that evaluates these ephemerides

**jplephem and Skyfield.** jplephem reads SPK types 2, 3 and 9 and returns kilometres for a TDB Julian date [@moon-jplephem-pypi]. Skyfield layers frames and reductions on it: barycentric, astrometric and apparent positions, ICRS internally and GCRS when measured from the geocentre [@moon-skyfield-positions]. Skyfield also reads the lunar frame kernels and PCKs, as set out in [lunar figure, radius ratio k, and libration](lunar-figure-and-libration.md) [@moon-skyfield-planetary].

**astropy.** `get_body` returns GCRS coordinates and "the coordinate returned is the apparent position, which is the position of the body at time t minus the light travel time from the body to the observing location", while `get_body_barycentric` returns ICRS Cartesian positions [@moon-astropy-solarsystem] [@moon-astropy-source]. The internal helper is documented as "Calculate the apparent position of body relative to Earth. This corrects for the light-travel time to the object" [@moon-astropy-source]. No aberration is mentioned in either docstring, so astropy's "apparent" is the almanac's astrometric place. The default `'builtin'` ephemeris uses ERFA's plan94 and epv00 with rms Earth errors "about 4.6 km and 1.4 mm/s" [@moon-astropy-solarsystem]. Set `solar_system_ephemeris.set('de440')` or a URL to use a JPL file [@moon-astropy-solarsystem].

**SPICE.** `spkezr_c` takes "seconds past J2000 TDB" and an aberration flag: NONE returns "the geometric state of the target body relative to the observer"; LT corrects "for one-way light time (also called 'planetary aberration')"; LT+S adds stellar aberration; CN and CN+S iterate the light-time solution to convergence [@moon-spice-spkezr]. For an Earth-based eclipse computation NONE gives geometric positions, LT gives astrometric, LT+S gives apparent in the almanac sense, and the Sun and Moon must be called with the same flag.

**Swiss Ephemeris.** "Swiss Ephemeris is based on JPL Ephemeris DE431" since version 2.0, its compressed files agree with JPL "to 1 milli-arcsecond (0.001\")" for the Moon, and the Moshier fallback is good to 0.5 arcseconds relative to DE404 over 1369 BC to AD 3000 [@moon-swisseph]. Its apparent positions apply "Light-time correction", "Annual aberration of light" and "Light deflection by the gravity of the Sun" [@moon-swisseph]. The DE431 base means a Swiss Ephemeris eclipse differs from a DE440 one by the DE431-to-DE440 lunar difference, which is under 10 m within the LLR era.

## Pitfalls

1. **Barycentre for Sun.** Segment 0→10 must be used, not the origin. The error is up to 0.44 degrees (derived above from [@moon-folkner-2014]).
2. **Earth-Moon barycentre for Earth.** Segment 3 is the barycentre. The Earth is 3→399 and the Moon 3→301 [@moon-jplephem-pypi]. The barycentre is about 4,670 km from the geocentre, so the error is about 1.2 degrees in the Moon's direction.
3. **Geometric Sun with apparent Moon.** Roughly 20.5 arcseconds, 38 km of path, 55 s of contact time (derived from the Sun's light-time and [@moon-skyfield-positions]).
4. **TT and UT mixed.** The ephemeris is evaluated in TDB, indistinguishable from TT at the millisecond level, but Earth rotation is in UT1. With ΔT near 69 s the Earth turns 69 × 15.04 arcseconds = 0.29 degrees, 32 km of longitude at the equator. Espenak's EclipseWise page states "ΔT has a value of 71.5 seconds for this eclipse" for 2024 and "UT1 = TD − ΔT" [@moon-eclipsewise-2024]. The Explanatory Supplement records that eclipse predictions "were given in ephemeris time (ET) until 1981" and that UT1 is what surface phenomena need [@moon-es-1992].
5. **Forgetting the ellipsoid.** The observer's geocentric position enters through the fundamental plane. That is [earth figure and terrain](../07-earth-and-time/earth-figure-and-terrain.md), not this note, but the ephemeris frame must be the same GCRS-aligned frame the Earth orientation rotates into.
6. **Long-span kernel for modern dates.** DE441 diverges from DE440 by about 10 m per century in along-track lunar position [@moon-jpl-eph-export]. Harmless for eclipses, but there is no reason to accept it.
7. **Stale ephemeris.** DE405 to DE421 lunar differences reach tens of metres by 2020 [@moon-williams-2008]. Still harmless against a 1 km limb uncertainty, but a product claiming metre-level paths must say which DE it used.

## Sources compared

| Source | What it uniquely provides |
|---|---|
| Folkner et al. 2014, DE430/431 report [@moon-folkner-2014] | Frame (ICRF2), TDB definition and integrated TT−TDB, lunar core-mantle model, mass table, span rationale |
| Williams, Boggs, Folkner 2013 lunar memo [@moon-williams-2013] | LLR data count and residuals, DE430 vs DE421 (½ mas), PA/ME rotation angles for DE430 |
| Park et al. 2021 DE440/441 [@moon-park-2021] | 1.3 cm LLR residuals, geodetic precession on librations, ICRF3, DE440 vs DE441 recommendation |
| NAIF summaries and directory [@moon-naif-summaries] [@moon-naif-planets-dir] | Exact kernel spans, sizes and dates including DE442 |
| JPL bsp README [@moon-jpl-bsp-readme] | TT−TDB pseudo-body 1000000001, `t` file semantics |
| Skyfield planets page [@moon-skyfield-planets] | Practical file recommendation and excerpting |
| Espenak and Meeus Catalog [@moon-espenak-meeus-canon] | ELP-2000/82 and VSOP87D as used, truncation error, ΔT correction for secular acceleration |
| INPOP21a notes [@moon-fienga-2021] | Station-by-station LLR residuals, INPOP vs DE440 planetary differences |
| IAA EPM page [@moon-iaa-epm] | EPM2021 contents, spans, SPICE format |
| VSOP87 notice [@moon-imcce-vsop87-doc] | 1 arcsecond over ±4000 yr, frame of each version |

## What a developer should do

1. Download de440s.bsp (31 MB, 1849 to 2150) from https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/ and moon_pa_de440_200625.bpc plus moon_de440_250416.tf from the NAIF pck and fk directories [@moon-naif-planets-dir] [@moon-naif-pck-dir]. Record the file names and dates in the product's provenance.
2. Read the Moon as (3→301) − (3→399) and the Sun as (0→10) − ((0→3) + (3→399)) in kilometres, TDB [@moon-jplephem-pypi].
3. Treat TT as TDB for the eclipse, an error below a milliarcsecond, but convert to UT1 with ΔT before any Earth rotation [@moon-es-1992].
4. Reduce Sun and Moon to the same level. Follow the almanac and use apparent places, or use astrometric for both and document it [@moon-es-1961] [@moon-skyfield-positions].
5. Read Folkner et al. 2014 sections I to III and Park et al. 2021 section 2 first, then Williams et al. 2013 for the lunar frames [@moon-folkner-2014] [@moon-park-2021] [@moon-williams-2013].
6. For validation against Espenak, remember he used DE405 and ELP/VSOP, so metre-level differences are expected and are his, not yours [@moon-eclipsewise-2024] [@moon-espenak-meeus-canon].

## What this changes

The ephemeris is not where eclipse error lives. Every DE since DE421 puts the Moon within a few metres of truth in the present century, which is under 10 ms of contact time. The pipeline design can fix DE440 (de440s.bsp) as the single source for Sun, Earth and Moon, and put its validation effort into ΔT, the lunar limb profile, and the solar radius. The one design consequence is that lunar orientation must come from the matching DE440 PCK, not from the IAU series, so the limb-profile module depends on the same kernel set.

## Open questions

- Obtain Chapront and Francou 2003 (A&A 404, 735) and record ELP/MPP02's stated difference from DE405 and DE406 in arcseconds over 1950 to 2050 and over ±3000 years.
- Obtain Standish's DE405 memo in text form (JPL IOM 312.F-98-048) and extract the DE200 to DE405 lunar difference in arcseconds for 1990 to 2010.
- Obtain the DE442 technical comments' statement, if any, on whether the lunar initial conditions or LLR set changed from DE440, and confirm with JPL whether moon_pa_de440_200625.bpc is still the recommended PCK for DE442.
- Fetch Fienga et al. 2019 (INPOP19a, IMCCE Notes S109) and Pitjeva's EPM2021 paper for a Moon-versus-DE440 difference in metres over 1980 to 2040.
- Extract the physical libration tables from Tables 6 to 8 of IMCCE's INPOP21a notes to quantify INPOP-versus-DE440 libration differences in milliarcseconds, which bear on the limb profile more than on the orbit.
