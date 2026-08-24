#!/usr/bin/env python3
"""runner. stdlib only. CC0.

ORDER IS NOT ARBITRARY.
    D first  — discriminator. Its outcome constrains how A is read.
    B second — independent, safe to run.
    C third  — CURRENTLY DEFECTIVE (see RESULTS.md). Runs, means nothing.
    A last   — BLOCKED on D. Skipped unless --force-a.

usage:
    python3 run_all.py
    python3 run_all.py --quick
    python3 run_all.py --force-a
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PLAN = [
    ("SIM-D  temperature null [DISCRIMINATOR]",
     "sim_d_temperature_null.py", ["--samples", "3000"], True),
    ("SIM-B  entropy depletion",
     "sim_b_entropy_depletion.py", ["--sweep", "--gens", "12",
                                    "--corpus", "3000"], True),
    ("SIM-C  loop threshold [DEFECTIVE — output not readable]",
     "sim_c_loop_threshold.py", ["--grid", "5", "--iters", "150"], True),
    ("SIM-A  field vs coupling [BLOCKED on SIM-D]",
     "sim_a_field_vs_coupling.py", ["--n", "16", "--steps", "120",
                                    "--trials", "24"], False),
]


def main():
    quick = "--quick" in sys.argv
    force_a = "--force-a" in sys.argv

    for label, script, args, enabled in PLAN:
        if not enabled and not force_a:
            print("\n" + "=" * 64)
            print(label)
            print("=" * 64)
            print("SKIPPED. SIM-D invalidated the temperature leg of this")
            print("mapping. Output would have no interpretation.")
            print("Override with --force-a if you know why you want it.")
            continue
        print("\n" + "=" * 64)
        print(label)
        print("=" * 64)
        a = list(args)
        if quick:
            a = [x for x in a]
        try:
            subprocess.run([sys.executable,
                            os.path.join(HERE, script)] + a, timeout=1800)
        except subprocess.TimeoutExpired:
            print("TIMEOUT — reduce grid/samples and retry")

    print("\n" + "=" * 64)
    print("Findings go in RESULTS.md. Log failures as failures.")
    print("Do not tune parameters until an expected result appears.")
    print("=" * 64)


if __name__ == "__main__":
    main()
