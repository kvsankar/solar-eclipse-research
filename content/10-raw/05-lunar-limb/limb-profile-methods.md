---
title: Limb profile methods
description: From Watts' charts to LOLA point clouds, the geometry that produces a limb-height table for one observer at one instant, and what it changes in contact times and path limits.
order: 1
status: working
updated: 2026-09-15
tags: [lunar-limb, watts, lola, sldem2015, contact-times, path-limits]
---

::: summary
- **The Moon's silhouette departs from a circle by up to about 3 arcseconds**, about 6 km at the Moon, and that is enough to move second and third contact by 2 to 3 seconds anywhere in the path and by tens of seconds near the edges [@limb-espenak-limb-page] [@limb-herald-1983].
- **Watts' 1963 charts** were the only limb data for half a century. They are 1800 contour charts at 0.2 degree steps in Watts angle, with a datum that is elliptical, offset from the centre of mass and libration-dependent, so they need the Morrison and Appleby 1981 corrections of up to 0.4 arcseconds [@limb-vizier-vi122] [@limb-morrison-appleby-1981].
- **Modern profiles come from laser-altimeter DEMs**: Kaguya (SELENE) LALT at 16 pixels per degree and LRO LOLA LDEM or SLDEM2015 at up to 512 pixels per degree, all as heights above a 1737.4 km sphere centred on the centre of mass in the mean Earth/polar axis frame, so the centre-of-figure correction disappears [@limb-lola-ldem128-label] [@limb-lalt-ggt-map-label].
- **The profile is observer- and time-dependent.** It is built by rotating the DEM point cloud into the observer's line of sight using the topocentric libration and keeping, in each position-angle bin, the point of largest angular radius [@limb-wright-young-2024] [@limb-svs-4517].
- **Herald 1983 gives the contact-time correction**: plot the Sun's limb as $h = 960''(M-1)(1-\cos C)$ against the lunar profile, with $C$ the angle from the contact point, and convert the radial displacement to time with the relative rate $r\cos(\mathrm{PA}-N)$. Espenak's symbol is $C$. Herald writes $P$, which is not the position angle [@limb-herald-1983].
- **Path limits move by kilometres**: Espenak's 2001 bulletin tabulates interior and exterior corrections up to 4 arcmin of latitude and defines a 5 to 10 km graze zone. Wright's 2017 umbra is a 49-sided polygon, each side one lunar valley [@limb-espenak-tp2001] [@limb-wright-young-2024].
- **Accuracy today** is about 0.2 to 0.3 s in contact times with LOLA profiles, against 0.5 s with corrected Watts data [@limb-eclipsewise-limb] [@limb-occult-accuracy-2016].
:::

**The question.** An eclipse computed with Besselian elements treats the Moon as a sphere of radius $k$ Earth radii. The real limb has mountains and valleys. This note answers how the limb profile has been measured, how a developer turns a digital elevation model into a table of limb height against position angle for a given observer and instant, how that table modifies contact times and path limits, and which implementations do what.

## History: Watts and the corrections to Watts

Chester B. Watts of the US Naval Observatory completed a photographic survey of the Moon's marginal zone in 1956 and published it in 1963 as Volume XVII of the Astronomical Papers of the American Ephemeris [@limb-morrison-appleby-1981] [@limb-watts-1963]. The survey used 503 photograph sequences taken between 1927 and 1956 at Washington, Johannesburg and Flagstaff [@limb-vizier-vi122]. Watts built a machine that traced the limb on some 700 photographs across the full range of visible librations, an effort of 17 years [@limb-svs-4517] [@limb-vizier-vi122].

The product is 1800 charts, one for each 0.2 degrees of [?watts-angle|Watts angle] around the limb, each chart giving height contours at an interval of 0.2 arcseconds as a function of libration in longitude $L$ from $-9^{\circ}$ to $+9^{\circ}$ and latitude $B$ from $-8^{\circ}$ to $+8^{\circ}$ [@limb-vizier-vi122]. Heights are with respect to an adopted smooth reference surface, the [?watts-datum|Watts datum] [@limb-morrison-appleby-1981]. The digitised version, produced by HMNAO and reformatted by USNO, stores one 6-byte record per grid point with the height in units of 0.01 arcseconds and two accuracy codes. The record index is

$$\mathrm{Record} = 729000\,(9.0 - L) + 9000\,(8.0 - B) + 5\,\mathrm{WA} + 1$$

for 91 longitude blocks, 81 latitude blocks and 1800 Watts-angle points per block, 13,267,800 records in all [@limb-vizier-vi122].

The Watts angle is not the true [?position-angle-of-axis|axis angle]. The VizieR documentation states that 0.21 degrees must be added to a computed axis angle to obtain the corresponding Watts angle, and that Watts used a lunar equator inclination of 1.564 degrees against the current 1.542 degrees, requiring a further term $-0.022\cos(L - W)$ in degrees, with $L - W$ the lunar elongation [@limb-vizier-vi122]. Morrison and Appleby entered the charts with the argument $Q + 0.25^{\circ}$ following Morrison 1970 [@limb-morrison-appleby-1981]. Solar Eclipse Maestro corrects a 0.241 degree difference between Watts angles and the axis angle [@limb-jubier-sem-limb-window]. A developer using Watts data must pick one of these and say which.

### Systematic errors and the Morrison and Appleby corrections

Occultation analyses by Van Flandern in 1970 and Morrison in 1979 showed that the average cross-section of Watts' datum is slightly elliptical and that its implicit centre, the [?centre-of-figure|centre of figure], is displaced from the point the lunar ephemeris tracks [@limb-morrison-1979] [@limb-morrison-appleby-1981]. Morrison and Appleby then analysed 66,000 occultation timings from 1943 to 1979 and found that the radius, shape and centre of the datum all vary with libration, producing errors that reach 0.4 arcseconds at some position angles [@limb-morrison-appleby-1981].

Their reduction assumed a datum radius of 1737.97 km, equivalent to a semi-diameter of 932.58 arcseconds at the mean distance corresponding to an equatorial horizontal parallax of 3422.608 arcseconds [@limb-morrison-appleby-1981]. The correction they derive is to be added to Watts' heights when the charts are used with a centre-of-mass ephemeris. It is a second-order harmonic in the position angle $Q$ measured eastward from the projected north pole:

$$\Delta h = \delta r_0 + \delta x \sin Q + \delta y \cos Q + \delta r_2 \cos 2(Q - 146^{\circ})$$

where the four coefficients are read from their Figure 3 as functions of libration [@limb-morrison-appleby-1981]. The mean values over all librations are $\delta r_0 = +0.04$ arcseconds, $\delta y = -0.18 \pm 0.01$ arcseconds, and $\delta r_2 \approx -0.09$ arcseconds [@limb-morrison-appleby-1981]. Watts had already moved his original datum 0.3 arcseconds along position angle 333 degrees. He had also applied an ellipticity term of $+0.15'' \cos 2(Q - 153^{\circ})$, and the analysis shows it should have been about $+0.06''$ [@limb-morrison-appleby-1981]. For the displacement between centre of figure and centre of mass in orbital longitude they recommend adding a further $+0.50'' \sin Q$, uncertain by about 0.2 arcseconds. The occultations themselves give 0.72 arcseconds and Apollo laser altimetry gives about 1 km, or 0.5 arcseconds, with the centre of figure leading the centre of mass in longitude in every solution [@limb-morrison-appleby-1981]. Espenak's bulletins apply exactly these corrections, for centre of mass and ellipticity, and state that the aim is to make the datum a sphere centred on the centre of mass [@limb-espenak-tp2001].

Later refinements by Rosselló and Jordi in 1991 gave a datum radius of 1738.103 km [@limb-sigismondi-thesis-2011]. Solar Eclipse Maestro uses the Watts profile corrected first by Morrison and Appleby and then by Rosselló and Jordi [@limb-jubier-sem-limb-window]. The precision of an individual Watts height is about 0.20 arcseconds and was treated as random [@limb-sigismondi-thesis-2011].

### IOTA and the eclipse edge

Duncombe published selected Watts-derived profiles in 1973 for eclipse observers [@limb-herald-1983]. In 1979 Sofia, Dunham and Fiala proposed observing a solar eclipse the way one observes a grazing occultation: stand on the predicted edges of the umbral track, time the formation and disappearance of individual [?bailys-beads|Baily's beads], identify each with a Watts limb feature, and solve for the apparent solar diameter and the Sun's position relative to the Moon [@limb-fiala-dunham-sofia-1994]. Herald's 1983 paper gave the graphical procedure for correcting contact times with these profiles and thanked Fiala of USNO [@limb-herald-1983]. The first published result, from eclipses of 1715, 1976 and 1979, appeared in Science in 1980 [@limb-dunham-1980-science]. Fiala, Dunham and Sofia reported in 1994 that "the precision and accuracy of the observations depends upon Watts' limb profile data," and looked forward to "improved lunar limb data" from orbiting laser altimeters [@limb-fiala-dunham-sofia-1994]. That data arrived with Kaguya in 2009 and LRO in 2010, and Dave Herald reduced limb profiles from it for Occult [@limb-eclipse-orchestrator-lro] [@limb-sigismondi-thesis-2011].

## Modern DEMs in one paragraph

The datasets are described fully in [Datasets: Watts, Kaguya, LOLA](datasets-watts-kaguya-lola.md). The facts that matter for the geometry are these. Kaguya's LALT global grid is 16 pixels per degree, 1.895 km per pixel, heights in kilometres above a 1737.4 km sphere centred on the centre of mass in the mean Earth/polar axis frame of DE421 [@limb-lalt-ggt-map-label]. LRO's LOLA LDEM series is gridded at 4, 16, 64, 128, 256 and 512 pixels per degree, with 128 pixels per degree being 236.901 m per pixel, heights in metres stored as 16-bit integers with a scaling factor of 0.5 above the same 1737.4 km sphere in the same frame [@limb-lola-ldem128-label] [@limb-lola-gdr-dscat]. SLDEM2015 merges LOLA with Kaguya Terrain Camera stereo between 60 S and 60 N at 512 pixels per degree, about 60 m, with a typical vertical accuracy of 3 to 4 m [@limb-ode-sldem] [@limb-sldem2015-label]. Because every one of these grids is relative to a sphere centred on the [?centre-of-mass|centre of mass], the centre-of-figure correction that dominated the Watts era is not applied. The offset itself is 1.9347 km toward 7.12 N, 202.38 E according to LOLA, a value taken secondhand from Smith et al. 2010 rather than from the paper [@limb-smith-2010-lola].

## From DEM to limb profile: the geometry

### What the limb is

For an observer at distance $d$ from the Moon's centre, the limb is the set of surface points that are farthest from the line of sight in angular terms. On a sphere it is the great circle 90 degrees from the [?sub-observer-point|sub-observer point], slightly less than 90 degrees at finite distance since $\cos\psi = R/d$ gives $\psi \approx 89.74^{\circ}$ for $R = 1737.4$ km and $d = 384{,}400$ km. On the real Moon a mountain 3 degrees behind the geometric limb can still project beyond a valley on it, so the limb point at a given position angle must be found by search, not by reading the DEM at $\psi = 90^{\circ}$. The astronomy-bundle implementation searches $\psi$ from 87 to 93 degrees in 0.02 degree steps along each position angle and keeps the maximum apparent radius [@limb-andrmoel-lunar-limb-profile]. Wright and Young keep the maximum over all DEM points falling in each angle bin. That is the same search applied to the whole point cloud [@limb-wright-young-2024].

![The Moon's silhouette departs from a circle by up to about three arcseconds, so second contact is fixed not by the mean limb but by whichever valley is the last to let sunlight through and whichever peak is the first to cut it off [@limb-espenak-limb-page] [@limb-herald-1983].](img/limb-profile.svg)

### Wright and Young's procedure

The clearest published description is in [Wright and Young 2024](../11-svs-wright/wright-2024-paper.md), which is also the method behind the NASA SVS 2017 and 2024 maps. The steps are, in their words paraphrased closely [@limb-wright-young-2024] [@limb-svs-4517]:

1. Convert each DEM pixel to rectangular coordinates in the Moon body-fixed frame. Because LDEM and SLDEM heights are relative to a spherical datum and the latitude is planetocentric, the conversion is direct: with radius $R = 1737.4\ \mathrm{km} + h$, longitude $\lambda$ and latitude $\varphi$, $x = R\cos\varphi\cos\lambda$, $y = R\cos\varphi\sin\lambda$, $z = R\sin\varphi$.
2. Apply a rotation matrix that encodes the [?topocentric-libration|topocentric libration] at the observer, so that the $x$ axis points from the Moon's centre to the observer.
3. Convert each transformed point's $(y, z)$ to polar form $(r, \theta)$ and compute its angular radius as seen by the observer, $\alpha = \tan^{-1}\!\big(r/(d - x)\big)$, where $d$ is the observer's distance from the Moon's centre.
4. Bin $\theta$ into $L$ equal intervals and store in each bin the largest $\alpha$. "An $L$ of 18,000 elements has a resolution of 0.02° (roughly 600 m) and pairs well with DEMs of 240 m resolution."
5. Regenerate the profile "at time steps of a few minutes, or whenever a libration angle has changed by some small threshold, say 0.01°."

The SVS page describes the same computation in the language of the fundamental plane: "each point in an elevation map is transformed into 3D cartesian coordinates in a Moon body-fixed frame. At each time step in the eclipse calculation, the point cloud is rotated into fundamental plane coordinates. The limb profile then comprises the set of points lying farthest from the shadow axis" [@limb-svs-4517]. The topocentric libration and the observer's distance are obtained in the paper's Appendix A by a SPICE sequence: subtract the Moon's position from the observer's, rotate the vector with the Moon ME frame matrix, and take `reclat_c` to get distance, longitude and latitude [@limb-wright-young-2024]. The lunar orientation kernels named are `moon_pa_de440_200625.bpc` and `moon_de440_200625.tf` with `de440.bsp` for positions, the 2020 release of that frame kernel. NAIF's current file is `moon_de440_250416.tf` [@limb-wright-young-2024].

The angular radius of the reference sphere for the same observer is $\alpha_0 = \sin^{-1}(R_0/d)$ with $R_0 = 1737.4$ km. The limb height at bin $i$ is then $\Delta_i = \alpha_i - \alpha_0$, in radians, or in arcseconds after multiplying by 206265. To express it against the conventional mean limb instead, replace $R_0$ by $k R_\oplus$ with $k = 0.2725076$ and $R_\oplus = 6378.137$ km, which gives 1738.09 km, the value Solar Eclipse Maestro quotes for the IAU mean radius [@limb-jubier-sem-limb-window]. The 0.69 km difference between the DEM sphere and the $k$ sphere is 0.37 arcseconds at mean distance and is a constant offset in every limb height, so it must be applied consistently or the corrected contact times inherit it.

### The astronomy-bundle formulation

The TypeScript package works per position angle rather than over the whole cloud. It converts the requested celestial position angle to an angle from lunar north by subtracting the position angle of the axis. It then builds an orthonormal frame at the sub-observer point from the libration longitude and latitude. For each $\psi$ along that direction it samples the DEM bilinearly and computes the apparent radius in metres as

$$\rho_{\mathrm{app}} = \frac{R_s \sin\psi \, D}{D - R_s \cos\psi}$$

where $R_s = 1737400 + h$ is the surface radius and $D$ is the observer distance, returning $(\max\rho_{\mathrm{app}} - \rho_{\mathrm{ref}})/1000$ in kilometres [@limb-andrmoel-lunar-limb-profile]. This quantity is a projected length in the plane through the Moon's centre perpendicular to the line of sight, and dividing by $D$ gives the small-angle equivalent of Wright's $\tan\alpha$. The package defaults to `ldem_16` and suggests `ldem_64` for finer detail [@limb-andrmoel-lunar-limb-profile].

### Resolution: what a DEM cell is worth at the limb

At the Moon's mean distance one arcsecond is 1.863 km [@limb-espenak-limb-page] [@limb-herald-1983]. Kaguya's 16 pixels per degree grid, 1.895 km per pixel, therefore samples the limb at about one arcsecond. Sigismondi quotes the LALT track data as "a sampling each 1.5 km (about 1 arcsecond at the lunar distance)" [@limb-sigismondi-thesis-2011]. LDEM_128 at 237 m per pixel is 0.13 arcseconds. SLDEM2015 at 59 m is 0.03 arcseconds. The Moon moves relative to the Sun at 0.3 to 0.5 arcseconds per second during a central eclipse, for example 0.364 arcseconds per second in Espenak's 2001 example [@limb-espenak-tp2001], so one LDEM_128 cell is worth about 0.3 to 0.4 s of contact time and one Kaguya grid cell is worth 2 to 3 s. That is why Occult and Eclipse Orchestrator went back to the raw altimeter shots rather than the 16 pixels per degree grid: Eclipse Orchestrator's limb file was built from about 434 million filtered LOLA RDR points merged with Kaguya, and missed mountains in either dataset alone changed 2010 contact times by up to 0.5 s [@limb-eclipse-orchestrator-lro]. Wright's choice of 0.02 degree bins with a 240 m DEM matches the bin width to the cell size at the limb.

The vertical accuracy of the DEMs, 3 to 4 m for SLDEM2015 and about 1 m absolute for individual LOLA shots, is negligible at 0.002 arcseconds [@limb-ode-sldem] [@limb-pgda-sldem2015]. The residual error in a modern profile is horizontal, from which cell happens to fall on the limb, and from the libration and orientation model.

### Dependence on the observer

Every observer has a distinct topocentric libration and therefore a distinct profile. Wright and Young judge that "the differences for observers near each other are vanishingly small relative to the finite resolution of the limb profile," and compute one profile for the observer on the shadow axis, refreshing it every few minutes or whenever a libration angle changes by 0.01 degrees [@limb-wright-young-2024]. Along a whole path the change is not small: Espenak's 2001 bulletin notes the topocentric libration in longitude ranging from $-3.1^{\circ}$ to $-4.6^{\circ}$ along the path and states that "a limb profile with the appropriate libration is required in any detailed analysis of contact times, central durations, etc." [@limb-espenak-tp2001]. For the path limits he adds that "a single correction at each limit is not possible since the Moon's libration in longitude and the contact points of the limits along the Moon's limb each vary as a function of time and position along the umbral path" [@limb-espenak-tp2001].

Near the path edge the sensitivity is different in kind. The profile hardly changes over a few kilometres, but the contact point does: at the edge the Sun's limb is tangent to the lunar profile over a wide arc of position angle, so a small lateral move changes which valley is the last to show light. Herald's error analysis captures this with a factor $\sec(\mathrm{PA} - N)$ that multiplies every timing uncertainty as the site moves from the central line toward the limits [@limb-herald-1983]. Occult's 2016 update found that an error of only about 0.2 degrees in the computed position angle of an event corrupted the limb correction enough to explain its residuals [@limb-occult-accuracy-2016].

## The correction to contact times

### Herald's displacement-curve method

Herald 1983 is the algorithm that every implementation automates. Second and third contacts are the instants when the solar limb is tangent to the lunar limb without intersecting it. On a chart with the radial scale exaggerated about 70 times, the Sun's limb near the contact point can be drawn relative to the mean lunar limb as

$$h = 960''\,(M - 1)\,(1 - \cos C)$$

where $M$ is the [?eclipse-magnitude|eclipse magnitude] and $C$ the angle from the point of nominal contact, Espenak's symbol. Herald writes that angle $P$, which is not the position angle. The formula assumes a mean solar radius and errs by no more than 2 per cent in $h$ [@limb-herald-1983]. Espenak writes the same curve as $h = s_0(m-1)(1-\cos C)$ with $s_0$ the Sun's semidiameter, for which his own text uses the letter $S$ [@limb-espenak-tp2001]. The curve is drawn on tracing paper, slid radially along the line from the Moon's centre until it is tangent to the lowest valley for a total eclipse, or the highest peak for an annular one, and the radial displacement $XX'$ is read off in arcseconds [@limb-herald-1983].

The displacement is converted to time with the Moon's radial rate relative to the Sun. Herald gives

$$r = \frac{\pi n}{3600}\ \text{arcseconds per second} \approx 0.97\,M\,n$$

with $\pi$ the topocentric lunar parallax in arcseconds and $n$ the shadow's speed relative to the observer on the fundamental plane in Earth radii per hour, and, where $n$ is not available, $n = \pm 3900(1-M)/\big(d(1+M)\big)$ from the central duration $d$ in seconds [@limb-herald-1983]. The rate along a position angle $\mathrm{PA}$ is

$$r\cos(\mathrm{PA} - N)$$

where $N$ is the direction of apparent relative motion, obtainable as $\arctan(u'/v')$ from the Besselian rates or as the mean of the C2 and C3 position angles plus or minus 90 degrees [@limb-herald-1983]. Espenak's equation [9] states the time correction as the displacement divided by this rate,

$$\tau = \frac{d}{v\cos(X - C)}$$

with $d$ the radial distance of the solar limb from the mean limb in arcseconds, $v$ the relative angular velocity in arcseconds per second, $X$ the central-line contact position angle and $C$ the angle from the contact point [@limb-espenak-tp2001]. His worked example for Lusaka on 2001 June 21 reads corrections of $+4.0$ s at second contact and $-1.2$ s at third contact from the chart, "within 0.2 seconds of a rigorous calculation using the actual limb profile" [@limb-espenak-tp2001].

### The digital version

With a digital profile the tangency search is a loop. For each bin $i$ of the profile with height $\Delta_i$ above the mean limb, the time at which the Sun's limb reaches that point is the nominal contact time plus $(\Delta_i - h_i)/(v\cos(X - \theta_i))$, with $h_i$ the epicyclic departure at that bin. Second contact of a total eclipse is the latest of these over the bins near $X$, since totality begins only when the last valley darkens, and third contact is the earliest. For an annular eclipse the extrema swap. Wright and Young avoid the tangency construction entirely and test totality directly at each pixel and time step. The scale $s = (d_0/d)/r_\odot$ converts the profile radii $L_i$ into units of the solar radius, so that $a = sL_i$. The element's position angle is $\theta = 2\pi i/n + c$ with $c$ the position angle of the lunar axis. With $\delta$ and $\varphi$ the Sun's separation and position angle from the Moon's centre in the same units,

$$\rho = a^2 + \delta^2 - 2a\delta\cos(\theta - \varphi)$$

and the eclipse is not total at that pixel if any $\rho < 1$ [@limb-wright-young-2024]. Two quick tests bracket the search: if $s\max(L) - \delta < 1$ the observer is outside the umbra, and if $s\min(L) - \delta \geq 1$ the observer is inside [@limb-wright-young-2024]. Contact times fall out as the first and last time steps at which the pixel passes.

## Effect on eclipse products

### Contact times and central duration

Without limb corrections, contact times and durations "may be in error by as much as 2 to 3 seconds (and more near the path limits where the geometry is far more critical)" [@limb-espenak-limb-page]. With corrected Watts data agreement is "better than 0.5 seconds" [@limb-espenak-limb-page]. Kaguya and LRO data bring this "to the ~0.2 second level" [@limb-eclipsewise-limb]. Herald puts the uncorrected error at "tens of seconds at locations well away from the central line" [@limb-herald-1983]. Occult's occultation predictions, which use the same profile machinery, are mostly within 0.3 s of observation once the LOLA limb is installed [@limb-occult-accuracy-2016]. Jubier's map help says the limb correction "can produce a few seconds time difference on the start and end of totality or annularity" [@limb-jubier-map-help].

Sigismondi's thesis gives a concrete Watts-versus-Kaguya comparison for Hao atoll on 2010 July 11. Occult 4 with Watts predicted C2 at 18:37:43.8 and C3 at 18:38:08.6 UT, a duration of 24.8 s. Occult 4 with Kaguya gave 18:37:41.6 and 18:38:12.2, a duration of 30.6 s. An IMCCE Kaguya computation referred to the centre of mass gave 18:37:43.4 and 18:38:11.3, a duration of 27.98 s. He attributes the spread to the different datum radii and centre choices and prefers the centre-of-mass Kaguya result [@limb-sigismondi-thesis-2011]. Espenak's Table 6 for 2001 lists corrections to the central-line duration between $-1.8$ s and $+0.3$ s across the path, mostly positive, because his umbral computation already uses the reduced $k = 0.272281$ [@limb-espenak-tp2001].

The two $k$ values are part of this story. Their full history and which published table prints which value are in [Besselian elements](../01-foundations/besselian-elements.md), and this paragraph keeps only what the limb stage needs. From 1968 to 1980 the Nautical Almanac Office used $k = 0.2724880$ for penumbral contacts and $k = 0.272281$, a mean minimum radius, for umbral contacts of total eclipses [@limb-espenak-tp2001]. The IAU adopted $k = 0.2725076$ in 1982 for all purposes. Espenak's bulletins keep the IAU value for exterior contacts and the smaller value for interior contacts, because the IAU mean "guarantees that some annular or annular-total eclipses will be misidentified as total" [@limb-espenak-tp2001]. His example is 1986 October 3, listed as a 3 s total eclipse that was in fact beaded annular [@limb-espenak-tp2001]. Herald's Table I gives the limiting magnitudes: a true total eclipse needs magnitude at least 1.0016 at longitude libration $-5^{\circ}$ or 1.0027 at $+5^{\circ}$, and a true annular eclipse needs magnitude at most 0.9981 or 0.9979 [@limb-herald-1983].

### Path limits and the graze zone

Espenak states that his northern and southern limits are computed for the centre of mass and a mean radius and "have not been corrected for the Moon's center of figure or the effects of the lunar limb profile" [@limb-espenak-tp2001]. Table 6 of the 2001 bulletin then tabulates, every five minutes, interior and exterior corrections to each limit in minutes of arc of latitude: at 12:00 UT the northern limit moves $-0.4'$ (interior) and $+0.8'$ (exterior) and the southern limit $+1.5'$ (interior) and $-2.8'$ (exterior), with southern exterior values reaching $-4.1'$ earlier in the path [@limb-espenak-tp2001]. One minute of latitude is 1.85 km, so these are shifts of 1 to 8 km. The [?graze-zone|graze zone] between interior and exterior boundary "is typically five to ten kilometers wide" [@limb-espenak-tp2001]. The interior boundary is where "no photospheric beads are visible along a ±30° segment of the Moon's limb, symmetric about the extreme contact points at the instant of maximum eclipse" [@limb-espenak-tp2001]. The exterior boundary is where "an unbroken photospheric crescent of 60° in angular extent is visible" [@limb-espenak-tp2001]. He gives the accuracy of these graze coordinates as ±0.3 arcseconds given the Watts uncertainties, tells observers to stand at least 1 km inside the interior limit, and notes that the most dynamic beading occurs within 1.5 arcseconds of the lunar limb, about 3 km with a scale factor of 2 km per arcsecond [@limb-espenak-tp2001]. Dunham's graze predictions for stars use a 2 to 3 km wide zone for the same geometry [@limb-dunham-rasc-2026]. IOTA eclipse-edge teams place stations 1 to 3 km inside the path [@limb-eclipsetours-edge].

Herald converts a limb displacement at the limit into a ground distance with

$$(1.863\ \mathrm{km}/'')\sqrt{\frac{\sin^2 D}{\sin^2 a} + \cos^2 D}$$

where $a$ is the Sun's altitude and $D$ the difference between the Sun's azimuth and the azimuth of the limit line, and estimates the resulting uncertainty in the location of a limit at about ±0.6 km from limb data alone and ±1 km overall [@limb-herald-1983]. Espenak's elevation factor for the same purpose is $\tan(90^{\circ} - A)\sin D$ metres of shift per metre of height [@limb-espenak-tp2001].

### The polygonal umbra

The SVS 2017 visualisation was the first to draw the umbra's true outline: "an irregular polygon with slightly curved edges. Each edge corresponds to a single valley on the lunar limb, the last (or first) spot on the limb that lets sunlight through," and an observer at a cusp between two edges sees a double diamond ring [@limb-svs-4517]. At 18:00 UTC on 2017 August 21 "the outline of the umbra at this time is a polygon with 49 sides" [@limb-wright-young-2024]. Earth elevation adds a second deformation, shifting the 2017 umbra toward the Sun's azimuth "by as much as 3 kilometers" over the western states [@limb-svs-4517], with the general rule that the shift is roughly $h\cot a$ for observer height $h$ and Sun altitude $a$ [@limb-wright-young-2024]. The 2024 map and its released umbra polygons at 1 s intervals were computed the same way with LOLA, SLDEM2015, SRTM and DE421 [@limb-svs-5073] [@limb-svs-5219]. Polygonal edges can even re-enter: a 2026 Greenland site computed by John Irwin sees about 9 s of totality interrupted by about 2 s of partiality, and the outcome flips with a 0.05 arcsecond change in solar radius [@limb-besselianelements-reentrant].

### The solar radius couples to everything

Wright and Young adopt 696,000 km, 959.63 arcseconds at 1 au, and note that "a discrepancy of 1 s in duration, for example, corresponds to an error as small as 20 km (0″.03) in solar radius" [@limb-wright-young-2024]. Jubier's calculator uses the same IAU 1976 value while stating that the true photospheric radius is closer to 959.98 ± 0.02 arcseconds [@limb-jubier-map-help]. The 0.35 arcsecond difference is comparable to the whole Watts correction budget and larger than any modern limb-profile error, which is why [Baily's beads](bailys-beads.md) treats the two together.

## Software and code

- **Occult 4** (Dave Herald, IOTA). Ships the Watts profile and the Kaguya and LOLA profiles as separate downloads, and the LOLA limb is download #26 [@limb-occult-accuracy-2016]. For graze and eclipse profiles the current instruction is to select LOLA with the HiRes option and leave Observed data at None, since the observed corrections were only useful with Watts [@limb-iota-2026-predictions]. The profile calculation is described as computer-intensive [@limb-iota-2026-predictions]. Occult's internal file format for the Kaguya and LOLA limb data is not documented on any page found. The Eclipse Orchestrator description of a limb file built from filtered altimeter shots is the closest public account of that kind of product [@limb-eclipse-orchestrator-lro].
- **Solar Eclipse Maestro** (Xavier Jubier). Computes contacts from Besselian elements, then a limb correction from LRO LOLA RDR and Kaguya data, with the Morrison/Appleby and Rosselló/Jordi corrected Watts profile for comparison [@limb-jubier-sem-limb-window]. The profile window shows heights in arcseconds against $k = 0.2725076$ on an axis-angle abscissa at 14400 by 400 pixels and marks C2, C3, C2' and C3'. It exports the profile "for the current topocentric libration" as a text file [@limb-jubier-sem-limb-window] [@limb-jubier-sem-beads-window]. Jubier's online map gives the correction as an LC column in seconds and requires an internet connection for it [@limb-jubier-map-help].
- **NASA SVS** (Ernie Wright). The algorithm is published in Wright and Young 2024 with SPICE pseudocode in Appendix A, and the code itself is not released. Released data are shapefiles and KML of the central line, duration contours, obscuration contours, `umbra_hi` polygons at 1 s and `umbra_lo` at 10 s, and city times, with a Zenodo DOI. No limb-profile table is among them [@limb-svs-5073] [@limb-wright-young-2024].
- **Eclipse Orchestrator** (Moonglow Technologies). A 6 MB limb file derived from LOLA RDR and Kaguya track data, merged by hand after plotting both against each other [@limb-eclipse-orchestrator-lro].
- **astronomy-bundle-js / lunar-limb-profile** (npm). One of two open codes found that derive limb height from an LDEM file with libration and axis angle as inputs. The other is tomasrojasc/eclipse-2026, and the inventory is in [GitHub repositories](../09-software-and-repos/github-repositories.md). The package documents no validation against timings [@limb-andrmoel-lunar-limb-profile].
- **LTVT**. Reads the Kaguya LALT_GGT_MAP grid and the 64 pixels per degree polar grids for visualisation, not for eclipse timing [@limb-ltvt-kaguya-wiki].
- **Stellarium**. The project's issue tracker records no work on a lunar limb profile, and the program carries no limb model [@limb-stellarium-issues]. No public Python package builds an eclipse limb profile from LOLA or Kaguya; the tools published under those terms, and under the Watts profile, are crater-cutout and geology utilities. Both are negative findings rather than gaps in coverage.

## A worked pipeline

Inputs: instant $t$ in TT, observer geodetic coordinates and height, a planetary ephemeris (DE440 or DE421), a lunar orientation model consistent with it, a DEM (LDEM_128 for a first build, SLDEM2015 at 128 or 256 pixels per degree for production), and the mean-limb prediction of C2, C3, their position angles $X$, the relative rate $v$ and the magnitude $M$.

1. Form the observer's position in the ICRF from geodetic coordinates and Earth orientation, subtract the Moon's ICRF position, and rotate the difference into the [?moon-me-frame|mean Earth/polar axis frame] with the frame matrix at $t$. Then `reclat` of the result gives the topocentric distance $d$, the sub-observer longitude $l$ and latitude $b$ [@limb-wright-young-2024].
2. Compute the position angle $c$ of the Moon's north pole on the sky for the observer, from the same frame matrix projected onto the observer's celestial axes.
3. Load the DEM. Restrict to pixels whose angular distance from $(l, b)$ lies between about 86 and 94 degrees, which keeps a few per cent of the grid. Convert those pixels to $(x, y, z)$ with $R = 1737.4\ \mathrm{km} + h$.
4. Rotate by $\mathbf{R}_y(b)\,\mathbf{R}_z(-l)$ so that the sub-observer point lies on $+x$, then by $\mathbf{R}_x(-c)$ so that lunar north projects toward celestial north in the $(z, y)$ plane. For each point compute $\alpha = \tan^{-1}\big(\sqrt{y^2+z^2}/(d - x)\big)$ and the position angle $\theta = \operatorname{atan2}(y, z)$ measured from north through east, with the sign of $y$ chosen so that east is positive in the observer's sky.
5. Bin $\theta$ into $L = 18000$ bins and keep $\max\alpha$ per bin. Empty bins, which happen near the poles of a low-resolution grid, are filled by interpolation from neighbours.
6. Subtract the mean-limb angular radius: $\Delta_i = \alpha_i - \sin^{-1}(k R_\oplus/d)$ with $k = 0.2725076$, or with the DEM sphere if the rest of the pipeline uses it, and convert to arcseconds. This is the limb-height table. For a Watts comparison the abscissa must be shifted by the 0.21 to 0.25 degree Watts-angle offset [@limb-vizier-vi122] [@limb-morrison-appleby-1981].
7. Contact times: for bins within about ±40 degrees of $X$, evaluate $T_i = T_0 + \big(\Delta_i - s_0(M-1)(1-\cos(\theta_i - X))\big)/\big(v\cos(X - \theta_i)\big)$ following Espenak's equations [8] and [9], with $s_0$ the solar semidiameter. C2 of a total eclipse is $\max T_i$, C3 is $\min T_i$, and the bins that produce them are the last and first beads [@limb-espenak-tp2001] [@limb-herald-1983]. A direct time-stepped test with Wright's $\rho$ is the robust alternative and handles hybrid and broken-annular cases that the tangency construction cannot [@limb-wright-young-2024].
8. Path limits: at each time step, walk perpendicular to the path from the mean-limb limit and find the offset at which the $\rho$ test first passes on all bins, which is the interior limit, and at which a 60 degree unbroken crescent first appears, which is Espenak's exterior limit [@limb-espenak-tp2001]. Herald's factor converts an arcsecond displacement at the limit to kilometres on the ground [@limb-herald-1983].
9. Refresh the profile when $l$ or $b$ has changed by 0.01 degrees or every few minutes along the path, and refresh it per site for anything within a few kilometres of a limit [@limb-wright-young-2024].

Validation targets: Espenak's Lusaka example, $+4.0$ s and $-1.2$ s on 2001 June 21 with a Watts profile [@limb-espenak-tp2001], the Hao atoll 2010 table [@limb-sigismondi-thesis-2011], and the SVS 2024 `umbra_hi` polygons, which encode the LOLA-corrected umbra outline every second [@limb-svs-5073].

## Sources compared

| Source | Limb data | What it uniquely provides |
|---|---|---|
| Watts 1963 and VizieR VI/122 [@limb-vizier-vi122] | Photographic charts | The only pre-2009 limb dataset, the record format, the Watts-angle offset and inclination correction |
| Morrison and Appleby 1981 [@limb-morrison-appleby-1981] | 66,000 occultations | The harmonic correction formula, the 1737.97 km datum, the centre-of-figure terms |
| Herald 1983 [@limb-herald-1983] | Watts via Duncombe | The contact-time correction algorithm, the limit displacement factor, the limiting magnitudes, the error budget |
| Espenak TP 2001 [@limb-espenak-tp2001] | Corrected Watts | Equations [8] and [9], the two k values, Table 6 limit corrections, graze-zone definitions |
| Wright and Young 2024 [@limb-wright-young-2024] | SLDEM2015 and LDEM | The DEM-to-profile algorithm with bin count and refresh rule, the raster totality test, the polygonal umbra |
| SVS 4517, 5073, 5219 [@limb-svs-4517] [@limb-svs-5073] | SLDEM2015 | The released umbra polygons and the point-cloud description |
| Solar Eclipse Maestro help [@limb-jubier-sem-limb-window] | LRO, Kaguya, Watts | Three profiles side by side, the 0.241 degree offset, the 1738.091 km k sphere, text export |
| Occult pages [@limb-occult-accuracy-2016] [@limb-iota-2026-predictions] | Kaguya and LOLA | The 0.3 s prediction accuracy and the position-angle error finding |
| Eclipse Orchestrator [@limb-eclipse-orchestrator-lro] | LOLA RDR and Kaguya | A description of building a limb file from raw shots, and the 0.5 s missed-mountain effect |
| Sigismondi thesis [@limb-sigismondi-thesis-2011] | Watts and Kaguya | The Hao 2010 numerical comparison and the datum radius table |
| astronomy-bundle-js [@limb-andrmoel-lunar-limb-profile] | LDEM | Open-source code with the psi search formula |

## What a developer should do

Read Herald 1983 and the Lunar Limb Profile and Graze Zones sections of Espenak's 2001 bulletin first, because they define the quantities and give worked numbers. Then read Section 3 and Appendix A of Wright and Young 2024 for the DEM algorithm.

Download `ldem_128.img` and its label from the PDS GDR cylindrical directory for development, and `sldem2015_128_60s_60n_000_360_float.img` plus the LDEM polar tiles for production [@limb-lola-gdr-dir] [@limb-sldem2015-label]. Use the mean Earth/polar axis frame from the same JPL ephemeris family as the positions, and compute topocentric libration with SPICE or an equivalent, never from geocentric libration tables. Build the profile with 18,000 bins by the maximum-angular-radius rule and store it with the libration, distance and axis angle it was built for. Express heights against $k = 0.2725076$ and state that choice in every output.

Implement contact correction as the direct time-stepped totality test, and keep the Herald tangency construction as a cross-check because the bulletins' worked examples are stated in its terms. Treat the solar radius as an explicit input in two modes: 959.63 arcseconds to reproduce almanac products, and 959.95 ± 0.05 arcseconds for edge products, as decided in [Solar radius values and their provenance](../06-solar-radius/solar-radius-values.md). Near a path limit a 0.03 arcsecond change is one second of duration, and on the central line it is about 0.15 s [@limb-wright-young-2024].

## What this changes

The pipeline needs a limb stage between local circumstances and the reported contacts, and a second limb stage inside the path-limit search. Both stages need the lunar orientation model and the observer vector in the Moon frame, which the Besselian stage does not otherwise compute, so the ephemeris layer must expose a body-fixed lunar frame. The centre-of-figure machinery of the Watts era is dropped entirely when a centre-of-mass DEM is used. The path product changes shape: the umbra outline is a polygon that must be emitted as a polygon, and a limit line becomes a pair of lines, interior and exterior.

## Open questions

- Obtain Occult 4's help text for the Kaguya/LOLA profile options and its limb data file format, to confirm whether Occult uses gridded DEMs or the raw altimeter tracks and how it bins position angle.
- Obtain Smith et al. 2010 GRL and Barker et al. 2016 Icarus to verify the centre-of-mass to centre-of-figure vector and the SLDEM2015 mean radius quoted here from search summaries [@limb-smith-2010-lola] [@limb-barker-2016-sldem].
- Obtain the Solar Eclipse Maestro profile text export for one eclipse and compare it bin by bin with a profile built from LDEM_128 by the algorithm above, to settle the offset and sign conventions.
- Obtain the SVS 2024 `umbra_hi` shapefile and reproduce one polygon from SLDEM2015 with the ρ test, as the end-to-end validation of a new implementation [@limb-svs-5073].
- Find Rosselló and Jordi 1991 (Astrophysics and Space Science 177, 331) to document the second Watts correction that Solar Eclipse Maestro applies [@limb-jubier-sem-limb-window].
- Obtain a peer-reviewed comparison of Kaguya (SELENE), LOLA and Watts limb heights at the limb itself, a paper in Icarus, JGR Planets or the Journal for Occultation Astronomy. None was found by the searches run for this note, and the only numerical comparison located is the Hao 2010 table in a thesis [@limb-sigismondi-thesis-2011].
