"""Phase 2 — physical transduction chain: phenomenon -> ... -> indication."""
from dataclasses import dataclass, field

@dataclass
class TransductionLink:
    name: str
    physics: str
    fidelity: float
    grade: str                   # measured | estimated | assumed
    alias_states: list[str] = field(default_factory=list)

@dataclass
class TransductionChain:
    links: list[TransductionLink]

    def chain_fidelity(self) -> float:
        out = 1.0
        for l in self.links:
            out *= l.fidelity
        return out

    def weakest_link(self) -> TransductionLink:
        return min(self.links, key=lambda l: l.fidelity)

    def report(self) -> dict:
        wl = self.weakest_link()
        return {"chain_fidelity": round(self.chain_fidelity(), 4),
                "weakest_link": {"name": wl.name, "fidelity": wl.fidelity, "grade": wl.grade},
                "links": [{"name": l.name, "fidelity": l.fidelity, "grade": l.grade,
                           "aliases": l.alias_states} for l in self.links]}
