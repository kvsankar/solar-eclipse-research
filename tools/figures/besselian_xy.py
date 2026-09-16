#!/usr/bin/env python3
"""The fundamental plane seen down the shadow axis.

The companion to `fundamental_plane.py`. That figure is a cross-section; this
one is the view along the axis, where the shadow is two concentric circles on
a disc of unit radius. It makes x, y, l1, l2 and gamma concrete.

The umbral circle is drawn far larger than it is. For 2024 April 8 the
published elements give l1 = 0.5358 and l2 = -0.0103 Earth radii, so at true
scale the umbra would be about one pixel across. The figure says so on its
face.

    cd tools/figures && python besselian_xy.py
"""

import math

from figlib import Figure

# --- layout ---------------------------------------------------------------
W, H = 700, 420

CX, CY = 300.0, 215.0          # the Earth's centre
RE = 130.0                     # one Earth equatorial radius, in pixels

XE, YE = -0.45, 0.28           # the shadow axis on the plane, in Earth radii
L1 = 0.54                      # penumbral radius, near the published value
L2_DRAWN = 0.10                # umbral radius, deliberately enlarged

PX = CX + XE * RE
PY = CY - YE * RE
R1 = L1 * RE
R2 = L2_DRAWN * RE

GAMMA = math.hypot(XE, YE)

f = Figure(
    W, H,
    title="The shadow on the fundamental plane",
    desc=(
        "The fundamental plane viewed along the shadow axis. The Earth is a "
        "circle of unit radius with its centre marked. An x axis runs east "
        "from that centre and a y axis runs north. Two concentric circles, "
        "the large penumbra of radius l1 and the small umbra of radius l2, "
        "are centred on the point (x, y) up and to the left of the Earth's "
        "centre. A line from the Earth's centre to that point is labelled "
        "gamma."
    ),
)

# --- the Earth's disc -----------------------------------------------------
f.circle(CX, CY, RE, cls="body")

# --- the two shadow circles ----------------------------------------------
f.circle(PX, PY, R1, cls="cone")
f.circle(PX, PY, R1, cls="accent dashed")
f.circle(PX, PY, R2, cls="cone-deep")
f.circle(PX, PY, R2, cls="accent-2")

# --- the axes -------------------------------------------------------------
f.line(CX, CY, 470, CY, cls="axis", marker="arrow")
f.line(CX, CY, CX, 55, cls="axis", marker="arrow")
f.text(476, CY + 4, "x  (east)", cls="label-em")
f.text(CX, 44, "y  (north)", anchor="middle", cls="label-em")

# --- gamma ----------------------------------------------------------------
dx, dy = PX - CX, PY - CY
glen = math.hypot(dx, dy)
ux, uy = dx / glen, dy / glen
mx, my = CX + dx / 2, CY + dy / 2
# offset the label along the normal, away from the umbral circle
gx, gy = mx + 13.0 * (-uy), my + 13.0 * ux
f.line(CX, CY, PX, PY, cls="accent-2")
f.circle(CX, CY, 3, cls="accent-2-fill")
f.circle(PX, PY, 2.5, cls="accent-2-fill")
f.text(gx, gy + 4, "γ", anchor="middle", cls="label-em")

# --- l1, measured from the shadow centre to the penumbral edge ------------
a1 = math.radians(200.0)
e1x, e1y = PX + R1 * math.cos(a1), PY - R1 * math.sin(a1)
f.line(PX, PY, e1x, e1y, cls="accent", marker="arrow")
f.text((PX + e1x) / 2 + 4, (PY + e1y) / 2 - 8, "l₁", anchor="middle",
       cls="label-em")
f.text(e1x - 6, e1y + 14, "penumbra", anchor="end", cls="label-dim")

# --- l2, called out with a leader because the circle is small -------------
a2 = math.radians(135.0)
e2x, e2y = PX + R2 * math.cos(a2), PY - R2 * math.sin(a2)
f.line(e2x, e2y, 150, 110, cls="rule thin")
f.text(146, 110, "l₂  (umbra)", anchor="end", cls="label-em")
f.text(146, 124, "drawn much enlarged", anchor="end", cls="label-dim")

# --- the remaining labels -------------------------------------------------
f.text(PX, PY - R2 - 10, "(x, y)", anchor="middle", cls="label-em")
f.text(CX + 8, CY + 17, "the Earth's centre", cls="label-dim")
f.text(CX, CY + RE + 23, "the Earth's disc, radius 1", anchor="middle",
       cls="label")

f.text(8, H - 8,
       "Schematic. The umbral circle is drawn about ten times its true size; "
       "published elements give l₂ near 0.01 Earth radii against "
       "l₁ near 0.54.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/01-foundations/img/besselian-xy.svg")
print(f"  shadow centre px=({PX:.1f}, {PY:.1f})  r1={R1:.1f}  r2={R2:.1f}"
      f"  gamma={GAMMA:.3f}")
