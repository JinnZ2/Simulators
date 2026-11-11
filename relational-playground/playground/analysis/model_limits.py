"""Failure region: where a model's prediction leaves the stated uncertainty. Kept, not dropped."""


def failure_region(points):
    """points: list of dict(point=..., predicted=..., observed=..., uncertainty=...).
    A point with no observation or no stated uncertainty reads NOT EVALUABLE."""
    rows = []
    for p in points:
        if p.get("status") == "MODEL FAILED":
            rows.append(dict(point=p["point"], reading="MODEL FAILED", detail=p.get("error")))
        elif p.get("observed") is None or p.get("uncertainty") is None:
            rows.append(dict(point=p["point"], reading="NOT EVALUABLE", detail="no observation or no stated uncertainty"))
        else:
            miss = abs(p["predicted"] - p["observed"])
            rows.append(dict(point=p["point"], reading="OUTSIDE" if miss > p["uncertainty"] else "WITHIN", miss=miss))
    return dict(rows=rows, counts={r: sum(1 for x in rows if x["reading"] == r) for r in ("WITHIN", "OUTSIDE", "NOT EVALUABLE", "MODEL FAILED")})
