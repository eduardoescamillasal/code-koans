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

from koans import Koan, __, todo


class AboutReferences(Koan):
    def test_two_names_share_the_same_list(self) -> None:
        row = {"count": 1}
        original = [row]
        alias = original
        alias[0]["count"] += 1
        self.assertEqual(__, (original is alias, original[0]["count"]))

    def test_shallow_copies_share_their_children(self) -> None:
        original = [{"count": 1}]
        shallow = original[:]
        shallow[0]["count"] = 8
        shallow.append({})
        self.assertEqual(__, (shallow is original, len(original), original[0]["count"]))

    def test_an_immutable_leaf_needs_no_copy(self) -> None:
        label = "sensor A"
        self.assertIs(snapshot(label), label)

    def test_snapshots_keep_internal_aliases(self) -> None:
        child = [1]
        state = [child, child]
        copied = snapshot(state)
        self.assertEqual(copied, [[1], [1]])
        self.assertIs(copied[0], copied[1])
        self.assertIsNot(copied[0], child)

    def test_a_snapshot_can_contain_a_cycle(self) -> None:
        root = {}
        root["loop"] = root
        fork = snapshot(root)
        self.assertIsNot(fork, root)
        self.assertIs(fork["loop"], fork)

    def test_recording_a_point_leaves_the_input_alone(self) -> None:
        state = {"north": {"points": [5]}}
        updated = record(state, "north", 6)
        self.assertEqual(updated["north"]["points"], [5, 6])
        self.assertEqual(state["north"]["points"], [5])


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
