#!/usr/bin/env python3
"""Flag forward references: a term or a name used before the reader is told what it is.

    python tools/jargon_check.py             # per-page counts, worst first
    python tools/jargon_check.py --detail    # every flagged first use, with its line
    python tools/jargon_check.py <path>...   # detail for specific pages

Two defect classes, one rule. Both are about first use on a page, because a
reader arrives at any page cold and the page has to stand up on its own.

  jargon  A term of art whose first use on the page carries no [?slug]
          explainer and no gloss nearby. "the GST argument" in a summary that
          does not explain GST for another fifty lines is the case that
          prompted this.

  entity  A named third party — an operator, a vendor, a regulator — whose
          first mention on the page carries neither a [@slug] citation nor a
          markdown link. The reader gets a name with nothing behind it, and on
          a summary page it usually means a sourced claim was paraphrased out
          of its citation.

`prose_check.py` looks inside a sentence; this looks at the order of a page.
Both are advisory. A page whose entire subject is one operator does not need
that operator linked in its first line if the heading has already said so —
read the flag before acting on it.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# Shorthand that carries no glossary entry and must therefore carry its meaning
# the first time a page uses it.
SHORTHAND = [
    "GST argument", "customs argument", "the export argument",
    "place of supply", "Circular 232", "zero-rating", "zero-rated",
    "input tax credit", "break-even", "contribution", "cohort",
    "occupancy", "fill rate", "swing diameter", "roll-off", "pier",
    "capex", "depreciation", "reverse charge", "blocked credit",
]

# Named third parties. A mention is fine; an unlinked, uncited first mention is
# the flag.
ENTITIES = [
    "Starfront", "Starscapes", "PixelSkies", "Telescope Live", "iTelescope",
    "Astronomads", "Starvoirs", "Slooh", "ChileScope", "Deep Sky Chile",
    "Obstech", "DSP Remote", "ZWO", "Askar", "ZWO Seestar", "Vorion",
    "ARIES", "IIA", "Backblaze", "Starlink", "Vaonis", "Unistellar",
]

WINDOW = 240        # characters after first use that may still carry the gloss


def load_glossary() -> set[str]:
    slugs = set()
    with (ROOT / "glossary.tsv").open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh, delimiter="\t"):
            if row and not row[0].startswith("#"):
                slugs.add(row[0])
    return slugs


def prose_of(path: Path) -> str:
    """Blank out front matter, generated blocks and code fences.

    Replaced with the same number of newlines rather than deleted, so reported
    line numbers still point at the line in the file.
    """
    text = path.read_text(encoding="utf-8")
    def blank(m):
        return "\n" * m.group(0).count("\n")

    text = re.sub(r"^---.*?^---", blank, text, flags=re.S | re.M)
    text = re.sub(r"<!--\w+:START-->.*?<!--\w+:END-->", blank, text, flags=re.S)
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    return text


def line_of(body: str, pos: int) -> int:
    return body.count("\n", 0, pos) + 1


def first_use(body: str, term: str) -> int | None:
    """Position of the first plain-prose use, ignoring [?...] and [@...] markers."""
    for m in re.finditer(rf"(?<!\w){re.escape(term)}(?!\w)", body, re.I):
        before = body[max(0, m.start() - 2):m.start()]
        if before.endswith(("[?", "[@")):
            continue
        return m.start()
    return None


def scan(paths: list[Path]) -> tuple[Counter, dict, list]:
    totals: Counter = Counter()
    per_page: dict[str, Counter] = defaultdict(Counter)
    detail: list[tuple[str, str, str, int, str]] = []

    for p in sorted(paths):
        rel = str(p.relative_to(CONTENT)).replace("\\", "/")
        body = prose_of(p)

        for term in SHORTHAND:
            pos = first_use(body, term)
            if pos is None:
                continue
            head = body[:pos]
            tail = body[pos:pos + WINDOW]
            # Already explained: an explainer for the term anywhere before it,
            # or an explainer or a parenthetical definition close after it.
            tagged = re.search(rf"\[\?[\w-]+(\|[^\]]*)?\]", head + tail) and \
                re.search(re.escape(term), head + tail[:80], re.I)
            glossed = re.search(r"\bmeans\b|\bthat is,|\bi\.e\.|\((?:the )?[a-z][^)]{20,}\)",
                                tail, re.I)
            if tagged or glossed:
                continue
            totals["jargon"] += 1
            per_page[rel]["jargon"] += 1
            detail.append((rel, "jargon", term, line_of(body, pos),
                           body[max(0, pos - 60):pos + 120].replace("\n", " ")))

        for name in ENTITIES:
            pos = first_use(body, name)
            if pos is None:
                continue
            near = body[max(0, pos - 200):pos + WINDOW]
            # A citation, an outward link, or an inward link to the page that
            # analyses it all count as putting something behind the name.
            if re.search(r"\[@[\w-]+\]", near) or re.search(r"\]\([^)]+\)", near):
                continue
            totals["entity"] += 1
            per_page[rel]["entity"] += 1
            detail.append((rel, "entity", name, line_of(body, pos),
                           body[max(0, pos - 60):pos + 120].replace("\n", " ")))

    return totals, per_page, detail


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    want_detail = "--detail" in argv or bool(args)
    paths = [Path(a) if Path(a).is_absolute() else (CONTENT / a) for a in args] \
        if args else list(CONTENT.rglob("*.md"))
    missing = [p for p in paths if not p.exists()]
    if missing:
        print("no such page: " + ", ".join(str(m) for m in missing))
        return 2

    totals, per_page, detail = scan(paths)

    if want_detail:
        current = None
        for rel, kind, term, line, ctx in detail:
            if rel != current:
                print(f"\n{rel}")
                current = rel
            print(f"  {line:>4}  [{kind}] {term}")
            print(f"        ...{ctx.strip()}...")
        print()

    print("totals")
    for k, v in totals.most_common():
        print(f"{v:6}  {k}")
    if not totals:
        print("     0  clean")
        return 0

    print(f"\npages, worst first ({len(per_page)} with any)")
    for rel, c in sorted(per_page.items(), key=lambda kv: -sum(kv[1].values()))[:30]:
        print(f"{sum(c.values()):5}  {rel:56} {dict(c)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main(sys.argv[1:]))
