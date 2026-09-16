#!/usr/bin/env python3
"""
Normalise house-style spellings and notation in prose, leaving quotations,
code, URLs, math and citation tags untouched.

    python tools/normalise_prose.py --check   # report, change nothing
    python tools/normalise_prose.py           # rewrite content/**/*.md

Protected spans, in this order: fenced code blocks, inline code spans, math
(`$...$` and `$$...$$`), URLs, markdown link targets, `[@slug]`, `[?slug]`,
and any text inside double quotation marks (straight or curly). Quoted source
text must keep its own spelling, so the site can quote NASA's "Catalog" while
writing "catalogue" in its own voice.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

PROTECT = re.compile(
    r"```.*?```"                      # fenced code
    r"|~~~.*?~~~"
    r"|`[^`]*`"                       # inline code
    r"|\$\$.*?\$\$"                   # display math
    r"|\$[^$\n]+?\$"                  # inline math
    r"|https?://\S+"                  # bare URLs
    r"|\]\([^)]*\)"                   # link targets
    r"|\[@[^\]]*\]"                   # citations
    r"|\[\?[^\]]*\]"                  # glossary tags
    r"|“[^”]*”"        # curly double quotes
    r'|"[^"\n]*"',                    # straight double quotes
    re.S,
)

# Proper names that keep their source spelling even in the site's own voice.
KEEP = [
    "Five Millennium Catalog",
    "Catalog of Solar Eclipses",
    "Thousand Year Canon",
    "Eclipse Catalog",
]

SUBS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bcatalog\b"), "catalogue"),
    (re.compile(r"\bCatalog\b"), "Catalogue"),
    (re.compile(r"\bcatalogs\b"), "catalogues"),
    (re.compile(r"\bCatalogs\b"), "Catalogues"),
    (re.compile(r"\bvisualizations\b"), "visualisations"),
    (re.compile(r"\bvisualization\b"), "visualisation"),
    (re.compile(r"\bgray\b"), "grey"),
    # Notation: ΔT in prose, headings and front matter.
    (re.compile(r"\bDelta T\b"), "ΔT"),
    (re.compile(r"\bdelta T\b"), "ΔT"),
    # One name for the central line.
    (re.compile(r"\bcentreline\b"), "central line"),
    (re.compile(r"\bCentreline\b"), "Central line"),
    (re.compile(r"\bcentre line\b"), "central line"),
    (re.compile(r"\bCentre line\b"), "Central line"),
]


def fix_prose(text: str) -> str:
    for pat, rep in SUBS:
        text = pat.sub(rep, text)
    return text


def process(body: str) -> str:
    out: list[str] = []
    pos = 0
    for m in PROTECT.finditer(body):
        out.append(fix_prose(body[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix_prose(body[pos:]))
    joined = "".join(out)
    # Restore proper names the blanket rule over-corrected.
    for name in KEEP:
        joined = joined.replace(name.replace("Catalog", "Catalogue"), name)
    return joined


def main() -> int:
    check = "--check" in sys.argv
    changed = 0
    for md in sorted(CONTENT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        new = process(text)
        if new != text:
            changed += 1
            n = sum(1 for a, b in zip(text.split("\n"), new.split("\n")) if a != b)
            print(f"{'would change' if check else 'changed'} {md.relative_to(ROOT).as_posix()} ({n} lines)")
            if not check:
                md.write_text(new, encoding="utf-8", newline="\n")
    print(f"{changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
