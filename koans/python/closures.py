"""Trace which calls share a dictionary captured by a wrapper.
Build a memoizing decorator for hashable positional and keyword arguments.
Keyword order must have no effect. Preserve metadata and __wrapped__. Cache only
successful calls. Positional and keyword spellings may use separate entries.

For transfer, count distinct right/down routes across an inclusive n by m grid from
(0, 0) to (n, m), skipping blocked coordinates. Aim for O(n*m) state visits.
Coordinates are nonnegative and each dimension is small enough for recursion.
"""

from collections.abc import Callable, Hashable
from functools import wraps
from typing import ParamSpec, TypeVar

from koans import Koan, __, todo


class AboutClosures(Koan):
    @staticmethod
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

    def test_a_new_dictionary_never_reuses_a_call(self) -> None:
        self.assertEqual(__, self._count_calls(cache_outside=False))

    def test_a_wrapper_keeps_its_dictionary(self) -> None:
        # Why does the second wrapper still compute a result?
        self.assertEqual(__, self._count_calls(cache_outside=True))

    def test_keyword_order_does_not_change_a_cache_key(self) -> None:
        first = _cache_key((4,), {"scale": 3, "offset": 1})
        reordered = _cache_key((4,), {"offset": 1, "scale": 3})
        different = _cache_key((4,), {"offset": 2, "scale": 3})
        self.assertEqual(first, reordered)
        self.assertNotEqual(first, different)
        self.assertIsInstance(hash(first), int)

    def test_repeated_arguments_reuse_a_result(self) -> None:
        calls: list[int] = []

        def scale(number: int, *, factor: int) -> int:
            calls.append(number)
            return number * factor

        compute = memoize(scale)
        self.assertEqual(compute(3, factor=2), 6)
        self.assertEqual(compute(3, factor=2), 6)
        self.assertEqual(compute(3, factor=4), 12)
        self.assertEqual(calls, [3, 3])

    def test_separately_decorated_functions_have_separate_caches(self) -> None:
        def first(value: int) -> int:
            return value + 1

        def second(value: int) -> int:
            return value + 2

        self.assertEqual(memoize(first)(4), 5)
        self.assertEqual(memoize(second)(4), 6)

    def test_blocked_cells_change_the_number_of_routes(self) -> None:
        self.assertEqual(routes(1, 2, set()), 3)
        self.assertEqual(routes(1, 2, {(0, 1)}), 1)


P = ParamSpec("P")
R = TypeVar("R")


def _cache_key(args: tuple[object, ...], kwargs: dict[str, object]) -> Hashable:
    # Keep both positional values and named values. Make the named portion
    # insensitive to insertion order.
    todo("build a hashable key from positional and keyword arguments")


def memoize(function: Callable[P, R]) -> Callable[P, R]:
    cache: dict[Hashable, R] = {}

    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        key = _cache_key(args, kwargs)
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
