#!/usr/bin/env python3
"""The four satellite-Jupiter phenomena, seen from above Jupiter's north pole.

A satellite on one orbit meets four zones. Two are fixed by the Sun: the
shadow behind Jupiter (eclipse) and the line between the Sun and Jupiter
(shadow transit). Two are fixed by the Earth: the corridor behind the disc
(occultation) and the corridor in front of it (transit). The Sun zones and
the Earth zones are separated by the phase angle, Jupiter's Sun-Jupiter-Earth
angle, which is why an eclipse and the occultation of the same satellite do
not coincide.

The phase angle is drawn as 35 degrees. The real maximum is about 12 degrees,
and at that angle the zones overlap so much that the drawing loses its point.
The caption and the footnote on the figure say so.

    python tools/figures/jup_phenomena.py
"""

import math

from figlib import Figure, n

W, H = 760, 470
CX, CY = 420.0, 235.0      # Jupiter's centre
RJ = 44.0                  # Jupiter's radius on the drawing
RORB = 150.0               # satellite orbit radius on the drawing
RSAT = 7.0                 # satellite radius on the drawing
PHASE = 35.0               # drawn Sun-Jupiter-Earth angle, degrees (exaggerated)


def at(radius: float, deg: float) -> tuple[float, float]:
    """Point at an angle measured counterclockwise from +x (screen y is down)."""
    a = math.radians(deg)
    return CX + radius * math.cos(a), CY - radius * math.sin(a)


SUN_DIR = 180.0                 # direction from Jupiter towards the Sun
EARTH_DIR = 180.0 + PHASE       # direction from Jupiter towards the Earth
SHADOW_DIR = SUN_DIR - 180.0    # anti-solar direction
OCC_DIR = EARTH_DIR - 180.0     # direction behind Jupiter as seen from Earth

f = Figure(
    W, H,
    title="Eclipse, occultation, transit and shadow transit of a Galilean satellite",
    desc=(
        "A view from above Jupiter's north pole. Sunlight arrives from the left. "
        "A shaded band, Jupiter's shadow, extends to the right of the planet. "
        "A circle around Jupiter is a satellite's orbit, traversed "
        "counterclockwise. An arrow from Jupiter points down and to the left "
        "towards the Earth, at an angle to the sunlight. Two dashed lines "
        "tangent to Jupiter and parallel to the Earth direction mark the "
        "corridor that the Earth sees as Jupiter's disc. Four satellite "
        "positions are labelled: shadow transit on the Sun side, eclipse inside "
        "the shadow band, occultation inside the dashed corridor behind "
        "Jupiter, and transit inside the dashed corridor in front of Jupiter. "
        "The eclipse and occultation positions are separated by the angle "
        "between the Sun and Earth directions."
    ),
)

# --- Jupiter's shadow: umbra band with thin penumbral wedges -----------------
far = 335.0
ux, uy = math.cos(math.radians(SHADOW_DIR)), -math.sin(math.radians(SHADOW_DIR))
px, py = -uy, ux                                    # perpendicular, on screen
pen = 0.05                                          # penumbra spread per unit length
umb = 0.02                                          # umbra taper per unit length
p_top0 = (CX + px * RJ, CY + py * RJ)
p_bot0 = (CX - px * RJ, CY - py * RJ)
f.polygon(
    [p_top0,
     (CX + ux * far + px * (RJ + pen * far), CY + uy * far + py * (RJ + pen * far)),
     (CX + ux * far - px * (RJ + pen * far), CY + uy * far - py * (RJ + pen * far)),
     p_bot0],
    cls="cone",
)
f.polygon(
    [p_top0,
     (CX + ux * far + px * (RJ - umb * far), CY + uy * far + py * (RJ - umb * far)),
     (CX + ux * far - px * (RJ - umb * far), CY + uy * far - py * (RJ - umb * far)),
     p_bot0],
    cls="cone-deep",
)

# --- sunlight -------------------------------------------------------------------
for dy in (-30, 0, 30, 60, 90):
    f.line(28, CY + dy, 150, CY + dy, cls="rule thin", marker="arrow")
f.text(30, CY - 42, "sunlight", cls="label-dim")

# --- the Earth's view: corridor tangent to Jupiter along the Earth direction ----
ex, ey = math.cos(math.radians(EARTH_DIR)), -math.sin(math.radians(EARTH_DIR))
qx, qy = -ey, ex
reach = RORB + 40.0
for s in (1, -1):
    x0, y0 = CX + s * qx * RJ, CY + s * qy * RJ
    f.line(x0 - ex * reach, y0 - ey * reach, x0 + ex * reach, y0 + ey * reach,
           cls="rule dashed")

# arrow to the Earth
e1 = at(RJ + 4, EARTH_DIR)
e2 = at(RORB + 85, EARTH_DIR)
f.line(*e1, *e2, cls="accent", marker="arrow")
f.text(e2[0] + 10, e2[1] + 16, "to the Earth", cls="label-accent")

# --- the orbit and Jupiter -------------------------------------------------------
f.circle(CX, CY, RORB, cls="rule")
f.circle(CX, CY, RJ, cls="body")
f.text(CX, CY + 5, "Jupiter", anchor="middle", cls="label")

# direction of motion along the orbit
a0, a1 = at(RORB, 100.0), at(RORB, 118.0)
f.path(f"M {n(a0[0])} {n(a0[1])} A {n(RORB)} {n(RORB)} 0 0 0 {n(a1[0])} {n(a1[1])}",
       cls="accent-2", marker="arrow")
f.text(at(RORB + 14, 112.0)[0], at(RORB + 14, 112.0)[1], "orbital motion",
       anchor="end", cls="label-dim")

# --- the four positions ----------------------------------------------------------
positions = [
    (SUN_DIR, "shadow transit", "its shadow falls on the disc", (-60, -95)),
    (SHADOW_DIR, "eclipse", "satellite inside the shadow", (40, 95)),
    (OCC_DIR, "occultation", "satellite behind the disc", (85, -60)),
    (EARTH_DIR, "transit", "satellite in front of the disc", (-130, 40)),
]
for deg, name, note, (dx, dy) in positions:
    sx, sy = at(RORB, deg)
    f.circle(sx, sy, RSAT, cls="accent-2-fill")
    lx, ly = sx + dx, sy + dy
    f.line(sx, sy, lx, ly - 4, cls="rule thin")
    anchor = "start" if dx > 0 else "end"
    f.text(lx, ly, name, anchor=anchor, cls="label-em")
    f.text(lx, ly + 14, note, anchor=anchor, cls="label-dim")

# the satellite's own shadow cone in the shadow-transit case
sx, sy = at(RORB, SUN_DIR)
f.line(sx + RSAT * 0.2, sy - RSAT, CX - RJ + 2, CY - 3, cls="rule thin")
f.line(sx + RSAT * 0.2, sy + RSAT, CX - RJ + 2, CY + 3, cls="rule thin")

# --- the phase angle --------------------------------------------------------------
r_arc = 62.0
b0, b1 = at(r_arc, SHADOW_DIR), at(r_arc, OCC_DIR)
f.path(f"M {n(b0[0])} {n(b0[1])} A {n(r_arc)} {n(r_arc)} 0 0 0 {n(b1[0])} {n(b1[1])}",
       cls="accent thin")
f.text(at(r_arc + 10, (SHADOW_DIR + OCC_DIR) / 2)[0],
       at(r_arc + 10, (SHADOW_DIR + OCC_DIR) / 2)[1] - 22,
       "phase angle", cls="label-accent")

f.text(W - 6, CY - 84, "Jupiter's shadow: umbra darker,", anchor="end", cls="label-dim")
f.text(W - 6, CY - 70, "penumbra lighter", anchor="end", cls="label-dim")

f.text(8, H - 22,
       "Schematic, viewed from above Jupiter's north pole. Not to scale. The phase angle is",
       cls="label-dim")
f.text(8, H - 8,
       "drawn as 35 degrees; at Jupiter it never exceeds about 12 degrees.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/15-jupiter-satellites/img/jup-phenomena.svg")
