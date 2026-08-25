#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
pressure_record.py - why the crossing is the only period that shows it.

    python3 pressure_record.py [--selftest]

Marker under exploration. Delivered spec: SPEC_ADDENDUM.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE ASYMMETRY, AS DELIVERED. "Once refusal no longer holds, pressure stops
being applied, because nothing requires it. The negotiation disappears from
the record. Absence of documented pressure in later periods is therefore NOT
evidence of less pressure. It is consistent with the boundary being gone."

DOCUMENTED PRESSURE IS NON-MONOTONIC IN THE THING IT IS READ AS MEASURING,
AND ZERO OCCURS ON BOTH SIDES OF THE PEAK. Before the reorganisation the
decision sat with the function, so nothing needed pressing. During the
crossing the boundary was contested, so pressure was applied and a refusal
held. After, nothing requires pressure. The record therefore shows a spike
between two zeros, and the two zeros mean opposite things: one is a boundary
that was never tested because it was never approached, the other is a
boundary that is gone.

This is the same shape as the stop count in stop_authority.py -- a facility
where the authority is actively refused publishes MORE stops than a safe one --
and it is the shape twice, which is worth saying plainly rather than counting
as two findings.

THE PRESSURE EVENT IS EVIDENCE THAT A BOUNDARY EXISTED. That is the one thing
a documented pressure event establishes cleanly: someone had to be pushed,
which means something was in the way. It does not establish that the boundary
held afterwards, and this module does not infer that.

THE CROSSING IS DOCUMENTED BY NOBODY WHOSE JOB IS TO DOCUMENT. "The before
and after states are both documented by parties who write; the crossing is
not." Which makes transition-period witness accounts the only observations
that can show the mechanism, and makes them the observations with no
institutional producer. n=1 here, and the open work says so.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

PERIODS = ("BEFORE", "TRANSITION", "AFTER")

BOUNDARY = {
    "BEFORE": "INTACT_UNAPPROACHED",
    "TRANSITION": "CONTESTED",
    "AFTER": "UNKNOWN_POSSIBLY_GONE",
}


def record():
    """Documented pressure events per period, and what each zero means."""
    return [
        {"period": "BEFORE",
         "documented_pressure_events": 0,
         "boundary": BOUNDARY["BEFORE"],
         "why_zero": "the decision sat with the function. Nothing needed "
                     "pressing, so nothing was pressed and nothing was "
                     "recorded",
         "reading_if_count_alone": "no pressure -- read as a healthy period"},
        {"period": "TRANSITION",
         "documented_pressure_events": 1,
         "boundary": BOUNDARY["TRANSITION"],
         "why_zero": None,
         "reading_if_count_alone": "pressure present -- read as the "
                                   "unhealthy period"},
        {"period": "AFTER",
         "documented_pressure_events": 0,
         "boundary": BOUNDARY["AFTER"],
         "why_zero": "if refusal no longer holds, nothing requires pressure. "
                     "The negotiation does not occur, so it is not recorded",
         "reading_if_count_alone": "no pressure -- read as a healthy period, "
                                   "and as an improvement on the transition"},
    ]


def zeros_are_not_the_same():
    """The two zeros, and what separates them. Nothing in the count does."""
    rows = record()
    before = [r for r in rows if r["period"] == "BEFORE"][0]
    after = [r for r in rows if r["period"] == "AFTER"][0]
    return {
        "before_count": before["documented_pressure_events"],
        "after_count": after["documented_pressure_events"],
        "counts_identical": (before["documented_pressure_events"]
                             == after["documented_pressure_events"]),
        "before_boundary": before["boundary"],
        "after_boundary": after["boundary"],
        "boundaries_identical": before["boundary"] == after["boundary"],
        "separated_by_the_count": False,
        "state": "INDISTINGUISHABLE_BY_COUNT",
        "why": "identical observable, opposite states. Absence of documented "
               "pressure in later periods is not evidence of less pressure; "
               "it is consistent with the boundary being gone",
    }


def shape_of_the_series():
    """Non-monotonic, with the informative period between the two zeros."""
    rows = record()
    counts = [r["documented_pressure_events"] for r in rows]
    peak = counts.index(max(counts))
    return {
        "counts": counts,
        "peak_period": PERIODS[peak],
        "monotonic": counts == sorted(counts) or counts == sorted(
            counts, reverse=True),
        "informative_periods": [PERIODS[i] for i, c in enumerate(counts)
                                if c > 0],
        "n_informative": sum(1 for c in counts if c > 0),
        "why": "the only period producing an observation is the crossing. "
               "Sampling later periods finds zero and reads it as "
               "improvement over the transition, which is the reading the "
               "series is shaped to produce",
    }


def what_the_pressure_event_establishes():
    """One thing cleanly, and not the next thing."""
    return {
        "establishes": "a boundary existed to press against at that time. "
                       "Someone had to be pushed, so something was in the "
                       "way",
        "does_not_establish": "that the boundary held afterwards. The "
                              "refusal held at that time, and the record "
                              "contains no later test because a later test "
                              "would require pressure nobody needed to "
                              "apply",
        "held_at_the_time": True,
        "held_afterwards": None,
        "why_none": "None, not False. No later refusal is recorded and no "
                    "later pressure is recorded either, which is the "
                    "asymmetry rather than an answer to it",
    }


# --- open work, item 5: the attempts-vs-executions survey ------------------
# "Test whether any published SWA program reports attempts separately from
# executions. If none do, that absence is itself the finding."
#
# The survey is not run here. This side has no access to a corpus of
# published SWA programs, and a table of invented rows would be worse than an
# empty one. What ships is the harness, the one row available, and an
# explicit NOT_RUN state -- because an empty registry is not the finding.

SURVEY_MIN_N = 5


class ProgramRecord(object):
    def __init__(self, name, reports_executions, reports_attempts, source,
                 note=None):
        if reports_executions is None or reports_attempts is None:
            raise ValueError(
                "both fields are required, and None is not False. A program "
                "whose reporting was not examined is not a program that "
                "reports nothing")
        if not source:
            raise ValueError("a survey row cites where it was read")
        self.name = name
        self.reports_executions = reports_executions
        self.reports_attempts = reports_attempts
        self.source = source
        self.note = note

    def row(self):
        return {"program": self.name,
                "reports_executions": self.reports_executions,
                "reports_attempts": self.reports_attempts,
                "separates_them": (self.reports_attempts
                                   and self.reports_executions),
                "source": self.source, "note": self.note}


SURVEY = [
    ProgramRecord(
        name="prior art: SWA as core program element",
        reports_executions=True,
        reports_attempts=False,
        source="SPEC_STOP_AUTHORITY.md, PRIOR ART section",
        note="stops recalled (zero) stands as the execution report. No "
             "attempts figure appears anywhere in the account"),
]


def survey_state():
    rows = [p.row() for p in SURVEY]
    separating = [r for r in rows if r["separates_them"]]
    return {
        "n": len(rows),
        "n_separating": len(separating),
        "rows": rows,
        "finding": None,
        "state": "NOT_RUN",
        "why": "the finding the spec names -- that no published program "
               "separates attempts from executions -- requires a survey of "
               "published programs, and none has been conducted here. One "
               "row is not a survey and an empty registry is not a result. "
               "NOT_RUN is the state; ABSENT would be the finding and it is "
               "not available",
        "what_would_make_it_a_finding":
            "at least %d programs read from their own published material, "
            "each row citing where it was read, with reports_attempts "
            "recorded as False only where the material was examined and the "
            "figure was absent -- never where nobody looked" % SURVEY_MIN_N,
    }


# --- open work, item 3: one move or two ------------------------------------

def one_move_or_two():
    """Whether stop-authority hollowing and safety-scope contraction are one.

    Discriminating test: one facility with BOTH axes recorded. If they are
    one move they co-occur and share a mechanism; if two, either occurs
    without the other. The cases available are from different facilities and
    each records one axis, so the test cannot be run.
    """
    cases = [
        {"case": "SWA prior art", "stop_authority": "HOLLOW_UNTESTED",
         "safety_scope": "NOT_RECORDED"},
        {"case": "institutional safety (term-drift)",
         "stop_authority": "NOT_RECORDED", "safety_scope": "CONTRACTED"},
        {"case": "Eagan reorganisation", "stop_authority": "NOT_RECORDED",
         "safety_scope": "MEASUREMENT_POINT_RELOCATED"},
    ]
    both = [c for c in cases if c["stop_authority"] != "NOT_RECORDED"
            and c["safety_scope"] != "NOT_RECORDED"]
    return {
        "cases": cases,
        "n_with_both_axes": len(both),
        "verdict": None,
        "state": "CANNOT_DISCRIMINATE",
        "discriminating_test": "one facility with both axes recorded. Two "
                               "facilities each showing one axis are "
                               "consistent with one move and with two",
        "why": "three cases, three different facilities, one axis each. "
               "Nothing here separates the hypotheses and the cases cannot "
               "be pooled -- a facility is the unit, and no facility here "
               "has both",
    }


OPEN_WORK = [
    {"item": "collect additional transition-period witness accounts",
     "state": "OPEN", "n_now": 1,
     "note": "the crossing has no institutional producer, which is why "
             "n=1 and why it will not rise on its own"},
    {"item": "recover pressure events after the boundary is gone",
     "state": "NO_METHOD_PROPOSED", "n_now": None,
     "note": "the events do not occur, so there is nothing to recover. A "
             "method would have to reconstruct a negotiation that did not "
             "happen"},
    {"item": "is stop-authority hollowing the same move as safety-scope "
             "contraction",
     "state": "CANNOT_DISCRIMINATE", "n_now": 0,
     "note": "no facility here has both axes recorded"},
    {"item": "collection mechanism for WARRANTED-IN-REVIEW",
     "state": "NO_METHOD_PROPOSED", "n_now": None,
     "note": "every mechanism proposed so far requires the reviewing party "
             "to admit the count matters, which is the same authority "
             "question one level up"},
    {"item": "do any published SWA programs report attempts separately",
     "state": "NOT_RUN", "n_now": 1,
     "note": "harness built and shipped empty. One row available, and the "
             "spec's 'if none do, that absence is the finding' needs a "
             "survey before an absence means anything"},
]


def confidence():
    return {"the_witnessed_case": "one account, from the operator, from a "
                                  "position held during the transition. "
                                  "Carried as delivered. Nothing here "
                                  "verifies it and nothing here could",
            "n": "one. The spec says so and the open-work register keeps it "
                 "visible rather than letting three modules built on it "
                 "read as three observations",
            "the_period_structure": "before / transition / after with the "
                                    "counts 0, 1, 0 is the account's own "
                                    "shape made explicit, not a measured "
                                    "series",
            "the_survey": "NOT_RUN. One row, and one row is not a survey. "
                          "The spec's finding needs an absence established "
                          "by looking, and no looking has been done",
            "one_move_or_two": "CANNOT_DISCRIMINATE. Three cases, three "
                               "facilities, one axis each",
            "resolved": False}


def breaks():
    return [
        "DOCUMENTED PRESSURE IS ZERO ON BOTH SIDES OF THE PEAK AND THE TWO "
        "ZEROS MEAN OPPOSITE THINGS. Before, the decision sat with the "
        "function and nothing needed pressing. After, if refusal no longer "
        "holds, nothing requires pressure. Identical observable, opposite "
        "states, and the count separates neither -- so a survey sampling "
        "later periods finds zero and reads it as an improvement on the "
        "transition. That is the reading the series is shaped to produce",
        "THIS IS THE SAME SHAPE AS THE STOP COUNT AND IT IS ONE FINDING, "
        "NOT TWO. stop_authority.py already showed a facility where the "
        "authority is actively refused publishing MORE stops than a safe "
        "one. Here the contested period is the one that produces a record. "
        "Both are the observable running non-monotonic in the thing it is "
        "read as measuring, in one repo by one builder, and counting them "
        "as two independent results would be the inherited-agreement error "
        "operator-structure-echo exists to catch",
        "n=1, AND THREE MODULES NOW REST ON THAT ONE ACCOUNT. relocation.py, "
        "this module and the open-work register all take their structure "
        "from a single witnessed transition. Building three readouts on one "
        "observation does not make it three observations, and the spec's "
        "own open work leads with collecting more. The account is also the "
        "operator's own, carried without independent check, which is the "
        "only form this evidence comes in and is still what it is",
        "THE SURVEY IS NOT RUN AND ITS ABSENCE IS NOT THE FINDING. The spec "
        "says that if no published SWA program reports attempts separately "
        "from executions, that absence is itself the finding. It would be. "
        "Establishing it requires reading published programs, this side has "
        "no access to a corpus of them, and inventing rows would be worse "
        "than an empty table. The harness ships with one row and state "
        "NOT_RUN -- ABSENT is a different state and is not available",
        "THE WARRANTED-IN-REVIEW COLLECTION PROBLEM IS NOT SOLVED HERE AND "
        "MAY NOT BE SOLVABLE IN THE FORM STATED. Every mechanism requires "
        "the reviewing party to admit the count matters, which is the same "
        "authority question one level up: the party who would have to "
        "collect the denominator is the party a stop binds against. "
        "Recording that recursion is not progress on it",
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
    L = ["PRESSURE RECORD -- why the crossing is the only period that shows "
         "it", "=" * 72, ""]
    L.append("  Once refusal no longer holds, pressure stops being applied,")
    L.append("  because nothing requires it. The negotiation disappears")
    L.append("  from the record.")
    L.append("")
    L.append("  %-14s %-8s %-26s %s"
             % ("period", "events", "boundary", ""))
    for r in record():
        L.append("  %-14s %-8d %-26s"
                 % (r["period"], r["documented_pressure_events"],
                    r["boundary"]))
    L.append("")
    sh = shape_of_the_series()
    L.append("    counts: %s   monotonic: %s   peak: %s"
             % (sh["counts"], sh["monotonic"], sh["peak_period"]))
    L.append("    periods producing an observation: %d of %d"
             % (sh["n_informative"], len(PERIODS)))
    L.append("")
    for line in _wrap(sh["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE TWO ZEROS")
    L.append("")
    z = zeros_are_not_the_same()
    L.append("    BEFORE  count %d   boundary %s"
             % (z["before_count"], z["before_boundary"]))
    L.append("    AFTER   count %d   boundary %s"
             % (z["after_count"], z["after_boundary"]))
    L.append("")
    L.append("    counts identical:     %s" % z["counts_identical"])
    L.append("    boundaries identical: %s" % z["boundaries_identical"])
    L.append("    separated by count:   %s" % z["separated_by_the_count"])
    L.append("    state: %s" % z["state"])
    L.append("")
    for line in _wrap(z["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  WHAT THE PRESSURE EVENT ESTABLISHES")
    L.append("")
    w = what_the_pressure_event_establishes()
    for line in _wrap("establishes: " + w["establishes"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap("does not establish: " + w["does_not_establish"],
                      "    "):
        L.append(line)
    L.append("")
    L.append("    held at the time:  %s" % w["held_at_the_time"])
    L.append("    held afterwards:   %s" % w["held_afterwards"])
    for line in _wrap(w["why_none"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  OPEN WORK")
    L.append("")
    L.append("    %-46s %s" % ("item", "state"))
    for o in OPEN_WORK:
        L.append("    %-46s %s" % (o["item"][:46], o["state"]))
    L.append("")
    L.append("  ITEM 5 -- THE SURVEY, AND WHY IT IS NOT A FINDING YET")
    L.append("")
    s = survey_state()
    L.append("    rows: %d   separating attempts from executions: %d"
             % (s["n"], s["n_separating"]))
    for r in s["rows"]:
        L.append("      %-40s exec=%s attempts=%s"
                 % (r["program"][:40], r["reports_executions"],
                    r["reports_attempts"]))
    L.append("")
    L.append("    finding: %s    state: %s" % (s["finding"], s["state"]))
    for line in _wrap(s["why"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap("what would make it one: "
                      + s["what_would_make_it_a_finding"], "    "):
        L.append(line)
    L.append("")
    L.append("  ITEM 3 -- ONE MOVE OR TWO")
    L.append("")
    om = one_move_or_two()
    for c in om["cases"]:
        L.append("    %s" % c["case"])
        L.append("      stop authority: %-20s" % c["stop_authority"])
        L.append("      safety scope:   %s" % c["safety_scope"])
    L.append("")
    L.append("    facilities with both axes: %d" % om["n_with_both_axes"])
    L.append("    verdict: %s   state: %s" % (om["verdict"], om["state"]))
    for line in _wrap(om["discriminating_test"], "    "):
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

    z = zeros_are_not_the_same()
    ck("before and after publish an identical count", z["counts_identical"])
    ck("and their boundary states are opposite",
       z["boundaries_identical"] is False)
    ck("the count separates neither",
       z["separated_by_the_count"] is False
       and z["state"] == "INDISTINGUISHABLE_BY_COUNT")

    sh = shape_of_the_series()
    ck("documented pressure is non-monotonic", sh["monotonic"] is False)
    ck("the peak is the transition, between the two zeros",
       sh["peak_period"] == "TRANSITION" and sh["counts"] == [0, 1, 0])
    ck("only one of three periods produces an observation",
       sh["n_informative"] == 1)

    w = what_the_pressure_event_establishes()
    ck("the pressure event establishes a boundary existed at that time",
       w["held_at_the_time"] is True)
    ck("and says nothing about afterwards -- None, not False",
       w["held_afterwards"] is None and "not False" in w["why_none"])

    s = survey_state()
    ck("the survey is NOT_RUN and returns no finding",
       s["state"] == "NOT_RUN" and s["finding"] is None)
    ck("one row is present and it does not separate the two figures",
       s["n"] == 1 and s["n_separating"] == 0)
    ck("and NOT_RUN is distinguished from the ABSENT the spec would call a "
       "finding", "ABSENT would be the finding" in s["why"])
    ck("the bar for the survey is stated in the module, not left to a "
       "reader", str(SURVEY_MIN_N) in s["what_would_make_it_a_finding"])
    try:
        ProgramRecord("p", True, None, "src")
        ok = False
    except ValueError:
        ok = True
    ck("a program whose reporting was not examined cannot be filed as "
       "reporting nothing", ok)
    try:
        ProgramRecord("p", True, False, "")
        ok = False
    except ValueError:
        ok = True
    ck("a survey row cites where it was read", ok)

    om = one_move_or_two()
    ck("no facility has both axes recorded", om["n_with_both_axes"] == 0)
    ck("so the hypotheses cannot be discriminated",
       om["state"] == "CANNOT_DISCRIMINATE" and om["verdict"] is None)
    ck("and the discriminating test is named rather than approximated",
       "one facility with both axes" in om["discriminating_test"])

    ck("all five open-work items are carried", len(OPEN_WORK) == 5)
    ck("and none is marked done",
       all(o["state"] in ("OPEN", "NO_METHOD_PROPOSED",
                          "CANNOT_DISCRIMINATE", "NOT_RUN")
           for o in OPEN_WORK))

    ck("the two-zeros result leads the breaks list",
       "ZERO ON BOTH SIDES" in breaks()[0])
    ck("the shared shape with the stop count is called one finding, not two",
       any("ONE FINDING, NOT TWO" in b for b in breaks()))
    ck("three modules resting on one account is disclosed",
       any("THREE MODULES NOW REST" in b for b in breaks()))
    ck("the survey not being run is disclosed as not-the-finding",
       any("ITS ABSENCE IS NOT THE FINDING" in b for b in breaks()))
    ck("the warranted-in-review recursion is disclosed",
       any("one level up" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "THE TWO ZEROS" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="pressure record")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
