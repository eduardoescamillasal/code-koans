"""Provider-neutral types and deterministic transport contract."""
from dataclasses import dataclass
from typing import Literal, Mapping, Protocol

Provider = Literal["claude", "azure"]
Role = Literal["user", "assistant"]
Payload = dict[str, object]


@dataclass(frozen=True)
class Message:
    role: Role
    text: str


@dataclass(frozen=True)
class Reply:
    provider: Provider
    text: str
    tokens: int


class Transport(Protocol):
    def send(self, provider: Provider, payload: Payload) -> Mapping[str, object]:
        ...


class ProviderError(Exception):
    def __init__(self, status: int) -> None:
        super().__init__(status)
        self.status = status
