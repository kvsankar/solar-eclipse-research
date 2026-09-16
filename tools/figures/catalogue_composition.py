#!/usr/bin/env python3
"""Composition of the Five Millennium Catalogue by eclipse type.

Counts and percentages are the catalogue's own, NASA/TP-2009-214174, as
quoted in `enumerating-eclipses.md`: 11,898 eclipses in -1999 to +3000, of
which 4,200 partial (35.3%), 3,956 annular (33.2%), 3,173 total (26.7%) and
569 hybrid (4.8%). No number here is derived.

    cd tools/figures && python catalogue_composition.py
"""

from figlib import Figure, n

W, H = 700, 320

ROWS = [
    ("partial", 4200, "35.3%"),
    ("annular", 3956, "33.2%"),
    ("total", 3173, "26.7%"),
    ("hybrid", 569, "4.8%"),
]

BAR_X = 122.0                 # the zero line
BAR_MAX = 442.0               # pixels for the longest bar
BAR_H = 34.0
TOP = 62.0                    # centre of the first bar
STEP = 55.0
AXIS_MAX = 4200

TOP_RULE = TOP - BAR_H / 2 - 12
BOT_RULE = TOP + STEP * 3 + BAR_H / 2 + 12


def bx(count: float) -> float:
    return BAR_X + count / AXIS_MAX * BAR_MAX


f = Figure(
    W, H,
    title="Composition of the Five Millennium Catalogue",
    desc=(
        "A horizontal bar chart of the 11,898 solar eclipses in the Five "
        "Millennium Catalogue by type. Partial is the longest bar at 4,200 "
        "eclipses or 35.3 per cent, annular next at 3,956 or 33.2 per cent, "
        "total next at 3,173 or 26.7 per cent, and hybrid a short bar at 569 "
        "or 4.8 per cent. Partial, annular and total are of comparable size; "
        "hybrid is smaller than any of them by a factor of about six."
    ),
)

f.text(8, 28, "Five Millennium Catalogue of Solar Eclipses, "
              "−1999 to +3000: 11,898 eclipses", cls="label")

# gridlines behind the bars
for v in (1000, 2000, 3000, 4000):
    f.line(bx(v), TOP_RULE, bx(v), BOT_RULE, cls="rule dotted")

for i, (name, count, pct) in enumerate(ROWS):
    cy = TOP + STEP * i
    f.rect(BAR_X, cy - BAR_H / 2, bx(count) - BAR_X, BAR_H, cls="cone")
    f.rect(BAR_X, cy - BAR_H / 2, bx(count) - BAR_X, BAR_H, cls="rule thin")
    f.text(BAR_X - 10, cy + 4, name, anchor="end", cls="label")
    shown = f"{count:,}"
    f.text(bx(count) + 12, cy + 4, shown, cls="label")
    f.text(bx(count) + 24 + 7.2 * len(shown), cy + 4, f"({pct})",
           cls="label-dim")

# axis
f.line(BAR_X, TOP_RULE, BAR_X, BOT_RULE, cls="rule")
f.line(BAR_X, BOT_RULE, bx(AXIS_MAX), BOT_RULE, cls="rule")
for v in (0, 1000, 2000, 3000, 4000):
    f.line(bx(v), BOT_RULE, bx(v), BOT_RULE + 4, cls="rule")
    f.text(bx(v), BOT_RULE + 17, f"{v:,}", anchor="middle", cls="tick")
f.text((BAR_X + bx(AXIS_MAX)) / 2.0, BOT_RULE + 38, "number of eclipses",
       anchor="middle", cls="label")

f.save(__file__, "../../content/10-raw/02-catalogs/img/catalogue-composition.svg")
print(f"  longest bar ends at x={n(bx(4200))}, baseline y={n(BOT_RULE)}")
