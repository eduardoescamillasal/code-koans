"""Explain descriptor precedence over an instance dictionary.
Construct a bounded integer descriptor with per-instance storage, class-level
introspection, and AttributeError on unset reads. Reject bool and out-of-range
assignments with ValueError before changing state. Each bound attribute name
needs an independent descriptor instance.

For transfer, build a reading type from a mapping of field names to
inclusive bound pairs. Return a class with one field per entry and a zero-arg
constructor. Different schemas and subclasses must retain their own behavior.
"""

from typing import Self, overload
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    class NonData:
        def __get__(self, instance: object, owner: type) -> str:
            return "computed"

    class Record:
        value = NonData()

    record = Record()
    record.__dict__["value"] = "local"
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, record.value)


def contrast(t: TestCase, *answers: object) -> None:
    class Record:
        @property
        def value(self) -> str:
            return "computed"

    record = Record()
    record.__dict__["value"] = "local"
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, record.value)


class BoundedInt:
    def __init__(self, low: int, high: int) -> None:
        self.low = low
        self.high = high

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    @overload
    def __get__(self, instance: None, owner: type | None = None) -> Self: ...

    @overload
    def __get__(self, instance: object, owner: type | None = None) -> int: ...

    def __get__(self, instance: object | None, owner: type | None = None) -> int | Self:
        if instance is None:
            return self
        todo("read this field from the instance and raise AttributeError if unset")

    def __set__(self, instance: object, value: int) -> None:
        todo("validate an exact int in bounds and write per-instance storage")


def bounded_int(low: int, high: int) -> BoundedInt:
    return BoundedInt(low, high)


def reading_type(schema: dict[str, tuple[int, int]]) -> type:
    namespace: dict[str, object] = {}
    # For each name install a new descriptor. type(name, bases, namespace)
    # invokes __set_name__ on descriptors.
    todo("populate the class namespace and construct the reading type")


def practice(t: TestCase, exercise: Exercise) -> None:
    class Reading:
        value = exercise.bounded_int(1, 4)

    first, second = Reading(), Reading()
    first.value, second.value = 1, 4
    t.assertEqual(first.value, 1)
    t.assertEqual(second.value, 4)


def practice_break(t: TestCase, exercise: Exercise) -> None:
    class Reading:
        count = exercise.bounded_int(0, 1)

    reading = Reading()
    reading.count = 1
    with t.assertRaises(ValueError):
        reading.count = True
    t.assertEqual(reading.count, 1)


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    Reading = exercise.reading_type({"degrees": (-20, 50)})
    reading = Reading()
    reading.degrees = -20
    t.assertEqual(reading.degrees, -20)
