#!/usr/bin/env python3
"""Classification regions in the plane of gamma against u.

Every boundary is one of the inequalities Meeus gives in Astronomical
Algorithms, chapter 52 of the first edition and chapter 54 of the second, as
quoted in the corpus:

    no eclipse            |gamma| > 1.5433 + u
    partial               0.9972 + |u| <= |gamma| <= 1.5433 + u
    non-central umbral    0.9972 < |gamma| < 0.9972 + |u|
    central               |gamma| < 0.9972
      total               u < 0
      annular             u > 0.0047
      hybrid              0 < u < 0.0047 and u < 0.00464 sqrt(1 - gamma^2)

Nothing is plotted that is not one of those expressions. The inset repeats
the non-central band on a stretched gamma axis, because at the scale of the
main panel it is under four pixels thick.

    cd tools/figures && python gamma_u_classification.py
"""

import math

from figlib import Figure, n

# --- constants, all quoted from the corpus --------------------------------
G_CENTRAL = 0.9972
G_NONE = 1.5433
U_ANNULAR = 0.0047
OMEGA = 0.00464

# --- main panel -----------------------------------------------------------
MX0, MX1 = 70.0, 400.0
MY0, MY1 = 50.0, 330.0             # top and bottom of the plot box
U_MIN, U_MAX = -0.020, 0.020
G_MIN, G_MAX = 0.0, 1.70

# --- inset panel ----------------------------------------------------------
IX0, IX1 = 476.0, 660.0
IY0, IY1 = 96.0, 270.0
IG_MIN, IG_MAX = 0.9900, 1.0300

W, H = 700, 400


def mx(u: float) -> float:
    return MX0 + (u - U_MIN) / (U_MAX - U_MIN) * (MX1 - MX0)


def my(g: float) -> float:
    return MY1 - (g - G_MIN) / (G_MAX - G_MIN) * (MY1 - MY0)


def ix(u: float) -> float:
    return IX0 + (u - U_MIN) / (U_MAX - U_MIN) * (IX1 - IX0)


def iy(g: float) -> float:
    return IY1 - (g - IG_MIN) / (IG_MAX - IG_MIN) * (IY1 - IY0)


f = Figure(
    W, H,
    title="Eclipse classification in the gamma-u plane",
    desc=(
        "A plot of the absolute value of gamma against the umbral radius u, "
        "both in Earth equatorial radii. A nearly horizontal line at gamma = "
        "1.5433 + u divides no eclipse above from partial below. A horizontal "
        "line at gamma = 0.9972 divides partial above from central below, "
        "with a very thin wedge between 0.9972 and 0.9972 + the absolute "
        "value of u holding the non-central umbral eclipses. The central "
        "region is cut vertically at u = 0, with total to the left and "
        "annular to the right, and a narrow wedge beside u = 0 bounded by "
        "the curve u = 0.00464 times the square root of one minus gamma "
        "squared holds the hybrid eclipses. A second, smaller panel on the "
        "right repeats the non-central wedge on a stretched gamma axis "
        "running from 0.990 to 1.030."
    ),
)

# ---------------------------------------------------------------- main plot
# partial band: between |gamma| = 0.9972 + |u| and |gamma| = 1.5433 + u
f.polygon(
    [(mx(U_MIN), my(G_CENTRAL + abs(U_MIN))), (mx(0.0), my(G_CENTRAL)),
     (mx(U_MAX), my(G_CENTRAL + abs(U_MAX))),
     (mx(U_MAX), my(G_NONE + U_MAX)), (mx(U_MIN), my(G_NONE + U_MIN))],
    cls="cone",
)

# non-central umbral wedge, at true scale
f.polygon(
    [(mx(U_MIN), my(G_CENTRAL + abs(U_MIN))), (mx(0.0), my(G_CENTRAL)),
     (mx(U_MAX), my(G_CENTRAL + abs(U_MAX))), (mx(U_MAX), my(G_CENTRAL)),
     (mx(U_MIN), my(G_CENTRAL))],
    cls="cone-deep",
)
f.line(mx(U_MIN), my(G_CENTRAL + abs(U_MIN)), mx(0.0), my(G_CENTRAL),
       cls="accent-2 dashed")
f.line(mx(0.0), my(G_CENTRAL), mx(U_MAX), my(G_CENTRAL + abs(U_MAX)),
       cls="accent-2 dashed")

# hybrid wedge: 0 < u < 0.00464 sqrt(1 - gamma^2), below |gamma| = 0.9972
STEPS = 48
curve = [(mx(OMEGA * math.sqrt(max(1.0 - g * g, 0.0))), my(g))
         for g in (G_CENTRAL * i / STEPS for i in range(STEPS + 1))]
f.polygon([(mx(0.0), my(0.0))] + curve + [(mx(0.0), my(G_CENTRAL))],
          cls="cone-deep")

# boundaries
f.line(mx(U_MIN), my(G_NONE + U_MIN), mx(U_MAX), my(G_NONE + U_MAX),
       cls="accent dashed")
f.line(mx(U_MIN), my(G_CENTRAL), mx(U_MAX), my(G_CENTRAL), cls="accent")
f.line(mx(0.0), my(G_CENTRAL), mx(0.0), my(G_MIN), cls="accent-2")
f.line(mx(U_ANNULAR), my(G_CENTRAL), mx(U_ANNULAR), my(G_MIN),
       cls="rule dotted")
f.polyline(curve, cls="accent-2 dashed")

# plot frame and ticks
f.line(MX0, MY0, MX0, MY1, cls="rule")
f.line(MX0, MY1, MX1, MY1, cls="rule")
for g in (0.0, 0.5, 1.0, 1.5):
    f.line(MX0 - 4, my(g), MX0, my(g), cls="rule")
    f.text(MX0 - 8, my(g) + 3.5, f"{g:.1f}", anchor="end", cls="tick")
for u in (-0.02, -0.01, 0.0, 0.01, 0.02):
    f.line(mx(u), MY1, mx(u), MY1 + 4, cls="rule")
    f.text(mx(u), MY1 + 16, f"{u:+.2f}".replace("+0.00", "0"), anchor="middle",
           cls="tick")

# region labels
MID = (MX0 + MX1) / 2.0
f.text(MID, my(G_NONE) - 12, "no eclipse", anchor="middle", cls="label")
f.text(MID, my(G_NONE) + 14, "|γ| = 1.5433 + u", anchor="middle",
       cls="label-dim")
f.text(MID, my(1.28), "partial", anchor="middle", cls="label")
f.text(MID, my(G_CENTRAL) - 8, "|γ| = 0.9972", anchor="middle",
       cls="label-dim")
f.text(mx(-0.0125), my(0.72), "total", anchor="middle", cls="label")
f.text(mx(-0.0125), my(0.60), "u < 0", anchor="middle", cls="label-dim")
f.text(mx(0.0125), my(0.72), "annular", anchor="middle", cls="label")
f.text(mx(U_ANNULAR) + 5, my(0.94), "u = 0.0047", cls="label-dim")

# the hybrid wedge is a few pixels wide, so it is called out
f.line(mx(0.0022), my(0.42), mx(-0.0055), my(0.32), cls="rule thin")
f.text(mx(-0.0058), my(0.30), "hybrid", anchor="end", cls="label")
f.text(mx(-0.0058), my(0.22), "u < 0.00464√(1 − γ²)",
       anchor="end", cls="label-dim")

# axis titles
f.text(MX0, MY0 - 14, "|γ|", anchor="middle", cls="label-em")
f.text(MID, MY1 + 38,
       "u, the umbral radius on the fundamental plane (Earth equatorial radii)",
       anchor="middle", cls="label")

# --------------------------------------------------------------- inset plot
f.text((IX0 + IX1) / 2.0, IY0 - 30, "Detail: the non-central band",
       anchor="middle", cls="label")
f.text((IX0 + IX1) / 2.0, IY0 - 16, "0.9972 < |γ| < 0.9972 + |u|",
       anchor="middle", cls="label-dim")

f.polygon(
    [(ix(U_MIN), iy(G_CENTRAL + abs(U_MIN))), (ix(0.0), iy(G_CENTRAL)),
     (ix(U_MAX), iy(G_CENTRAL + abs(U_MAX))), (ix(U_MAX), iy(IG_MAX)),
     (ix(U_MIN), iy(IG_MAX))],
    cls="cone",
)
f.polygon(
    [(ix(U_MIN), iy(G_CENTRAL + abs(U_MIN))), (ix(0.0), iy(G_CENTRAL)),
     (ix(U_MAX), iy(G_CENTRAL + abs(U_MAX))), (ix(U_MAX), iy(G_CENTRAL)),
     (ix(U_MIN), iy(G_CENTRAL))],
    cls="cone-deep",
)
f.line(ix(U_MIN), iy(G_CENTRAL), ix(U_MAX), iy(G_CENTRAL), cls="accent")
f.line(ix(U_MIN), iy(G_CENTRAL + abs(U_MIN)), ix(0.0), iy(G_CENTRAL),
       cls="accent-2 dashed")
f.line(ix(0.0), iy(G_CENTRAL), ix(U_MAX), iy(G_CENTRAL + abs(U_MAX)),
       cls="accent-2 dashed")

f.line(IX0, IY0, IX0, IY1, cls="rule")
f.line(IX0, IY1, IX1, IY1, cls="rule")
for g in (0.9972, 1.0172):
    f.line(IX0 - 4, iy(g), IX0, iy(g), cls="rule")
    f.text(IX0 - 8, iy(g) + 3.5, f"{g:.4f}", anchor="end", cls="tick")
for u in (-0.02, 0.0, 0.02):
    f.line(ix(u), IY1, ix(u), IY1 + 4, cls="rule")
    f.text(ix(u), IY1 + 16, f"{u:+.2f}".replace("+0.00", "0"), anchor="middle",
           cls="tick")
f.text((IX0 + IX1) / 2.0, IY1 + 34, "u", anchor="middle", cls="label-em")

f.text((IX0 + IX1) / 2.0, iy(1.0230), "partial", anchor="middle", cls="label")
f.text(ix(-0.0115), iy(1.0045), "non-central", anchor="middle", cls="label")
f.text(ix(-0.0115), iy(1.0000), "umbral", anchor="middle", cls="label")
f.text((IX0 + IX1) / 2.0, iy(0.9930), "central", anchor="middle", cls="label")

f.text(8, H - 8,
       "Every boundary is one of Meeus's inequalities; nothing else is "
       "plotted. u is the umbral radius on the fundamental plane, the same "
       "quantity as l₂.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/02-catalogs/img/gamma-u-classification.svg")
print(f"  0.9972 at y={n(my(G_CENTRAL))}   1.5433 at y={n(my(G_NONE))}"
      f"   band thickness={n(my(G_CENTRAL) - my(G_CENTRAL + 0.02))} px")
