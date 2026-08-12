"""Phase 7 — grounding coverage report: how much ground is grounded."""
from .instruments import GRADE_WEIGHT

def coverage_report(aspects: list[dict]) -> dict:
    """aspects: [{'aspect': str, 'grade': measured|estimated|assumed,
                  'grounding_level': G1..G5, 'upgrade_path': str}]"""
    if not aspects:
        return {"aspects": [], "grounded_fraction": 0.0, "weakest_aspects": []}
    frac = sum(GRADE_WEIGHT[a["grade"]] for a in aspects) / len(aspects)
    weakest = sorted(aspects, key=lambda a: GRADE_WEIGHT[a["grade"]])[:3]
    return {
        "aspects": aspects,
        "grounded_fraction": round(frac, 3),
        "weakest_aspects": [a["aspect"] for a in weakest],
        "verdict": ("well grounded" if frac >= 0.8 else
                    "partially grounded" if frac >= 0.5 else
                    "mostly assumed — investigation incomplete"),
    }
