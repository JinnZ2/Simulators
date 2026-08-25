#!/usr/bin/env python3
"""Runs notes/datasets/mesa_sof.md against this tree. Edits nothing.

The note is stored as delivered. This file reports four readings and one
computation, and none of them is a verdict on the note.

The note proposes two real cohorts as the empirical answer to a question
`sim-span/RESULTS.md` left open. Three things about that are checkable
from inside this repo:

    1. does it answer what RESULTS.md actually asked, both halves
    2. do its cross-references resolve in this tree
    3. what the sim's swept parameters correspond to in the measurements
       the note names

And one thing is not, and is marked rather than guessed: every fact about
MESA and SOF -- the sample size, the age range, what was recorded -- is
carried from the note. The egress gate refuses the sources that would
check them.

usage:
    python3 check_datasets.py
    python3 check_datasets.py --selftest
"""

import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTE = os.path.join(HERE, "datasets", "mesa_sof.md")
RESULTS = os.path.join(ROOT, "sim-span", "RESULTS.md")

sys.path.insert(0, os.path.join(ROOT, "sim-span"))


def _read(p):
    return open(p, errors="replace").read()


def _flat(p):
    return " ".join(_read(p).split())


# --------------------------------------------------------------------------
# 1. does the note answer what RESULTS.md asked?
#
# Two items were left open. They are quoted from the file at run time, so
# a quote that has drifted turns the selftest red.
# --------------------------------------------------------------------------

ASKED = [
    ("outcome fit",
     "in a study with polysomnography or actigraphy, both `true_sleep` and "
     "`frag` are measured separately. Fit the outcome on both.",
     "PSG gives true_sleep and awakenings on the same person",
     True),
    ("the fraction p",
     "the fraction of respondents who answer a sleep-duration question with "
     "time in bed rather than time asleep. A validation sub-study against "
     "actigraphy would give it directly",
     "the note names a questionnaire alongside PSG and actigraphy on the "
     "same person, which is that sub-study -- but it does not claim this",
     True),
]


def asked_items():
    txt = _flat(RESULTS)
    return [(name, " ".join(q.split()) in txt, why, claimed)
            for name, q, why, claimed in ASKED]


# --------------------------------------------------------------------------
# 2. do the note's cross-references resolve?
# --------------------------------------------------------------------------

REFS = ["G-SPAN", "parity", "MESA", "SOF"]

# Word-bounded. A bare substring scan matched `parity` inside "disparity"
# and `SOF` inside other words on the first run of this file -- which is
# `uninstrumented` UNI_009's `lean` / "clean" defect, committed here three
# drops after it was recorded. The raw counts it produced (parity 17,
# SOF 81) are kept in FINDINGS_DATASETS.md beside the bounded ones.
def _pattern(token):
    return re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])"
                      % re.escape(token), re.I)


# This audit's own products. Without them the scan measures its own
# previous run: writing "MESA" into CLAUDE.md to describe the finding put
# MESA into the tree, and the next run reported it as resolving. That is
# `uninstrumented` UNI_010's self-reference loop -- scan.py reading the
# directory scan_audit.py writes into -- arriving in notes/, and found the
# same way, by running twice and diffing.
#
# Excluding by path is a HAND-BROKEN loop, not a fix, and it is stated
# rather than left true quietly: anyone grepping this tree for MESA still
# finds the commentary. The principled version compares against the git
# tree as of the note's own commit, which is what "does this token have an
# antecedent" actually means; not built.
EXCLUDE = (
    "notes/datasets", "notes/check_datasets.py",
    "notes/FINDINGS_DATASETS.md", "notes/samples/check_datasets.sample.txt",
    "notes/README.md", "CLAUDE.md", "README.md",
)


def resolve(token):
    """Where does this token appear in the tree, outside this audit?"""
    pat = _pattern(token)
    hits = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            if any(rel == e or rel.startswith(e + os.sep) for e in EXCLUDE):
                continue
            if pat.search(_read(p)):
                hits.append(rel)
    return sorted(hits)


# --------------------------------------------------------------------------
# 3. what the sim's swept parameters are, in the note's measurements
#
# span      = true_sleep + frag * wake_cost      (sim)
# TIB       = TST + WASO + sleep onset latency   (polysomnography)
#
# So `frag * wake_cost` is WASO, and `span - true_sleep` is WASO plus
# onset latency. Both are PSG readouts. The question is whether the sim's
# two swept parameters carry any information beyond their product -- if
# they do not, WASO alone is the axis; if they do, the awakening count is
# a second one, and the note's instrument has both.
# --------------------------------------------------------------------------

EQUAL_PRODUCT = [(1.0, 120.0), (2.0, 60.0), (4.0, 30.0), (8.0, 15.0)]


def product_test(n=20000, seed=1000):
    import sim_span as S
    rows = []
    for fm, wm in EQUAL_PRODUCT:
        rng = random.Random(seed)
        pop = S.add_span(S.agents(n, rng, fm, wm))
        excess = sum(a["span"] - a["true_sleep"] for a in pop) / float(len(pop))
        d = S.one_run(n, "mono", 1.0, seed, frag_mean=fm, wake_mean=wm)
        d = d["reported"]
        rows.append({"frag": fm, "wake": wm, "product_h": fm * wm / 60.0,
                     "excess_h": excess, "a": d["a"], "vertex": d["vertex"],
                     "is_u": d["is_u"]})
    return rows


def product_verdict(rows):
    """Mean excess should equal the product. Vertex should not."""
    mean_err = max(abs(r["excess_h"] - r["product_h"]) for r in rows)
    vs = [r["vertex"] for r in rows if r["vertex"] is not None]
    return {"mean_matches_product": mean_err < 0.05, "mean_err": mean_err,
            "vertex_spread": (max(vs) - min(vs)) if len(vs) > 1 else 0.0,
            "u_disagree": len(set(r["is_u"] for r in rows)) > 1}


# --------------------------------------------------------------------------
# 4. what cannot be checked from here
# --------------------------------------------------------------------------

CARRIED = [
    "MESA Sleep n = 2,237",
    "MESA has PSG + 7-day actigraphy + questionnaire on the same person",
    "MESA ages 45-84 at baseline, sleep exam roughly a decade in",
    "SOF is all women, older, with PSG and actigraphy",
    "SOF carries mortality and incident disease outcomes",
]


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON notes/datasets/mesa_sof.md -- the note is not edited\n")

    print("1  does the note answer what sim-span/RESULTS.md asked?")
    for name, found, why, claimed in asked_items():
        print("   %-14s quote in RESULTS.md: %-5s" % (name, found))
        print("      %s" % why)
    print("   Both halves are answered by one design. The note claims the")
    print("   first and not the second: it says 'measured sleep, measured")
    print("   awakenings, and what they said when asked', which IS the")
    print("   validation sub-study `p` needs, and then does not say so.")
    print("   `p` needs a THREE-way comparison the note stops short of")
    print("   specifying: self-report against total sleep time AND against")
    print("   time in bed, per person, classified by which it is nearer.")
    print("   Two-way against sleep alone gives the gap, not the fraction.")
    print()

    print("2  do the note's cross-references resolve in this tree?")
    for tok in REFS:
        hits = resolve(tok)
        shown = ", ".join(hits[:2]) + (" (+%d)" % (len(hits) - 2)
                                       if len(hits) > 2 else "")
        print("   %-8s %-3d %s" % (tok, len(hits), shown or "NOT IN TREE"))
    print("   Scanned with this audit's own products excluded (%d paths)."
          % len(EXCLUDE))
    print("   Without that exclusion the scan measures its own previous")
    print("   run: writing MESA into CLAUDE.md to describe the finding put")
    print("   MESA into the tree, and the next run reported it resolving.")
    print("   UNI_010's loop in notes/, found the same way -- by running")
    print("   twice. Excluding by path is a hand-broken loop, not a fix.")
    print()
    print("   G-SPAN, MESA and SOF resolved ZERO times when this check")
    print("   was written and resolve now -- every hit under sim-span/,")
    print("   which is work written AFTER the note, using its vocabulary.")
    print("   The note was written into the tree it is checked against:")
    print("   ANC_001..004 at repo scale, reaching this checker through a")
    print("   sibling folder, which is the route an EXCLUDE list does not")
    print("   close (QA_007). The assertion was changed rather than the")
    print("   list widened -- these must resolve ONLY under sim-span/, so")
    print("   a hit elsewhere still fires. Finding 8.")
    print("   `parity` resolves %d times and NOT ONCE in the note's sense."
          % len(resolve("parity")))
    print("   Every repo use is the equality sense -- `parity()` as a")
    print("   comparison function in the divergence log, 'what would count")
    print("   as parity' as equivalence. The note means the obstetric")
    print("   sense: number of pregnancies. One word, two senses, and a")
    print("   resolver that counts occurrences reports a reference as")
    print("   resolving %d times when it resolves zero times."
          % len(resolve("parity")))
    print("   That is `uninstrumented` case 021's sense substitution and")
    print("   `nonidentity-census` T1-3's `state` finding (nation-state vs")
    print("   steady state), third instance in this tree -- and it is a")
    print("   limit of THIS checker, not of the note: word boundaries fix")
    print("   substring bleed and do nothing about sense. Only hand-reading")
    print("   the sixteen got the right number, which is T1-1 one level up.")
    print("   So the SOF half is a thread from outside this repo, and")
    print("   nothing here can say what question it answers.")
    print()

    print("3  what the sim's swept parameters are, in PSG terms")
    print("     sim   span = true_sleep + frag * wake_cost")
    print("     PSG   TIB  = TST + WASO + onset latency")
    print("   so `frag * wake_cost` is WASO, and the sim's span excess is")
    print("   WASO plus onset latency. Both are PSG readouts.")
    print()
    rows = product_test()
    print("   %-7s %-7s %-10s %-10s %-10s %-8s %s"
          % ("frag", "wake", "product_h", "excess_h", "a", "vertex", "is_u"))
    for r in rows:
        print("   %-7.1f %-7.0f %-10.2f %-10.2f %-+10.4f %-8.2f %s"
              % (r["frag"], r["wake"], r["product_h"], r["excess_h"],
                 r["a"], r["vertex"] or 0.0, r["is_u"]))
    v = product_verdict(rows)
    print()
    print("   mean excess equals the product : %s (max error %.3f h)"
          % (v["mean_matches_product"], v["mean_err"]))
    print("   vertex spread at fixed product : %.2f h" % v["vertex_spread"])
    print("   the four disagree on is_u      : %s" % v["u_disagree"])
    print()
    print("   The MEAN is the product exactly. The SHAPE is not: at a fixed")
    print("   two hours of WASO the manufactured minimum moves %.2f h as the"
          % v["vertex_spread"])
    print("   split runs from few-long awakenings to many-short, and many")
    print("   short ones push it DOWN the axis, toward the window where a")
    print("   published minimum sits.")
    print("   So WASO alone is not the axis. The awakening count is a second")
    print("   one -- and the note's instrument reports both, which is more")
    print("   than the note claims for it.")
    print()

    print("4  carried from the note, not checked here")
    for c in CARRIED:
        print("   - %s" % c)
    print("   The egress gate refuses the sources that would confirm any of")
    print("   these. Same status as `shape-spec-audit` MS_004. Nothing in")
    print("   this file rests on a dataset fact being right; the readings")
    print("   above are about the note's fit to this repo and about the")
    print("   sim's own arithmetic.")
    print()
    print("   `notes/study_watch.py` is NOT the instrument for these. It")
    print("   reads `uninstrumented.ENTRIES`, and this is an operator note,")
    print("   not a register entry. Filing it as one to make it watchable")
    print("   would be filing it under a mechanism it does not claim.")
    print()

    print("5  the caveat the note states, and how far it reaches")
    print("   Stated: ages 45-84, no young cohort, no ageing clocks,")
    print("   mortality is the outcome you get.")
    print("   It reaches further than that, in the note's favour. sim-span")
    print("   assumes frag and true_sleep are INDEPENDENT and flags the")
    print("   assumption as probably wrong. In a 45-84 cohort they are")
    print("   near-certainly correlated. So MESA does not only test the")
    print("   finding -- it measures the sim's own weakest assumption,")
    print("   because both quantities are recorded per person. That makes")
    print("   it the hard case rather than a convenient one, which is the")
    print("   right way round for a test that could refute.")
    print()


def selftest():
    fails = []

    for name, found, _why, _claimed in asked_items():
        if not found:
            fails.append("the RESULTS.md quote for %r no longer matches" % name)

    if not os.path.exists(NOTE):
        fails.append("the note is missing")
    if not os.path.exists(RESULTS):
        fails.append("sim-span/RESULTS.md is missing")

    rows = product_test(n=8000)
    v = product_verdict(rows)
    if not v["mean_matches_product"]:
        fails.append("mean span excess no longer equals frag*wake/60 "
                     "(max error %.3f h); the WASO mapping must be restated"
                     % v["mean_err"])
    if v["vertex_spread"] < 0.5:
        fails.append("the vertex no longer moves at fixed product (spread "
                     "%.2f h); 'WASO alone is not the axis' must be restated"
                     % v["vertex_spread"])

    # G-SPAN, MESA and SOF used to resolve nowhere, and finding 3's table
    # recorded three zeros. They now resolve, and NOT because the note was
    # wrong: sim-span/RESULTS.md, NOTES_INSTRUMENT.md and three_column.py
    # adopted the note's own vocabulary after the table was written. The
    # note was written INTO the tree it is checked against -- the
    # anchor-interval corpus loop (ANC_001..004) and UNI_010, at repo
    # scale, arriving through a sibling folder rather than through this
    # checker's own output.
    #
    # So the assertion is no longer "must not resolve". It is "must
    # resolve only downstream of the note", which still has a reachable
    # negative: a hit outside sim-span/ would mean the term has an
    # antecedent independent of the note, and finding 3 would have to be
    # restated for the reason it originally claimed.
    for tok in ("G-SPAN", "MESA", "SOF"):
        outside = [h for h in resolve(tok) if not h.startswith("sim-span" + os.sep)]
        if outside:
            fails.append("%s resolves outside sim-span/ (%s); the term has "
                         "an antecedent independent of the note and finding 3 "
                         "must be restated" % (tok, ", ".join(outside)))
    # The word-bounded resolver must still be sense-blind on `parity`, or
    # the finding about it has to be restated. It counts >0 and the count
    # in the note's sense is 0; that gap IS the finding.
    if not resolve("parity"):
        fails.append("`parity` no longer resolves at all; the sense-blindness "
                     "finding must be restated")
    # sim-span must resolve, or the note has nothing to attach to.
    if not resolve("MESA") and not os.path.exists(RESULTS):
        fails.append("nothing for the note to attach to")

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
