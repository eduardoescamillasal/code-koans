from collections.abc import Iterable, Sequence

from koans.deep_learning.evaluation import Scored, Counts, Evaluation

prediction = (19, 0)
contrast = (19, 2)


def _probability(value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError("probability out of range")


def confusion(rows: Iterable[Scored], threshold: float) -> Counts:
    _probability(threshold)
    counts = dict.fromkeys(((True, True), (False, True), (True, False), (False, False)), 0)
    for row in rows:
        _probability(row.score)
        if type(row.label) is not bool:
            raise ValueError("label must be boolean")
        counts[row.label, row.score >= threshold] += 1
    return Counts(*counts.values())


def _f1(counts: Counts) -> float:
    numerator = 2 * counts.tp
    denominator = numerator + counts.fp + counts.fn
    return numerator / denominator if denominator else 0.0


def select_threshold(validation: Sequence[Scored], candidates: Sequence[float]) -> float:
    if not candidates:
        raise ValueError("no candidate thresholds")
    return max(candidates, key=lambda candidate: (_f1(confusion(validation, candidate)), candidate))


def evaluate(
    validation: Sequence[Scored], holdout: Sequence[Scored], candidates: Sequence[float]
) -> Evaluation:
    threshold = select_threshold(validation, candidates)
    return Evaluation(threshold, confusion(validation, threshold), confusion(holdout, threshold))
