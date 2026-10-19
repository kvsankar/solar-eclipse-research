"""Acceptance tests AT-PRI-1 to AT-PRI-6 and AT-FIG-1 to AT-FIG-3 (docs/acceptance-tests.md)."""

import html
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIMER = ROOT / "content" / "05-primer"
GENERAL = PRIMER / "how-eclipses-occultations-and-transits-are-computed.md"
WORKED = PRIMER / "worked-example-solar-eclipse.md"
IMG = PRIMER / "img"

KINDS = {
    "Solar eclipse": ("Hidden", "disc"),
    "Transit of Mercury or Venus": ("Hidden", "disc"),
    "Lunar occultation of a star": ("Hidden", "point"),
    "Lunar occultation of a planet": ("Hidden", "disc"),
    "Occultation by an asteroid or TNO": ("Hidden", "point"),
    "Occultation of a satellite by its planet": ("Hidden", "disc"),
    "Transit of a satellite": ("Hidden", "disc"),
    "Mutual occultation": ("Hidden", "disc"),
    "Occultation of one planet by another": ("Hidden", "disc"),
    "Lunar eclipse": ("Darkened", "disc"),
    "Eclipse of a satellite": ("Darkened", "disc"),
    "Shadow transit": ("Darkened", "disc"),
    "Mutual eclipse": ("Darkened", "disc"),
}
CASES = {
    "Hidden": ("case-hidden.svg", [("Light source", "a star"), ("Blocking body", "the Moon"),
                                   ("Observer", "on the Earth")]),
    "Darkened": ("case-darkened.svg", [("Light source", "the Sun"), ("Blocking body", "the Earth"),
                                       ("Darkened body", "the Moon"), ("Observer", "on the Earth's night side")]),
}
EXAMPLES = {
    "example-satellite-eclipse.svg": ("Darkened", [("Light source", "the Sun"), ("Blocking body", "Jupiter"),
                                                   ("Darkened body", "Io, in Jupiter's shadow"),
                                                   ("Observer", "on the Earth")]),
    "example-shadow-transit.svg": ("Darkened", [("Light source", "the Sun"), ("Blocking body", "Io"),
                                                ("Darkened body", "Jupiter's cloud tops, a patch"),
                                                ("Observer", "on the Earth")]),
    "example-satellite-occultation.svg": ("Hidden", [("Light source", "the Sun"), ("Lit body", "Io"),
                                                     ("Blocking body", "Jupiter"), ("Observer", "on the Earth")]),
    "example-asteroid-occultation.svg": ("Hidden", [("Light source", "a star"), ("Blocking body", "an asteroid"),
                                                    ("Observer", "on the Earth, in the shadow path")]),
    "example-solar-eclipse.svg": ("Hidden", [("Light source", "the Sun"), ("Blocking body", "the Moon"),
                                             ("Observer", "on the Earth")]),
    "example-venus-transit.svg": ("Hidden", [("Light source", "the Sun"), ("Blocking body", "Venus"),
                                             ("Observer", "on the Earth")]),
}
STATIC = [c[0] for c in CASES.values()] + ["shadow-shape.svg"] + list(EXAMPLES)
FIG_SCRIPTS = ROOT / "tools" / "figures"
ANIMATED = ["anim-solar-eclipse.svg", "anim-lunar-eclipse.svg", "anim-io-orbit.svg"]


def inside_with_margin(poly, x, y, margin):
    """True when (x, y) is inside the polygon and at least margin from every edge."""
    inside = False
    n = len(poly)
    for k in range(n):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
        dx, dy = x2 - x1, y2 - y1
        t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy or 1)))
        if ((x - x1 - t * dx) ** 2 + (y - y1 - t * dy) ** 2) ** 0.5 < margin:
            return False
    return inside


def front(text):
    block = text.split("---", 2)[1]
    return dict(re.findall(r"^(\w+):\s*(.*)$", block, flags=re.M))


def sections(text):
    """Map each ## heading to the text under it."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


class GeneralPrimerTest(unittest.TestCase):
    def setUp(self):
        self.text = GENERAL.read_text(encoding="utf-8")
        self.secs = sections(self.text)

    def test_pri_1_first_page_and_the_two_cases(self):
        meta = front(self.text)
        self.assertEqual(meta["title"], "How eclipses, occultations and transits are computed")
        self.assertEqual(meta["order"], "1")
        for case in ("Hidden", "Darkened"):
            self.assertTrue(any(h.startswith(case) for h in self.secs), case)
        self.assertFalse(any(h.startswith("Both") for h in self.secs))

    def test_pri_2_every_kind_classified_once_with_a_live_link(self):
        rows = re.findall(r"^\| ([^|]+?) \| (Darkened|Hidden) \| (point|disc) \| \[[^]]+\]\(([^)]+)\) \|$",
                          self.text, flags=re.M)
        found = {name: (case, src) for name, case, src, _ in rows}
        self.assertEqual(found, KINDS)
        for _, _, _, link in rows:
            self.assertTrue((PRIMER / link).resolve().is_file(), link)

    def test_pri_3_shadow_shape_vocabulary(self):
        shape = self.secs["The shape of a shadow"]
        for word in ("umbra", "penumbra", "antumbra", "total", "partial", "annular", "cylinder"):
            self.assertIn(word, shape)

    def test_pri_4_supplement_terms_cited(self):
        names = self.secs["How the Explanatory Supplement names them"]
        for term in ("eclipse", "occultation", "transit", "shadow transit"):
            self.assertIn(f"**{term}**", names)
        self.assertIn("[@prim-es1992-terms]", names)

    def test_pri_7_terminology_explains_the_site_name(self):
        names = " ".join(self.secs["How the Explanatory Supplement names them"].split())
        self.assertIn("Computing Eclipses and Occultations", names)
        self.assertIn("a transit is an occultation", names.lower())
        self.assertIn("Eclipses, Occultations, and Transits", names)

    def test_s3d_1_case_diagrams_offer_3d_scenes(self):
        for svg, scene in (("case-hidden.svg", "hidden-cases"), ("case-darkened.svg", "darkened-cases")):
            self.assertIn(f'(img/{svg}){{.fig3d scene="{scene}"}}', self.text)
        import build  # the page as the build renders it, wrappers included
        node = next(n for n in build.walk(build.build_tree()) if n.src == GENERAL)
        _, body = build.pandoc_render(build.strip_leading_h1(node.body_md, node.title), False)
        body = build.inline_svgs(build.rewrite_links(body), node)
        for scene in ("hidden-cases", "darkened-cases"):
            self.assertEqual(body.count(f'<div class="fig3d-host" data-scene="{scene}">'), 1, scene)

    def test_pri_5_ends_with_the_way_on(self):
        last = list(self.secs)[-1]
        self.assertEqual(last, "Where to go next")
        body = self.secs[last]
        for target in ("worked-example-solar-eclipse.md", "glossary.md",
                       "../10-raw/_index.md", "../20-reports/_index.md"):
            self.assertIn(f"]({target})", body)


class WorkedExampleTest(unittest.TestCase):
    def test_pri_6_title_order_and_other_events(self):
        text = WORKED.read_text(encoding="utf-8")
        meta = front(text)
        self.assertEqual(meta["title"], "Worked example: a solar eclipse")
        self.assertEqual(meta["order"], "2")
        secs = sections(text)
        last = list(secs)[-1]
        self.assertEqual(last, "What changes for other events")
        body = secs[last]
        for event, link in (("lunar eclipse", "30-lunar-eclipses/_index.md"),
                            ("occultation", "13-lunar-occultations/_index.md"),
                            ("transit", "14-transits/_index.md")):
            self.assertIn(event, body.lower())
            self.assertIn(link, body)


class PrimerFigureTest(unittest.TestCase):
    def setUp(self):
        self.text = GENERAL.read_text(encoding="utf-8")
        self.prov = (PRIMER / "images.tsv").read_text(encoding="utf-8")

    def test_fig_1_figures_embedded_with_provenance(self):
        for name in STATIC + ANIMATED:
            self.assertIn(f"(img/{name})", self.text, name)
            self.assertIn(f"05-primer/img/{name}\t", self.prov, name)

    def test_fig_1_case_diagrams_lead_their_sections_with_two_labels(self):
        secs = sections(self.text)
        for case, (name, labels) in CASES.items():
            sec = next(v for k, v in secs.items() if k.startswith(case))
            first = re.search(r"!\[[^\]]*\]\(img/([^)]+)\)", sec, flags=re.S).group(1)
            self.assertEqual(first, name, case)
            svg = (IMG / name).read_text(encoding="utf-8")
            visible = [html.unescape(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg)]
            for role, body in labels:
                self.assertIn(role, visible, (name, role))
                self.assertIn(body, visible, (name, body))

    def test_fig_1_examples_in_their_sections_with_two_labels(self):
        secs = sections(self.text)
        self.assertNotIn("gallery-", self.text)
        for name, (case, labels) in EXAMPLES.items():
            sec = next(v for k, v in secs.items() if k.startswith(case))
            self.assertIn(f"(img/{name})", sec, name)
            svg = (IMG / name).read_text(encoding="utf-8")
            visible = [html.unescape(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg)]
            for role, body in labels:
                self.assertIn(role, visible, (name, role))
                self.assertIn(body, visible, (name, body))

    def test_fig_7_sun_colour(self):
        css = (ROOT / "templates" / "static" / "site.css").read_text(encoding="utf-8")
        self.assertGreaterEqual(css.count("--fig-sun:"), 3)
        self.assertGreaterEqual(css.count("--fig-silhouette:"), 3)
        self.assertIn(".figsvg .sun-fill", css)
        self.assertIn(".figsvg .silhouette-fill", css)
        for script in FIG_SCRIPTS.glob("prim_*.py"):
            self.assertNotIn("sky-fill", script.read_text(encoding="utf-8"), script.name)
        for script in FIG_SCRIPTS.glob("prim_*.py"):
            src = script.read_text(encoding="utf-8")
            for line in src.splitlines():
                if "accent-fill" in line:
                    self.assertNotRegex(line.lower(), r"sun|sx, sy|# the source as seen", f"{script.name}: {line}")

    def test_fig_8_observer_inside_the_stated_shadow(self):
        for name, cls in (("example-solar-eclipse.svg", "cone-deep"), ("example-venus-transit.svg", "cone")):
            svg = (IMG / name).read_text(encoding="utf-8")
            obs = re.search(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="[\d.]+" class="accent-2-fill"', svg)
            ox, oy = float(obs.group(1)), float(obs.group(2))
            polys = [[tuple(map(float, pt.split(","))) for pt in m.split()]
                     for m in re.findall(rf'<polygon points="([^"]+)" class="{cls}"', svg)]
            self.assertTrue(any(inside_with_margin(pg, ox, oy, 4) for pg in polys), name)
        svg = (IMG / "example-solar-eclipse.svg").read_text(encoding="utf-8")
        suns = re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" class="sun-fill"', svg)
        sils = re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" class="silhouette-fill"', svg)
        self.assertTrue(any(cx == sx and cy == sy and float(r2) >= float(r1)
                            for sx, sy, r1 in suns for cx, cy, r2 in sils),
                        "the inset's silhouette covers the whole Sun")

    def test_fig_2_each_figure_says_schematic(self):
        for name in STATIC + ANIMATED:
            svg = (IMG / name).read_text(encoding="utf-8")
            visible = " ".join(re.findall(r"<text[^>]*>([^<]*)</text>", svg))
            self.assertIn("Schematic", visible, name)

    def test_fig_3_animations_wait_for_play(self):
        for name in ANIMATED:
            self.assertIn(f"(img/{name}){{.anim}}", self.text, name)
            svg = (IMG / name).read_text(encoding="utf-8")
            anims = re.findall(r"<(animate|animateTransform|animateMotion|set)\b[^>]*>", svg)
            self.assertTrue(anims, name)
            for tag in re.findall(r"<(?:animate|animateTransform|animateMotion|set)\b[^>]*>", svg):
                self.assertIn('begin="indefinite"', tag, name)


if __name__ == "__main__":
    unittest.main()
