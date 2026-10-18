#!/usr/bin/env python3
"""Shared drawing for the three primer gallery figures (spec FIG-1, item 3).

Not a figure itself: prim_gallery_darkened.py, prim_gallery_hidden.py and
prim_gallery_both.py each import it and save one SVG. Schematic only.
"""

from figlib import Figure

W, H = 680, 250
PANEL = W / 3


def new(title: str, desc: str) -> Figure:
    f = Figure(width=W, height=H, title=title, desc=desc)
    for i in (1, 2):
        f.line(PANEL * i, 24, PANEL * i, H - 40, cls="rule thin dotted")
    f.text(W - 10, H - 8, "Schematic, not to scale", anchor="end", cls="label-dim")
    return f


def caption(f: Figure, i: int, title: str, lines: list[str]) -> None:
    x = PANEL * i + PANEL / 2
    f.text(x, 22, title, anchor="middle", cls="label")
    for k, line in enumerate(lines):
        f.text(x, H - 58 + 14 * k, line, anchor="middle", cls="label-dim")


def sun(f: Figure, x: float, y: float, r: float = 13) -> None:
    f.circle(x, y, r, cls="accent-fill")


def cone(f: Figure, x0: float, y: float, r0: float, x1: float, r1: float) -> None:
    """A shadow from a body of radius r0 at x0, narrowing to half-width r1 at x1."""
    f.polygon([(x0, y - r0), (x1, y - r1), (x1, y + r1), (x0, y + r0)], cls="cone-deep")


def eye(f: Figure, x: float, y: float, tx: float, ty: float) -> None:
    """The observer, with a dotted line of sight to (tx, ty)."""
    f.line(x, y, tx, ty, cls="accent-2 thin dotted")
    f.circle(x, y, 4, cls="accent-2-fill")
