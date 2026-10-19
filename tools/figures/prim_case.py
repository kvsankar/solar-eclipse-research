#!/usr/bin/env python3
"""Shared drawing for the three case diagrams (spec FIG-1, item 1).

Not a figure itself: prim_case_darkened.py, prim_case_hidden.py and
prim_case_both.py each import it and save one SVG. Every body carries two
labels, its role and its name. Schematic only.
"""

from figlib import Figure

W, H = 680, 250
AXIS = 112
PANEL_W = 190      # width added for a "What the observer sees" panel (FIG-9)


def new(title: str, desc: str, panel: bool = False) -> Figure:
    width = W + PANEL_W if panel else W
    f = Figure(width=width, height=H, title=title, desc=desc)
    f.text(width - 10, H - 8, "Schematic, not to scale", anchor="end", cls="label-dim")
    return f


def view_panel(f: Figure) -> tuple[float, float]:
    """The framed panel to the right of the main drawing (FIG-9). The ground
    rectangle ends the main drawing at its usual width, so a body that runs
    off the edge, such as the Earth, stops there. Returns the centre of the
    view."""
    f.rect(W, 0, PANEL_W, H, cls="panel-ground")
    x, y, w, h = W + 14, 22, PANEL_W - 24, 186
    f.rect(x, y, w, h, cls="panel", rx=6)
    f.text(x + w / 2, y + 20, "What the observer sees", anchor="middle", cls="label")
    return x + w / 2, y + h / 2 + 8


def labels(f: Figure, x: float, y: float, role: str, name: str, extra: str = "",
           anchor: str = "middle") -> None:
    """The role on the first line, the name on the second, an optional third."""
    f.text(x, y, role, anchor=anchor, cls="label")
    f.text(x, y + 15, name, anchor=anchor, cls="label-dim")
    if extra:
        f.text(x, y + 30, extra, anchor=anchor, cls="label-dim")


def sun(f: Figure, x: float, y: float, r: float) -> None:
    f.circle(x, y, r, cls="sun-fill")
