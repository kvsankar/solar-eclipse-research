---
title: Refraction, light-time and frames
description: Refraction, apparent positions, aberration, light-time and TT versus TDB in eclipse calculations, with documented effects and implementation choices.
order: 3
status: working
updated: 2026-09-30
tags: [refraction, aberration, light-time, tdb, apparent-place, effects-table]
seo_title: Eclipse Calculation: Refraction, Light-Time and Frames
---

::: summary
- **The classical nominal contacts omit refraction.** Espenak states that "refraction corrections to the path are uncertain since they depend on the atmospheric temperature-pressure profile, which cannot be predicted in advance", the 1961 Supplement draws the rising and setting curves "neglecting refraction, that is assuming a zenith distance of 90°", and Jubier's calculator says "astronomical horizon, no atmospheric refraction" [@earth-espenak-tp2001] [@earth-es1961] [@earth-jubier-calc].
- **Transform both limbs consistently.** A common one-to-one angular mapping preserves their contact and containment, including nonlinear mappings. The cited sources do not establish a general low-altitude contact-time correction. Atmospheric visibility requires separate modelling [@earth-es1961] [@earth-espenak-tp2001].
- **The almanac formulas are Bennett's for apparent altitude and Sæmundsson's for true altitude**, $R = 1.02 / \tan(h + 10.3/(h + 5.11))$ arcminutes scaled by $(P/1010)(283/(273 + T))$, with 34′ on the horizon for rise and set. Stellarium implements both with defaults of 1013 mbar and 10 °C and cuts off at $-3.54^{\circ}$ [@earth-es1992] [@earth-stellarium-refraction].
- **The Besselian elements are built from apparent places.** The 1992 Supplement: the inputs are "the apparent right ascension, declination, and distance of the Sun ... and of the Moon", and "Since the apparent positions of the Sun and Moon are used in the calculations aberration is already included, except for the inappreciable difference between the light-time from the Sun to the Moon and from the Sun to the Earth" [@earth-es1992]. Mixing observer aberration conventions can introduce a direction difference of about 20.5 arcseconds. At a lunar distance of 384,400 km that angular scale is about 38 km. It is a diagnostic scale, rather than a universal shift between two consistently reduced solvers [@earth-spice-abcorr].
- **TT and TDB differ by at most about 1.7 ms**, "which for the geocentric position of the Moon would correspond to an angular error of <1 mas", which is about 2 m on the shadow. The DE ephemerides are in TDB and must be entered with the JPL formula, but an eclipse product can use TT. On first use here, TT is printed as TDT or TD in NASA tables and was called ET before 1984 [@earth-circ179] [@earth-de430-memo].
- **Omissions and residual uncertainties are different.** Aberration inconsistency and a spherical Earth can introduce kilometre-scale shifts. Geoid-height mistakes can reach 170 metres at a 30-degree Sun. Polar motion, nutation differences and TT−TDB have metre-to-tens-of-metres scales [@earth-es1992] [@earth-espenak-tp2001] [@earth-circ179]. Lunar laser-ranging residuals do not bound every component of the lunar orbit [@moon-park-2021].
:::

**The question.** Do eclipse predictors include atmospheric refraction in contact times and in the path near sunrise and sunset, and should they, given the size of the effect at 5° and 1° of altitude? Which refraction formulas do the Explanatory Supplement, Meeus, the Swiss Ephemeris and Stellarium use, and what does the "rise/set curves" convention assume about the horizon? How are light-time and aberration handled for the Sun and Moon, are the elements built from apparent or geometric places, does the TT versus TDB distinction matter, and what is the origin for the Sun's position? Finally, how large is every effect in this topic, in seconds of time and in metres on the ground, and which predictors include each?

## Refraction: what the sources say

The Explanatory Supplement treats refraction as a refinement outside the standard computation. The 1992 edition lists among "refinements to be considered in performing precise calculations: choosing a consistent ephemeris, corrections for Earth's rate of rotation, and, for the Moon, offset of center of figure from center of mass; correcting for irregularities of the lunar limb; and effects of the Earth's atmosphere (refraction in solar eclipses and the effect on the shadow in lunar eclipses)", and then does not apply it in the algorithms that follow [@earth-es1992]. The 1961 edition defines the [?rise-set-curve|rising and setting curves] without it: "points on the rising and setting curve (neglecting refraction, that is assuming a zenith distance of 90°) may be calculated for each stated time by noting that ζ is equal to zero" [@earth-es1961]. That is the convention on every almanac and NASA map: the "eclipse begins at sunrise" curve is where the Sun's centre is on the geometric horizon, with no refraction and no semidiameter. An observer sees the upper limb rise when the centre is at $-34' - 16' = -50'$ of true altitude (the Supplement's rise and set convention is "a constant of 34′ is used for the horizontal refraction; thus for the center of the Sun or Moon to be coincident with the horizon the true altitude will be −34′" [@earth-es1992]), which at the equator is about 3.3 minutes earlier than the geometric moment. On the ground the mapped curve is displaced from the visible sunrise line by $50'$ of terminator position, about 93 km, always toward the night side.

Espenak's bulletins state the policy of the NASA products: "Unless otherwise stated, all predictions are based on center of mass positions for the Moon and Sun with no corrections made for center of figure, lunar limb profile or atmospheric refraction", and for the maps, "Atmospheric refraction has not been included, as its effects play a significant role only at very low solar altitudes. In any case, refraction corrections to the path are uncertain since they depend on the atmospheric temperature-pressure profile, which cannot be predicted in advance" [@earth-espenak-tp2001]. The local-circumstance tables say the same: "The effects of refraction have not been included in these calculations" [@earth-espenak-tp2001]. The NASA and EclipseWise 2017 and 2024 pages carry no refraction statement at all [@earth-nasa-2017-google] [@earth-eclipsewise-2024].

Jubier's calculator labels its diagram "Relative positions of the Sun and Moon (astronomical horizon, no atmospheric refraction)" [@earth-jubier-calc]. timeanddate does not mention refraction for eclipse contacts, and for rise and set says its times "are based on a flat horizon where the observer is at the same altitude as the horizon" [@earth-timeanddate-accuracy]. The technical note for The Photographer's Ephemeris (Photo Ephemeris) applies refraction only to its picture: "the simulator is corrected for refraction using the US Standard Atmosphere model, but the apparent limb shape of each body remains circular" [@earth-photoephemeris]. Occult's graze listings say "The path is adjusted for the effects of refraction at low moon altitudes", for lunar grazes. Nothing was found about solar-eclipse limits [@earth-occult-tutorial]. The Swiss Ephemeris applies it selectively: "Algorithms for the central line is taken from Montenbruck, pp. 179ff., with the exception, that we consider refraction for the maxima of partial and noncentral eclipses", with an error budget entry "from displacement of shadow points by atmospheric refraction: a few meters" and the warning "if the sun is close to the horizon, all of these errors can grow up to a km or more" [@earth-swisseph-swecl]. It also uses refraction plus dip to decide visibility: "approximate minimum height for visibility, considering refraction and dip: 34.4556′: refraction at horizon, from Bennets formulae; 1.75′/sqrt(geohgt): dip of horizon; 0.37′/sqrt(geohgt): refraction between horizon and observer", coded as `hmin_appr = -(34.4556 + (1.75 + 0.37) * sqrt(geohgt)) / 60` degrees [@earth-swisseph-swecl].

## The formulas

The 1992 Supplement's low-precision formula, "accurate to 0′.5" and adequate for "the times of rising and setting", is in terms of the apparent altitude $H$ in degrees, temperature $T$ in °C and pressure $P$ in millibars:

$$R = \frac{P}{1010}\,\frac{283}{273 + T}\;\frac{0.0167^{\circ}}{\tan\!\left(H + \dfrac{7.31}{H + 4.4}\right)}$$

"If $T$ and $P$ are unknown, assume the term in the first bracket is unity", and for $H < 15^{\circ}$ the alternative

$$R = \frac{P}{1010}\,\frac{283}{273 + T}\;\frac{0.1594 + 0.0196H + 0.00002H^2}{1 + 0.505H + 0.0845H^2}\ \text{degrees}$$

[@earth-es1992]. The first is Bennett's formula ($0.0167^{\circ} = 1.002'$). The Swiss Ephemeris `swe_refrac` uses the Astronomical Almanac pair: above 15° "$D = 0.00452\,P/((273 + T)\tan h)$" degrees with "Accuracy 'usually about 0.1′'", and below it the "Almanac for Computers" form with $N = 1/\tan(h + 7.31/(h + 4.4))$ and $D = N P' / (60 + Q(N + 39))$, inverted by Newton iteration when converting true to apparent [@earth-swisseph-swecl]. eclipse-chasers.com uses the same two [@earth-eclipse-chasers].

Meeus's Astronomical Algorithms gives the true-altitude form due to Sæmundsson, which Stellarium implements as its forward transformation: "refraction from Saemundsson, S&T1986 p70 / in Meeus, Astr.Alg.", coded as

$$R' = \frac{P}{1010}\,\frac{283}{273 + T}\left[\frac{1.02}{\tan\!\left(h + \dfrac{10.3}{h + 5.11}\right)} + 0.0019279\right]\ \text{arcmin}$$

with $h$ the geometric altitude in degrees, and the backward transformation "refraction from Bennett, in Meeus, Astr.Alg." with the constant 0.0013515 [@earth-stellarium-refraction] [@earth-meeus-aa] [@earth-saemundsson-1986]. The small added constants make each formula vanish at the zenith. Stellarium's defaults are `pressure(1013.f), temperature(10.f)`, and it stops applying the formula below the horizon: `MIN_GEO_ALTITUDE_DEG = -3.54f`, `MIN_APP_ALTITUDE_DEG = -3.21783f`, with linear transition zones, and a polynomial inverse below $-2^{\circ}$ because "Bennett's formula is not a strict inverse of Saemundsson's" [@earth-stellarium-refraction]. The developer documentation adds only that "Typical horizons do not go down below -1, so strange effects (distortion) between -2 and -5 should be covered" [@earth-stellarium-doc].

Evaluating Sæmundsson's formula at standard conditions (computed here): $R = 29.0'$ at $h = 0^{\circ}$, $21.7'$ at $1^{\circ}$, $16.9'$ at $2^{\circ}$, $9.7'$ at $5^{\circ}$, $5.4'$ at $10^{\circ}$, $2.7'$ at $20^{\circ}$, $1.0'$ at $45^{\circ}$. Bennett's gives $34.5'$ at an apparent altitude of $0^{\circ}$, which is the origin of the 34′ convention. The gradient, which is what matters for an eclipse, is $dR/dh = 5.9'$ per degree at $1^{\circ}$, $1.5'$ per degree at $5^{\circ}$, $0.5'$ per degree at $10^{\circ}$ and $0.04'$ per degree at $45^{\circ}$.

## Refraction mapping and contact geometry

A common smooth one-to-one mapping applied to every point of both apparent limbs preserves intersection and containment. At contact the coincident points map to the same point. An invertible smooth mapping also preserves tangency. This holds when the mapping is nonlinear. It is a mathematical property of the stated mapping, rather than an empirical atmospheric bound.

Differential refraction changes centre separations and limb shapes. Applying refraction only to the centres while retaining circular limbs is inconsistent. A centre-separation estimate therefore cannot determine a contact-time correction. Atmospheric ray bending and finite-distance effects can change the effective observing geometry near the horizon, but the sources compared here do not quantify a general C1–C4 timing shift. A validated propagation model is needed before assigning one [@earth-es1992] [@earth-espenak-tp2001]. Refraction still changes displayed altitude and visibility. The Swiss Ephemeris uses a separate low-altitude visibility test [@earth-swisseph-swecl].

## Apparent places, aberration and light-time

The [?apparent-place|apparent place] of a body is its geocentric direction corrected for [?light-time|light-time], [?aberration|aberration], precession and nutation. The Supplement is unambiguous that the Besselian elements are built from apparent places: "The basic quantities for calculations of solar and lunar eclipses are: the apparent right ascension ($\alpha_s$), declination ($\delta_s$), and distance ($R_s$) of the Sun, and the apparent right ascension ($\alpha_m$), declination ($\delta_m$), and distance ($R_m$) of the Moon, for every hour of TDT during the eclipse ... The apparent places of the Sun and the Moon are computed rigorously using the same ephemerides for the Sun and the Moon as are used for The Astronomical Almanac, and using the reduction methods described elsewhere in this book (see Chapter 3)" [@earth-es1992]. On aberration: "Since the apparent positions of the Sun and Moon are used in the calculations aberration is already included, except for the inappreciable difference between the light-time from the Sun to the Moon and from the Sun to the Earth" [@earth-es1992].

Reception light-time and observer aberration are separate corrections. NAIF's barycentric reception model evaluates the target at emission and the observer at reception:

$$\mathbf{r}_{\mathrm{LT}} = \mathbf{T}(t-\tau)-\mathbf{O}(t),\qquad \tau = |\mathbf{r}_{\mathrm{LT}}|/c$$

Here $t$ and $\tau$ are in TDB seconds, the position vectors have the same length unit and $c$ has that length unit per second. The target's barycentric motion determines its light-time displacement. Observer aberration instead depends on the observer's barycentric velocity [@earth-spice-abcorr].

The Sun's approximately 499-second light-time must not be multiplied by Earth's orbital angular rate to obtain the annual aberration angle. Earth's orbital velocity supplies that separate correction, with a scale of about 20.5 arcseconds. The Moon also receives an observer-aberration correction. Its small net geometric-to-apparent displacement can involve cancellation with target retardation, rather than a small aberration term by itself [@earth-spice-abcorr]. Mixing reduction conventions for the two bodies can therefore introduce large errors. Apply the same documented chain and keep each correction identifiable. The Supplement's quoted Sun-to-Moon versus Sun-to-Earth light-time qualification does not establish a 100-metre bound [@earth-es1992].

The Supplement's second correction at this stage is the centre of figure: "Gravitational ephemerides refer to the positions of the centers of mass of the bodies concerned. Eclipses, however, are governed by the positions of the centers of figures ... The range of the corrections is less than 0″5, and for the calculations in The Astronomical Almanac, only the minimum corrections are applied. These are Δλ = +0″50 and Δβ = −0″25 for the LE200 lunar ephemeris" [@earth-es1992]. Espenak does not apply it: "The lunar coordinates have been calculated with respect to the Moon's Center of Mass. They DO NOT include a correction to the Center of Figure" [@earth-nasa-2024-beselm]. SVS puts the offset at "about 0.5 kilometers" and absorbs it in the limb profile [@earth-svs-4314]. That is the sky-plane component. The full centre-of-mass to centre-of-figure vector from LOLA is 1.935 km, mostly along the Earth-Moon line [@moon-jones-2025]. Those quantities belong to [lunar figure, radius ratio k, and libration](../08-lunar-and-solar-model/lunar-figure-and-libration.md) and are listed in the table below only for scale.

Espenak fits the elements rather than tabulating them: "The Besselian elements were derived from a least-squares fit to elements calculated at five uniformly spaced times over a six hour period centered at t0" [@earth-nasa-2017-beselm]. The Swiss Ephemeris computes Sun and Moon with `SEFLG_SPEED | SEFLG_EQUATORIAL` plus the caller's ephemeris flag, which by default yields apparent positions with light-time and aberration, and, as noted in the ΔT note, drops nutation only if mean sidereal time is used for the hour angle [@earth-swisseph-swecl].

## TT, TDB and the barycentric origin

The JPL ephemerides are integrated in [?tdb|TDB]. The DE430 memo: "The coordinate time scale used for DE430 and DE431 is Barycentric Dynamical Time (TDB) as defined in terms of Barycentric Coordinate Time (TCB)", with the TDB − TT expression given in full, and "The origin of the ICRS is the solar system barycenter" [@earth-de430-memo]. Circular 179 gives the working relation:

$$T_{\mathrm{eph}} \approx \mathrm{TDB} \approx \mathrm{TT} + 0.001657 \sin(628.3076\,T + 6.2401) + 0.000022 \sin(575.3385\,T + 4.2970) + \cdots\ \mathrm{s}$$

with $T$ in Julian centuries of TT from J2000.0, and states the consequence of ignoring it: "The total error in time in using TT as the input argument is <2 ms, which for the geocentric position of the Moon would correspond to an angular error of <1 mas" [@earth-circ179]. The Moon moves $0.55''$/s, so 1.7 ms is $0.0009''$, or 1.7 m on the shadow axis (computed here). An eclipse product may evaluate the ephemeris at TT without measurable loss, but a developer reading a DE file directly should still enter it with TDB, because the library interfaces (SPICE, the Swiss Ephemeris) expect it.

The origin question is one of bookkeeping. The DE files give positions relative to the [?ssb|solar-system barycentre], with the Earth-Moon barycentre and the geocentric Moon as separate objects. The geocentric Sun needed for the elements is $\mathbf{r}_{\odot} - \mathbf{r}_{\oplus}$, where $\mathbf{r}_{\oplus}$ is recovered from the barycentre and the Moon using the ephemeris's own Earth-Moon mass ratio. The light-time and aberration corrections are then applied to that geocentric vector, and the Moon is already geocentric. Doing this by hand invites a mismatch between the mass ratio and the ephemeris. The SPICE and Swiss Ephemeris interfaces do it internally [@earth-de430-memo] [@earth-swisseph-swecl].

## Every effect in this topic

The full ranked budget is in [error budget and validation protocol](../10-validation/error-budget-and-validation-protocol.md). This table keeps the rows this topic owns. Sizes on the ground are for the umbral path or a contact position. Times are for contact instants. "Included" means documented on the pages read; a dash means not documented either way.

| Effect | Typical size, time | Typical size, ground | Espenak NASA and EclipseWise | NASA SVS | Jubier | timeanddate | Occult | Swiss Ephemeris |
|---|---|---|---|---|---|---|---|---|
| Ellipsoid instead of sphere | tens of s at contacts | up to 21 km | Yes (implied by the elements) | Yes, WGS 84 | not stated | Yes ("squashed") | Yes, WGS 84 | Yes, z-scaling |
| Choice among IAU 1976, GRS 80, WGS 84 | 0 | 3 m in $a$, 16 mm in $b$ | any | WGS 84 | not stated | not stated | WGS 84 | AA 2006 |
| Observer elevation, path limits | s to tens of s at limits | $h \cot A \sin D$: 0.6 to 1.7 km per 1000 m at 60° to 30° | Sea level; elevation factor supplied | Yes, SRTM | Altitude input | No, sea level | Site altitude | Height input, global paths at sea level |
| Observer elevation, duration | under 1 s | $2h \tan f_2$, 82 m at Everest | No | Yes | Yes | No | not stated | Yes |
| Geoid versus ellipsoid height | under 1 s | $N \cot A$, up to 170 m at 30° | No | Yes, EGM96 | not stated | No | not stated | Listed as error |
| DEM vertical error | under 1 s | under 20 m for SRTM at 30° | n/a | SRTM | not stated | n/a | not stated | n/a |
| ΔT prediction error | 0.05 s at 1 yr, 0.6 s at 5 yr, 4.6 s at 20 yr, 52 s at 100 yr | $465\cos\phi$ m per second: 0.02, 0.2, 1.6, 18 km at 40° | Yes; 2024 was 1.4 to 2.3 s high | Yes; 2017 within 0.08 s | Yes, value not read | Yes, value not published | not stated | Yes, model switch at 1955 |
| UT1 versus UTC | up to 0.9 s, epoch-dependent | up to 0.42 km | UT1 printed | Leap seconds in "Delta UTC" | not stated | not stated | not stated | UT1 |
| Polar motion | 0 | about 10 m | No | Implicit in SPICE kernel | No | No | No | Listed as error, not applied |
| Mean versus apparent sidereal time, if inconsistent | up to 1.1 s | up to 0.5 km | consistent | consistent | not stated | not stated | not stated | consistent by construction |
| Nutation and precession model (1980 vs 2000A) | 0 | under 20 m | any | SPICE | not stated | not stated | not stated | any |
| Aberration of the Sun, if omitted or mixed | tens of s | 38 km | Apparent places | Apparent (DE421 via SPICE) | not stated | not stated | not stated | Apparent by default |
| Sun-to-Moon versus Sun-to-Earth light-time | Not quantified here | Not quantified here | No | not stated | not stated | not stated | not stated | No |
| TT versus TDB | 1.7 ms | 2 m | any | TDB via SPICE | not stated | not stated | not stated | TDB internally |
| Refraction at 2nd and 3rd contact | No validated bound here | No validated bound here | No | No | No | No | not stated | No |
| Refraction at 1st and 4th contact near the horizon | No validated bound here | No validated bound here | No | No | No | No | not stated | Maxima of partial eclipses only |
| Rise and set curves, refracted versus geometric horizon | about 3.3 min | about 93 km along the terminator | Geometric | not stated | Geometric | Flat horizon for rise and set | not stated | Visibility test with 34.4556′ plus dip |
| Centre of figure versus centre of mass (for scale) | under 1 s | about 0.5 to 1 km | No | Absorbed in limb profile | via limb correction | No | via limb data | No |
| Ephemeris error | Not certified by a ranging residual | DE440 fits recent lunar laser-ranging data near a centimetre in range. This is not a 3D orbit bound. Swiss Ephemeris budgets 40 m for an assumed 0.01 arcseconds | DE405 on the 2017 Google-map page, VSOP87/ELP2000-85 on the 2024 element page | DE421 on the product pages, DE440 in the paper's appendix | not stated | not stated | not stated | DE431 default |

Sources for the rows: ellipsoid and elevation [@earth-es1961] [@earth-es1992] [@earth-espenak-tp2001] [@earth-svs-4517] [@earth-timeanddate-accuracy] [@earth-swisseph-swecl]; ΔT [@earth-nasa-deltat-uncertainty] [@earth-usno-deltat-data] [@earth-nasa-2024-google] [@earth-eclipsewise-2024] [@earth-svs-4515]; UT1 and polar motion [@earth-iers-bulletin-a]; sidereal time and nutation [@earth-circ179]; aberration and light-time [@earth-es1992]; TDB [@earth-circ179] [@earth-de430-memo]; refraction [@earth-es1992] [@earth-stellarium-refraction]; centre of figure [@earth-es1992] [@earth-svs-4314] [@earth-nasa-2024-beselm]; ephemeris error [@moon-park-2021] [@earth-swisseph-swecl] [@earth-nasa-2017-google].

## Sources compared

| Source | Refraction in contacts | Refraction in rise/set curves | Positions used | Time argument | What it uniquely provides |
|---|---|---|---|---|---|
| Explanatory Supplement 1961 [@earth-es1961] | Not applied | Geometric horizon, stated | Apparent places | ET | The rise/set convention in words |
| Explanatory Supplement 1992 [@earth-es1992] | Listed as a refinement, not applied | 34′ for rise/set tables, geometric for eclipse curves | Apparent places, stated; centre-of-figure +0″50, −0″25 | TDT | The refraction formulas and the aberration statement |
| Espenak NASA bulletins [@earth-espenak-tp2001] | Not applied, with the reason | Geometric | Centre of mass, no limb | TDT and UT | The clearest policy statement |
| Swiss Ephemeris [@earth-swisseph-swecl] | Only for maxima of partial eclipses; visibility test with 34.4556′ plus dip | n/a | Apparent, flags | UT in, TT internally | An explicit error budget |
| Stellarium [@earth-stellarium-refraction] | n/a (display) | n/a | n/a | n/a | The Sæmundsson and Bennett formulas as code, with cut-offs |
| Jubier calculator [@earth-jubier-calc] | Diagram without refraction | n/a | n/a | ΔT printed | Limb correction at contacts |
| Photo Ephemeris [@earth-photoephemeris] | Simulator only, US Standard Atmosphere | n/a | Meeus elements | USNO ΔT | A stated refraction model for the picture |
| Circular 179 [@earth-circ179] | n/a | n/a | n/a | TT, TDB, sidereal time | The TDB series and the sizes of nutation-model effects |
| DE430 memo [@earth-de430-memo] | n/a | n/a | SSB, ICRS | TDB | The time argument and origin of the ephemeris |

## What a developer should do

1. Build classical almanac elements from apparent places of both bodies through one documented reduction chain. Verify light-time, observer aberration and the frame rotation separately against a fixed source fixture. A generic 20-arcsecond right-ascension difference is not a valid check at every solar position [@earth-es1992] [@earth-spice-abcorr].
2. Enter the DE ephemeris with TDB if reading it directly, or let SPICE or the Swiss Ephemeris do it. Do not spend effort on the 1.7 ms [@earth-circ179] [@earth-de430-memo].
3. Leave refraction out of nominal geometric contacts and state the convention. Model displayed altitude and atmospheric visibility separately. Publish a contact-time adjustment only after validating the propagation model and both transformed limbs [@earth-es1992] [@earth-espenak-tp2001].
4. Draw rise and set curves for the geometric horizon, as the almanacs do, and label them. Add a visible-sunrise curve at $-50'$ of true altitude only as a separately labelled layer [@earth-es1961] [@earth-es1992].
5. Use the Swiss Ephemeris visibility test, $h_{\min} = -(34.4556 + 2.12\sqrt{h_{\mathrm{obs}}})/60$ degrees, to decide whether a contact near the horizon is observable at all [@earth-swisseph-swecl].

Read first: Section 8.12 of the 1992 Supplement for the apparent-place statement, Section 3.283 for the refraction formulas, Section 2 of Circular 179 for the time scales, and the comment block at the head of `eclipse_where` in `swecl.c` for the error budget.

## What this changes

Nothing in the geometry stage. The pipeline needs an "apparent places" contract on the ephemeris interface and a stated refraction policy in the output metadata. The effects table fixes the order in which validation effort should be spent: aberration consistency and the ellipsoid first, then terrain and ΔT, then everything else.

## Open questions

- Obtain Meeus's Elements of Solar Eclipses 1951–2200 and check whether his elements are computed from apparent places and how he treats the Sun's aberration. The Photo Ephemeris products rest on it [@earth-meeus-elements].
- Obtain Occult's solar-eclipse help topic to learn whether the refraction adjustment applied to graze paths is also applied to eclipse limits near the horizon [@earth-occult-tutorial].
- Obtain a ray-traced finite-distance test case with a specified atmospheric profile and both transformed limbs at solar altitudes of 2 and 5 degrees. Compare its contacts with the nominal geometric solution before assigning a physical timing shift [@earth-espenak-tp2001].
- Obtain the 2013 Explanatory Supplement's eclipse chapter for any change to the apparent-place and centre-of-figure statements of 1992 [@earth-es2013].
