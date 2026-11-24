def implement(t, s):
    t.assertEqual(s.add([[1], [2]], [[10, 20, 30]]), [[11, 21, 31], [12, 22, 32]])
    t.assertEqual(s.add([[10, 20]], [[1, 2]]), [[11, 22]])


def break_cases(t, s):
    for a, b in (([[1, 2]], [[1, 2, 3]]), ([[1], []], [[1]]), ([[]], [[1]])):
        with t.assertRaises(ValueError):
            s.add(a, b)


def transfer(t, s):
    t.assertEqual(s.totals([3, -3, 0], [-1, 1]), ([6, -6, 0], [-3, 3]))
    t.assertEqual(s.totals([2, 5], [3, -1, 9]), ([17, 26], [13, 5, 25]))
