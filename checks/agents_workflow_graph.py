from types import SimpleNamespace
from unittest import TestCase

from koans.agents._workflow_graph import Checkpoint, RunResult, State


def predict(t: TestCase, s: SimpleNamespace) -> None:
    original = {"attempts": 1}
    candidate = original
    candidate["attempts"] += 1
    t.assertEqual(s.prediction, (original["attempts"], candidate["attempts"]))


def contrast(t: TestCase, s: SimpleNamespace) -> None:
    original = {"attempts": 1}
    candidate = original.copy()
    candidate["attempts"] += 1
    t.assertEqual(s.contrast, (original["attempts"], candidate["attempts"]))


def increment(state: State) -> str | None:
    state["count"] += 1
    return "inc" if state["count"] < 3 else None


def implement(t: TestCase, s: SimpleNamespace) -> None:
    start = Checkpoint("inc", 0, {"count": 0})
    graph = s.WorkflowGraph({"inc": increment})
    first = graph.advance(start, 1)
    t.assertEqual(first, RunResult("paused", Checkpoint("inc", 1, {"count": 1})))
    t.assertEqual(graph.advance(first.checkpoint, 2), RunResult("complete", Checkpoint(None, 3, {"count": 3})))
    t.assertEqual(start.state, {"count": 0})


def break_cases(t: TestCase, s: SimpleNamespace) -> None:
    def clean(state: State) -> str:
        state["count"] += 1
        return "bad"

    def explode(state: State) -> str:
        state["count"] += 100
        raise RuntimeError("transient error")

    def unknown(state: State) -> str:
        state["count"] += 200
        return "missing"

    start = Checkpoint("clean", 0, {"count": 0})
    for bad in (explode, unknown):
        graph = s.WorkflowGraph({"clean": clean, "bad": bad})
        t.assertEqual(graph.advance(start, 3), RunResult("failed", Checkpoint("bad", 1, {"count": 1})))
        with t.assertRaises(ValueError):
            graph.advance(start, -1)

    def loop(state: State) -> str:
        state["count"] += 1
        return "loop"

    graph = s.WorkflowGraph({"loop": loop})
    t.assertEqual(graph.advance(Checkpoint("loop", 0, {"count": 0}), 5),
                  RunResult("paused", Checkpoint("loop", 5, {"count": 5})))


def transfer(t: TestCase, s: SimpleNamespace) -> None:
    graph = s.WorkflowGraph({"inc": increment})
    start = Checkpoint("inc", 0, {"count": 0})
    first = graph.run_pages(start, 1, 2)
    t.assertEqual(first, RunResult("paused", Checkpoint("inc", 2, {"count": 2})))
    t.assertEqual(graph.run_pages(first.checkpoint, 1, 4),
                  RunResult("complete", Checkpoint(None, 3, {"count": 3})))
    t.assertEqual(graph.run_pages(start, 1, 0), RunResult("paused", start))

    attempted: list[int] = []

    def flaky(state: State) -> None:
        attempted.append(state["count"])
        state["count"] += 1
        if len(attempted) == 1:
            raise RuntimeError("temporary")

    retry_graph = s.WorkflowGraph({"flaky": flaky})
    restart = Checkpoint("flaky", 4, {"count": 10})
    failed = retry_graph.run_pages(restart, 1, 3)
    t.assertEqual(failed, RunResult("failed", restart))
    t.assertEqual(attempted, [10])
    t.assertEqual(retry_graph.run_pages(failed.checkpoint, 1, 1),
                  RunResult("complete", Checkpoint(None, 5, {"count": 11})))
    t.assertEqual(attempted, [10, 10])
    with t.assertRaises(ValueError):
        graph.run_pages(start, 0, 1)
    with t.assertRaises(ValueError):
        graph.run_pages(start, 1, -1)
