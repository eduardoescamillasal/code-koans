"""Curriculum order and common unittest adapter."""

from importlib import import_module
import unittest

TRACKS = {
    "python": ("references", "closures", "attributes", "streams", "scheduler", "rest_service"),
    "deep_learning": ("linear", "precision", "autodiff", "tensor", "attention"),
    "agents": ("protocol", "tools", "retrieval", "planning", "runtime", "providers", "workflow_graph", "grounded_qa", "webhooks"),
    "cross_track": ("diagnosis",),
}
STAGES = ("predict", "contrast", "implement", "break_cases", "transfer")


def load_module(track, name):
    return import_module(f"checks.{track}_{name}")


def make_case(check, exercise, stage):
    def test(self):
        getattr(check, stage)(self, exercise)

    test.__name__ = f"test_{stage}"
    module_name = getattr(exercise, "__name__", "")
    label = module_name.replace(".", "/") + ".py" if module_name.startswith("koans.") else check.__name__
    test.__doc__ = f"{label} · {stage}"
    case = type(check.__name__.split(".")[-1], (unittest.TestCase,), {test.__name__: test})
    return case(test.__name__)


def suite(track=None, module=None):
    for track_name, names in TRACKS.items():
        if track is not None and track != track_name:
            continue
        for name in names:
            if module is not None and module != name:
                continue
            check = load_module(track_name, name)
            exercise = import_module(f"koans.{track_name}.{name}")
            for stage in STAGES:
                yield make_case(check, exercise, stage)
