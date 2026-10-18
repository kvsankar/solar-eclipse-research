#!/usr/bin/env python3
"""Saturn's globe and ring edges as Meeus chapter 45 scales them.

The ring edges are drawn as ellipses with major axis a and minor axis
b = a sin|B|, where a for the outer edge of ring A is 375.35 arcseconds
divided by the distance in au, and the inner edges are fixed fractions of
it (0.8801, 0.8599, 0.6650, 0.5486), as transcribed in the soniakeys/meeus
saturnring package. B is set to 20 degrees for the drawing.

The globe is drawn with Saturn's equatorial radius, 60,268 km, converted to
arcseconds at 1 au, so its size relative to the rings is to scale. Its
projected polar radius uses the 54,364 km polar radius and the opening
angle B. The position angle P is set to zero, so the minor axis is vertical.

    python tools/figures/sats_ring_ellipse.py
"""

import math

from figlib import Figure, n

# --- inputs quoted in the note --------------------------------------------
AU_KM = 149597870.7
ARCSEC_KM_1AU = AU_KM * math.pi / 180.0 / 3600.0
A_OUTER = 375.35                    # arcsec at 1 au, full major axis, ring A outer edge
RINGS = [
    # label, Meeus fraction of a, angle on the ellipse for the leader (deg)
    ("1  outer edge of ring A, 1.0000 a", 1.0, 232.0),
    ("2  inner edge of ring A, 0.8801 a", 0.8801, 214.0),
    ("3  outer edge of ring B, 0.8599 a", 0.8599, 198.0),
    ("4  inner edge of ring B, 0.6650 a", 0.6650, 190.0),
    ("5  inner edge of ring C, 0.5486 a", 0.5486, 183.0),
]
R_EQ_KM, R_POL_KM = 60268.0, 54364.0
B_DEG = 20.0

# --- layout ---------------------------------------------------------------
W, H = 760, 470
CX, CY = 400.0, 190.0
SCALE = 620.0 / A_OUTER             # px per arcsec of full major axis

sinb = math.sin(math.radians(B_DEG))
cosb = math.cos(math.radians(B_DEG))


def semi(frac):
    a = 0.5 * A_OUTER * frac * SCALE
    return a, a * sinb


glob_a = R_EQ_KM / ARCSEC_KM_1AU * SCALE
glob_b = math.hypot(R_EQ_KM * sinb, R_POL_KM * cosb) / ARCSEC_KM_1AU * SCALE


def band(fo, fi, front, cls):
    ao, bo = semi(fo)
    ai, bi = semi(fi)
    so, si = (0, 1) if front else (1, 0)
    d = (f"M {n(CX - ao)} {n(CY)} A {n(ao)} {n(bo)} 0 0 {so} {n(CX + ao)} {n(CY)} "
         f"L {n(CX + ai)} {n(CY)} A {n(ai)} {n(bi)} 0 0 {si} {n(CX - ai)} {n(CY)} Z")
    f.path(d, cls=cls)


def edge(frac, front):
    a, b = semi(frac)
    s = 0 if front else 1
    f.path(f"M {n(CX - a)} {n(CY)} A {n(a)} {n(b)} 0 0 {s} {n(CX + a)} {n(CY)}",
           cls="rule thin")


f = Figure(
    W, H,
    title="Saturn's globe and ring edges at a ring opening of 20 degrees",
    desc=(
        "Five concentric ellipses centred on Saturn, numbered 1 to 5, show the "
        "outer and inner edges of ring A, the outer and inner edges of ring B "
        "and the inner edge of ring C. Rings A, B and C are shaded alike. The gap between edges 2 and 3 is the Cassini "
        "Division. The flattened globe sits in the middle and hides the middle "
        "of the back arc of each ellipse, while the front arc crosses in front of it. "
        "An arrow marks half the major axis of edge 1 and a dashed line marks "
        "half its minor axis."
    ),
)

for front in (False, True):
    if front:
        f.raw(f'<ellipse cx="{n(CX)}" cy="{n(CY)}" rx="{n(glob_a)}" '
              f'ry="{n(glob_b)}" class="body"/>')
    band(1.0, 0.8801, front, "cone")
    band(0.8599, 0.6650, front, "cone")
    band(0.6650, 0.5486, front, "cone")
    for _, frac, _ in RINGS:
        edge(frac, front)

# half axes of edge 1
a1, b1 = semi(1.0)
f.line(CX, CY, CX + a1, CY, cls="accent", marker="arrow")
f.text(CX + a1 * 0.62, CY - 7, "a/2", anchor="middle", cls="label-accent")
f.line(CX, CY, CX, CY - b1, cls="axis dashed")
f.text(CX + 8, CY - b1 + 14, "b/2 = (a/2) sin|B|", cls="label-em")

# numbered leaders from each edge to a legend at lower left
for i, (label, frac, theta) in enumerate(RINGS):
    a, b = semi(frac)
    t = math.radians(theta)
    px, py = CX + a * math.cos(t), CY - b * math.sin(t)
    ly = 330 + 20 * i
    f.circle(px, py, 2.5, cls="accent-fill")
    f.line(px, py, 30, ly - 4, cls="rule thin")
    f.text(34, ly, label, cls="label")

f.text(W - 10, 330, "globe to scale with the rings:", anchor="end", cls="label-dim")
f.text(W - 10, 346, "equatorial radius 60,268 km", anchor="end", cls="label-dim")
f.text(W - 10, 362, "polar radius 54,364 km", anchor="end", cls="label-dim")
f.text(8, H - 24, "Data figure. Edges at Meeus's fractions of a = 375.35″/Δ, with B = 20° and P = 0.",
       cls="label-dim")
f.text(8, H - 8, "Shading marks the ring bands only. It does not show optical depth.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/50-planetary-satellites/16-saturn-and-outer-satellites/img/sats-ring-ellipse.svg")
print(f"  globe a={n(glob_a)} b={n(glob_b)}  ring a={n(a1)} b={n(b1)}")
