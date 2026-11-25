# Code Koans

Predict what Python will do, explain the mechanism, then implement it yourself.
Code Koans is a CLI-only curriculum for Python internals, deep learning, and
agent engineering. The opening curriculum includes 20 modules and a cross-track
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
test_two_names_share_the_same_list (koans.python.references.AboutReferences.test_two_names_share_the_same_list) ... FAIL
...
AssertionError: __ (fill in your prediction) != (True, 2)

----------------------------------------------------------------------
Ran 1 test in ...

FAILED (failures=1)
```

Open `koans/python/references.py`. Each lesson is an `About…` class with short
`test_…` methods in reading order. Read the setup and fill the blanks directly
in the assertions. A method can have several blanks. The runner stops at the
first one that fails, including when other blanks remain in the same method.

After the inline koans, the runner starts the implementation checks. Replace
each focused `todo("...")` in the learner file with the requested code.
The fixed project checks live under `checks/`. Keep your edits in `koans/`.
Local checks and reference solutions are inspectable.

The inline lesson style is inspired by [Python Koans](https://github.com/gregmalcolm/python_koans/tree/master/koans).

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
| Python | References and aliasing, closures and decorators, descriptor lookup, lazy iteration, AsyncIO, REST service contracts | Schedule bounded jobs in input order and drain workers on error or cancellation |
| Deep Learning | Linear maps, floating point and cross-entropy, scalar autodiff, rank-two broadcasting, masked attention | Backpropagate through shared graph nodes and use gradients to fit a model |
| Agentic AI | Message schemas, tool permissions, cosine retrieval, dependency planning, bounded runtime, provider adapters, checkpointed workflows, grounded QA, webhooks | Reject ambiguous messages, deduplicate attempted actions, and report partial execution |

The cross-track challenge uses your autodiff, broadcasting, retrieval, and
agent components to diagnose a small neural training run under a read-only
policy.

The [workflow practice guide](docs/workflow-practice.md) maps the typed,
class-based koans to FastAPI, Claude, Azure OpenAI, LangChain, LangGraph, n8n,
and Langflow. The exercises run with local fixtures. See the [math notes](docs/math.md) and [curriculum roadmap](docs/roadmap.md).

## Contributing

Run `python -m maintainer.validate` on an untouched set of starters to verify
starter failures, reference passes, and plausible wrong answers. The
[contribution guide](CONTRIBUTING.md) and [authoring guide](docs/authoring.md)
describe how to propose and validate a koan.

## License

[MIT](LICENSE).
