"""Treat columns as the images of basis vectors.
Predict how composition order changes a transformation. Implement rectangular
matrix multiplication on nonempty, rectangular row lists. Reject invalid
shapes with ValueError. Derive (AB)[i,j] = sum_k A[i,k] B[k,j] by expanding
column j of B in the basis before applying the linear map A.

For transfer, apply a list of linear maps to many displacements stored as
columns. Each map consumes the output of the preceding map and may change the
number of coordinates. An empty sequence leaves the input unchanged.
"""


from koans import Koan, __, todo


class AboutLinearMaps(Koan):
    def test_scaling_before_shearing(self) -> None:
        # Double x, then add x to y.
        x, y = 2, 3
        x = 2 * x
        self.assertEqual(__, (x, x + y))

    def test_shearing_before_scaling(self) -> None:
        # Add x to y, then double x.
        x, y = 2, 3
        y = x + y
        self.assertEqual(__, (2 * x, y))

    def test_basis_vectors_pick_out_columns(self) -> None:
        rows = [[2, 5], [3, 7]]
        left_basis = [1, 0]
        right_basis = [0, 1]
        self.assertEqual(__, [sum(a * b for a, b in zip(row, left_basis)) for row in rows])
        self.assertEqual(__, [sum(a * b for a, b in zip(row, right_basis)) for row in rows])

    def test_rows_dot_columns_not_other_rows(self) -> None:
        a = [[1, 2], [3, 4]]
        b = [[2, 10], [3, 20]]
        columns = list(zip(*b))
        self.assertEqual(__, columns[0])
        self.assertEqual(__, sum(x * y for x, y in zip(a[0], columns[0])))
        self.assertEqual(__, sum(x * y for x, y in zip(a[1], columns[1])))

    def test_zip_truncates_unless_we_require_equal_lengths(self) -> None:
        row = [2, 4]
        column = [3]
        self.assertEqual(__, list(zip(row, column)))
        try:
            list(zip(row, column, strict=True))
        except ValueError as error:
            result = type(error).__name__
        else:
            result = "accepted"
        self.assertEqual(__, result)


Matrix = list[list[float]]


def _shape(matrix: Matrix) -> tuple[int, int]:
    if not matrix or not matrix[0]:
        raise ValueError("empty matrix")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("ragged matrix")
    return len(matrix), width


def matmul(left: Matrix, right: Matrix) -> Matrix:
    _, inner = _shape(left)
    height, _ = _shape(right)
    if inner != height:
        todo("reject incompatible inner dimensions before zipping")
    columns = list(zip(*right))

    def cell(row: list[float], column: tuple[float, ...]) -> float:
        todo("calculate one row-column dot product")

    return [[cell(row, column) for column in columns] for row in left]


def transform(displacements: Matrix, maps: list[Matrix]) -> Matrix:
    # Each map acts on the result left behind by the previous map.
    todo("apply the maps in sequence to the column vectors")
