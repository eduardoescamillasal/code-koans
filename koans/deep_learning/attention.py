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

import math
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    # Replacing a masked score with zero still gives it positive mass.
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(math.exp(x) / 2 for x in (0, 0)))


def contrast(t: TestCase, *answers: object) -> None:
    weights = [math.exp(x) for x in (0, -math.inf)]
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(x / sum(weights) for x in weights))


def _visible_weights(scores: list[float], keep: list[bool]) -> list[float]:
    visible = [score for score, allowed in zip(scores, keep) if allowed]
    if not visible:
        raise ValueError("attention needs a visible key")
    peak = max(visible)
    # Normalize after subtraction. Keep masked entries exactly zero.
    todo("turn visible scores into stable weights")


def attend(
    query: list[float], keys: list[list[float]], values: list[list[float]], keep: list[bool]
) -> tuple[list[float], list[float]]:
    if not query or not keys or len(keys) != len(values) or len(keys) != len(keep):
        raise ValueError("incompatible lengths")
    if not values[0] or any(len(row) != len(values[0]) for row in values):
        raise ValueError("values must form a nonempty rectangle")
    if any(len(key) != len(query) for key in keys):
        raise ValueError("key width differs from query width")
    scale = math.sqrt(len(query))
    scores = [sum(q * k for q, k in zip(query, key)) / scale for key in keys]
    weights = _visible_weights(scores, keep)
    todo("reduce the value rows using their attention weights")


def causal_smooth(keys: list[list[float]], values: list[list[float]]) -> list[list[float]]:
    # Use each key as a query. Build one mask per query position.
    todo("collect a result for each prefix without reading future values")


def practice(t: TestCase, exercise: Exercise) -> None:
    output, weights = exercise.attend([1], [[1000], [1]], [[17], [3]], [False, True])
    t.assertEqual(weights, [0, 1])
    t.assertEqual(output, [3])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    # With no visible values there is no probability distribution.
    with t.assertRaises(ValueError):
        exercise.attend([1], [[1]], [[9]], [False])


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.causal_smooth([[0], [0]], [[2], [8]]), [[2], [5]])
