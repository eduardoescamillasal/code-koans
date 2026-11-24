from koans.python._rest_service import Job, Response


from dataclasses import replace

prediction = ("queued", "queued")
contrast = ("queued", "complete")


class JobService:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._requests: dict[str, Response] = {}

    def submit(self, key: str, description: str) -> Response:
        if not key.strip() or not description.strip():
            return Response(422)
        prior = self._requests.get(key)
        if prior is not None:
            assert prior.job is not None
            return prior if prior.job.description == description else Response(409)
        job = Job(str(len(self._jobs) + 1), description)
        created = Response(201, job, f"/jobs/{job.id}")
        self._jobs[job.id] = job
        self._requests[key] = created
        return created

    def get(self, job_id: str) -> Response:
        job = self._jobs.get(job_id)
        return Response(404) if job is None else Response(200, job)

    def complete(self, job_id: str) -> Response:
        job = self._jobs.get(job_id)
        if job is None:
            return Response(404)
        updated = replace(job, state="complete")
        self._jobs[job_id] = updated
        return Response(200, updated)
