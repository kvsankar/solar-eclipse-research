#!/usr/bin/env python3
"""Hidden, with a disc as the source: a solar eclipse. The observer stands in
the Moon's umbra, so the Moon hides the whole Sun. Schematic."""

import math

from prim_case import AXIS, labels, new, sun

f = new(
    "Hidden: the observer stands in the Moon's umbra and the Sun is hidden",
    ("Left, the Sun, labelled light source. Middle, the Moon, labelled "
     "blocking body. Behind the Moon a pale penumbra spreads out and a darker "
     "umbra narrows towards the Earth on the right, where both fall on the "
     "Earth's surface. An observer, labelled observer, stands inside the "
     "umbra on the Earth. An inset above shows what the observer sees: a "
     "total eclipse, the Moon's dark disc covering the Sun with a thin "
     "bright ring around it."),
)
y = AXIS
sx, sr = 80, 42
mx, mr = 300, 13

# The Earth: a full circle running off the right edge; x_s is its surface on
# the axis. The cones run on under the surface, which hides their ends.
ecx, er = 660, 100
xs = ecx - er
reach = xs + 30
umb = 13                            # the umbra's half-width where it reaches the Earth
pen = 46


for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, mx, y + sgn * mr, cls="rule thin")
f.polygon([(mx, y - mr), (reach, y - pen), (reach, y + pen), (mx, y + mr)], cls="cone")
f.polygon([(mx, y - mr), (reach, y - umb), (reach, y + umb), (mx, y + mr)], cls="cone-deep")
sun(f, sx, y, sr)
f.circle(mx, y, mr, cls="body")
f.circle(ecx, y, er, cls="body")
f.polygon([(xs - 1, y - umb + 1), (xs + 5, y - umb + 2), (xs + 5, y + umb - 2), (xs - 1, y + umb - 1)],
          cls="cone-deep")
ox, oy = xs + 1, y
f.circle(ox, oy, 3.5, cls="accent-2-fill")

# What the observer sees: totality.
ix, iy = 590, 34
f.circle(ix, iy, 22, cls="accent thin dotted")
f.circle(ix, iy, 17, cls="sun-fill")
f.circle(ix, iy, 15, cls="sun-fill")
f.circle(ix, iy, 15, cls="silhouette-fill")
f.line(ox, oy - 6, ix - 10, iy + 20, cls="accent-2 thin dotted")
f.text(ix - 28, iy + 4, "what they see: totality", anchor="end", cls="label-dim")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, mx, y + mr + 26, "Blocking body", "the Moon")
labels(f, xs - 50, y + 70, "Observer", "on the Earth", "in the Moon's umbra")
f.text((mx + reach) / 2 + 20, y + 4, "umbra", anchor="middle", cls="label-dim")

f.save(__file__, "../../content/05-primer/img/example-solar-eclipse.svg")
