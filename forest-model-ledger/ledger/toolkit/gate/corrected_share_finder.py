# SPDX-License-Identifier: CC0-1.0
"""Finder: noise-floor-corrected share (work order TK-G1 follow-up 3,
2026-11-24).  Standard library only.  Synthetic rows only.

    python3 ledger/toolkit/gate/corrected_share_finder.py

REPORT ONLY.  No threshold is read, set or changed here.

    corrected share = recovered share - null median
    null median     = median recovered share over 200 shuffles of the
                      planted labels, at the same planted s (replicate 0)

Tag: DERIVED (basis: OBSERVED).  The recovered and realized shares are the
gate's and the sweep's own (same seeds, recomputed here; the share does
not depend on the finder's inner shuffles, so they are set to 1).  The
subtraction is the derived step.

Seeds: s in {0.1, 0.3, 0.5} use the gate's (gate_missing_column_finder);
s in {0.02, 0.03, 0.05, 0.07} use the power-floor sweep's for the
replicates, and SEED + 2500000 + index for the null shuffles.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import gate_missing_column_finder as gate  # noqa: E402

SWEEP = [0.02, 0.03, 0.05, 0.07]
SHUFFLES = 200


def share(rows, seed):
    return gate.read(rows, perm_seed=seed, n_perm=1)[1]["share"]


def null_median(rows, seed, shuffle_seed):
    rng = random.Random(shuffle_seed)
    got = []
    for _ in range(SHUFFLES):
        labels = [r["planted"] for r in rows]
        rng.shuffle(labels)
        got.append(share([dict(r, planted=lab) for r, lab in zip(rows, labels)], seed))
    return gate.pct(got, 0.5)


def main():
    print("corrected_share_finder: REPORT ONLY, thresholds unchanged.  Tag: DERIVED (basis: OBSERVED)")
    print("  corrected = recovered mean - null median (%d shuffles at the same s); %d replicates"
          % (SHUFFLES, gate.REPS))
    print()
    print("  planted s   realized   recovered   null median   corrected   recovered/realized"
          "   corrected/realized")
    cases = [(s, gate.SEED + 2000000 + 1000 * i, gate.SEED + 2500000 + i) for i, s in enumerate(SWEEP)]
    cases += [(s, gate.SEED + 1000 * i, gate.SEED + 500000 + i) for i, s in enumerate(gate.SHARES)]
    for s, base, shuffle_seed in cases:
        real, rec = [], []
        for rep in range(gate.REPS):
            rows, realized = gate.dataset(s, base + rep)
            real.append(realized)
            rec.append(share(rows, base + rep))
        rows0, _ = gate.dataset(s, base)
        med = null_median(rows0, base, shuffle_seed)
        r, m = sum(real) / gate.REPS, sum(rec) / gate.REPS
        print("  %9.2f   %8.4f   %9.4f   %11.4f   %9.4f   %18.3f   %18.3f"
              % (s, r, m, med, m - med, m / r, (m - med) / r))


if __name__ == "__main__":
    main()
