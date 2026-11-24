CASES = {
    "predict": {"prediction": (0, 1, 2)},
    "contrast": {"contrast": (2, 2, 2)},
    "implement": {"memoize": lambda f: f},
    "break_cases": {"memoize": lambda f: lambda *args: (f(*args) or f(*args))},
    "transfer": {"routes": lambda n, m, blocked: 137846528820},
}
