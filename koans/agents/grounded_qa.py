"""Build a retrieval-grounded answering service with injected retriever and
generator interfaces. Supply complete excerpts in rank order under a total
character budget (sum of text lengths). Skip excerpts that do not fit and
keep looking. A negative budget raises ValueError. Abstain by returning None
if no evidence fits, or if a generated answer has blank text, missing or
duplicate citations, or cites an ID outside the supplied excerpts. Never pass
unselected excerpts to the generator. Documents remain opaque data. The
citation guard checks provenance only and cannot verify claim entailment.
For transfer, score examples in order. Count total cases, non-abstentions,
and exact matches. An abstention matches an expected None. Otherwise compare
answer text exactly and citation IDs as sets, because rendering order can vary."""

from koans import __
from koans.agents._grounded_qa import Answer, Document, Example, Generator, Retriever, Score

prediction = __
contrast = __



class GroundedQA:
    def __init__(self, retriever: Retriever, generator: Generator) -> None:
        self.retriever = retriever
        self.generator = generator

    def answer(self, question: str, budget: int) -> Answer | None:
        raise AssertionError("Implement answer")

    def evaluate(self, examples: tuple[Example, ...], budget: int) -> Score:
        raise AssertionError("Implement evaluate")
