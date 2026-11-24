"""Delivery envelopes and processor interface for local webhook fixtures."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Delivery:
    timestamp: int
    body: bytes
    signature: str


@dataclass(frozen=True)
class Event:
    id: str
    amount: int


@dataclass(frozen=True)
class Receipt:
    status: int
    value: int | None = None


class Processor(Protocol):
    def __call__(self, event: Event, /) -> int:
        """Return a result or raise before committing side effects."""
        ...
