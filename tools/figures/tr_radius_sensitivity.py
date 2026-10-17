#!/usr/bin/env python3
"""How many seconds a contact moves per arcsecond of contact radius.

A data figure. The curve is computed from the contact solution of the 1961
Explanatory Supplement, section 9F, quoted in the note:

    t = -(u u' + v v') / n^2  +/-  L cos(psi) / n,   sin(psi) = b / L

where b is the least separation of centres and n the relative hourly motion.
Its derivative with respect to the contact radius L is

    dt/dL = L / (n sqrt(L^2 - b^2)) = (1 / n) / sqrt(1 - (b/L)^2)

in hours per arcsecond, multiplied here by 3600 for seconds. The four
points use b and n from the published 2004, 2012, 2016 and 2019 data that
the note cites (Espenak, IMCCE, and Jubier's element tables), and L for
interior contacts with s0 = 959.63 arcseconds, Venus 8.34 and Mercury 3.36
arcseconds at 1 au.

    python tools/figures/tr_radius_sensitivity.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 400
PL, PR = 76.0, 640.0
PT, PB = 50.0, 310.0

X_MIN, X_MAX = 0.0, 0.95       # b / L
Y_MIN, Y_MAX = 0.0, 40.0       # seconds of time per arcsecond

# transit, b (arcsec), n (arcsec/hour), L interior (arcsec), body
POINTS = [
    ("2004 Venus", 626.9, 240.54, 916.50, "venus"),
    ("2012 Venus", 553.0, 240.41, 916.80, "venus"),
    ("2016 Mercury", 318.5, 240.50, 944.35, "mercury"),
    ("2019 Mercury", 75.9, 354.56, 964.32, "mercury"),
]


def sens(beta: float, rate: float) -> float:
    return 3600.0 / rate / math.sqrt(1.0 - beta * beta)


def gx(beta: float) -> float:
    return PL + (beta - X_MIN) / (X_MAX - X_MIN) * (PR - PL)


def gy(sec: float) -> float:
    return PB - (sec - Y_MIN) / (Y_MAX - Y_MIN) * (PB - PT)


f = Figure(
    W, H,
    title="Contact-time shift per arcsecond of contact radius",
    desc=(
        "A chart with the ratio of least separation to contact radius, b over "
        "L, from zero to 0.95 along the horizontal axis and the shift of a "
        "contact in seconds of time per arcsecond of contact radius, from zero "
        "to forty, on the vertical axis. Two rising curves start flat and "
        "steepen towards the right. The solid curve, for a relative motion of "
        "240 arcseconds per hour, starts at 15 seconds per arcsecond. The "
        "dashed curve, for 355 arcseconds per hour, starts at about 10. Two "
        "open circles on the solid curve mark the 2012 and 2004 Venus transits "
        "near 19 and 21 seconds per arcsecond. Two squares mark the 2016 "
        "Mercury transit on the solid curve near 16 and the 2019 Mercury "
        "transit on the dashed curve near 10."
    ),
)

# --- grid and axes --------------------------------------------------------
for sec in (10.0, 20.0, 30.0, 40.0):
    f.line(PL, gy(sec), PR, gy(sec), cls="rule thin dotted")
for sec in (0.0, 10.0, 20.0, 30.0, 40.0):
    f.text(PL - 8, gy(sec) + 4, f"{int(sec)} s", anchor="end", cls="tick")
for beta in (0.0, 0.2, 0.4, 0.6, 0.8):
    f.line(gx(beta), PB, gx(beta), PB + 5, cls="rule thin")
    f.text(gx(beta), PB + 18, f"{beta:.1f}", anchor="middle", cls="tick")
f.line(PL, PT, PL, PB, cls="rule thin")
f.line(PL, PB, PR, PB, cls="rule thin")
f.text((PL + PR) / 2, PB + 38,
       "b / L: least separation over contact radius", anchor="middle",
       cls="label-dim")
f.text(PL - 50, PT - 18, "seconds of time per arcsecond of L", cls="label-dim")

# --- the two curves -------------------------------------------------------
for rate, cls in ((240.5, "accent"), (354.6, "accent-2 dashed")):
    pts = []
    steps = 120
    for i in range(steps + 1):
        beta = X_MIN + (X_MAX - X_MIN) * i / steps
        s = sens(beta, rate)
        if s > Y_MAX:
            break
        pts.append((gx(beta), gy(s)))
    f.polyline(pts, cls=cls)

f.text(gx(0.86), gy(sens(0.86, 240.5)) - 10, "n = 240″/h", anchor="end",
       cls="label-accent")
f.text(gx(0.78), gy(sens(0.78, 354.6)) + 20, "n = 355″/h", anchor="middle",
       cls="label-dim")

# --- the four transits ----------------------------------------------------
for name, b, rate, L, body in POINTS:
    beta = b / L
    s = sens(beta, rate)
    x, y = gx(beta), gy(s)
    if body == "venus":
        f.circle(x, y, 5.5, cls="rule")
    else:
        f.rect(x - 5, y - 5, 10, 10, cls="rule")
    dx, dy, anchor = {"2004 Venus": (-6, -30, "end"),
                      "2012 Venus": (-8, -12, "end"),
                      "2016 Mercury": (0, 20, "middle"),
                      "2019 Mercury": (0, -12, "middle")}[name]
    f.text(x + dx, y + dy, f"{name}: {s:.1f} s", anchor=anchor, cls="tick")
    print(f"  {name}: b/L={beta:.3f}  {s:.2f} s per arcsec")

# --- legend ---------------------------------------------------------------
LX, LY = gx(0.04), gy(37.0)
f.circle(LX, LY, 5.5, cls="rule")
f.text(LX + 12, LY + 4, "Venus, interior contacts", cls="label-dim")
f.rect(LX - 5, LY + 13, 10, 10, cls="rule")
f.text(LX + 12, LY + 22, "Mercury, interior contacts", cls="label-dim")

f.text(8, H - 8,
       "Computed from the Explanatory Supplement contact solution; geocentric, "
       "parallax not included.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/14-transits/img/tr-radius-sensitivity.svg")
