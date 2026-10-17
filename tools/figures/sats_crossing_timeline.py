#!/usr/bin/env python3
"""Saturn's ring-plane crossings by the Sun and the Earth, 1995 to 2025.

A data figure. It plots only crossing dates quoted in the note:

* Sun crossings: 1995 Nov 19 (PDS Rings Node, RPX letter), 2009 Aug 10
  (NASA Photojournal PIA10563 and APOD 2009 August 25; Arlot and Thuillot
  2008 predicted Aug 12), 2025 May 6 (BAA 2025 apparition notes).
* Earth crossings: 1995 May 21, 1995 Aug 11, 1996 Feb 11 (RPX letter),
  2009 Sep 4 (Arlot and Thuillot 2008), 2025 Mar 23 (BAA notes).

The intervals between Sun crossings are computed from those dates.

    python tools/figures/sats_crossing_timeline.py
"""

import datetime as dt

from figlib import Figure, n


def year_frac(y, m, d):
    t = dt.date(y, m, d)
    s, e = dt.date(y, 1, 1), dt.date(y + 1, 1, 1)
    return y + (t - s).days / (e - s).days


SUN = [(1995, 11, 19), (2009, 8, 10), (2025, 5, 6)]
EARTH = [(1995, 5, 21), (1995, 8, 11), (1996, 2, 11), (2009, 9, 4), (2025, 3, 23)]

W, H = 760, 250
X0, X1 = 60.0, 720.0
Y0, Y1 = 1993.0, 2028.0
SUN_Y, EARTH_Y = 96.0, 156.0


def x(year):
    return X0 + (year - Y0) / (Y1 - Y0) * (X1 - X0)


f = Figure(
    W, H,
    title="Ring-plane crossings of Saturn by the Sun and the Earth, 1995 to 2025",
    desc=(
        "A horizontal time axis runs from 1993 to 2028 with ticks every five "
        "years. An upper row of circles marks the three Sun crossings in "
        "November 1995, August 2009 and May 2025. Brackets between them give "
        "the intervals, 13.72 years and 15.74 years. A lower row of diamonds "
        "marks the Earth crossings: three in 1995 and 1996, one in 2009 and "
        "one in 2025."
    ),
)

# axis
f.line(X0, 200, X1, 200, cls="axis")
for yr in range(1995, 2030, 5):
    f.line(x(yr), 200, x(yr), 206, cls="tick")
    f.text(x(yr), 222, str(yr), anchor="middle", cls="label-dim")

f.text(X0 - 6, SUN_Y + 4, "Sun", anchor="end", cls="label")
f.text(X0 - 6, EARTH_Y + 4, "Earth", anchor="end", cls="label")
f.line(X0, SUN_Y, X1, SUN_Y, cls="rule thin dotted")
f.line(X0, EARTH_Y, X1, EARTH_Y, cls="rule thin dotted")

sun_years = [year_frac(*d) for d in SUN]
for (yy, mm, dd), yf in zip(SUN, sun_years):
    f.circle(x(yf), SUN_Y, 6, cls="accent-fill")
    f.text(x(yf), SUN_Y + 22, f"{yy}-{mm:02d}-{dd:02d}", anchor="middle", cls="label-dim")

for (yy, mm, dd) in EARTH:
    yf = year_frac(yy, mm, dd)
    cx = x(yf)
    f.polygon([(cx, EARTH_Y - 6), (cx + 6, EARTH_Y), (cx, EARTH_Y + 6), (cx - 6, EARTH_Y)],
              cls="accent-2-fill")

# intervals between Sun crossings
for a, b in zip(sun_years, sun_years[1:]):
    xa, xb = x(a), x(b)
    f.line(xa, SUN_Y - 22, xb, SUN_Y - 22, cls="accent")
    f.line(xa, SUN_Y - 28, xa, SUN_Y - 16, cls="accent")
    f.line(xb, SUN_Y - 28, xb, SUN_Y - 16, cls="accent")
    f.text((xa + xb) / 2, SUN_Y - 30, f"{b - a:.2f} years", anchor="middle",
           cls="label-accent")

f.text((x(sun_years[0]) + x(sun_years[2])) / 2, 30,
       f"two intervals sum to {sun_years[2] - sun_years[0]:.2f} years, about one Saturnian year",
       anchor="middle", cls="label-em")
f.text(8, H - 6, "Data figure. Circles: Sun crossings (Saturnian equinoxes). "
       "Diamonds: Earth crossings.", cls="label-dim")

f.save(__file__, "../../content/10-raw/16-saturn-and-outer-satellites/img/sats-crossing-timeline.svg")
print("  intervals", [n(b - a) for a, b in zip(sun_years, sun_years[1:])])
