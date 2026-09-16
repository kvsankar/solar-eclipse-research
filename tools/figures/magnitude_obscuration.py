#!/usr/bin/env python3
"""Obscuration against magnitude, from the quoted two-disc overlap formula.

A data figure. Every plotted point is computed here from the lens-area formula
the corpus quotes from the 1961 Explanatory Supplement, section 9D, with the
solar radius as the unit of length and s the lunar radius in the same unit:

    delta = 1 + s - 2 M                      separation of the two centres
    alpha = arccos((delta^2 + s^2 - 1) / (2 delta s))
    beta  = arccos((delta^2 + 1 - s^2) / (2 delta))
    area  = s^2 alpha + beta
            - 1/2 sqrt((-delta+1+s)(delta+1-s)(delta-1+s)(delta+1+s))
    obscuration = area / pi

The representative ratio is s = 1.00, equal apparent discs, which is the case
the corpus states a number for: magnitude 0.5 hides about 39 per cent of the
disc. The script prints that check value.

    cd tools/figures && python magnitude_obscuration.py
"""

import math

from figlib import Figure, n

W, H = 680, 448
X0, X1 = 80.0, 420.0                    # plot box, x
Y0, Y1 = 380.0, 40.0                    # plot box, y (y0 is the bottom)
S = 1.00                                # apparent radius ratio, Moon / Sun


def obscuration(magnitude: float, s: float = S) -> float:
    """Fraction of the solar area covered, from the quoted lens-area formula."""
    d = 1.0 + s - 2.0 * magnitude
    if d >= 1.0 + s:
        return 0.0
    if d <= abs(s - 1.0):
        return min(s * s, 1.0)
    alpha = math.acos((d * d + s * s - 1.0) / (2.0 * d * s))
    beta = math.acos((d * d + 1.0 - s * s) / (2.0 * d))
    root = math.sqrt((-d + 1.0 + s) * (d + 1.0 - s) * (d - 1.0 + s) * (d + 1.0 + s))
    return (s * s * alpha + beta - 0.5 * root) / math.pi


def px(magnitude: float) -> float:
    return X0 + magnitude * (X1 - X0)


def py(value: float) -> float:
    return Y0 + value * (Y1 - Y0)


CHECK_M = 0.5
CHECK_O = obscuration(CHECK_M)

f = Figure(
    W, H,
    title="Obscuration against magnitude for equal apparent discs",
    desc=(
        "A square plot with magnitude from zero to one along the horizontal "
        "axis and obscuration from zero to one up the vertical axis. A dashed "
        "straight line runs corner to corner where obscuration would equal "
        "magnitude. The computed curve starts at the same origin, stays well "
        "below that line throughout, rising slowly at first and steeply near "
        "the right, and meets it again only at the top right corner where the "
        "discs coincide. A marked point on the curve shows that a magnitude of "
        "0.50 corresponds to an obscuration of 0.391."
    ),
)

# --- axes -----------------------------------------------------------------
f.line(X0, Y0, X1, Y0, cls="rule")
f.line(X0, Y0, X0, Y1, cls="rule")

for i in range(6):
    v = i / 5.0
    f.line(px(v), Y0, px(v), Y0 + 5, cls="rule thin")
    f.text(px(v), Y0 + 18, f"{v:.1f}", anchor="middle", cls="tick")
    f.line(X0, py(v), X0 - 5, py(v), cls="rule thin")
    f.text(X0 - 9, py(v) + 4, f"{v:.1f}", anchor="end", cls="tick")
    if i:
        f.line(X0, py(v), X1, py(v), cls="rule thin dotted")

f.text((X0 + X1) / 2.0, Y0 + 40, "magnitude, the fraction of the solar diameter",
       anchor="middle", cls="label")
f.text(X0 - 42, Y1 - 12, "obscuration", cls="label")

# --- the reference line obscuration = magnitude ---------------------------
f.line(px(0.0), py(0.0), px(1.0), py(1.0), cls="accent-2 dashed")

# --- the computed curve ---------------------------------------------------
curve = [(px(i / 400.0), py(obscuration(i / 400.0))) for i in range(401)]
f.polyline(curve, cls="accent")

# --- the check point the corpus states a number for -----------------------
f.circle(px(CHECK_M), py(CHECK_O), 3.6, cls="accent-fill")
f.line(px(CHECK_M) + 5, py(CHECK_O) + 5, px(CHECK_M) + 18, py(CHECK_O) + 16,
       cls="rule thin")
f.text(px(CHECK_M) + 20, py(CHECK_O) + 20,
       f"obscuration {CHECK_O:.3f} at magnitude {CHECK_M:.2f}", cls="label")

# --- the right-hand column ------------------------------------------------
COL = 446.0
f.text(COL, 60, "apparent radius ratio", cls="label")
f.text(COL, 76, "s = 1.00, equal discs", cls="label-em")

f.text(COL, 106, "magnitude is the fraction of", cls="label-dim")
f.text(COL, 118, "the solar diameter covered", cls="label-dim")
f.text(COL, 138, "obscuration is the fraction", cls="label-dim")
f.text(COL, 150, "of the solar area covered", cls="label-dim")

f.line(COL, 180, COL + 30, 180, cls="accent-2 dashed")
f.text(COL + 36, 184, "obscuration = magnitude", cls="label-dim")
f.line(COL, 204, COL + 30, 204, cls="accent")
f.text(COL + 36, 208, "the computed curve", cls="label-dim")
f.text(COL, 228, "which lies below it at every", cls="label-dim")
f.text(COL, 240, "magnitude short of one", cls="label-dim")

f.text(8, H - 8,
       "Computed from the lens-area formula of the 1961 Explanatory "
       "Supplement, section 9D.", cls="label-dim")

f.save(__file__,
       "../../content/10-raw/04-local-circumstances/img/magnitude-obscuration.svg")
for m in (0.0, 0.2, 0.5, 0.8, 0.95, 1.0):
    print(f"  M={m:.2f}  obscuration={obscuration(m):.4f}")
