# Code Koans

Predict what Python will do, explain the mechanism, then implement it yourself.
Code Koans is a CLI-only curriculum for Python internals, deep learning, and
agent engineering. The opening curriculum includes 15 modules and a cross-track
diagnosis challenge, all driven by ordinary Python files and `unittest`.

## Quick start

You need Git and CPython 3.11–3.14. The current curriculum uses the standard
library and deterministic, local model mocks. Familiarity with Python
functions, classes, and tests is helpful. The math track uses algebra and
introduces the differentiation needed in the exercises.

```sh
git clone https://github.com/eduardoescamillasal/code-koans.git
cd code-koans
python contemplate.py
```

On systems where the command is named `python3`, use it in place of `python`.
The first run stops here (traceback shortened).

```text
test_predict (checks.python_references.test_predict)
koans/python/references.py · predict ... FAIL
...
AssertionError: __ (fill in your prediction) != (True, 2)

----------------------------------------------------------------------
Ran 1 test in ...

FAILED (failures=1)
```

Open `koans/python/references.py` and read the matching case in
`checks/python_references.py`. Before running a new case, commit to a prediction
and write down why. Fill the blank or implement the requested behavior, then
rerun. When a contrast changes the result, identify exactly which rule changed.
Keep edits in `koans/`. The checks live separately so you can read them while
preserving the exercise contract. Local tests and reference implementations
are inspectable. Use them to evaluate your reasoning.

```sh
python contemplate.py python
python contemplate.py deep_learning autodiff
python contemplate.py agents runtime
python contemplate.py cross_track diagnosis
```

Each module follows the same progression.

| Level | Stage | Work |
| --- | --- | --- |
| 1 | Predict | Work out the result before executing the example |
| 2 | Explain through contrasts | Identify the mechanism behind a nearby result |
| 3 | Implement | Build the underlying behavior |
| 4 | Break | Account for failure cases and invariants |
| 5 | Transfer | Write code for a new application |

## Curriculum

| Track | Opening modules | Advanced implementation |
| --- | --- | --- |
| Python | References and aliasing, closures and decorators, descriptor lookup, lazy iteration, AsyncIO | Schedule bounded jobs in input order and drain workers on error or cancellation |
| Deep Learning | Linear maps, floating point and cross-entropy, scalar autodiff, rank-two broadcasting, masked attention | Backpropagate through shared graph nodes and use gradients to fit a model |
| Agentic AI | Message schemas, tool permissions, cosine retrieval, dependency planning, bounded runtime | Reject ambiguous messages, deduplicate attempted actions, and report partial execution |

The cross-track challenge uses your autodiff, broadcasting, retrieval, and
agent components to diagnose a small neural training run under a read-only
policy. See the [math notes](docs/math.md) and [curriculum roadmap](docs/roadmap.md).

## Contributing

Run `python -m maintainer.validate` on an untouched set of starters to verify
starter failures, reference passes, and plausible wrong answers. The
[contribution guide](CONTRIBUTING.md) and [authoring guide](docs/authoring.md)
describe how to propose and validate a koan.

## License

[MIT](LICENSE).
