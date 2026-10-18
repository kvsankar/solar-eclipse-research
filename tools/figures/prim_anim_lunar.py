#!/usr/bin/env python3
"""Animated: the Moon passing through the Earth's shadow (spec FIG-3). The
still frame is totality, the Moon inside the umbra and reddened. The accent
colour stands for the reddening because it is copper-coloured in both
themes. The SMIL elements wait for a play event. Schematic only."""

from figlib import Figure

DUR = "12s"
f = Figure(
    width=680, height=280,
    title="The Moon passing through the Earth's shadow",
    desc=("The Earth's shadow at the Moon's distance, seen face on: a dark "
          "inner disc, the umbra, inside a paler ring, the penumbra. The "
          "Moon sits in the middle of the umbra, tinted copper. When played, "
          "the Moon moves from left to right through the penumbra and the "
          "umbra and out again, its copper tint deepening inside the umbra "
          "and fading outside it."),
)

cx, cy = 340, 135
f.circle(cx, cy, 95, cls="cone")
f.circle(cx, cy, 58, cls="cone-deep")
f.circle(cx, cy, 95, cls="rule thin dashed")
f.circle(cx, cy, 58, cls="rule thin")
f.line(40, cy + 10, 640, cy + 10, cls="rule thin dotted")
f.text(cx, cy - 64, "the Earth's umbra", anchor="middle", cls="label-dim")
f.text(cx, cy - 100, "the Earth's penumbra", anchor="middle", cls="label-dim")

# Positions run from dx = -300 to +300 over the animation. The Moon (radius 22)
# touches the penumbra at |dx| = 117, the umbra at |dx| = 80, and is wholly
# inside the umbra for |dx| <= 36.
times = "0;0.305;0.367;0.44;0.56;0.633;0.695;1"
tints = "0;0;0.2;0.8;0.8;0.2;0;0"
f.raw(
    f'<g><circle cx="{cx}" cy="{cy + 10}" r="22" class="body"/>'
    f'<text x="{cx}" y="{cy + 50}" text-anchor="middle" class="label">Darkened body</text>'
    f'<text x="{cx}" y="{cy + 64}" text-anchor="middle" class="label-dim">the Moon</text>'
    f'<circle cx="{cx}" cy="{cy + 10}" r="22" class="accent-fill" opacity="0.8">'
    f'<animate attributeName="opacity" values="{tints}" keyTimes="{times}" '
    f'dur="{DUR}" begin="indefinite" repeatCount="indefinite"/></circle>'
    f'<animateTransform attributeName="transform" type="translate" '
    f'values="-300 0;300 0" dur="{DUR}" begin="indefinite" repeatCount="indefinite"/></g>'
)
f.text(10, 20, "Light source", cls="label")
f.text(10, 34, "the Sun, behind the Earth", cls="label-dim")
f.text(10, 54, "Blocking body", cls="label")
f.text(10, 68, "the Earth, casting this shadow", cls="label-dim")
f.text(670, 20, "Observer", anchor="end", cls="label")
f.text(670, 34, "anyone on the Earth's night side", anchor="end", cls="label-dim")
f.text(cx, 272, "Still frame: totality. The Moon is in the umbra and lit only by sunlight "
       "bent through the Earth's atmosphere.", anchor="middle", cls="label-dim")
f.text(670, 250, "Schematic, not to scale", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/anim-lunar-eclipse.svg")
