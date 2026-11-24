from itertools import islice


def predict(t, s):
    source = iter([10, 20, 30])
    t.assertEqual(s.prediction, (tuple(islice(source, 2)), tuple(source)))


def contrast(t, s):
    source = [10, 20, 30]
    t.assertEqual(s.contrast, (tuple(islice(source, 2)), tuple(source)))


def implement(t, s):
    seen = []
    def input_stream():
        for value in (1, 2, 3):
            seen.append(value)
            yield value
    windows = s.windows(input_stream(), 2)
    t.assertEqual(seen, [])
    t.assertEqual(next(windows), (1, 2))
    t.assertEqual(seen, [1, 2])
    t.assertEqual(list(windows), [(2, 3)])


def break_cases(t, s):
    t.assertEqual(list(s.windows([1], 2)), [])
    t.assertEqual(list(s.windows([1], 1)), [(1,)])
    with t.assertRaises(ValueError):
        list(s.windows([], 0))


def transfer(t, s):
    from itertools import count
    seen = []
    def sensor():
        for value in (3, 1, 4, 2, 5):
            seen.append(value)
            yield value
    t.assertEqual(s.first_rises(sensor(), 1), [1])
    t.assertEqual(seen, [3, 1, 4])
    t.assertEqual(s.first_rises(count(1), 3), [0, 1, 2])
    t.assertEqual(s.first_rises([], 1), [])
    t.assertEqual(s.first_rises(sensor(), 0), [])
    t.assertEqual(seen, [3, 1, 4])
