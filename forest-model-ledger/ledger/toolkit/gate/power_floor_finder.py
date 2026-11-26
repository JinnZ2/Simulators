# SPDX-License-Identifier: CC0-1.0
"""Finder power floor (work order TK-G1 follow-up 2, 2026-11-24).
Standard library only.  Synthetic rows only; no real row is read.

    python3 ledger/toolkit/gate/power_floor_finder.py

The sweep, its seeds, the null maximum and the floor rule are read from
the last amendment in gate/DECLARED.json, committed before this was run.
Nothing here changes a threshold.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import gate_missing_column_finder as gate  # noqa: E402
import missing_column_finder_stdlib as finder  # noqa: E402

NEED = 19


def main():
    declared = [a for a in json.load(open(os.path.join(HERE, "DECLARED.json")))["amendments"]
                if "power_floor_sweep" in a][-1]["power_floor_sweep"]
    null_max, reps = declared["null_max"]["value"], declared["replicates"]
    print("power_floor_finder: %d replicates per planted s, design %d studies x %d rows, %d levels"
          % (reps, gate.STUDIES, gate.ROWS, gate.LEVELS))
    print("  declared null max %.4f; floor = smallest s with >= %d of %d above it" % (null_max, NEED, reps))
    print()
    print("  planted s   realized (mean)   recovered mean      min      max   above null max"
          "   finder FLAG   bias (recovered / realized)")
    floor = None
    for si, s in enumerate(declared["planted_s"]):
        real, rec, flags = [], [], 0
        for rep in range(reps):
            seed = gate.SEED + 2000000 + 1000 * si + rep
            rows, realized = gate.dataset(s, seed)
            _, w = gate.read(rows, perm_seed=seed, n_perm=finder.N_PERM)
            real.append(realized)
            rec.append(w["share"])
            flags += w["flag"]
        above = sum(x > null_max for x in rec)
        if floor is None and above >= NEED:
            floor = s
        print("  %9.2f   %15.4f   %14.4f   %6.4f   %6.4f   %8d of %d   %5d of %d   %10.3f"
              % (s, sum(real) / reps, sum(rec) / reps, min(rec), max(rec), above, reps,
                 flags, reps, sum(rec) / sum(real)))
    print()
    print("  floor: %s" % ("planted s = %.2f" % floor if floor is not None
                           else "NOT REACHED in this sweep"))


if __name__ == "__main__":
    main()
