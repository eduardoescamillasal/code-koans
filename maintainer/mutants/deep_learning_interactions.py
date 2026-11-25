from maintainer.references.deep_learning_interactions import InteractionModel


class NoInteraction(InteractionModel):
    def predict(self, x: float, y: float) -> float:
        return self.weights.bias + self.weights.x * x + self.weights.y * y


class SumGradient(InteractionModel):
    def fit(self, rows, rate: float, steps: int) -> None:
        super().fit(rows, rate * len(rows), steps)


class TrainsOnce(InteractionModel):
    def fit(self, rows, rate: float, steps: int) -> None:
        super().fit(rows, rate, min(steps, 1))


CASES = {
    "predict": {"prediction": (-4, 4)},
    "contrast": {"contrast": (2, 2)},
    "implement": {"InteractionModel": NoInteraction},
    "break_cases": {"InteractionModel": SumGradient},
    "transfer": {"InteractionModel": TrainsOnce},
}
