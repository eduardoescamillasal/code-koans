CASES = {
    "predict": {"prediction": (False, 2)},
    "contrast": {"contrast": (False, 1, 1)},
    "implement": {"snapshot": lambda x: x[:]},
    "break_cases": {"snapshot": lambda x: x.copy()},
    "transfer": {"snapshot": lambda state: {name: settings.copy() for name, settings in state.items()}},
}
