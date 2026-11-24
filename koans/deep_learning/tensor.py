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

from koans import Koan, __, todo


class AboutBroadcasting(Koan):
    def test_zip_stops_at_the_shorter_input(self) -> None:
        self.assertEqual(__, tuple(zip([1, 2], [10])))

    def test_a_singleton_can_expand(self) -> None:
        self.assertEqual(__, tuple((x, 10) for x in [1, 2]))

    def test_rows_and_columns_can_expand_together(self) -> None:
        self.assertEqual(add([[2]], [[1, 3]]), [[3, 5]])
        self.assertEqual(add([[1], [3]], [[10, 20]]), [[11, 21], [13, 23]])

    def test_two_cannot_broadcast_to_three(self) -> None:
        # A singleton can expand, but a size of two cannot broadcast to three.
        with self.assertRaises(ValueError):
            add([[1, 2]], [[3, 4, 5]])

    def test_totals_reduce_over_different_axes(self) -> None:
        self.assertEqual(totals([1, 3], [10, 20]), ([32, 36], [24, 44]))


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
