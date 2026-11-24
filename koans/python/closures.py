"""Explain when a closure resolves a name and when a default is evaluated.
Build a memoizing decorator for hashable positional and keyword arguments.
Keyword order must have no effect. Preserve metadata and __wrapped__. Cache only
successful calls. Positional and keyword spellings may use separate entries.

For transfer, count distinct right/down routes across an inclusive n by m grid from
(0, 0) to (n, m), skipping blocked coordinates. Aim for O(n*m) state visits.
Coordinates are nonnegative and each dimension is small enough for recursion.
"""

from koans import __

prediction = __
contrast = __


def memoize(function):
    raise AssertionError("Implement closures")


def routes(n, m, blocked):
    raise AssertionError("Implement routes")
