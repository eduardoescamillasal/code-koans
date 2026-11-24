"""Check every stage against its starter, reference, and targeted wrong answer."""

from importlib import import_module
from types import SimpleNamespace
import unittest

from checks import STAGES, TRACKS, load_module, make_case
from koans import __


def outcome(check, exercise, stage):
    result = unittest.TestResult()
    make_case(check, exercise, stage).run(result)
    if result.errors:
        return "error", result.errors[0][1]
    if result.failures:
        return "failure", result.failures[0][1]
    return "pass", ""


def validate():
    failures = []
    verified = 0
    for track, names in TRACKS.items():
        for name in names:
            key = f"{track}_{name}"
            check = load_module(track, name)
            starter = import_module(f"koans.{track}.{name}")
            solution = import_module(f"maintainer.references.{key}")
            mutants = import_module(f"maintainer.mutants.{key}").CASES
            for stage in STAGES:
                altered = SimpleNamespace(**{**vars(solution), **mutants[stage]})
                for label, candidate, expected, marker in (
                    ("starter", starter, "failure", repr(__) if stage in STAGES[:2] else "Implement "),
                    ("reference", solution, "pass", ""),
                    ("mutant", altered, "failure", ""),
                ):
                    actual, detail = outcome(check, candidate, stage)
                    if actual != expected or marker not in detail:
                        failures.append(f"{key}/{stage} ({label}): expected {expected}, got {actual}\n{detail}")
                verified += 1
    for failure in failures:
        print(failure)
    if failures:
        return 1
    print(f"Validated {verified} stages against starter, reference, and mutant.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
