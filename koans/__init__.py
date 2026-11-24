"""Markers for incomplete predictions and unfinished code."""

from types import ModuleType, SimpleNamespace
from typing import Never
from unittest import TestCase

Exercise = ModuleType | SimpleNamespace


class Koan(TestCase):
    """A lesson whose cases run in the order in which they are written."""

    @classmethod
    def steps(cls) -> tuple[str, ...]:
        return tuple(name for name in vars(cls) if name.startswith("test_"))


class _Blank:
    def __repr__(self) -> str:
        return "__ (fill in your prediction)"


__ = _Blank()


def todo(task: str) -> Never:
    """Stop at the first missing implementation step."""
    raise AssertionError(f"Implement {task}")
