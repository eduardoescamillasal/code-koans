from koans.cross_track.model_audit import Cohort
from maintainer.references.cross_track_model_audit import CohortAudit, run_audit


class TreatsMissingAsZero(CohortAudit):
    def inspect(self, group: str) -> Cohort:
        row = super().inspect(group)
        return row._replace(rate=row.rate or 0.0)


class IgnoresSupport(CohortAudit):
    def worst(self, min_positives: int) -> Cohort | None:
        return super().worst(1)


def omits_documents(audit, model, notes=()):
    return run_audit(audit, model)


CASES = {
    "predict": {"prediction": (12, 12)},
    "contrast": {"contrast": (11, 0.08333333333333333)},
    "implement": {"CohortAudit": TreatsMissingAsZero},
    "break_cases": {"CohortAudit": IgnoresSupport},
    "transfer": {"run_audit": omits_documents},
}
