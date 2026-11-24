"""Curriculum order and common unittest adapter."""

from collections.abc import Iterator
from importlib import import_module
from types import ModuleType
import unittest

from koans import Exercise

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


def make_case(check: ModuleType, examples: ModuleType, exercise: Exercise, stage: str) -> unittest.TestCase:
    def test(self: unittest.TestCase) -> None:
        if stage in ("predict", "contrast"):
            observe = getattr(examples, stage)
            answer = "prediction" if stage == "predict" else "contrast"
            if exercise is examples:
                observe(self)
            else:
                observe(self, getattr(exercise, answer))
            return
        if stage == "implement":
            examples.practice(self, exercise)
        elif stage == "break_cases":
            examples.practice_break(self, exercise)
        elif stage == "transfer":
            examples.practice_transfer(self, exercise)
        getattr(check, stage)(self, exercise)

    test.__name__ = f"test_{stage}"
    module_name = getattr(exercise, "__name__", "")
    label = module_name.replace(".", "/") + ".py" if module_name.startswith("koans.") else check.__name__
    test.__doc__ = f"{label} · {stage}"
    case = type(check.__name__.split(".")[-1], (unittest.TestCase,), {test.__name__: test})
    return case(test.__name__)


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
                yield make_case(check, exercise, exercise, stage)
