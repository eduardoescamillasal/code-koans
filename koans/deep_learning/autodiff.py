"""Build reverse-mode automatic differentiation for scalar values.
Implement Value with data, grad, addition and multiplication between Values,
and backward(seed=1.0). For each node collect downstream contributions before
propagating its local derivatives. x*x has two incoming operand edges even
when both point to x. Each backward call replaces gradients on reachable
nodes. Support deep graphs without Python recursion in backward.

For transfer, fit a single slope through the origin to input/target pairs
using squared error, starting from zero. Perform the requested number of steps
and return the final slope. Differentiate the aggregate loss through your
scalar objects. Inputs are nonempty pairs with finite values.
"""

from koans import __

prediction = __
contrast = __


class Value:
    def __init__(self, data):
        raise AssertionError("Implement autodiff")


def fit_slope(samples, rate, steps):
    raise AssertionError("Implement fit_slope")
