from koans.python._rest_service import Response
from maintainer.references.python_rest_service import JobService


class WrongStatus(JobService):
    def submit(self, key: str, description: str) -> Response:
        result = super().submit(key, description)
        return Response(200, result.job)


class LatestOnReplay(JobService):
    def submit(self, key: str, description: str) -> Response:
        if key in self._requests:
            return self._requests[key]
        return super().submit(key, description)


class ReadOnlyCompletion(JobService):
    def complete(self, job_id: str) -> Response:
        return self.get(job_id)


CASES = {
    "predict": {"prediction": ("queued", "complete")},
    "contrast": {"contrast": ("complete", "complete")},
    "implement": {"JobService": WrongStatus},
    "break_cases": {"JobService": LatestOnReplay},
    "transfer": {"JobService": ReadOnlyCompletion},
}
