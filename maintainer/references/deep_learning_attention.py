import math

prediction = (0.5, 0.5)
contrast = (1.0, 0.0)


def attend(query, keys, values, keep):
    if not query or not keys or len(keys) != len(values) or len(keys) != len(keep):
        raise ValueError("incompatible lengths")
    if (not values[0] or any(len(row) != len(values[0]) for row in values)
            or any(len(row) != len(query) for row in keys) or not any(keep)):
        raise ValueError("invalid dimensions or mask")
    scale = math.sqrt(len(query))
    scores = [sum(q*k for q, k in zip(query, key)) / scale if visible else -math.inf
              for key, visible in zip(keys, keep)]
    peak = max(scores)
    exps = [math.exp(score - peak) for score in scores]
    total = sum(exps)
    weights = [value / total for value in exps]
    output = [sum(w*v for w, v in zip(weights, col)) for col in zip(*values)]
    return output, weights


def causal_smooth(keys, values):
    return [
        attend(query, keys, values, [index <= end for index in range(len(keys))])[0]
        for end, query in enumerate(keys)
    ]
