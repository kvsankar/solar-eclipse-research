---
title: How eclipses, occultations and transits are computed
description: One idea explains every event on this site: a body cuts the light path from a source to an observer. Where it cuts the path decides what happens.
order: 1
status: working
updated: 2026-10-18
seo_title: Eclipses, Occultations and Transits Explained with One Geometry
---

::: summary
- **Every event is one body cutting a light path.** Light travels from a source, the Sun or a star, to an observer, either directly or by reflecting off a body such as the Moon or a planet. An event happens when another body cuts that path.
- **Where it cuts the path decides what happens.** Cutting the light that reaches a body darkens it for everyone. Cutting the light that reaches the observer hides something from that observer only. Cutting the observer's view of the source itself does both.
- **The shadow's shape follows from the source's size.** The Sun casts a cone with an umbra, a penumbra and an antumbra, which give total, partial and annular events. A star casts a cylinder, so it vanishes at once [@bes-es1961] [@occ-es1961].
- **The names come from history, and the geometry is shared.** The Explanatory Supplement itself notes that a solar eclipse is really an occultation [@prim-es1992-terms]. The same construction computes them all.
:::

## The light path

Light leaves a source and reaches an observer. Sometimes it travels straight
there, as when we look at the Sun or a star. Sometimes it first lights a
body, such as the Moon, a planet or a satellite, and reaches us by
reflection. A body that gets in the way cuts the path in one of three
places: the light on its way to a lit body, the light on its way to the
observer, or the observer's view of the source itself. The three sections
below take each in turn. In every diagram each body has two labels: the part
it plays, and what it is in that example.

## Darkened: a body goes dark for everyone

When a body cuts the sunlight reaching another body, that body goes dark.
This is an [?eclipse] in the strict sense. Everyone who can see the darkened
body sees it at the same instant, apart from the time light takes to reach
them, so a prediction is a list of times rather than a map of paths. Where
the observer stands only decides whether the body is above their horizon
[@lun-5mcle-tp2009].

![In a lunar eclipse the Earth blocks the sunlight on its way to the Moon, so the Moon goes dark for everyone on the Earth's night side, wherever they stand.](img/case-darkened.svg)

- A **lunar eclipse** is the Moon in the Earth's shadow
  [@lun-5mcle-tp2009].
- An **eclipse of a satellite** is, for example, Io in Jupiter's shadow
  [@jup-imcce-phenjupiter-readme].
- A **shadow transit** is a satellite's shadow falling on its planet's cloud
  tops, a patch of the planet in eclipse [@jup-imcce-phenjupiter-readme].
- A **mutual eclipse** is one satellite in another satellite's shadow
  [@jup-imcce-phenjupiter-readme].

![Jupiter blocks the sunlight on its way to Io, so Io goes dark for every observer who can see it.](img/example-satellite-eclipse.svg)

![Io blocks the sunlight on its way to a patch of Jupiter's cloud tops, which shows as a dark spot: a shadow transit.](img/example-shadow-transit.svg)

![When played, the Moon crosses the Earth's shadow and its copper tint deepens in the umbra, where only sunlight bent through the Earth's atmosphere reaches it. The still frame is totality.](img/anim-lunar-eclipse.svg){.anim}

## Hidden: something disappears for one observer

When a body cuts the light on its way to the observer, something disappears
for that observer only. This is an [?occultation]. A body nearby, or one
looking from somewhere else, may see nothing happen, so the time depends on
where the observer stands [@occ-es1961].

![In a lunar occultation the Moon blocks the starlight on its way to the observer. Only observers inside the band behind the Moon lose sight of the star.](img/case-hidden.svg)

- The Moon **occults a star or a planet** [@occ-es1961].
- An **asteroid or a trans-Neptunian object occults a star**. Only observers
  inside a narrow band on the Earth see it
  [@mb-gomes-junior-2022-sora].
- A planet **occults its own satellite**, and a satellite **transits** across
  its planet [@jup-imcce-phenjupiter-readme].
- One satellite **occults another**, a mutual occultation
  [@jup-imcce-phenjupiter-readme].
- One planet **occults another**, which last happened in 1818
  [@mb-gray-mutual].

A star is so far away that its light arrives in parallel lines. The body
then casts a "shadow" in starlight that is a cylinder exactly as wide as the
body. That shadow darkens nothing, but it is how these events are computed:
an occultation is predicted as the path of that cylinder across the Earth
[@occ-es1961] [@mb-gomes-junior-2022-sora].

![The Sun lights Io, and Jupiter blocks the observer's view of it: an occultation of a satellite by its planet.](img/example-satellite-occultation.svg)

![An asteroid blocks the starlight on its way to a narrow band across the Earth. Only observers inside that band see the star disappear.](img/example-asteroid-occultation.svg)

![When played, Io goes once round Jupiter and passes the four places where each kind of event happens. The angle between the Sun and the Earth is exaggerated to separate them. The still frame shows Io in Jupiter's shadow.](img/anim-io-orbit.svg){.anim}

## Both: the observer stands in a shadow

When a body cuts the observer's view of the source itself, both things
happen at once. The observer stands in the body's shadow, and the observer
sees the source hidden by the body. These are the same fact described two
ways. This is why the Supplement says a solar eclipse is really an
occultation, and why it describes a [?transit] of Mercury or Venus as a
planet's shadow falling on the Earth [@prim-es1992-terms].

![In a solar eclipse the Moon blocks the observer's view of the Sun. The same observer stands in the Moon's shadow, so being in the shadow and seeing the Sun hidden are one event.](img/case-both.svg)

- A **solar eclipse**: the observer stands in the Moon's shadow
  [@bes-es1961].
- A **transit of Mercury or Venus**: the observer stands in the planet's
  shadow, which is far too narrow to cover the Sun [@tr-es1961].

![Venus is far too small to cover the Sun, so its umbra closes before reaching the Earth. The observer stands in the antumbra and sees a dot cross the Sun.](img/example-venus-transit.svg)

![When played, the Moon's shadow slides across the Earth while, on the right, the Moon slides across the Sun as the observer at the dot sees it. The Sun is fully covered only while the umbra is on the observer. The still frame is totality.](img/anim-solar-eclipse.svg){.anim}

## The shape of a shadow

The source's size decides the shadow's shape. The Sun is a disc, so a body
casts a cone with three parts [@bes-es1961]:

- the [?umbra], where the whole Sun is hidden and the event is **total**;
- the [?antumbra], beyond the point where the umbra closes, where the body
  looks smaller than the Sun and the event is **annular**;
- the [?penumbra], where part of the Sun is hidden and the event is
  **partial**.

A transit is the annular case with a body far too small to cover the Sun:
the observer is in the planet's antumbra and sees a dot on the Sun
[@tr-es1961]. A star is a point, so its shadow is a cylinder with no
penumbra. The star does not fade but vanishes at once, apart from faint
diffraction fringes [@occ-es1961].

![The source's size decides the shadow's shape: the Sun gives a cone whose umbra, penumbra and antumbra give total, partial and annular views, and a star gives a cylinder with no penumbra, so it vanishes at once.](img/shadow-shape.svg)

The computation follows the same steps for every event. Choose a plane
perpendicular to the shadow, the [?fundamental-plane]. Find the body's
shadow on it as a circle. Find the observer on it as a point. An event begins
and ends when the point crosses the circle [@bes-es1961] [@occ-es1961].

## Which events fall where

| Event | Case | Where it is covered |
|---|---|---|
| Solar eclipse | Both | [Solar eclipses and transits](../10-raw/20-solar-eclipses-and-transits/_index.md) |
| Transit of Mercury or Venus | Both | [Transits](../10-raw/20-solar-eclipses-and-transits/14-transits/_index.md) |
| Lunar eclipse | Darkened | [Lunar eclipses](../10-raw/30-lunar-eclipses/_index.md) |
| Eclipse of a satellite | Darkened | [Jupiter's satellites](../10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) |
| Shadow transit | Darkened | [Jupiter's satellites](../10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) |
| Mutual eclipse | Darkened | [Planetary satellites](../10-raw/50-planetary-satellites/_index.md) |
| Lunar occultation of a star | Hidden | [Lunar occultations](../10-raw/40-occultations/13-lunar-occultations/_index.md) |
| Lunar occultation of a planet | Hidden | [Lunar occultations](../10-raw/40-occultations/13-lunar-occultations/_index.md) |
| Occultation by an asteroid or TNO | Hidden | [Occultations by planets and minor bodies](../10-raw/40-occultations/17-occultations-by-planets-and-minor-bodies/_index.md) |
| Occultation of a satellite by its planet | Hidden | [Jupiter's satellites](../10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) |
| Transit of a satellite | Hidden | [Jupiter's satellites](../10-raw/50-planetary-satellites/15-jupiter-satellites/_index.md) |
| Mutual occultation | Hidden | [Planetary satellites](../10-raw/50-planetary-satellites/_index.md) |
| Occultation of one planet by another | Hidden | [Occultations by planets and minor bodies](../10-raw/40-occultations/17-occultations-by-planets-and-minor-bodies/_index.md) |

## How the Explanatory Supplement names them

The 1992 Explanatory Supplement uses four names [@prim-es1992-terms]:

- an **eclipse**, when one body passes into the shadow of another;
- an **occultation**, when a larger body passes in front of a smaller one;
- a **transit**, when a smaller body passes in front of a larger one;
- a **shadow transit**, when the shadow of a smaller body passes in front of
  a larger one.

Its chapter on eclipses draws the line between shadow and line of sight. It
adds that long observation from the Earth gave the events their names before
the distinction was understood [@prim-es1992-terms]. In the terms of this
page, its eclipse is the darkened case. Its occultation and transit are the
hidden case, told apart only by which body looks larger. A solar eclipse
and a transit of a planet across the Sun are the case where both happen at
once.

## Where to go next

- The [worked example](worked-example-solar-eclipse.md) follows one solar
  eclipse from the positions of the Sun and the Moon to the second totality
  begins at one place.
- The [glossary](glossary.md) defines every term the site explains inline.
- The [research notes](../10-raw/_index.md) are grouped by these cases.
- The [reports](../20-reports/_index.md) set out the computation pipeline,
  its error budget and the open questions.
