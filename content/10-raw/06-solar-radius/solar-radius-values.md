---
title: Solar radius values and their provenance
description: Every solar radius in circulation, the edge each one measures, its wavelength and uncertainty, and which eclipse predictor uses which.
order: 1
status: working
updated: 2026-09-15
tags: [solar-radius, auwers, iau-2015, helioseismology, bailys-beads, flash-spectrum]
---

::: summary
- **Three values dominate.** The [?canonical-solar-radius|canonical] 959.63 arcseconds at 1 au (Auwers 1891), the IAU 2015 [?nominal-solar-radius|nominal] radius of exactly 695,700 km (959.22 arcseconds), and an [?eclipse-solar-radius] near 959.95 arcseconds measured from the edge of totality. They differ because they measure different layers of the Sun, not because one is wrong [@sun-rozelot-kosovichev-2026].
- **Auwers' value is 135 years old.** It is a weighted mean of 19th-century heliometer, meridian and eclipse-contact measures, adopted by the IAU in 1976 and still the value in the Astronomical Almanac, Meeus, Espenak, Jubier and Occult [@sun-mcglaun-auwers] [@sun-meeus-aa] [@sun-jubier-map-help].
- **696,000 km is the same value rounded.** 696,000 km is 959.645 arcseconds by arcsine or 959.634 arcseconds by arctangent. NASA SVS, USNO, Stellarium and the Swiss Ephemeris all use it [@sun-svs-4515] [@sun-usno-computer] [@sun-stellarium-sec] [@sun-swisseph-swecl].
- **The seismic radius is about 300 km smaller.** f-mode helioseismology gives 695,680 ± 30 km. Haberreiter, Schmutz and Kosovichev showed that the inflection point of the limb-darkening profile sits 0.333 ± 0.008 Mm above the $\tau_{\mathrm{Ross}} = 2/3$ surface. That offset is the basis of the IAU 2015 nominal value of 695,700 km [@sun-schou-1997] [@sun-haberreiter-2008] [@sun-prsa-2016].
- **Space limb measurements scatter by 0.5 arcseconds.** HMI at 617.3 nm during the 2012 Venus transit gave 959.57 ± 0.02 arcseconds. SOHO/MDI during the Mercury transits gave 960.12 ± 0.09 arcseconds. PICARD/SODISM gave 696,156 ± 145 km at 607.1 nm [@sun-emilio-2015] [@sun-emilio-2012] [@sun-meftah-2018].
- **Eclipse measurements cluster at 959.95 to 960.0 arcseconds.** Lamy et al. found 959.99 ± 0.06 arcseconds from 17 photometer light curves at four eclipses. Quaglia et al. found 959.95 ± 0.05 arcseconds from the 2017 flash spectrum. Adassuriya found 959.89 ± 0.18 arcseconds from 2010 beads. Kubo's 1970 to 1991 values lie in 959.74 to 959.88 arcseconds [@sun-lamy-2015] [@sun-quaglia-2021] [@sun-adassuriya-2011] [@sun-kubo-1993].
- **The eclipse radius is 0.32 arcseconds or 232 km larger than Auwers'.** Totality ends only when the last photospheric light is gone, and photospheric light is detectable at least 0.65 arcseconds beyond the inflection point [@sun-raponi-sigismondi-2011] [@sun-quaglia-2021].
- **No predictor except Irwin's and the simulator inside The Photographer's Ephemeris (Photo Ephemeris) has switched.** NASA SVS used 696,000 km in both 2017 and 2024, Jubier and Occult default to 959.63 arcseconds, and Solar Eclipse Maestro and Occult let the user change it [@sun-wright-young-2024] [@sun-jubier-map-help] [@sun-quaglia-2021].
:::

**The question.** An eclipse computation needs a single number for the angular radius of the Sun at 1 au. Which numbers are in circulation, what did each measurement actually measure, how large are the uncertainties, why do eclipse-derived radii come out about 0.3 arcseconds larger than the almanac value, and which value does each predictor use? This note answers those questions with quoted values. The companion note [Effect of the radius on eclipse products](effect-on-eclipse-products.md) converts the differences into kilometres of path limit and seconds of totality.

![The eclipse determinations cluster near 959.95 to 960.01 arcseconds, about a third of an arcsecond above the 959.63 arcseconds that the almanacs and most predictors still use, and about three quarters of an arcsecond above the IAU 2015 nominal radius [@sun-mcglaun-auwers] [@sun-prsa-2016] [@sun-kubo-1993] [@sun-adassuriya-2011] [@sun-quaglia-2021] [@sun-lamy-2015] [@sun-wright-young-2024].](img/solar-radius-values.svg)

## Converting between arcseconds and kilometres

The angular semidiameter $s_0$ at 1 au and the linear radius $R_\odot$ are related through the astronomical unit $a = 149{,}597{,}870.7$ km:

$$R_\odot = a \sin s_0 \qquad\text{or}\qquad R_\odot = a \tan s_0$$

The two conventions differ by 0.011 arcseconds, or 7.5 km, at the solar radius. Rozelot and Kosovichev note that the IAU nominal radius is "959.22 arcsec (959.23, confounding the angle and its tangent)" [@sun-rozelot-kosovichev-2026]. The Yatskiv value of 696,000 km used by NASA SVS corresponds to 959.645 arcseconds by arcsine and to 959.634 arcseconds by arctangent. SVS prints the arcsine figure [@sun-svs-4515]. With the arcsine convention and the 2012 au, the values below convert as follows (this table is computed for this note):

| Arcseconds at 1 au | km (arcsine) | Source of the value |
|---|---|---|
| 958.96 | 695,508 | Brown and Christensen-Dalsgaard 1998, 800 nm |
| 959.20 | 695,680 | Schou et al. 1997 seismic |
| 959.22 | 695,700 | IAU 2015 nominal (exact in km) |
| 959.57 | 695,946 | Emilio et al. 2015, HMI 617.3 nm |
| 959.63 | 695,990 | Auwers 1891, IAU 1976, Astronomical Almanac |
| 959.645 | 696,000 | Yatskiv 1978, NASA SVS, USNO |
| 959.78 | 696,098 | Meftah et al. 2014, ground 535.7 nm |
| 959.86 | 696,156 | Meftah et al. 2018, PICARD 607.1 nm |
| 959.95 | 696,221 | Quaglia et al. 2021, eclipse 2017 |
| 959.99 | 696,250 | Lamy et al. 2015, eclipses 2010 to 2015 |
| 960.12 | 696,345 | Emilio et al. 2012, MDI Mercury transits |

One arcsecond at 1 au is 725 km on the Sun. The 0.32 arcsecond gap between the canonical and eclipse radii is 232 km. The 0.41 arcsecond gap between the canonical and nominal radii is 297 km [@sun-rozelot-2016-history].

## The canonical value: 959.63 arcseconds (Auwers 1891)

Arthur Auwers published "Der Sonnendurchmesser und der Venusdurchmesser nach den Beobachtungen an den Heliometern der deutschen Venus-Expeditionen" in Astronomische Nachrichten 128, 361 (1891) [@sun-auwers-1891]. The paper was not read for this note. According to McGlaun's account of it, Auwers combined heliometer measures made by 29 observers between 1873 and 1886 with Bessel's Königsberg heliometer series, Klinkerfues' Göttingen series, Gambart's meridian-circle observations and eclipse-contact timings from 1842 and 1860, weighting each class of observation by a credibility factor before forming the mean. The result was 959.63 arcseconds at 1 au, and Auwers himself described it as an empirical compromise [@sun-mcglaun-auwers]. Rozelot and Kosovichev give it as the consensus value from 1895 to 2015 and quote a linear equivalent of 695,997 ± 36 km using the arctangent [@sun-rozelot-kosovichev-2026].

The value entered the IAU (1976) system of astronomical constants and the Astronomical Almanac. Meeus, *Astronomical Algorithms*, chapter "Semidiameters of the Sun, Moon, and Planets", gives the Sun's semidiameter at unit distance as $s_0 = 15'59''.63 = 959''.63$ [@sun-meeus-aa]. The Swiss Ephemeris source carries the same provenance in a comment: a solar diameter of 1,391,978,489.9 m "is consistent with 959.63 arcsec at AU distance (Astr. Alm.)" [@sun-swisseph-swecl]. Quaglia et al. state that the value "has remained unchanged for more than a century" and "is still used in all published eclipse predictions and softwares" [@sun-quaglia-2021]. Jubier's interactive map help says the computations "are executed using the standard IAU 1976 solar radius, that is 959.63 arc-seconds at one astronomical unit" [@sun-jubier-map-help].

What the value measures is a 19th-century visual limb: the point where a heliometer observer judged the bright disk to end, in white light through the atmosphere, blended with eclipse-contact timings that record the disappearance of the last photospheric light. It is therefore neither a pure [?inflection-point-radius] nor a pure eclipse radius. Its formal uncertainty is quoted as ± 0.05 arcseconds [@sun-rozelot-kosovichev-2026], but Quaglia et al. warn that quoting it to two decimals "has unfortunately fostered a false sense of accuracy" [@sun-quaglia-2021].

## 696,000 km: the same value rounded

Wright and Young write that "nearly all eclipse calculations use a de facto standard value of the solar radius first published more than a century ago and expressed as either 959.63 arcseconds at 1 au (Auwers 1891) or 696,000 km (Yatskiv 1978)" [@sun-wright-young-2024]. Sigismondi describes 959.63 arcseconds as "exactly the angle formed by 696000 km seen from 1 AU, adopted by the International Astronomical Union" [@sun-sigismondi-2012]. The two are equal only to about 0.01 arcseconds, which matters for nothing in an eclipse product. Users of 696,000 km, each quoting its own source text:

- NASA SVS: "Sun radius 696,000 km (959.645 arcsec at 1 AU)" [@sun-svs-4515].
- USNO Solar Eclipse Computer: "Sun 696000 km; Moon 1737.4 km", described as values "adopted by the International Astronomical Union" [@sun-usno-computer].
- Stellarium `SolarEclipseComputer.cpp`: "NASA's solar eclipse predictions use solar radius of 696,000 km calculated from arctan of IAU 1976 solar radius (959.63 arcsec at 1 au)" [@sun-stellarium-sec]. Its `ssystem_major.ini` sets `radius=696000.` [@sun-stellarium-ssystem].
- Swiss Ephemeris: the active definition is `DSUN (1392000000.0 / AUNIT)`, and the 959.63-arcsecond-consistent diameter is disabled under `#if 0` [@sun-swisseph-swecl].

## The IAU 2015 nominal radius: 695,700 km

IAU 2015 Resolution B3 defines the nominal solar radius $\mathcal{R}^{N}_\odot = 6.957 \times 10^8$ m exactly. Prša et al. explain the choice: "The chosen value corresponds to the solar photospheric radius suggested by Haberreiter et al. (2008), defined to be where the Rosseland optical depth $\tau = 2/3$. This study resolved the long-standing discrepancy between the seismic and photospheric solar radii. The nominal value ($6.957 \times 10^8$ m) is the rounded Haberreiter et al. value (695 658 ± 140 km) within the uncertainty" [@sun-prsa-2016]. The same paper insists that nominal values "represent a new set of units of measure rather than any measured quantity itself" [@sun-prsa-2016]. Wright and Young quote the resolution's own caveat that "these nominal values should be understood as conversion factors only, not as the true [...] properties or current best estimates" and conclude that the nominal radius "does not provide the solar radius required for accurate eclipse prediction, which defines totality as the complete extinction of the photosphere" [@sun-wright-young-2024].

The nominal radius is the value exposed by astropy: `R_sun = 6.957e8 m`, reference "IAU 2015 Resolution B 3", with `au = 1.49597870700e11 m` from IAU 2012 Resolution B2 [@sun-astropy-iau2015]. In arcseconds it is 959.22 (arctangent) or 959.23 (arcsine) [@sun-rozelot-kosovichev-2026] [@sun-rozelot-2016-history]. Photo Ephemeris uses it as the base of its chromosphere thickness scaling ("scaling up from 959.22″ (IAU) to 959.95″ (Quaglia et al.)") [@sun-photoephemeris-technote]. Rozelot et al. note that a linear conversion puts the nominal radius 0.41 arcseconds or 297 km below Auwers' value [@sun-rozelot-2016-history].

## Helioseismic radii and the 0.33 Mm offset

Schou, Kosovichev, Goode and Dziembowski measured the frequencies of the Sun's fundamental (f) modes with SOHO/MDI in the degree range $l = 88$ to $250$ and derived a [?seismic-radius] of 695,680 ± 30 km, which is 317 km below Auwers' value [@sun-schou-1997] [@sun-rozelot-kosovichev-2026]. The Schou paper itself was not read. The value is taken from the Rozelot and Kosovichev review. Tripathy and Antia obtained 695,770 ± 100 km from GONG, and Takada and Gough obtained 695,780 ± 160 km from p modes [@sun-rozelot-kosovichev-2026].

Haberreiter, Schmutz and Kosovichev explained the gap between the seismic radius and limb-based radii: "The calculated difference between the seismic radius and the inflection point is 0.347 ± 0.006 Mm with respect to $\tau_{5000} = 1$, and 0.333 ± 0.008 Mm with respect to $\tau_{\mathrm{Ross}} = 2/3$." Lowering the standard radius by 0.333 ± 0.008 Mm yields 695.66 Mm, which reconciles inflection-point measurements with the seismic radius within their uncertainties [@sun-haberreiter-2008]. The mechanism is geometric: the limb ray path is tangential, so the intensity inflection point seen at the limb sits several hundred kilometres above the layer where the disk-centre optical depth reaches unity. Meftah et al. restate this as "at 535.7 nm, approximately 330 km separates the seismic and photospheric radius definitions" [@sun-meftah-2018]. The seismic radius also varies with the activity cycle, but only by 1 to 2 km at the surface, with 5 to 8 km changes at a depth of about 5 Mm [@sun-kosovichev-rozelot-2018]. That variation is 0.003 arcseconds and irrelevant to eclipse products.

## Photospheric radii from space and the ground

The [?inflection-point-radius] is the radius at which the limb-darkening intensity profile has its steepest gradient. Measurements of it disagree by half an arcsecond:

| Measurement | Value | Wavelength | Edge definition | Notes |
|---|---|---|---|---|
| Brown and Christensen-Dalsgaard 1998, HAO Solar Diameter Monitor, 1981 to 1987 | 695.508 ± 0.026 Mm (958.96 arcseconds) | 800 nm | meridian transit duration fitted with a limb-darkening model | value in Allen's *Astrophysical Quantities* [@sun-brown-cd-1998] [@sun-rozelot-kosovichev-2026] |
| Emilio et al. 2012, SOHO/MDI, Mercury transits 2003 and 2006 | 960.12 ± 0.09 arcseconds (696,342 ± 65 km) | MDI continuum near 677 nm | transit timing gives the plate scale, limb from inflection | "The true solar radius is still a matter of debate" [@sun-emilio-2012] |
| Emilio et al. 2015, SDO/HMI, Venus transit 2012 | 959.57 ± 0.02 arcseconds (695,946 ± 15 km) | 617.3 nm continuum wing | inflection point | AIA gave 963.04 ± 0.03 at 160 nm and 961.76 ± 0.03 at 170 nm; values taken from Rozelot et al. 2016 [@sun-emilio-2015] [@sun-rozelot-2016-history] |
| Meftah et al. 2014, SODISM II at Calern, 2011 to 2013 | 959.78 ± 0.19 arcseconds (696,113 ± 138 km) | 535.7 nm | inflection point, more than 20,000 ground images | variations under 50 milliarcseconds, out of phase with activity [@sun-meftah-2014] |
| Meftah et al. 2018, PICARD/SODISM, Venus transit calibration | 696,134 ± 261 km at 535.7 nm; 696,156 ± 145 km at 607.1 nm; 696,192 ± 247 km at 782.2 nm | 535.7 to 1025 nm | inflection point | inflection-point differences below 60 km across 607 to 1025 nm relative to 535.7 nm [@sun-meftah-2018] |
| Morand et al. 2011, Calern astrolabe 1985 to 2009 | 959.48 ± 0.01 arcseconds | 540 nm | astrolabe transit | quoted by Rozelot and Kosovichev [@sun-rozelot-kosovichev-2026] |
| Rozelot et al. 2003, Pic du Midi scans | 959.434 ± 0.008 arcseconds | 505.8 nm | photoelectric limb scans | four days of 18 cm seeing [@sun-rozelot-kosovichev-2026] |

The spread is instrumental, not solar. Emilio et al. attribute literature differences of "several tenths of an arcsecond (~500 km)" largely to systematic instrument errors [@sun-emilio-2012]. Rozelot et al. show that Calern astrolabe series taken at the same site in the same years disagree by 0.3 arcseconds and conclude that ground data "show evidently a mix of atmospheric and solar signals" [@sun-rozelot-2016-history]. The one robust statement is Meftah's: the inflection-point radius depends only weakly on wavelength between 535 and 1025 nm [@sun-meftah-2018]. Rozelot and Kosovichev's 2026 review recommends the seismic radius as "the best determination" of the physical radius and proposes a glossary that separates photospheric, canonical, nominal, generic and seismic radii [@sun-rozelot-kosovichev-2026].

## Eclipse-derived radii

Eclipses measure a different edge. The observable is the time at which photospheric light vanishes or reappears in a lunar valley, so the quantity recovered is the radius of the last detectable photospheric light, given an ephemeris and a lunar limb profile. Sigismondi summarises the reduction: "The profile of the lunar limb, the solar standard radius R = 959.63 arcsec and the ephemerides allow to predict the appearance of the beads. All departures from these predictions are averaged to obtain the correction to R" [@sun-sigismondi-2012]. Occult 4 is the reference tool for this: "The simulated Sun by Occult 4 has the standard radius: 959.63 arcsec at 1 AU. The difference between the simulations and the observations is a measure of the radius correction with respect to the standard radius" [@sun-raponi-sigismondi-2011].

| Campaign | Eclipses | Value at 1 au | Edge and method | Limb data | Wavelength |
|---|---|---|---|---|---|
| Dunham et al. 1980 | 1715 England, 1976 Australia, 1979 North America | contraction of 0.34 ± 0.2 arcseconds in 264 years | Baily's-bead timings at both path edges | Watts | white light; value from an abstract summary [@sun-dunham-1980] |
| Kubo 1993 | 1970, 1973, 1980, 1991 | 959.74 to 959.88 arcseconds | photometer light curves of the flash spectrum, contact times fitted | Watts | white light; range quoted by Quaglia et al. [@sun-kubo-1993] [@sun-quaglia-2021] |
| Fiala, Dunham and Sofia 1994 | 1715 to 1991 | project description; no single value in the abstract | systematic re-reduction with newer ephemerides | Watts | [@sun-fiala-1994] |
| Kilcik, Sigismondi, Rozelot and Guhl 2009 | 2006 March 29, Turkey and Egypt | 959.22 ± 0.04 arcseconds | eclipse imaging with edge detection; the reference list cites Canny 1986 | not stated in abstract | [@sun-kilcik-2009] |
| Adassuriya et al. 2011 | 2010 January 15 annular, southern limit, Sri Lanka | 959.89 ± 0.18 arcseconds (ΔR = +0.26 ± 0.18) | on/off timing of 8 beads, Occult 4.0.8.6, DE423/LE423 | Kaguya (SELENE) | video, ND filter [@sun-adassuriya-2011] |
| Raponi and Sigismondi 2011 | 2010 January 15, Uganda and India videos | inflection point bounded by −0.190 < ΔR < +0.050 arcseconds | limb-darkening function reconstructed from bead light curves | Kaguya (SELENE) LALT, 4.1 m radial error | panchromatic and green ND [@sun-raponi-sigismondi-2011] |
| Lamy et al. 2015 | 2010 July 11, 2012 November 13, 2013 November 3, 2015 March 20 | 959.94 ± 0.02, 960.02 ± 0.04, 959.99 ± 0.09, 960.01 ± 0.09; mean 959.99 ± 0.06 arcseconds (696,246 ± 45 km) | 17 unattended photometers, light curves at C2 and C3 fitted to synthetic curves | Kaguya (SELENE) topographic model | 540 nm [@sun-lamy-2015] |
| Quaglia et al. 2021 | 2017 August 21, southern limit near Vale, Oregon | 959.95 ± 0.05 arcseconds; visual estimate 960.01 ± 0.08 | [?flash-spectrum] video, light curves of the last and first beads matched to simulations | LRO LOLA SLDEM2015 at 256 and LDEM at 128 pixels per degree, lunar datum 1738.091 km, Irwin's model | 480, 580 and 640 nm, no wavelength dependence [@sun-quaglia-2021] |
| Jubier et al. 2021 and Guhl 2023 | not stated | 959.98 and 960.01 arcseconds | cited by Wright and Young; not read | | [@sun-wright-young-2024] |
| Dunham, Sofia, Guhl and Herald 2016 | eclipses since the 1990s | "[956.40", 956.80"]" as printed by Quaglia et al., evidently 959.40 to 959.80 | IOTA bead timings | Watts then Kaguya | [@sun-dunham-2016] [@sun-quaglia-2021] |

Three points about this table. First, the modern high-resolution results agree: Lamy 959.99 ± 0.06, Quaglia 959.95 ± 0.05, Jubier 959.98, Guhl 960.01, Adassuriya 959.89 ± 0.18 and Jubier's help-page figure of 959.98 ± 0.02 [@sun-jubier-map-help] all fall within 0.1 arcseconds of 959.95. Wright and Young list the first four together and call the need for consensus "acute" [@sun-wright-young-2024]. Second, the Kilcik 2009 value of 959.22 ± 0.04 is 0.7 arcseconds below the others. The abstract describes an imaging analysis, not bead timing at the path limit, so it is measuring a different edge and should not be pooled with the bead results [@sun-kilcik-2009]. Third, IOTA no longer claims to see solar radius variation. Dunham wrote in 2024: "We thought in previous years that our analysis of timings of total and annular eclipses observed near the path edges showed variations in the solar radius. But now we believe that the real errors of the observations were larger than earlier formal estimates [...] So now we believe the solar radius is constant, or nearly so" [@sun-iota-dunham-2024].

## What "radius" means in an eclipse computation

Every eclipse code assumes a sharp solar edge: "In all previous diagrams and computations, we have assumed a sharp solar edge. This is the assumption that all eclipse computations implicitly make. It would be impractical to do otherwise" [@sun-quaglia-2021]. The question is which physical layer the sharp edge should stand for, and the answer depends on the product.

**The photospheric limb** is the inflection point of the [?limb-darkening-function]. It is what limb-imaging instruments measure and what Haberreiter et al. tie to the seismic radius [@sun-haberreiter-2008]. Sigismondi calls the inflection point "the standard definition of the solar limb (Hill et al. 1975)" [@sun-sigismondi-2012].

**The Baily's-bead edge** is where photospheric light becomes undetectable in a lunar valley. Raponi and Sigismondi reconstructed the outer limb-darkening function from bead light curves at the 2010 annular eclipse and found "light from solar limb detected at least 0.65 arcsec beyond the LDF inflection point" [@sun-raponi-sigismondi-2011]. Sigismondi adds that emission lines in the lower chromosphere blend into white light "located 0.7 arcsec above the photosphere" and were "perceived as the continuation of the photospheric bead", so that "observations made with different equipments yield different corrections" [@sun-sigismondi-2012]. Fig. 1 of Raponi and Sigismondi shows the perceived radius correction varying with telescope aperture and filter density [@sun-raponi-sigismondi-2011]. The same group's Solar Physics reduction of the same eclipse puts the excess at 0.85 arcseconds rather than the 0.65 arcseconds of the earlier arXiv analysis, so the two figures are two reductions of one dataset and not a disagreement about the Sun [@sun-raponi-sigismondi-2011]. On/off bead timing therefore measures an edge that depends on the detector's sensitivity and on wavelength, and it overestimates the radius when the limb-darkening function is treated as a step [@sun-raponi-sigismondi-2011].

**The eclipse solar radius** of Quaglia et al. removes the detector dependence by separating photospheric continuum from chromospheric emission in the flash spectrum. Totality is "the period of time during which the photosphere is fully and unequivocally blocked by the limb of the Moon", the radius "corresponds closely with the notion of complete [?photospheric-extinction]", and the fitted value is 959.95 ± 0.05 arcseconds with "no significant dependence on wavelength" [@sun-quaglia-2021]. They reason that "the photosphere is a layer 500 km deep and the eclipse radius should approximately be the one corresponding to the top of the photosphere", that the edge is a transition layer perhaps 50 km (0.07 arcseconds) thick, and that path limits "should be viewed as fuzzy bands 100 m wide, rather than sharp lines" [@sun-quaglia-2021]. Lamy et al. reach the same value by fitting whole light curves through a limb-darkening model at 540 nm [@sun-lamy-2015].

**Inner contacts versus outer contacts.** C2 and C3, the path limits and the central duration are all governed by the last and first photospheric light, so the eclipse radius is the right choice for them. C1 and C4 are governed by the first and last overlap of the Moon's limb with the visible disk. Observers see them through filters against the full-brightness limb, so the inflection-point radius is the closer physical model. The difference between the two radii shifts C1 or C4 by only a fraction of a second, as [Effect of the radius on eclipse products](effect-on-eclipse-products.md) sets out, and no predictor uses different solar radii for the two contact classes. Espenak does the analogous thing on the lunar side, with $k$ = 0.2725076 for penumbral contacts in the bulletins and the smaller $k$ = 0.272281 for umbral contacts, because the smaller value "avoid[s] eclipse type misidentification and predict[s] central durations that are closer to the actual durations observed at total eclipses" [@sun-espenak-seradius]. The eclipse-radius question is the solar-side twin of that choice.

## Why eclipse radii come out larger, and by how much

The mechanism is now settled. The inflection point lies about 0.33 Mm above the $\tau_{\mathrm{Ross}} = 2/3$ surface [@sun-haberreiter-2008], and detectable photospheric light extends at least a further 0.65 arcseconds (about 470 km) beyond the inflection point [@sun-raponi-sigismondi-2011]. A detector that records the last photospheric photons therefore sees a larger Sun than an instrument that fits the inflection point, and both see a larger Sun than helioseismology. The offsets, relative to Auwers' 959.63 arcseconds, are:

- Seismic and nominal radius: 0.41 arcseconds (297 km) smaller [@sun-rozelot-2016-history].
- Inflection-point radii from space: between 0.06 arcseconds smaller (HMI, 959.57) and 0.49 arcseconds larger (MDI, 960.12), with PICARD at 0.23 arcseconds larger [@sun-emilio-2015] [@sun-emilio-2012] [@sun-meftah-2018].
- Eclipse radius: 0.32 to 0.36 arcseconds (232 to 260 km) larger [@sun-quaglia-2021] [@sun-lamy-2015].

Quaglia et al. state the eclipse result: the eclipse solar radius "can be quite comfortably estimated to within 0.1″ (but certainly not to within 0.01″) and [...] its value is definitely larger than the standard radius by around 0.3″" [@sun-quaglia-2021]. Kubo's 1970 to 1991 values were already "systematically larger than the standard value of 959.63″ used for eclipse computations" [@sun-quaglia-2021]. Auwers' value sits between the inflection point and the bead edge because it mixed heliometer limb measures with eclipse-contact timings [@sun-mcglaun-auwers].

## What each predictor uses

| Predictor | Solar radius | Where stated | Notes |
|---|---|---|---|
| Astronomical Almanac, Meeus | 959.63 arcseconds at 1 au | Meeus chapter on semidiameters; Swiss Ephemeris comment "(Astr. Alm.)" [@sun-meeus-aa] [@sun-swisseph-swecl] | the algorithmic reference value |
| Espenak, NASA GSFC and EclipseWise | 959.63 arcseconds by every secondary account; the GSFC explanation page gives DE200/LE200 and k but not the solar radius | [@sun-gsfc-explain] [@sun-quaglia-2021] | $k$ = 0.2724880 penumbral in the Five Millennium Canon, 0.2725076 in the bulletins and EclipseWise, 0.272281 umbral [@sun-espenak-seradius]. No page by Espenak stating the solar radius was found by the searches described below |
| NASA SVS 2017 (Wright) | 696,000 km (959.645 arcseconds) | SVS 4515 constants table: Earth 6378.137 km, Moon 1737.4 km, DE421, ΔT 68.917 s [@sun-svs-4515] | archived snapshot read |
| NASA SVS 2023 and 2024 (Wright) | 696,000 km | Wright and Young 2024 compute their figures "assuming $r_\odot$ = 696,000 km"; SVS 5073 lists DE421, LOLA, SLDEM2015 and SRTM but no radius [@sun-wright-young-2024] [@sun-svs-5073] | no change between 2017 and 2024; the paper discusses 959.95 but does not adopt it |
| Jubier interactive maps | 959.63 arcseconds | help page: "not the true photospheric solar radius that is closer to 959.98 arc-seconds at one astronomical unit (±0.02 arc-second)" [@sun-jubier-map-help] | Dunham confirms the 2024 map used the 1976 value [@sun-iota-dunham-2024] |
| Solar Eclipse Maestro (Jubier) | defaults to 959.63 arcseconds, user-adjustable | [@sun-be-impact] [@sun-quaglia-2021] | gives durations 4 s or more longer than Irwin's model at the same radius near the limit [@sun-quaglia-2021] |
| Occult 4 (Herald) | 959.63 arcseconds, user-adjustable in the Baily's beads tool | [@sun-raponi-sigismondi-2011] [@sun-quaglia-2021] | the IOTA reduction standard; its software page lists eclipse prediction and bead analysis but states no constants [@sun-occult4-page]; gives durations 2 s or more longer than Irwin's model at the same radius [@sun-quaglia-2021] |
| Besselian Elements (Irwin, Quaglia) | 959.95 ± 0.05 arcseconds | [@sun-be-solar-radius] | the 2024 map that moved the northern limit "several city blocks" [@sun-wright-young-2024] |
| solareclipses.com (McGlaun) | 959.95 arcseconds, stated as 696,221.3 km, with k = 0.272399309 from the 1737.4 km LRO datum | [@sun-solareclipses-formulas] | one of the few Besselian-element generators documenting the switch |
| Photo Ephemeris | 959.95 arcseconds in the bead simulator only, with contact times on a smooth Moon | [@sun-photoephemeris-technote] | Kaguya (SELENE) and Herald limb, 1,800 points at 0.2° |
| USNO Solar Eclipse Computer | 696,000 km | [@sun-usno-computer] [@sun-usno-2024] | no limb profiles |
| timeanddate | not stated; "the exact position and size of each shaded area may be off by a few hundred meters" | [@sun-timeanddate-help] | advises moving "a few hundred meters toward the center" |
| Stellarium | 696,000 km, $k$ = 0.2725076 penumbral and 0.272281 umbral, copied from Espenak | [@sun-stellarium-sec] [@sun-stellarium-ssystem] | |
| Swiss Ephemeris | 696,000 km (DSUN = 1,392,000,000 m); 959.63-consistent value disabled | [@sun-swisseph-swecl] | |
| astropy | 695,700 km (IAU 2015 nominal) | [@sun-astropy-iau2015] | a conversion factor, not an eclipse radius |
| Skyfield | 696,340 km in `eclipselib.py`, lunar eclipses only | [@sun-skyfield-eclipselib] | no solar eclipse routine; the constant has no cited source |

## Sources compared

| Source | What it uniquely provides |
|---|---|
| Rozelot and Kosovichev 2026 [@sun-rozelot-kosovichev-2026] | The only review that tabulates canonical, nominal, seismic, photospheric and eclipse radii side by side with km and arcsecond values and a proposed glossary. |
| Prša et al. 2016 [@sun-prsa-2016] | The authoritative statement of what the nominal radius is and is not. |
| Haberreiter, Schmutz and Kosovichev 2008 [@sun-haberreiter-2008] | The physical explanation of the 0.33 Mm inflection-point offset. |
| Meftah et al. 2018 [@sun-meftah-2018] | The wavelength dependence of the inflection point, measured from space. |
| Lamy et al. 2015 [@sun-lamy-2015] | The largest homogeneous eclipse dataset: 17 determinations, 4 eclipses, one wavelength. |
| Quaglia et al. 2021 [@sun-quaglia-2021] | The definition of the eclipse solar radius, the sensitivity analysis at a path limit, and a three-way comparison of Occult, Solar Eclipse Maestro and Irwin's model. |
| Raponi and Sigismondi 2011 [@sun-raponi-sigismondi-2011] | Direct evidence that photospheric light extends 0.65 arcseconds beyond the inflection point. |
| Wright and Young 2024 [@sun-wright-young-2024] | NASA's own position, the 696,000 km assumption, and the sensitivity 1 s ↔ 0.03 arcseconds near the limits. |
| Dunham, IOTA 2024 [@sun-iota-dunham-2024] | The IOTA retraction of radius variation and the practical 2 km umbral-depth rule. |
| SVS 4515 [@sun-svs-4515] | The only SVS page that prints the constants block. |

## What a developer should do

1. Store the solar radius as a named, versioned constant in arcseconds at 1 au and convert with $R_\odot = a \sin s_0$, recording which convention you use, since arcsine and arctangent differ by 0.011 arcseconds.
2. Default the umbral and antumbral computations (path limits, C2, C3, central duration, bead simulation) to the eclipse solar radius 959.95 arcseconds and carry ± 0.05 arcseconds as its uncertainty [@sun-quaglia-2021]. Keep 959.63 arcseconds available as a compatibility mode, because every published almanac product and most third-party checks still use it.
3. Never use the IAU 2015 nominal value or astropy's `R_sun` for eclipse geometry. It is 0.73 arcseconds smaller than the eclipse radius and would widen the path by about 2.5 to 4 km [@sun-wright-young-2024].
4. Read first: Quaglia et al. 2021 (arXiv 2107.09416) for the definition and the sensitivity plots, Lamy et al. 2015 for the photometer method, Haberreiter et al. 2008 for the physics, and section 6.4 of Wright and Young 2024 for the state of the debate.
5. Data to obtain: the LOLA SLDEM2015 and LDEM at 128 pixels per degree grids used by Irwin and by Wright, whose labels and download locations are in [Datasets: Watts, Kaguya, LOLA](../05-lunar-limb/datasets-watts-kaguya-lola.md), because an eclipse radius is only meaningful together with the limb profile it was fitted against.

## What this changes

The pipeline design gains one explicit parameter, `solar_radius_arcsec`, with a default, an uncertainty and a provenance string, and a rule that the umbral products use it while the penumbral products may use the same value without measurable loss. The path-limit and duration outputs gain an uncertainty band derived from ± 0.05 arcseconds. Nothing else in the Besselian or raster formulation changes, since the radius enters only through the cone half-angles and the limb test [@sun-wright-young-2024].

## Open questions

- Obtain Auwers 1891 (Astronomische Nachrichten 128, 361) and confirm the eclipse-contact component of the mean and the stated uncertainty [@sun-auwers-1891].
- Obtain the Jubier et al. 2021 and Guhl 2023 papers cited by Wright and Young for 959.98 and 960.01 arcseconds and record their limb datasets and wavelengths [@sun-wright-young-2024].
- Obtain Kilcik et al. 2009 in full to establish which edge the 959.22 ± 0.04 arcsecond value measures [@sun-kilcik-2009].
- Obtain the IOTA analyses of the 2023 October 14 annular and 2024 April 8 total eclipse bead videos, which Dunham says will appear in the Journal for Occultation Astronomy, for a post-2021 eclipse radius [@sun-iota-dunham-2024].
- Obtain an explicit statement by Espenak of the solar radius used in the Five Millennium Canon, NASA/TP-2006-214141. Searches of eclipsewise.com and eclipse.gsfc.nasa.gov for "solar radius" and "959.63" returned only the lunar-radius page and the prediction explanation, neither of which names the solar value [@sun-espenak-seradius] [@sun-gsfc-explain].
- Read the Occult 4 help text for the solar-radius input in the Baily's beads tool to record Herald's default and any correction option.
