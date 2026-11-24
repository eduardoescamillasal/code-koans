"""Design an in-memory application service for POST /jobs and GET /jobs/{id}.
Predict aliasing versus replacement for frozen resource snapshots. Submit
returns 201 with a Location and a queued job. An identical key and description
returns the original creation response, including after the job completes.
Reusing a key for different input returns 409. A blank key or description
returns 422 and consumes no ID. GET returns 200 or 404. IDs are sequential
strings starting at "1". Separate request validation from state mutation.
For transfer, complete a known job, returning 200 with the latest snapshot.
Repeating completion is harmless. A missing job returns 404. No HTTP server
is involved. Each instance describes a single-process, sequential API service."""

from dataclasses import replace
from unittest import TestCase

from koans import Exercise, __, todo
from koans.python._rest_service import Job, Response


def predict(t: TestCase, *answers: object) -> None:
    original = Job("1", "index")
    alias = original
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (original.state, alias.state))


def contrast(t: TestCase, *answers: object) -> None:
    original = Job("1", "index")
    updated = replace(original, state="complete")
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, (original.state, updated.state))


class JobService:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._requests: dict[str, Response] = {}

    def submit(self, key: str, description: str) -> Response:
        if not key.strip() or not description.strip():
            return Response(422)
        prior = self._requests.get(key)
        if prior is not None:
            todo("replay the original response or reject a conflicting description")
        job = Job(str(len(self._jobs) + 1), description)
        created = Response(201, job, f"/jobs/{job.id}")
        todo("persist the job and creation response, then return the response")

    def get(self, job_id: str) -> Response:
        job = self._jobs.get(job_id)
        todo("turn the lookup into a found or missing response")

    def complete(self, job_id: str) -> Response:
        # Job is frozen. The creation response must keep its original snapshot.
        job = self._jobs.get(job_id)
        todo("replace the current snapshot and return the new representation")


def practice(t: TestCase, exercise: Exercise) -> None:
    api = exercise.JobService()
    create = api.submit("sample", "refresh index")
    t.assertEqual(create, Response(201, Job("1", "refresh index"), "/jobs/1"))
    t.assertEqual(api.get("1"), Response(200, Job("1", "refresh index")))


def practice_break(t: TestCase, exercise: Exercise) -> None:
    api = exercise.JobService()
    t.assertEqual(api.submit("same", ""), Response(422))
    t.assertEqual(api.submit("same", "refresh").job, Job("1", "refresh"))
    t.assertEqual(api.submit("same", "different"), Response(409))


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    api = exercise.JobService()
    api.submit("first", "rebuild")
    t.assertEqual(api.complete("1"), Response(200, Job("1", "rebuild", "complete")))
