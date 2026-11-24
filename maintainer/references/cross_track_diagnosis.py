import json
import math

from maintainer.references.agents_protocol import parse
from maintainer.references.agents_retrieval import retrieve
from maintainer.references.agents_runtime import run
from maintainer.references.agents_tools import dispatch
from maintainer.references.deep_learning_autodiff import Value
from maintainer.references.deep_learning_tensor import add

prediction = 0.0
contrast = 1.5


def diagnose(trace):
    if len(trace) < 2 or not all(math.isfinite(value) for row in trace for value in row):
        raise ValueError("expected at least two finite samples")
    first, last = trace[0][0], trace[-1][0]
    if last > first:
        return "reduce learning rate"
    if last < first:
        return "loss decreasing"
    if trace[-1][1] == 0:
        return "inspect gradient"
    return "check learning rate"


def training_report(rate):
    weight = 0.0
    trace = []
    for _ in range(3):
        parameter = Value(weight)
        residuals = add([[parameter]], [[Value(-2)], [Value(-4)]])
        left, right = (row[0] for row in residuals)
        loss = left * left + right * right
        loss.backward()
        trace.append((loss.data, parameter.grad))
        weight -= rate * parameter.grad

    documents = [
        ("training", (1, 0), "Use the loss trace to diagnose training."),
        ("archive", (0, 1), "This is an unrelated run."),
    ]
    selected = retrieve((1, 0), documents, 1)
    model_calls = iter([
        {"type": "call", "id": "write", "name": "change", "args": {}},
        {"type": "call", "id": "read", "name": "inspect", "args": {}},
    ])

    def forbidden():
        return "unauthorized write ran"

    registry = {"change": ({}, forbidden), "inspect": ({}, lambda: diagnose(trace))}

    def execute(name, args):
        return dispatch(registry, {"inspect"}, name, args)

    def model(context):
        if len(context["results"]) < 2:
            return json.dumps(next(model_calls))
        result = context["results"][-1]
        return json.dumps({"type": "final", "text": result["value"]})

    return run(model, parse, execute, policy="inspect only",
               documents=[record[2] for record in selected])
