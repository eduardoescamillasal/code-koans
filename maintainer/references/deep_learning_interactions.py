from collections.abc import Sequence
import math

from koans.deep_learning.interactions import Sample, Weights

prediction = (4, 4)
contrast = (-2, 2)


def _features(x: float, y: float) -> tuple[float, float, float, float]:
    return 1, x, y, x * y


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
                    gradient[index] += 2 * residual * feature
            self.weights = Weights(*(w - rate * g / len(rows) for w, g in zip(self.weights, gradient)))
