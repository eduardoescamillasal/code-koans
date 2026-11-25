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

    def test_an_inherited_property_uses_the_receiving_instance(self) -> None:
        class Reading:
            @property
            def kelvin(self) -> int:
                return self.celsius + 273

            celsius = 0

        class WarmReading(Reading):
            celsius = 10

        self.assertEqual(__, Reading().kelvin)
        self.assertEqual(__, WarmReading().kelvin)
        self.assertEqual(__, isinstance(WarmReading.kelvin, property))

    def test_set_name_observes_which_attribute_is_bound(self) -> None:
        class Label:
            def __set_name__(self, owner: type, name: str) -> None:
                self.name = name

        field = Label()

        class Reading:
            pressure = field

        self.assertEqual(__, field.name)
        self.assertEqual(__, Reading.pressure is field)

    def test_a_descriptor_setter_can_validate_before_storing(self) -> None:
        class Reading:
            def __init__(self) -> None:
                self._count = 0

            @property
            def count(self) -> int:
                return self._count

            @count.setter
            def count(self, value: int) -> None:
                if type(value) is not int:
                    raise ValueError("exact integer required")
                self._count = value

        row = Reading()
        row.count = 4
        try:
            row.count = True
        except ValueError:
            reason = "rejected"
        else:
            reason = "accepted"
        self.assertEqual(__, reason)
        self.assertEqual(__, row.count)


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
