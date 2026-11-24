from koans.agents._workflow_graph import Checkpoint, Node, RunResult, State


prediction = (2, 2)
contrast = (1, 2)


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
            try:
                destination = self.nodes[current.next_node](candidate)
                if destination is not None and destination not in self.nodes:
                    return RunResult("failed", current)
            except Exception:
                return RunResult("failed", current)
            current = Checkpoint(destination, current.revision + 1, candidate.copy())
        return RunResult("complete" if current.next_node is None else "paused", current)

    def run_pages(self, checkpoint: Checkpoint, page_size: int, pages: int) -> RunResult:
        if page_size < 1 or pages < 0:
            raise ValueError("invalid page limit")
        result = self.advance(checkpoint, 0)
        for _ in range(pages):
            if result.status != "paused":
                break
            result = self.advance(result.checkpoint, page_size)
        return result
