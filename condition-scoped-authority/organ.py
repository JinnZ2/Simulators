#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
organ.py - the coordinating organ is a specialization, not a rank.

    python3 organ.py [--selftest]

Marker under exploration. Delivered spec: SPEC_CONDITION_SCOPE.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE ORGAN ERROR. "The coordinating organ is not senior to the others. It is a
different organ, which cannot do what they do and cannot sense what they
sense." That is a structural claim and it is checkable: if the coordinator's
sense channels were a superset of the others', it WOULD be a rank. `Organ`
refuses to build a coordinator that senses everything, because such a thing is
a hierarchy written in anatomy vocabulary.

FAILURE 1 -- REASSIGNMENT BY DECREE. Instructing the hand to be a foot does
not produce a degraded system, it produces a non-functioning one, and the
distinction is not rhetorical. An organ reassigned to a task whose sense
channel it does not have cannot read the input at all, so there is no partial
performance to degrade from: output is exactly zero, not a fraction. And the
failure lands downstream, where the decree cannot observe it -- the
coordinator's own signals are unchanged, because the coordinator is still
coordinating.

FAILURE 2 -- MEASUREMENT. Scoring only the coordinating organ and reporting
the result as the whole system's capacity. This is the THIRD instance in this
repo of one shape: measure a subset, report it as the whole. The safety metric
rising while the facility degrades is the same move, and so is the narrow
stop count. Recorded as one shape recurring, not as three findings -- by
operator-structure-echo/corroboration.py, agreement between three modules by
one builder is INHERITED.

The spec adds that failure 2 is "the same error as the centralized-executive
prior in consciousness and intelligence rubrics. Org chart and measurement
instrument, one shape." That claim about rubrics is carried and not tested:
this module has no rubric corpus and does not pretend to one.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys


class OrganError(Exception):
    pass


class Organ(object):
    def __init__(self, name, senses, acts, is_coordinator=False):
        if not senses or not acts:
            raise OrganError(
                "an organ with no sense channel or no act channel is not an "
                "organ. %s" % name)
        self.name = name
        self.senses = set(senses)
        self.acts = set(acts)
        self.is_coordinator = is_coordinator

    def can_perform(self, task):
        """Needs both the sense channel and the act channel for the task."""
        return (task["needs_sense"] in self.senses
                and task["needs_act"] in self.acts)

    def output(self, task):
        """Zero when the sense channel is absent. Not a reduced fraction.

        There is no partial reading of an input the organ cannot detect, so
        there is nothing for a degradation to start from.
        """
        if task["needs_sense"] not in self.senses:
            return {"output": 0.0, "state": "CANNOT_SENSE_THE_INPUT",
                    "why": "the organ has no channel for %s. It is not "
                           "performing the task badly, it is not receiving "
                           "the task" % task["needs_sense"]}
        if task["needs_act"] not in self.acts:
            return {"output": 0.0, "state": "CANNOT_ACT",
                    "why": "the organ reads the input and has no channel to "
                           "act on it"}
        return {"output": 1.0, "state": "PERFORMS", "why": "both channels"}


class Body(object):
    """Organs, tasks, and one coordinator that is not senior to them."""

    def __init__(self, organs, tasks):
        coords = [o for o in organs if o.is_coordinator]
        if len(coords) != 1:
            raise OrganError("exactly one coordinating organ is expected")
        c = coords[0]
        others = [o for o in organs if not o.is_coordinator]
        all_other_senses = set()
        for o in others:
            all_other_senses |= o.senses
        if all_other_senses <= c.senses:
            raise OrganError(
                "the coordinator senses everything the others sense, which "
                "makes it a rank rather than an organ. Coordination is a "
                "specialization: it must have channels the others lack AND "
                "lack channels they have")
        if not (c.senses - all_other_senses):
            raise OrganError(
                "the coordinator has no sense channel of its own, so it is "
                "not a different organ, it is a subset")
        self.organs = list(organs)
        self.coordinator = c
        self.others = others
        self.tasks = list(tasks)
        self.assignment = dict((t["name"], t["organ"]) for t in tasks)

    def by_name(self, name):
        for o in self.organs:
            if o.name == name:
                return o
        raise OrganError("no organ %r" % name)

    def run(self, assignment=None):
        a = assignment or self.assignment
        rows = []
        for t in self.tasks:
            organ = self.by_name(a[t["name"]])
            r = organ.output(t)
            rows.append({"task": t["name"], "organ": organ.name,
                         "output": r["output"], "state": r["state"],
                         "why": r["why"], "downstream": t["downstream"]})
        total = sum(r["output"] for r in rows)
        return {"rows": rows,
                "system_capacity": total / len(rows) if rows else 0.0,
                "functioning": all(r["output"] > 0 for r in rows),
                "n_zero": sum(1 for r in rows if r["output"] == 0.0)}


# --- the body --------------------------------------------------------------

HAND = Organ("hand", senses=["touch", "grip_slip"], acts=["grasp"])
FOOT = Organ("foot", senses=["ground_contact", "balance"], acts=["push_off"])
COORD = Organ("coordinator", senses=["timing", "sequence"],
              acts=["schedule"], is_coordinator=True)

TASKS = [
    {"name": "hold the tool", "needs_sense": "grip_slip",
     "needs_act": "grasp", "organ": "hand", "downstream": True},
    {"name": "stay upright", "needs_sense": "balance",
     "needs_act": "push_off", "organ": "foot", "downstream": True},
    {"name": "order the steps", "needs_sense": "sequence",
     "needs_act": "schedule", "organ": "coordinator", "downstream": False},
]

BODY = Body([HAND, FOOT, COORD], TASKS)


def decree_reassign(organ_from="hand", organ_to="foot"):
    """Instruct one organ to do another's task. What actually happens.

    The decree is issued at the coordinator, and the coordinator's own task
    is untouched. The failure is downstream of where the decree can look.
    """
    a = dict(BODY.assignment)
    target = [t["name"] for t in TASKS if t["organ"] == organ_to
              and t["downstream"]]
    if not target:
        raise OrganError("no downstream task belongs to %r" % organ_to)
    a[target[0]] = organ_from
    before = BODY.run()
    after = BODY.run(a)
    coord_rows_before = [r for r in before["rows"] if not r["downstream"]]
    coord_rows_after = [r for r in after["rows"] if not r["downstream"]]
    coord_unchanged = ([r["output"] for r in coord_rows_before]
                       == [r["output"] for r in coord_rows_after])
    return {
        "decree": "%s performs the task of %s" % (organ_from, organ_to),
        "task_reassigned": target[0],
        "before_capacity": before["system_capacity"],
        "after_capacity": after["system_capacity"],
        "before_functioning": before["functioning"],
        "after_functioning": after["functioning"],
        "degraded_or_nonfunctioning":
            "NON_FUNCTIONING" if not after["functioning"] else "DEGRADED",
        "failed_task_output": [r["output"] for r in after["rows"]
                               if r["task"] == target[0]][0],
        "failed_task_state": [r["state"] for r in after["rows"]
                              if r["task"] == target[0]][0],
        "coordinator_signal_unchanged": coord_unchanged,
        "observable_at_the_decree": not coord_unchanged,
        "why": "the reassigned organ has no sense channel for the task, so "
               "its output is exactly zero rather than reduced. The "
               "coordinator's own task is unaffected, so the signal visible "
               "where the decree was issued does not move",
    }


def coordinator_only_score():
    """Failure 2: score the coordinator, report it as the system."""
    run = BODY.run()
    coord = [r for r in run["rows"] if not r["downstream"]]
    dec = decree_reassign()
    a = dict(BODY.assignment)
    target = dec["task_reassigned"]
    a[target] = "hand"
    broken = BODY.run(a)
    broken_coord = [r for r in broken["rows"] if not r["downstream"]]
    return {
        "healthy_system_capacity": run["system_capacity"],
        "healthy_coordinator_score": sum(r["output"] for r in coord)
                                     / len(coord),
        "broken_system_capacity": broken["system_capacity"],
        "broken_coordinator_score": sum(r["output"] for r in broken_coord)
                                    / len(broken_coord),
        "coordinator_score_moved": (sum(r["output"] for r in coord)
                                    != sum(r["output"]
                                           for r in broken_coord)),
        "system_capacity_moved": run["system_capacity"]
                                 != broken["system_capacity"],
        "why": "the coordinator scores the same in both bodies. Reporting "
               "that score as the system's capacity reports a number that "
               "does not move when the system stops working",
        "same_shape_as": ["stop-authority: the narrow safety metric rising "
                          "while the facility degrades",
                          "stop-authority: the stop count read as the "
                          "authority measurement"],
        "counted_as": "ONE_SHAPE_RECURRING_NOT_THREE_FINDINGS",
    }


# --- OPEN WORK -------------------------------------------------------------
# "Unknown whether BOUND authority survives anywhere outside regulated
# domains (nuclear, aviation, protective detail). If it survives only where a
# regulator forced it, that is itself the finding."

REGULATED_DOMAINS = ["nuclear", "aviation", "protective detail"]


def bound_outside_regulation():
    """The population that would answer it, and how many rows are in it.

    The question needs instances of BOUND authority in UNREGULATED domains.
    Zero are recorded here, and zero-with-no-search is NOT_SEARCHED. The
    spec's conditional finding requires an absence established by looking.
    """
    unregulated_instances = []
    return {
        "regulated_domains_named": list(REGULATED_DOMAINS),
        "n_unregulated_instances": len(unregulated_instances),
        "instances": unregulated_instances,
        "state": "NOT_SEARCHED",
        "finding": None,
        "why": "the finding the spec names -- that BOUND survives only where "
               "a regulator forced it -- is an absence, and an absence needs "
               "a search behind it. None has been conducted. Zero rows here "
               "is the size of the search, not the size of the population",
        "what_would_make_it_a_finding":
            "a search of unregulated domains that looked for BOUND "
            "authority and reported where it looked, so that a zero carries "
            "a denominator",
    }


OPEN_WORK = [
    {"item": "restore scope-partition to a structure already collapsed to "
             "rank",
     "state": "NO_METHOD_PROPOSED",
     "note": "the spec lists it open and nothing here closes it. The "
             "collapse removes the condition column; nothing in this module "
             "puts one back"},
    {"item": "does BOUND authority survive outside regulated domains",
     "state": "NOT_SEARCHED",
     "note": "zero unregulated instances recorded, and zero without a "
             "search is NOT_SEARCHED rather than ABSENT"},
    {"item": "if it survives only where a regulator forced it, that is the "
             "finding",
     "state": "CONDITIONAL_ON_THE_ABOVE",
     "note": "the conditional is well-formed and its antecedent is "
             "unestablished, so the consequent is not available"},
]


def averaging_hides_it():
    """The aggregate reads as a shortfall; the system is not working.

    A mean over tasks turns one organ at exactly zero into a 33% dip. The
    number that says NON_FUNCTIONING is the per-task zero, and it is the one
    the average removes.
    """
    d = decree_reassign()
    return {"system_capacity_after": d["after_capacity"],
            "reads_as": "a %.0f%% shortfall"
                        % ((1 - d["after_capacity"]) * 100),
            "actually": d["degraded_or_nonfunctioning"],
            "failed_task_output": d["failed_task_output"],
            "why": "the mean is over tasks, and one task at exactly zero "
                   "averages into a fraction. Degraded and non-functioning "
                   "differ in whether any required channel is absent, which "
                   "is a property of the worst task and not of the mean"}


def confidence():
    return {"the_body": "three organs and three tasks, stipulated. It shows "
                        "what follows from sense channels being distinct, "
                        "and is not a model of anatomy or of any "
                        "organisation",
            "the_zero": "structural, not tuned. An organ with no channel for "
                        "an input scores zero because there is nothing to "
                        "score, and no parameter here sets it",
            "failure_2": "the third instance of one shape in this repo, "
                         "recorded as recurrence rather than as a new "
                         "result",
            "the_rubric_claim": "the spec's link to the centralized-executive "
                                "prior in consciousness and intelligence "
                                "rubrics is carried and NOT tested. This "
                                "module has no rubric corpus",
            "resolved": False}


def breaks():
    return [
        "THE COORDINATOR'S SCORE DOES NOT MOVE AT ALL BETWEEN A WORKING BODY "
        "AND A BROKEN ONE. Healthy system capacity 1.00 with a coordinator "
        "score of 1.00; after the decree, system capacity 0.67 and the "
        "coordinator score still 1.00. Reporting the coordinator as the "
        "system does not give a biased estimate of capacity, it gives a "
        "number with zero sensitivity to it -- the measurement cannot fail, "
        "which is what makes it attractive",
        "AND THE AVERAGE IS ITSELF THE DEGRADATION ILLUSION. System capacity "
        "reads 0.67, which presents as a 33% shortfall. The system is "
        "NON_FUNCTIONING: one task is at exactly zero because the organ "
        "assigned has no channel for the input. Degraded and non-functioning "
        "differ in whether a required channel is absent, which is a property "
        "of the worst task and precisely what a mean removes",
        "THE DECREE CANNOT OBSERVE ITS OWN CONSEQUENCE, AND THAT IS "
        "STRUCTURAL RATHER THAN A REPORTING LAPSE. The coordinator's task is "
        "untouched by the reassignment, so the signal visible where the "
        "decree was issued does not move. No amount of attention at that "
        "point reveals the failure; the failure is in a channel the "
        "coordinator does not have, which is why it was reassignable in the "
        "first place",
        "THIS IS THE THIRD INSTANCE OF ONE SHAPE AND IT IS NOT THREE "
        "FINDINGS. Measure a subset, report it as the whole: the narrow "
        "safety metric rising while the facility degrades, the stop count "
        "read as the authority measurement, and now the coordinator score "
        "read as system capacity. One repo, one builder. By "
        "operator-structure-echo/corroboration.py that agreement is "
        "INHERITED, and counting it three times would be the error that "
        "register exists to catch",
        "THE LINK TO CONSCIOUSNESS AND INTELLIGENCE RUBRICS IS CARRIED, NOT "
        "TESTED. The spec says failure 2 is the same error as the "
        "centralized-executive prior in those rubrics, and that org chart "
        "and measurement instrument are one shape. It is a claim about a "
        "literature this module has no access to. Nothing here supports it "
        "and nothing here contradicts it",
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
    L = ["THE ORGAN ERROR -- coordination is a specialization, not a rank",
         "=" * 72, ""]
    L.append("  %-14s %-28s %s" % ("organ", "senses", "acts"))
    for o in BODY.organs:
        L.append("  %-14s %-28s %s"
                 % (o.name + (" *" if o.is_coordinator else ""),
                    ", ".join(sorted(o.senses)), ", ".join(sorted(o.acts))))
    L.append("")
    L.append("  * the coordinator. It has channels the others lack AND")
    L.append("    lacks channels they have -- a coordinator that sensed")
    L.append("    everything would be a rank, and Body refuses to build one.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  FAILURE 1 -- REASSIGNMENT BY DECREE")
    L.append("")
    d = decree_reassign()
    L.append("    decree: %s" % d["decree"])
    L.append("    task reassigned: %s" % d["task_reassigned"])
    L.append("")
    L.append("    %-26s %-10s %s" % ("", "capacity", "functioning"))
    L.append("    %-26s %-10.2f %s"
             % ("before", d["before_capacity"], d["before_functioning"]))
    L.append("    %-26s %-10.2f %s"
             % ("after", d["after_capacity"], d["after_functioning"]))
    L.append("")
    L.append("    verdict: %s" % d["degraded_or_nonfunctioning"])
    L.append("    the reassigned task outputs %.1f -- state %s"
             % (d["failed_task_output"], d["failed_task_state"]))
    L.append("")
    for line in _wrap(d["why"], "    "):
        L.append(line)
    L.append("")
    ah = averaging_hides_it()
    L.append("    and the aggregate hides it:")
    L.append("      system capacity %.2f reads as %s"
             % (ah["system_capacity_after"], ah["reads_as"]))
    L.append("      the system is %s" % ah["actually"])
    for line in _wrap(ah["why"], "      "):
        L.append(line)
    L.append("")
    L.append("    WHERE THE DECREE CAN LOOK")
    L.append("")
    L.append("      coordinator signal unchanged: %s"
             % d["coordinator_signal_unchanged"])
    L.append("      observable at the decree:     %s"
             % d["observable_at_the_decree"])
    L.append("")
    L.append("      The failure lands downstream, in a channel the")
    L.append("      coordinator does not have -- which is why the task")
    L.append("      looked reassignable in the first place.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  FAILURE 2 -- SCORING THE COORDINATOR AS THE SYSTEM")
    L.append("")
    c = coordinator_only_score()
    L.append("    %-14s %-18s %s" % ("", "system capacity", "coordinator"))
    L.append("    %-14s %-18.2f %.2f"
             % ("healthy", c["healthy_system_capacity"],
                c["healthy_coordinator_score"]))
    L.append("    %-14s %-18.2f %.2f"
             % ("broken", c["broken_system_capacity"],
                c["broken_coordinator_score"]))
    L.append("")
    L.append("    system capacity moved:    %s" % c["system_capacity_moved"])
    L.append("    coordinator score moved:  %s" % c["coordinator_score_moved"])
    L.append("")
    for line in _wrap(c["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    same shape as, and counted as one:")
    for s in c["same_shape_as"]:
        for line in _wrap("- " + s, "      "):
            L.append(line)
    L.append("    %s" % c["counted_as"])
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  OPEN WORK")
    L.append("")
    for o in OPEN_WORK:
        for line in _wrap(o["item"], "    "):
            L.append(line)
        L.append("      -> %s" % o["state"])
    L.append("")
    b = bound_outside_regulation()
    L.append("    regulated domains named: %s"
             % ", ".join(b["regulated_domains_named"]))
    L.append("    unregulated instances recorded: %d"
             % b["n_unregulated_instances"])
    L.append("    state: %s      finding: %s" % (b["state"], b["finding"]))
    L.append("")
    for line in _wrap(b["why"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap("what would make it one: "
                      + b["what_would_make_it_a_finding"], "    "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b2 in breaks():
        for line in _wrap("- " + b2, "    "):
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
        Body([Organ("c", ["a", "b"], ["x"], is_coordinator=True),
              Organ("o", ["a"], ["y"])], [])
        ok = False
    except OrganError:
        ok = True
    ck("a coordinator that senses everything the others do is refused -- "
       "that is a rank, not an organ", ok)
    try:
        Body([Organ("c", ["a"], ["x"], is_coordinator=True),
              Organ("o", ["a", "b"], ["y"])], [])
        ok = False
    except OrganError:
        ok = True
    ck("and a coordinator with no channel of its own is refused too", ok)
    ck("the shipped body is buildable, so the constraint is satisfiable",
       BODY.coordinator.name == "coordinator" and len(BODY.others) == 2)

    d = decree_reassign()
    ck("the decree produces a NON_FUNCTIONING system, not a degraded one",
       d["degraded_or_nonfunctioning"] == "NON_FUNCTIONING"
       and d["after_functioning"] is False)
    ck("the reassigned task outputs exactly zero, not a reduced fraction",
       d["failed_task_output"] == 0.0)
    ck("because the organ cannot sense the input at all",
       d["failed_task_state"] == "CANNOT_SENSE_THE_INPUT")
    ck("the coordinator's own signal does not move",
       d["coordinator_signal_unchanged"] is True)
    ck("so the failure is not observable where the decree was issued",
       d["observable_at_the_decree"] is False)

    ah = averaging_hides_it()
    ck("the mean over tasks presents the failure as a shortfall",
       0 < ah["system_capacity_after"] < 1)
    ck("while the system is non-functioning",
       ah["actually"] == "NON_FUNCTIONING")
    ck("and the module says the mean is what removes the distinction",
       "not of the mean" in ah["why"])

    c = coordinator_only_score()
    ck("system capacity moves between the healthy and broken body",
       c["system_capacity_moved"] is True)
    ck("and the coordinator score does not move at all",
       c["coordinator_score_moved"] is False
       and c["healthy_coordinator_score"]
       == c["broken_coordinator_score"] == 1.0)
    ck("so scoring the coordinator gives a number with no sensitivity to "
       "the failure",
       "zero sensitivity" in breaks()[0])
    ck("this is recorded as one shape recurring, not three findings",
       c["counted_as"] == "ONE_SHAPE_RECURRING_NOT_THREE_FINDINGS"
       and len(c["same_shape_as"]) == 2)

    b = bound_outside_regulation()
    ck("no unregulated instances are recorded",
       b["n_unregulated_instances"] == 0)
    ck("and zero without a search is NOT_SEARCHED, not ABSENT",
       b["state"] == "NOT_SEARCHED" and b["finding"] is None)
    ck("the conditional finding's antecedent is unestablished",
       any(o["state"] == "CONDITIONAL_ON_THE_ABOVE" for o in OPEN_WORK))
    ck("all three open items are carried and none closed",
       len(OPEN_WORK) == 3
       and all(o["state"] != "CLOSED" for o in OPEN_WORK))

    ck("the zero-sensitivity result leads the breaks list",
       "DOES NOT MOVE AT ALL" in breaks()[0])
    ck("the averaging illusion is disclosed",
       any("DEGRADATION ILLUSION" in b2 for b2 in breaks()))
    ck("the third-instance recurrence is disclosed",
       any("THIRD INSTANCE OF ONE SHAPE" in b2 for b2 in breaks()))
    ck("the untested rubric claim is disclosed",
       any("CARRIED, NOT" in b2 for b2 in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "REASSIGNMENT BY DECREE" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="the organ error")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
