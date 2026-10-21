"""Page addresses (docs/specs.md URL-1 to URL-3; AT-URL-1, AT-URL-2)."""
from __future__ import annotations

import posixpath
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import url_names as un  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIRS = {"00-meta", "05-primer", "05-primer/img", "10-raw", "10-raw/10-shared",
        "10-raw/10-shared/01-foundations", "10-raw/10-shared/01-foundations/img", "20-reports"}
NAMES = {"10-raw": "research-notes"}
REF_RE = re.compile(r'\b(?:href|src)="([^"]*)"')


class Mapping(unittest.TestCase):
    """AT-URL-1."""

    def setUp(self):
        self.urls = un.UrlNames(DIRS, NAMES)

    def test_folders(self):
        self.assertEqual(self.urls.url("10-raw/10-shared/01-foundations/besselian-elements.html"),
                         "research-notes/shared/foundations/besselian-elements.html")
        self.assertEqual(self.urls.url("05-primer/img/case-hidden.svg"), "primer/img/case-hidden.svg")
        self.assertEqual(self.urls.url("20-reports/index.html"), "reports/index.html")
        self.assertEqual(self.urls.url("computing.html"), "computing.html")

    def test_paths_outside_content_do_not_change(self):
        self.assertEqual(self.urls.url("assets/site.css"), "assets/site.css")

    def test_relative_links(self):
        page = "10-raw/10-shared/01-foundations/besselian-elements"
        self.assertEqual(self.urls.link("../../../05-primer/glossary.html#ref-1", page),
                         "../../../primer/glossary.html#ref-1")
        self.assertEqual(self.urls.link("img/plane.svg", page), "img/plane.svg")
        self.assertEqual(self.urls.link("../../../assets/site.css?v=1", page), "../../../assets/site.css?v=1")
        for href in ("https://example.org/", "#top", "/astro/", "mailto:a@b.c"):
            self.assertEqual(self.urls.link(href, page), href)

    def test_two_folders_with_one_address_fail(self):
        with self.assertRaises(ValueError):
            un.UrlNames({"05-primer", "06-primer"}, {})

    def test_url_name_that_is_a_source_folder_fails(self):
        with self.assertRaises(ValueError):
            un.UrlNames({"00-meta", "05-primer"}, {"00-meta": "05-primer"})


class BuiltSite(unittest.TestCase):
    """AT-URL-2: the whole site, built into a temporary folder."""

    @classmethod
    def setUpClass(cls):
        import build
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        with patch.object(build, "OUT", cls.out), patch.object(sys, "argv", ["build.py", "--quiet"]):
            cls.status = build.main()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_build_succeeds(self):
        self.assertEqual(self.status, 0)

    def test_no_numbered_folders(self):
        numbered = [p.relative_to(self.out).as_posix() for p in self.out.rglob("*")
                    if p.is_dir() and re.match(r"\d{2}-", p.name)]
        self.assertEqual(numbered, [])

    def test_top_level_folders(self):
        tops = sorted(p.name for p in self.out.iterdir() if p.is_dir())
        self.assertEqual(tops, ["assets", "img", "meta", "primer", "reports", "research-notes"])

    def test_every_relative_link_resolves(self):
        broken = []
        for page in sorted(self.out.rglob("*.html")):
            rel = page.relative_to(self.out).as_posix()
            text = page.read_text(encoding="utf-8")
            text = re.sub(r"<script\b.*?</script>", "", text, flags=re.S)
            for href in REF_RE.findall(text):
                if not href or re.match(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|/)", href):
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href.split("#")[0].split("?")[0]))
                if target in (".", "") or (self.out / target).exists():
                    continue
                broken.append(f"{rel}: {href}")
        self.assertEqual(broken, [], "\n".join(broken[:20]))


if __name__ == "__main__":
    unittest.main()
