"""Fit a model whose features can interact.

The model is a + b*x + c*y + d*x*y. Train with mean squared error and full-batch
gradient descent, using the same coefficients for every gradient in a batch.
The intercept and linear coefficients cannot fit the parity target on all
four sign pairs. The product term can. Fit accepts a reusable batch of finite
(x, y, target) rows. Empty batches, negative or nonfinite rates, and negative
step counts are invalid. A zero step count leaves the model unchanged.
"""
from collections.abc import Sequence
import math
from typing import NamedTuple

from koans import Koan, __, todo


class Sample(NamedTuple):
    x: float
    y: float
    target: float


class Weights(NamedTuple):
    bias: float
    x: float
    y: float
    cross: float


class AboutFeatureInteractions(Koan):
    def test_an_additive_model_has_the_same_difference_on_both_sides(self) -> None:
        def score(x: int, y: int) -> int:
            return 2 * x - y

        self.assertEqual(__, (score(1, -1) - score(-1, -1), score(1, 1) - score(-1, 1)))

    def test_an_interaction_can_reverse_a_features_effect(self) -> None:
        def score(x: int, y: int) -> int:
            return x * y

        self.assertEqual(__, (score(1, -1) - score(-1, -1), score(1, 1) - score(-1, 1)))

    def test_centering_changes_the_origin_of_an_interaction(self) -> None:
        a, b = (11, 13), (19, 21)
        centered = [(x - 12) * (y - 20) for x, y in zip(a, b)]
        raw = [x * y for x, y in zip(a, b)]
        self.assertEqual(__, centered)
        self.assertEqual(__, raw)

    def test_the_same_residual_flows_through_different_local_features(self) -> None:
        x, y, target = 2, -3, 1
        prediction = 0
        residual = prediction - target
        terms = [2 * residual * feature for feature in (1, x, y, x * y)]
        self.assertEqual(__, terms[:3])
        self.assertEqual(__, terms[3])

    def test_cancelling_linear_gradients_can_hide_a_product_signal(self) -> None:
        cases = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        residuals = [-x * y for x, y in cases]
        self.assertEqual(__, sum(r * x for r, (x, y) in zip(residuals, cases)))
        self.assertEqual(__, sum(r * x * y for r, (x, y) in zip(residuals, cases)))


def _features(x: float, y: float) -> tuple[float, float, float, float]:
    cross: float = todo("compute the xy feature")
    return 1.0, x, y, cross


class InteractionModel:
    def __init__(self, weights: Weights = Weights(0, 0, 0, 0)) -> None:
        self.weights = weights

    def predict(self, x: float, y: float) -> float:
        return sum(weight * feature for weight, feature in zip(self.weights, _features(x, y)))

    def fit(self, rows: Sequence[Sample], rate: float, steps: int) -> None:
        if not rows or not math.isfinite(rate) or rate < 0 or steps < 0:
            raise ValueError("expected a nonempty batch and valid training settings")
        for _ in range(steps):
            gradient = [0.0] * 4
            for row in rows:
                residual = self.predict(row.x, row.y) - row.target
                for index, feature in enumerate(_features(row.x, row.y)):
                    gradient[index] += todo("differentiate the squared error for this coefficient")
            # Update together after accumulating the whole batch.
            self.weights = todo("apply the mean batch gradient to all four weights")
