---
title: Saturn's satellite theories and ring geometry
seo_title: Saturn Satellite Ephemerides and Ring Geometry
description: Which theories and ephemerides place Saturn's satellites, how Meeus chapters 45 and 46 compute ring aspect and satellite positions, and which constants matter.
order: 1
status: working
updated: 2026-10-17
tags: [saturn, satellites, tass, dourneau, sat441, noe, meeus, rings]
---

::: summary
- **Four generations of theory place Saturn's main satellites.** They are Dourneau's elements of 1987 to 1993, Harper and Taylor 1993, TASS 1.6 and 1.7 of Vienne and Duriez, and the numerical ephemerides NOE of [IMCCE](https://www.imcce.fr/) and SAT441 of JPL [@sats-dourneau-1993] [@sats-harper-taylor-1993] [@sats-vienne-duriez-1995] [@sats-arlot-2012-phesat09] [@sats-naif-sat441-cmt].
- **Their accuracy differs by an order of magnitude.** Dourneau estimated 350 to 500 km for Enceladus to [Titan](https://en.wikipedia.org/wiki/Titan_(moon)) and 2500 km for Hyperion. Against the 2009 [mutual events](../15-jupiter-satellites/mutual-events.md), TASS 1.7 left 48.5 milliarcseconds of right-ascension residual against 16.4 for Lainey's NOE solution and 17.3 for JPL SAT351 [@sats-dourneau-1993] [@sats-arlot-2012-phesat09].
- **[Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) chapter 46 is Dourneau's elements in a compact form.** Its Mimas, Enceladus, Tethys and Dione constants and the equator node and inclination 168.8112 and 28.0817 degrees match Dourneau's published values [@sats-soniakeys-saturnmoons] [@sats-harper-taylor-1993] [@sats-dourneau-1993].
- **Meeus chapter 45 gives the ring aspect in six numbers.** They are B, B′, ΔU, P and the full major and minor axes a and b of the outer ring edge, with $a = 375.35''/\Delta$ and $b = a\sin|B|$. The radius of the edge is $a/2$. Four fixed fractions of a give the inner edges [@sats-soniakeys-saturnring].
- **Saturn is not a sphere.** Its 1 bar equatorial and polar radii are 60,268 and 54,364 km, a flattening of 0.09796. A gravity file may quote 60,330 km or 60,000 km as a reference radius. That is a different quantity [@sats-nssdc-saturn] [@sats-naif-pck00011] [@sats-naif-sat441-cmt] [@sats-harper-taylor-1993].
- **Meeus's ring fractions are older than the Voyager and Cassini radii.** At 1 au they put the inner edge of ring A at 119,795 km, against 122,340 km in NASA's ring fact sheet, a 2 per cent difference [@sats-soniakeys-saturnring] [@sats-nssdc-rings].
:::

**The question.** Which theories and ephemerides give the positions of Saturn's satellites, in which versions and with what accuracy, and how does a program turn them, together with Saturn's figure and rings, into the apparent geometry that phenomena predictions need? The Galilean satellites share much of this geometry, and [the Jupiter satellite topic](../15-jupiter-satellites/_index.md) treats them separately.

## Theories and ephemerides, by generation

A satellite [?ephemeris] for phenomena work must give the satellite's position relative to Saturn's centre, not only its sky position. The relative position decides whether a satellite is in front of the globe, behind it or in its shadow. Two kinds of model exist. A [?sats-semi-analytical-theory] writes the orbital elements as series in time and is cheap to evaluate. A [?sats-numerical-ephemeris] integrates all the bodies together and is delivered as [?chebyshev] coefficients in a file.

### Dourneau (1987 thesis, 1993 paper)

Dourneau collected "nearly 22000 satellite observed coordinates" from H. Struve's visual work of 1886 to photographic plates of 1980 to 1985, and fitted theories of motion of all eight major satellites to them [@sats-dourneau-1993]. The fit corrected mean motions, node and pericentre rates, and the parameters of the Mimas-Tethys, Enceladus-Dione and Titan-Hyperion librations [@sats-dourneau-1993]. The paper estimates position uncertainties for recent years "between 350 and 500 km for the satellites II-VI, from 800 to 1000 km for Iapetus and Mimas, and about 2500km for Hyperion". It adds that comparison with the 1980 mutual events gives "lower uncertainties, evaluated between 50 and 100 km" for Tethys, Dione and Rhea [@sats-dourneau-1993].

The Institut de mécanique céleste et de calcul des éphémérides (IMCCE) distributes the theory as Fortran subroutines that return "saturnicentric rectangular coordinates of the 8 major Saturnian satellites, in the FK4 system (B1950.0)" [@sats-dourneau-do87-readme]. The Bureau des longitudes used it with the planetary theory VSOP82 for its printed 1996 predictions of Saturnian phenomena [@sats-imcce-1996-booklet]. The 2009 predictions still listed it beside TASS as "Do93" [@sats-arlot-thuillot-2008].

### Harper and Taylor (1993)

Harper and Taylor augmented the Strugnell and Taylor catalogue "by several thousand additional observations" and fitted theories of all the satellites except Hyperion [@sats-harper-taylor-1993]. They determined the masses of Mimas to Dione and Saturn's form factors $J_2 = 0.016478 \pm 0.000038$ and $J_4 = -0.00110 \pm 0.00028$. Those form factors were "calculated assuming the equatorial radius of Saturn to be 60000 kilometres" [@sats-harper-taylor-1993]. They place Saturn's equator plane at node $168.8387^{\circ} \pm 0.0035^{\circ}$ and inclination $28.0653^{\circ} \pm 0.0016^{\circ}$ on the ecliptic and equinox of B1950. Their Table 2b sets Dourneau's values $168.8112^{\circ}$ and $28.0817^{\circ}$ beside these [@sats-harper-taylor-1993].

### TASS 1.6 and 1.7 (Vienne and Duriez, 1995 and 1996)

[?sats-tass] is "a new theory of high precision (about ten kilometers)" for Mimas, Enceladus, Tethys, Dione, Rhea, Titan and Iapetus [@sats-vienne-duriez-1995]. It is analytical in 55 dynamical parameters: the satellite masses, $J_2$, $J_4$ and $J_6$, six initial conditions per satellite, the inclination and node of Saturn's equator on the J2000 ecliptic, and Saturn's mass [@sats-vienne-duriez-1995]. TASS 1.6 was fitted to about 50,000 equations of condition from the Strugnell and Taylor catalogue [@sats-vienne-duriez-1995]. Each satellite is located by four complex osculating elements referred to Saturn's equator and its node on the ecliptic of 2000:

$$
p = \frac{n}{N} - 1, \qquad \lambda = Nt + \varepsilon, \qquad z = e\,\exp(\sqrt{-1}\,\varpi), \qquad \zeta = \sin\frac{i}{2}\,\exp(\sqrt{-1}\,\Omega)
$$

Here $N$ is the "mean mean motion", whose product with time is the linear part of the mean longitude, and $n$, $\lambda$, $e$, $i$, $\varpi$, $\Omega$ are the classical elliptic elements [@sats-vienne-duriez-1995]. The printed tables keep terms above 20 km. The full series include terms above 1 km [@sats-vienne-duriez-1995]. TASS 1.7, dated 1996 November 5, adds Hyperion and is distributed as the Fortran file `tass17.f`. Its positions are "referred to the center of Saturn and to the mean ecliptic and mean equinox for J2000.0 epoch" [@sats-tass17-readme].

By 2008 TASS had "a drift reaching about 100 km", and Arlot and Thuillot judged JPL's Cassini-fitted SAT252 more accurate. They still used TASS for the 2009 predictions because the event times differed by only 10 to 30 seconds of time [@sats-arlot-thuillot-2008].

### IMCCE numerical ephemerides (NOE, 2011 onward)

The IMCCE ephemeris NOE-6-2011-MAIN, a [?noe] solution, "was produced from the numerical integration of the orbital motion of the eight main Saturnian moons" with mutual perturbations, Saturn's gravity field to order six, solar and Jovian perturbations and tides [@sats-arlot-2012-phesat09]. It was fitted to astrometry from 1886 to 2009, including the 2009 mutual events. Its internal accuracy is "a few hundreds of meters". Its expected accuracy over the whole period is "about 600 km for the six innermost moons, and 1,800 km for Hyperion and Iapetus" [@sats-arlot-2012-phesat09]. It is published in [SPICE](https://naif.jpl.nasa.gov/naif/) format [@sats-arlot-2012-phesat09].

The same integration underlies Lainey's tidal studies. The 2012 fit found Saturn's tidal ratio $k_2/Q = (2.3 \pm 0.7)\times 10^{-4}$ [@sats-lainey-2012]. The 2017 fit added Cassini astrometry and gave $k_2 = 0.390 \pm 0.024$ [@sats-lainey-2017]. The 2020 fit found Titan receding at 11.3 ± 2.0 cm per year [@sats-lainey-2020]. These tidal terms matter for a developer only as a reason: an ephemeris without them drifts over centuries.

NOE stands for "Numerical Orbit and Ephemerides". It is an N-body code that was applied to the Martian moons before the Uranian ones [@sats-arlot-2006-uranus]. IMCCE's Miriade service labels its Saturnian satellite positions "INPOP19 + LTE-NOE" [@sats-miriade-ephemcc-output]. LTE stands for Laboratoire Temps Espace, the name that IMCCE's campaign page carries [@sats-imcce-phemu-campaign]. The MULTI-SAT phenomena server offers five theory sets for satellites S1 to S8: Lainey et al. (2015), Lainey (2011), Vienne and Duriez, Dourneau, and Harper and Taylor [@sats-multisat-saturn].

### JPL SAT ephemerides (SAT351 to SAT441)

JPL delivers numbered [?sats-sat-ephemeris] files as SPICE [?spk-kernel|SPK kernels]. The current main-satellite file is SAT441, and JPL's table cites Jacobson (2022), "The Orbits of the Main Saturnian Satellites, the Saturnian System Gravity Field, and the Orientation of Saturn's Pole" for it [@sats-jpl-sat-ephem-table] [@sats-jacobson-2022]. The NAIF copy `sat441.bsp` was created 2022-01-29 from SAT441.24. It covers Mimas to Phoebe, Helene, Telesto, Calypso, Methone, Polydeuces and Saturn itself from 1749 December 29 to 2250 January 5 [@sats-naif-sat441-cmt]. It is consistent with the planetary ephemeris [DE440](../../10-shared/08-lunar-and-solar-model/ephemerides.md), uses the model SATORBINT, and states a Chebyshev interpolation error of 7.5 m [@sats-naif-sat441-cmt] [@moon-park-2021]. The small inner satellites such as Janus and Epimetheus are in the separate file SAT415 [@sats-naif-sat415-cmt] [@sats-jpl-sat-ephem-table].

Each satellite SPK "provides the state ... of the named satellites relative to the barycenter of that planetary system", and the planet is carried "as a satellite of its own barycenter" [@sats-naif-sat-readme]. A program must therefore subtract Saturn's own state, body 699, to get a saturnicentric vector. Using the barycentre, body 6, puts every satellite off by Saturn's reflex motion.

### Accuracy, side by side

The 2009 mutual events give the only common yardstick in this topic. For the 23 best light curves, the root-mean-square [?o-minus-c] residuals in right ascension and declination were [@sats-arlot-2012-phesat09]:

| Theory or ephemeris | O − C in RA (mas) | O − C in Dec (mas) |
|---|---|---|
| TASS 1.7 (Vienne and Duriez) | 48.5 | 21.7 |
| Lainey and collaborators (NOE) | 16.4 | 20.7 |
| JPL SAT351 through [Horizons](https://ssd.jpl.nasa.gov/horizons/) | 17.3 | 21.6 |

One [?milliarcsecond|milliarcsecond] at Saturn is about 6 km, since Arlot and Thuillot equate 0.001 to 0.01 arcseconds with 6 to 60 km [@sats-arlot-thuillot-2008]. Direct ground-based astrometry reaches "0.1 arcsec at best, which corresponds to 600 km" [@sats-arlot-thuillot-2008]. The 1980 mutual events already reached post-fit residuals of 80 km, "approx. 0.01″ in astrometric accuracy" [@sats-rpx-dps-letter].

## Meeus chapter 46: satellite positions in the sky

Meeus's *Astronomical Algorithms*, second edition, chapter 46, computes apparent positions of Mimas to Iapetus [@earth-meeus-aa]. The formulas below are quoted from the MIT-licensed Go transcription by Sonia Keys, not from the book. Its test reproduces the book's Example 46.a [@sats-soniakeys-saturnmoons]. A JavaScript port carries the same constants [@sats-astronomia-saturn].

**The theory behind it.** The chapter's constants are Dourneau's. Mimas's mean longitude $127.64^{\circ} + 381.994497^{\circ}\,t_1$ with $t_1$ counted from JD 2411093.0, its eccentricity 0.01905, and the Mimas-Tethys [libration](../../10-shared/08-lunar-and-solar-model/lunar-figure-and-libration.md) epoch 1866.39 all appear in Dourneau's element table [@sats-soniakeys-saturnmoons] [@sats-dourneau-1993]. The equator node $168.8112^{\circ}$ and inclination $28.0817^{\circ}$ are the values Harper and Taylor attribute to Dourneau [@sats-harper-taylor-1993]. The positions therefore carry Dourneau's accuracy of hundreds of kilometres, not TASS's or SAT441's.

**Time arguments.** With JDE the Julian Ephemeris Day at the [?light-time]-corrected instant:

$$
\begin{aligned}
t_1 &= \mathrm{JDE} - 2411093.0, & t_2 &= t_1/365.25, & t_3 &= (\mathrm{JDE} - 2433282.423)/365.25 + 1950.0,\\
t_4 &= \mathrm{JDE} - 2411368.0, & t_5 &= t_4/365.25, & t_6 &= \mathrm{JDE} - 2415020.0,\\
t_7 &= t_6/36525, & t_8 &= t_6/365.25, & t_9 &= (\mathrm{JDE} - 2442000.5)/365.25,\\
t_{10} &= \mathrm{JDE} - 2409786.0, & t_{11} &= t_{10}/36525.
\end{aligned}
$$

Nine angles follow, in degrees [@sats-soniakeys-saturnmoons]:

$$
\begin{aligned}
W_0 &= 5.095\,(t_3 - 1866.39), & W_1 &= 74.4 + 32.39\,t_2, & W_2 &= 134.3 + 92.62\,t_2,\\
W_3 &= 42.0 - 0.5118\,t_5, & W_4 &= 276.59 + 0.5118\,t_5, & W_5 &= 267.2635 + 1222.1136\,t_7,\\
W_6 &= 175.4762 + 1221.5515\,t_7, & W_7 &= 2.4891 + 0.002435\,t_7, & W_8 &= 113.35 - 0.2597\,t_7.
\end{aligned}
$$

**One satellite, Mimas.** Each satellite gets a mean longitude, an equation of the centre $E_c$, a radius in Saturn radii, an inclination $i_j$ and a node $\Omega$ on Saturn's equator [@sats-soniakeys-saturnmoons]. Meeus writes C for the equation of the centre and γ for the inclination. They are renamed here because $C$ and γ name other quantities in this corpus:

$$
\begin{aligned}
L &= 127.64 + 381.994497\,t_1 - 43.57\sin W_0 - 0.720\sin 3W_0 - 0.02144\sin 5W_0,\\
p &= 106.1 + 365.549\,t_2, \qquad M = L - p,\\
E_c &= 2.18287\sin M + 0.025988\sin 2M + 0.00043\sin 3M,\\
\lambda &= L + E_c, \qquad r = \frac{3.06879}{1 + 0.01905\cos(M + E_c)}, \qquad i_j = 1.563, \qquad \Omega = 54.5 - 365.072\,t_2.
\end{aligned}
$$

Enceladus, Tethys and Dione follow the same pattern with their own constants. Rhea, Titan, Hyperion and Iapetus use longer series and a common routine that solves the equation of the centre to fifth order in $e$ [@sats-soniakeys-saturnmoons].

**From orbit to equator to ecliptic.** With $u = \lambda - \Omega$ and $w = \Omega - 168.8112^{\circ}$, the saturnicentric coordinates in Saturn radii are [@sats-soniakeys-saturnmoons]:

$$
X = r(\cos u\cos w - \sin u\cos i_j\sin w), \quad Y = r(\sin u\cos w\cos i_j + \cos u\sin w), \quad Z = r\sin u\sin i_j.
$$

The vector is rotated by $28.0817^{\circ}$ about the X axis and by $168.8112^{\circ}$ about the Z axis into the ecliptic and equinox of B1950. It is then rotated by Saturn's geocentric longitude $\lambda_0$ and latitude $\beta_0$, which the code precesses to B1950 first [@sats-soniakeys-saturnmoons]. A fictitious ninth body at $(0, 0, 1)$, the pole of Saturn's equator, goes through the same rotations. The angle $D = \operatorname{atan2}(A_0, C_0)$ of its projection then turns the result so that Y lies along the projected pole [@sats-soniakeys-saturnmoons]:

$$
X' = A\cos D - C\sin D, \qquad Y' = A\sin D + C\cos D, \qquad Z' = B.
$$

**Two small corrections.** The code then applies, for satellite $j$ with orbital radius $r_j$ [@sats-soniakeys-saturnmoons]:

$$
X' \leftarrow X' + \frac{|Z'|}{K_j}\sqrt{1 - \left(\frac{X'}{r_j}\right)^2}, \qquad W = \frac{\Delta}{\Delta + Z'/2475}, \qquad X = X'W, \quad Y = Y'W,
$$

with $K_j$ = 20947, 23715, 26382, 29876, 35313, 53800, 59222, 91820 for Mimas to Iapetus and $\Delta$ the Earth-Saturn distance in au. The factor $W$ is perspective. Since $Z'$ is in Saturn radii and $\Delta$ in au, the constant 2475 implies a unit radius of 149,597,870.7 / 2475 ≈ 60,444 km. The $K_j$ term is a differential [light-time](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) correction. A satellite nearer or farther than Saturn's centre by $Z'$ radii is seen as it was $Z'R/c$ earlier or later, and in that time it moves $v Z'R/c$ along its orbit. This gives $K = c/v$. With the chapter's own orbital radii, the 60,444 km unit and periods from the mean motions, $c/v$ is 20,946 for Mimas and 53,794 for Titan, against the tabulated 20,947 and 53,800. This check is arithmetic on the transcribed constants. The book's own explanation of $K_j$ is not quoted here.

**Light time.** Saturn's geocentric distance is iterated twice with $\tau = 0.0057755183\,\Delta$ days. The satellite theory is evaluated at the retarded instant $\mathrm{JDE} - \tau$ [@sats-soniakeys-saturnmoons]. Meeus's planetary positions come from VSOP87 [@sats-soniakeys-saturnmoons].

**Test vector.** For JDE 2451439.50074 the transcription's test reproduces Example 46.a, giving $X, Y$ in Saturn radii of (+3.102, −0.204) for Mimas, (+14.568, +4.738) for Titan and (−48.760, +4.137) for Iapetus [@sats-soniakeys-saturnmoons].

## Meeus chapter 45: the ring's aspect

Chapter 45 returns six quantities: $B$ and $B'$, the saturnicentric latitudes of the Earth and the Sun referred to the ring plane. These are the [?sats-ring-opening-b|ring opening angles]. It also returns $\Delta U$, the difference between the saturnicentric longitudes of the Sun and the Earth (see [?sats-delta-u]), the [?position-angle] $P$ of the northern semi-minor axis, and the axes $a$ and $b$ of the outer edge of the outer ring [@sats-soniakeys-saturnring]. The same caveat applies: the formulas are quoted from the Go transcription, whose test reproduces the book's Example 45.a [@sats-soniakeys-saturnring].

**Ring plane.** With $T$ in Julian centuries from J2000.0, the inclination and ascending node of the ring plane on the ecliptic are [@sats-soniakeys-saturnring]:

$$
i = 28.075216^{\circ} - 0.012998^{\circ}\,T + 0.000004^{\circ}\,T^2, \qquad
\Omega = 169.508470^{\circ} + 1.394681^{\circ}\,T + 0.000412^{\circ}\,T^2.
$$

**Geocentric Saturn.** The Earth's heliocentric $l_0, b_0, R$ and Saturn's $l, b, r$ come from VSOP87, converted to FK5. Saturn's are taken at $t - \tau$ in a two-pass light-time loop [@sats-soniakeys-saturnring]:

$$
x = r\cos b\cos l - R\cos l_0, \quad y = r\cos b\sin l - R\sin l_0, \quad z = r\sin b - R\sin b_0, \quad \Delta = \sqrt{x^2+y^2+z^2},
$$

$$
\lambda = \operatorname{atan2}(y, x), \qquad \beta = \arctan\frac{z}{\sqrt{x^2+y^2}}.
$$

**Opening angle seen from the Earth and ring axes.**

$$
\sin B = \sin i\cos\beta\sin(\lambda - \Omega) - \cos i\sin\beta, \qquad a = \frac{375.35''}{\Delta}, \qquad b = a\,|\sin B|.
$$

The inner edges are fixed fractions of $a$ and $b$ [@sats-soniakeys-saturnring]. The fraction is 0.8801 for the inner edge of the outer ring and 0.8599 for the outer edge of the inner ring. It is 0.6650 for the inner edge of the inner ring and 0.5486 for the inner edge of the "dusky" ring.

**Opening angle seen from the Sun.** Saturn's heliocentric position is corrected with $N = 113.6655^{\circ} + 0.8771^{\circ}\,T$ [@sats-soniakeys-saturnring]:

$$
l' = l - \frac{0.01759^{\circ}}{r}, \qquad b' = b - 0.000764^{\circ}\,\frac{\cos(l - N)}{r}, \qquad
\sin B' = \sin i\cos b'\sin(l' - \Omega) - \cos i\sin b'.
$$

**Longitude difference.**

$$
U_1 = \operatorname{atan2}(\sin i\sin b' + \cos i\cos b'\sin(l'-\Omega),\ \cos b'\cos(l'-\Omega)),
$$
$$
U_2 = \operatorname{atan2}(\sin i\sin\beta + \cos i\cos\beta\sin(\lambda-\Omega),\ \cos\beta\cos(\lambda-\Omega)), \qquad \Delta U = |U_1 - U_2|.
$$

**Position angle.** The pole of the ring plane is at ecliptic $\lambda_0 = \Omega - 90^{\circ}$, $\beta_0 = 90^{\circ} - i$. Saturn's $\lambda, \beta$ get the annual aberration [@sats-soniakeys-saturnring]:

$$
\lambda \leftarrow \lambda + 0.005693^{\circ}\,\frac{\cos(l_0 - \lambda)}{\cos\beta}, \qquad \beta \leftarrow \beta + 0.005693^{\circ}\,\sin(l_0 - \lambda)\sin\beta.
$$

Nutation in longitude $\Delta\psi$ is added to $\lambda_0$ and $\lambda$. Both points are converted to $(\alpha_0, \delta_0)$ and $(\alpha, \delta)$ with the true obliquity, and [@sats-soniakeys-saturnring]:

$$
\tan P = \frac{\cos\delta_0\sin(\alpha_0 - \alpha)}{\sin\delta_0\cos\delta - \cos\delta_0\sin\delta\cos(\alpha_0 - \alpha)}.
$$

**Test vector.** For JDE 2448972.50068 the test reproduces Example 45.a: $B = 16.442^{\circ}$, $B' = 14.679^{\circ}$, $\Delta U = 4.198^{\circ}$, $P = 6.741^{\circ}$, $a = 35.87''$, $b = 10.15''$ [@sats-soniakeys-saturnring].

![At a ring opening of 20 degrees the outer edge's minor axis is a third of its major axis, and the flattened globe hides the middle of the back of every ring edge while the front passes across it. Edges follow Meeus's fractions of $a = 375.35''/\Delta$ [@sats-soniakeys-saturnring], and the globe uses the 60,268 km and 54,364 km radii [@sats-nssdc-saturn].](img/sats-ring-ellipse.svg)

## Saturn's figure and the rings in kilometres

**The globe.** NASA's fact sheet gives an equatorial radius of 60,268 km and a polar radius of 54,364 km at the 1 bar level, and a flattening of 0.09796 [@sats-nssdc-saturn]. The NAIF constants kernel carries the same triaxial radii, 60268, 60268 and 54364 km, and the IAU pole at right ascension $40.589^{\circ} - 0.036^{\circ}T$ and declination $83.537^{\circ} - 0.004^{\circ}T$ [@sats-naif-pck00011]. Three other radii appear in the sources and must not be confused with the [?sats-saturn-radius]:

- 60,330 km is the reference radius of the gravity harmonics in SAT441 [@sats-naif-sat441-cmt].
- 60,000 km is the reference radius of Harper and Taylor's $J_2$ and $J_4$ [@sats-harper-taylor-1993].
- About 60,444 km is the unit implied by Meeus's perspective constant 2475, derived above from the transcribed code [@sats-soniakeys-saturnmoons].

A predictor of transits and occultations by the globe must use the oblate outline. The cited equatorial and polar radii differ by 5,904 km, computed from the 60,268 km and 54,364 km values, so a spherical model misplaces a contact on the polar part of the limb by up to that distance. Some services ignore it, as [the phenomena note](saturn-phenomena-and-mutual-events.md#what-the-public-tools-model) records.

**The rings.** NASA's ring fact sheet gives the main edges in kilometres from Saturn's centre, with normal optical depth $\tau$ [@sats-nssdc-rings]:

| Edge | Radius (km) | Meeus fraction × a/2, at 1 au (km) | Normal optical depth of the ring |
|---|---|---|---|
| A outer | 136,780 | 136,115 | A: 0.4 to 1.0 |
| A inner | 122,340 | 119,795 (0.8801) | |
| Cassini Division | 117,507 to 122,340 | | 0 to 0.1 |
| B outer | 117,507 | 117,045 (0.8599) | B: 0.4 to 2.5 |
| B inner, C outer | 91,975 | 90,517 (0.6650) | C: 0.05 to 0.35 |
| C inner | 74,658 | 74,673 (0.5486) | |

Meeus's $a$ and $b$ are full axes, so the radius of an edge is half the axis. The third column converts half of Meeus's $a = 375.35''$ at 1 au into a radius with 725.27 km per arcsecond. That scale follows from the au of 149,597,870.7 km used in SAT441's constants [@sats-soniakeys-saturnring] [@sats-naif-sat441-cmt]. Meeus's outer edge is 0.5 per cent smaller than the fact sheet's. His inner edge of ring A is 2.1 per cent smaller, which narrows the Cassini Division on a drawn ring. These differences are below the resolution of a sketch. They matter for a prediction of when a satellite enters the Cassini Division's shadow. The B ring is thick enough, with $\tau$ up to 2.5, to hide a satellite almost completely. The C ring and Cassini Division pass much of the light [@sats-nssdc-rings]. How these optical depths enter an eclipse calculation, and how a sky-plane position becomes a ring-plane radius, is in [the phenomena note](saturn-phenomena-and-mutual-events.md#eclipses-by-the-rings-and-the-iapetus-case).

The ring plane is not fixed. Solar torques make it precess. The 1993 occultation results implied "an advance of ~2 hours in the time of ring plane crossing after a 15 yr interval" [@sats-rpx-dps-letter]. Meeus's polynomial for $i$ and $\Omega$ and the IAU pole in the PCK are both smooth fits. Neither carries that precession explicitly [@sats-soniakeys-saturnring] [@sats-naif-pck00011].

## Software and the theory each one uses

| Program or service | Saturn's main satellites | Source read |
|---|---|---|
| Meeus ch. 46 ports (soniakeys Go, astronomia JS) | Dourneau's elements, simplified | [@sats-soniakeys-saturnmoons] [@sats-astronomia-saturn] |
| [Stellarium](https://stellarium.org/) | TASS 1.7, as a C rearrangement by J. Gajdosik | [@sats-stellarium-tass17] [@sats-stellarium-ephemwrapper] |
| Cartes du Ciel (Skychart) | TASS, translated from Xplanet's libmoons, and Zadunaisky elements for Phoebe | [@sats-skychart-plansat] |
| IMCCE Miriade (ephemcc) | INPOP19 planets with LTE-NOE satellites | [@sats-miriade-ephemcc-output] |
| IMCCE and Sternberg Astronomical Institute (SAI) MULTI-SAT | Choice of Lainey 2015, Lainey 2011, TASS, Dourneau, Harper and Taylor | [@sats-multisat-saturn] |
| JPL Horizons | SAT441 for Mimas to Iapetus, SAT415 for small inner moons | [@sats-jpl-sat-ephem-table] [@sw-horizons-manual] |
| SPICE (NAIF generic kernels) | `sat441.bsp`, `sat415.bsp` with DE440 | [@sats-naif-sat441-cmt] [@sats-naif-sat415-cmt] |

Stellarium's rearrangement changes the independent variable to $T = \mathrm{JD} - 2444240$ for all satellites. It also precomputes constant terms and merges terms of equal frequency [@sats-stellarium-tass17]. Cartes du Ciel states that its satellite code is a Pascal rewrite of Xplanet's libmoons, so that Cartes du Ciel and Xplanet draw satellites in the same places [@sats-skychart-plansat]. The [Astronomical Almanac](https://en.wikipedia.org/wiki/Astronomical_Almanac)'s satellite section has been printed from compact series. A 1995 Royal Greenwich Observatory abstract describes moving it to the Chapront and Vu mixed-function form [@sats-taylor-yallop]. No primary source in this corpus states which ephemeris feeds the current Almanac's Saturn pages.

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Dourneau 1993 | The element tables behind Meeus ch. 46, a century of observations, honest kilometre uncertainties per satellite |
| Harper and Taylor 1993 | An independent fit with masses, $J_2$, $J_4$, and a direct comparison table against Dourneau |
| Vienne and Duriez 1995, TASS 1.7 README | The semi-analytical theory most open-source planetaria use, its element definitions and frame |
| Arlot et al. 2012 | The only side-by-side O − C of TASS, NOE and a JPL ephemeris against mutual-event astrometry |
| NAIF sat441.cmt and JPL table | Exact span, bodies, planetary ephemeris and interpolation error of the current JPL file |
| soniakeys ch. 45 and 46 transcriptions | Implementable formulas with constants and test vectors from Meeus's worked examples |
| NSSDC fact sheets and NAIF PCK | Kilometre radii of globe and ring edges, flattening, optical depths and pole |

## What a developer should do

1. **Use SAT441 through SPICE for anything that will be compared with observations.** Load `sat441.bsp` with a DE440 kernel, and subtract body 699 to get saturnicentric vectors [@sats-naif-sat441-cmt] [@sats-naif-sat-readme].
2. **Use TASS 1.7 when an analytic, file-free model is needed.** Expect residuals of tens of milliarcseconds in right ascension, about three times SAT351's in 2009 [@sats-arlot-2012-phesat09] [@sats-tass17-readme].
3. **Treat Meeus chapter 46 as a drawing aid.** It carries Dourneau's hundreds-of-kilometres accuracy and VSOP87 planets. Use its two test vectors to validate a port, and do not use it for event times [@sats-dourneau-1993] [@sats-soniakeys-saturnmoons].
4. **Use Meeus chapter 45 for B, B′, ΔU and P.** These angles are smooth and the chapter is adequate for them. Take the ring radii in kilometres from the fact sheet rather than the fixed fractions if the product will predict ring-shadow events [@sats-soniakeys-saturnring] [@sats-nssdc-rings].
5. **Model the globe as an oblate spheroid of 60,268 by 54,364 km.** Keep the gravity reference radii out of the geometry [@sats-naif-pck00011] [@sats-naif-sat441-cmt].
6. **Read first:** Arlot et al. 2012 for the accuracy table, Vienne and Duriez 1995 for the theory, and the SAT441 comment file for the current JPL fit.

## What this changes

The eclipse pipeline's ephemeris layer gains a second level. Planet positions come from DE440, and satellite positions relative to their planet come from a satellite file such as SAT441. The two must be consistent, which SAT441's own DE440 header guarantees [@sats-naif-sat441-cmt]. The body-shape layer gains a non-spherical primary with a ring system, which the solar-eclipse pipeline never needed.

## Open questions

- **Meeus's source statement.** Obtain *Astronomical Algorithms*, second edition, chapters 45 and 46, and record the book's own attribution of the satellite theory and of the ring fractions. The attribution here rests on matched constants.
- **The Astronomical Almanac's current Saturn source.** Obtain the "Notes and References" section of a recent Astronomical Almanac and record which SAT or NOE file feeds Section F.
- **TASS 1.7 drift today.** Obtain or compute a TASS 1.7 minus SAT441 difference series for 2024 to 2026, the PHESAT season, to replace the 2008 "about 100 km" estimate.
- **Jacobson 2022.** Read AJ 164, 199 for SAT441's stated position uncertainties per satellite, which the comment file does not give.
