#!/usr/bin/env python3
"""Animated: the Moon's shadow crossing the Earth, linked to what one
observer sees (spec FIG-3). The still frame is mid-eclipse: the umbra on the
observer and the Sun covered. The SMIL elements wait for a play event
(begin="indefinite"), so nothing moves until the reader presses Play.
Schematic only."""

from figlib import Figure, n

DUR = "10s"
f = Figure(
    width=680, height=290,
    title="The Moon's shadow crossing the Earth, and what one observer sees",
    desc=("Left: the Earth's disc with the Moon's shadow on it, a wide pale "
          "penumbra around a small dark umbra, centred on an observer marked "
          "with a dot. Right: the observer's sky, with the Sun covered by "
          "the Moon. When played, the shadow slides across the Earth from "
          "left to right while, on the right, the Moon slides across the Sun, "
          "covering it fully only while the umbra is on the observer."),
)

ex, ey, er = 170, 140, 105
# The sky offset of the Moon is K times the shadow's offset on the Earth, and
# the radii are chosen so the two panels agree: the discs first touch when
# the penumbra's edge reaches the observer (R_P * K = SUN + MOON), and the
# Sun is covered while the umbra is on the observer (R_U * K = MOON - SUN).
K = 1.5
SUN, MOON = 39, 48
R_P = (SUN + MOON) / K       # 58
R_U = (MOON - SUN) / K       # 6
TRAVEL = 220                 # the shadow's offset at the start and end
f.raw(f'<defs><clipPath id="earth"><circle cx="{ex}" cy="{ey}" r="{er}"/></clipPath>'
      f'<clipPath id="sky"><rect x="360" y="20" width="300" height="240"/></clipPath></defs>')
f.circle(ex, ey, er, cls="body")
f.raw(
    f'<g clip-path="url(#earth)"><g>'
    f'<circle cx="{ex}" cy="{ey}" r="{n(R_P)}" class="cone"/>'
    f'<circle cx="{ex}" cy="{ey}" r="{n(R_U)}" class="cone-deep"/>'
    f'<animateTransform attributeName="transform" type="translate" '
    f'values="{-TRAVEL} {-TRAVEL * 0.2};{TRAVEL} {TRAVEL * 0.2}" dur="{DUR}" '
    f'begin="indefinite" repeatCount="indefinite"/>'
    f'</g></g>'
)
f.circle(ex, ey, er, cls="rule")
f.circle(ex, ey, 3.5, cls="accent-2-fill")
f.text(ex, ey + er + 22, "The Moon's shadow on the Earth", anchor="middle", cls="label")
f.text(ex + 8, ey - 8, "observer", cls="label-dim")

sx, sy = 510, 140
f.circle(sx, sy, SUN + 14, cls="accent thin dotted")
f.circle(sx, sy, SUN, cls="accent-fill")
f.raw(
    f'<g clip-path="url(#sky)"><circle cx="{sx}" cy="{sy}" r="{MOON}" class="sky-fill">'
    f'<animate attributeName="cx" values="{sx + TRAVEL * K};{sx - TRAVEL * K}" dur="{DUR}" '
    f'begin="indefinite" repeatCount="indefinite"/>'
    f'<animate attributeName="cy" values="{sy + TRAVEL * 0.2 * K};{sy - TRAVEL * 0.2 * K}" dur="{DUR}" '
    f'begin="indefinite" repeatCount="indefinite"/></circle></g>'
)
f.text(sx, sy + er + 22, "What the observer sees", anchor="middle", cls="label")
f.text(sx, sy + er + 37, "still frame: the Sun covered, totality", anchor="middle", cls="label-dim")
f.text(670, 16, "Schematic, not to scale", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/anim-solar-eclipse.svg")
