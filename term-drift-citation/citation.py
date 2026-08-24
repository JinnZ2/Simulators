#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
citation.py - does a cited measurement still attach to the word carrying it.

    python3 citation.py [--selftest]

Marker under exploration. Delivered spec: SPEC_CITATION.md, also in
PREAMBLE.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

A citation carries a measurement forward under a word. It is valid only if the
word's referent held between the measurement and the use, and nothing in a
citation records whether it did. The three questions:

  1. What was the referent at time of measurement -- the object the study
     actually measured, not today's definition.
  2. What was load-bearing in it -- which element, if removed, makes the
     measured result not reproduce.
  3. Is that element present in the present-day object.

DOES_NOT_TRANSFER IS NOT REFUTED, AND THE TWO ARE HELD APART IN THE TYPE.
The spec says it in one line -- "the result may be correct and still not
attach" -- and that line is the whole reason this is a separate verdict rather
than a score. A citation that does not transfer says nothing about whether the
original measurement was right. `transfers()` returns a transfer verdict and a
SEPARATE `original_result` field that is never set by this module, because
nothing here measures the original.

ABSENCE OF RETEST IS NOT REFUTATION, AND SOMETIMES RETEST IS UNAVAILABLE.
The spec's LIMIT: some original objects are no longer instantiable. Testing
Holling's resilience needs a system with slack in it, and where slack has been
optimised away the original claim cannot be retested at all. So a case carries
a retest state -- NOT_RETESTED, NOT_INSTANTIABLE, RETESTED -- and none of them
is REFUTED. Folding NOT_INSTANTIABLE into "unsupported" would convert the
disappearance of the test bed into evidence against the claim.

A WORD IS NOT A MEASUREMENT, AND THIS MODULE DOES NOT DECIDE WHICH WORDS ARE.
A term without a quantity, a sign, or a formal definition in its field's
equations is not carrying a measurement, and must not be loaded. Whether a
given term has those is an assessment about a field, so the three fields
default to UNASSESSED and `carries_a_measurement()` refuses rather than
guessing. Same constraint as scope-bound-shapes' FROZEN list: an inferred
answer here would be the tool asserting something it did not check.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

TRANSFER = ("TRANSFERS", "DOES_NOT_TRANSFER", "UNASSESSED")
RETEST = ("RETESTED", "NOT_RETESTED", "NOT_INSTANTIABLE")
PRESENCE = ("PRESENT", "REMOVED", "UNASSESSED")


class CitationError(Exception):
    pass


class Citation(object):
    """One cited result, and the three questions asked of it."""

    def __init__(self, term, source, referent_at_measurement, load_bearing,
                 present_referent, load_bearing_now, status,
                 retest="NOT_RETESTED", declared_by=None, coexisting=False,
                 note=None):
        for name, val in (("referent_at_measurement", referent_at_measurement),
                          ("load_bearing", load_bearing),
                          ("present_referent", present_referent)):
            if not val:
                raise CitationError(
                    "%s is required. The check is three questions and a "
                    "citation missing one of the answers has not been "
                    "checked, which is a different state from having "
                    "passed" % name)
        if load_bearing_now not in PRESENCE:
            raise CitationError("load_bearing_now must be one of %s"
                                % (PRESENCE,))
        if retest not in RETEST:
            raise CitationError("retest must be one of %s" % (RETEST,))
        if not declared_by:
            raise CitationError(
                "a citation check records who answered the three questions. "
                "The answers are readings of a literature and a present-day "
                "object, and an unattributed reading is this module's guess")
        self.term = term
        self.source = source
        self.referent_at_measurement = referent_at_measurement
        self.load_bearing = list(load_bearing)
        self.present_referent = present_referent
        self.load_bearing_now = load_bearing_now
        self.status = status
        self.retest = retest
        self.declared_by = declared_by
        self.coexisting = coexisting
        self.note = note
        # A word is not a measurement. Nobody has assessed these.
        self.quantity = None
        self.sign = None
        self.formal_definition = None

    def transfers(self):
        """The verdict, with the original result held separately."""
        if self.load_bearing_now == "UNASSESSED":
            verdict = "UNASSESSED"
        elif self.load_bearing_now == "REMOVED":
            verdict = "DOES_NOT_TRANSFER"
        else:
            verdict = "TRANSFERS"
        return {
            "term": self.term,
            "source": self.source,
            "verdict": verdict,
            "load_bearing": self.load_bearing,
            "load_bearing_now": self.load_bearing_now,
            "coexisting_referents": self.coexisting,
            "retest": self.retest,
            # Never set here. Nothing in this module measures the original.
            "original_result": "NOT_ASSESSED_HERE",
            "why_original_is_separate":
                "the result may be correct and still not attach. A transfer "
                "verdict is about whether the measured object survived, not "
                "about whether the measurement was right",
            "why_retest_is_separate":
                "absence of retest is not refutation, and where the original "
                "object is no longer instantiable there is no retest to be "
                "absent from",
        }

    def carries_a_measurement(self):
        """REFUSED unless someone declared the three fields.

        A term without a quantity, a sign, or a formal definition in its
        field's equations is not carrying a measurement. Deciding that about
        a field is an assessment, so it is not made here.
        """
        fields = {"quantity": self.quantity, "sign": self.sign,
                  "formal_definition": self.formal_definition}
        if all(v is None for v in fields.values()):
            return {"verdict": None, "state": "UNASSESSED",
                    "fields": fields,
                    "why": "none of the three has been declared for this "
                           "term. UNASSESSED is not 'no' -- a word that has "
                           "not been checked is not thereby a word that "
                           "fails the check",
                    "loadable": False,
                    "why_not_loadable": "a term may not be loaded on an "
                                        "unassessed basis, which is the "
                                        "spec's rule read forward rather "
                                        "than a claim about this term"}
        carries = any(bool(v) for v in fields.values())
        return {"verdict": carries,
                "state": "ASSESSED",
                "fields": fields,
                "why": "carries a measurement" if carries else
                       "no quantity, no sign, no formal definition: not "
                       "carrying a measurement. It may still be doing useful "
                       "work and it cannot be cut with",
                "loadable": carries,
                "why_not_loadable": None if carries else "do not load it"}


# --- the three worked cases, as delivered ----------------------------------

DELIVERED_BY = "operator, SPEC_CITATION.md worked cases"

CASES = [
    Citation(
        term='TPS / "lean"',
        source="1980s TPS literature",
        referent_at_measurement="worker holds machine-specific diagnostic "
                                "knowledge; any worker may stop the line "
                                "(Jidoka)",
        load_bearing=["line-stop authority at lowest reading point",
                      "knowledge transmitted by mentoring"],
        present_referent="worker as fungible input; procedure compliance; "
                         "rotation between machines",
        load_bearing_now="REMOVED",
        status="load-bearing element REMOVED. Original results still cited. "
               "Citation does not transfer.",
        retest="NOT_RETESTED",
        declared_by=DELIVERED_BY),
    Citation(
        term="Resilience",
        source="Holling 1973",
        referent_at_measurement="magnitude of disturbance absorbable before "
                                "state shift; defined explicitly AGAINST "
                                "engineered stability",
        load_bearing=["unused capacity -- slack, redundancy, variation"],
        present_referent="rapid recovery to prior state; slack classified "
                         "as waste",
        load_bearing_now="REMOVED",
        status="load-bearing element is what the present-day program "
               "eliminates. Both words run simultaneously in the same "
               "institution.",
        retest="NOT_INSTANTIABLE",
        coexisting=True,
        declared_by=DELIVERED_BY,
        note="testing this requires a system with slack in it; where those "
             "have been optimised away the original claim cannot be "
             "retested"),
    Citation(
        term="Safety",
        source="institutional practice",
        referent_at_measurement="whole-facility operability -- air handling, "
                                "water, ergonomics, office and floor; held "
                                "binding authority upward, including over "
                                "executives",
        load_bearing=["enforcement",
                      "scope covering everything that could degrade "
                      "operability"],
        present_referent="worker compliance with procedure",
        load_bearing_now="REMOVED",
        status="scope contracted, enforcement removed. Frozen variables do "
               "not stop existing; they stop being read. Metric can improve "
               "while facility degrades.",
        retest="NOT_RETESTED",
        declared_by=DELIVERED_BY),
]


def table():
    return [c.transfers() for c in CASES]


def counts():
    out = dict((v, 0) for v in TRANSFER)
    for r in table():
        out[r["verdict"]] += 1
    return out


# --- the safety case, run ---------------------------------------------------
# "Frozen variables do not stop existing; they stop being read. Metric can
# improve while facility degrades." That is arithmetic, so it is run rather
# than restated.

FACILITY = ["air handling", "water", "ergonomics", "office", "floor",
            "procedure compliance"]

# Then: everything is read. Now: only compliance is read. The unread
# variables keep existing and keep moving.
READ_THEN = list(FACILITY)
READ_NOW = ["procedure compliance"]


def facility_run(steps=6, compliance_gain=0.05, unread_decay=0.04):
    """One facility, two measurement scopes, over time.

    Deterministic, no rng. Compliance is worked on because it is what is
    read; everything unread degrades at a fixed rate. The question is what
    each scope's metric says about the same facility.
    """
    # The read variable starts with room to improve -- it is the one being
    # worked on, because it is the one being read. The rest start sound.
    state = dict((k, 0.70 if k in READ_NOW else 1.0) for k in FACILITY)
    rows = []
    for t in range(steps):
        for k in state:
            if k in READ_NOW:
                state[k] = min(1.0, state[k] + compliance_gain)
            else:
                state[k] = max(0.0, state[k] - unread_decay)
        metric_now = sum(state[k] for k in READ_NOW) / len(READ_NOW)
        metric_then = sum(state[k] for k in READ_THEN) / len(READ_THEN)
        rows.append({"t": t + 1, "metric_now": metric_now,
                     "metric_then": metric_then,
                     "state": dict(state)})
    first, last = rows[0], rows[-1]
    return {
        "rows": rows,
        "narrow_metric_delta": last["metric_now"] - first["metric_now"],
        "whole_facility_delta": last["metric_then"] - first["metric_then"],
        "diverged": (last["metric_now"] > first["metric_now"]
                     and last["metric_then"] < first["metric_then"]),
        "unread": [k for k in FACILITY if k not in READ_NOW],
        "n_unread": len(FACILITY) - len(READ_NOW),
        "why": "the released variables are UNDECLARED, not FROZEN. A frozen "
               "variable is declared held still; these were declared by "
               "nobody and kept moving. The narrow metric is correct about "
               "what it reads",
    }


# --- what the safety case's "frozen" means, against SPEC_SHAPES ------------

def frozen_term_check():
    """The word "frozen" in this spec and in SPEC_SHAPES.md.

    SPEC_SHAPES.md: "FROZEN entries are declared by the builder, not
    inferred", and a variable in neither the LIVE nor the FROZEN list is
    UNDECLARED -- a claim nobody made.

    SPEC_CITATION.md: "Frozen variables do not stop existing; they stop
    being read."

    In the safety case, the variables that stopped being read -- air
    handling, water, ergonomics, office, floor -- were not declared by
    anyone. The scope contracted and they fell out. Under SPEC_SHAPES' own
    constraint, calling them FROZEN is exactly the inference that spec
    forbids.

    So the two deliveries use the word for different objects. Reported, not
    resolved: three readings are available and picking one would settle by
    arithmetic a question about what the operator meant.
    """
    readings = [
        {"name": "UNDECLARED",
         "claim": "nobody declared these held still; the scope contracted "
                  "and they fell out. This is SPEC_SHAPES' third state",
         "fits": "the constraint that FROZEN is declared, never inferred",
         "misses": "the citation note's emphasis that they keep MOVING, "
                   "which UNDECLARED does not itself say"},
        {"name": "ASSUMED_FROZEN",
         "claim": "treated as held still by not being read, while in fact "
                  "moving. Neither declared-frozen nor merely undeclared",
         "fits": "why the metric can improve while the facility degrades -- "
                 "it needs the variables to be presumed constant AND to be "
                 "changing",
         "misses": "SPEC_SHAPES has no such state, so adopting it would "
                   "extend that spec rather than read this one"},
        {"name": "SAME_WORD_LOOSELY",
         "claim": "'frozen' here is ordinary usage for held-constant, with "
                  "no reference to SPEC_SHAPES' declared list",
         "fits": "the two notes were delivered separately and neither "
                 "cites the other",
         "misses": "the repo now runs both, and a reader moving between "
                   "them meets one word and two objects"},
    ]
    return {"collision": True,
            "spec_shapes": "FROZEN entries are declared by the builder, "
                           "not inferred",
            "spec_citation": "Frozen variables do not stop existing; they "
                             "stop being read",
            "readings": readings,
            "picked": None,
            "why_not_picked": "which one holds is a question about what was "
                              "meant, and this module cannot answer it. "
                              "PREAMBLE.md's own TERM COLLISION note is the "
                              "instrument for this, and its rule is that the "
                              "senses get named, not merged"}


def confidence():
    return {"the_three_cases": "delivered verbatim, including their status "
                               "lines. The referents, load-bearing elements "
                               "and present-day objects are the operator's "
                               "readings of three literatures and this "
                               "module carries them without checking them",
            "transfer_verdicts": "computed from load_bearing_now, which is "
                                 "a declared field. The computation is "
                                 "trivial; the input is the whole claim",
            "original_results": "NOT_ASSESSED_HERE on every row, and that "
                                "is permanent. Nothing in this module "
                                "measures whether the original studies were "
                                "right",
            "carries_a_measurement": "UNASSESSED on every term. The three "
                                     "fields are declared by an assessor, "
                                     "not inferred here",
            "the_facility_run": "a stipulated arithmetic demonstration that "
                                "a narrow metric can rise while a wide one "
                                "falls. It shows the mechanism is available, "
                                "not that it occurred anywhere",
            "resolved": False}


def breaks():
    return [
        "ALL THREE DELIVERED CASES COME BACK DOES_NOT_TRANSFER, AND THE "
        "MODULE COULD NOT HAVE RETURNED ANYTHING ELSE. Each case arrived "
        "with its status already stating that the load-bearing element was "
        "removed, so `load_bearing_now` was 'REMOVED' before any code ran. "
        "The verdict is the input restated in a type. What the module adds "
        "is the fields the verdict must NOT be confused with -- the original "
        "result and the retest state -- not the verdict itself",
        "THE THREE CASES ARE ALSO A SELECTED SET. They are the ones the "
        "operator noticed and wrote down, and every one of them drifted. A "
        "check whose worked examples all fail is a check with no negative "
        "control: nothing here shows what a citation that DOES transfer "
        "looks like when run through the same three questions",
        "'FROZEN' MEANS DIFFERENT THINGS IN THE TWO SPECS AND THIS MODULE "
        "DOES NOT PICK. SPEC_SHAPES.md says FROZEN entries are declared by "
        "the builder and never inferred; SPEC_CITATION.md says frozen "
        "variables stop being read. The safety case's unread variables were "
        "declared by nobody, so under the first spec they are UNDECLARED and "
        "calling them frozen is the inference that spec forbids. Three "
        "readings are printed and none is chosen, because which holds is a "
        "question about what was meant",
        "THE FACILITY RUN IS A DEMONSTRATION, NOT EVIDENCE. Compliance "
        "starts low and is worked on; everything unread decays at a fixed "
        "rate; both numbers follow. It establishes that the divergence is "
        "arithmetically available given those assumptions, and says nothing "
        "about whether any real facility behaved that way. The decay rate "
        "was chosen to make the effect legible",
        "carries_a_measurement() RETURNS UNASSESSED FOR EVERY TERM HERE, "
        "INCLUDING ONES WHERE THE DELIVERED TEXT ARGUABLY SUPPLIES THE "
        "ANSWER. Holling's referent is given as 'magnitude of disturbance "
        "absorbable before state shift', which reads like a quantity with a "
        "sign. Filling the field from that would be this module deciding "
        "what counts as a formal definition in ecology, so the field stays "
        "empty and the reading stays available to whoever assesses it",
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
    L = ["TERM-DRIFT CITATION CHECK -- does the measurement still attach",
         "=" * 72, ""]
    L.append("  A citation carries a measurement forward under a word. It is")
    L.append("  valid only if the word's referent held between the")
    L.append("  measurement and the use, and nothing in a citation records")
    L.append("  whether it did.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    for c in CASES:
        r = c.transfers()
        L.append("  %s  (%s)" % (c.term, c.source))
        L.append("")
        for label, val in (("referent then", c.referent_at_measurement),
                           ("load-bearing", "; ".join(c.load_bearing)),
                           ("referent now", c.present_referent)):
            for line in _wrap("%-15s %s" % (label + ":", val), "    "):
                L.append(line)
        L.append("")
        L.append("    load-bearing now: %s" % c.load_bearing_now)
        L.append("    VERDICT:          %s" % r["verdict"])
        L.append("    original result:  %s" % r["original_result"])
        L.append("    retest:           %s" % r["retest"])
        if c.coexisting:
            L.append("    both referents run in the same institution.")
        L.append("")
    c2 = counts()
    L.append("  %s" % ", ".join("%s=%d" % (k, v)
                                for k, v in sorted(c2.items())))
    L.append("")
    L.append("  DOES_NOT_TRANSFER IS NOT REFUTED. The result may be correct")
    L.append("  and still not attach. `original_result` is NOT_ASSESSED_HERE")
    L.append("  on every row and stays that way: nothing in this module")
    L.append("  measures whether the original studies were right.")
    L.append("")
    L.append("  ABSENCE OF RETEST IS NOT REFUTATION EITHER, and Holling is")
    L.append("  NOT_INSTANTIABLE -- testing it needs a system with slack in")
    L.append("  it, and where slack was optimised away there is no retest")
    L.append("  for the absence to be an absence of.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE SAFETY CASE, RUN")
    L.append("")
    L.append("  'Frozen variables do not stop existing; they stop being")
    L.append("  read. Metric can improve while facility degrades.'")
    L.append("  That is arithmetic, so here it is.")
    L.append("")
    f = facility_run()
    L.append("    read now:  %s" % ", ".join(READ_NOW))
    L.append("    unread:    %s" % ", ".join(f["unread"]))
    L.append("")
    L.append("    %-6s %-16s %s" % ("t", "metric (read now)", "whole"))
    for row in f["rows"]:
        L.append("    %-6d %-16.3f %.3f"
                 % (row["t"], row["metric_now"], row["metric_then"]))
    L.append("")
    L.append("    narrow metric  %+.3f" % f["narrow_metric_delta"])
    L.append("    whole facility %+.3f" % f["whole_facility_delta"])
    L.append("    diverged:      %s" % f["diverged"])
    L.append("")
    L.append("    The narrow metric reaches 1.000 and is not wrong. It is")
    L.append("    correct about what it reads.")
    L.append("")
    for line in _wrap(f["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  'FROZEN' IN THIS SPEC AND IN SPEC_SHAPES.md")
    L.append("")
    ft = frozen_term_check()
    for line in _wrap("SPEC_SHAPES.md:   " + ft["spec_shapes"], "    "):
        L.append(line)
    for line in _wrap("SPEC_CITATION.md: " + ft["spec_citation"], "    "):
        L.append(line)
    L.append("")
    L.append("    Two deliveries, one word, two objects. The safety case's")
    L.append("    unread variables were declared by nobody, so under the")
    L.append("    first spec they are UNDECLARED, and calling them FROZEN")
    L.append("    is the inference that spec forbids.")
    L.append("")
    for rd in ft["readings"]:
        L.append("    %s" % rd["name"])
        for line in _wrap(rd["claim"], "      "):
            L.append(line)
        for line in _wrap("fits: " + rd["fits"], "        "):
            L.append(line)
        for line in _wrap("misses: " + rd["misses"], "        "):
            L.append(line)
        L.append("")
    L.append("    picked: %s" % ft["picked"])
    for line in _wrap(ft["why_not_picked"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  A WORD IS NOT A MEASUREMENT")
    L.append("")
    L.append("    %-16s %-12s %s" % ("term", "state", "loadable"))
    for c in CASES:
        m = c.carries_a_measurement()
        L.append("    %-16s %-12s %s"
                 % (c.term[:16], m["state"], m["loadable"]))
    L.append("")
    L.append("    UNASSESSED is not 'no'. A word that has not been checked")
    L.append("    is not thereby a word that fails the check -- and it is")
    L.append("    still not loadable, which is the spec's rule read forward")
    L.append("    rather than a verdict on these terms.")
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
        Citation("t", "s", "", ["lb"], "now", "REMOVED", "st",
                 declared_by="op")
        ok = False
    except CitationError:
        ok = True
    ck("a citation missing one of the three answers is refused -- "
       "unchecked is not passed", ok)
    try:
        Citation("t", "s", "then", ["lb"], "now", "REMOVED", "st",
                 declared_by=None)
        ok = False
    except CitationError:
        ok = True
    ck("the three answers carry who answered them", ok)

    ck("all three delivered cases are DOES_NOT_TRANSFER",
       counts()["DOES_NOT_TRANSFER"] == 3 and len(CASES) == 3)
    ck("and every one holds the original result apart from the verdict",
       all(r["original_result"] == "NOT_ASSESSED_HERE" for r in table()))
    ck("does-not-transfer is never refuted: the result may be correct and "
       "still not attach",
       all("still not attach" in r["why_original_is_separate"]
           for r in table()))
    ck("Holling is NOT_INSTANTIABLE, not merely NOT_RETESTED",
       [c for c in CASES if c.source == "Holling 1973"][0].retest
       == "NOT_INSTANTIABLE")
    ck("and NOT_INSTANTIABLE is not one of the transfer verdicts, so it "
       "cannot be read as one", "NOT_INSTANTIABLE" not in TRANSFER)
    ck("the coexisting-referents case is flagged as such",
       [c for c in CASES if c.source == "Holling 1973"][0].coexisting
       is True)
    ck("a PRESENT load-bearing element would transfer, so the verdict is "
       "not hardcoded",
       Citation("t", "s", "then", ["lb"], "now", "PRESENT", "st",
                declared_by="op").transfers()["verdict"] == "TRANSFERS")
    ck("and UNASSESSED stays its own verdict",
       Citation("t", "s", "then", ["lb"], "now", "UNASSESSED", "st",
                declared_by="op").transfers()["verdict"] == "UNASSESSED")

    for c in CASES:
        m = c.carries_a_measurement()
        ck("%s: carries_a_measurement is UNASSESSED, not decided here"
           % c.term, m["state"] == "UNASSESSED" and m["verdict"] is None)
        ck("%s: and unassessed is not loadable" % c.term,
           m["loadable"] is False)
    probe = Citation("p", "s", "then", ["lb"], "now", "PRESENT", "st",
                     declared_by="op")
    probe.quantity = "magnitude, dimensionless"
    ck("a term with a declared quantity does carry a measurement",
       probe.carries_a_measurement()["verdict"] is True
       and probe.carries_a_measurement()["loadable"] is True)

    fr = facility_run()
    ck("the narrow metric rises while the whole facility falls",
       fr["diverged"] is True and fr["narrow_metric_delta"] > 0
       and fr["whole_facility_delta"] < 0)
    ck("the narrow metric reaches its ceiling and is correct about what it "
       "reads", abs(fr["rows"][-1]["metric_now"] - 1.0) < 1e-9)
    ck("five of six facility variables are unread", fr["n_unread"] == 5)
    ck("and the unread ones kept moving rather than being held still",
       all(fr["rows"][-1]["state"][k] < 1.0 for k in fr["unread"]))

    ft = frozen_term_check()
    ck("the two specs use 'frozen' for different objects", ft["collision"])
    ck("three readings are offered and none is picked",
       len(ft["readings"]) == 3 and ft["picked"] is None)
    ck("the input-restated-as-verdict limit leads the breaks list",
       "COULD NOT HAVE RETURNED ANYTHING ELSE" in breaks()[0])
    ck("the missing negative control is disclosed",
       any("no negative control" in b for b in breaks()))
    ck("the frozen collision is disclosed in breaks too",
       any("MEANS DIFFERENT THINGS IN THE TWO SPECS" in b
           for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE SAFETY CASE, RUN" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="term-drift citation check")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
