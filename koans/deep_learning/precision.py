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

    def test_equal_logits_share_probability_mass(self) -> None:
        loss, gradient = cross_entropy([1000, 1000], 0)
        self.assertAlmostEqual(loss, math.log(2))
        self.assertEqual(gradient, [-0.5, 0.5])

    def test_underflow_need_not_make_the_loss_infinite(self) -> None:
        # The true target probability can underflow while its negative log stays finite.
        loss, gradient = cross_entropy([1200.0, 0.0], 1)
        self.assertAlmostEqual(loss, 1200.0)
        self.assertEqual(gradient, [1.0, -1.0])

    def test_a_shared_bias_receives_two_derivative_terms(self) -> None:
        loss, slope = calibrate([0, 0, 0], 2, 0, (0, 1))
        self.assertAlmostEqual(loss, math.log(3))
        self.assertAlmostEqual(slope, 2 / 3)


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
