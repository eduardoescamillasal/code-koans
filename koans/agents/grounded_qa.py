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


from koans import Koan, __, todo
from koans.agents._grounded_qa import Answer, Document, Example, Generator, Retriever, Score


class AboutGroundedAnswers(Koan):
    def test_a_citation_can_exist_in_the_corpus(self) -> None:
        full_corpus, _ = _citation_candidates(limit=2)
        self.assertEqual(__, {"archive"} <= full_corpus)

    def test_a_corpus_citation_may_be_outside_context(self) -> None:
        _, in_context = _citation_candidates(limit=2)
        self.assertEqual(__, {"archive"} <= in_context)

    def test_answers_depend_on_selected_evidence(self) -> None:
        service = GroundedQA(_SampleCorpus(), _SampleGenerator())
        self.assertIsNone(service.answer("unknown", 20))
        self.assertEqual(service.answer("where?", 20), Answer("Local files", ("guide",)))

    def test_citations_must_come_from_the_supplied_context(self) -> None:
        class WrongCitation:
            def generate(self, question: str, excerpts: tuple[Document, ...]) -> Answer:
                return Answer("result", ("not-in-context",))

        service = GroundedQA(_SampleCorpus(), WrongCitation())
        self.assertIsNone(service.answer("where?", 20))

    def test_expected_abstentions_count_as_matches(self) -> None:
        service = GroundedQA(_SampleCorpus(), _SampleGenerator())
        examples = (Example("unknown", None),)
        self.assertEqual(service.evaluate(examples, 20), Score(1, 0, 1))


def _citation_candidates(limit: int) -> tuple[set[str], set[str]]:
    ranked = (Document("lead", "A"), Document("archive", "Older guidance"))
    full_corpus = {excerpt.id for excerpt in ranked}
    # This sketch filters by individual length. The service needs a total budget.
    in_context = {excerpt.id for excerpt in ranked if len(excerpt.text) <= limit}
    return full_corpus, in_context


class GroundedQA:
    def __init__(self, retriever: Retriever, generator: Generator) -> None:
        self.retriever = retriever
        self.generator = generator

    def answer(self, question: str, budget: int) -> Answer | None:
        if budget < 0:
            raise ValueError("negative evidence budget")
        selected: list[Document] = []
        for excerpt in self.retriever.search(question):
            todo("select excerpts within the remaining budget")
        if not selected:
            return None
        answer = self.generator.generate(question, tuple(selected))
        permitted = {excerpt.id for excerpt in selected}
        todo("return the answer only when its text and cited ids pass validation")

    def evaluate(self, examples: tuple[Example, ...], budget: int) -> Score:
        if budget < 0:
            raise ValueError("negative evidence budget")
        answered = exact = 0
        for example in examples:
            actual = self.answer(example.question, budget)
            todo("count non-abstentions and exact matches, including matching abstentions")
        return Score(len(examples), answered, exact)


class _SampleCorpus:
    def search(self, question: str) -> tuple[Document, ...]:
        return (Document("guide", "Local files"),) if question == "where?" else ()


class _SampleGenerator:
    def generate(self, question: str, excerpts: tuple[Document, ...]) -> Answer:
        return Answer(excerpts[0].text, (excerpts[0].id,))
