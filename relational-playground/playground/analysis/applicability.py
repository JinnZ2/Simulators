"""Applicability record: ten questions per equation per context. No score, no order."""
CRITERIA = ("applicability", "predictive_adequacy", "stability", "sensitivity", "boundary_dependence",
            "energy_consistency", "observability", "identifiability", "computational_cost", "failure_region")
NOT_ASSESSED = "NOT ASSESSED"


def record(model, context, **answers):
    unknown = [k for k in answers if k not in CRITERIA]
    if unknown:
        raise ValueError("not criteria: %s" % unknown)
    rec = dict(model=model, context=context)
    for c in CRITERIA:
        a = answers.get(c, NOT_ASSESSED)
        if a != NOT_ASSESSED and not (isinstance(a, dict) and "finding" in a and "basis" in a):
            raise ValueError("%s: give dict(finding=..., basis=...) or leave it %s" % (c, NOT_ASSESSED))
        rec[c] = a
    rec["not_assessed"] = [c for c in CRITERIA if rec[c] == NOT_ASSESSED]
    return rec


def score(*_a, **_k):
    raise RuntimeError("an applicability record has no score and no rank")
