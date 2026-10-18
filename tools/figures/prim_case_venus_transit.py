#!/usr/bin/env python3
"""Both, second example: a transit of Venus. Venus blocks part of the
observer's view of the Sun, so the observer stands in Venus's antumbra and
sees a dot on the Sun. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Both: Venus blocks part of the observer's view of the Sun",
    ("Left, the Sun, labelled light source. Middle, Venus, labelled blocking "
     "body, small. Its dark umbra closes to a point a short way behind it, "
     "and beyond that point the antumbra opens out towards the Earth on the "
     "right. An observer on the Earth, labelled observer, stands in the "
     "antumbra. An inset shows what the observer sees: a small dark dot on "
     "the Sun's disc."),
)
y = AXIS
sx, sr = 80, 44
vx, vr = 260, 6
vertex = 320
ex = 580

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, vx, y + sgn * vr, cls="rule thin")
f.polygon([(vx, y - vr), (vertex, y), (vx, y + vr)], cls="cone-deep")
f.polygon([(vertex, y), (ex, y - 26), (ex, y + 26)], cls="cone")
f.polyline([(vx, y - vr), (vertex, y), (ex, y - 26)], cls="rule thin")
f.polyline([(vx, y + vr), (vertex, y), (ex, y + 26)], cls="rule thin")
sun(f, sx, y, sr)
f.circle(vx, y, vr, cls="body")
f.path(f"M {ex + 20} {y - 70} A 80 80 0 0 0 {ex + 20} {y + 70}", cls="body")
f.circle(ex - 2, y, 3.5, cls="accent-2-fill")
f.text((vertex + ex) / 2, y + 4, "antumbra", anchor="middle", cls="label-dim")

ix, iy = 610, 30
f.circle(ix, iy, 18, cls="sun-fill")
f.circle(ix + 6, iy - 3, 2.6, cls="sky-fill")
f.line(ex, y - 6, ix - 8, iy + 18, cls="accent-2 thin dotted")
f.text(ix - 26, iy + 4, "what they see", anchor="end", cls="label-dim")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, vx, y + 36, "Blocking body", "Venus")
labels(f, ex - 64, y + 62, "Observer", "on the Earth", "in Venus's antumbra")

f.save(__file__, "../../content/05-primer/img/example-venus-transit.svg")
