#!/usr/bin/env python3
"""Hidden, second example: the Sun lights Io, and Jupiter blocks the
observer's view of it. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Hidden: Jupiter blocks the observer's view of Io",
    ("Top left, the Sun, labelled light source, lighting Io along a line. "
     "Left, Io, labelled lit body. Middle, Jupiter, labelled blocking body, "
     "with a pale band stretching left from it: seen from the Earth, "
     "anything in that band is behind Jupiter. Io sits inside the band. "
     "Right, an observer on the Earth, labelled observer, whose dotted line "
     "of sight towards Io ends at Jupiter."),
)
y = AXIS + 16
sx, sy, sr = 78, 52, 30
ix, ir = 200, 8
jx, jr = 380, 38
ox = 620

f.rect(150, y - jr, jx - 150, 2 * jr, cls="cone")
f.line(sx + sr - 4, sy + 12, ix - ir, y - 4, cls="rule thin")
sun(f, sx, sy, sr)
f.circle(ix, y, ir, cls="body")
f.circle(jx, y, jr, cls="body")
f.circle(ox, y, 3.5, cls="accent-2-fill")
f.line(ox - 5, y, jx + jr + 4, y, cls="accent-2 thin dotted")
f.text(270, y - jr - 8, "seen from the Earth, Io is behind Jupiter here", anchor="middle",
       cls="label-dim")

labels(f, sx + sr + 12, sy - 6, "Light source", "the Sun", anchor="start")
labels(f, ix, y + jr + 26, "Lit body", "Io")
labels(f, jx, y + jr + 26, "Blocking body", "Jupiter")
labels(f, ox - 8, y + 30, "Observer", "on the Earth")

f.save(__file__, "../../content/05-primer/img/example-satellite-occultation.svg")
