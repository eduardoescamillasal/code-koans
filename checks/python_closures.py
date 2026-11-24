def predict(t, s):
    captures = [lambda: i for i in range(3)]
    t.assertEqual(s.prediction, tuple(f() for f in captures))


def contrast(t, s):
    captures = [lambda i=i: i for i in range(3)]
    t.assertEqual(s.contrast, tuple(f() for f in captures))


def implement(t, s):
    calls = []
    def f(a, b):
        """Combine values."""
        calls.append((a, b))
        return a * b
    wrapped = s.memoize(f)
    t.assertEqual(wrapped(a=2, b=3), 6)
    t.assertEqual(wrapped(b=3, a=2), 6)
    t.assertEqual(calls, [(2, 3)])
    t.assertIs(getattr(wrapped, "__wrapped__", None), f)
    t.assertEqual(wrapped.__doc__, f.__doc__)


def break_cases(t, s):
    calls = []
    @s.memoize
    def recover(key):
        calls.append(key)
        if len(calls) == 1:
            raise ValueError("temporary")
        return None
    with t.assertRaises(ValueError):
        recover("a")
    t.assertIsNone(recover("a"))
    t.assertIsNone(recover("a"))
    t.assertEqual(calls, ["a", "a"])


def transfer(t, s):
    t.assertEqual(s.routes(20, 20, set()), 137846528820)
    t.assertEqual(s.routes(2, 2, {(1, 1)}), 2)
    t.assertEqual(s.routes(2, 2, {(0, 0)}), 0)
    t.assertEqual(s.routes(2, 2, {(2, 2)}), 0)
