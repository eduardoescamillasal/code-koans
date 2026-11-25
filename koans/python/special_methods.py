"""Give vectors an explicit numerical protocol.

Store coordinates as a tuple. Addition and @ require equal-length vectors;
raise ValueError on a mismatch. Multiplication scales a vector by an exact
int or float, on either side. Unknown operand types return NotImplemented
so Python can try the reflected operation. repr is Vector(1, 2) for coordinates
(1, 2). The final check walks a short path and projects it onto a direction.
"""
from collections.abc import Iterator
from types import NotImplementedType
from typing import Self

from koans import Koan, __, todo


class AboutSpecialMethods(Koan):
    def test_new_creates_the_object_before_init_populates_it(self) -> None:
        class Sample:
            def __new__(cls, label: str) -> Self:
                instance = super().__new__(cls)
                instance.trace = ["new"]
                return instance

            def __init__(self, label: str) -> None:
                self.trace.append(label)

        sample = Sample("init")
        self.assertEqual(__, sample.trace)

    def test_repr_and_str_answer_different_questions(self) -> None:
        class Cell:
            def __repr__(self) -> str:
                return "Cell(7)"

            def __str__(self) -> str:
                return "seven"

        value = Cell()
        self.assertEqual(__, (repr(value), str(value), repr([value])))

    def test_not_implemented_allows_a_reflected_operation(self) -> None:
        class Left:
            def __add__(self, other: object) -> NotImplementedType:
                return NotImplemented

        class Right:
            def __radd__(self, other: object) -> str:
                return "reflected"

        self.assertEqual(__, Left().__add__(Right()) is NotImplemented)
        self.assertEqual(__, Left() + Right())

    def test_multiplication_syntax_selects_the_method_by_operand_order(self) -> None:
        class Scale:
            def __mul__(self, other: int) -> tuple[str, int]:
                return "left", other

            def __rmul__(self, other: int) -> tuple[str, int]:
                return "right", other

        value = Scale()
        self.assertEqual(__, value * 3)
        self.assertEqual(__, 3 * value)

    def test_an_in_place_expression_can_rebind_instead_of_mutating(self) -> None:
        values = (2, 3)
        alias = values
        values += (4,)
        self.assertEqual(__, values)
        self.assertEqual(__, alias)
        self.assertEqual(__, values is alias)


    def test_indexing_passes_slices_to_getitem(self) -> None:
        class Bag:
            items = (2, 5, 8)

            def __getitem__(self, key: int | slice) -> int | tuple[int, ...]:
                return self.items[key]

        bag = Bag()
        self.assertEqual(__, bag[-1])
        self.assertEqual(__, bag[1:])
        self.assertEqual(__, tuple(bag))

    def test_bool_uses_len_when_bool_is_absent(self) -> None:
        class Bag:
            def __init__(self, items: tuple[int, ...]) -> None:
                self.items = items

            def __len__(self) -> int:
                return len(self.items)

        self.assertEqual(__, bool(Bag(())))
        self.assertEqual(__, bool(Bag((0,))))


class Vector:
    def __init__(self, *coordinates: float) -> None:
        self.coordinates = coordinates

    def __repr__(self) -> str:
        fields = ", ".join(map(repr, self.coordinates))
        return todo("wrap the comma-separated coordinates in Vector(...)")

    def _pairs(self, other: "Vector") -> Iterator[tuple[float, float]]:
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("dimension mismatch")
        return zip(self.coordinates, other.coordinates, strict=True)

    def __add__(self, other: object) -> "Vector | NotImplementedType":
        if not isinstance(other, Vector):
            return NotImplemented
        return todo("build a Vector from pairwise coordinate sums")

    def __mul__(self, other: object) -> "Vector | NotImplementedType":
        if type(other) not in (int, float):
            return NotImplemented
        return todo("scale each coordinate by the scalar")

    def __rmul__(self, other: object) -> "Vector | NotImplementedType":
        return self.__mul__(other)

    def __matmul__(self, other: object) -> float | NotImplementedType:
        if not isinstance(other, Vector):
            return NotImplemented
        return todo("reduce pairwise coordinate products to a dot product")
