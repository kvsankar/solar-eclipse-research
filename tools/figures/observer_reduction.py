#!/usr/bin/env python3
"""Reducing one observer onto the fundamental plane.

Left: a cross-section through the Earth and the observer. The observer sits at
geodetic latitude phi, and the perpendicular dropped from the observer to the
fundamental plane is zeta. Right: the same plane seen face-on, carrying the
in-plane coordinates xi and eta of the observer, the shadow axis at (x, y),
the differences u and v, the distance m, and the two shadow radii both as
tabulated on the plane and as shrunk to the observer's own plane.

Every coordinate drawn here is a placed constant, not a computed eclipse: the
figure is a schematic of the algebra, and says so on its face.

    cd tools/figures && python observer_reduction.py
"""

import math

from figlib import Figure, n

W, H = 760, 420

# --- left panel: the cross-section ---------------------------------------
EX, EY, ER = 168.0, 214.0, 104.0        # the Earth
PHI = 30.0                              # latitude of the observer
OBS_A = 50.0                            # angle of the observer from the axis

OX = EX - ER * math.cos(math.radians(OBS_A))
OY = EY - ER * math.sin(math.radians(OBS_A))
ZETA = EX - OX                          # the perpendicular to the plane
ETA_LEN = EY - OY                       # the in-plane offset, in this section

# The equator is the radius to the observer turned by phi, screen-clockwise.
R_ANG = math.degrees(math.atan2(OY - EY, OX - EX))      # ~ -130 degrees
E_ANG = R_ANG - PHI


def at(angle_deg: float, radius: float) -> tuple[float, float]:
    a = math.radians(angle_deg)
    return EX + radius * math.cos(a), EY + radius * math.sin(a)


# --- right panel: the plane seen face-on ----------------------------------
PX, PY = 556.0, 206.0                   # the Earth's centre on the plane
OBS = (PX - 60.0, PY + 30.0)            # the observer at (xi, eta)
AXIS = (PX + 20.0, PY - 34.0)           # the shadow axis at (x, y)
L1, L1P = 128.0, 112.0                  # penumbral radius, before and after
L2, L2P = 32.0, 26.0                    # umbral radius, before and after
U = AXIS[0] - OBS[0]
V = OBS[1] - AXIS[1]
M = math.hypot(U, V)

f = Figure(
    W, H,
    title="The observer reduced to the fundamental plane",
    desc=(
        "Two panels. The left panel is a cross-section through the Earth. A "
        "vertical line through the Earth's centre is the fundamental plane, "
        "perpendicular to the shadow axis, which runs horizontally toward the "
        "Sun. An observer sits on the surface on the sunward side, at geodetic "
        "latitude phi measured from the equator, and a horizontal segment from "
        "the observer to the plane is labelled zeta, the height above the "
        "plane. The right panel shows that plane face-on, with axes xi to the "
        "east and eta to the north from the Earth's centre. The observer's "
        "projection sits below and left of the centre and the shadow axis "
        "above and right of it. A horizontal segment labelled u and a vertical "
        "segment labelled v join the two, and the straight line between them "
        "is m. Four circles are centred on the shadow axis: the penumbral and "
        "umbral radii as tabulated on the plane, dotted, and the same two "
        "radii shrunk to the observer's own plane, dashed and solid."
    ),
)

f.text(EX, 34, "a cross-section through the observer", anchor="middle",
       cls="label-dim")
f.text(PX, 34, "the plane itself, seen from the Sun", anchor="middle",
       cls="label-dim")

# ---------------------------------------------------------------- left panel
f.circle(EX, EY, ER, cls="body")

# the shadow axis and the plane perpendicular to it
f.line(EX, EY, 32, EY, cls="axis dashed", marker="arrow")
f.text(34, EY - 8, "to the Sun", cls="label-dim")
f.line(EX, 86, EX, 352, cls="accent")
f.text(EX, 76, "fundamental plane", anchor="middle", cls="label-accent")

# the equator, the radius to the observer, and the latitude between them
e1 = at(E_ANG, ER + 14)
e2 = at(E_ANG + 180.0, ER + 14)
f.line(e1[0], e1[1], e2[0], e2[1], cls="axis dotted")
f.text(e2[0] + 4, e2[1] + 12, "equator", cls="label-dim")
f.line(EX, EY, OX, OY, cls="axis thin")

a1 = at(E_ANG, 34.0)
a2 = at(R_ANG, 34.0)
f.path(f"M {n(a1[0])} {n(a1[1])} A 34 34 0 0 1 {n(a2[0])} {n(a2[1])}",
       cls="rule thin")
lab = at(E_ANG + PHI / 2.0, 50.0)
f.text(lab[0], lab[1] + 4, "φ", anchor="middle", cls="label-em")

# the observer and the perpendicular to the plane
f.circle(OX, OY, 3.4, cls="accent-2-fill")
f.text(OX - 8, OY - 6, "observer", anchor="end", cls="label")
f.line(OX, OY, EX, OY, cls="accent-2")
f.text((OX + EX) / 2.0, OY - 8, "ζ", anchor="middle", cls="label-em")
f.text(126, 100, "height above", anchor="middle", cls="label-dim")
f.text(126, 112, "the plane", anchor="middle", cls="label-dim")

# eta, measured on the plane in this section; xi points out of the page
f.line(EX, EY, EX, EY - ETA_LEN, cls="accent-2")
f.text(EX + 7, EY - ETA_LEN / 2.0 + 4, "η", cls="label-em")
f.text(EX + 7, 330, "ξ points out", cls="label-dim")
f.text(EX + 7, 342, "of the page", cls="label-dim")
f.text(84, 296, "Earth", cls="label")

# --------------------------------------------------------------- right panel
# the two pairs of shadow radii, centred on the shadow axis
f.circle(AXIS[0], AXIS[1], L1, cls="accent dotted thin")
f.circle(AXIS[0], AXIS[1], L1P, cls="accent dashed")
f.circle(AXIS[0], AXIS[1], L2P, cls="cone-deep")
f.circle(AXIS[0], AXIS[1], L2, cls="accent dotted thin")
f.circle(AXIS[0], AXIS[1], L2P, cls="accent")

# axes of the plane
f.line(PX - 108, PY, PX + 150, PY, cls="axis", marker="arrow")
f.text(PX + 156, PY + 4, "ξ", cls="label-em")
f.line(PX, PY + 40, PX, PY - 128, cls="axis", marker="arrow")
f.text(PX + 5, PY - 134, "η", cls="label-em")
f.circle(PX, PY, 2.6, cls="accent-fill")
f.text(PX - 7, PY + 15, "centre", anchor="end", cls="label-dim")

# the observer, the shadow axis and the three lengths between them
f.line(OBS[0], OBS[1], AXIS[0], OBS[1], cls="axis dashed")
f.line(AXIS[0], OBS[1], AXIS[0], AXIS[1], cls="axis dashed")
f.text((OBS[0] + AXIS[0]) / 2.0, OBS[1] + 20, "u = x − ξ", anchor="middle",
       cls="label")
f.text(AXIS[0] + 12, (OBS[1] + AXIS[1]) / 2.0 + 12, "v = y − η", cls="label")

f.line(OBS[0], OBS[1], AXIS[0], AXIS[1], cls="accent-2")
mid = ((OBS[0] + AXIS[0]) / 2.0, (OBS[1] + AXIS[1]) / 2.0)
perp = (-V / M, -U / M)
f.text(mid[0] + 13 * perp[0], mid[1] + 13 * perp[1] + 4, "m", anchor="middle",
       cls="label-em")

f.circle(OBS[0], OBS[1], 3.4, cls="accent-2-fill")
f.text(OBS[0] - 8, OBS[1] + 4, "(ξ, η)", anchor="end", cls="label-em")
f.circle(AXIS[0], AXIS[1], 3.4, cls="accent-fill")
f.text(AXIS[0] + 8, AXIS[1] - 6, "(x, y) the shadow axis", cls="label")

# the four circles, named where they cross a clear vertical
def label_circle(radius, text, dx, dy):
    px = AXIS[0] + dx
    py = AXIS[1] - math.sqrt(max(radius * radius - dx * dx, 0.0))
    f.line(px, py, px + 6, py - 6, cls="rule thin")
    f.text(px + 8, py - 6 + dy, text, cls="label-accent")


label_circle(L1, "L₁", 54.0, 0.0)
label_circle(L1P, "L₁′", 12.0, 0.0)
f.line(AXIS[0] - 18, AXIS[1] - 19, AXIS[0] - 40, AXIS[1] - 32, cls="rule thin")
f.text(AXIS[0] - 44, AXIS[1] - 29, "L₂′", anchor="end", cls="label-accent")

f.text(432, 344, "dotted: L₁ and L₂, the radii tabulated on the plane",
       cls="label-dim")
f.text(432, 360, "L₁′ = L₁ − ζ tan f₁      L₂′ = L₂ − ζ tan f₂", cls="label")
f.text(432, 376, "the same radii shrunk to the observer's own plane, ζ away",
       cls="label-dim")

f.text(8, H - 8,
       "Schematic. The coordinates drawn are chosen for legibility, not "
       "computed for any eclipse.", cls="label-dim")

f.save(__file__,
       "../../content/10-raw/04-local-circumstances/img/observer-reduction.svg")
print(f"  zeta={n(ZETA)} eta={n(ETA_LEN)} u={n(U)} v={n(V)} m={n(M)}"
      f"  L1'={n(L1P)}")
