"""Build the home page collage from the photographs in tools/collage/.

The layout is fixed: the solar eclipse fills a square on the left, the
other hidden-case photographs fill the top row on the right and the
darkened-case photographs the bottom row. Each source is cropped to the
box in sources.tsv and resized to its tile. The same sources and the same
Pillow version give the same bytes.

    python tools/make_collage.py [--out content/img/collage-v1.jpg]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "collage"
OUT = ROOT / "content" / "img" / "collage-v1.jpg"

WIDTH, HEIGHT, GAP = 1800, 600, 6
BACKGROUND = (11, 11, 13)


def tiles() -> list[tuple[int, int, int, int]]:
    """Tile boxes in the order of sources.tsv: left square, then 2 x 2."""
    side = HEIGHT
    x0 = side + GAP
    w = (WIDTH - x0 - GAP) // 2
    h = (HEIGHT - GAP) // 2
    boxes = [(0, 0, side, side)]
    for row in range(2):
        for col in range(2):
            x = x0 + col * (w + GAP)
            y = row * (h + GAP)
            boxes.append((x, y, x + w, y + h))
    return boxes


def sources() -> list[tuple[str, tuple[int, int, int, int]]]:
    rows = []
    for line in (SRC / "sources.tsv").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        crop = tuple(int(v) for v in cols[5].split(","))
        rows.append((cols[0], crop))
    return rows


def build(out: Path) -> None:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    for (name, crop), box in zip(sources(), tiles(), strict=True):
        with Image.open(SRC / name) as im:
            part = im.convert("RGB").crop(crop)
        size = (box[2] - box[0], box[3] - box[1])
        canvas.paste(part.resize(size, Image.Resampling.LANCZOS), box[:2])
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=84, optimize=True, progressive=False, subsampling=2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    build(ap.parse_args().out)


if __name__ == "__main__":
    main()
