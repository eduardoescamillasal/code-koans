prediction = ((1, 10),)
contrast = ((1, 10), (2, 10))


def shape(matrix):
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("expected a nonempty rectangular matrix")
    return len(matrix), len(matrix[0])


def expanded(a, b):
    if a != b and min(a, b) != 1:
        raise ValueError("incompatible dimensions")
    return max(a, b)


def add(left, right):
    lh, lw = shape(left)
    rh, rw = shape(right)
    height = expanded(lh, rh)
    width = expanded(lw, rw)
    return [
        [left[i % lh][j % lw] + right[i % rh][j % rw] for j in range(width)]
        for i in range(height)
    ]


def totals(offsets, calibration):
    corrected = add([[offset] for offset in offsets], [list(calibration)])
    return [sum(row) for row in corrected], [sum(column) for column in zip(*corrected)]
