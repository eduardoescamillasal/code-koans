from collections import defaultdict
from collections.abc import Iterable
import csv
import math

from koans.python.named_records import Reading, Summary

prediction = ('north', 2, 0.0)
contrast = (True, False)


def parse_row(cells: list[str]) -> Reading:
    if len(cells) != 3:
        raise ValueError("expected three columns")
    sensor, tick_text, value_text = (cell.strip() for cell in cells)
    tick = int(tick_text)
    value = None if not value_text else float(value_text)
    if not sensor or tick < 0 or (value is not None and not math.isfinite(value)):
        raise ValueError("invalid reading")
    return Reading(sensor, tick, value)


def summarize(lines: Iterable[str]) -> list[Summary]:
    groups: dict[str, list[Reading]] = defaultdict(list)
    seen: set[tuple[str, int]] = set()
    for cells in csv.reader(lines):
        reading = parse_row(cells)
        key = reading.sensor, reading.tick
        if key in seen:
            raise ValueError("duplicate sensor and tick")
        seen.add(key)
        groups[reading.sensor].append(reading)
    report = []
    for sensor, rows in sorted(groups.items()):
        values = [row.value for row in rows if row.value is not None]
        average = math.fsum(value / len(values) for value in values) if values else None
        report.append(Summary(sensor, len(values), len(rows) - len(values), average))
    return report
