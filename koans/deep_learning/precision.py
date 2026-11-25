"""Compare direct and shifted exponentiation in binary64 floating point.
Implement stable categorical cross-entropy from finite logits and a target index.
Return (loss, gradient list). Shift by the largest logit before exponentiating.
Derive dL/dz_j from L = log(sum(exp(z))) - z_target to get p_j - 1[j=target].
Reject empty logits, nonfinite logits, and invalid targets with ValueError.

For transfer, a single adjustable bias is added to two of three class
logits. Return the loss and derivative with respect to bias for the supplied
logits, target, and bias. The two affected class indices are distinct.
"""

import math

from koans import Koan, __, todo


class AboutStableProbabilities(Koan):
    def test_large_logits_can_overflow(self) -> None:
        logits = [1000.0, 1000.0]
        try:
            weights = [math.exp(logit) for logit in logits]
        except OverflowError:
            outcome: object = "overflow"
        else:
            outcome = tuple(weight / sum(weights) for weight in weights)
        self.assertEqual(__, outcome)

    def test_shifting_logits_keeps_weights_finite(self) -> None:
        logits = [1000.0, 1000.0]
        weights = [math.exp(logit - max(logits)) for logit in logits]
        self.assertEqual(__, tuple(weight / sum(weights) for weight in weights))

    def test_floating_point_addition_can_erase_a_small_increment(self) -> None:
        self.assertEqual(__, (1e16 + 1.0) - 1e16)
        self.assertEqual(__, (1.0 + 1.0) - 1.0)

    def test_the_log_loss_can_survive_probability_underflow(self) -> None:
        target, peak = 0.0, 1000.0
        weights = [math.exp(peak - peak), math.exp(target - peak)]
        self.assertEqual(__, weights[1] / sum(weights))
        self.assertEqual(__, math.log(sum(weights)) - (target - peak))

    def test_only_the_target_coordinate_gets_the_indicator(self) -> None:
        probabilities = [0.25, 0.5, 0.25]
        target = 1
        gradients = [p - (index == target) for index, p in enumerate(probabilities)]
        self.assertEqual(__, gradients[0])
        self.assertEqual(__, gradients[target])
        self.assertEqual(__, sum(gradients))


def cross_entropy(logits: list[float], target: int) -> tuple[float, list[float]]:
    if type(target) is not int or not 0 <= target < len(logits):
        raise ValueError("invalid target")
    if not all(math.isfinite(logit) for logit in logits):
        raise ValueError("logits must be finite")
    peak = max(logits)
    shifted = [logit - peak for logit in logits]
    weights = [math.exp(logit) for logit in shifted]
    normalizer = sum(weights)
    # Use shifted[target] to calculate log-probability without taking log(0).
    todo("calculate the loss and subtract the target indicator from the probabilities")


def calibrate(
    logits: list[float], target: int, bias: float, affected: tuple[int, int]
) -> tuple[float, float]:
    adjusted = logits.copy()
    for index in affected:
        adjusted[index] += bias
    loss, _gradient = cross_entropy(adjusted, target)
    todo("reduce the per-logit derivatives to one derivative for bias")
