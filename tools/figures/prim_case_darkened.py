#!/usr/bin/env python3
"""The darkened case, shown as a lunar eclipse: the Earth blocks the sunlight
reaching the Moon, which goes dark for everyone who can see it. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Darkened: the Earth blocks the sunlight reaching the Moon",
    ("Left, the Sun, labelled light source. Middle, the Earth, labelled "
     "blocking body, with sunlight reaching it and its shadow stretching to "
     "the right. Right, the Moon inside that shadow, labelled darkened body. "
     "An observer on the Earth's night side, labelled observer, looks along a "
     "dotted line at the darkened Moon."),
)
y = AXIS
sx, sr = 80, 42
ex, er = 330, 26
mx, mr = 540, 12

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, ex, y + sgn * er, cls="rule thin")
f.polygon([(ex, y - er), (640, y - 9), (640, y + 9), (ex, y + er)], cls="cone-deep")
sun(f, sx, y, sr)
f.circle(ex, y, er, cls="body")
f.circle(mx, y, mr, cls="body")
f.circle(mx, y, mr, cls="cone-deep")

ox, oy = ex + er - 4, y - 10
f.circle(ox, oy, 3.5, cls="accent-2-fill observer")
f.line(ox + 4, oy, mx - mr - 3, y - 3, cls="accent-2 thin dotted")
f.line(ox, oy - 4, 400, 52, cls="rule thin dotted")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, ex, y + er + 26, "Blocking body", "the Earth")
labels(f, mx, y + mr + 26, "Darkened body", "the Moon", "in the Earth's shadow")
labels(f, 404, 34, "Observer", "on the Earth's night side", anchor="start")

f.save(__file__, "../../content/05-primer/img/case-darkened.svg")
