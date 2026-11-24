"""State, node interface, and checkpoint types for the graph exercise."""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

State = dict[str, int]
Node = Callable[[State], str | None]
Status = Literal["complete", "paused", "failed"]


@dataclass(frozen=True)
class Checkpoint:
    next_node: str | None
    revision: int
    state: State


@dataclass(frozen=True)
class RunResult:
    status: Status
    checkpoint: Checkpoint
