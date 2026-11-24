"""Curriculum order and common unittest adapter."""

from collections.abc import Iterator
from importlib import import_module
from types import ModuleType
import unittest

from koans import Exercise, Koan

TRACKS = {
    "python": ("references", "closures", "attributes", "streams", "scheduler", "rest_service"),
    "deep_learning": ("linear", "precision", "autodiff", "tensor", "attention"),
    "agents": ("protocol", "tools", "retrieval", "planning", "runtime", "providers", "workflow_graph", "grounded_qa", "webhooks"),
    "cross_track": ("diagnosis",),
}
STAGES = ("predict", "contrast", "implement", "break_cases", "transfer")


def load_module(track: str, name: str) -> ModuleType:
    return import_module(f"checks.{track}_{name}")


def load_exercise(track: str, name: str) -> ModuleType:
    return import_module(f"koans.{track}.{name}")


def _lesson(examples: ModuleType) -> type[Koan]:
    lessons = [
        value
        for value in vars(examples).values()
        if isinstance(value, type) and issubclass(value, Koan) and value.__module__ == examples.__name__
    ]
    if len(lessons) != 1 or len(lessons[0].steps()) < len(STAGES):
        raise ValueError(f"{examples.__name__} needs one Koan class with at least five test methods")
    return lessons[0]


def make_cases(
    check: ModuleType, examples: ModuleType, exercise: Exercise, stage: str
) -> Iterator[unittest.TestCase]:
    lesson = _lesson(examples)
    prediction, contrast, *construction, boundary, transfer = lesson.steps()
    groups = ((prediction,), (contrast,), tuple(construction), (boundary,), (transfer,))
    names = groups[STAGES.index(stage)]

    def build(name: str, verify: bool) -> unittest.TestCase:
        example = getattr(lesson, name)

        def test(self: unittest.TestCase) -> None:
            example(self)
            if verify:
                getattr(check, stage)(self, exercise)

        test.__doc__ = f"{examples.__name__.replace('.', '/')}.py · {stage}"
        case = type(lesson.__name__, (lesson,), {name: test, "__module__": lesson.__module__})
        return case(name)

    for name in names:
        yield build(name, verify=stage not in STAGES[:2] and name == names[-1])


def suite(track: str | None = None, module: str | None = None) -> Iterator[unittest.TestCase]:
    for track_name, names in TRACKS.items():
        if track is not None and track != track_name:
            continue
        for name in names:
            if module is not None and module != name:
                continue
            check = load_module(track_name, name)
            exercise = load_exercise(track_name, name)
            for stage in STAGES:
                yield from make_cases(check, exercise, exercise, stage)
