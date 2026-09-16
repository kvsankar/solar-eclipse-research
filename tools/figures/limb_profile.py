#!/usr/bin/env python3
"""The true lunar limb against the mean limb, with one valley and one peak.

A schematic. The relief is a sum of fixed sinusoids with a valley and a peak
added at chosen position angles, not a real profile, and the radial departure
is exaggerated by the factor printed on the figure so that a few arcseconds
are visible against a limb of about 932 arcseconds.

The figure has to carry three things: that position angle runs from the
Moon's north pole through east, that the departure from the mean limb is a
few arcseconds either way, and that a valley keeps sunlight flowing after the
nominal second contact while a peak cuts it off early.

    python tools/figures/limb_profile.py
"""

import math

from figlib import Figure, n, polar

# --- layout ---------------------------------------------------------------
W, H = 700, 420
CX, CY = 236.0, 220.0
R = 132.0                      # the mean limb, drawn
AMP = 8.0                      # drawn pixels per arcsecond of relief
MAX_RELIEF = 3.0               # arcseconds, the figure's largest departure
MEAN_LIMB_ARCSEC = 932.58      # semidiameter of the mean limb at mean distance

EXAGGERATION = AMP / (R / MEAN_LIMB_ARCSEC)

TEXT_X = 452.0                 # left edge of the right-hand text column
PEAK_PA = 66.0
VALLEY_PA = 114.0
CONTACT_PA = 90.0


def relief(deg: float) -> float:
    """Departure from the mean limb in arcseconds. Fixed, not random."""
    t = math.radians(deg)
    base = (0.36 * math.sin(3 * t + 0.4)
            + 0.30 * math.sin(7 * t + 1.1)
            + 0.28 * math.sin(11 * t + 2.3)
            + 0.26 * math.sin(17 * t + 0.7)
            + 0.20 * math.sin(29 * t + 1.9))
    h = base / 1.40 * 1.45
    h += 2.30 * math.exp(-((angdiff(deg, PEAK_PA)) / 5.0) ** 2)
    h -= 2.20 * math.exp(-((angdiff(deg, VALLEY_PA)) / 5.5) ** 2)
    return max(-MAX_RELIEF, min(MAX_RELIEF, h))


def angdiff(a: float, b: float) -> float:
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d


def radius(deg: float) -> float:
    return R + AMP * relief(deg)


def pt(deg: float) -> tuple[float, float]:
    return polar(CX, CY, radius(deg), deg)


def span(centre: float, want_outside: bool) -> tuple[float, float]:
    """Contiguous run of position angles around `centre` on one side of R."""
    def outside(d):
        return relief(d) > 0.0

    lo = centre
    while outside(lo - 0.5) == want_outside and centre - lo < 40.0:
        lo -= 0.5
    hi = centre
    while outside(hi + 0.5) == want_outside and hi - centre < 40.0:
        hi += 0.5
    return lo, hi


def sliver(lo: float, hi: float) -> list[tuple[float, float]]:
    """Polygon between the true profile and the mean limb over [lo, hi]."""
    pts = [pt(lo + 0.5 * i) for i in range(int((hi - lo) / 0.5) + 1)]
    back = [polar(CX, CY, R, hi - 0.5 * i)
            for i in range(int((hi - lo) / 0.5) + 1)]
    return pts + back


f = Figure(
    W, H,
    title="The true lunar limb against the mean limb",
    desc=(
        "A circle stands for the mean lunar limb. A closed wiggly curve drawn "
        "around it is the true limb, departing inward and outward by up to "
        "about two and a half arcseconds, with the departure exaggerated "
        "about fifty-seven times. Position angle is marked at zero, ninety, "
        "one hundred and eighty and two hundred and seventy degrees, measured "
        "from the Moon's north pole through east. Near position angle "
        "sixty-six degrees the true limb bulges outside the circle at a "
        "mountain peak, and near one hundred and fourteen degrees it dips "
        "inside the circle at a valley. "
        "The peak region and the valley region are shaded and labelled: the "
        "peak hides the Sun early, the valley still lets sunlight through "
        "after the nominal second contact."
    ),
)

# --- the two shaded departures -------------------------------------------
p_lo, p_hi = span(PEAK_PA, True)
v_lo, v_hi = span(VALLEY_PA, False)
f.polygon(sliver(p_lo, p_hi), cls="cone-deep")
f.polygon(sliver(v_lo, v_hi), cls="cone")

# --- the mean limb --------------------------------------------------------
f.circle(CX, CY, R, cls="axis dashed")

# --- the true limb --------------------------------------------------------
whole = [pt(0.5 * i) for i in range(720)]
f.polygon(whole, cls="rule")

peak_arc = [pt(p_lo + 0.5 * i) for i in range(int((p_hi - p_lo) / 0.5) + 1)]
valley_arc = [pt(v_lo + 0.5 * i) for i in range(int((v_hi - v_lo) / 0.5) + 1)]
f.polyline(peak_arc, cls="accent")
f.polyline(valley_arc, cls="accent-2")

# --- position angle ticks -------------------------------------------------
for pa in (0.0, 90.0, 180.0, 270.0):
    x1, y1 = polar(CX, CY, R - AMP * MAX_RELIEF - 4, pa)
    x2, y2 = polar(CX, CY, R + AMP * MAX_RELIEF + 4, pa)
    f.line(x1, y1, x2, y2, cls="rule thin dotted")

LAB = R + AMP * MAX_RELIEF + 10
f.text(CX, CY - LAB - 6, "PA 0°, lunar north", anchor="middle", cls="label-dim")
f.text(CX, CY + LAB + 16, "PA 180°", anchor="middle", cls="label-dim")
f.text(CX - LAB - 6, CY + 4, "PA 270°", anchor="end", cls="label-dim")
f.text(CX + LAB + 6, CY - 6, "PA 90°, east", cls="label-dim")
f.text(CX + LAB + 6, CY + 8, "nominal contact point", cls="label-dim")

# --- the mean limb label, placed in the quiet south-west quadrant ---------
mx, my = polar(CX, CY, R, 225.0)
f.line(mx, my, mx - 44, my + 34, cls="rule thin")
f.text(mx - 108, my + 46, "mean limb, and the Sun's", cls="label-dim")
f.text(mx - 108, my + 58, "limb at nominal C2", cls="label-dim")

# --- callouts -------------------------------------------------------------
px, py = pt(PEAK_PA)
f.line(px, py, TEXT_X - 22, 122, cls="accent thin")
f.text(TEXT_X, 110, "Peak at PA 66°", cls="label-accent")
f.text(TEXT_X, 126, "The Moon already covers the Sun", cls="label-dim")
f.text(TEXT_X, 138, "here, so the light at this angle", cls="label-dim")
f.text(TEXT_X, 150, "is cut off before nominal C2.", cls="label-dim")

vx, vy = pt(VALLEY_PA)
f.line(vx, vy, TEXT_X - 22, 276, cls="accent-2 thin")
f.text(TEXT_X, 264, "Valley at PA 114°", cls="label")
f.text(TEXT_X, 280, "Sunlight still reaches the observer", cls="label-dim")
f.text(TEXT_X, 292, "through this valley after nominal", cls="label-dim")
f.text(TEXT_X, 304, "C2, so second contact comes late.", cls="label-dim")

f.text(TEXT_X, 62, "Position angle runs from the Moon's", cls="label-dim")
f.text(TEXT_X, 74, "north pole through east.", cls="label-dim")

f.text(8, H - 8,
       "Schematic. The relief is exaggerated about "
       f"{round(EXAGGERATION)} times, and the profile is invented "
       "rather than real LOLA data.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/05-lunar-limb/img/limb-profile.svg")
print(f"  exaggeration x{n(EXAGGERATION)}  peak {n(p_lo)}..{n(p_hi)}  "
      f"valley {n(v_lo)}..{n(v_hi)}")
