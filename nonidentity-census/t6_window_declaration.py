# SPDX-License-Identifier: CC0-1.0
"""
T6 -- WINDOW DECLARATION vs ENTITY READING.

HYPOTHESIS (operator's, under test, not assumed): identity claims correlate
with an UNDECLARED measurement window. Where a rate or interval is stated,
the main term reads as process. Where none is stated, the missing parameter
defaults to permanent and the term reads as entity.

NOT CLAIMED: that authors believe anything. The mechanism is omission, not
belief. No column here codes intent, and none is inferred anywhere in this
file.

UNIT: one row per paper, main causal claim only, extracted by T1's rule.
`BOUNDARY.md` D0 is reused, not re-derived.

TWO INSTRUMENTS SUPPLY TWO COLUMNS, and keeping them apart is what makes the
EXIT check mean anything:

    reading      from D6, the verb-first test. BEARER_REQUIRED -> ENTITY,
                 READS_WITHOUT / VERB_CARRIES_IT -> PROCESS,
                 BOTH_READINGS -> UNDETERMINED.
    decided_by   from T1's own classifier, carried forward verbatim as the
                 instrument's self-report. T1's `TABLE` is this work order's
                 `LEXICAL`; the rename is recorded rather than applied
                 silently.

HARD RULES, implemented rather than restated:

  - A window taken from an ABSTRACT is recorded and marked INADMISSIBLE.
    The enum accepts ABSTRACT because sources exist there; the rule says
    not to use them, so `admissible()` returns False and the row is
    excluded from the 2x2 with its exclusion counted.
  - No unit conversion. `window_value` is verbatim. There is no seconds
    field in this module and `--selftest` fails if one appears.
  - AMBIGUOUS and UNDETERMINED are terminal. Nothing resolves them.
  - No verdict is computed and no p-value is reported. The 2x2 and the
    decided_by split inside each cell are the output.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import sys

import t1_predicate_unit as t1
import t1_verb_first as vf

YES, NO, AMBIGUOUS = "YES", "NO", "AMBIGUOUS"
DECLARED = (YES, NO, AMBIGUOUS)

METHODS, RESULTS, FIGURE_AXIS, ABSTRACT, NONE = (
    "METHODS", "RESULTS", "FIGURE_AXIS", "ABSTRACT", "NONE")
SOURCES = (METHODS, RESULTS, FIGURE_AXIS, ABSTRACT, NONE)

# The hard rule: abstracts are where the nominalization lives, so sampling
# that channel measures the register and not the claim.
ADMISSIBLE_SOURCES = (METHODS, FIGURE_AXIS, RESULTS, NONE)

ENTITY, PROCESS, UNDETERMINED = "ENTITY", "PROCESS", "UNDETERMINED"
READINGS = (ENTITY, PROCESS, UNDETERMINED)

LEXICAL, PREDICATE, UNDEC_BY = "LEXICAL", "PREDICATE", "UNDECIDABLE"

# T1's own column, renamed. Recorded here rather than applied silently.
DECIDED_BY_RENAME = {t1.BY_TABLE: LEXICAL,
                     t1.BY_PREDICATE: PREDICATE,
                     t1.BY_NEITHER: UNDEC_BY}

# D6 option -> reading. BOTH_READINGS is terminal, not a tie to break.
READING_FROM_OPTION = {
    vf.BEARER_REQUIRED: ENTITY,
    vf.READS_WITHOUT: PROCESS,
    vf.VERB_CARRIES_IT: PROCESS,
    vf.BOTH_READINGS: UNDETERMINED,
    vf.NO_FRONTING: UNDETERMINED,
    vf.UNGRAMMATICAL: UNDETERMINED,
}


class WeldedColumns(Exception):
    """Raised when the null test cannot build an off-diagonal cell."""


def row(paper_id, claim, field, window_declared, window_value,
        window_source, d6_option, notes=None):
    if window_declared not in DECLARED:
        raise ValueError("window_declared must be one of %r" % (DECLARED,))
    if window_source not in SOURCES:
        raise ValueError("window_source must be one of %r" % (SOURCES,))
    if d6_option not in vf.OPTIONS:
        raise ValueError("d6_option must be one of %r" % (vf.OPTIONS,))
    if window_declared == NO and window_source != NONE:
        raise ValueError("%s: window_declared NO with source %r -- NONE "
                         "means NONE" % (paper_id, window_source))
    if window_declared == YES and window_source == NONE:
        raise ValueError("%s: window_declared YES with no source"
                         % paper_id)
    c = t1.classify(claim)
    return {
        "paper_id": paper_id,
        "claim": claim,
        "main_term": c["head"],
        "field": field,
        "window_declared": window_declared,
        "window_value": window_value,      # verbatim, never converted
        "window_source": window_source,
        "reading": READING_FROM_OPTION[d6_option],
        "d6_option": d6_option,
        "decided_by": DECIDED_BY_RENAME[c["decided_by"]],
        "admissible": window_source in ADMISSIBLE_SOURCES,
        "notes": notes,
    }


# --------------------------------------------------------------------------
# NULL TEST. Three rows per cell of {YES, NO} x {ENTITY, PROCESS}. The
# off-diagonals are the point.
#
# Every row is HAND-BUILT for this test. None is a paper. The methods
# sentence in each is written here so the window has a source to come from.
# --------------------------------------------------------------------------

NULL_ROWS = [
    # --- cell YES x ENTITY : a stated interval, and the term is a carrier
    row("N-A1", "We find that firms with concentrated ownership reduce "
        "investment following the reform.", "economics",
        YES, "quarterly", METHODS, vf.BEARER_REQUIRED,
        "methods states firms were surveyed quarterly"),
    row("N-A2", "We show that participants who relocated earned more.",
        "sociology", YES, "5-year follow-up", METHODS,
        vf.BEARER_REQUIRED, "cohort followed five years"),
    row("N-A3", "We report that colonies fragmented under shear.",
        "ecology", YES, "30 Hz", FIGURE_AXIS, vf.BEARER_REQUIRED,
        "figure x-axis in frames at 30 Hz"),

    # --- cell NO x PROCESS : no interval anywhere, and the term is a process
    row("N-B1", "Allocation proceeds without any central coordinator.",
        "economics", NO, None, NONE, vf.VERB_CARRIES_IT,
        "no methods section states a rate"),
    row("N-B2", "Diffusion dominates transport in the interior.",
        "thermodynamics", NO, None, NONE, vf.READS_WITHOUT,
        "no interval stated"),
    row("N-B3", "Selection acts on variance rather than on means.",
        "ecology", NO, None, NONE, vf.VERB_CARRIES_IT,
        "no generation time stated"),

    # --- cell YES x PROCESS
    row("N-C1", "We find that transport increases with surface roughness.",
        "thermodynamics", YES, "30 Hz", METHODS, vf.READS_WITHOUT,
        "flow sampled at 30 Hz"),
    row("N-C2", "We show that turnover rose through the sampled interval.",
        "organizational_theory", YES, "monthly", METHODS,
        vf.VERB_CARRIES_IT, "monthly payroll records"),
    row("N-C3", "Mixing slows as stratification strengthens.",
        "systems_control", YES, "1 s", FIGURE_AXIS, vf.READS_WITHOUT,
        "figure x-axis in seconds"),

    # --- cell NO x ENTITY
    row("N-D1", "We show that populations declined across all sampled "
        "sites.", "ecology", NO, None, NONE, vf.BEARER_REQUIRED,
        "no census interval stated"),
    row("N-D2", "We demonstrate that institutions persist long after the "
        "conditions that produced them.", "sociology", NO, None, NONE,
        vf.BEARER_REQUIRED, "no observation window stated"),
    row("N-D3", "We argue that the norm eroded once enforcement lapsed.",
        "law", NO, None, NONE, vf.BEARER_REQUIRED,
        "no interval stated"),
]


# --------------------------------------------------------------------------
# MATCHED NULL SET. Built after the first one, because the first one's
# `decided_by` column tracked `window_declared` 11 of 12 -- see FINDINGS
# T6-3. The cause was construction, not the world: the NO rows reused T1's
# own fixture sentences, whose head nouns are all in the D3 table, and the
# YES rows were written fresh with terms that are not.
#
# Here the SAME three head nouns appear in both window arms of each reading,
# so `decided_by` is held constant across the exposure by construction and
# cannot track it. Any residual association would be real.
# --------------------------------------------------------------------------

MATCHED_ROWS = [
    # ENTITY terms: populations, institutions, firms -- both window arms
    row("M-E1y", "We show that populations declined across all sampled "
        "sites.", "ecology", YES, "annual census", METHODS,
        vf.BEARER_REQUIRED, "matched pair with M-E1n"),
    row("M-E2y", "We demonstrate that institutions persist long after the "
        "conditions that produced them.", "sociology", YES,
        "decadal waves", METHODS, vf.BEARER_REQUIRED,
        "matched pair with M-E2n"),
    row("M-E3y", "We find that firms with concentrated ownership reduce "
        "investment following the reform.", "economics", YES, "quarterly",
        METHODS, vf.BEARER_REQUIRED, "matched pair with M-E3n"),
    row("M-E1n", "We show that populations declined across all sampled "
        "sites.", "ecology", NO, None, NONE, vf.BEARER_REQUIRED,
        "matched pair with M-E1y"),
    row("M-E2n", "We demonstrate that institutions persist long after the "
        "conditions that produced them.", "sociology", NO, None, NONE,
        vf.BEARER_REQUIRED, "matched pair with M-E2y"),
    row("M-E3n", "We find that firms with concentrated ownership reduce "
        "investment following the reform.", "economics", NO, None, NONE,
        vf.BEARER_REQUIRED, "matched pair with M-E3y"),

    # PROCESS terms: allocation, diffusion, transport -- both window arms
    row("M-P1y", "Allocation proceeds without any central coordinator.",
        "economics", YES, "daily", METHODS, vf.VERB_CARRIES_IT,
        "matched pair with M-P1n"),
    row("M-P2y", "Diffusion dominates transport in the interior.",
        "thermodynamics", YES, "1 s", FIGURE_AXIS, vf.READS_WITHOUT,
        "matched pair with M-P2n"),
    row("M-P3y", "We find that transport increases with surface "
        "roughness.", "thermodynamics", YES, "30 Hz", METHODS,
        vf.READS_WITHOUT, "matched pair with M-P3n"),
    row("M-P1n", "Allocation proceeds without any central coordinator.",
        "economics", NO, None, NONE, vf.VERB_CARRIES_IT,
        "matched pair with M-P1y"),
    row("M-P2n", "Diffusion dominates transport in the interior.",
        "thermodynamics", NO, None, NONE, vf.READS_WITHOUT,
        "matched pair with M-P2y"),
    row("M-P3n", "We find that transport increases with surface "
        "roughness.", "thermodynamics", NO, None, NONE, vf.READS_WITHOUT,
        "matched pair with M-P3y"),
]


def decided_by_tracks_window(rows):
    """
    How far apart the two window arms are in `decided_by`, as a count of
    rows -- not a coefficient and not a p-value.

    Returns (rows_to_move, n, per_arm). `rows_to_move` is the number of rows
    whose `decided_by` would have to change to make the YES and NO arms
    carry identical distributions. 0 means the columns are independent on
    this data. Higher means `decided_by` is partly readable off
    `window_declared`, which for a hand-built null set is a fact about the
    hand.

    An earlier version of this function took the majority label per arm and
    divided by n. That returns the marginal majority rate, so it read 0.83
    on the matched set where the two arms are IDENTICAL by construction and
    the true association is zero. Replaced; the wrong number is recorded in
    FINDINGS T6-4 rather than quietly dropped.
    """
    arms = {}
    labels = set()
    for r in rows:
        if not r["admissible"]:
            continue
        arms.setdefault(r["window_declared"], {})
        arms[r["window_declared"]][r["decided_by"]] = \
            arms[r["window_declared"]].get(r["decided_by"], 0) + 1
        labels.add(r["decided_by"])
    n = sum(sum(v.values()) for v in arms.values())
    if len(arms) < 2:
        return 0, n, arms
    (a, b) = list(arms.values())[:2]
    na, nb = sum(a.values()), sum(b.values())
    if not na or not nb:
        return 0, n, arms
    tvd = 0.5 * sum(abs(a.get(l, 0) / float(na) - b.get(l, 0) / float(nb))
                    for l in labels)
    return int(round(tvd * min(na, nb))), n, arms


def cells(rows):
    """The 2x2, with the decided_by split inside each cell."""
    out = {}
    excluded = []
    for r in rows:
        if not r["admissible"]:
            excluded.append(r)
            continue
        if r["window_declared"] == AMBIGUOUS or r["reading"] == UNDETERMINED:
            key = (r["window_declared"], r["reading"])
        else:
            key = (r["window_declared"], r["reading"])
        c = out.setdefault(key, {"n": 0, LEXICAL: 0, PREDICATE: 0,
                                 UNDEC_BY: 0, "ids": [], "fields": {}})
        c["n"] += 1
        c[r["decided_by"]] += 1
        c["ids"].append(r["paper_id"])
        c["fields"][r["field"]] = c["fields"].get(r["field"], 0) + 1
    return out, excluded


def null_test(rows=None, verbose=True):
    """
    Runs BEFORE any real run. Raises WeldedColumns if an off-diagonal cell
    is empty -- that is the STOP condition, not a warning.
    """
    rows = NULL_ROWS if rows is None else rows
    grid, excluded = cells(rows)
    required = [(YES, ENTITY), (NO, PROCESS), (YES, PROCESS), (NO, ENTITY)]
    off_diagonal = [(YES, ENTITY), (NO, PROCESS)]
    missing = [k for k in required if grid.get(k, {"n": 0})["n"] == 0]
    if verbose:
        print("NULL TEST -- 3 rows per cell, hand-built, none is a paper\n")
        render(grid, excluded)
        print()
    bad_off = [k for k in off_diagonal if k in missing]
    if bad_off:
        raise WeldedColumns(
            "off-diagonal cell(s) %r could not be built. window_declared and "
            "reading are welded and T6 measures one variable twice. STOP."
            % (bad_off,))
    if verbose:
        print("off-diagonal cells built: %s"
              % ", ".join("%s x %s = %d" % (a, b, grid[(a, b)]["n"])
                          for a, b in off_diagonal))
        print("the two columns are not welded. T6 may proceed.")
        unused = [v for v in (AMBIGUOUS,) if
                  not any(r["window_declared"] == v for r in rows)]
        unused += [v for v in (UNDETERMINED,) if
                   not any(r["reading"] == v for r in rows)]
        if unused:
            print()
            print("NOT EXERCISED by the null test as specified: %s."
                  % ", ".join(unused))
            print("The design is a 2x2 and these are terminal values "
                  "outside it, so nothing here shows the instrument can "
                  "emit them. Recorded, not repaired -- repairing it means "
                  "changing the null test the work order specified.")
    return grid, excluded


def render(grid, excluded=None):
    print("%-12s %-12s %4s   %-8s %-10s %-11s  %s"
          % ("window", "reading", "n", "LEXICAL", "PREDICATE",
             "UNDECIDABLE", "fields"))
    for w in (YES, NO, AMBIGUOUS):
        for rd in (ENTITY, PROCESS, UNDETERMINED):
            c = grid.get((w, rd))
            if not c:
                continue
            flds = ", ".join("%s:%d" % (k, v)
                             for k, v in sorted(c["fields"].items()))
            print("%-12s %-12s %4d   %-8d %-10d %-11d  %s"
                  % (w, rd, c["n"], c[LEXICAL], c[PREDICATE],
                     c[UNDEC_BY], flds))
    if excluded:
        print()
        print("excluded, window taken from an inadmissible source: %s"
              % ", ".join("%s (%s)" % (r["paper_id"], r["window_source"])
                          for r in excluded))


def association(rows):
    """
    Counts only. No coefficient, no p-value -- the work order says report
    the 2x2. This reports how `reading` lines up with each candidate, so
    the EXIT check can be read off two tables rather than a statistic.
    """
    a = {}
    b = {}
    for r in rows:
        if not r["admissible"]:
            continue
        a[(r["window_declared"], r["reading"])] = \
            a.get((r["window_declared"], r["reading"]), 0) + 1
        b[(r["decided_by"], r["reading"])] = \
            b.get((r["decided_by"], r["reading"]), 0) + 1
    return a, b


def exit_check(rows=None, verbose=True):
    rows = NULL_ROWS if rows is None else rows
    a, b = association(rows)
    if verbose:
        print("reading x window_declared")
        for k in sorted(a):
            print("  %-12s %-12s %d" % (k[0], k[1], a[k]))
        print()
        print("reading x decided_by  (T1's self-report)")
        for k in sorted(b):
            print("  %-12s %-12s %d" % (k[0], k[1], b[k]))
        print()
        print("On the null rows `window_declared` is balanced 6/6 against")
        print("`reading` BY CONSTRUCTION, so the first table carries no")
        print("information and is printed to show that it does not. The")
        print("second is measured. If a real run ever shows reading")
        print("tracking decided_by more tightly than window_declared, the")
        print("instrument is the finding again.")
    return a, b


# --------------------------------------------------------------------------
# The real run.
# --------------------------------------------------------------------------

def eligible_sample():
    """
    The work order permits falling back to the papers already in hand from
    T1. There are none. T1's twelve items are authored sentences written in
    this repo; they have no methods section, no figure axis, and no
    publication. Every one would take window_source NONE by construction.
    """
    return []


def real_run(verbose=True):
    sample = eligible_sample()
    if verbose:
        print("REAL RUN\n")
        print("  eligible papers: %d" % len(sample))
        print()
        print("  T1's twelve items are authored sentences, not papers. They")
        print("  have no methods section and no figure axis, so every row")
        print("  would take window_source NONE and window_declared NO by")
        print("  construction -- one column constant across the whole")
        print("  sample. That is the welded-column failure arriving from")
        print("  the sample side rather than the concept side, and running")
        print("  it would produce a 2x2 with two empty columns that looked")
        print("  like a result.")
        print()
        print("  Bulk sources remain refused by egress (FINDINGS T2-1) and")
        print("  a snippet sample is refused for the reason T2 refused it.")
        print("  Not labelled CONVENIENCE and run anyway: a convenience")
        print("  sample still has to be able to vary the exposure, and this")
        print("  one cannot.")
    return sample


def selftest():
    fails = []
    for r in NULL_ROWS:
        if "seconds" in r:
            fails.append("%s carries a converted value; window_value is "
                         "verbatim only" % r["paper_id"])
    try:
        row("X", "The market cleared.", "economics", NO, "quarterly",
            METHODS, vf.READS_WITHOUT)
        fails.append("window_declared NO with a source must be refused")
    except ValueError:
        pass
    try:
        row("X", "The market cleared.", "economics", YES, "quarterly",
            NONE, vf.READS_WITHOUT)
        fails.append("window_declared YES with no source must be refused")
    except ValueError:
        pass
    r = row("X", "The market cleared.", "economics", YES, "quarterly",
            ABSTRACT, vf.READS_WITHOUT)
    if r["admissible"]:
        fails.append("a window sourced from an ABSTRACT must be marked "
                     "inadmissible")
    grid, excluded = cells(NULL_ROWS)
    for k in ((YES, ENTITY), (NO, PROCESS), (YES, PROCESS), (NO, ENTITY)):
        if grid.get(k, {"n": 0})["n"] != 3:
            fails.append("cell %r has %d rows, want 3"
                         % (k, grid.get(k, {"n": 0})["n"]))
    try:
        null_test(verbose=False)
    except WeldedColumns as ex:
        fails.append("null test raised: %s" % ex)
    thin = [r for r in NULL_ROWS if r["main_term"] is None]
    if thin:
        fails.append("main_term not extracted for %r"
                     % [r["paper_id"] for r in thin])
    if eligible_sample():
        fails.append("eligible_sample() returned rows; T1 has no papers")
    mg, _ = cells(MATCHED_ROWS)
    for k in ((YES, ENTITY), (NO, PROCESS), (YES, PROCESS), (NO, ENTITY)):
        if mg.get(k, {"n": 0})["n"] != 3:
            fails.append("matched cell %r has %d rows, want 3"
                         % (k, mg.get(k, {"n": 0})["n"]))
    for arm in (YES, NO):
        terms = sorted(r["main_term"] for r in MATCHED_ROWS
                       if r["window_declared"] == arm)
        other = sorted(r["main_term"] for r in MATCHED_ROWS
                       if r["window_declared"] != arm)
        if terms != other:
            fails.append("matched set is not matched: %r vs %r"
                         % (terms, other))
    m1, n1, _ = decided_by_tracks_window(NULL_ROWS)
    m2, n2, _ = decided_by_tracks_window(MATCHED_ROWS)
    if m2 != 0:
        fails.append("the matched set holds decided_by constant across the "
                     "window arms by construction; rows_to_move must be 0, "
                     "got %d" % m2)
    if m1 <= m2:
        fails.append("the as-specified null set should show more "
                     "decided_by/window tracking than the matched one; got "
                     "%d and %d" % (m1, m2))
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def table(rows=None):
    rows = NULL_ROWS if rows is None else rows
    hdr = ("paper_id", "main_term", "window_declared", "window_value",
           "window_source", "reading", "decided_by")
    print("| " + " | ".join(hdr) + " | field |")
    print("|" + "---|" * (len(hdr) + 1))
    for r in rows:
        print("| %s | %s | %s | %s | %s | %s | %s | %s |"
              % (r["paper_id"], r["main_term"], r["window_declared"],
                 r["window_value"] if r["window_value"] else "--",
                 r["window_source"], r["reading"], r["decided_by"],
                 r["field"]))


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--null" in argv:
        try:
            null_test()
        except WeldedColumns as ex:
            print("STOP: %s" % ex)
            return 1
        return 0
    if "--table" in argv:
        table()
        return 0
    if "--exit" in argv:
        exit_check()
        return 0
    if "--matched" in argv:
        print("MATCHED NULL SET -- same head nouns in both window arms\n")
        grid, excluded = cells(MATCHED_ROWS)
        render(grid, excluded)
        m1, n1, a1 = decided_by_tracks_window(NULL_ROWS)
        m2, n2, a2 = decided_by_tracks_window(MATCHED_ROWS)
        print()
        print("rows whose decided_by would have to change to make the two")
        print("window arms identical:")
        print("  as-specified null set  %d of %d" % (m1, n1))
        for arm in sorted(a1):
            print("      %-4s %s" % (arm, dict(sorted(a1[arm].items()))))
        print("  matched null set       %d of %d" % (m2, n2))
        for arm in sorted(a2):
            print("      %-4s %s" % (arm, dict(sorted(a2[arm].items()))))
        print()
        print("The first figure is a property of how the rows were built,")
        print("not of the hypothesis. The matched set removes it by using")
        print("the same head nouns in both window arms.")
        print()
        exit_check(MATCHED_ROWS)
        return 0
    if "--run" in argv:
        real_run()
        return 0
    print(__doc__.strip())
    print("\nusage: t6_window_declaration.py [--selftest | --null | "
          "--table | --exit | --run]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
