#!/usr/bin/env python3
"""Why raising an observer moves the shadow edge by h cot A.

A schematic. The edge of the umbra is a surface inclined at the Sun's
altitude A, so an observer raised by h above the ellipsoid meets it at a point
displaced horizontally by h cot A toward the Sun's azimuth. The drawing is
laid out at A = 60 degrees, the angle of the worked number the corpus quotes,
so the drawn ratio of the offset to the drawn height really is cot 60 = 0.577.

Only the component perpendicular to the limit line moves the observer into or
out of the umbra, which is the sin D in Espenak's elevation factor. The panel
carries the quoted numbers.

    python tools/figures/terrain_shift.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 400
GROUND = 300.0
LEFT, RIGHT = 40.0, 470.0
TOP_Y = 70.0
OBS_X = 320.0
Hgt = 96.0                     # drawn observer height, pixels
ALT = 60.0                     # the Sun's altitude, degrees

COT = 1.0 / math.tan(math.radians(ALT))
EDGE_X = OBS_X - Hgt * COT      # where the same edge meets the ellipsoid

PANEL_X = 494.0
WORKED = [("60°", "577 m"), ("45°", "1000 m"), ("30°", "1732 m")]


def ray(x0: float, y0: float, t: float) -> tuple[float, float]:
    """A point t along the sunward direction from (x0, y0)."""
    return (x0 + t * math.cos(math.radians(ALT)),
            y0 - t * math.sin(math.radians(ALT)))


EDGE_TOP = ray(EDGE_X, GROUND, (GROUND - TOP_Y) / math.sin(math.radians(ALT)))

f = Figure(
    W, H,
    title="An observer raised by h meets the shadow edge h cot A sooner",
    desc=(
        "A cross-section. A solid horizontal line is the ellipsoid and a "
        "dashed horizontal line above it is the terrain at height h. A "
        "straight line inclined at sixty degrees, the Sun's altitude, is the "
        "edge of the umbra: it runs down from the upper right, crosses the "
        "terrain line at the observer, and meets the ellipsoid further to the "
        "left at the point where a sea-level map draws the limit. The "
        "horizontal gap between those two crossings, marked with a double "
        "arrow below the ellipsoid, is h cot A. Everything to the left of the "
        "edge is shaded as inside the umbra. Dotted rays parallel to the edge "
        "show the direction of the Sun. A panel lists the shift per thousand "
        "metres of elevation: 577 metres with the Sun at sixty degrees, 1000 "
        "metres at forty-five and 1732 metres at thirty."
    ),
)

# --- inside the umbra, left of the edge -----------------------------------
f.polygon([(LEFT, TOP_Y), (EDGE_TOP[0], TOP_Y), (EDGE_X, GROUND),
           (LEFT, GROUND)], cls="cone-deep")
f.text(LEFT + 12, TOP_Y + 22, "inside the umbra", cls="label-dim")

# --- the two surfaces -----------------------------------------------------
f.line(LEFT, GROUND, RIGHT, GROUND, cls="axis")
f.text(RIGHT - 2, GROUND + 16, "WGS 84 ellipsoid", anchor="end", cls="label-dim")

f.line(LEFT, GROUND - Hgt, RIGHT, GROUND - Hgt, cls="axis dashed")
f.text(RIGHT - 2, GROUND - Hgt - 8, "terrain at height h", anchor="end",
       cls="label-dim")

# --- the shadow edge ------------------------------------------------------
f.line(EDGE_TOP[0], TOP_Y, EDGE_X, GROUND, cls="accent")
f.text(EDGE_TOP[0] + 6, TOP_Y + 12, "edge of the umbra", cls="label-accent")

# --- the Sun's direction --------------------------------------------------
for off in (60.0, 90.0, 120.0):
    x0, y0 = EDGE_X + off, GROUND - 8.0
    f.line(x0, y0, *ray(x0, y0, 120.0), cls="rule thin dotted")

ax, ay = EDGE_X + 150.0, GROUND - 8.0
f.line(*ray(ax, ay, 100.0), *ray(ax, ay, 140.0), cls="axis", marker="arrow")
tip = ray(ax, ay, 140.0)
f.text(tip[0] - 6, tip[1] - 6, "to the Sun", anchor="end", cls="label-dim")

# --- the altitude angle at the ellipsoid ---------------------------------
arc_end = ray(EDGE_X, GROUND, 42.0)
f.path(f"M {n(EDGE_X + 42)} {n(GROUND)} A 42 42 0 0 0 "
       f"{n(arc_end[0])} {n(arc_end[1])}", cls="rule thin")
f.text(EDGE_X + 8, GROUND - 8, "A = 60°", cls="label-em")

# --- the observer, the height and the shift ------------------------------
f.line(OBS_X, GROUND - Hgt, OBS_X, GROUND, cls="accent-2 dashed")
f.text(OBS_X + 6, GROUND - Hgt / 2 + 4, "h", cls="label-em")
f.circle(OBS_X, GROUND - Hgt, 4.5, cls="accent-2-fill")
f.text(OBS_X + 16, GROUND - Hgt - 24, "observer", cls="label")

f.line(EDGE_X, GROUND + 30, OBS_X, GROUND + 30, cls="accent-2", marker="arrow")
f.line(OBS_X, GROUND + 30, EDGE_X, GROUND + 30, cls="accent-2", marker="arrow")
f.text((EDGE_X + OBS_X) / 2, GROUND + 46, "h cot A", anchor="middle",
       cls="label-em")

f.line(EDGE_X, GROUND, EDGE_X, GROUND + 34, cls="rule thin")
f.text(EDGE_X - 6, GROUND + 62, "the limit drawn", anchor="end", cls="label-dim")
f.text(EDGE_X - 6, GROUND + 74, "at sea level", anchor="end", cls="label-dim")
f.text(OBS_X + 6, GROUND + 62, "where the raised observer", cls="label-dim")
f.text(OBS_X + 6, GROUND + 74, "actually meets the edge", cls="label-dim")

# --- the numbers ----------------------------------------------------------
f.text(PANEL_X, 92, "Shift per 1000 m of elevation,", cls="label")
f.text(PANEL_X, 106, "with the Sun square to the limit:", cls="label")
row = 132.0
for angle, shift in WORKED:
    f.text(PANEL_X + 20, row, f"A = {angle}", cls="label-dim")
    f.text(PANEL_X + 174, row, shift, anchor="end", cls="tick")
    row += 20

f.text(PANEL_X, row + 16, "Only the component across the", cls="label-dim")
f.text(PANEL_X, row + 28, "limit counts, so the full shift is", cls="label-dim")
f.text(PANEL_X, row + 46, "Δ⊥ = h cot A sin D,", cls="label-em")
f.text(PANEL_X, row + 64, "with D the angle between the", cls="label-dim")
f.text(PANEL_X, row + 76, "Sun's azimuth and the limit line.", cls="label-dim")

f.text(8, H - 8,
       "Schematic. The height is exaggerated and the ellipsoid is drawn flat, "
       "but the drawn offset really is cot 60° of the drawn height.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/07-earth-and-time/img/terrain-shift.svg")
print(f"  edge at x={n(EDGE_X)}  observer x={n(OBS_X)}  "
      f"offset={n(OBS_X - EDGE_X)} px for h={n(Hgt)} px  cot A={n(COT)}")
