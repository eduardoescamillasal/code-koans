import math


def implement(t, s):
    docs = [("off", (7, 7), "off-topic"), ("on", (1, 0), "evidence")]
    t.assertEqual(s.retrieve((1, 0), docs, 1), [docs[1]])


def break_cases(t, s):
    for query, vector in (((0, 0), (1, 0)), ((1, 0), (0, 0)), ((1, 0), (1,)),
                          ((1, 0), (math.nan, 1))):
        with t.assertRaises(ValueError):
            s.retrieve(query, [("a", vector, "")], 1)
    with t.assertRaises(ValueError):
        s.retrieve((1, 0), [], -1)
    t.assertEqual(s.retrieve((1, 0), [], 3), [])


def transfer(t, s):
    docs = [("b", (2, 0), "two"), ("a", (1, 0), "oversized"), ("c", (-1, 0), "X")]
    t.assertEqual(s.evidence((4, 0), docs, 3, 5), (["b", "c"], "two\nX"))
    t.assertEqual(s.evidence((4, 0), docs, 2, 5), (["b"], "two"))
    t.assertEqual(s.evidence((4, 0), docs, 3, 2), (["c"], "X"))
