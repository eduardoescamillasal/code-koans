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

    def test_creation_and_lookup_have_different_response_metadata(self) -> None:
        job = Job("3", "refresh")
        created = Response(201, job, "/jobs/3")
        found = Response(200, job)
        self.assertEqual(__, created.status == found.status)
        self.assertEqual(__, found.location)
        self.assertEqual(__, created.job == found.job)

    def test_replacing_the_registry_entry_keeps_a_stored_creation_response(self) -> None:
        queued = Job("1", "refresh")
        response = Response(201, queued, "/jobs/1")
        resource = {"1": queued}
        resource["1"] = replace(queued, state="complete")
        self.assertEqual(__, queued.state)
        self.assertEqual(__, resource["1"].state)
        self.assertEqual(__, response.job is resource["1"])

    def test_a_request_key_can_refer_to_one_original_input(self) -> None:
        indexed = {"job-key": "refresh"}
        replay = indexed.setdefault("job-key", "refresh")
        collision = indexed.setdefault("job-key", "reindex")
        self.assertEqual(__, replay)
        self.assertEqual(__, collision)
        self.assertEqual(__, len(indexed))


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
