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

from koans import Koan, __, todo
from koans.python._rest_service import Job, Response


class AboutRestResources(Koan):
    def test_aliasing_keeps_the_resource_snapshot(self) -> None:
        original = Job("1", "index")
        alias = original
        self.assertEqual(__, (original.state, alias.state))

    def test_replacing_a_resource_produces_a_new_snapshot(self) -> None:
        original = Job("1", "index")
        updated = replace(original, state="complete")
        self.assertEqual(__, (original.state, updated.state))

    def test_creating_a_job_supplies_a_location(self) -> None:
        api = JobService()
        create = api.submit("sample", "refresh index")
        self.assertEqual(create, Response(201, Job("1", "refresh index"), "/jobs/1"))
        self.assertEqual(api.get("1"), Response(200, Job("1", "refresh index")))

    def test_a_replayed_key_cannot_change_its_input(self) -> None:
        api = JobService()
        self.assertEqual(api.submit("same", ""), Response(422))
        self.assertEqual(api.submit("same", "refresh").job, Job("1", "refresh"))
        self.assertEqual(api.submit("same", "different"), Response(409))

    def test_completion_keeps_the_original_creation_snapshot(self) -> None:
        api = JobService()
        api.submit("first", "rebuild")
        self.assertEqual(api.complete("1"), Response(200, Job("1", "rebuild", "complete")))


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
