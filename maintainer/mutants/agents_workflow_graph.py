from koans.agents._workflow_graph import Checkpoint, RunResult
from maintainer.references.agents_workflow_graph import WorkflowGraph


class IgnoreBudget(WorkflowGraph):
    def advance(self, checkpoint: Checkpoint, budget: int) -> RunResult:
        return super().advance(checkpoint, budget + 3)


class ForgetCheckpoint(WorkflowGraph):
    def advance(self, checkpoint: Checkpoint, budget: int) -> RunResult:
        result = super().advance(checkpoint, budget)
        if result.status == "failed":
            return RunResult("failed", checkpoint)
        return result


class OnePage(WorkflowGraph):
    def run_pages(self, checkpoint: Checkpoint, page_size: int, pages: int) -> RunResult:
        return self.advance(checkpoint, page_size)


CASES = {
    "predict": {"prediction": (1, 2)},
    "contrast": {"contrast": (2, 2)},
    "implement": {"WorkflowGraph": IgnoreBudget},
    "break_cases": {"WorkflowGraph": ForgetCheckpoint},
    "transfer": {"WorkflowGraph": OnePage},
}
