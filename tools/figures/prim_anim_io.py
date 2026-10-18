#!/usr/bin/env python3
"""Animated: one orbit of Io seen from above, with the four places where it
is eclipsed, occulted, in transit, and casting its shadow on Jupiter (spec
FIG-3). The still frame shows Io in Jupiter's shadow. The angle between the
directions to the Sun and to the Earth is exaggerated so the four places
separate. The SMIL element waits for a play event. Schematic only."""

import math

from figlib import Figure, n

DUR = "14s"
f = Figure(
    width=680, height=370,
    title="One orbit of Io: four kinds of event",
    desc=("A view from above Jupiter. Sunlight comes from the left, so "
          "Jupiter's shadow is a band to its right. The Earth lies off to the "
          "lower left, so Jupiter hides a band behind it to the upper right "
          "as seen from the Earth. Io's orbit is a dashed circle with four "
          "labelled places: on the Sun side its shadow falls on Jupiter; on "
          "the Earth side it crosses in front of Jupiter; behind Jupiter as "
          "seen from the Earth it is occulted; in the shadow it is eclipsed. "
          "Io sits in the shadow at the still frame. When played, Io goes "
          "round the orbit."),
)

jx, jy, jr, orbit = 300, 185, 38, 122
ex, ey = -math.cos(math.radians(30)), math.sin(math.radians(30))  # towards the Earth

# Jupiter's shadow, away from the Sun.
f.rect(jx, jy - jr, 330, 2 * jr, cls="cone-deep")
f.text(560, jy - jr - 8, "Jupiter's shadow", anchor="middle", cls="label-dim")
# The band hidden behind Jupiter as seen from the Earth.
bx, by = -ex, -ey
px, py = -by, bx
far = 300
f.polygon([(jx + px * jr, jy + py * jr), (jx + px * jr + bx * far, jy + py * jr + by * far),
           (jx - px * jr + bx * far, jy - py * jr + by * far), (jx - px * jr, jy - py * jr)],
          cls="cone")
f.text(jx + bx * 210 + 34, jy + by * 210, "hidden from the Earth", cls="label-dim")

f.circle(jx, jy, orbit, cls="rule dashed")
f.circle(jx, jy, jr, cls="body")
f.text(jx, jy + 4, "Jupiter", anchor="middle", cls="label")

# Directions.
f.line(110, 34, 40, 34, cls="accent", marker="arrow")
f.text(118, 38, "to the Sun", cls="label")
f.line(jx + ex * 150, jy + ey * 150, jx + ex * 230, jy + ey * 230, cls="accent-2", marker="arrow")
f.text(jx + ex * 236 + 4, jy + ey * 236 + 18, "to the Earth", anchor="middle", cls="label")


def place(angle_deg, label, dx, dy, anchor):
    a = math.radians(angle_deg)
    x, y = jx + orbit * math.cos(a), jy - orbit * math.sin(a)
    f.circle(x, y, 3, cls="accent-2-fill")
    f.text(x + dx, y + dy, label, anchor=anchor, cls="label")


place(180, "shadow transit", -10, -10, "end")
place(210, "transit", -12, 18, "end")
place(30, "occultation", 10, -8, "start")
place(0, "eclipse", 12, 22, "start")

# Io, starting in the shadow, rotating once round Jupiter.
f.raw(
    f'<g><circle cx="{n(jx + orbit)}" cy="{jy}" r="8" class="body"/>'
    f'<circle cx="{n(jx + orbit)}" cy="{jy}" r="8" class="rule"/>'
    f'<text x="{n(jx + orbit)}" y="{jy - 14}" text-anchor="middle" class="label">Io</text>'
    f'<animateTransform attributeName="transform" type="rotate" '
    f'values="0 {jx} {jy};-360 {jx} {jy}" dur="{DUR}" begin="indefinite" '
    f'repeatCount="indefinite"/></g>'
)
f.text(670, 362, "Schematic, not to scale; angles exaggerated", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/anim-io-orbit.svg")
