#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
stop_authority.py - a count of zero, and the two states it is consistent with.

    python3 stop_authority.py [--selftest]

Marker under exploration. Delivered spec: SPEC_STOP_AUTHORITY.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

THE PROBLEM, AS DELIVERED. "Stop work authority exists" is evidenced by policy
text and by stop COUNT. Both are unsigned. A count of zero is consistent with
two opposite states:

    A. no condition warranted a stop
    B. the authority is not honored, so none were attempted

Published cases treat zero as evidence of A. Nothing in the measurement
distinguishes them. A worker who knows a stop will not be honored does not
attempt one -- so under B, non-use is produced BY the hollowness, and reads as
safety.

THIS MODULE DOES NOT FLIP THE ERROR. Treating zero as evidence of B would be
the same mistake pointing the other way. Every readout here returns
INDISTINGUISHABLE where the record cannot separate them, and the whole point
is which extra number would.

WHAT THE THREE NUMBERS EACH BUY, AND WHERE EACH ONE DIES.
  1  stops ATTEMPTED, not executed -- including reversed, discouraged, or
     resolved informally before recording.
  2  honored / attempted. The ratio is the authority measurement; the count
     alone is not.
  3  warranted-in-review: of incidents that occurred, how many had a prior
     state where a stop was warranted and available, determined by review
     rather than by whether anyone called it.

At zero attempts, (1) and (2) are both degenerate -- the ratio is 0/0, which
is not 1.0 and not 0.0 -- so (3) is the ONLY live measurement left. That is
the spec's "denominator the other two are missing", made exact: the two
numbers that look like the authority measurement are the two that go blind
first, and they go blind precisely in the state that most needs measuring.

THE MEASUREMENT EXTINGUISHES ITS OWN DENOMINATOR. Attempts respond to the
honor rate workers have observed. A low honor rate drives attempts toward
zero; at zero attempts the ratio is undefined; with no ratio there is no
measurement; and the stop count -- still the published evidence -- reads
cleaner every year. `suppression_run()` runs that loop. It is a stipulated
model of a stated mechanism, not evidence that any facility behaved this way.

RELATED, AND NOT INDEPENDENT OF IT. extraction-blindness-sim already builds
"absence of an error signal read as confirmation of safety" on a physical
substrate. This is the same reading error with an extra loop the extraction
case does not have: there the sensor merely fails to see the damage, here the
hollowness CAUSES the silence, so the zero is not just uninformative but
anti-correlated with the thing it is read as evidence for. Same builder, same
repo: by operator-structure-echo/corroboration.py the agreement between these
two folders is INHERITED, not found.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

STATES = ("A_NO_CONDITION_WARRANTED", "B_NOT_HONORED_SO_NONE_ATTEMPTED",
          "INDISTINGUISHABLE")


class Record(object):
    """What a facility's stop-work record contains.

    Every field defaults to None, meaning NOT COLLECTED. Zero is a
    measurement; None is the absence of one, and the spec's whole subject is
    that these get confused.
    """

    def __init__(self, name, years=None, stops_executed=None,
                 stops_attempted=None, warranted_in_review=None,
                 incidents=None, note=None):
        self.name = name
        self.years = years
        self.stops_executed = stops_executed
        self.stops_attempted = stops_attempted
        self.warranted_in_review = warranted_in_review
        self.incidents = incidents
        self.note = note

    def honor_ratio(self):
        """honored / attempted. Refused at zero attempts, and at not-collected.

        0/0 is not 1.0 and it is not 0.0. A facility with no attempts has not
        demonstrated that its authority is honored OR that it is hollow, and
        returning either number would manufacture the finding.
        """
        a, h = self.stops_attempted, self.stops_executed
        if a is None or h is None:
            return {"ratio": None, "state": "NOT_COLLECTED",
                    "why": "attempts or honors were never recorded. That is "
                           "not the same as their being zero"}
        if a == 0:
            return {"ratio": None, "state": "UNDEFINED_NO_ATTEMPTS",
                    "why": "0/0. The ratio is the authority measurement and "
                           "it has no value here, which is a different "
                           "statement from the authority being perfect or "
                           "being hollow"}
        return {"ratio": h / a, "state": "MEASURED",
                "why": "honored over attempted, over %d attempts" % a}

    def attempt_rate(self):
        """attempted / warranted-in-review. The spec's missing denominator."""
        a, w = self.stops_attempted, self.warranted_in_review
        if w is None:
            return {"rate": None, "state": "NO_DENOMINATOR",
                    "why": "warranted-in-review was never determined, so "
                           "attempts float free of the hazard rate and "
                           "nothing anchors them"}
        if a is None:
            return {"rate": None, "state": "NOT_COLLECTED",
                    "why": "attempts were never recorded"}
        if w == 0:
            return {"rate": None, "state": "UNDEFINED_NO_WARRANTED",
                    "why": "no reviewed incident had a prior state where a "
                           "stop was warranted and available. With no "
                           "hazard to respond to, an attempt rate has no "
                           "denominator -- and this is the one reading "
                           "consistent with state A"}
        return {"rate": a / w, "state": "MEASURED",
                "why": "attempted over warranted, over %d warranted" % w}

    def diagnose(self):
        """Which of A and B the record supports. Usually neither."""
        hr, ar = self.honor_ratio(), self.attempt_rate()
        w, a = self.warranted_in_review, self.stops_attempted
        if w is None:
            state, why = "INDISTINGUISHABLE", (
                "without warranted-in-review there is no denominator, and "
                "the stop count is consistent with both states. This is the "
                "published case: zero read as A")
        elif w == 0:
            state, why = "A_NO_CONDITION_WARRANTED", (
                "review found no incident with a prior state where a stop "
                "was warranted and available. This is what evidence for A "
                "looks like, and it comes from the review, never from the "
                "count")
        elif a == 0:
            state, why = "B_NOT_HONORED_SO_NONE_ATTEMPTED", (
                "review found %d warranted-and-available prior states and "
                "not one stop was attempted. The hazard was there and the "
                "authority produced nothing" % w)
        elif hr["state"] == "MEASURED" and hr["ratio"] < 0.5:
            state, why = "B_NOT_HONORED_SO_NONE_ATTEMPTED", (
                "stops were attempted against %d warranted states and "
                "honored at %.2f. The authority is being exercised and not "
                "binding" % (w, hr["ratio"]))
        else:
            state, why = "INDISTINGUISHABLE", (
                "attempts and honors are present but do not separate the "
                "two states on their own")
        return {"facility": self.name, "state": state, "why": why,
                "stops_executed": self.stops_executed,
                "honor_ratio": hr, "attempt_rate": ar,
                "warranted_in_review": w,
                "count_alone_would_say": _count_reading(self.stops_executed)}


def _count_reading(n):
    """What the published practice reads off the count alone."""
    if n is None:
        return "no count published"
    if n == 0:
        return "zero stops -- read as evidence of A (no condition warranted)"
    return "%d stop%s -- read as the authority functioning" % (
        n, "" if n == 1 else "s")


# --- three facilities, and what the count sees ------------------------------

SAFE = Record("A: genuinely low hazard", years=10, stops_executed=0,
              stops_attempted=0, warranted_in_review=0, incidents=3)

HOLLOW_SILENT = Record("B: hollow, fully suppressed", years=10,
                       stops_executed=0, stops_attempted=0,
                       warranted_in_review=12, incidents=12)

HOLLOW_NOISY = Record("C: hollow, partly suppressed", years=10,
                      stops_executed=1, stops_attempted=5,
                      warranted_in_review=12, incidents=11)

PUBLISHED = Record(
    "prior art: SWA as core program element", years=10,
    stops_executed=0, stops_attempted=None, warranted_in_review=None,
    incidents=None,
    note="safety manager cannot recall a single stop in ~10 years. Evidence "
         "offered of function: workers reported having CONVERSATIONS about "
         "safety. Zero attempts, zero honors, no review denominator. "
         "Published as working")

FACILITIES = [SAFE, HOLLOW_SILENT, HOLLOW_NOISY, PUBLISHED]


def count_is_uninformative():
    """A and B produce an identical published record, and C ranks above both.

    The stop count does not merely fail to separate A from B. It orders the
    three facilities in a way that is unrelated to the health of the
    authority: the partly-hollow facility, where stops are attempted and
    mostly refused, publishes MORE stops than the genuinely safe one.
    """
    rows = [(f.name, f.stops_executed) for f in
            (SAFE, HOLLOW_SILENT, HOLLOW_NOISY)]
    return {
        "rows": rows,
        "A_and_B_identical": SAFE.stops_executed == HOLLOW_SILENT.stops_executed,
        "C_outranks_A": HOLLOW_NOISY.stops_executed > SAFE.stops_executed,
        "ordering_by_count": [n for n, _ in sorted(rows, key=lambda r: -r[1])],
        "why": "the count separates none of them usefully. A and B are "
               "identical at zero, and C -- where the authority is being "
               "refused in practice -- publishes the highest number of the "
               "three",
    }


def what_each_number_buys():
    """Which of the three numbers is live in which state.

    At zero attempts the ratio is 0/0 and the attempt count is zero on both
    sides, so warranted-in-review is the only number left that moves.
    """
    out = []
    for f in (SAFE, HOLLOW_SILENT):
        hr, ar = f.honor_ratio(), f.attempt_rate()
        out.append({"facility": f.name,
                    "stops_executed": f.stops_executed,
                    "stops_attempted": f.stops_attempted,
                    "honor_ratio_state": hr["state"],
                    "warranted_in_review": f.warranted_in_review,
                    "attempt_rate_state": ar["state"]})
    separated_by = []
    a, b = out[0], out[1]
    for key in ("stops_executed", "stops_attempted", "warranted_in_review"):
        if a[key] != b[key]:
            separated_by.append(key)
    return {"rows": out, "separated_by": separated_by,
            "n_separating": len(separated_by),
            "why": "numbers 1 and 2 are degenerate at zero attempts -- the "
                   "ratio is 0/0 in both facilities and the attempt count is "
                   "zero in both. Only warranted-in-review differs, which is "
                   "why the spec calls it the denominator the other two are "
                   "missing"}


# --- the loop that eats the denominator ------------------------------------

def suppression_run(steps=10, warranted_per_step=3, honor_rate=0.15,
                    initial_propensity=1.0, learning=0.55):
    """Attempts respond to the honor rate workers have observed.

    Deterministic, no rng. Propensity is the share of warranted states a
    worker will attempt a stop in; it moves toward the observed honor rate.
    A low honor rate drives attempts down, attempts drive the denominator of
    the ratio down, and at zero the measurement stops existing while the
    published stop count reads cleaner every year.

    Stipulated model of a stated mechanism. Not evidence about any facility.
    """
    propensity = initial_propensity
    rows = []
    cum_attempts = cum_honored = cum_warranted = 0
    for t in range(steps):
        attempts = int(round(warranted_per_step * propensity))
        honored = int(attempts * honor_rate)
        cum_attempts += attempts
        cum_honored += honored
        cum_warranted += warranted_per_step
        observed = (honored / attempts) if attempts else None
        rows.append({
            "t": t + 1,
            "warranted": warranted_per_step,
            "attempts": attempts,
            "honored": honored,
            "propensity": propensity,
            "observed_honor": observed,
            "ratio_state": "MEASURED" if attempts else
                           "UNDEFINED_NO_ATTEMPTS",
            "cum_stops_published": cum_honored,
        })
        if attempts:
            propensity = max(0.0, propensity
                             - learning * (propensity - honor_rate))
        else:
            propensity = max(0.0, propensity)
    silent_from = None
    for r in rows:
        if r["attempts"] == 0:
            silent_from = r["t"]
            break
    tail = [r for r in rows if r["attempts"] == 0]
    return {
        "rows": rows,
        "went_silent_at": silent_from,
        "steps_with_no_measurement": len(tail),
        "hazard_unchanged": len(set(r["warranted"] for r in rows)) == 1,
        "warranted_total": cum_warranted,
        "stops_published_total": cum_honored,
        "final_ratio_state": rows[-1]["ratio_state"],
        "why": "the hazard rate never moves. Attempts fall because the "
               "honor rate is low, and once attempts reach zero the ratio "
               "has no denominator. The published stop count stops rising, "
               "which under the count-alone reading is the record improving",
    }


def confidence():
    return {"the_three_facilities": "stipulated, to show what the count can "
                                    "and cannot separate. They are not "
                                    "observations of anywhere",
            "the_prior_art_row": "delivered by the operator as a documented "
                                 "case and carried without independent "
                                 "check. What this module does with it is "
                                 "run it through the instrument, not verify "
                                 "it",
            "the_suppression_run": "a stipulated model of a stated "
                                   "mechanism. It shows the loop is "
                                   "arithmetically available given a "
                                   "learning rule and a low honor rate, and "
                                   "shows nothing about any real facility",
            "the_learning_rule": "propensity moves toward the observed "
                                 "honor rate at a fixed rate. That shape "
                                 "was chosen, not measured, and a different "
                                 "shape moves when silence arrives but not "
                                 "whether it does",
            "the_verdicts": "A is reachable only from the review "
                            "denominator. Where that is absent the module "
                            "returns INDISTINGUISHABLE and does not lean",
            "resolved": False}


def breaks():
    return [
        "THE COUNT DOES NOT MERELY FAIL TO SEPARATE A FROM B -- IT RANKS THE "
        "PARTLY-HOLLOW FACILITY ABOVE THE SAFE ONE. A and B both publish "
        "zero. C, where stops are attempted and refused four times in five, "
        "publishes one. Read as 'the authority is being used', C looks like "
        "the healthiest of the three and is the one demonstrably not "
        "binding. The count is not a weak signal here, it is ordered "
        "against the thing it is read as evidence for",
        "THE TWO NUMBERS THAT LOOK LIKE THE AUTHORITY MEASUREMENT GO BLIND "
        "FIRST, AND THEY GO BLIND IN THE STATE THAT MOST NEEDS MEASURING. At "
        "zero attempts the ratio is 0/0 and the attempt count is zero on "
        "both sides, so the only field separating A from B is "
        "warranted-in-review -- which is the one determined by post-incident "
        "review rather than by anything the authority itself produces. The "
        "measurement that works is the one outside the mechanism",
        "THIS MODULE CANNOT SAY THE PRIOR-ART CASE WAS HOLLOW, AND DOES NOT. "
        "Ten years, zero recalled stops, evidence offered being conversations "
        "-- and no attempts recorded and no review denominator, so the "
        "instrument returns INDISTINGUISHABLE. That is the whole finding: "
        "not that the authority was hollow, but that 'published as working' "
        "was not supported by anything in the record. Reading it as B would "
        "be the published error pointing the other way",
        "THE SUPPRESSION RUN IS A DEMONSTRATION AND ITS LEARNING RULE IS "
        "INVENTED. Propensity moves toward the observed honor rate at a "
        "fixed fraction per step. That produces silence at t=6 with these "
        "numbers; a different rule moves the arrival time and not the "
        "existence of the fixed point. Nothing here measures how workers "
        "actually update, and the honor rate of 0.15 was chosen to make the "
        "collapse legible within ten steps",
        "WARRANTED-IN-REVIEW IS ITSELF A JUDGEMENT MADE AFTER THE FACT BY "
        "PARTIES WHO MAY BE THE SAME ONES THE STOP WOULD HAVE COST. The spec "
        "says it is determined by post-incident review rather than by "
        "whether anyone called it, which removes the worker's suppressed "
        "judgement from the denominator and replaces it with a reviewer's. "
        "Nothing in this module checks who reviews, and a review conducted "
        "by the party a stop binds against is the same structure one level "
        "up",
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
    L = ["STOP-AUTHORITY INSTRUMENTATION GAP -- what a zero is consistent "
         "with", "=" * 72, ""]
    L.append("  A count of zero is consistent with two opposite states:")
    L.append("    A. no condition warranted a stop")
    L.append("    B. the authority is not honored, so none were attempted")
    L.append("")
    L.append("  Under B, non-use is produced BY the hollowness, and reads")
    L.append("  as safety.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  WHAT THE COUNT SEES")
    L.append("")
    ci = count_is_uninformative()
    L.append("    %-34s %s" % ("facility", "stops published"))
    for name, n in ci["rows"]:
        L.append("    %-34s %d" % (name, n))
    L.append("")
    L.append("    A and B identical:  %s" % ci["A_and_B_identical"])
    L.append("    C outranks A:       %s" % ci["C_outranks_A"])
    L.append("")
    for line in _wrap(ci["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  WHICH NUMBER IS LIVE AT ZERO ATTEMPTS")
    L.append("")
    wb = what_each_number_buys()
    L.append("    %-30s %-9s %-9s %s"
             % ("", "executed", "attempted", "warranted"))
    for r in wb["rows"]:
        L.append("    %-30s %-9s %-9s %s"
                 % (r["facility"][:30], r["stops_executed"],
                    r["stops_attempted"], r["warranted_in_review"]))
    L.append("")
    L.append("    honor ratio in both: %s" % wb["rows"][0]["honor_ratio_state"])
    L.append("    fields separating A from B: %s"
             % ", ".join(wb["separated_by"]))
    L.append("")
    for line in _wrap(wb["why"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  EACH FACILITY, DIAGNOSED")
    L.append("")
    for f in FACILITIES:
        d = f.diagnose()
        L.append("  %s" % f.name)
        L.append("    count alone would say:")
        for line in _wrap(d["count_alone_would_say"], "      "):
            L.append(line)
        L.append("    honor ratio:  %s" % d["honor_ratio"]["state"])
        L.append("    attempt rate: %s" % d["attempt_rate"]["state"])
        L.append("    VERDICT:      %s" % d["state"])
        for line in _wrap(d["why"], "      "):
            L.append(line)
        L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE MEASUREMENT EATS ITS OWN DENOMINATOR")
    L.append("")
    sr = suppression_run()
    L.append("    %-5s %-10s %-9s %-9s %-11s %s"
             % ("t", "warranted", "attempts", "honored", "propensity",
                "ratio"))
    for r in sr["rows"]:
        L.append("    %-5d %-10d %-9d %-9d %-11.3f %s"
                 % (r["t"], r["warranted"], r["attempts"], r["honored"],
                    r["propensity"],
                    "MEASURED" if r["attempts"] else "UNDEFINED"))
    L.append("")
    L.append("    hazard unchanged throughout:  %s" % sr["hazard_unchanged"])
    L.append("    went silent at t = %s" % sr["went_silent_at"])
    L.append("    warranted states total:       %d" % sr["warranted_total"])
    L.append("    stops published total:        %d"
             % sr["stops_published_total"])
    L.append("")
    for line in _wrap(sr["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    %d warranted-and-available prior states produced %d"
             % (sr["warranted_total"], sr["stops_published_total"]))
    L.append("    published stops, with the hazard rate constant.")
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

    ck("0/0 is refused: not 1.0, not 0.0",
       SAFE.honor_ratio()["ratio"] is None
       and SAFE.honor_ratio()["state"] == "UNDEFINED_NO_ATTEMPTS")
    ck("and a not-collected field is a different state from a zero one",
       PUBLISHED.honor_ratio()["state"] == "NOT_COLLECTED")
    ck("a real ratio is computed when attempts exist",
       abs(HOLLOW_NOISY.honor_ratio()["ratio"] - 0.2) < 1e-9)

    ci = count_is_uninformative()
    ck("A and B publish an identical count", ci["A_and_B_identical"])
    ck("and the partly-hollow facility outranks the safe one on count",
       ci["C_outranks_A"] is True)
    ck("so the count ordering puts C first", ci["ordering_by_count"][0]
       == "C: hollow, partly suppressed")

    wb = what_each_number_buys()
    ck("at zero attempts, exactly one field separates A from B",
       wb["n_separating"] == 1)
    ck("and it is warranted-in-review, the review denominator",
       wb["separated_by"] == ["warranted_in_review"])
    ck("the honor ratio is undefined in BOTH, so it separates nothing",
       all(r["honor_ratio_state"] == "UNDEFINED_NO_ATTEMPTS"
           for r in wb["rows"]))

    ck("A is diagnosed only from a review denominator of zero",
       SAFE.diagnose()["state"] == "A_NO_CONDITION_WARRANTED")
    ck("B is diagnosed from warranted states with no attempts",
       HOLLOW_SILENT.diagnose()["state"]
       == "B_NOT_HONORED_SO_NONE_ATTEMPTED")
    ck("C is diagnosed from a low honor ratio over real attempts",
       HOLLOW_NOISY.diagnose()["state"]
       == "B_NOT_HONORED_SO_NONE_ATTEMPTED")
    ck("and the published prior-art case is INDISTINGUISHABLE, not hollow",
       PUBLISHED.diagnose()["state"] == "INDISTINGUISHABLE")
    ck("which is the finding: 'published as working' was unsupported, not "
       "disproved",
       "consistent with both states" in PUBLISHED.diagnose()["why"])
    ck("the count-alone reading of zero is recorded as evidence-of-A",
       "read as evidence of A" in PUBLISHED.diagnose()["count_alone_would_say"])

    sr = suppression_run()
    ck("the hazard rate never moves", sr["hazard_unchanged"] is True)
    ck("attempts reach zero and stay there",
       sr["went_silent_at"] is not None
       and sr["rows"][-1]["attempts"] == 0)
    ck("after which the ratio has no denominator, permanently",
       sr["final_ratio_state"] == "UNDEFINED_NO_ATTEMPTS")
    ck("warranted states accumulate while published stops do not",
       sr["warranted_total"] == 30 and sr["stops_published_total"] == 0)
    ck("attempts fall monotonically, which is the loop",
       all(sr["rows"][i]["attempts"] >= sr["rows"][i + 1]["attempts"]
           for i in range(len(sr["rows"]) - 1)))

    ck("the count-ranks-C-above-A result leads the breaks list",
       "RANKS THE" in breaks()[0])
    ck("refusing to call the prior-art case hollow is disclosed",
       any("CANNOT SAY THE PRIOR-ART CASE WAS HOLLOW" in b
           for b in breaks()))
    ck("the invented learning rule is disclosed",
       any("LEARNING RULE IS" in b for b in breaks()))
    ck("who conducts the review being unchecked is disclosed",
       any("who reviews" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "EATS ITS OWN DENOMINATOR" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="stop-authority gap")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
