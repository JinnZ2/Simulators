# SPDX-License-Identifier: CC0-1.0
"""Gate for denominator_sorter (work order TK-G1, 2026-11-23).
Standard library only.  Synthetic rows only; no real row is read.

    python3 ledger/toolkit/gate/gate_denominator_sorter.py

Imports the tool itself (its sort and field-drop code use the standard
library): sort_studies, study_units, drop_null, FIELDS.

NUMBERS ONLY.  This script sets no PASS / FAIL threshold and prints no
verdict.  The owner sets thresholds after reading the tables.

What the sorter can and cannot split on.  sort_studies() groups studies by
seven recorded columns and never reads rr.  So "two measurands pooled
under one label" is run in two forms and both are reported:

  RECORDED    the two measurands differ in one signature field (Response:
              "Aboveground" vs "Total_biomass"); every other field is the
              same.  The label that pools them is rr.
  UNRECORDED  the two measurands carry the SAME value in all seven fields.
              Nothing recorded tells them apart.

Per replicate: STUDIES studies, half per measurand, ROWS rows each.
  rr = N(0, ROW_SD) for measurand one, N(g * ROW_SD, ROW_SD) for two.
  g is the mean gap in row standard deviations: 0.2, 0.5, 1.0.

split found        sort_studies() returns exactly two scope groups
assignment accuracy  each returned group takes its majority true
                   measurand; share of studies sitting with their own.
                   One group holding everything reads 0.5.
outcome test       drop_null() on the Response field: "moves outcome" when
                   the spread rise from dropping the field is above the
                   95th percentile of its own shuffle null (the tool's
                   rule, DROP_SHUFFLES shuffles, unchanged).  Residuals
                   handed to it: rr minus the replicate's mean, weight 1.

Null: one measurand (g = 0), NULL_DRAWS draws.
  RECORDED    Response still takes two values, assigned to studies at
              random, tied to nothing.
  UNRECORDED  one value everywhere.
  false split = sort_studies() returns more than one group.
  false "moves outcome" = the outcome test fires.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import denominator_sorter as sorter  # noqa: E402

SEED = 20261123
GAPS = [0.2, 0.5, 1.0]
REPS = 20
NULL_DRAWS = 200
STUDIES = 20
ROWS = 10
ROW_SD = 0.3
DESIGN = {"Experimental.setting": "Greenhouse", "Phase2.time": "5", "Approach": "Self-Other",
          "Phase1.culti": "Monoculture", "SoilTp": "Whole soil", "Phase2.grow": "Alone"}
RESPONSE = ["Aboveground", "Total_biomass"]
R_INDEX = sorter.FIELDS.index("Response")


def dataset(g, seed, recorded, random_labels=False):
    rng = random.Random(seed)
    truth = {}
    which = [i % 2 for i in range(STUDIES)]
    labels = list(which)
    if random_labels:
        rng.shuffle(labels)
    rows = []
    for i in range(STUDIES):
        name = "S%02d" % i
        truth[name] = which[i]
        resp = RESPONSE[labels[i]] if recorded else RESPONSE[0]
        for _ in range(ROWS):
            rows.append(dict(DESIGN, Author=name, Year="2010", Response=resp,
                             rr="%.6f" % rng.gauss(which[i] * g * ROW_SD, ROW_SD), var="0.05"))
    return rows, truth


def read(rows, truth, seed):
    res = sorter.sort_studies(rows)
    groups = [g["studies"] for g in res["groups"]] + [g["studies"] for g in res["singletons"]]
    right = 0
    for members in groups:
        ones = sum(truth[m] for m in members)
        right += max(ones, len(members) - ones)
    ys = [float(r["rr"]) for r in rows]
    mean = sum(ys) / len(ys)
    resid = {id(r): (y - mean, 1.0) for r, y in zip(rows, ys)}
    row = sorter.drop_null(sorter.study_units(rows), resid, seed=seed)[R_INDEX]
    return len(res["groups"]), right / len(truth), row[6]


def main():
    print("gate_denominator_sorter: seed %d, %d studies x %d rows, row sd %.1f,"
          % (SEED, STUDIES, ROWS, ROW_SD))
    print("  field-drop shuffles %d (tool default), 95th percentile rule unchanged"
          % sorter.DROP_SHUFFLES)
    print("  thresholds: NOT SET (numbers only)")
    print()
    print("KNOWN-ANSWER: two measurands, %d replicates per gap" % REPS)
    print("  form         gap g   split found   assignment accuracy (mean)   outcome test fires")
    for form, recorded in (("RECORDED", True), ("UNRECORDED", False)):
        for gi, g in enumerate(GAPS):
            split = moves = 0
            acc = []
            marks = {}
            for rep in range(REPS):
                seed = SEED + 1000 * gi + rep
                rows, truth = dataset(g, seed, recorded)
                n, a, mark = read(rows, truth, seed)
                split += n == 2
                acc.append(a)
                moves += mark == "moves outcome"
                marks[mark] = marks.get(mark, 0) + 1
            print("  %-10s   %5.1f   %2d of %2d   %26.3f   %2d of %2d   (%s)"
                  % (form, g, split, REPS, sum(acc) / REPS, moves, REPS,
                     "; ".join("%s %d" % kv for kv in sorted(marks.items()))))
    print()
    print("NULL: one measurand, %d draws" % NULL_DRAWS)
    print("  form         false split rate   false 'moves outcome' rate")
    for form, recorded in (("RECORDED", True), ("UNRECORDED", False)):
        split = moves = 0
        for d in range(NULL_DRAWS):
            seed = SEED + 900000 + d
            rows, truth = dataset(0.0, seed, recorded, random_labels=True)
            n, _, mark = read(rows, truth, seed)
            split += n > 1
            moves += mark == "moves outcome"
        print("  %-10s   %16.3f   %26.3f" % (form, split / NULL_DRAWS, moves / NULL_DRAWS))


if __name__ == "__main__":
    main()
