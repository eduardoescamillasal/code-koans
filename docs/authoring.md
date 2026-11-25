# Authoring a koan

1. Identify the mechanism and a concrete misconception. Write down what the
   learner should be able to explain or build afterward.
2. Add one `About…(Koan)` class in `koans/<track>/<module>.py`. Each
   `test_…` method should run against a short, already working example and
   contain one or more inline `self.assertEqual(__, expression)` blanks.
   Keep related assertions together. The first two methods make a contrast
   that exposes a decision the learner will face in the implementation.
3. Put the typed implementation scaffold below the examples, with local
   `todo("...")` calls and enough surrounding code to make the next edit
   concrete. Put fixed `implement`, `break_cases`, and `transfer` checks under
   `checks/<track>_<module>.py`. Each takes a `TestCase` and a candidate
   namespace. The runner finishes the inline exercises before these checks.
4. Put the project solution and first two answers (`prediction` and
   `contrast`) under `maintainer/references/`. Put plausible wrong answers and
   project substitutions under `maintainer/mutants/`. For remaining inline
   methods, add the correct and mistaken guess tuples to
   `maintainer/lesson_answers.py`, in assertion order. The validator runs
   against untouched starters.
5. Add the module to the correct position in `checks.TRACKS`. Run the selected
   module, then run `python -m maintainer.validate` and
   `python -m unittest maintainer.test_runner`. Review every failure path.

Learner-facing checks should never import reference answers or mutate learner
source. Use fixed data, in-process model fixtures, and explicit coordination
events for concurrency. Use timeouts to detect deadlocks and tolerances to
compare floating-point results. Check semantic observables, such as side
effects, gradients, and result order. Cost constraints that cannot be
reliably measured should be described in the contract and reviewed manually.
