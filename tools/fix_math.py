#!/usr/bin/env python3
r"""
Rewrite TeX constructs that pandoc's math parser rejects, inside $...$ and
$$...$$ spans only, so that --mathml succeeds instead of falling back to raw
TeX in a <span class="math">.

    python tools/fix_math.py          # rewrite content/**/*.md in place
    python tools/fix_math.py --check  # report, change nothing

Rewrites:  {\rm X} and \rm X  ->  \mathrm{X}
           °                  ->  ^{\circ}
           \cosec             ->  \csc
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MATH = re.compile(r"(\$\$.*?\$\$|\$[^$\n]+?\$)", re.S)
RM_BRACED = re.compile(r"\{\\rm\s+([^{}]+?)\}")
RM_BARE = re.compile(r"\\rm\s+([A-Za-z]+)")


def fix_span(m: re.Match) -> str:
    s = m.group(0)
    s = RM_BRACED.sub(lambda k: "\\mathrm{" + k.group(1) + "}", s)
    s = RM_BARE.sub(lambda k: "\\mathrm{" + k.group(1) + "}", s)
    s = s.replace("\u00b0", "^{\\circ}")
    s = s.replace("\\cosec", "\\csc")
    return s


def main() -> int:
    check = "--check" in sys.argv
    changed = 0
    for p in sorted(CONTENT.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        new = MATH.sub(fix_span, text)
        if new != text:
            changed += 1
            print(("would change " if check else "changed ") + p.relative_to(ROOT).as_posix())
            if not check:
                p.write_text(new, encoding="utf-8", newline="\n")
    print(f"{changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
