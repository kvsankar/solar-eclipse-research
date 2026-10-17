---
title: Shadow geometry and enlargement
seo_title: Earth's Shadow Size in Lunar Eclipse Calculation
description: How the Earth's umbra and penumbra are sized for lunar eclipses, and how the Chauvenet, Danjon and Herald and Sinnott rules change the results.
order: 2
status: working
updated: 2026-10-17
tags: [lunar-eclipse, umbra, penumbra, shadow-enlargement, danjon, chauvenet, herald-sinnott]
---

::: summary
- **The Earth's shadow at the Moon is computed from three angles.** The umbral radius is the Moon's horizontal parallax minus the Sun's semidiameter plus the Sun's parallax, and the penumbral radius is the sum of all three. Every almanac then enlarges the result, because the observed umbra is larger than the airless geometry predicts [@lun-es1992] [@lun-5mcle-tp2009].
- **Three enlargement rules are in use.** Chauvenet multiplies both radii by 1.02. Danjon adds a fixed layer of about 1/85 of the Earth's radius through the factor 1.01 on the lunar parallax. Herald and Sinnott add a layer 0.0136 Earth radii, or 87 km, above an oblate Earth whose apparent radius depends on the contact point [@bes-chauvenet-1863] [@lun-nasa-shadow-page] [@lun-herald-sinnott-2014].
- **Who uses which.** The Astronomical Almanac and Stellarium's default use Chauvenet. The Connaissance des Temps, Meeus, the NASA Five Millennium Canon of Lunar Eclipses (NASA/TP-2009-214172) and Skyfield use Danjon. EclipseWise pages updated in 2022 use Herald and Sinnott. Astronomy Engine uses a sphere of 6371 km plus 88 km [@lun-5mcle-tp2009] [@sw-skyfield-eclipselib] [@lun-stellarium-solarsystem] [@lun-ew-2025mar14] [@sw-astronomy-engine-c].
- **Danjon gives umbral magnitudes about 0.005 smaller and penumbral magnitudes about 0.026 smaller than Chauvenet.** That moves umbral contacts by roughly 20 to 30 seconds and penumbral contacts by about 1.5 minutes. It also changes the type of an eclipse near a boundary, for example 1988 March 3 [@cat-meeus-1991-aa] [@lun-nasa-shadow-page].
- **Crater timings favour a constant layer height over a constant percentage.** From 22,539 timings at 94 eclipses between 1842 and 2011, the percentage enlargement depends on the lunar distance and the layer height does not. The mean height is 86.9 ± 0.2 km, and single eclipses range from 82.2 to 90.7 km [@lun-herald-sinnott-2014].
- **The umbra's flattening is the Earth's, projected.** Herald and Sinnott find no latitude trend in the layer height, which rejects the older claims of an extra-flattened umbra such as Soulsby's 1/102 [@lun-herald-sinnott-2014] [@cat-meeus-1991-aa].
:::

**The question.** How are the angular radii of the Earth's umbra and penumbra at the Moon's distance computed, which atmospheric enlargement does each almanac and program apply, and how large are the resulting differences in magnitude, contact times and eclipse type?

## The airless geometry

A lunar eclipse is the Moon entering the [?lun-earth-umbra|Earth's umbra] or [?lun-earth-penumbra|penumbra]. The geometry is the solar-eclipse geometry with the Earth as the shadow-casting body. The 1992 Explanatory Supplement derives the penumbral radius $R_p$, as seen from the Earth's centre, from three known angles. They are the Moon's [?horizontal-parallax|horizontal parallax] $\pi_m$, the Sun's apparent semidiameter $s_\odot$ and the Sun's horizontal parallax $\pi_\odot$ [@lun-es1992]:

$$R_p = \pi_m + \pi_\odot + s_\odot \qquad (8.231\text{-}1)$$

The umbra is bounded by the exterior tangents of the Sun and Earth, with its vertex beyond the Moon. Its radius at the Moon's distance is [@lun-es1992]

$$R_u = \pi_m + \pi_\odot - s_\odot .$$

The Supplement writes these radii as $f_1$ and $f_2$. In this corpus $f_1$ and $f_2$ are the vertex half-angles of the Moon's shadow cones, so this topic uses NASA's $R_p$ and $R_u$ instead [@lun-nasa-shadow-page]. All three inputs are geocentric angles, usually in arcseconds. The Moon's own semidiameter $s_m$ enters only when the radii are turned into contact conditions, as described in [Enumeration, elements and contacts](enumeration-elements-and-contacts.md).

For a mean lunar parallax of 3422.6 arcseconds and the Sun at 1 au, with $s_\odot = 959.63$ arcseconds and $\pi_\odot = 8.794$ arcseconds, the airless umbra on the 45-degree radius is about 2466 arcseconds, or 41.1 arcminutes. The Moon's diameter at this distance is about 1865 arcseconds, so the airless umbral diameter is about 2.6 times the Moon's diameter. The enlarged umbra of the table below is about 2.7 times. These figures are computed here from the formulas above. The Canon quotes "~2.7x" for the umbral diameter [@lun-5mcle-tp2009].

## The oblate Earth in the classical rules

The Earth is not a sphere, so its shadow is not a circular cone. The classical rules replace the Earth by a sphere of the radius at latitude 45 degrees. The 1992 Supplement does this by "substituting for $\pi_m$ a parallax reduced to latitude 45°, so that $\pi_1 = 0.998340\,\pi_m$" [@lun-es1992]. The 1961 Supplement printed the factor as 0.998333 and noted the change to 0.998340 "for 1968 onwards" [@lun-es1961]. NASA explains the factor as "0.998340 ≅ 1 - 0.5 * 1/300", half of a flattening of about 1/300 [@lun-nasa-shadow-page]. The Connaissance des Temps uses 1/594, which is half of its flattening of 1/297 [@lun-5mcle-tp2009].

The true cross-section is an ellipse whose flattening changes during the year. Herald and Sinnott state that the flattening of the base of the umbral cone "varies between about 1/298 for eclipses near an equinox, to about 1/355 for eclipses near a solstice" [@lun-herald-sinnott-2014]. The cause is the tilt of the polar axis towards the Sun, which changes the apparent polar radius [@lun-herald-sinnott-2014]. At the Moon's distance the flattening grows for geometric reasons, and Ahnert and Meeus give 1/214 as the mean [@lun-herald-sinnott-2014] [@cat-meeus-1991-aa]. Meeus adds that Soulsby found "a mean oblateness of 1/102 from observations made at 18 lunar eclipses in the period 1974 - 1989" [@cat-meeus-1991-aa] [@lun-soulsby-1990].

## The enlargement problem

The observed umbra is larger than the geometry predicts, and the correction for it is called [?lun-shadow-enlargement|shadow enlargement]. Philippe de La Hire found in the early 1700s that the predicted radius "needed to be enlarged by about 1/41" to fit timings [@lun-5mcle-tp2009]. Herald and Sinnott trace the practice to de La Hire's tables of 1687, which added 90 arcseconds to the umbral radius "because of the shadow of the atmosphere", revised to 60 arcseconds from the 1702 edition [@lun-herald-sinnott-2014]. Enlargements of 1/40 to 1/65 appear in the eighteenth and nineteenth century literature [@lun-herald-sinnott-2014].

The physical cause is the atmosphere, but the edge is a perception. NASA states that "there is no abrupt boundary between the umbra and penumbra" and that, by Kuhl's 1928 contrast theory, "the edge of the umbra is perceived at the point of inflexion in the shadow density" [@lun-nasa-shadow-page]. The Canon equates that inflexion with "a layer in Earth's atmosphere at an altitude of about 120 to 150 km" [@lun-5mcle-tp2009]. Herald and Sinnott avoid any physical claim: their layer is "merely a single quantity, derived from timings and free of the effect of the known oblateness of the solid Earth, that represents the effects of the Earth's atmosphere" [@lun-herald-sinnott-2014].

### Chauvenet's rule: 2 per cent of both radii

Chauvenet's 1863 Manual multiplies the umbral radius by 51/50. His equation (587) reads $\text{App. semid. of shadow} = \tfrac{51}{50}(\pi - s' + \pi')$, with $\pi$ the lunar and $\pi'$ the solar parallax and $s'$ the solar semidiameter [@bes-chauvenet-1863]. His footnote cites Lambert's 1/40, Mayer's 1/60, and 1/50 from Beer and Mädler's timings of "eclipses of lunar spots" on 1833 December 26 [@bes-chauvenet-1863]. The modern almanac form adds the 45-degree factor [@lun-es1992] [@lun-nasa-shadow-page]:

$$R_p = 1.02\,(0.998340\,\pi_m + s_\odot + \pi_\odot), \qquad R_u = 1.02\,(0.998340\,\pi_m - s_\odot + \pi_\odot).$$

Herald and Sinnott confirm that this expression "with E set to 1.02, is still used today in the Astronomical Almanac for predicting the primary contacts of lunar eclipses", citing page A83 of the 2014 volume [@lun-herald-sinnott-2014]. No source cited here states the Almanac's rule for any later year.

### Danjon's rule: a fixed layer on the Earth's radius

Danjon argued in 1951 that a relative enlargement of both radii is wrong. The NASA page summarises his argument: "the only reasonable way of accounting for a layer of opaque air surrounding Earth is to increase the planet's radius by the altitude of the layer", so that both shadows receive "the same absolute correction and not the same relative correction" [@lun-nasa-shadow-page] [@lun-danjon-1951]. Danjon put the layer at 75 km, "an enlargement of Earth's radius and the Moon's parallax of about 1/85" [@lun-nasa-shadow-page]. The rounded factor 1.01 adds $1.01 - 0.998340 = 0.01166$ Earth radii to the 45-degree radius, which is 74 km. This topic quotes 75 km for Danjon's stated layer and 74 km for the layer that the factor 1.01 implies. The 74 km value is computed here. The Connaissance des Temps adopted the rule in 1951 [@lun-5mcle-tp2009]:

$$R_p = 1.01\,\pi_m + s_\odot + \pi_\odot, \qquad R_u = 1.01\,\pi_m - s_\odot + \pi_\odot, \qquad 1.01 \cong 1 + \tfrac{1}{85} - \tfrac{1}{594}.$$

Herald and Sinnott write the same rule as $r_u = (0.998340 + h)\,\pi_\mathrm{Moon} - s_\mathrm{Sun} + \pi_\mathrm{Sun}$ with $h = 0.0118$ Earth radii [@lun-herald-sinnott-2014].

Danjon's own paper derives the factor slightly differently. It writes the umbral and penumbral semidiameters as $\rho = p + p' - s$ and $\sigma = p + p' + s$, with $p$ and $p'$ the parallaxes of the Sun and Moon and $s$ the Sun's semidiameter [@lun-danjon-1951]. The penumbral condition is $d < \sigma + s'$, with $s'$ the Moon's semidiameter [@lun-danjon-1951]. In this notation $\rho$ and $\sigma$ are Danjon's, not Meeus's radii in Earth radii. Danjon first argues that the empirical correction should be the same absolute amount for both shadows, equal to 1/50 of the umbral semidiameter, "en moyenne 50″" [@lun-danjon-1951]. He then states the Connaissance des Temps value: an effective atmosphere of 75 km, "soit 1 : 85 du rayon équatorial de la Terre", applied to the lunar parallax, less 1/586 "pour la ramener au rayon moyen de l'ombre", so that "la correction totale est ainsi très voisine de 1 : 100" [@lun-danjon-1951]. On average this enlarges $\rho$ by 1/73 and $\sigma$ by only 1/123 [@lun-danjon-1951]. NASA's 1/594 for the oblateness term is therefore a later value. Danjon printed 1/586.

Danjon's worked case is the eclipse of 1951 February 21, at 21h 29m UT. He takes $d = 5380.5''$, $p = 8.8''$, $p' = 3405.7''$, $s = 971.7''$ and $s' = 927.3''$, so that $\sigma = 4386.2''$ [@lun-danjon-1951]. The 1/50 rule adds 87.7 arcseconds and gives a penumbral eclipse of magnitude 0.011, as the Handbook of the British Astronomical Association (BAA) predicted. The Connaissance des Temps correction of 34.1 arcseconds leaves the lunar limb 32.9 arcseconds outside the penumbra, so no eclipse occurs [@lun-danjon-1951]. NASA's list of penumbral eclipses that exist only under Chauvenet's rule includes this date [@lun-nasa-shadow-page]. This account covers pages 51 and 52 of the paper. Page 53 is not reproduced here.

The note of the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) for the penumbral eclipse of 2023 May 5 shows the rule in current French practice. The note gives the Moon's equatorial parallax as 57 arcminutes 40.11 arcseconds and the Sun's as 8.72 arcseconds. It gives the umbral cone diameter as 85.07 arcminutes and the penumbral cone diameter as 148.51 arcminutes [@lun-imcce-2023-may]. With the Sun's semidiameter taken as 959.63 arcseconds divided by the Earth–Sun distance of 1.0086 au, Danjon's formulas give 85.06 and 148.50 arcminutes. Chauvenet's give 85.39 and 150.10 arcminutes. This reduction is computed here and is not stated in the IMCCE note.

### Herald and Sinnott: a layer above an oblate Earth

Herald and Sinnott reduce each timing to the height of a "notional eclipse-forming layer", the [?lun-nel|NEL], above the oblate Earth [@lun-herald-sinnott-2014]. Their geometry uses the fundamental plane through the Earth's centre perpendicular to the umbral axis. With $R$ the Earth's effective radius in equatorial radii at the tangent point, the half-angle at the vertex of the shadow cone is $f = s_\mathrm{Sun} - R\,\pi_\mathrm{Sun}$. The umbral radius on the fundamental plane is $R/\cos f$, and through a crater at distance $Z_c$ beyond the plane it is [@lun-herald-sinnott-2014]

$$r_u = \frac{R}{\cos f} - Z_c \tan f . \qquad [3]$$

This $f$ is the Earth's umbral vertex angle, the analogue of the corpus's $f_2$ for the Moon's shadow. The $r_u$ of equation [3] is a linear radius in equatorial Earth radii, measured on the plane through the crater. Herald and Sinnott use it only to reduce crater and contact timings. Equation [2] and the recommended rule below give instead an angular $r_u$ in the units of the parallaxes. That angular radius is the $R_u$ that enters $L_2$ and $L_3$. $Z_c$ comes from the Moon's distance $Z_m$ in the Besselian elements and from projecting the crater with the heliocentric libration [@lun-herald-sinnott-2014]. The Earth's apparent radius seen from the Sun at an angle $\theta$ around the umbra is [@lun-herald-sinnott-2014]

$$R = 1 + h - 0.003353\,\sin^2\theta\,\cos^2(\delta_\mathrm{Sun} + f\sin\theta), \qquad [4]$$

where 0.003353 is the Earth's flattening, 1/298.256, and $\delta_\mathrm{Sun}$ is the Sun's declination. The angle $\theta$ is measured "northward (+) or southward (-) from the east-west direction on the sky", by analogy with latitude [@lun-herald-sinnott-2014]. This topic writes the angle $\theta$.

Their recommendation for predicting primary contacts is [@lun-herald-sinnott-2014]

$$r_u = R\,\pi_\mathrm{Moon} - s_\mathrm{Sun} + \pi_\mathrm{Sun}, \qquad h = 0.0136,$$

with $R$ from equation [4], $\theta$ the position angle of the contact point about the umbra, and $f = s_\mathrm{Sun} - R\,\pi_\mathrm{Sun}$. "The calculation requires only a single iteration to generate mutually consistent values of R and θ" [@lun-herald-sinnott-2014]. $R$ and $\theta$ depend on where the Moon meets the umbra, so the iteration is made separately for each umbral contact: U1, U2, U3 and U4 each have their own $\theta$, $R$ and $f$. This reading of the rule is made here from the definition of $\theta$. The value $h = 0.0136$ corresponds to 87 km. The paper gives no penumbral counterpart, because the penumbral contacts are not observed. How EclipseWise forms its penumbral radius under this rule is not stated in the EclipseWise pages cited here.

The paper's reasons for the recommendation are explicit. "The traditional predictions using either the Chauvenet or Danjon approach include the simplification of a spherical Earth having a radius equal to that at 45° latitude. But this simplification can lead to errors of the order of 1 minute of time" [@lun-herald-sinnott-2014]. And the Chauvenet rule "leads to an error that is dependent upon the lunar distance. The Danjon method is clearly preferable in this respect" [@lun-herald-sinnott-2014].

![Chauvenet's 2 per cent rule is equivalent to a layer that thins from about 94 to 90 km as the Moon recedes, while Danjon's factor 1.01 and Herald and Sinnott's $h = 0.0136$ give fixed layers of about 74 and 86.6 km. The observed single-eclipse means of 82.2 to 90.7 km bracket only the last [@lun-herald-sinnott-2014] [@lun-nasa-shadow-page]. Curves computed from the quoted formulas with the Sun at 1 au. Heights are above the 45-degree radius 0.998340. The Herald and Sinnott value is evaluated at $\theta = 45^{\circ}$ with the Sun on the equator. At $\theta = 0^{\circ}$ it is 97.3 km and at $\theta = 90^{\circ}$ it is 75.9 km. These two values are computed here.](img/shadow-rules.svg)

## The measured layer

Herald and Sinnott's dataset holds 22,539 observations, or 26,685 individual timings, at 94 lunar eclipses from 1842 to 2011 [@lun-herald-sinnott-2014]. They base their statistics on 20,678 records of craters and small spots, excluding limb contacts and extended features [@lun-herald-sinnott-2014]. The results are [@lun-herald-sinnott-2014]:

- percentage enlargement: mode 1.7 per cent, median 1.8 per cent, mean 1.88 per cent;
- NEL height: mode 78 km, median 85 km, mean 86.9 ± 0.2 km;
- "As expected, the percentage enlargement depends somewhat on the lunar distance, but the NEL value does not."

The paper finds no cycle with the 11-year solar cycle or with the season, and no long-term trend once a few poorly observed eclipses of 1943 to 1974 are set aside [@lun-herald-sinnott-2014]. It does find real eclipse-to-eclipse variation: 1,164 timings of 1982 July 6 give 90.7 ± 1.2 km and 1,119 timings of 1989 August 17 give 82.2 ± 1.0 km [@lun-herald-sinnott-2014]. Ingresses give a layer 3.5 km higher than egresses on average, which the authors judge "insufficient to support a predictable, systematic difference" between the sunset and sunrise terminators [@lun-herald-sinnott-2014].

On the shape, the NEL heights binned in 10-degree steps of $\theta$ show no trend. "The absence of any such trend demonstrates that the shape of the umbral shadow is fully attributable to the oblateness of the Earth" [@lun-herald-sinnott-2014]. This rejects the extra flattening reported by Kosik, Bouška, Link, Ashbrook and Soulsby [@lun-herald-sinnott-2014].

Earlier determinations agree with the 1.7 to 2.2 per cent range. The Canon tabulates Sky & Telescope crater-timing enlargements of 1.69 and 1.68 per cent for 1972 January 30, 1.79 and 1.61 for 1975 May 24, 2.02 and 2.24 for 1982 July 5 (date as printed), and 1.74 and 1.74 for 1982 December 30, for entrances and exits respectively [@lun-5mcle-tp2009]. It cites Link's 1969 mean of 2.3 per cent from 57 eclipses over 150 years [@lun-5mcle-tp2009] [@lun-link-1969].

## Effect on magnitude, contacts and type

At a mean lunar parallax of 3422.6 arcseconds and the Sun at 1 au, the rules give these angular radii. The values are computed here from the formulas quoted above.

| Rule | $R_u$, arcseconds | $R_p$, arcseconds | Umbral radius minus Danjon, arcseconds |
|---|---|---|---|
| Airless, 45° radius | 2466.1 | not computed | −39.9 |
| Danjon, factor 1.01 | 2506.0 | 4425.3 | 0 |
| Chauvenet, factor 1.02 | 2515.4 | 4473.0 | +9.4 |
| Herald and Sinnott, $\theta = 0^{\circ}$ | 2518.3 | not given | +12.3 |
| Herald and Sinnott, $\theta = 45^{\circ}$ | 2512.6 | not given | +6.6 |
| Herald and Sinnott, $\theta = 90^{\circ}$ | 2506.8 | not given | +0.8 |

The Herald and Sinnott rows assume the Sun on the equator. Dividing by the Moon's diameter, about 1865 arcseconds at this distance, turns a radius difference into a magnitude difference. Chauvenet minus Danjon is then +0.0050 in umbral magnitude and +0.0256 in penumbral magnitude. NASA states "approximately 0.006 and 0.026" [@lun-nasa-shadow-page]. Meeus states "about 0.005 for umbral eclipses, by about 0.026 for penumbral eclipses" [@cat-meeus-1991-aa]. NASA's example is the partial eclipse of 2008 August 16, umbral magnitude 0.813 in the Astronomical Almanac and 0.806 in Meeus and Mucke [@lun-nasa-shadow-page] [@lun-meeus-mucke-1979].

Meeus gives the two rules as alternative constants in Earth radii at the Moon's distance. For the Danjon rule the penumbral radius is $\rho = 1.2848 + u$ and the umbral radius is $\sigma = 0.7403 - u$. For the traditional rule Meeus says to "replace 1.2848 by 1.2985, 0.7403 by 0.7432, 1.5573 by 1.5710, 1.0128 by 1.0157, 0.4678 by 0.4707" [@cat-meeus-1991-aa]. The semiduration of a phase is $\tfrac{60}{n}\sqrt{L^2 - \gamma^2}$ minutes, with $L$ one of 1.5573 + u, 1.0128 − u or 0.4678 − u and $n = 0.5458 + 0.0400\cos M'$ [@cat-meeus-1991-aa]. Differentiating gives the shift of a contact for a change $\Delta L$ in the limiting distance:

$$\Delta t = \frac{L\,\Delta L}{n\sqrt{L^2-\gamma^2}} \ \text{hours}.$$

This derivative is derived here from Meeus's formula. For $\gamma = 0.35$, $u = 0$ and $n = 0.5458$, the Chauvenet minus Danjon shift is about 20 seconds at U1 and U4, about 29 seconds at U2 and U3, and about 93 seconds at P1 and P4. A rule change therefore lengthens or shortens totality by about one minute. A reimplementation of Meeus's method, computed here over the 228 catalogued eclipses of 1951 to 2050, agrees. Switching from the Danjon to the traditional constants raised the mean total-phase duration difference against the NASA catalogue from −0.75 to +0.32 minutes, consistent with that estimate [@cat-meeus-1991-aa] [@lun-5mkle-ascii]. The details of that check are in [Observation, brightness and validation](observation-brightness-and-validation.md).

One kilometre of layer height subtends about 0.54 arcseconds at the mean lunar distance. The Moon moves against the shadow at about 0.52 arcseconds per second of time. A change of 1 km in the layer therefore moves a contact by about 1 second of time, more where the Moon meets the edge obliquely. This rule of thumb is derived here and matches Herald and Sinnott's statement that a 25 to 30 second timing error gives "an uncertainty of about 25 to 30 km in NEL height" [@lun-herald-sinnott-2014].

Near a type boundary the rule decides the type. NASA lists five eclipses from 1501 to 3000 that are total under Chauvenet and partial under Danjon, for example 1540 September 16 at 1.0007 against 0.9947 [@lun-nasa-shadow-page]. It lists partial-to-penumbral cases, for example 1988 March 3 at 0.0028 against −0.0017 and 2042 September 29 at 0.0027 against −0.0031 [@lun-nasa-shadow-page]. Nine penumbral eclipses of 1801 to 2300 in Liu and Fiala's Chauvenet-based canon do not occur at all under Danjon, among them 2016 August 18 at penumbral magnitude 0.0165 [@lun-nasa-shadow-page] [@lun-liu-fiala-1992]. "It is important to note which shadow enlargement convention is used because it is critical in comparing predictions from different sources" [@lun-nasa-shadow-page].

The Herald and Sinnott rule and the Danjon rule can be compared on three total eclipses that both NASA and EclipseWise list. The NASA catalogue uses Danjon with VSOP87 and ELP-2000/82. The EclipseWise pages use Herald and Sinnott with the Jet Propulsion Laboratory (JPL) ephemeris DE430 [@lun-5mcle-tp2009] [@lun-ew-2022nov08] [@lun-ew-2025mar14] [@lun-ew-2025sep07].

| Eclipse | Umbral magnitude, NASA | Umbral magnitude, EclipseWise | Totality, NASA | Totality, EclipseWise |
|---|---|---|---|---|
| 2022 Nov 08 | 1.3589 | 1.36069 | 85.0 min | 85.66 min |
| 2025 Mar 14 | 1.1784 | 1.18038 | 65.4 min | 66.07 min |
| 2025 Sep 07 | 1.3619 | 1.36379 | 82.1 min | 82.69 min |

The EclipseWise values are about 0.002 larger in umbral magnitude and about 0.6 minutes longer in totality [@lun-nasa-le2001] [@lun-ew-2022nov08] [@lun-ew-2025mar14] [@lun-ew-2025sep07]. The ephemerides also differ between the two sources, so the table bounds the combined effect rather than isolating the enlargement rule. Gamma agrees to 0.0001 in all three cases.

## Which implementation uses which rule

| Product or program | Rule | Earth figure | Other constants | Source |
|---|---|---|---|---|
| Astronomical Almanac | Chauvenet, 1.02 | 45° radius, 0.998340 | not stated in the cited sources | [@lun-herald-sinnott-2014] [@lun-es1992] |
| Connaissance des Temps, IMCCE | Danjon, 1.01 since 1951 | 45° radius, flattening 1/297 | IMCCE 2023 shadow diameters match Danjon | [@lun-5mcle-tp2009] [@lun-imcce-2023-may] |
| Meeus, *Astronomical Algorithms* | Danjon, with 1/50 constants given | circular | radii in Earth radii | [@cat-meeus-1991-aa] |
| NASA Five Millennium Canon and Catalogue (2009) | Danjon, 1.01 | 45° radius | VSOP87, ELP-2000/82, $k = 0.2724880$ | [@lun-5mcle-tp2009] |
| EclipseWise prime pages (2022) | Herald and Sinnott | oblate, layer 87 km | JPL DE430, "Shadow Enlargement: 1.000" | [@lun-ew-2025mar14] [@lun-ew-leshadow2] |
| NASA crater-timing page (2009) | Danjon "1/85", with oblateness | oblate | not stated | [@lun-nasa-crater-page] |
| Skyfield `eclipselib` | Danjon, `pi_1 = 1.01 * pi_m` | equatorial radius `ERAD` | Sun 696,340 km, Moon 1,737.1 km | [@sw-skyfield-eclipselib] |
| Stellarium | Chauvenet by default, Danjon optional | 45° radius in the Chauvenet branch | Moon and Sun equatorial radii from its data | [@lun-stellarium-solarsystem] |
| Astronomy Engine | sphere 6371 km plus 88 km | spherical | Moon 1737.4 km | [@sw-astronomy-engine-c] |
| Occult 4 | not documented in the cited sources | not documented | not documented | [@sw-occult4] |

Three details matter when comparing these. Skyfield's comment says "Use Danjon's method", and it applies the factor 1.01 to the parallax computed from the equatorial radius without the arcsine, as its comment notes [@sw-skyfield-eclipselib]. Stellarium reads the setting `astro/shadow_enlargement_danjon` with a default of `false`, and its Danjon branch uses `1+1./85.-1./594.` [@lun-stellarium-solarsystem]. The function carries the comment "The application of this shadow enlargement is not according to the books, but looks close enough for now", although the radii it returns follow the printed formulas [@lun-stellarium-solarsystem]. Astronomy Engine's comment for the 88 km layer cites the NASA shadow page, but 6371 plus 88 km on a sphere is closer to Herald and Sinnott's 87 km than to Danjon's 75 km [@sw-astronomy-engine-c].

## Sources compared

| Source | Rule given | Constants | What it adds |
|---|---|---|---|
| Chauvenet 1863 [@bes-chauvenet-1863] | 51/50 on the umbral radius | Lambert 1/40, Mayer 1/60, Beer and Mädler 1/50 | The origin of the 2 per cent rule |
| Explanatory Supplement 1961, 1992 [@lun-es1961] [@lun-es1992] | Chauvenet with 0.998333 or 0.998340 | $R_p$, $R_u$ derivation | The almanac formulation and type conditions |
| NASA shadow page and Canon [@lun-nasa-shadow-page] [@lun-5mcle-tp2009] | Chauvenet and Danjon | 1.01 = 1 + 1/85 − 1/594 | Magnitude differences and type-change tables 1501 to 3000 |
| Meeus 1991 [@cat-meeus-1991-aa] | Danjon, with 1/50 alternatives | ρ, σ, semiduration constants | Closed forms in Earth radii, umbra flattening 1/214 |
| Herald and Sinnott 2014 [@lun-herald-sinnott-2014] | Layer above oblate Earth | $h = 0.0136$, flattening 0.003353 | 22,539 timings, NEL statistics, rejection of extra flattening |
| EclipseWise [@lun-ew-2025mar14] [@lun-ew-leshadow2] | Herald and Sinnott | DE430 | Current predictions under the new rule |
| IMCCE 2023 note [@lun-imcce-2023-may] | Danjon by reduction | shadow cone diameters | Evidence of current French practice |
| Skyfield, Stellarium, Astronomy Engine code [@sw-skyfield-eclipselib] [@lun-stellarium-solarsystem] [@sw-astronomy-engine-c] | Danjon, Chauvenet default, sphere plus 88 km | as in the table above | What open-source users actually get |

## What a developer should do

Implement the shadow radii as a pluggable rule with three options: Chauvenet, Danjon and Herald and Sinnott. Report the rule with every result, because the rule alone moves umbral magnitudes by 0.005, penumbral magnitudes by 0.026 and penumbral contacts by about 1.5 minutes. Use Herald and Sinnott with $h = 0.0136$ as the default for new predictions of umbral contacts, and solve for $R$ and $\theta$ at each contact with the single iteration the paper describes. For comparisons with the NASA Five Millennium Canon or with Meeus, switch to Danjon with the factor 1.01. For comparisons with the Astronomical Almanac, use Chauvenet with 0.998340. Read Herald and Sinnott 2014 in full first, then the NASA shadow page. Use VizieR VI/140 to test a crater-timing implementation, as described in [Observation, brightness and validation](observation-brightness-and-validation.md).

## What this changes

A lunar-eclipse pipeline needs one input that solar eclipses do not: an atmospheric enlargement model. It plays the role that the lunar radius and the limb profile play for solar contacts. The Besselian stage can stay as it is, because the rule enters only through the radii $L_1$, $L_2$ and $L_3$. The output schema must carry the rule name and the layer height.

## Open questions

- Obtain page 53 of Danjon 1951, L'Astronomie 65, for the rest of his argument [@lun-danjon-1951].
- Obtain the current Astronomical Almanac section A on lunar eclipses, or the USNO lunar eclipse data service page `https://aa.usno.navy.mil/data/LunarEclipses`, to establish whether the Almanac still uses Chauvenet's 1.02 after 2014.
- Obtain EclipseWise's PDF "21CCLE Shadows" from the *21st Century Canon of Lunar Eclipses* to learn how the penumbral radius is formed under the Herald and Sinnott rule and what "Shadow Enlargement: 1.000" means [@lun-ew-leshadow2].
- Obtain Occult 4's lunar eclipse help topic or code to establish its enlargement rule [@sw-occult4].
- Obtain the 2013 Explanatory Supplement, section 11.2.3, which Skyfield cites, to see whether the third edition changed the 1992 rule [@earth-es2013].
- Obtain Soulsby 1990, JBAA 100, 293 to 305, and Link 1969 to compare their flattening and enlargement methods with Herald and Sinnott's NEL reduction [@lun-soulsby-1990] [@lun-link-1969].
