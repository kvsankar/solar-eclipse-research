#!/usr/bin/env python3
"""The umbral path and its limits, drawn as the envelope of the moving shadow.

The Earth is a disc seen from the Sun. The umbra is a small ellipse that walks
along the central line. The northern and southern limits are drawn here as the
locus of that ellipse's own cross-track extreme, so each limit is tangent to
every drawn ellipse. That is the whole point: a limit is where the eclipse
begins and ends at the same instant, which is the envelope of the moving
shadow, not a curve solved independently of the central line.

The ellipse grows toward the ends of the path because the surface tilts away
there, and the limits therefore spread apart at the ends. The along-track
extent of the path is solved by bisection so that the widest limit point lands
exactly on the limb.

    cd tools/figures && python path_and_limits.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 462
CX, CY, R = 350.0, 240.0, 170.0        # the Earth's disc

RISE = 58.0                            # curvature of the central line
TOP = 72.0                             # height of the path above the centre
PEN_R = 232.0                          # penumbral radius
PEN_CY = CY - 68.0

SAMPLES = [i / 80.0 for i in range(-80, 81)]
ELLIPSES = [-0.84, -0.44, 0.0, 0.44, 0.84]


def semi_along(s: float) -> float:
    return 9.0 * (1.0 + 1.6 * s * s)


def semi_across(s: float) -> float:
    return 11.0 * (1.0 + 0.8 * s * s)


def build(a: float):
    """Central line, tangent-normal frame and the two limits, for span `a`."""

    def centre(s):
        return CX + a * s, CY - TOP + RISE * s * s

    def nvec(s):
        tx, ty = a, 2.0 * RISE * s
        k = math.hypot(tx, ty)
        return ty / k, -tx / k          # unit normal, pointing "north" (up)

    north, south = [], []
    for s in SAMPLES:
        cx, cy = centre(s)
        nx, ny = nvec(s)
        b = semi_across(s)
        north.append((cx + b * nx, cy + b * ny))
        south.append((cx - b * nx, cy - b * ny))
    return centre, nvec, north, south


def widest(a: float) -> float:
    _, _, north, south = build(a)
    return max(math.hypot(px - CX, py - CY) for px, py in north + south)


# Bisect the span so the outermost limit point sits on the limb.
lo, hi = 60.0, 200.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if widest(mid) < R:
        lo = mid
    else:
        hi = mid
SPAN = 0.5 * (lo + hi)
centre, nvec, NORTH, SOUTH = build(SPAN)

f = Figure(
    W, H,
    title="The umbral path and its limits on the Earth's disc",
    desc=(
        "The Earth is drawn as a disc seen from the Sun. A pale region covers "
        "most of the disc and is labelled the penumbral outline, its edge a "
        "dashed arc low on the disc. A curve runs from limb to limb across the "
        "upper half of the disc: the central line, the track of the shadow "
        "axis. Five small dark ellipses sit on that curve at successive "
        "instants, each the umbra on the ground, smallest near the middle of "
        "the path and larger toward its ends where the surface tilts away. "
        "Two further curves, one dashed and one dotted, run either side of the "
        "central line and touch every one of the five ellipses. They are the "
        "northern and southern limits, drawn as the envelope of the moving "
        "ellipse, and they spread apart toward the ends of the path as the "
        "ellipses grow."
    ),
)

# --- penumbral outline, clipped to the disc -------------------------------
f.raw(
    '<defs><clipPath id="earthdisc">'
    f'<circle cx="{n(CX)}" cy="{n(CY)}" r="{n(R)}"/>'
    "</clipPath></defs>"
)
f.raw(
    '<g clip-path="url(#earthdisc)">'
    f'<circle cx="{n(CX)}" cy="{n(PEN_CY)}" r="{n(PEN_R)}" class="cone"/>'
    f'<circle cx="{n(CX)}" cy="{n(PEN_CY)}" r="{n(PEN_R)}"'
    ' class="accent-2 dashed"/>'
    "</g>"
)

# --- the Earth ------------------------------------------------------------
f.circle(CX, CY, R, cls="rule")

# --- limits ---------------------------------------------------------------
f.polyline(NORTH, cls="accent dashed")
f.polyline(SOUTH, cls="accent dotted")

# --- the umbra at five instants -------------------------------------------
for s in ELLIPSES:
    cx, cy = centre(s)
    nx, ny = nvec(s)
    ang = math.degrees(math.atan2(-nx, ny))    # tangent direction
    rx, ry = semi_along(s), semi_across(s)
    for cls in ("cone-deep", "rule thin"):
        f.raw(
            f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}"'
            f' class="{cls}" transform="rotate({n(ang)} {n(cx)} {n(cy)})"/>'
        )

# --- the central line -----------------------------------------------------
f.polyline([centre(s) for s in SAMPLES], cls="accent-2")


# --- labels, positioned from the geometry ---------------------------------
def leader(x1, y1, x2, y2):
    f.line(x1, y1, x2, y2, cls="rule thin")


# northern limit: above the curve, in the clear band below the limb
sn = 0.34
pnx, pny = centre(sn)
nx, ny = nvec(sn)
pnx += semi_across(sn) * nx
pny += semi_across(sn) * ny
f.text(pnx, pny - 36, "northern limit", anchor="middle", cls="label")
leader(pnx, pny - 30, pnx, pny - 6)

# southern limit: below the curve
ss = -0.34
psx, psy = centre(ss)
nx, ny = nvec(ss)
psx -= semi_across(ss) * nx
psy -= semi_across(ss) * ny
f.text(psx, psy + 46, "southern limit", anchor="middle", cls="label")
leader(psx, psy + 34, psx, psy + 6)

# central line: called out from the right-hand end, outside the disc
ccx, ccy = centre(0.86)
f.text(CX + R + 6, CY - 4, "central line", cls="label")
f.text(CX + R + 6, CY + 11, "the shadow axis", cls="label-dim")
f.text(CX + R + 6, CY + 23, "on the ground", cls="label-dim")
leader(CX + R + 2, CY - 8, ccx + 6, ccy + 4)

# the umbra series: called out low and left, inside the disc
eux, euy = centre(-0.64)
f.text(224, 318, "the umbra at five instants", cls="label")
f.text(224, 334, "each ellipse touches both limits,", cls="label-dim")
f.text(224, 346, "which is what makes them limits", cls="label-dim")
leader(250, 310, eux - 2, euy + semi_across(-0.64) + 4)

# penumbral outline: called out from its own arc, low on the disc
arc_x = CX - 50.0
arc_y = PEN_CY + math.sqrt(PEN_R * PEN_R - 50.0 * 50.0)
f.text(12, 352, "penumbral outline", cls="label")
f.text(12, 367, "the partial phase", cls="label-dim")
f.text(12, 379, "is under way inside it", cls="label-dim")
leader(128, 368, arc_x, arc_y)

f.text(CX, CY + R + 26, "the Earth as seen from the Sun", anchor="middle",
       cls="label-dim")
f.text(8, H - 8,
       "Schematic. The umbra is drawn far larger, relative to the Earth, than "
       "it ever is.", cls="label-dim")

f.save(__file__,
       "../../content/10-raw/03-global-circumstances/img/path-and-limits.svg")
print(f"  span={n(SPAN)}  widest={n(widest(SPAN))}  arc=({n(arc_x)},{n(arc_y)})")
