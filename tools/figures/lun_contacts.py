#!/usr/bin/env python3
"""The Moon's track through the Earth's shadows and the six contacts.

A schematic drawn to scale in the plane through the Moon perpendicular to the
shadow axis, in equatorial Earth radii. Radii are Meeus's Danjon-rule values
for u = 0 (penumbra 1.2848, umbra 0.7403) and the Moon's radius is
k = 0.2725. The track is a straight line at gamma = 0.35, drawn with celestial
north up and east to the left, so the Moon moves from right to left as in the
NASA canon figures. The track's tilt is chosen for legibility.

Contact positions solve |m| = L for L1 = rho + k, L2 = sigma + k and
L3 = sigma - k on that straight track, the same condition the Explanatory
Supplement writes for x and y.

    python tools/figures/lun_contacts.py
"""

import math

from figlib import Figure, n

RHO, SIGMA, K = 1.2848, 0.7403, 0.2725
GAMMA = 0.35
TILT = math.radians(-8.0)       # track inclination on the figure

W, H = 760, 440
CX, CY = 380.0, 222.0           # shadow axis on the figure
S = 128.0                       # pixels per Earth radius

# Unit vector along the track (moving leftwards) and its normal.
ux, uy = -math.cos(TILT), -math.sin(TILT)
nx, ny = -uy, ux
# Closest point of the track to the axis, at distance gamma, north (up).
if ny > 0:
    nx, ny = -nx, -ny
FX, FY = GAMMA * nx, GAMMA * ny   # in Earth radii, y down on screen


def at(s: float) -> tuple[float, float]:
    return FX + s * ux, FY + s * uy


def contact(L: float) -> tuple[float, float]:
    half = math.sqrt(L * L - GAMMA * GAMMA)
    return -half, half


def px(p: tuple[float, float]) -> tuple[float, float]:
    return CX + S * p[0], CY + S * p[1]


f = Figure(
    W, H,
    title="The six contacts of a total lunar eclipse",
    desc=(
        "Two concentric circles centred on the shadow axis: the larger is the "
        "penumbra and the smaller the umbra. A straight line, the Moon's "
        "track, crosses them above the centre, with a short perpendicular "
        "marked gamma from the centre to the track. Seven outlined Moon "
        "disks sit on the track from right to left: P1 touching the outside "
        "of the penumbra, U1 touching the outside of the umbra, U2 just "
        "inside the umbra, G at the point nearest the centre, U3 just inside "
        "the umbra on the other side, U4 touching its outside, and P4 "
        "touching the outside of the penumbra. Penumbral contacts are drawn "
        "dashed and umbral contacts solid."
    ),
)

# --- shadows --------------------------------------------------------------
f.circle(CX, CY, S * RHO, cls="cone")
f.circle(CX, CY, S * SIGMA, cls="cone-deep")
f.circle(CX, CY, S * RHO, cls="rule thin dashed")
f.circle(CX, CY, S * SIGMA, cls="rule")

# --- track ----------------------------------------------------------------
a = px(at(-2.05))
b = px(at(2.05))
f.line(a[0], a[1], b[0], b[1], cls="axis", marker="arrow")
f.line(CX, CY, *px((FX, FY)), cls="accent-2")
f.text(CX + 6, CY - S * GAMMA / 2 + 4, "γ", cls="label-em")
f.circle(CX, CY, 2.2, cls="accent-2-fill")

# --- contacts -------------------------------------------------------------
p1, p4 = contact(RHO + K)
u1, u4 = contact(SIGMA + K)
u2, u3 = contact(SIGMA - K)
moons = [
    ("P1", p1, "rule dashed"), ("U1", u1, "body"), ("U2", u2, "body"),
    ("G", 0.0, "accent"), ("U3", u3, "body"), ("U4", u4, "body"),
    ("P4", p4, "rule dashed"),
]
# Positions along the track are measured in the direction of motion, which is
# leftward, so the first contact has the most negative s and sits on the right.
for i, (name, s, cls) in enumerate(moons):
    x, y = px(at(s))
    f.circle(x, y, S * K, cls=cls if cls != "body" else "rule")
    f.circle(x, y, 1.8, cls="accent-fill")
    dy = S * K + 16 if name in ("U1", "U4") else -S * K - 8
    f.text(x, y + dy, name, anchor="middle", cls="label")

# --- labels ---------------------------------------------------------------
f.text(CX + S * RHO * 0.72, CY + S * RHO * 0.86, "penumbra",
       cls="label-dim")
f.text(CX + 12, CY + S * SIGMA * 0.62, "umbra", cls="label-dim")
f.text(b[0] - 6, b[1] + 4, "Moon's motion", anchor="end", cls="label-dim")
f.text(W - 12, 22, "north up, east left", anchor="end", cls="label-dim")
f.text(8, H - 8,
       "Schematic to scale in Earth radii (ρ = 1.2848, σ = 0.7403, k = 0.2725, "
       "γ = 0.35); the straight track and its tilt are idealised.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/30-lunar-eclipses/img/lunar-contacts.svg")
print(f"  P1 s={n(p1)}  U1 s={n(u1)}  U2 s={n(u2)}")
