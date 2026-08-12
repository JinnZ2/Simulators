"""Phase 2 — causal grounding chain from observable to target variable."""
from dataclasses import dataclass, field

@dataclass
class ChainLink:
    name: str
    mechanism: str                       # why target moves observable
    fidelity: float                      # 0..1, graded separately
    grade: str                           # measured | estimated | assumed
    alternative_causes: list[str] = field(default_factory=list)
    feedback_risk: str = ""              # does using the proxy change the chain?

@dataclass
class GroundingChain:
    links: list[ChainLink]

    def chain_fidelity(self) -> float:
        out = 1.0
        for l in self.links:
            out *= l.fidelity
        return out

    def weakest_link(self) -> ChainLink:
        return min(self.links, key=lambda l: l.fidelity)

    def report(self) -> dict:
        wl = self.weakest_link()
        return {
            "chain_fidelity": round(self.chain_fidelity(), 4),
            "n_links": len(self.links),
            "weakest_link": {"name": wl.name, "fidelity": wl.fidelity, "grade": wl.grade},
            "links": [{"name": l.name, "fidelity": l.fidelity, "grade": l.grade,
                       "alternative_causes": l.alternative_causes} for l in self.links],
        }
