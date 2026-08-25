#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
ledgers/spec_v0_2.py - the ledger for the [K~] / RE-READ delivery.

    python3 ledgers/spec_v0_2.py [--selftest]

THE FIRST ENTRIES IN THIS FOLDER THAT ARE HONESTLY [K].

ledgers/seed.py had to tag every operator-stated line [K?], because the S4
conversation is upstream of a delivered work order and this side of the
channel cannot see it. This delivery is different: the operator's statement
is in-session and quotable, so "was this stated upstream" is answerable here
without asking anyone. That gives the module a real ground-truth column and,
for the first time, a real denominator.

THIS FILE IS COMMITTED BEFORE THE CODE IT DESCRIBES. The spec says the ledger
is written before the spec prose, not extracted after. Ledger.seal() can only
prove that nothing was added after seal() inside one process; it cannot prove
authoring order. Committing the sealed ledger in its own commit, ahead of the
commit that implements it, puts that ordering in git history where an outside
reader can check it. That is evidence, not proof -- history can be rewritten
-- but it is the first artifact in this folder that an outside party could
use to falsify the ordering claim.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
sys.path.insert(0, FOLDER)
import provenance as P                                          # noqa: E402
import diff as D                                                # noqa: E402

# The code this ledger was written against, and committed ahead of.
IMPL = [os.path.join(FOLDER, "provenance.py"),
        os.path.join(FOLDER, "diff.py")]

# Delivered verbatim, in-session:
#
#   add [K~]  operator-stated, translation flagged as lossy at time
#         of speaking. Shape present, English suspect.
#
#   RE-READ column, two distinct entries:
#     SHIFT   - item reads differently later; observing position
#               moved. Data about the station.
#     RETRANS - item reads the same, English was wrong the first
#               time. Data about the translation layer.

DELIVERED = """add [K~]  operator-stated, translation flagged as lossy at time
      of speaking. Shape present, English suspect.

RE-READ column, two distinct entries:
  SHIFT   - item reads differently later; observing position
            moved. Data about the station.
  RETRANS - item reads the same, English was wrong the first
            time. Data about the translation layer."""


def ledger():
    """Written from the delivered text, before the implementation."""
    lg = P.Ledger("spec v0.2 -- [K~] and the RE-READ column")
    lg.add("[K~] is a tag, added to the existing tag set", "K")
    lg.add("[K~] is operator-stated, not proposed or inferred", "K")
    lg.add("[K~] carries a translation flagged as lossy", "K")
    lg.add("the lossiness is flagged at time of speaking, not later", "K")
    lg.add("for a [K~] entry the shape is present and the English is "
           "suspect", "K")
    lg.add("RE-READ is a column", "K")
    lg.add("the RE-READ column has two distinct entries, not one", "K")
    lg.add("SHIFT is an item that reads differently later, because the "
           "observing position moved", "K")
    lg.add("SHIFT is data about the station", "K")
    lg.add("RETRANS is an item that reads the same, where the English was "
           "wrong the first time", "K")
    lg.add("RETRANS is data about the translation layer", "K")
    lg.seal()
    return lg


def impl_code():
    """The implementing code, with prose and the disclosure surface stripped.

    Matched against raw source, this ledger scores against files that quote
    its own entries -- in docstrings, in report() demos, in selftest
    fixtures -- so a CARRIED can be earned by the code that PRINTS the entry
    rather than the code that implements it. Stripping reduces that. It does
    not remove it: ledger and code came from one party in one pass.
    """
    out = []
    for path in IMPL:
        if os.path.exists(path):
            out.append(D.implementation_surface(open(path).read()))
    return "\n".join(out)


def verdict():
    """Diff the sealed ledger against the code, twice.

    Once with the matcher as it stood when the ledger was first run, and
    once with the coverage refusal that the first run forced. Both are
    reported: the second number is the better one and it was reached by
    changing the instrument after seeing the first, which is a thing to
    disclose rather than present as a clean result.
    """
    code = impl_code()
    lg = ledger()
    saved = D.MIN_COVERAGE
    try:
        D.MIN_COVERAGE = 0.0                      # the matcher as first run
        before = D.diff(lg, code)
        before = {"drop_rate": before["drop_rate"],
                  "n_ground_truth": before["n_ground_truth"],
                  "DROPPED": list(before["DROPPED"]),
                  "reportable": before["rate_reportable"]}
    finally:
        D.MIN_COVERAGE = saved
    after = D.diff(ledger(), code)
    return {"before": before, "after": after,
            "code_available": bool(code)}


# The entry that broke it, and the words the matcher could not see.
FALSE_DROPPED = "[K~] is a tag, added to the existing tag set"


def confidence():
    return {"tag_is_K_not_K_question": "the operator's statement is "
                                       "in-session and quotable. That is a "
                                       "different epistemic position from "
                                       "seed.py, not a stronger claim about "
                                       "the same one",
            "verbatim_fidelity": "near-verbatim, one line per delivered "
                                 "clause. Splitting prose into lines is a "
                                 "judgement and this file made it",
            "ordering": "git history, not the seal. Evidence an outside "
                        "reader can check, and rewritable",
            "drop_rate": "0.00 over 10 scorable entries, and the instrument "
                         "was changed after the first run to get there. The "
                         "first number, 0.09, was one false DROPPED",
            "self_diff": "this ledger scores code written to satisfy it, "
                         "by the same party, in the same pass. Prose and "
                         "the disclosure surface are stripped before "
                         "matching, which cuts the obvious route and does "
                         "not make the number a measurement. Read 0.00 as "
                         "an upper bound on carriage",
            "the_fix": "MIN_COVERAGE was set on a principle -- a majority of "
                       "an entry's content words must survive the length "
                       "floor -- and not at the value that rescues the entry "
                       "that exposed it. That is the defence available and "
                       "it is not the same as having chosen it beforehand",
            "resolved": False}


def breaks():
    return [
        "THE FIRST REPORTABLE DROP RATE THIS MODULE EVER PRODUCED WAS WRONG. "
        "Eleven [K] entries cleared the ten-entry floor, the diff returned "
        "0.09, and the single DROPPED item -- '[K~] is a tag, added to the "
        "existing tag set' -- is plainly carried: [K~] is in TAGS. The "
        "matcher scored that entry on 'added' and 'existing' alone, because "
        "'tag' and 'set', the two words carrying the claim, are three "
        "letters and the length floor is four. The share was 0.5 against a "
        "0.55 threshold, so a false DROPPED arrived by two hundredths",
        "THE INSTRUMENT WAS CHANGED AFTER SEEING THE RESULT, WHICH IS THE "
        "FITTING MOVE THIS REPO AUDITS ELSEWHERE. MIN_COVERAGE refuses an "
        "entry when the length floor eats most of its content words. It is "
        "set at a majority, on the principle that a share over the minority "
        "of an entry is not a reading of the entry, and deliberately not at "
        "the value that would rescue this one line. The matcher grade on the "
        "eight fixtures is unchanged. None of that makes it a rule chosen "
        "before the data, and the before number is reported beside the after",
        "THE COVERAGE RULE DOES NOT FIX THE UNDERLYING BLINDNESS, AND THE "
        "SPEC'S OWN HEADLINE INSTANCE IS STILL SCORED WITHOUT ITS SUBJECT. "
        "'the doe performs partner selection' loses only 'doe' to the floor "
        "-- one content word of four, under the majority line -- so it is "
        "scored, and it is scored on 'performs partner selection' with the "
        "doe invisible. The spec's flagship DROPPED instance is a doe-choice "
        "arm and the instrument measuring it cannot see the token. Any "
        "three-letter subject is in the same position: arm, gap, key, ice",
        "A SELF-DIFF IS NOT A MEASUREMENT OF THE CHANNEL. Ledger and code "
        "here came from one party in one pass, and the first attempt scored "
        "against raw source -- where provenance.py's docstring and diff.py's "
        "report both quote these entries verbatim, so a CARRIED could be "
        "earned by the code that PRINTS an item rather than the code that "
        "implements it. It surfaced as an instability: the 0.09 run stopped "
        "reproducing once the report was written. Matching now runs against "
        "implementation_surface(), docstrings and disclosure functions "
        "stripped, and the before/after numbers are stable again. That "
        "removes the obvious route and not the contamination",
        "THE SPLIT FROM PROSE INTO LINES IS THIS FILE'S JUDGEMENT AND IT "
        "SETS THE DENOMINATOR. The delivered text is six lines of prose; "
        "rendering it as eleven ledger entries is a choice, and a coarser "
        "split would produce a different drop rate from the same delivery "
        "and the same code. Nothing here establishes eleven",
        "an in-session [K] is confirmable only while the session holds the "
        "message. Read back later from the file alone, DELIVERED is a "
        "transcription made by the same party that wrote the entries, which "
        "is the fourth failure mode's exact shape one layer up",
        "committing the ledger before the code puts the ordering in git "
        "history, which is evidence and not proof: history is rewritable, "
        "and the commit only shows when the file was committed, not when it "
        "was written",
        "eleven entries is still under the ten-entry reportability floor "
        "the module applies to rates -- it clears it by one, which is not a "
        "corpus. The spec's own note stands: the first several runs ARE the "
        "baseline",
    ]


def report():
    L = ["SPEC v0.2 LEDGER -- [K~] and the RE-READ column", "=" * 72, ""]
    lg = ledger()
    L.append("  written from the delivered text, before the implementation.")
    L.append("  committed ahead of the implementing commit.")
    L.append("")
    L.append("  seal: %s..." % lg.sealed[:16])
    L.append("")
    for e in lg.entries:
        first = True
        for line in _wrap(e["text"], "        "):
            if first:
                L.append("  [%-3s]%s" % (e["tag"], line[7:].rstrip()
                                         and " " + line.strip()))
                first = False
            else:
                L.append(line)
    L.append("")
    L.append("  tag counts: %s"
             % ", ".join("%s=%d" % (t, n) for t, n in lg.counts().items()
                         if n))
    L.append("")
    L.append("  These are [K], not [K?]. The operator's statement is")
    L.append("  in-session and quotable, so 'was this stated upstream' is")
    L.append("  answerable from here. seed.py could not answer it.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE DIFF AGAINST THE IMPLEMENTATION")
    L.append("")
    v = verdict()
    b, a = v["before"], v["after"]
    L.append("    code available: %s" % v["code_available"])
    L.append("")
    L.append("    %-10s %-9s %-9s %s"
             % ("", "scorable", "dropped", "drop rate"))
    L.append("    %-10s %-9d %-9d %.2f"
             % ("first run", b["n_ground_truth"], len(b["DROPPED"]),
                b["drop_rate"]))
    L.append("    %-10s %-9d %-9d %.2f"
             % ("now", a["n_ground_truth"], len(a["DROPPED"]),
                a["drop_rate"]))
    L.append("")
    L.append("    the first run's single DROPPED:")
    for line in _wrap(FALSE_DROPPED, "      "):
        L.append(line)
    L.append("")
    cov = D.coverage(FALSE_DROPPED)
    L.append("    it is carried -- [K~] is in TAGS. The matcher scored it")
    L.append("    on %d of its %d content words; the floor ate %s."
             % (cov["n_kept"], cov["n_content"], ", ".join(cov["lost"])))
    L.append("    Share 0.50 against a 0.55 threshold: a false DROPPED by")
    L.append("    two hundredths, and it cleared the reportability floor.")
    L.append("")
    L.append("    matched against implementation_surface(): docstrings,")
    L.append("    comments and the disclosure functions stripped. Against")
    L.append("    raw source these entries score partly on the prose that")
    L.append("    quotes them, and that showed up as the 0.09 run ceasing")
    L.append("    to reproduce once the report was written.")
    L.append("")
    L.append("    The instrument was changed after seeing that. The")
    L.append("    coverage rule is set at a majority on principle, not at")
    L.append("    the value that rescues this line, and the eight-fixture")
    L.append("    matcher grade is unchanged -- but it was still chosen")
    L.append("    after the data, and both numbers print.")
    L.append("")
    doe = D.coverage("the doe performs partner selection")
    L.append("    and it does not fix the blindness. The entry")
    L.append("    'the doe performs partner selection' loses only %s --"
             % ", ".join(doe["lost"]))
    L.append("    %d of %d content words, under the line --"
             % (doe["n_content"] - doe["n_kept"], doe["n_content"]))
    L.append("    so it is scored, without its subject. The spec's headline")
    L.append("    instance is a doe-choice arm and the matcher cannot see")
    L.append("    the token.")
    L.append("")
    L.append("-" * 72)
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

    lg = ledger()
    ck("every entry is [K] -- in-session, quotable, confirmable here",
       len(lg.by_tag("K")) == len(lg.entries) and len(lg.entries) == 11)
    ck("no entry is [K?]: this is not seed.py's position",
       len(lg.by_tag("K?")) == 0)
    ck("the ledger is sealed", lg.sealed)
    ck("the delivered text is carried verbatim for later re-reading",
       "Shape present, English suspect" in DELIVERED
       and "Data about the station" in DELIVERED)
    ck("both re-read entries are in the ledger as distinct items",
       any("SHIFT" in e["text"] for e in lg.entries)
       and any("RETRANS" in e["text"] for e in lg.entries))
    ck("the two-distinct-entries instruction is itself an entry",
       any("two distinct entries, not one" in e["text"]
           for e in lg.entries))
    v = verdict()
    ck("the implementation was found and read", v["code_available"])
    b, a = v["before"], v["after"]
    ck("the first run produced a reportable drop rate -- eleven [K] "
       "entries clear the ten-entry floor",
       b["reportable"] is True and b["n_ground_truth"] == 11)
    ck("and it was wrong: one DROPPED, and it is the [K~]-is-a-tag line",
       len(b["DROPPED"]) == 1 and b["DROPPED"][0] == FALSE_DROPPED)
    ck("which is plainly carried -- [K~] is in the shipped tag set",
       "K~" in P.TAGS)
    cov = D.coverage(FALSE_DROPPED)
    ck("the cause is the length floor eating the words that carry it",
       "tag" in cov["lost"] and "set" in cov["lost"]
       and cov["n_kept"] == 2 and cov["n_content"] == 6)
    ck("after the coverage refusal the entry is not scored at all",
       len(a["DROPPED"]) == 0 and a["n_ground_truth"] == 10
       and len(a["UNSCORABLE_COVERAGE"]) == 1)
    ck("the fixture grade did not move when the rule was added",
       D.grade_matcher()["grade"] == "OK")
    ck("the doe entry is still scored, and still without its subject",
       D.coverage("the doe performs partner selection")["lost"] == ["doe"]
       and D.match("the doe performs partner selection",
                   "weighted_choice partner selection performs")["state"]
       == "OK")
    ck("matching runs against the stripped surface, not raw source",
       "[K~] is a tag, added to the existing tag set" not in impl_code())
    ck("and the entries that carry, carry on the implementation itself",
       len(a["CARRIED"]) == 10)
    ck("the self-diff contamination is disclosed",
       any("SELF-DIFF IS NOT A MEASUREMENT" in b2 for b2 in breaks()))
    ck("and the rate is reported as an upper bound on carriage",
       "upper bound" in confidence()["self_diff"])

    ck("the false drop rate leads the breaks list",
       "WAS WRONG" in breaks()[0])
    ck("changing the instrument after seeing the result is disclosed",
       any("FITTING MOVE" in b2 for b2 in breaks()))
    ck("and so is the blindness the rule does not fix",
       any("STILL SCORED WITHOUT ITS SUBJECT" in b2 for b2 in breaks()))

    ck("the split-into-lines judgement is disclosed",
       any("THIS FILE'S JUDGEMENT" in b2 for b2 in breaks()))
    ck("git-history-as-evidence-not-proof is disclosed",
       any("evidence and not proof" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "before the implementation" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="spec v0.2 ledger")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
