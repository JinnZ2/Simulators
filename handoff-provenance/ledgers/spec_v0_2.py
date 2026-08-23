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
            "resolved": False}


def breaks():
    return [
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
        L.append("  [%-3s] %s" % (e["tag"], e["text"]))
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
    ck("the split-into-lines judgement is disclosed first",
       "THIS FILE'S JUDGEMENT" in breaks()[0])
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
