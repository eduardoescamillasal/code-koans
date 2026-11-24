"""Compare subtraction at two scales in binary64 floating point.
Implement stable categorical cross-entropy from finite logits and a target index.
Return (loss, gradient list). Shift by the largest logit before exponentiating.
Derive dL/dz_j from L = log(sum(exp(z))) - z_target to get p_j - 1[j=target].
Reject empty logits, nonfinite logits, and invalid targets with ValueError.

For transfer, a single adjustable bias is added to two of three class
logits. Return the loss and derivative with respect to bias for the supplied
logits, target, and bias. The two affected class indices are distinct.
"""

from koans import __

prediction = __
contrast = __


def cross_entropy(logits, target):
    raise AssertionError("Implement precision")


def calibrate(logits, target, bias, affected):
    raise AssertionError("Implement calibrate")
