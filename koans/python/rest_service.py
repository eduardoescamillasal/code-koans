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

from koans import __
from koans.python._rest_service import Job, Response

prediction = __
contrast = __



class JobService:
    def __init__(self) -> None:
        pass

    def submit(self, key: str, description: str) -> Response:
        raise AssertionError("Implement submit")

    def get(self, job_id: str) -> Response:
        raise AssertionError("Implement get")

    def complete(self, job_id: str) -> Response:
        raise AssertionError("Implement complete")
