from koans.agents._grounded_qa import Answer, Example, Score
from maintainer.references.agents_grounded_qa import GroundedQA


class StopAtFirstOverflow(GroundedQA):
    def answer(self, question: str, budget: int) -> Answer | None:
        selected = []
        for excerpt in self.retriever.search(question):
            if len(excerpt.text) > budget:
                break
            selected.append(excerpt)
            budget -= len(excerpt.text)
        return self.generator.generate(question, tuple(selected)) if selected else None


class TrustAllCitations(GroundedQA):
    def answer(self, question: str, budget: int) -> Answer | None:
        excerpts = tuple(doc for doc in self.retriever.search(question) if len(doc.text) <= budget)
        return self.generator.generate(question, excerpts) if excerpts else None


class OrderMatters(GroundedQA):
    def evaluate(self, examples: tuple[Example, ...], budget: int) -> Score:
        results = [self.answer(example.question, budget) for example in examples]
        return Score(len(examples), sum(answer is not None for answer in results),
                     sum(result == example.expected for result, example in zip(results, examples)))


CASES = {
    "predict": {"prediction": False},
    "contrast": {"contrast": True},
    "implement": {"GroundedQA": StopAtFirstOverflow},
    "break_cases": {"GroundedQA": TrustAllCitations},
    "transfer": {"GroundedQA": OrderMatters},
}
