"""Select a binary classifier threshold on validation data, then score a holdout.

Scores are probabilities in [0, 1]. A score exactly on the threshold is positive.
Counts are true positives, false positives, false negatives, and true negatives.
F1 is 2TP / (2TP + FP + FN), with zero for a zero denominator. Select the
validation threshold with highest F1, breaking ties toward the higher threshold.
Reject nonfinite or out-of-range values and an empty candidate list.
"""
from collections.abc import Iterable, Sequence
from typing import NamedTuple

from koans import Koan, __, todo


class Scored(NamedTuple):
    label: bool
    score: float


class Counts(NamedTuple):
    tp: int
    fp: int
    fn: int
    tn: int


class Evaluation(NamedTuple):
    threshold: float
    validation: Counts
    holdout: Counts


class AboutBinaryEvaluation(Koan):
    def test_accuracy_can_look_high_when_positives_are_rare(self) -> None:
        labels = [False] * 19 + [True]
        predicted = [False] * len(labels)
        self.assertEqual(__, (sum(a == b for a, b in zip(labels, predicted)), sum(predicted)))

    def test_an_accurate_model_can_recover_all_the_positives(self) -> None:
        labels = [False] * 19 + [True]
        predicted = [True] + [False] * 18 + [True]
        self.assertEqual(__, (sum(a == b for a, b in zip(labels, predicted)), sum(predicted)))

    def test_changing_the_threshold_changes_who_is_missed(self) -> None:
        rows = [Scored(True, 0.7), Scored(False, 0.8), Scored(True, 0.4)]
        low = [row.label for row in rows if row.score >= 0.4]
        high = [row.label for row in rows if row.score >= 0.7]
        self.assertEqual(__, low)
        self.assertEqual(__, high)
        self.assertEqual(__, sum(row.score < 0.7 and row.label for row in rows))

    def test_f1_depends_on_positive_errors_not_true_negatives(self) -> None:
        cases = [Counts(2, 0, 2, 97), Counts(2, 2, 0, 7), Counts(2, 0, 0, 0)]
        numerators = [2 * c.tp for c in cases]
        denominators = [2 * c.tp + c.fp + c.fn for c in cases]
        self.assertEqual(__, denominators)
        self.assertEqual(__, numerators[-1] / denominators[-1])

    def test_averaging_rates_weights_groups_differently_from_pooling_counts(self) -> None:
        small = Counts(1, 0, 1, 0)
        large = Counts(9, 0, 1, 0)
        self.assertEqual(__, (small.tp + large.tp, small.fn + large.fn))
        self.assertEqual(__, (small.tp / (small.tp + small.fn) + large.tp / (large.tp + large.fn)) / 2)


def _probability(value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError("probability out of range")


def confusion(rows: Iterable[Scored], threshold: float) -> Counts:
    _probability(threshold)
    counts: dict[tuple[bool, bool], int] = dict.fromkeys(
        ((True, True), (False, True), (True, False), (False, False)), 0
    )
    for row in rows:
        _probability(row.score)
        if type(row.label) is not bool:
            raise ValueError("label must be boolean")
        prediction: bool = todo("apply the inclusive threshold")
        counts[row.label, prediction] += 1
    return Counts(*counts.values())


def _f1(counts: Counts) -> float:
    numerator = 2 * counts.tp
    denominator = numerator + counts.fp + counts.fn
    return todo("return zero for a zero denominator, otherwise divide")


def select_threshold(validation: Sequence[Scored], candidates: Sequence[float]) -> float:
    if not candidates:
        raise ValueError("no candidate thresholds")

    def rank(threshold: float) -> tuple[float, float]:
        score = _f1(confusion(validation, threshold))
        return todo("rank by F1 first and prefer the higher threshold on ties")

    return max(candidates, key=rank)


def evaluate(
    validation: Sequence[Scored], holdout: Sequence[Scored], candidates: Sequence[float]
) -> Evaluation:
    threshold = select_threshold(validation, candidates)
    return Evaluation(threshold, confusion(validation, threshold), confusion(holdout, threshold))
