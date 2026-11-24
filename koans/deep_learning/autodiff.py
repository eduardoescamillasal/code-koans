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

from typing import Self

from koans import Koan, __, todo


class AboutReverseMode(Koan):
    def test_both_operands_can_move_together(self) -> None:
        # Central difference for x*x at x=3.
        self.assertEqual(__, (4**2 - 2**2) / (4 - 2))

    def test_holding_one_operand_fixed_changes_the_slope(self) -> None:
        # Here the second operand stays fixed.
        self.assertEqual(__, (4*3 - 2*3) / (4 - 2))

    def test_both_edges_of_a_square_contribute(self) -> None:
        x = Value(4)
        self.assertEqual((x + x).data, 8)
        z = x * x
        self.assertEqual(z.data, 16)
        z.backward()
        self.assertEqual(x.grad, 8)

    def test_backward_restarts_with_a_new_seed(self) -> None:
        x = Value(2)
        z = x * x
        z.backward(3)
        self.assertEqual(x.grad, 12)
        z.backward(1)
        self.assertEqual(x.grad, 4)

    def test_one_gradient_step_moves_the_slope(self) -> None:
        # At a slope of zero this single sample has a gradient of -8.
        self.assertAlmostEqual(fit_slope([(1, 4)], 0.25, 1), 2)


class Value:
    def __init__(self, data: float, edges: tuple[tuple[Self, float], ...] = ()) -> None:
        self.data: float = data
        self.grad: float = 0.0
        self._edges = edges

    def __add__(self, other: Self) -> Self:
        return type(self)(self.data + other.data, ((self, 1.0), (other, 1.0)))

    def __mul__(self, other: Self) -> Self:
        product = self.data * other.data
        todo("record both operand edges and their local derivatives")

    def _postorder(self) -> list[Self]:
        ordered: list[Self] = []
        seen: set[Self] = set()
        pending = [(self, False)]
        while pending:
            node, expanded = pending.pop()
            if expanded:
                ordered.append(node)
            elif node not in seen:
                seen.add(node)
                pending.append((node, True))
                pending.extend((parent, False) for parent, _ in node._edges)
        return ordered

    def backward(self, seed: float = 1.0) -> None:
        nodes = self._postorder()
        for node in nodes:
            node.grad = 0.0
        self.grad = seed
        todo("walk output-to-leaf and accumulate the derivative on each incoming edge")


def fit_slope(samples: list[tuple[float, float]], rate: float, steps: int) -> float:
    weight = 0.0
    for _ in range(steps):
        parameter = Value(weight)
        loss = Value(0)
        # Form one loss by summing squared residuals, then update once per pass.
        todo("build the loss, differentiate it, and update weight")
    return weight
