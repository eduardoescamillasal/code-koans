def unchecked(left, right):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*right)] for row in left]

CASES = {
    "predict": {"prediction": (4, 5)},
    "contrast": {"contrast": (4, 7)},
    "implement": {"matmul": lambda left, right: [[sum(row)] for row in left]},
    "break_cases": {"matmul": unchecked},
    "transfer": {"transform": lambda points, maps: points},
}
