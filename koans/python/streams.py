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

from koans import Koan, __, todo


class AboutLazyStreams(Koan):
    def test_reading_an_iterator_consumes_it(self) -> None:
        source = iter([10, 20, 30])
        self.assertEqual(__, (tuple(islice(source, 2)), tuple(source)))

    def test_reading_a_list_allows_another_pass(self) -> None:
        source = [10, 20, 30]
        self.assertEqual(__, (tuple(islice(source, 2)), tuple(source)))

    def test_constructing_a_generator_leaves_work_pending(self) -> None:
        seen: list[int] = []

        def readings() -> Iterator[int]:
            for value in (4, 8, 12):
                seen.append(value)
                yield value

        source = readings()
        self.assertEqual(__, seen.copy())
        self.assertEqual(__, next(source))
        self.assertEqual(__, seen.copy())
        self.assertEqual(__, tuple(source))

    def test_freezing_a_moving_buffer_keeps_an_earlier_window(self) -> None:
        buffer = deque([1, 2], maxlen=2)
        first = tuple(buffer)
        buffer.append(3)
        self.assertEqual(__, first)
        self.assertEqual(__, tuple(buffer))

    def test_taking_matches_consumes_rejected_items_along_the_way(self) -> None:
        source = iter([2, 3, 4, 5, 6])
        odds = (value for value in source if value % 2)
        self.assertEqual(__, list(islice(odds, 1)))
        self.assertEqual(__, next(source))
        self.assertEqual(__, list(odds))


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
