#!/usr/bin/env python3
"""
Shared drawing helpers for the site's own figures.

Every figure in `content/**/img/` that we draw ourselves is produced by a
script in this directory that imports this module. The rules the module
enforces:

* **Deterministic output.** Coordinates are rounded through `n()`, no
  timestamps or random ids are emitted, and dictionaries are written in
  insertion order. Two runs produce identical bytes.
* **Theme-aware.** Colours are CSS custom properties, never literals. The
  build inlines these SVGs into the page, so `var(--fig-ink)` resolves
  against the reader's current theme and the figure follows the theme
  toggle. A figure must never fill its own background: it sits on the page.
* **Legible without colour.** Colour may reinforce a distinction but must
  never carry it alone. Use a dash pattern, a label or a shape as well.
* **Accessible.** Every figure carries a `<title>` and a `<desc>`; the
  caption in the Markdown states the finding, and the `<desc>` describes the
  drawing for a reader who cannot see it.

Typical use:

    from figlib import Figure, n

    f = Figure(width=680, height=320,
               title="The fundamental plane",
               desc="A cross-section through the shadow cones ...")
    f.line(0, 160, 680, 160, cls="axis")
    f.text(340, 150, "shadow axis", anchor="middle", cls="label")
    f.save(__file__, "../../content/10-raw/01-foundations/img/plane.svg")
"""

from __future__ import annotations

import html as _html
import math
from pathlib import Path

__all__ = ["Figure", "n", "polar"]


def n(value: float) -> str:
    """Format a number for SVG: fixed precision, no trailing zeros, no -0."""
    r = round(float(value), 2)
    if r == 0:
        r = 0.0
    text = f"{r:.2f}".rstrip("0").rstrip(".")
    return text if text else "0"


def polar(cx: float, cy: float, radius: float, degrees: float) -> tuple[float, float]:
    """Point at an angle measured clockwise from north, for limb-style plots."""
    rad = math.radians(degrees - 90.0)
    return cx + radius * math.cos(rad), cy + radius * math.sin(rad)


class Figure:
    """A single SVG figure, drawn in user units and scaled by the viewBox."""

    def __init__(self, width: float, height: float, title: str, desc: str):
        self.width = width
        self.height = height
        self.title = title
        self.desc = desc
        self.parts: list[str] = []
        self._markers: set[str] = set()

    # ---------------------------------------------------------------- shapes
    def line(self, x1, y1, x2, y2, cls="rule", marker: str | None = None,
             extra: str = "") -> None:
        m = f' marker-end="url(#{marker})"' if marker else ""
        if marker:
            self._markers.add(marker)
        self.parts.append(
            f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"'
            f' class="{cls}"{m}{self._extra(extra)}/>')

    def path(self, d: str, cls="rule", marker: str | None = None,
             extra: str = "") -> None:
        m = f' marker-end="url(#{marker})"' if marker else ""
        if marker:
            self._markers.add(marker)
        self.parts.append(
            f'<path d="{d}" class="{cls}"{m}{self._extra(extra)}/>')

    def circle(self, cx, cy, r, cls="rule", extra: str = "") -> None:
        self.parts.append(
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"'
            f' class="{cls}"{self._extra(extra)}/>')

    def rect(self, x, y, w, h, cls="rule", rx: float = 0, extra: str = "") -> None:
        r = f' rx="{n(rx)}"' if rx else ""
        self.parts.append(
            f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"'
            f'{r} class="{cls}"{self._extra(extra)}/>')

    def polygon(self, points: list[tuple[float, float]], cls="rule",
                extra: str = "") -> None:
        pts = " ".join(f"{n(x)},{n(y)}" for x, y in points)
        self.parts.append(
            f'<polygon points="{pts}" class="{cls}"{self._extra(extra)}/>')

    def polyline(self, points: list[tuple[float, float]], cls="rule",
                 extra: str = "") -> None:
        pts = " ".join(f"{n(x)},{n(y)}" for x, y in points)
        self.parts.append(
            f'<polyline points="{pts}" class="{cls}"{self._extra(extra)}/>')

    def text(self, x, y, content, anchor="start", cls="label",
             extra: str = "") -> None:
        self.parts.append(
            f'<text x="{n(x)}" y="{n(y)}" text-anchor="{anchor}"'
            f' class="{cls}"{self._extra(extra)}>{_html.escape(str(content))}</text>')

    def group(self, body: str, extra: str = "") -> None:
        self.parts.append(f"<g{self._extra(extra)}>{body}</g>")

    def raw(self, markup: str) -> None:
        self.parts.append(markup)

    @staticmethod
    def _extra(extra: str) -> str:
        return f" {extra}" if extra else ""

    # ----------------------------------------------------------------- output
    def _defs(self) -> str:
        if not self._markers:
            return ""
        out = ["<defs>"]
        for name in sorted(self._markers):
            cls = "arrowhead" if name == "arrow" else f"arrowhead {name}"
            out.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5"'
                ' markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 9 5 L 0 9 z" class="{cls}"/></marker>')
        out.append("</defs>")
        return "".join(out)

    def to_svg(self) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(self.width)}'
            f' {n(self.height)}" role="img" class="figsvg">'
            f"<title>{_html.escape(self.title)}</title>"
            f"<desc>{_html.escape(self.desc)}</desc>"
            f"{self._defs()}"
            + "".join(self.parts)
            + "</svg>\n"
        )

    def save(self, script: str, relative_target: str) -> Path:
        """Write the SVG relative to the calling script's directory."""
        target = (Path(script).resolve().parent / relative_target).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.to_svg(), encoding="utf-8", newline="\n")
        print(f"wrote {target}")
        return target
