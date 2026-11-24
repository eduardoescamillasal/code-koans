def predict(t, s):
    weight, gradient, rate = 0.0, -6.0, 0.0
    t.assertEqual(s.prediction, weight - rate * gradient)


def contrast(t, s):
    weight, gradient, rate = 0.0, -6.0, 0.25
    t.assertEqual(s.contrast, weight - rate * gradient)


def implement(t, s):
    t.assertEqual(s.diagnose([(8, -4), (8, -4)]), "check learning rate")
    t.assertEqual(s.diagnose([(8, -4), (2, -2)]), "loss decreasing")


def break_cases(t, s):
    for trace in ([], [(8, -4)], [(8, -4), (float("inf"), 0)], [(8, float("nan")), (8, 0)]):
        with t.assertRaises(ValueError):
            s.diagnose(trace)
    t.assertEqual(s.diagnose([(8, 0), (8, 0)]), "inspect gradient")
    t.assertEqual(s.diagnose([(8, -4), (20, 8)]), "reduce learning rate")


def transfer(t, s):
    for rate, expected in ((0, "check learning rate"), (0.1, "loss decreasing"), (0.8, "reduce learning rate")):
        with t.subTest(rate=rate):
            status, advice, events = s.training_report(rate)
            t.assertEqual((status, advice), ("final", expected))
            t.assertEqual(events, [
                {"id": "write", "ok": False, "value": "tool failed"},
                {"id": "read", "ok": True, "value": expected},
            ])
