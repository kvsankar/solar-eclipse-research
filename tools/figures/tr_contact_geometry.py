#!/usr/bin/env python3
"""The four contacts of a planetary transit, seen from the Earth's centre.

A schematic. The planet moves along a straight chord across the solar disc,
east to west. Contacts I and IV happen when the centre separation equals
the sum of the two semidiameters, contacts II and III when it equals their
difference. The least separation b is reached at greatest transit. The
planet is drawn about twenty times too large, so the four contacts separate
on the page.

    python tools/figures/tr_contact_geometry.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 760, 430
CX, CY = 270.0, 250.0          # centre of the Sun
SUN_R = 170.0                  # solar semidiameter on the page
PLANET_R = 16.0                # planet semidiameter, exaggerated
B = 92.0                       # least separation on the page
PATH_Y = CY - B                # path lies north of the centre

L_EXT = SUN_R + PLANET_R
L_INT = SUN_R - PLANET_R


def contact_x(radius: float, sign: int) -> float:
    return CX + sign * math.sqrt(radius * radius - B * B)


X1 = contact_x(L_EXT, -1)
X2 = contact_x(L_INT, -1)
X3 = contact_x(L_INT, +1)
X4 = contact_x(L_EXT, +1)

f = Figure(
    W, H,
    title="The four contacts of a planetary transit",
    desc=(
        "A large circle is the solar disc with north at the top and east on "
        "the left. A dashed horizontal line above the centre is the planet's "
        "path, crossed from left to right. Four small circles sit on the "
        "path. The two outer ones, labelled I and IV, touch the solar limb "
        "from outside. The two inner ones, labelled II and III, touch it from "
        "inside. A filled circle marks the planet at greatest transit, "
        "directly above the solar centre, and a short vertical segment labelled "
        "b joins it to the centre. A line from the centre to contact II, and "
        "an arc from the north direction to that line, show the position angle "
        "P. A panel on the right states the contact condition."
    ),
)

# --- the Sun --------------------------------------------------------------
f.circle(CX, CY, SUN_R, cls="cone")
f.circle(CX, CY, SUN_R, cls="rule")
f.circle(CX, CY, 2.5, cls="accent-2-fill")

# --- north and east -------------------------------------------------------
f.line(CX, CY, CX, CY - SUN_R - 34, cls="rule thin dashed", marker="arrow")
f.text(CX, CY - SUN_R - 40, "N", anchor="middle", cls="label")
f.line(CX - SUN_R + 10, CY + SUN_R - 40, CX - SUN_R - 26, CY + SUN_R - 40,
       cls="rule thin", marker="arrow")
f.text(CX - SUN_R - 32, CY + SUN_R - 36, "E", anchor="end", cls="label")

# --- the path -------------------------------------------------------------
f.line(X1 - 50, PATH_Y, X4 + 50, PATH_Y, cls="axis dashed", marker="arrow")
f.text(X4 + 50, PATH_Y + 18, "path", anchor="end", cls="label-dim")

# --- the planet at each contact -------------------------------------------
for x, label in ((X1, "I"), (X2, "II"), (X3, "III"), (X4, "IV")):
    f.circle(x, PATH_Y, PLANET_R, cls="body")
    f.text(x, PATH_Y - PLANET_R - 8, label, anchor="middle", cls="label-em")

# --- greatest transit and b -----------------------------------------------
f.circle(CX, PATH_Y, PLANET_R, cls="accent-fill")
f.line(CX, CY, CX, PATH_Y + PLANET_R, cls="accent")
f.text(CX + 8, (CY + PATH_Y) / 2 + 12, "b", cls="label-accent")
f.text(CX + PLANET_R + 8, PATH_Y + PLANET_R + 14, "greatest transit",
       cls="label-dim")

# --- position angle P of contact II ---------------------------------------
f.line(CX, CY, X2, PATH_Y, cls="accent-2 thin")
ang2 = math.degrees(math.atan2(-(X2 - CX), CY - PATH_Y))   # from north, east-positive
ARC_R = 44.0
pts = []
for i in range(0, 21):
    a = math.radians(ang2 * i / 20.0)
    pts.append((CX - ARC_R * math.sin(a), CY - ARC_R * math.cos(a)))
f.polyline(pts, cls="accent-2")
f.text(CX - 14, CY - 22, "P", anchor="middle", cls="label-em")

# --- ingress and egress brackets ------------------------------------------
BR_Y = PATH_Y - PLANET_R - 30
f.line(X1, BR_Y, X2, BR_Y, cls="rule thin")
f.text((X1 + X2) / 2, BR_Y - 6, "ingress", anchor="middle", cls="label-dim")
f.line(X3, BR_Y, X4, BR_Y, cls="rule thin")
f.text((X3 + X4) / 2, BR_Y - 6, "egress", anchor="middle", cls="label-dim")

# --- the condition, in a side panel ---------------------------------------
PX = 520.0
f.text(PX, 104, "Contact condition", cls="label-em")
f.text(PX, 128, "separation of centres = L", cls="label")
f.text(PX, 150, "I and IV:  L = s☉ + s_p", cls="label")
f.text(PX, 170, "II and III:  L = s☉ − s_p", cls="label")
f.text(PX, 198, "b: least separation of centres", cls="label-dim")
f.text(PX, 216, "P: position angle, north through east", cls="label-dim")
f.text(PX, 244, "A larger s☉ moves I and II earlier", cls="label-dim")
f.text(PX, 262, "and III and IV later.", cls="label-dim")

f.text(8, H - 8,
       "Schematic, geocentric. The planet is drawn about twenty times too large "
       "relative to the Sun.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/20-solar-eclipses-and-transits/14-transits/img/tr-contact-geometry.svg")
print(f"  contacts x: {n(X1)} {n(X2)} {n(X3)} {n(X4)}  P(II)={n(ang2)} deg")
