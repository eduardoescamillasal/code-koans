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
        self.assertIn("test_two_names_share_the_same_list", result.stderr)
        self.assertIn("__ (fill in your prediction) != (True, 2)", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)
        self.assertNotIn("test_shallow_copies_share_their_children", result.stderr)

    def test_selected_module(self):
        result = self.run_cli("agents", "runtime")
        self.assertEqual(result.returncode, 1)
        self.assertIn("test_parsing_document_roles_can_inherit_authority", result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_invalid_selection(self):
        result = self.run_cli("python", "runtime")
        self.assertEqual(result.returncode, 2)
        self.assertIn("choose a module from", result.stderr)

    def test_multiple_blanks_in_one_method_precede_the_project(self) -> None:
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for directory in ("checks", "koans"):
                shutil.copytree(ROOT / directory, root / directory,
                                ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(ROOT / "contemplate.py", root / "contemplate.py")
            learner = root / "koans/python/closures.py"

            def fill(*answers: object) -> None:
                source = learner.read_text()
                for answer in answers:
                    source = source.replace("self.assertEqual(__,", f"self.assertEqual({answer!r},", 1)
                learner.write_text(source)

            fill((7, 7, 7), (7, 7))
            next_method = self.run_cli("python", "closures", cwd=root)
            self.assertIn("test_defaults_capture_values_while_closures_read_cells", next_method.stderr)
            self.assertIn("__ (fill in your prediction) != 5", next_method.stderr)
            self.assertIn("Ran 3 tests", next_method.stderr)

            fill(5)
            same_method = self.run_cli("python", "closures", cwd=root)
            self.assertIn("test_defaults_capture_values_while_closures_read_cells", same_method.stderr)
            self.assertIn("__ (fill in your prediction) != 2", same_method.stderr)
            self.assertIn("Ran 3 tests", same_method.stderr)

            fill(2, False, True, False, "dosage", "Scale the measurement.", True)
            project = self.run_cli("python", "closures", cwd=root)
            self.assertEqual(project.returncode, 1)
            self.assertIn("Implement build a hashable key", project.stderr)
            self.assertIn("Ran 6 tests", project.stderr)
