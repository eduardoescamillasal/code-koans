def truncate(left, right):
    return [[a + b for a, b in zip(x, y)] for x, y in zip(left, right)]

CASES = {
    "predict": {"prediction": ((1, 10), (2, 10))},
    "contrast": {"contrast": ((1, 10),)},
    "implement": {"add": truncate},
    "break_cases": {"add": truncate},
    "transfer": {"totals": lambda offsets, calibration: (offsets, calibration)},
}
