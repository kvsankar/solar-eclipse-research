#!/usr/bin/env python3
"""The standard error of ΔT against year, on a logarithmic scale.

A data figure. Every point is a row of the table Espenak's uncertainty page
gives and the corpus quotes. No curve is drawn through them, because two
different models produce them: Morrison and Stephenson's sigma = 0.8 t^2 with
the telescopic-era values, and Huber's Brownian-motion model outside the
observed record.

    python tools/figures/delta_t_uncertainty.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 400
PL, PR = 76.0, 648.0
PT, PB = 62.0, 300.0

Y_MIN, Y_MAX = -1000.0, 3000.0
S_MIN, S_MAX = 0.06, 3000.0

# year, sigma in seconds, from the record (True) or from Huber's model (False)
POINTS = [
    (-1000.0, 636.0, True),
    (0.0, 265.0, True),
    (500.0, 139.0, True),
    (1000.0, 54.0, True),
    (1200.0, 31.0, True),
    (1700.0, 5.0, True),
    (1800.0, 1.0, True),
    (1900.0, 0.1, True),
    (2500.0, 612.0, False),
    (3000.0, 1885.0, False),
]

GORE = 265.0                   # the Five Millennium Canon's gore threshold


def gx(year: float) -> float:
    return PL + (year - Y_MIN) / (Y_MAX - Y_MIN) * (PR - PL)


def gy(sigma: float) -> float:
    lo, hi = math.log10(S_MIN), math.log10(S_MAX)
    return PB - (math.log10(sigma) - lo) / (hi - lo) * (PB - PT)


f = Figure(
    W, H,
    title="The standard error of ΔT against year",
    desc=(
        "A chart with the year from minus one thousand to plus three thousand "
        "along the horizontal axis and the standard error of delta T, in "
        "seconds, on a logarithmic vertical axis running from a tenth of a "
        "second to nearly two thousand. Ten points fall in a deep V, with the "
        "trough in the telescopic era. They drop from 636 "
        "seconds at year minus one thousand through 265 at year zero, 139 at "
        "500, 54 at 1000 and 31 at 1200 to 5 seconds at 1700, 1 second at 1800 "
        "and a tenth of a second at 1900, then climb again to 612 seconds at "
        "2500 and 1885 seconds at 3000. The last two, and only those, come "
        "from Huber's extrapolation and are drawn as open squares. A "
        "horizontal dashed line at 265 seconds marks the level above which the "
        "Five Millennium Canon draws a longitude gore on its maps."
    ),
)

# --- gridlines and axes ---------------------------------------------------
for decade in (0.1, 1.0, 10.0, 100.0, 1000.0):
    f.line(PL, gy(decade), PR, gy(decade), cls="rule thin dotted")
    label = "0.1 s" if decade < 1 else f"{int(decade)} s"
    f.text(PL - 8, gy(decade) + 3.5, label, anchor="end", cls="tick")

f.line(PL, PT, PL, PB, cls="rule thin")
f.line(PL, PB, PR, PB, cls="rule thin")

for year in (-1000.0, 0.0, 1000.0, 2000.0, 3000.0):
    f.line(gx(year), PB, gx(year), PB + 5, cls="rule thin")
    f.text(gx(year), PB + 18, f"{int(year)}", anchor="middle", cls="tick")
f.text((PL + PR) / 2, PB + 36, "year", anchor="middle", cls="label-dim")
f.text(PL - 46, PT - 14, "standard error of ΔT", cls="label-dim")

# --- the gore threshold ---------------------------------------------------
f.line(PL, gy(GORE), PR, gy(GORE), cls="accent dashed")
f.text(gx(-200.0), gy(GORE) - 26,
       "265 s: above this the Five Millennium Canon", cls="label-accent")
f.text(gx(-200.0), gy(GORE) - 14,
       "draws a longitude gore on the map", cls="label-accent")

# --- the points -----------------------------------------------------------
for year, sigma, measured in POINTS:
    if measured:
        f.circle(gx(year), gy(sigma), 4.5, cls="accent-2-fill")
    else:
        f.rect(gx(year) - 4.5, gy(sigma) - 4.5, 9, 9, cls="accent-2")

# --- the legend, in the empty lower right ---------------------------------
LEG_X, LEG_Y = gx(2050.0), gy(0.4)
f.circle(LEG_X, LEG_Y, 4.5, cls="accent-2-fill")
f.text(LEG_X + 12, LEG_Y + 4, "from the observed record", cls="label-dim")
f.rect(LEG_X - 4.5, LEG_Y + 14.5, 9, 9, cls="accent-2")
f.text(LEG_X + 12, LEG_Y + 23, "from Huber's extrapolation", cls="label-dim")

# --- the three values worth reading off the page --------------------------
f.text(gx(-1000.0) + 10, gy(636.0) + 4, "636 s", cls="tick")
f.text(gx(1900.0) - 10, gy(0.1) + 4, "0.1 s", anchor="end", cls="tick")
f.text(gx(3000.0) - 10, gy(1885.0) + 4, "1885 s", anchor="end", cls="tick")

f.text(8, H - 10,
       "One second of ΔT moves the whole eclipse 465 m in longitude at the "
       "equator and 356 m at latitude 40°.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/07-earth-and-time/img/delta-t-uncertainty.svg")
print(f"  y for 0.1 s {n(gy(0.1))}, for 1885 s {n(gy(1885.0))}, "
      f"gore line {n(gy(GORE))}")
