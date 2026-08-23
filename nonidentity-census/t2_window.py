# SPDX-License-Identifier: CC0-1.0
"""
T2, replacement output -- DISSOLUTION WINDOWS (BOUNDARY.md D7).

Proposal, relayed by the operator after D6 had run:

    Every claim gets a window at which its main term stops reading as a
    thing. population: months to years, and it dissolves at generational
    rate. firm: quarters. market: the window it's priced at. The output is
    a distribution of windows across a field, not a count of identity vs
    non-identity papers. One thing it needs that the word-list version
    didn't: the window has to come from the claim's own measurement
    interval -- sampling frequency, follow-up period, the units on the
    x-axis. Which is recoverable from methods sections, not abstracts.

WHAT THIS MODULE ACCEPTS. The first half. Identity-bearing-ness is
scale-relative, so the output is a distribution and not a count, and the
whole D3 table dissolves because every term becomes claim-level the way
D2 argued only `market` was. It also moves the discriminator off the
single-reader judgement D6 put it on, which is D6's stated cost.

WHAT THIS MODULE SPLITS. The second half names ONE window and the proposal
uses TWO:

    W_dissolve   the timescale at which the term stops denoting a
                 persistent individuated thing. A property of the world and
                 the concept. `population ... dissolves at generational
                 rate` is this one.

    W_measure    sampling frequency, follow-up period, x-axis units. A
                 property of the study. `market: the window it's priced at`
                 is this one, and `firm: quarters` is a reporting interval,
                 so it is this one too.

Two of the proposal's three worked examples are `W_measure` and one is
`W_dissolve`. The requirement -- "the window has to come from the claim's
own measurement interval" -- is that conflation stated as a rule.

WHY THE SPLIT IS NOT PEDANTRY. Reading W_dissolve off W_measure assumes they
coincide, and the case where they do not is the informative one. A study
sampling firms quarterly, whose unit dissolves at decades, is resolving well
inside its term's stable regime; a study sampling at the dissolution scale
could have watched the term come apart and did not report it. The ratio says
which, per claim:

    W_measure / W_dissolve   >= margin   the study is too coarse to have
                                         seen the term dissolve. The
                                         identity framing could not have
                                         failed at this resolution.
                             <= 1/margin the study resolves well inside the
                                         stable regime; the framing is
                                         licensed by the apparatus.

That is `reasoning-gate`'s G-RES pair -- instrument resolution against the
feature being resolved -- and the same shape as
`uninstrumented/coupling_audit/provisioning.py`, where bone collagen is
12.2x too coarse for a seasonal feature so the coupling hypothesis cannot
fail in that tissue.

THE OTHER READING, AND WHY IT IS NOT BUILT. The proposal can be read as
defining the window scale-relatively: the term as used in THIS paper, so
W = W_measure by construction. That reading is coherent and it makes the
instrument incapable of failing -- every claim satisfies it, and a paper
sampling at the wrong scale for its own unit is undetectable. `MF_020`'s
shape. Both readings are stated; the two-number one is built because it can
return a negative.

WHAT IT DOES AND DOES NOT UNBLOCK. It removes T2's BULK requirement -- no
citation API, no stratified thousands. It adds a DEPTH requirement: methods
sections, which are behind more paywalls than abstracts, not fewer. Net, T2
becomes runnable by hand at small n and remains not runnable at the
eight-field stratified scale the work order specifies. A scope change, not
an unblocking.

EVERY NUMBER IN THE SEED IS STIPULATED. No methods section was read. The
seed is the proposal's own three examples plus their classification. Values
carry `[STIPULATED]` and `stipulated()` refuses to let them into a
distribution report unless the caller passes `allow_stipulated=True`, which
prints a banner.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import sys

SECOND = 1.0
MINUTE = 60.0
HOUR = 3600.0
DAY = 86400.0
WEEK = 7 * DAY
MONTH = 30.4375 * DAY
QUARTER = 3 * MONTH
YEAR = 365.25 * DAY
DECADE = 10 * YEAR

UNITS = {"second": SECOND, "seconds": SECOND, "minute": MINUTE,
         "minutes": MINUTE, "hour": HOUR, "hours": HOUR, "day": DAY,
         "days": DAY, "week": WEEK, "weeks": WEEK, "month": MONTH,
         "months": MONTH, "quarter": QUARTER, "quarters": QUARTER,
         "year": YEAR, "years": YEAR, "decade": DECADE, "decades": DECADE}

# `generation` is not a unit until a referent is named. The proposal's own
# `dissolves at generational rate` names none. The spread is computed from
# this table rather than asserted -- `--selftest` checks the number the
# error message quotes against the table it is quoting.
GENERATION_REFERENT = {
    "human": 25 * YEAR,
    "cattle": 5 * YEAR,
    "drosophila": 12 * DAY,
    "e_coli": 20 * MINUTE,
}

def generation_spread():
    """Ratio between the longest and shortest referent generation."""
    vals = list(GENERATION_REFERENT.values())
    return max(vals) / min(vals)


def generation_spread_text():
    import math
    r = generation_spread()
    return "a factor of %.0f, %.2f orders of magnitude" % (
        r, math.log10(r))


W_DISSOLVE = "W_dissolve"
W_MEASURE = "W_measure"
KINDS = (W_DISSOLVE, W_MEASURE)

STIPULATED = "STIPULATED"
FROM_SOURCE = "FROM_SOURCE"
NOT_LOCATED = "NOT_LOCATED"      # looked, did not find
UNBOUNDED = "UNBOUNDED"          # located, and the term does not dissolve
PROVENANCE = (STIPULATED, FROM_SOURCE, NOT_LOCATED, UNBOUNDED)

MARGIN = 2.0   # G-RES margin. Declared, not tuned. See T2-7.


class WindowGateError(Exception):
    """Raised rather than guessing a missing or unlike-unit number."""


def window(value, unit, kind, provenance, basis, referent=None):
    """
    One window. `value`/`unit` may be None only when provenance is
    NOT_LOCATED or UNBOUNDED -- the two states are kept apart because a
    term nobody looked up and a term that does not dissolve are different
    findings.
    """
    if kind not in KINDS:
        raise ValueError("kind must be one of %r, got %r" % (KINDS, kind))
    if provenance not in PROVENANCE:
        raise ValueError("provenance must be one of %r, got %r"
                         % (PROVENANCE, provenance))
    if provenance in (NOT_LOCATED, UNBOUNDED):
        if value is not None:
            raise ValueError("%s carries no value; got %r"
                             % (provenance, value))
        seconds = None
    elif unit == "generation":
        if referent is None:
            raise WindowGateError(
                "`generation` is not a unit until a referent is named. "
                "The referents in this table span %s, and the proposal's "
                "`generational rate` names none of them."
                % generation_spread_text())
        if referent not in GENERATION_REFERENT:
            raise WindowGateError("unknown generation referent %r; known: %r"
                                  % (referent, sorted(GENERATION_REFERENT)))
        seconds = float(value) * GENERATION_REFERENT[referent]
    else:
        if unit not in UNITS:
            raise WindowGateError("unknown unit %r; known: %r"
                                  % (unit, sorted(set(UNITS))))
        seconds = float(value) * UNITS[unit]
    if not basis:
        raise WindowGateError(
            "every window states where it came from. A number with no "
            "basis is the thing this module exists to stop.")
    return {"value": value, "unit": unit, "kind": kind,
            "provenance": provenance, "basis": basis,
            "referent": referent, "seconds": seconds}


def claim(cid, term, field, w_dissolve, w_measure, note=None):
    if w_dissolve["kind"] != W_DISSOLVE:
        raise ValueError("%s: first window must be %s" % (cid, W_DISSOLVE))
    if w_measure["kind"] != W_MEASURE:
        raise ValueError("%s: second window must be %s" % (cid, W_MEASURE))
    return {"id": cid, "term": term, "field": field,
            "w_dissolve": w_dissolve, "w_measure": w_measure, "note": note}


TOO_COARSE = "CANNOT_HAVE_SEEN_IT"
RESOLVES = "RESOLVES_IT"
MARGINAL = "MARGINAL"
UNDECIDABLE = "UNDECIDABLE"


def verdict(c, margin=MARGIN):
    """
    G-RES pair. Returns the verdict, the ratio, and why. Never returns a
    number when either window is missing.
    """
    d, m = c["w_dissolve"], c["w_measure"]
    if d["provenance"] == UNBOUNDED:
        return {"verdict": UNDECIDABLE, "ratio": None,
                "why": "the term is recorded as not dissolving; a ratio "
                       "against an unbounded window has no value"}
    if d["seconds"] is None or m["seconds"] is None:
        missing = []
        if d["seconds"] is None:
            missing.append("W_dissolve (%s)" % d["provenance"])
        if m["seconds"] is None:
            missing.append("W_measure (%s)" % m["provenance"])
        return {"verdict": UNDECIDABLE, "ratio": None,
                "why": "missing: " + ", ".join(missing)}
    r = m["seconds"] / d["seconds"]
    if r >= margin:
        v, why = TOO_COARSE, ("sampling %.3gx the dissolution window; the "
                              "identity framing could not have failed at "
                              "this resolution" % r)
    elif r <= 1.0 / margin:
        v, why = RESOLVES, ("sampling %.3gx the dissolution window; well "
                            "inside the stable regime" % r)
    else:
        v, why = MARGINAL, ("ratio %.3g sits inside the declared margin of "
                            "%.3g either way" % (r, margin))
    return {"verdict": v, "ratio": r, "why": why}


# --------------------------------------------------------------------------
# Seed: the proposal's own three examples, classified. No methods section was
# read, so every value is STIPULATED and says so.
# --------------------------------------------------------------------------

PROPOSAL_EXAMPLES = [
    {"term": "population",
     "as_given": "months to years, and it dissolves at generational rate",
     "kind": W_DISSOLVE,
     "why": "names when the term stops denoting the same thing; a property "
            "of the world, not of a study"},
    {"term": "firm",
     "as_given": "quarters",
     "kind": W_MEASURE,
     "why": "a quarter is a reporting interval. Firms do not dissolve "
            "quarterly; they are observed quarterly"},
    {"term": "market",
     "as_given": "the window it's priced at",
     "kind": W_MEASURE,
     "why": "stated as a measurement interval in the proposal's own words"},
]

SEED = [
    claim("P-1", "population", "ecology",
          window(1, "generation", W_DISSOLVE, STIPULATED,
                 "the proposal's `dissolves at generational rate`, with a "
                 "referent supplied here because the proposal names none",
                 referent="human"),
          window(1, "year", W_MEASURE, STIPULATED,
                 "annual census, the common interval in the field. Not read "
                 "from any methods section"),
          note="the one proposal example that is a dissolution window"),
    claim("P-2", "firm", "economics",
          window(NOT_LOCATED and None, None, W_DISSOLVE, NOT_LOCATED,
                 "the proposal gives `quarters`, which is a reporting "
                 "interval; no dissolution window was given or located"),
          window(1, "quarter", W_MEASURE, STIPULATED,
                 "the proposal's `quarters`, read as the reporting interval "
                 "it is"),
          note="proposal example reclassified; W_dissolve left NOT_LOCATED "
               "rather than back-filled from the interval"),
    claim("P-3", "market", "economics",
          window(None, None, W_DISSOLVE, NOT_LOCATED,
                 "the proposal defines this one as a measurement interval "
                 "outright"),
          window(1, "day", W_MEASURE, STIPULATED,
                 "`the window it's priced at`, taken as daily close. The "
                 "proposal does not fix a number"),
          note="the conflation in its clearest form: the example is stated "
               "wholly in W_measure"),
]

# Known-truth pair, constructed so the verdicts must separate.
NULL_PAIR = [
    claim("N-coarse", "cohort", "constructed",
          window(1, "year", W_DISSOLVE, STIPULATED, "constructed"),
          window(20, "years", W_MEASURE, STIPULATED, "constructed"),
          note="W_measure 20x W_dissolve; must read CANNOT_HAVE_SEEN_IT"),
    claim("N-fine", "cohort", "constructed",
          window(20, "years", W_DISSOLVE, STIPULATED, "constructed"),
          window(1, "year", W_MEASURE, STIPULATED, "constructed"),
          note="W_measure 1/20 W_dissolve; must read RESOLVES_IT"),
]


def stipulated(claims):
    return [c for c in claims
            if STIPULATED in (c["w_dissolve"]["provenance"],
                              c["w_measure"]["provenance"])]


def distribution(claims, allow_stipulated=False):
    """Per-field verdict distribution. Refuses stipulated input by default."""
    stip = stipulated(claims)
    if stip and not allow_stipulated:
        raise WindowGateError(
            "%d of %d claims carry a STIPULATED window and no methods "
            "section was read. Pass allow_stipulated=True to see the shape "
            "of the report; do not quote the numbers."
            % (len(stip), len(claims)))
    if stip:
        print("!! %d of %d windows are STIPULATED. This is the report's "
              "SHAPE, not a result." % (len(stip), len(claims)))
    out = {}
    for c in claims:
        v = verdict(c)
        f = out.setdefault(c["field"], {TOO_COARSE: 0, RESOLVES: 0,
                                        MARGINAL: 0, UNDECIDABLE: 0,
                                        "n": 0, "ratios": []})
        f[v["verdict"]] += 1
        f["n"] += 1
        if v["ratio"] is not None:
            f["ratios"].append(v["ratio"])
    return out


def render(dist):
    print("%-14s %4s %8s %8s %8s %8s   %s"
          % ("field", "n", "coarse", "resolves", "marginal", "undec",
             "ratios"))
    for f in sorted(dist):
        d = dist[f]
        rs = ", ".join("%.3g" % r for r in d["ratios"]) or "--"
        print("%-14s %4d %8d %8d %8d %8d   %s"
              % (f, d["n"], d[TOO_COARSE], d[RESOLVES], d[MARGINAL],
                 d[UNDECIDABLE], rs))


def classify_proposal():
    print("The proposal's three worked examples, classified\n")
    for e in PROPOSAL_EXAMPLES:
        print("  %-11s %-14s %s" % (e["term"], e["kind"], e["as_given"]))
        print("              %s" % e["why"])
    kinds = [e["kind"] for e in PROPOSAL_EXAMPLES]
    print("\n  W_dissolve %d of %d   W_measure %d of %d"
          % (kinds.count(W_DISSOLVE), len(kinds),
             kinds.count(W_MEASURE), len(kinds)))


def selftest():
    fails = []
    try:
        window(1, "generation", W_DISSOLVE, STIPULATED, "x")
        fails.append("`generation` must be refused without a referent")
    except WindowGateError as ex:
        import math
        want = "%.2f orders" % math.log10(generation_spread())
        if want not in str(ex):
            fails.append("the generation-spread figure in the error message "
                         "does not match the table it quotes: %r" % want)
    try:
        window(1, "year", W_DISSOLVE, STIPULATED, "")
        fails.append("a window with no basis must be refused")
    except WindowGateError:
        pass
    try:
        window(1, "fortnight", W_DISSOLVE, STIPULATED, "x")
        fails.append("an unknown unit must be refused, not coerced")
    except WindowGateError:
        pass
    try:
        window(5, None, W_DISSOLVE, NOT_LOCATED, "x")
        fails.append("NOT_LOCATED must carry no value")
    except ValueError:
        pass
    vc = verdict(NULL_PAIR[0])
    vf = verdict(NULL_PAIR[1])
    if vc["verdict"] != TOO_COARSE:
        fails.append("coarse control read %s" % vc["verdict"])
    if vf["verdict"] != RESOLVES:
        fails.append("fine control read %s" % vf["verdict"])
    if vc["verdict"] == vf["verdict"]:
        fails.append("the two controls do not separate")
    for c in SEED:
        v = verdict(c)
        if c["id"] in ("P-2", "P-3") and v["verdict"] != UNDECIDABLE:
            fails.append("%s must be UNDECIDABLE: its W_dissolve is "
                         "NOT_LOCATED and back-filling it from the "
                         "interval is the error under audit" % c["id"])
    try:
        distribution(SEED)
        fails.append("distribution() must refuse stipulated input by "
                     "default")
    except WindowGateError:
        pass
    kinds = [e["kind"] for e in PROPOSAL_EXAMPLES]
    if kinds.count(W_MEASURE) != 2 or kinds.count(W_DISSOLVE) != 1:
        fails.append("the proposal-example classification changed without "
                     "the finding being restated")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--proposal" in argv:
        classify_proposal()
        return 0
    if "--controls" in argv:
        print("constructed known-truth pair\n")
        for c in NULL_PAIR:
            v = verdict(c)
            print("  %-10s %-20s ratio=%s" % (c["id"], v["verdict"],
                  ("%.3g" % v["ratio"]) if v["ratio"] else "--"))
            print("             %s" % v["why"])
        return 0
    if "--seed" in argv:
        print("seed claims -- EVERY WINDOW STIPULATED, no methods section "
              "read\n")
        for c in SEED:
            v = verdict(c)
            print("  %-5s %-11s %-14s W_diss=%-12s W_meas=%s"
                  % (c["id"], c["term"], v["verdict"],
                     c["w_dissolve"]["provenance"],
                     c["w_measure"]["provenance"]))
            print("        %s" % v["why"])
        print()
        render(distribution(SEED, allow_stipulated=True))
        return 0
    print(__doc__.strip())
    print("\nusage: t2_window.py [--selftest | --proposal | --controls | "
          "--seed]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
