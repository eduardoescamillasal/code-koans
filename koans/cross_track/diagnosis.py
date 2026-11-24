"""Investigate a neural training run with a deterministic read-only agent.

A trace contains (loss, gradient) pairs. First classify a trace with diagnose.
Then build training_report using your Value, matrix add, retrieve, parse, dispatch
and run implementations. See docs/diagnosis.md for the integration contract.
"""


import json
import math
from collections.abc import Sequence
from koans.agents.runtime import Context, Report

from koans import Koan, __, todo


class AboutTrainingDiagnosis(Koan):
    def test_zero_learning_rate_freezes_the_weight(self) -> None:
        weight, gradient, rate = 0.0, -6.0, 0.0
        self.assertEqual(__, weight - rate * gradient)

    def test_a_nonzero_rate_moves_the_weight(self) -> None:
        weight, gradient, rate = 0.0, -6.0, 0.25
        self.assertEqual(__, weight - rate * gradient)

    def test_loss_and_gradient_identify_two_training_outcomes(self) -> None:
        self.assertEqual(diagnose([(10, -1), (5, -1)]), "loss decreasing")
        self.assertEqual(diagnose([(10, 0), (10, 0)]), "inspect gradient")

    def test_invalid_samples_cannot_be_diagnosed(self) -> None:
        with self.assertRaises(ValueError):
            diagnose([(2, 3), (float("nan"), 1)])
        self.assertEqual(diagnose([(2, -1), (3, 2)]), "reduce learning rate")

    def test_the_agent_reads_the_trace_with_read_only_tools(self) -> None:
        status, text, events = training_report(0)
        self.assertEqual((status, text), ("final", "check learning rate"))
        self.assertEqual([event["ok"] for event in events], [False, True])


Trace = Sequence[tuple[float, float]]


def diagnose(trace: Trace) -> str:
    if len(trace) < 2 or not all(math.isfinite(value) for row in trace for value in row):
        raise ValueError("expected at least two finite samples")
    start_loss = trace[0][0]
    current_loss, current_gradient = trace[-1]
    todo("classify the loss trend and distinguish the two flat-loss cases")


def _train(rate: float) -> list[tuple[float, float]]:
    weight = 0.0
    trace: list[tuple[float, float]] = []
    for _ in range(3):
        # Broadcast the scalar parameter across targets 2 and 4. Save the loss
        # and gradient before changing weight.
        todo("construct the residuals, differentiate squared loss, and update weight")
    return trace


def training_report(rate: float) -> Report:
    trace = _train(rate)
    documents = [
        ("training", (1, 0), "Use the loss trace to diagnose training."),
        ("archive", (0, 1), "This is an unrelated run."),
    ]
    requested = iter([
        {"type": "call", "id": "write", "name": "change", "args": {}},
        {"type": "call", "id": "read", "name": "inspect", "args": {}},
    ])

    def model(context: Context) -> str:
        if len(context["results"]) < 2:
            return json.dumps(next(requested))
        return json.dumps({"type": "final", "text": context["results"][-1]["value"]})

    # Register both tools but allow inspect only. Bind the parser, tool dispatcher,
    # selected document text, and scripted model into one runtime call.
    todo("wire the typed runtime and return its report")
