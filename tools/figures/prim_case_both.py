#!/usr/bin/env python3
"""The both case, shown as a solar eclipse: the Moon blocks the observer's
view of the Sun, so the observer stands in the Moon's shadow. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Both: the Moon blocks the observer's view of the Sun",
    ("Left, the Sun, labelled light source. Middle, the Moon, labelled "
     "blocking body, with sunlight reaching it. Behind the Moon a pale "
     "penumbra spreads out and a darker umbra narrows towards the Earth on "
     "the right. An observer on the Earth, labelled observer, stands where "
     "the umbra meets the Earth. An inset above shows what the observer "
     "sees: the Sun covered by the Moon."),
)
y = AXIS
sx, sr = 80, 42
mx, mr = 300, 13
ex = 570

for sgn in (-1, 1):
    f.line(sx, y + sgn * sr, mx, y + sgn * mr, cls="rule thin")
f.polygon([(mx, y - mr), (ex, y - 44), (ex, y + 44), (mx, y + mr)], cls="cone")
f.polygon([(mx, y - mr), (ex, y - 3), (ex, y + 3), (mx, y + mr)], cls="cone-deep")
sun(f, sx, y, sr)
f.circle(mx, y, mr, cls="body")
f.path(f"M {ex + 20} {y - 70} A 80 80 0 0 0 {ex + 20} {y + 70}", cls="body")
f.circle(ex - 2, y, 3.5, cls="accent-2-fill")

# What the observer sees.
ix, iy = 600, 34
f.circle(ix, iy, 20, cls="accent thin dotted")
f.circle(ix, iy, 15, cls="sun-fill")
f.circle(ix, iy, 15.5, cls="sky-fill")
f.line(ex, y - 6, ix - 12, iy + 16, cls="accent-2 thin dotted")
f.text(ix - 26, iy + 4, "what they see", anchor="end", cls="label-dim")

labels(f, sx, y + sr + 26, "Light source", "the Sun")
labels(f, mx, y + mr + 26, "Blocking body", "the Moon")
labels(f, ex - 30, y + 84, "Observer", "on the Earth", "in the Moon's shadow")

f.save(__file__, "../../content/05-primer/img/case-both.svg")
