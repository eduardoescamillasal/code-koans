"""Lift scalar addition to nonempty rectangular matrices with rank-two
broadcasting. On each axis, equal sizes match and a singleton dimension can
expand. Incompatible or ragged inputs raise ValueError. Add elements using + so
the same operation works for numbers and prior-module Value objects. During
backpropagation, repeated uses of an expanded element sum into its gradient.

For transfer, each station has an offset and each channel has a calibration.
Return (station totals, channel totals), computed from the sum of the two
adjustments for every pair. Totals follow the original station/channel order.
Both inputs are nonempty sequences of numbers.
"""

from typing import Protocol, Self, TypeVar
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(zip([1, 2], [10])))


def contrast(t: TestCase, *answers: object) -> None:
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple((x, 10) for x in [1, 2]))


T = TypeVar("T", bound="Addable")


class Addable(Protocol):
    def __add__(self, other: Self, /) -> Self:
        ...


def _shape(matrix: list[list[T]]) -> tuple[int, int]:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("expected a nonempty rectangle")
    return len(matrix), len(matrix[0])


def _axis(a: int, b: int) -> int:
    todo("choose the size for matching or singleton axes; reject other combinations")


def add(left: list[list[T]], right: list[list[T]]) -> list[list[T]]:
    lh, lw = _shape(left)
    rh, rw = _shape(right)
    height = _axis(lh, rh)
    width = _axis(lw, rw)
    # At each output position, an expanded input always uses index zero
    # on any axis whose original size is one.
    todo("build the output cells by mapping their positions into both inputs")


def totals(offsets: list[float], calibration: list[float]) -> tuple[list[float], list[float]]:
    # Treat the offsets as a column and the calibration as a row.
    todo("combine both adjustments and reduce across stations and channels")


def practice(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.add([[2]], [[1, 3]]), [[3, 5]])
    t.assertEqual(exercise.add([[1], [3]], [[10, 20]]), [[11, 21], [13, 23]])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    # A singleton can expand, but a size of two cannot broadcast to three.
    with t.assertRaises(ValueError):
        exercise.add([[1, 2]], [[3, 4, 5]])


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.totals([1, 3], [10, 20]), ([32, 36], [24, 44]))
