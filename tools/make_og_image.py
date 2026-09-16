#!/usr/bin/env python3
"""Compose the 1200x630 social preview card from the totality photograph.

A social card is shown without the page around it, so the credit the licence
asks for has to travel inside the image itself. The source is CC BY-SA 3.0 and
this crop of it is a derivative, so the card carries the attribution and the
licence, and is published under the same terms.

Padding a photograph that is already on black is seamless, so the corona is
scaled to fit and centred rather than cropped: the prominences around the limb
are the part worth showing and a 1200x630 crop would cut them off.

    python tools/make_og_image.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "content" / "img" / "totality-1999-viatour.jpg"
TARGET = ROOT / "content" / "img" / "social-card.jpg"

WIDTH, HEIGHT = 1200, 630
MARGIN = 28           # black kept above and below the corona
CREDIT = "Luc Viatour / lucnix.be \u00b7 CC BY-SA 3.0"
CAPTION = "Computing Solar Eclipses"

# Deterministic output: same input, same bytes, on any machine that has one of
# these fonts. The bitmap fallback keeps the build working where none is
# installed rather than failing over a caption.
FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
]


def load_font(size: int):
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: {SOURCE} is missing", file=sys.stderr)
        return 1

    card = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    photo = Image.open(SOURCE).convert("RGB")

    box = HEIGHT - 2 * MARGIN
    scale = box / max(photo.width, photo.height)
    size = (round(photo.width * scale), round(photo.height * scale))
    photo = photo.resize(size, Image.LANCZOS)

    # Sit the corona against the right edge rather than centred, so the title
    # has a column of real black to sit in instead of competing with the glow.
    photo_x = WIDTH - MARGIN - size[0]
    card.paste(photo, (photo_x, (HEIGHT - size[1]) // 2))

    draw = ImageDraw.Draw(card)

    left = 60
    usable = photo_x - left - 36
    credit_font = load_font(19)

    # Fit the title to the column instead of assuming a size: the font that is
    # actually installed decides the width, and an overflowing title would run
    # under the corona.
    title_font = load_font(46)
    for points in range(46, 23, -2):
        title_font = load_font(points)
        if draw.textlength(CAPTION, font=title_font) <= usable:
            break

    draw.text((left, HEIGHT // 2 - 30), CAPTION, font=title_font,
              fill=(242, 238, 230), anchor="ls")
    draw.text((left, HEIGHT // 2 + 8), "sankara.net", font=credit_font,
              fill=(166, 158, 146), anchor="ls")
    draw.text((WIDTH - MARGIN - 14, HEIGHT - 34), CREDIT, font=credit_font,
              fill=(154, 148, 138), anchor="ra")

    card.save(TARGET, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"{TARGET.relative_to(ROOT)}: {TARGET.stat().st_size // 1024} KB, "
          f"{WIDTH}x{HEIGHT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
