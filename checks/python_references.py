def implement(t, s):
    label = "sensor A"
    t.assertIs(s.snapshot(label), label)
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
    defaults = {"volume": 3}
    original = {"speaker": defaults, "headphones": defaults, "alarm": {"volume": 3}}
    preview = s.snapshot(original)
    preview["speaker"]["volume"] = 8

    t.assertEqual(preview["headphones"]["volume"], 8)
    t.assertEqual(preview["alarm"]["volume"], 3)
    t.assertEqual(original["speaker"]["volume"], 3)

    second_preview = s.snapshot(preview)
    second_preview["headphones"]["volume"] = 1
    t.assertEqual(second_preview["speaker"]["volume"], 1)
    t.assertEqual(preview["speaker"]["volume"], 8)
