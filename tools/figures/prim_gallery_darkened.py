#!/usr/bin/env python3
"""Gallery of the darkened case: a body cuts the sunlight reaching another
body, which goes dark for everyone who can see it. Schematic only."""

from prim_gallery import PANEL, caption, cone, eye, new, sun

f = new(
    "Darkened: a body cuts the sunlight reaching another body",
    ("Three panels. Left, lunar eclipse: the Sun, the Earth and its shadow "
     "cone, with the Moon inside the shadow; an observer on the Earth's "
     "night side looks at it. Middle, eclipse of a satellite: the Sun, "
     "Jupiter and its shadow, with Io inside; the observer looks from "
     "elsewhere. Right, shadow transit: the Sun, Io between the Sun and "
     "Jupiter, and Io's small shadow falling on Jupiter's disc as a dark "
     "spot."),
)
y = 110

# Lunar eclipse.
x0 = 0
sun(f, x0 + 28, y)
cone(f, x0 + 100, y, 22, x0 + 205, 9)
f.circle(x0 + 100, y, 22, cls="body")
f.circle(x0 + 175, y, 9, cls="body")
f.circle(x0 + 175, y, 9, cls="cone-deep")
eye(f, x0 + 112, y + 17, x0 + 170, y + 6)
f.text(x0 + 100, y + 4, "Earth", anchor="middle", cls="label-dim")
caption(f, 0, "Lunar eclipse", ["the Moon in the Earth's shadow", "same instant for everyone"])

# Eclipse of a satellite by its planet.
x0 = PANEL
sun(f, x0 + 28, y)
cone(f, x0 + 100, y, 26, x0 + 215, 20)
f.circle(x0 + 100, y, 26, cls="body")
f.circle(x0 + 175, y - 4, 6, cls="body")
f.circle(x0 + 175, y - 4, 6, cls="cone-deep")
eye(f, x0 + 150, y + 62, x0 + 174, y + 2)
f.text(x0 + 100, y + 4, "Jupiter", anchor="middle", cls="label-dim")
f.text(x0 + 183, y - 14, "Io", cls="label-dim")
caption(f, 1, "Eclipse of a satellite", ["Io in Jupiter's shadow", "seen from the Earth"])

# Shadow transit.
x0 = 2 * PANEL
sun(f, x0 + 28, y)
f.circle(x0 + 85, y - 6, 6, cls="body")
cone(f, x0 + 85, y - 6, 6, x0 + 152, 3)
f.circle(x0 + 175, y, 28, cls="body")
f.circle(x0 + 152, y - 6, 4.5, cls="cone-deep")
f.circle(x0 + 152, y - 6, 4.5, cls="rule thin")
eye(f, x0 + 130, y + 64, x0 + 150, y + 2)
f.text(x0 + 85, y - 16, "Io", anchor="middle", cls="label-dim")
f.text(x0 + 186, y + 4, "Jupiter", anchor="middle", cls="label-dim")
caption(f, 2, "Shadow transit", ["Io's shadow on Jupiter's", "cloud tops"])

f.save(__file__, "../../content/05-primer/img/gallery-darkened.svg")
