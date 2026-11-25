from koans.deep_learning.evaluation import Counts, Evaluation
from maintainer.references.deep_learning_evaluation import confusion, select_threshold


def strict_threshold(rows, threshold: float) -> Counts:
    return confusion(rows, threshold + 1e-8)


def reverse_tie(validation, candidates) -> float:
    return min(candidates)


def tunes_on_holdout(validation, holdout, candidates) -> Evaluation:
    threshold = select_threshold(holdout, candidates)
    return Evaluation(threshold, confusion(validation, threshold), confusion(holdout, threshold))


CASES = {
    "predict": {"prediction": (19, 1)},
    "contrast": {"contrast": (20, 2)},
    "implement": {"confusion": strict_threshold},
    "break_cases": {"select_threshold": reverse_tie},
    "transfer": {"evaluate": tunes_on_holdout},
}
