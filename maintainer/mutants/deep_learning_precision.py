import math


CASES = {
    "predict": {"prediction": (0.5, 0.5)},
    "contrast": {"contrast": "overflow"},
    "implement": {"cross_entropy": lambda xs, i: (0, [0] * len(xs))},
    "break_cases": {"cross_entropy": lambda xs, i: (math.log(len(xs)), [1 / len(xs)] * len(xs))},
    "transfer": {"calibrate": lambda logits, target, bias, affected: (1, 0)},
}
