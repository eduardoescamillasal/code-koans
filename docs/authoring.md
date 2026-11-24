# Authoring a koan

1. Identify the mechanism and a concrete misconception. Write down what the
   learner should be able to explain or build afterward.
2. Add `koans/<track>/<module>.py` with the objective and contract in its
   docstring. Document expected types, bounds, edge cases, platform assumptions,
   and any time or space constraints. Leave `prediction` and `contrast` set to
   the shared `__` marker. Put an `AssertionError("Implement ...")` inside each
   unfinished entry point so the module imports cleanly.
3. In `checks/<track>_<module>.py`, define `predict`, `contrast`, `implement`,
   `break_cases`, and `transfer`. Each takes a `unittest.TestCase` and a module
   or namespace exposing the exercise API. Use the same checks for starter and
   reference. Make the first two stages similar enough that one local change
   exposes the mechanism. Give transfer its own problem and learner entry
   point, with independent fixtures.
4. Put the solved API under `maintainer/references/`. Put one targeted
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
