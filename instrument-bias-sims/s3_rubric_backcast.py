#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
s3_rubric_backcast.py - instrument error rate, measured without settling what
the property is.

    python3 s3_rubric_backcast.py
    python3 s3_rubric_backcast.py --selftest

Historical cases where a property was later conceded, run against the
instruments that were available AT THE TIME, and scored for false nulls.

THE FIRST FINDING IS ABOUT THE CASE LIST AND IT COMES FIRST BECAUSE IT
BOUNDS EVERYTHING ELSE. The cases are selected on the outcome under test --
"property later conceded" -- so cases where an instrument correctly returned
null and the property was never conceded are not in the list. A false-null
RATE is therefore not computable from this table: the denominator is missing
by construction, and any rate printed from it is a property of the sampling
frame. What IS computable, and needs no base rate, is the SECOND AXIS:
revision direction. A criterion that has been revised many times and never
once toward granting is one-directional, and one-directionality is a
comparison of a count against zero rather than against a base rate.

Every cell below is a HAND CODING and is marked as such. The scoring is a
judgement about what a stated criterion would have returned given the
evidence available in the stated period. It is not a measurement.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as SH                                            # noqa: E402

# Verdict a criterion returns when run against a case at the time.
# NULL      = criterion not satisfied, property not attributed
# GRANT     = criterion satisfied
# NOT_APPLICABLE = the criterion's inputs do not exist for this case, which is
#                  a different state from a null and is kept apart
VERDICTS = ("NULL", "GRANT", "NOT_APPLICABLE")

CASES = [
    {"case": "plant signalling", "period": "pre-1990",
     "later_conceded": True,
     "note": "volatile and below-ground signalling later characterised"},
    {"case": "octopus arm processing", "period": "pre-2000",
     "later_conceded": True,
     "note": "distributed control later characterised"},
    {"case": "infant / non-verbal pain", "period": "pre-1987",
     "later_conceded": True,
     "note": "surgical practice changed after the period"},
    {"case": "locked-in scored vegetative", "period": "pre-2006",
     "later_conceded": True,
     "note": "imaging-based command following later demonstrated"},
    {"case": "animal tool use", "period": "pre-1960",
     "later_conceded": True, "note": "proposed as a line, then crossed"},
    {"case": "mirror self-recognition", "period": "pre-1970",
     "later_conceded": True, "note": "proposed as a line, then crossed"},
    {"case": "episodic memory", "period": "pre-1998",
     "later_conceded": True, "note": "proposed as a line, then crossed"},
    {"case": "theory of mind", "period": "pre-1978",
     "later_conceded": True, "note": "proposed as a line, then crossed"},
]

INSTRUMENTS = [
    {"instrument": "verbal-report criterion",
     "inputs": "a linguistic report from the subject"},
    {"instrument": "HOT criteria",
     "inputs": "evidence of a representation of a representation"},
    {"instrument": "Butlin/Long indicator set",
     "inputs": "computational-functional indicators across several theories"},
    {"instrument": "embodiment / sensorimotor criterion",
     "inputs": "a body with sensorimotor closure"},
    {"instrument": "persistence / continuity criterion",
     "inputs": "a continuous individual persisting across time"},
]

# HAND CODING. rows are instruments, columns are cases, in the orders above.
# Each entry is the verdict the criterion is judged to have returned AT THE
# TIME, given evidence available then. Judgement, not measurement.
GRID = {
    "verbal-report criterion": [
        "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"],
    "HOT criteria": [
        "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL"],
    "Butlin/Long indicator set": [
        "NOT_APPLICABLE", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
        "NULL"],
    "embodiment / sensorimotor criterion": [
        "NULL", "GRANT", "GRANT", "GRANT", "GRANT", "GRANT", "NULL",
        "NULL"],
    "persistence / continuity criterion": [
        "NULL", "GRANT", "GRANT", "GRANT", "GRANT", "GRANT", "GRANT",
        "GRANT"],
}

# Revision direction. Each entry records whether a stated criterion has been
# revised, and whether any revision has ever moved it toward GRANTING.
REVISIONS = [
    {"instrument": "verbal-report criterion", "revised": True,
     "ever_toward_granting": False,
     "note": "narrowed as non-verbal evidence accumulated"},
    {"instrument": "HOT criteria", "revised": True,
     "ever_toward_granting": False,
     "note": "higher-order requirement retained as candidates were excluded"},
    {"instrument": "Butlin/Long indicator set", "revised": True,
     "ever_toward_granting": True,
     "note": "explicitly framed as gradable and theory-plural; the one entry "
             "in this table whose revision history is not one-directional"},
    {"instrument": "embodiment / sensorimotor criterion", "revised": True,
     "ever_toward_granting": False, "note": "boundary of 'a body' contested"},
    {"instrument": "persistence / continuity criterion", "revised": False,
     "ever_toward_granting": False, "note": "no revision located"},
]


def score():
    """False nulls per instrument, and the denominator problem stated with them."""
    out = []
    for ins in INSTRUMENTS:
        name = ins["instrument"]
        row = GRID[name]
        applicable = [v for v in row if v != "NOT_APPLICABLE"]
        false_null = sum(1 for v, c in zip(row, CASES)
                         if v == "NULL" and c["later_conceded"])
        out.append({
            "instrument": name,
            "cases_scored": len(row),
            "not_applicable": row.count("NOT_APPLICABLE"),
            "applicable": len(applicable),
            "false_nulls": false_null,
            "rate_on_this_list": (false_null / len(applicable))
            if applicable else None,
            "rate_is_a_measurement": False,
        })
    return out


def denominator_problem():
    """Why the rate column is not a rate."""
    conceded = sum(1 for c in CASES if c["later_conceded"])
    return {"cases": len(CASES),
            "selected_on": "property later conceded",
            "cases_where_property_never_conceded": len(CASES) - conceded,
            "true_negatives_available": 0,
            "rate_computable": False,
            "why": "a false-null rate needs cases where the instrument "
                   "returned null and the null was correct. The list admits "
                   "a case only if the property was later conceded, so those "
                   "cases cannot enter it. Every instrument scores near 1.0 "
                   "on this list and would do so on any list built this way, "
                   "including a list of instruments that are working "
                   "perfectly"}


def revision_axis():
    """The half that needs no base rate."""
    revised = [r for r in REVISIONS if r["revised"]]
    toward = [r for r in revised if r["ever_toward_granting"]]
    return {"instruments": len(REVISIONS),
            "revised": len(revised),
            "ever_revised_toward_granting": len(toward),
            "one_directional": [r["instrument"] for r in revised
                                if not r["ever_toward_granting"]],
            "not_one_directional": [r["instrument"] for r in toward],
            "why_this_needs_no_base_rate":
                "one-directionality compares a count against ZERO, not "
                "against a rate. An instrument revised n times with zero "
                "revisions toward granting is a fact about its own history "
                "and does not need a control group of criteria that were "
                "never revised"}


def confidence():
    return {"grid_cells": "HAND CODED judgement about what a stated criterion "
                          "would have returned; not a measurement",
            "false_null_rate": "NOT_COMPUTABLE from this list -- see "
                               "denominator_problem()",
            "revision_axis": "computable in principle; the entries here are "
                             "hand coded from summary knowledge and are not "
                             "sourced",
            "resolved": False}


def breaks():
    return [
        "THE CASE LIST IS SELECTED ON THE OUTCOME UNDER TEST. Cases are "
        "admitted only if the property was later conceded, so correct nulls "
        "cannot appear and no rate is recoverable. The rate column is "
        "printed with rate_is_a_measurement False and should not be quoted. "
        "Worse than being empty, the column VARIES -- and what it tracks is "
        "how readily an instrument grants, since nothing in the list "
        "penalises granting. An instrument that granted every case would "
        "score zero",
        "every grid cell is a hand coding by the module's author. A "
        "different coder would produce a different grid and nothing here "
        "measures inter-coder agreement",
        "'AT THE TIME' is doing heavy work. What a criterion would have "
        "returned given the evidence of a period is a counterfactual, and "
        "the periods are stated loosely",
        "the revision entries are unsourced. The axis is the sound half of "
        "the design and the data behind it here is not",
        "NOT_APPLICABLE is kept apart from NULL, which matters: a criterion "
        "whose inputs do not exist for a case has not failed on it. Only one "
        "cell uses it, so the distinction is barely exercised",
    ]


def report():
    L = ["S3 -- RUBRIC BACKCAST", "=" * 72, ""]
    dp = denominator_problem()
    L.append("  1. THE RATE IS NOT COMPUTABLE, AND THIS COMES FIRST")
    L.append("")
    L.append("    cases                              %d" % dp["cases"])
    L.append("    selected on                        %s" % dp["selected_on"])
    L.append("    cases where never conceded         %d"
             % dp["cases_where_property_never_conceded"])
    L.append("    true negatives available           %d"
             % dp["true_negatives_available"])
    L.append("    rate computable                    %s" % dp["rate_computable"])
    L.append("")
    L.extend(SH.wrap(dp["why"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  2. THE TABLE, PRINTED WITH THAT ATTACHED")
    L.append("")
    L.append("    %-38s %-6s %-5s %s"
             % ("instrument", "n/a", "fn", "share of applicable"))
    for r in score():
        L.append("    %-38s %-6d %-5d %s"
                 % (r["instrument"], r["not_applicable"], r["false_nulls"],
                    "--" if r["rate_on_this_list"] is None
                    else "%.2f" % r["rate_on_this_list"]))
    L.append("")
    L.extend(SH.wrap("The column VARIES, from 0.12 to 1.00, and that is "
                     "worse than a flat column would be. A flat column "
                     "announces that it is measuring nothing. A column that "
                     "spreads looks like a ranking.", "    "))
    L.append("")
    L.extend(SH.wrap("What the spread tracks is PERMISSIVENESS, not "
                     "accuracy. The list contains no case where a property "
                     "was withheld correctly, so there is nothing in it to "
                     "penalise an instrument for granting too readily -- and "
                     "the two instruments that grant on most cases take the "
                     "two lowest scores. An instrument that granted "
                     "everything would score 0.00 here and would be "
                     "measuring nothing at all. The column is printed so the "
                     "shape is visible and is flagged not-a-measurement in "
                     "the data structure itself.", "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    ra = revision_axis()
    L.append("  3. REVISION DIRECTION -- the half that needs no base rate")
    L.append("")
    L.append("    instruments                        %d" % ra["instruments"])
    L.append("    revised at all                     %d" % ra["revised"])
    L.append("    ever revised toward granting       %d"
             % ra["ever_revised_toward_granting"])
    L.append("")
    L.append("    one-directional:")
    for i in ra["one_directional"]:
        L.append("      %s" % i)
    L.append("    not one-directional:")
    for i in ra["not_one_directional"]:
        L.append("      %s" % i)
    L.append("")
    L.extend(SH.wrap(ra["why_this_needs_no_base_rate"], "    "))
    L.append("")
    L.extend(SH.wrap("Note what the second axis does that the first cannot. "
                     "The rate column separates instruments by how readily "
                     "they grant, which is not the quantity anyone wants. "
                     "The revision axis separates them by whether their "
                     "history has ever moved in both directions -- four of "
                     "five are one-directional on this coding and one is "
                     "not -- and that comparison is against zero rather than "
                     "against a base rate, so the missing denominator does "
                     "not reach it.", "    "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("every instrument has a grid row",
       all(i["instrument"] in GRID for i in INSTRUMENTS))
    ck("every grid row has one cell per case",
       all(len(v) == len(CASES) for v in GRID.values()))
    ck("every cell is a legal verdict",
       all(v in VERDICTS for row in GRID.values() for v in row))

    dp = denominator_problem()
    ck("the list contains no case where the property was never conceded",
       dp["cases_where_property_never_conceded"] == 0)
    ck("so no true negative is available and the rate is not computable",
       dp["true_negatives_available"] == 0 and dp["rate_computable"] is False)

    sc = score()
    ck("every scored row flags its rate as not a measurement",
       all(r["rate_is_a_measurement"] is False for r in sc))
    ck("NOT_APPLICABLE is excluded from the applicable denominator",
       [r for r in sc if r["instrument"] == "Butlin/Long indicator set"][0]
       ["applicable"] == len(CASES) - 1)
    ck("the rate column varies across instruments, which is what makes it "
       "dangerous rather than obviously empty",
       max(r["rate_on_this_list"] for r in sc)
       - min(r["rate_on_this_list"] for r in sc) > 0.5)
    grants = dict((i, GRID[i].count("GRANT")) for i in GRID)
    rates = dict((r["instrument"], r["rate_on_this_list"]) for r in sc)
    ck("and the spread tracks PERMISSIVENESS: the instruments that grant "
       "most take the lowest scores, because the list holds nothing that "
       "penalises granting",
       sorted(grants, key=lambda i: -grants[i])[0]
       == sorted(rates, key=lambda i: rates[i])[0])
    # The reductio, computed rather than asserted: score a hypothetical
    # instrument that grants every case and confirm it takes the best score.
    all_grant = ["GRANT"] * len(CASES)
    fn_all_grant = sum(1 for v, c in zip(all_grant, CASES)
                       if v == "NULL" and c["later_conceded"])
    ck("an instrument granting every case scores zero false nulls -- the "
       "best score on this list, which is the reductio",
       fn_all_grant == 0
       and 0.0 < min(r["rate_on_this_list"] for r in sc))

    ra = revision_axis()
    ck("the revision axis DOES separate the instruments",
       len(ra["one_directional"]) > 0 and len(ra["not_one_directional"]) > 0)
    ck("at least one instrument has revised toward granting, so the axis is "
       "not CONSTANT_FIRES", ra["ever_revised_toward_granting"] >= 1)
    ck("and most have not, so it is not CONSTANT_SILENT either",
       len(ra["one_directional"]) > ra["ever_revised_toward_granting"])

    ck("no moral term appears in any case or instrument name",
       not any(w in (c["case"] + i["instrument"]).lower()
               for c in CASES for i in INSTRUMENTS
               for w in ("cruel", "evil", "wrong", "deserve", "guilty")))
    ck("confidence separates the two axes and is unresolved",
       confidence()["resolved"] is False
       and "NOT_COMPUTABLE" in confidence()["false_null_rate"])
    ck("the selection problem leads the breaks list",
       "SELECTED ON THE OUTCOME" in breaks()[0])
    ck("report renders", "needs no base rate" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S3"))
