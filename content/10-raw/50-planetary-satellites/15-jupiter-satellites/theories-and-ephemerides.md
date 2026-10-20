---
title: Theories and ephemerides of the Galilean satellites
seo_title: Galilean Satellite Ephemerides: Lieske E5 to JUP365
description: The satellite theories behind Jupiter-moon predictions, from Sampson's tables and Lieske's E5 to Lainey's NOE and JPL's JUP365, with Meeus's formulas.
order: 1
status: working
updated: 2026-10-17
tags: [jupiter, galilean-satellites, ephemerides, lieske, lainey, jup365, meeus]
---

::: summary
- **Three families of theory have carried the predictions.** Sampson's analytical theory, published as tables in 1910 and as a theory in 1921, was redeveloped by Lieske in 1977 with 49 adjustable constants. Its fits E-1 to E5 and Arlot's G-5 served until about 2014. Numerical integrations replaced it: Lainey's L1 (2004) and NOE series at [IMCCE](https://www.imcce.fr/), and Jacobson's JUP series at JPL [@jup-lieske-1977] [@jup-arlot-1982] [@jup-lainey-2004a] [@jup-naif-jup310-cmt].
- **The published phenomena of the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) changed theory twice.** They used G-5 (Sampson-Lieske) up to the 2014 predictions, Lainey's L1 for 2015 to 2022, and Lainey's 2021 NOE solution after that [@jup-imcce-phenjupiter-readme].
- **The analytical theory had internal errors of a few hundred km.** Lainey et al. say so of the Sampson-Lieske theory, and the L1 README promises "a few hundreds of kilometers" for 1970 to 2010. The modern numerical fits reach about 0.025 arcseconds with [mutual events](mutual-events.md), about 75 km at Jupiter [@jup-lainey-2009] [@jup-imcce-l11-readme].
- **JUP365 is JPL's current Galilean ephemeris.** It is the JUP365.26 global fit, merged with DE440, spans 1600 to 2200, uses a Jupiter radius of 71,492 km and carries a 16 m Chebyshev interpolation error. JUP310 (2013) was the DE430-era predecessor [@jup-naif-jup365-cmt] [@jup-naif-jup310-cmt].
- **[Meeus](https://en.wikipedia.org/wiki/Jean_Meeus) chapter 44 gives two algorithms.** The low-accuracy method uses four circular orbits with one perturbation each. The high-accuracy method is an abridged E5 with explicit rotations, a differential [light-time](../../10-shared/07-earth-and-time/refraction-light-time-and-frames.md) term and a perspective factor. The formulas here are transcribed from two open implementations, not from the printed book [@jup-soniakeys-jupitermoons] [@jup-pymeeus-jupitermoons].
- **Desktop planetaria use different theories.** [Stellarium](https://stellarium.org/) uses Lainey's L1.2 synthetic series for all four moons. Cartes du Ciel (Skychart) uses E5 or [SPICE](https://naif.jpl.nasa.gov/naif/) kernels through CALCEPH. PyMeeus and the Go port use the Meeus abridgement of E5 [@jup-stellarium-l12] [@sats-skychart-plansat] [@jup-pymeeus-jupitermoons].
:::

**The question.** Which theories of motion of the [?jup-galilean-satellites|Galilean satellites] have been used to predict their phenomena, when was each one made, what data were they fitted to, and how accurate are they? Which formulas does Meeus give for a developer who wants positions without a satellite kernel, and which theory does each common program actually use?

## From Cassini's tables to Sampson

The first usable predictions were Cassini's. In Cassini's own words, prediction "only became possible in 1668, when Mr. Cassini published ephemerides from these satellites, and the method to calculate their eclipses" [@jup-bobis-lequeux-2008]. Delambre built new tables of the satellites' motion in 1792 and 1817 from about 6000 eclipse observations. Those reductions were thought lost for most of the nineteenth century [@jup-lieske-1986].

R. A. Sampson published "Tables of the Four Great Satellites of Jupiter" in 1910 and "Theory of the Four Great Satellites of Jupiter" in 1921 [@jup-lieske-1986] [@jup-lieske-1977]. Lieske calls the 1921 theory "the most widely used basis for calculating the coordinates of the Galilean satellites" in 1977. Sampson aimed at one arcsecond as seen from Jupiter's centre, which Lieske converts to 2, 3.3, 5.2 and 9.1 km for satellites I to IV. Lieske also states that Sampson did not reach that goal [@jup-lieske-1977]. Sampson's 1910 search for the Delambre material recovered the eclipse records of satellites II and IV only [@jup-lieske-1986].

## The Sampson-Lieske theory and its fits

Lieske's 1977 paper is a redevelopment of Sampson's method with computer algebra. It removes algebraic and arithmetic errors, adds solar terms and the 3:7 commensurability of satellites III and IV, allows free [libration](../../10-shared/08-lunar-and-solar-model/lunar-figure-and-libration.md), and expresses the coordinates as analytic functions of 49 arbitrary constants with analytic partial derivatives [@jup-lieske-1977]. This is the [?jup-sampson-lieske|Sampson-Lieske theory]. The constants are fitted separately, and each fit has its own name.

| Fit | Data | Source |
|---|---|---|
| E-1 | Old eclipse observations, 1878 to 1903 | Arlot (1982) describing Lieske (1978) [@jup-arlot-1982] |
| E-2 | E-1 data, visual eclipses 1903 to 1972, mutual events of 1973, photographic plates 1967 to 1978 | Arlot (1982) describing Lieske (1980) [@jup-arlot-1982] |
| G-5 | 8856 photographic observations, 1891 to 1978 | Arlot (1982) [@jup-arlot-1982] |
| E5 | Produced for the Galileo mission, B1950 frame with J2000 results | Lieske (1998), abstract only [@jup-lieske-1998] |

E-2 was still the comparison standard of the eclipse-timing programme of the Association of Lunar and Planetary Observers (ALPO) in 2006 [@jup-westfall-alpo]. G-5 was the theory of IMCCE's published phenomena until the 2014 predictions [@jup-imcce-phenjupiter-readme]. The E5 abstract describes E5 as better than E3 and E4 and recommends it for general use [@jup-lieske-1998].

The weakness of the analytical approach is the missing long-period terms. Lainey et al. state that the Sampson-Lieske model "has internal errors on the order of a few hundred kilometres". They attribute the scatter of published tidal accelerations to that error [@jup-lainey-2009].

## Meeus chapter 44: the low-accuracy method

Meeus's *Astronomical Algorithms* gives two methods for the satellites' apparent positions. The formulas below are those of Sonia Keys's Go port, which names the chapter. They are not checked against the printed edition [@jup-soniakeys-jupitermoons] [@jup-meeus-1998-ch44]. Angles are in degrees and $d = \mathrm{JDE} - 2451545.0$ in days of TT.

$$
\begin{aligned}
V &= 172.74 + 0.00111588\,d, \qquad M = 357.529 + 0.9856003\,d,\\
N &= 20.020 + 0.0830853\,d + 0.329\sin V, \qquad J = 66.115 + 0.9025179\,d - 0.329\sin V,\\
A &= 1.915\sin M + 0.020\sin 2M, \qquad B = 5.555\sin N + 0.168\sin 2N, \qquad K = J + A - B,\\
R &= 1.00014 - 0.01671\cos M - 0.00014\cos 2M, \qquad r = 5.20872 - 0.25208\cos N - 0.00611\cos 2N,\\
\Delta &= \sqrt{r^2 + R^2 - 2rR\cos K}, \qquad \psi = \arcsin\!\left(\frac{R}{\Delta}\sin K\right).
\end{aligned}
$$

$R$ and $r$ are the Earth-Sun and Jupiter-Sun distances in au, and $\Delta$ is the Earth-Jupiter distance in au. $\psi$ is the phase angle of Jupiter. The [?jup-jovicentric-declination|jovicentric declinations] of the Sun and the Earth follow from $\lambda = 34.35 + 0.083091\,d + 0.329\sin V + B$:

$$
D_S = 3.12\sin(\lambda + 42.8), \qquad
D_E = D_S - 2.22\sin\psi\cos(\lambda + 22) - 1.30\,\frac{r-\Delta}{\Delta}\sin(\lambda - 100.5).
$$

Each satellite has an angle $u$, evaluated at a time earlier by the light-time $\Delta/173$ days. Here 173 is the speed of light in au per day.

$$
\begin{aligned}
u_1 &= 163.8069 + 203.4058646\,(d - \Delta/173) + \psi - B,\\
u_2 &= 358.4140 + 101.2916335\,(d - \Delta/173) + \psi - B,\\
u_3 &= 5.7176 + 50.2345180\,(d - \Delta/173) + \psi - B,\\
u_4 &= 224.8092 + 21.4879800\,(d - \Delta/173) + \psi - B.
\end{aligned}
$$

One periodic term corrects each angle and each radius. With $G = 331.18 + 50.310482\,(d - \Delta/173)$ and $H = 87.45 + 21.569231\,(d - \Delta/173)$:

$$
\begin{aligned}
u_1 &\mathrel{+}= 0.473\sin 2(u_1 - u_2), & r_1 &= 5.9057 - 0.0244\cos 2(u_1 - u_2),\\
u_2 &\mathrel{+}= 1.065\sin 2(u_2 - u_3), & r_2 &= 9.3966 - 0.0882\cos 2(u_2 - u_3),\\
u_3 &\mathrel{+}= 0.165\sin G, & r_3 &= 14.9883 - 0.0216\cos G,\\
u_4 &\mathrel{+}= 0.843\sin H, & r_4 &= 26.3627 - 0.1939\cos H.
\end{aligned}
$$

The radii are in Jupiter equatorial radii. The apparent [?jup-xy-coordinates|coordinates X, Y] are then

$$
X = r\sin u, \qquad Y = -r\cos u\,\sin D_E .
$$

The port computes the periodic arguments from the uncorrected $u$ and evaluates $X$ and $Y$ with the corrected ones [@jup-soniakeys-jupitermoons]. The method treats each orbit as a circle in Jupiter's equatorial plane. It has no inclination terms and no differential light-time.

## Meeus chapter 44: the high-accuracy method (abridged E5)

The second method is an abridgement of E5. In the Go port and in PyMeeus, the time argument is $t = \mathrm{JDE} - 2443000.5 - \tau$, where $\tau$ is the light-time from Jupiter to the observer found by iterating on VSOP87 positions [@jup-soniakeys-jupitermoons] [@jup-pymeeus-jupitermoons]. The mean longitudes are

$$
\begin{aligned}
l_1 &= 106.07719 + 203.488955790\,t, & l_2 &= 175.73161 + 101.374724735\,t,\\
l_3 &= 120.55883 + 50.317609207\,t, & l_4 &= 84.44459 + 21.571071177\,t,
\end{aligned}
$$

with perijove longitudes $\pi_i$, node longitudes $\omega_i$, the longitude $\psi$ of the node of Jupiter's equator on the ecliptic, and the solar arguments $G$, $G'$ and $\Pi = 13.469942^{\circ}$ [@jup-soniakeys-jupitermoons]. This $\psi$ is not the phase angle of the low-accuracy method. The periodic sums $\Sigma_i$ add to the mean longitudes. Their largest terms show the Laplace resonance:

$$
\Sigma_1 \ni 0.47259\sin 2(l_1 - l_2), \quad \Sigma_2 \ni 1.06476\sin 2(l_2 - l_3), \quad \Sigma_3 \ni 0.16490\sin(l_3 - \pi_3), \quad \Sigma_4 \ni 0.84287\sin(l_4 - \pi_4).
$$

The Go port carries 21, 37, 43 and 50 terms in the four sums, plus series for the latitudes $B_i$ and the radii $R_i$. The radius series start from 5.90569, 9.39657, 14.98832 and 26.36273 Jupiter radii [@jup-soniakeys-jupitermoons]. Precession in longitude from B1950 enters as $p_{1950} = (1.3966626 + 0.0003088\,T_0)\,T_0$ degrees, Meeus's $P$, which is not a position angle, with $T_0 = (\mathrm{JDE} - 2433282.423)/36525$. The inclination of Jupiter's equator on its orbit is $I = 3.120262^{\circ} + 0.0006^{\circ}\,T$ with $T$ in Julian centuries from J1900 [@jup-soniakeys-jupitermoons].

Five rotations take the jovicentric rectangular coordinates to the sky plane. A fictitious fifth satellite at $(0, 0, 1)$, on Jupiter's pole, gives the angle $D = \operatorname{atan2}(A_5, C_5)$ that aligns Y with the projected pole [@jup-soniakeys-jupitermoons]. Two corrections follow, quoted from the code [@jup-soniakeys-jupitermoons] [@jup-pymeeus-jupitermoons]:

$$
X \leftarrow X + \frac{|Z|}{K_i}\sqrt{1 - \left(\frac{X}{R_i}\right)^2}, \qquad
W = \frac{\Delta}{\Delta + Z/2095}, \qquad X \leftarrow WX, \quad Y \leftarrow WY,
$$

with $K_i = 17295, 21819, 27558, 36548$ for satellites I to IV. The first term is the [?jup-differential-light-time|differential light-time]. Each $K_i$ is close to the speed of light divided by the mean orbital speed: $299{,}792/17.33 = 17{,}299$ for [Io](https://en.wikipedia.org/wiki/Io_(moon)) and $299{,}792/13.74 = 21{,}819$ for [Europa](https://en.wikipedia.org/wiki/Europa_(moon)), with the speeds of Westfall's table [@jup-westfall-alpo]. The second is the perspective factor. 2095 is the number of Jupiter radii in one au if the radius is about 71,400 km. The code does not name the radius it assumes [@jup-soniakeys-jupitermoons].

PyMeeus adds a solar variant. With `solar=True` it sets the Earth-Sun distance to zero, so the same series give the coordinates as seen from the Sun. Those coordinates decide eclipses and shadow transits [@jup-pymeeus-jupitermoons]. [Eclipses, occultations, transits and shadows](eclipses-occultations-transits-shadows.md) uses this distinction.

## Lainey's numerical ephemerides at IMCCE

Lainey, Duriez and Vienne published a theory "based on the numerical integration of elaborated equations of motion" in 2004. They tested many usually neglected perturbations and compared the model with E5 [@jup-lainey-2004a]. Paper II fitted it to observations from 1891 and named the result L1 [@jup-lainey-2004b]. The L1.1 subroutine README (2007) states a fit to observations from 1891 to 2003 and an expected accuracy of "few hundreds of kilometers for the period [1970:2010]" [@jup-imcce-l11-readme]. Its input is TDB in Julian days from the epoch JD 2433282.5, which is 1950 January 1 at 0h TDB. Its output is either elliptic elements in Jupiter's mean equator of date or jovicentric Cartesian coordinates in the J2000 Earth mean equator [@jup-imcce-l11-readme].

Lainey, Duriez and Vienne then turned L1 into a quasi-periodic Fourier series by frequency analysis. The series' arguments are integer combinations of the system's fundamental arguments [@jup-lainey-2006]. This is the L1.2 form that a program can evaluate without an integrator.

The next solution was fitted with the tidal dissipation of Io and Jupiter as free parameters. It used astrometric observations from 1891 to 2007 [@jup-lainey-2009]. Its 1σ post-fit residuals are mostly between 0.02 and 0.15 arcseconds, 60 to 450 km at Jupiter. The mutual events from 1973 to 2003 have a 1σ accuracy of about 0.025 arcseconds [@jup-lainey-2009]. The code is the [?noe|NOE] integrator, for Numerical Orbit and Ephemerides [@jup-lainey-hdr]. The resulting kernel is NOE-5-2010-GAL. The PHEMU15 reduction used it with INPOP13c [@jup-saquet-2018]. The reduction of observations from the Vainu Bappu Observatory (VBO) calls it "L2" and used the kernel NOE-5-2010-GAL-a2.bsp [@jup-vasundhara-2017]. According to Saquet et al., NOE models Jupiter's gravity field to degree six and the satellites' to degree two. It adds solar and Saturnian perturbations from DE430, Jupiter's precession and the tides through $k_2/Q$, and it integrates in a jovicentric frame on the Earth mean equator J2000 [@jup-saquet-2018].

The current IMCCE solution is NOE-5-2021. It was fitted to "all Earth based (including radar) observations from 1891, HST, Voyager and Galileo imaging data". It covers 1879 December 31 to 2049 December 30 [@jup-imcce-noe-2021]. A long variant, NOE-5-2021L, covers 1649 to 1999 and is "mostly designed for comparison with old eclipses (1652-1900)". Both are SPICE [?spk-kernel|SPK kernels] [@jup-imcce-noe-2021]. Their companion text kernel gives Jupiter's GM as 126,683,750.52 km³ s⁻² [@jup-imcce-noe-2021].

## JPL's JUP series

JPL's Galilean ephemerides are numerical integrations by R. A. Jacobson, distributed as SPK kernels by NAIF. JUP310 was released on 2013 November 25. It is the JUP310.2 global fit "to Earthbased and spacecraft data", merged with DE430, and spans 1799 December 18 to 2200 January 14 [@jup-naif-jup310-cmt]. Its Chebyshev interpolation error is 0.5 m. It adopts an equatorial radius of 71,492 km [@jup-naif-jup310-cmt].

JUP365 is the current generic kernel. Its comment file names the JUP365.26 global fit, the DE440 planetary ephemeris, a span from 1600 January 10 to 2200 January 10, and a "Chebyshev interpolation error: 16.00 meters" [@jup-naif-jup365-cmt]. The kernel carries Io, Europa, [Ganymede](https://en.wikipedia.org/wiki/Ganymede_(moon)), [Callisto](https://en.wikipedia.org/wiki/Callisto_(moon)), Amalthea, Thebe, Adrastea, Metis and Jupiter relative to the Jupiter barycentre. It is 1,136,581,632 bytes [@jup-naif-jup365-cmt] [@sats-naif-aa-summaries]. JUP347, JUP348 and JUP349 carry only irregular outer moons. JUP365 is the one to use for the [Galilean satellites](_index.md) [@sats-naif-aa-summaries].

[Skyfield](https://rhodesmill.org/skyfield/) reads these kernels as ordinary SPK files. Its documentation uses JUP310 as the example "for its support of Jupiter's moons". It warns that apparent positions need the segments of a planetary ephemeris added, because the satellite kernel lacks Saturn [@moon-skyfield-planets]. [Horizons](https://ssd.jpl.nasa.gov/horizons/) uses JPL's satellite solutions for its observer tables. Its manual warns that satellite eclipse circumstances "may not be accurate to less than a minute since factors such as the primarys' oblateness and atmosphere are not currently modelled" [@sw-horizons-manual].

## Accuracy compared

| Theory or file | Date | Data span | Stated accuracy | Source |
|---|---|---|---|---|
| Sampson | 1910, 1921 | eclipses to about 1903 | goal 2 to 9 km, not reached | [@jup-lieske-1977] |
| Sampson-Lieske (E-2, G-5, E5) | 1977 to 1998 | to 1978 (G-5) | internal errors of a few hundred km | [@jup-lainey-2009] |
| L1 | 2004 | 1891 to 2003 | a few hundred km, 1970 to 2010 | [@jup-imcce-l11-readme] |
| NOE (L2) | 2009 | 1891 to 2007 | residuals 0.02 to 0.15 arcseconds | [@jup-lainey-2009] |
| JUP310 | 2013 | through 2013 | rms O-C 65.5 mas against PHEMU15 | [@jup-saquet-2018] |
| NOE-5-2010-GAL | 2009 to 2010 | as NOE | rms O-C 49.9 mas against PHEMU15 | [@jup-saquet-2018] |
| JUP365 | 2021 | not stated in the comment file | agreement at about 5 mas with the 2021 Brazilian light curves | [@jup-catani-2023] |
| NOE-5-2021 | 2021 | 1891 onwards, HST, spacecraft | not stated in the README | [@jup-imcce-noe-2021] |

Among the papers cited in this topic, the PHEMU15 comparison is the only head-to-head of two modern ephemerides on the same independent data. Both NOE-5-2010-GAL and JUP310 used the PHEMU85 to PHEMU03 data. Their difference of 15 [?milliarcsecond|milliarcseconds] in rms [?o-minus-c|O-C] is 45 km at Jupiter [@jup-saquet-2018]. The "rms O-C" there includes the measurement error of amateur light curves, so it is an upper bound on the ephemeris error. The same paper reports an internal accuracy of the NOE theory of "around 1 km" as a private communication from Lainey [@jup-saquet-2018].

## Which program uses which theory

| Program | Theory in the code | Time argument | Source |
|---|---|---|---|
| Stellarium | L1.2 (Lainey, Vienne, Duriez) ported from FORTRAN, all four moons | TT JD, $t = \mathrm{JD} - 2433282.5$, output Jupiter-centred in the VSOP87 frame | [@jup-stellarium-l12] |
| Cartes du Ciel | E5 from Lieske (1998), with more digits than Meeus, or SPK kernels through CALCEPH when enabled | JDE minus light-time | [@sats-skychart-plansat] |
| PyMeeus | Meeus chapter 44 high-accuracy method (abridged E5) | JDE, iterated light-time | [@jup-pymeeus-jupitermoons] |
| soniakeys/meeus (Go) | Meeus chapter 44, both methods | JDE | [@jup-soniakeys-jupitermoons] |
| Juptool (Nagoya) | Meeus chapter 44 high-accuracy method "with several 'short cuts'" | not stated | [@jup-juptool-nagoya] |
| Skyfield | any SPK, for example JUP310 or JUP365 | TDB through the kernel | [@moon-skyfield-planets] |
| Horizons | JPL satellite solutions with the DE planets | not examined | [@sw-horizons-manual] |
| IMCCE phenomena files | G-5 to 2014, L1 for 2015 to 2022, Lainey 2021 after | TT | [@jup-imcce-phenjupiter-readme] |

Stellarium's L1.2 port starts from the elements $a$, $L$, $k + ih$ and $q + ip$, each a sum of cosine or sine terms in $t$. It converts them to position and velocity, then rotates them with a fixed matrix into the VSOP87 frame [@jup-stellarium-l12]. Cartes du Ciel's `jupsat` function cites Lieske (1998) and starts $l_1$ as $106.077187^{\circ} + 203.48895579033^{\circ}\,t$. That has two more digits in the rate than the Meeus abridgement [@sats-skychart-plansat] [@jup-soniakeys-jupitermoons].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Lieske (1977), first page [@jup-lieske-1977] | What Sampson attempted, and what the 49-constant redevelopment changed |
| Arlot (1982), first page [@jup-arlot-1982] | The data behind E-1, E-2 and G-5 |
| IMCCE phenjupiter README [@jup-imcce-phenjupiter-readme] | Which theory produced which year's published phenomena |
| L1.1 README and NOE-5-2021 README [@jup-imcce-l11-readme] [@jup-imcce-noe-2021] | Time scale, epoch, frames, data span and coverage of the IMCCE files |
| Lainey et al. (2009) [@jup-lainey-2009] | Quantified internal error of Sampson-Lieske, and residual levels of the numerical fit |
| NAIF comment files [@jup-naif-jup365-cmt] [@jup-naif-jup310-cmt] | Version, planetary ephemeris, span, radius and interpolation error of JPL's kernels |
| Saquet et al. (2018) [@jup-saquet-2018] | The only comparison of NOE and JUP310 on the same independent data |
| Go and Python ports of Meeus [@jup-soniakeys-jupitermoons] [@jup-pymeeus-jupitermoons] | Implementable formulas, including the light-time constants |
| Stellarium and Cartes du Ciel source [@jup-stellarium-l12] [@sats-skychart-plansat] | What two widely used programs actually evaluate |

## What a developer should do

1. **Use JUP365 with DE440 through SPICE or Skyfield** for positions accurate to tens of km. Load the planetary kernel too, so that apparent positions can be formed [@jup-naif-jup365-cmt] [@moon-skyfield-planets].
2. **Use NOE-5-2021 as the independent check.** It is the solution IMCCE uses for its own phenomena from 2023 on, and the PHEMU15 comparison shows that NOE and JPL differ at the tens-of-km level [@jup-imcce-phenjupiter-readme] [@jup-saquet-2018].
3. **Use Meeus's high-accuracy method only where kernels cannot be shipped.** Keep the differential light-time and perspective corrections, and compute a separate solar version for eclipses and shadows. Expect errors in the hundreds of km, the level of the Sampson-Lieske theory it abridges [@jup-pymeeus-jupitermoons] [@jup-lainey-2009].
4. **Do not use the low-accuracy method for phenomena times.** It has circular, coplanar orbits and one perturbation per satellite [@jup-soniakeys-jupitermoons].
5. **Record the satellite ephemeris version with every prediction.** The same year's events were computed from G-5, L1 or NOE depending on the publication date [@jup-imcce-phenjupiter-readme].

Read first: the IMCCE phenjupiter README, the JUP365 comment file, Lainey et al. (2009) and Saquet et al. (2018).

## What this changes

The eclipse pipeline gains a second ephemeris layer. Solar eclipse work needs the Sun, Earth and Moon from a DE file, as in [ephemerides](../../10-shared/08-lunar-and-solar-model/ephemerides.md). Jovian phenomena need a satellite kernel as well, merged with the same DE version. The pipeline should treat the pair, for example DE440 with JUP365, as one versioned input [@jup-naif-jup365-cmt].

## Open questions

- **Lieske (1998), full text.** Obtain the A&AS paper through a library to quote E5's fitted data span, its stated accuracy and the complete term lists, and to check the Meeus abridgement and the Cartes du Ciel coefficients against it.
- **The printed Meeus chapter 44.** Check the transcribed constants, the sign convention of X, and the radius behind the constant 2095 against the printed second edition.
- **JUP365 documentation.** Find a JPL report or paper that states the JUP365 data set and its formal uncertainty, which the comment file does not give.
- **NOE-5-2021 technical note.** The README promises "technical notes for details (soon available)". Obtain it for the fitted data and accuracy.
- **Cartes du Ciel default kernel.** Identify which satellite solution the distributed `cdcbase.bsp` and `cdcext.bsp` files contain.
