def predict(t, s):
    # Double x, then add x to y.
    x, y = 2, 3
    x = 2 * x
    t.assertEqual(s.prediction, (x, x + y))


def contrast(t, s):
    # Add x to y, then double x.
    x, y = 2, 3
    y = x + y
    t.assertEqual(s.contrast, (2 * x, y))


def implement(t, s):
    t.assertEqual(s.matmul([[1, 2, -1], [0, 3, 4]], [[2, 0], [1, 2], [0, 5]]),
                  [[4, -1], [3, 26]])


def break_cases(t, s):
    for a, b in (([[1, 2]], [[1]]), ([[1], [2, 3]], [[1]]), ([], [[1]]), ([[]], [])):
        with t.assertRaises(ValueError):
            s.matmul(a, b)


def transfer(t, s):
    points = [[2, 0, 1], [0, 2, 1]]
    rotation = [[0, -1], [1, 0]]
    calibration = [[2, 0], [0, 3], [1, 1]]
    t.assertEqual(s.transform(points, [rotation, calibration]), [[0, -4, -2], [6, 0, 3], [2, -2, 0]])
    t.assertEqual(s.transform(points, []), points)
