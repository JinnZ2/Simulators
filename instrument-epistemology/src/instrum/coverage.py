"""Phase 7 — epistemic coverage report."""
GRADE_WEIGHT = {"measured": 1.0, "estimated": 0.5, "assumed": 0.0}

def coverage_report(aspects: list[dict]) -> dict:
    if not aspects:
        return {"aspects": [], "grounded_fraction": 0.0, "verdict": "no aspects"}
    frac = sum(GRADE_WEIGHT[a["grade"]] for a in aspects) / len(aspects)
    weakest = sorted(aspects, key=lambda a: GRADE_WEIGHT[a["grade"]])[:3]
    return {"aspects": aspects,
            "grounded_fraction": round(frac, 3),
            "weakest_aspects": [a["aspect"] for a in weakest],
            "verdict": ("well grounded" if frac >= 0.8 else
                        "partially grounded" if frac >= 0.5 else
                        "mostly assumed — investigation incomplete")}
