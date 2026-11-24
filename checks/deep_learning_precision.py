import math


def implement(t, s):
    loss, gradient = s.cross_entropy([math.log(2), 0, 0], 1)
    t.assertAlmostEqual(loss, math.log(4))
    for got, expected in zip(gradient, (0.5, -0.75, 0.25), strict=True):
        t.assertAlmostEqual(got, expected)


def break_cases(t, s):
    loss, gradient = s.cross_entropy([1000, 1000, -1000], 2)
    t.assertAlmostEqual(loss, 2000 + math.log(2))
    t.assertEqual(gradient, [0.5, 0.5, -1.0])
    for logits, index in (([], 0), ([0], -1), ([0], True), ([math.inf], 0)):
        with t.assertRaises(ValueError):
            s.cross_entropy(logits, index)


def transfer(t, s):
    logits = [0.0, 2.0, -1.0]
    bias, step = 0.7, 1e-5
    loss, slope = s.calibrate(logits, 1, bias, (0, 2))
    upper = s.calibrate(logits, 1, bias + step, (0, 2))[0]
    lower = s.calibrate(logits, 1, bias - step, (0, 2))[0]
    t.assertAlmostEqual(slope, (upper - lower) / (2 * step), places=7)
    t.assertGreater(loss, 0.0)
    t.assertGreater(slope, 0.0)
    t.assertLess(s.calibrate(logits, 1, bias, (0, 1))[1], 0)
    t.assertEqual(logits, [0.0, 2.0, -1.0])
