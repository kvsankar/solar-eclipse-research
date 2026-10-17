"""The prose normaliser rewrites files only when called with no arguments."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import normalise_prose


class CommandLineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.page = root / "content" / "page.md"
        self.page.parent.mkdir()
        self.original = "The catalog is in the center.\n"
        self.page.write_text(self.original, encoding="utf-8")
        self.patches = [patch.object(normalise_prose, "ROOT", root),
                        patch.object(normalise_prose, "CONTENT", root / "content")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = normalise_prose.main(argv)
        return code, out.getvalue() + err.getvalue()

    def test_help_prints_usage_and_changes_nothing(self):
        code, output = self.run_main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--check", output)
        self.assertEqual(self.page.read_text(encoding="utf-8"), self.original)

    def test_unknown_argument_is_refused_and_changes_nothing(self):
        code, output = self.run_main(["--dry-run"])
        self.assertEqual(code, 2)
        self.assertIn("--dry-run", output)
        self.assertEqual(self.page.read_text(encoding="utf-8"), self.original)

    def test_check_reports_without_writing(self):
        code, output = self.run_main(["--check"])
        self.assertEqual(code, 0)
        self.assertIn("would change", output)
        self.assertEqual(self.page.read_text(encoding="utf-8"), self.original)

    def test_no_arguments_rewrites(self):
        code, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertNotEqual(self.page.read_text(encoding="utf-8"), self.original)


if __name__ == "__main__":
    unittest.main()
