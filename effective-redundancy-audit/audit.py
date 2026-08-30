#!/usr/bin/env python3
# audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# What can be established about this protocol without running the study.
#
# THE STUDY IS NOT RUN HERE, and the reason is not only egress. Three
# things block it, and the third is the load-bearing one:
#
#   1. the public investigation reports (CSB, NTSB, IAEA, FEMA, GAO)
#      refuse CONNECT from this environment -- measured below;
#   2. the design requires TWO human coders, independently, blind;
#   3. coding a real disaster's shared-node structure is a claim about a
#      real event with real dead people. Constructing a Case for
#      Fukushima or Katrina and asserting "N_eff = 1, that is why it
#      failed" would be a fabricated finding about a real disaster. The
#      author shipped ONE coded example (Kerr County, Section 5); this
#      file runs THAT -- reproduction of the author's coding, not new
#      coding -- and constructs no case of its own.
#
# So H1 vs H0 is UNVERIFIED here. What IS checkable is the delivered
# instrument: its arithmetic, and whether it computes what the protocol
# says to compute.

import io
import inspect
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import effective_redundancy as ER  # noqa: E402

# Measured 2026-08-29. Every source the protocol names in Section 3.1.
EGRESS = [
    ("www.csb.gov", "000", "CSB refinery/chemical reports"),
    ("www.ntsb.gov", "000", "NTSB transport reports"),
    ("www.iaea.org", "000", "IAEA/INPO nuclear reports"),
    ("www.fema.gov", "000", "FEMA after-action reports"),
    ("www.gao.gov", "000", "GAO reports"),
]


def _delivered_cases():
    """The Section 5 worked example, as the author shipped it. Imported
    with stdout suppressed so the delivered `report(cases)` call at the
    bottom of that file does not print here."""
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import worked_example
    return worked_example.cases


# -------------------------------------------------- the honest positive

FISHER_REFS = [
    ((3, 1, 1, 3), 0.4857, "tea-tasting 2x2"),
    ((8, 2, 1, 5), 0.03497, "a standard asymmetric 2x2"),
]


def fisher_is_correct():
    """The one thing the delivered stats code does, checked against two
    independently known values."""
    out = []
    for (a, b, c, d), ref, name in FISHER_REFS:
        got = ER.fisher_exact_2sided(a, b, c, d)
        out.append((name, (a, b, c, d), round(got, 5), ref,
                    abs(got - ref) < 5e-4))
    return out


# --------------------------------------------------------- THE FINDING

def kappa_is_omitted():
    """The protocol (Section 3.2) says 'Report the kappa first, always.'
    Section 3.4 makes kappa one of the two 'honest' theory-killers. The
    delivered report() does not compute it, and the Case data model
    cannot hold the two codings kappa needs.

    So the instrument ships without its own primary falsification guard,
    and cannot be given one without changing the data model."""
    rep = inspect.getsource(ER.report)
    case_fields = list(ER.Case.__dataclass_fields__)
    return {
        "cohen_kappa_defined": hasattr(ER, "cohen_kappa"),
        "report_calls_kappa": "cohen_kappa" in rep,
        "report_prints_kappa": "kappa" in rep.lower(),
        "case_holds_two_codings": "coder" in " ".join(case_fields).lower(),
        "case_fields": case_fields,
        "what_report_prints": [
            ln.split('"')[1].split(" ")[0] if '"' in ln else ln.strip()
            for ln in rep.splitlines() if "print(" in ln],
    }


def kappa_works_when_wired():
    """cohen_kappa itself is correct -- the omission is in the wiring,
    not the function. Perfect agreement -> 1.0, and a partial case is in
    range."""
    perfect = ER.cohen_kappa(list("AABB"), list("AABB"))
    partial = ER.cohen_kappa(list("yyynn"), list("yynnn"))
    return {"perfect": perfect, "partial": round(partial, 4),
            "correct": perfect == 1.0 and 0.0 <= partial <= 1.0}


# ------------------------------------------- reproduce the delivered coding

def worked_example_reproduces():
    """Known-answer check on the delivered code, using the delivered
    data. The prose states Kerr 2025 -> N_eff = 1 (failed) and the
    control -> N_eff = 2 (held). The code should agree."""
    cases = _delivered_cases()
    by = dict((c.name, c) for c in cases)
    k25 = by["Kerr County 2025"]
    k26 = by["Kerr County 2026"]
    return {
        "kerr2025_n_eff": k25.n_eff, "kerr2025_expected": 1,
        "kerr2026_n_eff": k26.n_eff, "kerr2026_expected": 2,
        "matches": k25.n_eff == 1 and k26.n_eff == 2,
        # prose says N_nominal ~4 (counts sirens, which 'did not exist');
        # the code counts channels only, so 3. The '~' hedges it and the
        # code is the more defensible count.
        "kerr2025_n_nominal_code": k25.n_nominal,
        "kerr2025_n_nominal_prose": "~4",
    }


# ------------------------------------------- the seed set is self-forbidden

def seed_set_degenerate():
    """The Section 6 seed outcomes, transcribed from the delivered table
    (LABELS ONLY -- no channel coding, which would be fabrication). The
    protocol says DO NOT TEST ON THESE (Section 6, circular) and DO NOT
    SAMPLE ON DISASTERS (Section 3.1). Both hold, and the second is
    provable from the outcome labels alone: 5 failed, 1 held, so the 2x2
    held column is n=1 and no test has power regardless of coding."""
    outcomes = ["failed", "failed", "failed", "failed", "failed", "held"]
    failed = outcomes.count("failed")
    held = outcomes.count("held")
    return {"n": len(outcomes), "failed": failed, "held": held,
            "held_column_n": held,
            "degenerate": held <= 1,
            "reason": "sampled on disasters (Section 3.1 forbids it); the "
                      "held column has n=%d, so cells c and d cannot both "
                      "be populated and no 2x2 test has power" % held}


# ---------------------------------------------------- a latent edge

def zero_channel_edge():
    """contingency() tests n_eff == 1 exactly. A case with no channels
    has n_eff = 0, so it is 'not collapsed' and a FAILED zero-channel
    case lands in cell b -- 'failed WITH real redundancy', a false
    counterexample. Minor (a zero-channel case is malformed input), but
    the exact-equality test has no guard for it."""
    z = ER.Case("empty", "x", "failed", set(), [])
    a, b, c, d = ER.contingency([z])
    return {"n_eff": z.n_eff, "lands_in_b": b == 1,
            "note": "n_eff=0 reads as 'has redundancy'; input needs a "
                    "channels-nonempty guard the code does not have"}


def render():
    out = []
    w = out.append
    w("EFFECTIVE REDUNDANCY AUDIT -- what holds without running the study")
    w("")
    w("The delivered code runs and is faithful. The STUDY does not run")
    w("here, for three reasons, the third load-bearing:")
    w("  1. every report source in Section 3.1 refuses CONNECT (below);")
    w("  2. the design calls for two human coders, blind;")
    w("  3. coding a real disaster's shared-node structure is a claim")
    w("     about a real event -- a fabricated Case for Fukushima or")
    w("     Katrina asserting 'N_eff=1, that is why it failed' would be a")
    w("     fabricated finding about a real disaster. Only the author's")
    w("     one delivered coding (Kerr County) is run; no case is coded")
    w("     here.")
    w("")

    w("0. THE REPORT SOURCES REFUSE CONNECT (measured)")
    for host, code, what in EGRESS:
        w("   %-16s %s   %s" % (host, code, what))
    w("")

    w("1. THE HONEST POSITIVE -- Fisher is numerically correct")
    for name, tbl, got, ref, ok in fisher_is_correct():
        w("   %-24s %s -> p=%s  (ref %s)  %s"
          % (name, tbl, got, ref, "OK" if ok else "MISMATCH"))
    w("   The one thing the delivered statistics do, they do right.")
    w("")

    w("2. THE FINDING -- THE PROTOCOL'S PRIMARY GUARD IS NOT COMPUTED")
    k = kappa_is_omitted()
    w("   Section 3.2: 'Report the kappa first, always.'")
    w("   Section 3.4: kappa is one of the two 'honest' theory-killers.")
    w("")
    w("   cohen_kappa defined:        %s" % k["cohen_kappa_defined"])
    w("   report() calls it:          %s" % k["report_calls_kappa"])
    w("   report() prints kappa:      %s" % k["report_prints_kappa"])
    w("   Case holds two codings:     %s" % k["case_holds_two_codings"])
    w("   Case fields:                %s" % ", ".join(k["case_fields"]))
    w("")
    w("   report() prints the 2x2, the counterexamples, Fisher, and the")
    w("   nominal averages -- and NOT the kappa the protocol says to report")
    w("   first. And it cannot: the Case data model holds ONE coding, so")
    w("   the two-coder blind protocol (Section 3.2) has no")
    w("   representation in the shipped code. cohen_kappa is defined and")
    w("   never called, over data that could not feed it.")
    kw = kappa_works_when_wired()
    w("   The function itself is correct (perfect agreement -> %s), so"
      % kw["perfect"])
    w("   the omission is in the wiring and the data model, not the math.")
    w("")

    w("3. WHY THAT IS LOAD-BEARING -- THE RECURSION BITES")
    w("   Section 7: 'Mode F is the audit itself ... the checker is a")
    w("   shared node.' This instrument is coded by humans against one")
    w("   reading of one report, so by its own Mode F it IS a shared")
    w("   node. Its only defense against being narrative-not-structure")
    w("   is kappa (Section 3.4 threat 3). That defense is exactly the")
    w("   number the delivered code omits. As shipped, the tool cannot")
    w("   detect the failure mode the protocol foregrounds as honest.")
    w("")

    w("4. THE WORKED EXAMPLE REPRODUCES THE STATED CODING")
    we = worked_example_reproduces()
    w("   Kerr County 2025  N_eff = %d  (prose: %d, failed)  %s"
      % (we["kerr2025_n_eff"], we["kerr2025_expected"],
         "match" if we["kerr2025_n_eff"] == 1 else "MISMATCH"))
    w("   Kerr County 2026  N_eff = %d  (prose: %d, held)    %s"
      % (we["kerr2026_n_eff"], we["kerr2026_expected"],
         "match" if we["kerr2026_n_eff"] == 2 else "MISMATCH"))
    w("   One discrepancy: the prose says N_nominal ~4 for 2025 (it")
    w("   counts sirens, which 'did not exist'); the code counts %d"
      % we["kerr2025_n_nominal_code"])
    w("   channels. The '~' hedges it and the code is the more")
    w("   defensible count.")
    w("")

    w("5. THE SEED SET IS SELF-FORBIDDEN AND DEGENERATE")
    s = seed_set_degenerate()
    w("   Section 6: 'DO NOT TEST ON THESE' (circular -- they built the")
    w("   hypothesis). And Section 3.1: 'DO NOT sample on disasters.'")
    w("   The seed outcomes (labels only, no channel coding): %d failed,"
      % s["failed"])
    w("   %d held. The 2x2 held column has n=%d, so no test has power"
      % (s["held"], s["held_column_n"]))
    w("   regardless of how the channels are coded -- provable from the")
    w("   delivered outcome labels alone. Sampling on disasters is the")
    w("   what Section 3.1 forbids, and the seed set is all disasters.")
    w("")

    w("6. A LATENT EDGE -- exact n_eff == 1 has no zero-channel guard")
    z = zero_channel_edge()
    w("   a failed case with no channels has n_eff = %d, so it lands in"
      % z["n_eff"])
    w("   cell b ('failed WITH real redundancy') -- a false")
    w("   counterexample. Minor: a zero-channel case is malformed input,")
    w("   and the code has no channels-nonempty guard.")
    w("")

    w("7. WHAT THIS FOLDER DOES NOT ESTABLISH")
    w("   Whether N_eff separates failed from held (H1) vs not (H0). That")
    w("   is the whole study, and it takes 8-15 EXPOSURE-sampled cases")
    w("   coded blind by two coders from public reports -- reports")
    w("   unreachable, coders absent, and not fabricated here. The")
    w("   protocol's own verdict conditions (Section 3.4) are untouched")
    w("   in either direction.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that exercise "
            "it live in selftest_er.py.\n"
            "    python3 effective-redundancy-audit/selftest_er.py\n")
        sys.exit(2)
    print(render())
