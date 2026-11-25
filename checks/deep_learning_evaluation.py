from koans.deep_learning.evaluation import Counts, Evaluation, Scored


def implement(t, s):
    rows = [Scored(True, 0.5), Scored(False, 0.9), Scored(True, 0.1), Scored(False, 0.1)]
    t.assertEqual(s.confusion(iter(rows), 0.5), Counts(1, 1, 1, 1))
    t.assertEqual(s.confusion(rows[:1], 0.5), Counts(1, 0, 0, 0))


def break_cases(t, s):
    t.assertEqual(s.select_threshold([Scored(False, 0.2)], [0.4, 0.8]), 0.8)
    with t.assertRaises(ValueError):
        s.select_threshold([], [])
    with t.assertRaises(ValueError):
        s.confusion([Scored(True, float("nan"))], 0.2)
    with t.assertRaises(ValueError):
        s.confusion([], -0.1)
    with t.assertRaises(ValueError):
        s.confusion([Scored(1, 0.8)], 0.8)


def transfer(t, s):
    # Holdout would favor 0.2; tuning on it would make evaluation optimistic.
    validation = [Scored(True, 0.9), Scored(False, 0.3)]
    holdout = [Scored(True, 0.4), Scored(False, 0.1)]
    expected = Evaluation(0.8, Counts(1, 0, 0, 1), Counts(0, 0, 1, 1))
    t.assertEqual(s.evaluate(validation, holdout, [0.2, 0.8]), expected)
