# SPDX-License-Identifier: CC0-1.0
"""
T1, second instrument -- THE VERB-FIRST TEST (BOUNDARY.md D6).

Rule, as supplied by the operator after `t1_predicate_unit.py` had run:

    Rewrite the main claim verb-first. If you must supply a bearer to make
    it grammatical, it's identity-bearing. If it reads without one, it's
    process.

This is an OPERATION and an OBSERVATION OF WHAT THE OPERATION FORCES. It is
not a property looked up on a noun, which is what step 3 of the first
instrument does, and which is what FINDINGS T1-1 measured at 10 of 12.

WHY THIS FILE DOES NOT REPLACE `t1_predicate_unit.py`. The rule arrived after
that instrument ran. Editing it to match would erase the disagreement between
the two, and the disagreement is the useful part. Both run; the comparison is
reported.

SIX OPTIONS, NOT TWO. The rule as stated is binary. Working the twelve-item
set by hand produced four states the binary has no room for, and two of them
are the informative ones:

    BEARER_REQUIRED   completing the residue needs a noun it does not carry
    READS_WITHOUT     residue complete, no noun wanted
    VERB_CARRIES_IT   residue complete BECAUSE the fronted verb is what the
                      subject named -- `allocation` -> `allocating`
    BOTH_READINGS     residue complete AND a bearer is natural; two readings,
                      both grammatical, and they are different claims
    NO_FRONTING       the operation could not be performed -- no main verb,
                      or a copula with a predicate nominal
    UNGRAMMATICAL     fronting yields non-English regardless of any bearer

`VERB_CARRIES_IT` is the one worth having. Under a binary it lands in
`READS_WITHOUT` and reads as a clean process framing. It is not the same
finding: it marks a claim where the carrier may have been folded into a
nominalization -- `the allocator allocates` written as `allocation proceeds`
-- and the residue alone cannot tell that from a genuinely carrier-free
claim. Collapsing it hides an identity framing wearing a noun.

`BOTH_READINGS` is the second. Under a binary it goes wherever the reader
leaned, unrecorded.

`NO_FRONTING` and `UNGRAMMATICAL` are not readings at all. They record that
the instrument produced no observation, which is not the same as observing
that no bearer is needed. Same absent-vs-known-negative rule the register
runs on.

THE JUDGEMENT IS AN INPUT. Steps 1 and 2 are mechanical and are performed
here. Step 3 is a judgement and is supplied with provenance. `score()` raises
`JudgementNotSupplied` rather than guessing.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import re
import sys

import t1_predicate_unit as t1

BEARER_REQUIRED = "BEARER_REQUIRED"
READS_WITHOUT = "READS_WITHOUT"
VERB_CARRIES_IT = "VERB_CARRIES_IT"
BOTH_READINGS = "BOTH_READINGS"
NO_FRONTING = "NO_FRONTING"
UNGRAMMATICAL = "UNGRAMMATICAL"

OPTIONS = (BEARER_REQUIRED, READS_WITHOUT, VERB_CARRIES_IT,
           BOTH_READINGS, NO_FRONTING, UNGRAMMATICAL)

# How each option maps onto the census arms. Two options map to no arm at
# all, and that is deliberate.
ARM = {
    BEARER_REQUIRED: t1.IDENTITY,
    READS_WITHOUT: t1.NONIDENTITY,
    VERB_CARRIES_IT: t1.NONIDENTITY,
    BOTH_READINGS: None,      # own arm, never folded
    NO_FRONTING: None,        # no observation made
    UNGRAMMATICAL: None,      # no observation made
}


class JudgementNotSupplied(Exception):
    """Raised when scoring is attempted without step 3."""


IRREG_ING = {
    "is": "being", "are": "being", "was": "being", "were": "being",
    "has": "having", "have": "having", "had": "having",
    "fell": "falling", "rose": "rising", "grew": "growing",
    "took": "taking", "made": "making", "led": "leading",
    "drove": "driving", "held": "holding", "went": "going",
    "ran": "running", "gave": "giving", "found": "finding",
    "became": "becoming", "remained": "remaining", "declined": "declining",
    "eroded": "eroding", "tightened": "tightening", "shrank": "shrinking",
}


# Verbs of two or more syllables that still double the final consonant,
# because the stress falls on the last syllable. Not derivable from spelling,
# so it is a list and says so.
_STRESS_FINAL = {
    "occur", "refer", "prefer", "defer", "infer", "confer", "deter",
    "begin", "forget", "regret", "admit", "permit", "commit", "submit",
    "omit", "emit", "transmit", "allot", "control", "patrol", "compel",
    "expel", "rebel", "propel", "repel", "upset", "reset", "offset",
    "prefer", "equip", "unwrap",
}

_VOWEL_GROUP = re.compile(r"[aeiouy]+")


def _doubles(stem):
    """
    English doubles a final consonant before -ing when the last syllable is
    stressed and ends consonant-vowel-consonant. Approximated: any
    monosyllable ending CVC, plus a list for the polysyllables.

    Added after `--front` emitted `seting`, `runing` and `begining`. The
    first version had no doubling rule at all, which is a defect and not a
    limit: the residues it produced were not English, and a reader asked to
    judge whether a residue needs a bearer cannot judge a residue that is
    not a sentence.
    """
    if len(stem) < 3:
        return False
    a, b, c = stem[-3], stem[-2], stem[-1]
    cvc = (a not in "aeiou" and b in "aeiou" and
           c not in "aeiouwxy")
    if not cvc:
        return False
    if len(_VOWEL_GROUP.findall(stem)) == 1:
        return True
    return stem in _STRESS_FINAL


def _to_ing(verb):
    """Mechanical, and wrong on irregulars not in the table above."""
    v = verb.lower()
    if v in IRREG_ING:
        return IRREG_ING[v]
    if v.endswith("ed") and len(v) > 3:
        stem = v[:-2]
        if stem.endswith("i"):
            stem = stem[:-1] + "y"
        return _to_ing(stem)
    if v.endswith("ies"):
        return v[:-3] + "ying"
    if v.endswith(("ses", "xes", "zes", "ches", "shes")):
        return v[:-2] + "ing"
    if v.endswith("s") and not v.endswith("ss"):
        v = v[:-1]
    if v.endswith("e") and not v.endswith(("ee", "ye", "oe")):
        return v[:-1] + "ing"
    if _doubles(v):
        return v + v[-1] + "ing"
    return v + "ing"


def front(claim):
    """
    Steps 1 and 2: take the main claim, drop the subject, front the verb.
    Returns the residue a reader is asked to judge, plus what was dropped.
    """
    c = t1.classify(claim)
    subject, verb = c["subject"], c["verb"]
    if not verb:
        return {"claim": c["claim"], "subject": subject, "verb": None,
                "residue": None, "fronted": False,
                "why": "no main verb located; step 2 cannot be performed"}
    tail = ""
    m = re.search(re.escape(verb), c["claim"] or "", re.I)
    if m:
        tail = (c["claim"] or "")[m.end():].strip()
    residue = (_to_ing(verb) + (" " + tail if tail else "")).strip()
    residue = residue.rstrip(".").strip()
    return {"claim": c["claim"], "subject": subject, "verb": verb,
            "residue": residue, "fronted": True,
            "why": "subject dropped, verb fronted"}


# --------------------------------------------------------------------------
# Step 3, supplied. Provenance is per-judgement, not per-file.
# --------------------------------------------------------------------------

JUDGE = "model, in-session, 2026-08-23, no second reader"

# What the judge actually read to answer. Added after the first scored run,
# because inspecting the residues showed that some judgements could not have
# been made from the residue -- see FINDINGS T1-7.
ON_RESIDUE = "RESIDUE"          # read step 2's output, as specified
ON_CLAIM = "CLAIM"              # read the original; step 2's output was
                                # malformed or insufficient
ON_DROPPED = "DROPPED_SUBJECT"  # read the noun step 2 deleted
READ_ON = (ON_RESIDUE, ON_CLAIM, ON_DROPPED)

JUDGEMENTS = {
    "KS-01": (BEARER_REQUIRED, "reducing investment -- reducing by whom",
              ON_CLAIM),
    "KS-02": (BEARER_REQUIRED, "declining -- declining what", ON_RESIDUE),
    "KS-03": (BOTH_READINGS,
              "consumption smoothing is a named process and reads alone; "
              "the claim also attributes the smoothing to someone",
              ON_RESIDUE),
    "KS-04": (BEARER_REQUIRED, "eroding -- eroding what", ON_RESIDUE),
    "KS-05": (BEARER_REQUIRED,
              "persisting -- and `them` has no antecedent once the subject "
              "is dropped", ON_RESIDUE),
    "KS-06": (VERB_CARRIES_IT,
              "`flux` is the flowing; the subject was already the verb",
              ON_DROPPED),
    "KS-07": (READS_WITHOUT, "stabilizing at moderate gain reads alone",
              ON_RESIDUE),
    "KS-08": (VERB_CARRIES_IT,
              "`allocation` is the allocating", ON_DROPPED),
    "KS-09": (BEARER_REQUIRED,
              "remaining unoccupied -- what remained; the state needs a "
              "thing in it", ON_RESIDUE),
    "KS-10": (VERB_CARRIES_IT,
              "`the rate of transmission` is the transmitting", ON_DROPPED),
    "KS-11": (BOTH_READINGS,
              "tightening reads alone as a process; `what tightened` is "
              "also natural", ON_RESIDUE),
    "KS-12": (READS_WITHOUT,
              "allocating scarce goods without a designer reads alone",
              ON_RESIDUE),
}


def score(items, judgements, judge=JUDGE):
    """
    items: [(id, claim), ...]. judgements: {id: (option, why)}.
    Raises rather than guessing a missing or invalid judgement.
    """
    rows = []
    for iid, claim in items:
        if iid not in judgements:
            raise JudgementNotSupplied(
                "no step-3 judgement for %r; the rule's discriminator is "
                "the judgement, so there is nothing to fall back on" % iid)
        j = judgements[iid]
        opt, why = j[0], j[1]
        read_on = j[2] if len(j) > 2 else None
        if read_on is not None and read_on not in READ_ON:
            raise ValueError("read_on must be one of %r, got %r"
                             % (READ_ON, read_on))
        if opt not in OPTIONS:
            raise ValueError("option must be one of %r, got %r"
                             % (OPTIONS, opt))
        f = front(claim)
        if opt in (NO_FRONTING, UNGRAMMATICAL) and f["fronted"] and \
                opt == NO_FRONTING:
            raise ValueError(
                "%s judged NO_FRONTING but step 2 succeeded: %r"
                % (iid, f["residue"]))
        rows.append({"id": iid, "claim": claim, "residue": f["residue"],
                     "verb": f["verb"], "option": opt, "why": why,
                     "read_on": read_on, "arm": ARM[opt], "judge": judge})
    return rows


def tally(rows):
    out = {o: 0 for o in OPTIONS}
    arms = {t1.IDENTITY: 0, t1.NONIDENTITY: 0, "own_arm": 0,
            "no_observation": 0}
    for r in rows:
        out[r["option"]] += 1
        if r["arm"] == t1.IDENTITY:
            arms[t1.IDENTITY] += 1
        elif r["arm"] == t1.NONIDENTITY:
            arms[t1.NONIDENTITY] += 1
        elif r["option"] == BOTH_READINGS:
            arms["own_arm"] += 1
        else:
            arms["no_observation"] += 1
    return out, arms


# --------------------------------------------------------------------------
# Morphological proxy. Suffix shape is a property of the token's FORM, not
# membership in a list, so it is one step less lexical than the D3 table.
# It is still not the rule, and the point of running it is to measure how
# far short it falls.
# --------------------------------------------------------------------------

NOMINALIZING = ("tion", "sion", "ment", "ance", "ence", "ity",
                "al", "ure", "age", "ing")


def proxy(claim):
    """Guess VERB_CARRIES_IT from the subject head's suffix alone."""
    c = t1.classify(claim)
    head = c["head"]
    if not head:
        return None
    h = head[:-1] if head.endswith("s") and not head.endswith("ss") else head
    for suf in NOMINALIZING:
        if h.endswith(suf) and len(h) > len(suf) + 2:
            return VERB_CARRIES_IT
    return BEARER_REQUIRED


def proxy_agreement(items, judgements):
    """Agreement between the morphological proxy and the recorded rule."""
    agree, rows = 0, []
    for iid, claim in items:
        want = judgements[iid][0]
        got = proxy(claim)
        # The proxy only distinguishes carrier-folded from bearer-needed.
        want_coarse = (VERB_CARRIES_IT if want == VERB_CARRIES_IT
                       else BEARER_REQUIRED if want == BEARER_REQUIRED
                       else None)
        ok = (want_coarse is not None and got == want_coarse)
        if ok:
            agree += 1
        rows.append((iid, want, got, ok))
    return agree, rows


ITEMS = [("KS-%02d" % i, t) for i, (t, _) in
         enumerate(t1.KNOWN_SIGNAL, 1)]


def compare(verbose=True):
    """The two instruments, item by item. No blending."""
    rows = score(ITEMS, JUDGEMENTS)
    old = {r["id"]: r for r in t1.report(
        [(i, "authored", c) for i, c in ITEMS])}
    agree = disagree = contested = 0
    lines = []
    for r in rows:
        o = old[r["id"]]
        new_arm = r["arm"]
        if r["option"] == BOTH_READINGS:
            verdict = "CONTESTED"
            contested += 1
        elif new_arm == o["label"]:
            verdict = "agree"
            agree += 1
        else:
            verdict = "DISAGREE"
            disagree += 1
        lines.append((r["id"], o["label"], o["decided_by"], r["option"],
                      verdict, r["residue"]))
    if verbose:
        print("D1/D3 instrument vs D6 verb-first test, n=%d" % len(rows))
        print("%-7s %-17s %-10s %-16s %-9s %s"
              % ("id", "D1/D3", "decided_by", "D6 option", "verdict",
                 "residue"))
        for l in lines:
            print("%-7s %-17s %-10s %-16s %-9s %s" % l)
        print()
        print("agree %d   DISAGREE %d   CONTESTED %d" %
              (agree, disagree, contested))
        by_table = [l for l in lines if l[2] == t1.BY_TABLE]
        bad = [l for l in by_table if l[4] != "agree"]
        by_pred = [l for l in lines if l[2] == t1.BY_PREDICATE]
        badp = [l for l in by_pred if l[4] != "agree"]
        print("of the %d the first instrument decided BY TABLE, %d do not "
              "agree" % (len(by_table), len(bad)))
        print("of the %d it decided BY PREDICATE, %d do not agree"
              % (len(by_pred), len(badp)))
    return {"agree": agree, "disagree": disagree, "contested": contested,
            "lines": lines}


def selftest():
    fails = []
    rows = score(ITEMS, JUDGEMENTS)
    if len(rows) != 12:
        fails.append("expected 12 scored rows, got %d" % len(rows))
    try:
        score([("MISSING", "The market cleared.")], JUDGEMENTS)
        fails.append("score() must raise on a missing judgement")
    except JudgementNotSupplied:
        pass
    try:
        score([("KS-01", ITEMS[0][1])], {"KS-01": ("NOT_AN_OPTION", "x")})
        fails.append("score() must raise on an invalid option")
    except ValueError:
        pass
    opts, arms = tally(rows)
    if opts[BOTH_READINGS] == 0:
        fails.append("BOTH_READINGS unused -- the sixth option would be "
                     "unearned")
    if opts[VERB_CARRIES_IT] == 0:
        fails.append("VERB_CARRIES_IT unused -- the option this file argues "
                     "for would be unearned")
    if arms["own_arm"] != opts[BOTH_READINGS]:
        fails.append("BOTH_READINGS must not be folded into an arm")
    f = front("Populations declined across all sampled sites.")
    if not f["fronted"] or not f["residue"].startswith("declining"):
        fails.append("fronting failed on the worked D6 example: %r"
                     % (f["residue"],))
    f2 = front("Allocation proceeds without any central coordinator.")
    if not f2["residue"].startswith("proceeding"):
        fails.append("fronting failed on the second D6 example: %r"
                     % (f2["residue"],))
    # Known answers for the doubling rule. A residue that is not English
    # cannot be judged, so these are correctness and not polish.
    for verb, want in (("set", "setting"), ("sets", "setting"),
                       ("run", "running"), ("stop", "stopping"),
                       ("begin", "beginning"), ("occur", "occurring"),
                       ("refer", "referring"), ("plan", "planning"),
                       ("count", "counting"), ("name", "naming"),
                       ("open", "opening"), ("visit", "visiting"),
                       ("offer", "offering"), ("fix", "fixing"),
                       ("row", "rowing"), ("proceeds", "proceeding")):
        got = _to_ing(verb)
        if got != want:
            fails.append("_to_ing(%r) = %r, want %r" % (verb, got, want))
    on = {}
    for r in rows:
        on[r["read_on"]] = on.get(r["read_on"], 0) + 1
    if on.get(ON_RESIDUE, 0) == len(rows):
        fails.append("every judgement claims to have been made on the "
                     "residue; inspecting the residues says otherwise")
    for r in rows:
        if r["option"] == VERB_CARRIES_IT and r["read_on"] != ON_DROPPED:
            fails.append("%s judged VERB_CARRIES_IT without reading the "
                         "dropped subject, which is the only place that "
                         "option is visible" % r["id"])
    a, _ = proxy_agreement(ITEMS, JUDGEMENTS)
    if a == len(ITEMS):
        fails.append("proxy agrees on every item -- it would then BE the "
                     "rule, and the file's argument is that it is not")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for x in fails:
        print("  " + x)
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--front" in argv:
        for iid, claim in ITEMS:
            f = front(claim)
            print("%-7s %s" % (iid, f["residue"] or "(" + f["why"] + ")"))
        return 0
    if "--score" in argv:
        rows = score(ITEMS, JUDGEMENTS)
        opts, arms = tally(rows)
        print("D6 verb-first, n=%d   judge: %s\n" % (len(rows), JUDGE))
        for r in rows:
            print("%-7s %-16s [%s] %s"
                  % (r["id"], r["option"], r["read_on"], r["residue"]))
            print("        %s" % r["why"])
        print()
        for o in OPTIONS:
            print("  %-16s %d" % (o, opts[o]))
        print()
        on = {}
        for r in rows:
            on[r["read_on"]] = on.get(r["read_on"], 0) + 1
        for k in READ_ON:
            print("  judged on %-15s %d" % (k, on.get(k, 0)))
        print()
        print("  arms: identity %d  process %d  own arm %d  "
              "no observation %d"
              % (arms[t1.IDENTITY], arms[t1.NONIDENTITY], arms["own_arm"],
                 arms["no_observation"]))
        return 0
    if "--proxy" in argv:
        a, rows = proxy_agreement(ITEMS, JUDGEMENTS)
        print("morphological proxy vs the recorded rule, n=%d" % len(rows))
        for iid, want, got, ok in rows:
            print("  %-7s rule=%-16s proxy=%-16s %s"
                  % (iid, want, got, "ok" if ok else "MISS"))
        print("\n  agreement %d/%d" % (a, len(rows)))
        return 0
    if "--compare" in argv:
        compare()
        return 0
    print(__doc__.strip())
    print("\nusage: t1_verb_first.py [--selftest | --front | --score | "
          "--proxy | --compare]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
