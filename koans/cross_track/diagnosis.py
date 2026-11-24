"""Investigate a neural training run with a deterministic read-only agent.

A trace contains (loss, gradient) pairs. First classify a trace with diagnose.
Then build training_report using your Value, matrix add, retrieve, parse, dispatch
and run implementations. See docs/diagnosis.md for the integration contract.
"""

from koans import __

prediction = __
contrast = __


def diagnose(trace):
    raise AssertionError("Implement diagnose")


def training_report(rate):
    raise AssertionError("Implement training_report")
