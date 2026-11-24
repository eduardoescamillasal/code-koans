"""Inputs and results for citation-checked retrieval and evaluation."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Document:
    id: str
    text: str


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[str, ...]


@dataclass(frozen=True)
class Example:
    question: str
    expected: Answer | None


@dataclass(frozen=True)
class Score:
    total: int
    answered: int
    exact: int


class Retriever(Protocol):
    def search(self, question: str) -> tuple[Document, ...]:
        """Return ranked excerpts with unique IDs."""
        ...


class Generator(Protocol):
    def generate(self, question: str, excerpts: tuple[Document, ...]) -> Answer:
        ...
