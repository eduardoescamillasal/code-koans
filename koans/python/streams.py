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

    def test_adjacent_windows_overlap(self) -> None:
        source = iter([2, 4, 8, 16])
        iterator = windows(source, 3)
        self.assertEqual(next(iterator), (2, 4, 8))
        self.assertEqual(tuple(iterator), ((4, 8, 16),))

    def test_invalid_width_leaves_input_unconsumed(self) -> None:
        items = iter([1, 2])
        with self.assertRaises(ValueError):
            list(windows(items, 0))
        self.assertEqual(next(items), 1)

    def test_rise_indices_refer_to_the_left_item(self) -> None:
        self.assertEqual(first_rises([7, 6, 9, 9, 12], 2), [1, 3])


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
