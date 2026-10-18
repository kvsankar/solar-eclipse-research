#!/usr/bin/env python3
"""Gallery of the both case: the observer stands in a body's shadow and sees
the Sun hidden. Schematic only."""

from prim_gallery import PANEL, caption, new, sun

f = new(
    "Both: the observer stands in a shadow and sees the Sun hidden",
    ("Three panels. Left, solar eclipse: the Sun, the Moon and its shadow "
     "cone touching the Earth, with an observer inside it; an inset shows "
     "the Sun covered. Middle, transit of Venus: the Sun, Venus and its "
     "long narrow shadow, which ends far short of the Earth, so the "
     "observer is in the antumbra; an inset shows a small dark dot on the "
     "Sun. Right, the general rule: being inside a body's shadow and "
     "seeing the source hidden by that body are the same thing."),
)
y = 110


def inset(x, y, kind):
    f.circle(x, y, 13, cls="accent-fill")
    if kind == "total":
        f.circle(x, y, 17, cls="accent thin dotted")
        f.circle(x, y, 13.5, cls="sky-fill")
    else:
        f.circle(x + 4, y - 3, 2.5, cls="sky-fill")


# Solar eclipse.
x0 = 0
sun(f, x0 + 28, y, 18)
f.circle(x0 + 110, y, 8, cls="body")
f.polygon([(x0 + 110, y - 8), (x0 + 170, y - 2), (x0 + 170, y + 2), (x0 + 110, y + 8)],
          cls="cone-deep")
f.path(f"M {x0 + 186} {y - 46} A 56 56 0 0 0 {x0 + 186} {y + 46}", cls="body")
f.circle(x0 + 172, y, 3, cls="accent-2-fill")
f.text(x0 + 110, y - 14, "Moon", anchor="middle", cls="label-dim")
f.text(x0 + 200, y - 50, "Earth", anchor="end", cls="label-dim")
inset(x0 + 160, y + 56, "total")
caption(f, 0, "Solar eclipse", ["the observer in the Moon's", "umbra sees the Sun covered"])

# Transit of Venus.
x0 = PANEL
sun(f, x0 + 28, y, 18)
f.circle(x0 + 80, y, 4, cls="body")
f.polygon([(x0 + 80, y - 4), (x0 + 130, y), (x0 + 80, y + 4)], cls="cone-deep")
f.polygon([(x0 + 130, y), (x0 + 190, y - 5), (x0 + 190, y + 5)], cls="cone")
f.path(f"M {x0 + 202} {y - 46} A 56 56 0 0 0 {x0 + 202} {y + 46}", cls="body")
f.circle(x0 + 188, y, 3, cls="accent-2-fill")
f.text(x0 + 80, y - 10, "Venus", anchor="middle", cls="label-dim")
f.text(x0 + 150, y - 14, "antumbra", anchor="middle", cls="label-dim")
inset(x0 + 160, y + 56, "transit")
caption(f, 1, "Transit of Venus", ["the observer in the antumbra", "sees a dot on the Sun"])

# The rule.
x0 = 2 * PANEL
lines = ["Inside a body's shadow,", "the source is hidden", "behind that body.",
         "", "A total eclipse is the umbra,", "an annular eclipse or a", "transit the antumbra,",
         "a partial eclipse the penumbra."]
for k, line in enumerate(lines):
    f.text(x0 + PANEL / 2, 52 + 16 * k, line, anchor="middle", cls="label")
caption(f, 2, "The same event, two ways", ["", ""])

f.save(__file__, "../../content/05-primer/img/gallery-both.svg")
