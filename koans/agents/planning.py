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

from collections.abc import Iterable, Mapping
from heapq import heapify, heappop, heappush

from koans import Koan, __, todo


class AboutDependencyPlanning(Koan):
    def test_a_ready_job_has_no_prerequisites(self) -> None:
        graph = {"package": {"compile"}, "compile": set(), "test": {"compile"}}
        self.assertEqual(__, tuple(job for job, deps in graph.items() if not deps))

    def test_a_cycle_can_leave_nothing_ready(self) -> None:
        graph = {"package": {"compile"}, "compile": {"package"}, "test": {"compile"}}
        self.assertEqual(__, tuple(job for job, deps in graph.items() if not deps))

    def test_prerequisites_run_first(self) -> None:
        graph = {"send": ["review"], "review": ["draft"], "draft": []}
        self.assertEqual(plan(graph), ["draft", "review", "send"])

    def test_ready_work_can_hide_a_separate_cycle(self) -> None:
        # Having an initially ready job does not prove that the remaining jobs are acyclic.
        with self.assertRaises(ValueError):
            plan({"ready": [], "closed": ["closed"]})

    def test_changes_propagate_to_dependents(self) -> None:
        graph = {"clean": [], "package": ["clean"], "publish": ["package"], "note": []}
        self.assertEqual(rebuild(graph, "package"), ["package", "publish"])


Dependencies = Mapping[str, Iterable[str]]


def plan(dependencies: Dependencies) -> list[str]:
    downstream: dict[str, list[str]] = {job: [] for job in dependencies}
    remaining: dict[str, int] = {}
    for job, prerequisites in dependencies.items():
        parents = set(prerequisites)
        remaining[job] = len(parents)
        for parent in parents:
            if parent not in downstream:
                raise ValueError("missing prerequisite")
            downstream[parent].append(job)

    ready = [job for job, count in remaining.items() if count == 0]
    heapify(ready)
    order: list[str] = []
    while ready:
        job = heappop(ready)
        order.append(job)
        for dependent in downstream[job]:
            todo("decrement this dependent's unmet prerequisites")
            if remaining[dependent] == 0:
                heappush(ready, dependent)

    todo("detect an incomplete order before returning it")


def rebuild(dependencies: Dependencies, changed: str) -> list[str]:
    graph = {job: set(parents) for job, parents in dependencies.items()}
    if changed not in graph:
        raise ValueError("unknown job")
    affected = {changed}
    todo("walk the plan and propagate changes through prerequisites")
