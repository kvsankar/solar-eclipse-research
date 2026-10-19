#!/usr/bin/env python3
"""The shape of a shadow: the cone an extended source casts, with its umbra,
penumbra and antumbra and what an observer in each sees, beside the cylinder a
point source casts (spec FIG-1, item 2). Schematic only."""

from figlib import Figure
from prim_corona import corona

f = Figure(
    width=680, height=480,
    title="Cone and cylinder: the two shapes of a shadow",
    desc=("Top: a large source disc on the left and a small body in the "
          "middle. The umbra narrows behind the body to a point and opens "
          "out again beyond it as the antumbra. The wider penumbra spreads "
          "around both. Three observers sit in the umbra, the penumbra and "
          "the antumbra. A framed panel below shows what each one sees of the "
          "source disc: wholly covered with a faint corona around it, partly "
          "covered, and covered except for a ring. "
          "Bottom: parallel lines from a star at the far left pass a body "
          "and leave a straight band behind it, the cylinder, with an "
          "observer in it for whom the star is hidden."),
)

# ---- top: extended source --------------------------------------------------
cy = 140
sx, sr = 62, 40          # source
bx, br = 300, 16         # body
x_end = 660

vx = bx + br * (bx - sx) / (sr - br)      # umbral vertex
cx_ = sx + sr * (bx - sx) / (sr + br)     # where the inner tangents cross


def outer(x):
    return br * abs(vx - x) / (vx - bx)


def inner(x):
    return br * (x - cx_) / (bx - cx_)


pen = [(bx, cy - inner(bx)), (x_end, cy - inner(x_end)),
       (x_end, cy + inner(x_end)), (bx, cy + inner(bx))]
umb = [(bx, cy - br), (vx, cy), (bx, cy + br)]
ant = [(vx, cy), (x_end, cy - outer(x_end)), (x_end, cy + outer(x_end))]
f.polygon(pen, cls="cone")
f.polygon(umb, cls="cone-deep")
f.polygon(ant, cls="cone-deep")
f.polyline([pen[0], pen[1]], cls="rule thin dashed")
f.polyline([pen[3], pen[2]], cls="rule thin dashed")
f.polyline([umb[0], umb[1], ant[1]], cls="rule thin")
f.polyline([umb[2], umb[1], ant[2]], cls="rule thin")

# Tangent rays from the source's edges: outer ones bound the umbra, the
# crossing inner ones bound the penumbra.
for sgn in (-1, 1):
    f.line(sx, cy + sgn * sr, bx, cy + sgn * br, cls="rule thin")
    f.line(sx, cy + sgn * sr, bx, cy - sgn * br, cls="rule thin dashed")
f.circle(sx, cy, sr, cls="sun-fill")
f.text(sx, cy + sr + 18, "Light source", anchor="middle", cls="label")
f.text(sx, cy + sr + 32, "the Sun, a disc", anchor="middle", cls="label-dim")
f.circle(bx, cy, br, cls="body")
f.text(bx, cy - br - 26, "Blocking body", anchor="middle", cls="label")
f.text(bx, cy - br - 11, "the Moon", anchor="middle", cls="label-dim")
f.text((bx + vx) / 2 - 10, cy + 4, "umbra", anchor="middle", cls="label")
f.text(600, cy + 4, "antumbra", anchor="middle", cls="label")
f.text(560, cy - inner(560) + 18, "penumbra", anchor="middle", cls="label")


# What each observer sees, in a framed panel between the two halves (FIG-9).
PX, PY, PW, PH = 20, 248, 640, 96
f.rect(PX, PY, PW, PH, cls="panel", rx=6)
f.text(PX + 14, PY + 22, "What the observer sees", cls="label")


def on_world(x, y):
    """A small world behind an observer at (x, y), so they stand on it
    (spec FIG-11). The light comes from the left, so they face left."""
    f.circle(x + 8, y, 8, cls="body")
    f.circle(x, y, 4, cls="accent-fill observer")


def observer(x, y, kind, label, ix, iy):
    on_world(x, y)
    f.circle(ix, iy, 15, cls="sun-fill")        # the source as seen
    if kind == "total":
        corona(f, ix, iy, 15, "corona-shadow-shape")
        f.circle(ix, iy, 15, cls="silhouette-fill")
    elif kind == "annular":
        f.circle(ix, iy, 10.5, cls="silhouette-fill")
    elif kind == "partial":
        f.circle(ix + 12, iy - 6, 15, cls="silhouette-fill")
    f.text(ix, iy + 34, label, anchor="middle", cls="label-dim")


observer(vx - 22, cy, "total", "in the umbra: total", 270, 290)
observer(500, cy + 40, "partial", "in the penumbra: partial", 430, 290)
observer(620, cy + 10, "annular", "in the antumbra: annular", 590, 290)

# ---- bottom: point source --------------------------------------------------
f.line(20, 352, 660, 352, cls="rule thin dashed")
by = 398
for dy in (-22, -8, 8, 22):
    f.line(26, by + dy, 250, by + dy, cls="accent thin", marker="arrow")
f.rect(bx, by - br, x_end - bx, 2 * br, cls="cone-deep")
f.line(bx, by - br, x_end, by - br, cls="rule thin")
f.line(bx, by + br, x_end, by + br, cls="rule thin")
f.circle(bx, by, br, cls="body")
f.circle(14, by, 4, cls="sun-fill")
f.text(20, by + 44, "Light source", cls="label")
f.text(20, by + 58, "a star: a point at infinity, so its light arrives in parallel lines",
       cls="label-dim")
f.text(bx, by - br - 24, "Blocking body", anchor="middle", cls="label")
f.text(bx, by - br - 9, "the Moon", anchor="middle", cls="label-dim")
f.text(470, by - 26, "cylinder: no penumbra", anchor="middle", cls="label")
on_world(610, by)
f.text(610, by + 36, "Observer", anchor="middle", cls="label")
f.text(610, by + 50, "the star is hidden", anchor="middle", cls="label-dim")

f.text(670, 474, "Schematic, not to scale", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/shadow-shape.svg")
