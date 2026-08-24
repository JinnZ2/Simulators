# SPDX-License-Identifier: CC0-1.0
"""
Runs `operators/D2.md` against this tree. Reads the entry, never edits it.

Four questions, each answered per instance rather than for the entry as a
whole:

  1. RESOLUTION   does the instance name something in this repo? Verified by
                  locating a file and a literal marker string inside it, not
                  by assertion. VERIFIED / NOT_IN_TREE / AMBIGUOUS.
  2. PAIR KIND    what are the two representations? The entry requires two
                  and does not say what kind of pair they may be. They turn
                  out to be at least five different kinds.
  3. SIGNATURE    does "the instrument reverts to the channel it was built
                  to avoid" hold for this instance?
  4. PROVENANCE   the STANDING CHECK says it was derived from two of the
                  instances above it. Are both of them in the list?

Markers are checked, not asserted. Two of the paths recorded below were
wrong when first written -- a marker with a space that the file does not
have, and a claim id filed under AUDIT_NOTES.md when it lives in
CLAIM_TABLE.md. Both were caught by running this, which is the operation
the entry describes, applied to the reading of the entry.

No verdict is computed on the entry. Counts and per-instance readings only.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENTRY = os.path.join(HERE, "operators", "D2.md")

VERIFIED, NOT_IN_TREE, AMBIGUOUS = "VERIFIED", "NOT_IN_TREE", "AMBIGUOUS"
HOLDS, FAILS, ARGUABLE = "HOLDS", "FAILS", "ARGUABLE"

# Pair kinds. Not a vocabulary the entry supplies -- it requires two
# representations and does not say of what kind. These are read off the
# instances.
ARTIFACT_ARTIFACT = "artifact vs artifact"
SCHEMA_DATA = "schema vs the data it admits"
CLAIM_BEHAVIOUR = "stated rule vs measured behaviour"
OUTPUT_KNOWN = "output vs a known answer"
DECLARED_REACHABLE = "declared value set vs reachable states"


def _has(path, marker):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return False
    with open(full, encoding="utf-8", errors="replace") as fh:
        return marker in fh.read()


# One record per instance line in the entry, keyed by a distinctive fragment
# of that line so the entry stays the source of the list.
READINGS = {
    "documented appendix": {
        "resolution": AMBIGUOUS,
        "candidates": [
            ("reasoning-gate/AUDIT_NOTES.md",
             "G-FIT", "guards.json stages G-FIT post; gate.py enforces it "
             "in pre()"),
            ("aperiodic-order-sim-stack/CLAIM_TABLE.md",
             "AOS_", "figures shipped that the report does not mention"),
            ("criteria-drift/CLAIM_TABLE.md",
             "CD_007", "'significant' twice in README, zero times in "
             "regress.py"),
        ],
        "pair_kind": ARTIFACT_ARTIFACT,
        "signature": FAILS,
        "signature_why": "a document and a program drifting apart is not a "
                         "reversion to an avoided channel; nothing reverts",
    },
    "realized record schema": {
        "resolution": VERIFIED,
        "path": "uninstrumented/specimens/INSTANCE_LOG_SURVEY.md",
        "marker": "They disagree on four things",
        "pair_kind": ARTIFACT_ARTIFACT,
        "signature": FAILS,
        "signature_why": "drift between a realized and a specified schema. "
                         "No channel was avoided and none was returned to",
    },
    "varying a CUE": {
        "resolution": NOT_IN_TREE,
        "path": None,
        "marker": None,
        "pair_kind": None,
        "signature": None,
        "signature_why": "not checked; the material is not in this repo and "
                         "the literature claim was not verified. Same status "
                         "as UNI_166 records for it",
    },
    "schema accepting anything": {
        "resolution": VERIFIED,
        "path": "uninstrumented/specimens/INSTANCE_LOG_INDEX.md",
        # The literal in the index is `{"type":"array"}`, no space after
        # the colon. A first draft of this marker had the space and the
        # selftest reported MARKER_MISSING -- which is the checker doing
        # its job on its own reading before doing it on the entry.
        "marker": "anyOf[1].properties.events",
        "marker_alt": '{"type":"array"}',
        "pair_kind": SCHEMA_DATA,
        "signature": FAILS,
        "signature_why": "the schema does not revert to an avoided channel; "
                         "its rejection branch is unreachable. UNI_166's "
                         "cannot-refuse direction",
    },
    "predicate detector deciding": {
        "resolution": VERIFIED,
        "path": "nonidentity-census/FINDINGS.md",
        "marker": "decides most cases lexically",
        "pair_kind": CLAIM_BEHAVIOUR,
        "signature": HOLDS,
        "signature_why": "built to escape lexical detection, decides 10 of "
                         "12 by word list. The avoided channel is named in "
                         "the module docstring and is the one it returns to",
    },
    "metric returning 0.83": {
        "resolution": VERIFIED,
        "path": "tools/known_answer.py",
        "marker": "marginal_majority (REPLACED)",
        "pair_kind": OUTPUT_KNOWN,
        "signature": ARGUABLE,
        "signature_why": "an association metric returning a marginal rate "
                         "is a reversion to the base rate it was meant to "
                         "look past, but no avoided channel was declared "
                         "in advance, so the fit is read backwards",
    },
    "null test unable to emit": {
        "resolution": VERIFIED,
        "path": "nonidentity-census/FINDINGS.md",
        "marker": "never fire",
        "pair_kind": DECLARED_REACHABLE,
        "signature": FAILS,
        "signature_why": "two declared values with no path to them. "
                         "UNI_166's cannot-emit direction. Nothing reverts",
    },
}

# The STANDING CHECK's two sources.
STANDING_SOURCES = [
    ("metric returning 0.83 where true association is zero",
     "in the instance list"),
    ("null-harness _verdict returning OK at TP=0.5 and TP=1.0 alike",
     "NOT in the instance list"),
]


def instances():
    """The list, read from the entry. The entry is the source, not this file."""
    with open(ENTRY, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^INSTANCES.*?$\n(.*?)(?=^\n^SIGNATURE)", text,
                  re.M | re.S)
    if not m:
        return []
    return [l.strip("- ").strip() for l in m.group(1).split("\n")
            if l.strip().startswith("-")]


def reading_for(line):
    for key, rec in READINGS.items():
        if key in line:
            return key, rec
    return None, None


def check():
    lines = instances()
    rows = []
    for line in lines:
        key, rec = reading_for(line)
        if rec is None:
            rows.append({"line": line, "resolution": "UNMAPPED",
                         "detail": "no reading recorded for this instance"})
            continue
        res, detail = rec["resolution"], ""
        if res == VERIFIED:
            ok = _has(rec["path"], rec["marker"])
            if not ok and rec.get("marker_alt"):
                ok = _has(rec["path"], rec["marker_alt"])
            if not ok:
                res = "MARKER_MISSING"
                detail = "%s does not contain %r" % (rec["path"],
                                                     rec["marker"])
            else:
                detail = rec["path"]
        elif res == AMBIGUOUS:
            live = [c for c in rec["candidates"] if _has(c[0], c[1])]
            detail = "%d candidates in tree: %s" % (
                len(live), "; ".join("%s (%s)" % (c[0], c[2]) for c in live))
        else:
            detail = "not in this repo"
        rows.append({"line": line, "resolution": res, "detail": detail,
                     "pair_kind": rec.get("pair_kind"),
                     "signature": rec.get("signature"),
                     "signature_why": rec.get("signature_why")})
    return rows


def report():
    rows = check()
    print("D2 instances checked against this tree, n=%d\n" % len(rows))
    for r in rows:
        print("- %s" % r["line"])
        print("    resolution : %-14s %s" % (r["resolution"], r["detail"]))
        if r.get("pair_kind"):
            print("    pair kind  : %s" % r["pair_kind"])
        if r.get("signature"):
            print("    signature  : %-9s %s" % (r["signature"],
                                                r["signature_why"]))
        elif r.get("signature_why"):
            print("    signature  : %-9s %s" % ("--", r["signature_why"]))
        print()

    res = {}
    for r in rows:
        res[r["resolution"]] = res.get(r["resolution"], 0) + 1
    print("RESOLUTION   " + "  ".join("%s %d" % (k, v)
                                      for k, v in sorted(res.items())))

    kinds = {}
    for r in rows:
        if r.get("pair_kind"):
            kinds[r["pair_kind"]] = kinds.get(r["pair_kind"], 0) + 1
    print()
    print("PAIR KINDS   %d distinct across %d readable instances:"
          % (len(kinds), sum(kinds.values())))
    for k, v in sorted(kinds.items()):
        print("    %-32s %d" % (k, v))
    print("    The entry requires two representations and does not say of")
    print("    what kind. Two runs of D2 can therefore compare very")
    print("    different things without the difference being declared.")

    sig = {}
    for r in rows:
        if r.get("signature"):
            sig[r["signature"]] = sig.get(r["signature"], 0) + 1
    print()
    print("SIGNATURE    'the instrument reverts to the channel it was built")
    print("             to avoid', per instance:")
    for k in (HOLDS, ARGUABLE, FAILS):
        if k in sig:
            print("    %-9s %d" % (k, sig[k]))
    print("    Holds cleanly on 1 of %d, arguably on 1, fails on %d."
          % (sum(sig.values()), sig.get(FAILS, 0)))
    print("    The two it fails on as a pair -- schema accepting anything,")
    print("    null test unable to emit -- are the two directions of")
    print("    UNI_166, reached here from a different side.")

    print()
    print("STANDING CHECK provenance -- 'derived from two of the above':")
    for src, where in STANDING_SOURCES:
        print("    %-8s %s" % ("[in]" if "NOT" not in where else "[out]",
                               src))
    print("    One of the two sources is not in the instance list. The")
    print("    check is right and its stated derivation is one short.")
    return 0


def selftest():
    fails = []
    lines = instances()
    if len(lines) != 7:
        fails.append("expected 7 instance lines parsed from the entry, got "
                     "%d" % len(lines))
    for line in lines:
        key, rec = reading_for(line)
        if rec is None:
            fails.append("no reading recorded for %r" % line[:40])
    rows = check()
    bad = [r for r in rows if r["resolution"] == "MARKER_MISSING"]
    for r in bad:
        fails.append("marker missing: %s" % r["detail"])
    sigs = [r.get("signature") for r in rows if r.get("signature")]
    if HOLDS not in sigs:
        fails.append("no instance where the signature holds; the entry's "
                     "own strongest case would be missing")
    if FAILS not in sigs:
        fails.append("no instance where the signature fails; a check that "
                     "only confirms is not a check")
    kinds = set(r.get("pair_kind") for r in rows if r.get("pair_kind"))
    if len(kinds) < 2:
        fails.append("pair kinds do not vary; the finding about undeclared "
                     "pair kind would be unearned")
    with open(ENTRY, encoding="utf-8") as fh:
        entry = fh.read()
    if "SIGNATURE across instances" not in entry:
        fails.append("the entry no longer states the signature this checker "
                     "is checking")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    return report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
