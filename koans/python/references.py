"""Distinguish an alias from a shallow copy and a rebinding.
Levels 1–2: predict and explain the identity checks before running. Record why
the outer lists differ but the nested dictionaries can still be shared.
Levels 3–5: snapshot a tree of exact dict/list containers and immutable leaves.
Preserve shared containers and self-cycles within the new graph. Keep dict keys
as-is. Use explicit traversal and a memo rather than copy.deepcopy.

The final example follows two names for the same settings inside a fork.
"""

from copy import deepcopy
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

    def test_rebinding_a_name_leaves_the_other_name_alone(self) -> None:
        current = ["queued"]
        previous = current
        current = ["done"]
        self.assertEqual(__, previous)
        self.assertEqual(__, current is previous)

    def test_a_shallow_copy_preserves_repeated_child_references(self) -> None:
        shared = {"count": 1}
        rows = [shared, shared]
        clone = rows.copy()
        clone[1]["count"] += 2
        self.assertEqual(__, clone is rows)
        self.assertEqual(__, clone[0] is clone[1])
        self.assertEqual(__, rows[0]["count"])

    def test_deep_copy_detaches_a_container_and_keeps_shared_children(self) -> None:
        child = ["marker"]
        original = [child, child]
        fork = deepcopy(original)
        self.assertEqual(__, fork[0] is child)
        self.assertEqual(__, fork[0] is fork[1])
        fork[0].append("new")
        self.assertEqual(__, original[1])

    def test_a_copy_can_point_to_itself(self) -> None:
        node: list[object] = []
        node.append(node)
        shallow = node.copy()
        detached = deepcopy(node)
        self.assertEqual(__, shallow[0] is shallow)
        self.assertEqual(__, detached[0] is detached)
        self.assertEqual(__, detached[0] is node)

    def test_a_fork_keeps_shared_settings_inside_the_new_graph(self) -> None:
        defaults = {"volume": 3}
        original = {"speaker": defaults, "headphones": defaults}
        preview = deepcopy(original)
        preview["speaker"]["volume"] = 8
        self.assertEqual(__, preview["headphones"]["volume"])
        self.assertEqual(__, original["speaker"]["volume"])
        self.assertEqual(__, preview["speaker"] is original["speaker"])


T = TypeVar("T")


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
