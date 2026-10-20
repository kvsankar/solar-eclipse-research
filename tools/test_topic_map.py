"""Acceptance tests AT-MAP-1, -2, -3, -5, -6 and -7 (docs/acceptance-tests.md):
the topic map."""

import re
import unittest
from pathlib import Path

import build
import topic_map

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PAGE = CONTENT / "00-meta" / "topic-map.md"
LINK = re.compile(r"\]\(([^)\s#]+?\.md)(?:#[^)\s]*)?\)")


def expected_topics() -> set[str]:
    """Each research-notes folder of pages, and each page of the other
    sections, except the map page itself."""
    keys = set()
    for d in sorted((CONTENT / "10-raw").rglob("*")):
        if not d.is_dir() or not any(d.glob("*.md")):
            continue
        if any(c.is_dir() and any(c.rglob("*.md")) for c in d.iterdir()):
            continue
        keys.add(d.relative_to(CONTENT).as_posix())
    for section in ("00-meta", "05-primer", "20-reports"):
        for md in (CONTENT / section).glob("*.md"):
            if md.name != "_index.md" and md != PAGE:
                keys.add(md.relative_to(CONTENT).with_suffix("").as_posix())
    return keys


def owner(path: Path, keys: set[str]) -> str | None:
    rel = path.relative_to(CONTENT).with_suffix("").as_posix()
    if rel in keys:
        return rel
    parent = path.parent.relative_to(CONTENT).as_posix()
    return parent if parent in keys else None


class TopicMapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = build.build_tree()
        cls.here = next(n for n in build.walk(cls.root)
                        if n.src is not None and n.src.resolve() == PAGE.resolve())
        cls.data = topic_map.topic_map(cls.root, cls.here)
        cls.html = topic_map.render_topic_map(cls.root, cls.here)
        cls.svg = cls.html[cls.html.index("<svg"):cls.html.index("</svg>")]

    def test_page_in_meta(self):
        # AT-MAP-1
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("title: Topic map", text)
        self.assertIn(topic_map.MARKER, text)
        self.assertEqual(self.html.count('<svg class="tm"'), 1)

    def test_every_topic_once(self):
        # AT-MAP-1
        keys = [l.key for l in self.data["leaves"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(set(keys), expected_topics())
        for l in self.data["leaves"]:
            self.assertEqual(self.svg.count(f'id="{topic_map.node_id(l)}"'), 1, l.key)

    def test_every_node_is_a_link_that_resolves(self):
        # AT-MAP-2
        urls = {n.url_from_root for n in build.walk(self.root)}
        hrefs = re.findall(r'<a class="tm-node[^"]*" id="[^"]+" href="([^"]+)"', self.svg)
        self.assertEqual(len(hrefs), self.svg.count('<a class="tm-node'))
        prefix = "../" * self.here.depth
        for h in hrefs:
            self.assertTrue(h.startswith(prefix), h)
            self.assertIn(h[len(prefix):], urls)

    def test_curves_count_the_links(self):
        # AT-MAP-3: recount the links between topics, independently.
        keys = expected_topics()
        counts: dict[tuple[str, str], int] = {}
        for md in sorted(CONTENT.rglob("*.md")):
            a = owner(md, keys)
            if a is None:
                continue
            for m in LINK.finditer(md.read_text(encoding="utf-8")):
                target = (md.parent / m.group(1)).resolve()
                if not target.is_file():
                    continue
                b = owner(target, keys)
                if b is None or b == a:
                    continue
                pair = tuple(sorted((a, b)))
                counts[pair] = counts.get(pair, 0) + 1
        self.assertEqual(self.data["edges"], counts)
        self.assertTrue(counts)
        widths = {}
        for w, sw in re.findall(r'data-w="(\d+)" style="stroke-width:([\d.]+)"', self.svg):
            widths.setdefault(int(w), float(sw))
        self.assertEqual(sum(1 for _ in re.finditer(r"data-w=", self.svg)), len(counts))
        ordered = [widths[w] for w in sorted(widths)]
        self.assertEqual(ordered, sorted(ordered))
        self.assertLess(ordered[0], ordered[-1])

    def test_table_lists_topics_and_pages(self):
        # AT-MAP-5
        table = self.html[self.html.index('<table class="tm-table"'):]
        self.assertEqual(table.count("<tr id="), len(self.data["leaves"]))
        for l in self.data["leaves"]:
            pages = [n for n in topic_map.walk_nodes(l.node) if n.src is not None]
            for p in pages:
                if p is l.node and l.node.is_dir:
                    continue
                self.assertIn(p.url_from_root + '"', table, p.rel)

    def test_deterministic_and_themed(self):
        # AT-MAP-6
        again = topic_map.render_topic_map(self.root, self.here)
        self.assertEqual(self.html, again)
        self.assertNotRegex(self.svg, r"#[0-9a-fA-F]{3,6}\b|rgb\(|fill=\"|stroke=\"")
        css = (ROOT / "templates" / "static" / "site.css").read_text(encoding="utf-8")
        for rule in (".tm-links path", ".tm-node circle", ".tm-node text"):
            block = css[css.index(rule):]
            self.assertIn("var(--fig-", block[:block.index("}")], rule)

    def test_home_links_the_map(self):
        # AT-MAP-7
        home = (CONTENT / "_index.md").read_text(encoding="utf-8")
        self.assertIn("(00-meta/topic-map.md)", home)


if __name__ == "__main__":
    unittest.main()
