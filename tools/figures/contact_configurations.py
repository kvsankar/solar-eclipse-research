#!/usr/bin/env python3
"""The four contacts as tangencies of the two discs.

Each contact is the instant at which the lunar and solar discs are tangent:
externally at C1 and C4, internally at C2 and C3. The four panels are one
relative path, drawn as the dotted line through every panel, sampled at the
four instants when the separation of the centres equals the sum or the
difference of the two radii. The position angle P of the contact point is
marked on C4, measured eastward from the north point of the solar limb.

The panels are drawn as the observer sees the sky: north up, east to the left,
so an eastward angle opens counter-clockwise on the page. The discs are sized
for legibility, with the lunar disc larger than the solar one as in a total
eclipse.

    cd tools/figures && python contact_configurations.py
"""

import math

from figlib import Figure, n

W, H = 700, 322
CY = 168.0
CENTRES = [96.0, 268.0, 440.0, 612.0]
RS, RM = 22.0, 26.0                 # solar and lunar apparent radii
B = 1.5                             # least separation of the centres

DIR = (-math.cos(math.radians(6.0)), math.sin(math.radians(6.0)))
PERP = (-DIR[1], DIR[0])


def moon_offset(sep: float, before: bool) -> tuple[float, float]:
    """Offset of the lunar centre when the separation of centres is `sep`."""
    t = math.sqrt(sep * sep - B * B)
    if before:
        t = -t
    return (B * PERP[0] + t * DIR[0], B * PERP[1] + t * DIR[1])


def position_angle(off: tuple[float, float], interior: bool) -> float:
    """Position angle of the contact point, eastward from north, in degrees."""
    k = math.hypot(*off)
    ux, uy = off[0] / k, off[1] / k
    if interior:
        ux, uy = -ux, -uy
    return math.degrees(math.atan2(-ux, -uy)) % 360.0


CONTACTS = [
    ("C1", RS + RM, True, False, "exterior tangency", "the partial phase begins"),
    ("C2", RM - RS, True, True, "interior tangency", "totality begins"),
    ("C3", RM - RS, False, True, "interior tangency", "totality ends"),
    ("C4", RS + RM, False, False, "exterior tangency", "the partial phase ends"),
]

f = Figure(
    W, H,
    title="The four contacts as tangencies of the solar and lunar discs",
    desc=(
        "Four panels in a row, each showing the Sun as a light disc and the "
        "Moon as a slightly larger grey disc, with a dotted line through both "
        "marking the Moon's path relative to the Sun and an arrow showing it "
        "moving to the left, eastward. In the first panel the two discs touch "
        "from outside on the right of the Sun: first contact, the beginning of "
        "the partial phase. In the second the lunar disc has just swallowed "
        "the solar one and touches it from inside: second contact, the "
        "beginning of totality. In the third the discs touch from inside on "
        "the opposite side: third contact, the end of totality. In the fourth "
        "they touch from outside on the left: fourth contact, the end of the "
        "partial phase. On the fourth panel a line runs from the Sun's centre "
        "up to its north point and another to the point of tangency, with an "
        "arc between them labelled P, the position angle, opening "
        "counter-clockwise from north through about ninety degrees."
    ),
)

f.text(W / 2.0, 34, "the two discs as the observer sees them: north up, "
                    "east to the left", anchor="middle", cls="label-dim")

for cx, (name, sep, before, interior, what, when) in zip(CENTRES, CONTACTS):
    # the relative path of the lunar centre, arrow toward the east
    p0 = (cx + B * PERP[0] - 78 * DIR[0], CY + B * PERP[1] - 78 * DIR[1])
    p1 = (cx + B * PERP[0] + 78 * DIR[0], CY + B * PERP[1] + 78 * DIR[1])
    f.line(p0[0], p0[1], p1[0], p1[1], cls="axis dotted", marker="arrow")

    ox, oy = moon_offset(sep, before)
    f.circle(cx, CY, RS, cls="body")
    f.circle(cx + ox, CY + oy, RM, cls="cone-deep")
    f.circle(cx + ox, CY + oy, RM, cls="rule")

    # the point of tangency, on the line of centres
    k = math.hypot(ox, oy)
    sign = -1.0 if interior else 1.0
    tx, ty = cx + sign * RS * ox / k, CY + sign * RS * oy / k
    f.circle(tx, ty, 3.2, cls="accent-fill")

    f.text(cx, 238, name, anchor="middle", cls="label")
    f.text(cx, 254, what, anchor="middle", cls="label-dim")
    f.text(cx, 266, when, anchor="middle", cls="label-dim")

# --- the position angle, marked on C4 -------------------------------------
cx = CENTRES[3]
ox, oy = moon_offset(RS + RM, False)
P = position_angle((ox, oy), False)
k = math.hypot(ox, oy)
tx, ty = cx + RS * ox / k, CY + RS * oy / k

f.line(cx, CY, cx, CY - 38, cls="axis")
f.text(cx, CY - 44, "N", anchor="middle", cls="label-dim")
f.line(cx, CY, tx, ty, cls="accent")

ARC = 34.0
end = (cx - ARC * math.sin(math.radians(P)), CY - ARC * math.cos(math.radians(P)))
large = 1 if P > 180.0 else 0
f.path(f"M {n(cx)} {n(CY - ARC)} A {n(ARC)} {n(ARC)} 0 {large} 0"
       f" {n(end[0])} {n(end[1])}", cls="accent thin")
half = math.radians(P / 2.0)
f.text(cx - 45 * math.sin(half), CY - 45 * math.cos(half) + 4, "P",
       anchor="middle", cls="label-accent")

f.text(cx, 288, "P is measured eastward from the", anchor="middle",
       cls="label-dim")
f.text(cx, 300, "north point of the solar limb", anchor="middle",
       cls="label-dim")

f.text(8, 108, "the Moon's path", cls="label-dim")
f.text(8, 120, "relative to the Sun", cls="label-dim")
f.line(66, 124, 40, 171, cls="rule thin")

f.text(8, H - 8,
       "Schematic. At the interior contacts the two limbs are drawn four "
       "pixels apart.", cls="label-dim")

f.save(__file__,
       "../../content/10-raw/04-local-circumstances/img/contact-configurations.svg")
for name, sep, before, interior, _, _ in CONTACTS:
    print(f"  {name}: P = {position_angle(moon_offset(sep, before), interior):.1f} deg")
