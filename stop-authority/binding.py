#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
binding.py - authority is defined by what it can bind, not by who holds it.

    python3 binding.py [--selftest]

Marker under exploration. Delivered spec: SPEC_STOP_AUTHORITY.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE STRUCTURAL QUESTION, AS DELIVERED. Record, per facility: the highest
organizational level a stop has bound; whether any stop has been reversed and
by whom; and whether the holder of the authority reports to a party whose
objectives the stop can cost.

UNTESTED IS NOT THE SAME AS FUNCTIONING, AND THEY ARE SEPARATE VALUES HERE.
"A stop authority that has never bound upward has not been tested." A facility
whose stops have only ever bound peers has produced no evidence either way,
and the readout for that is UNTESTED_ABOVE -- never FUNCTIONING, and never
HOLLOW either. The same refusal as the count: an absence of trials is not a
result, in either direction.

NO REVERSAL RECORDED IS NOT NO REVERSAL. With zero stops there is nothing to
have been reversed, so an empty reversal record is NOT_LOOKED. An empty
reversal record beside real stops is NONE_FOUND, which is a different fact.
The two are distinguished by the stop count beside them, never by the
emptiness of the list.

ON DISTRIBUTION, THE MODULE RECORDS AND DOES NOT GRADE. Extending authority to
everyone reads as expansion and MAY be contraction: authority located in
everyone is enforced by no one and has no identified holder to be reversed
against. The spec says "may", so `holder()` reports the structural facts --
whether a named position holds it, whether there is anyone to reverse against
-- and returns no verdict on expansion or contraction. Which it is depends on
the facility, and nothing here measures a facility.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stop_authority as SA                                     # noqa: E402

# Ordered. "Upward" means above the level the holder sits at.
LEVELS = ("NONE", "PEER", "SUPERVISOR", "MANAGER", "EXECUTIVE")

BINDING_STATES = ("BOUND_ABOVE_HOLDER", "UNTESTED_ABOVE", "NO_STOPS_AT_ALL")
HOLDER_KINDS = ("NAMED_POSITION", "EVERYONE", "UNSPECIFIED")
REVERSAL_STATES = ("NONE_FOUND", "FOUND", "NOT_LOOKED")


class BindingError(Exception):
    pass


class Authority(object):
    def __init__(self, facility, holder_kind, holder_level,
                 highest_bound="NONE", stops_executed=0, reversals=None,
                 holder_reports_to_costed_party="UNASSESSED",
                 named_position=None, note=None):
        if holder_kind not in HOLDER_KINDS:
            raise BindingError("holder_kind must be one of %s"
                               % (HOLDER_KINDS,))
        if highest_bound not in LEVELS or holder_level not in LEVELS:
            raise BindingError("levels must be drawn from %s" % (LEVELS,))
        if holder_kind == "NAMED_POSITION" and not named_position:
            raise BindingError(
                "a NAMED_POSITION holder needs the position named. The "
                "spec's distribution note turns on whether a named position "
                "holds it, and an unnamed 'named position' is the "
                "everyone case wearing a label")
        self.facility = facility
        self.holder_kind = holder_kind
        self.holder_level = holder_level
        self.named_position = named_position
        self.highest_bound = highest_bound
        self.stops_executed = stops_executed
        self.reversals = list(reversals or [])
        self.holder_reports_to_costed_party = holder_reports_to_costed_party
        self.note = note

    def bound_upward(self):
        """Has a stop ever bound above the level the holder sits at."""
        if self.stops_executed == 0:
            return {"state": "NO_STOPS_AT_ALL",
                    "highest_bound": self.highest_bound,
                    "tested": False,
                    "why": "no stop has been executed, so nothing has been "
                           "bound and nothing has been refused. The "
                           "authority has produced no trial in either "
                           "direction"}
        hi = LEVELS.index(self.highest_bound)
        holder = LEVELS.index(self.holder_level)
        if hi > holder:
            return {"state": "BOUND_ABOVE_HOLDER",
                    "highest_bound": self.highest_bound,
                    "tested": True,
                    "why": "a stop has bound at %s, above the holder at %s"
                           % (self.highest_bound, self.holder_level)}
        return {"state": "UNTESTED_ABOVE",
                "highest_bound": self.highest_bound,
                "tested": False,
                "why": "stops have bound only at or below the holder's own "
                       "level (%s). An authority that has never bound "
                       "upward has not been tested, which is not the same "
                       "as its having failed" % self.holder_level}

    def reversal_record(self):
        """Empty is NOT_LOOKED when there were no stops to reverse."""
        if self.stops_executed == 0:
            return {"state": "NOT_LOOKED", "reversals": [],
                    "why": "with no stops there is nothing that could have "
                           "been reversed. An empty reversal record here is "
                           "an empty record, not a clean one"}
        if not self.reversals:
            return {"state": "NONE_FOUND", "reversals": [],
                    "why": "%d stop%s executed and none reversed"
                           % (self.stops_executed,
                              "" if self.stops_executed == 1 else "s")}
        return {"state": "FOUND", "reversals": list(self.reversals),
                "why": "reversed by: %s"
                       % ", ".join(r["by"] for r in self.reversals)}

    def holder(self):
        """Structural facts about who holds it. No expansion/contraction
        verdict: the spec says distribution MAY be contraction, and which it
        is depends on a facility this module does not measure."""
        named = self.holder_kind == "NAMED_POSITION"
        return {"kind": self.holder_kind,
                "named_position": self.named_position,
                "a_named_position_holds_it": named,
                "someone_to_reverse_against": named,
                "enforced_by": (self.named_position if named else
                                "no identified holder"),
                "verdict_on_expansion": None,
                "why_no_verdict": "authority located in everyone is enforced "
                                  "by no one and has no identified holder to "
                                  "be reversed against. Whether that is "
                                  "expansion or contraction depends on the "
                                  "facility, and the spec says MAY. The "
                                  "structural facts are recorded; the grade "
                                  "is not"}

    def conflict(self):
        return {"holder_reports_to_costed_party":
                self.holder_reports_to_costed_party,
                "why": "whether the holder reports to a party whose "
                       "objectives the stop can cost. UNASSESSED is not NO"}

    def summary(self):
        b, r, h = self.bound_upward(), self.reversal_record(), self.holder()
        return {"facility": self.facility,
                "binding": b["state"],
                "tested": b["tested"],
                "highest_bound": self.highest_bound,
                "holder_level": self.holder_level,
                "reversals": r["state"],
                "named_holder": h["a_named_position_holds_it"],
                "reversible_against": h["someone_to_reverse_against"],
                "conflict": self.holder_reports_to_costed_party,
                "functioning": None,
                "why_functioning_is_none":
                    "FUNCTIONING is not a value this module returns. An "
                    "untested authority is untested; a tested one has a "
                    "binding record to read directly. Collapsing both into "
                    "a single functioning flag is the move the whole "
                    "instrument exists to refuse"}


# --- facilities ------------------------------------------------------------

PRIOR_ART = Authority(
    facility="prior art: SWA as core program element",
    holder_kind="EVERYONE",
    holder_level="PEER",
    highest_bound="NONE",
    stops_executed=0,
    reversals=None,
    holder_reports_to_costed_party="UNASSESSED",
    note="~10 years, no stop recalled. Evidence offered of function: workers "
         "reported having CONVERSATIONS about safety. Published as working")

NAMED_UNTESTED = Authority(
    facility="named holder, stops only at peer level",
    holder_kind="NAMED_POSITION",
    named_position="line safety officer",
    holder_level="SUPERVISOR",
    highest_bound="PEER",
    stops_executed=4,
    reversals=None,
    holder_reports_to_costed_party="YES")

NAMED_BOUND_UP = Authority(
    facility="named holder, one stop bound at executive level",
    holder_kind="NAMED_POSITION",
    named_position="line safety officer",
    holder_level="SUPERVISOR",
    highest_bound="EXECUTIVE",
    stops_executed=6,
    reversals=[{"by": "plant manager", "note": "one stop reversed"}],
    holder_reports_to_costed_party="YES")

FACILITIES = [PRIOR_ART, NAMED_UNTESTED, NAMED_BOUND_UP]


def prior_art_readout():
    """Every axis the spec names, against the documented case."""
    a = PRIOR_ART
    s = a.summary()
    gap = SA.PUBLISHED.diagnose()
    return {"summary": s,
            "count_diagnosis": gap["state"],
            "evidence_offered": "workers reported having CONVERSATIONS "
                                "about safety",
            "conversations_are_a_measurement": False,
            "why_conversations_do_not_count":
                "a conversation is not a stop attempted, not a stop honored "
                "and not a reviewed warranted state. It is not one of the "
                "three numbers, and offering it as evidence of function "
                "substitutes an activity for a measurement",
            "axes_that_returned_a_measurement": [],
            "verdict": "UNTESTED_ON_EVERY_AXIS",
            "why": "no stop executed, so nothing bound and nothing was "
                   "reversed; authority in everyone, so no named holder and "
                   "nobody to reverse against; conflict unassessed; and no "
                   "review denominator, so the count is INDISTINGUISHABLE. "
                   "Published as working, with every axis empty"}


def confidence():
    return {"the_facilities": "one delivered case and two stipulated "
                              "contrasts. The contrasts exist to show the "
                              "axes moving and are not observations",
            "UNTESTED": "returned wherever the authority has produced no "
                        "trial. It is not a soft HOLLOW and not a soft "
                        "FUNCTIONING",
            "functioning": "never returned. There is no such field on the "
                           "summary, by construction",
            "distribution": "the structural facts are recorded and the "
                            "expansion-or-contraction grade is not made. The "
                            "spec says MAY, and which it is depends on a "
                            "facility this module does not measure",
            "conflict_axis": "carried as declared. Nothing here checks a "
                             "reporting line, and UNASSESSED is not NO",
            "resolved": False}


def breaks():
    return [
        "THE DOCUMENTED CASE RETURNS UNTESTED ON EVERY AXIS AND THAT IS THE "
        "WHOLE READOUT. No stop executed, so nothing bound and no reversal "
        "record to read; authority located in everyone, so no named position "
        "holds it and there is nobody to reverse against; conflict "
        "unassessed; no review denominator, so the count is "
        "INDISTINGUISHABLE. Published as working with every axis empty. The "
        "instrument does not say the authority was hollow -- it says the "
        "published claim rested on nothing it could read",
        "'CONVERSATIONS ABOUT SAFETY' IS NOT ON ANY AXIS, AND THE MODULE CAN "
        "ONLY SAY THAT. It is not a stop attempted, not a stop honored, not "
        "a reviewed warranted state, and not a binding event. Recording that "
        "it fails to be a measurement is different from establishing that "
        "the conversations did nothing, and nothing here does the second",
        "UNTESTED_ABOVE IS RETURNED BY A COMPARISON OF TWO DECLARED LEVELS "
        "AND BOTH ARE SUPPLIED BY WHOEVER FILLS THE RECORD. highest_bound "
        "and holder_level are inputs, so a facility that files its holder at "
        "PEER makes any supervisor-level stop read as upward binding. The "
        "ordering is real and the placement in it is a declaration",
        "THE MODULE REFUSES TO GRADE DISTRIBUTION AND THAT REFUSAL HAS A "
        "COST. It records that authority in everyone has no identified "
        "holder and nobody to reverse against, then declines to say whether "
        "that is contraction. A reader wanting a verdict gets two structural "
        "facts and no number, which is correct under the spec's MAY and is "
        "less useful than the verdict would be if the verdict were earned",
        "NOTHING HERE MEASURES A FACILITY. Two of the three rows are "
        "stipulated to make the axes move, and the third is the operator's "
        "documented case carried without independent check. The instrument "
        "is a set of refusals with a worked example, not a survey",
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
    L = ["STOP AUTHORITY -- what it can bind", "=" * 72, ""]
    L.append("  Authority is defined by what it can bind, not by who")
    L.append("  holds it. A stop authority that has never bound upward")
    L.append("  has not been tested. Untested is not the same as")
    L.append("  functioning.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  %-30s %-20s %s" % ("facility", "binding", "tested"))
    for a in FACILITIES:
        s = a.summary()
        L.append("  %-30s %-20s %s"
                 % (a.facility[:30], s["binding"], s["tested"]))
    L.append("")
    L.append("  %-30s %-12s %-8s %s"
             % ("", "reversals", "named", "conflict"))
    for a in FACILITIES:
        s = a.summary()
        L.append("  %-30s %-12s %-8s %s"
                 % (a.facility[:30], s["reversals"], s["named_holder"],
                    s["conflict"]))
    L.append("")
    L.append("  functioning: %s on every row -- there is no such field."
             % FACILITIES[0].summary()["functioning"])
    for line in _wrap(FACILITIES[0].summary()["why_functioning_is_none"],
                      "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  EACH AXIS")
    L.append("")
    for a in FACILITIES:
        L.append("  %s" % a.facility)
        for label, d in (("binds", a.bound_upward()),
                         ("reversals", a.reversal_record())):
            L.append("    %-10s %s" % (label, d["state"]))
            for line in _wrap(d["why"], "      "):
                L.append(line)
        h = a.holder()
        L.append("    %-10s %s" % ("holder", h["kind"]))
        L.append("      enforced by: %s" % h["enforced_by"])
        L.append("      someone to reverse against: %s"
                 % h["someone_to_reverse_against"])
        L.append("    %-10s %s"
                 % ("conflict", a.holder_reports_to_costed_party))
        L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  ON DISTRIBUTION -- RECORDED, NOT GRADED")
    L.append("")
    h = PRIOR_ART.holder()
    L.append("    verdict on expansion: %s" % h["verdict_on_expansion"])
    for line in _wrap(h["why_no_verdict"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE DOCUMENTED CASE")
    L.append("")
    pa = prior_art_readout()
    L.append("    evidence offered of function:")
    for line in _wrap(pa["evidence_offered"], "      "):
        L.append(line)
    L.append("")
    L.append("    is that a measurement? %s"
             % pa["conversations_are_a_measurement"])
    for line in _wrap(pa["why_conversations_do_not_count"], "      "):
        L.append(line)
    L.append("")
    L.append("    axes returning a measurement: %d"
             % len(pa["axes_that_returned_a_measurement"]))
    L.append("    count diagnosis:              %s" % pa["count_diagnosis"])
    L.append("    VERDICT:                      %s" % pa["verdict"])
    L.append("")
    for line in _wrap(pa["why"], "    "):
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
        Authority("x", "NAMED_POSITION", "PEER", named_position=None)
        ok = False
    except BindingError:
        ok = True
    ck("a NAMED_POSITION holder must name the position -- otherwise it is "
       "the everyone case wearing a label", ok)

    b = PRIOR_ART.bound_upward()
    ck("with no stops, nothing has been bound and nothing refused",
       b["state"] == "NO_STOPS_AT_ALL" and b["tested"] is False)
    ck("stops only at peer level read UNTESTED_ABOVE, not failing",
       NAMED_UNTESTED.bound_upward()["state"] == "UNTESTED_ABOVE"
       and NAMED_UNTESTED.bound_upward()["tested"] is False)
    ck("and a stop above the holder's level is the one tested case",
       NAMED_BOUND_UP.bound_upward()["state"] == "BOUND_ABOVE_HOLDER"
       and NAMED_BOUND_UP.bound_upward()["tested"] is True)
    ck("UNTESTED and FUNCTIONING are not the same value, because "
       "FUNCTIONING is not a value",
       all(a.summary()["functioning"] is None for a in FACILITIES))
    ck("and the summary says why there is no such field",
       "refuse" in PRIOR_ART.summary()["why_functioning_is_none"])

    ck("no stops means the reversal record is NOT_LOOKED, not clean",
       PRIOR_ART.reversal_record()["state"] == "NOT_LOOKED")
    ck("stops with no reversals is NONE_FOUND, a different fact",
       NAMED_UNTESTED.reversal_record()["state"] == "NONE_FOUND")
    ck("and a recorded reversal names who reversed it",
       NAMED_BOUND_UP.reversal_record()["state"] == "FOUND"
       and NAMED_BOUND_UP.reversal_record()["reversals"][0]["by"]
       == "plant manager")

    h = PRIOR_ART.holder()
    ck("authority in everyone has no named holder",
       h["a_named_position_holds_it"] is False)
    ck("and nobody to be reversed against",
       h["someone_to_reverse_against"] is False
       and h["enforced_by"] == "no identified holder")
    ck("the expansion-or-contraction grade is NOT made: the spec says MAY",
       h["verdict_on_expansion"] is None)
    ck("a named position does give someone to reverse against",
       NAMED_UNTESTED.holder()["someone_to_reverse_against"] is True)

    ck("UNASSESSED on the conflict axis is not NO",
       PRIOR_ART.conflict()["holder_reports_to_costed_party"] == "UNASSESSED"
       and "not NO" in PRIOR_ART.conflict()["why"])

    pa = prior_art_readout()
    ck("the documented case returns a measurement on no axis",
       len(pa["axes_that_returned_a_measurement"]) == 0
       and pa["verdict"] == "UNTESTED_ON_EVERY_AXIS")
    ck("conversations are not a measurement on any of the three numbers",
       pa["conversations_are_a_measurement"] is False)
    ck("and the count side agrees it is INDISTINGUISHABLE, not hollow",
       pa["count_diagnosis"] == "INDISTINGUISHABLE")
    ck("the module does not claim the authority was hollow",
       "does not say the authority was hollow" in breaks()[0])

    ck("the every-axis-empty result leads the breaks list",
       "UNTESTED ON EVERY AXIS" in breaks()[0])
    ck("the declared-levels limit is disclosed",
       any("placement in it is a declaration" in b for b in breaks()))
    ck("the cost of refusing to grade distribution is disclosed",
       any("REFUSES TO GRADE DISTRIBUTION" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "RECORDED, NOT GRADED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="stop authority binding")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
