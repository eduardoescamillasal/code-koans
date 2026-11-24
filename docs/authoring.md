# Authoring a koan

1. Identify the mechanism and a concrete misconception. Write down what the
   learner should be able to explain or build afterward.
2. Add `koans/<track>/<module>.py` with a short contract and type annotations.
   Put runnable examples in `predict(t: TestCase, *answers: object)` and
   `contrast(t: TestCase, *answers: object)`. Set `expected: object = __` inside
   each example. Compare `answers[0] if answers else expected` against the
   observed behavior so maintainers can inject reference and mutant values.
   Change one detail between the examples and ground the
   contrast in a decision the learner will make while implementing the koan.
3. Scaffold the implementation with small, local `todo("...")` calls. Provide
   the surrounding control flow, fixtures, and helper signatures. Include
   `practice`, `practice_break`, and `practice_transfer` in the learner file.
   These functions take a `TestCase` and the exercise candidate and show concrete
   calls, expected outputs, and edge conditions. Put independent `implement`,
   `break_cases`, and `transfer` cases with the same signature under
   `checks/<track>_<module>.py`. The runner executes visible practice first.
4. Put the solved API and the two observation answers (`prediction` and
   `contrast`) under `maintainer/references/`. Put one targeted
   replacement per stage in `maintainer/mutants/` under the same module name.
   The `CASES` mapping contains stage names and field overrides for the
   reference namespace. Use wrong results a learner might reasonably produce,
   such as silently truncating mismatched dimensions. An import error or other
   unexpected exception will not satisfy the validator.
5. Add the module to the correct position in `checks.TRACKS`. Run the selected
   module, then run `python -m maintainer.validate` and
   `python -m unittest maintainer.test_runner`. Review every failure path.

Learner-facing checks should never import reference answers or mutate learner
source. Use fixed data, in-process model fixtures, and explicit coordination
events for concurrency. Use timeouts to detect deadlocks and tolerances to
compare floating-point results. Check semantic observables, such as side
effects, gradients, and result order. Cost constraints that cannot be
reliably measured should be described in the contract and reviewed manually.
