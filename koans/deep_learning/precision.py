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
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    logits = [1000.0, 1000.0]
    try:
        weights = [math.exp(logit) for logit in logits]
    except OverflowError:
        outcome: object = "overflow"
    else:
        outcome = tuple(weight / sum(weights) for weight in weights)
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, outcome)


def contrast(t: TestCase, *answers: object) -> None:
    logits = [1000.0, 1000.0]
    weights = [math.exp(logit - max(logits)) for logit in logits]
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(weight / sum(weights) for weight in weights))


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


def practice(t: TestCase, exercise: Exercise) -> None:
    loss, gradient = exercise.cross_entropy([1000, 1000], 0)
    t.assertAlmostEqual(loss, math.log(2))
    t.assertEqual(gradient, [-0.5, 0.5])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    # The true target probability can underflow while its negative log stays finite.
    loss, gradient = exercise.cross_entropy([1200.0, 0.0], 1)
    t.assertAlmostEqual(loss, 1200.0)
    t.assertEqual(gradient, [1.0, -1.0])


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    loss, slope = exercise.calibrate([0, 0, 0], 2, 0, (0, 1))
    t.assertAlmostEqual(loss, math.log(3))
    t.assertAlmostEqual(slope, 2 / 3)
