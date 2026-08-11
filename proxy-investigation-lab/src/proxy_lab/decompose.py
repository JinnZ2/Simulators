"""Phase 1 — decomposition of a proxy candidate."""
from dataclasses import dataclass, field

@dataclass
class Decomposition:
    target_variable: str        # the unobservable
    observable_metric: str      # the measurement
    claimed_mapping: str        # direction/form/rationale
    alternative_constructs: list[str] = field(default_factory=list)  # what else the metric might measure

    def redefinition_risk(self) -> str:
        if self.alternative_constructs:
            return ("HIGH: metric may measure " + "; ".join(self.alternative_constructs) +
                    " rather than the target (Seltzer 2021)")
        return "moderate: no alternative constructs listed — list some, absence of evidence is not evidence of absence"
