#!/usr/bin/env python3
"""Darkened, third example: Io blocks the sunlight reaching a patch of
Jupiter's cloud tops, its shadow transit. Schematic."""

from prim_case import AXIS, labels, new, observer_on_earth, sun

f = new(
    "Darkened: Io blocks the sunlight reaching Jupiter's cloud tops",
    ("Left, the Sun, labelled light source. Middle, Io, labelled blocking "
     "body, casting a long narrow shadow to the right. Right, Jupiter, "
     "labelled darkened body, with a small dark spot where Io's shadow meets "
     "its cloud tops. Below, an observer on the Earth, labelled observer, "
     "looks along a dotted line at the spot."),
)
y = AXIS
sx, sr = 72, 46
ix, ir = 280, 8
jx, jr = 560, 64

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, ix, y + sgn * ir, cls="rule thin")
f.polygon([(ix, y - ir), (jx - jr + 4, y - 5), (jx - jr + 4, y + 5), (ix, y + ir)],
          cls="cone-deep")
sun(f, sx, y, sr)
f.circle(ix, y, ir, cls="body")
f.circle(jx, y, jr, cls="body")
f.circle(jx - jr + 7, y, 6, cls="cone-deep")
f.circle(jx - jr + 7, y, 6, cls="cone-deep")
f.circle(jx - jr + 7, y, 6, cls="rule thin")
ox, oy = 420, 200
observer_on_earth(f, ox, oy, jx - jr + 5, y + 8)
f.line(ox + 3, oy - 4, jx - jr + 5, y + 8, cls="accent-2 thin dotted")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, ix, y + ir + 26, "Blocking body", "Io")
labels(f, jx, 30, "Darkened body", "Jupiter's cloud tops, a patch")
labels(f, ox - 46, oy + 12, "Observer", "on the Earth", anchor="end")

f.save(__file__, "../../content/05-primer/img/example-shadow-transit.svg")
