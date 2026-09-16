#!/usr/bin/env python3
"""The fundamental plane and the two shadow cones.

The single diagram the rest of the corpus leans on: it names the shadow axis,
the two cones, the plane through the Earth's centre, and the two radii l1 and
l2 measured on that plane.

Geometry is chosen so the umbral vertex falls just inside the Earth, which is
what makes the drawn eclipse total. The Moon is drawn far larger relative to
the Sun than it is, because at true relative size the cones would be
indistinguishable from parallel lines. The caption says so.

    python tools/figures/fundamental_plane.py
"""

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 760, 380
AXIS_Y = 190.0
RIGHT = 672.0

SUN_X, SUN_R = 10.0, 84.0          # centre off the left edge, so the disc clips
MOON_X, MOON_R = 320.0, 40.0
EARTH_X, EARTH_R = 560.0, 58.0     # the fundamental plane passes through here

# External tangents (umbra) meet at a vertex; internal tangents (penumbra)
# cross at the Moon and diverge.
VERTEX_X = MOON_X + MOON_R * (MOON_X - SUN_X) / (SUN_R - MOON_R)


def through(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    return lambda x: y1 + slope * (x - x1)


umbra_up = through(SUN_X, AXIS_Y - SUN_R, MOON_X, AXIS_Y - MOON_R)
pen_down = through(SUN_X, AXIS_Y - SUN_R, MOON_X, AXIS_Y + MOON_R)

l1 = pen_down(EARTH_X) - AXIS_Y          # penumbral radius on the plane
l2 = AXIS_Y - umbra_up(EARTH_X)          # umbral radius on the plane

f = Figure(
    W, H,
    title="The fundamental plane and the shadow cones",
    desc=(
        "A cross-section through the Sun, Moon and Earth. Tangents drawn to the "
        "outsides of the Sun and Moon form the umbral cone, which narrows to a "
        "vertex just inside the Earth. Tangents that cross between them form the "
        "penumbral cone, which widens past the Moon. A vertical line through the "
        "Earth's centre, perpendicular to the shadow axis, is the fundamental "
        "plane. The penumbral radius l1 and the much smaller umbral radius l2 "
        "are measured on that plane."
    ),
)

# --- cones ----------------------------------------------------------------
f.polygon(
    [(MOON_X, AXIS_Y - MOON_R), (RIGHT, 2 * AXIS_Y - pen_down(RIGHT)),
     (RIGHT, pen_down(RIGHT)), (MOON_X, AXIS_Y + MOON_R)],
    cls="cone",
)
f.polygon(
    [(MOON_X, AXIS_Y - MOON_R), (VERTEX_X, AXIS_Y), (MOON_X, AXIS_Y + MOON_R)],
    cls="cone-deep",
)

# --- bodies ---------------------------------------------------------------
f.circle(SUN_X, AXIS_Y, SUN_R, cls="body")
f.circle(MOON_X, AXIS_Y, MOON_R, cls="body")
f.circle(EARTH_X, AXIS_Y, EARTH_R, cls="body")

# --- axis and cone edges --------------------------------------------------
f.line(SUN_X, AXIS_Y, RIGHT, AXIS_Y, cls="axis dashed")
f.line(MOON_X, AXIS_Y - MOON_R, VERTEX_X, AXIS_Y, cls="axis thin")
f.line(MOON_X, AXIS_Y + MOON_R, VERTEX_X, AXIS_Y, cls="axis thin")
f.line(MOON_X, AXIS_Y - MOON_R, RIGHT, 2 * AXIS_Y - pen_down(RIGHT), cls="axis thin")
f.line(MOON_X, AXIS_Y + MOON_R, RIGHT, pen_down(RIGHT), cls="axis thin")

# --- the fundamental plane ------------------------------------------------
f.line(EARTH_X, 58, EARTH_X, H - 22, cls="accent")
f.text(EARTH_X, 30, "fundamental plane", anchor="middle", cls="label-accent")
f.text(EARTH_X, 45, "perpendicular to the axis, through the Earth's centre",
       anchor="middle", cls="label-dim")

# --- l1 and l2, both measured on the plane itself -------------------------
f.line(EARTH_X, AXIS_Y, EARTH_X, AXIS_Y - l1, cls="accent-2", marker="arrow")
f.text(EARTH_X - 8, AXIS_Y - l1 / 2 + 4, "l₁", anchor="end", cls="label-em")

# l2 spans only a few pixels here, so it is called out rather than bracketed.
f.line(EARTH_X + 4, AXIS_Y - 3, 646, 236, cls="rule thin")
f.text(650, 240, "l₂", cls="label-em")
f.text(650, 254, "negative: the vertex", cls="label-dim")
f.text(650, 266, "is past the plane", cls="label-dim")

# --- body and region labels ----------------------------------------------
f.text(SUN_X + 30, AXIS_Y + 4, "Sun", cls="label")
f.text(MOON_X, AXIS_Y - MOON_R - 11, "Moon", anchor="middle", cls="label")
f.text(EARTH_X, AXIS_Y + EARTH_R + 20, "Earth", anchor="middle", cls="label")
f.text(126, AXIS_Y - 7, "shadow axis", cls="label-dim")
f.text(432, 160, "umbral cone", anchor="middle", cls="label-dim")
f.text(360, AXIS_Y + 118, "penumbral cone", cls="label-dim")
f.text(VERTEX_X, AXIS_Y - 13, "vertex", anchor="middle", cls="label-dim")

f.text(8, H - 6,
       "Schematic. The Moon is drawn much larger relative to the Sun than it is.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/01-foundations/img/fundamental-plane.svg")
print(f"  vertex x={n(VERTEX_X)}  l1={n(l1)}  l2={n(l2)}")
