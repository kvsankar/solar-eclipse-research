"""House spelling: the site writes "catalogue"; proper names keep the source's "Catalog"."""

import unittest

from normalise_prose import process


class CatalogueSpellingTest(unittest.TestCase):
    def test_own_voice_uses_catalogue(self):
        self.assertEqual(process("The catalog lists them."), "The catalogue lists them.")

    def test_phrase_containing_eclipse_catalogue_is_left_alone(self):
        text = "seo_title: Solar Eclipse Catalogue Algorithms and Classification"
        self.assertEqual(process(text), text)

    def test_nasa_proper_names_keep_their_spelling(self):
        for name in ("Five Millennium Catalog", "Catalog of Solar Eclipses"):
            with self.subTest(name=name):
                self.assertEqual(process(f"See the {name}."), f"See the {name}.")


if __name__ == "__main__":
    unittest.main()
