# Math notes

## Linear maps and their derivatives

For an m-by-n matrix A, column k is A e_k, the image of input basis vector e_k.
If B's j-th column is Σ_k B[k,j] e_k, applying A yields Σ_k B[k,j] A e_k.
Taking coordinate i gives (AB)[i,j] = Σ_k A[i,k] B[k,j]. Changing the order
changes which map acts first.

The Jacobian of y = A x, using output coordinates for rows, is A. If L is a
scalar loss and g contains ∂L/∂y_i, the chain rule gives
∂L/∂x_j = Σ_i g_i A[i,j], or ∇_x L = Aᵀ g. Reverse-mode differentiation
computes such vector–Jacobian products without constructing dense Jacobians.

## Finite differences and reverse mode

Taylor-expand f(x+h) and f(x−h) around x. Subtracting cancels the even powers;
dividing by 2h leaves f′(x) with O(h²) error for a smooth function. In floating
point, very small h can erase the difference between the two function values.
Check several step sizes when validating a derivative.

For z = a + b, the local edge derivatives are 1 and 1. For z = a b, they are
b and a. Starting with ∂L/∂L = 1, visit nodes in reverse topological order.
For each edge, add the incoming gradient times the local derivative to its
parent. Every incoming edge contributes, even when two edges share a parent.
Broadcasting from a singleton coordinate is another form of reuse. Its
backward rule sums over all the expanded positions that read that coordinate.

## Stable probabilities

For logits z, p_j = exp(z_j) / Σ_k exp(z_k). Adding a common scalar cancels
between numerator and denominator. Let m = max(z). All exp(z_j − m) are at
most one and at least one is exactly one. Compute the target cross-entropy
as log(Σ_k exp(z_k − m)) − (z_target − m), so even a target probability that
would round to zero can have a finite loss. Differentiating yields
∂L/∂z_j = p_j − 1[j = target].

For attention, if q_i and k_i are independent with mean zero and variance one,
each product has variance one. Under independent coordinates their sum has
variance d. Dividing by √d scales the variance back to one. The mask removes
terms from the normalizer. An empty visible set leaves the distribution
undefined, so the koan raises an error.

## Cosine similarity

For nonzero vectors a and b, a·b = ‖a‖‖b‖ cos(θ). Divide by their lengths to
compare directions. Normalizing coordinates before taking their dot product
also avoids an intermediate product of two large vector norms.

## Interactions and batch gradients

For prediction ŷ = a + bx + cy + dxy, the effect of increasing x is b + dy.
That effect can change sign as y changes. For the loss (ŷ − t)², apply the
chain rule to get 2(ŷ − t) times (1, x, y, xy) for the four coefficients.
Average these vectors across the batch before updating the weights. Duplicating
every row leaves that mean gradient unchanged.

On the four balanced sign pairs x, y ∈ {−1, 1}, let t = xy. At zero weights the
residual is −xy. The bias and linear gradient sums cancel by symmetry. The
product-coordinate contribution is −2(xy)² = −2 for every row.

## Thresholds and cohort rates

A score becomes a label only after choosing an operating threshold. Lowering
the threshold can recover missed positives and introduce false alarms. F1
combines those errors through 2TP / (2TP + FP + FN). Select the threshold on
validation data, then evaluate that fixed threshold on a separate holdout.

Within a cohort, the false-negative rate is FN / (TP + FN). It is undefined
when there are no actual positives. Pooling the counts weights each cohort
by its number of actual positives. Averaging per-cohort rates gives
each eligible cohort the same weight.
