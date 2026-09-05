#!/usr/bin/env python3
"""run_all.py -- emit the full survey report to stdout. No input, no
network. Stdlib only.

    python3 run_all.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import report as R  # noqa: E402


def main():
    if "--selftest" in sys.argv:
        print("run_all has no selftest; run selftest_ds.py", file=sys.stderr)
        return 2
    print(R.full_report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
