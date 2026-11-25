"""Read a sensor CSV and produce typed summaries, preserving missing values.

Input lines have no header and contain sensor, tick, and reading. Tick is a
nonnegative integer. A blank reading means missing and zero is a valid reading.
Strip surrounding spaces and reject blank sensors, nonfinite values, wrong
column counts, and repeated (sensor, tick) keys. Summaries are sorted by sensor.
Mean excludes missing readings. An all-missing sensor has mean None.
"""
from collections import defaultdict, namedtuple
from collections.abc import Iterable
import csv
import math
from typing import NamedTuple

from koans import Koan, __, todo


class Reading(NamedTuple):
    sensor: str
    tick: int
    value: float | None = None


class Summary(NamedTuple):
    sensor: str
    observed: int
    missing: int
    mean: float | None


class AboutNamedRecords(Koan):
    def test_records_have_both_names_and_positions(self) -> None:
        reading = Reading("north", 2, 0.0)
        sensor, tick, value = reading
        self.assertEqual(__, (reading.sensor, reading[1], value))

    def test_tuple_equality_does_not_check_record_type(self) -> None:
        class OtherReading(NamedTuple):
            site: str
            clock: int
            temperature: float | None

        a = Reading("north", 2, 0.0)
        b = OtherReading("north", 2, 0.0)
        self.assertEqual(__, (a == b, type(a) is type(b)))

    def test_replace_creates_a_new_record(self) -> None:
        missing = Reading("north", 7)
        corrected = missing._replace(value=0.0)
        self.assertEqual(__, missing.value)
        self.assertEqual(__, corrected.value)
        self.assertEqual(__, missing is corrected)

    def test_value_membership_cannot_identify_a_missing_reading(self) -> None:
        rows = [Reading("a", 1, 0.0), Reading("a", 2)]
        self.assertEqual(__, sum(row.value is None for row in rows))
        self.assertEqual(__, sum(bool(row.value) for row in rows))
        self.assertEqual(__, rows[0]._asdict()["value"])

    def test_indexing_by_sensor_alone_loses_an_observation(self) -> None:
        rows = [Reading("a", 1, 2.0), Reading("a", 2, 8.0)]
        by_sensor = {row.sensor: row for row in rows}
        by_slot = {(row.sensor, row.tick): row for row in rows}
        self.assertEqual(__, by_sensor["a"].value)
        self.assertEqual(__, len(by_slot))


    def test_factory_namedtuples_use_defaults_from_the_right(self) -> None:
        Position = namedtuple("Position", "sensor tick value", defaults=(None,))
        sample = Position("west", 4)
        self.assertEqual(__, sample._fields)
        self.assertEqual(__, sample.value)
        self.assertEqual(__, sample == ("west", 4, None))


def parse_row(cells: list[str]) -> Reading:
    if len(cells) != 3:
        raise ValueError("expected three columns")
    sensor, tick_text, value_text = (cell.strip() for cell in cells)
    tick = int(tick_text)
    if not sensor or tick < 0:
        raise ValueError("invalid sensor or tick")
    value: float | None = todo("interpret a blank reading as missing, otherwise parse a float")
    if value is not None and not math.isfinite(value):
        raise ValueError("expected a finite reading")
    return Reading(sensor, tick, value)


def summarize(lines: Iterable[str]) -> list[Summary]:
    groups: dict[str, list[Reading]] = defaultdict(list)
    seen: set[tuple[str, int]] = set()
    for cells in csv.reader(lines):
        reading = parse_row(cells)
        key = (reading.sensor, reading.tick)
        if key in seen:
            raise ValueError("duplicate sensor and tick")
        seen.add(key)
        groups[reading.sensor].append(reading)

    report: list[Summary] = []
    for sensor, rows in sorted(groups.items()):
        observed = [row.value for row in rows if row.value is not None]
        mean: float | None = todo("calculate the mean only when observed readings exist")
        report.append(Summary(sensor, len(observed), len(rows) - len(observed), mean))
    return report
