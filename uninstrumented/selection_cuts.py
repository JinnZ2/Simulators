#!/usr/bin/env python3
"""
selection_cuts.py - T1 from 023, built as an instrument rather than a rubric.

Scores a domain on the four conditions selection vocabulary names, and REFUSES
to score an unknown domain until the cut set has been shown to separate a
calibration set of known cases.

    python3 selection_cuts.py --calibrate     # run the gate, print per-cut work
    python3 selection_cuts.py --score DOMAIN  # score one case
    python3 selection_cuts.py --report        # every case, gate first
    python3 selection_cuts.py --template      # blank case to fill in
    python3 selection_cuts.py --selftest

The gate is the point. 023 says: "if the audit does not separate Lysenkoism
from population genetics it is not measuring anything." That is a
known-null/known-signal pair specified before the instrument existed, so it is
enforced here rather than recommended -- `null-harness/archetype_library.py`'s
ArchetypeGateNotRun applied to a four-way categorical.

Reports states and per-cut discriminability. Computes no verdict on any
domain.

Calibration scores are AUTHORED, from the historical record as described in
023 and its sources. They are the input, not a finding. Anyone who disagrees
with a score should change it and rerun the gate -- if the gate still passes,
the instrument survives the disagreement; if it does not, that is the finding.

stdlib only. CC0.
"""

import argparse
import itertools
import json
import sys
from collections import OrderedDict

# --- the four cuts. values are ordered worst-for-selection last. ------------

CUTS = OrderedDict([
    ("C1_exclusivity",
     ["EXCLUSIVE", "NOT_DETERMINABLE", "NON_EXCLUSIVE"]),
    ("C2_authorship",
     ["ENCOUNTERED", "MIXED", "AUTHORED_BY_INTERESTED_PARTIES"]),
    ("C3_criterion_stability",
     ["STABLE_EPOCH_EXISTS", "NOT_DETERMINABLE", "UNDER_CONTINUOUS_REVISION"]),
    ("C4_application_grain",
     ["PER_ROUND_UNIFORM", "NOT_DETERMINABLE", "PER_INSTANCE"]),
])

CUT_QUESTION = {
    "C1_exclusivity": "does failing the criterion remove you from the population",
    "C2_authorship": "was the environment encountered, or specified by parties "
                     "holding a position in the outcome",
    "C3_criterion_stability": "is there an epoch over which the criterion held",
    "C4_application_grain": "is the same criterion applied to everything within "
                            "a round",
}

# --- calibration set. AUTHORED. see module docstring. -----------------------
# `expects` is the class the case belongs to, not a score derived from the cuts.
#   LITERAL  - the word names what is happening; selection in the biological sense
#   BORROWED - the word is carrying credibility the arrangement does not supply

CALIBRATION = OrderedDict([
    ("population_genetics", {
        "expects": "LITERAL",
        "note": "the reference case. 023 names it as the thing an instrument "
                "must separate Lysenkoism from.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "ENCOUNTERED",
        "C3_criterion_stability": "STABLE_EPOCH_EXISTS",
        "C4_application_grain": "PER_ROUND_UNIFORM",
    }),
    ("antibiotic_resistance", {
        "expects": "LITERAL",
        "note": "023 NOT CLAIMED HERE names this as satisfying C1-C4.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "MIXED",          # the drug is authored, the response is not
        "C3_criterion_stability": "STABLE_EPOCH_EXISTS",
        "C4_application_grain": "PER_ROUND_UNIFORM",
    }),
    ("directed_evolution", {
        "expects": "LITERAL",
        "note": "023 names this too. Environment fully authored, and the word "
                "still holds -- which is why C2 alone cannot carry the "
                "instrument.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "STABLE_EPOCH_EXISTS",
        "C4_application_grain": "PER_ROUND_UNIFORM",
    }),
    ("evolutionary_algorithms", {
        "expects": "LITERAL",
        "note": "023 names this. Same shape as directed evolution.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "STABLE_EPOCH_EXISTS",
        "C4_application_grain": "PER_ROUND_UNIFORM",
    }),
    ("lysenkoism", {
        "expects": "BORROWED",
        "note": "023's inverse case. NOTE C1: dissenting geneticists WERE "
                "removed -- imprisonment and death. On the stated definition "
                "this scores EXCLUSIVE.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "PER_INSTANCE",
    }),
    ("eugenics", {
        "expects": "BORROWED",
        "note": "023: closest match including C4. Boards and individual "
                "physicians, different standards, legal enforcement. "
                "Sterilization removes from the reproducing population.",
        "C1_exclusivity": "EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "PER_INSTANCE",
    }),
    ("spencer_social_darwinism", {
        "expects": "BORROWED",
        "note": "023: authored, non-exclusive, continuously revised.",
        "C1_exclusivity": "NON_EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "PER_INSTANCE",
    }),
    ("alchian_firm_selection", {
        "expects": "BORROWED",
        "note": "023 names the C1 hole: an exited firm is not removed from "
                "possibility space.",
        "C1_exclusivity": "NON_EXCLUSIVE",
        "C2_authorship": "MIXED",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "PER_ROUND_UNIFORM",
    }),
    ("memetics", {
        "expects": "BORROWED",
        "note": "023: replicator language without the substrate. No ratchet.",
        "C1_exclusivity": "NON_EXCLUSIVE",
        "C2_authorship": "ENCOUNTERED",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "NOT_DETERMINABLE",
    }),
])

# the case 023 is actually about. NOT part of the calibration set.
SUBJECT = OrderedDict([
    ("ai_model_selection", {
        "expects": None,
        "note": "023's subject. Scored from the file's own four sections. "
                "Not calibration -- this is the unknown the gate exists to "
                "license scoring.",
        "C1_exclusivity": "NON_EXCLUSIVE",
        "C2_authorship": "AUTHORED_BY_INTERESTED_PARTIES",
        "C3_criterion_stability": "UNDER_CONTINUOUS_REVISION",
        "C4_application_grain": "PER_INSTANCE",
    }),
])


class GateNotRun(Exception):
    pass


_GATE = {"run": False, "passed": False, "detail": None}


def validate(case):
    problems = []
    for cut, allowed in CUTS.items():
        v = case.get(cut)
        if v is None:
            problems.append("%s uncoded" % cut)
        elif v not in allowed:
            problems.append("%s=%r not in %r" % (cut, v, allowed))
    return problems


def cut_discriminability(cases):
    """Per cut: does it separate LITERAL from BORROWED on the calibration set?

    Returns, per cut, the value sets each class takes and whether they are
    disjoint. A cut whose value sets overlap is not doing work on this set.
    """
    out = OrderedDict()
    for cut in CUTS:
        lit = set(c[cut] for c in cases.values() if c["expects"] == "LITERAL")
        bor = set(c[cut] for c in cases.values() if c["expects"] == "BORROWED")
        overlap = lit & bor
        out[cut] = {
            "literal_values": sorted(lit),
            "borrowed_values": sorted(bor),
            "overlap": sorted(overlap),
            "separates": not overlap,
        }
    return out


def separable(cases):
    """Does the FULL cut vector separate the two classes?

    Two cases with identical vectors and different classes make the set
    unseparable no matter how good any single cut is.
    """
    vec = {}
    for name, c in cases.items():
        key = tuple(c[cut] for cut in CUTS)
        vec.setdefault(key, []).append((name, c["expects"]))
    collisions = [(k, v) for k, v in vec.items()
                  if len(set(e for _n, e in v)) > 1]
    return (not collisions), collisions


def minimal_separating_subsets(cases):
    """Which combinations of cuts separate the two classes, minimally?

    A four-cut instrument in which one cut separates alone is a one-cut
    instrument with three cuts alongside it. Reported rather than hidden.
    """
    cuts = list(CUTS)

    def sep(sub):
        vec = {}
        for c in cases.values():
            vec.setdefault(tuple(c[x] for x in sub), set()).add(c["expects"])
        return all(len(v) == 1 for v in vec.values())

    minimal = []
    for r in range(1, len(cuts) + 1):
        for sub in itertools.combinations(cuts, r):
            if sep(sub) and not any(set(f) < set(sub) for f in minimal):
                minimal.append(sub)
    necessary = [c for c in cuts
                 if not sep([x for x in cuts if x != c])]
    return {"minimal": [list(m) for m in minimal], "necessary": necessary}


def calibrate(cases=None):
    """The gate. Must pass before an unknown domain may be scored."""
    cases = cases or CALIBRATION
    problems = []
    for name, c in cases.items():
        problems += ["%s: %s" % (name, p) for p in validate(c)]
    ok_vec, collisions = separable(cases)
    per_cut = cut_discriminability(cases)
    subsets = minimal_separating_subsets(cases)
    passed = (not problems) and ok_vec
    _GATE.update({"run": True, "passed": passed,
                  "detail": {"problems": problems, "separable": ok_vec,
                             "collisions": collisions, "per_cut": per_cut,
                             "subsets": subsets, "n": len(cases)}})
    return _GATE["detail"]


def score(case, name="(unnamed)"):
    """Score one domain. REFUSES unless the gate has been run and passed."""
    if not _GATE["run"]:
        raise GateNotRun(
            "calibrate() has not been run. 023: 'if the audit does not "
            "separate Lysenkoism from population genetics it is not measuring "
            "anything.' Run --calibrate first.")
    if not _GATE["passed"]:
        raise GateNotRun(
            "the calibration set is not separable by these cuts; scoring an "
            "unknown domain would report a number the instrument has not "
            "earned. See --calibrate.")
    problems = validate(case)
    if problems:
        raise ValueError("%s: %s" % (name, "; ".join(problems)))
    worst = [cut for cut, allowed in CUTS.items()
             if case[cut] == allowed[-1]]
    return {"domain": name,
            "cuts": OrderedDict((c, case[c]) for c in CUTS),
            "n_conditions_absent": len(worst),
            "absent": worst}


def render_gate(d):
    L = ["SELECTION-CUTS CALIBRATION GATE", ""]
    L.append("  calibration cases: %d   coding problems: %d"
             % (d["n"], len(d["problems"])))
    for p in d["problems"]:
        L.append("    ! %s" % p)
    L.append("")
    L.append("  PER-CUT DISCRIMINABILITY on the calibration set")
    L.append("  %-24s %-9s %s" % ("cut", "separates", "overlap"))
    for cut, r in d["per_cut"].items():
        L.append("  %-24s %-9s %s"
                 % (cut, "yes" if r["separates"] else "NO",
                    ", ".join(r["overlap"]) or "-"))
    L.append("")
    L.append("  FULL VECTOR separates the two classes: %s"
             % ("yes" if d["separable"] else "NO"))
    for k, v in d["collisions"]:
        L.append("    ! identical vector, different class: %s"
                 % ", ".join("%s(%s)" % (n, e) for n, e in v))
    L.append("")
    L.append("  MINIMAL SEPARATING SUBSETS")
    for m in d["subsets"]["minimal"]:
        L.append("    %d cut(s): %s"
                 % (len(m), " + ".join(x.split("_")[0] for x in m)))
    L.append("  cuts that are NECESSARY (dropping one breaks separation): %s"
             % (", ".join(x.split("_")[0] for x in d["subsets"]["necessary"])
                or "none"))
    L.append("")
    L.append("  GATE: %s" % ("PASS -- unknown domains may be scored"
                             if d["separable"] and not d["problems"]
                             else "FAIL -- scoring refused"))
    L.append("")
    L.append("  READING NOTE")
    L.append("    a cut that does not separate is not thereby wrong. it is not")
    L.append("    doing work ON THIS SET, and the set is small and authored.")
    L.append("    the honest use is to report which cuts carried the")
    L.append("    separation rather than to present four as if each did.")
    L.append("    the calibration scores are AUTHORED (see the docstring).")
    L.append("    this measures the cut set against that coding, not against")
    L.append("    the world. recode and rerun to test a disagreement.")
    return "\n".join(L)


def render_scores(cases, title):
    L = [title, ""]
    L.append("  %-26s %-14s %-14s %-14s %-14s %s"
             % ("domain", "C1", "C2", "C3", "C4", "absent"))
    for name, c in cases.items():
        s = score(c, name)
        L.append("  %-26s %-14s %-14s %-14s %-14s %d/4"
                 % (name,
                    c["C1_exclusivity"][:14],
                    c["C2_authorship"][:14],
                    c["C3_criterion_stability"][:14],
                    c["C4_application_grain"][:14],
                    s["n_conditions_absent"]))
    return "\n".join(L)


def selftest():
    fails = checks = 0

    def ck(label, cond):
        nonlocal fails, checks
        checks += 1
        if not cond:
            fails += 1
            print("FAIL %s" % label)

    _GATE.update({"run": False, "passed": False, "detail": None})
    try:
        score(CALIBRATION["population_genetics"], "x")
        ck("scoring refused before the gate runs", False)
    except GateNotRun:
        ck("scoring refused before the gate runs", True)

    d = calibrate()
    ck("no coding problems in the shipped set", d["problems"] == [])
    ck("gate ran", _GATE["run"])
    ck("full vector separates", d["separable"])
    ck("gate passed", _GATE["passed"])

    s = score(SUBJECT["ai_model_selection"], "subject")
    ck("subject scores after the gate", s["n_conditions_absent"] == 4)

    # a cut that does not separate must be reported, not hidden
    ck("per-cut discriminability reported for all four",
       len(d["per_cut"]) == 4)
    ck("C1 overlap is surfaced",
       "overlap" in d["per_cut"]["C1_exclusivity"])
    ck("minimal subsets computed", d["subsets"]["minimal"] != [])
    ck("a single-cut separator is reported when one exists",
       any(len(m) == 1 for m in d["subsets"]["minimal"]))

    # planted collision must fail the gate
    bad = OrderedDict(CALIBRATION)
    clone = dict(CALIBRATION["population_genetics"])
    clone["expects"] = "BORROWED"
    bad["planted_collision"] = clone
    d2 = calibrate(bad)
    ck("planted collision fails separability", not d2["separable"])
    _GATE.update({"run": True, "passed": False, "detail": d2})
    try:
        score(SUBJECT["ai_model_selection"], "x")
        ck("scoring refused when the gate failed", False)
    except GateNotRun:
        ck("scoring refused when the gate failed", True)

    calibrate()  # restore
    ck("bad code caught", validate({"C1_exclusivity": "NOPE"}) != [])

    print("%d/%d checks passed" % (checks - fails, checks))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--score", metavar="DOMAIN")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.template:
        t = OrderedDict([("expects", None),
                         ("note", "what this domain is, and the source")])
        for cut, allowed in CUTS.items():
            t[cut] = "one of %s   -- %s" % (allowed, CUT_QUESTION[cut])
        print(json.dumps(t, indent=2))
        return 0

    d = calibrate()
    if a.calibrate:
        print(render_gate(d))
        return 0 if d["separable"] and not d["problems"] else 1
    if a.report:
        print(render_gate(d))
        print()
        print(render_scores(CALIBRATION, "CALIBRATION SET"))
        print()
        print(render_scores(SUBJECT, "SUBJECT (023's case, not calibration)"))
        return 0
    if a.score:
        pool = dict(CALIBRATION); pool.update(SUBJECT)
        if a.score not in pool:
            print("unknown domain. known: %s" % ", ".join(sorted(pool)),
                  file=sys.stderr)
            return 2
        print(json.dumps(score(pool[a.score], a.score), indent=2))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
