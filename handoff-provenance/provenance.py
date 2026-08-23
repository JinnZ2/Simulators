#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
provenance.py - tag vocabulary, ledger schema, and the ordering rule.

    python3 provenance.py [--selftest]

Object under test: the channel between conversation and code, not either
endpoint. Loss across that channel is currently SILENT -- a variable stated
aloud and absent from the code is indistinguishable from one never stated.

TAGS
  [K]   operator-stated, in conversation
  [K?]  operator-stated per the ledger, NOT CONFIRMED by the operator
  [R]   repo-derived; cite the path
  [C]   Claude-proposed, operator did not object
  [A]   Claude-proposed, operator ACCEPTED explicitly
  [X]   Claude Code's own addition, not in the spec

[C] and [A] are separate on purpose. Silence is not acceptance -- the same
rule as inverseminar's `unprobed` verdict, which logs a miss rather than a
confirmation.

THE ORDERING RULE. The ledger is written BEFORE the spec prose, not extracted
after. That is a claim about sequence and it is enforceable rather than
stated: `Ledger.seal()` records a hash and refuses to accept entries
afterwards, and `diff` refuses to run against an unsealed ledger. A ledger
extracted from finished prose cannot fail, which is the failure mode the rule
exists to prevent.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import hashlib
import sys

TAGS = ("K", "K?", "R", "C", "A", "X")

TAG_GLOSS = {
    "K": "operator-stated, in conversation",
    "K?": "operator-stated per the ledger, NOT CONFIRMED",
    "R": "repo-derived; path cited",
    "C": "Claude-proposed, operator did not object",
    "A": "Claude-proposed, operator ACCEPTED explicitly",
    "X": "Claude Code's own addition, not in the spec",
}

# Which tags are ground truth for the DROPPED measurement. [K?] is not:
# an unconfirmed entry may hold a mangled transcription, in which case a
# CARRIED verdict on it is not evidence of anything.
GROUND_TRUTH = ("K",)
GROUND_TRUTH_UNCONFIRMED = ("K?",)


class SchemaError(Exception):
    pass


class SealError(Exception):
    pass


def entry(text, tag, source=None, note=None):
    """One ledger line."""
    if tag not in TAGS:
        raise SchemaError("tag must be one of %s, got %r" % (TAGS, tag))
    if tag == "R" and not source:
        raise SchemaError("[R] requires a path; that is what makes it "
                          "repo-derived rather than remembered")
    if tag == "A" and not note:
        raise SchemaError("[A] requires the acceptance to be quoted or "
                          "located. Without it the entry is [C]")
    if not text or not text.strip():
        raise SchemaError("an empty ledger line is not an entry")
    return {"text": " ".join(text.split()), "tag": tag,
            "source": source, "note": note}


class Ledger(object):
    """The ground-truth column. Written before the spec prose."""

    def __init__(self, work_order):
        self.work_order = work_order
        self.entries = []
        self._sealed = None

    def add(self, text, tag, source=None, note=None):
        if self._sealed:
            raise SealError(
                "ledger sealed at %s. Adding after the seal is extraction "
                "from finished prose, which is the move the ordering rule "
                "exists to prevent" % self._sealed[:12])
        self.entries.append(entry(text, tag, source, note))
        return self

    def seal(self):
        if self._sealed:
            return self._sealed
        blob = "\n".join("%s|%s" % (e["tag"], e["text"]) for e in self.entries)
        self._sealed = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        return self._sealed

    @property
    def sealed(self):
        return self._sealed

    def by_tag(self, *tags):
        return [e for e in self.entries if e["tag"] in tags]

    def ground_truth(self):
        return self.by_tag(*GROUND_TRUTH)

    def unconfirmed(self):
        return self.by_tag(*GROUND_TRUTH_UNCONFIRMED)

    def confirm(self, index, note=None):
        """Operator confirms a [K?] entry. Allowed after sealing, because it
        changes a tag rather than adding a line -- and it is recorded."""
        e = self.entries[index]
        if e["tag"] != "K?":
            raise SchemaError("only [K?] entries are confirmable")
        e["tag"] = "K"
        e["note"] = (e["note"] or "") + (" | confirmed: %s" % note if note
                                         else " | confirmed")
        return e

    def counts(self):
        out = dict((t, 0) for t in TAGS)
        for e in self.entries:
            out[e["tag"]] += 1
        return out


def confidence():
    return {"tag_vocabulary": "a stipulation, and the [C]/[A] split is the "
                              "load-bearing part of it",
            "ordering_rule": "enforced by the seal, not stated. A ledger "
                             "extracted after the prose cannot pass",
            "K_question_handling": "[K?] entries are excluded from the "
                                   "ground-truth column, so a CARRIED "
                                   "verdict on one is not counted as "
                                   "evidence",
            "drop_rate": "UNMEASURED. the first several runs are the "
                         "baseline, by the spec's own statement",
            "resolved": False}


def breaks():
    return [
        "THE SEAL ENFORCES ORDER WITHIN ONE PROCESS, NOT ACROSS THE REAL "
        "HANDOFF. Nothing here can tell whether the ledger was written "
        "before the spec prose in the conversation that produced both -- "
        "only that entries were not added after seal() was called in this "
        "program. An operator can still write prose first and ledger second "
        "and seal honestly",
        "[K] versus [K?] is a claim about what was said, and this side of "
        "the channel has no access to the conversation upstream of a "
        "delivered spec. Every seed entry here is therefore [K?] until the "
        "operator confirms it -- which is the fourth failure mode "
        "instanced immediately, not avoided",
        "the tag is assigned by whoever writes the ledger. If that is the "
        "downstream model, [X] items can be recorded as [C] and the "
        "attribution-creep failure mode is not detectable from inside",
        "confirm() mutates a sealed ledger. That is a deliberate exception "
        "and it is the one hole in the seal: a caller could confirm every "
        "[K?] entry without asking anyone",
    ]


def report():
    L = ["HANDOFF PROVENANCE -- tags and ledger", "=" * 72, ""]
    L.append("  TAGS")
    for t in TAGS:
        L.append("    [%-3s] %s" % (t, TAG_GLOSS[t]))
    L.append("")
    L.append("  ground truth for the DROPPED measurement: %s"
             % ", ".join("[%s]" % t for t in GROUND_TRUTH))
    L.append("  excluded from it:                         %s"
             % ", ".join("[%s]" % t for t in GROUND_TRUTH_UNCONFIRMED))
    L.append("")
    L.append("  [C] and [A] are separate because silence is not acceptance.")
    L.append("  Same rule as inverseminar's `unprobed` verdict: an unprobed")
    L.append("  line is logged as a miss, never as a confirmation.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE ORDERING RULE, ENFORCED")
    L.append("")
    demo = Ledger("demo")
    demo.add("a doe selects", "K?")
    h = demo.seal()
    try:
        demo.add("added after the fact", "K?")
        after = "ACCEPTED -- the seal does not work"
    except SealError:
        after = "REFUSED"
    L.append("    seal: %s..." % h[:16])
    L.append("    add after seal: %s" % after)
    L.append("")
    L.append("    A ledger extracted from finished prose cannot fail, which")
    L.append("    is why the rule is enforced rather than stated.")
    return "\n".join(L)


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("all six tags are glossed", set(TAGS) == set(TAG_GLOSS))
    ck("[C] and [A] are distinct tags with distinct glosses",
       TAG_GLOSS["C"] != TAG_GLOSS["A"] and "not object" in TAG_GLOSS["C"]
       and "ACCEPTED" in TAG_GLOSS["A"])
    ck("[K?] is not ground truth",
       "K?" not in GROUND_TRUTH and "K?" in GROUND_TRUTH_UNCONFIRMED)

    try:
        entry("x", "Z")
        ok = False
    except SchemaError:
        ok = True
    ck("an unknown tag is refused", ok)

    try:
        entry("from a file", "R")
        ok = False
    except SchemaError:
        ok = True
    ck("[R] without a path is refused", ok)

    try:
        entry("accepted thing", "A")
        ok = False
    except SchemaError:
        ok = True
    ck("[A] without a located acceptance is refused -- it is [C] until "
       "someone can point at the acceptance", ok)

    lg = Ledger("wo")
    lg.add("first", "K?").add("second", "K")
    h = lg.seal()
    ck("sealing returns a stable hash", h == lg.seal())
    try:
        lg.add("third", "K")
        ok = False
    except SealError:
        ok = True
    ck("adding after the seal is refused", ok)

    ck("ground truth excludes the unconfirmed entry",
       len(lg.ground_truth()) == 1 and len(lg.unconfirmed()) == 1)
    lg.confirm(0, note="operator said so")
    ck("confirming a [K?] moves it into ground truth",
       len(lg.ground_truth()) == 2 and len(lg.unconfirmed()) == 0)
    ck("and the confirmation is recorded on the entry",
       "confirmed" in lg.entries[0]["note"])
    try:
        lg.confirm(1)
        ok = False
    except SchemaError:
        ok = True
    ck("confirming a non-[K?] entry is refused", ok)

    ck("the seal's within-process limit leads the breaks list",
       "WITHIN ONE PROCESS" in breaks()[0])
    ck("confirm() being a hole in the seal is disclosed",
       any("hole in the seal" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "silence is not acceptance" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="handoff provenance")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
