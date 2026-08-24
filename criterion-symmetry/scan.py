#!/usr/bin/env python3
"""SCAN — hold one criterion fixed, apply it unchanged across subject classes.

Built to SCAN_SPEC. The criterion is DATA, not code: swap `criterion` in
cases.json and re-run. Nothing about C1 is hard-coded here.

The one design decision the spec did not make, and the whole scan turns on
it: `criterion_disposition` is COMPUTED from the criterion's threshold and
the case's agreement_value. It is never hand-assigned. A case whose value
is not a number the criterion can read returns UNDETERMINED, which is a
third state and not a quiet `not_defect` -- the absent-versus-known-negative
repair this repo has recorded a dozen times.

That decision is what makes the scan able to fail. Hand-assigning
`criterion_disposition: defect` to the human cases would make the divergence
set fire by construction and the scan would report the answer it was given.

DECLARED. This module is written by a Claude instance and case A1 is a
criterion applied to a Claude run. The scan computes; it does not conclude.
See AUDIT_NOTES.md for what this folder does and does not score.

stdlib only. CC0. Parses under Python 3.9.

    python3 scan.py
    python3 scan.py --selftest
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "cases.json")

DEFECT = "defect"
NOT_DEFECT = "not_defect"
UNDETERMINED = "UNDETERMINED"


def load(path=CASES):
    with open(path, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    return d["criterion"], d["cases"]


# --------------------------------------------------------------------------
# apply the criterion -- mechanically, or not at all
# --------------------------------------------------------------------------

def criterion_disposition(crit, case):
    """What C returns for this case. UNDETERMINED when it cannot read it."""
    v = case.get("agreement_value")
    if v is None:
        return UNDETERMINED, "no numeric %s; C reads a rate and there is none" \
            % case.get("agreement_measure", "value")
    if case.get("quantity_type") != crit.get("reads_quantity_type"):
        return UNDETERMINED, (
            "quantity type is %s and C reads %s; different objects"
            % (case.get("quantity_type"), crit.get("reads_quantity_type")))
    over = v > crit["threshold"] if crit["direction"] == "above" \
        else v < crit["threshold"]
    if over:
        return crit["disposition_if_over"], "%.2f %s %.2f" % (
            v, ">" if crit["direction"] == "above" else "<", crit["threshold"])
    return NOT_DEFECT, "%.2f does not clear %.2f" % (v, crit["threshold"])


def actual(case):
    return DEFECT if case.get("actual_disposition") == DEFECT else NOT_DEFECT


def divergence(crit, case):
    cd, why = criterion_disposition(crit, case)
    ad = actual(case)
    if cd == UNDETERMINED:
        return "UNDETERMINED", cd, ad, why
    if cd == DEFECT and ad != DEFECT:
        return "FIRED", cd, ad, why
    if cd == NOT_DEFECT and ad == DEFECT:
        return "INVERSE", cd, ad, why
    return "agree", cd, ad, why


def scan(crit, cases):
    return [dict(case, _div=divergence(crit, case)) for case in cases]


# --------------------------------------------------------------------------
# the spec's own limits, enforced rather than described
# --------------------------------------------------------------------------

def quantity_types(cases):
    out = {}
    for c in cases:
        out.setdefault(c.get("quantity_type"), []).append(c["id"])
    return out


def combined_statistic(cases):
    """The spec forbids one. Refusing in code rather than in prose."""
    raise NotImplementedError(
        "agreement_value is not commensurable across cases: a within-body "
        "vote rate and a cross-body adoption fraction are properties of "
        "different objects. reasoning-gate G-DIM voids the RATIO; the "
        "side-by-side comparison stays legal. Report typed.")


def unsourced(cases):
    return [c["id"] for c in cases
            if c.get("retention_basis") not in (None, "not_applicable")
            and not c.get("source")]


# --------------------------------------------------------------------------
# falsifiers, as specified
# --------------------------------------------------------------------------

def falsifier_one(rows):
    """C returns the same disposition as actual across all human cases."""
    human = [r for r in rows if r["subject_class"] == "human_institution"
             and r["status"] == "SEED"]
    states = set(r["_div"][0] for r in human)
    if states == {"agree"}:
        return True, "C agrees with the actual disposition on all %d human " \
                     "seed cases; there is no asymmetry and the marker fails" \
                     % len(human)
    if UNDETERMINED in states:
        n = sum(1 for r in human if r["_div"][0] == "UNDETERMINED")
        return False, ("cannot fire: %d of %d human seed cases return "
                       "UNDETERMINED, so C has not been applied to them at "
                       "all" % (n, len(human)))
    return False, "C disagrees with the actual disposition somewhere"


def falsifier_two(rows):
    """Any human case with comparison_run and a result favouring the form."""
    out = []
    for r in rows:
        if r["subject_class"] != "human_institution":
            continue
        if r.get("comparison_run") and r.get("comparison_favours_dominant"):
            out.append(r["id"])
    return out


# --------------------------------------------------------------------------

def report():
    crit, cases = load()
    rows = scan(crit, cases)

    print("CRITERION-SYMMETRY SCAN")
    print("criterion %s: %s" % (crit["id"], crit["statement"]))
    print("  reads     : %s" % crit["reads_quantity_type"])
    print("  threshold : %s %.2f" % (crit["direction"], crit["threshold"]))
    print("  source    : %s" % crit["threshold_source"])
    print()

    print("%-5s %-20s %-30s %-10s %-13s %s"
          % ("id", "class", "quantity type", "value", "C returns", "actual"))
    print("-" * 100)
    for r in rows:
        v = ("%.2f" % r["agreement_value"]) if r.get("agreement_value") \
            is not None else (r.get("agreement_value_stated") or "unstated")
        print("%-5s %-20s %-30s %-10s %-13s %s"
              % (r["id"], r["subject_class"], r.get("quantity_type"),
                 v[:10], r["_div"][1], r["_div"][2]))
    print()

    fired = [r for r in rows if r["_div"][0] == "FIRED"]
    inverse = [r for r in rows if r["_div"][0] == "INVERSE"]
    undet = [r for r in rows if r["_div"][0] == "UNDETERMINED"]
    agree = [r for r in rows if r["_div"][0] == "agree"]

    print("DIVERGENCE, as the spec's scoring rule defines it")
    print("  FIRED        (C=defect, actual!=defect) : %d   %s"
          % (len(fired), " ".join(r["id"] for r in fired)))
    print("  INVERSE      (C!=defect, actual=defect) : %d   %s"
          % (len(inverse), " ".join(r["id"] for r in inverse)))
    print("  agree                                   : %d   %s"
          % (len(agree), " ".join(r["id"] for r in agree)))
    print("  UNDETERMINED (C cannot read the case)   : %d   %s"
          % (len(undet), " ".join(r["id"] for r in undet)))
    print()
    for r in undet:
        print("    %-4s %s" % (r["id"], r["_div"][3]))
    print()

    print("WHY THE FIRED SET IS %s" % ("EMPTY" if not fired else "NOT EMPTY"))
    if not fired:
        print("  Every human seed case returns UNDETERMINED, for two reasons")
        print("  and either one alone is sufficient:")
        print("    1. none carries a numeric agreement_value. The spec")
        print("       states them as 'near-universal' and as unquantified.")
        print("    2. their quantity type is cross_body_adoption_fraction")
        print("       and C reads within_body_agreement_rate. Different")
        print("       objects.")
        print("  So the scan does NOT show the asymmetry. It shows that the")
        print("  criterion has not been applied to the human cases -- which")
        print("  is what the marker's own standard asks for before the")
        print("  asymmetry is a measurement rather than an impression.")
    print()

    print("THE SPEC'S OWN LIMIT, ENFORCED")
    qt = quantity_types([r for r in rows])
    for t in sorted(qt, key=lambda x: (x is None, x)):
        print("  %-32s %s" % (t, " ".join(qt[t])))
    try:
        combined_statistic(rows)
    except NotImplementedError as ex:
        print("  combined statistic: REFUSED")
        for line in str(ex).split(". "):
            if line.strip():
                print("    %s" % line.strip().rstrip("."))
    print()

    print("SOURCES")
    u = unsourced(rows)
    print("  cases asserting a retention_basis with no source: %d of %d   %s"
          % (len(u), sum(1 for r in rows
                         if r.get("retention_basis") not in
                         (None, "not_applicable")), " ".join(u)))
    print("  The spec requires unsourced entries be marked. All of them are.")
    print("  retention_basis is the mechanism the whole argument runs on and")
    print("  it currently carries zero sourced entries.")
    print()

    print("FALSIFIERS, as specified")
    f1, why1 = falsifier_one(rows)
    print("  1  C agrees with actual across all human cases: %s" % f1)
    print("     %s" % why1)
    f2 = falsifier_two(rows)
    print("  2  human case with comparison_run and a result favouring the")
    print("     dominant form: %s" % (" ".join(f2) if f2 else "none"))
    print("     H4's comparison WAS run and the result does not favour the")
    print("     dominant form, so H4 does not exit the set. No case does.")
    print()

    prop = [r for r in rows if r["status"] == "PROPOSED"]
    print("THE INVERSE BRANCH")
    print("  seed cases able to reach it: %d"
          % sum(1 for r in rows if r["status"] == "SEED"
                and r.get("quantity_type") == crit["reads_quantity_type"]
                and r["id"] != "A1"))
    print("  Every seed case is a high-agreement or high-uniformity case, so")
    print("  the inverse branch is CONSTANT_SILENT on the delivered set. A")
    print("  case set in which only one branch can fire cannot separate 'the")
    print("  criterion is applied asymmetrically' from 'the set was selected")
    print("  on the variable under test' -- which is the spec's own stated")
    print("  limit, reached here as a countable property rather than a")
    print("  caveat.")
    if prop:
        print("  %s is the SHAPE of an inverse case, values left unstated"
              % " ".join(r["id"] for r in prop))
        print("  rather than invented. It is not evidence and is not scored.")
        print("  If low agreement in a legislature is scored a defect while")
        print("  high agreement would also be scored a defect, the criterion")
        print("  is not applied asymmetrically BY SUBJECT CLASS -- it returns")
        print("  defect at both ends for one class, which is a different")
        print("  failure and arguably a worse one.")
    print()


def selftest():
    fails = []
    crit, cases = load()
    rows = scan(crit, cases)

    ids = [c["id"] for c in cases]
    if len(set(ids)) != len(ids):
        fails.append("duplicate case ids")

    # The criterion must never be hand-assigned. If any case carries a
    # criterion_disposition field, the scan is being told its answer.
    told = [c["id"] for c in cases if "criterion_disposition" in c]
    if told:
        fails.append("criterion_disposition is hand-set on %s; the scan must "
                     "compute it or it reports the answer it was given"
                     % told)

    # A1 must be readable, or the scan has no anchor at all.
    a1 = [r for r in rows if r["id"] == "A1"][0]
    if a1["_div"][1] == UNDETERMINED:
        fails.append("A1 is UNDETERMINED; the one case with a number no "
                     "longer reads and the scan measures nothing")
    if a1["_div"][0] != "agree":
        fails.append("A1 no longer agrees (C=%s, actual=%s); RESULTS.md must "
                     "be restated" % (a1["_div"][1], a1["_div"][2]))

    # The headline: no human seed case may be scorable as delivered.
    human = [r for r in rows if r["subject_class"] == "human_institution"
             and r["status"] == "SEED"]
    scorable = [r["id"] for r in human if r["_div"][1] != UNDETERMINED]
    if scorable:
        fails.append("human seed cases %s are now scorable; the headline "
                     "finding must be restated" % scorable)

    # ...and the UNDETERMINED state must be reachable AND avoidable, or it
    # is not a state, it is the only answer.
    states = set(r["_div"][1] for r in rows)
    if UNDETERMINED not in states or len(states) < 2:
        fails.append("criterion_disposition returns %s; it cannot "
                     "discriminate" % states)

    # The inverse branch must be empty on seeds, or the finding is wrong.
    inv = [r["id"] for r in rows if r["_div"][0] == "INVERSE"
           and r["status"] == "SEED"]
    if inv:
        fails.append("a seed case reached the inverse branch (%s); the "
                     "CONSTANT_SILENT finding must be restated" % inv)

    # The spec's forbidden statistic must stay refused.
    try:
        combined_statistic(rows)
        fails.append("combined_statistic no longer refuses; the spec's "
                     "non-commensurability limit is unenforced")
    except NotImplementedError:
        pass

    # Every retention_basis claim must be marked unsourced, per the spec.
    claims = [c["id"] for c in cases
              if c.get("retention_basis") not in (None, "not_applicable")]
    if set(unsourced(cases)) != set(claims):
        fails.append("some retention_basis claim now carries a source; "
                     "RESULTS.md must be restated")

    # Criterion must be data, not code.
    src = open(os.path.join(HERE, "scan.py"), errors="replace").read()
    for token in ("rubber-stamp", "0.98", "Emergence"):
        if token in src.split('"""')[2] if src.count('"""') > 2 else False:
            fails.append("%r is hard-coded in scan.py's body" % token)

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
