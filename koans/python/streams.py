"""Distinguish a reusable iterable from an iterator with suspended state.
Implement lazy fixed-width windows. Consume each item at most once, use O(width)
auxiliary storage, yield immutable tuples, and validate positive width before
consuming input. An empty or short stream yields no windows.

For transfer, find indices of the first limit strictly increasing adjacent pairs
in a potentially infinite stream. The index denotes the left item. Stop
consuming as soon as enough matches have arrived. Zero limit consumes nothing.
"""

from collections import deque
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    source = iter([10, 20, 30])
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (tuple(islice(source, 2)), tuple(source)))


def contrast(t: TestCase, *answers: object) -> None:
    source = [10, 20, 30]
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (tuple(islice(source, 2)), tuple(source)))


T = TypeVar("T")


def windows(iterable: Iterable[T], width: int) -> Iterator[tuple[T, ...]]:
    if width < 1:
        raise ValueError("width must be positive")
    recent: deque[T] = deque(maxlen=width)
    for value in iterable:
        recent.append(value)
        if len(recent) == width:
            # Yield a stable snapshot while keeping the buffer available for the next iteration.
            yield todo("emit the current window")


def first_rises(readings: Iterable[float], limit: int) -> list[int]:
    adjacent = windows(readings, 2)
    # Count matching pairs, rather than taking the first limit pairs.
    todo("filter indexed pairs and stop after the requested number of rises")


def practice(t: TestCase, exercise: Exercise) -> None:
    source = iter([2, 4, 8, 16])
    iterator = exercise.windows(source, 3)
    t.assertEqual(next(iterator), (2, 4, 8))
    t.assertEqual(tuple(iterator), ((4, 8, 16),))


def practice_break(t: TestCase, exercise: Exercise) -> None:
    items = iter([1, 2])
    with t.assertRaises(ValueError):
        list(exercise.windows(items, 0))
    t.assertEqual(next(items), 1)


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.first_rises([7, 6, 9, 9, 12], 2), [1, 3])
