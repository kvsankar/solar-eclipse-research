#!/usr/bin/env python3
"""Shared drawing for the three case diagrams (spec FIG-1, item 1).

Not a figure itself: prim_case_darkened.py, prim_case_hidden.py and
prim_case_both.py each import it and save one SVG. Every body carries two
labels, its role and its name. Schematic only.
"""

from figlib import Figure

W, H = 680, 250
AXIS = 112


def new(title: str, desc: str) -> Figure:
    f = Figure(width=W, height=H, title=title, desc=desc)
    f.text(W - 10, H - 8, "Schematic, not to scale", anchor="end", cls="label-dim")
    return f


def labels(f: Figure, x: float, y: float, role: str, name: str, extra: str = "",
           anchor: str = "middle") -> None:
    """The role on the first line, the name on the second, an optional third."""
    f.text(x, y, role, anchor=anchor, cls="label")
    f.text(x, y + 15, name, anchor=anchor, cls="label-dim")
    if extra:
        f.text(x, y + 30, extra, anchor=anchor, cls="label-dim")


def sun(f: Figure, x: float, y: float, r: float) -> None:
    f.circle(x, y, r, cls="sun-fill")
