"""Distinguish a reusable iterable from an iterator with suspended state.
Implement lazy fixed-width windows. Consume each item at most once, use O(width)
auxiliary storage, yield immutable tuples, and validate positive width before
consuming input. An empty or short stream yields no windows.

For transfer, find indices of the first limit strictly increasing adjacent pairs
in a potentially infinite stream. The index denotes the left item. Stop
consuming as soon as enough matches have arrived. Zero limit consumes nothing.
"""

from koans import __

prediction = __
contrast = __


def windows(iterable, width):
    raise AssertionError("Implement streams")


def first_rises(readings, limit):
    raise AssertionError("Implement first_rises")
