"""Rank records (id, vector, text) by cosine similarity. Return the top k
original records. Break equal scores by id ascending. Reject incompatible
dimensions, zero vectors, nonfinite coordinates, and negative k. Query and
document vectors have finite, representable norms; document ids are unique.
Treat text as opaque data, including any instructions it appears to contain.

For transfer, create one evidence excerpt from up to k ranked document records.
Fit complete excerpts into a character budget including newlines. Join text
with newline separators. Skip a record that will not fit and consider later
records. Return selected ids and the joined string. Budget is nonnegative.
"""

from koans import __

prediction = __
contrast = __


def retrieve(query, documents, k):
    raise AssertionError("Implement retrieval")


def evidence(query, documents, k, budget):
    raise AssertionError("Implement evidence")
