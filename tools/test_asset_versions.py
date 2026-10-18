"""Pages request their stylesheet and scripts with a content hash, so a CDN or
browser cache can never pair a new page with an old stylesheet."""

import hashlib
import re
import unittest
from pathlib import Path

import build

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")


class AssetVersionTest(unittest.TestCase):
    def test_version_is_a_hash_of_the_file(self):
        for name in ("site.css", "site.js", "site3d.js"):
            want = hashlib.sha256((ROOT / "templates" / "static" / name).read_bytes()).hexdigest()[:10]
            self.assertEqual(build.asset_version(name), want)

    def test_template_requests_versioned_assets(self):
        for name in ("site.css", "site.js", "site3d.js"):
            refs = re.findall(r'assets/' + re.escape(name) + r'([^"]*)"', TEMPLATE)
            self.assertTrue(refs, name)
            for tail in refs:
                self.assertRegex(tail, r"^\?v=\{\{v_[a-z0-9]+\}\}$", name)


if __name__ == "__main__":
    unittest.main()
