"""B4.4 grade.py -- per item: requirement count, status and layer
distributions, policy-to-physical ratio, unresolved printed beside it.

The physical/policy split is computed FROM settling_test, never asked
for. What settles a requirement is read against two cue lists:

  physical : the test is a measurement or a physical derivation
  policy   : the test names a decision, statute, funding rule, procedure

Both lists are ARGUMENTS with defaults (--physical-cues, --policy-cues)
and are written into every output row, so the joint reports itself. A
cue is matched as a left-word-boundary prefix, case-insensitive. A test
hitting both lists, or neither, is `unresolved` with the sub-reason kept.

Command: python3 grade.py REQS.jsonl --out GRADE.jsonl [--physical-cues ...] [--policy-cues ...]
"""
import argparse
import re
import sys

from common import (REQ_FIELDS, Invalid, Run, check_fields, count_by,
                    finish, raise_if, read_jsonl, ref, write_jsonl)

PHYSICAL_CUES = ("measur", "deriv", "comput", "calculat", "instrument", "sensor",
                 "gauge", "physical law", "conservation", "thermodynamic", "assay",
                 "weigh", "load test", "pressure test", "flow rate", "timing")
POLICY_CUES = ("statute", "legislat", "regulat", "ordinance", "decision", "decid",
               "vote", "budget", "fund", "appropriat", "procedure", "policy",
               "mandate", "contract", "procurement", "tender", "staffing", "roster",
               "authoriz", "approv", "permit", "licens")


def compile_cues(cues):
    return [re.compile(r"\b" + re.escape(c.strip()), re.IGNORECASE) for c in cues if c.strip()]


def settles_by(test, phys_re, pol_re):
    p = any(r.search(test) for r in phys_re)
    q = any(r.search(test) for r in pol_re)
    if p and not q:
        return "measurement"
    if q and not p:
        return "decision"
    return "unresolved_both" if (p and q) else "unresolved_neither"


def grade(rows, physical_cues, policy_cues):
    probs = []
    for n, r in enumerate(rows, 1):
        probs += check_fields(r, REQ_FIELDS, "row %d" % n, exact=False)
    raise_if(probs)
    phys_re, pol_re = compile_cues(physical_cues), compile_cues(policy_cues)
    out = []
    for item in sorted(set(r["item_id"] for r in rows)):
        sub = [r for r in rows if r["item_id"] == item]
        reads = [{"ref": ref(r["reconstructor_id"], r["req_id"]),
                  "settles_by": settles_by(r["settling_test"], phys_re, pol_re)} for r in sub]
        n_phys = sum(1 for x in reads if x["settles_by"] == "measurement")
        n_pol = sum(1 for x in reads if x["settles_by"] == "decision")
        n_both = sum(1 for x in reads if x["settles_by"] == "unresolved_both")
        n_neither = sum(1 for x in reads if x["settles_by"] == "unresolved_neither")
        out.append({
            "item_id": item,
            "n_requirements": len(sub),
            "n_reconstructors": len(set(r["reconstructor_id"] for r in sub)),
            "status_counts": count_by(sub, "status"),
            "layer_counts": count_by(sub, "layer"),
            "physical": n_phys,
            "policy": n_pol,
            "unresolved": n_both + n_neither,
            "unresolved_both": n_both,
            "unresolved_neither": n_neither,
            "ratio_policy_to_physical": (round(n_pol / float(n_phys), 4) if n_phys else None),
            "ratio_note": "" if n_phys else "physical count is zero; ratio has no value",
            "reads": reads,
            "cues_physical": list(physical_cues),
            "cues_policy": list(policy_cues),
        })
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("requirements")
    ap.add_argument("--out", required=True)
    ap.add_argument("--physical-cues", default=",".join(PHYSICAL_CUES))
    ap.add_argument("--policy-cues", default=",".join(POLICY_CUES))
    ap.add_argument("--runs", default=None)
    a = ap.parse_args(argv)
    pc = [c for c in a.physical_cues.split(",") if c.strip()]
    qc = [c for c in a.policy_cues.split(",") if c.strip()]
    with Run("b4/grade.py", vars(a), None, [a.requirements], a.out, a.runs) as run:
        try:
            rows = read_jsonl(a.requirements)
            if not rows:
                return finish(run, "empty", {"requirements": 0})
            out = grade(rows, pc, qc)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        write_jsonl(a.out, out)
        tot = {k: sum(o[k] for o in out) for k in ("physical", "policy", "unresolved")}
        tot["items"] = len(out)
        return finish(run, "ok", tot)


if __name__ == "__main__":
    sys.exit(main())
