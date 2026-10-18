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
    "Solar eclipse": "Both",
    "Transit of Mercury or Venus": "Both",
    "Lunar eclipse": "Darkened",
    "Eclipse of a satellite": "Darkened",
    "Shadow transit": "Darkened",
    "Mutual eclipse": "Darkened",
    "Lunar occultation of a star": "Hidden",
    "Lunar occultation of a planet": "Hidden",
    "Occultation by an asteroid or TNO": "Hidden",
    "Occultation of a satellite by its planet": "Hidden",
    "Transit of a satellite": "Hidden",
    "Mutual occultation": "Hidden",
    "Occultation of one planet by another": "Hidden",
}
CASES = {
    "Darkened": ("case-darkened.svg", [("Light source", "the Sun"), ("Blocking body", "the Earth"),
                                       ("Darkened body", "the Moon"), ("Observer", "on the Earth's night side")]),
    "Hidden": ("case-hidden.svg", [("Light source", "a star"), ("Blocking body", "the Moon"),
                                   ("Observer", "on the Earth")]),
    "Both": ("case-both.svg", [("Light source", "the Sun"), ("Blocking body", "the Moon"),
                               ("Observer", "on the Earth")]),
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
    "example-venus-transit.svg": ("Both", [("Light source", "the Sun"), ("Blocking body", "Venus"),
                                           ("Observer", "on the Earth")]),
}
STATIC = [c[0] for c in CASES.values()] + ["shadow-shape.svg"] + list(EXAMPLES)
FIG_SCRIPTS = ROOT / "tools" / "figures"
ANIMATED = ["anim-solar-eclipse.svg", "anim-lunar-eclipse.svg", "anim-io-orbit.svg"]


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

    def test_pri_1_first_page_and_the_three_cases(self):
        meta = front(self.text)
        self.assertEqual(meta["title"], "How eclipses, occultations and transits are computed")
        self.assertEqual(meta["order"], "1")
        for case in ("Darkened", "Hidden", "Both"):
            self.assertTrue(any(h.startswith(case) for h in self.secs), case)

    def test_pri_2_every_kind_classified_once_with_a_live_link(self):
        rows = re.findall(r"^\| ([^|]+?) \| (Both|Darkened|Hidden) \| \[[^]]+\]\(([^)]+)\) \|$",
                          self.text, flags=re.M)
        found = {name: case for name, case, _ in rows}
        self.assertEqual(found, KINDS)
        for _, _, link in rows:
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
        self.assertIn(".figsvg .sun-fill", css)
        for script in FIG_SCRIPTS.glob("prim_*.py"):
            src = script.read_text(encoding="utf-8")
            for line in src.splitlines():
                if "accent-fill" in line:
                    self.assertNotRegex(line.lower(), r"sun|sx, sy|# the source as seen", f"{script.name}: {line}")

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
