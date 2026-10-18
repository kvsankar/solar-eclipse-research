#!/usr/bin/env python3
"""Hidden, third example: an asteroid blocks the starlight on its way to the
Earth, and its shadow path crosses the Earth as a narrow band. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Hidden: an asteroid blocks the starlight reaching part of the Earth",
    ("Left, a star, labelled light source, sending parallel lines of light. "
     "Middle, a small asteroid, labelled blocking body. Behind it a narrow "
     "band, its shadow in starlight, reaches the Earth on the right, which "
     "is drawn as a disc with the band crossing it. An observer inside the "
     "band, labelled observer, loses the star. Observers outside the band "
     "see nothing happen."),
)
y = AXIS
stx = 44
ax, ar = 300, 7
ex, er = 560, 70

for dy in (-30, 30):
    f.line(stx + 10, y + dy, ex - er - 10, y + dy, cls="accent thin", marker="arrow")
for dy in (-4, 4):
    f.line(stx + 10, y + dy, ax - ar - 6, y + dy, cls="accent thin", marker="arrow")
f.circle(ex, y, er, cls="body")
f.rect(ax, y - ar, ex + er - ax, 2 * ar, cls="cone-deep")
sun(f, stx, y, 6)
f.circle(ax, y, ar, cls="body")
f.circle(ex - 20, y, 3.5, cls="accent-2-fill")
f.text(ex, y + er + 18, "the Earth", anchor="middle", cls="label-dim")
f.text(ex, y + er + 32, "outside the band: nothing happens", anchor="middle", cls="label-dim")

labels(f, stx + 14, y + 52, "Light source", "a star")
labels(f, ax, y - 62, "Blocking body", "an asteroid")
labels(f, ex + er - 4, y - er - 22, "Observer", "on the Earth, in the shadow path", anchor="end")
f.line(ex - 20, y - 6, ex - 20, y - er - 2, cls="rule thin dotted")

f.save(__file__, "../../content/05-primer/img/example-asteroid-occultation.svg")
