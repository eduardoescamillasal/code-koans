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

    def test_rows_multiply_columns(self) -> None:
        self.assertEqual(matmul([[2, 3]], [[5], [-1]]), [[7]])
        self.assertEqual(matmul([[1, 0], [0, 1]], [[9], [8]]), [[9], [8]])

    def test_incompatible_dimensions_are_rejected(self) -> None:
        # zip alone would silently drop a coordinate.
        with self.assertRaises(ValueError):
            matmul([[3, 4]], [[2]])

    def test_maps_consume_the_previous_output(self) -> None:
        points = [[2], [3]]
        self.assertEqual(transform(points, [[[1, 1]], [[4]]]), [[20]])


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
