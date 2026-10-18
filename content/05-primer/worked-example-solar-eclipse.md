---
title: Worked example: a solar eclipse
description: Follow a solar eclipse calculation from Sun and Moon positions to shadow geometry and contact times, with links to algorithms and formulas.
order: 2
status: working
updated: 2026-10-18
seo_title: How to Calculate a Solar Eclipse: Methods and Formulas
---

::: summary
- **A solar eclipse is a shadow problem.** The Moon casts two cones, the [?umbra] and the [?penumbra], and the computation asks where and when each cone touches the Earth.
- **Bessel's method describes a smooth shadow on one plane** through the Earth's centre, the [?fundamental-plane], using the [?besselian-elements]. Direct topocentric calculations are another route to local contacts. Terrain and limb tests require additional inputs [@bes-es1961] [@bes-quaglia-2021] [@svs-wright-young-2024].
- **The elements carry the constants.** The Sun's radius, the Moon's radius and the choice of ephemeris all enter here, so two tables of elements for the same eclipse can differ.
- **The Earth rotates under the shadow**, and how far it has rotated depends on [?delta-t], the one input that cannot be computed in advance.
- **The Moon is not round and the Sun has no edge.** Those two facts, not the orbits, set the limit of what any prediction can promise at the edge of the path.
:::

## Two cones

Hold a coin in front of a lamp and it casts a dark inner shadow that
narrows to a point, and a lighter outer shadow that widens. The Moon does the
same with the Sun. The inner cone is the umbra. Where its tip reaches the
ground, observers see a total eclipse. If the tip falls short of the ground,
its extension beyond the tip, the [?antumbra], sweeps the ground instead and
observers see a ring of Sun around the Moon, an annular eclipse. The outer
cone is the penumbra, and anyone inside it sees a partial eclipse.

The whole computation is the geometry of those cones against a rotating,
slightly flattened Earth. Modern ephemerides fit recent lunar laser-ranging observations with range
residuals near a centimetre. That is not an accuracy bound on every component
of the Earth-Moon position [@moon-park-2021]. What is not known perfectly is the size of the Sun, the
shape of the Moon's edge, and how far the Earth has turned.

## Bessel's plane

Friedrich Bessel's contribution in 1829 was to stop working on the Earth's
surface and work instead on a plane through the Earth's centre, perpendicular
to the line from the Sun through the Moon, the shadow axis. On that plane the
shadow of a round Moon is a circle, and it moves almost in a straight line.
Eight numbers describe it: the position of the axis on the plane ($x$, $y$),
the direction of the axis on the sky ($d$, $\mu$), the radii of the penumbra
and umbra on the plane ($l_1$, $l_2$), and the half-angles of the two cones
($\tan f_1$, $\tan f_2$). Published tables give the first six as short
polynomials in time, valid for about six hours, and the two cone angles as
constants [@bes-es1961] [@bes-nasa-2024-elements].

The elements are computed from the apparent positions of the Sun and Moon
and from four constants: the Sun's radius, the Moon's radius as a fraction of
the Earth's ($k$), the Earth's equatorial radius and flattening. Two values of
$k$ are in use, one for the penumbra and a smaller one for the umbra, because
the smaller value reproduces observed durations of totality better
[@bes-nasa-radius]. Everything downstream inherits these choices.

## From the plane to a map

To find where the shadow falls at a given instant, draw the line from the
shadow's centre on the plane parallel to the axis and see where it meets the
Earth's ellipsoid. That point is on the [?central-line]. Repeat for the edges
of the umbral circle and you get the northern and southern [?path-limit]
lines. Repeat for the penumbral circle and you get the outline of the region
seeing a partial eclipse. The mathematics is a square root for the centre and
a one-dimensional root-find for the limits, both given in full in the
[global circumstances](../10-raw/20-solar-eclipses-and-transits/03-global-circumstances/_index.md) notes
[@glob-es1961].

The duration of totality at a point on the central line is the umbral
diameter divided by the speed of the shadow relative to the ground. The shadow
moves at about a kilometre a second, so a 100 km umbra gives about two minutes
[@glob-es1992].

## From the plane to one place

For a single observer the question is reversed: project the observer onto
the fundamental plane, and ask when the distance from the observer's projected
position to the shadow centre equals the shadow radius. That gives first and
fourth contact for the penumbra and second and third contact for the umbra.
The [?eclipse-magnitude] is the fraction of the Sun's diameter covered at
maximum; the [?obscuration] is the fraction of its area, which is a different
number found from the overlap of two circles. NASA's own JavaScript calculator
does exactly this in 1,200 lines, and the
[local circumstances](../10-raw/20-solar-eclipses-and-transits/04-local-circumstances/_index.md) notes walk
through it [@loc-es1961-local] [@loc-jsex-program-js].

## The Earth turns

The elements are computed in Terrestrial Time, a uniform clock. Longitudes on
the Earth depend on Universal Time, which follows the Earth's irregular
rotation. The difference, [?delta-t], is about 69 seconds today and drifts
unpredictably by a fraction of a second a year. One second of error moves the
whole eclipse about 350 m east or west at mid-latitudes. Predictions made
years ahead for 2024 were 1.4 to 2.3 s off, and a canon of eclipses two
thousand years ago carries an uncertainty of over four minutes, which is about
a hundred kilometres [@earth-usno-deltat-data] [@val-gsfc-uncertainty].

## The Moon is not round

At the scale of an eclipse edge the Moon's silhouette departs from a circle by
up to about 3 arcseconds, which is 6 km of lunar mountain and valley. A valley
on the trailing edge lets sunlight through a few seconds longer; a mountain
cuts it off early. Those are [?bailys-beads]. Laser altimeters on the SELENE
and Lunar Reconnaissance Orbiter missions have mapped the Moon to a few metres,
so the [?limb-profile] seen from any place at any instant can be built from a
digital elevation model. Applying it moves second and third contact by 2 to
3 s anywhere in the path and by tens of seconds near the edge, and turns the
umbra from an ellipse into a polygon with one side per valley
[@limb-herald-1983] [@svs-wright-young-2024].

![Each bead is sunlight reaching the observer through one lunar valley, so the beads measure the limb profile directly, at the position angles where they appear. Totality begins only when the last of them closes, which is why a prediction that assumes a round Moon states the wrong second. National Park Service / Jacob W. Frank, Craters of the Moon, Idaho, 2017 August 21 [@limb-herald-1983].](img/bailys-beads-2017.jpg)

## The Sun has no edge

Totality means the last of the bright photosphere has gone. Where exactly the
photosphere ends is a question of physics, not geometry. The value almost every
prediction uses, 959.63 arcseconds at one astronomical unit, dates from 1891.
Flash-spectrum and light-curve studies infer a radius about a third of an
arcsecond larger. Timing-based bead results depend on the adopted lunar limb
and detection threshold. The cited radius difference moves a limit inward
by about 600 m in the studied geometry. Its duration effect depends on the
observer's distance from that limit
[@sun-quaglia-2021] [@val-besselian-maps-accuracy].

![The corona is what the eye sees, but it is not what the computation solves for. Totality is the instant the last of the photosphere is hidden, and the photosphere has no sharp edge, so the moment has to be defined by a chosen radius rather than observed from the image. NASA's Scientific Visualization Studio, from Kerrville, Texas, 2024 April 8 [@sun-quaglia-2021].](img/totality-corona-2024.jpg)

## Where the products come from

Fred Espenak's tables on the NASA eclipse site and EclipseWise are computed
from the elements with a round Moon and observers at sea level, and Espenak
states that the limb moves the limits by 1 to 3 km. Xavier Jubier's
interactive maps add limb corrections at a clicked point. NASA's Scientific
Visualization Studio, in Ernie Wright's work for 2017, 2023 and 2024, puts
every map pixel at its true height and tests it against the true limb, and provides
reference map products for comparison. Dave Herald's
Occult is the
occultation community's tool for beads. Other surveyed apps use several computational methods and input datasets
[@svs-espenak-2024-path] [@svs-wright-young-2024] [@sw-occult4].

The [reports](../20-reports/_index.md) turn this into a pipeline a developer
can build, with the constants, the data files and the tests.

## What changes for other events

The steps above carry over to every event in the
[general primer](how-eclipses-occultations-and-transits-are-computed.md). Only
some of them change.

- **A lunar eclipse** swaps the roles. The Earth casts the shadow and the
  Moon moves through it, so the elements shrink to the Moon's position and
  three limiting separations. The contacts are the same instant for everyone,
  so there is no path and no step from the plane to one place. A new input,
  the enlargement of the Earth's shadow by its atmosphere, takes the place of
  the lunar limb [@lun-herald-sinnott-2014]. See
  [Lunar eclipses](../10-raw/30-lunar-eclipses/_index.md).
- **An occultation of a star** keeps every step but changes the source. The
  star is a point at infinity, so the two cones become one cylinder of the
  Moon's radius and there is no penumbra. The limb profile matters even more
  near the limits, where the star grazes the Moon's edge [@occ-es1961]. See
  [Lunar occultations](../10-raw/40-occultations/13-lunar-occultations/_index.md).
- **A transit of Mercury or Venus** keeps every step with the planet in place
  of the Moon. The planet is far too small to cover the Sun, so only the
  penumbra and the antumbra reach the Earth. The planet's radius joins the
  Sun's as an input that moves every contact [@tr-es1961]. See
  [Transits of Mercury and Venus](../10-raw/20-solar-eclipses-and-transits/14-transits/_index.md).
