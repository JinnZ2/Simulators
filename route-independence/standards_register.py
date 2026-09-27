# SPDX-License-Identifier: CC0-1.0
"""standards_register.py -- FWO-10. One row per field whose OWN written standard
addresses single-channel or single-path dependency, and whether that field has
applied its standard to the monetary medium.

    python3 standards_register.py            the register and the applied-column verdict
    python3 standards_register.py --choices  every [CHOICE n] in force
    python3 test_single_channel.py           the checks; this module refuses --selftest

WHAT IS AND IS NOT HERE
    Every standard named below is CARRIED_FROM_MEMORY: no standards body, regulator
    or publisher host answers under the egress allowlist (probes recorded in
    SOURCES.md), so no row was read from its document.  A standard's NAME recalled
    from memory is a pointer, not a source; each row says so in `source`.
    The applied-to-the-medium column is UNKNOWN_NOT_SEARCHED on every seed row: the
    question is whether ANY document in the field applies the criterion to the
    medium, and that is a search over a corpus this session cannot reach.  A
    memory note ("none recalled") is carried per row and is an UNBOUNDED null --
    no corpus, no terms -- which is not NOT_APPLIED.  The order's expectation
    (NOT_APPLIED in all three rows) is therefore NOT_EVALUABLE here, not held.
    fail_fixture() supplies a row declared APPLIED so the all-NOT_APPLIED reading
    can be shown to fail once a real search fills the column.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import sys

APPLIED_STATES = ("APPLIED", "NOT_APPLIED", "UNKNOWN_NOT_SEARCHED")
SOURCE_KINDS = ("CARRIED_FROM_MEMORY", "READ", "VERIFIED", "CONSTRUCTED")

CHOICES = {
    1: "applied_to_medium takes APPLIED / NOT_APPLIED / UNKNOWN_NOT_SEARCHED; a memory note never fills it",
    2: "the verdict over the column is NOT_EVALUABLE if any row is UNKNOWN_NOT_SEARCHED; a partial column is not a column",
    3: "the plumbing/medium split on the prior-art rows is this session's reading, declared per row",
}


class RegisterError(ValueError):
    pass


def row(field, standard, requires, applied, source, memory_note="", inspector_note=""):
    if applied not in APPLIED_STATES:
        raise RegisterError("applied_to_medium must be one of %s; got %r" % (APPLIED_STATES, applied))
    if not any(source.startswith(k) for k in SOURCE_KINDS):
        raise RegisterError("source starts with one of %s" % (SOURCE_KINDS,))
    if source.startswith("CARRIED_FROM_MEMORY") and applied != "UNKNOWN_NOT_SEARCHED":
        raise RegisterError("%s: a row carried from memory cannot fill applied_to_medium [CHOICE 1]" % field)
    return {"field": field, "standard": standard, "requires": requires, "applied_to_medium": applied,
            "source": source, "memory_note": memory_note, "inspector_note": inspector_note}


def seed_rows():
    m = "CARRIED_FROM_MEMORY: the standard's name recalled; its text not read (egress allowlist)"
    return [
        row("structural engineering",
            "fracture-critical member designation and redundancy classification (US bridge practice; "
            "the federal bridge inspection standards); independent inspection at a fixed interval",
            "a second load path, or a mandated inspection regime where there is none",
            "UNKNOWN_NOT_SEARCHED", m,
            memory_note="none recalled; unbounded null",
            inspector_note="OBSERVED (carried from the operator): the inspector is paid through the same path "
                           "as the structure inspected"),
        row("negotiation / mediation / diplomacy",
            "durability of settlements; integrative bargaining over more than one dimension against single-dimension distributive bargaining",
            "more than one channel of exchange; the exchange expanded past one dimension",
            "UNKNOWN_NOT_SEARCHED", m, memory_note="none recalled; unbounded null"),
        row("ecology / agronomy",
            "genetic vulnerability of major crops (the 1972 US national committee report after the 1970 "
            "corn leaf blight); crop diversity requirements",
            "diversity at the dependency layer; no single genotype carrying the whole crop",
            "UNKNOWN_NOT_SEARCHED", m, memory_note="none recalled; unbounded null"),
        row("reliability engineering",
            "common-cause / common-mode failure treatment in functional-safety standards (beta-factor models)",
            "independence of redundant channels demonstrated, not assumed; a shared cause counted once",
            "UNKNOWN_NOT_SEARCHED", m, memory_note="none recalled; unbounded null"),
        row("power grid",
            "N-1 contingency criterion in transmission planning standards",
            "the system survives the loss of any single element",
            "UNKNOWN_NOT_SEARCHED", m, memory_note="none recalled; unbounded null"),
        row("aviation",
            "no single failure may prevent continued safe flight (transport-category airworthiness rules); "
            "dual / dissimilar systems",
            "no single point of failure for a catastrophic outcome; dissimilar redundancy where common-mode is credible",
            "UNKNOWN_NOT_SEARCHED", m, memory_note="none recalled; unbounded null"),
    ]


# Prior-art check the order asks for: has anyone applied a common-mode / N-1 criterion
# to a currency or payment system?  NOT_RUN at the document level.  What memory holds,
# with the plumbing/medium split declared per entry [CHOICE 3]:
PRIOR_ART = {
    "status": "NOT_RUN (egress allowlist); entries below CARRIED_FROM_MEMORY, unverified",
    "entries": [
        {"what": "principles for financial market infrastructures (international payment/settlement standards, 2012)",
         "addresses": "plumbing: operational continuity, business continuity, settlement finality of the SYSTEM",
         "medium": "not the medium; the unit the system settles in is taken as given"},
        {"what": "central-bank payment-system resilience and cyber-resilience guidance",
         "addresses": "plumbing: recovery-time objectives for the settlement system",
         "medium": "not the medium"},
        {"what": "payment-system exposure policies at central banks",
         "addresses": "plumbing: credit and liquidity exposure inside the settlement system",
         "medium": "not the medium"},
        {"what": "a common-mode / N-1 criterion applied to the currency itself as a dependency",
         "addresses": "NONE RECALLED",
         "medium": "unbounded null: no corpus searched"},
    ],
}


def applied_verdict(rows):
    states = [r["applied_to_medium"] for r in rows]
    if any(s == "UNKNOWN_NOT_SEARCHED" for s in states):
        return "NOT_EVALUABLE"                                            # [CHOICE 2]
    if all(s == "NOT_APPLIED" for s in states):
        return "ALL_NOT_APPLIED"
    return "SOME_APPLIED"


def fail_fixture():
    """CONSTRUCTED: a searched column with one APPLIED row, so ALL_NOT_APPLIED fails on it."""
    c = "CONSTRUCTED: fail fixture; no real standard"
    return [row("fixture field A", "fixture standard", "fixture requirement", "NOT_APPLIED", c),
            row("fixture field B", "fixture standard", "fixture requirement", "APPLIED", c)]


def check_expectations(rows):
    v = applied_verdict(rows)
    return [("E10.1 applied column reads NOT_APPLIED in every row",
             "MATCH" if v == "ALL_NOT_APPLIED" else ("NOT_EVALUABLE" if v == "NOT_EVALUABLE" else "MISMATCH"))]


def render(out=None):
    out = out or sys.stdout
    w = out.write
    rows = seed_rows()
    w("standards_register -- FWO-10; fields whose own written standard addresses single-path dependency\n")
    w("every standard CARRIED_FROM_MEMORY (name recalled, text not read); applied column UNKNOWN_NOT_SEARCHED on every row\n\n")
    for r in rows:
        w("== %s\n   standard:  %s\n   requires:  %s\n   applied to the medium: %s  (memory: %s)\n"
          % (r["field"], r["standard"], r["requires"], r["applied_to_medium"], r["memory_note"]))
        if r["inspector_note"]:
            w("   %s\n" % r["inspector_note"])
    w("\napplied-column verdict: %s\n" % applied_verdict(rows))
    for l, v in check_expectations(rows):
        w("expected %-60s %s\n" % (l, v))
    w("\nprior art (common-mode / N-1 on a currency or payment system): %s\n" % PRIOR_ART["status"])
    for e in PRIOR_ART["entries"]:
        w("   %s\n      addresses: %s\n      medium:    %s\n" % (e["what"], e["addresses"], e["medium"]))
    w("\nfail fixture (CONSTRUCTED, column searched, one APPLIED): %s\n" % check_expectations(fail_fixture())[0][1])
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
