def implement(t, s):
    a, b = s.Vector(3, -2), s.Vector(6, 4)
    t.assertEqual(repr(a), "Vector(3, -2)")
    t.assertEqual((a + b).coordinates, (9, 2))
    t.assertEqual((2 * a).coordinates, (6, -4))
    t.assertEqual((b * 0.5).coordinates, (3, 2))
    t.assertEqual(a @ b, 10)


def break_cases(t, s):
    v = s.Vector(2, 3)
    with t.assertRaises(ValueError):
        _ = v + s.Vector(1)
    with t.assertRaises(ValueError):
        _ = v @ s.Vector(1)
    t.assertIs(v.__mul__(True), NotImplemented)

    class Reflected:
        def __radd__(self, other: object) -> str:
            return "handled"

    t.assertEqual(v + Reflected(), "handled")
    t.assertEqual(v.coordinates, (2, 3))


def transfer(t, s):
    start, step, drift = s.Vector(4, 1), s.Vector(-2, 3), s.Vector(3, -1)
    endpoint = start + 2 * step + drift * 3
    t.assertEqual(endpoint.coordinates, (9, 4))
    t.assertEqual(endpoint @ s.Vector(0, 1), 4)
    t.assertEqual(start @ s.Vector(2, -1), 7)
    t.assertEqual(start.coordinates, (4, 1))
