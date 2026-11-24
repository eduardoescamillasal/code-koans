# Contributing

Exercise proposals should identify a misconception or invariant, the learner
knowledge they build on, and an unfamiliar setting where it matters. Open a
curriculum proposal for changes that introduce a module or alter its order.
Small fixes can go directly to a pull request.

Fork the repository, clone your fork, and work on a branch. Use CPython
3.11–3.14. No dependency installation is required.

```sh
python contemplate.py
python -m maintainer.validate
python -m unittest maintainer.test_runner
```

For new modules, follow the [authoring guide](docs/authoring.md). Include
the learner file, separate checks, reference, targeted mutants, and any
derivations or external behavior assumptions. Keep starter answers blank and
implementation stubs unfinished. Avoid committing your answers from a study
session. Expect the default learner command to fail in a fresh checkout.

Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
