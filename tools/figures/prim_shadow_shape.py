#!/usr/bin/env python3
"""The shape of a shadow: the cone an extended source casts, with its umbra,
penumbra and antumbra and what an observer in each sees, beside the cylinder a
point source casts (spec FIG-1, item 2). Schematic only."""

from figlib import Figure

f = Figure(
    width=680, height=480,
    title="Cone and cylinder: the two shapes of a shadow",
    desc=("Top: a large source disc on the left and a small body in the "
          "middle. The umbra narrows behind the body to a point and opens "
          "out again beyond it as the antumbra. The wider penumbra spreads "
          "around both. Three observers sit in the umbra, the penumbra and "
          "the antumbra, each linked to a small inset of the source disc: "
          "wholly covered, partly covered, and covered except for a ring. "
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
f.circle(sx, cy, sr, cls="body")
f.text(sx, cy + sr + 18, "Extended source", anchor="middle", cls="label")
f.text(sx, cy + sr + 32, "the Sun", anchor="middle", cls="label-dim")
f.circle(bx, cy, br, cls="body")
f.text(bx, cy - br - 12, "Body", anchor="middle", cls="label")
f.text((bx + vx) / 2 - 10, cy + 4, "umbra", anchor="middle", cls="label")
f.text(600, cy + 4, "antumbra", anchor="middle", cls="label")
f.text(560, cy - inner(560) + 18, "penumbra", anchor="middle", cls="label")


def observer(x, y, kind, label, ix, iy):
    f.circle(x, y, 4, cls="accent-fill")
    f.line(x, y + 5, ix, iy - 18, cls="accent thin dotted")
    f.circle(ix, iy, 15, cls="accent-fill")     # the source as seen
    if kind == "total":
        f.circle(ix, iy, 16, cls="sky-fill")
    elif kind == "annular":
        f.circle(ix, iy, 10.5, cls="sky-fill")
    elif kind == "partial":
        f.circle(ix + 12, iy - 6, 15, cls="sky-fill")
    f.text(ix, iy + 32, label, anchor="middle", cls="label")


observer(vx - 22, cy, "total", "umbra: total", 330, 280)
observer(500, cy + 40, "partial", "penumbra: partial", 470, 280)
observer(620, cy + 10, "annular", "antumbra: annular", 610, 280)

# ---- bottom: point source --------------------------------------------------
f.line(20, 335, 660, 335, cls="rule thin dashed")
by = 400
for dy in (-36, -18, 18, 36):
    f.line(20, by + dy, bx - 30, by + dy, cls="accent thin", marker="arrow")
f.rect(bx, by - br, x_end - bx, 2 * br, cls="cone-deep")
f.line(bx, by - br, x_end, by - br, cls="rule thin")
f.line(bx, by + br, x_end, by + br, cls="rule thin")
f.circle(bx, by, br, cls="body")
f.text(20, by + 62, "Star: a point at infinity, so its light arrives in parallel lines",
       cls="label")
f.text(470, by - 26, "cylinder: no penumbra", anchor="middle", cls="label")
f.circle(610, by, 4, cls="accent-fill")
f.text(610, by + 34, "star hidden", anchor="middle", cls="label-dim")

f.text(670, 474, "Schematic, not to scale", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/shadow-shape.svg")
