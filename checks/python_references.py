def predict(t, s):
    row = {"count": 1}
    original = [row]
    alias = original
    alias[0]["count"] += 1
    t.assertEqual(s.prediction, (original is alias, original[0]["count"]))


def contrast(t, s):
    original = [{"count": 1}]
    shallow = original[:]
    shallow[0]["count"] = 8
    shallow.append({})
    t.assertEqual(s.contrast, (shallow is original, len(original), original[0]["count"]))


def implement(t, s):
    source = [{"count": 2}]
    copy = s.snapshot(source)
    t.assertEqual(copy, source)
    t.assertIsNot(copy[0], source[0])


def break_cases(t, s):
    source = []
    source.append(source)
    copy = s.snapshot(source)
    t.assertIsNot(copy, source)
    t.assertIs(copy[0], copy)


def transfer(t, s):
    shared = {"points": [1]}
    original = {"left": shared, "right": shared, "independent": {"points": [1]}}
    updated = s.record(original, "left", 2)
    t.assertEqual(updated["right"]["points"], [1, 2])
    t.assertEqual(updated["independent"]["points"], [1])
    t.assertEqual(original["left"]["points"], [1])
    t.assertEqual(s.record(updated, "right", 3)["left"]["points"], [1, 2, 3])
