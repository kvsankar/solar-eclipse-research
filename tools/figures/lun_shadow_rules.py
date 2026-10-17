#!/usr/bin/env python3
"""The atmospheric layer height that each umbra-enlargement rule implies.

A data figure. Every curve is computed from a formula quoted in
`content/10-raw/12-lunar-eclipses/shadow-geometry-and-enlargement.md`:

* Chauvenet: umbral radius 1.02 (0.998340 pi_M - s_S + pi_S).
* Danjon (Connaissance des Temps): 1.01 pi_M - s_S + pi_S.
* Herald and Sinnott 2014: R pi_M - s_S + pi_S with
  R = 1 + h - 0.003353 sin^2(theta) cos^2(delta_S + f sin(theta)),
  h = 0.0136 equatorial Earth radii, evaluated at theta = 45 degrees with
  the Sun on the equator.

Each rule is converted to the height, above the 45-degree Earth radius
0.998340, of the layer that would give the same umbral radius. That height is
(radius - airless radius) / pi_M in Earth radii, times 6378.137 km. The Sun is
held at 1 au (s_S = 959.63 arcsec, pi_S = 8.794 arcsec). The shaded band is
the range of single-eclipse means that Herald and Sinnott quote (82.2 km for
1989 Aug 17, 90.7 km for 1982 Jul 6). Nothing is fitted.

    python tools/figures/lun_shadow_rules.py
"""

import math

from figlib import Figure, n

# --- constants quoted in the note -----------------------------------------
A_KM = 6378.137          # equatorial radius used to express heights in km
R45 = 0.998340           # Earth radius at latitude 45 degrees, equatorial units
S_SUN = 959.63           # solar semidiameter at 1 au, arcsec
PI_SUN = 8.794           # solar horizontal parallax at 1 au, arcsec
H_HS = 0.0136            # Herald and Sinnott layer height, equatorial radii
BAND = (82.2, 90.7)      # single-eclipse means quoted by Herald and Sinnott, km

D_MIN, D_MAX = 56.0, 64.0        # lunar distance, equatorial Earth radii
Y_MIN, Y_MAX = 66.0, 100.0       # implied layer height, km


def parallax(d: float) -> float:
    return math.degrees(math.asin(1.0 / d)) * 3600.0


def chauvenet_km(d: float) -> float:
    pm = parallax(d)
    airless = R45 * pm - S_SUN + PI_SUN
    return 0.02 * airless / pm * A_KM


def danjon_km(d: float) -> float:
    return (1.01 - R45) * A_KM


def hs_km(d: float) -> float:
    # Herald and Sinnott's R at a contact angle of 45 degrees with the Sun on
    # the equator: 1 + h - 0.003353 sin^2(45) cos^2(~0), taken above R45
    return (1.0 + H_HS - 0.003353 * 0.5 - R45) * A_KM


# --- layout ---------------------------------------------------------------
W, H = 720, 400
PL, PR, PT, PB = 70.0, 520.0, 40.0, 330.0


def gx(d: float) -> float:
    return PL + (d - D_MIN) / (D_MAX - D_MIN) * (PR - PL)


def gy(km: float) -> float:
    return PB - (km - Y_MIN) / (Y_MAX - Y_MIN) * (PB - PT)


f = Figure(
    W, H,
    title="Atmospheric layer height implied by three umbra-enlargement rules",
    desc=(
        "A line chart. The horizontal axis is the Moon's distance from 56 to "
        "64 equatorial Earth radii. The vertical axis is the height in "
        "kilometres of the atmospheric layer that each rule effectively adds "
        "to the Earth. Chauvenet's 2 per cent rule is a solid line falling "
        "from about 94 km at 56 Earth radii to about 90 km at 64 Earth radii. "
        "Danjon's factor 1.01 is a dashed horizontal line near 74 km. Herald "
        "and Sinnott's 0.0136 Earth radii, evaluated at a contact angle of 45 "
        "degrees, is a dotted horizontal line near 86.6 km. A shaded band from 82.2 to 90.7 km shows the spread of "
        "single-eclipse mean heights that Herald and Sinnott report."
    ),
)

# --- band of observed single-eclipse means --------------------------------
f.rect(PL, gy(BAND[1]), PR - PL, gy(BAND[0]) - gy(BAND[1]), cls="cone")
f.text(PL + 8, gy(BAND[1]) + 14,
       "single-eclipse means, 82.2 to 90.7 km (Herald and Sinnott)",
       cls="label-dim")

# --- axes -----------------------------------------------------------------
f.line(PL, PB, PR, PB, cls="rule thin")
f.line(PL, PT, PL, PB, cls="rule thin")
for d in range(56, 65, 2):
    f.line(gx(d), PB, gx(d), PB + 5, cls="rule thin")
    f.text(gx(d), PB + 18, str(d), anchor="middle", cls="tick")
f.text((PL + PR) / 2, PB + 38, "lunar distance, equatorial Earth radii",
       anchor="middle", cls="label-dim")
for km in range(70, 101, 10):
    f.line(PL - 5, gy(km), PL, gy(km), cls="rule thin")
    f.text(PL - 9, gy(km) + 4, str(km), anchor="end", cls="tick")
f.text(16, (PT + PB) / 2, "implied layer height, km", anchor="middle",
       cls="label-dim", extra=f'transform="rotate(-90 16 {n((PT + PB) / 2)})"')

# --- curves ---------------------------------------------------------------
steps = [D_MIN + i * (D_MAX - D_MIN) / 40 for i in range(41)]
f.polyline([(gx(d), gy(chauvenet_km(d))) for d in steps], cls="accent")
f.polyline([(gx(d), gy(danjon_km(d))) for d in steps], cls="accent-2 dashed")
f.polyline([(gx(d), gy(hs_km(d))) for d in steps], cls="accent dotted")

# --- direct labels, so colour is never the only key -----------------------
LX = PR + 12
f.text(LX, gy(chauvenet_km(D_MAX)) - 2, "Chauvenet, 1.02", cls="label")
f.text(LX, gy(chauvenet_km(D_MAX)) + 12, "solid; varies with distance",
       cls="label-dim")
f.text(LX, gy(hs_km(D_MAX)) + 4, "Herald and Sinnott, h = 0.0136",
       cls="label")
f.text(LX, gy(hs_km(D_MAX)) + 18,
       f"dotted; {hs_km(D_MAX):.1f} km at θ = 45°", cls="label-dim")
f.text(LX, gy(danjon_km(D_MAX)) + 4, "Danjon, 1.01", cls="label")
f.text(LX, gy(danjon_km(D_MAX)) + 18,
       f"dashed; {danjon_km(D_MAX):.0f} km", cls="label-dim")

f.text(8, H - 8,
       "Computed from the quoted formulas with the Sun at 1 au; "
       "heights are above the 45-degree radius 0.998340.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/12-lunar-eclipses/img/shadow-rules.svg")
print(f"  chauvenet {n(chauvenet_km(D_MIN))}..{n(chauvenet_km(D_MAX))} km"
      f"  danjon {n(danjon_km(D_MIN))} km  hs {n(hs_km(D_MIN))} km")
