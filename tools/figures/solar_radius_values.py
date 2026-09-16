#!/usr/bin/env python3
"""The measured solar radius, in arcseconds at 1 au, with its uncertainties.

A data figure. Every value and every uncertainty is quoted from the note
`content/10-raw/06-solar-radius/solar-radius-values.md`, which cites the
source for each one. Nothing is interpolated and nothing is averaged here.

    python tools/figures/solar_radius_values.py
"""

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 400
PL, PR = 244.0, 664.0          # plot area in x
NAME_X = 8.0
VALUE_X = 236.0
AXIS_Y = 336.0

X_MIN, X_MAX = 959.08, 960.22

# Each row: name, printed value, centre, +/- uncertainty or None, range or None
STANDARDS = [
    ("Auwers 1891", "959.63 ± 0.05", 959.63, 0.05, None),
    ("IAU 2015 nominal", "959.22", 959.22, None, None),
]
ECLIPSE = [
    ("Kubo 1993", "959.74 to 959.88", None, None, (959.74, 959.88)),
    ("Adassuriya 2011", "959.89 ± 0.18", 959.89, 0.18, None),
    ("Quaglia 2021", "959.95 ± 0.05", 959.95, 0.05, None),
    ("Jubier 2021", "959.98", 959.98, None, None),
    ("Lamy 2015", "959.99 ± 0.06", 959.99, 0.06, None),
    ("Guhl 2023", "960.01", 960.01, None, None),
]

CLUSTER = (959.95, 960.01)     # where the modern eclipse values fall


def gx(v: float) -> float:
    return PL + (v - X_MIN) / (X_MAX - X_MIN) * (PR - PL)


f = Figure(
    W, H,
    title="Solar radius values in arcseconds at 1 au, with uncertainties",
    desc=(
        "A dot chart on a horizontal axis running from 959.1 to 960.2 "
        "arcseconds. Two standards are drawn as open squares: Auwers 1891 at "
        "959.63 with an error bar of plus or minus 0.05, and the IAU 2015 "
        "nominal radius at 959.22 with no error bar. Six eclipse "
        "determinations are drawn below them as filled circles: Kubo's range "
        "of 959.74 to 959.88 as a bar, Adassuriya 959.89 plus or minus 0.18, "
        "Quaglia 959.95 plus or minus 0.05, Jubier 959.98, Lamy 959.99 plus "
        "or minus 0.06 and Guhl 960.01. A dashed vertical line at 959.63 "
        "marks the standard still in use, and a shaded band from 959.95 to "
        "960.01 shows that the modern eclipse values cluster about a third of "
        "an arcsecond above it."
    ),
)

rows: list[tuple[str, str, float | None, float | None,
                 tuple[float, float] | None, float, bool]] = []
y = 74.0
rows_heading: list[tuple[float, str]] = []

rows_heading.append((y, "Standards in use, drawn as open squares"))
y += 22
for name, printed, centre, err, rng in STANDARDS:
    rows.append((name, printed, centre, err, rng, y, True))
    y += 26

y += 12
rows_heading.append((y, "Eclipse determinations, drawn as filled circles"))
y += 22
for name, printed, centre, err, rng in ECLIPSE:
    rows.append((name, printed, centre, err, rng, y, False))
    y += 26

TOP_Y = 66.0

# --- the cluster band and the standard line -------------------------------
f.rect(gx(CLUSTER[0]), TOP_Y, gx(CLUSTER[1]) - gx(CLUSTER[0]),
       AXIS_Y - TOP_Y, cls="cone")
f.line(gx(959.63), TOP_Y, gx(959.63), AXIS_Y, cls="accent dashed")

# --- the axis -------------------------------------------------------------
f.line(PL, AXIS_Y, PR, AXIS_Y, cls="rule thin")
for v in (959.2, 959.4, 959.6, 959.8, 960.0, 960.2):
    f.line(gx(v), AXIS_Y, gx(v), AXIS_Y + 5, cls="rule thin")
    f.text(gx(v), AXIS_Y + 18, f"{v:.1f}", anchor="middle", cls="tick")
f.text((PL + PR) / 2, AXIS_Y + 36,
       "solar angular semidiameter at 1 au, arcseconds",
       anchor="middle", cls="label-dim")

# --- the rows -------------------------------------------------------------
for ry, heading in rows_heading:
    f.text(NAME_X, ry, heading, cls="label")

for name, printed, centre, err, rng, ry, is_standard in rows:
    f.text(NAME_X, ry + 4, name, cls="label")
    f.text(VALUE_X, ry + 4, printed, anchor="end", cls="tick")
    if rng is not None:
        f.line(gx(rng[0]), ry, gx(rng[1]), ry, cls="accent-2")
        for edge in rng:
            f.line(gx(edge), ry - 5, gx(edge), ry + 5, cls="accent-2")
        continue
    if err is not None:
        f.line(gx(centre - err), ry, gx(centre + err), ry,
               cls="accent" if is_standard else "accent-2")
        for edge in (centre - err, centre + err):
            f.line(gx(edge), ry - 5, gx(edge), ry + 5,
                   cls="accent" if is_standard else "accent-2")
    if is_standard:
        f.rect(gx(centre) - 4.5, ry - 4.5, 9, 9, cls="accent")
    else:
        f.circle(gx(centre), ry, 4.5, cls="accent-2-fill")

# --- annotations ----------------------------------------------------------
f.text(gx(959.63) - 6, TOP_Y - 26, "959.63″, the standard",
       anchor="end", cls="label-accent")
f.text(gx(959.63) - 6, TOP_Y - 14, "still in use", anchor="end",
       cls="label-accent")
band_mid = (gx(CLUSTER[0]) + gx(CLUSTER[1])) / 2
f.text(band_mid, TOP_Y - 26, "the eclipse values", anchor="middle", cls="label")
f.text(band_mid, TOP_Y - 14, "cluster here", anchor="middle", cls="label")

f.text(NAME_X, H - 10,
       "The eclipse values measure the last photospheric light, about 0.32 "
       "arcseconds beyond Auwers' 19th-century limb.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/06-solar-radius/img/solar-radius-values.svg")
print(f"  rows {len(rows)}  axis {n(gx(X_MIN))}..{n(gx(X_MAX))}  "
      f"last row y={n(rows[-1][5])}")
