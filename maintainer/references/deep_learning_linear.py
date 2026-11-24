prediction = (4, 7)
contrast = (4, 5)


def matmul(left, right):
    if not left or not right or not left[0] or not right[0]:
        raise ValueError("expected nonempty matrices")
    inner, width = len(left[0]), len(right[0])
    if (len(right) != inner or any(len(row) != inner for row in left)
            or any(len(row) != width for row in right)):
        raise ValueError("incompatible matrix shapes")
    columns = list(zip(*right))
    return [[sum(a * b for a, b in zip(row, col)) for col in columns] for row in left]


def transform(displacements, maps):
    for matrix in maps:
        displacements = matmul(matrix, displacements)
    return displacements
