CASES = {
    "predict": {"prediction": False},
    "contrast": {"contrast": True},
    "implement": {"retrieve": lambda q, docs, k: docs[:k]},
    "break_cases": {"retrieve": lambda q, docs, k: docs[:k]},
    "transfer": {"evidence": lambda query, docs, k, budget: ([], "")},
}
