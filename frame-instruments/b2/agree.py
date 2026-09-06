"""B2.4 agree.py -- agreement across independent auditors. No correctness.

responses.jsonl: reader_id, case_id, condition (A|B|C|D1|D2), posed, target
  D1 = the A-stage response under D; each D1 row must hash to a commit in
  commits.jsonl (the lock enforced again at scoring time).
cases.jsonl supplies the key (for anchoring) and the optional arm.

Two readers agree on a field when the normalised strings are equal
(casefold, whitespace collapsed, trailing punctuation stripped). The rule
is written into every row as match_source. [CHOICE]

Output rows, in order:
  1. the A vs D1 check (FIRST): per case, within-A, within-D1 and cross
     A x D1 pairwise agreement; failed when the within values differ by
     more than --divergence-threshold or the cross falls below both
     withins by more than it. [CHOICE] default 0.2, printed.
  2. per (case, condition): n_auditors, agree_posed, agree_target,
     full_disagreement_pairs (pairs matching on neither field).
  3. per case, C vs D: key_match_rate under C and under D2, and the
     ratify rate among D readers whose D1 differed from the key.

Command: python3 agree.py RESPONSES.jsonl --cases CASES.jsonl --commits COMMITS.jsonl --out AGREE.jsonl [--divergence-threshold 0.2]
"""
import itertools
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, check_fields, finish, mean, parse_argv, raise_if, read_jsonl, usage_exit, write_jsonl  # noqa: E402
from conditions import validate_cases  # noqa: E402
from lock import response_hash  # noqa: E402

RESP_FIELDS = ("reader_id", "case_id", "condition", "posed", "target")
CONDS = ("A", "B", "C", "D1", "D2")
MATCH_SOURCE = "normalized_exact_match: casefold, whitespace collapsed, trailing punctuation stripped"


def norm(s):
    return " ".join(str(s).casefold().split()).strip(" .;:,!?\"'")


def same(a, b, k):
    return norm(a[k]) == norm(b[k])


def validate(responses, commits):
    probs = []
    hashes = set(c.get("sha256") for c in commits)
    for n, r in enumerate(responses, 1):
        w = "row %d" % n
        p = check_fields(r, RESP_FIELDS, w)
        if p:
            probs += p
            continue
        if r["condition"] not in CONDS:
            probs.append("%s: condition must be one of %s" % (w, CONDS))
        elif r["condition"] == "D1" and response_hash({"posed": r["posed"], "target": r["target"]}) not in hashes:
            probs.append("%s: D1 response for %s/%s has no matching commit" % (w, r["reader_id"], r["case_id"]))
    raise_if(probs)


def pair_stats(rows):
    pairs = list(itertools.combinations(rows, 2))
    if not pairs:
        return {"n_auditors": len(rows), "agree_posed": None, "agree_target": None, "full_disagreement_pairs": 0}
    return {"n_auditors": len(rows),
            "agree_posed": round(mean(same(a, b, "posed") for a, b in pairs), 4),
            "agree_target": round(mean(same(a, b, "target") for a, b in pairs), 4),
            "full_disagreement_pairs": sum(1 for a, b in pairs if not same(a, b, "posed") and not same(a, b, "target"))}


def cross(xs, ys, k):
    pairs = [(x, y) for x in xs for y in ys]
    return round(mean(same(x, y, k) for x, y in pairs), 4) if pairs else None


def ad_check(by, case, thr):
    A, D1 = by.get((case, "A"), []), by.get((case, "D1"), [])
    out = {"case_id": case, "n_A": len(A), "n_D1": len(D1)}
    for k in ("posed", "target"):
        wa, wd, cr = pair_stats(A)["agree_" + k], pair_stats(D1)["agree_" + k], cross(A, D1, k)
        out.update({"within_A_" + k: wa, "within_D1_" + k: wd, "cross_A_D1_" + k: cr})
        fails = []
        if wa is not None and wd is not None and abs(wa - wd) > thr:
            fails.append("within differ")
        if cr is not None and wa is not None and wd is not None and min(wa, wd) - cr > thr:
            fails.append("cross below withins")
        out["diverged_" + k] = fails
    out["diverged"] = bool(out["diverged_posed"] or out["diverged_target"])
    return out


def key_match(r, key):
    return same(r, {"posed": key["key_posed"]}, "posed") and same(r, {"target": key["key_target"]}, "target")


def anchoring(by, case, key):
    C, D1, D2 = by.get((case, "C"), []), by.get((case, "D1"), []), by.get((case, "D2"), [])
    d1 = {r["reader_id"]: r for r in D1}
    independent = [r for r in D2 if r["reader_id"] in d1 and not key_match(d1[r["reader_id"]], key)]
    return {"case_id": case, "n_C": len(C), "n_D2": len(D2),
            "key_match_rate_C": round(mean(key_match(r, key) for r in C), 4) if C else None,
            "key_match_rate_D2": round(mean(key_match(r, key) for r in D2), 4) if D2 else None,
            "n_D_independent_at_D1": len(independent),
            "ratify_rate_D": round(mean(key_match(r, key) for r in independent), 4) if independent else None}


def score(responses, cases, commits, thr):
    validate(responses, commits)
    keys = {c["case_id"]: c for c in cases}
    by = {}
    for r in responses:
        if r["case_id"] not in keys:
            raise Invalid("response case_id %r not in cases" % r["case_id"])
        by.setdefault((r["case_id"], r["condition"]), []).append(r)
    ids = sorted(keys)
    checks = [ad_check(by, c, thr) for c in ids if (c, "A") in by or (c, "D1") in by]
    head = {"a_vs_d1_check": checks, "failed": any(c["diverged"] for c in checks),
            "divergence_threshold": thr, "match_source": MATCH_SOURCE}
    cells = [dict({"case_id": c, "condition": cond, "arm": keys[c].get("arm")}, **pair_stats(by[(c, cond)]),
                  match_source=MATCH_SOURCE)
             for c in ids for cond in CONDS if (c, cond) in by]
    anchor = [dict(anchoring(by, c, keys[c]), arm=keys[c].get("arm"), match_source=MATCH_SOURCE) for c in ids]
    return [head] + cells + anchor


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=("responses",), options=("cases", "commits", "out", "divergence_threshold", "runs"),
                       required=("cases", "out"), defaults={"divergence_threshold": "0.2"})
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b2/agree.py", vars(a), None, [a.responses, a.cases, a.commits], a.out, a.runs) as run:
        try:
            thr = float(a.divergence_threshold)
            responses = read_jsonl(a.responses)
            if not responses:
                return finish(run, "empty", {"responses": 0})
            cases, _ = validate_cases(read_jsonl(a.cases))
            commits = read_jsonl(a.commits) if a.commits and os.path.exists(a.commits) else []
            out = score(responses, cases, commits, thr)
        except (Invalid, ValueError) as e:
            return finish(run, "error", notes=str(e))
        write_jsonl(a.out, out)
        return finish(run, "ok", {"a_vs_d1_failed": out[0]["failed"], "cells": len(out) - 1 - len(cases),
                                  "cases": len(cases)})


if __name__ == "__main__":
    sys.exit(main())
