#!/usr/bin/env python3
"""
Link the first mention of a mapped subject on each page (specs LNK-2, LNK-3).

    python tools/autolink.py            # report the links it would add, per page
    python tools/autolink.py --apply    # add them to the Markdown in content/

The map is `links.tsv` at the repository root: a pattern and a target per row.
A target is either a page of this site, relative to content/, or a canonical
page outside it on a host listed in CANONICAL_SITES in tools/build.py. Each
target is linked at most once per page, at its first mention in prose, and a
page never links to itself or repeats a target it already links.

Prose only: front matter, headings, image lines, fenced divs, block quotes,
quotations, tables' rule lines, code, maths, HTML, URLs, existing links,
citations and glossary markers are never touched. Run it after writing a note, then read the
diff: a mapped phrase can still mean something else in a given sentence.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MAP = ROOT / "links.tsv"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import site_name  # noqa: E402

# Spans that are not prose. Order does not matter: they are merged into one mask.
PROTECTED = [
    re.compile(r"\A---\n.*?\n---\n", re.S),               # front matter
    re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.S | re.M),   # fenced code
    re.compile(r"(?<!\\)\$\$.*?(?<!\\)\$\$", re.S),         # display maths
    re.compile(r"`[^`\n]+`"),                              # inline code
    re.compile(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<![\s\\])\$"),  # inline maths
    # Links and images, whose text may run over lines and hold [@cite] markers.
    re.compile(r"!?\[(?:[^\[\]]|\[[^\[\]]*\])*\]\((?:[^()\s]|\([^()\s]*\))*[^)]*\)"),
    re.compile(r"\[[@?][^\]\n]*\]"),                       # citations, glossary markers
    re.compile(r"<!--.*?-->", re.S),                       # comments
    re.compile(r"<[^>\n]+>"),                              # HTML tags
    re.compile(r"https?://\S+"),                           # bare URLs
    re.compile(r"\{[^}\n]*\}"),                            # attribute blocks
    re.compile(r'"[^"\n]{1,600}"|“[^”\n]{1,600}”'),           # quotations
    re.compile(r"^(?:#|!\[|:::|>|\|?[ \t]*:?-{3,}).*$", re.M),  # whole lines
]

# One level of parentheses inside a URL, as in Wikipedia's Io_(moon).
LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(((?:[^()\s]|\([^()\s]*\))+)[^)]*\)")


def load_map() -> list[tuple[re.Pattern, str]]:
    rows = []
    for lineno, raw in enumerate(MAP.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) < 2:
            raise SystemExit(f"links.tsv line {lineno}: expected pattern<TAB>target")
        pattern, target = parts[0], parts[1].strip()
        if target.startswith("http"):
            if site_name(target) is None:
                raise SystemExit(f"links.tsv line {lineno}: {target} is not on a canonical host")
        elif not (CONTENT / target.partition("#")[0]).is_file():
            raise SystemExit(f"links.tsv line {lineno}: no page content/{target}")
        rows.append((re.compile(rf"(?<![\w-])(?:{pattern})(?![\w-])"), target))
    return rows


def protected_mask(text: str) -> bytearray:
    mask = bytearray(len(text))
    for rx in PROTECTED:
        for m in rx.finditer(text):
            mask[m.start():m.end()] = b"\x01" * (m.end() - m.start())
    return mask


def page_key(page: Path) -> str:
    return page.relative_to(CONTENT).as_posix()


def existing_targets(page: Path, text: str) -> set[str]:
    """Targets the page already links, as content-relative paths or URLs."""
    out = set()
    for m in LINK_TARGET_RE.finditer(text):
        url = m.group(1)
        if url.startswith("http"):
            out.add(url)
        elif not url.startswith(("#", "mailto:")):
            path = url.partition("#")[0]
            if path:
                resolved = (page.parent / path).resolve()
                try:
                    out.add(resolved.relative_to(CONTENT.resolve()).as_posix())
                except ValueError:
                    pass
    return out


def plan(page: Path, text: str, rows) -> list[tuple[int, int, str]]:
    """The (start, end, href) of each link to add, in document order."""
    mask = protected_mask(text)
    used = existing_targets(page, text) | {page_key(page)}
    candidates = []
    for rx, target in rows:
        if target in used:
            continue
        for m in rx.finditer(text):
            if not any(mask[m.start():m.end()]):
                candidates.append((m.start(), -(m.end() - m.start()), m.end(), target))
                break
    # Earliest first; at one position the longest phrase wins.
    candidates.sort()
    taken: list[tuple[int, int, str]] = []
    for start, _, end, target in candidates:
        if target in used or any(s < end and start < e for s, e, _ in taken):
            continue
        used.add(target)
        href = target if target.startswith("http") else os.path.relpath(
            CONTENT / target, page.parent).replace(os.sep, "/")
        taken.append((start, end, href))
    return sorted(taken)


def apply(text: str, links) -> str:
    for start, end, href in reversed(links):
        text = f"{text[:start]}[{text[start:end]}]({href}){text[end:]}"
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the links into content/")
    ap.add_argument("paths", nargs="*", help="pages to process (default: all of content/)")
    args = ap.parse_args()
    rows = load_map()
    pages = [Path(p).resolve() for p in args.paths] or sorted(CONTENT.rglob("*.md"))
    total = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        links = plan(page, text, rows)
        if not links:
            continue
        total += len(links)
        print(f"{page_key(page)}: {len(links)}")
        for start, end, href in links:
            print(f"    {text[start:end]!r} -> {href}")
        if args.apply:
            page.write_text(apply(text, links), encoding="utf-8", newline="\n")
    print(f"{total} link(s) {'added' if args.apply else 'to add'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
