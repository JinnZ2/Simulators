#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
ledgers/seed.py - the seed data, and the one thing it cannot establish.

    python3 ledgers/seed.py [--selftest]

EVERY [K] SEED ENTRY HERE IS [K?], AND THAT IS THE POINT.

The spec names s4_antler_calibration's doe-choice arm as DROPPED: stated in
conversation, absent from the spec, therefore absent from the code. This side
of the channel has no access to the conversation upstream of a delivered work
order. What is verifiable from here is only that the S4 spec as received
contained no doe and the delivered patch said "was missing entirely" -- which
is consistent with DROPPED and also with never-stated, and the diff cannot
tell those apart.

So the entry lands as [K?]. That is the fourth failure mode instanced on the
first real data rather than avoided: the ledger holds a claim about what was
said, this side cannot confirm it, and treating it as [K] would produce a
DROPPED count with nothing under it.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)          # handoff-provenance/
REPO = os.path.dirname(FOLDER)          # repository root
sys.path.insert(0, FOLDER)
import provenance as P                                          # noqa: E402
import diff as D                                                # noqa: E402

# What this side CAN verify, per entry, without the upstream conversation.
VERIFIABLE_FROM_HERE = {
    "doe-choice arm": "the S4 work order as received contains no doe; the "
                      "delivered patch says 'was missing entirely'. "
                      "Consistent with DROPPED and with never-stated",
    "novelty floor": "absent from the original S4 spec, present in the "
                     "patch. Consistent with DROPPED and with never-stated, "
                     "the same way",
    "rank_prospect as a series": "absent from the original spec, present in "
                                 "the patch, and the original hardcoded "
                                 "dict is in the repo at "
                                 "instrument-bias-sims/s4_antler_"
                                 "calibration.py",
}


def s4_ledger():
    """The S4 ledger, written as the spec says: [K?] until confirmed."""
    lg = P.Ledger("s4_antler_calibration")
    lg.add("the doe performs partner selection", "K?",
           note="spec names this as the DROPPED instance")
    lg.add("novelty has a floor set by the annual delta, not a decay to "
           "zero", "K?")
    lg.add("rank_prospect is an input series with at least two arms, not a "
           "constant", "K?")
    lg.add("engagement rate proportional to expected doe access", "R",
           source="instrument-bias-sims/s4_antler_calibration.py")
    lg.add("AGENTS section comes first, missing agent a visible blank", "A",
           note="delivered patch, STRUCTURAL RULE section, stated as a rule "
                "for all future sim specs")
    lg.add("remove unused rng and statistics import", "K?")
    lg.seal()
    return lg


S4_PATH = os.path.join(REPO, "instrument-bias-sims",
                       "s4_antler_calibration.py")
S4_RAW = open(S4_PATH).read() if os.path.exists(S4_PATH) else ""
# Matched against the implementation surface -- docstrings, comments and the
# disclosure functions stripped -- so a CARRIED cannot be earned by prose
# describing the code. On this ledger the verdicts are the same either way,
# which is a robustness result and is checked rather than assumed.
S4_CODE = D.implementation_surface(S4_RAW) if S4_RAW else ""

# [X] items: this session's own additions to S4, not in the delivered patch.
S4_ADDED = [
    "GEOMETRY_DELTA as a separate term from antler mass",
    "mature-novelty reported as a fraction of the annual delta",
    "admissibility_check and RESIDENT_WRITER (added under an outside check)",
]


def run():
    lg = s4_ledger()
    d = D.diff(lg, S4_CODE, added_items=S4_ADDED)
    return {"ledger": lg, "diff": d, "code_available": bool(S4_CODE)}


def confidence():
    return {"every_K_entry": "[K?]. this side has no access to the "
                             "conversation upstream of a delivered spec",
            "what_is_verifiable": "only that an item is absent from the "
                                  "received spec and present in the patch, "
                                  "which is consistent with DROPPED and with "
                                  "never-stated",
            "drop_rate": "None. there are zero confirmed [K] entries, so "
                         "there is no denominator",
            "resolved": False}


def breaks():
    return [
        "THE SEED DATA CANNOT ESTABLISH ITS OWN HEADLINE. The spec names "
        "S4's doe-choice arm as DROPPED, and DROPPED requires that the item "
        "was stated upstream. This side cannot see upstream, so the entry is "
        "[K?] and the diff reports it in the unconfirmed column with no "
        "drop rate attached. One operator confirmation converts it; nothing "
        "else does",
        "the ledger was written AFTER the S4 code existed, which is the "
        "opposite of the ordering rule. It is seed data reconstructed from "
        "a finished artifact, and the seal proves only that nothing was "
        "added after seal() was called in this program",
        "[X] items are listed by the party that added them, which is the "
        "attribution-creep failure mode's other side: a model that forgot an "
        "addition would simply not list it, and nothing detects that",
        "THE SIXTH ENTRY BROKE THE MATCHER AND THAT IS HOW THE MATCHER GOT "
        "A NEGATION STATE. 'remove unused rng and statistics import' matched "
        "the delivered S4 code at share 1.00, its maximum, while 'import "
        "statistics' is absent from that file -- the words survive in the "
        "prose about the removal. It was reported as CARRIED at full "
        "confidence, exactly backwards. The entry is unchanged and the "
        "instrument was changed instead: it now lands in UNSCORABLE_NEGATED. "
        "One real ledger line of six was enough to invert the readout, and "
        "the eight matcher fixtures had all been positive entries",
        "ZERO RE-READS AND ZERO [K~] ON THIS LEDGER IS NOT EVIDENCE THE "
        "TRANSLATION LAYER IS CLEAN. Nothing here has been read a second "
        "time and nothing was flagged lossy when spoken, so both columns "
        "are empty for want of observation, not for want of loss. A RETRANS "
        "count is a lower bound on voice-layer mangling at the best of "
        "times; a count of zero from a ledger nobody re-read is not a bound "
        "on anything",
        "three entries, one denominator of zero. Nothing here is a rate and "
        "the spec says so: the first several runs ARE the baseline",
    ]


def report():
    L = ["SEED LEDGER -- s4_antler_calibration", "=" * 72, ""]
    r = run()
    lg, d = r["ledger"], r["diff"]
    L.append("  code available: %s" % r["code_available"])
    L.append("  ledger sealed:  %s..." % lg.sealed[:16])
    L.append("")
    L.append("  %-6s %s" % ("tag", "entry"))
    for e in lg.entries:
        L.append("  [%-3s] %s" % (e["tag"], e["text"][:60]))
    L.append("")
    L.append("  tag counts: %s"
             % ", ".join("%s=%d" % (t, n) for t, n in lg.counts().items()
                         if n))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  DIFF")
    L.append("")
    for key in ("CARRIED", "DROPPED", "CARRIED_UNCONFIRMED",
                "DROPPED_UNCONFIRMED", "UNSCORABLE_NEGATED",
                "UNSCORABLE_TRANSLATION", "UNSCORABLE_COVERAGE", "ADDED"):
        L.append("    %-22s %d" % (key, len(d[key])))
        for x in d[key]:
            L.append("      %s" % x[:64])
    L.append("")
    L.append("    drop rate      %s" % d["drop_rate"])
    L.append("    reportable     %s" % d["rate_reportable"])
    L.append("")
    for line in _wrap(d["why_rate_may_be_none"], "    "):
        L.append(line)
    L.append("")
    for line in _wrap(d["why_unscorable"], "    "):
        L.append(line)
    L.append("")
    L.append("    n_stated   %d   n_scorable %d   footprint %d"
             % (d["n_stated"], d["n_scorable"],
                d["translation_footprint"]["n_unreadable"]))
    L.append("")
    L.append("    no [K~] on this ledger and no re-reads: NOT_YET_OBSERVED,")
    L.append("    not zero. Nothing here has been read a second time, so a")
    L.append("    count of zero says nothing about the translation layer.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  WHAT THIS SIDE CAN VERIFY, PER ENTRY")
    for k2, v in sorted(VERIFIABLE_FROM_HERE.items()):
        L.append("    %s" % k2)
        for line in _wrap(v, "      "):
            L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k2 in sorted(confidence()):
        L.append("    %s" % k2)
        for line in _wrap(str(confidence()[k2]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


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


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    lg = s4_ledger()
    ck("every operator-stated seed entry is [K?], not [K]",
       len(lg.by_tag("K")) == 0 and len(lg.by_tag("K?")) > 0)
    ck("the [R] entry cites a path",
       all(e["source"] for e in lg.by_tag("R")))
    ck("the [A] entry locates its acceptance",
       all(e["note"] for e in lg.by_tag("A")))
    ck("the ledger is sealed", lg.sealed)

    r = run()
    ck("the S4 code was found and read", r["code_available"])
    d = r["diff"]
    ck("there is no confirmed ground truth, so no drop rate",
       d["drop_rate"] is None and d["n_ground_truth"] == 0)
    ck("and the unconfirmed columns are where the entries landed",
       len(d["CARRIED_UNCONFIRMED"]) + len(d["DROPPED_UNCONFIRMED"]) > 0)
    ck("ADDED is non-empty and is this session's own additions",
       len(d["ADDED"]) == 3)
    ck("the doe entry is CARRIED_UNCONFIRMED -- the patch put it in the "
       "code, and that says nothing about whether it was stated upstream",
       any("doe" in x for x in d["CARRIED_UNCONFIRMED"]))

    ck("the verdicts do not change when prose is stripped from the code -- "
       "no CARRIED here was earned by a docstring",
       [sorted(D.diff(s4_ledger(), c, added_items=S4_ADDED)[k])
        for k in ("CARRIED_UNCONFIRMED", "DROPPED_UNCONFIRMED")
        for c in (S4_RAW,)]
       == [sorted(D.diff(s4_ledger(), c, added_items=S4_ADDED)[k])
           for k in ("CARRIED_UNCONFIRMED", "DROPPED_UNCONFIRMED")
           for c in (S4_CODE,)])
    ck("no [K~] entries here, and that is NOT_YET_OBSERVED rather than a "
       "clean translation layer",
       len(s4_ledger().by_tag("K~")) == 0
       and len(d["UNSCORABLE_TRANSLATION"]) == 0)
    ck("and no re-reads: nothing has been read a second time",
       s4_ledger().reread_counts() == {"SHIFT": 0, "RETRANS": 0})

    ck("the negated entry is refused, not counted as carried",
       len(d["UNSCORABLE_NEGATED"]) == 1
       and any("remove" in x for x in d["UNSCORABLE_NEGATED"]))
    ck("and it is out of the carried column it used to sit in at share 1.00",
       not any("remove" in x for x in d["CARRIED_UNCONFIRMED"]))
    ck("the inversion it exposed is disclosed in breaks",
       any("BROKE THE MATCHER" in b for b in breaks()))

    ck("the headline the seed cannot establish leads the breaks list",
       "CANNOT ESTABLISH ITS OWN HEADLINE" in breaks()[0])
    ck("the ledger's own violation of the ordering rule is disclosed",
       any("opposite of the ordering rule" in b for b in breaks()))
    ck("every verifiable-from-here note stops short of confirming upstream",
       all("consistent with" in v.lower() or "in the repo at" in v.lower()
           for v in VERIFIABLE_FROM_HERE.values()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "WHAT THIS SIDE CAN VERIFY" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="seed ledger")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
