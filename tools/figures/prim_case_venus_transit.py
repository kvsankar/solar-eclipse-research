#!/usr/bin/env python3
"""Hidden, with a disc as the source: a transit of Venus. Venus blocks part of the
observer's view of the Sun, so the observer stands in Venus's antumbra and
sees a dot on the Sun. Schematic."""

from prim_case import AXIS, labels, new, sun, view_panel

f = new(
    "Hidden: the observer stands in Venus's antumbra and sees a dot on the Sun",
    ("Left, the Sun, labelled light source. Middle, Venus, labelled blocking "
     "body, small. Its dark umbra closes to a point a short way behind it, "
     "and beyond that point the antumbra opens out towards the Earth on the "
     "right. An observer on the Earth, labelled observer, stands in the "
     "antumbra. A framed panel on the right shows what the observer sees: "
     "a small dark dot on the Sun's disc."),
    panel=True,
)
y = AXIS
sx, sr = 80, 44
vx, vr = 260, 6
vertex = 320
ecx, er = 660, 100
xs = ecx - er                       # the Earth's surface on the axis
ex = xs + 30                        # the cones run on under the surface

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, vx, y + sgn * vr, cls="rule thin")
f.polygon([(vx, y - vr), (vertex, y), (vx, y + vr)], cls="cone-deep")
f.polygon([(vertex, y), (ex, y - 26), (ex, y + 26)], cls="cone")
f.polyline([(vx, y - vr), (vertex, y), (ex, y - 26)], cls="rule thin")
f.polyline([(vx, y + vr), (vertex, y), (ex, y + 26)], cls="rule thin")
sun(f, sx, y, sr)
f.circle(vx, y, vr, cls="body")
f.circle(ecx, y, er, cls="body")
f.circle(xs + 1, y, 3.5, cls="accent-2-fill observer")
f.text((vertex + ex) / 2, y + 4, "antumbra", anchor="middle", cls="label-dim")

# What the observer sees: a dot on the Sun, in its own panel.
ix, iy = view_panel(f)
f.circle(ix, iy, 40, cls="sun-fill")
f.circle(ix + 13, iy - 7, 5.5, cls="silhouette-fill")
f.text(ix, iy + 62, "Venus, a dot on the Sun", anchor="middle", cls="label-dim")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, vx, y + 36, "Blocking body", "Venus")
labels(f, xs - 44, y + 62, "Observer", "on the Earth", "in Venus's antumbra")

f.save(__file__, "../../content/05-primer/img/example-venus-transit.svg")
