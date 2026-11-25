from koans.python.named_records import Reading, Summary
from maintainer.references.python_named_records import parse_row, summarize


def missing_equals_zero(cells: list[str]) -> Reading:
    reading = parse_row(cells)
    return reading._replace(value=reading.value or None)


def permit_negative_tick(cells: list[str]) -> Reading:
    if len(cells) == 3 and cells[1] == "-1":
        return Reading(cells[0], -1, float(cells[2]))
    return parse_row(cells)


def average_all_intervals(lines) -> list[Summary]:
    return [
        row._replace(mean=row.mean * row.observed / (row.observed + row.missing))
        if row.mean is not None else row
        for row in summarize(lines)
    ]


CASES = {
    "predict": {"prediction": (2, 'north', None)},
    "contrast": {"contrast": (False, False)},
    "implement": {"parse_row": missing_equals_zero},
    "break_cases": {"parse_row": permit_negative_tick},
    "transfer": {"summarize": average_all_intervals},
}
