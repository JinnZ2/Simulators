"""Phase 4 — traceability audit against the SI pyramid."""
from dataclasses import dataclass

@dataclass
class TraceabilityChain:
    levels: list[dict]  # [{"level": str, "status": "ok|lapsed|broken|none", "note": str}]

    def unbroken(self) -> bool:
        return all(l["status"] == "ok" for l in self.levels)

    def highest_break(self) -> str:
        for l in self.levels:
            if l["status"] != "ok":
                return f"chain broken at {l['level']} ({l['status']}): {l.get('note','')}"
        return "unbroken chain to SI"

    def grade(self) -> str:
        if self.unbroken():
            return "measured"
        if any(l["status"] == "ok" for l in self.levels[:2]):
            return "estimated"
        return "assumed"
