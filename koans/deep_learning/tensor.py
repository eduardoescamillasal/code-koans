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

from koans import __

prediction = __
contrast = __


def add(left, right):
    raise AssertionError("Implement tensor")


def totals(offsets, calibration):
    raise AssertionError("Implement totals")
