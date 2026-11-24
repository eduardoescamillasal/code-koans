# Authoring a koan

1. Identify the mechanism and a concrete misconception. Write down what the
   learner should be able to explain or build afterward.
2. Add one `About…(Koan)` class to `koans/<track>/<module>.py`. Name methods
   after the behavior they demonstrate. The first two methods each use one
   inline `self.assertEqual(__, ...)` and change a detail that matters for the
   implementation. The runner follows declaration order.
3. Follow with one or more small construction methods, then one boundary
   method and one transfer method. Call the typed functions or classes
   directly from those tests. Scaffold each exercise with local
   `todo("...")` calls and enough surrounding code to make the next edit clear.
   Put independent `implement`, `break_cases`, and `transfer` cases under
   `checks/<track>_<module>.py`. Each takes a `TestCase` and a candidate
   namespace. The runner executes the visible lesson methods first.
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
