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

import math
from collections.abc import Iterable, Sequence
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    q, a, b = (1, 0), (7, 7), (1, 0)

    def dot(x: tuple[int, int], y: tuple[int, int]) -> int:
        return sum(i * j for i, j in zip(x, y))
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, dot(q, a) > dot(q, b))


def contrast(t: TestCase, *answers: object) -> None:
    a = 7 / math.hypot(7, 7)
    b = 1 / math.hypot(1, 0)
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, a > b)


Vector = Sequence[float]
Record = tuple[str, Vector, str]


def _unit(vector: Vector) -> list[float]:
    if not all(math.isfinite(value) for value in vector):
        raise ValueError("expected finite coordinates")
    norm = math.hypot(*vector)
    if not math.isfinite(norm) or norm == 0:
        raise ValueError("expected a finite nonzero norm")
    return [coordinate / norm for coordinate in vector]


def retrieve(query: Vector, documents: Iterable[Record], k: int) -> list[Record]:
    if k < 0:
        raise ValueError("negative result limit")
    direction = _unit(query)
    ranked: list[tuple[float, str, Record]] = []
    for record in documents:
        doc_id, vector, _ = record
        if len(vector) != len(direction):
            raise ValueError("dimension mismatch")
        normalized = _unit(vector)
        todo("store a sort key for higher similarity first, then document id")
    todo("return up to k original records in rank order")


def evidence(query: Vector, documents: Iterable[Record], k: int, budget: int) -> tuple[list[str], str]:
    chosen: list[str] = []
    excerpts: list[str] = []
    for doc_id, _, excerpt in retrieve(query, documents, k):
        # Every separator counts against the character budget.
        todo("accept an excerpt only when it fits the remaining space")
    return chosen, "\n".join(excerpts)


def practice(t: TestCase, exercise: Exercise) -> None:
    documents = [("down", (0, -3), "d"), ("up", (0, 2), "u")]
    t.assertEqual(exercise.retrieve((0, 1), documents, 1), [documents[1]])


def practice_break(t: TestCase, exercise: Exercise) -> None:
    docs = [("b", (1, 0), "late"), ("a", (9, 0), "first")]
    t.assertEqual(exercise.retrieve((1, 0), docs, 1), [docs[1]])
    with t.assertRaises(ValueError):
        exercise.retrieve((1, 0), [("x", (0, 0), "empty")], 1)


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    documents = [("a", (1, 0), "x"), ("b", (0, 1), "y")]
    t.assertEqual(exercise.evidence((1, 0), documents, 2, 3), (["a", "b"], "x\ny"))
