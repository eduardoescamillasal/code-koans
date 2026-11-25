from koans.python.named_records import Reading, Summary


def implement(t, s):
    t.assertEqual(s.parse_row([" north ", " 2 ", " 0 "]), Reading("north", 2, 0.0))
    t.assertEqual(s.parse_row(["north", "3", " "]), Reading("north", 3, None))
    t.assertEqual(s.parse_row(["east", "4", "-3.5"]), Reading("east", 4, -3.5))


def break_cases(t, s):
    # A valid row must remain usable after an invalid one.
    t.assertEqual(s.parse_row(["west", "7", "0"]), Reading("west", 7, 0.0))
    for row in (["x", "-1", "9"], [" ", "1", "1"], ["x", "1", "nan"], ["x", "1"]):
        with t.assertRaises(ValueError):
            s.parse_row(row)
    with t.assertRaises(ValueError):
        s.summarize(["x,1,2", "x,1,3"])


def transfer(t, s):
    lines = iter(['z,1,', 'a,3,0.0', 'a,1,6', '"rack, west",1,4', 'a,2,'])
    t.assertEqual(s.summarize(lines), [
        Summary("a", 2, 1, 3.0), Summary("rack, west", 1, 0, 4.0), Summary("z", 0, 1, None),
    ])
