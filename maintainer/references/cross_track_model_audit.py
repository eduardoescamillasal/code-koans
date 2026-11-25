from collections.abc import Iterable, Mapping, Sequence

from koans.agents.protocol import Scalar
from koans.agents.runtime import Model, Report
from koans.cross_track.model_audit import Cohort, Counter
from koans.deep_learning.evaluation import Scored
from maintainer.references.agents_protocol import parse
from maintainer.references.agents_runtime import run
from maintainer.references.deep_learning_evaluation import confusion

prediction = (12, 0)
contrast = (11, 1.0)


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
        rate = counts.fn / positives if positives else None
        return Cohort(group, positives, counts.fn, rate)

    def worst(self, min_positives: int) -> Cohort | None:
        if type(min_positives) is not int or min_positives < 1:
            raise ValueError("expected a positive integer support limit")
        eligible = []
        for group in self.groups:
            row = self.inspect(group)
            if row.positives >= min_positives and row.rate is not None:
                eligible.append((-row.rate, row.group, row))
        return min(eligible)[2] if eligible else None

    def execute(self, name: str, args: dict[str, Scalar]) -> dict[str, Scalar] | None:
        if name == "inspect" and args.keys() == {"group"} and isinstance(args["group"], str):
            result = self.inspect(args["group"])
        elif name == "worst" and args.keys() == {"min_positives"} and type(args["min_positives"]) is int:
            result = self.worst(args["min_positives"])
        else:
            raise ValueError("tool or arguments outside the audit contract")
        return None if result is None else result._asdict()


def run_audit(audit: CohortAudit, model: Model, notes: Iterable[str] = ()) -> Report:
    return run(model, parse, audit.execute, policy="inspect only", documents=notes)
