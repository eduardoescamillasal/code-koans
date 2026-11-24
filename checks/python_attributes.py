def predict(t, s):
    class NonData:
        def __get__(self, instance, owner):
            return "computed"

    class Record:
        value = NonData()

    record = Record()
    record.__dict__["value"] = "local"
    t.assertEqual(s.prediction, record.value)


def contrast(t, s):
    class Record:
        @property
        def value(self):
            return "computed"

    record = Record()
    record.__dict__["value"] = "local"
    t.assertEqual(s.contrast, record.value)


def implement(t, s):
    field = s.bounded_int(0, 10)
    class Record:
        count = field
    a, b = Record(), Record()
    a.count, b.count = 3, 7
    t.assertIs(Record.count, field)
    t.assertEqual((a.count, b.count), (3, 7))


def break_cases(t, s):
    class Record:
        count = s.bounded_int(0, 1)
    record = Record()
    with t.assertRaises(AttributeError):
        _ = record.count
    record.count = 1
    for bad in (True, -1, 2):
        with t.assertRaises(ValueError):
            record.count = bad
        t.assertEqual(record.count, 1)


def transfer(t, s):
    Reading = s.reading_type({"low": (0, 5), "high": (10, 20)})
    Other = s.reading_type({"low": (-20, -10)})

    class Calibrated(Reading):
        pass

    reading = Calibrated()
    reading.low, reading.high = 4, 12
    reading.__dict__["high"] = -10
    other = Other()
    other.low = -11
    t.assertEqual((reading.low, reading.high, other.low), (4, 12, -11))
    with t.assertRaises(ValueError):
        reading.high = 4
