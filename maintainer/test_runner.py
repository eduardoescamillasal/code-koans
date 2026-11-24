"""Regression checks for the learner CLI entry point."""

from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def run_cli(self, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "contemplate.py", *args],
            cwd=cwd,
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
        self.assertNotIn("test_shallow_copies_share_their_children", result.stderr)

    def test_selected_module(self):
        result = self.run_cli("agents", "runtime")
        self.assertEqual(result.returncode, 1)
        self.assertIn("koans/agents/runtime.py · predict", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_invalid_selection(self):
        result = self.run_cli("python", "runtime")
        self.assertEqual(result.returncode, 2)
        self.assertIn("choose a module from", result.stderr)

    def test_local_observations_lead_to_targeted_todo(self) -> None:
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for directory in ("checks", "koans"):
                shutil.copytree(ROOT / directory, root / directory,
                                ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(ROOT / "contemplate.py", root / "contemplate.py")
            learner = root / "koans/python/closures.py"
            source = learner.read_text()
            learner.write_text(source.replace("self.assertEqual(__,", "self.assertEqual((7, 7, 7),", 1))
            contrast = self.run_cli("python", "closures", cwd=root)
            self.assertIn("closures.py · contrast ... FAIL", contrast.stderr)
            self.assertIn("Ran 2 tests", contrast.stderr)

            learner.write_text(learner.read_text().replace("self.assertEqual(__,", "self.assertEqual((7, 7),", 1))
            scaffold = self.run_cli("python", "closures", cwd=root)
            self.assertEqual(scaffold.returncode, 1)
            self.assertIn("closures.py · implement ... FAIL", scaffold.stderr)
            self.assertIn("Implement build a hashable key", scaffold.stderr)
            self.assertIn("Ran 3 tests", scaffold.stderr)
