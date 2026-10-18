#!/usr/bin/env python3
"""The fundamental plane of a lunar occultation of a star.

For a star the shadow of the Moon is a cylinder, so on the fundamental plane
it is a circle of fixed radius k = 0.2725 Earth equatorial radii. Its centre
moves along an almost straight line x = x' t, y = Y + y' t from the time of
conjunction in right ascension. The two lines parallel to that track at a
perpendicular distance k bound the band the circle sweeps on the plane; where
the rotating Earth's surface meets their edges the northern and southern
limits of the occultation lie.

The elements are those of the Explanatory Supplement (1961), Example 10.2,
for Z.C. 2833 on 1960 September 1: Y = +0.9753, x' = +0.6046 and
y' = +0.0543 Earth radii per hour. The circles are drawn at true scale. The
Earth's rotation, which moves the observer's projection during the event, is
not drawn, so the figure is a schematic computed from quoted elements.

    cd tools/figures && python occ_fundamental_plane.py
"""

import math

from figlib import Figure

# --- elements (ES 1961, Example 10.2) -------------------------------------
K = 0.2725                     # lunar radius in Earth equatorial radii
Y0 = 0.9753                    # y at conjunction
XP = 0.6046                    # x', Earth radii per hour
YP = 0.0543                    # y', Earth radii per hour

# --- layout ---------------------------------------------------------------
W, H = 760, 500
CX, CY = 360.0, 280.0          # the Earth's centre
RE = 150.0                     # one Earth equatorial radius, in pixels


def px(x: float, y: float) -> tuple[float, float]:
    """Fundamental-plane coordinates (Earth radii) to SVG pixels."""
    return CX + x * RE, CY - y * RE


f = Figure(
    W, H,
    title="The fundamental plane of a lunar occultation",
    desc=(
        "The fundamental plane seen along the line from the star. The Earth "
        "is a circle of unit radius with x running east and y running north "
        "from its centre. A straight track, rising gently from left to right, "
        "crosses near the top of the Earth's disc; it is the path of the "
        "centre of the Moon's shadow. Three circles of radius k are drawn on "
        "the track, at one hour before conjunction, at conjunction and one "
        "hour after; the middle one is solid and the other two are dashed. "
        "Two dotted lines parallel to the track, one above and one below, "
        "bound the band the circle sweeps. The lower line cuts across the "
        "Earth's disc and is labelled southern limit; the upper line lies "
        "wholly off the disc and is labelled northern limit. A vertical "
        "dimension on the left marks Y, the height of the track above the "
        "Earth's centre at conjunction, and an arrow inside the middle "
        "circle marks its radius k."
    ),
)

# --- the Earth's disc and axes -------------------------------------------
f.circle(CX, CY, RE, cls="body")
f.line(CX, CY, CX + RE + 60, CY, cls="axis", marker="arrow")
f.line(CX, CY, CX, CY - RE - 25, cls="axis thin")
f.text(CX + RE + 66, CY + 4, "x  (east)", cls="label-em")
f.circle(CX, CY, 3, cls="accent-2-fill")
f.text(CX + 8, CY + 17, "the Earth's centre", cls="label-dim")
f.text(CX, CY + RE - 30, "the Earth's disc, radius 1", anchor="middle",
       cls="label")

# --- the track and the two limit lines -----------------------------------
T0, T1 = -2.6, 2.6             # hours either side of conjunction
theta = math.atan2(YP, XP)     # direction of motion from the x axis
nx, ny = -math.sin(theta), math.cos(theta)   # unit normal, pointing north


def track(t: float, offset: float = 0.0) -> tuple[float, float]:
    return px(XP * t + offset * nx, Y0 + YP * t + offset * ny)


a, b = track(T0), track(T1)
f.line(*a, *b, cls="accent-2", marker="arrow")
f.text(b[0] + 6, b[1] + 4, "track of (x, y)", cls="label-em")

for off, name in ((K, "northern limit"), (-K, "southern limit")):
    a, b = track(T0, off), track(T1, off)
    f.line(*a, *b, cls="accent dotted")
    f.text(b[0] + 6, b[1] + 4, name, cls="label-em")

# --- the shadow circle at three instants ---------------------------------
for t, label in ((-1.0, "T₀ − 1 h"), (0.0, "T₀"), (1.0, "T₀ + 1 h")):
    cx, cy = track(t)
    if t == 0.0:
        f.circle(cx, cy, K * RE, cls="cone")
        f.circle(cx, cy, K * RE, cls="accent")
    else:
        f.circle(cx, cy, K * RE, cls="accent dashed")
    f.circle(cx, cy, 2.5, cls="accent-2-fill")
    ly = cy + K * RE + 14 if t == 0.0 else cy - K * RE - 8
    f.text(cx, ly, label, anchor="middle", cls="label")

# --- k and Y callouts ------------------------------------------------------
cx, cy = track(0.0)
ex, ey = cx + K * RE * math.cos(math.radians(-35)), cy - K * RE * math.sin(
    math.radians(-35))
f.line(cx, cy, ex, ey, cls="accent", marker="arrow")
f.text((cx + ex) / 2 + 8, (cy + ey) / 2 + 2, "k", cls="label-em")
yx = CX - 1.35 * RE
f.line(yx, CY, yx, cy, cls="rule thin", marker="arrow")
f.line(yx - 6, CY, CX - RE, CY, cls="rule thin")
f.line(yx - 6, cy, cx - K * RE, cy, cls="rule thin")
f.text(yx - 6, (CY + cy) / 2, "Y", anchor="end", cls="label-em")

f.text(8, H - 26,
       "Schematic from the elements of ES 1961 Example 10.2: Y = +0.9753, "
       "x′ = +0.6046, y′ = +0.0543, k = 0.2725.",
       cls="label-dim")
f.text(8, H - 10,
       "The Earth's rotation is not drawn, so the band shows the shadow's "
       "sweep on the plane, not the zone on the ground.",
       cls="label-dim")

f.save(__file__,
       "../../content/10-raw/40-occultations/13-lunar-occultations/img/occultation-plane.svg")
