---
title: Besselian elements for lunar occultations
seo_title: Lunar Occultation Prediction: Besselian Elements and Limits
description: How almanac offices and IOTA predict lunar occultations of stars, from the cylindrical shadow and conjunction elements to station times, coefficients and limits.
order: 1
status: working
updated: 2026-10-17
tags: [occultations, besselian, fundamental-plane, prediction, iota]
---

::: summary
- **A star casts a cylindrical lunar shadow.** On the fundamental plane, which is perpendicular to the star direction, the shadow is a circle of fixed radius $k = 0.2725$ Earth equatorial radii. The prediction condition is $(x-\xi)^2 + (y-\eta)^2 = k^2$ [@occ-es1961] [@occ-es1992].
- **The elements are given once, at conjunction in right ascension.** They are the time $T_0$, the star's Greenwich hour angle $H$, $Y = y(T_0)$, the hourly rates $x'$ and $y'$, and the star's place. The Supplement treats $x$ and $y$ as linear in time to prediction precision [@occ-es1961] [@occ-es1992].
- **Timing errors scale as $1/(kn\cos\psi)$.** This quantity falls to zero at a graze. HM Nautical Almanac Office (HMNAO) dropped predictions when $|kn\cos\psi| < 0.030$ and dropped the longitude and latitude coefficients below 0.060 [@occ-es1961].
- **The limit lines of an occultation are the eclipse limit lines with $L$ replaced by $k$.** Chauvenet states the condition as $(x-\xi)\cos N - (y-\eta)\sin N = \pm k$, with $N$ the direction of the shadow's motion [@bes-chauvenet-1863].
- **Several values of $k$ have been in use.** Predictions used 0.2725, reductions used Innes' 0.2724953 and then 0.2725026 from 1968, and the IAU adopted 0.2725076 in 1982 "to conform to the value used in occultation predictions" [@occ-es1961] [@occ-es1992].
- **Publication moved from almanac offices to IOTA.** HMNAO made worldwide predictions from 1937. The Astronomical Almanac of 1992 printed only dates and areas for planets and bright stars. The International Occultation Timing Association (IOTA) and the Royal Astronomical Society of Canada's Observer's Handbook (RASC Observer's Handbook) now publish predictions computed with Herald's Occult [@occ-es1961] [@occ-es1992] [@limb-dunham-rasc-2026].
- **Standard-station coefficients have two sign conventions.** The 1961 Supplement multiplies its $a$ by degrees of longitude west. The current RASC tables multiply $A$ by east-positive longitude. A program that mixes them inverts the longitude correction [@occ-es1961] [@limb-dunham-rasc-2026].
:::

**The question.** How is the geometry of a solar eclipse reused to predict a [?occ-lunar-occultation|lunar occultation] of a star? This note gives the elements, the station reduction, the limits on the Earth and the constants, as the almanac offices published them. It also says who publishes the predictions today and in what form. Limb corrections and grazes are in [Grazes and the lunar limb](grazes-and-limb.md). Catalogues, planets, reductions and the error budget are in [Planets, catalogues and reduction](planets-catalogues-and-reduction.md).

## From the shadow cone to the shadow cylinder

The [?besselian-elements|Besselian elements] of a solar eclipse describe two cones, because the Sun has a finite size and distance. A star has neither, so the cones become one cylinder. The 1961 Explanatory Supplement states the geometry directly: "In occultations, the [?fundamental-plane|fundamental plane] passes through the centre of the Earth and is perpendicular to the line joining the star and the centre of the Moon, i.e. to the axis of the shadow" [@occ-es1961]. The axes are the eclipse axes. The $x$ axis lies in the equator and is positive east, and the $y$ axis is positive north. The unit is the Earth's equatorial radius [@occ-es1961]. The Supplement continues: "The great distance of the star implies that the fundamental plane is perpendicular to the line joining the centre of the Earth to the star, and that the Moon's shadow is essentially a cylinder whose intersection with the fundamental plane is a circle of invariable size, its diameter being equal to that of the Moon" [@occ-es1961]. The 1992 Supplement repeats the paragraph in section 9.41 [@occ-es1992].

This [?occ-shadow-cylinder|shadow cylinder] removes four eclipse elements. There is no $d$ or $\mu$ to compute, because the axis points at a fixed star. Its direction is the star's apparent right ascension $\alpha_*$ and declination $\delta_*$. There are no $l_1$, $l_2$, $\tan f_1$ or $\tan f_2$, because the radius on every plane parallel to the fundamental plane is the same constant $k$. The [?k-lunar-radius|ratio k] is the lunar radius in Earth equatorial radii, as in the eclipse case. The derivation of the eclipse elements is in [Besselian elements](../01-foundations/besselian-elements.md), and this note only states where the occultation case differs.

![For a star the Moon's shadow is a circle of fixed radius $k = 0.2725$ moving along an almost straight track. The occultation zone is bounded by the two lines parallel to that track at distance $k$. Here, with $Y = +0.9753$, the northern line misses the Earth, so only a southern limit exists [@occ-es1961].](img/occultation-plane.svg)

## The coordinates of the shadow axis

The Moon's apparent right ascension $\alpha_\mathrm{m}$, declination $\delta_\mathrm{m}$ and equatorial [?horizontal-parallax|horizontal parallax] $\pi_\mathrm{m}$ give the axis coordinates. The 1961 Supplement writes [@occ-es1961]

$$
x\sin\pi_\mathrm{m} = \cos\delta_\mathrm{m}\sin(\alpha_\mathrm{m}-\alpha_*),\qquad
y\sin\pi_\mathrm{m} = \sin\delta_\mathrm{m}\cos\delta_* - \cos\delta_\mathrm{m}\sin\delta_*\cos(\alpha_\mathrm{m}-\alpha_*).
$$

These are the eclipse equations for $x$ and $y$ with the point Z replaced by the star, so $a \to \alpha_*$ and $d \to \delta_*$ [@occ-es1961] [@bes-es1961]. For predictions the Supplement reduces them to

$$
x = \frac{15\cos\delta_\mathrm{m}\,(\alpha_\mathrm{m}-\alpha_*)}{\pi_\mathrm{m}},\qquad
y = \frac{\delta_\mathrm{m}-\delta_*}{\pi_\mathrm{m}} + 0.000036\,x\,(\alpha_\mathrm{m}-\alpha_*)\sin\delta_*,
$$

"in which $\alpha_\mathrm{m}-\alpha_*$ is in seconds of time, and $\delta_\mathrm{m}-\delta_*$ and $\pi_\mathrm{m}$ are in seconds of arc" [@occ-es1961]. The second term of $y$ "may be replaced by $+0.0083x^2\tan\delta_*$, with a further error not exceeding 0.0002" [@occ-es1961]. The 1992 edition gives the same reduction in degrees as its equation 9.41-2 [@occ-es1992]:

$$
x = \frac{(\alpha-\alpha_s)\cos\delta}{\pi},\qquad
y = \frac{\delta-\delta_s}{\pi} + 0.0087\,x\,(\alpha-\alpha_s)\sin\delta_s .
$$

Here unsubscripted symbols are the Moon's and the subscript $s$ is the star's. The constants agree. In seconds of time, $0.000036 \approx 15/(2\times 206265)$. In degrees, 0.0087 is half of one degree in radians, 0.008727. Both are half the radians-per-unit factor of the angle. That factor comes from the first-order term of $1-\cos(\alpha_\mathrm{m}-\alpha_*)$.

### The elements at conjunction

The elements are given "for one instant only, namely, the time of conjunction of the star and Moon in right ascension, when $x$ is zero" [@occ-es1961]. This set of [?occ-conjunction-elements|occultation elements] is [@occ-es1961] [@occ-es1992]:

| Element | Meaning |
|---|---|
| $T_0$ | UT of conjunction in right ascension |
| $H$ | Greenwich hour angle of the star at $T_0$ |
| $Y$ | $y$ at $T_0$, in Earth equatorial radii |
| $x'$, $y'$ | hourly rates of $x$ and $y$, Earth radii per hour |
| $\alpha_*$, $\delta_*$ | apparent right ascension and declination of the star |

At conjunction the Supplement gives [@occ-es1961]

$$
x = 0,\qquad Y = \frac{\delta_\mathrm{m}-\delta_*}{\pi_\mathrm{m}},\qquad
x' = \frac{15\cos\delta_\mathrm{m}\,\alpha'_\mathrm{m}}{\pi_\mathrm{m}},\qquad
y' = \frac{\delta'_\mathrm{m} - Y\pi'_\mathrm{m}}{\pi_\mathrm{m}},
$$

with $\alpha'_\mathrm{m}$ the hourly variation of right ascension in seconds of time and $\delta'_\mathrm{m}$, $\pi'_\mathrm{m}$ in seconds of arc. "As $x$ and $y$ are linear to the precision required $x'$ and $y'$ are constant" [@occ-es1961]. The 1992 edition derives the rates by "differentiating the Moon's daily polynomial coefficients" [@occ-es1992].

The Office computed every element twice as a check. The first method takes $x_1, y_1$ and $x_2, y_2$ at the integral hours $T_1$ and $T_2$ that bracket conjunction. Then $x' = x_2 - x_1$, $y' = y_2 - y_1$, $T_E = T_1 - x_1/x'$ and $Y = y_1 - x_1 y'/x'$ [@occ-es1961]. The second method interpolates the lunar ephemeris to $T_E$ and applies the direct formulas [@occ-es1961]. The Moon's ephemeris was tabulated in Ephemeris Time, so the elements were computed in that scale and then moved to UT by [@occ-es1961]

$$
T_0 = T_E - \Delta T,\qquad H = H_E - 1.002738\,\Delta T .
$$

The worked example is Z.C. 2833, Zodiacal Catalogue number 2833, on 1960 September 1. It gives $T_E = 19^\mathrm{h}.7924$ ET, $Y = +0.9753$, $x' = +0.6046$, $y' = +0.0543$ and, with $\Delta T = 36$ s, $T_0 = 19^\mathrm{h}.7824$ UT [@occ-es1961]. A modern implementation takes these quantities in TT from a JPL ephemeris and applies [?delta-t|ΔT] once, as for eclipses. The selection of conjunctions before this step is a declination test. "If at any instant a star is within an angular distance of the Moon of less than the sum of the Moon's horizontal parallax and semi-diameter, it must be occulted as seen from some point on the Earth" [@occ-es1961] [@occ-es1992].

## The station reduction and the time of contact

For an observer with geocentric coordinates $\rho\sin\varphi'$ and $\rho\cos\varphi'$, the [?rho-sin-phi|parallax constants], and longitude $\lambda$, the Supplement forms the star's local hour angle at the trial interval $t$ from conjunction [@occ-es1961]:

$$
h = H - \lambda + t_s,\qquad t_s = 1.002738\,t .
$$

In the 1961 Supplement $\lambda$ is in hours and positive west. Strasbourg has $\lambda = -0^\mathrm{h}.518$ in the worked example [@occ-es1961]. The observer's projection on the fundamental plane is

$$
\xi = \rho\cos\varphi'\sin h,\qquad \eta = \rho\sin\varphi'\cos\delta_* - q_h\sin\delta_*,\qquad q_h = \rho\cos\varphi'\cos h .
$$

The Supplement writes $q_h$ as $Q$ [@occ-es1961]. This site keeps $Q$ for the shadow-edge angle, so the auxiliary is renamed here. The relative coordinates and their hourly rates are

$$
f = x - \xi,\quad g = y - \eta,\qquad
f' = x' - h'q_h,\quad g' = y' - h'\xi\sin\delta_*,
$$

where $h' = 2\pi\times1.002738/24 = 0.2625$ radians per hour is the Earth's rotation rate [@occ-es1961]. The Supplement's $f$ and $g$ are the $u = x - \xi$ and $v = y - \eta$ of the eclipse contact solution in [Contact times and magnitude](../04-local-circumstances/contact-times-and-magnitude.md). This topic keeps the Supplement's letters.

"The only mathematical condition to be satisfied is that, at the time of disappearance or reappearance, the line joining the star and the observer must be tangential to the limb of the Moon" [@occ-es1961]. On the plane this is

$$
f^2 + g^2 - k^2 = 0,\qquad k = 0.2725 .
$$

From a preliminary interval $t_1$ the first correction is [@occ-es1961]

$$
\Delta t_1 = \frac{k^2 - f_1^2 - g_1^2}{2\,(f_1f_1' + g_1g_1')} .
$$

The Supplement adds a second-order term $\Delta t_2$ that "is negligible in most cases but becomes appreciable as $kn_1\cos\psi_1$ becomes small, that is as grazing conditions are approached" [@occ-es1961]. With

$$
n^2 = f'^2 + g'^2,\qquad kn\cos\psi = ff' + gg',
$$

the exact condition at $t_1 + \Delta t$ is the quadratic $n_1^2\Delta t^2 + 2kn_1\cos\psi_1\,\Delta t - (k^2 - f_1^2 - g_1^2) = 0$. Its second-order solution gives $\Delta t_2 = -n_1^2\,\Delta t_1^2/(2kn_1\cos\psi_1)$. This form is derived here from the quadratic and is not the Supplement's printed expression, which this note does not reproduce. It shows why the term grows as $kn_1\cos\psi_1$ falls. A third correction, if one is needed, is $(k^2 - f^2 - g^2)/(2kn\cos\psi)$ [@occ-es1961]. The [?position-angle|position angle] of the event, "measured eastwards from the north point of the Moon's disk", follows from [@occ-es1961]

$$
\sin P = -f/k,\qquad \cos P = -g/k .
$$

The Supplement's worked numbers check these signs. At Strasbourg, $f = -0.2716$ and $g = +0.0238$ give $P = 95^{\circ}$, and $kn\cos\psi = -0.118$ marks a disappearance. The predicted time is $19^\mathrm{h}\,01^\mathrm{m}.0$ UT [@occ-es1961]. The symbol $P$ has this site's meaning, the position angle of a contact.

### What kn cos ψ measures

"The quantity $n$ is a measure of the Moon's motion relative to the observer and $\psi$ is the angle between the radius from the centre of the Moon to the star and the direction of this motion" [@occ-es1961]. The angle $\psi$ lies between 90 and 180 degrees for disappearances and between 0 and 90 degrees for reappearances. So [?occ-kn-cos-psi|kn cos ψ] is negative for a [?occ-disappearance-reappearance|disappearance] and positive for a reappearance [@occ-es1961]. "Any error in the position of the star or in the assumed limb of the Moon gives rise to an error in the predicted time of occultation that is inversely proportional to $kn\cos\psi$" [@occ-es1961]. This is the occultation form of Herald's $\sec(\mathrm{PA}-N)$ factor for eclipse contacts [@limb-herald-1983]. HMNAO used it as the graze filter. "The occultations are omitted completely when the value of $kn\cos\psi$ at the moment of occultation is numerically less than 0.030, unless the star is brighter than 1.5 when the limiting value is 0.015", and the coefficients are omitted below 0.060 [@occ-es1961].

Because $f^2 + g^2 = k^2$ at contact, the rate at which the observer's distance from the shadow axis changes is $(ff' + gg')/k = n\cos\psi$. So $kn\cos\psi$ is $k$ times the radial rate, and the radial rate itself is $n\cos\psi = (kn\cos\psi)/k$ Earth radii per hour. One Earth radius on the plane subtends $\pi_\mathrm{m}$ at the Moon's distance, about 3422 arcseconds at mean distance [@occ-morrison-appleby-1981-pe]. For the Strasbourg event the radial rate is $0.118/0.2725 \times 3422/3600 = 0.41$ arcseconds per second of time normal to the limb. This conversion is derived here. It matches the 0.2 to 0.4 arcseconds per second that the light-curve archive gives for typical events [@occ-vizier-bocc].

### Altitude, Sun and preliminary times

The program also rejected low events. After forming $h$ it computes

$$
s_\mathrm{alt} = \sin(\mathrm{alt}) - \sin 10^{\circ} = \rho\sin\varphi'\sin\delta_* + q_h\cos\delta_* - 0.173,
$$

and examines events with negative $s_\mathrm{alt}$ [@occ-es1961]. The Supplement writes $s$. The subscript is added here because $s$ is the lunar semidiameter elsewhere in this topic. The magnitude and Sun limits of 1961 were these. Stars to magnitude 7.5 from the Zodiacal Catalogue were included. Events at the [?occ-dark-limb|bright limb] were limited: disappearances were included only to magnitude 4.5 and reappearances to 3.5. Dark-limb reappearances were included to 6.5. The Moon had to be 10 degrees high, or 2 degrees for stars of magnitude 1.9 and brighter. Solar depression limits ran from sunset to 12 degrees depending on magnitude [@occ-es1961]. The IOTA manual states that "observations of daytime events are usually impossible for stars fainter than magnitude 3.0-3.5" [@occ-iota-manual-2007]. The RASC Handbook graze maps draw daytime tracks dotted and mark with S the end of a track where "sunlight or twilight interferes" [@limb-dunham-rasc-2026].

Preliminary times came from the "occultation machine". This was a globe and a cylindrical beam of light set to the elements, built for HMNAO in 1934 after J. D. McNeile's 1928 machine [@occ-es1961]. A computer replaces it with either of the Supplement's alternatives. One alternative solves the quadratic $(f_0 + f_0'\Delta t)^2 + (g_0 + g_0'\Delta t)^2 - k^2 = 0$ from conjunction. The other tabulates $f^2 + g^2 - k^2$ at five or six whole hours and interpolates inversely [@occ-es1961]. For the second, the rigorous station terms from conjunction are [@occ-es1961]

$$
f_t = f_0 + x't + \xi_0(1-\cos t_s) - q_{h0}\sin t_s,\qquad
g_t = g_0 + y't - \sin\delta_*\,\big[q_{h0}(1-\cos t_s) + \xi_0\sin t_s\big],
$$

with $t_s$ in radians of sidereal rotation. The factor $\xi_0$ on $\sin t_s$ is supplied here from the condition that $dg_t/dt$ at $t = 0$ equal $g'$ as defined above. The Supplement warns that "the non-linearity of $f'$ and $g'$ may make the difference between a 'graze' and a complete miss". In the miss case the time of closest approach $\Delta t = -(f_0f_0' + g_0g_0')/n^2$ is the new starting point [@occ-es1961].

## Coefficients for nearby observers

A table for about 80 standard stations served the world in 1961 [@occ-es1961]. Observers near a station corrected the time with the [?occ-ab-coefficients|a and b coefficients] [@occ-es1961]:

$$
a = -\frac{K}{kn\cos\psi}\,\big(f q_h + g\xi\sin\delta_*\big),\qquad
b = -\frac{K}{kn\cos\psi}\,\big\{C_{\mathrm{ell}}^2\rho\sin\varphi'\,(f\sin h - g\sin\delta_*\cos h) - SC_{\mathrm{ell}}\rho\cos\varphi'\,g\cos\delta_*\big\},
$$

where $K = 1.047$ converts hours per radian to minutes of time per degree, and $S = \rho\sin\varphi'/\sin\varphi$ and $C_{\mathrm{ell}} = \rho\cos\varphi'/\cos\varphi$ are the ellipsoid auxiliaries [@occ-es1961]. The Supplement writes $C$ for $C_{\mathrm{ell}}$. This site keeps $C$ for Herald's angle from the contact point. They "may each be taken as unity", with a maximum error of 0.03 minutes [@occ-es1961]. For an observer $\Delta\lambda$ degrees west and $\Delta\varphi$ degrees north of the station,

$$
\text{approximate time} = \text{predicted time} + a\,\Delta\lambda + b\,\Delta\varphi .
$$

The Strasbourg example gives $a = -1.5$ and $b = +0.4$ minutes per degree [@occ-es1961]. The error is "unlikely to be greater than one minute" within 200 miles and may reach two minutes at 300 miles. A second-order correction of $+0.075\cos^2\varphi\,(\Delta\varphi)^2$ minutes is added for disappearances and subtracted for reappearances [@occ-es1961].

The RASC Handbook uses the same device for its 18 North American standard stations, computed by Dunham with Occult 4 [@limb-dunham-rasc-2026]. Its formula is $\mathrm{UT} = \mathrm{UT}_* + A(L_o - L_o^*) + B(L_a - L_a^*)$ in minutes per degree, for stations within 300 km. "Longitude measured west of Greenwich is assumed to be negative (which is now the IAU convention and that used by IOTA's Occult software)" [@limb-dunham-rasc-2026]. The 1961 $a$ multiplies degrees west, so $A = -a$ for the same event. The RASC tables warn that values of A or B above 5 "will not give a reliable prediction for other places" near grazes [@limb-dunham-rasc-2026].

## Where the occultation can be seen

### Chauvenet's limit condition

Chauvenet treats the limits by the eclipse method. "For a point on the limiting curve, the least value of $\Delta$ in Art. 324 is in a solar eclipse $= L$, but in an occultation it is $= k$" [@bes-chauvenet-1863]. With the direction of relative motion $N$ defined by $n\sin N = x'$ and $n\cos N = y'$, the condition becomes [@bes-chauvenet-1863]

$$
(x - \xi)\cos N - (y - \eta)\sin N = \pm k .
$$

With $x$ and $y$ linear in time, Chauvenet reduces it to $(x_0 - \xi)\cos N - (y_0 - \eta)\sin N = \pm k$, with $x_0$ and $y_0$ at any epoch $T_0$ [@bes-chauvenet-1863]. Geometrically, the observer's projection must lie on one of the two lines parallel to the shadow track at perpendicular distance $k$. These are the [?occ-limit-line|northern and southern limit lines]. Because $\xi$ and $\eta$ depend on time through the Earth's rotation, a point on the ground satisfies the condition at the instant of closest approach. The same condition with the sign choice and $N$ defines the [?graze-zone|graze zone], which [Grazes and the lunar limb](grazes-and-limb.md) treats with the limb profile.

### Limiting parallels

Before maps were practical the almanacs printed [?occ-limiting-parallels|limiting parallels] "outside which the star could not be occulted" [@occ-es1961]. The 1961 Supplement summarises Chauvenet's result. Set $\cot N = y'/x'$ with $y'$ positive and $0 < N < 90^{\circ}$. Then $\cos\varepsilon_1 = Y\sin N + 0.2725$, $\cos\varepsilon_2 = Y\sin N - 0.2725$ and $\sin\beta = \sin N\cos\delta_*$ [@occ-es1961]. The Supplement writes $\gamma_1$ and $\gamma_2$. They are renamed here because $\gamma$ is the eclipse axis distance elsewhere on this site. A table of ten cases for northern and southern declinations then gives the northern and southern limiting latitudes $\varphi_1$ and $\varphi_2$, from forms such as $\sin\varphi_2 = \sin(N - \varepsilon_2)\cos\delta_*$, or the poles when an $\varepsilon$ is imaginary [@occ-es1961]. The Supplement credits the method to Chauvenet, volume 1, page 561 [@occ-es1961]. This note does not reproduce the case table. A modern implementation does not need it, because it can trace the limit lines directly.

### The 1992 visibility map

The 1992 Supplement replaces the limiting parallels with a map recipe for a personal computer [@occ-es1992]. The shadow centre at time $t$ from conjunction is $x = x't$, $y = y't + Y$ (equation 9.41-4). Its geographic position on a spherical Earth of unit radius comes from equation 9.41-5:

$$
\varphi = \sin^{-1}(y\cos\delta_s + z\sin\delta_s),\qquad
h = \tan^{-1}\frac{x}{-y\sin\delta_s + z\cos\delta_s},\qquad
\lambda = h - (H + 15t\times1.0027380),
$$

with $z$ the coordinate along the axis toward the Moon [@occ-es1992]. On the unit sphere $z = \sqrt{1 - x^2 - y^2}$. In the form above $\lambda$ is positive east and angles are in degrees. The signs in the longitude line are fixed here by the requirement that $x$ is positive east. Points on the edge of the shadow are $\xi = x - k\sin Q$ and $\eta = y - k\cos Q$ as $Q$ runs from 0 to 360 degrees, with $k = 0.2725$ (equation 9.41-6) [@occ-es1992]. Here $Q$ is an angle around the shadow edge, which is this site's use of $Q$. When the shadow is only partly on the Earth, the cut points come from equation 9.41-8 with $D = \sqrt{x_0^2 + y_0^2}$ and $\vartheta_D = \tan^{-1}(y_0/x_0)$ [@occ-es1992]. The Supplement writes $S$ for $\vartheta_D$. This site keeps $S$ for the ellipsoid auxiliary. The Supplement gives $Q_2 = 180^{\circ} - Q_1 - 2\vartheta_D$ and a right side with denominator $2kD$ [@occ-es1992]. Requiring the edge point to lie on the unit circle gives the full equation, derived here:

$$
\sin(Q_1 + \vartheta_D) = \frac{D^2 + k^2 - 1}{2kD} .
$$

The recipe is spherical and ignores the observer's height. It is a visibility map, not a limit-line product. "A similar procedure may be applied for predicting the areas of visibility of occultations of planets by the Moon" [@occ-es1992].

## The constant k

The occultation literature carries its own history of $k$, tied to the eclipse history in [Besselian elements](../01-foundations/besselian-elements.md).

| Value of $k$ | Where used | Source |
|---|---|---|
| 0.27227 | Burckhardt's value from eclipses and occultations, used by Chauvenet for eclipses | [@bes-chauvenet-1863] |
| 0.27264 | Oudemans' value "for occultations", about 1.25 arcseconds larger in semidiameter | [@bes-chauvenet-1863] |
| 0.2724953 | Innes 1924, HMNAO occultation reductions | [@occ-es1961] |
| 0.2725026 | HMNAO reductions "for 1968 onwards" | [@occ-es1961] |
| 0.2725 | HMNAO and ES 1992 predictions and maps | [@occ-es1961] [@occ-es1992] |
| 0.2725076 | IAU 1982, adopted "to conform to the value used in occultation predictions" | [@occ-es1992] |

Chauvenet notes that "it is only for the reduction of isolated observations that we need an exact value, since, when we have a number of observations, the correction of whatever value of $k$ we may use will be obtained by the solution of our equations of condition" [@bes-chauvenet-1863]. The 1992 Supplement says the 1982 adoption meant "that limb effects are no longer accounted for, but are averaged" [@occ-es1992]. Morrison's reductions instead carried a semidiameter at mean distance of 932.58 arcseconds, computed as $s_{\mathrm{m},0} = 0.0799 + 0.272453\,\pi_0$ arcseconds from the parallax [@occ-morrison-1979]. Morrison writes $s_0$. This site keeps $s_0$ for the solar semidiameter at 1 au. The photoelectric solution of Morrison and Appleby then corrected it by $+0.044 \pm 0.015$ arcseconds [@occ-morrison-appleby-1981-pe]. A modern reduction with Lunar Orbiter Laser Altimeter (LOLA) limb heights has a different reference radius again. That question is in [Grazes and the lunar limb](grazes-and-limb.md).

## Who published predictions

**Almanac offices.** Prediction elements first appeared in The Nautical Almanac for 1824, with predictions for Greenwich from 1834. "The American Ephemeris gave prediction elements and predictions for Washington from its introduction in 1855" [@occ-es1961]. HMNAO undertook "a world-wide coverage of predictions" from 1937. From 1943 it was "responsible for the collation, reduction, and discussion of observations" [@occ-es1961]. The programme "may well include over 8000 predictions a year" [@occ-es1961]. Grazing-occultation maps and detailed graze predictions were issued from the 1960s, according to the 1973 note in the reprint [@occ-es1961]. Elements were dropped from the American Ephemeris after 1959. Predictions were left to "other publications" for North America and the Commonwealth [@occ-es1961]. The BAA computing section reduced amateur observations up to 1942, and the BAA Handbook carried the predictions of occultations of stars by planets [@occ-es1961].

**The Astronomical Almanac and ILOC.** By 1992 "only dates and general areas of visibility for the occultations of planets and bright stars by the Moon are published in The Astronomical Almanac" [@occ-es1992]. The International Lunar Occultation Centre of the Hydrographic Department in Tokyo was "responsible for the predictions and reductions of timings", and IOTA "provides predictions of occultations" [@occ-es1992]. ILOC collected observations from 1981 to 2008, when IOTA took over [@occ-vizier-vi132c]. For grazes in North America, "prior to 1993, data for predictions were provided by the United States Naval Observatory" [@occ-iota-manual-2007]. This note does not establish whether the current Astronomical Almanac still prints these occultations.

**IOTA, RASC, BAA and RASNZ.** The RASC Handbook for 2026 prints total-occultation tables for 18 standard stations to magnitude 6.0, with $A$, $B$ and the [?occ-cusp-angle|cusp angle]. Dunham computed them with Occult 4. Riedel and Dunham add a graze map and table for 21 bright events [@limb-dunham-rasc-2026]. The British Astronomical Association (BAA) Handbook carries graze predictions and the BAA Lunar Section sends timings to IOTA [@occ-baa-lunar]. The Royal Astronomical Society of New Zealand (RASNZ) Occultation Section publishes yearly total-occultation predictions for New Zealand and Australia and recommends Herald's program [@occ-rasnz-totals]. Occult itself produces single-site and all-star searches and graze tables [@bes-occult-tutorial] [@occ-occult4-page].

## Sources compared

| Source | Elements and formulas | Constants | Unique content |
|---|---|---|---|
| ES 1961 section 10 [@occ-es1961] | $x, y$, rates, conjunction elements, station reduction, $\Delta t$ iteration, $a$ and $b$, limiting parallels | $k = 0.2725$ for prediction, 0.2724953 and 0.2725026 for reduction, $h' = 0.2625$ | The worked Z.C. 2833 example, prediction limits, the $kn\cos\psi$ graze filter |
| ES 1992 section 9.4 [@occ-es1992] | The same elements in degrees, shadow-centre and shadow-edge geography, visibility map | $k = 0.2725$, IAU 0.2725076 in 8.12 | Map recipe 9.41-4 to 9.41-9, the planetary condition 9.42-1, ILOC's role |
| Chauvenet [@bes-chauvenet-1863] | Prediction for a place, limiting curves and parallels | Burckhardt 0.27227, Oudemans 0.27264 | The limit condition $(x-\xi)\cos N - (y-\eta)\sin N = \pm k$ |
| RASC Handbook 2026 [@limb-dunham-rasc-2026] | Standard-station tables from Occult 4 | Not stated | East-positive $A$ and $B$, cusp angle, 300 km validity |
| Occult [@occ-occult4-page] [@bes-occult-tutorial] | Implementation, closed source | Not documented online | Current predictions for IOTA and RASC |

## What a developer should do

Implement the 1961 station reduction as written, with $f$, $g$, $f'$, $g'$ and $kn\cos\psi$. Then replace its linear elements by a direct evaluation of $x$ and $y$ from the ephemeris at each iteration. The linear form is exact enough for minutes and seconds of prediction but not for 0.01 second reductions. Compute the star's apparent place for the event date, and take $\alpha_\mathrm{m}$, $\delta_\mathrm{m}$ and $\pi_\mathrm{m}$ from a JPL DE ephemeris in TT. Use the same rigorous $\xi$ and $\eta$ as the eclipse pipeline, with geodetic height and an ellipsoid. Report $kn\cos\psi$, or the radial limb rate $n\cos\psi$ in arcseconds per second, with every time. Flag events where it is small, as HMNAO did. Report position angle $P$ and the cusp angle. Make $k$ an explicit input. Use 0.2725076 when reproducing modern smooth-limb predictions, and let the limb stage carry the real silhouette. If you publish standard-station coefficients, state the longitude sign. Trace limit lines from Chauvenet's condition by solving, for each longitude, for the latitude at which the minimum of $\sqrt{f^2+g^2}$ over time equals $k$. This search is derived from the condition and is not quoted from a source.

## What this changes

The eclipse pipeline already has everything an occultation needs except the star. The ephemeris layer must accept a catalogue star with its epoch and space motion as a target, and the element stage must accept a cylinder, so that $l_1 = l_2 = k$ and $\tan f_1 = \tan f_2 = 0$. The local-circumstance solver can be shared if it takes $k$ and a target direction as inputs. Products gain two fields that eclipses lack: $kn\cos\psi$, which is $k$ times the radial limb rate, and the cusp angle.

## Open questions

- Obtain the HMNAO booklet "The Prediction and Reduction of Occultations" (supplement to The Nautical Almanac for 1938). It describes the occultation machine and Comrie's reduction elements that the Supplement summarises.
- Obtain ES 1961 pp. 285 and 288 as page images, for the ten-case limiting-parallel table and the printed $\Delta t_2$ term.
- Obtain a current edition of The Astronomical Almanac to confirm whether it still prints lunar occultations of planets and bright stars, and in which section.
- Obtain Occult's help file topic on lunar predictions to record which $k$, which reference radius and which ephemeris the 2026 version uses.
- Obtain Foxell's 1934 paper in Memoirs of the British Astronomical Association, volume 30, pages 107 to 148, which the Supplement cites for occultation maps.
