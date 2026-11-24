"""Markers for incomplete predictions and unfinished code."""

from types import ModuleType, SimpleNamespace
from typing import Never

Exercise = ModuleType | SimpleNamespace


class _Blank:
    def __repr__(self) -> str:
        return "__ (fill in your prediction)"


__ = _Blank()


def todo(task: str) -> Never:
    """Stop at the first missing implementation step."""
    raise AssertionError(f"Implement {task}")
