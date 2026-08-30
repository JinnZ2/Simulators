#!/usr/bin/env python3
"""Selftest for audit.py.

Each of the drop's five failure modes is a guard, and a guard that
cannot stay silent is not a guard. Every one gets both arms: it must
fire on a planted violation and not fire on a clean case.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import audit as A  # noqa: E402


def _req(**kw):
    d = {"name": "x", "bound_by": A.LAW, "required": 1.0,
         "required_units": "W", "attested": 2.0, "attested_units": "W"}
    d.update(kw)
    return d


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    src = open(os.path.join(HERE, "audit.py"), encoding="utf-8").read()

    # -- 1. the closure test, all four verdicts reachable
    chk("residual <= 1 is satisfied", A.verdict(0.5) == A.SATISFIED)
    chk("just above 1 is a gap", A.verdict(1.01) == A.GAP)
    chk("at the declared threshold it is falsified",
        A.verdict(A.FALSIFY_AT) == A.FALSIFIED)
    chk("None is unmeasured", A.verdict(None) == A.UNMEASURED)
    chk("exactly 1 is satisfied, not a gap", A.verdict(1.0) == A.SATISFIED)
    chk("the falsification threshold is declared, not in prose",
        isinstance(A.FALSIFY_AT, float) and "FALSIFY_AT" in src)

    # -- 2. RECORD GAP AS PASS. The repair, both directions.
    chk("absent attested gives no residual",
        A.residual(5.0, None) is None)
    chk("and never zero", A.residual(5.0, None) != 0)
    try:
        A.residual(5.0, 0)
        chk("attested of zero is refused, not treated as absent", False)
    except A.LedgerError:
        chk("attested of zero is refused, not treated as absent", True)
    rows = A.close({"requirements": [_req(attested=None,
                                          attested_units=None)]})
    chk("an absent cell scores UNMEASURED",
        rows[0]["verdict"] == A.UNMEASURED)
    g = A.guard_record_gap_as_pass(rows)
    chk("the guard is silent on a correctly-scored table", not g["fired"])
    bent = [dict(rows[0], verdict=A.SATISFIED)]
    chk("and fires when an absent cell is scored satisfied",
        A.guard_record_gap_as_pass(bent)["fired"])

    # -- 3. COLLAPSED PROXIES, imported vocabulary, both arms
    clean = {"requirements": [_req(name="shaft_power_per_rower")]}
    dirty = {"requirements": [_req(name="labor_required"),
                             _req(name="total_resources")]}
    cg, dg = (A.guard_collapsed_proxies(clean),
              A.guard_collapsed_proxies(dirty))
    chk("collapsed-proxy guard silent on a conserved quantity",
        not cg["fired"])
    chk("and fires on a collapsed proxy", dg["fired"])
    chk("it names which term", {h["term"] for h in dg["hits"]}
        == {"labor", "resources"})
    chk("the vocabulary is imported from fold-matrix",
        "fold_register" in cg["source"])
    vocab, FR = A._collapsed_vocabulary()
    chk("and it includes that register's own terms",
        "resources" in FR.REGISTER and "resources" in vocab)
    # fold_register.py's header is `#` comments, so __doc__ is None --
    # experience-ledger EL_002, the same shape one folder over.
    chk("the register has no docstring, so the source is read",
        FR.__doc__ is None)
    chk("and it calls them scalars wearing a matrix's costume",
        "scalar" in open(os.path.join(A.ROOT, "fold-matrix",
                                      "fold_register.py"),
                         encoding="utf-8").read().lower())

    # -- 4. SMUGGLED CONSTANTS. UNSOURCED is legal; unmarked is not.
    ok_c = {"constants": [{"name": "g", "value": 9.81,
                           "provenance": A.PHYSICAL}]}
    marked = {"constants": [{"name": "cd", "value": 0.3,
                             "provenance": A.UNSOURCED,
                             "why": "no replication"}]}
    unmarked = {"constants": [{"name": "cd", "value": 0.3,
                               "provenance": "modern handbook"}]}
    bare = {"constants": [{"name": "cd", "value": 0.3,
                           "provenance": A.UNSOURCED}]}
    chk("a sourced constant does not fire",
        not A.guard_smuggled_constants(ok_c)["fired"])
    chk("an UNSOURCED constant WITH a reason does not fire",
        not A.guard_smuggled_constants(marked)["fired"])
    chk("but it is counted",
        A.guard_smuggled_constants(marked)["unsourced_share"] == 1.0)
    chk("a provenance outside the vocabulary fires",
        A.guard_smuggled_constants(unmarked)["fired"])
    chk("and UNSOURCED with no reason fires",
        A.guard_smuggled_constants(bare)["fired"])
    chk("the share is None when there are no constants",
        A.guard_smuggled_constants({})["unsourced_share"] is None)

    # -- 5. TIME AS SOLVENT, three states
    chk("no duration used is not a firing",
        not A.guard_time_as_solvent({})["fired"])
    chk("an unbounded duration fires",
        A.guard_time_as_solvent({"duration": {"value": 30.0}})["fired"])
    fine = {"duration": {"value": 30.0, "bounded_by": "dated phases",
                         "bound_resolution": 5.0}}
    chk("a bounded one does not", not A.guard_time_as_solvent(fine)["fired"])
    coarse = {"duration": {"value": 30.0, "bounded_by": "dated phases",
                           "bound_resolution": 200.0}}
    r = A.guard_time_as_solvent(coarse)
    chk("a bound coarser than the duration fires", r["fired"])
    chk("and says so", r["state"] == "BOUND_COARSER_THAN_DURATION")

    # -- 6. LABOR ELASTICITY
    chk("no scaling claimed is not a firing",
        not A.guard_labor_elasticity({})["fired"])
    part = {"labor_scaling": {"factor": 2.0,
                              "dependents": ["calories", "water",
                                             "housing"],
                              "rescaled": ["calories"]}}
    full = {"labor_scaling": {"factor": 2.0,
                              "dependents": ["calories"],
                              "rescaled": ["calories"]}}
    chk("scaling labor without rescaling dependents fires",
        A.guard_labor_elasticity(part)["fired"])
    chk("it names the ones not rescaled",
        A.guard_labor_elasticity(part)["not_rescaled"]
        == ["housing", "water"])
    chk("rescaling all of them does not fire",
        not A.guard_labor_elasticity(full)["fired"])

    # -- 7. G-DIM at the residual. The spec does not ask for this.
    mismatched = A.close({"requirements": [
        _req(required_units="kcal/day", attested_units="t")]})
    chk("a ratio across unlike units is not computed",
        mismatched[0]["residual"] is None)
    chk("and lands on UNMEASURED rather than a number",
        mismatched[0]["verdict"] == A.UNMEASURED)
    chk("the units check says why",
        mismatched[0]["units"]["state"] == "UNITS_DIFFER")
    undecl = A.close({"requirements": [_req(required_units=None)]})
    chk("undeclared units are refused too",
        undecl[0]["units"]["state"] == "UNITS_UNDECLARED")
    matched = A.close({"requirements": [_req()]})
    chk("matched units compute", matched[0]["residual"] == 0.5)

    # -- 8. no aggregation, enforced rather than instructed
    agg = A.no_aggregate(matched)
    chk("no aggregate is emitted", agg["aggregate"] is None)
    chk("and it says why", "localises" in agg["why"])
    # The first version of this grepped `sum(` across close() through
    # missing_component_spec and caught table_split's cell COUNTS,
    # which are counts of verdicts and not aggregates of residuals.
    # The rule is about residuals, so the check is too.
    import ast as _ast
    tree = _ast.parse(src)
    fns = {n.name: n for n in _ast.walk(tree)
           if isinstance(n, _ast.FunctionDef)}
    agg = []
    for fname in ("close", "table_split", "no_aggregate",
                  "missing_component_spec"):
        for node in _ast.walk(fns[fname]):
            if isinstance(node, _ast.Call) and \
                    isinstance(node.func, _ast.Name) and \
                    node.func.id in ("sum", "max", "min"):
                srcseg = _ast.dump(node)
                if "residual" in srcseg:
                    agg.append(fname)
    chk("no residual is ever summed, maxed, or averaged", not agg)
    chk("and the cell counts that ARE summed are verdicts, not residuals",
        "sum(1 for r in sub" in src)

    # -- 9. bound_by is required and validated
    try:
        A.close({"requirements": [_req(bound_by="MAYBE")]})
        chk("an undeclared bound_by is refused", False)
    except A.LedgerError:
        chk("an undeclared bound_by is refused", True)
    chk("both bounds exist", set(A.BOUNDS) == {"LAW", "RECORD"})

    # -- 10. the cases. The table must discriminate.
    cases = {c["id"]: A.run_case(c) for c in A.load_cases()}
    chk("three cases", len(cases) == 3)
    verds = set()
    for r in cases.values():
        for row in r["rows"]:
            verds.add(row["verdict"])
    chk("all four verdicts occur across the corpus",
        verds == {A.SATISFIED, A.GAP, A.FALSIFIED, A.UNMEASURED})
    chk("so the table is not CONSTANT_SILENT and not CONSTANT_FIRES",
        A.SATISFIED in verds and A.FALSIFIED in verds)
    chk("the two constructed cases say so in their own text",
        all(c["artifact"].startswith("CONSTRUCTED")
            for c in A.load_cases() if c.get("constructed")))

    # -- 11. the real run, and its honesty
    w = cases["watercraft-propulsion"]
    chk("the real case is not marked constructed", not w["constructed"])
    chk("its LAW cell closes", w["split"]["LAW"]["unmeasured"] == 0)
    chk("and every RECORD cell does not",
        w["split"]["RECORD"]["unmeasured"] == w["split"]["RECORD"]["n"])
    chk("the RECORD side is non-empty", w["split"]["RECORD"]["n"] >= 4)
    sm = [g for g in w["guards"] if g["guard"] == "SMUGGLED_CONSTANTS"][0]
    chk("most of its constants are unsourced",
        sm["unsourced_share"] > 0.5)
    chk("and each unsourced one carries a reason", not sm["unmarked"])
    ts = [g for g in w["guards"] if g["guard"] == "TIME_AS_SOLVENT"][0]
    chk("TIME AS SOLVENT fires on the real case, unrepaired",
        ts["fired"] and ts["state"] == "DURATION_UNBOUNDED")
    chk("the gap produces a missing-component spec", w["specs"])
    chk("whose reachability is left open",
        "OPEN" in w["specs"][0]["reachable"])

    # -- 12. an empty corpus is refused
    saved = A.CASEDIR
    try:
        A.CASEDIR = os.path.join(HERE, "no_such_dir")
        try:
            A.load_cases()
            chk("an absent corpus is refused", False)
        except A.LedgerError:
            chk("an absent corpus is refused", True)
    finally:
        A.CASEDIR = saved

    # -- 13. the screen
    sys.path.insert(0, os.path.join(A.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    out = A.render()
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis case is broken\n")))
    chk("the report states the egress constraint",
        "allowlist" in out)
    chk("and refuses to let the residual be quoted alone",
        "NOT a measurement" in out)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
