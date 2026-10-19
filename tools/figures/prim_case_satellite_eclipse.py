#!/usr/bin/env python3
"""Darkened, second example: Jupiter blocks the sunlight reaching Io, which
goes dark for every observer who can see it. Schematic."""

from prim_case import AXIS, labels, new, observer_on_earth, sun

f = new(
    "Darkened: Jupiter blocks the sunlight reaching Io",
    ("Left, the Sun, labelled light source. Middle, Jupiter, labelled "
     "blocking body, with its shadow stretching to the right. Inside the "
     "shadow, Io, labelled darkened body. Below, an observer on the Earth, "
     "labelled observer, looks up along a dotted line at the darkened Io."),
)
y = AXIS
sx, sr = 72, 46
jx, jr = 300, 30
ix, ir = 520, 8

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, jx, y + sgn * jr, cls="rule thin")
f.polygon([(jx, y - jr), (650, y - 22), (650, y + 22), (jx, y + jr)], cls="cone-deep")
sun(f, sx, y, sr)
f.circle(jx, y, jr, cls="body")
f.circle(ix, y, ir, cls="body")
f.circle(ix, y, ir, cls="cone-deep")
ox, oy = 585, 190
observer_on_earth(f, ox, oy, ix, y + ir)
f.line(ox - 3, oy - 4, ix + 4, y + ir + 2, cls="accent-2 thin dotted")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, jx, y + jr + 26, "Blocking body", "Jupiter")
labels(f, ix, 44, "Darkened body", "Io, in Jupiter's shadow")
labels(f, ox - 12, oy - 6, "Observer", "on the Earth", anchor="end")

f.save(__file__, "../../content/05-primer/img/example-satellite-eclipse.svg")
