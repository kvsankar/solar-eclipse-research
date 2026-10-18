---
title: Observation, brightness and validation
seo_title: Lunar Eclipse Crater Timings, Danjon Scale and Accuracy
description: How crater timings test lunar eclipse predictions, why brightness is not predicted, and how historical lunar eclipses constrain ΔT.
order: 3
status: working
updated: 2026-10-17
tags: [lunar-eclipse, crater-timings, danjon-scale, aerosols, validation, delta-t, historical-eclipses]
---

::: summary
- **Crater timings are the observable that tests lunar eclipse predictions.** An observer times the instant the steepest gradient of the umbra's edge crosses a crater. A single timing has a standard deviation of 25 to 30 seconds, and the 22,539 timings in VizieR VI/140 cover 94 eclipses from 1842 to 2011 [@lun-nasa-crater-page] [@lun-herald-sinnott-2014] [@lun-vizier-vi140].
- **Limb contacts are worse than crater timings.** Primary contacts reduce to layer heights of 80.0 km at ingress and 90.4 km at egress, against 88.2 and 84.7 km for craters. At a limb contact the observer sees only one side of the edge [@lun-herald-sinnott-2014].
- **An umbral contact can be predicted to a few seconds against the mean of many observers**, and to about half a minute against a single observer. The ephemeris contributes about 1/40 second, and the real layer varies by about ±4 km, or ±4 seconds, between eclipses. The choice of enlargement rule moves contacts by 20 to 90 seconds, so the rule must be stated [@lun-5mcle-tp2009] [@lun-herald-sinnott-2014].
- **None of the products and programs cited here predicts brightness.** The Danjon scale of 0 to 4 grades it after the fact. Volcanic aerosols dominate it: eclipses after Agung, El Chichón and Pinatubo were very dark, and Keen turns the deficit against a clear-sky prediction into aerosol optical depth [@lun-danjon-1921] [@lun-5mcle-tp2009] [@lun-keen-2019].
- **Independent predictors agree closely.** Skyfield matches the NASA Canon's 3,642 eclipses of AD 1000 to 2500 with 8 type disagreements and times a few seconds earlier. Meeus's closed form finds 227 of the 228 catalogued eclipses of 1951 to 2050 with a mean time error of 0.37 minutes [@sw-skyfield-almanac] [@cat-meeus-1991-aa] [@lun-5mkle-ascii].
- **Timed lunar eclipses are the backbone of ancient ΔT.** Babylonian texts are mostly lunar, and Stephenson, Morrison and Hohenkerk use 180 Babylonian timings from −720 to −9. A single eclipsed Moon that set before sunrise in −694 constrains ΔT near +20,000 seconds [@earth-smh2016].
:::

**The question.** What can be observed during a lunar eclipse, how do the observations test the shadow model and the brightness of the eclipsed Moon, how well do the main predictors agree, and how are lunar eclipse records used to measure ΔT?

## Crater timings

A [?lun-crater-timing|crater timing] records the instant the umbra's edge crosses a lunar feature. NASA's guidance asks for "a precision of 0.1 min" and for the instant "when the most abrupt gradient at the umbra's edge crosses the apparent center of the crater" [@lun-nasa-crater-page]. For large craters such as Tycho and Copernicus the observer times the two opposite edges and averages them [@lun-nasa-crater-page]. The same page states that predicted times are tabulated for up to 20 craters per eclipse and are computed with Danjon's 1/85 enlargement "and the effects of Earth's oblateness" [@lun-nasa-crater-page].

Herald and Sinnott describe the history. Graham and Short timed the umbra on Tycho, Plato, Manilius and Mare Crisium in 1736 to the nearest 5 seconds [@lun-herald-sinnott-2014]. Most of their 1842 to 2011 timings date from 1960 to 2000, from programmes run by Byron Soulsby and by Sky & Telescope under Joseph Ashbrook [@lun-herald-sinnott-2014]. All were made visually at the eyepiece, "typically with telescopes of 5 to 25 cm aperture" [@lun-herald-sinnott-2014].

The dataset is VizieR catalogue VI/140. Its file `crater_t.dat` has 22,539 records, each with the eclipse date, the feature name from the Gazetteer of the International Astronomical Union (IAU), an event code, the UT of the event to the second, the number of observers combined, the computed layer height in km, the latitude of the event on the umbra and the percentage enlargement [@lun-vizier-vi140]. The event codes run from 0, first contact with the Moon's limb, through 1 to 3 for a feature at ingress, 4 for second contact, 5 for third contact, 6 to 8 for a feature at egress, and 9 for fourth contact [@lun-vizier-vi140]. The archive also holds a scan of J. F. J. Schmidt's unpublished manuscript of observations of 1842 to 1879 [@lun-vizier-vi140].

### The reduction

For each timing Herald and Sinnott compute the observed umbral radius. They then compute theoretical radii with equations [3] and [4] of [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md) for $h = 0$ and for $h = 0.02352$ Earth radii, which is 150 km. A linear interpolation between the two gives the observed layer height [@lun-herald-sinnott-2014]. The method treats each crater at its own distance, which the classical rules do not [@lun-herald-sinnott-2014].

The paper describes the projection of a crater in words only. "The distance $Z_m$ of the Moon beyond the fundamental plane is obtained from the Besselian elements. The distance $(Z_m - Z_c)$ of a point on the Moon's surface at the edge of the shadow is obtained by projecting that point onto the plane through $Z_m$ using the heliocentric lunar librations." The same projection, "when combined with the geocentric rectangular coordinates of the Moon, gives the location of the point on the Moon's surface relative to the shadow axis" [@lun-herald-sinnott-2014]. The paper prints no formula for either step.

A formula consistent with that description is derived here and is not given by the paper. Let the crater have selenographic longitude $l$ and latitude $b$. Let $(l_\odot, b_\odot)$ be the heliocentric libration, the selenographic coordinates of the point on the Moon nearest the Sun. During an eclipse that point is near the shadow axis on the Earth-facing side. With the lunar radius $k$ in Earth radii,

$$Z_m - Z_c = k\,[\sin b\,\sin b_\odot + \cos b\,\cos b_\odot\cos(l - l_\odot)].$$

The crater's offset across the axis follows by rotating the same selenocentric unit vector into the fundamental-plane axes and adding the Moon's $x$ and $y$. The libration angles and the frames that give them are in [Lunar figure and libration](../10-shared/08-lunar-and-solar-model/lunar-figure-and-libration.md). There the geocentric libration is the selenographic position of the point nearest the Earth. The heliocentric libration is the same computation with the Sun in place of the Earth.

### What the timings show about the observers

"The standard deviation of an individual timing is of the order of 25 to 30 secs" [@lun-herald-sinnott-2014]. "This produces an uncertainty of about 25 to 30 km in NEL height (again, for a single timing), making it essential to combine many timings" [@lun-herald-sinnott-2014].

Limb contacts are biased. "At first and fourth contact, the observer sees only the penumbral side of the umbra's edge. At second and third contact, the observer sees only the umbral side" [@lun-herald-sinnott-2014]. Craters and spots give mean layer heights of 88.2 km at ingress and 84.7 km at egress. Primary contacts give 80.0 km and 90.4 km [@lun-herald-sinnott-2014]. Within a single eclipse the derived height also tends "to come out slightly smaller when the Moon as a whole is darkest (nearer totality), probably biasing observers' judgment of the umbral edge", as shown for 1989 August 17 [@lun-herald-sinnott-2014].

The paper tests the claim of Marmet and Couture that the enlargement is an optical illusion. If it were, the angular enlargement would be constant and the layer height would grow by about 10 km between lunar distances of 56 and 64 Earth radii. The measured heights show no such trend, which "prima facie negates the hypothesis" [@lun-herald-sinnott-2014].

## The Danjon scale

Danjon proposed the brightness scale in 1921. His original text gives five "coefficients d'éclat" from 0 to 4 [@lun-danjon-1921]:

- 0: very dark eclipse, the Moon almost invisible, especially at mid-totality;
- 1: dark eclipse, grey or brownish, details hard to make out;
- 2: dark red or rust-coloured eclipse, usually with a very dark central spot and a fairly bright outer zone;
- 3: brick-red eclipse, the shadow often bordered by a grey or yellow, fairly bright zone;
- 4: copper-red or orange eclipse, very bright, with a very bright bluish outer zone.

These are paraphrased from the French. The NASA Canon prints an English version with the same five steps [@lun-5mcle-tp2009]. The [?lun-danjon-scale|Danjon scale value L] is best judged "with the naked eye, binoculars, or a small telescope near the time of mid-totality", with the outer umbra judged near the start and end of totality, recording "the instrumentation and the time" [@lun-5mcle-tp2009].

Danjon used the scale to relate brightness to the solar cycle. His table gives the mean brightness of 70 eclipses grouped by the years since solar minimum, for 1823 to 1867 and for 1867 to 1920 [@lun-danjon-1921]. The overall mean rises from 1.1 in the first two years after minimum to 2.2, 2.6, 3.2 and 3.3 in the later groups [@lun-danjon-1921]. Later work weakened the link. Herald and Sinnott summarise Bouška and Švestka's 1950 analysis of 33 eclipses as finding "only a weak correlation, at best, with solar activity" [@lun-herald-sinnott-2014]. They also find that "published Danjon L ratings show a great deal of scatter" [@lun-herald-sinnott-2014].

## Volcanic aerosols and the brightness of totality

The light in the umbra is sunlight refracted by the atmosphere. The Canon describes the troposphere and stratosphere acting "together as a ring-shaped lens that refracts heavily reddened sunlight into Earth's umbral shadow", with the inner umbra fed by lower, denser layers [@lun-5mcle-tp2009]. Aerosols "can significantly attenuate sunlight before it is refracted into the umbra". The Canon names the 1963 Agung and 1982 El Chichón eruptions, both "followed by several years of very dark eclipses", and Pinatubo in 1991, after which the eclipse of 1992 December 9 was "so dark that the Moon's dull gray disk was difficult to see with the naked eye" [@lun-5mcle-tp2009].

The darkness does not change the umbra's size. For 1963 December 30, nine months after Agung, Sky & Telescope collected 13 estimates giving a visual magnitude of +4.1 at mid-totality. Herald and Sinnott's layer height for that eclipse is 87.1 ± 1.4 km, against 86.9 km for the whole dataset [@lun-herald-sinnott-2014]. They conclude that "any correlation with the brightness or darkness of the umbra is not statistically significant" [@lun-herald-sinnott-2014].

Keen turned the brightness deficit into a measurement. His 1983 Science paper compared the observed brightness of 21 eclipses of 1960 to 1982 with "theoretical calculations based on refraction by an aerosol-free atmosphere" to derive global [?lun-aod|aerosol optical depths] (AOD). That description is the abstract, reported secondhand and unconfirmed against the paper [@lun-keen-1983]. His 2019 poster for the National Oceanic and Atmospheric Administration (NOAA) states the method directly: "Knowing the eclipse's geometry, the moon's brightness can be predicted (assuming no volcanic aerosols)" [@lun-keen-2019]. The record then held 147 eclipses from the literature, observations sent by observers and 31 eclipses observed by Keen, extending from 1805 to 2019 [@lun-keen-2019]. It gives a mean volcanic optical depth of 0.002 for 1996 to 2018 against 0.041 for the previous 14 years. The eclipse of 2019 January ran "about half a magnitude fainter, or about 40% dimmer, than the prediction", which "computes to an AOD of about 0.01, likely due to the eruption of Ambae volcano" [@lun-keen-2019].

The scattered component complicates prediction. García Muñoz and colleagues analysed a spectrum of the umbra on 2008 August 16 and found that "diffuse sunlight is a major component of the measured spectrum at wavelengths shorter than 600 nm" [@lun-garciamunoz-2011-grl]. They attribute it to the Kasatochi cloud, which "both attenuates the unscattered sunlight and enhances moderately the scattered component" [@lun-garciamunoz-2011-grl]. Their companion theory paper in the Journal of Quantitative Spectroscopy and Radiative Transfer (JQSRT) models the scattered component, and its content is not reproduced here [@lun-garciamunoz-palle-2011].

### The limits of brightness prediction

A brightness prediction needs the eclipse geometry, a refraction and extinction model of the atmosphere at the terminator, and the aerosol and cloud load on the eclipse date. The first is exact. The other two are not known in advance. No cited product or program predicts L or the eclipsed Moon's magnitude. The list covers the NASA Canon and Catalogue, the EclipseWise eclipse pages, the 2023 note of the Institut de mécanique céleste et de calcul des éphémérides (IMCCE), Skyfield's `eclipselib`, Stellarium's eclipse tables and Astronomy Engine [@lun-5mcle-tp2009] [@lun-ew-2025mar14] [@lun-imcce-2023-may] [@sw-skyfield-eclipselib] [@sw-stellarium-astrocalc] [@sw-astronomy-engine-c]. The penumbral phase is a different matter. The Canon states that a penumbral magnitude above about 0.6 is needed before skilled observers see shading, and that the penumbral eclipse "only becomes readily apparent when it is within ~0.05 magnitudes of becoming a partial eclipse" [@lun-5mcle-tp2009]. Stellarium flags a partial penumbral eclipse as visible to the unaided eye only when the penumbral magnitude exceeds 0.7, a value its code calls a "rule of thumb" [@sw-stellarium-astrocalc].

## Validation of predictions

### Observed against predicted shadow size

The shadow model is the only part of a lunar eclipse prediction that observation tests at the level of seconds. The tests are the enlargement determinations in [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md). Sky & Telescope's crater timings give 1.61 to 2.24 per cent for four eclipses of 1972 to 1982, against Chauvenet's 2 per cent [@lun-5mcle-tp2009]. Herald and Sinnott's 94 eclipses give a mean of 1.88 per cent, or 86.9 km, with single eclipses from 82.2 to 90.7 km [@lun-herald-sinnott-2014]. Under Danjon's factor 1.01, a layer of about 74 km above the 45-degree radius, the umbra is predicted too small by about 12 km of layer on average. That is about 12 seconds of time at a radial crossing, computed here from the rule of thumb of about 1 second per kilometre.

### Predictor against predictor

**IMCCE and NASA.** For the penumbral eclipse of 2023 May 5 IMCCE gives maximum at 17h 22min 54.174s UTC and penumbral magnitude 0.9637796 [@lun-imcce-2023-may]. The NASA catalogue gives 17:24:05 TD with ΔT 73 seconds, or 17:22:52 UT, and penumbral magnitude 0.9636 [@lun-5mkle-ascii]. Both use Danjon's rule.

**EclipseWise and NASA.** For three total eclipses of 2022 and 2025, EclipseWise under Herald and Sinnott and DE430 gives umbral magnitudes about 0.002 larger and totality about 0.6 minutes longer than the NASA catalogue under Danjon. Gamma agrees to 0.0001 [@lun-ew-2022nov08] [@lun-ew-2025mar14] [@lun-ew-2025sep07] [@lun-nasa-le2001]. The table is in [Shadow geometry and enlargement](shadow-geometry-and-enlargement.md).

**Skyfield and the NASA Canon.** Skyfield's documentation reports its own comparison, generated by the script `design/eclipses_lunar.py` against the NASA ASCII catalogue with DE422 [@sw-skyfield-almanac] [@lun-skyfield-design]. For AD 1000 to 2500 it finds all 3,642 eclipses and disagrees on partial against total in 8 cases, about 0.2 per cent. It finds an eclipse on 1571 July 7 that the Canon does not list [@sw-skyfield-almanac]. Its times are "a few seconds earlier" than the Canon's. The difference "rarely exceeds 2 seconds" near the present and reaches "20 seconds" for eclipses 2,000 years ago [@sw-skyfield-almanac]. Over the full five millennia it misses four eclipses and finds two extra. The two missed eclipses nearest the present, 859 April and 2791 February, have penumbral magnitudes of 0.0007 and 0.0006 in the Canon [@sw-skyfield-almanac]. The documentation attributes the disagreements to the Supplement having "used the old VSOP87 theory". In fact the Canon, not the Supplement, uses VSOP87 and ELP-2000/82 [@sw-skyfield-almanac] [@lun-5mcle-tp2009].

### Meeus's method against the NASA catalogue

Meeus's closed form is reimplemented here from the constants quoted in [Enumeration, elements and contacts](enumeration-elements-and-contacts.md) and evaluated for every full moon of 1951 to 2050. The results are matched by time against the 228 eclipses in the NASA ASCII catalogue [@cat-meeus-1991-aa] [@lun-5mkle-ascii]. With Meeus's Danjon constants the results are:

- 227 eclipses found and none spurious. The one missed is the penumbral eclipse of 2027 July 18, catalogue magnitude 0.0014;
- one type disagreement: 2015 April 4, total at umbral magnitude 1.0008 in the catalogue and partial at 0.9956 by Meeus;
- time of greatest eclipse: mean absolute difference 0.37 minutes, maximum 1.21 minutes;
- gamma: mean absolute difference 0.0025, maximum 0.0069, mean difference 0.0000;
- umbral magnitude: mean difference −0.0045, maximum absolute 0.0129. Penumbral magnitude: mean difference −0.0040;
- durations: mean differences −2.2 minutes penumbral, −1.5 minutes partial and −0.75 minutes total.

With Meeus's constants for the traditional 1/50 rule, the method finds all 228 eclipses plus 2016 August 18 at penumbral magnitude 0.0138. NASA lists that date among the penumbral eclipses that exist only under Chauvenet's rule [@lun-nasa-shadow-page]. The umbral magnitude bias becomes +0.0008, the penumbral +0.0211, the total-duration bias +0.32 minutes, and there are no type disagreements [@cat-meeus-1991-aa] [@lun-5mkle-ascii]. The time and gamma errors match Meeus's own accuracy statement for solar eclipses of 0.36 minutes mean and 1.1 minutes greatest [@cat-meeus-1991-aa]. The systematic offset of the umbral magnitude under the Danjon constants is larger than the scatter. No cited source explains it. Meeus's own example compares his penumbral magnitude of 0.463 for 1973 June 15 with 0.469 in the Connaissance des Temps, and his maximum at 20h 51m TD with 20h 50.7m [@cat-meeus-1991-aa].

### What accuracy is achievable

The error budget of an umbral contact time has these terms:

| Term | Size | Source |
|---|---|---|
| Truncated ELP-2000/82 against full theory | about 1/40 second | [@lun-5mcle-tp2009] |
| Centre of figure against centre of mass, about 0.5 arcseconds | about 1 second, computed here at 0.52 arcseconds per second | [@lun-5mcle-tp2009] |
| ΔT for a past modern eclipse | well below 1 second | [@earth-usno-deltat] |
| Choice of enlargement rule, Danjon against Chauvenet | about 20 seconds at U1 and U4, 29 seconds at U2 and U3, 93 seconds at P1 and P4 | computed here from [@cat-meeus-1991-aa] |
| Spherical 45-degree Earth against oblate | "of the order of 1 minute" | [@lun-herald-sinnott-2014] |
| Eclipse-to-eclipse change of the layer, ±4 km | about ±4 seconds at a radial crossing | computed here from [@lun-herald-sinnott-2014] |
| One visual observer | 25 to 30 seconds | [@lun-herald-sinnott-2014] |

With the Herald and Sinnott rule, a predicted umbral contact or crater passage is therefore good to a few seconds against the mean of many observers. It is good to about half a minute against any single observer. P1 and P4 are "completely unobservable", so their prediction cannot be validated by observation at all [@lun-nasa-shadow-page].

## Historical lunar eclipses as evidence for ΔT

Lunar eclipses dominate the ancient record. Stephenson, Morrison and Hohenkerk state that "most of the surviving eclipse texts are of lunar eclipses", from before 700 BC to about 50 BC in Babylon [@earth-smh2016]. Babylonian first contacts are timed from sunrise or sunset, later phases from first contact, and after about 250 BC also from the culmination of chosen stars [@earth-smh2016]. Their analysis uses 180 Babylonian timings of lunar and solar eclipses from −720 to −9 [@earth-smh2016]. It weights them with Huber and De Meis's variance $\sigma^2 = 2.8^2 + (0.14\,d)^2$, "where $d$ is the elapsed time in degrees from sunset/sunrise to the eclipse contact" [@earth-smh2016]. One time-degree is 4 minutes.

Other cultures add timings. Chinese lunar eclipses before about AD 1050 were "timed to the nearest fifth of a night watch", and later to the nearest *ke* [@earth-smh2016]. Ptolemy's *Almagest* preserves eight Greek lunar timings, mainly from 201 BC to 141 BC [@earth-smh2016]. Medieval Arab astronomers timed contacts by "the altitude of the Moon or a selected bright star", and 32 Arab lunar timings of 854 to 1019 enter the solution [@earth-smh2016].

Untimed records constrain ΔT as well. Seven Babylonian lunar eclipses in which the Moon rose or set eclipsed bound the solution. "The upper limit of the lunar eclipse (Babylonian) of −694 ... where the eclipsed Moon set before sunrise" is one of two observations "critical in constraining the value of ΔT close to +20 000 s around the epoch −700" [@earth-smh2016].

The reduction needs the same contact computation as a prediction. The authors "developed our own software for the computation of the contact times on the TT time scale for solar and lunar eclipses ... from the procedures set out in chapter 8 of the Explanatory Supplement" [@earth-smh2016]. The paper does not state its shadow enlargement. Chapter 8 of the 1992 Supplement uses Chauvenet's rule [@lun-es1992]. A change of rule moves a contact by 20 to 90 seconds, which is small against a Babylonian standard deviation of at least 2.8 time-degrees, or about 11 minutes. This comparison is computed here. The paper adds that its ΔT values "should be used in conjunction with the lunar ephemeris JPL DE430", whose tidal acceleration is −25.82 arcseconds per century squared [@earth-smh2016]. The NASA Canon applies the equivalent correction for its −25.858 [@lun-5mcle-tp2009]. The models built from these data are compared in [ΔT and Earth rotation](../10-shared/07-earth-and-time/delta-t-and-earth-rotation.md).

## Sources compared

| Source | Observations | What it measures | What it adds |
|---|---|---|---|
| Herald and Sinnott 2014 [@lun-herald-sinnott-2014] | 22,539 timings, 94 eclipses | NEL height, enlargement, shape | Observer bias, rejection of extra flattening, recommended rule |
| VizieR VI/140 [@lun-vizier-vi140] | the same timings | per-timing height and enlargement | Machine-readable test set and Schmidt's 1842 to 1879 manuscript |
| NASA crater page [@lun-nasa-crater-page] | method only | how to time | Timing protocol and the rule used for predicted crater times |
| Danjon 1921 [@lun-danjon-1921] | 70 eclipses | brightness against solar phase | The original L scale |
| Keen 1983, 2019 [@lun-keen-1983] [@lun-keen-2019] | 21 eclipses, later 147 plus 31 | aerosol optical depth | Brightness deficit against a clear-sky prediction |
| García Muñoz et al. 2011 [@lun-garciamunoz-2011-grl] | one umbral spectrum | scattered against refracted light | Limit of the refraction-only brightness model |
| Skyfield documentation [@sw-skyfield-almanac] | 3,642 and 12,064 eclipses | type and time against the Canon | An independent ephemeris-based check |
| Stephenson, Morrison and Hohenkerk 2016 [@earth-smh2016] | Babylonian, Chinese, Greek, Arab records | ΔT | Lunar eclipses as the main ancient clock |

## What a developer should do

Validate a lunar eclipse implementation in three steps. First, reproduce the NASA ASCII catalogue for 1951 to 2050 with the Danjon rule. Expect agreement in type except for eclipses within about 0.005 of a boundary, and agreement in time to a few seconds with a full ephemeris. Second, switch to Herald and Sinnott and reproduce the EclipseWise pages for 2022 November 8 and 2025 March 14 and September 7 to within a second. Third, reduce the VI/140 timings to layer heights with your own crater projection, and check that the mean is close to 87 km with no trend in lunar distance. Do not offer a brightness prediction beyond a clear-atmosphere estimate labelled as such. Read Herald and Sinnott 2014 and the VI/140 ReadMe first.

## What this changes

Validation of lunar eclipse products needs a second kind of reference data. Solar products are validated against limb-corrected contacts and path edges. Lunar products are validated against crater timings, and through them against the enlargement model. The pipeline's validation stage should load VI/140 and the NASA catalogue as fixtures. Nothing else in the pipeline changes.

## Open questions

- Obtain Keen 1983, Science 222, 1011 to 1013, for the clear-atmosphere brightness model and its constants [@lun-keen-1983].
- Obtain García Muñoz and Pallé 2011, JQSRT 112, 1609 to 1621, for a radiative-transfer model of the umbra that includes scattering [@lun-garciamunoz-palle-2011].
- Obtain Link 1969, *Eclipse Phenomena in Astronomy*, for the classical refraction theory of umbral brightness [@lun-link-1969].
- Obtain post-2011 crater-timing reductions, for example from the 2014 to 2015 tetrad or 2022, to test whether the 87 km layer still holds.
- Obtain the electronic supplementary tables S5 and S9 of Stephenson, Morrison and Hohenkerk 2016 to reproduce the lunar-eclipse ΔT values and their stated enlargement rule [@earth-smh2016].
- Obtain Sky & Telescope's crater-timing results for 1982, cited in the Canon's Table 1-3, to compare its reduction with VI/140 [@lun-5mcle-tp2009].
