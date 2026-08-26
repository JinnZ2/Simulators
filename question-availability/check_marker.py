#!/usr/bin/env python3
"""Runs MARKER.md against this tree. The marker is not edited.

Four things in it are checkable from inside the repo, and one is
checkable by construction:

    the ordinal      Q2 is offered as a "candidate ninth exclusion
                     mechanism". Count what is already filed.
    the mechanism    is Q2 new, or is it one the register already
                     identified as named-but-unfiled.
    the cross-links  five named; how many resolve.
    A1              "two booleans. Cheap." -- against the marker's own
                     Open section, which says the two states A1 would
                     have to separate cannot be separated.
    A4              built here, unrun. What it needs beyond the data.

stdlib only. CC0. Parses under Python 3.9.

    python3 check_marker.py
    python3 check_marker.py --selftest
"""

import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# This audit's own products. Two drops ago a checker in notes/ measured
# its own previous run because the commentary it wrote into CLAUDE.md
# became part of the corpus it scanned -- UNI_010. Excluding by path is a
# hand-broken loop and is stated rather than left quietly true.
EXCLUDE = ("question-availability", "CLAUDE.md", "README.md")


def _pattern(token):
    # Word-bounded. A bare substring scan matched `parity` inside
    # "disparity" two drops ago -- UNI_009. Boundaries fix substring
    # bleed and do nothing about sense.
    return re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])"
                      % re.escape(token), re.I)


def artifact_exists(token):
    """Is there a FOLDER or file by this name, as opposed to a mention?

    `resolve()` counts textual occurrences and that is not the same
    question. `report-typing` acquired occurrences the moment the previous
    drop's marker named it in ITS cross-link list, so a mention count would
    now report it as resolving while the artifact is still absent -- the
    UNI_010 self-reference shape, arriving through a sibling folder rather
    than through this audit's own output.
    """
    for cand in (token, token + ".md", token.replace("-", "_") + ".py"):
        if os.path.exists(os.path.join(ROOT, cand)):
            return True
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        if os.path.basename(dirpath) == token:
            return True
    return False


def resolve(token):
    pat = _pattern(token)
    hits = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            if any(rel == e or rel.startswith(e + os.sep) for e in EXCLUDE):
                continue
            try:
                if pat.search(open(os.path.join(dirpath, fn),
                                   errors="replace").read()):
                    hits.append(rel)
            except OSError:
                continue
    return sorted(hits)


# --------------------------------------------------------------------------
# the ordinal
# --------------------------------------------------------------------------

def filed_mechanisms():
    """Everything already filed as a numbered exclusion mechanism."""
    reg = []
    p = os.path.join(ROOT, "uninstrumented", "uninstrumented.py")
    if os.path.exists(p):
        txt = open(p, errors="replace").read()
        m = re.search(r"MECHANISMS\s*=\s*\((.*?)\)", txt, re.S)
        if m:
            reg = re.findall(r'"([A-Z_]+)"', m.group(1))
    numbered = []
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
                numbered.append((int(mm.group(1)),
                                 os.path.relpath(os.path.join(dirpath, fn),
                                                 ROOT), title))
    numbered.sort()
    return reg, numbered


def next_ordinal():
    reg, numbered = filed_mechanisms()
    top = max([len(reg)] + [n for n, _p, _t in numbered]) if (reg or numbered) \
        else 0
    return top + 1, reg, numbered


# --------------------------------------------------------------------------
# is Q2 new?
#
# UNI_012 recorded a mechanism named in the register's own literature note
# and filed nowhere: `affect routing`. Its shape and Q2's are compared by
# quoting both, not by summarising either.
# --------------------------------------------------------------------------

UNI_012_SHAPE = "so the reading never reaches a guard at all"
UNI_012_UNFALSIFIABLE = ("the classification is unfalsifiable from the "
                         "speaker's side, because objecting to it reads as "
                         "confirming it")
Q2_SHAPE = ("the label is applied prior to content, so the content never "
            "reaches evaluation")
Q2_UNFALSIFIABLE = ("Answering the label does not clear it; the pre-emptive "
                    "denial imports the frame")


def _flat(p):
    return " ".join(open(p, errors="replace").read().split())


def q2_versus_affect_routing():
    reg = os.path.join(ROOT, "uninstrumented", "CLAIM_TABLE.md")
    marker = os.path.join(HERE, "MARKER.md")
    if not os.path.exists(reg):
        return {"register_present": False}
    r, m = _flat(reg), _flat(marker)
    return {
        "register_present": True,
        "uni_012_shape": " ".join(UNI_012_SHAPE.split()) in r,
        "uni_012_unfalsifiable": " ".join(UNI_012_UNFALSIFIABLE.split()) in r,
        "q2_shape": " ".join(Q2_SHAPE.split()) in m,
        "q2_unfalsifiable": " ".join(Q2_UNFALSIFIABLE.split()) in m,
        "affect_routing_filed": "affect routing" in r and
                                "affect_routing" in _flat(
                                    os.path.join(ROOT, "uninstrumented",
                                                 "uninstrumented.py")),
    }


# --------------------------------------------------------------------------
# A1 -- two booleans against three states
# --------------------------------------------------------------------------

STATES = ("comparison_found",
          "absent_in_a_stated_corpus_under_stated_terms",
          "not_searched")


def a1_encode(state):
    """A1 as specified: control_exists, comparison_exists. Two booleans."""
    return (True, state == "comparison_found")


def a1_collisions():
    seen = {}
    for s in STATES:
        seen.setdefault(a1_encode(s), []).append(s)
    return [v for v in seen.values() if len(v) > 1]


# --------------------------------------------------------------------------
# A4 -- built, and not run
#
# "citation ratio, corrected version vs superseded version, by year since
# correction." The computation is here. The data is not, and is not
# invented: the egress gate refuses the citation sources.
# --------------------------------------------------------------------------

NOT_FETCHED = "NOT_FETCHED"


def displacement_series(corrected, superseded):
    """Ratio per year since correction. Returns None where undefined."""
    out = []
    for i, (c, s) in enumerate(zip(corrected, superseded)):
        out.append((i, None if (c + s) == 0 else c / float(c + s)))
    return out


def half_life(series):
    """Years until the corrected share reaches 0.5, by linear interpolation.

    Returns None when the series never crosses -- which is the Q3 case and
    must be a distinct value, not a large number.
    """
    pts = [(y, v) for y, v in series if v is not None]
    for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
        if v0 < 0.5 <= v1:
            if v1 == v0:
                return float(y1)
            return y0 + (0.5 - v0) * (y1 - y0) / (v1 - v0)
    return None


def a4_data():
    """No citation counts are supplied. See RESULTS."""
    return {"case": "captive-wolf alpha hierarchy",
            "corrected": NOT_FETCHED, "superseded": NOT_FETCHED,
            "why": ("citation databases are refused by this environment's "
                    "egress gate; notes/study_watch.py runs on a runner "
                    "that reaches them")}


def reference_class_needed():
    """Two corrections with the SAME ratio at one year and opposite fates."""
    fast = [(1, 0.10), (5, 0.30), (10, 0.45), (20, 0.80)]
    stalled = [(1, 0.25), (5, 0.40), (10, 0.45), (20, 0.44)]
    return {"same_at_year_10": fast[2][1] == stalled[2][1],
            "hl_fast": half_life(fast), "hl_stalled": half_life(stalled),
            "fast": fast, "stalled": stalled}


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON MARKER.md -- the marker is not edited\n")

    print("1  the ordinal")
    nxt, reg, numbered = next_ordinal()
    print("   register MECHANISMS tuple : %d   %s"
          % (len(reg), ", ".join(reg)))
    for n, p, t in numbered:
        print("   MECHANISM_%02d              : %s" % (n, t))
    print("   next unused ordinal       : %d" % nxt)
    print("   marker says               : 'candidate ninth exclusion")
    print("                               mechanism', and 'eight exclusion")
    print("                               mechanisms' in Related")
    print("   Off by three. Nine, ten and eleven are taken -- CATEGORY WELD,")
    print("   GENERATION CAPACITY REMOVED, DERIVATION DISCARDED. Second")
    print("   instance of this exact slip: `nonidentity-census` T4 caught")
    print("   the same one and recorded 'this would be a twelfth, not a")
    print("   ninth'. The eight-item list is the REGISTER; the numbered")
    print("   mechanisms live in sibling folders and are easy to miss from")
    print("   outside.")
    print()

    print("2  is Q2 a new mechanism?")
    q = q2_versus_affect_routing()
    for k in sorted(q):
        print("   %-24s %s" % (k, q[k]))
    print()
    print("   UNI_012, on the register's own literature note:")
    print("     '...a channel reclassified at intake, %s'" % UNI_012_SHAPE)
    print("     '%s'" % UNI_012_UNFALSIFIABLE)
    print("   MARKER.md Q2:")
    print("     '%s'" % Q2_SHAPE)
    print("     '%s'" % Q2_UNFALSIFIABLE)
    print()
    print("   Same mechanism, two statements. UNI_012 recorded `affect")
    print("   routing` as named in the register's literature note and filed")
    print("   NOWHERE -- 'affect routing has neither', neither an entry nor")
    print("   a mechanism. Q2 is that mechanism arriving with a name and a")
    print("   second case. So Q2 is not a candidate ninth; it is the twelfth")
    print("   ordinal for a mechanism the register already knew was missing.")
    print()
    print("   And Q2's own second case IS UNI_012's case -- 'driver")
    print("   diagnostic question typed as complaint by reporter position'.")
    print("   The marker names it and does not connect it. Its FIRST case,")
    print("   'why is this arrangement retained' filed as conspiracy-")
    print("   adjacent, is from a different field, which is what UNI_002's")
    print("   open cross-field check has been waiting for.")
    print()

    print("3  cross-links")
    links = ["uninstrumented", "report-typing", "criterion-symmetry",
             "rubric-backcasting", "merit-anchoring"]
    print("   %-22s %-9s %-9s %s" % ("link", "mentions", "artifact", "where"))
    for t in links:
        h = resolve(t)
        ex = artifact_exists(t)
        print("   %-22s %-9d %-9s %s"
              % (t, len(h), "yes" if ex else "NO",
                 (", ".join(h[:2]) + (" (+%d)" % (len(h) - 2)
                                      if len(h) > 2 else "")) or "--"))
    n_ex = sum(1 for t in links if artifact_exists(t))
    print("   artifacts present: %d of %d" % (n_ex, len(links)))
    print("   `criterion-symmetry` exists because the last drop landed it,")
    print("   so the named-and-absent set converges as drops arrive.")
    print("   MENTION IS NOT EXISTENCE, and the two columns disagree.")
    print("   `report-typing` has mentions and no artifact, and it acquired")
    print("   them the moment the PREVIOUS marker named it in its own")
    print("   cross-link list. A mention count would now report it as")
    print("   resolving. That is UNI_010's self-reference shape reaching")
    print("   this audit through a sibling folder rather than through its")
    print("   own output, and the fix is a second column, not an exclusion.")
    print()

    print("4  A1: 'two booleans. Cheap.'")
    print("   The marker's Open section says Q1 needs 'a criterion for")
    print("   distinguishing not asked from asked and not found by me.'")
    print("   A1's second boolean is the result of a search. Three states:")
    for s in STATES:
        print("     %-46s -> %s" % (s, a1_encode(s)))
    coll = a1_collisions()
    print("   collisions: %s" % coll)
    print("   A1 encodes three states in two values, so two of them share a")
    print("   cell -- and they are exactly the two the Open section says")
    print("   must be separated. **A1 cannot answer the question its own")
    print("   marker poses about Q1.**")
    print("   The repair is the one this repo keeps reaching for: a third")
    print("   state. 'Absent in a stated corpus under stated terms' is a")
    print("   measurement; 'I did not find it' is not, and 'not searched'")
    print("   is neither. Bounding the null is what makes Q1 enterable.")
    print()

    print("5  A4: 'the cheapest real measurement in the set and runnable now'")
    d = a4_data()
    print("   case      : %s" % d["case"])
    print("   corrected : %s" % d["corrected"])
    print("   superseded: %s" % d["superseded"])
    print("   why       : %s" % d["why"])
    print("   The computation is built and the data is not fetched. No")
    print("   citation count is supplied from memory.")
    print()
    r = reference_class_needed()
    print("   And it needs one thing beyond the data. Two corrections with")
    print("   the SAME corrected-share at year 10 and opposite fates:")
    print("     %-10s %s" % ("displaced", r["fast"]))
    print("     %-10s %s" % ("stalled", r["stalled"]))
    print("     same value at year 10: %s" % r["same_at_year_10"])
    print("     half-life  displaced %.1f y   stalled %s"
          % (r["hl_fast"], r["hl_stalled"]))
    print("   The trajectory separates them and a single year's ratio does")
    print("   not -- which the marker already gets right by asking for it")
    print("   'by year since correction'. What it does not say is that the")
    print("   trajectory is still uninterpretable alone: whether a given")
    print("   curve counts as 'did not displace' needs a REFERENCE CLASS of")
    print("   corrections that did. `criterion-symmetry`'s missing")
    print("   comparison table, on a second substrate.")
    print("   `half_life` returns None for a curve that never crosses --")
    print("   the Q3 case -- rather than a large number.")
    print()

    print("6  runnability of A1-A4 from here")
    rows = [("A1", "broken by the marker's own Open section (finding 4)"),
            ("A2", "needs a venue-typed corpus; none exists in this tree"),
            ("A3", "is report-typing's residue measurement; that folder is "
                   "not in this tree"),
            ("A4", "built here; data refused by the egress gate")]
    for a, why in rows:
        print("   %-4s %s" % (a, why))
    print("   0 of 4 runnable in this environment. The marker says one is")
    print("   'runnable now', and A4 IS runnable -- by someone with a")
    print("   citation database. notes/study_watch.py runs on a runner that")
    print("   reaches them, and A4 is the second item in this drop family")
    print("   the watcher exists for, after shape-spec-audit MS_004.")
    print()


def selftest():
    fails = []

    nxt, reg, numbered = next_ordinal()
    if nxt <= 9:
        fails.append("next ordinal is %d; the marker's 'ninth' is no longer "
                     "wrong and finding 1 must be restated" % nxt)
    if len(reg) != 8:
        fails.append("the register holds %d mechanisms, not 8; finding 1's "
                     "arithmetic must be restated" % len(reg))

    q = q2_versus_affect_routing()
    if not q.get("register_present"):
        fails.append("uninstrumented/CLAIM_TABLE.md is missing; finding 2 "
                     "rests on it")
    for k in ("uni_012_shape", "uni_012_unfalsifiable", "q2_shape",
              "q2_unfalsifiable"):
        if not q.get(k):
            fails.append("quotation %r no longer matches its source" % k)
    if q.get("affect_routing_filed"):
        fails.append("affect routing is now filed in the register; finding 2 "
                     "must be restated")

    coll = a1_collisions()
    if not coll:
        fails.append("A1 no longer collides; finding 4 must be restated")
    if len(STATES) <= 2:
        fails.append("fewer than three states declared; the collision is "
                     "trivial and finding 4 shows nothing")

    r = reference_class_needed()
    if not r["same_at_year_10"]:
        fails.append("the two synthetic curves no longer agree at year 10; "
                     "finding 5's demonstration is broken")
    if r["hl_stalled"] is not None:
        fails.append("half_life returns %r for a curve that never crosses; "
                     "it must return None" % r["hl_stalled"])
    if r["hl_fast"] is None:
        fails.append("half_life returns None for a curve that does cross; "
                     "it cannot return a positive")

    if a4_data()["corrected"] != NOT_FETCHED:
        fails.append("A4 now carries citation data; RESULTS must say where "
                     "it came from")

    # cross-links: at least one must resolve and at least one must not, or
    # the resolver is not discriminating.
    # `report-typing` was the absent half of this pair until it landed
    # (2026-08-26). It is kept as a token that DOES resolve and the
    # absent sample moves to `merit-anchoring`, which the arriving
    # marker's own cross-refs named. The check is about the resolver
    # discriminating, not about any one token.
    got = [artifact_exists(t) for t in
           ("uninstrumented", "merit-anchoring", "report-typing")]
    if all(got) or not any(got):
        fails.append("artifact_exists returns one answer for all tokens; it "
                     "cannot discriminate")
    # mention and existence must be able to DISAGREE, or the second column
    # is decorative.
    # QA_007's stated falsifier fired on 2026-08-26: `report-typing`
    # landed, so it no longer has mentions without an artifact. The
    # claim is updated in CLAIM_TABLE.md rather than the check being
    # loosened; the finding's live instance moves to `merit-anchoring`,
    # which has mentions and no artifact and acquired two of them from
    # the arriving marker's own cross-refs -- the same route.
    if artifact_exists("merit-anchoring") or not resolve("merit-anchoring"):
        fails.append("merit-anchoring no longer has mentions-without-"
                     "artifact; the mention-is-not-existence finding needs "
                     "a live instance")

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
