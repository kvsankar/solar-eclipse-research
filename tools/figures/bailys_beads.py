#!/usr/bin/env python3
"""Herald's chart: the Sun's limb crossing a stretch of the lunar profile.

A schematic drawn in the coordinates Herald 1983 and Espenak's bulletins use:
the angle C from the point of nominal second contact along the abscissa, and
the limb height above the mean limb, in arcseconds, along a greatly
exaggerated ordinate. The Sun's limb is the quoted curve

    h = 960'' (M - 1) (1 - cos C)

drawn twice. Once a few seconds before second contact, where four valleys
still show sunlight as separate beads, and once at second contact, where it
has sunk until the last of those beads closes.

The magnitude is 1.0016, Herald's limiting magnitude for a true total eclipse
at a longitude libration of -5 degrees, which keeps the curve shallow enough
for the profile to decide the contact. The profile itself is invented: the
valley depths are chosen so that the four beads close in turn.

    python tools/figures/bailys_beads.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 400
L, RGT = 78.0, 660.0           # plot area in x
TOP, BOT = 50.0, 286.0         # plot area in y

C_MIN, C_MAX = -40.0, 40.0     # degrees from the nominal contact point
H_MIN, H_MAX = -1.30, 2.20     # arcseconds above the mean limb

S0 = 960.0                     # solar semidiameter, arcseconds at 1 au
MAG = 1.0016                   # eclipse magnitude


def gx(c: float) -> float:
    return L + (c - C_MIN) / (C_MAX - C_MIN) * (RGT - L)


def gy(h: float) -> float:
    return BOT - (h - H_MIN) / (H_MAX - H_MIN) * (BOT - TOP)


def rise(c: float) -> float:
    """The curve's own rise away from the contact point."""
    return S0 * (MAG - 1.0) * (1.0 - math.cos(math.radians(c)))


def sun(c: float, base: float) -> float:
    return base + rise(c)


def wiggle(c: float) -> float:
    t = math.radians(c * 4.2)
    return 1.05 * (0.34 * math.sin(t + 0.5)
                   + 0.26 * math.sin(2.3 * t + 1.9)
                   + 0.19 * math.sin(4.1 * t + 0.3)
                   + 0.13 * math.sin(7.7 * t + 2.6)
                   + 0.09 * math.sin(12.1 * t + 1.2))


# Four valleys, each placed so that its floor sits a stated margin below the
# curve. The deepest margin is the one that survives to second contact.
VALLEYS = [(-30.0, 3.4, -1.10), (-8.0, 4.0, -1.06),
           (21.0, 3.6, -1.02), (33.0, 3.0, -0.98)]
DEPTHS = [(c, s, wiggle(c) - margin - rise(c)) for c, s, margin in VALLEYS]


def terrain(c: float) -> float:
    h = wiggle(c)
    for cc, s, d in DEPTHS:
        h -= d * math.exp(-((c - cc) / s) ** 2)
    return h


STEPS = 640
CS = [C_MIN + (C_MAX - C_MIN) * i / STEPS for i in range(STEPS + 1)]

BASE_C2 = min(terrain(c) - rise(c) for c in CS)
BASE_NOW = BASE_C2 + 0.18

f = Figure(
    W, H,
    title="Baily's beads as gaps between the solar limb and the lunar profile",
    desc=(
        "A chart with the angle from the nominal point of second contact along "
        "the horizontal axis, from minus forty to plus forty degrees, and limb "
        "height in arcseconds above the mean lunar limb on the vertical axis. "
        "A jagged curve is the lunar limb profile, with the Moon's body shaded "
        "below it. A shallow upward-curving line is the Sun's limb a few "
        "seconds before second contact. Wherever the profile lies below that "
        "line a narrow sliver of sunlight survives, and four such slivers are "
        "shaded and labelled as beads. A dotted copy of the same curve, lower "
        "on the chart, has sunk until the last of those slivers closes: that "
        "is second contact."
    ),
)

# --- the Moon's body ------------------------------------------------------
prof = [(gx(c), gy(terrain(c))) for c in CS]
f.polygon(prof + [(RGT, BOT), (L, BOT)], cls="cone-deep")

# --- the beads ------------------------------------------------------------
runs: list[list[float]] = []
run: list[float] = []
for c in CS:
    if terrain(c) < sun(c, BASE_NOW):
        run.append(c)
    elif run:
        runs.append(run)
        run = []
if run:
    runs.append(run)
beads = [r for r in runs if len(r) > 5]

for r in beads:
    top = [(gx(c), gy(sun(c, BASE_NOW))) for c in r]
    bottom = [(gx(c), gy(terrain(c))) for c in reversed(r)]
    f.polygon(top + bottom, cls="accent-2-fill")

# --- the mean limb and the frame ------------------------------------------
f.line(L, gy(0.0), RGT, gy(0.0), cls="axis dashed")
f.text(RGT - 2, gy(0.0) - 6, "mean limb", anchor="end", cls="label-dim")

f.line(L, TOP, L, BOT, cls="rule thin")
f.line(L, BOT, RGT, BOT, cls="rule thin")

for c in (-40.0, -20.0, 0.0, 20.0, 40.0):
    f.line(gx(c), BOT, gx(c), BOT + 5, cls="rule thin")
    f.text(gx(c), BOT + 18, f"{int(c)}°", anchor="middle", cls="tick")
f.text((L + RGT) / 2, BOT + 36,
       "C, the angle from the point of nominal second contact",
       anchor="middle", cls="label-dim")

for h in (-1.0, 0.0, 1.0, 2.0):
    f.line(L - 5, gy(h), L, gy(h), cls="rule thin")
    f.text(L - 9, gy(h) + 3.5, "0" if h == 0.0 else f"{h:+.0f}",
           anchor="end", cls="tick")
f.text(L - 40, TOP - 10, "limb height, arcseconds", cls="label-dim")

# --- the profile and the two positions of the solar limb ------------------
f.polyline(prof, cls="rule")
f.polyline([(gx(c), gy(sun(c, BASE_C2))) for c in CS], cls="axis dotted")
f.polyline([(gx(c), gy(sun(c, BASE_NOW))) for c in CS], cls="accent")

# --- labels, all kept in the clear band above the highest peak ------------
f.text(L + 4, 70, "h = 960″ (M − 1)(1 − cos C),  M = 1.0016", cls="label-em")

LEAD_NOW = 380.0
f.line(LEAD_NOW, 100, LEAD_NOW, gy(sun((LEAD_NOW - L) / (RGT - L)
                                      * (C_MAX - C_MIN) + C_MIN, BASE_NOW)) - 3,
       cls="accent thin")
f.text(RGT - 4, 92, "the Sun's limb a few seconds before second contact",
       anchor="end", cls="label-accent")

LEAD_C2 = 340.0
f.line(LEAD_C2, 78, LEAD_C2, gy(sun((LEAD_C2 - L) / (RGT - L)
                                     * (C_MAX - C_MIN) + C_MIN, BASE_C2)) - 3,
       cls="axis thin")
f.text(RGT - 4, 70,
       "dotted: the same curve at second contact, when the last bead goes out",
       anchor="end", cls="label-dim")

last = min(beads, key=lambda r: min(terrain(c) - rise(c) for c in r))
lc = sum(last) / len(last)
f.line(gx(lc), 138, gx(lc), gy(sun(lc, BASE_NOW)) - 3, cls="accent-2 thin")
f.text(L + 4, 130, "beads: sunlight surviving in the valleys", cls="label")

f.text(8, H - 8,
       "Schematic. The profile is invented, and the height scale is "
       "exaggerated against the angle scale by about a thousand times.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/05-lunar-limb/img/bailys-beads.svg")
print(f"  base at C2 {n(BASE_C2)}  base drawn {n(BASE_NOW)}  beads {len(beads)}"
      f"  last bead near C={n(lc)}")
for r in beads:
    print(f"    bead {n(r[0])}° to {n(r[-1])}°")
