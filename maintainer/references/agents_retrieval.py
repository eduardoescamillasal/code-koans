import math

prediction = True
contrast = False


def unit(vector):
    if not all(math.isfinite(value) for value in vector):
        raise ValueError("nonfinite coordinate")
    norm = math.hypot(*vector)
    if not math.isfinite(norm) or norm == 0:
        raise ValueError("expected a finite nonzero vector")
    return [value / norm for value in vector]


def retrieve(query, documents, k):
    if k < 0:
        raise ValueError("negative result limit")
    direction = unit(query)
    ranked = []
    for record in documents:
        key, vector, _ = record
        if len(vector) != len(direction):
            raise ValueError("dimension mismatch")
        score = math.fsum(a*b for a, b in zip(direction, unit(vector)))
        ranked.append((-score, key, record))
    ranked.sort(key=lambda entry: entry[:2])
    return [entry[2] for entry in ranked[:k]]


def evidence(query, documents, k, budget):
    selected, excerpts = [], []
    used = 0
    for key, _, text in retrieve(query, documents, k):
        cost = len(text) + bool(excerpts)
        if used + cost <= budget:
            selected.append(key)
            excerpts.append(text)
            used += cost
    return selected, "\n".join(excerpts)
