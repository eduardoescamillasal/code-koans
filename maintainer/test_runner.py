"""Regression checks for the learner CLI entry point."""

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "contemplate.py", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_default_reports_only_first_starter_failure(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("koans/python/references.py · predict", result.stderr)
        self.assertIn("__ (fill in your prediction) != (True, 2)", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)
        self.assertNotIn("test_contrast", result.stderr)

    def test_selected_module(self):
        result = self.run_cli("agents", "runtime")
        self.assertEqual(result.returncode, 1)
        self.assertIn("koans/agents/runtime.py · predict", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_invalid_selection(self):
        result = self.run_cli("python", "runtime")
        self.assertEqual(result.returncode, 2)
        self.assertIn("choose a module from", result.stderr)
