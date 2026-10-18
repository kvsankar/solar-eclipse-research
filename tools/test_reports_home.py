"""Acceptance tests AT-REP-1 to AT-REP-4 and AT-HOME-1 to AT-HOME-5 (docs/acceptance-tests.md)."""

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REPORTS = CONTENT / "20-reports"
HOME = CONTENT / "_index.md"
COLLAGE = CONTENT / "img" / "collage-v1.jpg"
SOURCES = ROOT / "tools" / "collage" / "sources.tsv"
GROUPS = ["Shared geometry and inputs", "Solar eclipses and transits", "Lunar eclipses",
          "Occultations", "Planetary satellites"]
OPEN_LICENCES = ("Public domain", "CC BY-SA")


def read(path):
    return path.read_text(encoding="utf-8")


def front(text):
    return dict(re.findall(r"^(\w+):\s*(.*)$", text.split("---", 2)[1], flags=re.M))


def body(text):
    return text.split("---", 2)[2]


def h2(text):
    return re.findall(r"^## (.+)$", text, flags=re.M)


class ReportsTest(unittest.TestCase):
    def test_rep_1_cases_before_solar(self):
        heads = h2(read(REPORTS / "executive-summary.md"))
        solar = next(i for i, h in enumerate(heads) if "solar eclipse" in h.lower())
        for case in ("Hidden", "Darkened"):
            idx = next((i for i, h in enumerate(heads) if h.startswith(case)), None)
            self.assertIsNotNone(idx, case)
            self.assertLess(idx, solar, case)

    def test_rep_2_solar_titles_and_link(self):
        for name, title in (("pipeline-design.md", "Solar eclipse pipeline"),
                            ("error-budget.md", "Solar eclipse error budget")):
            text = read(REPORTS / name)
            self.assertEqual(front(text)["title"], title)
            after_summary = body(text).split(":::", 2)[-1]
            opening = next(p for p in re.split(r"\n\s*\n", after_summary) if p.strip())
            self.assertIn("solar eclipse", opening.lower(), name)
            self.assertIn("(other-events.md)", opening, name)

    def test_rep_3_order(self):
        want = ["Executive summary", "Solar eclipse pipeline", "Extending the pipeline to other events",
                "Solar eclipse error budget", "Reading list and reference matrix", "Open questions"]
        pages = []
        for p in REPORTS.glob("*.md"):
            if p.name == "_index.md":
                continue
            meta = front(read(p))
            pages.append((int(meta["order"]), meta["title"]))
        self.assertEqual([t for _, t in sorted(pages)], want)

    def test_rep_4_group_sections(self):
        for name in ("reading-list.md", "open-questions.md"):
            heads = h2(read(REPORTS / name))
            for group in GROUPS:
                self.assertIn(group, heads, f"{name}: {group}")


class HomeTest(unittest.TestCase):
    def setUp(self):
        self.text = read(HOME)
        self.body = body(self.text)

    def test_home_1_collage_and_credits(self):
        first_img = re.search(r"\]\(([^)\s]+)\)\{\.hero\}", self.body).group(1)
        self.assertEqual(self.body[: self.body.index("{.hero}")].count("!["), 1, "the hero is not the first image")
        self.assertEqual(first_img, "img/collage-v1.jpg")
        prov = read(CONTENT / "images.tsv")
        row = next(l for l in prov.splitlines() if l.startswith("img/collage-v1.jpg\t"))
        self.assertTrue(any(lic in row for lic in OPEN_LICENCES), row)
        rows = [l.split("\t") for l in read(SOURCES).splitlines() if l and not l.startswith("#")]
        self.assertGreaterEqual(len(rows), 4)
        for cols in rows:
            file, case, author, licence = cols[0], cols[1], cols[2], cols[3]
            self.assertTrue(licence.startswith(OPEN_LICENCES), (file, licence))
            self.assertTrue((SOURCES.parent / file).is_file(), file)
            self.assertIn(author, self.body, f"credit for {file}")
        self.assertEqual({c[1] for c in rows} >= {"hidden", "darkened"}, True)

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow is not installed")
    def test_home_2_collage_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            outs = []
            for i in range(2):
                out = Path(tmp) / f"c{i}.jpg"
                subprocess.run([sys.executable, str(ROOT / "tools" / "make_collage.py"), "--out", str(out)],
                               check=True, capture_output=True)
                outs.append(out.read_bytes())
            self.assertEqual(outs[0], outs[1])
            self.assertEqual(outs[0], COLLAGE.read_bytes())

    def test_home_3_intro(self):
        after_img = self.body.split("{.hero}", 1)[1]
        intro = " ".join(next(p for p in re.split(r"\n\s*\n", after_img) if p.strip()).split())
        self.assertIn("shadow", intro)
        self.assertIn("who stands in", intro)
        self.assertIn("solar eclipses", intro.lower())
        self.assertIn("most depth", intro)

    def test_home_4_summary(self):
        summary = self.body.split("::: summary", 1)[1].split(":::", 1)[0]
        bullets = re.findall(r"^- \*\*([^*]+)\*\*", summary, flags=re.M)
        for case in ("Hidden", "Darkened"):
            self.assertTrue(any(b.startswith(case) for b in bullets), case)
        self.assertTrue(any("solar eclipse" in b.lower() for b in bullets))

    def test_home_5_grouped_table(self):
        heads = re.findall(r"^### (.+)$", self.body, flags=re.M)
        for group in GROUPS:
            self.assertIn(group, heads, group)
        for idx in (CONTENT / "10-raw").rglob("_index.md"):
            rel = idx.relative_to(CONTENT).as_posix()
            if rel == "10-raw/_index.md" or idx.parent.parent.name == "10-raw" and any(
                    d.is_dir() and (d / "_index.md").exists() for d in idx.parent.iterdir()):
                continue
            self.assertIn(f"]({rel})", self.body, rel)


if __name__ == "__main__":
    unittest.main()
