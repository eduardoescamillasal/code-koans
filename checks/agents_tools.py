def implement(t, s):
    registry = {"scale": ({"n": int}, lambda n: n * 2)}
    t.assertEqual(s.dispatch(registry, {"scale"}, "scale", {"n": 3}), 6)


def break_cases(t, s):
    calls = []
    registry = {"scale": ({"n": int}, lambda n: calls.append(n))}
    for name, allowed, args, error in (
        ("scale", set(), {"n": 3}, PermissionError),
        ("missing", {"missing"}, {}, PermissionError),
        ("scale", {"scale"}, {"n": True}, ValueError),
        ("scale", {"scale"}, {"n": "3"}, ValueError),
        ("scale", {"scale"}, {"n": 3, "extra": 9}, ValueError),
        ("scale", {"scale"}, {}, ValueError),
    ):
        with t.assertRaises(error):
            s.dispatch(registry, allowed, name, args)
    t.assertEqual(calls, [])


def transfer(t, s):
    events = []
    registry = {
        "preview": ({"qty": int}, lambda qty: qty * 3),
        "reserve": ({"qty": int}, lambda qty: events.append(qty)),
    }
    requests = [("reserve", {"qty": 4}), ("preview", {"qty": True}),
                ("preview", {"qty": 3}), ("preview", {"qty": 4})]
    t.assertEqual(s.preview_batch(registry, requests),
                  [("rejected", None), ("rejected", None), ("ok", 9), ("ok", 12)])
    t.assertEqual(events, [])
