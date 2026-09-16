#!/usr/bin/env python3
"""Flag prose tics and over-long sentences across content/.

    python tools/prose_check.py            # summary counts and per-page totals
    python tools/prose_check.py --detail   # every offending sentence
    python tools/prose_check.py <path>...  # detail for specific pages

Advisory, not a build gate: several patterns have legitimate uses and the
tool cannot tell them apart. A deliberate parallel construction ("the
equipment is the point / the photograph is the point") will be flagged and
should be kept. Read the sentence before changing it.

Generated model blocks and code fences are excluded, so the counts describe
prose the author wrote.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

LONG_SENTENCE = 42

# Each pattern marks a habit that usually signals compressed or self-regarding
# prose. See "Writing standards" in AGENTS.md for what to do about each.
PATTERNS: dict[str, str] = {
    "flourish": r"\b(that is the honest|changes everything|the firm finding|"
                r"where the evidence|whole basis of|in commercial shape|not absurd|"
                r"the whole point|says everything|tells you everything|"
                r"that is the answer)\b",
    "worth-x": r"\b(worth (stating|noting|thinking|saying|having|doing)|it is worth)\b",
    "intensifier": r"\b(materially|meaningfully|genuinely|precisely|squarely|plainly|"
                   r"frankly|deeply|profoundly|starkly|considerably|substantially)\b",
    "not-x-but-y": r"\b(is not \w+[ ,]+(but|it is)|rather than an?\b|not \w+, but)\b",
    "both-ways": r"\b(cuts (both ways|in both directions)|in both directions)\b",
    "self-reference": r"\b(this (page|analysis|research|section|document)|"
                      r"the analysis (here|itself)|as (stated|noted) (above|earlier))\b",
    "which-is": r", which is (the|a|why|what|where|how)\b",
    "the-real-x": r"\bthe (real|honest|actual|true) "
                  r"(question|answer|state|finding|problem|issue|number|cost)\b",
    "hedge": r"\b(it must be said|to be fair|in fairness|arguably|one might|"
             r"it should be noted)\b",
    # A parenthetical em-dash pair usually means a second idea has been posted
    # into the middle of the first. Two sentences almost always read better.
    "em-dash-pair": r"—[^—\n]{0,80}—",
    # Invariant 5: the site states positions, not revisions.
    "process-narration": r"\b(earlier version|previously (said|stated)|has since been|"
                         r"now corrected|after (review|correction)|survives every|"
                         r"during review|over-?correct|is retained because|"
                         r"no longer recommended)\b",
}


def prose_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^---.*?^---", "", text, flags=re.S | re.M)      # front matter
    text = re.sub(r"<!--\w+:START-->.*?<!--\w+:END-->", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)               # code fences
    text = re.sub(r"^\|.*$", "", text, flags=re.M)                  # table rows
    return text


def sentences(body: str) -> list[str]:
    lines = [l for l in body.splitlines()
             if l.strip() and not l.lstrip().startswith(("|", ">", ":::", "!"))]
    joined = " ".join(lines)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", joined) if s.strip()]


def scan(paths: list[Path]) -> tuple[Counter, dict, list]:
    totals: Counter = Counter()
    per_page: dict[str, Counter] = defaultdict(Counter)
    detail: list[tuple[str, str, str]] = []
    for p in sorted(paths):
        rel = str(p.relative_to(CONTENT)).replace("\\", "/")
        body = prose_of(p)
        for name, pat in PATTERNS.items():
            n = len(re.findall(pat, body, re.I))
            if n:
                totals[name] += n
                per_page[rel][name] = n
        for s in sentences(body):
            hits = [k for k, pat in PATTERNS.items() if re.search(pat, s, re.I)]
            words = len(s.split())
            if words >= LONG_SENTENCE:
                totals["long-sentence"] += 1
                per_page[rel]["long-sentence"] += 1
                hits.append(f"long({words})")
            if hits:
                detail.append((rel, ",".join(hits), s))
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
        for rel, tags, s in detail:
            if rel != current:
                print(f"\n{rel}")
                current = rel
            print(f"  [{tags}] {s[:200]}")
        print()

    print("tic totals")
    for k, v in totals.most_common():
        print(f"{v:6}  {k}")
    if not totals:
        print("     0  clean")
        return 0

    print(f"\npages, worst first ({len(per_page)} with any)")
    for rel, c in sorted(per_page.items(), key=lambda kv: -sum(kv[1].values()))[:25]:
        print(f"{sum(c.values()):5}  {rel:56} {dict(c)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main(sys.argv[1:]))
