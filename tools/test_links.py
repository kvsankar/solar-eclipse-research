"""Acceptance tests AT-LNK-1 to AT-LNK-7 (docs/acceptance-tests.md): links."""

import re
import unittest
from pathlib import Path

import autolink
import build
import link_check

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
WIKI = "https://en.wikipedia.org/wiki/Saros_(astronomy)"


class GlossaryLinkTest(unittest.TestCase):
    """AT-LNK-1 and the glossary half of AT-LNK-5."""

    terms = {"saros": ("Saros", "A cycle of 223 synodic months.", WIKI),
             "gamma": ("gamma", "The axis distance.", "")}

    def test_panel_and_listing_carry_the_link(self):
        html = build.resolve_glossary("The [?saros] and [?gamma].", self.terms, set(), set())
        self.assertEqual(html.count('class="gloss-more"'), 1)
        self.assertIn(f'<a href="{WIKI}">Read on Wikipedia</a>', html)
        listing = build.render_glossary_list(self.terms)
        self.assertEqual(listing.count("Read on Wikipedia"), 1)

    def test_panel_stays_open_for_keyboard(self):
        css = (ROOT / "templates" / "static" / "site.css").read_text(encoding="utf-8")
        self.assertIn(".gloss:focus-within .gloss-pop", css)

    def test_glossary_rows_use_canonical_hosts(self):
        for slug, (_, _, url) in build.load_glossary().items():
            if url:
                self.assertIsNotNone(build.site_name(url), f"{slug}: {url}")
        self.assertIsNone(build.site_name("http://en.wikipedia.org/wiki/Saros"))
        self.assertIsNone(build.site_name("https://example.com/saros"))

    def test_other_host_is_a_build_error(self):
        import tempfile
        saved, saved_errors = build.GLOSSARY_FILE, list(build.DATA_ERRORS)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "glossary.tsv"
            path.write_text("saros\tSaros\tA cycle.\thttps://example.com/saros\n", encoding="utf-8")
            try:
                build.GLOSSARY_FILE = path
                build.load_glossary()
                self.assertTrue(any("LNK-5" in e for e in build.DATA_ERRORS))
            finally:
                build.GLOSSARY_FILE = saved
                build.DATA_ERRORS[:] = saved_errors


class CorpusLinkTest(unittest.TestCase):
    """AT-LNK-2 to AT-LNK-6 over the corpus."""

    @classmethod
    def setUpClass(cls):
        cls.errors, cls.external = link_check.check(report=False)

    def test_nothing_left_to_link(self):
        rows = autolink.load_map()
        for page in sorted(CONTENT.rglob("*.md")):
            text = page.read_text(encoding="utf-8")
            self.assertEqual(autolink.plan(page, text, rows), [], page)

    def test_no_page_links_itself(self):
        for page in sorted(CONTENT.rglob("*.md")):
            internal, _, _ = link_check.page_links(page)
            for target, anchor, url in internal:
                if target == page.resolve():
                    self.assertTrue(anchor, f"{page}: {url}")

    def test_link_check_is_clean(self):
        self.assertEqual(self.errors, [])

    def test_external_links_are_https(self):
        for url in self.external:
            self.assertTrue(url.startswith("https://"), url)


class NewTabTest(unittest.TestCase):
    """AT-LNK-8: external links open a new tab, internal ones do not."""

    def test_external_only(self):
        html = build.open_external_in_new_tab(
            '<a href="https://en.wikipedia.org/wiki/Io_(moon)">Io</a> '
            '<a href="https://doi.org/10.1/x" rel="noreferrer">paper</a> '
            '<a href="../b.html#c">page</a> <a href="#ref-1">1</a>')
        self.assertIn('<a href="https://en.wikipedia.org/wiki/Io_(moon)" rel="noopener" target="_blank">', html)
        self.assertIn('rel="noreferrer noopener" target="_blank"', html)
        self.assertIn('<a href="../b.html#c">', html)
        self.assertIn('<a href="#ref-1">', html)

    def test_built_pages(self):
        site = ROOT / "site"
        if not site.is_dir():
            self.skipTest("no build")
        tag = re.compile(r"<a\b[^>]*>")
        for page in sorted(site.rglob("*.html")):
            for a in tag.findall(page.read_text(encoding="utf-8")):
                external = re.search(r'\bhref="https?://', a)
                self.assertEqual(bool(external), 'target="_blank"' in a, f"{page}: {a}")
                if external:
                    self.assertIn("noopener", a, f"{page}: {a}")


class ProtectedSpanTest(unittest.TestCase):
    """AT-LNK-7: the places a first-mention link must never go."""

    SAMPLE = "\n".join([
        "---",
        "title: Saros",
        "---",
        "## Saros in a heading",
        "",
        "![A caption naming the Saros and",
        "running over two lines](img/x.svg){.fig}",
        "",
        'Quoted: "the Saros of old". Code: `Saros`. Maths: $Saros$.',
        "Marked: [@cat-saros] [?saros] [the Saros](https://en.wikipedia.org/wiki/Saros_(astronomy)).",
        "",
        "Prose: the Saros at last.",
    ])

    def test_only_the_prose_mention_is_linked(self):
        page = CONTENT / "20-reports" / "sample.md"
        rows = [(re.compile(r"(?<![\w-])(?:Saros)(?![\w-])"),
                 "10-raw/20-solar-eclipses-and-transits/02-catalogs/enumerating-eclipses.md")]
        links = autolink.plan(page, self.SAMPLE, rows)
        self.assertEqual(len(links), 1)
        start, end, href = links[0]
        self.assertEqual(self.SAMPLE[start - 11:end], "Prose: the Saros")
        self.assertTrue(href.startswith("../10-raw/"), href)


if __name__ == "__main__":
    unittest.main()
