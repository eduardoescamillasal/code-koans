"""Distinguish an alias from a shallow copy and a rebinding.
Levels 1–2: predict and explain the identity checks before running. Record why
the outer lists differ but the nested dictionaries can still be shared.
Levels 3–5: snapshot a tree of exact dict/list containers and immutable leaves.
Preserve shared containers and self-cycles within the new graph. Keep dict keys
as-is. Use explicit traversal and a memo rather than copy.deepcopy.

For transfer, a timeline forks a snapshot of state, then appends one reading
to a named branch's points list. Return the updated state. Changes must remain
visible to other branches sharing that list in the fork.
"""

from typing import TypeVar, cast
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    row = {"count": 1}
    original = [row]
    alias = original
    alias[0]["count"] += 1
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (original is alias, original[0]["count"]))


def contrast(t: TestCase, *answers: object) -> None:
    original = [{"count": 1}]
    shallow = original[:]
    shallow[0]["count"] = 8
    shallow.append({})
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (shallow is original, len(original), original[0]["count"]))


T = TypeVar("T")
Timeline = dict[str, dict[str, list[int]]]


def snapshot(root: T) -> T:
    memo: dict[int, object] = {}

    def clone(value: object) -> object:
        if type(value) not in (list, dict):
            return value
        identity = id(value)
        if identity in memo:
            return memo[identity]

        # Register the empty destination before descending. A cycle can reenter clone.
        destination = {} if type(value) is dict else []
        todo("register the destination, then clone each child into it")
        return destination

    return cast(T, clone(root))


def record(state: Timeline, branch: str, value: int) -> Timeline:
    # A branch contains a points list. Fork the state before adding the point.
    todo("fork the state, append the point, and return the fork")


def practice(t: TestCase, exercise: Exercise) -> None:
    child = [1]
    state = [child, child]
    copied = exercise.snapshot(state)
    t.assertEqual(copied, [[1], [1]])
    t.assertIs(copied[0], copied[1])
    t.assertIsNot(copied[0], child)


def practice_break(t: TestCase, exercise: Exercise) -> None:
    root = {}
    root["loop"] = root
    fork = exercise.snapshot(root)
    t.assertIsNot(fork, root)
    t.assertIs(fork["loop"], fork)


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    state = {"north": {"points": [5]}}
    updated = exercise.record(state, "north", 6)
    t.assertEqual(updated["north"]["points"], [5, 6])
    t.assertEqual(state["north"]["points"], [5])
