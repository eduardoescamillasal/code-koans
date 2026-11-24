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

from koans import __

prediction = __
contrast = __


def snapshot(root):
    raise AssertionError("Implement references")


def record(state, branch, value):
    raise AssertionError("Implement record")
