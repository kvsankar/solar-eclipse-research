---
title: Grazing occultations and the lunar limb
seo_title: Grazing Lunar Occultations: Limit Lines and Limb Profiles
description: How grazing occultations are predicted, how limb profiles and observer height move the limit line, and how expeditions place observers.
order: 2
status: working
updated: 2026-10-17
tags: [occultations, graze, limb-profile, lola, iota, occult]
---

::: summary
- **A graze is an occultation seen near a limit line.** The star skims the Moon's north or south edge and blinks behind peaks and valleys. The useful zone is a few hundred metres to 8 km wide, set by the polar limb heights [@occ-iota-manual-2007] [@limb-dunham-rasc-2026]. The sources are the International Occultation Timing Association (IOTA) manual and the Royal Astronomical Society of Canada's Observer's Handbook (RASC Observer's Handbook).
- **Every graze prediction is a limb-profile prediction.** The smooth-limb limit line is only the reference. Occult plots the predicted profile against distance from that line in kilometres, with minute ticks from central graze, and leaders place observers on that plot [@occ-iota-manual-2007].
- **Observer height shifts the line.** The shift is $d = h\tan z$ toward the Moon's azimuth. Its component perpendicular to the limit line is $X = h\tan z\sin D$, which can be three or four times the height for a low Moon [@occ-iota-manual-2007].
- **Position angle precision drives the limb correction.** Morrison required position angles to 0.01 degrees on Watts' charts and shifted the chart angles by 0.25 degrees. Occult found in 2016 that an error of up to about 0.2 degrees in its position angle had been corrupting both predictions and graze profiles [@occ-morrison-1979] [@limb-occult-accuracy-2016].
- **The archive's limb is the Lunar Orbiter Laser Altimeter (LOLA) grid in position angle.** VI/132C converts the LOLA 1/512 degree grid to 72,036,000 points at 0.01 degrees in position angle, with limb heights believed accurate to 0.01 arcseconds [@occ-vizier-vi132c].
- **Grazes are now mainly for double stars and limb checks.** With Gaia positions and LOLA heights, the RASC Handbook says one to three stations are enough. Video resolves doubles of 0.02 arcseconds at a graze [@limb-dunham-rasc-2026] [@occ-iota-manual-2007].
:::

**The question.** What happens to an occultation prediction near its northern or southern limit, where a [?occ-grazing-occultation|grazing occultation] is seen, how do the limb profile and the observer's height move that limit, and how do predictors and observers turn this into a graze expedition and a reduction? The limb datasets and the general DEM-to-profile geometry are in [Lunar limb profile](../../20-solar-eclipses-and-transits/05-lunar-limb/_index.md) and are not repeated here.

## The geometry of a graze

The [?occ-limit-line|limit lines] are where the star's apparent track is tangent to the Moon's mean limb, as defined in [Besselian elements for lunar occultations](besselian-elements-for-occultations.md). The IOTA manual describes what an observer near them sees. "The star would thus appear to skim by the Moon's northern or southern limb. The visible effect would reveal the star passing in and out from behind the lunar mountains and valleys" [@occ-iota-manual-2007]. The series "will last a fraction of a second to a minute or longer" [@occ-iota-manual-2007].

Each occultation has two limits, one at each pole of the Moon, and they lie 180 degrees apart on the limb. So "one graze will be on the Moon's sunlit (bright) limb and the other graze along the dark limb", except during a total lunar eclipse [@occ-iota-manual-2007]. Only the brighter stars can be seen at a bright-limb graze [@occ-iota-manual-2007]. The width of the multiple-event band "may vary from several hundred meters to 8 km depending on whether the graze occurs at the Moon's northern or southern limb", because "the widths of these graze paths are directly related to the heights of the mountains in the Moon's polar regions" [@occ-iota-manual-2007]. The RASC Handbook speaks of a "2- or 3-km-wide zone where multiple disappearances of the star may occur" [@limb-dunham-rasc-2026]. Both are statements of the [?graze-zone|graze zone] for stars.

In the prediction equations a graze is where $kn\cos\psi$ goes to zero, the quantity defined in [Besselian elements for lunar occultations](besselian-elements-for-occultations.md). The time of a smooth-limb event becomes indeterminate there. A small error in the star or the limb then moves the event by a large time and the limit by a small distance. HM Nautical Almanac Office (HMNAO) therefore omitted predictions with $|kn\cos\psi| < 0.030$ and issued separate graze maps and predictions from the 1960s [@occ-es1961]. The graze product is a line on the ground and a profile, not a time.

Two angles from the limb literature describe where on the limb a graze falls. The [?watts-angle|Watts angle] "is measured positive eastward around the lunar limb starting at the Moon's north pole" [@occ-iota-manual-2007]. The [?occ-cusp-angle|cusp angle] is measured from the nearer cusp, positive on the dark side [@limb-dunham-rasc-2026]. Occult's graze table lists both a position angle and an axis angle, and the cusp angle with N or S for the pole [@bes-occult-tutorial]. Regions just beyond the poles that come into profile at extreme libration are never fully lit when at the limb. Watts could not map them from Earth-based photographs, and IOTA calls them "Cassini" regions [@occ-iota-manual-2007].

## History in one paragraph

The IOTA manual credits D. Koch in Danzig with the first observed graze, a northern-limit graze of Aldebaran on 1794 March 7 with five events [@occ-iota-manual-2007]. Jean Meeus computed and observed a graze on 1959 November 20, "the first predicted and observed grazing occultation by the Moon" [@occ-iota-manual-2007]. David Dunham's prediction of the graze of 5 Tau on 1962 September 18 was the first in the United States, and the first organised expedition followed on 1963 September 9 near Davis, California [@occ-iota-manual-2007]. After the 1963 October 8 graze was published in Sky & Telescope, Tom Van Flandern at the US Naval Observatory (USNO) "was amazed to find more than 0.8 km error in the current combination of star position, lunar ephemeris and lunar limb data", and USNO began supporting graze predictions [@occ-iota-manual-2007]. HMNAO's 1973 note records that graze maps were issued "since the observations provide useful data about the latitude of the Moon and the profile of its limb" [@occ-es1961]. Before Hipparcos in 1997, "the polar diameter determination of the Moon by nearly simultaneous observation of grazes at opposite limits was an important goal of IOTA" [@occ-iota-manual-2007].

## The limb correction in an occultation reduction

### Watts' charts as HMNAO used them

The 1961 Supplement already described the limb correction for every timed occultation, waiting on Watts' charts. The chart arguments, in degrees, are the topocentric position angle from the Moon's central meridian $\Pi$, the libration in longitude $l$ and the libration in latitude $b$ [@occ-es1961]. The topocentric values come from the daily geocentric librations $l_0$, $b_0$ and the axis angle, written here $C_0$ as in the Supplement [@occ-es1961]:

$$
\Pi = \chi - C_0 + A X_\ell + B Y_\ell,\qquad
l = l_0 + \sec b_0\,(-X_\ell\cos C_0 + Y_\ell\sin C_0),\qquad
b = b_0 + (X_\ell\sin C_0 + Y_\ell\cos C_0).
$$

Here $\chi$ is the position angle of the event, and $A$ and $B$ are two daily auxiliaries [@occ-es1961]:

$$
A = +\tan b_0\cos C_0 + \tan\delta_\mathrm{m},\qquad B = -\tan b_0\sin C_0,
$$

with $\delta_\mathrm{m}$ the Moon's declination. The angular offsets are $X_\ell = s_\mathrm{t}\xi$ and $Y_\ell = s_\mathrm{t}\eta$, with $\xi$ and $\eta$ in lunar radii. Here $s_\mathrm{t}$ is "strictly the topocentric semi-diameter in degrees, but is generally taken as $s''/3600$, where $s''$ is the geocentric value in seconds of arc" [@occ-es1961]. The Supplement writes $S$, $X$ and $Y$. This site keeps $S$ for the ellipsoid auxiliary, and $Y$ is also an occultation element. The axis angle $C_0$ is the [?position-angle-of-axis|position angle of the lunar axis], not Herald's angle $C$ from the contact point. The chart value is at mean distance, so it "must accordingly be multiplied by the ratio of the actual to the mean semi-diameters, $s/s_0 = 0.0010723\,s''$, and subtracted from the value of $\Delta\sigma$" [@occ-es1961]. In the quotation $s_0$ is the Moon's mean semidiameter, written $s_{\mathrm{m},0}$ elsewhere in this topic, and not the solar $s_0$ of this site. In the Supplement's fictitious Strasbourg reduction the chart gives $-0.74$ arcseconds, scaled to $-0.78$. This turns a residual of $-0.8$ arcseconds into 0.0 [@occ-es1961].

Morrison's 1943 to 1974 analysis did the same with a computerised Watts dataset. He computed topocentric librations by adding parallactic corrections to the geocentric ones [@occ-morrison-1979]:

$$
\Delta l = (\Delta\alpha\cos\delta\cos C_0 - \Delta\delta\sin C_0)\sec b_0,\qquad
\Delta b = -\Delta\alpha\cos\delta\sin C_0 - \Delta\delta\cos C_0,\qquad
\Delta C = \Delta l\sin b_0 + \Delta\alpha\sin\delta,
$$

where $\Delta\alpha$ and $\Delta\delta$ are the lunar parallax corrections. Morrison writes the axis angle as $X$, the angle between the projected poles of the Earth's equator and the Moon's mean equator. It is written $C_0$ here as above. He used 1.564 degrees for the inclination of the lunar equator "because this was the value that Watts (1955) used in constructing his charts" [@occ-morrison-1979]. Two of his findings set the precision a limb correction needs. First, Watts' profiles "accord better with the results of grazing occultations if the tabular position angles of the charts are amended systematically by $-0.25^{\circ}$" [@occ-morrison-1979]. Second, "the computed position angle P ... should be within $\pm0.01^{\circ}$ of the correct angle", because "the steepest lunar slopes have an inclination of about 13°, so the greatest change in height along the profile is about 0".04 in 0°.01 of position angle" [@occ-morrison-1979]. He also added $+0.050$ seconds of time to star right ascensions when computing $P$, to remove the FK4 equinox offset of the lunar ephemeris [@occ-morrison-1979]. He coded chart heights as uncertain by 0.2 arcseconds, or 0.5 arcseconds where Watts' contours were extrapolated [@occ-morrison-1979]. The later systematic corrections to the Watts datum are in [Limb profile methods](../../20-solar-eclipses-and-transits/05-lunar-limb/limb-profile-methods.md#systematic-errors-and-the-morrison-and-appleby-corrections) [@limb-morrison-appleby-1981].

### LOLA in the archive and in Occult

The modern reduction keeps the same structure with a different limb. The VI/132C archive states: "The 1/512 gridded data set was converted to 72,036,000 data points in the [P,D] reference frame, to facilitate the determination of the apparent limb height at any point around the limb. The data spacing was 0.01 deg in P (equivalent to about 0.17" in Position Angle at the mean distance of the moon), and 0.02 deg in D (from -20 to +20 deg)" [@occ-vizier-vi132c]. The limb height is "the point in the P,D reference frame that has the greatest projected distance (at the relevant position angle, librations, and lunar distance from the observer) from the apparent center of the moon, with interpolation between data points" [@occ-vizier-vi132c]. "It is believed that the limb heights so derived are accurate at about the 0.01" level" [@occ-vizier-vi132c]. The documentation does not define $D$ beyond its range. The rule of taking the greatest projected distance in each position-angle bin is the same rule Wright and Young use for eclipses, described in [Limb profile methods](../../20-solar-eclipses-and-transits/05-lunar-limb/limb-profile-methods.md#from-dem-to-limb-profile-the-geometry).

Herald's 2016 note shows what a 0.2 degree error costs. Observed-minus-predicted times were larger than the small reduction residuals allowed. "The major cause for this was identified (after much effort) as being due to how the position angle of the event was calculated - with the traditional method having an error of up to ~0.2°" [@limb-occult-accuracy-2016]. After the fix, "the great majority of predictions are now within 0.3sec of the observed time", provided the LOLA limb, Occult download 26, is installed. "The same issue existed when generating a graze profile - with the orientation of the profile potentially being in error by up to ~0.2°" [@limb-occult-accuracy-2016]. By Morrison's slope figure, 0.2 degrees of position angle on a 13 degree slope can move the limb height by up to about 0.8 arcseconds. That is an inference from the two sources, not a figure either states. The current IOTA instruction for graze and eclipse profiles is to select LOLA with the HiRes option and leave the observed corrections at None [@limb-iota-2026-predictions].

## The graze profile

A graze prediction is a table and a picture. Occult first lists the sea-level limit line as longitude and latitude points with the UT of central graze at each, and columns for Sun and Moon altitude, Moon azimuth, $\tan Z$, position angle, axis angle and cusp angle [@occ-iota-manual-2007] [@bes-occult-tutorial]. It then "draws a limb profile of the Moon at the time and position angle of central graze nearest the observer's site" [@occ-iota-manual-2007]. The IOTA manual describes the 2007 version of the plot. The mean limb is a bowl-shaped dotted curve. The vertical scales are kilometres from the mean limit. The predicted profile is "the wiggly continuous line", and earlier graze observations are scattered dots. A horizontal row of ticks gives minutes from central graze [@occ-iota-manual-2007]. In a southern-limit profile "the mountain peaks indicated by Watts data and data points from observations are facing downward" [@occ-iota-manual-2007]. The 2007 plots offered Watts, ACLPPP or MoonLimb limb data. The observed points were then the better guide, because "the Watts data is not necessarily accurate everywhere around the limb" [@occ-iota-manual-2007]. In the LOLA era the observed corrections are switched off [@limb-iota-2026-predictions].

The profile is read as a cross-section of the band on the ground. For any location within a few miles of the predicted limit the star "will appear to move in a horizontal line across the profile chart" [@occ-iota-manual-2007]. An observer at $+2$ km sees the star cross the profile along the line two kilometres above the mean limit. The events are the crossings of that line with the predicted terrain. The kilometre scale is the shift on the ground perpendicular to the limit line. It equals the shift on the fundamental plane only when the Moon is in the zenith and the limit line is perpendicular to the Moon's azimuth, which Herald's factor in [Limb profile methods](../../20-solar-eclipses-and-transits/05-lunar-limb/limb-profile-methods.md#path-limits-and-the-graze-zone) accounts for in the eclipse case [@limb-herald-1983].

## Placing observers

### The elevation correction

The predicted limit is for sea level. An observer at height $h$ sees the Moon from a point displaced toward the Moon. The IOTA manual gives the [?occ-tan-z-correction|elevation correction] as [@occ-iota-manual-2007]

$$
d = h\tan z,
$$

with $z$ the zenith distance of the star at central graze, applied "in the direction of the Moon's azimuth". The limit line is then shifted parallel to itself by

$$
X = d\sin D = h\tan z\sin D,\qquad D = G - F,
$$

with $G$ the Moon's azimuth and $F$ the azimuth of the sea-level limit line [@occ-iota-manual-2007]. "The correction amount d can range from zero to 3 or 4 times the observer's elevation for a low altitude Moon", and corrections are usually made only above 200 metres [@occ-iota-manual-2007]. For a site north of latitude $+31^{\circ}$ the shift is always southward, because the Moon never reaches the zenith there [@occ-iota-manual-2007]. When the limit-line azimuth $F$ is not printed, the manual derives it from two limit points as $F = 90^{\circ} + b$ with $\tan b = \Delta\varphi/(\Delta\lambda\cos\varphi)$, a plane approximation over 10 km [@occ-iota-manual-2007]. The manual's example has $h = 596.7$ m and $\tan z = 1.65$, so $d = 984.8$ m and $X = 767$ m south of the sea-level line [@occ-iota-manual-2007]. Espenak's eclipse elevation factor $\tan(90^{\circ} - A)\sin D$ is the same expression with the altitude $A$ in place of the zenith distance [@limb-espenak-tp2001].

The manual's $D$ is an azimuth difference and $b$ a plane-triangle angle. Neither is this topic's coefficient $b$ or libration $b$.

### Station spacing on the profile

The manual's worked example is the graze of SAO 189348 on 2007 October 20 in Oklahoma. It shows how a leader reads the profile. Observations showed a 4 km mountain just after central graze and a 3 km peak near $-2$ minutes. "With more influence of the open circle data points from observations rather than the Watts data line a four station expedition is chosen" [@occ-iota-manual-2007]. One station is placed 0.8 km inside the mean limit. Three are placed outside it, at $+1.2$ km, $+2.2$ km and $+3.7$ km in the numbered list. The figure caption and map give $+2.7$ km for the third, so the manual is inconsistent there [@occ-iota-manual-2007]. Stations are left out of zones that "would likely be a long total occultation 6-7 minutes as the limb profile drifted over them" and out of zones with "risk of having a miss" [@occ-iota-manual-2007]. The time of central graze at the chosen road is found by linear interpolation in longitude between two table rows. In the example a 19 s difference over the interval places central graze at $0^\mathrm{h}\,53^\mathrm{m}\,22^\mathrm{s}$ UT. The observing window is then read from the profile as $-3.5$ to $+2.5$ minutes [@occ-iota-manual-2007].

Spacing perpendicular to the line samples the profile at different heights. The manual says a line of well-spaced observers gives "much better" resolution than a single chord [@occ-iota-manual-2007]. A double star gets two profiles. "If the difference in component magnitude of the double star is 1.5 or greater, it is best to position observers based on the profile of the brighter component" [@occ-iota-manual-2007].

### Mapping the line

The 2007 workflow plotted two limit points 10 to 20 km apart on a topographic or road map and drew the elevation-corrected line parallel to it [@occ-iota-manual-2007]. The RASC Handbook notes that IOTA overlays limit lines on Google Maps, "but further corrections are needed based on the predicted lunar profile and the observer's height above sea level" [@limb-dunham-rasc-2026]. The lunar-shadows repository automates both corrections for one event. It samples the LOLA 118 m digital elevation model (DEM) along each limb direction in the Moon's body frame for the highest point seen from the star. It projects that point along the star direction to a 6371 km spherical Earth, then walks the ray to the Copernicus terrain on WGS84 [@occ-lunar-shadows]. Its first intersection is with a sphere, and the repository documents no validation against observed grazes. It is a third-party reimplementation, useful as a reading of the steps rather than as a reference [@occ-lunar-shadows].

## What grazes measure now

The RASC Handbook for 2026 states the change. "Lunar orbiter and Gaia observations have obviated the main need for such observations." Because "the lunar topography is so well-known, recordings from only one to three stations are needed" [@limb-dunham-rasc-2026]. It also says that "especially grazing occultation observations have revealed small errors whose source is still being investigated" [@limb-dunham-rasc-2026]. That sentence names no error and no paper. The Occult tutorial advises that "grazing occultations are not likely to yield unique information about the star or the moon" now that Gaia and LOLA are available [@bes-occult-tutorial].

Double stars remain. "A resolution of 0.05" is obtainable from a graze of a double star observed visually along flat lunar surfaces", and "video observations of double stars can resolve 0.02" separations with favorable geometry" [@occ-iota-manual-2007]. The manual adds a caution: "gradual or fading events seen during grazes are more often due to grazing enhancement of Fresnel diffraction at the Moon's limb rather than to stellar duplicity" [@occ-iota-manual-2007]. The archive puts a number on visual false positives. Video has shown "that about 80% of double star discoveries reported from visual observations show no evidence of being double" [@occ-vizier-vi132c].

## Reducing a graze

A graze reduction is the ordinary reduction applied to each event, with the residual compared with the limb height at the event's position angle. [Planets, catalogues and reduction](planets-catalogues-and-reduction.md) gives that reduction. What differs is the error pattern. In the VI/132C rebuild, corrections to site coordinates dominate for grazes: 1700, 1265 and 3420 site corrections in the three periods, against 450, 817 and 496 for ordinary occultations [@occ-vizier-vi132c]. The reasons are concrete. Observers stood at road intersections identified on survey maps. One South African graze had altitudes recorded as 350 m that Google Earth showed to be 1350 m. One Florida observer was placed 40 km out to sea by a typing error. One expedition used the wrong cross-street for every station [@occ-vizier-vi132c]. Because each observer records a sequence, "an error in the time base means that all events will be in error by an equal amount", so one offset corrects all of an observer's events [@occ-vizier-vi132c]. A graze identifier groups all events of one graze. Where the same star was observed at both limbs on one night, both grazes carry the same identifier [@occ-vizier-vi132c].

## Sources compared

| Source | Limb data | Formulas and numbers | Unique content |
|---|---|---|---|
| ES 1961 section 10 [@occ-es1961] | Watts, then pending | Chart arguments $\Pi$, $l$, $b$; auxiliaries $A$ and $B$; scaling $0.0010723\,s''$ | The limb correction inside a reduction, the graze filter |
| Morrison 1979 [@occ-morrison-1979] | Computerised Watts | Topocentric libration corrections, 0.01 degree requirement, 0.25 degree shift | Why position angle precision matters |
| IOTA manual 2007 [@occ-iota-manual-2007] | Watts, ACLPPP, MoonLimb | $d = h\tan z$, $X = h\tan z\sin D$, zone width to 8 km | Profile reading, station placement, history of grazes |
| VI/132C doc [@occ-vizier-vi132c] | LOLA, P,D grid | 0.01 degree spacing, 0.01 arcsecond heights | Graze data corrections and their causes |
| Herald 2016 note [@limb-occult-accuracy-2016] | LOLA | 0.2 degree position-angle error, 0.3 s agreement | The fix in Occult's position angle |
| RASC 2026 [@limb-dunham-rasc-2026] | LOLA via Occult | 2 to 3 km zone | Current scientific status of grazes |
| lunar-shadows [@occ-lunar-shadows] | LOLA 118 m | Sphere then terrain | Open code for a DEM-corrected limit line |

## What a developer should do

Build the graze product on the same limb stage the eclipse pipeline uses. For each point along the smooth limit line, compute the topocentric libration and the event position angle to better than 0.01 degrees. Extract the LOLA profile over about $\pm 10$ degrees of position angle around the graze point, with the greatest-projected-distance rule. Emit the profile in kilometres perpendicular to the limit line with time ticks, as Occult does. Apply the observer-height shift $h\tan z\sin D$ per site, using ellipsoidal height consistently with the limit line. Better, intersect the star ray with the terrain model directly. Report double-star components as separate profiles. Test the position angle against an independent computation first, since Occult's own history shows that a 0.2 degree error survives casual checks. Read the IOTA manual chapter 5 and the VI/132C doc.txt before designing the product.

## What this changes

The pipeline needs a second limit-line mode for stars. In that mode the limit is a band with a profile across it. The limb stage must accept a star direction, because the profile of a graze depends only on the observer and the Moon, as for eclipses. The ground product needs a terrain step, which the eclipse limit lines already need for the same reason.

## Open questions

- Obtain Morrison 1970, the paper cited in Morrison 1979 for the $-0.25$ degree shift of Watts' chart position angles, to see how it was derived from grazes.
- Obtain Occult's help topic on graze profiles to record how its 2026 version bins position angle, which LOLA product it uses, and whether it intersects the terrain or applies $h\tan z$.
- Obtain the "small errors" in graze results that the RASC Handbook says are under investigation, as a paper or an IOTA report with the residuals.
- Obtain a definition of the $D$ coordinate in the VI/132C limb grid from Herald or from the Occult source.
- Obtain Riedel's GRAZPREP-4 documentation, which the British Astronomical Association (BAA) cites for placing mobile observers [@occ-baa-lunar].
