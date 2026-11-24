"""Value types shared by the REST service exercise and its checks."""
from dataclasses import dataclass
from typing import Literal

JobState = Literal["queued", "complete"]


@dataclass(frozen=True)
class Job:
    id: str
    description: str
    state: JobState = "queued"


@dataclass(frozen=True)
class Response:
    status: int
    job: Job | None = None
    location: str | None = None
