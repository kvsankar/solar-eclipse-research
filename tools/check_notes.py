#!/usr/bin/env python3
"""
Check raw research notes against the shape AGENTS.md prescribes.

    python tools/check_notes.py            # all of content/10-raw
    python tools/check_notes.py 05-lunar-limb

Reports, per note: missing front matter keys, a missing `::: summary` block,
missing required sections, citation slugs not defined in any refs.tsv,
glossary slugs not defined in any terms.tsv, word count, citation count, and
em-dashes (the writing standard forbids them).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "content" / "10-raw"

REQUIRED_META = ("title", "description", "order", "status", "updated")
REQUIRED_SECTIONS = ("sources compared", "what a developer should do", "what this changes", "open questions")
CITE_RE = re.compile(r"\[@([A-Za-z0-9][A-Za-z0-9._-]*)\]")
GLOSS_RE = re.compile(r"\[\?([A-Za-z0-9][A-Za-z0-9._-]*)(?:\|[^\]]+)?\]")
CODE_RE = re.compile(r"(```.*?```|~~~.*?~~~|`[^`]*?`)", re.S)


def load_slugs(name: str) -> set[str]:
    slugs = set()
    for frag in (ROOT / "content").rglob(name):
        for line in frag.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                slugs.add(line.split("\t")[0].strip())
    return slugs


def main() -> int:
    refs = load_slugs("refs.tsv")
    terms = load_slugs("terms.tsv")
    targets = [RAW / a for a in sys.argv[1:]] or [RAW]
    problems = 0
    for base in targets:
        for md in sorted(base.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            rel = md.relative_to(ROOT).as_posix()
            issues = []
            fm = {}
            if text.startswith("---"):
                block = text.split("---", 2)[1]
                for line in block.splitlines():
                    m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line.strip())
                    if m:
                        fm[m.group(1)] = m.group(2)
            missing_meta = [k for k in REQUIRED_META if k not in fm]
            if md.name != "_index.md" and missing_meta:
                issues.append(f"front matter missing {', '.join(missing_meta)}")
            body = "".join(p for i, p in enumerate(CODE_RE.split(text)) if i % 2 == 0)
            if md.name != "_index.md":
                if "::: summary" not in text:
                    issues.append("no ::: summary block")
                low = body.lower()
                for sec in REQUIRED_SECTIONS:
                    if not re.search(r"^#{2,3}\s+.*" + re.escape(sec), low, re.M):
                        issues.append(f"missing section '{sec}'")
            cites = CITE_RE.findall(body)
            unknown = sorted({c for c in cites if c not in refs})
            if unknown:
                issues.append(f"unknown citation slugs: {', '.join(unknown)}")
            gl = GLOSS_RE.findall(body)
            gunknown = sorted({g for g in gl if g not in terms})
            if gunknown:
                issues.append(f"unknown glossary slugs: {', '.join(gunknown)}")
            dashes = body.count("—")
            if dashes:
                issues.append(f"{dashes} em-dash(es)")
            words = len(re.findall(r"\w+", body))
            status = "OK " if not issues else "!! "
            print(f"{status}{rel}: {words} words, {len(cites)} citations, {len(set(cites))} distinct")
            for i in issues:
                print(f"     - {i}")
                problems += 1
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
