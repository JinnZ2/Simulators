#!/usr/bin/env python3
"""
run_all.py - run the three screens in order and print them together.

    1. tenability      how t_available moves with volume and containment
    2. t_hold          what the enclosure must therefore survive, per line
    3. detection_loop  whether detection or containment carries the outcome

stdlib only. CC0.
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("TENABILITY", ["tenability.py"]),
    ("REQUIRED HOLD TIME", ["t_hold.py",
                            "--lines", os.path.join(HERE, "params",
                                                    "example_lines.json")]),
    ("DETECTION LOOP", ["detection_loop.py", "--trials", "8000"]),
]


def main():
    for title, argv in STEPS:
        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)
        r = subprocess.run([sys.executable, os.path.join(HERE, argv[0])]
                           + argv[1:], cwd=HERE)
        if r.returncode != 0:
            print("step failed: %s" % argv[0])
            return 1
    print("\n" + "=" * 70)
    print("envelope of these outputs is stated in README.md. they are")
    print("configuration comparisons, not predictions. see CLAIMS.md for")
    print("what would falsify each result.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
