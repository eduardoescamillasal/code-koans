"""Validate each inline lesson and each project stage against their fixtures."""

from importlib import import_module
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from checks import PROJECT_STAGES, TRACKS, lesson_cases, load_exercise, load_module, project_case
from koans import __
from maintainer.lesson_answers import ANSWERS


def outcome(case: unittest.TestCase) -> tuple[str, str]:
    result = unittest.TestResult()
    result.failfast = True
    case.run(result)
    if result.errors:
        return "error", result.errors[0][1]
    if result.failures:
        return "failure", result.failures[0][1]
    return "pass", ""


def try_answers(case: unittest.TestCase, guesses: tuple[object, ...]) -> tuple[str, str]:
    """Fill the assertion arguments in order without editing lesson source."""
    assert_equal = case.assertEqual
    guessed = iter(guesses)
    consumed = 0

    def compare(first: object, second: object, msg: str | None = None) -> None:
        nonlocal consumed
        if first is __:
            consumed += 1
            first = next(guessed, __)
        assert_equal(first, second, msg)

    with patch.object(case, "assertEqual", compare):
        status, detail = outcome(case)
    if status == "pass" and consumed != len(guesses):
        return "error", f"found {consumed} blanks for {len(guesses)} supplied answers"
    return status, detail


def validate() -> int:
    failures: list[str] = []
    lessons = projects = 0

    def verify(
        label: str, result: tuple[str, str], expected: str, marker: str = ""
    ) -> None:
        actual, detail = result
        if actual != expected or marker not in detail:
            failures.append(f"{label}: expected {expected}, got {actual}\n{detail}")

    for track, names in TRACKS.items():
        for name in names:
            key = f"{track}_{name}"
            check = load_module(track, name)
            starter = load_exercise(track, name)
            solution = import_module(f"maintainer.references.{key}")
            mutants = import_module(f"maintainer.mutants.{key}").CASES

            for index, case in enumerate(lesson_cases(starter)):
                method = case.id().rsplit(".", 1)[-1]
                if index < 2:
                    stage, field = (("predict", "prediction"), ("contrast", "contrast"))[index]
                    right, wrong = (getattr(solution, field),), (mutants[stage][field],)
                else:
                    right, wrong = ANSWERS[key][method]
                label = f"{key}/{method}"
                verify(f"{label} (starter)", outcome(case), "failure", repr(__))
                verify(f"{label} (reference)", try_answers(case, right), "pass")
                verify(f"{label} (wrong answers)", try_answers(case, wrong), "failure")
                lessons += 1

            for stage in PROJECT_STAGES:
                altered = SimpleNamespace(**{**vars(solution), **mutants[stage]})
                label = f"{key}/{stage}"
                verify(f"{label} (starter)", outcome(project_case(check, starter, stage)),
                       "failure", "Implement ")
                verify(f"{label} (reference)", outcome(project_case(check, solution, stage)), "pass")
                verify(f"{label} (mutant)", outcome(project_case(check, altered, stage)), "failure")
                projects += 1

    for failure in failures:
        print(failure)
    if failures:
        return 1
    print(f"Validated {lessons} inline koans and {projects} project stages against starter, reference, and mutant.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
