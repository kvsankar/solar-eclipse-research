#!/usr/bin/env python3
"""The four eclipse types as four cross-sections.

One quantity separates them: where the vertex of the umbral cone falls
relative to the Earth's surface. The Moon is drawn at a different distance in
each panel, which is the physical cause, and the drawn cone half-angle is the
same in all four.

Everything is exaggerated: the cone half-angle, the Moon's size, and the
spread of the Moon's distance. The real vertex falls within a few hundred
kilometres of the surface either way. The figure says so on its face.

    cd tools/figures && python eclipse_types.py
"""

import math

from figlib import Figure, n

# --- layout ---------------------------------------------------------------
W, H = 700, 360
PANEL = W / 4.0                    # 175

EARTH_CY, EARTH_R = 270.0, 60.0    # the Earth's centre and radius, in pixels
CLIP_TOP, CLIP_BOT = 26.0, 280.0

MOON_R = 18.0
SLOPE = 0.19                       # drawn cone half-angle, exaggerated
CONE_LEN = MOON_R / SLOPE          # Moon centre to umbral vertex, 94.7 px

LABEL_Y = (300.0, 315.0, 327.0, 339.0)

# For the hybrid panel the Moon's distance is not chosen by eye. It is solved
# so that the arc of constant vertex distance crosses the Earth's surface at
# this angle from the sub-lunar point, which is what puts the total stretch in
# the middle of the path and the annular stretches at its ends.
HYBRID_CROSS_DEG = 48.0


def surface_y(dx: float) -> float:
    """Height of the Earth's surface at a horizontal offset from the axis."""
    return EARTH_CY - math.sqrt(max(EARTH_R * EARTH_R - dx * dx, 0.0))


def hybrid_moon_y(cross_deg: float) -> float:
    """Moon height putting the vertex-distance arc across the surface.

    The vertex sits CONE_LEN from the Moon's centre, so the set of points as
    far from the Moon as the vertex is a circle of that radius. Solving for
    the Moon's distance d that places a surface point at `cross_deg` from the
    sub-lunar point exactly on that circle:

        (d - R cos T)^2 + (R sin T)^2 = CONE_LEN^2
    """
    t = math.radians(cross_deg)
    d = EARTH_R * math.cos(t) + math.sqrt(
        CONE_LEN * CONE_LEN - (EARTH_R * math.sin(t)) ** 2)
    return EARTH_CY - d


f = Figure(
    W, H,
    title="Partial, annular, total and hybrid eclipses",
    desc=(
        "Four cross-sections side by side, each with the Moon above and the "
        "curved surface of the Earth below. In the first the shadow axis "
        "passes clear of the Earth and only the penumbra lands, giving a "
        "partial eclipse. In the second the Moon is far away, the umbral cone "
        "closes to a vertex above the surface, and the widening antumbra "
        "reaches the ground, giving an annular eclipse. In the third the Moon "
        "is close, the vertex falls below the surface, and the umbra itself "
        "reaches the ground, giving a total eclipse. In the fourth a dashed "
        "arc marks every point as far from the Moon as the vertex is. The "
        "curved surface of the Earth crosses that arc twice. The middle of "
        "the surface lies inside the arc, nearer the Moon than the vertex, so "
        "the umbra reaches it and the eclipse is total there; beyond the two "
        "crossings the surface falls outside the arc, the vertex is short of "
        "the ground, and the eclipse is annular."
    ),
)


def panel(index: int, moon_dx: float, moon_y: float, bot: float, name: str,
          lines: tuple, mark_hybrid: bool = False) -> None:
    cx = PANEL * index + PANEL / 2.0
    mx = cx + moon_dx
    vy = moon_y + CONE_LEN
    sub = surface_y(moon_dx)
    on_axis = abs(moon_dx) < EARTH_R
    start = len(f.parts)

    # penumbra: widening from the Moon's limb
    pen_half = MOON_R + SLOPE * (bot - moon_y)
    f.polygon([(mx - MOON_R, moon_y), (mx - pen_half, bot),
               (mx + pen_half, bot), (mx + MOON_R, moon_y)], cls="cone")

    # umbra: the converging cone down to the vertex
    f.polygon([(mx - MOON_R, moon_y), (mx, vy), (mx + MOON_R, moon_y)],
              cls="cone-deep")

    # antumbra: the same two lines continued past the vertex
    if vy < bot:
        anti = SLOPE * (bot - vy)
        f.polygon([(mx, vy), (mx - anti, bot), (mx + anti, bot)], cls="cone")
        f.line(mx, vy, mx - anti, bot, cls="axis thin dotted")
        f.line(mx, vy, mx + anti, bot, cls="axis thin dotted")

    f.line(mx - MOON_R, moon_y, mx, vy, cls="axis thin")
    f.line(mx + MOON_R, moon_y, mx, vy, cls="axis thin")
    f.line(mx, moon_y, mx, sub if on_axis else bot, cls="axis dashed")

    # the Earth, opaque, drawn over the cones
    hx = math.sqrt(EARTH_R * EARTH_R - (CLIP_BOT - EARTH_CY) ** 2)
    f.path(f"M {n(cx - hx)} {n(CLIP_BOT)}"
           f" A {n(EARTH_R)} {n(EARTH_R)} 0 0 1 {n(cx + hx)} {n(CLIP_BOT)} Z",
           cls="body")

    f.circle(mx, moon_y, MOON_R, cls="body")

    # where the vertex falls below the surface, redraw the last stretch of
    # the cone over the Earth, so the reader can see it get there
    if on_axis and vy > sub:
        half = MOON_R * (vy - sub) / CONE_LEN
        f.line(mx - half, sub, mx, vy, cls="accent-2 thin dotted")
        f.line(mx + half, sub, mx, vy, cls="accent-2 thin dotted")
        f.line(mx, sub, mx, vy, cls="axis dashed")
    if on_axis:
        f.circle(mx, vy, 3, cls="accent-2-fill")
        if mark_hybrid:
            f.text(mx, vy + 15, "vertex", anchor="middle", cls="label-dim")
        else:
            f.text(mx + 8, vy + 4, "vertex", cls="label-dim")

    if mark_hybrid:
        # Every point on this arc is exactly as far from the Moon as the
        # vertex. Inside it the ground is nearer than the vertex and the umbra
        # lands; outside it the vertex is short and the antumbra lands. Drawing
        # the criterion is what makes the A-T-A pattern something the reader
        # can check rather than something the caption asserts.
        t = math.radians(HYBRID_CROSS_DEG)
        kx, ky = EARTH_R * math.sin(t), EARTH_CY - EARTH_R * math.cos(t)
        span = math.radians(HYBRID_CROSS_DEG + 10.0)
        ax, ay = CONE_LEN * math.sin(span), moon_y + CONE_LEN * math.cos(span)
        f.path(f"M {n(mx - ax)} {n(ay)}"
               f" A {n(CONE_LEN)} {n(CONE_LEN)} 0 0 0 {n(mx + ax)} {n(ay)}",
               cls="accent-2 thin dashed")
        for sx in (-1.0, 1.0):
            f.circle(mx + sx * kx, ky, 2.2, cls="accent-2-fill")

        # Off the axis: the shadow axis and the umbra's last stretch are drawn
        # down the middle of the cap, and a letter sitting on them is unreadable.
        f.text(cx - 15.0, surface_y(-15.0) + 14, "T",
               anchor="middle", cls="label-em")
        for sx in (-1.0, 1.0):
            ax_lab = sx * (kx + 9.0)
            f.text(cx + ax_lab, surface_y(ax_lab) + 11, "A",
                   anchor="middle", cls="label-em")

    body = "".join(f.parts[start:])
    del f.parts[start:]
    f.raw(f'<defs><clipPath id="etp{index}">'
          f'<rect x="{n(PANEL * index)}" y="{n(CLIP_TOP)}"'
          f' width="{n(PANEL)}" height="{n(CLIP_BOT - CLIP_TOP)}"/>'
          f"</clipPath></defs>")
    f.group(body, extra=f'clip-path="url(#etp{index})"')

    f.text(cx, LABEL_Y[0], name, anchor="middle", cls="label")
    for i, line in enumerate(lines):
        f.text(cx, LABEL_Y[1 + i], line, anchor="middle", cls="label-dim")


panel(0, -66.0, 95.0, 230.0, "Partial",
      ("the axis misses the Earth", "only the penumbra lands"))
panel(1, 0.0, 60.0, CLIP_BOT, "Annular",
      ("vertex short of the surface", "antumbra reaches the ground"))
panel(2, 0.0, 155.0, CLIP_BOT, "Total",
      ("vertex beyond the surface", "the umbra reaches the ground"))
panel(3, 0.0, hybrid_moon_y(HYBRID_CROSS_DEG), CLIP_BOT, "Hybrid",
      ("the surface crosses the", "vertex distance: total (T) inside,",
       "annular (A) beyond"), mark_hybrid=True)

for i in (1, 2, 3):
    f.line(PANEL * i, CLIP_TOP + 6, PANEL * i, CLIP_BOT, cls="rule thin dotted")

f.text(8, H - 8,
       "Schematic. The cone angle, the Moon's size and the spread of its "
       "distance are exaggerated; the real vertex falls near the surface.",
       cls="label-dim")

f.save(__file__, "../../content/10-raw/02-catalogs/img/eclipse-types.svg")
