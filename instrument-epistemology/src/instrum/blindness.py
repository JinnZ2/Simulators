"""Phase 5 — observational blindness mapping."""
from dataclasses import dataclass, field

@dataclass
class BlindSpot:
    kind: str            # null_state | alias_state | saturation | gate | frame
    description: str
    consequence: str

@dataclass
class BlindnessMap:
    spots: list[BlindSpot] = field(default_factory=list)

    def by_kind(self, kind: str) -> list[BlindSpot]:
        return [s for s in self.spots if s.kind == kind]

    def absence_interpretable(self) -> bool:
        return not (self.by_kind("null_state") or self.by_kind("gate"))

    def summary(self) -> dict:
        return {"n_spots": len(self.spots),
                "kinds": sorted({s.kind for s in self.spots}),
                "absence_interpretable_as_absence": self.absence_interpretable(),
                "spots": [{"kind": s.kind, "description": s.description,
                           "consequence": s.consequence} for s in self.spots]}
