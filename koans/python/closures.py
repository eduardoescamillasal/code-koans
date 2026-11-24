"""Trace which calls share a dictionary captured by a wrapper.
Build a memoizing decorator for hashable positional and keyword arguments.
Keyword order must have no effect. Preserve metadata and __wrapped__. Cache only
successful calls. Positional and keyword spellings may use separate entries.

For transfer, count distinct right/down routes across an inclusive n by m grid from
(0, 0) to (n, m), skipping blocked coordinates. Aim for O(n*m) state visits.
Coordinates are nonnegative and each dimension is small enough for recursion.
"""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar
from unittest import TestCase

from koans import Exercise, __, todo


def _count_calls(cache_outside: bool) -> tuple[int, ...]:
    called: list[int] = []

    def build(tag: str) -> Callable[[int], str]:
        shared: dict[int, str] = {}

        def wrapper(value: int) -> str:
            cache = shared if cache_outside else {}
            if value not in cache:
                called.append(value)
                cache[value] = f"{tag}:{value}"
            return cache[value]

        return wrapper

    first = build("a")
    second = build("b")
    first(7)
    first(7)
    second(7)
    return tuple(called)


def predict(t: TestCase, *answers: object) -> None:
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, _count_calls(cache_outside=False))


def contrast(t: TestCase, *answers: object) -> None:
    # Why does the second wrapper still compute a result?
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, _count_calls(cache_outside=True))


P = ParamSpec("P")
R = TypeVar("R")


def memoize(function: Callable[P, R]) -> Callable[P, R]:
    cache: dict[object, R] = {}

    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        # Convert the arguments into a hashable key. Keyword order is irrelevant.
        # Store the result only after function returns.
        todo("look up the call key or compute and cache a fresh result")

    return wrapped


def routes(n: int, m: int, blocked: set[tuple[int, int]]) -> int:
    # Count arrivals from a coordinate. Cases: outside grid, blocked, destination,
    # or an interior cell with two possible next moves.
    def visit(row: int, column: int) -> int:
        todo("handle the base cases and count continuations from this coordinate")

    # Use a fresh cache for each blocked layout.
    todo("start the traversal at (0, 0) with a per-call memoized visit")


def practice(t: TestCase, exercise: Exercise) -> None:
    calls: list[int] = []

    def scale(number: int, *, factor: int) -> int:
        calls.append(number)
        return number * factor

    compute = exercise.memoize(scale)
    t.assertEqual(compute(3, factor=2), 6)
    t.assertEqual(compute(3, factor=2), 6)
    t.assertEqual(compute(3, factor=4), 12)
    t.assertEqual(calls, [3, 3])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    def first(value: int) -> int:
        return value + 1

    def second(value: int) -> int:
        return value + 2

    t.assertEqual(exercise.memoize(first)(4), 5)
    t.assertEqual(exercise.memoize(second)(4), 6)


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.routes(1, 2, set()), 3)
    t.assertEqual(exercise.routes(1, 2, {(0, 1)}), 1)
