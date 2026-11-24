import math

prediction = "overflow"
contrast = (0.5, 0.5)


def cross_entropy(logits, target):
    if type(target) is not int or not 0 <= target < len(logits):
        raise ValueError("invalid target")
    if not all(math.isfinite(value) for value in logits):
        raise ValueError("expected finite logits")
    peak = max(logits)
    shifted = [value - peak for value in logits]
    weights = [math.exp(value) for value in shifted]
    total = sum(weights)
    gradient = [weight / total for weight in weights]
    gradient[target] -= 1
    return math.log(total) - shifted[target], gradient


def calibrate(logits, target, bias, affected):
    shifted = list(logits)
    for index in affected:
        shifted[index] += bias
    loss, gradient = cross_entropy(shifted, target)
    return loss, sum(gradient[index] for index in affected)
