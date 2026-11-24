from koans.agents._grounded_qa import Answer, Document, Example, Generator, Retriever, Score


prediction = True
contrast = False


class GroundedQA:
    def __init__(self, retriever: Retriever, generator: Generator) -> None:
        self.retriever = retriever
        self.generator = generator

    def answer(self, question: str, budget: int) -> Answer | None:
        if budget < 0:
            raise ValueError("negative evidence budget")
        selected: list[Document] = []
        for excerpt in self.retriever.search(question):
            if len(excerpt.text) <= budget:
                selected.append(excerpt)
                budget -= len(excerpt.text)
        if not selected:
            return None
        answer = self.generator.generate(question, tuple(selected))
        cited = set(answer.citations)
        permitted = {excerpt.id for excerpt in selected}
        if not answer.text.strip() or not cited or len(cited) != len(answer.citations):
            return None
        return answer if cited <= permitted else None

    def evaluate(self, examples: tuple[Example, ...], budget: int) -> Score:
        if budget < 0:
            raise ValueError("negative evidence budget")
        answered = exact = 0
        for example in examples:
            result = self.answer(example.question, budget)
            expected = example.expected
            if result is None:
                exact += expected is None
                continue
            answered += 1
            if expected is not None:
                exact += result.text == expected.text and set(result.citations) == set(expected.citations)
        return Score(len(examples), answered, exact)
