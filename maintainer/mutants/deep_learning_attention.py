CASES = {
    "predict": {"prediction": (1, 0)},
    "contrast": {"contrast": (0.5, 0.5)},
    "implement": {"attend": lambda q, k, v, m: (v[0], [1, 0])},
    "break_cases": {"attend": lambda q, k, v, m: (v[-1], [0, 1])},
    "transfer": {"causal_smooth": lambda keys, values: values},
}
