"""Implement single-query scaled dot-product attention for rectangular
nonempty keys and values, and a boolean keep mask. Return (weighted value,
weights). Divide scores by sqrt(query width) to keep their variance roughly
constant when coordinates are independent with unit variance. Normalize only
over visible keys after subtracting their maximum. Reject incompatible shapes
and an all-masked row with ValueError. Inputs are finite with finite dot products.

For transfer, give each timestep a context-dependent estimate. Its query is
its own key. For each row, use only values at that step and earlier. Return
one output vector per timestep, retaining original order.
"""

from koans import __

prediction = __
contrast = __


def attend(query, keys, values, keep):
    raise AssertionError("Implement attention")


def causal_smooth(keys, values):
    raise AssertionError("Implement causal_smooth")
