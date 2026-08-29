#!/usr/bin/env python3
"""Dependency Ledger Audit, built and run.

SOURCE_DROP.md asks: "Apply it to one case and publish the residual
table, including the unmeasured cells. The unmeasured cells are the
finding."

This builds the method as an instrument and runs it. One hard
constraint is stated before any number: step 5 is CHECK each terminal
requirement against an INDEPENDENT record, and egress from this
environment is an allowlist that refuses every archive. So on the real
case every record-bounded cell comes back UNMEASURED, which is the
outcome the drop predicts and is the published finding.

An addition, derived from running the method rather than from reading
it. Steps 3 and 4 pull opposite ways:

    step 3   stop at conserved quantities -- energy, mass, momentum,
             time, material volume. These are bounded by physical LAW
             and are checkable from anywhere.
    step 4   expand each into its dependency set -- arable area, quarry
             volume, spoil heaps, pollen records. These are bounded by
             the RECORD and are checkable only with access to archives.

The propagation crosses from one class to the other and the spec gives
one procedure with no marker for where it changes character. So every
terminal requirement here carries `bound_by`, and the residual table is
split on it. The split is not cosmetic: it is the difference between a
cell anyone can close and a cell that requires an excavation.

usage:  python3 audit.py                 # the report
        python3 audit.py --case <id>
        python3 audit.py --selftest

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASEDIR = os.path.join(HERE, "cases")


class LedgerError(Exception):
    """A guard refused. Not recoverable by retrying."""


# --------------------------------------------------------- vocabulary

LAW = "LAW"        # bounded by physics; checkable from anywhere
RECORD = "RECORD"  # bounded by the archaeological/industrial record
BOUNDS = (LAW, RECORD)

# Step 3's stopping set, from the delivered text.
CONSERVED = ("energy", "mass", "momentum", "time", "material_volume")

# Closure verdicts. UNMEASURED is a first-class value and is never a
# pass -- the drop's RECORD GAP AS PASS failure mode, designed in.
SATISFIED = "SATISFIED"
GAP = "GAP"
FALSIFIED = "FALSIFIED"
UNMEASURED = "UNMEASURED"

# The drop writes "residual >> 1  method falsified as stated" and gives
# no value for >>. Declared here rather than left in prose, and every
# report prints it.
FALSIFY_AT = 10.0

# Provenance for a coefficient. SMUGGLED CONSTANTS requires the third.
ATTESTED = "attested"        # sourced to an artifact
REPLICATED = "replicated"    # sourced to an experimental replication
PHYSICAL = "physical"        # a physical constant or a law
UNSOURCED = "UNSOURCED"      # neither, and must say so
PROVENANCE = (ATTESTED, REPLICATED, PHYSICAL, UNSOURCED)


# ------------------------------------------------------------- guards
#
# The drop's five failure modes, as checks rather than prose. Each has
# a null test in the selftest: it must fire on a planted violation and
# stay silent on a clean case.

def _collapsed_vocabulary():
    """COLLAPSED PROXIES. The terms are imported, not retyped.

    The drop names "labor", "resources", "organisation" and says each
    is "a matrix entered as a scalar". `fold-matrix`'s register is a
    list of exactly that -- "a compact matrix wearing the costume of a
    scalar" is its own header -- and it already carries `resources` as
    "a stock and a flow, welded". Imported so the two cannot drift.
    """
    p = os.path.join(ROOT, "fold-matrix")
    if p not in sys.path:
        sys.path.insert(0, p)
    import fold_register as FR
    named = {"labor", "labour", "resources", "organisation",
             "organization", "workers", "ramps"}
    return named | set(FR.REGISTER), FR


def guard_collapsed_proxies(case):
    """A terminal requirement must not be a collapsed proxy."""
    vocab, _ = _collapsed_vocabulary()
    hits = []
    for r in case.get("requirements", []):
        name = r.get("name", "").lower()
        # The first version used [a-z_]+, which puts the underscore
        # IN the word class -- so `labor_required` is one token and
        # `labor` never appears. UNI_009's shape in the guard's own
        # tokenizer. Split on the separator instead.
        for w in re.findall(r"[a-z]+", name):
            if w in vocab:
                hits.append({"requirement": r.get("name"), "term": w})
    return {"guard": "COLLAPSED_PROXIES", "fired": bool(hits),
            "hits": hits,
            "vocabulary_size": len(vocab),
            "source": "fold-matrix.fold_register.REGISTER, imported"}


def guard_smuggled_constants(case):
    """Every coefficient carries provenance, and UNSOURCED is legal.

    The drop says a coefficient must be sourced "or marked when it is
    neither". So an unsourced constant is not refused -- it is required
    to say so, and the count is reported.
    """
    bad, unsourced = [], []
    for c in case.get("constants", []):
        p = c.get("provenance")
        if p not in PROVENANCE:
            bad.append({"constant": c.get("name"), "provenance": p})
        elif p == UNSOURCED:
            if not str(c.get("why", "")).strip():
                bad.append({"constant": c.get("name"),
                            "provenance": p,
                            "problem": "UNSOURCED with no reason"})
            unsourced.append(c.get("name"))
    return {"guard": "SMUGGLED_CONSTANTS", "fired": bool(bad),
            "unmarked": bad, "unsourced": unsourced,
            "n_constants": len(case.get("constants", [])),
            "unsourced_share": (len(unsourced) /
                                float(len(case.get("constants", [])))
                                if case.get("constants") else None)}


def guard_time_as_solvent(case):
    """Duration may close a ledger only if independently bounded."""
    d = case.get("duration")
    if d is None:
        return {"guard": "TIME_AS_SOLVENT", "fired": False,
                "state": "NO_DURATION_USED"}
    bound = d.get("bounded_by")
    if not bound:
        return {"guard": "TIME_AS_SOLVENT", "fired": True,
                "state": "DURATION_UNBOUNDED",
                "why": "duration enters the propagation and nothing "
                       "bounds it independently. Unbounded duration "
                       "absorbs any energy gap."}
    # A bound is itself a measurement and has a resolution. A bound
    # coarser than the duration it bounds is a G-RES failure.
    res, val = d.get("bound_resolution"), d.get("value")
    if res is not None and val is not None and res > val:
        return {"guard": "TIME_AS_SOLVENT", "fired": True,
                "state": "BOUND_COARSER_THAN_DURATION",
                "resolution": res, "duration": val,
                "why": "the independent bound is coarser than the "
                       "duration it bounds, so it cannot constrain it"}
    return {"guard": "TIME_AS_SOLVENT", "fired": False,
            "state": "BOUNDED", "bounded_by": bound}


def guard_labor_elasticity(case):
    """If the method scales workforce, every dependent must rescale."""
    s = case.get("labor_scaling")
    if not s:
        return {"guard": "LABOR_ELASTICITY", "fired": False,
                "state": "NO_SCALING_CLAIMED"}
    factor = s.get("factor")
    rescaled = set(s.get("rescaled", []))
    deps = set(s.get("dependents", []))
    missing = sorted(deps - rescaled)
    return {"guard": "LABOR_ELASTICITY", "fired": bool(missing),
            "factor": factor, "not_rescaled": missing,
            "why": "workforce is not free: it propagates to calories, "
                   "water, housing, waste and command overhead"}


def guard_record_gap_as_pass(rows):
    """An unmeasured cell must never be scored as satisfied."""
    bad = [r["name"] for r in rows
           if r["attested"] is None and r["verdict"] != UNMEASURED]
    return {"guard": "RECORD_GAP_AS_PASS", "fired": bool(bad),
            "mis_scored": bad,
            "why": "absent evidence is neither pass nor fail"}


GUARDS = ("COLLAPSED_PROXIES", "SMUGGLED_CONSTANTS", "TIME_AS_SOLVENT",
          "LABOR_ELASTICITY", "RECORD_GAP_AS_PASS")


# ------------------------------------------------------- closure test

def residual(req, att):
    """required / attested, three-valued. Never returns 0 for absent."""
    if att is None:
        return None
    if att == 0:
        raise LedgerError("attested is zero, not absent. A zero "
                          "denominator is not a residual; state the "
                          "requirement as unmeasured or fix the units.")
    return req / float(att)


def verdict(r):
    if r is None:
        return UNMEASURED
    if r <= 1.0:
        return SATISFIED
    if r >= FALSIFY_AT:
        return FALSIFIED
    return GAP


def check_units(r):
    """G-DIM at the residual.

    required/attested is a ratio, and the drop does not say the two
    must be the same quantity about the same object. Calories per day
    over granary tonnes is not a residual. Refused here.
    """
    ru, au = r.get("required_units"), r.get("attested_units")
    if r.get("attested") is None:
        return {"state": "NO_ATTESTED_VALUE", "ok": None}
    if not ru or not au:
        return {"state": "UNITS_UNDECLARED", "ok": False}
    if ru != au:
        return {"state": "UNITS_DIFFER", "ok": False,
                "required_units": ru, "attested_units": au}
    return {"state": "MATCHED", "ok": True, "units": ru}


def close(case):
    """The residual table. Not aggregated -- the drop forbids it."""
    rows = []
    for r in case.get("requirements", []):
        if r.get("bound_by") not in BOUNDS:
            raise LedgerError("requirement %r declares bound_by=%r, "
                              "not one of %s"
                              % (r.get("name"), r.get("bound_by"), BOUNDS))
        u = check_units(r)
        att = r.get("attested")
        if u["ok"] is False:
            res, v = None, UNMEASURED
        else:
            res = residual(r["required"], att)
            v = verdict(res)
        rows.append({
            "name": r["name"], "bound_by": r["bound_by"],
            "required": r["required"], "attested": att,
            "residual": res, "verdict": v,
            "units": u,
            "why_unmeasured": r.get("why_unmeasured"),
        })
    return rows


def table_split(rows):
    """Split on bound_by. The addition step 3 and step 4 need."""
    out = {}
    for b in BOUNDS:
        sub = [r for r in rows if r["bound_by"] == b]
        out[b] = {
            "n": len(sub),
            "unmeasured": sum(1 for r in sub
                              if r["verdict"] == UNMEASURED),
            "by_verdict": {v: sum(1 for r in sub if r["verdict"] == v)
                           for v in (SATISFIED, GAP, FALSIFIED,
                                     UNMEASURED)},
        }
    return out


def no_aggregate(rows):
    """The drop: 'Do not aggregate residuals into one score.'

    Enforced rather than instructed. Nothing here returns a mean, and
    the selftest reads this module's source to assert none appears.
    """
    return {"aggregate": None,
            "why": "the per-requirement residual localises the missing "
                   "capability to a named subsystem. A mean over "
                   "subsystems names none of them.",
            "n_rows": len(rows)}


def missing_component_spec(case, rows):
    """The product. Not a verdict -- a target someone can search for."""
    out = []
    for r in rows:
        if r["verdict"] in (GAP, FALSIFIED):
            s = case.get("specs", {}).get(r["name"], {})
            out.append({
                "subsystem": s.get("subsystem", r["name"]),
                "required_perf": "%.4g %s" % (r["required"],
                                              r["units"].get("units", "")),
                "closes_at_residual": 1.0,
                "constraints": s.get("constraints"),
                "reachable": s.get("reachable", "OPEN -- separate "
                                                "investigation"),
            })
    return out


# ------------------------------------------------------------- cases

def load_cases():
    if not os.path.isdir(CASEDIR):
        raise LedgerError("no cases/ directory")
    out = []
    for fn in sorted(os.listdir(CASEDIR)):
        if fn.endswith(".json"):
            with open(os.path.join(CASEDIR, fn), encoding="utf-8") as fh:
                d = json.load(fh)
            d.setdefault("id", fn[:-5])
            out.append(d)
    if not out:
        raise LedgerError("cases/ is empty; a residual table over no "
                          "case is a denominator of zero")
    return out


def run_case(case):
    rows = close(case)
    return {
        "id": case["id"],
        "constructed": bool(case.get("constructed")),
        "rows": rows,
        "split": table_split(rows),
        "guards": [
            guard_collapsed_proxies(case),
            guard_smuggled_constants(case),
            guard_time_as_solvent(case),
            guard_labor_elasticity(case),
            guard_record_gap_as_pass(rows),
        ],
        "specs": missing_component_spec(case, rows),
        "aggregate": no_aggregate(rows),
    }


# ------------------------------------------------------------- report

def wrap(t, w=68, ind="   "):
    out, cur = [], ind
    for word in t.split():
        if len(cur) + len(word) + 1 > w and cur.strip():
            out.append(cur.rstrip())
            cur = ind
        cur += word + " "
    if cur.strip():
        out.append(cur.rstrip())
    return out


def render():
    o = []
    o.append("DEPENDENCY LEDGER AUDIT -- built and run")
    o.append("SOURCE_DROP.md: \"Apply it to one case and publish the")
    o.append("residual table, including the unmeasured cells. The")
    o.append("unmeasured cells are the finding.\"")
    o.append("")
    o += wrap("Step 5 is CHECK against an INDEPENDENT record, and "
              "egress from this environment is an allowlist that "
              "refuses every archive. So on the real case every "
              "record-bounded cell is UNMEASURED. That is not a "
              "workaround; it is the run.", ind="")
    o.append("")

    o.append("0. THE LAW / RECORD SPLIT -- an addition, not in the spec")
    o += wrap("Step 3 says stop at conserved quantities: energy, mass, "
              "momentum, time, material volume. Those are bounded by "
              "physical LAW and are checkable from anywhere. Step 4 "
              "says expand each into its dependency set: arable area, "
              "quarry volume, spoil heaps, pollen records. Those are "
              "bounded by the RECORD and are checkable only with "
              "archive access.")
    o += wrap("The propagation crosses from one class to the other and "
              "the spec gives one procedure with no marker for where "
              "it changes character. Every terminal requirement here "
              "carries `bound_by` and the table is split on it. The "
              "split is the difference between a cell anyone can close "
              "and a cell that requires an excavation.")
    o.append("")
    o.append("   falsification threshold, declared: residual >= %.1f"
             % FALSIFY_AT)
    o += wrap("The drop writes \"residual >> 1\" and gives no value "
              "for >>. Stated here so it is a parameter rather than a "
              "reading.")
    o.append("")

    for case in load_cases():
        r = run_case(case)
        tag = "  [CONSTRUCTED]" if r["constructed"] else "  [REAL RUN]"
        o.append("=" * 62)
        o.append("CASE: %s%s" % (r["id"], tag))
        o.append("   artifact: %s" % case.get("artifact", "")[:200])
        o.append("")
        o.append("   RESIDUAL TABLE -- not aggregated")
        o.append("   %-34s %-7s %-11s %s"
                 % ("requirement", "bound", "residual", "verdict"))
        for row in r["rows"]:
            res = ("%.3g" % row["residual"]) if row["residual"] \
                is not None else "--"
            o.append("   %-34s %-7s %-11s %s"
                     % (row["name"][:34], row["bound_by"], res,
                        row["verdict"]))
            if row["verdict"] == UNMEASURED and row["why_unmeasured"]:
                o += wrap("^ " + row["why_unmeasured"], ind="       ")
        o.append("")
        for b in BOUNDS:
            sp = r["split"][b]
            o.append("   %-7s  %d cells, %d unmeasured   %s"
                     % (b, sp["n"], sp["unmeasured"],
                        ", ".join("%s=%d" % (k, v) for k, v
                                  in sorted(sp["by_verdict"].items())
                                  if v)))
        o.append("")
        o.append("   GUARDS")
        for g in r["guards"]:
            extra = ""
            if g["guard"] == "SMUGGLED_CONSTANTS":
                sh = g["unsourced_share"]
                extra = ("  unsourced %d of %d (%.0f%%)"
                         % (len(g["unsourced"]), g["n_constants"],
                            100 * sh) if sh is not None else "")
            if g["guard"] == "TIME_AS_SOLVENT":
                extra = "  " + g["state"]
            o.append("     %-20s fired: %-6s%s"
                     % (g["guard"], g["fired"], extra))
        o.append("")
        if r["specs"]:
            o.append("   MISSING COMPONENT SPEC")
            for s in r["specs"]:
                o.append("     subsystem     : %s" % s["subsystem"])
                o.append("     required perf : %s" % s["required_perf"])
                o.append("     constraints   : %s" % s["constraints"])
                o.append("     reachable?    : %s" % s["reachable"])
        o.append("")

    o.append("=" * 62)
    o.append("WHAT THE REAL RUN SHOWS, AND WHAT IT DOES NOT")
    o += wrap("The one cell that can be closed from here is the one "
              "whose independent record is PHYSIOLOGY rather than "
              "archaeology -- sustained human mechanical output, "
              "reachable from anywhere. It comes back GAP. Every "
              "record-bounded cell is UNMEASURED.")
    o += wrap("So the audit closes exactly on the terminal quantities "
              "that are laws and on none of the ones that are "
              "artifacts, which is the LAW/RECORD split showing up as "
              "a property of a run rather than a distinction argued "
              "for.")
    o += wrap("The residual on that one cell is built from six "
              "UNSOURCED coefficients out of eight. It is a "
              "demonstration that the propagation runs. It is NOT a "
              "measurement about any vessel, any river, or any period, "
              "and the SMUGGLED CONSTANTS guard reports the share so "
              "the number cannot be quoted without it.")
    o += wrap("TIME AS SOLVENT fires on the real case: a 30-day "
              "duration enters the propagation with nothing bounding "
              "it. Left firing rather than repaired, because bounding "
              "it requires occupation layers this environment cannot "
              "reach.")
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_audit
        return selftest_audit.run()
    if "--case" in argv:
        want = argv[argv.index("--case") + 1]
        for c in load_cases():
            if c["id"] == want:
                print(json.dumps(run_case(c), indent=2))
                return 0
        sys.stderr.write("no case %r; have: %s\n"
                         % (want, ", ".join(c["id"]
                                            for c in load_cases())))
        return 1
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
