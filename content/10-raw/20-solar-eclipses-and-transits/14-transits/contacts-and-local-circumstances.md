---
title: Transit contacts and local circumstances
seo_title: Transit Contact Times and Local Circumstances
description: The contact-time solution for transits of Mercury and Venus, the almanac reduction formulas for any observer, and the constants that move the times.
order: 2
status: working
updated: 2026-10-17
tags: [transits, contacts, local-circumstances, solar-radius, delta-t, parallax]
---

::: summary
- **Contacts come from one quadratic.** With relative position $(u, v)$ and motion $(u', v')$, a contact at radius $L$ occurs at $t = L\cos\psi/n - (uu' + vv')/n^2$, with $\sin\psi = (uv' - u'v)/(nL)$ and $\cos\psi$ negative for ingress. The 1961 Explanatory Supplement and Chauvenet give the same solution [@tr-es1961] [@bes-chauvenet-1863].
- **A local contact time is a geocentric time plus a three-constant correction.** The almanac form is $T = T_0 + a\,\rho\sin\phi' + b\,\rho\cos\phi'\cos(c + \lambda)$. The yearbook of the Institute of Applied Astronomy of the Russian Academy of Sciences (IAA RAS) prints $a$, $b$, $c$ for each contact, and the 1961 Supplement derives them with ΔT inside the cosine [@tr-iaa-2019] [@tr-es1961].
- **Parallax moves Venus contacts by up to about 7 minutes and Mercury contacts by up to about 2 minutes.** Using geocentric times for a site can be wrong by up to 10 minutes for Venus and 3 minutes for Mercury [@tr-nasa-oh2012] [@tr-ew-tm2019] [@tr-nasa-visibility].
- **The solar radius moves every contact.** At the four modern transits one arcsecond of contact radius moves a geocentric interior contact by 10 to 21 seconds of time. The 0.32 arcsecond gap between 959.63 and 959.95 arcseconds is worth 3.3 s per contact in 2019 and 6.5 s in 2004. These values are computed here from the Supplement's solution with the published elements [@tr-es1961] [@tr-eso-eis-b1] [@tr-ew-tm2016] [@tr-ew-tm2019] [@tr-jubier-mtc-js] [@tr-jubier-vtc-js].
- **Planet radii are not standard.** Meeus prefers 8.41 arcseconds for Venus in transit work because 8.34 refers to the crust. Swiss Ephemeris and the Institut de mécanique céleste et de calcul des éphémérides (IMCCE) use the solid-body value, and Jubier uses 8.3442 arcseconds [@cat-meeus-1991-aa] [@tr-swisseph-swevents] [@tr-eso-eis-b1] [@tr-jubier-vtc-js].
- **Published 2004 Venus contacts differ by 4 to 5 seconds between Espenak and IMCCE.** The pattern, exterior contacts outward and interior contacts inward, matches a Venus semidiameter of 8.41 against 8.34 arcseconds to within half a second. Espenak and IAA agree to 1.5 seconds for Mercury in 2016 and to 1 second in 2019 [@tr-nasa-oh2004] [@tr-eso-eis-b1] [@tr-ew-tm2016] [@tr-iaa-2016] [@tr-ew-tm2019] [@tr-iaa-2019].
- **ΔT and the longitude convention are where predictions go wrong silently.** The IAA formulas take longitude east-positive. The 1961 Supplement and Jubier's code take it west-positive and add $1.002738\,\Delta T$ to it [@tr-iaa-2016] [@tr-es1961] [@tr-jubier-mtc-js].
:::

**The question.** Given elements for a transit, how are the geocentric contact times, the least separation and the position angles computed, how does a predictor turn them into contact times for an observer anywhere on Earth, and which constants change the answer by how much? The elements and the enumeration are in [Enumerating transits and their elements](enumeration-and-elements.md). The solar-eclipse counterparts are [Contact times and magnitude](../04-local-circumstances/contact-times-and-magnitude.md) and [The topocentric method](../04-local-circumstances/topocentric-method.md). The solar radius values themselves are in [Solar radius values](../06-solar-radius/solar-radius-values.md).

## Geocentric contacts

The 1961 Supplement solves for each [?tr-contacts|contact] by one correction to a trial time $T_0$ near it. With $u_0, v_0, u'_0, v'_0, n_0$ the values at $T_0$, the condition at $T = T_0 + \tau$ is

$$
(u_0 + u'_0\tau)^2 + (v_0 + v'_0\tau)^2 = L^2 .
$$

"Solving for $\tau$ by setting $\sin\psi = (u_0 v'_0 - u'_0 v_0)/(n_0 L)$ yields

$$
\tau = \frac{L\cos\psi}{n_0} - \frac{u_0 u'_0 + v_0 v'_0}{n_0^2}
$$

where $\cos\psi$ is taken as negative for ingress and positive for egress" [@tr-es1961]. The result "may be tested by means of the criterion $m = L$ and another approximation made if necessary" [@tr-es1961]. $L$ is $L_1$ for exterior contacts I and IV and $L_2$ for interior contacts II and III, in the heliocentric units of the previous note. In Example 9.26 three approximations give geocentric interior egress of Mercury on 1960 November 7 at "19h 10m 40s.8" E.T. [@tr-es1961].

Chauvenet gives the same solution in geocentric equatorial terms. With $\alpha, \delta$ for the planet and $\alpha', \delta'$ for the Sun at $T_0$, $\delta_0 = \tfrac12(\delta + \delta')$, and $a, d$ the relative hourly motions in right ascension and declination,

$$
m\sin M = (\alpha - \alpha')\cos\delta_0,\quad m\cos M = \delta - \delta',\quad n\sin N = a\cos\delta_0,\quad n\cos N = d,
$$
$$
\sin\psi = \frac{m\sin(M - N)}{s' \pm s},\qquad
T = T_0 + \frac{s' \pm s}{n}\cos\psi - \frac{m}{n}\cos(M - N),
$$

with $s'$ and $s$ the apparent semidiameters of the Sun and planet, the upper sign for exterior contacts, and $\cos\psi$ negative for ingress [@bes-chauvenet-1863]. Chauvenet notes that the angle $N + \psi$ "is (as in eclipses) the position angle of the point of contact" [@bes-chauvenet-1863]. He writes it $Q$. Here it is $P = N + \psi$, because the corpus keeps $Q$ for the shadow-edge angle of the limit condition. Jubier's calculator runs the same iteration in arcseconds on his polynomial elements:

```
L = ss + sp;            // contacts 1 and 4; ss - sp for 2 and 3
var SM = ((Xa * Ypa) - (Ya * Xpa)) / (n * L);
Tau = -(((Xa * Xpa) + (Ya * Ypa)) / n2) - ((L / n) * Math.sqrt(1 - (SM * SM)));   // ingress
```

with `ss` and `sp` the apparent semidiameters from 959.62 and 3.3558 arcseconds at 1 au, iterated until $|\tau| < 10^{-6}$ hours [@tr-jubier-mtc-js]. Stellarium's `localTransit` evaluates the eclipse form `dt = (L * cfi / sqrt(udot*udot + vdot*vdot)) - (u*udot + v*vdot)/n2` on its geocentric elements [@tr-stellarium-transits].

### Least separation and greatest transit

Chauvenet gives the least distance of centres directly, "$\Delta = m\sin(M - N)$" at "$T_1 = T_0 - (m/n)\cos(M - N)$" [@bes-chauvenet-1863]. The 1961 Supplement is more careful about the heliocentric angle. The geocentric separation is $\sigma = mg$ with $g = r/\Delta$, $\Delta$ the Earth-Mercury distance, and the minimum of $\sigma$ is where $m^2 g^2$ is a minimum [@tr-es1961]. The Supplement writes the separation $S$. It is $\sigma$ here because the corpus keeps $S$ for the ellipsoid auxiliary. The minimum is at the time correction

$$
t = -\frac{(u_0u'_0 + v_0v'_0)\,g_0^2 + m_0^2\,g_0 g'_0}{n_0^2 g_0^2 + 4(u_0u'_0 + v_0v'_0)\,g_0 g'_0 + m_0^2 g'^2_0}.
$$

Example 9.28 gives least geocentric distance "16h 53m 35s.2" E.T. with $m = 1130''.49$ and $\sigma = 528''.1$ [@tr-es1961]. Espenak's catalogue lists 527.9 arcseconds at 16:53 UT for the same transit [@tr-nasa-mercury-catalog].

### Position angles

The Supplement gives the [?position-angle-p|position angle] of a contact point "measured from the north point of the Sun's limb towards the east" as

$$
P = M \pm 180^{\circ} + V,\qquad \cos V = \cos\varepsilon\,\sec\delta_\odot ,
$$

where $V$ is the angle between the north point of the solar limb and the point nearest the north pole of the ecliptic, "in the first quadrant for November transits and in the fourth quadrant for May transits" [@tr-es1961]. The extra angle $V$ is needed because the heliocentric $M$ is measured from the ecliptic north. For 1960 November 7 interior egress, $V = 16^{\circ}.9$ and $P = 262^{\circ}.1$ [@tr-es1961]. Espenak and the IAA yearbook measure the same angle, "counterclockwise from the celestial north point" in Espenak's words [@tr-nasa-oh2012] [@tr-iaa-2019]. Their 2019 values agree to 0.05 degrees: 109.8, 109.8, 24.3, 298.8 and 298.7 degrees from Espenak against 109 degrees 51 arcminutes, 109 degrees 48 arcminutes, 24 degrees 17 arcminutes, 298 degrees 45 arcminutes and 298 degrees 43 arcminutes from the IAA [@tr-ew-tm2019] [@tr-iaa-2019].

## Local contacts

### The rigorous form in the 1961 Supplement

At a point on the Earth the heliocentric quantities change by small parallactic terms. The Supplement writes $u_1 = u + q$, $v_1 = v + p$, $L_1 = L + w$ and quotes Newcomb's expressions [@tr-es1961]:

$$
q = \pi_\odot(\rho\sin\phi'\cos\varepsilon - \rho\cos\phi'\sin\varepsilon\sin\tau_\mathrm{h})
$$
$$
p = \pi_\odot(-\rho\sin\phi'\sin\varepsilon\cos l_\oplus - \rho\cos\phi'\cos\varepsilon\cos l_\oplus\sin\tau_\mathrm{h} + \rho\cos\phi'\sin l_\oplus\cos\tau_\mathrm{h})
$$
$$
w = \pi_\odot\sin s_0\,(\rho\sin\phi'\sin\varepsilon\sin l_\oplus + \rho\cos\phi'\cos\varepsilon\sin l_\oplus\sin\tau_\mathrm{h} + \rho\cos\phi'\cos l_\oplus\cos\tau_\mathrm{h})
$$

Here $\rho\sin\phi'$ and $\rho\cos\phi'$ are the observer's [?rho-sin-phi|geocentric coordinates], $\varepsilon$ the obliquity, $\pi_\odot = 8''.80/R$ the Sun's horizontal parallax ($8''.794$ from 1968), and $\tau_\mathrm{h} = \mu - \lambda^*$ the local sidereal hour angle, with $\mu$ the ephemeris sidereal time of the geocentric contact and $\lambda^*$ the observer's ephemeris longitude [@tr-es1961]. The Supplement writes this angle as $\tau$. It is renamed $\tau_\mathrm{h}$ here because $\tau$ is already the time correction. Every local quantity then has "the general form $A + B\rho\sin\phi' + \rho\cos\phi'(C\sin\tau_\mathrm{h} + D\cos\tau_\mathrm{h})$", with $A, B, C, D$ "independent of the observer's position", so they "may be tabulated, together with $\mu$, for a particular transit" [@tr-es1961]. The local contact is found by the same $\tau$ formula with the local quantities. "The method outlined above is equivalent to Newcomb's ... rigorous solution", and is "suitable in all cases, including those in which the least angular distance of centres is nearly as great as the Sun's semi-diameter" [@tr-es1961]. That is, it works for grazing transits.

### The reduction formula

When the least distance is small compared with $s_0$, the Supplement linearises to a time correction $t$ that is itself of the general form, $t = B\rho\sin\phi' + \rho\cos\phi'(C\sin\tau_\mathrm{h} + D\cos\tau_\mathrm{h})$, with

$$
B = F\,(v\sin\varepsilon\cos l_\oplus - u\cos\varepsilon + G\sin\varepsilon\sin l_\oplus),
$$
$$
C = F\,(v\cos\varepsilon\cos l_\oplus + u\sin\varepsilon + G\cos\varepsilon\sin l_\oplus),\qquad
D = F\,(-v\sin l_\oplus + G\cos l_\oplus),
$$

where $F = 3600\,\pi_\odot/(uu' + vv')$ and $G = m\sin s_0$ [@tr-es1961]. The constants $F$ and $G$ are named in the worked example. Putting $C = \kappa\sin K$ and $D = \kappa\cos K$ gives the traditional [?tr-reduction-formula|reduction formula]

$$
\mathrm{UT} = T_c + B\rho\sin\phi' + \kappa\,\rho\cos\phi'\cos(K - \mu + \lambda + 1.002738\,\Delta T) - \Delta T
$$

"if $\lambda$ is the geographic longitude of the observer", with $B$ and $\kappa$ in seconds and "four such relations, one for each contact" [@tr-es1961]. The Supplement prints the amplitude as $k$. It is written $\kappa$ here because $k$ is the lunar radius ratio elsewhere in the corpus. Longitudes in the 1961 Supplement are positive west: the U.S. Naval Observatory is at $\lambda = +77^{\circ}\,03'.9$ [@tr-es1961].

Example 9.32 gives, for interior egress on 1960 November 7, $B = -6^{s}.55$, $C = +38^{s}.097$, $D = -32^{s}.451$, $\kappa = +50^{s}.04$, $K = 130^{\circ}\,25'.5$ and $\mu = 334^{\circ}\,39'.1$ [@tr-es1961]. At the Naval Observatory, with $\rho\sin\phi' = 0.6249$, $\rho\cos\phi' = 0.7791$ and ΔT = 36 s, the terms are $-4^{s}.1$ and $-23^{s}.5$. The local contact is 19h 10m 13s.2 E.T., or 19h 09m 37s.2 UT [@tr-es1961]. The rigorous method of Example 9.31 gives the same 19h 10m 13s.2 [@tr-es1961]. The example is a complete regression test for an implementation.

### Lagrange's method in Chauvenet

Chauvenet's own method for a place uses a point $G$ on the sky whose right ascension $A$ and declination $D$ are constants of the contact [@bes-chauvenet-1863]. Lagrange's result is that the apparent separation of centres at a place is $m' = m - g\rho\cos\chi$, where $\chi$ is the arc from the observer's zenith to $G$ and $g = \pi - \pi'$ is the difference of the horizontal parallaxes of the planet and the Sun [@bes-chauvenet-1863]. Chauvenet calls this "this remarkably simple form", and notes that on a spherical Earth "the apparent distance of the bodies is the same for all places ... whose zeniths are in a small circle described from the point G as a pole" [@bes-chauvenet-1863]. With $dm/dt = n\cos\psi$ at the contact, the local time is

$$
T' = T + \frac{\pi - \pi'}{n\cos\psi}\left[\rho\sin\phi'\sin D + \rho\cos\phi'\cos D\cos(\theta - \omega)\right],\qquad \theta = \mu - A ,
$$

with $\omega$ the west longitude and $\mu$ the sidereal time at the first meridian, so that $T' = T + B\rho\sin\phi' + C\rho\cos\phi'\cos(\theta - \omega)$ with constants $B$ and $C$ for each contact [@bes-chauvenet-1863]. For egress of the 1861 November 11 transit of Mercury he obtains, in Washington mean time,

$$
T' = 16^{h}\,12^{m}\,23^{s}.8 + 48^{s}.10\,\rho\sin\phi' + 26^{s}.23\,\rho\cos\phi'\cos(303^{\circ}\,20'.6 - \omega)
$$

and predicts egress at Altona at 22h 1m 10s.4 local mean time. "The time actually observed by Petersen and Pape was 22h 1m 8s.5" [@bes-chauvenet-1863]. Chauvenet credits the 1.9 s agreement to "the excellence of Le Verrier's Theory of Mercury" [@bes-chauvenet-1863].

### The yearbook form today

The IAA RAS yearbook prints the four formulas directly. For 2019 November 11 [@tr-iaa-2019]:

$$
T_1 = 12^{h}\,35^{m}\,26^{s}.3 + 13^{s}.44\,r\sin f' - 39^{s}.89\,r\cos f'\cos(275^{\circ}\,50'.9 + l)
$$
$$
T_2 = 12^{h}\,37^{m}\,07^{s}.7 + 13^{s}.42\,r\sin f' - 39^{s}.90\,r\cos f'\cos(276^{\circ}\,17'.7 + l)
$$
$$
T_3 = 18^{h}\,02^{m}\,32^{s}.0 + 19^{s}.46\,r\sin f' + 37^{s}.23\,r\cos f'\cos(176^{\circ}\,10'.3 + l)
$$
$$
T_4 = 18^{h}\,04^{m}\,13^{s}.5 + 19^{s}.44\,r\sin f' + 37^{s}.25\,r\cos f'\cos(176^{\circ}\,37'.3 + l)
$$

"In these formulae r denotes the geocentric radius of the Earth at that point in units of the equatorial radius, l denotes the longitude, f' denotes the geocentric latitude" [@tr-iaa-2019]. The yearbook does not state the sign of $l$. Substituting Murmansk's east longitude as positive into the 2016 formula for $T_1$ reproduces the tabulated 11h 11m 53s, and substituting it as negative gives a time 43 s later [@tr-iaa-2016]. The IAA convention is therefore east-positive, the opposite of the 1961 Supplement. For 2016 the Mercury coefficients are larger, for example $T_1 = 11^{h}\,12^{m}\,17^{s}.8 - 12^{s}.33\,r\sin f' - 111^{s}.60\,r\cos f'\cos(256^{\circ}\,20'.4 + l)$, because Mercury was nearer the Earth in May. The difference of the horizontal parallaxes of Mercury and the Sun was 15.79 − 8.71 = 7.08 arcseconds in 2016 against 13.01 − 8.88 = 4.13 arcseconds in 2019, and the relative motion was 240 against 355 arcseconds per hour [@tr-iaa-2016] [@tr-iaa-2019] [@tr-jubier-mtc-js].

IMCCE published the 2004 Venus coefficients in a third form, with $E$, $F$ and $G$ in minutes for each contact, longitude positive west, and the formula as an image [@tr-eso-eis-b1]. The form

$$
\Delta t = E\cos\phi\cos\lambda + F\cos\phi\sin\lambda + G\sin\phi
$$

with geographic latitude $\phi$ reproduces all four values of IMCCE's Paris example to 0.0003 minutes. For first external contact, $E = 6.4823$, $F = -0.0556$ and $G = 2.8992$ minutes give $\Delta t = 6.4474$ minutes and 5h 20m 0.0s UTC. IMCCE's rigorous value is 5h 20m 6.1s, and it states that the linear and rigorous results differ "of the order of the tenth of a minute" [@tr-eso-eis-b1]. This form drops the separate $\rho$ factors and so is good to a few seconds, not to the 0.1 s of the Supplement's form.

### The size of the parallax effect

For Venus, "the horizontal parallax of Venus (~30 arc-sec) introduces a topocentric correction of up to ±7 minutes with respect to the geocentric contact times" [@tr-nasa-venus0412]. For Mercury in 2019 local times "may differ from the geocentric times by up to 2 minutes" [@tr-ew-tm2019], and in 2006 by up to a minute [@tr-nasa-oh2006]. Espenak's catalogue visibility method, which uses geocentric times, can be wrong "up to 3 minutes for Mercury and up to 10 minutes for Venus" [@tr-nasa-visibility]. These are the amounts the reduction formulas recover. They are also the signal that Halley and Delisle exploited, treated in [Observations, the black drop and the solar radius](observations-black-drop-and-solar-radius.md).

### Northern and southern limits on the ground

The interior contacts exist only for an observer inside the umbral cone, and the exterior contacts only for one inside the penumbral cone [@tr-es1961]. In a grazing transit the edge of a cone crosses the Earth, and its trace on the ground is a limit line. Espenak describes it for 1999: "as one approaches the southern limit of the total transit, contacts II and III will converge and vanish" [@tr-nasa-oh1999]. IMCCE gives the related curve on which a contact occurs at the geocentric time as the intersection of the shadow cone with the terrestrial ellipsoid [@tr-imcce-vt2004-note1]. None of the sources of this topic prints a limit-line procedure for transits, so the construction that follows is derived here. Stellarium's transit elements $x, y, d, \mu, \tan f_1, \tan f_2, L_1, L_2$ have the meaning of the eclipse elements, with the planet-to-Earth radius ratio in place of the lunar $k$ [@tr-stellarium-transits]. The limit condition and the iteration of [Path and limits](../03-global-circumstances/path-and-limits.md) therefore apply as they stand: with $L_2$ and $\tan f_2$ for the limit of the interior contacts, and with $L_1$ and $\tan f_1$ for the limit of the exterior contacts. The Supplement puts the vertex of the umbral cone between the planet and the Earth [@tr-es1961], so the Earth lies beyond the vertex and the interior-contact zone has the geometry of an annular path.

Two differences from an eclipse matter in practice. The shadow radii are large. The penumbral radius in Earth radii is the sum of the semidiameters divided by the difference of the horizontal parallaxes. The IAA RAS values give about 135 Earth radii for Mercury in 2016 and about 236 in 2019. Espenak's rounded 2004 values give about 46 for Venus. The umbral radii are 1.7 to 2.7 Earth radii smaller. These radii are computed here [@tr-iaa-2016] [@tr-iaa-2019] [@tr-nasa-venus0412]. A limit therefore reaches the Earth only when the shadow axis passes within about one Earth radius of the cone's edge. This is the grazing case. The terms in the planet-to-Sun distance ratio are also large, so the exact point-Z formulas must be used [@bes-chauvenet-1863].

### Where each contact is visible

Espenak's visibility method tests the Sun's altitude $a$ at each geocentric contact, with

$$
\sin a = \sin d\sin\phi + \cos d\cos h\cos\phi,\qquad h = 15\,(\mathrm{GST} + t - \alpha) + \lambda ,
$$

where $d$ and $\alpha$ are the Sun's declination in degrees and right ascension in hours, GST the Greenwich sidereal time at 0h UT in hours, $t$ the UT of the contact in hours, $\lambda$ the longitude east-positive and $\phi$ the latitude [@tr-nasa-visibility]. The method neglects "the effects of atmospheric refraction and planetary parallax" [@tr-nasa-visibility]. Setting $a = 0$ gives the curve on which the Sun is on the horizon at that contact,

$$
\tan\phi = -\cot d\cos h ,
$$

which is the horizon circle of the subsolar point. The lunar-eclipse note writes the same great circle for the sublunar point in [Lunar eclipse enumeration, elements and contacts](../../30-lunar-eclipses/enumeration-elements-and-contacts.md). The rearrangement is derived here. Espenak puts the error of geocentric times at up to 3 minutes for Mercury and 10 minutes for Venus, or up to 1 degree and 2.5 degrees of solar altitude [@tr-nasa-visibility]. A map that must be better than that has to move each curve by the local parallax correction. At points near the geocentric curve, compute the local contact time with the rigorous form or the reduction formula above, evaluate the Sun's altitude at that local time, and solve for the point where it is zero. This refinement is derived here. It is not a published map procedure.

## ΔT and time scales

The elements are computed in TT and the contact times are published in UT. ΔT enters twice. It converts the time, and it converts the observer's longitude into an ephemeris longitude, because the Earth's rotation angle at a given TT depends on UT1. In the 1961 Supplement this appears as $\lambda^* = \lambda + 1.002738\,\Delta T$ inside the cosine and $-\Delta T$ outside it [@tr-es1961]. In Jubier's code the hour angles are `Hs = Ms - gLng - (SIDEREAL2SOLARTIME * deltaT)` with `SIDEREAL2SOLARTIME = 0.004178074622295` degrees per second, which is $1.002738 \times 15/3600$ [@tr-jubier-mtc-js]. The general treatment is in [ΔT and Earth rotation](../../10-shared/07-earth-and-time/delta-t-and-earth-rotation.md).

The ΔT values used for the same transit differ by predictor:

| Transit | Predictor | ΔT or offset stated |
|---|---|---|
| 2004 Venus | IMCCE | TT − UTC = 65.184 s [@tr-eso-eis-b1] |
| 2004 Venus | Jubier | 64.184 s and 64.635 s in the element array [@tr-jubier-vtc-js] |
| 2012 Venus | Jubier | 66.76 s [@tr-jubier-vtc-js] |
| 2016 Mercury | Jubier | 68.34 s [@tr-jubier-mtc-js] |
| 2019 Mercury | IAA RAS | TDT − UT1 = 70.0 s [@tr-iaa-2019] |
| 2019 Mercury | Jubier | 69.35 s [@tr-jubier-mtc-js] |

IMCCE's 65.184 s and Jubier's 64.184 s for 2004 differ by exactly one second, the size of a leap second. Espenak's 2016 and 2019 tables state UT1 but not ΔT [@tr-ew-tm2016] [@tr-ew-tm2019]. A one-second change in ΔT shifts every contact by one second and rotates the Earth under the geometry by 15.04 arcseconds, which matters only to the parallax terms.

## Constants: the solar and planetary radii

### What each source uses

| Source | $s_0$ (1 au) | Mercury (1 au) | Venus (1 au or km) |
|---|---|---|---|
| Explanatory Supplement 1961 [@tr-es1961] | 959.63″ | 3.34″ | not covered |
| Chauvenet [@bes-chauvenet-1863] | | $k = 0.3897$ Earth radii | $k = 0.9975$ Earth radii |
| Meeus, *Astronomical Algorithms* [@cat-meeus-1991-aa] | 959.63″ | 3.34″ old, 3.36″ later | 8.41″ old, 8.34″ later, 8.41″ preferred for transits |
| IMCCE 2004 [@tr-eso-eis-b1] | 959.63″ (IAU 1976) | | 6051.8 km |
| IAA RAS yearbooks [@tr-iaa-2016] [@tr-iaa-2019] | apparent values only | apparent values only | |
| Swiss Ephemeris `swevents` [@tr-swisseph-swevents] | 959.63″ | 3.36″ | 8.34″ |
| Jubier calculators [@tr-jubier-mtc-js] [@tr-jubier-vtc-js] | 959.62″ (comment 959.63) | 3.3558″ (comment 3.3629) | 8.3442″ (comment 8.41) |
| Stellarium [@tr-stellarium-ssystem] | 696 000 km | 2440.53 km | 6051.8 km |
| Espenak catalogues and articles | not stated | not stated | not stated |

Meeus explains the Venus choice: "the value 8".34 refers to the planet's crust, not to the top cloud level as seen from the Earth. For this reason, we prefer to use the older value 8".41 for Venus when calculating astronomical phenomena such as transits and occultations" [@cat-meeus-1991-aa]. At 1 au, 8.34 arcseconds is 6049 km and 8.41 arcseconds is 6100 km. Jubier's 8.3442 arcseconds is 6051.8 km, the IAU solid-body radius. The IAA yearbook prints only apparent semidiameters. Dividing them by Jubier's distances gives 959.62 and 959.63 arcseconds for the Sun and 3.365 and 3.366 arcseconds for Mercury in 2016 and 2019 [@tr-iaa-2016] [@tr-iaa-2019] [@tr-jubier-mtc-js].

The solar value 959.63 arcseconds is Auwers's 1891 heliometer result from the German Venus expeditions [@sun-auwers-1891]. The IAU 2015 nominal radius is 695 700 km, about 959.22 arcseconds [@sun-prsa-2016] [@sun-quaglia-2021], and eclipse-derived photospheric radii cluster near 959.95 arcseconds [@sun-quaglia-2021]. The full set of values and their definitions is in [Solar radius values](../06-solar-radius/solar-radius-values.md).

### How much the radii move the contacts

Differentiating the contact solution with respect to $L$, with $b = L\sin\psi$ the least separation, gives

$$
\frac{dt}{dL} = \pm\frac{L}{n\sqrt{L^2 - b^2}} = \pm\frac{1}{n\sqrt{1 - (b/L)^2}}
$$

in hours per arcsecond. This follows directly from the Supplement's $\tau$ formula [@tr-es1961]. The sensitivity depends only on the relative motion and on how central the transit is. It is smallest for a central transit and grows without limit for a grazing one.

![Per arcsecond of contact radius, an interior contact moves 10 seconds of time in the near-central 2019 Mercury transit and 21 seconds in the 2004 Venus transit. The curves are $3600/(n\sqrt{1-(b/L)^2})$ from the Explanatory Supplement contact solution, evaluated with $b$ and $n$ from the published tables [@tr-es1961] [@tr-eso-eis-b1] [@tr-nasa-oh2012] [@tr-ew-tm2016] [@tr-ew-tm2019] [@tr-jubier-mtc-js] [@tr-jubier-vtc-js].](img/tr-radius-sensitivity.svg)

With $b$ and $n$ from the published elements and minimum separations, and $L$ from $s_0 = 959.63$, Venus 8.34 and Mercury 3.36 arcseconds, the interior-contact sensitivities are 20.5 s per arcsecond in 2004, 18.8 in 2012, 15.9 in 2016 and 10.2 in 2019 [@tr-eso-eis-b1] [@tr-ew-tm2016] [@tr-ew-tm2019] [@tr-jubier-mtc-js] [@tr-jubier-vtc-js]. Raising $s_0$ from 959.63 to 959.95 arcseconds adds 0.31 to 0.32 arcseconds of apparent radius and moves each geocentric contact by:

| Transit | $b/L$ | $n$ (″/h) | Shift per contact for +0.32″ at 1 au |
|---|---|---|---|
| 2004 Venus | 0.684 | 240.5 | 6.5 s interior, 6.2 s exterior |
| 2012 Venus | 0.603 | 240.4 | 5.9 s interior, 5.7 s exterior |
| 2016 Mercury | 0.337 | 240.5 | 5.0 s |
| 2019 Mercury | 0.079 | 354.6 | 3.3 s |

Contacts I and II move earlier and III and IV later, so the duration between interior contacts grows by twice the tabulated shift. These shifts are larger than the 1 to 2 s agreement between modern predictors, so the radius is the dominant constant in a transit prediction once the ephemeris is modern.

### Predictor against predictor

The published geocentric contacts can be compared directly:

| Contact | Espenak 2004 [@tr-nasa-oh2004] | IMCCE 2004 [@tr-eso-eis-b1] | Difference |
|---|---|---|---|
| I | 05:13:29 | 05:13:33.2 | −4.2 s |
| II | 05:32:55 | 05:32:49.8 | +5.2 s |
| Greatest | 08:19:44 | 08:19:43.5 | +0.5 s |
| III | 11:06:33 | 11:06:37.1 | −4.1 s |
| IV | 11:25:59 | 11:25:53.8 | +5.2 s |

Espenak's contacts I and III are earlier and II and IV later, so his transit has longer ingress and egress phases and the same midpoint. A larger planet does exactly this. Changing the Venus semidiameter from 8.34 to 8.41 arcseconds at 1 au adds 0.242 arcseconds at the 2004 distance. By the formula above that moves exterior contacts out by 4.7 s and interior contacts in by 5.0 s. The observed differences are 4.1 to 4.2 s and 5.2 s. Neither Espenak's 2004 article nor his catalogues state his Venus semidiameter [@tr-nasa-oh2004] [@tr-nasa-catalog-key], but the pattern is consistent with Meeus's preferred 8.41 arcseconds [@cat-meeus-1991-aa] against IMCCE's stated 6051.8 km [@tr-eso-eis-b1].

For Mercury the predictors agree more closely:

| Contact | Espenak 2016 | IAA 2016 | Espenak 2019 | IAA 2019 |
|---|---|---|---|---|
| I | 11:12:19 | 11:12:17.8 | 12:35:27 | 12:35:26.3 |
| II | 11:15:31 | 11:15:29.7 | 12:37:08 | 12:37:07.7 |
| Greatest | 14:57:26 | 14:57:28.1 | 15:19:48 | 15:19:47.3 |
| III | 18:39:14 | 18:39:12.6 | 18:02:33 | 18:02:32.1 |
| IV | 18:42:26 | 18:42:24.5 | 18:04:14 | 18:04:13.5 |

Sources: [@tr-ew-tm2016] [@tr-iaa-2016] [@tr-ew-tm2019] [@tr-iaa-2019]. In 2016 Espenak's four contacts are 1.2 to 1.5 s later than the IAA's, a uniform shift of the kind a ΔT or ephemeris-time difference produces. His greatest transit is 2.1 s earlier, which suggests a different definition or a rounding of that instant. In 2019 all five of Espenak's values, rounded to the second, are 0.3 to 0.9 s later. The Handbook values quoted by the British Astronomical Association (BAA) for 2019, 12:35:26 and 18:04:14 UT with greatest transit at 15:19:47.4, sit between the two [@tr-baa-2019].

## Sources compared

| Source | What it gives that the others do not |
|---|---|
| Explanatory Supplement 1961, section 9F [@tr-es1961] | The cone membership that defines each contact, the rigorous local solution with Newcomb's $q, p, w$, the linearised $B, C, D$ with formulas, the reduction formula with ΔT, position angles with $V$, and worked examples to 0.1 s. |
| Chauvenet, Arts. 357 and 358 [@bes-chauvenet-1863] | Lagrange's method with the point $G$, a constant-per-contact reduction formula, and an 1861 prediction checked against an observation. |
| IAA RAS yearbooks [@tr-iaa-2016] [@tr-iaa-2019] | Current almanac reduction formulas for each contact, with ΔT and city tables that allow a sign check. |
| IMCCE for VT-2004 [@tr-eso-eis-b1] | Constants, $E, F, G$ coefficients and a rigorous worked example for Paris. |
| Espenak [@tr-nasa-oh2004] [@tr-nasa-oh2012] [@tr-ew-tm2016] [@tr-ew-tm2019] [@tr-nasa-visibility] | Geocentric contacts and position angles for each modern transit, and the Sun-altitude visibility test. No constants stated. |
| Meeus, *Astronomical Algorithms* [@cat-meeus-1991-aa] | The argument for 8.41 arcseconds for Venus in transit work. |
| Jubier calculators [@tr-jubier-mtc-js] [@tr-jubier-vtc-js] | Complete readable implementation with constants, ΔT and topocentric terms. |
| Stellarium [@tr-stellarium-transits] | Open-source local contacts in the solar-eclipse formulation. |
| Swiss Ephemeris `swevents` [@tr-swisseph-swevents] | A geocentric exterior-contact estimate only. |

## What a developer should do

1. Implement the contact solution with $L$ as an input built from explicit $s_0$ and planet semidiameter parameters. Default to $s_0 = 959.63$ arcseconds to match the almanacs [@tr-es1961] [@tr-eso-eis-b1], and expose it, since 959.95 arcseconds moves 2004-type Venus contacts by about 6 s.
2. Choose the Venus radius deliberately and say which. Use 6051.8 km to match IMCCE, Jubier and Stellarium [@tr-eso-eis-b1] [@tr-jubier-vtc-js] [@tr-stellarium-ssystem], or 8.41 arcseconds to follow Meeus [@cat-meeus-1991-aa]. The choice alone moves contacts by about 5 s.
3. Compute local circumstances by the rigorous route, either the Supplement's $A + B\rho\sin\phi' + \rho\cos\phi'(C\sin\tau_\mathrm{h} + D\cos\tau_\mathrm{h})$ form or a full topocentric vector computation. Use the reduction formula only as a published product or a check, and not near grazing transits [@tr-es1961].
4. Reproduce the 1961 Supplement's Examples 9.26 to 9.32 to 0.1 s, then the IAA 2016 and 2019 city tables to 1 s, then Espenak's geocentric contacts to the second with his ephemeris [@tr-es1961] [@tr-iaa-2016] [@tr-iaa-2019] [@tr-ew-tm2019].
5. For grazing transits, compute the limits of the interior and exterior contacts with the eclipse limit machinery and the planet's $L_1$, $L_2$. For visibility maps, start from the Sun's horizon circle at each geocentric contact and correct it with local contact times [@tr-nasa-visibility] [@tr-stellarium-transits].
6. Store the longitude sign convention with every published coefficient set. The IAA uses east-positive, the 1961 Supplement and Jubier use west-positive [@tr-iaa-2016] [@tr-es1961] [@tr-jubier-mtc-js].

## What this changes

The local-circumstance stage gains a second body type. The same $(u, v, u', v', L)$ solver serves eclipses and transits, but the transit stage needs both semidiameters as explicit inputs, and the planetary radius joins $s_0$ and $k$ in the metadata every prediction must carry. The validation stage gains a cheap regression set: the Supplement's 1960 examples and the IAA city tables.

## Open questions

- The 1961 Supplement's printed equation for the cone angles $f_1, f_2$: obtain a clean image of page 266 to confirm $f_2 = (s_0 - s)/r$ as inferred from Example 9.26 [@tr-es1961].
- Espenak's Venus and Mercury semidiameters: obtain his statement of constants, for example from the 2018 Canon, to confirm the 8.41 arcsecond inference from the 2004 comparison [@tr-espenak-2018-canon].
- The IAA RAS yearbooks do not name their ephemeris. Obtain the yearbook's introduction to record whether EPM was used and which version [@tr-iaa-2019].
- The origin of Jubier's 3.3558 and 3.3629 arcsecond Mercury values: 3.3558 arcseconds is 2434 km at 1 au, which matches no radius in the other sources. Ask the author or find a comment in his other code [@tr-jubier-mtc-js].
- Espenak's greatest transit in 2016 is 2.1 s earlier than the IAA's while his contacts are 1.3 s later. Obtain both predictors' definitions of greatest transit [@tr-ew-tm2016] [@tr-iaa-2016].
