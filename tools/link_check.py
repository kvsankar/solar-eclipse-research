#!/usr/bin/env python3
"""
Check the site's links and report how densely each page links (spec LNK).

    python tools/link_check.py            # broken links, hosts, density floors
    python tools/link_check.py --report   # also print every page's counts
    python tools/link_check.py --online   # also fetch every external URL once

Run it after `tools/build.py`: anchors are checked against the built pages.
`--online` needs network access and is meant for a workstation, not CI.

Exit status is 1 when any check fails.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import site_name  # noqa: E402

# A research note links at least this many other pages of the site and this
# many canonical pages outside it (LNK-6). Glossary terms with a canonical
# page count towards the second, because the explainer carries the link.
MIN_INTERNAL = 5
MIN_EXTERNAL = 3

CODE_RE = re.compile(r"```.*?```|`[^`\n]+`", re.S)
LINK_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(((?:[^()\s]|\([^()\s]*\))+)(?:\s+\"[^\"]*\")?\)")
GLOSS_RE = re.compile(r"\[\?([A-Za-z0-9][A-Za-z0-9._-]*)(?:\|[^\]]+)?\]")
ID_RE = re.compile(r'\bid="([^"]+)"')


def is_note(page: Path) -> bool:
    rel = page.relative_to(CONTENT).as_posix()
    return rel.startswith("10-raw/") and page.name != "_index.md"


def glossary_urls() -> dict[str, str]:
    out = {}
    for raw in (ROOT / "glossary.tsv").read_text(encoding="utf-8").splitlines():
        if raw.startswith("#") or not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) > 3 and parts[3].strip():
            out[parts[0]] = parts[3].strip()
    return out


def built_ids(page: Path) -> set[str] | None:
    """The element ids of a page's built HTML, or None before a build."""
    rel = page.relative_to(CONTENT)
    html_path = SITE / (rel.parent / "index.html" if rel.name == "_index.md"
                        else rel.with_suffix(".html"))
    if not html_path.is_file():
        return None
    return set(ID_RE.findall(html_path.read_text(encoding="utf-8")))


def page_links(page: Path):
    """(internal targets as resolved Paths with anchors, external URLs, glossary slugs)."""
    text = CODE_RE.sub("", page.read_text(encoding="utf-8"))
    internal, external = [], []
    for m in LINK_RE.finditer(text):
        url = m.group(1)
        if url.startswith(("http://", "https://")):
            external.append(url)
        elif url.startswith(("#", "mailto:")):
            continue
        else:
            path, _, anchor = url.partition("#")
            internal.append(((page.parent / path).resolve(), anchor, url))
    return internal, external, set(GLOSS_RE.findall(text))


def check(report: bool) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    every_external: set[str] = set()
    gloss_urls = glossary_urls()
    for url in gloss_urls.values():
        every_external.add(url)
    rows = []
    for page in sorted(CONTENT.rglob("*.md")):
        rel = page.relative_to(CONTENT).as_posix()
        internal, external, slugs = page_links(page)
        targets = set()
        for target, anchor, url in internal:
            if not target.is_file():
                errors.append(f"{rel}: link {url} goes to no file")
                continue
            if target.suffix == ".md":
                if target != page.resolve():
                    targets.add(target)
                ids = built_ids(target)
                if anchor and ids is not None and anchor not in ids:
                    errors.append(f"{rel}: link {url} names no heading on that page")
        for url in external:
            every_external.add(url)
            if not url.startswith("https://"):
                errors.append(f"{rel}: {url} is not https (LNK-5)")
            elif is_note(page) and site_name(url) is None:
                errors.append(f"{rel}: {url} is not on a canonical host (LNK-5)")
        canonical = {u for u in external if site_name(u)}
        canonical |= {gloss_urls[s] for s in slugs if s in gloss_urls}
        rows.append((rel, len(targets), len(canonical)))
        if is_note(page):
            if len(targets) < MIN_INTERNAL:
                errors.append(f"{rel}: links {len(targets)} other pages, "
                              f"fewer than {MIN_INTERNAL} (LNK-6)")
            if len(canonical) < MIN_EXTERNAL:
                errors.append(f"{rel}: links {len(canonical)} canonical pages, "
                              f"fewer than {MIN_EXTERNAL} (LNK-6)")
    if report:
        print(f"{'pages':>6} {'canon':>6}  page")
        for rel, n_int, n_ext in rows:
            print(f"{n_int:6} {n_ext:6}  {rel}")
    return errors, every_external


def fetch_all(urls: set[str]) -> list[str]:
    failures = []
    for url in sorted(urls):
        req = urllib.request.Request(url, headers={"User-Agent": "link_check/1"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status >= 400:
                    failures.append(f"{url}: HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            failures.append(f"{url}: HTTP {e.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            failures.append(f"{url}: {e}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", action="store_true", help="print every page's counts")
    ap.add_argument("--online", action="store_true", help="fetch every external URL")
    args = ap.parse_args()
    errors, external = check(args.report)
    if args.online:
        errors += fetch_all(external)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"{len(external)} distinct external URLs; {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
