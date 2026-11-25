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
PROJECT_STAGES = ("implement", "break_cases", "transfer")


def load_module(track: str, name: str) -> ModuleType:
    return import_module(f"checks.{track}_{name}")


def load_exercise(track: str, name: str) -> ModuleType:
    return import_module(f"koans.{track}.{name}")


def lesson_cases(exercise: ModuleType) -> Iterator[Koan]:
    lessons = [
        value
        for value in vars(exercise).values()
        if isinstance(value, type) and issubclass(value, Koan) and value.__module__ == exercise.__name__
    ]
    if len(lessons) != 1 or not lessons[0].steps():
        raise ValueError(f"{exercise.__name__} needs one Koan class with test methods")
    lesson = lessons[0]
    for name in lesson.steps():
        yield lesson(name)


def project_case(check: ModuleType, exercise: Exercise, stage: str) -> unittest.TestCase:
    def test(self: unittest.TestCase) -> None:
        getattr(check, stage)(self, exercise)

    name = f"test_{stage}"
    case = type(check.__name__.split(".")[-1], (unittest.TestCase,), {
        name: test,
        "__module__": check.__name__,
    })
    return case(name)


def suite(track: str | None = None, module: str | None = None) -> Iterator[unittest.TestCase]:
    for track_name, names in TRACKS.items():
        if track is not None and track != track_name:
            continue
        for name in names:
            if module is not None and module != name:
                continue
            exercise = load_exercise(track_name, name)
            yield from lesson_cases(exercise)
            check = load_module(track_name, name)
            for stage in PROJECT_STAGES:
                yield project_case(check, exercise, stage)
