#!/usr/bin/env python3
"""The light path from a source to an observer, and the three places a body
can cut it (spec FIG-1, item 1). Schematic only: no positions are computed."""

from figlib import Figure

f = Figure(
    width=680, height=330,
    title="Three places a body can cut the light path",
    desc=("A light source on the left sends light along three straight legs: "
          "to a body at the top that reflects it, from that body down to an "
          "observer on the right, and straight from the source to the "
          "observer. A small dark disc sits on each leg, numbered 1 to 3, "
          "with a short label saying what an observer notices when a body "
          "cuts that leg."),
)

src = (80, 190)
lit = (360, 62)
obs = (610, 220)

f.line(*src, *lit, cls="accent")
f.line(*lit, *obs, cls="accent-2")
f.line(*src, *obs, cls="accent dashed")

f.circle(*src, 38, cls="body")
f.text(src[0], src[1] + 58, "Source", anchor="middle", cls="label")
f.text(src[0], src[1] + 73, "the Sun, or a star", anchor="middle", cls="label-dim")
f.circle(*lit, 18, cls="body")
f.text(lit[0], lit[1] - 26, "A body lit by the source", anchor="middle", cls="label")
f.circle(*obs, 22, cls="body")
f.text(obs[0], obs[1] + 40, "Observer", anchor="middle", cls="label")


def cut(p, q, t, number, lines, dx, dy):
    x = p[0] + (q[0] - p[0]) * t
    y = p[1] + (q[1] - p[1]) * t
    f.circle(x, y, 11, cls="body")
    f.text(x, y + 4, number, anchor="middle", cls="label")
    for i, line in enumerate(lines):
        f.text(x + dx, y + dy + 15 * i, line, anchor="start" if number != "1" else "end",
               cls="label" if i == 0 else "label-dim")


cut(src, lit, 0.5, "1", ["Darkened", "the lit body goes dark", "for everyone"], -20, -40)
cut(lit, obs, 0.45, "2", ["Hidden", "the observer loses", "sight of the lit body"], 18, -24)
cut(src, obs, 0.5, "3", ["Both", "the observer stands in a shadow", "and sees the source hidden"], -60, 32)

f.text(670, 318, "Schematic, not to scale", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/light-path.svg")
