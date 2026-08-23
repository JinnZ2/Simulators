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
  [K~]  operator-stated, translation flagged as lossy AT TIME OF SPEAKING.
        Shape present, English suspect.
  [K?]  operator-stated per the ledger, NOT CONFIRMED by the operator
  [R]   repo-derived; cite the path
  [C]   Claude-proposed, operator did not object
  [A]   Claude-proposed, operator ACCEPTED explicitly
  [X]   Claude Code's own addition, not in the spec

[C] and [A] are separate on purpose. Silence is not acceptance -- the same
rule as inverseminar's `unprobed` verdict, which logs a miss rather than a
confirmation.

[K~] SPLITS TWO AXES THIS MODULE HAD CONFLATED. Before it, one constant --
GROUND_TRUTH -- answered two different questions at once: "is this confirmed
to have been said?" and "can the matcher be trusted on it?" For [K] and [K?]
those answers happen to move together, so a single constant worked and the
conflation was invisible. [K~] separates them, and the separation was already
needed:

  STATED           [K] [K~]   confirmed to have been said. This is the
                              population the channel is losing things from.
  MATCHER_SCORABLE [K]        the matcher reads English stems, and a [K~]
                              entry is one whose English the operator flagged
                              at the time of speaking.

A [K~] that does not match cannot be read as DROPPED, because "the English
was wrong so the stems do not match code that does implement the shape" is a
live alternative and the matcher cannot separate it from absence. So [K~]
entries are refused rather than scored -- the same repair as NEGATED, at the
translation layer instead of at the polarity of the sentence.

The gap between STATED and MATCHER_SCORABLE is the translation layer's
footprint on a ledger, and it is the only quantity here that measures it.

THE RE-READ COLUMN. An item read a second time can differ from the first
reading for two reasons that are not the same measurement:

  SHIFT     the item reads differently later; the observing position moved.
            DATA ABOUT THE STATION.
  RETRANS   the item reads the same; the English was wrong the first time.
            DATA ABOUT THE TRANSLATION LAYER.

Both produce the same observable: the ledger line's text changed. The
discriminator is whether the SHAPE moved, and that is not visible in the
text -- so `reread()` requires the kind to be operator-attributed and refuses
to infer it. Aggregating the two into one "re-read count" would produce a
number meaning "the ledger churned", which answers neither question.

They also differ in what they do to a diff already taken. Under SHIFT the
item genuinely changed, so a past CARRIED verdict was about a different item
and is stale without having been wrong. Under RETRANS the item never changed,
so a past CARRIED verdict was taken against wrong English and may have been a
FALSE carried -- which is the spec's fourth failure mode, surfacing after the
fact. RETRANS is the only route by which that failure mode ever becomes
visible in this module. It is not detection: it is the operator noticing from
upstream and reporting back down. A RETRANS count is therefore a LOWER BOUND
on voice-layer mangling, never a measurement of it.

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

TAGS = ("K", "K~", "K?", "R", "C", "A", "X")

TAG_GLOSS = {
    "K": "operator-stated, in conversation",
    "K~": "operator-stated; translation flagged lossy when spoken",
    "K?": "operator-stated per the ledger, NOT CONFIRMED",
    "R": "repo-derived; path cited",
    "C": "Claude-proposed, operator did not object",
    "A": "Claude-proposed, operator ACCEPTED explicitly",
    "X": "Claude Code's own addition, not in the spec",
}

# Two axes, separated. They were one constant until [K~] arrived, because
# for [K] and [K?] the two answers move together and the conflation does not
# show.
#
# STATED -- confirmed to have been said. The population the channel loses
# things from, and the right denominator for "did it survive".
STATED = ("K", "K~")
# MATCHER_SCORABLE -- the matcher reads English stems. A [K~] entry is one
# whose English the operator flagged at the time of speaking, so a non-match
# on it is ambiguous between absence and bad English, and it is refused.
MATCHER_SCORABLE = ("K",)

# Ground truth for the DROPPED measurement. [K?] is excluded because an
# unconfirmed entry may hold a mangled transcription; [K~] is excluded
# because the matcher cannot read it, which is a different reason.
GROUND_TRUTH = ("K",)
GROUND_TRUTH_UNCONFIRMED = ("K?",)
GROUND_TRUTH_UNSCORABLE = ("K~",)

# --- the re-read column ----------------------------------------------------
REREAD_KINDS = ("SHIFT", "RETRANS")

REREAD_GLOSS = {
    "SHIFT": "item reads differently later; observing position moved. "
             "Data about the station",
    "RETRANS": "item reads the same, English was wrong the first time. "
               "Data about the translation layer",
}

REREAD_MEASURES = {
    "SHIFT": "the station",
    "RETRANS": "the translation layer",
}

REREAD_EFFECT_ON_PRIOR_DIFF = {
    "SHIFT": "STALE_NOT_WRONG. The item changed, so a prior verdict was "
             "about a different item. Re-run the diff; the old one was not "
             "an error",
    "RETRANS": "POSSIBLY_FALSE_CARRIED. The item did not change, so a prior "
               "verdict was taken against wrong English. If it read CARRIED "
               "it may have been the fourth failure mode",
}


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
    if tag == "K~" and not note:
        raise SchemaError("[K~] requires the flag to be located: the "
                          "lossiness is flagged AT TIME OF SPEAKING, by the "
                          "operator. Without that, the entry records the "
                          "downstream model deciding the English looked "
                          "shaky, which is a different act and overrides "
                          "the operator's own confidence rather than "
                          "recording it")
    if not text or not text.strip():
        raise SchemaError("an empty ledger line is not an entry")
    return {"text": " ".join(text.split()), "tag": tag,
            "source": source, "note": note}


class Ledger(object):
    """The ground-truth column. Written before the spec prose."""

    def __init__(self, work_order):
        self.work_order = work_order
        self.entries = []
        self.rereads = []
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

    def stated(self):
        """Confirmed to have been said: the population the channel loses
        things from. Wider than the set the matcher can score."""
        return self.by_tag(*STATED)

    def scorable(self):
        """The subset the matcher can be trusted on."""
        return self.by_tag(*MATCHER_SCORABLE)

    def translation_footprint(self):
        """How much of the stated population the matcher cannot read.

        This is the only quantity in the module that measures the
        translation layer directly, and it is a count, not a rate: with
        n this small a share would read as a precision it does not have.
        """
        n_stated, n_scorable = len(self.stated()), len(self.scorable())
        return {"n_stated": n_stated,
                "n_scorable": n_scorable,
                "n_unreadable": n_stated - n_scorable,
                "share": None,
                "why_share_is_none": "a share over a handful of entries "
                                     "reads as a precision it does not "
                                     "have. The count is the readout"}

    def reread(self, index, kind, new_text, attributed_to, note=None,
               still_lossy=None):
        """Record a second reading of an entry. Two kinds, never merged.

        SHIFT and RETRANS produce the SAME observable -- the line's text
        changed. The discriminator is whether the shape moved, which is not
        in the text, so `attributed_to` is required and the kind is never
        inferred here.
        """
        if kind not in REREAD_KINDS:
            raise SchemaError(
                "re-read kind must be one of %s, got %r. SHIFT and RETRANS "
                "are separate measurements -- one is about the station, the "
                "other about the translation layer -- and there is no "
                "generic re-read that means both" % (REREAD_KINDS, kind))
        if not attributed_to:
            raise SchemaError(
                "a re-read must be attributed. SHIFT and RETRANS look "
                "identical from the text: both say the line changed. Which "
                "one it is depends on whether the SHAPE moved, and this "
                "side of the channel cannot see that")
        e = self.entries[index]
        old_text = e["text"]
        new_text = " ".join(new_text.split())
        if new_text == old_text:
            raise SchemaError(
                "the text is unchanged, so this is neither kind. SHIFT is "
                "an item reading differently; RETRANS is the same item "
                "rendered in corrected English. Both change the line. An "
                "unchanged re-read is a confirmation and is not recorded "
                "in this column")
        promoted = False
        if kind == "RETRANS" and e["tag"] == "K~" and still_lossy is False:
            e["tag"] = "K"
            promoted = True
        e["text"] = new_text
        rec = {"index": index, "kind": kind, "old_text": old_text,
               "new_text": new_text, "attributed_to": attributed_to,
               "note": note, "measures": REREAD_MEASURES[kind],
               "effect_on_prior_diff": REREAD_EFFECT_ON_PRIOR_DIFF[kind],
               "tag_promoted_to_K": promoted}
        self.rereads.append(rec)
        return rec

    def reread_counts(self):
        """Counted apart, always. A merged total answers neither question."""
        out = dict((k, 0) for k in REREAD_KINDS)
        for r in self.rereads:
            out[r["kind"]] += 1
        return out

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
            "K_tilde_handling": "[K~] is STATED but not MATCHER_SCORABLE. It "
                                "counts in the population the channel loses "
                                "things from and it is refused by the "
                                "matcher, which are two different axes that "
                                "one constant used to answer at once",
            "reread_kinds": "SHIFT and RETRANS are never summed. One is "
                            "data about the station, the other about the "
                            "translation layer, and a merged count answers "
                            "neither",
            "RETRANS_as_a_measure": "a LOWER BOUND on voice-layer mangling, "
                                    "not a measurement of it. Only the "
                                    "instances the operator happened to "
                                    "re-read and catch are ever counted",
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
        "SHIFT AND RETRANS ARE INDISTINGUISHABLE FROM THIS SIDE AND THE "
        "MODULE CANNOT CHECK THE ATTRIBUTION IT REQUIRES. Both produce one "
        "observable: the line's text changed. Which one it is depends on "
        "whether the shape moved, which lives upstream. reread() refuses an "
        "unattributed re-read, and that is the whole of its defence -- it "
        "cannot tell whether the attribution it was handed is right, so a "
        "caller who labels every re-read RETRANS produces a clean-looking "
        "station and a filthy translation layer, and nothing here objects",
        "a RETRANS on a [K~] entry does NOT promote it to [K] unless the "
        "caller passes still_lossy=False. The tempting default is to read a "
        "retranslation offered without a fresh flag as no-longer-lossy, but "
        "that reads silence as acceptance, and silence-is-not-acceptance is "
        "the rule the [C]/[A] split exists to enforce. The module applies it "
        "to itself here and the cost is that [K~] entries accumulate",
        "translation_footprint() is a count and stays a count. It reports "
        "how many stated entries the matcher cannot read, which is a "
        "property of this ledger and its flagger, not a rate for the "
        "translation layer in general. Two operators flagging differently "
        "would move it with the layer unchanged",
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
    L.append("")
    L.append("  TWO AXES, SEPARATED BY [K~]")
    L.append("")
    L.append("    STATED            %s"
             % "  ".join("[%s]" % t for t in STATED))
    L.append("      confirmed to have been said. The population the")
    L.append("      channel loses things from.")
    L.append("")
    L.append("    MATCHER_SCORABLE  %s"
             % "  ".join("[%s]" % t for t in MATCHER_SCORABLE))
    L.append("      the matcher reads English stems, and a [K~] entry is")
    L.append("      one whose English the operator flagged when speaking.")
    L.append("")
    L.append("    One constant answered both until [K~] arrived. For [K]")
    L.append("    and [K?] the two answers move together, so the")
    L.append("    conflation never showed.")
    L.append("")
    L.append("  ground truth for the DROPPED measurement: %s"
             % ", ".join("[%s]" % t for t in GROUND_TRUTH))
    L.append("  excluded, not confirmed:                  %s"
             % ", ".join("[%s]" % t for t in GROUND_TRUTH_UNCONFIRMED))
    L.append("  excluded, matcher cannot read it:         %s"
             % ", ".join("[%s]" % t for t in GROUND_TRUTH_UNSCORABLE))
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
    L.append("    A ledger extracted from finished prose cannot fail,")
    L.append("    which is why the rule is enforced rather than stated.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE RE-READ COLUMN -- TWO ENTRIES, NEVER SUMMED")
    L.append("")
    for kind in REREAD_KINDS:
        L.append("    %-9s %s" % (kind, REREAD_GLOSS[kind].split(".")[0]))
        L.append("              measures: %s" % REREAD_MEASURES[kind])
        for line in _wrap("prior diff: "
                          + REREAD_EFFECT_ON_PRIOR_DIFF[kind], " " * 14):
            L.append(line)
        L.append("")
    d2 = Ledger("reread demo")
    d2.add("the doe performs partner selection", "K")
    d2.seal()
    try:
        d2.reread(0, "SHIFT", "the doe performs partner selection",
                  attributed_to="operator")
        same = "ACCEPTED -- unchanged read as re-read"
    except SchemaError:
        same = "REFUSED (unchanged = a confirmation)"
    try:
        d2.reread(0, "SHIFT", "two does perform selection",
                  attributed_to=None)
        unattr = "ACCEPTED -- the kind was inferred"
    except SchemaError:
        unattr = "REFUSED (shape question is upstream)"
    L.append("    unchanged-text re-read: %s" % same)
    L.append("    unattributed re-read:   %s" % unattr)
    L.append("")
    L.append("    Both kinds produce ONE observable: the line changed.")
    L.append("    Which one it is depends on whether the SHAPE moved, and")
    L.append("    that is not in the text. RETRANS is the only route by")
    L.append("    which the spec's fourth failure mode ever surfaces here,")
    L.append("    and it surfaces as a LOWER BOUND, never a measurement:")
    L.append("    only what the operator re-read and caught is counted.")
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

    # --- [K~]: two axes, separated ---
    try:
        entry("shape present, English suspect", "K~")
        ok = False
    except SchemaError:
        ok = True
    ck("[K~] without a located flag is refused -- otherwise it records the "
       "downstream model doubting the English, not the operator", ok)
    e2 = entry("the doe performs partner selection", "K~",
               note="operator flagged the rendering when speaking")
    ck("[K~] with a located flag is accepted", e2["tag"] == "K~")

    kt = Ledger("k-tilde")
    kt.add("plain confirmed item", "K")
    kt.add("flagged item", "K~", note="flagged when spoken")
    kt.add("unconfirmed item", "K?")
    ck("[K~] is STATED: it counts in the population the channel loses from",
       len(kt.stated()) == 2 and "K~" in [x["tag"] for x in kt.stated()])
    ck("[K~] is NOT matcher-scorable: its English is what was flagged",
       len(kt.scorable()) == 1
       and [x["tag"] for x in kt.scorable()] == ["K"])
    ck("so the two axes disagree, which is why [K~] has to split them",
       len(kt.stated()) != len(kt.scorable()))
    tf = kt.translation_footprint()
    ck("the translation footprint is the gap between them",
       tf["n_stated"] == 2 and tf["n_scorable"] == 1
       and tf["n_unreadable"] == 1)
    ck("and it is a count, not a share, at this n", tf["share"] is None)

    # --- the re-read column ---
    rr = Ledger("rereads")
    rr.add("the doe performs partner selection", "K")
    rr.add("flagged rendering", "K~", note="flagged when spoken")
    rr.seal()
    try:
        rr.reread(0, "REREAD", "two does select", attributed_to="operator")
        ok = False
    except SchemaError:
        ok = True
    ck("there is no generic re-read kind meaning both", ok)
    try:
        rr.reread(0, "SHIFT", "the doe performs partner selection",
                  attributed_to="operator")
        ok = False
    except SchemaError:
        ok = True
    ck("an unchanged re-read is a confirmation, not a re-read event", ok)
    try:
        rr.reread(0, "SHIFT", "two does select together", attributed_to=None)
        ok = False
    except SchemaError:
        ok = True
    ck("an unattributed re-read is refused: the shape question is upstream",
       ok)

    sh = rr.reread(0, "SHIFT", "two does select together",
                   attributed_to="operator")
    ck("SHIFT measures the station, not the translation layer",
       sh["measures"] == "the station")
    ck("and it leaves a prior diff stale rather than wrong",
       sh["effect_on_prior_diff"].startswith("STALE_NOT_WRONG"))
    rt = rr.reread(1, "RETRANS", "the rendering, corrected",
                   attributed_to="operator")
    ck("RETRANS measures the translation layer, not the station",
       rt["measures"] == "the translation layer")
    ck("and it puts a prior CARRIED verdict in doubt -- the one route by "
       "which the fourth failure mode ever surfaces here",
       rt["effect_on_prior_diff"].startswith("POSSIBLY_FALSE_CARRIED"))
    ck("the two are counted apart and never summed",
       rr.reread_counts() == {"SHIFT": 1, "RETRANS": 1})
    ck("a re-read keeps the old text, since a prior diff was taken on it",
       sh["old_text"] == "the doe performs partner selection")

    ck("a RETRANS alone does NOT promote [K~] to [K]: that would read "
       "silence as acceptance, the rule the [C]/[A] split enforces",
       rr.entries[1]["tag"] == "K~" and rt["tag_promoted_to_K"] is False)
    rr2 = Ledger("promote")
    rr2.add("flagged rendering", "K~", note="flagged when spoken")
    rr2.seal()
    p2 = rr2.reread(0, "RETRANS", "the corrected rendering",
                    attributed_to="operator", still_lossy=False)
    ck("an explicit still_lossy=False does promote it, and says so",
       rr2.entries[0]["tag"] == "K" and p2["tag_promoted_to_K"] is True)

    ck("the un-checkable attribution is disclosed in breaks",
       any("INDISTINGUISHABLE FROM THIS SIDE" in b for b in breaks()))
    ck("so is the module applying silence-is-not-acceptance to itself",
       any("still_lossy=False" in b for b in breaks()))
    ck("RETRANS is reported as a lower bound, not a measurement",
       "LOWER BOUND" in confidence()["RETRANS_as_a_measure"])
    ck("the report shows both re-read entries with what each measures",
       "NEVER SUMMED" in report() and "measures: the station" in report())

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
