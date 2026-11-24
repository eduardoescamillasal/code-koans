CASES = {
    "predict": {"prediction": ((10, 20), (10, 20, 30))},
    "contrast": {"contrast": ((10, 20), (30,))},
    "implement": {"windows": lambda source, width: iter([(1, 2), (1, 3)])},
    "break_cases": {"windows": lambda source, width: iter(())},
    "transfer": {"first_rises": lambda readings, limit: list(range(limit))},
}
