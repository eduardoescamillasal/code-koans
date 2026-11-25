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
from koans.agents._workflow_graph import Checkpoint, Node, RunResult


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

    def test_a_frozen_record_can_still_contain_a_mutable_dictionary(self) -> None:
        first = Checkpoint("start", 1, {"count": 0})
        candidate = Checkpoint("next", 2, first.state)
        candidate.state["count"] += 1
        self.assertEqual(__, first.revision)
        self.assertEqual(__, first.state["count"])
        self.assertEqual(__, candidate.state is first.state)

    def test_a_transition_validates_its_route_before_committing(self) -> None:
        current = Checkpoint("start", 1, {"count": 0})
        proposed = current.state.copy()
        proposed["count"] = 7
        destination = "later"
        graph = {"start"}
        if destination in graph:
            current = Checkpoint(destination, 2, proposed)
        self.assertEqual(__, current.revision)
        self.assertEqual(__, current.state)
        self.assertEqual(__, current.next_node)

    def test_pausing_preserves_the_next_node(self) -> None:
        page = RunResult("paused", Checkpoint("next", 3, {"count": 9}))
        self.assertEqual(__, page.status == "complete")
        self.assertEqual(__, page.checkpoint.next_node)
        self.assertEqual(__, page.checkpoint.revision)


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
