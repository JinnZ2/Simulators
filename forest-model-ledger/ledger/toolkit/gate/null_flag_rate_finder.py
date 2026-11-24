# SPDX-License-Identifier: CC0-1.0
"""Finder FLAG rate under the null (work order TK-G1 follow-up, 2026-11-24).
Standard library only.  Synthetic rows only; no real row is read.

    python3 ledger/toolkit/gate/null_flag_rate_finder.py

Rules are read from gate/DECLARED.json, committed before this was run.
Per planted share s: the gated design's replicate-0 rows, with the planted
labels shuffled across rows, 200 times.  On each shuffled set the finder
runs in full (499 inner shuffles, MIN_EXCESS unchanged) and its FLAG on
the planted grouping is read.  The lab (Author) test is read beside it;
nothing is planted there either.

Also reported, by leave-one-out over the same 200 shuffled shares: how
often one null share exceeds the maximum of the other 199.  That is the
declared finder rule turned on its own null.

NUMBERS ONLY.  If any FLAG rate is above 0.05 the script says so and sets
no threshold.
"""
import json
import multiprocessing
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import gate_missing_column_finder as gate  # noqa: E402
import missing_column_finder_stdlib as finder  # noqa: E402

LIMIT = 0.05
WORKERS = 4


def one(job):
    si, k, rows, labels = job
    shuf = [dict(r, planted=lab) for r, lab in zip(rows, labels)]
    seed = gate.SEED + 700000 + 1000 * si + k
    o = finder.analyse(shuf, perm_seed=seed, n_perm=finder.N_PERM, columns=gate.COLUMNS,
                       binary={}, groupings=gate.GROUPINGS)
    w = o["groupings"]["planted"]["within_study"]
    b = o["groupings"]["planted"]["between_study"]
    return (w["share"], bool(w["flag"]), bool(isinstance(b, dict) and b["flag"]),
            bool(o["groupings"]["Author"]["lab"]["flag"]))


def main():
    declared = json.load(open(os.path.join(HERE, "DECLARED.json")))["null_flag_rate_run"]
    n = declared["shuffles"]
    print("null_flag_rate_finder: %d shuffles per planted s, finder shuffles %d, MIN_EXCESS %.2f"
          % (n, finder.N_PERM, finder.MIN_EXCESS))
    print("  design: %d studies x %d rows; seed %d + 700000 + index of s"
          % (gate.STUDIES, gate.ROWS, gate.SEED))
    print("  rule (DECLARED.json): %s" % declared["rule"])
    print()
    print("  planted s   FLAG within-study   FLAG between-study   FLAG lab (Author)   "
          "max null share   declared rule, leave-one-out")
    over = []
    with multiprocessing.Pool(WORKERS) as pool:
        for si, s in enumerate(declared["planted_s"]):
            rows, _ = gate.dataset(s, gate.SEED + 1000 * si)
            rng = random.Random(gate.SEED + 700000 + si)
            jobs = []
            for k in range(n):
                labels = [r["planted"] for r in rows]
                rng.shuffle(labels)
                jobs.append((si, k, rows, labels))
            res = pool.map(one, jobs)
            shares = [r[0] for r in res]
            fw, fb, fl = (sum(r[i] for r in res) for i in (1, 2, 3))
            loo = sum(shares[k] > max(shares[:k] + shares[k + 1:]) for k in range(n))
            print("  %9.1f   %4d of %d (%.3f)   %5d of %d (%.3f)   %4d of %d (%.3f)   %14.4f   %d of %d (%.3f)"
                  % (s, fw, n, fw / n, fb, n, fb / n, fl, n, fl / n, max(shares), loo, n, loo / n))
            for name, c in (("within-study", fw), ("between-study", fb), ("lab", fl)):
                if c / n > LIMIT:
                    over.append("s %.1f %s %.3f" % (s, name, c / n))
    print()
    if over:
        print("  FLAG rate above %.2f: %s -> reported; no threshold set" % (LIMIT, "; ".join(over)))
    else:
        print("  no FLAG rate above %.2f" % LIMIT)


if __name__ == "__main__":
    main()
