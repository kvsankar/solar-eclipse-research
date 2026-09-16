import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
for p in sorted(Path(sys.argv[1]).glob("*.md")):
    t = p.read_text(encoding="utf-8")
    print(f"\n######## {p.name}")
    m = re.search(r"^title:\s*(.*)$", t, re.M); print("TITLE:", m.group(1) if m else "")
    s = re.search(r"::: summary(.*?):::", t, re.S); print("SUMMARY:" + (s.group(1) if s else " (none)"))
    if p.name == "_index.md":
        print(t.split("---",2)[2][:3000]); continue
    for sec in ("sources compared", "what a developer should do", "what this changes", "open questions"):
        mm = re.search(r"^(#{2,3}\s+[^\n]*" + sec + r"[^\n]*)\n(.*?)(?=^#{2,3}\s|\Z)", t, re.S | re.M | re.I)
        if mm: print("\n" + mm.group(1) + "\n" + mm.group(2).strip()[:6000])
