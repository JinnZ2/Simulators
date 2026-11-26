# SPDX-License-Identifier: CC0-1.0
"""Gate for missing_column_finder (work order TK-G1, 2026-11-23).
Standard library only.  Synthetic rows only; no real row is read.

    python3 ledger/toolkit/gate/gate_missing_column_finder.py

Reads the tool through missing_column_finder_stdlib.analyse(), the
standard-library port.  The numpy original is not imported here.

NUMBERS ONLY.  This script sets no PASS / FAIL threshold and prints no
verdict.  The owner sets thresholds after reading the tables.

Synthetic data set, per replicate:
  STUDIES studies of ROWS rows.  Three recorded columns c1, c2, c3, each
  drawn N(0, 1) per row and tied to nothing.  One planted column, a label
  with LEVELS values drawn per row, independent of study.  It is NOT among
  the recorded columns; the finder sees it only as a grouping.
      rr = level_effect[label] + noise
  level effects are fixed: equally spaced, centred, scaled so that their
  variance across equally likely levels is s * TOTAL_VAR.  noise is
  N(0, (1 - s) * TOTAL_VAR).  var = SAMPLING_VAR on every row.
  s is the planted variance share: 0.1, 0.3, 0.5.

Known-answer: per s, REPS replicates.  recovered share = the finder's
  within-study share for the planted grouping (share of the spread left
  after the three columns and after study means).  realized share = the
  share the planted effect holds in that replicate's drawn rr, read from
  the generator, not from the finder.

Null: per s, replicate 0's rows with the planted labels shuffled across
  rows, NULL_SHUFFLES times.  Recovered share on each; median, 95th
  percentile and maximum reported.  The finder's own FLAG is not read in
  the null leg (its inner shuffles are set to 1 there to save time; the
  share does not depend on them).
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import missing_column_finder_stdlib as finder  # noqa: E402

SEED = 20261123
SHARES = [0.1, 0.3, 0.5]
REPS = 20
NULL_SHUFFLES = 200
STUDIES = 40
ROWS = 15
LEVELS = 6
TOTAL_VAR = 0.09
SAMPLING_VAR = 0.01
COLUMNS = ["c1", "c2", "c3"]
GROUPINGS = ["Author", "planted"]


def level_effects(s):
    raw = [k - (LEVELS - 1) / 2.0 for k in range(LEVELS)]
    sd = math.sqrt(sum(x * x for x in raw) / LEVELS)
    return [x / sd * math.sqrt(s * TOTAL_VAR) for x in raw]


def dataset(s, seed):
    rng = random.Random(seed)
    eff = level_effects(s)
    rows, effect, total = [], [], []
    for st in range(STUDIES):
        for _ in range(ROWS):
            k = rng.randrange(LEVELS)
            rr = eff[k] + rng.gauss(0, math.sqrt((1 - s) * TOTAL_VAR))
            effect.append(eff[k])
            total.append(rr)
            rows.append({"Author": "S%02d" % st, "planted": "L%d" % k,
                         "c1": "%.6f" % rng.gauss(0, 1), "c2": "%.6f" % rng.gauss(0, 1),
                         "c3": "%.6f" % rng.gauss(0, 1),
                         "rr": "%.6f" % rr, "var": "%.6f" % SAMPLING_VAR})
    return rows, _var(effect) / _var(total)


def _var(x):
    m = sum(x) / len(x)
    return sum((a - m) ** 2 for a in x) / len(x)


def read(rows, perm_seed, n_perm):
    o = finder.analyse(rows, perm_seed=perm_seed, n_perm=n_perm, columns=COLUMNS,
                       binary={}, groupings=GROUPINGS)
    return o, o["groupings"]["planted"]["within_study"]


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]


def main():
    print("gate_missing_column_finder: seed %d, %d studies x %d rows, %d planted levels,"
          % (SEED, STUDIES, ROWS, LEVELS))
    print("  total variance %.2f, sampling variance %.2f, finder shuffles %d, FLAG rule unchanged"
          % (TOTAL_VAR, SAMPLING_VAR, finder.N_PERM))
    print("  thresholds: NOT SET (numbers only)")
    print()
    print("KNOWN-ANSWER: %d replicates per planted share" % REPS)
    print("  planted s   realized share (mean)   recovered share: mean    min    max   "
          "flagged   three columns together (mean)")
    for si, s in enumerate(SHARES):
        real, rec, flags, tog = [], [], 0, []
        for rep in range(REPS):
            seed = SEED + 1000 * si + rep
            rows, realized = dataset(s, seed)
            o, w = read(rows, perm_seed=seed, n_perm=finder.N_PERM)
            real.append(realized)
            rec.append(w["share"])
            flags += w["flag"]
            tog.append(o["together"]["share"])
        print("  %9.1f   %21.4f   %22.4f  %5.4f  %5.4f   %2d of %2d   %12.4f"
              % (s, sum(real) / REPS, sum(rec) / REPS, min(rec), max(rec), flags, REPS,
                 sum(tog) / REPS))
    print()
    print("NULL: planted labels shuffled across rows, %d shuffles per planted share" % NULL_SHUFFLES)
    print("  planted s   recovered share: median    95th pct     max     unshuffled (same rows)")
    for si, s in enumerate(SHARES):
        seed = SEED + 1000 * si
        rows, _ = dataset(s, seed)
        base = read(rows, perm_seed=seed, n_perm=1)[1]["share"]
        rng = random.Random(SEED + 500000 + si)
        got = []
        for _ in range(NULL_SHUFFLES):
            labels = [r["planted"] for r in rows]
            rng.shuffle(labels)
            shuf = [dict(r, planted=lab) for r, lab in zip(rows, labels)]
            got.append(read(shuf, perm_seed=seed, n_perm=1)[1]["share"])
        print("  %9.1f   %23.4f   %9.4f  %6.4f   %10.4f"
              % (s, pct(got, 0.5), pct(got, 0.95), max(got), base))


if __name__ == "__main__":
    main()
