"""Where the site lives and what it is called, stated once and checked everywhere it is repeated."""

import unittest
from pathlib import Path

import build
import deploy

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = (ROOT / ".github" / "workflows" / "deploy-hetzner.yml").read_text(encoding="utf-8")

PUBLIC_BASE = "https://sankara.net/astro/eclipses/"
REMOTE_PATH = "/var/www/sankara.net/astro/eclipses/"
SITE_NAME = "Computing Eclipses, Occultations and Transits"


class SiteIdentityTest(unittest.TestCase):
    def test_build_publishes_under_the_eclipses_path(self):
        self.assertEqual(build.BASE_URL, PUBLIC_BASE)

    def test_local_deploy_targets_the_same_subtree(self):
        self.assertEqual(deploy.REMOTE_PATH, REMOTE_PATH)
        self.assertEqual(deploy.PUBLIC_URL, PUBLIC_BASE + "computing.html")

    def test_workflow_targets_the_same_subtree(self):
        self.assertIn(f"REMOTE_PATH: {REMOTE_PATH}", WORKFLOW)
        self.assertIn(f"PUBLIC_URL: {PUBLIC_BASE}computing.html", WORKFLOW)
        self.assertIn(f'test "$REMOTE_PATH" = "{REMOTE_PATH}"', WORKFLOW)
        self.assertNotIn("solar-eclipses", WORKFLOW)

    def test_site_name_and_smoke_checks_agree(self):
        self.assertEqual(build.SITE_TITLE, SITE_NAME)
        self.assertEqual(deploy.SMOKE_STRING, SITE_NAME)
        self.assertIn(f'grep -q "{SITE_NAME}"', WORKFLOW)

    def test_social_card_is_the_redrawn_one(self):
        self.assertEqual(build.SOCIAL_IMAGE, "img/social-card-v3.jpg")
        self.assertTrue((ROOT / "content" / build.SOCIAL_IMAGE).is_file())


if __name__ == "__main__":
    unittest.main()
