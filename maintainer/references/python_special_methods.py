from collections.abc import Iterator
from types import NotImplementedType

prediction = ['new', 'init']
contrast = ('Cell(7)', 'seven', '[Cell(7)]')


class Vector:
    def __init__(self, *coordinates: float) -> None:
        self.coordinates = coordinates

    def __repr__(self) -> str:
        return f"Vector({', '.join(map(repr, self.coordinates))})"

    def _pairs(self, other: "Vector") -> Iterator[tuple[float, float]]:
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("dimension mismatch")
        return zip(self.coordinates, other.coordinates, strict=True)

    def __add__(self, other: object) -> "Vector | NotImplementedType":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(*(a + b for a, b in self._pairs(other)))

    def __mul__(self, other: object) -> "Vector | NotImplementedType":
        if type(other) not in (int, float):
            return NotImplemented
        return Vector(*(value * other for value in self.coordinates))

    def __rmul__(self, other: object) -> "Vector | NotImplementedType":
        return self.__mul__(other)

    def __matmul__(self, other: object) -> float | NotImplementedType:
        if not isinstance(other, Vector):
            return NotImplemented
        return sum(a * b for a, b in self._pairs(other))
