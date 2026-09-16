#!/usr/bin/env python3
"""The ranked error budget as edge position error, on a log axis.

A data figure. Every bar is one row of the ranked budget table in
`content/20-reports/error-budget.md`, plotted at the edge position error that
row states, in metres. Nothing is interpolated and nothing is computed: where
the table gives a range the bar runs to the upper value and a tick marks the
lower one, and where the table gives no metre figure for the edge, the row is
not plotted. The two observer rows are left out because they are the observer's
error, not the product's.

    cd tools/figures && python error_budget.py
"""

import math

from figlib import Figure, n

# --- the data, read straight from the table -------------------------------
# (rank, term, low metres, high metres, printed value, dominant)
ROWS = [
    (1,  "Geometric Sun with apparent Moon", None,   38000.0, "38 km",      False),
    (2,  "TT used as UT",                    None,   32000.0, "32 km",      False),
    (3,  "Sphere instead of ellipsoid",      None,   21000.0, "up to 21 km", False),
    (4,  "Terrain omitted",                  None,    3000.0, "up to 3 km", True),
    (5,  "Lunar limb omitted",              1000.0,   3000.0, "1 to 3 km",  True),
    (7,  "Lunar radius k, umbral, IAU value", None,   1400.0, "1.4 km",     False),
    (19, "Moon light-time omitted",          None,    1300.0, "1.3 km",     False),
    (9,  "Centre of figure against centre of mass", 500.0, 1000.0, "0.5 to 1 km", False),
    (8,  "ΔT prediction error, realised in 2024",   500.0,  800.0, "500 to 800 m", False),
    (10, "Watts-era limb data",              600.0,   750.0, "600 to 750 m", False),
    (6,  "Solar radius 959.63″ against 959.95″", None, 600.0, "600 m",      True),
    (17, "Sidereal time, mean against apparent", None, 500.0, "up to 500 m", False),
    (18, "UT1 against UTC",                   None,   420.0, "up to 420 m", False),
    (11, "Geoid against ellipsoid height",    None,   170.0, "up to 170 m", False),
    (12, "Implementation spread, identical inputs", 60.0, 130.0, "60 to 130 m", False),
    (13, "Solar radius residual, ± 0.05″",    None,   100.0, "100 m band", False),
    (24, "Nutation, 1980 against 2000A",      None,    20.0, "under 20 m", False),
    (21, "Ephemeris, DE403 to DE421, at 2020", None,   16.0, "16 m",       False),
    (22, "ELP-2000/82 truncated as in the Canon", None, 10.0, "10 m",      False),
    (23, "Polar motion",                      None,    10.0, "about 10 m", False),
    (25, "TT against TDB",                    None,     2.0, "2 m",        False),
    (20, "Ephemeris, DE421 to DE440",         None,     0.9, "under 1 m",  False),
]

# --- layout ---------------------------------------------------------------
W, H = 760, 462
GUT = 300.0          # right edge of the term labels
X0, X1 = 306.0, 654.0
TOP = 44.0           # centre of the first bar
PITCH = 16.0
BAR_H = 9.0
VMIN, VMAX = 0.6, 60000.0

LOG_MIN, LOG_SPAN = math.log10(VMIN), math.log10(VMAX) - math.log10(VMIN)


def x_of(v: float) -> float:
    return X0 + (math.log10(v) - LOG_MIN) / LOG_SPAN * (X1 - X0)


AXIS_Y = TOP + (len(ROWS) - 1) * PITCH + 20.0
GRID_TOP = TOP - 14.0

f = Figure(
    W, H,
    title="The ranked error budget, as position error at an eclipse limit",
    desc=(
        "A horizontal bar chart on a logarithmic axis running from one metre to "
        "ten kilometres. Twenty-two terms from the error budget are ranked from "
        "largest to smallest. Two implementation bugs head the list at tens of "
        "kilometres: a geometric Sun paired with an apparent Moon at 38 km and TT "
        "used where UT belongs at 32 km, with a sphere used instead of the "
        "ellipsoid at 21 km behind them. Three shaded bars follow at kilometre "
        "scale and are the terms the corpus calls dominant: terrain omitted at up "
        "to 3 km, the lunar limb omitted at 1 to 3 km, and the choice of solar "
        "radius at 600 m. Below them the lunar radius constant, lunar light-time, "
        "the centre-of-figure offset and the delta T prediction error lie between "
        "400 m and 1.4 km. Everything else falls under 200 m, and the ephemeris "
        "terms at the foot of the chart are between 16 m and under a metre."
    ),
)

# --- decade grid ----------------------------------------------------------
for decade, label in ((1.0, "1 m"), (10.0, "10 m"), (100.0, "100 m"),
                      (1000.0, "1 km"), (10000.0, "10 km")):
    x = x_of(decade)
    f.line(x, GRID_TOP, x, AXIS_Y, cls="rule thin dotted")
    f.text(x, AXIS_Y + 14, label, anchor="middle", cls="tick")

f.line(X0, AXIS_Y, X1, AXIS_Y, cls="rule")

# --- bars -----------------------------------------------------------------
for i, (rank, term, lo, hi, printed, dominant) in enumerate(ROWS):
    cy = TOP + i * PITCH
    x_end = x_of(hi)
    f.rect(X0, cy - BAR_H / 2.0, x_end - X0, BAR_H,
           cls="accent-fill" if dominant else "cone")
    f.rect(X0, cy - BAR_H / 2.0, x_end - X0, BAR_H, cls="rule thin")
    if lo is not None:
        xl = x_of(lo)
        f.line(xl, cy - BAR_H / 2.0 - 2.5, xl, cy + BAR_H / 2.0 + 2.5, cls="rule")
    f.text(x_end + 6, cy + 4, printed, cls="tick")
    f.text(6, cy + 4, rank, cls="tick")
    f.text(GUT, cy + 4, ("▸ " if dominant else "") + term, anchor="end",
           cls="label-accent" if dominant else "label")

# --- axis title and legend -------------------------------------------------
f.text((X0 + X1) / 2.0, GRID_TOP - 12, "edge position error, metres, log scale",
       anchor="middle", cls="label-dim")
f.text(6, 24, "rank", cls="label-dim")
f.text(GUT, 24, "term, as the error budget ranks it", anchor="end", cls="label-dim")

f.rect(6, H - 26, 16, 8, cls="accent-fill")
f.text(28, H - 19,
       "▸ the three terms the corpus calls dominant. A tick inside a bar marks the "
       "low end of a stated range.", cls="label-dim")

f.save(__file__, "../../content/20-reports/img/error-budget.svg")
print(f"  axis {n(X0)} to {n(X1)}, 1 m at x={n(x_of(1))}, 38 km at x={n(x_of(38000))}")
