---
title: Planets, star catalogues and the reduction of occultations
seo_title: Lunar Occultations of Planets and Star Catalogues
description: How planet occultations, star catalogues, double stars and diffraction enter occultation work, and how timings are reduced to residuals and ΔT.
order: 3
status: working
updated: 2026-10-17
tags: [occultations, planets, catalogues, gaia, delta-t, reduction, error-budget]
---

::: summary
- **A planet is an eclipse, not a star.** Chauvenet reduces a lunar occultation of a planet to the eclipse of one disc by another, with the planet's radius replaced by the perpendicular from its centre to the common tangent. That perpendicular depends on the planet's phase and oblateness. For Uranus, Neptune and asteroids he times the centre with the relative parallax [@bes-chauvenet-1863].
- **The star catalogue went from the Zodiacal Catalogue (ZC) to XZ to Gaia.** Robertson's 1940 Zodiacal Catalogue of 3539 stars set the prediction list for decades. The XZ catalogue began at the US Naval Observatory (USNO) in 1977 with 32,221 stars, and XZ80Q has 244,437 to magnitude 12.0. Most stars in the 2022 archive reduction use Gaia EDR3 positions [@occ-es1961] [@occ-vizier-i291] [@occ-vizier-vi132c].
- **A reduction yields one number per timing.** It is the residual $\Delta\sigma$, the computed distance of the star from the limb at the observed time, in arcseconds. Its derivatives with respect to the Moon's longitude, latitude and parallax drive the least-squares analyses [@occ-es1961] [@occ-morrison-1979].
- **Occultations measured ΔT from 1623 to the atomic era.** Stephenson, Morrison and Hohenkerk recover ΔT for each of 478,843 timings as the assumed value minus $\Delta\sigma$ divided by its rate. They keep only rates above 0.2 arcseconds per second [@cat-stephenson-2016].
- **Visual timings carry a personal equation of 0.3 to 1 second.** It depends on lunar phase and star brightness. Morrison and Appleby's expressions are still the archive default [@occ-morrison-appleby-1981-pe] [@occ-vizier-vi132c].
- **The error budget has shrunk from 0.5 to about 0.04 arcseconds.** Visual residuals of 1943 to 1974 had a spread of 0.49 arcseconds. With Gaia DR1 positions in XZ80, the typical residual fell below 0.04 arcseconds, and most predictions agree with video timings to 0.3 s [@occ-morrison-1979] [@limb-occult-accuracy-2016].
- **Light curves give star diameters.** Fresnel fringes from the limb sweep past at about 0.75 to 0.9 m per millisecond. Fitting them resolves stars of a few milliarcseconds and binaries of a few milliarcseconds [@occ-nather-evans-1970] [@occ-richichi-2010].
:::

**The question.** What changes when the occulted body is a planet? Which star catalogues and positions occultation work has used, and how are double stars and stellar diameters handled? How is a timing reduced to a residual, and how were residuals turned into lunar-ephemeris corrections and ΔT? What is the error budget of a prediction today? The geometry of the prediction is in [Besselian elements for lunar occultations](besselian-elements-for-occultations.md) and the limb in [Grazes and the lunar limb](grazes-and-limb.md).

## Occultations of planets by the Moon

### Chauvenet's treatment

Chauvenet opens the subject with the shortcut and its limits. "If the disc of a planet were always a circle, and fully illuminated, its occultation by the moon might be computed by the general method used for solar eclipses by merely substituting the parallax and semidiameter of the planet for those of the sun" [@bes-chauvenet-1863]. With the telescopes and chronographs of his day, however, "it is possible to observe the instants of contact with the planet's limb to such a degree of accuracy that it appears to be worth while to take into account the true figure of the visible illuminated portion of the planet" [@bes-chauvenet-1863]. He models the planet as a spheroid. Fully lit, its outline is an ellipse. Partly lit, the outline is "composed of two ellipses, of which one is the boundary of the spheroid and the other is the limit of illumination" [@bes-chauvenet-1863].

The contact computation then reduces to the eclipse case. "Since the apparent semidiameter of any of the planets is never greater than 31″", the short arc of the Moon's limb at the contact point coincides with the common tangent of the two bodies [@bes-chauvenet-1863]. "If, then, the planet were a spherical body with the radius OD, the observed time of contact would not be changed. We may, therefore, reduce the occultation of a planet to the general case of eclipse of one spherical body by another, by substituting the perpendicular OD for the radius of the disc of the eclipsed body" [@bes-chauvenet-1863]. Here $O$ is the planet's apparent centre and $D$ the foot of the perpendicular on the common tangent. Chauvenet calls this perpendicular $s''$ [@bes-chauvenet-1863]. This site writes it $s_\perp$, because $s''$ is a semidiameter in arcseconds elsewhere in this topic.

### The perpendicular and the defective limb

Chauvenet works in rectangular axes through the planet's apparent centre. The axis of $v$ points to the projected pole of the planet's equator, at position angle $p$ reckoned eastward from the declination circle, and the axis of $u$ is perpendicular to it [@bes-chauvenet-1863]. Let $s$ be "the greatest apparent semidiameter of the planet" and $c = \sqrt{1 - e^2\cos^2\beta}$, with $e$ "the eccentricity of the planet's meridians" and $\beta$ the latitude of the line of sight referred to the planet's equator [@bes-chauvenet-1863]. The outline is then the ellipse of his equation (611), and the limit of illumination seen from the Earth is the ellipse of equation (616) [@bes-chauvenet-1863]:

$$
s^2 = u^2 + \frac{v^2}{c^2},\qquad
s^2 = \left(u\cos w - v\,\frac{\sin w}{c}\right)^2 + \left(u\sin w + v\,\frac{\cos w}{c}\right)^2\sec^2 V .
$$

Here $V$ is "very nearly the angular distance between the sun and the earth as seen from the planet", and $w$ is an angle of the spherical triangle formed by the planet's pole, the Earth and the Sun [@bes-chauvenet-1863]. Chauvenet states that "in all practical cases we may take $w = 90^{\circ}$" [@bes-chauvenet-1863]. He finds $V$ from $\sin V = (R/R')\sin E_\mathrm{p}$, with $R$ and $R'$ the heliocentric distances of the Earth and the planet and $E_\mathrm{p}$ the arc between the geocentric places of the Sun and the planet [@bes-chauvenet-1863]. Chauvenet writes $\gamma$ for $E_\mathrm{p}$. The geocentric semidiameter is $s = s_{\mathrm{p},0}/r'$, with $r'$ the geocentric distance in astronomical units and $s_{\mathrm{p},0}$ the semidiameter at unit distance, which Chauvenet writes $s_0$ [@bes-chauvenet-1863].

Let $\vartheta$ be the angle from the axis of $v$ to the perpendicular. Then $\vartheta = P_\mathrm{M} - p$, where $P_\mathrm{M}$ is the position angle of the Moon's centre seen from the planet's centre [@bes-chauvenet-1863]. Chauvenet writes $Q$ for $P_\mathrm{M}$ and takes it from the eclipse solution as $N + \psi$, with $N$ and $\psi$ his eclipse auxiliaries [@bes-chauvenet-1863]. With $w = 90^{\circ}$ his equations (628) give the perpendicular [@bes-chauvenet-1863]:

$$
\tan\vartheta' = \frac{\tan\vartheta}{c},\qquad
\sin\kappa = \sin\vartheta'\sin V,\qquad
s_\perp = \frac{s\sin\vartheta\cos\kappa}{\sin\vartheta'} .
$$

Chauvenet writes $\chi$ for $\kappa$. The general forms, for any $w$, are $c'\sin\vartheta' = \sin\vartheta/c$, $c'\cos\vartheta' = \cos\vartheta$, $\sin\kappa = \cos(\vartheta' - w)\sin V$ and $s_\perp = s\,cc'\cos\kappa$, his equations (626) and (627) [@bes-chauvenet-1863]. Three special cases follow [@bes-chauvenet-1863]:

- At a cusp of Venus or Mercury, $s_\perp = s\cos\vartheta$, "for the axis of $v$ coincides with the line joining the cusps", and $V$ is not needed.
- On the full limb, put $V = 0$, so $s_\perp = s\sin\vartheta/\sin\vartheta'$.
- On the full limb of a spherical planet, Venus, Mercury or Mars, $c = 1$ and $s_\perp = s$.

The value of $s_\perp$ "is to be substituted ... for the apparent semidiameter of the eclipsed body" in the eclipse formulas, with $\sin H = r'\sin s_\perp$ for the semidiameter $H$ at unit distance [@bes-chauvenet-1863]. Because $\vartheta$ depends on the contact, the solution is iterative. The first approximation takes $L = \pm k$, and "the second approximation will mostly be final". Only for a very elliptical outline, such as Saturn's ring near the Moon's northern or southern limb, may a third pass be needed [@bes-chauvenet-1863]. The symbol $H$ here is Chauvenet's and not the Greenwich hour angle of the occultation elements.

The sign rule settles which limb a contact is on. Chauvenet writes that "a point is to be regarded as on the east limb for values of $\vartheta$ between 0° and 180°, and on the west limb for values of $\vartheta$ between 180° and 360°", and "the east or the west limb is defective according as $V$ is between 0° and 180° or between 180° and 360°" [@bes-chauvenet-1863]. With $\sin\kappa = \sin\vartheta'\sin V$ this reduces to a single test: "the observed point is on the defective limb when $\sin\chi$ is positive, and on the full limb when $\sin\chi$ is negative" [@bes-chauvenet-1863]. A crescent planet has $V$ between 90 and 270 degrees, and a gibbous planet has $V$ beyond 270 or below 90 degrees [@bes-chauvenet-1863].

Chauvenet gives the planet-specific constants of his time. For Jupiter he takes $c$ constant with $\log c = 9.9672$, from Struve's ratio 0.92723, and $V = A' - \lambda'$, the heliocentric minus the geocentric longitude [@bes-chauvenet-1863]. For Saturn's ring he puts $e = 1$, so $c = \sin\beta$. Mars, Venus and Mercury are treated as spheres with $c = 1$, and the pole is chosen so that $\beta = 0$ [@bes-chauvenet-1863]. A modern implementation takes $p$, $\beta$, the radii and $V$ from a current physical ephemeris instead.

For the faint planets the centre is timed. "In the cases of the planets Neptune, Uranus, and the asteroids, the occultation of their centres will be observed, and it will be most convenient to compute by the method for a fixed star, only substituting for it the difference of the moon's and planet's horizontal parallaxes - that is, the [?occ-relative-parallax|relative parallax] - in the formulae for $x$ and $y$" [@bes-chauvenet-1863]. "This artifice of using the relative parallax may also be used with advantage for Jupiter and Saturn" [@bes-chauvenet-1863]. His worked example is a set of occultations of Saturn's ring, timed by Kane in north-west Greenland on 1853 December 12 as the contact "of last point of ring" at immersion and emersion [@bes-chauvenet-1863].

### The four contacts

For a planet of finite disc each phase has two contacts, as in a partial solar eclipse with the planet as the eclipsed body. Numbering them follows the eclipse convention in [Contact times and magnitude](../04-local-circumstances/contact-times-and-magnitude.md). First contact is the Moon's limb touching the planet's leading limb. Second contact is the planet fully hidden. Third contact is the first reappearance of the planet's limb. Fourth contact is the planet fully clear. This mapping is derived from Chauvenet's reduction to the eclipse case. None of the sources cited in this topic prints it with these labels [@bes-chauvenet-1863]. Second and third contacts are the internal tangencies of the Moon's limb with the planet's outline. With a crescent planet, a contact on the defective limb uses $s_\perp$ from the terminator ellipse [@bes-chauvenet-1863]. The interval between first and second contact is the planet's projected diameter divided by the limb rate. For a 40 arcsecond disc and 0.4 arcseconds per second that is about 100 seconds of time. This is arithmetic from the rates in [Besselian elements for lunar occultations](besselian-elements-for-occultations.md), not a published figure.

### Almanac and modern practice

HM Nautical Almanac Office (HMNAO) applied "the same limitations ... on the predictions of occultations of planets and minor planets as are used for stars". The planet's position was computed at the two integral hours and its motion was allowed for in the elements [@occ-es1961]. The 1992 Supplement says the map method for stars "may be applied for predicting the areas of visibility of occultations of planets by the Moon" [@occ-es1992]. Its section 9.42, and section F of 1961, treat the different case of stars occulted by planets. There an occultation is possible somewhere on Earth when $|\delta - \delta_s| < (\pi + s)/|\sin p|$ at conjunction in right ascension. Here $\pi$ and $s$ are the planet's horizontal parallax and semidiameter and $p$ the position angle of its motion [@occ-es1992] [@occ-es1961].

The Royal Astronomical Society of Canada's Observer's Handbook (RASC Handbook) lists lunar occultations of planets with the stars. For dark-side events of Jupiter they also give Io and Ganymede, while Europa and Callisto fall below the magnitude 6.0 limit [@limb-dunham-rasc-2026]. The archive reduces 710 planet events with positions from the JPL ephemeris DE440, and 138 events of planetary satellites and asteroids with positions from JPL Horizons [@occ-vizier-vi132c]. When it identifies an unmatched timing it checks "the major planets, Plus Jupiter satellites I-IV, and Saturn VI". For a major planet it assumes that the reported time is "the 'interior contact' between the planet disk and the lunar limb" [@occ-vizier-vi132c]. That is second or third contact in the numbering above.

Satellites and asteroids are point targets for this purpose. Chauvenet's relative-parallax method treats them as stars: compute $x$ and $y$ with the difference of the Moon's and the body's horizontal parallaxes, with "the other formulae remaining unchanged" [@bes-chauvenet-1863]. Chauvenet names Neptune, Uranus and the asteroids. Applying the same method to the Galilean satellites and to Titan is an inference here, because a satellite's disc is not resolved in the timing. The body's position comes from its own ephemeris, which in the archive is JPL Horizons [@occ-vizier-vi132c].

Occult computes these events. Its published pages do not document its treatment of phase, oblateness and the terminator [@occ-occult4-page] [@bes-occult-tutorial]. The Occult tutorial notes that lunar occultations of planets "are not frequent and the circumstances are usually already posted to an IOTA website" [@bes-occult-tutorial]. IOTA is the International Occultation Timing Association. Planet occultations also enter ΔT. The 1992 Supplement cites Hilton et al. (1989), who derived ΔT from 58 Chinese records of occultations of planets by the Moon between 68 BC and AD 575 [@occ-es1992]. Stephenson, Morrison and Hohenkerk include a lunar occultation of Jupiter in their telescopic series [@cat-stephenson-2016].

## Star catalogues and positions

### Robertson's Zodiacal Catalogue

The 1961 Supplement explains why the catalogue mattered. Brown's 1919 tables gave "a firm basis for the comparison of observation with theory. But, until the availability in 1940 of the Catalog of 3539 Zodiacal Stars for the Equinox 1950.0, the errors in the star positions placed a severe limitation on the accuracy obtainable" [@occ-es1961] [@occ-robertson-1940]. HMNAO confined predictions to "magnitude 7.5 and brighter" stars of the [?occ-zc|Zodiacal Catalogue] [@occ-es1961]. Morrison's 1943 to 1974 reduction computed apparent places "from their catalogue places and proper motions given in the ZC", adjusted to the FK4 system [@occ-morrison-1979]. Morrison and Appleby restricted their personal-equation analysis to stars "with positions in Robertson's (1940) catalogue", which "is nearly complete to magnitude 7.5" [@occ-morrison-appleby-1981-pe]. Isao Sato republished the ZC in 1986 for epoch J2000 with added double-star data. ZC numbers still name the stars in the RASC tables [@limb-dunham-rasc-2026].

### The XZ catalogue

The [?occ-xz-catalogue|XZ catalogue] "was created at the U.S. Naval Observatory in 1977 by Richard Schmidt and Tom Van Flandern, primarily for the purpose of generating predictions of lunar occultations, and for analyzing timings of these events" [@occ-vizier-i291]. "It was designed to include all stars within 6d 40' of the ecliptic (the 'Zodiac'), which is as far as the Moon's limb can ever get as seen from anywhere on the Earth's surface, leaving some margin for stellar proper motions and change in the obliquity of the ecliptic over the course of three centuries" [@occ-vizier-i291]. The original had 32,221 entries. XZ80N was published by Dunham and others in 1995 (VizieR I/201), XZ80P by Mitsuru Soma, and Herald's XZ80Q in 2003 [@occ-vizier-i291]. XZ80Q has 244,437 records and is "complete over the Zodiac for stars down to visual magnitude 12.0" [@occ-vizier-i291]. Each record carries an ICRS position at epoch J2000 with proper motions in seconds of time per century and arcseconds per century. It also carries the standard errors at the source epoch, the source epoch, parallax, radial velocity, a double-star code and cross-identifications including the ZC number [@occ-vizier-i291].

In 2016 Herald updated XZ80 "to use Gaia DR1 position when available", so that "over 80% of the stars in XZ80 are now based on Gaia". As a result "the typical residual for a lunar occultation event is now smaller than 0.04"" [@limb-occult-accuracy-2016]. The RASC handbook says the ZC and XZ80Q were "updated in 2018 by D. Herald" [@limb-dunham-rasc-2026]. Occult 2026 offers "a downloadable subset of the Gaia EDR3 catalogue to mag 16.0", 2.64 GB, and accepts UCAC4 [@occ-occult4-page]. Gaia DR3 "neither contains new astrometry nor new photometric calibrations", so EDR3 and DR3 share the same astrometry [@occ-gaia-dr3-overview]. For the 2022 archive reduction, positions came from Gaia EDR3 for 455,015 records, Hipparcos 2 for 20,577, the UBAD database for 8498, Gaia TGAS for 305 and XZ80Q for 8014 [@occ-vizier-vi132c]. The older Lunar Occultation Workbench (LOW) used the Guide Star Catalog (GSC) 1.1, with "over 476,000 stars ... in the Zodiacal region" in its professional edition [@occ-iota-manual-2007].

### Propagating Gaia positions to the event date

Gaia DR3 astrometry, including EDR3, has reference epoch 2016.0. Its positional uncertainties are 0.01 to 0.02 milliarcseconds for $G < 15$ and 0.05 milliarcseconds at $G = 17$. Its proper motion uncertainties are 0.02 to 0.03 milliarcseconds per year and 0.07 milliarcseconds per year respectively [@occ-gaia-dr3-overview]. Moving a star from 2016.0 to the event, [?occ-epoch-propagation|epoch propagation], uses the Gaia documentation's model of "uniform rectilinear motion with respect to the solar-system barycentre". With $t = T - T_0$, unit direction $\mathbf{r}_0$, proper motion vector $\boldsymbol{\mu}_0$ and radial proper motion $\mu_{r0}$ [@occ-gaia-dr3-propagation]:

$$
f = \left[1 + 2\mu_{r0}t + (\mu_0^2 + \mu_{r0}^2)t^2\right]^{-1/2},\qquad
\mathbf{u} = \left[\mathbf{r}_0(1 + \mu_{r0}t) + \boldsymbol{\mu}_0 t\right]f,
$$
$$
\varpi = \varpi_0 f,\qquad
\boldsymbol{\mu} = \left[\boldsymbol{\mu}_0(1 + \mu_{r0}t) - \mathbf{r}_0\mu_0^2 t\right]f^3,\qquad
\mu_r = \left[\mu_{r0} + (\mu_0^2 + \mu_{r0}^2)t\right]f^2 .
$$

Here $\mu_{r0} = v_r\varpi_0/A_V$ with $A_V = 4.740470464$ km yr s⁻¹, and $\mu_{\alpha*} = \mathbf{p}'\boldsymbol{\mu}$ and $\mu_\delta = \mathbf{q}'\boldsymbol{\mu}$ recover the components [@occ-gaia-dr3-propagation]. The factor $f$ is the documentation's symbol and is unrelated to the $f$ of the occultation station reduction. "The radial velocity is crucial for the rigorous propagation." Without it the documentation sets $v_{r0} = 0$ with a large uncertainty, so that "the unknown perspective acceleration is accounted for in the uncertainty of the propagated astrometric parameters" [@occ-gaia-dr3-propagation]. The propagated barycentric direction then goes through the usual apparent-place chain of aberration, light deflection, precession and nutation, as for any star. At 0.07 milliarcseconds per year, ten years from epoch adds 0.7 milliarcseconds. That is far below the 0.01 arcsecond limb accuracy, so a correctly propagated Gaia star is no longer a significant term for single stars. This comparison is arithmetic on the cited figures.

### Double stars

Double stars are the main source of bad residuals once positions are good. XZ80Q flags them with codes C, c, D, d, W and w for separations under 1 arcsecond, under 10 arcseconds and over 10 arcseconds. The case letter says whether the companion has its own XZ entry, and a separate file holds the orbital and measured details [@occ-vizier-i291]. The RASC Handbook's double-star table draws on DSFILE, compiled by Stockbauer, Bulder, Soma, Herald and Dunham. Its codes distinguish visual doubles, spectroscopic binaries and occultation-only doubles, and the separation and position angle are computed for the event date "from orbital elements when available" [@limb-dunham-rasc-2026]. The archive records a Washington Double Star (WDS) component identifier for new observations, so that the reduction can take the component's offset from the catalogue position [@occ-vizier-vi132c].

One occultation measures one component of the separation. Nather and Evans explain: "If a single occultation of a double star is obtained, the 'vector separation' of the pair is measured", which is "the minimum separation between two stars ... in the direction of fringe passage" [@occ-nather-evans-1970]. A second event at another position angle fixes the pair [@occ-nather-evans-1970]. This [?occ-vector-separation|vector separation] is what video lunar occultations still contribute to double-star catalogues [@limb-occult-accuracy-2016]. Visual reports are unreliable, since "about 80% of double star discoveries reported from visual observations show no evidence of being double" [@occ-vizier-vi132c].

## Star diameters from light curves

The diffraction pattern was noticed early. MacMahon proposed in 1909 that the time of disappearance measured a star's diameter. Eddington replied that diffraction at the limb would limit a point source to about eight times MacMahon's 1/500 second, and both "indicated that the critical size of an irregularity would be about 42 ft, the size of the first Fresnel zone at the lunar distance" [@occ-nather-evans-1970]. Williams showed in 1939 that for diameters of about 0.001 to 0.010 arcseconds "the shape of the diffraction pattern is modified in a way that can be interpreted directly in terms of stellar diameter" [@occ-nather-evans-1970].

The time scale follows from the Moon's motion. "The moon moves at a rate of about 0.5 arc sec per sec against the stellar background as seen from the center of the Earth; this results in a fringe passage rate of about 0.9 km per sec (0.9 m/ms) for a star occulted at the leading edge of the moon's disk" [@occ-nather-evans-1970]. Away from the leading edge, the effective time of fringe passage "will be lengthened by the factor sec θ", with θ the angle between the motion and the radius to the star. This is the same geometry as $kn\cos\psi$. Earth rotation can reduce the apparent rate by about 50 per cent for an equatorial observer with the Moon near the zenith [@occ-nather-evans-1970]. Richichi and colleagues give a typical speed "of order ≈0.75 m/ms" at the telescope [@occ-richichi-2010]. They note that above "about 20 to 40 milliarcseconds (mas) at near-infrared wavelengths, the diffraction fringes are completely smeared". Their Very Large Telescope (VLT) programme set upper limits "mostly in the 1 to 5 mas range" [@occ-richichi-2010]. The [?occ-fresnel-pattern|occultation diffraction pattern] for a resolved disc in a broad band is modelled "by the convolution of several point-like monochromatic patterns" [@occ-richichi-2010].

The limb is part of this measurement. Nather and Evans in 1970 called the limb corrections then in use "the major source of error in making use of occultation timings, limiting the accuracy of any one determination to about 0.1 sec of time", against a photoelectric timing precision of 0.001 to 0.002 s [@occ-nather-evans-1970]. The light-curve archive, VizieR B/occ, now holds video light curves for almost all coordinated observations. The topocentric lunar motion is 0.3 to 0.4 arcseconds per second, and the limb moves normal to the star at 0.2 to 0.4 arcseconds per second. Video therefore resolves "about 0.01" to 0.02" at frame rate, or 0.005" to 0.01" at field rate" [@occ-vizier-bocc]. The Lunar Orbiter Laser Altimeter (LOLA) dataset "allows the slope of the lunar limb to be reliably determined over circumferential distances of less than 0.2" in the sky plane", so the local limb slope can be fixed rather than fitted [@occ-vizier-bocc].

## Reducing a timing to a residual

### The HMNAO method

The 1961 Supplement reduces each observation to "the excess of the apparent distance of the star from the centre of the Moon over the adopted apparent semi-diameter of the Moon, together with the position angle of the star measured from the direction of the Moon's motion" [@occ-es1961]. The unit is the Moon's radius, "as a legacy from the period of 'hand' calculation", with $k = 0.2724953$ (0.2725026 from 1968) [@occ-es1961]. The observer's projection is

$$
\xi = \frac{\rho\cos\varphi'\sin h}{k},\qquad
\eta = \frac{\rho\sin\varphi'\cos\delta_* - \rho\cos\varphi'\sin\delta_*\cos h}{k},\qquad
h = \text{GST}_{0^\mathrm{h}} + t_s - \alpha_* - \lambda,
$$

with $\lambda$ positive west [@occ-es1961]. The Moon's coordinates are the formulas for $x$ and $y$ divided by $k\sin\pi_\mathrm{m}$, entered at the UT of observation plus "the latest approximation to ΔT" [@occ-es1961]. The [?occ-residual|residual] is then

$$
\Delta\sigma = s\left\{\left[(x-\xi)^2 + (y-\eta)^2\right]^{1/2} - 1\right\},
$$

with $s$ the Moon's geocentric semidiameter, so $\Delta\sigma$ is reduced to the geocentric distance [@occ-es1961]. The position angle $\chi$ from north follows from $\tan\chi = -(x-\xi)/-(y-\eta)$. The angle $p - \chi$ from the direction of motion follows with $\cot p = y'/x'$ [@occ-es1961]. The Supplement's $p$ is the direction of relative motion, written $N$ elsewhere in this topic. The limb correction from [Grazes and the lunar limb](grazes-and-limb.md) is subtracted from $\Delta\sigma$ [@occ-es1961]. The annual solutions used an equation of condition in $\delta L \cos(p-\chi)$ and $\delta B \sin(p-\chi)$, the errors in the Moon's orbital longitude and latitude [@occ-es1961]. This note does not reproduce its right-hand side. "If reductions were done using the improved lunar ephemeris, $\delta L$ in this equation would be replaced by $\{0.549\,\delta(\Delta T) + \delta L\}$" [@occ-es1961]. The factor 0.549 is the Moon's mean motion in arcseconds per second of time, which ties an error in ΔT to an apparent error in longitude.

### Morrison's analysis of 1943 to 1974

Morrison reduced 62,000 timings against the lunar ephemeris $j = 2$, Brown's theory with ephemeris time and the IAU 1964 constants [@occ-morrison-1979]. He interpolated the ephemeris to dynamical time with $\mathrm{TD} = \mathrm{UT} + \Delta T$. Before 1955 July 1 he took ΔT from a linear approximation. After that date he used $\Delta T = (\mathrm{TAI} - \mathrm{UT1}) + 32.184$ s [@occ-morrison-1979]. The geocentric semidiameter was $s_{\mathrm{m},0} = 0.0799 + 0.272453\,\pi_0$ arcseconds, corresponding to 932.58 arcseconds at mean distance. Morrison's $s_0$ is written $s_{\mathrm{m},0}$ here, because $s_0$ is the solar semidiameter at 1 au on this site. It was scaled to the topocentric distance [@occ-morrison-1979]. He defined the residual "in the sense Observed - Computed" as $O - C = -\Delta\sigma$, because the observed separation is zero [@occ-morrison-1979]. The partial derivatives he used are

$$
\frac{\partial\sigma}{\partial\lambda} = -\sin P_\mathrm{ecl},\quad
\frac{\partial\sigma}{\partial\beta} = -\cos P_\mathrm{ecl},\quad
\frac{\partial\sigma}{\partial\pi} = -0.2725,\quad
\frac{\partial\sigma}{\partial\alpha'} = +\sin P,\quad
\frac{\partial\sigma}{\partial\delta'} = +\cos P,
$$

with $\lambda$ and $\beta$ the Moon's ecliptic longitude and latitude, $\alpha'$ and $\delta'$ the star's coordinates, $P$ the position angle from the north of the equator, and $P_\mathrm{ecl} = P + V$ the position angle from the ecliptic pole [@occ-morrison-1979]. Morrison writes $N$ for $P_\mathrm{ecl}$. It is renamed here because $N$ is the direction of motion in this topic. His derivative of $\sigma$ with respect to time was computed numerically [@occ-morrison-1979].

His refraction treatment raises the observer's geocentric radius to compensate refraction at low altitude. The change is 30 m at 15 degrees altitude. With $\Delta\alpha$ and $\Delta\delta$ the parallactic displacements, the residual changes by

$$
\delta\sigma = \frac{\delta h}{h}\,(\Delta\alpha\sin P + \Delta\delta\cos P),
$$

which is 0.02 arcseconds at 15 degrees and about 0.9 arcseconds at the horizon [@occ-morrison-1979]. The archive applies the same approach below 30 degrees, from Section 2E of the 1969 Explanatory Supplement [@occ-vizier-vi132c].

The weights combine four error sources [@occ-morrison-1979]:

$$
W = \frac{f_\mathrm{P}\,(0.47)^2}{\epsilon_t^2 + \epsilon_*^2 + \epsilon_\mathrm{W}^2 + (0.16)^2},
$$

where $\epsilon_t$ is the timing error converted to arcseconds and $\epsilon_*$ the catalogue error from the ZC. $\epsilon_\mathrm{W}$ is the Watts chart error of 0.2 or 0.5 arcseconds, and 0.16 arcseconds is the adopted ephemeris error. $f_\mathrm{P} = 0.083$ for the Pleiades, to stop their 12 stars per square degree dominating, and 1 otherwise. The residuals of 56,000 observations followed "a normal frequency curve with zero mean and standard deviation of 0".49". Rejecting those above 1.3 arcseconds removed about 10 per cent rather than the expected 1 per cent. Morrison ascribed the excess to "mistakes made by observers in identifying or recording the correct second" [@occ-morrison-1979].

The results were a correction to the Moon's mean longitude, in arcseconds with $T$ in Julian centuries from 1900 [@occ-morrison-1979],

$$
\delta L = -0.806 - 0.411\,(T - 0.77) - 1.78\,(T - 0.77)^2,
$$

and a dynamical time scale before 1955.5 of

$$
\mathrm{TD} = \mathrm{UT} + 31.24 + 0.331\,(Y - 1955.5) - 0.009\,(Y - 1955.5)^2 \ \mathrm{s},
$$

with $Y$ the date in years [@occ-morrison-1979]. He adopted $-13$ arcseconds $T^2$ for the tidal term in mean longitude. He found "no clear evidence ... for any divergence between the dynamical and atomic time-scales", and quasi-periodic residuals of 0.2 arcseconds that he ascribed to truncated planetary terms in Brown's theory [@occ-morrison-1979]. The 1992 Supplement cites this work: "lunar occultations alone provide fairly precise values from 1861 to 1954" [@occ-es1992].

### Personal equation

Visual timings lag the event. In 1981 most visual timings used a stopwatch started at the event, and about 20 per cent used the eye-and-ear method against time signals [@occ-morrison-appleby-1981-pe]. Morrison and Appleby used 2175 photoelectric timings as a control. They found the [?occ-personal-equation|personal equation] "a function of the elongation of the Moon (for reappearances) and the magnitude of the star" [@occ-morrison-appleby-1981-pe]. Their Table 2 gives the corrections in seconds, with $D$ the Moon's elongation in degrees [@occ-morrison-appleby-1981-pe]:

| Method | Disappearance | Reappearance |
|---|---|---|
| Stopwatch | $-0.48$ | $-0.99 + 0.79\,u - 0.29\,u^2$ |
| Eye and ear | $-0.07$ | $-0.50 + 0.79\,u - 0.29\,u^2$ |

where $u = (D - 180^{\circ})/100$. The last term is taken as quadratic in $u$, the form of the fitted parabola. "For stars brighter than 4.0 mag, +0.20 s should be applied", and the expressions carry a systematic uncertainty of ±0.06 s [@occ-morrison-appleby-1981-pe]. The archive still applies "0.48s for Disappearances, and 0.99s for Reappearances - except that if star magnitude is 4.0 or brighter the values used are 0.28s and 0.79s" when an observer gives none [@occ-vizier-vi132c]. Video removes the term. The RASC Handbook asks for visual timings to 0.2 s, or 0.5 s at grazes [@limb-dunham-rasc-2026].

### ΔT from the archive

The 2022 archive reduces every timing from 1623 with DE440, LOLA limb heights and the best star positions. It provides, per record, the limb height, the O−C residual "computed height of the star above the lunar limb", the position angle, and `dOC`, the "change in the O-C residual for a time difference of +1.0 second" [@occ-vizier-vi132c]. Times after 1972 are converted to TT through leap seconds with UT1−UTC applied. Times from 1961 to 1971 use the offsets of that period. Before 1961, "TT time was derived by the application of the quantity deltaT", taken from the spline table of the UK Hydrographic Office (UKHO) at astro.ukho.gov.uk [@occ-vizier-vi132c]. Earth rotation uses the Earth rotation angle "consistent with the IAU1976 model for precession". Sites are moved to WGS84 by the Molodensky transformation and corrected for polar motion from the C01 and C04 series of the International Earth Rotation and Reference Systems Service (IERS) [@occ-vizier-vi132c].

Stephenson, Morrison and Hohenkerk use an earlier DE430 version of the same reduction. The residual is "reckoned positive outside the limb", and the reduction "includes the change in $\Delta\sigma$ owing to a change of +1 s in the time of observation, which we refer to as the rate of change" [@cat-stephenson-2016]. Then "the actual value of ΔT for each observation can thus be recovered from the estimate used in the reduction by subtracting from it $\Delta\sigma$ divided by its rate of change":

$$
\Delta T = \Delta T_\mathrm{est} - \frac{\Delta\sigma}{d\Delta\sigma/dt} .
$$

They use "only observations with a rate of change greater than 0.2″ s⁻¹", because near a graze "the correction to the estimate of ΔT becomes indeterminate" [@cat-stephenson-2016]. Before 1945 an average error of ±0.3 s is assumed. After 1945 only electronic timings and visual timings stated to ±0.1 s are kept. Outliers are filtered at ±100 s before 1700 and ±25 s after [@cat-stephenson-2016]. The retained series has 478,843 occultation timings from 1623 to 2015. It "should be used in conjunction with the lunar ephemeris JPL DE430, or with other ephemerides in which the tidal acceleration is close to the value of −25.82″ cy⁻²" [@cat-stephenson-2016]. The ΔT series and its use for eclipses are in [ΔT and Earth rotation](../07-earth-and-time/delta-t-and-earth-rotation.md).

### The archive and its custody

HMNAO collected and reduced timings from 1943, published those before 1981 on microfiche in RGO Bulletins 183, 186 and 192, and built the historical file from Newcomb's compilation [@occ-vizier-vi132c]. The International Lunar Occultation Centre (ILOC) in Tokyo then took custody. "In 1981 ILOC took over the responsibility for collecting lunar occultation observations." It introduced electronic reporting and "continued in this role until 2008. In 2008 IOTA took over responsibility" [@occ-vizier-vi132c]. Herald and Gault rebuilt the whole series as VizieR VI/132, now version C of July 2022 [@occ-vizier-vi132c]. Of 461,692 events up to 2010, 21,054 needed a correction of date, star or site [@occ-vizier-vi132c]. Observations fell "from about 5500 per year in 2009, to 1300 in 2020", which the authors attribute to accurate ephemerides, Gaia and LOLA [@occ-vizier-vi132c]. The 1992 Supplement called occultations "the most accurate current method for investigating dynamical time" [@occ-es1992]. The 2016 note says that with current prediction accuracy "VISUAL observations to determine the EVENT TIME of ordinary occultations no longer have an accuracy that can lead to the observation being useful" [@limb-occult-accuracy-2016].

## The error budget of a timing prediction

Every term converts between time and angle through the radial limb rate $|n\cos\psi| = |kn\cos\psi|/k$ in angular units, typically 0.2 to 0.4 arcseconds per second [@occ-vizier-bocc]. Here $kn\cos\psi$ is $k$ times the radial rate, as [Besselian elements for lunar occultations](besselian-elements-for-occultations.md) shows. An error of 0.04 arcseconds is therefore about 0.1 to 0.2 s for a central event and grows without bound toward a graze [@occ-es1961].

| Term | Era and size | Source |
|---|---|---|
| Lunar ephemeris | $j = 2$: 0.16 arcseconds adopted per observation; corrections of 0.8 arcseconds in mean longitude found | [@occ-morrison-1979] |
| Star position | ZC era: about 0.3 arcseconds standard error; XZ80 with Gaia DR1: typical residual under 0.04 arcseconds in total; Gaia DR3: 0.01 to 0.05 milliarcseconds at epoch | [@occ-morrison-1979] [@limb-occult-accuracy-2016] [@occ-gaia-dr3-overview] |
| Lunar limb | Watts: about 0.15 to 0.2 arcseconds, 0.5 where extrapolated; LOLA: about 0.01 arcseconds | [@occ-morrison-1979] [@occ-vizier-vi132c] |
| Position angle of the event | 0.01 degrees needed on slopes to 13 degrees; a 0.2 degree error degraded Occult predictions until 2016 | [@occ-morrison-1979] [@limb-occult-accuracy-2016] |
| ΔT and UT1 | Before 1955: preliminary TD within 0.2 s; modern: UT1−UTC from IERS, so negligible | [@occ-morrison-1979] [@occ-vizier-vi132c] |
| Observer coordinates | 1 arcsecond and 30 m give parallax to 0.01 arcseconds; RASC asks for 0.5 arcseconds and 16 m | [@occ-morrison-1979] [@limb-dunham-rasc-2026] |
| Refraction | 0.02 arcseconds at 15 degrees altitude, about 0.9 at the horizon | [@occ-morrison-1979] |
| Personal equation | Visual: 0.3 to 1.0 s, systematic ±0.06 s after correction; video: none | [@occ-morrison-appleby-1981-pe] |
| Timing | Visual 0.1 to 0.2 s; photoelectric 0.001 s; video one field | [@occ-nather-evans-1970] [@occ-vizier-bocc] |
| Result | 1943 to 1974: residual spread 0.49 arcseconds; 2016: most predictions within 0.3 s of observed | [@occ-morrison-1979] [@limb-occult-accuracy-2016] |

The RASNZ page states the scale observers meet: a timing to 0.1 s fixes the Moon's edge to about 80 metres [@occ-rasnz-totals]. At 0.4 arcseconds per second and 1.863 km per arcsecond, 0.1 s is 75 m. The figures agree [@limb-espenak-limb-page].

## Software and constants

| Program | Status | What it uses | Source |
|---|---|---|---|
| Occult 4 (Herald) | Free Windows program, source not public | XZ80Q, Gaia EDR3 subset to magnitude 16, UCAC4, LOLA limb (download 26), DE ephemerides | [@occ-occult4-page] [@limb-occult-accuracy-2016] |
| Lunar Occultation Workbench (Limburg) | Freeware, Lite and Professional | 80,000 or 476,000 stars from GSC 1.1; Watts and MoonLimb limb databases | [@occ-iota-manual-2007] |
| Grazereg and GRAZPREP-4 (Riedel) | IOTA/ES graze tools | Graze tables, limit-line headings, station planning | [@occ-iota-manual-2007] [@occ-baa-lunar] |
| Limovie and Tangra | Video photometry | Light curves for Occult reports and B/occ | [@occ-vizier-bocc] |
| lunar-shadows (Molteno) | Open source, third party | 1737.4 km lunar sphere, LOLA 118 m, 6371 km sphere then WGS84 terrain | [@occ-lunar-shadows] |

The constants that a reader meets across these sources are listed below. Prediction $k$ is 0.2725 [@occ-es1961]. Reduction $k$ was 0.2724953 and later 0.2725026 [@occ-es1961]. The IAU $k$ is 0.2725076 [@occ-es1992]. The $j = 2$ semidiameter is 932.58 arcseconds at a parallax of 3422.608 arcseconds and an Earth radius of 6,378,160 m, corrected by $+0.04$ arcseconds [@occ-morrison-appleby-1981-pe]. The LOLA reference sphere is 1737.4 km [@occ-lunar-shadows]. Occult's own choices of $k$ and reference radius are not published online.

## Sources compared

| Source | Subject | Unique content |
|---|---|---|
| Chauvenet [@bes-chauvenet-1863] | Planets | Reduction of a planet contact to the eclipse case, relative parallax, phase and terminator |
| ES 1961 [@occ-es1961] | Reduction | $\Delta\sigma$ in lunar radii, limb correction, the 0.549 ΔT factor |
| Morrison 1979 [@occ-morrison-1979] | Analysis | Partials, weights, refraction, longitude and TD corrections |
| Morrison and Appleby 1981 [@occ-morrison-appleby-1981-pe] | Personal equation | Phase and magnitude dependence |
| VI/132C [@occ-vizier-vi132c] | Archive | Custody, star sources, LOLA limb, conversion to TT, default corrections |
| Stephenson et al. 2016 [@cat-stephenson-2016] | ΔT | Recovery formula, rate filter, 478,843 timings |
| XZ80Q ReadMe [@occ-vizier-i291] | Catalogue | History, coverage, record content, double codes |
| Gaia DR3 documentation [@occ-gaia-dr3-propagation] | Positions | Rigorous epoch propagation |
| Nather and Evans 1970, Richichi et al. 2010 [@occ-nather-evans-1970] [@occ-richichi-2010] | Diameters | Fringe rate, Fresnel scale, resolution limits |

## What a developer should do

Take star positions from Gaia DR3 and propagate them with the full six-parameter model, falling back to XZ80Q only for stars Gaia lacks. Carry the WDS component and its offset for doubles. Reduce each timing to $\Delta\sigma$ with its rate $d\Delta\sigma/dt$, its position angle and the limb height used. Then a user can recover ΔT, or the limb residual, with Stephenson's formula. Express time in TT internally and record the UT1 source. Treat a planet by Chauvenet's construction. Compute the planet's outline and terminator from its pole, radii and phase, find the perpendicular to the Moon's limb at the contact point, and solve the four contacts as an eclipse of two discs. Fall back to the relative-parallax star method only for small discs. Read the VI/132C doc.txt, Morrison 1979 sections 2 to 4, and Chauvenet's articles 347 to 355 first.

## What this changes

The pipeline needs a star-catalogue stage with epoch propagation, which eclipses never needed, and a reduction stage that runs the prediction backwards to an O−C residual. Planet occultations reuse the eclipse contact solver with a non-circular occulted body. Its edge is an outline and a terminator computed from the physical ephemeris. Nothing in the error budget is now dominated by the star, so the limb stage and the position angle become the accuracy-critical parts.

## Open questions

- Obtain Hilton et al. (1989), cited by the 1992 Supplement, for the reduction of 58 Chinese planetary occultations to ΔT.
- Obtain Occult's help topics on lunar occultations of planets, to record how it models phase, oblateness and the four contacts.
- Obtain Morrison and Appleby (1981a), the catalogue of occultations 1972 to 1979, and RGO Bulletins 183, 186 and 192 for the original HMNAO reductions.
- Obtain the CHARM2 catalogue paper (Richichi et al. 2005) for a compiled list of lunar-occultation diameters with their methods.
- Obtain the XZ80Q doc.txt history file that the ReadMe references, for the XZ80N and XZ80P revisions.
- Obtain the UKHO spline table of ΔT that VI/132C uses before 1961, to record its version and date.
