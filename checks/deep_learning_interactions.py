from koans.deep_learning.interactions import Sample, Weights


def implement(t, s):
    model = s.InteractionModel(Weights(2, 1, -1, 3))
    t.assertEqual(model.predict(2, -1), -1)
    model.fit([Sample(2, -1, 1)], 0.1, 1)
    for got, expected in zip(model.weights, Weights(2.4, 1.8, -1.4, 2.2), strict=True):
        t.assertAlmostEqual(got, expected)


def break_cases(t, s):
    sample = Sample(1, 1, 1)
    one, duplicate = s.InteractionModel(), s.InteractionModel()
    one.fit([sample], 0.1, 1)
    duplicate.fit([sample, sample], 0.1, 1)
    t.assertEqual(one.weights, duplicate.weights)
    one.fit([sample], 0.1, 0)
    t.assertEqual(one.weights, duplicate.weights)
    for rows, rate, steps in (([], 0.1, 1), ([sample], float("nan"), 1), ([sample], 0.1, -1)):
        with t.assertRaises(ValueError):
            one.fit(rows, rate, steps)


def transfer(t, s):
    train = [Sample(x, y, x * y) for x in (-1, 1) for y in (-1, 1)]
    model = s.InteractionModel()
    model.fit(train, 0.15, 35)
    # Novel magnitudes test the learned interaction, beyond the training corners.
    t.assertAlmostEqual(model.predict(2, -3), -6, places=3)
    t.assertAlmostEqual(model.predict(-2, -3), 6, places=3)
    t.assertAlmostEqual(model.weights.bias, 0)
