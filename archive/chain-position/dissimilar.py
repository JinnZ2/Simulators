#!/usr/bin/env python3
"""dissimilar.py -- WO-1 step 4 as a specification, NOT RUN on any model.

The order's first counter-argument: dissimilar redundancy works in
spaceflight because the spec is fixed and verifiable; two models on one
task produce disagreement that cannot be adjudicated, so diversity may
yield noise rather than fault detection. Marked UNRESOLVED there.

What this module does is name the input that decides it. Adjudication
of a disagreement needs a CHECKER independent of both outputs. With one,
disagreement is a fault detection and the checker says which copy
failed. Without one, disagreement is exactly as informative as
agreement was uninformative -- there is no reading. So the step-4
experiment has a precondition the order does not state: the task must
ship a checker, or the run returns DISAGREE_UNADJUDICABLE by
construction and settles nothing about model families.

`n_eff` counts DISTINCT families, because copies of one model share
their common-mode flaws (the order's gap 3); it is the structural form
of the count and makes no claim about any real family's independence.

Every output here is CONSTRUCTED. No model is called. The comparison
that would settle the counter-argument is the operator's step.
"""
import sys

STATES = ("AGREE", "DISAGREE_ADJUDICATED", "DISAGREE_UNADJUDICABLE", "ALL_FAIL", "EMPTY", "SINGLE")


def family(copy_id):
    """[CHOICE 4] a copy id is 'family' or 'family-copy'; the family is the prefix."""
    return str(copy_id).split("-")[0]


def n_eff(copy_ids):
    """Distinct families among the copies. None on empty."""
    fams = [family(c) for c in copy_ids if c is not None]
    return len(set(fams)) if fams else None


def adjudicate(outputs, checker=None):
    """outputs: family -> output. checker: output -> bool, independent of
    both outputs, or None when the task ships none."""
    if not outputs:
        return {"state": "EMPTY", "n_eff": None}
    ne = n_eff(outputs.keys())
    if len(outputs) == 1:
        return {"state": "SINGLE", "n_eff": ne, "why": "one copy; nothing to disagree with"}
    vals = list(outputs.values())
    if all(v == vals[0] for v in vals):
        return {"state": "AGREE", "n_eff": ne, "informative_about_correctness": False,
                "why": "agreement among copies reads as correctness only if the copies are independent"}
    if checker is None:
        return {"state": "DISAGREE_UNADJUDICABLE", "n_eff": ne, "checker": None,
                "why": "no checker independent of both outputs; noise and fault detection read alike"}
    passes = {fam: bool(checker(out)) for fam, out in outputs.items()}
    if not any(passes.values()):
        return {"state": "ALL_FAIL", "n_eff": ne, "passes": passes}
    return {"state": "DISAGREE_ADJUDICATED", "n_eff": ne, "passes": passes,
            "failed": sorted(f for f, ok in passes.items() if not ok)}


def constructed():
    """Constructed cases; the checker is a fixed spec, the spaceflight case."""
    spec = lambda out: out == 42
    return [
        ("same family, two copies, agree", {"F1": 42, "F1-copy": 42}, None),
        ("two families disagree, no checker", {"F1": 42, "F2": 41}, None),
        ("two families disagree, fixed spec", {"F1": 42, "F2": 41}, spec),
        ("two families disagree, both off spec", {"F1": 40, "F2": 41}, spec),
    ]


def render():
    lines = ["dissimilar -- WO-1 step 4 as a specification; NOT RUN on any model",
             "  every output CONSTRUCTED; the checker where present is a fixed spec; copy ids [CHOICE 4]"]
    for label, outs, chk in constructed():
        r = adjudicate(outs, chk)
        lines.append("    %-42s %-24s n_eff=%s %s" % (label, r["state"], r["n_eff"], r.get("failed", r.get("passes", ""))))
    lines.append("  reading: the run the order asks for has a precondition it does not state -- a checker")
    lines.append("           independent of both outputs; without one the result is fixed before any model runs")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("dissimilar.py refuses --selftest; run: python3 selftest.py")
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
