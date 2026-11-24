"""A node receives a private mutable state copy. It returns the name of the next
node or None to finish. The graph accepts a mapping of names to callables.
advance runs at most budget nodes. Each successful transition increments the
revision and commits the state only after validating the destination. A node
exception or an unknown route returns failed at the last committed checkpoint.
Return paused when the budget ends with pending work and complete when no work
remains. Negative budgets raise ValueError. Caller-owned state must stay intact.
For transfer, continue a graph in pages using a positive page size and at most
the requested number of pages. Stop at failure or completion. Reject invalid
page size or negative page count. Zero pages still reports the checkpoint status."""

from unittest import TestCase

from koans import Exercise, __, todo
from koans.agents._workflow_graph import Checkpoint, Node, RunResult, State


def predict(t: TestCase, *answers: object) -> None:
    original = {"attempts": 1}
    candidate = original
    candidate["attempts"] += 1
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (original["attempts"], candidate["attempts"]))


def contrast(t: TestCase, *answers: object) -> None:
    original = {"attempts": 1}
    candidate = original.copy()
    candidate["attempts"] += 1
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (original["attempts"], candidate["attempts"]))


class WorkflowGraph:
    def __init__(self, nodes: dict[str, Node]) -> None:
        self.nodes = dict(nodes)

    def advance(self, checkpoint: Checkpoint, budget: int) -> RunResult:
        if budget < 0:
            raise ValueError("negative node budget")
        current = Checkpoint(checkpoint.next_node, checkpoint.revision, checkpoint.state.copy())
        for _ in range(budget):
            if current.next_node is None:
                break
            candidate = current.state.copy()
            # Invoke the node on candidate and validate its destination before committing.
            todo("commit a successful transition or preserve the last accepted checkpoint")
        return RunResult("complete" if current.next_node is None else "paused", current)

    def run_pages(self, checkpoint: Checkpoint, page_size: int, pages: int) -> RunResult:
        if page_size < 1 or pages < 0:
            raise ValueError("invalid page limit")
        result = self.advance(checkpoint, 0)
        for _ in range(pages):
            todo("advance one page unless already finished or failed")
        return result


def _count_once(state: State) -> None:
    state["count"] += 1


def practice(t: TestCase, exercise: Exercise) -> None:
    start = Checkpoint("count", 2, {"count": 7})
    graph = exercise.WorkflowGraph({"count": _count_once})
    t.assertEqual(graph.advance(start, 1), RunResult("complete", Checkpoint(None, 3, {"count": 8})))
    t.assertEqual(start.state, {"count": 7})


def practice_break(t: TestCase, exercise: Exercise) -> None:
    def invalid(state: State) -> str:
        state["count"] += 99
        return "missing"

    start = Checkpoint("bad", 4, {"count": 1})
    graph = exercise.WorkflowGraph({"bad": invalid})
    t.assertEqual(graph.advance(start, 1), RunResult("failed", start))
    t.assertEqual(start.state, {"count": 1})


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    start = Checkpoint("count", 0, {"count": 0})
    graph = exercise.WorkflowGraph({"count": _count_once})
    t.assertEqual(graph.run_pages(start, 1, 0), RunResult("paused", start))
    t.assertEqual(graph.run_pages(start, 1, 3),
                  RunResult("complete", Checkpoint(None, 1, {"count": 1})))
