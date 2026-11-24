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

from koans import Koan, __, todo


class AboutDescriptors(Koan):
    def test_an_instance_can_shadow_a_nondata_descriptor(self) -> None:
        class NonData:
            def __get__(self, instance: object, owner: type) -> str:
                return "computed"

        class Record:
            value = NonData()

        record = Record()
        record.__dict__["value"] = "local"
        self.assertEqual(__, record.value)

    def test_a_property_takes_precedence(self) -> None:
        class Record:
            @property
            def value(self) -> str:
                return "computed"

        record = Record()
        record.__dict__["value"] = "local"
        self.assertEqual(__, record.value)

    def test_a_field_stores_values_per_instance(self) -> None:
        class Reading:
            value = bounded_int(1, 4)

        first, second = Reading(), Reading()
        first.value, second.value = 1, 4
        self.assertEqual(first.value, 1)
        self.assertEqual(second.value, 4)

    def test_an_invalid_write_leaves_the_old_value_alone(self) -> None:
        class Reading:
            count = bounded_int(0, 1)

        reading = Reading()
        reading.count = 1
        with self.assertRaises(ValueError):
            reading.count = True
        self.assertEqual(reading.count, 1)

    def test_a_schema_creates_a_validated_attribute(self) -> None:
        Reading = reading_type({"degrees": (-20, 50)})
        reading = Reading()
        reading.degrees = -20
        self.assertEqual(reading.degrees, -20)


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
