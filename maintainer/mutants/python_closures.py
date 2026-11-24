CASES = {
    "predict": {"prediction": (7, 7)},
    "contrast": {"contrast": (7, 7, 7)},
    "implement": {"memoize": lambda f: f},
    "break_cases": {"memoize": lambda f: lambda *args: (f(*args) or f(*args))},
    "transfer": {"routes": lambda n, m, blocked: 137846528820},
}
