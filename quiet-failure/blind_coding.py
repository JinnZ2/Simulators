"""WO-2 step 2 -- the decomposition tested against a case set chosen by
someone who has not seen it. Blind coding.

Not run here, and not runnable from here: every coding in this folder
was produced by the hand that read the order, so it is REFUSED as a
blind coding by the one rule the step turns on. What ships is the
admission gate and the agreement arithmetic, so a blind run has a place
to land: each coder declares whether they saw the decomposition, and a
coding pair enters the agreement count only when neither did.

Agreement is per field and never combined into one number: the fields
are three-valued vocabularies of different kinds (a signal state, a
count, a duration) and one percentage over them would compare unlike
objects.
Library module: refuses --selftest; the suite is selftest.py.
"""
import sys

CODED_FIELDS = ("signal_present", "signal_reported", "join_assigned", "described_as")


def admit(coding):
    """A coding enters step 2 iff it declares saw_decomposition False and
    names its coder. A coding that saw it, or does not say, is refused
    with the reason; refused is not the same as absent."""
    if not isinstance(coding, dict):
        return {"state": "MALFORMED"}
    if "coder" not in coding or "case" not in coding:
        return {"state": "REFUSED", "why": "coder or case not named"}
    saw = coding.get("saw_decomposition", "UNDECLARED")
    if saw is True:
        return {"state": "REFUSED", "why": "coder saw the decomposition; not blind"}
    if saw is not False:
        return {"state": "REFUSED", "why": "saw_decomposition not declared; not admitted by default"}
    return {"state": "ADMITTED"}


def agreement(a, b):
    """Two admitted codings of one case -> per-field AGREE / DISAGREE /
    UNSEARCHED_ON_ONE_SIDE (one coder did not look; not a disagreement)."""
    if admit(a)["state"] != "ADMITTED" or admit(b)["state"] != "ADMITTED":
        return {"state": "NOT_EVALUABLE", "why": "both codings have to be admitted"}
    if a.get("case") != b.get("case"):
        return {"state": "NOT_EVALUABLE", "why": "different cases"}
    per = {}
    for f in CODED_FIELDS:
        x, y = a.get(f, "UNSEARCHED"), b.get(f, "UNSEARCHED")
        if "UNSEARCHED" in (x, y) or "UNDECLARED" in (x, y):
            per[f] = "UNSEARCHED_ON_ONE_SIDE"
        else:
            per[f] = "AGREE" if x == y else "DISAGREE"
    return {"state": "EVALUATED", "case": a["case"], "per_field": per}


def corpus_agreement(pairs):
    """Over coding pairs: per field, counts of AGREE / DISAGREE /
    UNSEARCHED_ON_ONE_SIDE, plus refused pairs listed. No composite."""
    out = {f: {"AGREE": 0, "DISAGREE": 0, "UNSEARCHED_ON_ONE_SIDE": 0} for f in CODED_FIELDS}
    refused = []
    for a, b in pairs:
        g = agreement(a, b)
        if g["state"] != "EVALUATED":
            refused.append(g["why"])
            continue
        for f, v in g["per_field"].items():
            out[f][v] += 1
    return {"per_field": out, "pairs_evaluated": len(pairs) - len(refused), "refused": refused,
            "state": "NOT_RUN" if len(pairs) == len(refused) else "EVALUATED"}


def constructed_pairs():
    """CONSTRUCTED blind pairs so both agreement values are reachable."""
    c1 = {"case": "K-1", "coder": "coder-a", "saw_decomposition": False, "signal_present": "PRESENT", "signal_reported": "PRESENT", "join_assigned": "UNASSIGNED", "described_as": "SUDDEN"}
    c2 = dict(c1, coder="coder-b", join_assigned="ASSIGNED", described_as="UNSEARCHED")
    return [(c1, c2)]


def render(session_codings):
    ad = [admit(c)["state"] for c in session_codings]
    lines = ["blind_coding -- step 2, NOT RUN: every coding in this folder saw the decomposition",
             "  this session's codings admitted as blind: %d of %d (%s)" % (ad.count("ADMITTED"), len(ad), ", ".join(sorted(set(ad)))),
             "  why: %s" % admit(session_codings[0])["why"]]
    ca = corpus_agreement(constructed_pairs())
    lines.append("  CONSTRUCTED blind pair: %s" % ", ".join("%s %s" % (f, [k for k, v in ca["per_field"][f].items() if v][0]) for f in CODED_FIELDS))
    lines.append("  real blind pairs: %s" % corpus_agreement([])["state"])
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("library module; run: python3 selftest.py")
        sys.exit(2)
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
    import decomposition
    print(render(decomposition.carried_codings()))
