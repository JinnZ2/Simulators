#!/usr/bin/env python3
"""Selftest for bins.py. Every falsifier in SPEC.md S7 gets an arm.

Two things this asserts that a pass alone does not show:

  the spec and the code agree     -- BINS, NONBINS, ROUTES and MODES are
                                     parsed, and the parse is checked
                                     against a constructed spec so a
                                     silently-empty parse cannot pass.
  the classifier discriminates    -- constructed pairs differing on ONE
                                     signal must land in different bins,
                                     and NOT_FORESEEN must be reachable.

CC0. stdlib only. Parses under Python 3.9.
"""

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bins as B  # noqa: E402


def _case(**sig):
    """A case with every signal ABSENT unless named."""
    s = {k: B.ABSENT for k in B.SIGNALS}
    s.update(sig)
    return {"id": "constructed", "signals": s}


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 0. the spec parse. A parse returning nothing must not pass.
    chk("five bins are parsed", len(B.BINS) == 5)
    chk("the negative is one of them", B.NEGATIVE in B.BINS)
    chk("two non-bins are parsed", len(B.NONBINS) == 2)
    chk("NOT_DERIVABLE is one", B.UNDERIVABLE in B.NONBINS)
    chk("MULTIPLE is the other", B.MULTIPLE in B.NONBINS)
    chk("two modes are parsed", set(B.MODES) == {"RETROSPECTIVE",
                                                 "FORWARD"})
    chk("every non-negative bin routes somewhere",
        all(B.ROUTES.get(b) for b in B.BINS if b != B.NEGATIVE))
    chk("the negative routes nowhere", not B.ROUTES.get(B.NEGATIVE))
    chk("every routed folder exists in the tree",
        all(os.path.isdir(os.path.join(B.ROOT, f))
            for fs in B.ROUTES.values() for f in fs))
    chk("one signal per non-negative bin",
        sorted(s["bin"] for s in B.SIGNALS.values())
        == sorted(b for b in B.BINS if b != B.NEGATIVE))

    # -- 1. S7: the classifier must read each signal separately.
    #    Pairs differing on exactly one signal must not agree.
    seen = {}
    for name, spec in B.SIGNALS.items():
        v = B.classify(_case(**{name: B.PRESENT}))["verdict"]
        seen[name] = v
        chk("%s alone lands on its own bin" % name, v == spec["bin"])
    chk("no two signals land on the same bin",
        len(set(seen.values())) == len(seen))

    # -- 2. S7: the negative must be reachable.
    allabs = B.classify(_case())
    chk("all-ABSENT reaches the negative", allabs["verdict"] == B.NEGATIVE)
    chk("and fires nothing", allabs["fires"] == [])

    # -- 3. S2/S7: NOT_DERIVABLE and NOT_FORESEEN must not collapse.
    #    The two cases fire NOTHING in both arms; only the search state
    #    differs, which is the whole of the distinction.
    uns = B.classify({"signals": {k: B.UNSEARCHED for k in B.SIGNALS}})
    chk("all-UNSEARCHED reaches NOT_DERIVABLE",
        uns["verdict"] == B.UNDERIVABLE)
    chk("both arms fire nothing",
        uns["fires"] == [] and allabs["fires"] == [])
    chk("and they are different verdicts",
        uns["verdict"] != allabs["verdict"])
    chk("the unsearched signals are named, not counted",
        sorted(uns["unsearched"]) == sorted(B.SIGNALS))
    mixed = B.classify(_case(prior_report=B.UNSEARCHED))
    chk("one unsearched signal with nothing firing is NOT_DERIVABLE",
        mixed["verdict"] == B.UNDERIVABLE)
    chk("a firing signal outranks an unsearched one",
        B.classify(_case(prior_report=B.UNSEARCHED,
                         no_instrument=B.PRESENT))["verdict"]
        == "GAP_UNINSTRUMENTED")

    # -- 4. MULTIPLE
    m = B.classify(_case(prior_report=B.PRESENT,
                         designed_control=B.PRESENT))
    chk("two signals give MULTIPLE", m["verdict"] == B.MULTIPLE)
    chk("both are listed", len(m["fires"]) == 2)
    chk("the primary is not computed when undeclared",
        m["primary"] == B.MULTIPLE)
    dm = B.classify(dict(_case(prior_report=B.PRESENT,
                               designed_control=B.PRESENT),
                         primary="KNOWN_ROUTED_AWAY"))
    chk("a declared primary is honoured",
        dm["primary"] == "KNOWN_ROUTED_AWAY")
    chk("and the rest go to `also`", dm["also"] == ["CONCEIVED_NOT_BUILT"])
    try:
        B.classify(dict(_case(prior_report=B.PRESENT),
                        primary="GAP_UNINSTRUMENTED"))
        chk("a primary that did not fire is refused", False)
    except B.SpecMismatch:
        chk("a primary that did not fire is refused", True)

    # -- 5. bad input refuses rather than defaulting
    try:
        B.classify({"signals": {"prior_report": "yes"}})
        chk("an unrecognised signal value is refused", False)
    except B.SpecMismatch:
        chk("an unrecognised signal value is refused", True)
    chk("a missing signal reads UNSEARCHED, not ABSENT",
        B.classify({"signals": {}})["verdict"] == B.UNDERIVABLE)

    # -- 6. S0: the rate is refused, and the refusal names the reason
    try:
        B.rate()
        chk("rate() refuses", False)
    except B.RateRefused as e:
        chk("rate() refuses", True)
        chk("and names the uncounted population",
            "generation-capacity R4" in str(e))
        chk("and names the mode that escapes it", "FORWARD" in str(e))

    # -- 7. S0.2 route-to-remedy. Three states, and the third is the
    #       one a boolean over an empty list destroys.
    hit = B.remedy_mismatch(dict(_case(prior_report=B.PRESENT),
                                 remedy={"addresses_bin":
                                         "KNOWN_ROUTED_AWAY"}))
    miss = B.remedy_mismatch(dict(_case(prior_report=B.PRESENT),
                                  remedy={"addresses_bin":
                                          "GAP_UNINSTRUMENTED"}))
    none = B.remedy_mismatch(dict(_case(),
                                  remedy={"addresses_bin":
                                          "GAP_UNINSTRUMENTED"}))
    chk("a remedy aimed at a firing bin is not a mismatch",
        hit["state"] == "CHECKED" and hit["mismatch"] is False)
    chk("a remedy aimed elsewhere is a mismatch",
        miss["state"] == "CHECKED" and miss["mismatch"] is True)
    chk("a remedy on a case where nothing fired is a third state",
        none["state"] == "NO_BIN_FIRED")
    chk("and its mismatch is None, not False", none["mismatch"] is None)
    chk("an undeclared remedy bin does not guess",
        B.remedy_mismatch(dict(_case(), remedy={"text": "x"}))["state"]
        == "REMEDY_BIN_UNDECLARED")
    chk("no remedy at all is its own state",
        B.remedy_mismatch(_case())["state"] == "NO_REMEDY_STATED")
    try:
        B.remedy_mismatch(dict(_case(), remedy={"addresses_bin": "XX"}))
        chk("a remedy aimed at a non-bin is refused", False)
    except B.SpecMismatch:
        chk("a remedy aimed at a non-bin is refused", True)

    # -- 8. S0.3 the recursion
    chk("an open recommendation is bin 3 again",
        B.recursion({"remedy": {"status": "OPEN"}})["is_bin_3_again"])
    chk("a closed-unimplemented one is too",
        B.recursion({"remedy": {"status": "CLOSED_UNIMPLEMENTED"}}
                    )["is_bin_3_again"])
    chk("an implemented one is not",
        B.recursion({"remedy": {"status": "IMPLEMENTED"}}
                    )["is_bin_3_again"] is False)
    chk("an unrecorded status is None, not False",
        B.recursion({"remedy": {"status": "UNRECORDED"}}
                    )["is_bin_3_again"] is None)
    chk("a missing status is None too",
        B.recursion({})["is_bin_3_again"] is None)
    try:
        B.recursion({"remedy": {"status": "PENDING"}})
        chk("an unrecognised status is refused", False)
    except B.SpecMismatch:
        chk("an unrecognised status is refused", True)

    # -- 9. S6 the calibration set
    cal = B.calibrate()
    chk("the case set is non-empty", cal["n"] > 0)
    chk("every case reproduces the bin it was built as",
        cal["agree"] == cal["n"])
    chk("the negative is reached on the real set",
        cal["negative_reachable"])
    chk("every verdict is reachable on the set",
        cal["verdicts_never_reached"] == [])
    # The first version of this check grepped the function body as a
    # string, and the body's own docstring says "Never reads
    # case['truth']" -- so the guard written to prove a field is not
    # read fired on the sentence saying it is not read. UNI_009 /
    # T1-1 inside the guard. AST, with the docstring removed.
    import ast
    tree = ast.parse(open(os.path.join(HERE, "bins.py"),
                          encoding="utf-8").read())
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "classify")
    body = fn.body[1:] if (fn.body and isinstance(fn.body[0], ast.Expr)
                           and isinstance(fn.body[0].value, ast.Constant)
                           and isinstance(fn.body[0].value.value, str)
                           ) else fn.body
    lits = [n.value for n in ast.walk(ast.Module(body=body, type_ignores=[]))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    chk("classify never reads `truth`", "truth" not in lits)
    chk("and the docstring that says so is what broke the first check",
        "truth" in ast.get_docstring(fn))
    chk("every case declares itself constructed",
        all(c.get("constructed") for c in B.load_cases()))
    chk("every case carries a basis per signal",
        all(sorted(c.get("signal_basis", {})) == sorted(B.SIGNALS)
            for c in B.load_cases()))
    chk("every case carries an authoring note",
        all(c.get("authoring_note") for c in B.load_cases()))

    # -- 10. S7: route-to-remedy must not fire on everything
    states = [B.remedy_mismatch(c)["mismatch"] for c in B.load_cases()]
    chk("at least one case has an aligned remedy", False in states)
    chk("at least one case has a mismatch", True in states)

    # -- 11. FORWARD mode
    fw = B.occupancy([_case(prior_report=B.PRESENT),
                      _case(no_instrument=B.PRESENT),
                      _case()])
    chk("occupancy counts systems", fw["n_systems"] == 3)
    chk("a system can occupy more than one bin",
        sum(B.occupancy([_case(prior_report=B.PRESENT,
                               no_instrument=B.PRESENT)]
                        )["occupancy"].values()) == 2)
    chk("the negative is counted as its own bin",
        fw["occupancy"][B.NEGATIVE] == 1)
    chk("the note refuses a probability reading",
        "Not a probability" in fw["note"])
    chk("forward mode emits no rate",
        not any(isinstance(v, float) for v in fw["occupancy"].values()))

    # -- 11b. the one wired route
    g = B.gap_mechanism(_case(no_instrument=B.PRESENT))
    chk("a gap case with no declared mechanism does not guess",
        g["state"] == "MECHANISM_UNDECLARED")
    chk("a non-gap case is its own state",
        B.gap_mechanism(_case(prior_report=B.PRESENT))["state"]
        == "BIN_DID_NOT_FIRE")
    ok_g = B.gap_mechanism(dict(_case(no_instrument=B.PRESENT),
                                gap={"mechanism": "STORAGE"}))
    chk("a declared mechanism in the vocabulary is accepted",
        ok_g["state"] == "DECLARED" and ok_g["mechanism"] == "STORAGE")
    try:
        B.gap_mechanism(dict(_case(no_instrument=B.PRESENT),
                             gap={"mechanism": "MADE_UP"}))
        chk("one outside it is refused", False)
    except B.SpecMismatch:
        chk("one outside it is refused", True)
    chk("the vocabulary is imported, not copied",
        ok_g["vocabulary_size"] == 8
        and "MECHANISMS" not in open(os.path.join(HERE, "bins.py"),
                                     encoding="utf-8")
        .read().split("def _mechanisms(")[0])
    chk("the real gap case declares one",
        any(B.gap_mechanism(c)["state"] == "DECLARED"
            for c in B.load_cases()))

    # -- 12. the report
    out = B.render()
    chk("the report names every bin", all(b in out for b in B.BINS))
    chk("it states the selection trap", "selected on the outcome" in out)
    chk("it says every case is constructed", "CONSTRUCTED" in out)
    chk("it shows the refusal rather than describing it",
        "rate() raises" in out)

    # -- 13. the screen
    sys.path.insert(0, os.path.join(B.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    # One declared exemption, and it is measured rather than taken.
    # `recommendation` is what a CSB-style body issues -- the domain's
    # own noun for the artifact whose status S0.3 reads -- and it is on
    # the interpretation list. Three arms, per SSS_049.
    EXEMPT = ("recommendation",)
    def masked(t):
        for w in EXEMPT:
            t = t.replace(w, "X" * len(w))
        return t
    chk("the exemption is one token", len(EXEMPT) == 1)
    chk("the report is clean once it is masked",
        not no_severity.hits(masked(out)))
    chk("and that token is the only thing that fires without the mask",
        all(h[1] == EXEMPT[0] for h in no_severity.hits(out)))
    chk("the screen is not silent by construction",
        bool(no_severity.hits(masked(out) + "\nthis case is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
