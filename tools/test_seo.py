"""Regression checks for published URLs and page-specific search metadata.

Run with: uv run --no-project python -m unittest discover -s tools -p test_seo.py
"""

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

import build
from check_seo import Metadata


class SearchMetadataTests(unittest.TestCase):
    def setUp(self):
        self.root = build.build_tree()
        self.nodes = list(build.walk(self.root))

    def test_home_uses_existing_published_filename(self):
        self.assertEqual(build.public_url(self.root), build.BASE_URL + "computing.html")
        self.assertIn('rel="canonical" href="' + build.public_url(self.root) + '"',
                      build.render_social(self.root))

    def test_internal_home_links_prefer_canonical_filename_offline(self):
        node = self.nodes[-1]
        self.assertEqual(self.root.url_from_root, build.HOME_FILENAME)
        home_href = 'href="' + build.rel_root(node.depth) + build.HOME_FILENAME + '"'
        self.assertIn(home_href, build.render_nav(self.root, node))
        self.assertIn(home_href, build.render_crumbs(node, self.root))
        template = (build.TEMPLATES / "page.html").read_text(encoding="utf-8")
        with patch.object(build, "pandoc_render", return_value=("", "<p>test</p>")), \
             patch.object(build, "render_reference_list", return_value=""):
            result = build.render_page(node, self.root, template, {}, set(), {}, set(), set())
        self.assertIn('class="brand" ' + home_href, result)
        self.assertIn('property="og:url" content="' + build.public_url(self.root) + '"',
                      build.render_social(self.root))

    def test_deep_page_address_uses_url_names(self):
        # URL-1: the canonical address drops the folders' number prefixes.
        node = next(n for n in self.nodes if n.rel.as_posix().endswith("besselian-elements"))
        self.assertEqual(build.public_url(node), build.BASE_URL +
                         "research-notes/shared/foundations/besselian-elements.html")

    def test_every_page_has_an_explicit_unique_search_title_and_description(self):
        titles = [n.meta.get("seo_title", "") for n in self.nodes]
        descriptions = [n.description for n in self.nodes]
        self.assertTrue(all(titles))
        self.assertTrue(all(descriptions))
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_home_names_calculation_and_algorithms(self):
        title = build.page_head_title(self.root).lower()
        for term in ("eclipse", "occultation", "transit", "calculation", "algorithms"):
            self.assertIn(term, title)

    def test_seo_2_home_names_transits(self):
        self.assertIn("transit", build.page_head_title(self.root).lower())
        self.assertIn("transits", self.root.description.lower())

    def test_seo_3_transit_pages_name_transits(self):
        pages = [n for n in self.nodes if "14-transits" in n.rel.as_posix()]
        self.assertGreaterEqual(len(pages), 4)
        for node in pages:
            self.assertIn("transit", node.meta["seo_title"].lower(), node.rel)

    def test_seo_4_website_structured_data_on_home_only(self):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            build.render_social(self.root), flags=re.S)
        self.assertEqual(len(blocks), 1)
        data = json.loads(blocks[0])
        self.assertEqual(data["@context"], "https://schema.org")
        self.assertEqual(data["@type"], "WebSite")
        self.assertEqual(data["name"], build.SITE_TITLE)
        self.assertIn("Computing Eclipses, Occultations and Transits", data["alternateName"])
        self.assertEqual(data["url"], build.public_url(self.root))
        self.assertEqual(data["description"], self.root.description)
        self.assertNotIn("application/ld+json", build.render_social(self.nodes[-1]))

    def test_social_and_document_titles_use_the_same_page_metadata(self):
        node = self.nodes[-1]
        self.assertIn('property="og:title" content="' +
                      build.html.escape(build.page_head_title(node)) + '"',
                      build.render_social(node))
        with patch.object(build, "pandoc_render", return_value=("", "<p>test</p>")), \
             patch.object(build, "render_reference_list", return_value=""):
            result = build.render_page(node, self.root, "<title>{{head_title}}</title>",
                                       {}, set(), {}, set(), set())
        self.assertEqual(result, "<title>" + build.html.escape(build.page_head_title(node)) + "</title>")

    def test_metadata_is_escaped(self):
        self.root.meta["seo_title"] = 'Calculation <guide> & "examples"'
        result = build.render_social(self.root)
        self.assertIn("Calculation &lt;guide&gt; &amp; &quot;examples&quot;", result)

    def test_sitemap_contains_each_canonical_once_and_no_aliases(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, "OUT", Path(tmp)):
            build.write_sitemap(self.nodes)
            path = Path(tmp) / "sitemap.xml"
            first = path.read_bytes()
            urls = [n.text for n in ET.fromstring(first).findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            self.assertEqual(urls, sorted(build.public_url(n) for n in self.nodes))
            self.assertEqual(len(urls), len(set(urls)))
            self.assertNotIn(build.BASE_URL + "index.html", urls)
            self.assertNotIn(build.BASE_URL, urls)
            build.write_sitemap(list(reversed(self.nodes)))
            self.assertEqual(first, path.read_bytes())

    def test_svg_accessibility_title_is_not_a_document_title(self):
        meta = Metadata()
        meta.feed('<html><head><title>Eclipse calculation</title></head>'
                  '<body><svg><title>Shadow geometry</title></svg></body></html>')
        self.assertEqual(meta.titles, ["Eclipse calculation"])

    def test_checker_still_reports_duplicate_document_titles(self):
        meta = Metadata()
        meta.feed('<html><head><title>One</title><title>Two</title></head></html>')
        self.assertEqual(meta.titles, ["One", "Two"])


if __name__ == "__main__":
    unittest.main()
