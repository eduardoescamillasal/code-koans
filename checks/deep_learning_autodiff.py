def implement(t, s):
    x, y = s.Value(2), s.Value(3)
    z = x * y + y
    z.backward()
    t.assertEqual((z.data, z.grad, x.grad, y.grad), (9, 1, 3, 3))


def break_cases(t, s):
    x = s.Value(3)
    shared = x * x
    z = shared * shared + shared
    for seed, expected in ((1, 114), (2, 228), (-1, -114)):
        z.backward(seed)
        t.assertEqual(x.grad, expected)
        t.assertEqual(z.grad, seed)
    chain = x
    one = s.Value(1)
    for _ in range(1600):
        chain = chain + one
    chain.backward()
    t.assertEqual((x.grad, one.grad), (1, 1600))


def transfer(t, s):
    t.assertAlmostEqual(s.fit_slope([(1, 3), (2, 6)], 0.05, 80), 3)
    t.assertAlmostEqual(s.fit_slope([(1, 0), (2, 10)], 0.05, 80), 4)
    t.assertEqual(s.fit_slope([(1, 3)], 0.1, 0), 0)
