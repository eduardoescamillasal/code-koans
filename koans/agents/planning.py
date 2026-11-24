"""Find a deterministic execution order for a dependency graph.
Input maps job ids to iterables of prerequisite ids. Treat duplicate edges as
one. Return job ids, choosing the lexicographically smallest available job at
each step. Reject missing prerequisites and any cycle with ValueError.
Aim for O(E + V log V) using an in-degree table and a priority queue.

For transfer, given a job whose output changed, return the jobs that need a
rebuild in deterministic dependency order. Include the changed job and all
transitive dependents. Raise ValueError for unknown jobs and invalid graphs.
Prerequisite lists may be single-pass iterators.
"""

from koans import __

prediction = __
contrast = __


def plan(dependencies):
    raise AssertionError("Implement planning")


def rebuild(dependencies, changed):
    raise AssertionError("Implement rebuild")
