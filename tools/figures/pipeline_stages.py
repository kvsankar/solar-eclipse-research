#!/usr/bin/env python3
"""The nine pipeline stages, the two computational paths, and the two modes.

A schematic of the design in `content/20-reports/pipeline-design.md`: the
configuration record fixed before stage 1, the ephemeris layer both paths read,
the elements path down the left, the direct topocentric path down the right,
their rejoining at local circumstances as a 0.1 s cross-check, and the bracket
that separates almanac mode from what edge mode adds.

    cd tools/figures && python pipeline_stages.py
"""

from figlib import Figure

# --- layout ---------------------------------------------------------------
W, H = 740, 706

MAIN_X0, MAIN_X1 = 52.0, 430.0      # the elements path column
SIDE_X0, SIDE_X1 = 470.0, 724.0     # the direct topocentric column
FULL_X0, FULL_X1 = 52.0, 724.0      # stages both paths share
BOX_H = 40.0
RAIL_X = 30.0                       # the mode brackets

ROW = {                             # top edge of each box
    "cfg": 56.0,
    1: 124.0,
    2: 200.0,
    3: 260.0,
    4: 320.0,
    5: 380.0,
    6: 440.0,
    7: 516.0,
    8: 576.0,
    9: 636.0,
}

MAIN_MID = (MAIN_X0 + MAIN_X1) / 2.0
SIDE_MID = (SIDE_X0 + SIDE_X1) / 2.0

f = Figure(
    W, H,
    title="The nine-stage eclipse computation pipeline",
    desc=(
        "A flow chart read from top to bottom. A configuration record sits above "
        "everything, followed by stage 1, the ephemeris, orientation and time "
        "layer, which spans the full width. Below it the flow splits in two. The "
        "left column is the elements path: stage 2 enumeration, stage 3 Besselian "
        "elements, stage 4 global circumstances, stage 5 partial-eclipse maps and "
        "stage 6 local circumstances. The right column is a single dashed box, the "
        "direct topocentric path, which root-finds on apparent topocentric places "
        "and takes no Besselian elements. An arrow leads from it back into stage 6, "
        "labelled as a cross-check the two paths must pass to 0.1 seconds. Below "
        "stage 6 the flow is one column again: stage 7 terrain, stage 8 lunar limb "
        "and stage 9 products with uncertainty. A bracket down the left edge marks "
        "stages 1 to 6 as almanac mode and stages 7 and 8 as what edge mode adds; "
        "stage 9 belongs to both."
    ),
)


def box(x0, x1, y, number, heading, sub, dashed=False):
    """A stage box: fill, outline, stage number, heading and one dim subtitle."""
    f.rect(x0, y, x1 - x0, BOX_H, cls="cone", rx=4)
    f.rect(x0, y, x1 - x0, BOX_H, cls="rule dashed" if dashed else "rule", rx=4)
    tx = x0 + 14
    if number is not None:
        f.text(tx, y + 25, number, cls="label-accent")
        tx += 16
    f.text(tx, y + 17, heading, cls="label")
    f.text(tx, y + 31, sub, cls="label-dim")


def down(x, y_from, y_to, cls="axis"):
    f.line(x, y_from, x, y_to, cls=cls, marker="arrow")


# --- stage 0: the configuration record ------------------------------------
f.rect(FULL_X0, ROW["cfg"], FULL_X1 - FULL_X0, BOX_H, cls="rule dotted", rx=4)
f.text(FULL_X0 + 14, ROW["cfg"] + 17,
       "Configuration record, fixed before stage 1 and printed with every product",
       cls="label")
f.text(FULL_X0 + 14, ROW["cfg"] + 31,
       "ephemeris, lunar orientation, ellipsoid, s₀, k₁, k₂, terrain, ΔT, time scale, refraction",
       cls="label-dim")
down(MAIN_MID, ROW["cfg"] + BOX_H, ROW[1] - 4)

# --- stage 1: the layer both paths read -----------------------------------
box(FULL_X0, FULL_X1, ROW[1], "1", "Ephemeris, orientation and time",
    "apparent places of Sun and Moon, sidereal time, topocentric libration, ΔT as metadata")

# --- the split -------------------------------------------------------------
down(MAIN_MID, ROW[1] + BOX_H, ROW[2] - 4)
f.text(MAIN_MID + 8, ROW[1] + BOX_H + 22, "elements path", cls="label-dim")

down(SIDE_MID, ROW[1] + BOX_H, ROW[3] - 4)
f.text(SIDE_MID - 8, ROW[1] + BOX_H + 30, "direct topocentric path",
       anchor="end", cls="label-dim")

# --- the elements path -----------------------------------------------------
box(MAIN_X0, MAIN_X1, ROW[2], "2", "Enumeration and provisional type",
    "lunations, γ and u, type, Saros")
down(MAIN_MID, ROW[2] + BOX_H, ROW[3] - 4)

box(MAIN_X0, MAIN_X1, ROW[3], "3", "Besselian elements",
    "x, y, d, μ, l₁, l₂, tan f₁, tan f₂")
down(MAIN_MID, ROW[3] + BOX_H, ROW[4] - 4)

box(MAIN_X0, MAIN_X1, ROW[4], "4", "Global circumstances, smooth Moon",
    "central line, limits, durations, width")
down(MAIN_MID, ROW[4] + BOX_H, ROW[5] - 4)

box(MAIN_X0, MAIN_X1, ROW[5], "5", "Partial-eclipse maps",
    "magnitude and obscuration contours")
down(MAIN_MID, ROW[5] + BOX_H, ROW[6] - 4)

box(MAIN_X0, MAIN_X1, ROW[6], "6", "Local circumstances, smooth Moon",
    "contacts, magnitude, obscuration, P and V")

# --- the direct topocentric path -------------------------------------------
SIDE_Y0, SIDE_Y1 = ROW[3], ROW[5] + 30.0
f.rect(SIDE_X0, SIDE_Y0, SIDE_X1 - SIDE_X0, SIDE_Y1 - SIDE_Y0,
       cls="rule dashed", rx=4)
f.text(SIDE_X0 + 14, SIDE_Y0 + 22, "Direct topocentric path", cls="label")
f.text(SIDE_X0 + 14, SIDE_Y0 + 40, "root-find δ(t) = rₛ ± rₘ on the", cls="label-dim")
f.text(SIDE_X0 + 14, SIDE_Y0 + 54, "apparent topocentric places of", cls="label-dim")
f.text(SIDE_X0 + 14, SIDE_Y0 + 68, "stage 1, with no elements formed", cls="label-dim")
f.text(SIDE_X0 + 14, SIDE_Y0 + 90, "site-level work and limb tests", cls="label-dim")

# --- the rejoin, drawn as a cross-check ------------------------------------
JOIN_Y = ROW[6] + BOX_H / 2.0
f.path(f"M {SIDE_MID} {SIDE_Y1} L {SIDE_MID} {JOIN_Y} L {MAIN_X1 + 6} {JOIN_Y}",
       cls="accent-2 dashed", marker="arrow")
f.text(SIDE_MID - 8, JOIN_Y - 20, "cross-check", anchor="end", cls="label-accent")
f.text(SIDE_MID - 8, JOIN_Y - 7, "the two paths agree to 0.1 s",
       anchor="end", cls="label-dim")

# --- the shared tail -------------------------------------------------------
down(MAIN_MID, ROW[6] + BOX_H, ROW[7] - 4)

box(FULL_X0, FULL_X1, ROW[7], "7", "Terrain",
    "SRTM GL1 or Copernicus GLO-30 orthometric height plus geoid undulation")
down(MAIN_MID, ROW[7] + BOX_H, ROW[8] - 4)

box(FULL_X0, FULL_X1, ROW[8], "8", "Lunar limb",
    "LOLA profile binned to 18,000 elements, then umbra polygons, true limits and beads")
down(MAIN_MID, ROW[8] + BOX_H, ROW[9] - 4)

box(FULL_X0, FULL_X1, ROW[9], "9", "Products with uncertainty",
    "error-budget rows summed in quadrature, limits drawn at s₀ and s₀ ± σ")

# --- the mode brackets -----------------------------------------------------
def bracket(y0, y1, cls, label, label_cls):
    f.line(RAIL_X, y0, RAIL_X, y1, cls=cls)
    f.line(RAIL_X, y0, RAIL_X + 9, y0, cls=cls)
    f.line(RAIL_X, y1, RAIL_X + 9, y1, cls=cls)
    mid = (y0 + y1) / 2.0
    f.text(RAIL_X - 7, mid, label, anchor="middle", cls=label_cls,
           extra=f'transform="rotate(-90 {RAIL_X - 7} {mid})"')


bracket(ROW[1], ROW[6] + BOX_H, "accent",
        "almanac mode: stages 1 to 6", "label-accent")
bracket(ROW[7], ROW[8] + BOX_H, "accent-2 dashed",
        "edge mode adds 7 and 8", "label-accent")
f.text(RAIL_X - 7, ROW[9] + BOX_H / 2.0, "both modes", anchor="middle",
       cls="label-dim",
       extra=f'transform="rotate(-90 {RAIL_X - 7} {ROW[9] + BOX_H / 2.0})"')

f.text(8, H - 8,
       "Schematic. Stage numbers follow the pipeline design note. "
       "A dashed outline marks the path that forms no elements.",
       cls="label-dim")

f.save(__file__, "../../content/20-reports/img/pipeline-stages.svg")
