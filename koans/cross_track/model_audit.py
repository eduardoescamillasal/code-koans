"""Audit false negatives by cohort with a read-only local agent.

Use the threshold chosen upstream. Return a cohort's number of actual
positives, false negatives, and their ratio. Use None when a cohort has no
positives. Rank eligible cohorts by highest false-negative rate, using the
lexicographically smallest name for ties. Eligibility requires at least
min_positives actual positives. Review synthetic data only.
"""
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import NamedTuple

from koans import Koan, __, todo
from koans.agents.protocol import Scalar, parse
from koans.agents.runtime import Model, Report, run
from koans.deep_learning.evaluation import Counts, Scored, confusion


class Cohort(NamedTuple):
    group: str
    positives: int
    missed: int
    rate: float | None


Counter = Callable[[Iterable[Scored], float], Counts]


class AboutModelAudit(Koan):
    def test_perfect_accuracy_can_hide_an_absent_positive_class(self) -> None:
        counts = Counts(0, 0, 0, 12)
        self.assertEqual(__, (counts.tn, counts.tp + counts.fn))

    def test_one_positive_is_enough_to_change_the_miss_rate(self) -> None:
        counts = Counts(0, 0, 1, 11)
        self.assertEqual(__, (counts.tn, counts.fn / (counts.tp + counts.fn)))

    def test_evidence_support_is_not_the_size_of_the_cohort(self) -> None:
        small = Counts(0, 1, 1, 12)
        large = Counts(3, 0, 2, 1)
        self.assertEqual(__, (sum(small), sum(large)))
        self.assertEqual(__, (small.tp + small.fn, large.tp + large.fn))

    def test_an_undefined_rate_is_distinct_from_no_missed_positives(self) -> None:
        empty = Counts(0, 0, 0, 5)
        hit = Counts(4, 0, 0, 0)
        rates = [c.fn / (c.tp + c.fn) if c.tp + c.fn else None for c in (empty, hit)]
        self.assertEqual(__, rates[0])
        self.assertEqual(__, rates[1])

    def test_a_model_request_cannot_grant_itself_write_permission(self) -> None:
        requested = ["inspect", "change_threshold", "worst"]
        allowed = {"inspect", "worst"}
        self.assertEqual(__, [action for action in requested if action in allowed])
        self.assertEqual(__, len(set(requested) - allowed))


class CohortAudit:
    def __init__(
        self, groups: Mapping[str, Sequence[Scored]], threshold: float,
        *, count: Counter = confusion,
    ) -> None:
        self.groups = {name: tuple(rows) for name, rows in groups.items()}
        self.threshold = threshold
        self._count = count

    def inspect(self, group: str) -> Cohort:
        counts = self._count(self.groups[group], self.threshold)
        positives = counts.tp + counts.fn
        rate: float | None = todo("distinguish a missing denominator from a zero miss rate")
        return Cohort(group, positives, counts.fn, rate)

    def worst(self, min_positives: int) -> Cohort | None:
        if type(min_positives) is not int or min_positives < 1:
            raise ValueError("expected a positive integer support limit")
        eligible: list[tuple[float, str, Cohort]] = []
        for group in self.groups:
            row = self.inspect(group)
            if row.positives >= min_positives and row.rate is not None:
                todo("rank higher miss rates first and resolve ties by group")
        return min(eligible)[2] if eligible else None

    def execute(self, name: str, args: dict[str, Scalar]) -> dict[str, Scalar] | None:
        if name == "inspect" and args.keys() == {"group"} and isinstance(args["group"], str):
            result = self.inspect(args["group"])
        elif name == "worst" and args.keys() == {"min_positives"} and type(args["min_positives"]) is int:
            result = self.worst(args["min_positives"])
        else:
            raise ValueError("tool or arguments outside the audit contract")
        # Convert the named record to JSON-compatible data without losing field names.
        return None if result is None else result._asdict()


def run_audit(audit: CohortAudit, model: Model, notes: Iterable[str] = ()) -> Report:
    return run(model, parse, audit.execute, policy="inspect only", documents=notes)
