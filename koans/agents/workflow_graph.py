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

from koans import __
from koans.agents._workflow_graph import Checkpoint, Node, RunResult, State

prediction = __
contrast = __



class WorkflowGraph:
    def __init__(self, nodes: dict[str, Node]) -> None:
        self.nodes = dict(nodes)

    def advance(self, checkpoint: Checkpoint, budget: int) -> RunResult:
        raise AssertionError("Implement advance")

    def run_pages(self, checkpoint: Checkpoint, page_size: int, pages: int) -> RunResult:
        raise AssertionError("Implement run_pages")
