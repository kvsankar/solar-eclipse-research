---
title: Wright and Young 2024, the raster method
description: What the Astronomical Journal paper actually specifies, formula by formula, and what it leaves out.
order: 1
status: working
updated: 2026-09-15
tags: [svs, wright, raster, limb-profile, limb-test, broken-annular, solar-radius]
---

::: summary
- **Citation.** Ernie Wright and C. Alex Young, "A Raster-oriented Method for Creating Eclipse Maps", The Astronomical Journal, volume 168, article 163, 13 pages, October 2024. Received 2024 April 23, accepted July 29, published September 19. DOI 10.3847/1538-3881/ad6b23. CC BY 4.0 [@svs-wright-young-2024].
- **The algorithm** colours each map pixel total, partial or uneclipsed at each time step. Only pixels that cannot be classified trivially are submitted to a full limb test against an 18,000-element limb profile [@svs-wright-young-2024].
- **The limb profile** is built from SLDEM2015 (512 pixels per degree, 60 m at the equator) and the polar LDEM, in the Moon Mean Earth frame of DE421, on a 1737.4 km datum sphere. It is rebuilt every few minutes or whenever a libration angle changes by 0.01 degrees [@svs-wright-young-2024].
- **The limb test** is $\rho = a^2 + \delta^2 - 2a\delta\cos(\theta-\phi)$ with the eclipse not total if $\rho < 1$. Distances are in apparent solar radii on the observer's image plane [@svs-wright-young-2024].
- **The umbra is a polygon** because each edge is an arc of a Sun image projected through one limb valley. At 18:00 UTC on 2017 August 21 the outline had 49 sides [@svs-wright-young-2024].
- **A third eclipse type**, broken annular, is mapped with the criterion $\max(L) - \min(L) > \delta$ [@svs-wright-young-2024].
- **The paper does not state** a $\Delta T$ value, a time step for 2024, a refraction model or a numerical comparison with Espenak or Jubier. Those come from the SVS pages, covered in [svs-products-and-data.md](svs-products-and-data.md) and [svs-vs-other-predictors.md](svs-vs-other-predictors.md).
:::

**The question.** What does Ernie Wright's published method actually specify, with which datasets and constants, and how much of an implementation can a developer reconstruct from the paper alone?

## The publication

The published method is Wright, E. and Young, C. A. 2024, "A Raster-oriented Method for Creating Eclipse Maps", The Astronomical Journal 168:163 (13 pages), published 2024 September 19, DOI 10.3847/1538-3881/ad6b23 [@svs-wright-young-2024]. Wright's affiliation is Universities Space Research Association and the Scientific Visualization Studio, Goddard Space Flight Center, Code 606.4. Young is Associate Director for Science, Heliophysics Science Division, Code 670. Wright's ORCID is 0000-0002-5970-5019. The article is open access under the Creative Commons Attribution 4.0 licence and carries an online animation as supplementary material [@svs-wright-young-2024].

Crossref confirms the DOI, the authorship and the issue date [@svs-crossref-wright], and the paper is indexed as gold open access under a CC BY licence [@svs-wright-young-2024]. NASA's September 2024 announcement [@svs-nasa-accurate-maps-article] and the USRA newsroom release [@svs-usra-newsroom-2024] both give the title and journal. No preprint exists: there is no arXiv version, and the ADS EPRINT link for bibcode 2024AJ....168..163W does not resolve.

Quotations below are from the publisher's PDF as captured by the Internet Archive on 2024 November 19; the article page itself is not retrievable without a browser session [@svs-wright-young-2024].

## What the paper claims

The abstract states the thesis in one sentence: "Ignoring the terrain of both bodies introduces errors on the order of kilometers in the ground track of the umbra and seconds in the duration and contact times of totality" [@svs-wright-young-2024]. The paper's own summary of its contribution is that it is "the first detailed description in the eclipse calculation literature" of numerical eclipse simulation, while explicitly not claiming to be the first implementation [@svs-wright-young-2024].

The background section credits prior limb-corrected maps to Michael Zeiler from 2012, "using eclipse software adapted for raster-oriented map calculations by Xavier Jubier and William Kramer", and dates the SVS work to December 2016, when maps and animations of the 2017 August 21 eclipse "for the first time accounted not only for the roughness of the lunar limb but also the terrain of the Earth" [@svs-wright-young-2024].

## The raster approach

The method is defined against the [?besselian-elements] tradition. Bessel's method projects the shadow onto the [?fundamental-plane] and characterises the eclipse by a few elements and their rates. The paper lists its simplifying assumptions: the Moon is a smooth sphere, its centre of mass coincides with its [?centre-of-figure], and all observers lie on an ellipsoid [@svs-wright-young-2024].

The raster method instead finds "the presence or absence of the Moon's shadow at every pixel of a raster map over a large number of time steps". Each pixel is coloured "black for total, gray for partial, and white for no eclipse". Repeating over time gives an animation, and integrating the image sequence gives the path of totality [@svs-wright-young-2024]. This is how the path limits and the central line are derived: they are not solved for as curves. They emerge as the boundary of the union of the umbra rasters, and the central line is the track of the shadow-axis intersection.

Each pixel is placed in three-dimensional space. Its geodetic longitude and latitude follow from the map projection. Its height above mean sea level is read from an Earth DEM. Height above the ellipsoid is obtained "by adding the geoid height". The paper states that most global DEMs "are now based on the WGS84 ellipsoid and EGM96 geoid" and that the DEM and the coordinate conversion must agree on both [@svs-wright-young-2024]. The Earth DEM used for the NASA maps is not named in the paper. The SVS pages name SRTM [@svs-4517-umbra-shapes].

The terrain effect is quantified as a shift of roughly $h \cot a$, where $h$ is the elevation and $a$ is the Sun's altitude, in the direction of the Sun's azimuth [@svs-wright-young-2024]. Figure 1 shows the umbra west of Idaho Falls on 2017 August 21 "perturbed and shifted roughly 1.5 km southeast by the elevation of the Earth's terrain". The 2016 SVS page puts the western-states shift at "as much as 3 kilometers" [@svs-4517-umbra-shapes].

For pixels near the umbra edge the traditional local-circumstances calculation supplies three values: the distance between the centres of the lunar and solar discs in apparent solar radii, the relative sizes of the discs, and the [?position-angle] of the Moon with respect to the Sun. "To test for totality, the Moon circle is replaced by a limb profile, an array of radii representing the actual shape of the limb. The eclipse is total for a given observer if the limb profile completely encompasses the Sun circle" [@svs-wright-young-2024]. The paper stresses that this is a direct comparison on an image plane unique to each observer, whereas the Besselian test of distance from the shadow axis "relies crucially on the assumption that the cross section of the shadow is circular".

## Creating the limb profile

Section 4 defines a [?limb-profile] $L$ as "a one-dimensional array of radii at equally spaced angular intervals around the lunar limb". For an observer at distance $d$ from the Moon's centre the construction is [@svs-wright-young-2024]:

1. Convert each pixel of the lunar DEM to rectangular coordinates.
2. Apply a rotation matrix encoding the topocentric [?libration] at the observer.
3. Convert the transformed position's $(y, z)$ to polar $(r, \theta)$.
4. Replace $r$ with the angular radius $\alpha = \tan^{-1}\!\big(r / (d - x)\big)$.
5. Convert $\theta$ to an index $i$ into the array $L$.
6. If $\alpha$ is greater than $L_i$, set $L_i = \alpha$.

The rotation in step 2 encodes the [?moon-me-frame] longitude and latitude of the sub-observer point. After the rotation the centre of the disc as seen by the observer has coordinates $(x, 0, 0)$, "where $x$ is the datum radius (1737.4 km for LRO DEMs) plus the elevation at that point". The arctangent in step 4 performs perspective foreshortening, and the paper notes that far-side points "can and do contribute to the limb". Index 0 is north and $i$ increases counterclockwise [@svs-wright-young-2024].

![The relief the profile is drawn from. Colour codes elevation over the eastern limb, from 2.4 billion LOLA shots. The profile is not a picture of this surface but one number per 0.02° bin, the largest angular radius any point in that bin presents to the observer, so a far-side peak can enter the limb and a near-side plain never does. NASA/Goddard/MIT/Brown.](img/lola-eastern-limb.jpg)

The datasets are named precisely. "As of this writing, the highest-quality lunar DEMs are [?sldem2015] (Barker et al. 2016), produced by combining data from the terrain camera (TC) on SELENE and the LRO laser altimeter (LOLA) on LRO, and the polar stereographic [?ldem] from LOLA." SLDEM2015 covers 60 N to 60 S at 512 pixels per degree (60 m at the equator), with subsampled versions at 256 and 128 pixels per degree. The polar LDEMs fill the poles. Both are archived on the LRO node of the Planetary Data System, and the paper gives the link https://pds-geosciences.wustl.edu/missions/lro/lola.htm [@svs-wright-young-2024] [@svs-pds-lola]. Barker et al. describe SLDEM2015 as built from about 4.5 billion LOLA heights co-registered with 43,200 SELENE TC stereo DEMs, with typical vertical accuracy of 3 to 4 m [@svs-barker-2016-sldem2015].

The coordinate frame is stated: "LRO data are tied to the Moon Mean Earth (Moon ME) frame as realized by the Jet Propulsion Laboratory Developmental Ephemeris 421 (DE421)". The origin of longitude is the mean sub-Earth point, latitudes are [?planetocentric-latitude] because the DEM elevations are relative to a sphere, and the axes follow the modern convention with $x$ through longitude 0, $z$ north, $y$ east [@svs-wright-young-2024]. The LRO project's coordinate document confirms the ME system, the 1737.4 km reference radius and the selection of DE421 [@svs-lro-coordinate-system-2008].

Resolution of the profile: "An L of 18,000 elements has a resolution of 0.02 degrees (roughly 600 m) and pairs well with DEMs of 240 m resolution." Too large an array "may include points not on the limb", too small "will miss small valleys" [@svs-wright-young-2024]. The 240 m figure corresponds to the 128 pixel per degree subsample of SLDEM2015, not the full 512 pixel per degree product.

Cost control: creating a profile for every observer "is prohibitively expensive on modest computing hardware. A reasonable compromise is to create a profile for the observer on the shadow axis at time steps of a few minutes, or whenever a libration angle has changed by some small threshold, say 0.01 degrees." Only DEM points within 75 to 105 degrees east and west longitude in SLDEM and a 450 km wide swath through each polar LDEM are processed. Libration in latitude is always small during solar eclipses because they occur near the nodes [@svs-wright-young-2024].

## The limb test

Section 5 lists the required quantities [@svs-wright-young-2024]:

- $n$, the number of elements in $L$.
- $d_0$, the observer to Moon distance at which $L$ was created.
- $d$, the current observer's Moon distance.
- $c$, the [?axis-angle], the position angle of the Moon's north pole axis.
- $\delta$, the Sun to Moon apparent distance in solar radii.
- $\phi$, the position angle of the Sun with respect to the Moon (the more usual angle of the Moon with respect to the Sun differs by $\pi$).
- $r$, the apparent radius of the Sun in radians.

The test examines each $L_i$:

1. $s = (d_0/d)/r$
2. $a = s L_i$
3. $\theta = 2\pi i/n + c$
4. $\rho = a^2 + \delta^2 - 2a\delta\cos(\theta - \phi)$
5. If $\rho < 1$, the eclipse is not total for the observer.

The Sun and Moon are placed in polar coordinates on the observer's image plane, celestial north up, units of apparent solar radius, Moon at the origin and Sun at $(\delta, \phi)$. The scale $s$ corrects for the observer's distance and converts limb radii to solar radii. Step 4 is the polar distance formula with the square root omitted because the comparison is against 1 [@svs-wright-young-2024]. The axis angle $c$ and the profile are computed once per time step for the observer on the shadow axis, since differences between nearby observers are far smaller than the profile resolution.

Trivial exclusion defines the [?limb-test-zone] [@svs-wright-young-2024]:

- if $s\max(L) - \delta < 1$, the observer is outside the umbra;
- if $s\min(L) - \delta \ge 1$, the observer is inside the umbra.

Only observers satisfying neither condition need the full test. For annularity the sense reverses, failing on $\rho \ge 1$, with exclusions $s\max(L) + \delta < 1$ (inside the [?antumbra]) and $s\min(L) + \delta \ge 1$ (outside). For eclipses with magnitude near 1 both tests are applied [@svs-wright-young-2024].

[?antialiasing] is folded into the test. For failed elements the sum of $1 - \rho$ is accumulated. If the sum is greater than 0 but less than a threshold $\epsilon$, the pixel gets the intermediate value $1 - \text{sum}/\epsilon$. "For $n$ = 18,000, setting $\epsilon = A(p)/10$ works well, where $p$ is the pixel at the center of the shadow and $A$ is the area in square kilometers" [@svs-wright-young-2024]. The stated purpose is to remove false precision and to help contour-tracing algorithms, which is how the vector shapefiles are extracted from the rasters.

## Contact times at a site

The paper does not describe a separate local-circumstances routine. Second and third contact at a site follow from the same test applied to that site across time steps: totality begins at the first step where the limb profile encompasses the Sun and ends at the last. The cities JSON released with the 2024 map gives contact times to the second for towns in totality and appears to be produced this way [@svs-cities-2024-json]. The time resolution of the released umbra polygons, 1 s for the high-resolution set, bounds the timing precision of anything derived from them [@svs-5123-2024-map].

## The polygon explained

Section 6.2 uses the antialiasing pass to identify, for each edge pixel, "which $L_i$ is at the greatest internal distance from the solar limb". Plotting those elements "form[s] a minimal and coherent set of umbra polygon edges". Each limb point is then treated as a pinhole projecting an image of the Sun onto the Earth. "The locus of all such rays forms a double cone with its apex at the limb point." The Sun-image cone angle equals the shadow-cone angle and its axis deviates from the shadow axis by 2.4 arcseconds, the angle subtended by the Moon's radius at the Sun [@svs-wright-young-2024].

The shape follows: "The outer edge of the penumbra is defined by the outer edges of the Sun images. The umbra is the set of interior points not reached by any of these Sun images." At 18:00 UTC on 2017 August 21, 49 valleys contributed edges, and Figure 12 shows the 49 projected Sun images with the umbra as the hole in the middle. The edges are arcs, not straight lines. For the antumbra the focal points are peaks and the shape is the intersection of the Sun images [@svs-wright-young-2024]. The 2024 SVS explainer page reproduces this account and the 49-valley count [@svs-5366-shadow-shape]. Observers on an edge see the diamond ring from that valley, and observers at a vertex see a double diamond ring, a point the paper credits to Zeiler [@svs-zeiler-double-diamond].

## Broken annular

Section 6.3 introduces a "third type of central eclipse in which the shadow axis intersects the Earth's surface but the eclipse at that location is neither total nor annular". In the smooth-limb model the umbra and antumbra cones meet at a point, so a hybrid switches instantly. In reality there is a gap in which "a very thin ring of sunlight around the Moon is interrupted by high points on the lunar limb" [@svs-wright-young-2024].

The proposed criterion is that [?broken-annular] locations are the locus of points for which

$$\max(L) - \min(L) > \delta,$$

valid only at locations that have already failed both the totality and annularity tests [@svs-wright-young-2024]. Three examples are given. The 1894 April 6 eclipse "is never actually total, spending 2 hr as a broken annular over a span of nearly 5400 km". The 2005 April 8 hybrid has totality "flanked by more than 1300 and 730 km of broken annularity". The 2013 November 3 hybrid "has no true annular phase". Figure 13 maps the 2005 path assuming $r$ = 696,000 km and simulates Baily's beads at 1 s intervals from 21:55:26 to 21:55:32 UTC as seen from 94.02587 W, 6.45677 N. The SVS release of that simulation runs in real time from 21:55:20.5 to 21:55:35.5 UTC [@svs-5365-broken-annular].

## The solar radius

Section 6.4 is the paper's statement on the constant that matters most near the limits. "Nearly all eclipse calculations use a de facto standard value of the solar radius first published more than a century ago and expressed as either 959.63 arcseconds at 1 au (Auwers 1891) or 696,000 km (Yatskiv 1978)." The IAU 2015 nominal unit is 695,700 km, equivalent to 959.22 arcseconds, and the paper quotes Prsa et al. that nominal values "should be understood as conversion factors only" [@svs-wright-young-2024].

The paper argues the [?nominal-solar-radius] "does not provide the solar radius required for accurate eclipse prediction, which defines totality as the complete extinction of the photosphere". It lists recent [?eclipse-solar-radius] determinations: 959.99 plus or minus 0.06 arcseconds (Lamy et al. 2015), 959.95 plus or minus 0.05 (Quaglia et al. 2021), 959.98 (Jubier et al. 2021) and 960.01 (Guhl 2023) [@svs-wright-young-2024]. Quaglia et al. obtained their value from flash-spectrum video at the southern limit of the 2017 path and report no significant wavelength dependence [@svs-quaglia-2021-apjs]. Guhl's value comes from Baily's beads photometry at the northern limit of the 2023 April 20 hybrid, a correction of plus 0.38 arcseconds to 959.63, giving 960.01 plus or minus 0.12 arcseconds [@svs-guhl-2023-joa].

The sensitivity statement is quotable: "a discrepancy of 1 s in duration, for example, corresponds to an error as small as 20 km (0.03 arcseconds) in solar radius" for points very close to the path limits [@svs-wright-young-2024]. The paper recounts the March 2024 episode in which John Irwin's map, "based on a solar radius of 959.95 arcseconds", shifted the northern limit "to the southeast by several city blocks compared to maps calculated with the conventional radius", and dozens of journalists asked whether NASA would revise its map [@svs-wright-young-2024]. It did not. See [svs-vs-other-predictors.md](svs-vs-other-predictors.md).

The paper does not say which solar radius the 2024 NASA map used. The SVS product pages for 2017 state 696,000 km [@svs-4515-2017-path], and the paper's Figure 13 uses the same value, so the working assumption is that all SVS maps to date use 696,000 km, which is 959.63 to 959.645 arcseconds depending on the au conversion used.

## Appendix A, the software stack

The appendix is the only public description of the implementation. "The code that generated the NASA maps relies primarily on SPICE." It prints C-language calls [@svs-wright-young-2024]:

```
vsub_c( obs, mpos, pos );          /* translate to Moon-centered */
mxv_c( mmat, pos, pos );           /* rotate from ICRF to Moon ME */
reclat_c( pos, dist, lam, bet );   /* to spherical coords */
```

which return the observer's Moon distance and the Moon ME sub-observer longitude and latitude, that is, the topocentric libration. The Moon's ICRF position comes from `spkezp_c(ID_MOON, t, "ICRF", "lt+s", ID_EARTH, mpos, &lt)` with light time and stellar aberration, from the kernel `de440.bsp`. The rotation to the body-fixed frame is `pxform_c("ICRF", "MOON_ME_DE440_ME421", t, mmat)` using `moon_pa_de440_200625.bpc` and `moon_de440_200625.tf`. That frame kernel is the 2020 release, and NAIF's current file for the same frame is `moon_de440_250416.tf`. The frame name records that "the origin of selenographic coordinates for LRO data products is the mean sub-Earth point found by the DE421 calculation, not that of DE440" [@svs-wright-young-2024].

The observer is placed with `georec_c(lon, lat, h, earth_r, flattening, obs)`, where $h$ is ellipsoid height, and rotated to the ICRF with `pxform_c("ITRF93", "ICRF", t, omat)` using `earth_latest_high_prec.bpc`. The paper warns that "SPICE Earth orientation kernels are less reliable or nonexistent for times in the future or before 1962" and gives the SOFA equivalent, `iauC2t06a(tta, ttb, uta, utb, xp, yp, omat_inv)` followed by a transpose [@svs-wright-young-2024]. This is where [?delta-t] enters: it is implicit in the [?eop] kernel rather than a stated number. The SVS 2017 pages state the value that resulted, $\Delta T$ = 68.917 s, and describe the kernel as "earth_070425_370426_predict.bpc (ΔT corrected)" [@svs-4515-2017-path].

The ephemeris is therefore DE440 at the time of writing the paper, while every SVS product page from 2015 through 2025 lists DE421 as its dataset [@svs-5123-2024-map] [@svs-5510-mar-2025-partial-map]. Both cannot be true for the same run. The likely reading is that the maps were made with DE421 and the paper's appendix was written against the current kernel set. The difference between DE421 and DE440 in the Moon's geocentric position in 2024 is far below the 600 m limb-profile resolution, so the choice has no visible effect on the products.

Nothing in the paper or on any SVS page mentions Maya, RenderMan or any commercial renderer for the eclipse calculation itself. The 2017 shapefile page says only that "the map was rendered in animation software, but maps are more typically created using GIS tools" [@svs-4518-2017-map-shapefiles]. The 2015 page says the Besselian method "was adapted to the routines available in NAIF's SPICE software library" [@svs-4314-2017-usa].

## What the paper does not say

- **No $\Delta T$ value** for 2024. It is embedded in the Earth orientation kernel.
- **No time step** for the 2024 map. The released umbra_hi shapefile is at 1 s and umbra_lo at 10 s [@svs-5123-2024-map].
- **No refraction model.** The March 2025 map page says the sunrise and sunset lines "are based on an idealized model" and that "the apparent positions of the Sun and Moon relative to the horizon are affected by local terrain and atmospheric refraction" [@svs-5510-mar-2025-partial-map].
- **No Earth DEM named.** SVS pages credit SRTM [@svs-4517-umbra-shapes].
- **No numerical comparison** with Espenak or Jubier. The only comparison is the qualitative "several city blocks" against Irwin's map.
- **No stated uncertainty** in kilometres for its own path edges. NASA's public statement during the 2024 dispute acknowledged "a tiny but real uncertainty about the size of the Sun" and that "uncertainty in the Earth's rotation can also affect eclipse predictions on this level" [@svs-cnn-wattles-2024].
- **No code release.** See the searches described in [svs-products-and-data.md](svs-products-and-data.md).

## Prior art the paper builds on

The reference list is the best map of the field's genealogy. On the limb: Kopal 1965 and Weimer 1979 for early catalogues, then the [?watts-charts] of 1963, which "remained in use for eclipse and occultation timing for half a century" despite flaws documented by Scott 1988, before being supplanted by SELENE and LRO altimetry [@svs-wright-young-2024] [@svs-watts-1963] [@svs-scott-1988-aj] [@svs-araki-2009-kaguya] [@svs-smith-2017-lola]. On applying limb profiles: Herald 1983 in the Journal of the BAA, "a purely graphical construction that involves plotting solar limb curves on transparencies" over exaggerated limb plots like Duncombe's 1973 USNO circular, sliding along the position angle to find the limb-corrected contacts [@svs-herald-1983-jbaa] [@svs-duncombe-1973]. The paper says software authors "have automated this method and adapted it to newer lunar terrain data, but the details of their implementations remain largely undocumented". It points to Herald's Occult documentation and to Wang et al. 2021 for details of limb-profile use [@svs-herald-occult] [@svs-wang-2021-raa].

On elevation: Williams 1971 for adapting Bessel by replacing 1 Earth radius with the elevated radius, Lewis 1940 for USNO central-line maps at ionospheric altitudes, Fiala et al. 1987 for interpolating between tabulated heights, and Schneider 2004 for aircraft intercepts [@svs-williams-1971-afcrl] [@svs-fiala-1987-usno]. On the canonical formulation: Bessel 1829 and 1830, Chauvenet 1863, both editions of the Explanatory Supplement, Meeus 1989 and Montenbruck and Pfleger 2000 [@svs-explanatory-supplement-2012]. On ephemerides and frames: Folkner et al. 2009 for DE421, Park et al. 2021 for DE440, the LRO coordinate-system memo of 2008 [@svs-folkner-2009-de421] [@svs-park-2021-de440] [@svs-lro-coordinate-system-2008].

Two names a reader of the eclipse-radius literature would expect are absent. Sigismondi is not cited. Dunham is not cited by name, though IOTA appears through Herald and through Guhl's paper in the Journal for Occultation Astronomy. The Kaguya (SELENE) work enters only as Araki et al. 2009 and through SLDEM2015's use of the SELENE terrain camera.

## Sources compared

| Source | What it uniquely provides |
|---|---|
| Wright and Young 2024 [@svs-wright-young-2024] | The algorithm: limb-profile construction, limb test, antialiasing threshold, broken-annular criterion, SPICE calls. Read in full from the PDF. |
| SVS 4515 and 4516 [@svs-4515-2017-path] | The constants table: radii, ellipsoid, geoid, ephemeris, EOP kernel, $\Delta T$ = 68.917 s for 2017. |
| SVS 4314 [@svs-4314-2017-usa] | The smooth-model baseline and its "About Accuracy" paragraph, including $k$ = 0.2723993 and the 0.5 km centre-of-mass offset. |
| SVS 4517 [@svs-4517-umbra-shapes] | The first published explanation of the polygon, with the 3 km terrain shift and the point-cloud rotation description. |
| SVS 5366 [@svs-5366-shadow-shape] | The pinhole explanation with the 49-valley count, released with the paper. |
| NASA press article [@svs-nasa-accurate-maps-article] | Wright's own plain-language framing and the "potato" quote. |
| Quaglia et al. 2021 [@svs-quaglia-2021-apjs] | The 959.95 arcsecond value the paper contrasts against. |

## What a developer should do

Read the paper's sections 4 and 5 first. They are complete enough to implement. Then:

1. Download SLDEM2015 at 128 or 256 pixels per degree and the polar LDEMs from the PDS LOLA node [@svs-pds-lola]. Read `dsmap.cat` and `dsmap_polar.cat` for the pixel-to-longitude mapping. Use the 1737.4 km datum and planetocentric latitude.
2. Use SPICE with `de440.bsp`, `moon_pa_de440_200625.bpc`, the frame kernel `moon_de440_250416.tf`, which is NAIF's current release of the `moon_de440_200625.tf` the paper prints, and the frame `MOON_ME_DE440_ME421`, exactly as printed in Appendix A, so that the DEM and the frame agree [@svs-wright-young-2024].
3. Build $L$ with 18,000 elements for the shadow-axis observer, rebuilt when libration moves by 0.01 degrees. Store $\min(L)$ and $\max(L)$.
4. Implement the limb test as written, with the trivial exclusions, and the antialiasing with $\epsilon = A(p)/10$.
5. Convert SRTM or a successor DEM's orthometric heights to ellipsoid heights with EGM96 before calling `georec_c`.
6. Choose and state the solar radius. The paper gives you the sensitivity: 0.03 arcseconds is 1 s of duration at the limits.
7. Validate against the released umbra_hi polygons for 2024 [@svs-2024-shapefiles-zip], which are the paper's own output.

## What this changes

For the pipeline design this replaces the "limb correction as a post-processing step on Besselian contacts" model with a per-pixel test. The path limits, central line, duration contours and obscuration contours are all derived products of a raster stack, which means one code path produces every map layer. It also establishes that the limb profile, not the ephemeris, sets the resolution floor at about 600 m, and that the solar radius, not the limb, is the dominant unresolved uncertainty at the limits.

## Open questions

- **The 2024 run's $\Delta T$ and ephemeris.** Obtain the SVS API JSON for page 5123 or an author statement to settle whether DE421 or DE440 and which EOP kernel produced the 2024 shapefiles.
- **The Earth DEM resolution used.** SRTM exists at 1 and 3 arcseconds. The paper's 240 m lunar pairing suggests a coarse Earth grid, but the map pixel size for 2024 is unstated. The insolation dataset is at 360/8192 degrees per pixel [@svs-5248-insolation-2024], which may be the shadow-raster grid.
- **A test of the broken-annular criterion against observation.** The 1986 October 3 and 2023 April 20 eclipses have observers. Compare the criterion's locus with the reported bead sequences.
- **The unpublished code.** Ask the author whether the C code can be released. Until then the shapefiles are the only ground truth.
