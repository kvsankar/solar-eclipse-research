#!/usr/bin/env python3
"""The hidden case, shown as a lunar occultation of a star: the Moon blocks
the starlight on its way to the observer. Schematic."""

from prim_case import AXIS, labels, new, sun

f = new(
    "Hidden: the Moon blocks the starlight reaching the observer",
    ("Left, a star, labelled light source, sending parallel lines of light "
     "to the right. Middle, the Moon, labelled blocking body. The lines that "
     "meet the Moon stop there, and a pale band behind the Moon marks where "
     "the star cannot be seen. Lines above and below the Moon carry on. "
     "Right, an observer on the Earth, labelled observer, inside the band."),
)
y = AXIS
stx = 44
mx, mr = 330, 22
ox = 600

f.rect(mx, y - mr, ox - mx, 2 * mr, cls="cone")
for dy in (-38, 38):
    f.line(stx + 10, y + dy, 650, y + dy, cls="accent thin", marker="arrow")
for dy in (-12, 0, 12):
    f.line(stx + 10, y + dy, mx - mr - 6, y + dy, cls="accent thin", marker="arrow")
sun(f, stx, y, 6)
f.circle(mx, y, mr, cls="body")
f.path(f"M {ox + 26} {y - 60} A 70 70 0 0 0 {ox + 26} {y + 60}", cls="body")
f.circle(ox, y, 3.5, cls="accent-2-fill")
f.line(ox - 5, y, mx + mr + 4, y, cls="accent-2 thin dotted")

labels(f, stx + 14, y + 58, "Light source", "a star", anchor="middle")
labels(f, mx, y + mr + 40, "Blocking body", "the Moon")
labels(f, ox - 10, y + 76, "Observer", "on the Earth")
f.text((mx + ox) / 2, y - 8, "the star is hidden in this band", anchor="middle", cls="label-dim")

f.save(__file__, "../../content/05-primer/img/case-hidden.svg")
