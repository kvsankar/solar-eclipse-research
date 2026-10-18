#!/usr/bin/env python3
"""Gallery of the hidden case: a body cuts the light reaching the observer,
and something disappears for that observer only. Schematic only."""

from prim_gallery import PANEL, caption, eye, new

f = new(
    "Hidden: a body cuts the light reaching the observer",
    ("Three panels. Left, lunar occultation of a star: parallel lines of "
     "starlight reach the Moon, and the observer behind the Moon cannot "
     "see the star. Middle, occultation of a satellite: Io half hidden "
     "behind Jupiter's limb as the observer sees it. Right, occultation "
     "by an asteroid: the asteroid's shadow in starlight crosses the "
     "Earth as a straight band, and observers inside the band see the "
     "star vanish."),
)
y = 110

# Lunar occultation of a star.
x0 = 0
for dy in (-14, 0, 14):
    f.line(x0 + 12, y + dy, x0 + 104, y + dy, cls="accent thin", marker="arrow")
f.circle(x0 + 8, y, 3, cls="accent-fill")
f.rect(x0 + 130, y - 18, 70, 36, cls="cone")
f.circle(x0 + 130, y, 18, cls="body")
eye(f, x0 + 185, y + 4, x0 + 112, y + 4)
f.text(x0 + 130, y - 24, "Moon", anchor="middle", cls="label-dim")
caption(f, 0, "Lunar occultation of a star", ["the star vanishes at once:", "a point has no penumbra"])

# Occultation of a satellite by its planet, as the observer sees it.
x0 = PANEL
f.circle(x0 + 156, y - 8, 7, cls="body")
f.circle(x0 + 110, y, 44, cls="body")
f.text(x0 + 110, y + 4, "Jupiter", anchor="middle", cls="label-dim")
f.text(x0 + 168, y - 14, "Io", cls="label-dim")
caption(f, 1, "Occultation of a satellite", ["Io passing behind Jupiter,", "as the observer sees it"])

# Occultation by an asteroid: a shadow path across the Earth.
x0 = 2 * PANEL
f.circle(x0 + 110, y, 48, cls="body")
f.polygon([(x0 + 40, y - 34), (x0 + 180, y - 4), (x0 + 180, y + 10), (x0 + 40, y - 20)],
          cls="cone-deep")
f.line(x0 + 40, y - 34, x0 + 180, y - 4, cls="rule thin")
f.line(x0 + 40, y - 20, x0 + 180, y + 10, cls="rule thin")
f.circle(x0 + 110, y - 12, 3, cls="accent-2-fill")
f.text(x0 + 176, y - 18, "shadow path", anchor="end", cls="label-dim")
f.text(x0 + 110, y + 34, "Earth", anchor="middle", cls="label-dim")
caption(f, 2, "Occultation by an asteroid", ["its shadow path is as wide", "as the asteroid"])

f.save(__file__, "../../content/05-primer/img/gallery-hidden.svg")
