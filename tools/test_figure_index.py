"""Acceptance test AT-FIG-16 (docs/acceptance-tests.md): the figure index."""

import re
import unittest
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
INDEX = CONTENT / "00-meta" / "figure-index.md"


def tsv_paths():
    rows = (ROOT / "images.tsv").read_text(encoding="utf-8").splitlines()
    return [r.split("\t")[0] for r in rows if r.strip() and not r.startswith("#")]


class FigureIndexTest(unittest.TestCase):
    def setUp(self):
        self.root = build.build_tree()
        self.shown, self.build_only = build.figure_index(self.root)

    def test_every_picture_once(self):
        listed = [r["path"] for r in self.shown + self.build_only]
        self.assertEqual(sorted(listed), sorted(tsv_paths()))
        self.assertEqual(len(listed), len(set(listed)))
        self.assertIn("img/social-card-v4.jpg", [r["path"] for r in self.build_only])

    def test_rows_link_their_page_and_caption(self):
        for r in self.shown:
            self.assertTrue(r["page"].endswith(".md"), r)
            self.assertTrue((CONTENT / r["page"]).is_file(), r)
            self.assertTrue(r["caption"], r)
            self.assertLessEqual(len(r["caption"].split()), 25, r)
            self.assertNotIn("[@", r["caption"])
            self.assertNotIn("[?", r["caption"])

    def test_kinds(self):
        kinds = {r["path"]: r["kind"] for r in self.shown + self.build_only}
        self.assertEqual(kinds["05-primer/img/anim-io-orbit.svg"], "animation")
        self.assertEqual(kinds["05-primer/img/case-hidden.svg"], "diagram")
        self.assertEqual(kinds["img/collage-v1.jpg"], "photograph")

    def test_page_and_rendered_table(self):
        self.assertIn("<!--FIGURES-->", INDEX.read_text(encoding="utf-8"))
        node = next(n for n in build.walk(self.root) if n.src == INDEX)
        html = build.render_figure_index(self.shown, self.build_only, node)
        rows = re.findall(r"<tr class=\"figrow\">", html)
        self.assertEqual(len(rows), len(self.shown) + len(self.build_only))
        for src in re.findall(r'<img src="([^"]+)"', html):
            self.assertTrue((INDEX.parent / src).resolve().is_file(), src)
        self.assertEqual(len(re.findall(r'<img src="', html)), len(rows))


if __name__ == "__main__":
    unittest.main()
