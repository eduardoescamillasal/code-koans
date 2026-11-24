CASES = {
    "predict": {"prediction": (False, 2)},
    "contrast": {"contrast": (False, 1, 1)},
    "implement": {"snapshot": lambda x: x[:]},
    "break_cases": {"snapshot": lambda x: x.copy()},
    "transfer": {"record": lambda state, branch, value: state},
}
