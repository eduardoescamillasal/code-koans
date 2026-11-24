from dataclasses import replace
from types import SimpleNamespace
from unittest import TestCase

from koans.python._rest_service import Job, Response


def predict(t: TestCase, s: SimpleNamespace) -> None:
    original = Job("1", "index")
    alias = original
    t.assertEqual(s.prediction, (original.state, alias.state))


def contrast(t: TestCase, s: SimpleNamespace) -> None:
    original = Job("1", "index")
    updated = replace(original, state="complete")
    t.assertEqual(s.contrast, (original.state, updated.state))


def implement(t: TestCase, s: SimpleNamespace) -> None:
    api = s.JobService()
    expected = Job("1", "index")
    t.assertEqual(api.submit("k", "index"), Response(201, expected, "/jobs/1"))
    t.assertEqual(api.get("1"), Response(200, expected))
    t.assertEqual(api.get("77"), Response(404))


def break_cases(t: TestCase, s: SimpleNamespace) -> None:
    api = s.JobService()
    t.assertEqual(api.submit("k", " "), Response(422))
    t.assertEqual(api.submit(" ", "index"), Response(422))
    original = api.submit("k", "index")
    t.assertEqual(api.submit("k", "index"), original)
    t.assertEqual(api.submit("k", "different"), Response(409))
    t.assertEqual(api.submit("other", "index"), Response(201, Job("2", "index"), "/jobs/2"))
    t.assertEqual(s.JobService().get("1"), Response(404))


def transfer(t: TestCase, s: SimpleNamespace) -> None:
    api = s.JobService()
    original = api.submit("r", "refresh")
    complete = Response(200, Job("1", "refresh", "complete"))
    t.assertEqual(api.complete("1"), complete)
    t.assertEqual(api.complete("1"), complete)
    t.assertEqual(api.get("1"), complete)
    t.assertEqual(api.complete("missing"), Response(404))
    t.assertEqual(api.submit("r", "refresh"), original)
    t.assertEqual(original.job, Job("1", "refresh"))
