import math


def predict(t, s):
    # Replacing a masked score with zero still gives it positive mass.
    t.assertEqual(s.prediction, tuple(math.exp(x) / 2 for x in (0, 0)))


def contrast(t, s):
    weights = [math.exp(x) for x in (0, -math.inf)]
    t.assertEqual(s.contrast, tuple(x / sum(weights) for x in weights))


def implement(t, s):
    output, weights = s.attend([1, 1, 1, 1], [[2, 0, 0, 0], [0, 0, 0, 0]], [[4, 2], [1, -1]], [True, True])
    p = math.e / (math.e + 1)
    t.assertAlmostEqual(weights[0], p)
    t.assertAlmostEqual(weights[1], 1 - p)
    for got, expected in zip(output, (1 + 3*p, -1 + 3*p), strict=True):
        t.assertAlmostEqual(got, expected)


def break_cases(t, s):
    t.assertEqual(s.attend([1000], [[-1], [1]], [[4], [99]], [True, False]), ([4], [1, 0]))
    for keys, values, keep in (([[1]], [[1]], [False]), ([[1, 2]], [[1]], [True]),
                              ([[1], [2]], [[1], [2, 3]], [True, True]), ([[1]], [[1]], [])):
        with t.assertRaises(ValueError):
            s.attend([1], keys, values, keep)


def transfer(t, s):
    keys = [[0], [0], [0]]
    before = s.causal_smooth(keys, [[3], [5], [10]])
    after = s.causal_smooth(keys, [[3], [5], [-8]])
    t.assertEqual(before, [[3], [4], [6]])
    t.assertEqual(after, [[3], [4], [0]])
    t.assertAlmostEqual(s.causal_smooth([[1], [2]], [[0], [1]])[1][0], 1 / (1 + math.exp(-2)))
