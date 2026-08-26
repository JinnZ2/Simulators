#!/usr/bin/env python3
"""investigation-sim -- foreknowledge bins for a CSB-style investigation.

Reads SPEC.md rather than restating it: the five bin names, the two
non-bin verdicts, the routing table and the mode list are parsed from
the spec at import, so a decision changed in one and not the other
turns --selftest red.

The classifier reads a case's SIGNALS -- what the record says exists --
and returns a primary bin plus every other bin that fires. It does not
read the case's `truth` field, which exists only so the calibration set
can be scored.

S0 is the load-bearing constraint: no rate is computable from a
retrospective corpus, so `rate()` raises rather than returning one.

usage:  python3 bins.py                      # the report
        python3 bins.py --case <id>          # one case
        python3 bins.py --forward <file>     # forward-mode occupancy
        python3 bins.py --selftest

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPEC = os.path.join(HERE, "SPEC.md")
CASEDIR = os.path.join(HERE, "cases")


class SpecMismatch(Exception):
    """The spec and the code disagree. Not recoverable at run time."""


class RateRefused(Exception):
    """S0. A rate over a corpus selected on the outcome has no value."""


# ---------------------------------------------------------------- spec

def _spec():
    return open(SPEC, encoding="utf-8").read()


def spec_bins():
    """The five bin names, in spec order, from S1."""
    body = _spec().split("## S1")[1].split("## S2")[0]
    return tuple(m.group(1) for m in
                 re.finditer(r"^    ([A-Z][A-Z_]+)$", body, re.M))


def spec_nonbins():
    """NOT_DERIVABLE and MULTIPLE, from S2."""
    body = _spec().split("## S2")[1].split("## S3")[0]
    return tuple(m.group(1) for m in
                 re.finditer(r"^    ([A-Z][A-Z_]+)$", body, re.M))


def spec_routes():
    """bin -> the folders S1 says it routes to."""
    body = _spec().split("## S1")[1].split("## S2")[0]
    out, cur = {}, None
    for ln in body.split("\n"):
        m = re.match(r"^    ([A-Z][A-Z_]+)$", ln)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur and "ROUTES TO:" in ln:
            out[cur] = [x.strip() for x in
                        ln.split("ROUTES TO:")[1].split(",") if x.strip()]
    return out


def spec_modes():
    body = _spec().split("## S4")[1].split("## S5")[0]
    return tuple(m.group(1) for m in
                 re.finditer(r"^    ([A-Z]+)\s{2,}", body, re.M))


BINS = spec_bins()
NONBINS = spec_nonbins()
ROUTES = spec_routes()
MODES = spec_modes()

# The negative. Named once, here, so nothing has to string-match it.
NEGATIVE = "NOT_FORESEEN"
UNDERIVABLE = "NOT_DERIVABLE"
MULTIPLE = "MULTIPLE"


# ------------------------------------------------------------- signals
#
# One signal per bin. A signal is a property of the RECORD, three-
# valued, and the third value is the one that keeps NOT_DERIVABLE and
# NOT_FORESEEN apart.
#
#   PRESENT      the record says it exists
#   ABSENT       the record was searched and says it does not
#   UNSEARCHED   nobody looked, or the record cannot say
#
# ABSENT is a measurement. UNSEARCHED is not. Collapsing them is the
# defect S2 exists to prevent.

PRESENT = "PRESENT"
ABSENT = "ABSENT"
UNSEARCHED = "UNSEARCHED"
SIGNAL_STATES = (PRESENT, ABSENT, UNSEARCHED)

SIGNALS = {
    "prior_report": {
        "bin": "KNOWN_ROUTED_AWAY",
        "asks": "Did a report of this hazard reach anyone in the "
                "organisation before the event?",
    },
    "figure_without_clock": {
        "bin": "CALCULATED_UNCLOCKED",
        "asks": "Was a governing number produced whose domain of "
                "validity or re-check interval is not carried with it?",
    },
    "designed_control": {
        "bin": "CONCEIVED_NOT_BUILT",
        "asks": "Was a control designed, costed, or scheduled and not "
                "implemented?",
    },
    "no_instrument": {
        "bin": "GAP_UNINSTRUMENTED",
        "asks": "Was the quantity outside what any instrument in place "
                "could report, by the instrument's constitution?",
    },
}


def _sig(case, name):
    v = (case.get("signals") or {}).get(name, UNSEARCHED)
    if v not in SIGNAL_STATES:
        raise SpecMismatch("signal %r has value %r, not one of %s"
                           % (name, v, SIGNAL_STATES))
    return v


def classify(case):
    """Primary bin, everything else that fires, and what was not looked at.

    Never reads case['truth'].
    """
    fires, unsearched = [], []
    for name, spec in SIGNALS.items():
        v = _sig(case, name)
        if v == PRESENT:
            fires.append(spec["bin"])
        elif v == UNSEARCHED:
            unsearched.append(name)

    if fires:
        primary = case.get("primary")
        if primary is not None and primary not in fires:
            raise SpecMismatch(
                "declared primary %r is not among the bins that fire: %s"
                % (primary, fires))
        if primary is None:
            primary = fires[0] if len(fires) == 1 else MULTIPLE
        return {
            "primary": primary,
            "fires": fires,
            "also": [b for b in fires if b != primary],
            "unsearched": unsearched,
            "verdict": MULTIPLE if len(fires) > 1 else fires[0],
        }

    # Nothing fired. The two ways that happens are not the same thing.
    if unsearched:
        return {
            "primary": UNDERIVABLE,
            "fires": [],
            "also": [],
            "unsearched": unsearched,
            "verdict": UNDERIVABLE,
        }
    return {
        "primary": NEGATIVE,
        "fires": [],
        "also": [],
        "unsearched": [],
        "verdict": NEGATIVE,
    }


# ------------------------------------------------- route-to-remedy (S0.2)

def remedy_mismatch(case):
    """Does the case's stated remedy aim at a bin that fired?

    Needs no denominator, which is why S0 lists it second. A remedy is
    declared with the bin it addresses; nothing is inferred from its
    prose.
    """
    r = case.get("remedy")
    if not r:
        return {"state": "NO_REMEDY_STATED", "aims_at": None,
                "fired": None, "mismatch": None}
    aims = r.get("addresses_bin")
    if aims is None:
        return {"state": "REMEDY_BIN_UNDECLARED", "aims_at": None,
                "fired": None, "mismatch": None}
    if aims not in BINS:
        raise SpecMismatch("remedy addresses %r, not a bin" % aims)
    c = classify(case)
    if not c["fires"]:
        # Third state, and it is not "no mismatch". A remedy aimed at a
        # bin on a case where NO bin fired is a remedy for a hazard the
        # record does not support -- which reads identically to a
        # correctly-aimed remedy if `mismatch` is a boolean over an
        # empty list. Found by running the report, not by reading it.
        return {"state": "NO_BIN_FIRED", "aims_at": aims,
                "fired": [], "mismatch": None}
    return {
        "state": "CHECKED",
        "aims_at": aims,
        "fired": c["fires"],
        "mismatch": aims not in c["fires"],
    }


# ---------------------------------------------------- the recursion (S0.3)

def recursion(case):
    """An issued recommendation not implemented IS bin 3, one level up.

    Checkable from recommendation status alone, with no denominator and
    no reading of the incident.
    """
    r = case.get("remedy") or {}
    st = r.get("status")
    if st is None:
        return {"state": "STATUS_UNRECORDED", "is_bin_3_again": None}
    if st not in ("IMPLEMENTED", "OPEN", "CLOSED_UNIMPLEMENTED",
                  "UNRECORDED"):
        raise SpecMismatch("remedy status %r not recognised" % st)
    if st == "UNRECORDED":
        return {"state": "STATUS_UNRECORDED", "is_bin_3_again": None}
    return {
        "state": st,
        "is_bin_3_again": st in ("OPEN", "CLOSED_UNIMPLEMENTED"),
        "reading": "a control conceived and not built, produced by the "
                   "process investigating controls conceived and not "
                   "built" if st != "IMPLEMENTED" else
                   "the remedy was built; the recursion does not apply",
    }


# --------------------------------------------------------------- S0 gate

def rate(*_a, **_k):
    """S0. Refused, not returned."""
    raise RateRefused(
        "A rate over a corpus selected on the outcome has no "
        "denominator. Every case in an incident-report corpus is a "
        "case where something happened, so the population of hazards "
        "carrying the same signature and no event is uncounted "
        "(generation-capacity R4). Run FORWARD mode instead: its "
        "frame is chosen before any outcome.")


# --------------------------------------------------------------- forward

def occupancy(systems):
    """FORWARD mode. Which bins currently hold, over systems chosen
    before any outcome. Counts of systems, never a probability."""
    out = {b: 0 for b in BINS}
    out[UNDERIVABLE] = 0
    unsearched = {k: 0 for k in SIGNALS}
    for s in systems:
        c = classify(s)
        for b in c["fires"]:
            out[b] += 1
        if not c["fires"]:
            out[c["primary"]] += 1
        for u in c["unsearched"]:
            unsearched[u] += 1
    return {
        "mode": "FORWARD",
        "n_systems": len(systems),
        "occupancy": out,
        "unsearched_signals": unsearched,
        "note": "counts of systems per bin. Not a probability, not a "
                "ranking, and not comparable to a retrospective count.",
    }


# ------------------------------------------------- one wired route
#
# The routes in S1 are DECLARED. This one is WIRED: a GAP_UNINSTRUMENTED
# case must name which of the eight exclusion mechanisms applies, and
# the vocabulary is IMPORTED from the register rather than copied, so
# the two cannot drift. The repo convention is to import (see
# msiaf-gdprf-bridge, reasoning-dial/gate_dial.py); five stale copies
# of one gate is what copying produced last time (MF_006, MF_011).

def _mechanisms():
    p = os.path.join(ROOT, "uninstrumented")
    if p not in sys.path:
        sys.path.insert(0, p)
    import uninstrumented as U
    return U.MECHANISMS


def gap_mechanism(case):
    """For a case that fires the GAP bin: which exclusion mechanism.

    Declared per case, validated against the register's own tuple.
    Nothing is inferred from prose -- deciding which mechanism a
    paragraph describes is a reading, and a word list doing it is
    nonidentity-census T1-1.
    """
    c = classify(case)
    if "GAP_UNINSTRUMENTED" not in c["fires"]:
        return {"state": "BIN_DID_NOT_FIRE", "mechanism": None}
    m = (case.get("gap") or {}).get("mechanism")
    if m is None:
        return {"state": "MECHANISM_UNDECLARED", "mechanism": None}
    known = _mechanisms()
    if m not in known:
        raise SpecMismatch(
            "gap mechanism %r is not in the register's vocabulary: %s"
            % (m, ", ".join(known)))
    return {"state": "DECLARED", "mechanism": m,
            "vocabulary_size": len(known),
            "source": "uninstrumented.MECHANISMS, imported"}


# ----------------------------------------------------------------- cases

def load_cases():
    if not os.path.isdir(CASEDIR):
        return []
    out = []
    for fn in sorted(os.listdir(CASEDIR)):
        if fn.endswith(".json"):
            with open(os.path.join(CASEDIR, fn), encoding="utf-8") as fh:
                d = json.load(fh)
            d.setdefault("id", fn[:-5])
            out.append(d)
    return out


def calibrate(cases=None):
    """Does the classifier reproduce the bin each case was BUILT to have?

    `truth` is set by how the case was authored and is never read by
    classify(). A case set that cannot produce a verdict cannot show
    the classifier discriminates on it, so coverage is reported too.
    """
    cases = load_cases() if cases is None else cases
    rows, agree = [], 0
    for c in cases:
        got = classify(c)
        want = c.get("truth")
        ok = (want == got["verdict"])
        agree += 1 if ok else 0
        rows.append({"id": c["id"], "built_as": want,
                     "classified": got["verdict"],
                     "primary": got["primary"],
                     "also": got["also"], "agree": ok})
    reachable = sorted(set(r["classified"] for r in rows))
    required = set(BINS) | {UNDERIVABLE, MULTIPLE}
    return {
        "rows": rows,
        "n": len(rows),
        "agree": agree,
        "verdicts_reached": reachable,
        "verdicts_never_reached": sorted(required - set(reachable)),
        "negative_reachable": NEGATIVE in reachable,
        "note": "agreement is over CONSTRUCTED cases whose bin is fixed "
                "by authoring. It says the classifier reads its own "
                "signals, and nothing about any real incident.",
    }


# ---------------------------------------------------------------- report

def wrap(t, w=66, ind="   "):
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
    o.append("INVESTIGATION SIM -- foreknowledge bins")
    o.append("CSB-style investigation across industrial, manufacturing")
    o.append("and infrastructure. SPEC.md is parsed, not restated.")
    o.append("")
    o += wrap("Every case here is CONSTRUCTED. Egress from this "
              "environment is an allowlist and every incident-report "
              "host is outside it, so nothing in this folder reads a "
              "real report or says anything about a real event.", ind="")
    o.append("")

    o.append("0. THE SELECTION TRAP")
    o += wrap("Every case in an incident-report corpus is a case where "
              "something happened, so a classifier run over one will "
              "find foreknowledge. rate() raises rather than returning "
              "a number. The mode that escapes it is FORWARD, whose "
              "frame is chosen before any outcome -- which is also the "
              "mode the tool is for.")
    o.append("")

    o.append("1. THE BINS")
    for b in BINS:
        o.append("     %-22s -> %s" % (b, ", ".join(ROUTES.get(b))
                                       or "(the negative)"))
    o.append("   not bins: %s" % ", ".join(NONBINS))
    o += wrap("NOT_DERIVABLE is not NOT_FORESEEN. One says look "
              "harder, the other says stop looking, and a scalar "
              "collapses them.")
    o.append("")

    cal = calibrate()
    o.append("1b. THE ONE WIRED ROUTE")
    o += wrap("The routes above are DECLARED. GAP_UNINSTRUMENTED is "
              "WIRED: a case firing it names which of the register's "
              "exclusion mechanisms applies, refusing anything outside "
              "that vocabulary, and the vocabulary is imported rather "
              "than copied so the two cannot drift.")
    for c in load_cases():
        g = gap_mechanism(c)
        if g["state"] != "BIN_DID_NOT_FIRE":
            o.append("     %-26s %-24s %s"
                     % (c["id"][:26], g["state"], g["mechanism"] or ""))
    o.append("   the other four routes are declared and not wired. That")
    o.append("   is the folder's largest open item and is IS_008.")
    o.append("")

    o.append("2. CALIBRATION -- constructed cases, bin fixed by authoring")
    o.append("   %-26s %-22s %-22s" % ("case", "built as", "classified"))
    for r in cal["rows"]:
        o.append("   %-26s %-22s %-22s %s"
                 % (r["id"][:26], r["built_as"], r["classified"],
                    "" if r["agree"] else "  <- DISAGREES"))
    o.append("   agree %d of %d" % (cal["agree"], cal["n"]))
    o.append("   verdicts reached      : %s"
             % ", ".join(cal["verdicts_reached"]))
    o.append("   never reached         : %s"
             % (", ".join(cal["verdicts_never_reached"]) or "none"))
    o.append("   the negative is reachable: %s" % cal["negative_reachable"])
    o += wrap("A classifier that never returns NOT_FORESEEN is telling "
              "the operator what they came to hear.")
    o.append("")

    o.append("3. ROUTE-TO-REMEDY MISMATCH -- no denominator required")
    for c in load_cases():
        m = remedy_mismatch(c)
        if m["state"] == "NO_BIN_FIRED":
            o.append("     %-26s aims at %-22s NO BIN FIRED -- the "
                     "remedy addresses a hazard the record does not "
                     "support" % (c["id"][:26], m["aims_at"]))
        elif m["state"] != "CHECKED":
            o.append("     %-26s %s" % (c["id"][:26], m["state"]))
        else:
            o.append("     %-26s aims at %-22s %s"
                     % (c["id"][:26], m["aims_at"],
                        "MISMATCH" if m["mismatch"] else "addresses a bin "
                        "that fired"))
    o.append("")

    o.append("4. THE RECURSION")
    for c in load_cases():
        r = recursion(c)
        o.append("     %-26s %-22s bin 3 again: %s"
                 % (c["id"][:26], r["state"],
                    "--" if r["is_bin_3_again"] is None
                    else r["is_bin_3_again"]))
    o += wrap("An issued recommendation that is not implemented is a "
              "control conceived and not built, produced by the process "
              "investigating controls conceived and not built.")
    o.append("")

    o.append("5. WHAT IS REFUSED")
    try:
        rate()
        o.append("     rate() RETURNED -- S0 is not implemented")
    except RateRefused as e:
        o += wrap("rate() raises: " + str(e))
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_bins
        return selftest_bins.run()
    if "--forward" in argv:
        p = argv[argv.index("--forward") + 1]
        print(json.dumps(occupancy(json.load(open(p))), indent=2))
        return 0
    if "--case" in argv:
        want = argv[argv.index("--case") + 1]
        for c in load_cases():
            if c["id"] == want:
                print(json.dumps({"classify": classify(c),
                                  "remedy": remedy_mismatch(c),
                                  "recursion": recursion(c)}, indent=2))
                return 0
        sys.stderr.write("no case %r; have: %s\n"
                         % (want, ", ".join(c["id"] for c in load_cases())))
        return 1
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
