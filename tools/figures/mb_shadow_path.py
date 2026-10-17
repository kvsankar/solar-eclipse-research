#!/usr/bin/env python3
"""Prediction and reduction of a stellar occultation on the fundamental plane.

A schematic in two panels. The left panel is the fundamental plane seen
along the star direction: the Earth's disc, the shadow band whose width
equals the body's diameter (the star is effectively at infinity, so the
shadow is a cylinder, not a cone), the central line and the two 1-sigma
lines that sit one ephemeris-plus-star uncertainty outside each edge. The
right panel is the same plane after the event: chords from observers at
different cross-track offsets, one miss, a fitted ellipse, and the offset
between the fitted centre and the ephemeris position, which is the
astrometric result.

Nothing here is data. The band width, the uncertainty and the ellipse are
chosen for legibility, and the figure says so on its face.

    python tools/figures/mb_shadow_path.py
"""

import math

from figlib import Figure, n

W, H = 760, 400

# ---------------------------------------------------------------- left panel
EX, EY, ER = 190.0, 215.0, 140.0      # Earth's disc on the fundamental plane
SLOPE = -0.32                          # shadow track direction (dy/dx)
HALF = 22.0                            # half the shadow width = body radius
SIGMA = 20.0                           # 1-sigma cross-track uncertainty
OFFSET = 18.0                          # central line offset from Earth's centre

ANG = math.atan(SLOPE)
NX, NY = -math.sin(ANG), math.cos(ANG)  # unit normal to the track


def track(d: float, t: float) -> tuple[float, float]:
    """Point at along-track t and cross-track d from the central line."""
    return (EX + t * math.cos(ANG) + (OFFSET + d) * NX,
            EY + t * math.sin(ANG) + (OFFSET + d) * NY)


def chord_in_circle(d: float) -> tuple[float, float]:
    """Along-track limits where the line at cross-track d meets the disc."""
    off = OFFSET + d
    half = math.sqrt(max(ER * ER - off * off, 0.0))
    return -half, half


# ---------------------------------------------------------------- right panel
BX, BY = 575.0, 215.0                  # fitted centre
A, B = 112.0, 78.0                     # apparent semi-axes
THETA = math.radians(-22.0)            # rotation of the major axis
PRED = (BX + 30.0, BY - 26.0)          # ephemeris position, before the fit
CHORDS = [-58.0, -22.0, 18.0, 52.0]    # cross-track offsets of positive chords
MISS = 96.0                            # cross-track offset of the miss


def ellipse_x(y: float) -> tuple[float, float] | None:
    """x limits where the horizontal line at height y meets the ellipse."""
    c, s = math.cos(THETA), math.sin(THETA)
    # u = x c + y s, v = -x s + y c ; u^2/A^2 + v^2/B^2 = 1, solve for x
    qa = c * c / (A * A) + s * s / (B * B)
    qb = 2 * y * (c * s / (A * A) - s * c / (B * B))
    qc = y * y * (s * s / (A * A) + c * c / (B * B)) - 1.0
    disc = qb * qb - 4 * qa * qc
    if disc <= 0:
        return None
    r = math.sqrt(disc)
    return (-qb - r) / (2 * qa), (-qb + r) / (2 * qa)


def ellipse_points(k: int = 120) -> list[tuple[float, float]]:
    c, s = math.cos(THETA), math.sin(THETA)
    pts = []
    for i in range(k + 1):
        t = 2 * math.pi * i / k
        u, v = A * math.cos(t), B * math.sin(t)
        pts.append((BX + u * c - v * s, BY + u * s + v * c))
    return pts


f = Figure(
    W, H,
    title="Predicting and reducing a stellar occultation on the fundamental plane",
    desc=(
        "Two panels. Left: a circle for the Earth seen from the star, crossed "
        "diagonally by a band of constant width, the shadow of the occulting "
        "body. A dashed central line runs along the middle of the band, and a "
        "dashed line lies parallel to each edge, outside it, marking the "
        "1-sigma uncertainty. An arrow shows the direction of motion. Right: "
        "an ellipse for the body's outline with four horizontal solid chords "
        "across it, each ending in two dots, and one dotted horizontal line "
        "that misses the ellipse. A small plus marks the ellipse centre and a "
        "small open circle marks the ephemeris position, joined by a short "
        "arrow labelled as the astrometric offset."
    ),
)

# --- left: Earth's disc and axes
f.circle(EX, EY, ER, cls="body")
f.line(EX - ER - 12, EY, EX + ER + 16, EY, cls="axis thin", marker="arrow")
f.line(EX, EY + ER + 8, EX, EY - ER - 16, cls="axis thin", marker="arrow")
f.text(EX + ER + 18, EY + 4, "x", cls="label-em")
f.text(EX + 6, EY - ER - 14, "y", cls="label-em")

# --- left: shadow band, clipped to the disc by computing the chord limits
lo, hi = chord_in_circle(-HALF)
lo2, hi2 = chord_in_circle(HALF)
f.polygon([track(-HALF, lo), track(-HALF, hi), track(HALF, hi2), track(HALF, lo2)],
          cls="cone-deep")
for d in (-HALF, HALF):
    a, b = chord_in_circle(d)
    x1, y1 = track(d, a)
    x2, y2 = track(d, b)
    f.line(x1, y1, x2, y2, cls="accent")
a, b = chord_in_circle(0.0)
x1, y1 = track(0.0, a)
x2, y2 = track(0.0, b)
f.line(x1, y1, x2, y2, cls="axis dashed")
for d in (-(HALF + SIGMA), HALF + SIGMA):
    a, b = chord_in_circle(d)
    x1, y1 = track(d, a)
    x2, y2 = track(d, b)
    f.line(x1, y1, x2, y2, cls="accent-2 dashed")

# direction of motion
ax1, ay1 = track(-HALF / 2, 20.0)
ax2, ay2 = track(-HALF / 2, 90.0)
f.line(ax1, ay1, ax2, ay2, cls="axis", marker="arrow")
f.text(ax2 + 4, ay2 - 6, "motion", cls="label-dim")

# labels for the left panel
f.text(EX, 26, "fundamental plane, seen along the star direction", anchor="middle",
       cls="label-accent")
lx, ly = track(-(HALF + SIGMA), -60.0)
f.text(8, 56, "1σ line: edge shifted by", cls="label-dim")
f.text(8, 70, "the cross-track uncertainty", cls="label-dim")
f.line(60, 76, lx, ly, cls="rule thin")
sx, sy = track(-HALF, 70.0)
f.text(300, 372, "shadow: width D,", cls="label-dim")
f.text(300, 386, "the body's diameter", cls="label-dim")
f.line(312, 362, sx + 2, sy + 2, cls="rule thin")
cx_, cy_ = track(0.0, -110.0)
f.text(8, 330, "central line", cls="label-dim")
f.line(40, 320, cx_, cy_, cls="rule thin")
f.text(EX + ER - 30, EY + ER - 4, "Earth", cls="label")

# --- right: ellipse, chords and the miss
f.polyline(ellipse_points(), cls="accent")
for dy in CHORDS:
    y = BY + dy
    lim = ellipse_x(dy)
    if lim is None:
        continue
    x1, x2 = BX + lim[0], BX + lim[1]
    f.line(BX - A - 24, y, x1, y, cls="rule thin dotted")
    f.line(x1, y, x2, y, cls="rule")
    f.line(x2, y, BX + A + 24, y, cls="rule thin dotted")
    f.circle(x1, y, 3.2, cls="accent-2-fill")
    f.circle(x2, y, 3.2, cls="accent-2-fill")
f.line(BX - A - 24, BY + MISS, BX + A + 24, BY + MISS, cls="rule thin dotted")
f.text(BX + A + 28, BY + MISS + 4, "miss", cls="label-dim")
f.text(BX + A + 28, BY + CHORDS[0] + 4, "chord", cls="label-dim")

# fitted centre and ephemeris position
f.line(BX - 7, BY, BX + 7, BY, cls="axis")
f.line(BX, BY - 7, BX, BY + 7, cls="axis")
f.circle(PRED[0], PRED[1], 5.0, cls="rule")
f.line(PRED[0] - 4, PRED[1] + 4, BX + 4, BY - 3, cls="accent-2", marker="arrow")
f.text(PRED[0] + 8, PRED[1] - 6, "ephemeris position", cls="label-dim")
f.text(BX - 8, BY + 18, "fitted centre", anchor="end", cls="label-dim")

f.text(BX, 26, "after the event: chords on the same plane", anchor="middle",
       cls="label-accent")
f.text(BX, 44, "ellipse fit gives a′, b′, its angle and the offset", anchor="middle",
       cls="label-dim")
f.line(BX - 30, 300 + 52, BX + 30, 300 + 52, cls="rule", marker="arrow")
f.text(BX, 300 + 70, "star motion relative to the body", anchor="middle",
       cls="label-dim")

f.text(8, H - 4,
       "Schematic. Widths, uncertainty and shape are illustrative, not an event.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/17-occultations-by-planets-and-minor-bodies/img/shadow-path-and-chords.svg")
print(f"  slope={n(SLOPE)} half={n(HALF)} sigma={n(SIGMA)}")
