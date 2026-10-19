#!/usr/bin/env python3
"""The corona at totality (spec FIG-10): a faint glow that fades outwards
from the dark disc, so totality never reads as the bright ring of an annular
eclipse. Not a figure itself; the figures that show totality import it."""

from figlib import Figure

# Opacity of the glow at fractions of the corona's radius. The disc covers
# the inner part, so the glow starts at its edge and fades to nothing.
STOPS = ((0.0, 0.0), (0.5, 0.75), (0.62, 0.45), (0.8, 0.15), (1.0, 0.0))


def corona(f: Figure, x: float, y: float, disc: float, gid: str) -> None:
    """Draw a corona around a disc of radius `disc` at (x, y). `gid` must be
    unique on the page, because every figure is inlined into one document."""
    stops = "".join(f'<stop offset="{o}" class="corona-stop" stop-opacity="{a}"/>' for o, a in STOPS)
    f.raw(f'<defs><radialGradient id="{gid}">{stops}</radialGradient></defs>')
    f.circle(x, y, disc * 2, cls="corona-fill", extra=f'fill="url(#{gid})"')
