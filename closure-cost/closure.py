#!/usr/bin/env python3
"""
CLOSURE COST
Reads recorded cases where a variable was closed before the event arrived.
Stdlib only.

The shape under test: response failure tracks whether a variable was carried
as live, not whether the event was severe and not whether information about
it was available. A variable closed as impossible has no handling class
attached to it, because none was ever needed. When the event fires, the delay
is not reaction time. It is categorisation — the reading is refused because
it contradicts something held as permanent.

TWO BRANCHES, kept apart because they close different things.

  instrument   a reliable intermediary exists and becomes the reading. The
               underlying quantity stops being sampled directly. Failure
               clusters where the intermediary has been correct for a long
               time, which is the inverse of how reliability is usually
               scored.

  event        the event itself is closed as not-happening-here. Procedure
               for it is never acquired, or acquired and not retained,
               because it attaches to something rated impossible.

Both are closure. One closes a reading, the other closes an occurrence. A
case that mixes them is recorded as mixed rather than forced into one.

THE RIVAL EXPLANATION, and why it is recorded rather than dismissed.

Missing procedure is the obvious competing account of non-response. It is
not independent: nobody acquires a protocol for an event they have closed.
So procedure absence can be a downstream readout of the closed prior rather
than an alternative to it. That collapse is not automatic. It is asserted
per case, with the ground stated, and the field records which.

What separates them is INFORMATION AVAILABILITY. If the information was
absent, procedure gap stands on its own. If the information was present —
and especially if a local documented instance of the event existed and was
publicly memorialised — then availability is ruled out and the procedure
gap needs a different explanation.

KNOWLEDGE STATE is three failures, not one:

  not_taught              never delivered
  taught_not_retained     delivered, did not attach
  retained_not_executed   present, not run under load
  not_separable           the record cannot tell them apart

They have different signatures and different remedies. Most disaster
self-report cannot separate them, and the field says so rather than guessing.

DIAGNOSTIC SPEND is the quantity from the operating side: time spent
establishing what class of event this is, over time available before action
had to be taken. A ratio at or above 1 means the whole budget went to
categorisation. Recorded only where both numbers are in the source.

No verdict is emitted. Every readout is a property of the record.

Usage:
  closure.py                  table over cases/
  closure.py --case NAME      detail
  closure.py --branch NAME    cases on one branch
  closure.py --new NAME       blank skeleton
  closure.py --jsonl
  closure.py --selftest
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASEDIR = os.path.join(HERE, "cases")

INSTRUMENT = "instrument"
EVENT = "event"
MIXED = "mixed"
BRANCHES = (INSTRUMENT, EVENT, MIXED)

CLOSED = "closed"
LIVE_LOW = "live_low"
NOT_ASSESSED = "not_assessed"
VARIABLE_STATES = (CLOSED, LIVE_LOW, NOT_ASSESSED)

ABSENT = "absent"
PRESENT = "present"
PRESENT_LOCAL = "present_local_instance"
AVAILABILITY = (ABSENT, PRESENT, PRESENT_LOCAL, None)

NOT_TAUGHT = "not_taught"
TAUGHT_NOT_RETAINED = "taught_not_retained"
RETAINED_NOT_EXECUTED = "retained_not_executed"
NOT_SEPARABLE = "not_separable"
KNOWLEDGE = (NOT_TAUGHT, TAUGHT_NOT_RETAINED, RETAINED_NOT_EXECUTED,
             NOT_SEPARABLE)


def load(path=CASEDIR):
    out = []
    if not os.path.isdir(path):
        return out
    for f in sorted(os.listdir(path)):
        if f.endswith(".json"):
            with open(os.path.join(path, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def score(c):
    lat = c.get("latency", {}) or {}
    diag = lat.get("diagnostic_seconds")
    budget = lat.get("budget_seconds")
    spend = None
    if isinstance(diag, (int, float)) and isinstance(budget, (int, float)) \
            and budget > 0:
        spend = round(diag / budget, 3)

    avail = c.get("information_availability")
    var = c.get("variable_state")
    # availability only rules the procedure gap out when the information was
    # there to be had and the variable was closed anyway. a local documented
    # instance is the strong form: the event is not abstract, it happened
    # here, and it is memorialised.
    rules_out = bool(avail in (PRESENT, PRESENT_LOCAL) and var == CLOSED)

    rival = c.get("procedure_gap", {}) or {}
    collapsed = rival.get("collapsed_into_closure")

    sig = c.get("signal", {}) or {}
    return {
        "case": c.get("case"),
        "branch": c.get("branch"),
        "variable_state": var,
        "information_availability": avail,
        "availability_rules_out_procedure_gap": rules_out,
        "availability_is_local_instance": avail == PRESENT_LOCAL,
        "knowledge_state": c.get("knowledge_state"),
        "knowledge_separable": c.get("knowledge_state") != NOT_SEPARABLE,
        "signal_present": sig.get("present"),
        "signal_relied_on": sig.get("relied_on_as_reading"),
        "signal_reliability_record": sig.get("years_correct"),
        "diagnostic_spend": spend,
        "budget_consumed": None if spend is None else spend >= 1.0,
        "procedure_gap_collapsed": collapsed,
        "collapse_ground": rival.get("ground"),
        "source_class": c.get("source_class"),
        "self_report": c.get("self_report"),
        "open": c.get("open", []),
    }


def fmt(x):
    if x is None:
        return "--"
    if x is True:
        return "yes"
    if x is False:
        return "no"
    if isinstance(x, float):
        return "%.2f" % x
    return str(x)


def wrap(t, w, ind=""):
    words, lines, cur = str(t).split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > w:
            lines.append(ind + cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(ind + cur)
    return lines


def table(scores):
    hdr = (f"{'case':<24}{'branch':>12}{'var':>14}{'info':>8}"
           f"{'rules':>7}{'spend':>7}{'sep':>5}")
    print(hdr)
    print("-" * len(hdr))
    for s in scores:
        info = {PRESENT_LOCAL: "local", PRESENT: "yes", ABSENT: "no"}.get(
            s["information_availability"], "--")
        print(f"{str(s['case'])[:24]:<24}{str(s['branch']):>12}"
              f"{str(s['variable_state']):>14}{info:>8}"
              f"{fmt(s['availability_rules_out_procedure_gap']):>7}"
              f"{fmt(s['diagnostic_spend']):>7}"
              f"{fmt(s['knowledge_separable']):>5}")
    print()
    print("var    was the variable carried live before the event")
    print("info   was information about the event available. local = a")
    print("       documented instance in the same place, memorialised")
    print("rules  availability rules out the procedure-gap rival")
    print("spend  time spent categorising / time available. >=1 means the")
    print("       whole budget went to working out what this was")
    print("sep    can the record separate not-taught from not-retained")
    print("       from not-executed")
    print()
    print("No case here quantifies the mechanism. These are properties of")
    print("the records, and the records were not built to ask this.")


def detail(s):
    print("CASE      %s" % s["case"])
    print("BRANCH    %s" % s["branch"])
    print("VARIABLE  %s" % s["variable_state"])
    print()
    print("INFORMATION AVAILABILITY  %s" % s["information_availability"])
    if s["availability_is_local_instance"]:
        print("  A documented local instance existed. Information")
        print("  availability is ruled out as the explanation.")
    print("KNOWLEDGE STATE           %s" % s["knowledge_state"])
    if not s["knowledge_separable"]:
        print("  The record cannot separate the three failures.")
    print()
    if s["signal_present"] is not None:
        print("SIGNAL")
        print("  present            %s" % fmt(s["signal_present"]))
        print("  relied on          %s" % fmt(s["signal_relied_on"]))
        print("  years correct      %s" % fmt(s["signal_reliability_record"]))
        print()
    print("DIAGNOSTIC SPEND  %s" % fmt(s["diagnostic_spend"]))
    if s["budget_consumed"]:
        print("  Categorisation consumed the entire action budget.")
    print()
    print("PROCEDURE GAP RIVAL")
    print("  collapsed into closure  %s" % fmt(s["procedure_gap_collapsed"]))
    if s["collapse_ground"]:
        for line in wrap(s["collapse_ground"], 56, "  "):
            print(line)
    print()
    print("SOURCE    %s   self-report: %s"
          % (s["source_class"], fmt(s["self_report"])))
    print()
    for o in s["open"]:
        print("OPEN")
        for line in wrap(o, 58, "    "):
            print(line)
        print()


SKELETON = {
    "case": "", "branch": EVENT, "variable_state": NOT_ASSESSED,
    "information_availability": None,
    "knowledge_state": NOT_SEPARABLE,
    "signal": {"present": None, "relied_on_as_reading": None,
               "years_correct": None},
    "latency": {"diagnostic_seconds": None, "budget_seconds": None,
                "note": ""},
    "procedure_gap": {"collapsed_into_closure": None, "ground": ""},
    "source_class": "", "self_report": None, "open": []
}


def selftest():
    a = score({
        "case": "a", "branch": EVENT, "variable_state": CLOSED,
        "information_availability": PRESENT_LOCAL,
        "knowledge_state": NOT_TAUGHT,
        "latency": {"diagnostic_seconds": 900, "budget_seconds": 900},
        "procedure_gap": {"collapsed_into_closure": True, "ground": "g"},
        "self_report": True})
    b = score({
        "case": "b", "branch": INSTRUMENT, "variable_state": NOT_ASSESSED,
        "information_availability": ABSENT,
        "knowledge_state": NOT_SEPARABLE,
        "signal": {"present": True, "relied_on_as_reading": True,
                   "years_correct": 30},
        "latency": {"diagnostic_seconds": 30, "budget_seconds": 120}})
    empty = score({"case": "e"})
    checks = [
        ("local instance flagged", a["availability_is_local_instance"]),
        ("availability rules out rival",
         a["availability_rules_out_procedure_gap"] is True),
        ("absent info does not rule out rival",
         b["availability_rules_out_procedure_gap"] is False),
        ("spend ratio computed", a["diagnostic_spend"] == 1.0),
        ("full budget flagged", a["budget_consumed"] is True),
        ("partial budget not flagged", b["budget_consumed"] is False),
        ("spend none without budget", empty["diagnostic_spend"] is None),
        ("budget flag none not false", empty["budget_consumed"] is None),
        ("knowledge separable true", a["knowledge_separable"] is True),
        ("not_separable detected", b["knowledge_separable"] is False),
        ("collapse carried with ground",
         a["procedure_gap_collapsed"] is True and a["collapse_ground"] == "g"),
        ("collapse none when unstated",
         b["procedure_gap_collapsed"] is None),
        ("signal fields absent stay none", a["signal_present"] is None),
        ("branches distinct", a["branch"] != b["branch"]),
        ("no verdict field", not any(
            k in a for k in ("verdict", "confirmed", "mechanism_shown"))),
    ]
    ok = 0
    for n, r in checks:
        print(("PASS" if r else "FAIL"), n)
        ok += bool(r)
    print("\n%d/%d" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--new" in a:
        i = a.index("--new")
        sk = json.loads(json.dumps(SKELETON))
        sk["case"] = a[i + 1] if len(a) > i + 1 else "unnamed"
        print(json.dumps(sk, indent=2))
        return
    scores = [score(c) for c in load()]
    if "--jsonl" in a:
        for s in scores:
            print(json.dumps(s))
        return
    if "--case" in a:
        want = a[a.index("--case") + 1]
        for s in scores:
            if s["case"] == want:
                detail(s)
                return
        print("no case named %s" % want, file=sys.stderr)
        sys.exit(1)
    if "--branch" in a:
        want = a[a.index("--branch") + 1]
        table([s for s in scores if s["branch"] == want])
        return
    table(scores)


if __name__ == "__main__":
    main()
