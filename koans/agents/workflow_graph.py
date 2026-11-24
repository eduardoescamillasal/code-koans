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


from koans import Koan, __, todo
from koans.agents._workflow_graph import Checkpoint, Node, RunResult, State


class AboutWorkflowCheckpoints(Koan):
    def test_aliasing_mutates_the_checkpoint(self) -> None:
        original = {"attempts": 1}
        candidate = original
        candidate["attempts"] += 1
        self.assertEqual(__, (original["attempts"], candidate["attempts"]))

    def test_a_copy_isolates_candidate_changes(self) -> None:
        original = {"attempts": 1}
        candidate = original.copy()
        candidate["attempts"] += 1
        self.assertEqual(__, (original["attempts"], candidate["attempts"]))

    def test_a_valid_transition_commits_a_revision(self) -> None:
        start = Checkpoint("count", 2, {"count": 7})
        graph = WorkflowGraph({"count": _count_once})
        self.assertEqual(graph.advance(start, 1), RunResult("complete", Checkpoint(None, 3, {"count": 8})))
        self.assertEqual(start.state, {"count": 7})

    def test_an_unknown_route_cannot_commit_state(self) -> None:
        def invalid(state: State) -> str:
            state["count"] += 99
            return "missing"

        start = Checkpoint("bad", 4, {"count": 1})
        graph = WorkflowGraph({"bad": invalid})
        self.assertEqual(graph.advance(start, 1), RunResult("failed", start))
        self.assertEqual(start.state, {"count": 1})

    def test_page_limits_allow_resuming_a_checkpoint(self) -> None:
        start = Checkpoint("count", 0, {"count": 0})
        graph = WorkflowGraph({"count": _count_once})
        self.assertEqual(graph.run_pages(start, 1, 0), RunResult("paused", start))
        self.assertEqual(graph.run_pages(start, 1, 3),
                      RunResult("complete", Checkpoint(None, 1, {"count": 1})))


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
