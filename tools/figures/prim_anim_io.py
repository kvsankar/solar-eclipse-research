#!/usr/bin/env python3
"""Animated: one orbit of Io seen from above, with the four places where it
is eclipsed, occulted, in transit, and casting its shadow on Jupiter (spec
FIG-3). The still frame shows Io in Jupiter's shadow. The angle between the
directions to the Sun and to the Earth is exaggerated so the four places
separate. The SMIL element waits for a play event. Schematic only."""

import math

from figlib import Figure, n

DUR = "14s"
PANEL = 200       # width added for the "What the observer sees" panel (FIG-12)
f = Figure(
    width=680 + PANEL, height=372,
    title="One orbit of Io: four kinds of event",
    desc=("A view from above Jupiter. Sunlight comes from the left, so "
          "Jupiter's shadow is a band to its right. The Earth lies off to the "
          "lower left, so Jupiter hides a band behind it to the upper right "
          "as seen from the Earth. Io's orbit is a dashed circle with four "
          "labelled places: on the Sun side its shadow falls on Jupiter; on "
          "the Earth side it crosses in front of Jupiter; behind Jupiter as "
          "seen from the Earth it is occulted; in the shadow it is eclipsed. "
          "Io sits in the shadow at the still frame. When played, Io goes "
          "round the orbit. A framed panel on the right shows what an "
          "observer on the Earth sees: Jupiter's disc with Io beside it, "
          "crossing in front, hidden behind or dark in the shadow, and "
          "Io's shadow as a dot on Jupiter, with the event's name lit."),
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
f.text(jx, jy - 2, "Jupiter", anchor="middle", cls="label")
f.text(jx, jy + 12, "the planet", anchor="middle", cls="label-dim")

# Directions.
f.line(110, 34, 40, 34, cls="accent", marker="arrow")
f.text(118, 32, "Light source", cls="label")
f.text(118, 46, "the Sun, this way", cls="label-dim")
f.line(jx + ex * 150, jy + ey * 150, jx + ex * 230, jy + ey * 230, cls="accent-2", marker="arrow")
f.text(jx + ex * 236 + 4, jy + ey * 236 + 16, "Observer", anchor="middle", cls="label")
f.text(jx + ex * 236 + 4, jy + ey * 236 + 30, "on the Earth, this way", anchor="middle", cls="label-dim")


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
    f'<g transform="translate({n(jx + orbit)} {jy})">'
    f'<circle cx="0" cy="0" r="8" class="body"/><circle cx="0" cy="0" r="8" class="rule"/>'
    f'<text x="0" y="-14" text-anchor="middle" class="label">Io</text>'
    f'<animateMotion path="M0,0 A{orbit},{orbit} 0 1 0 {-2 * orbit},0 A{orbit},{orbit} 0 1 0 0,0" '
    f'dur="{DUR}" begin="indefinite" repeatCount="indefinite"/></g>'
)
# ---- What the observer sees (FIG-12) --------------------------------------
# The same orbit, seen from the Earth. Everything lies in the orbit's plane,
# so the view is edge-on: Io moves along a line across Jupiter's equator.
# sky is the position across the view, depth the distance towards the Earth.
N = 144
qx, qy = ey, -ex                          # across the view, as seen from the Earth
PX, PY, PW, PH = 692, 30, 176, 214
vx, vy = PX + PW / 2, 128
S = 0.62                                  # panel pixels per drawing pixel


def frame(k):
    a = 2 * math.pi * k / N
    rx, ry = orbit * math.cos(a), -orbit * math.sin(a)
    sky, depth = rx * qx + ry * qy, rx * ex + ry * ey
    behind = depth < 0 and abs(sky) < jr
    eclipsed = rx > 0 and abs(ry) < jr
    spot = None
    if rx < 0 and abs(ry) < jr:              # Io between the Sun and Jupiter
        gx, gy = -math.sqrt(jr * jr - ry * ry), ry
        if gx * ex + gy * ey > 0:             # on the face turned to the Earth
            spot = gx * qx + gy * qy
    return {
        "x": vx + S * sky, "lit": 0 if behind or eclipsed else 1,
        "dark": 1 if eclipsed and not behind else 0,
        "spot": spot,
        "transit": depth > 0 and abs(sky) < jr, "shadow transit": spot is not None,
        "occultation": behind, "eclipse": eclipsed and not behind,
    }


frames = [frame(k) for k in range(N + 1)]
keys = ";".join(n(k / N) for k in range(N + 1))


def anim(attr, vals, discrete=False):
    mode = ' calcMode="discrete"' if discrete else ""
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{keys}"{mode} '
            f'dur="{DUR}" begin="indefinite" repeatCount="indefinite"/>')


f.rect(PX, PY, PW, PH, cls="panel", rx=6)
f.text(vx, PY + 20, "What the observer sees", anchor="middle", cls="label")
f.text(vx, PY + 35, "from the Earth", anchor="middle", cls="label-dim")
f.circle(vx, vy, jr * S, cls="body")
f0 = frames[0]
spots = [fr["spot"] for fr in frames]
last = 0.0
spot_x = []
for sp in spots:
    last = sp if sp is not None else last
    spot_x.append(n(vx + S * last))
f.raw(f'<circle cx="{spot_x[0]}" cy="{vy}" r="2.6" class="silhouette-fill" opacity="0">'
      + anim("cx", spot_x) + anim("opacity", ["1" if sp is not None else "0" for sp in spots], True)
      + "</circle>")
xs = [n(fr["x"]) for fr in frames]
f.raw(f'<circle cx="{xs[0]}" cy="{vy}" r="4.5" class="body" opacity="{f0["lit"]}">'
      + anim("cx", xs) + anim("opacity", [str(fr["lit"]) for fr in frames], True) + "</circle>")
f.raw(f'<circle cx="{xs[0]}" cy="{vy}" r="4.5" class="silhouette-fill" opacity="{f0["dark"]}">'
      + anim("cx", xs) + anim("opacity", [str(fr["dark"]) for fr in frames], True) + "</circle>")
# The four events, each lit while it is happening.
for i, name in enumerate(("transit", "shadow transit", "occultation", "eclipse")):
    on = [fr[name] for fr in frames]
    f.raw(f'<g opacity="{1 if on[0] else 0.3}">'
          + anim("opacity", ["1" if o else "0.3" for o in on], True)
          + f'<text x="{n(vx)}" y="{n(PY + 132 + 18 * i)}" text-anchor="middle" '
          f'class="view-event label">{name}</text></g>')

f.text(670, 344, "Io and Jupiter swap roles from one event to the next.", anchor="end", cls="label-dim")
f.text(670 + PANEL, 362, "Schematic, not to scale; angles exaggerated", anchor="end", cls="label-dim")
f.save(__file__, "../../content/05-primer/img/anim-io-orbit.svg")
