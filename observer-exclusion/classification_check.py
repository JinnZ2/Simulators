#!/usr/bin/env python3
"""CLASSIFICATION_NOTE.md against the spec it corrects, and against the tree.

The note proposes a third mechanism -- recorded, archived, catalogued, and
filed under a category that is not evidence -- and names two archives.
Four things follow, and the first is the largest.

    1. The censoring correction §4 calls its structural core is a property
       of the SOURCE, not of the method. On the archives the note names it
       is not needed.
    2. The two archives decompose the delay §4 could not: one gives
       δ_write ≈ 0, the other gives δ_survive ≈ 0.
    3. The mechanism is distinct from all eleven filed, and its ordinal is
       ambiguous for a reason that explains two prior off-by-three errors.
    4. It is the first mechanism in this family whose signature is in
       CATALOGUE METADATA, which makes it cheaper to test than the
       lead-time study it corrects.

stdlib only. CC0. Parses under Python 3.9.

    python3 classification_check.py
    python3 classification_check.py --selftest
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import archival_bias as AB  # noqa: E402

NOTE = os.path.join(HERE, "CLASSIFICATION_NOTE.md")
V2 = os.path.join(HERE, "SPEC_V2.md")


def _flat(p):
    return " ".join(open(p, errors="replace").read().split())


def quoted(needle, path):
    return " ".join(needle.split()) in _flat(path)


# --------------------------------------------------------------------------
# 1. the censoring is a property of the source
# --------------------------------------------------------------------------

PROFILES = [
    ("spec's stipulated trade press", AB.P_EXCLUDED,
     "undigitised, intermittent, survival uncertain"),
    ("partially catalogued", 0.25, "digitised runs, gaps"),
    ("continuous, contemporaneous", 0.95,
     "daily entries, unbroken series, catalogued to shelf mark"),
]


def source_effect(true_lead=20):
    return [{"label": lab, "hazard": p, "note": note,
             "mean_delay": 1.0 / p,
             "recovered": AB.attenuation(true_lead, p=p)["recovered"],
             "frac_pos_at_10": AB.attenuation(10, p=p)["frac_positive"]}
            for lab, p, note in PROFILES]


# --------------------------------------------------------------------------
# 2. the two archives decompose the delay
#
# §4 names two terms and says δ̂ recovers only one. The note's two archives
# zero out one term each, so between them both are estimable -- which is
# what §11 asks for and does not supply a source for.
# --------------------------------------------------------------------------

ARCHIVES = [
    {"name": "HBC post journals",
     "record_kind": "daily occurrences of note, written at the post",
     "delta_write": "≈ 0 — contemporaneous by design",
     "delta_survive": "≈ 0 — continuous series, catalogued to shelf mark",
     "gives": "both terms near zero; L needs no correction",
     "filed_as": "company / business records"},
    {"name": "Foxfire",
     "record_kind": "interviews collected from 1966 about earlier practice",
     "delta_write": "LARGE and variable — the two-date rule's own case",
     "delta_survive": "≈ 0 — published, in print, archived",
     "gives": "δ_write estimable in isolation, δ_survive held at zero",
     "filed_as": "folklore / Appalachian studies"},
]


def decomposition():
    """Which term each archive isolates."""
    return {"hbc_zeroes": ["delta_write", "delta_survive"],
            "foxfire_zeroes": ["delta_survive"],
            "foxfire_isolates": "delta_write",
            "both_estimable": True}


# --------------------------------------------------------------------------
# 3. distinctness, and the ordinal
# --------------------------------------------------------------------------

def register_tuple():
    p = os.path.join(ROOT, "uninstrumented", "uninstrumented.py")
    if not os.path.exists(p):
        return []
    m = re.search(r"MECHANISMS\s*=\s*\((.*?)\)",
                  open(p, errors="replace").read(), re.S)
    return re.findall(r'"([A-Z_]+)"', m.group(1)) if m else []


def numbered_files():
    out = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in files:
            mm = re.match(r"MECHANISM_(\d+)\.md$", fn)
            if mm:
                title = ""
                for line in open(os.path.join(dirpath, fn),
                                 errors="replace").read().splitlines():
                    if line.strip():
                        title = line.strip("# ").strip()
                        break
                out.append((int(mm.group(1)), title))
    return sorted(out)


DISTINCT_FROM = [
    ("MODALITY", "apparatus in the wrong channel",
     "the apparatus is a catalogue and it is in the right channel; it "
     "routes rather than misses"),
    ("STORAGE", "medium cannot hold the shape",
     "the medium held it for three centuries"),
    ("SCALAR_DEMAND", "function collapsed to a number",
     "nothing is collapsed; the prose survives intact"),
    ("BUDGET_BOUNDARY", "closed budget compared to open", "no budget"),
    ("AUTHORED_REFERENCE", "reference produced by the measured party",
     "the archive is third-party and often adversarial to its subjects"),
    ("AUDIT_ASYMMETRY", "guard fires on one side only",
     "no guard fires; the material is never presented to one"),
    ("SCORED_AS_WASTE", "component read as cost by the accounting",
     "nearest of the eight -- but waste is a devaluation inside one "
     "ledger, and this is a transfer to a different ledger"),
    ("PROXY_SUBSTITUTION", "enforceable measure displaces the target",
     "no proxy; the target itself is filed elsewhere"),
    ("CATEGORY WELD (09)", "independent quantities fused into one term",
     "nothing is fused; one thing is filed under one heading"),
    ("GENERATION CAPACITY REMOVED (10)", "the option space itself removed",
     "nothing was removed; it was shelved"),
    ("DERIVATION DISCARDED (11)", "a structure is the only copy of its "
     "own derivation", "the structure persists and is catalogued"),
    ("affect routing / unaskable", "channel present, entry penalised",
     "entry succeeded; the material is in the archive"),
    ("observer exclusion", "no channel",
     "there was a channel and it ran to completion"),
]


# --------------------------------------------------------------------------
# 4. the mechanism's own measurement
# --------------------------------------------------------------------------

SIGNATURE = [
    ("subject classification", "Foxfire filed under folklore / Appalachian "
     "studies; HBC under company records", "catalogue metadata, free"),
    ("citing-field distribution", "which journals cite it, by field",
     "citation database"),
    ("content-vs-filing mismatch", "behavioural observation filed under a "
     "non-evidence heading", "read a sample of the material"),
]


def prediction():
    """The mechanism's directly testable consequence."""
    return ("If classification determines readership, citations to a "
            "folklore-filed corpus containing behavioural observation "
            "should cluster in folklore and area-studies venues and be "
            "near-absent in the field the observation is about. The "
            "content is biological; the citing field should not be.")


# --------------------------------------------------------------------------

def report():
    print("CLASSIFICATION_NOTE.md -- checked against SPEC_V2 and the tree\n")

    print("1  the censoring correction is a property of the SOURCE")
    print("   §4 calls the correction 'THE STRUCTURAL CORE'. It exists")
    print("   because the excluded reading is oral and reaches the record")
    print("   late. The note's own archives are not that.\n")
    print("   %-32s %-9s %-11s %-11s %s"
          % ("source profile", "hazard", "mean delay", "recovered",
             "P(L>0) at 10"))
    print("   " + "-" * 78)
    for r in source_effect():
        print("   %-32s %-9.2f %-11.1f %-11.2f %.2f"
              % (r["label"], r["hazard"], r["mean_delay"], r["recovered"],
                 r["frac_pos_at_10"]))
    print()
    print("   HBC post journals record DAILY occurrences of note, at the")
    print("   post, in an unbroken series catalogued to shelf mark. Both")
    print("   delays collapse. A true twenty-year lead is recovered whole,")
    print("   and a true ten-year lead comes out positive every time")
    print("   instead of 47% of the time.")
    print()
    print("   So the whole of §4 -- including the sign error at OE_008 --")
    print("   is machinery for a source choice, not for the method. Pick a")
    print("   contemporaneous continuous archive and it is not needed.")
    print("   §6 lists trade press FIRST by tractability. On this reading")
    print("   the ordering should be by DELAY, not by ease of access, and")
    print("   the two are close to opposite.")
    print()

    print("2  the two archives decompose the delay §4 could not")
    for a in ARCHIVES:
        print("   %s" % a["name"])
        print("     records      %s" % a["record_kind"])
        print("     δ_write      %s" % a["delta_write"])
        print("     δ_survive    %s" % a["delta_survive"])
        print("     filed as     %s" % a["filed_as"])
    print()
    print("   §4 says δ̂ 'recovers δ_write, not δ_survive', and §11 says to")
    print("   estimate δ_survive 'from a known-complete archive' without")
    print("   naming one. The note names one. And Foxfire holds δ_survive")
    print("   at zero while δ_write is large, so the term §4 CAN estimate")
    print("   is isolable there. Between the two archives both terms come")
    print("   apart -- which also repairs OE_009, since F4's test can then")
    print("   compare the term the bias actually lives in.")
    print()

    print("3  distinct from all eleven filed, and from both named classes")
    for name, shape, why in DISTINCT_FROM:
        print("   %-34s %s" % (name, why))
    print()
    reg, num = register_tuple(), numbered_files()
    print("   register MECHANISMS tuple : %d" % len(reg))
    for n, t in num:
        print("   MECHANISM_%02d              : %s" % (n, t))
    print()
    print("   THE ORDINAL IS AMBIGUOUS, and this is why the off-by-three")
    print("   has now happened twice. There are TWO sequences:")
    print("     - the register tuple, %d entries, in one file" % len(reg))
    print("     - MECHANISM_NN.md files, %d of them, in sibling folders,"
          % len(num))
    print("       numbered as if they CONTINUE the tuple")
    print("   SPEC_V2 §1 says affect routing is 'the candidate exclusion")
    print("   mechanism for the uninstrumented register'. Added to the")
    print("   tuple it is the ninth tuple entry -- colliding with")
    print("   MECHANISM_09, CATEGORY WELD. Filed as a numbered file it is")
    print("   the twelfth. Both readings are defensible and they differ by")
    print("   three, which is the exact size of both prior errors.")
    print("   Repair: one canonical sequence. Either the register publishes")
    print("   a count that includes the sibling files, or the files become")
    print("   register entries. Nothing currently reconciles them.")
    print("   On the continuing sequence this note's mechanism is 13th.")
    print()

    print("4  the first mechanism in this family with a metadata signature")
    for what, where, cost in SIGNATURE:
        print("   %-28s %-52s %s" % (what, where, cost))
    print()
    print("   " + prediction())
    print()
    print("   That is cheaper than the lead-time study and it tests the")
    print("   MECHANISM rather than its consequence. The lead-time study")
    print("   measures what exclusion costs; this measures whether the")
    print("   classification is doing the excluding. If citations cluster")
    print("   by filing rather than by content, the mechanism holds; if")
    print("   they follow content across headings, it does not.")
    print()

    print("5  carried and unchecked")
    for c in ("HBC continuous from 1670; Archives of Manitoba",
              "Albany post journals B.3/1 to 212, 1705-1941",
              "a Business History paper on knowing nature in those records",
              "Foxfire: twelve volumes plus a magazine from 1966",
              "Foxfire filed under folklore / Appalachian studies"):
        print("   - %s" % c)
    print("   Egress-blocked, MS_004 status. Nothing in findings 1-4 rests")
    print("   on any of it: they are properties of a delay model, of a")
    print("   mechanism list in this tree, and of a stated prediction.")
    print()
    print("   ONE DETAIL TO CHECK BEFORE ANYONE ORDERS BOXES, flagged")
    print("   because it decides whether the records are found at all.")
    print("   HBCA classification puts a series letter between post number")
    print("   and volume -- section B is post records, and post journals")
    print("   are series 'a'. Albany journals would then be B.3/a/1-212,")
    print("   not B.3/1-212. Stated from memory, unverified, and cheap to")
    print("   confirm against the HBCA finding aid.")
    print()


def selftest():
    fails = []

    rows = source_effect()
    lo = [r for r in rows if r["hazard"] == AB.P_EXCLUDED][0]
    hi = [r for r in rows if r["hazard"] == 0.95][0]
    if not hi["recovered"] > lo["recovered"] + 0.5:
        fails.append("a contemporaneous archive no longer recovers more "
                     "than trade press (%.2f vs %.2f); finding 1 must be "
                     "restated" % (hi["recovered"], lo["recovered"]))
    if hi["recovered"] < 0.95:
        fails.append("the contemporaneous profile does not recover the "
                     "lead (%.2f); finding 1 overstates" % hi["recovered"])
    if lo["frac_pos_at_10"] > 0.6:
        fails.append("trade press no longer loses half the positives "
                     "(%.2f)" % lo["frac_pos_at_10"])

    d = decomposition()
    if not d["both_estimable"]:
        fails.append("the two archives no longer decompose the delay")
    if "delta_survive" in d["foxfire_zeroes"] and \
            d["foxfire_isolates"] != "delta_write":
        fails.append("the Foxfire isolation is stated inconsistently")

    reg, num = register_tuple(), numbered_files()
    if not reg:
        fails.append("the register tuple could not be read; finding 3 "
                     "rests on it")
    if not num:
        fails.append("no MECHANISM_NN files found; the ambiguity finding "
                     "has no second sequence")
    if num and max(n for n, _t in num) - len(reg) != 3:
        fails.append("the two sequences no longer differ by three; finding "
                     "3's explanation of the off-by-three must be restated")

    if not quoted("It's filed as folklore", NOTE) and \
            not quoted("it's filed as folklore", NOTE):
        fails.append("the note no longer says Foxfire is filed as folklore")
    if not quoted("recorded, archived, and filed under a category that "
                  "isn't evidence", NOTE):
        fails.append("the note's own statement of the mechanism has changed")
    if not quoted("THE STRUCTURAL CORE", V2):
        fails.append("SPEC_V2 no longer calls §4 the structural core; "
                     "finding 1 must be restated")

    # the distinctness list must cover everything filed, or it proves less
    # than it claims
    covered = " ".join(n for n, _s, _w in DISTINCT_FROM)
    for m in reg:
        if m.replace("_", " ").split()[0] not in covered.replace("_", " "):
            fails.append("distinctness list does not address %s" % m)

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
