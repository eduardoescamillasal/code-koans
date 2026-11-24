"""Treat columns as the images of basis vectors.
Predict how composition order changes a transformation. Implement rectangular
matrix multiplication on nonempty, rectangular row lists. Reject invalid
shapes with ValueError. Derive (AB)[i,j] = sum_k A[i,k] B[k,j] by expanding
column j of B in the basis before applying the linear map A.

For transfer, apply a list of linear maps to many displacements stored as
columns. Each map consumes the output of the preceding map and may change the
number of coordinates. An empty sequence leaves the input unchanged.
"""

from koans import __

prediction = __
contrast = __


def matmul(left, right):
    raise AssertionError("Implement linear")


def transform(displacements, maps):
    raise AssertionError("Implement transform")
