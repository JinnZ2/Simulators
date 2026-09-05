#!/usr/bin/env python3
"""run_all.py -- inventory -> extract -> checks -> queue, to stdout.
Operates on a local checkout (argv roots, default the checkout root). No
network. Stdlib only.

    python3 run_all.py [root ...]
    python3 run_all.py --write         # also (re)write QUEUE.md
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import inventory as I  # noqa: E402
import queue as Q  # noqa: E402


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("run_all has no selftest; run selftest_fa.py", file=sys.stderr)
        return 2
    roots = [a for a in argv if not a.startswith("-")] or None
    print("=" * 70)
    print(I.render(roots))
    print("\n" + "=" * 70)
    print(Q.render(roots))
    if "--write" in argv:
        Q.main((roots or []) + ["--write"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
