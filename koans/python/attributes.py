"""Explain descriptor precedence over an instance dictionary.
Construct a bounded integer descriptor with per-instance storage, class-level
introspection, and AttributeError on unset reads. Reject bool and out-of-range
assignments with ValueError before changing state. Each bound attribute name
needs an independent descriptor instance.

For transfer, build a reading type from a mapping of field names to
inclusive bound pairs. Return a class with one field per entry and a zero-arg
constructor. Different schemas and subclasses must retain their own behavior.
"""

from koans import __

prediction = __
contrast = __


def bounded_int(low, high):
    raise AssertionError("Implement attributes")


def reading_type(schema):
    raise AssertionError("Implement reading_type")
