#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
asymmetry.py - does the revision direction ever cost the reviser.

    python3 asymmetry.py [--selftest]

Marker under exploration. Delivered spec: SPEC_CITATION.md, also PREAMBLE.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE TEST, AS DELIVERED. "Refutations of older work land as 'they were
uninformed.' They do not land as 'we may be measuring a different object.'
Check whether the revision direction ever costs the reviser. If it never
does, the revision is a routing rule."

That is a tally, so it is run as one. Each row: what was revised, which way it
moved, whether the move cost the party making it, and how it was FRAMED --
UNINFORMED (the earlier party was wrong) or DIFFERENT_OBJECT (the referent
moved between measurement and use).

TWO POPULATIONS, AND THE SPEC IS ABOUT THE SECOND. Revising your own work in
progress and revising a predecessor's are different objects, and only the
second carries the asymmetry the spec describes -- a field's treatment of the
people who came before it. This session's record holds mostly the first. Both
are logged, counted apart, and the routing-rule test is applied only to the
population it is a test of. Running it over self-revision would produce a
number about a different thing.

THE LEDGER IS SELF-ASSESSED, WHICH IS THE WEAKEST POSSIBLE INSTRUMENT FOR
THIS. Whether a revision cost the reviser is judged here by the reviser. A
party motivated to look even-handed would produce exactly this ledger, and
nothing inside it distinguishes the two cases. What the rows carry instead is
a commit or a location, so an outside reader can check each one. That is the
only defence available and it is not the same as an outside assessment.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

COST = ("COST", "FREE", "CONTESTED", "UNASSESSED")
FRAME = ("UNINFORMED", "DIFFERENT_OBJECT", "SELF_ATTRIBUTED", "UNASSESSED")
POPULATION = ("SELF_REVISION", "PREDECESSOR_REVISION")


class LedgerError(Exception):
    pass


class Revision(object):
    def __init__(self, what, direction, cost, frame, population, evidence,
                 assessed_by, note=None):
        if cost not in COST:
            raise LedgerError("cost must be one of %s" % (COST,))
        if frame not in FRAME:
            raise LedgerError("frame must be one of %s" % (FRAME,))
        if population not in POPULATION:
            raise LedgerError("population must be one of %s" % (POPULATION,))
        if not evidence:
            raise LedgerError(
                "a revision row carries a commit or a location. Without one "
                "the ledger is a self-report nobody can check, and a "
                "self-report is exactly what this ledger cannot be trusted "
                "to be")
        if not assessed_by:
            raise LedgerError("a row records who judged the cost")
        self.what = what
        self.direction = direction
        self.cost = cost
        self.frame = frame
        self.population = population
        self.evidence = evidence
        self.assessed_by = assessed_by
        self.note = note

    def row(self):
        return {"what": self.what, "direction": self.direction,
                "cost": self.cost, "frame": self.frame,
                "population": self.population, "evidence": self.evidence,
                "assessed_by": self.assessed_by, "note": self.note}


SELF = "self-assessed by the reviser"

LEDGER = [
    Revision(
        what="MIN_COVERAGE added to the matcher after a false DROPPED",
        direction="drop rate 0.09 -> 0.00; the one DROPPED became "
                  "UNSCORABLE_COVERAGE",
        cost="CONTESTED",
        frame="SELF_ATTRIBUTED",
        population="SELF_REVISION",
        evidence="7eac4ad, handoff-provenance/diff.py",
        assessed_by=SELF,
        note="removed the module's only reportable drop rate, which is a "
             "finding lost; and it moved the headline toward a cleaner "
             "channel. Both directions are real and this row does not pick"),
    Revision(
        what="NEGATED state added; a CARRIED at share 1.00 was refused",
        direction="one CARRIED removed from the count",
        cost="COST",
        frame="SELF_ATTRIBUTED",
        population="SELF_REVISION",
        evidence="7eac4ad, handoff-provenance diff.match()",
        assessed_by=SELF,
        note="the entry had scored at the matcher's maximum; refusing it "
             "removed a favourable data point"),
    Revision(
        what="implementation_surface() strips prose before matching",
        direction="CARRIED became harder to earn; a docstring no longer "
                  "counts",
        cost="COST",
        frame="SELF_ATTRIBUTED",
        population="SELF_REVISION",
        evidence="7eac4ad, handoff-provenance/diff.py",
        assessed_by=SELF),
    Revision(
        what="word boundary added to the term-collision scanner",
        direction="8 reported hits -> 3",
        cost="COST",
        frame="SELF_ATTRIBUTED",
        population="SELF_REVISION",
        evidence="00855d4, tools/check_term_collision.py",
        assessed_by=SELF,
        note="shrank this work's own reported finding count by five"),
    Revision(
        what="N-body 'reproduction' in SCALING_CLASSES marked "
             "CONSTRUCTION_FITTED, attributing the deficiency to the source",
        direction="the source's figure was treated as not independently "
                  "reproduced",
        cost="FREE",
        frame="UNINFORMED",
        population="PREDECESSOR_REVISION",
        evidence="4491ecc then de5a3bd (correction H1)",
        assessed_by=SELF,
        note="THE CORRECT READING WAS DIFFERENT_OBJECT. The term was "
             "printed in the source label and lost in transfer; retagged "
             "LABEL_TRUNCATED_IN_TRANSFER. The revision landed as 'the "
             "source was deficient' when the object had changed between "
             "measurement and use, it cost nothing until an outside party "
             "caught it, and the outside party was the operator"),
]


def rows(population=None):
    return [r.row() for r in LEDGER
            if population is None or r.population == population]


def counts(population=None):
    out = dict((c, 0) for c in COST)
    for r in rows(population):
        out[r["cost"]] += 1
    return out


def frames(population=None):
    out = dict((f, 0) for f in FRAME)
    for r in rows(population):
        out[r["frame"]] += 1
    return out


def routing_rule_test():
    """Applied ONLY to predecessor revisions, which is what it is a test of.

    "If it never does, the revision is a routing rule." Never is the
    condition, so a single COST row falsifies it -- and with n this small,
    failing to find one is not evidence of the rule either.
    """
    pred = rows("PREDECESSOR_REVISION")
    costing = [r for r in pred if r["cost"] == "COST"]
    n = len(pred)
    if n == 0:
        return {"n": 0, "n_costing": 0, "verdict": None,
                "state": "NO_POPULATION",
                "why": "no predecessor revisions in this ledger. The test "
                       "is about how a party treats work that came before "
                       "it, and self-revision is a different object"}
    verdict = "ROUTING_RULE" if not costing else "NOT_A_ROUTING_RULE"
    return {"n": n, "n_costing": len(costing),
            "verdict": verdict,
            "state": "COMPUTED_AT_TINY_N",
            "why": "one row. 'Never' is falsified by a single counterexample "
                   "and confirmed by nothing, so a ROUTING_RULE verdict off "
                   "n=1 is a description of one revision and not a finding "
                   "about a practice"}


def contrast():
    """The two populations, side by side. The contrast is the readout."""
    s, p = counts("SELF_REVISION"), counts("PREDECESSOR_REVISION")
    ns = sum(s.values()) or 1
    npd = sum(p.values()) or 1
    return {"self": s, "predecessor": p,
            "self_cost_share": s["COST"] / ns,
            "predecessor_cost_share": p["COST"] / npd,
            "n_self": sum(s.values()), "n_predecessor": sum(p.values()),
            "shape_matches_the_spec": (s["COST"] > 0 and p["COST"] == 0),
            "why": "the contrast is the shape the spec describes and the "
                   "sample size establishes nothing. One predecessor "
                   "revision is an anecdote about one revision"}


def confidence():
    return {"assessment": "self-assessed by the reviser, which is the "
                          "weakest instrument available for this question. "
                          "A party motivated to look even-handed produces "
                          "this same ledger",
            "defence": "every row carries a commit or a location, so an "
                       "outside reader can check it. That is not an outside "
                       "assessment",
            "n_predecessor": "one. The routing-rule test runs on it and the "
                             "verdict is a description of that one revision",
            "completeness": "the rows are the revisions the reviser "
                            "remembered and chose to log. A revision that "
                            "went unnoticed is not here, and going "
                            "unnoticed is what a free revision does",
            "resolved": False}


def breaks():
    return [
        "THE ONE PREDECESSOR REVISION IN THIS LEDGER COST NOTHING AND WAS "
        "FRAMED AS 'THEY WERE DEFICIENT', WHICH IS THE ASYMMETRY THE SPEC "
        "DESCRIBES. The N-body figure in SCALING_CLASSES was marked "
        "CONSTRUCTION_FITTED against the source. The correct reading was "
        "DIFFERENT_OBJECT -- the term was printed in the source label and "
        "lost in transfer -- and it was the operator who caught it, not the "
        "reviser. Meanwhile all four self-revisions in the same session cost "
        "the reviser something. The contrast is the shape the spec names",
        "AND n=1 ESTABLISHES NOTHING. The routing-rule verdict runs over a "
        "single predecessor revision. 'Never costs' is falsified by one "
        "counterexample and confirmed by no number of non-counterexamples, "
        "so ROUTING_RULE here is a description of one revision, not a "
        "property of a practice. The contrast between the two populations is "
        "4 rows against 1",
        "THE LEDGER IS ASSESSED BY THE PARTY IT IS ABOUT AND NOTHING INSIDE "
        "IT FIXES THAT. Whether a revision cost the reviser is judged here "
        "by the reviser, and a reviser wanting to look even-handed would "
        "produce a ledger that looks like this one -- self-revisions costing, "
        "the awkward row disclosed. The commits are the only check, and "
        "checking them requires someone else",
        "THE ROWS ARE THE REVISIONS THE REVISER NOTICED. A revision that "
        "cost nothing and drew no correction leaves no trace to log, so the "
        "sampling is biased toward exactly the rows that got caught. The one "
        "FREE row is here because the operator objected; a FREE revision "
        "nobody objected to would not have been written down",
        "'COST' IS NOT DEFINED IN A UNIT. The column records a judgement "
        "that a revision moved against the reviser's interest, with no scale "
        "and no way to compare two rows. CONTESTED exists because one row "
        "moved both ways at once and forcing it either way would have been "
        "a number invented to complete a table",
    ]


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def report():
    L = ["REVISION ASYMMETRY -- does the direction ever cost the reviser",
         "=" * 72, ""]
    L.append("  'Refutations of older work land as they were uninformed.")
    L.append("   They do not land as we may be measuring a different")
    L.append("   object. Check whether the revision direction ever costs")
    L.append("   the reviser. If it never does, the revision is a routing")
    L.append("   rule.'")
    L.append("")
    L.append("  Two populations. Only the second is what the test is of.")
    L.append("")
    for pop in POPULATION:
        rs = rows(pop)
        L.append("-" * 72)
        L.append("")
        L.append("  %s  (%d)" % (pop, len(rs)))
        L.append("")
        for r in rs:
            L.append("    %-10s %-18s" % (r["cost"], r["frame"]))
            L.append("      %s" % r["evidence"])
            for line in _wrap(r["what"], "      "):
                L.append(line)
            for line in _wrap("-> " + r["direction"], "        "):
                L.append(line)
            if r["note"]:
                for line in _wrap(r["note"], "        "):
                    L.append(line)
            L.append("")
        c = counts(pop)
        L.append("    %s" % ", ".join("%s=%d" % (k, v)
                                      for k, v in sorted(c.items()) if v))
        L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE CONTRAST")
    L.append("")
    ct = contrast()
    L.append("    %-26s %-10s %s" % ("", "n", "COST"))
    L.append("    %-26s %-10d %d"
             % ("own work, in progress", ct["n_self"], ct["self"]["COST"]))
    L.append("    %-26s %-10d %d"
             % ("someone else's, earlier", ct["n_predecessor"],
                ct["predecessor"]["COST"]))
    L.append("")
    L.append("    matches the spec's shape: %s"
             % ct["shape_matches_the_spec"])
    L.append("")
    for line in _wrap(ct["why"], "    "):
        L.append(line)
    L.append("")
    rr = routing_rule_test()
    L.append("    routing-rule test (predecessor population only)")
    L.append("      n = %d, costing = %d" % (rr["n"], rr["n_costing"]))
    L.append("      verdict: %s   state: %s" % (rr["verdict"], rr["state"]))
    for line in _wrap(rr["why"], "      "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    try:
        Revision("w", "d", "COST", "UNINFORMED", "SELF_REVISION", "",
                 assessed_by="me")
        ok = False
    except LedgerError:
        ok = True
    ck("a row without a commit or location is refused -- an uncheckable "
       "self-report is what this ledger cannot be", ok)
    try:
        Revision("w", "d", "COST", "UNINFORMED", "SELF_REVISION", "abc123",
                 assessed_by=None)
        ok = False
    except LedgerError:
        ok = True
    ck("a row records who judged the cost", ok)
    ck("every shipped row carries evidence",
       all(r["evidence"] for r in rows()))
    ck("and every one is marked self-assessed",
       all("self-assessed" in r["assessed_by"] for r in rows()))

    ck("the two populations are counted apart",
       len(rows("SELF_REVISION")) == 4
       and len(rows("PREDECESSOR_REVISION")) == 1)
    ck("every self-revision cost the reviser or is contested; none was free",
       counts("SELF_REVISION")["FREE"] == 0
       and counts("SELF_REVISION")["COST"] == 3)
    ck("the single predecessor revision cost nothing",
       counts("PREDECESSOR_REVISION")["COST"] == 0
       and counts("PREDECESSOR_REVISION")["FREE"] == 1)
    ck("and it was framed UNINFORMED, not DIFFERENT_OBJECT",
       frames("PREDECESSOR_REVISION")["UNINFORMED"] == 1
       and frames("PREDECESSOR_REVISION")["DIFFERENT_OBJECT"] == 0)
    ck("which is the asymmetry the spec describes",
       contrast()["shape_matches_the_spec"] is True)
    ck("and the correct reading is recorded in the row itself",
       any("THE CORRECT READING WAS DIFFERENT_OBJECT" in (r["note"] or "")
           for r in rows("PREDECESSOR_REVISION")))
    ck("caught by an outside party, not the reviser",
       any("the outside party was the operator" in (r["note"] or "")
           for r in rows("PREDECESSOR_REVISION")))

    rr = routing_rule_test()
    ck("the routing-rule test runs only on the predecessor population",
       rr["n"] == 1)
    ck("and reports the tiny n in its state rather than in prose only",
       rr["state"] == "COMPUTED_AT_TINY_N")
    empty = routing_rule_test.__doc__
    ck("a single COST row would falsify 'never', and the docstring says so",
       "falsifies" in empty)

    ck("CONTESTED exists so a two-way row is not forced", "CONTESTED" in COST)
    ck("and one row uses it",
       counts()["CONTESTED"] == 1)

    ck("the awkward predecessor row leads the breaks list",
       "COST NOTHING AND WAS" in breaks()[0])
    ck("n=1 establishing nothing is the second break",
       "n=1 ESTABLISHES NOTHING" in breaks()[1])
    ck("self-assessment being the weak point is disclosed",
       any("ASSESSED BY THE PARTY IT IS ABOUT" in b for b in breaks()))
    ck("the sampling bias toward caught revisions is disclosed",
       any("would not have been written down" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE CONTRAST" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="revision asymmetry")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
