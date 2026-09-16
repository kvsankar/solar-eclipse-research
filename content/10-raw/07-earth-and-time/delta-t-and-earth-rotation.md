---
title: ΔT and Earth rotation
description: How TT − UT1 enters the Besselian elements, the ΔT models from Morrison and Stephenson to the IERS series, how far off a prediction is one to a hundred years ahead, and what each predictor used for 2017 and 2024.
order: 2
status: working
updated: 2026-09-15
tags: [delta-t, ut1, utc, leap-seconds, polar-motion, sidereal-time, iers]
---

::: summary
- **ΔT = TT − UT1** is the only quantity in eclipse prediction that cannot be computed from physics in advance. It equals $32.184 + (\mathrm{TAI} - \mathrm{UTC}) - (\mathrm{UT1} - \mathrm{UTC})$ s, which on 2026 September 4 was $32.184 + 37 - 0.000946 = 69.183$ s [@earth-iers-bulletin-a] [@earth-usno-deltat].
- **ΔT enters only through μ**, the Greenwich hour angle of the shadow axis. The elements are computed in TT, and converting a tabulated UT longitude for a revised $\delta T$ is $\delta\lambda = -1.002738\,\delta T$ [@earth-es1992]. One second of ΔT moves the whole eclipse 465 m in longitude at the equator and 356 m at latitude 40° ($\omega a = 7.292115 \times 10^{-5} \times 6378137$ m/s) [@earth-nga-wgs84].
- **The long-term models are parabolas of about 32 s/cy²** on top of splines through the historical record: Morrison and Stephenson 2004 give $-20 + 32u^2$ s with $u = (y - 1820)/100$, and Stephenson, Morrison and Hohenkerk 2016 give $-320.0 + (32.5 \pm 0.6)((y - 1825)/100)^2$ s, equivalent to a lengthening of the day of $+1.78 \pm 0.03$ ms/cy against $+2.3 \pm 0.1$ ms/cy from tidal friction alone [@earth-5mcse] [@earth-smh2016].
- **Every historical ΔT value is tied to a lunar tidal acceleration.** Morrison and Stephenson assumed $-26''$/cy², DE430 embeds $-25.82''$/cy², DE421 $-25.85''$/cy², DE405 and DE406 $-25.826''$/cy². Espenak's correction $c = -0.000012932(y - 1955)^2$ s and the Swiss Ephemeris rule $\Delta T \mathrel{+}= -0.000091(\dot n - \dot n_0)(y - 1955)^2$ s are the same formula [@earth-nasa-deltatpoly] [@earth-swisseph-swephlib] [@earth-swisseph-swephexp].
- **Prediction error grows from 0.05 s at one year to 0.6 s at five, 4.6 s at twenty and 52 s at a hundred** on Huber's model as used by NASA, which is 0.02, 0.2, 1.6 and 18 km of longitude at 40° [@earth-nasa-deltat-uncertainty]. The realised error of the 2006 Espenak and Meeus polynomial was 1.5 s for 2017 and 4.8 s for 2024, because the Earth stopped decelerating after 2005.
- **The predictors used different ΔT for the same eclipse.** For 2017 August 21: NASA 68.4 s, EclipseWise 68.8 s, SVS 68.917 s, against 68.84 s measured. For 2024 April 8: NASA 70.6 s, EclipseWise 71.5 s, against 69.20 s measured. The largest miss, 2.3 s, is 0.8 km of longitude at 40° [@earth-nasa-2017-google] [@earth-eclipsewise-2017] [@earth-svs-4515] [@earth-nasa-2024-google] [@earth-eclipsewise-2024] [@earth-usno-deltat-data].
- **Polar motion, the equation of the equinoxes and the choice of nutation model are below the noise**, at about 10 m, up to 0.5 km if sidereal time is used inconsistently, and under 20 m respectively; no predictor documents polar motion [@earth-iers-bulletin-a] [@earth-circ179] [@earth-swisseph-swecl].
:::

**The question.** What is ΔT, exactly where does it enter a Besselian-element computation, which models exist for the past, the present and the future, how uncertain is a prediction made one, five, twenty and a hundred years before an eclipse, what did each predictor use for 2017 and 2024 and how did that compare with the measured value, and what do UT1 versus UTC, polar motion, sidereal time and the precession-nutation model contribute at eclipse precision?

## Definition

[?delta-t|ΔT] is the difference between the uniform time of the ephemerides and the time kept by the rotating Earth. The Five Millennium Catalog, NASA/TP-2009-214174, states it as "ΔT = TD − UT" and explains why it is needed: "The orbital positions of the Sun and Moon required by eclipse predictions, are calculated using TD because it is a uniform time scale. World time zones and daily life, however, are based on UT. In order to convert eclipse predictions from TD to UT, the difference between these two time scales must be known" [@earth-5mcse]. TD, TDT and [?tt|TT] are the same scale under successive names. The USNO defines the modern quantity precisely as "TT − UT1" and Stephenson, Morrison and Hohenkerk give the chain: "Since 1955.5, highly stable atomic clocks have provided an independent, uniform time scale (TAI), which is related to TT by TT = TAI + 32.184 s" [@earth-usno-deltat] [@earth-smh2016]. The Swiss Ephemeris source spells out the arithmetic for the atomic era:

$$\Delta T = \mathrm{TAI} - \mathrm{UT1} + 32.184\ \mathrm{s} = (\mathrm{TAI} - \mathrm{UTC}) - (\mathrm{UT1} - \mathrm{UTC}) + 32.184\ \mathrm{s}$$

[@earth-swisseph-swephlib]. IERS Bulletin A of 2026 September 10 gives "TAI-UTC = 37.000 000 seconds" since 2017 January 1 and "UT1-UTC 0.000946" s for MJD 61287, so ΔT on 2026 September 4 was 69.183 s [@earth-iers-bulletin-a].

## Where ΔT enters the elements

The [?besselian-elements|Besselian elements] $x$, $y$, $d$, $l_1$, $l_2$ are functions of TT alone. They depend on the Sun and Moon and not on the Earth's rotation. The 1992 Supplement describes the input: "the apparent right ascension, declination, and distance of the Sun, and the apparent right ascension, declination, and distance of the Moon, for every hour of TDT during the eclipse; and the ephemeris sidereal time at 0h TDT for the day of the eclipse and for the following day" [@earth-es1992]. The rotation enters through [?earth-mu|μ], the Greenwich hour angle of the shadow axis, which is ephemeris sidereal time minus the right ascension of the axis. Ephemeris sidereal time is sidereal time evaluated as if TT were UT: "The ephemeris sidereal time at 0h TDT, which is the local apparent sidereal time on the ephemeris meridian, is the same numerically as the (Greenwich) apparent sidereal time at 0h UT" [@earth-es1992]. The ephemeris meridian therefore lies $1.002738\,\Delta T$ east of Greenwich, and every longitude computed from $\mu$ must be corrected by that amount. The Supplement gives the correction to apply when a better ΔT arrives after tabulation: "If a later value of ΔT is adopted, such that the offset becomes ΔT + δT, then tabular quantities may be corrected quite easily by applying

$$\delta\lambda = -1.002738\,\delta T \quad \text{(longitude measured eastward)}$$

to all longitudes in the tabulated phenomena, and subtracting δT algebraically from all tabulated times expressed in UT" [@earth-es1992]. The factor 1.002738 is the ratio of sidereal to solar rate, and $\delta\lambda$ is in seconds of time, 15.041 arcseconds of longitude per second. EclipseWise states the same conversion in the other direction: "UT1 = TD − ΔT" [@earth-eclipsewise-2017].

The ground displacement follows from the Earth's rotation rate. WGS 84 defines "Nominal Mean Angular Velocity of the Earth ω 7292115 × 10⁻¹¹ radians/second" [@earth-nga-wgs84], so the equator moves $\omega a = 465.1$ m/s and a point at latitude $\phi$ moves $465.1 \cos\phi$ m/s. One second of ΔT error shifts every feature of the eclipse, path, limits and contact times alike, by 465 m of longitude at the equator, 356 m at 40° and 233 m at 60°. The shift is along a parallel of latitude, so its component perpendicular to a path depends on the path azimuth. A predictor that is 1 s high in ΔT places the path 465 m too far west at the equator, and an observer sees every contact 1 s later than tabulated in UT. NASA's uncertainty page tabulates the same relation as an angle, "636 seconds" of ΔT standard error at year −1000 corresponding to "2.65°" of longitude [@earth-nasa-deltat-uncertainty].

The Swiss Ephemeris makes a point that follows from this: "the question when the next solar eclipse will happen anywhere on Earth is independent of the rotational position of the Earth and therefore independent of Delta T" [@earth-swisseph-prg]. The eclipse catalogue is in TT; only its placement on the globe needs ΔT.

## The models

### Historical era: Morrison and Stephenson 2004, and Stephenson, Morrison and Hohenkerk 2016

Before 1600 the only evidence is timed and untimed eclipse and occultation reports. Morrison and Stephenson (2004) fitted cubic splines from −500 to +1950 and tabulated ΔT at intervals with standard errors. The Five Millennium Catalog reproduces the table, with errors falling from 430 s at −500 through 260 s at year 0, 55 s at 1000, 20 s from 1300 to 1600, 5 s at 1700, 1 s at 1800 and under 0.1 s by 1950 [@earth-5mcse]. Outside the observed span both works use a parabola. The Catalogue gives "ΔT = −20 + 32u² s, where u = (year − 1820)/100" [@earth-5mcse]. The vertex near 1820 is not arbitrary: it is the mean epoch of the observations behind Newcomb's Tables of the Sun, from which the second of Ephemeris Time and hence the SI second were derived, so the mean solar day equalled 86400 SI s around then [@earth-smh2016].

Stephenson, Morrison and Hohenkerk (2016) re-reduced the whole record with JPL DE430 and 180 Babylonian timings among new material. Their overall fit is

$$\Delta T = -320.0 + (32.5 \pm 0.6)\left(\frac{\mathrm{year} - 1825}{100}\right)^2\ \mathrm{s}$$

and "The parabolic coefficient +32.5±0.6 in (4.1) is an improvement on the result +31.0±0.9 in our previous paper" [@earth-smh2016]. The coefficient converts to a rate of change of the [?earth-lod|length of day]: "the change in the length of the mean solar day (lod) increases at an average rate of +1.8 ms per century. This is significantly less than the rate predicted on the basis of tidal friction, which is +2.3 ms per century" [@earth-smh2016]. (A parabola $c\,t^2$ s with $t$ in centuries gives $d(\mathrm{lod})/dt = 2c/36525$ s per day per century, so 32.5 s/cy² is 1.78 ms/cy.) The tidal figure comes from lunar laser ranging: "Lunar laser ranging provides an accurate value for the Moon's tidal acceleration, −25.82±0.03″ cy⁻²", inserted into "ω̇_tidal = +(49 ± 3) × 0.004869 ṅ × 10⁻²² rad s⁻²" to give "−6.16 ± 0.4 × 10⁻²² rad s⁻²" [@earth-smh2016]. For the telescopic era they fitted "Cubic splines ... with knots spaced at intervals to reflect the accuracy and density of the observations", 5-year knots from 1800 to 1900 and 3-year knots from 1900 to 2016, chosen because "A 3 year interval for the knots in the spline fitted to ΔT produced the best agreement between the lod from the occultations and the IERS data" over 1962 to 2015, the span they used "as a comparative control" [@earth-smh2016]. On extrapolation they are cautious: "The extrapolation of the lod beyond the limits of the dataset is dependent on the reality of the 1500 year oscillation ... Both are somewhat conjectural" [@earth-smh2016]. The 2021 addendum added medieval European solar eclipses and revised the deceleration: "The revised observed deceleration is −4.59 ± 0.08 × 10⁻²² rad s⁻². By comparison the predicted tidal deceleration ... is −6.39 ± 0.03 × 10⁻²² rad s⁻². These signify a mean accelerative component of +1.8 ± 0.1 × 10⁻²² rad s⁻². There is also evidence of an oscillatory variation in the rate with a period of about 14 centuries" [@earth-mshz2021].

The figure of 1.4 ms/cy that circulates in older texts is from Stephenson and Morrison (1984). The 1992 Supplement quotes their telescopic-era parabola "ΔT = 25.5 t² ... where t is time in centuries from A.D. 1800. This result is equivalent to a rate of lengthening of the day of 1.4 ms/century", and their ancient-era parabola with coefficient 44.3, "equivalent rate of lengthening of the day is 2.4 ms/century" [@earth-es1992]. Those two numbers have been superseded by the single 2016 fit.

### The lunar secular acceleration and the ephemeris dependence

A ΔT derived from a historical eclipse is the correction that makes a lunar ephemeris reproduce the record, so it depends on the [?secular-acceleration|tidal acceleration] $\dot n$ built into that ephemeris. Stephenson, Morrison and Hohenkerk: "The value implicit in the JPL ephemerides DE430, which was used to reduce the occultation observations after AD 1600, is −25.82″ cy⁻² ... This is close to the value of −26.00″ cy⁻² introduced to the analytical ephemeris ... used here and in previous work in the reduction of the pre-telescopic observations", and "The values of ΔT derived in this paper should be used in conjunction with the lunar ephemeris JPL DE430, or with other ephemerides in which the tidal acceleration is close to the value of −25.82″ cy⁻²" [@earth-smh2016]. The per-ephemeris values, as collected in the Swiss Ephemeris header with their sources, are: DE200 −23.8946, DE403 and DE404 −25.580, DE405 and DE406 −25.826, DE421 and DE422 −25.85 ("JPL Interoffice Memorandum 14-mar-2008"), DE430 −25.82 ("JPL Interoffice Memorandum 9-jul-2013"), DE431 −25.80 ("IPN Progress Report 42-196"), DE441 −25.936 (unpublished), and −26.0 for Morrison and Stephenson [@earth-swisseph-swephexp].

The correction between two accelerations is a parabola in time from 1955, when atomic time made ΔT independent of the Moon. Espenak: "All values of ΔT based on Morrison and Stephenson [2004] assume a value for the Moon's secular acceleration of −26 arcsec/cy². However, the ELP-2000/82 lunar ephemeris employed in the Canon uses a slightly different value of −25.858 arcsec/cy². Thus, a small correction 'c' must be added ... c = −0.000012932 × (y − 1955)²", with "no correction ... needed" for 1955 to 2005 [@earth-nasa-deltatpoly]. The Swiss Ephemeris implements the general rule in `adjust_for_tidacc`:

$$\Delta T \mathrel{+}= -0.000091\,(\dot n - \dot n_0)\,(y - 1955)^2\ \mathrm{s} \qquad (y < 1955)$$

[@earth-swisseph-swephlib]. With $\dot n - \dot n_0 = -25.858 - (-26.0) = 0.142$ this gives $-0.0000129 (y - 1955)^2$, which is Espenak's constant. The magnitude matters only far from 1955: 0.5 s at 1755, 13 s at −1000.

### Espenak and Meeus polynomials

For programs that want a closed form, Espenak and Meeus fitted piecewise polynomials to the 2004 spline and the modern data, with the decimal year "y = year + (month − 0.5)/12" [@earth-nasa-deltatpoly]. The pieces relevant to a modern product are:

$$1986 \le y < 2005:\quad \Delta T = 63.86 + 0.3345\,t - 0.060374\,t^2 + 0.0017275\,t^3 + 0.000651814\,t^4 + 0.00002373599\,t^5,\quad t = y - 2000$$
$$2005 \le y < 2050:\quad \Delta T = 62.92 + 0.32217\,t + 0.005589\,t^2,\quad t = y - 2000$$
$$2050 \le y < 2150:\quad \Delta T = -20 + 32\left(\frac{y - 1820}{100}\right)^2 - 0.5628\,(2150 - y)$$
$$y \ge 2150:\quad \Delta T = -20 + 32u^2,\quad u = \frac{y - 1820}{100}$$

[@earth-nasa-deltatpoly]. The Catalogue's own statement of the outlook was "+67 s in 2010, +93 s in 2050, +203 s in 2100, and +442 s in 2200", with the warning that "Future changes and trends in ΔT can not be predicted with certainty because theoretical models of the physical causes are not of high enough precision" [@earth-5mcse]. The 2005 to 2050 piece evaluates to 70.34 s for 2017.64 and 74.03 s for 2024.27 (computed here). The measured values were 68.84 s and 69.20 s [@earth-usno-deltat-data]. The polynomial, fitted while ΔT was rising at 0.6 s/yr, missed the plateau that began around 2005: the USNO table shows ΔT rising only from 68.84 s in 2017 to 69.20 s in 2024 and then falling to 69.13 s by 2026 April [@earth-usno-deltat-data]. The technical note for The Photographer's Ephemeris (Photo Ephemeris) records the practical consequence, having "updated the 2017 eclipse from 70.3 s (NASA) to 68.8373 s (USNO)" [@earth-photoephemeris].

### Modern era: IERS and USNO

From 1962 the IERS combined series is the source. The C04 guide describes UT1 as derived from VLBI, translated "into the discontinuous series UT1-UTC", and states "Their present accuracy is about 6 μs for UT1" [@earth-iers-c04-guide]. The current series is "EOP Combined Series 20 C04 consistent with ITRF 2020", daily from 1962 [@earth-iers-c04]. For the recent past the USNO publishes `deltat.data`, "Monthly determinations of Delta T (TT - UT1) since 1973", and for the future `deltat.preds`, "Long-term predictions of Delta T (TT - UT1) from finals.data" [@earth-usno-deltat]. Bulletin A gives the short-term prediction formula and its accuracy: "UT1-UTC = -0.0790 - 0.00026 (MJD - 61301) - (UT2-UT1)" for the weeks after 2026 September, with "Estimated accuracies ... UT1-UTC 0.0014 0.0024 0.0032 0.0040" s at 10, 20, 30 and 40 days [@earth-iers-bulletin-a]. The Swiss Ephemeris switches from the 2016 spline to the almanac and IERS tables "at 1 Jan. 1955" with a 1000-day blending term, and for the future uses "the formula of Stephenson (1997; p. 507), with a modification that avoids a jump at the end of the tabulated period. A linear term is added that makes a slow transition from the table to the formula over a period of 100 years" [@earth-swisseph-swephlib].

## Prediction uncertainty by lead time

Two sources give numbers. The USNO prediction file carries an error column: 2024.0: 69.11 ± 0.033 s, 2025.0: 69.04 ± 0.088 s, 2026.0: 69.05 ± 0.189 s, 2027.0: 69.14 ± 0.327 s, 2028.0: 69.34 ± 0.486 s, 2030.0: 69.97 ± 0.768 s [@earth-usno-deltat-preds]. NASA's uncertainty page gives Huber's Brownian-motion model for lead times beyond the observed span, "σ = 365.25 × N × SQRT[(N × Q/3) × (1 + N/M)]/1000" s with $N$ the years from the calibration year, "M = 2500 years" and "Q = 0.058 ms²/yr", calibrated at 2005 for the future [@earth-nasa-deltat-uncertainty] [@earth-5mcse]. Evaluating it:

| Lead time | σ(ΔT) from Huber's model | USNO file, where available | Longitude shift at 40° |
|---|---|---|---|
| 1 year | 0.05 s | 0.09 s | 0.02 to 0.03 km |
| 5 years | 0.57 s | 0.77 s at 6 years | 0.2 to 0.3 km |
| 20 years | 4.6 s | (realised: 4.8 s for the 2006 polynomial at 2024) | 1.6 km |
| 100 years | 52 s | | 18 km |

The Catalogue's own table of the model gives 622 s at +2500, or "7.9°" of longitude [@earth-5mcse]. For an eclipse product the practical rule is that a path computed more than about five years ahead should be republished with the current USNO prediction, and that a path computed decades ahead carries a kilometre-scale longitude uncertainty that no limb or terrain modelling can remove.

![The standard error of ΔT is a tenth of a second at 1900 and grows as the square of the distance from that era in both directions, past the 265 s at which the Five Millennium Canon stops drawing a single path and starts drawing a longitude gore [@earth-nasa-deltat-uncertainty] [@val-5mcse-tp2009].](img/delta-t-uncertainty.svg)

## What each predictor used for 2017 and 2024

| Predictor | 2017 August 21 | 2024 April 8 | Source of the value |
|---|---|---|---|
| Measured (USNO `deltat.data`) | 68.84 s (Aug 1: 68.8373, Sep 1: 68.8477) | 69.20 s (Apr 1: 69.1983, May 1: 69.2018) | [@earth-usno-deltat-data] |
| NASA eclipse site, Espenak | 68.4 s; the 2017 Google-map page names JPL DE405 and the 2017 path-table page names VSOP87/ELP2000-85 | 70.6 s, VSOP87/ELP2000-85 | [@earth-nasa-2017-google] [@earth-nasa-2017-beselm] [@earth-nasa-2024-google] [@earth-nasa-2024-beselm] |
| NASA SEdata page and the Catalog CSV | – | 74.0 s, the 2006 polynomial value, later revised to 70.6 s on the path and element pages; see [Besselian elements](../01-foundations/besselian-elements.md) | [@earth-nasa-deltatpoly] [@earth-5mcse] |
| EclipseWise, Espenak | 68.8 s, JPL DE405 | 71.5 s, JPL DE405 | [@earth-eclipsewise-2017] [@earth-eclipsewise-2024] |
| NASA SVS, Wright | 68.917 s ("Delta UTC 69.184 seconds (TT – TAI + 37 leap seconds)", DE421, SPICE predict kernel "ΔT corrected"); an earlier product used Delta UTC 68.184 s with 36 leap seconds | Not printed on SVS 5073, 5123 or 5219 | [@earth-svs-4515] [@earth-svs-4314] [@earth-svs-5073] |
| Espenak and Meeus 2006 polynomial | 70.34 s (computed here) | 74.03 s (computed here) | [@earth-nasa-deltatpoly] |
| Photo Ephemeris | 68.8373 s from USNO, replacing NASA's 70.3 s | USNO predictions for 2024 to 2034 | [@earth-photoephemeris] |
| Jubier calculator | Prints "ΔT = xx.x s" per eclipse; the archived static page carries a placeholder | 69.1 s on the 2024 map page, read from its element array in [commercial and institutional tools](../09-software-and-repos/commercial-and-institutional-tools.md) | [@earth-jubier-calc] [@earth-jubier-2024map] |
| timeanddate | Not published; states that calculations "account for changes in the speed of Earth's rotation using a value called Delta T" | same | [@earth-timeanddate-accuracy] |
| Occult | Not documented on the pages read | same | [@earth-occult4] |

NASA labels its 2024 element page "VSOP87/ELP2000-85", while the Catalog text describes ELP-2000/82. Both labels are quoted here from the pages that carry them [@earth-nasa-2024-beselm] [@earth-5mcse].

The errors are small for 2017: −0.44 s for NASA, −0.04 s for EclipseWise and +0.08 s for SVS, which are 160 m, 15 m and 30 m of longitude at 40°. For 2024 the two Espenak products were +1.4 s and +2.3 s high, 0.5 km and 0.8 km of longitude at 40°, a consequence of predicting in the years when ΔT still appeared to be climbing. The SVS 2017 value combines the leap-second count with a predicted UT1 − UTC of $69.184 - 68.917 = 0.267$ s, against a measured 0.347 s. Its earlier product's "36 leap seconds" shows the count was updated after the 2017 January leap second [@earth-svs-4314] [@earth-svs-4515].

## UT1, UTC and leap seconds

Published eclipse times labelled UT are [?earth-ut1|UT1]. The 1992 Supplement: "Calculations are normally provided in provisional Universal Time (UT) or, more precisely, UT1 (see Chapter 2) using a predicted value of ΔT" [@earth-es1992]. Civil clocks keep [?earth-utc|UTC], which the Catalogue describes: "In order to keep the two times within 0.9 s of each other, a leap second is added to UTC about once every 12 to 18 months" [@earth-5mcse]. A product that prints contact times as UTC must subtract [?earth-dut1|DUT1] = UT1 − UTC from the UT1 times. Bulletin A: "DUT1 = (UT1-UTC) transmitted with time signals = 0.0 seconds beginning 09 April 2026" and "There will NOT be a leap second introduced in UTC at the end of December 2026" [@earth-iers-bulletin-a]. The largest possible error from ignoring the distinction is 0.9 s, or 0.42 km at the equator, and in 2026 it is under 1 ms. The place where a [?earth-leap-second|leap second] does bite is the bookkeeping of ΔT itself: a program that stores TAI − UTC as a constant, as the SVS 2017 products did in "Delta UTC", is wrong by exactly 1 s after each leap second until updated [@earth-svs-4314] [@earth-svs-4515].

## Polar motion

The [?earth-polar-motion|polar motion] coordinates in Bulletin A are "x = 0.20025 arcseconds, y = 0.33395 arcseconds" for 2026 September 10, predicted to "0.004 0.007 0.010 0.013" arcseconds at 10 to 40 days [@earth-iers-bulletin-a]. An offset of $0.3''$ of the rotation axis relative to the crust displaces an observer relative to the axis by $0.3'' \times a / 206265'' = 9$ m. The 1992 Supplement lists "formulas for polar motion and refraction, which are required in topocentric" reductions, but the eclipse chapter does not apply it [@earth-es1992]. The Swiss Ephemeris counts "from polar motion: a few meters" in its error budget and does not correct for it [@earth-swisseph-swecl]. No other predictor mentions it. SVS's SPICE Earth-orientation kernel carries polar motion as part of the IERS series, so SVS includes it implicitly [@earth-svs-4515]. At 10 m against 40 m of ephemeris error it can be neglected in a product, but a developer using SPICE or SOFA gets it free.

## Sidereal time, nutation and the precession-nutation model

The hour angle $\mu$ is built from apparent sidereal time, that is, [?earth-gast|GAST]. The 1992 Supplement's step for topocentric reduction gives Greenwich mean sidereal time as

$$\theta_m = 67310.54841 + (876600^{\mathrm h} + 8640184.812866)\,T_u + 0.093104\,T_u^2 - 6.2 \times 10^{-6}\,T_u^3\ \mathrm{s}$$

with $T_u$ in Julian centuries of UT1 from J2000.0, then adds the [?earth-equation-of-equinoxes|equation of the equinoxes] to obtain apparent sidereal time [@earth-es1992]. Circular 179 states the size of that term: "The difference between true and mean sidereal time is the equation of the equinoxes, which is a complex periodic function with a maximum amplitude of about 1 s" [@earth-circ179]. The requirement is consistency, not a particular choice. The Sun and Moon positions in the elements are referred to the true equator and equinox of date when apparent places are used, and then $\mu$ must use GAST. If mean places and GMST are used together the [?earth-nutation|nutation] cancels. The Swiss Ephemeris source records exactly this: "nutation need not be in lunar and solar positions, if mean sidereal time will be used" [@earth-swisseph-swecl]. Mixing the two conventions puts up to 1.1 s of time, 0.5 km at the equator, into $\mu$.

Whether the nutation series is IAU 1980 or IAU 2000A, and whether precession is IAU 1976 or IAU 2006, does not matter at eclipse precision. Circular 179: "the resolutions described here affect astronomical quantities only at the level of some tens of milliarcseconds or less at the present epoch ... The largest systematic change is due to the new rate of precession, which is 0.3 arcsecond per century less than the previous (1976) rate" [@earth-circ179]. Ten milliarcseconds at the Moon's distance is 19 m on the shadow axis. What does matter is that the ephemeris, the frame rotation and the Earth orientation all use one consistent set, which SPICE, SOFA and the Swiss Ephemeris each provide internally.

## Sources compared

| Source | Era covered | Form | Tidal acceleration assumed | Uncertainty given | What it uniquely provides |
|---|---|---|---|---|---|
| Morrison and Stephenson 2004 [@earth-ms2004] [@earth-5mcse] | −500 to +1950, parabola outside | Spline table with standard errors; $-20 + 32u^2$ | $-26.0''$/cy² | Yes, per tabulated year | The table Espenak's polynomials were fitted to |
| Stephenson, Morrison and Hohenkerk 2016 [@earth-smh2016] | −720 to 2015 | Spline with 3- and 5-year knots; $-320 + 32.5((y-1825)/100)^2$ | $-25.82''$/cy² (DE430) | Yes, and IERS control after 1962 | The current standard; lod $+1.78 \pm 0.03$ ms/cy versus tidal $+2.3$ |
| Addendum 2021 [@earth-mshz2021] | as above plus medieval Europe | Revised deceleration $-4.59 \times 10^{-22}$ rad/s² | as above | Yes | A 14-century oscillation |
| Espenak and Meeus polynomials [@earth-nasa-deltatpoly] | −1999 to +3000 | Piecewise polynomials in decimal year | $-25.858''$/cy² (ELP-2000/82) with correction $c$ | Only via Huber model | Closed form; the $c$ correction |
| IERS C04 and Bulletin A [@earth-iers-c04] [@earth-iers-bulletin-a] | 1962 to now, 1 year ahead | Daily UT1 − UTC, x, y | none | 6 μs (C04); 1.4 to 4 ms at 10 to 40 days | Measured values and polar motion |
| USNO deltat.data and deltat.preds [@earth-usno-deltat-data] [@earth-usno-deltat-preds] | 1973 to now; to about 2030 | Monthly ΔT; yearly predictions with errors | none | Yes, per year | The error column for lead times of one to six years |
| Swiss Ephemeris swephlib.c [@earth-swisseph-swephlib] [@earth-swisseph-swephexp] | all | Model switch at 1955; Stephenson 1997 formula for the future | Per ephemeris table | none | The general tidal-acceleration adjustment and the per-ephemeris constants |

## What a developer should do

1. Compute the elements in TT and keep them in TT. Apply ΔT once, in $\mu$, when placing the shadow on the Earth, and expose the value used in every output file [@earth-es1992].
2. For eclipses from 1962 onward use the IERS or USNO measured ΔT; for eclipses up to a few years ahead use `deltat.preds` and its error column; beyond that use the Stephenson, Morrison and Hohenkerk 2016 spline and parabola with the tidal-acceleration adjustment matched to the ephemeris, never the 2006 polynomial as published [@earth-usno-deltat-preds] [@earth-smh2016] [@earth-swisseph-swephlib].
3. Recompute and republish paths within a year of the eclipse. The change from 71.5 s to 69.2 s for 2024 was 0.8 km of longitude at 40°.
4. Print UT1 and say so, and add DUT1 when printing UTC. Keep TAI − UTC as a table keyed by date, not a constant [@earth-iers-bulletin-a].
5. Use one consistent Earth-orientation stack (SOFA, SPICE or the Swiss Ephemeris) for precession, nutation, sidereal time and, if it comes free, polar motion. Do not mix mean and apparent sidereal time [@earth-swisseph-swecl] [@earth-circ179].

Read first: Section 2.6 of the Five Millennium Catalog, Section 4 of Stephenson, Morrison and Hohenkerk 2016, and Section 8.363 of the 1992 Supplement.

## What this changes

The pipeline needs a ΔT provider with three regimes and a stated uncertainty, and every published path needs the ΔT value and its date stamped on it. The Besselian-element stage is unaffected. The validation stage should treat a longitude offset of the order of $465 \cos\phi$ m per second of ΔT difference as expected when comparing predictors that used different values.

## Open questions

- Obtain the ΔT value SVS used for 2024, either from shapefile metadata in SVS 5073 or from the SPICE predict kernel name it used, so that the 2024 SVS path can be compared with the others at the 100 m level [@earth-svs-5073].
- Obtain the ΔT value used by timeanddate, which is not on the pages read. Jubier's 2024 value is settled at 69.1 s by the element array quoted in [commercial and institutional tools](../09-software-and-repos/commercial-and-institutional-tools.md) [@earth-timeanddate-accuracy].
- Obtain Occult's ΔT source and update policy from its help file, which is distributed with the program rather than on the web [@earth-occult4].
- Obtain Morrison and Stephenson 2004 itself, to quote its Table 1 and its statement of the uncertainty model rather than the Catalogue's transcription [@earth-ms2004].
- Obtain the ΔT chapter of the 2013 Explanatory Supplement, which postdates the 2004 work and predates 2016 [@earth-es2013].
