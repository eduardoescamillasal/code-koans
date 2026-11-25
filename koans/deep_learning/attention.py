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

from koans import Koan, __, todo


class AboutAttentionMasks(Koan):
    def test_zero_logits_keep_probability_mass(self) -> None:
        # Replacing a masked score with zero still gives it positive mass.
        self.assertEqual(__, tuple(math.exp(x) / 2 for x in (0, 0)))

    def test_masked_logits_can_have_zero_mass(self) -> None:
        weights = [math.exp(x) for x in (0, -math.inf)]
        self.assertEqual(__, tuple(x / sum(weights) for x in weights))

    def test_a_mask_is_applied_before_choosing_the_normalizer(self) -> None:
        scores = [1000.0, 3.0, 3.0]
        keep = [False, True, True]
        visible = [value for value, allowed in zip(scores, keep) if allowed]
        peak = max(visible)
        self.assertEqual(__, peak)
        self.assertEqual(__, sum(math.exp(value - peak) for value in visible))

    def test_a_weighted_value_combines_coordinates_independently(self) -> None:
        weights = [0.0, 0.25, 0.75]
        vectors = [[100, 100], [2, 4], [6, 0]]
        columns = list(zip(*vectors))
        mixed = [sum(weight * value for weight, value in zip(weights, col)) for col in columns]
        self.assertEqual(__, mixed[0])
        self.assertEqual(__, mixed[1])

    def test_each_causal_row_exposes_a_different_prefix(self) -> None:
        positions = range(4)
        keep = [[source <= query for source in positions] for query in positions]
        self.assertEqual(__, keep[0])
        self.assertEqual(__, keep[2])
        self.assertEqual(__, sum(keep[3]))


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
