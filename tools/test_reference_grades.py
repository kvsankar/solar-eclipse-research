"""One source, one evidence grade, whichever topic cites it.

Each topic keeps its own prefixed slug for a source it shares with other
topics, so the same artefact can appear under several slugs. The grade must
still agree, because it states what the artefact is, not what a topic read.
"""

import collections
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pages that host several distinct works, cited each under its own title.
MULTI_WORK_URLS = {
    "https://eclipse.gsfc.nasa.gov/LEcat5/shadow.html",
    "https://ssd.jpl.nasa.gov/sats/ephem/sep.html",
    "https://www.willbell.com",
    "https://www.projectpluto.com/books.htm",
}

# The same work cited at different URLs.
SAME_WORK = {
    "Meeus, Astronomical Algorithms": [
        "bes-meeus-aa", "cat-meeus-1991-aa", "earth-meeus-aa", "jup-meeus-1998-ch44",
        "loc-meeus-aa-1998", "moon-meeus-1998", "sun-meeus-aa",
    ],
    "Meeus, Elements of Solar Eclipses 1951-2200": [
        "bes-meeus-1989", "cat-meeus-1989-elements", "earth-meeus-elements",
        "glob-meeus-1989", "loc-meeus-elements-1989",
    ],
    "Stephenson, Morrison and Hohenkerk 2016": ["cat-stephenson-2016", "earth-smh2016"],
}


def references():
    rows = {}
    for frag in sorted((ROOT / "content").rglob("refs.tsv")):
        for line in frag.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                cols = line.split("\t")
                rows[cols[0].strip()] = (cols[1].strip(), cols[3].strip())
    return rows


class ReferenceGradeTest(unittest.TestCase):
    def test_one_url_one_grade(self):
        by_url = collections.defaultdict(dict)
        for slug, (grade, url) in references().items():
            key = url.rstrip("/").split("#")[0]
            if key not in MULTI_WORK_URLS:
                by_url[key][slug] = grade
        conflicts = {u: g for u, g in by_url.items() if len(set(g.values())) > 1}
        self.assertEqual(conflicts, {})

    def test_one_work_one_grade(self):
        rows = references()
        for work, slugs in SAME_WORK.items():
            with self.subTest(work=work):
                grades = {s: rows[s][0] for s in slugs}
                self.assertEqual(len(set(grades.values())), 1, grades)


if __name__ == "__main__":
    unittest.main()
