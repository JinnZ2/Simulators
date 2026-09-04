#!/usr/bin/env python3
"""Runs the four checks in decreasing order of access requirement. P3
and P4 always run (P3 on a local corpus directory, P4 on nothing). P2
runs on a local source file. P1 runs only when a directory of methods
sections is supplied; none is shipped and none is invented.

    python3 run_all.py [--methods DIR] [--corpus DIR --term WORD] [--target FILE] [--out-dir DIR]
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p1_deps_extract as P1  # noqa: E402
import p2_substrate_audit as P2  # noqa: E402
import p3_comprehension as P3  # noqa: E402
import p4_goal_coherence as P4  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--methods", help="directory of plaintext methods sections, one file per result")
    ap.add_argument("--corpus", default=os.path.join(HERE, "..", "uninstrumented", "cases"))
    ap.add_argument("--term", default="mechanism")
    ap.add_argument("--target", default=os.path.join(HERE, "p4_goal_coherence.py"))
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--out-dir")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("run_all has no selftest; run selftest_csp.py", file=sys.stderr)
        return 2
    out = (lambda name: os.path.join(a.out_dir, name)) if a.out_dir else (lambda name: None)
    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
    blocks = []
    if a.methods:
        _, rep = P1.run(a.methods, out("deps.jsonl"))
        blocks.append(P1.render_report(rep))
    else:
        blocks.append("P1 dependency records: NOT_RUN -- no --methods DIR supplied; no methods section is shipped")
    res2 = P2.audit(a.target)
    if a.out_dir:
        with open(out("contracts.jsonl"), "w", encoding="utf-8") as fh:
            import json
            for r in res2["records_list"]:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    blocks.append(P2.render(res2))
    res3 = P3.run(a.corpus, a.term, null="shuffle")
    if a.out_dir:
        import json
        with open(out("consistency.json"), "w", encoding="utf-8") as fh:
            json.dump(res3, fh, indent=1, sort_keys=True)
    blocks.append(P3.render(res3))
    rows = P4.run(50, P4.grid("0.0:1.0:0.05"), a.trials, 10, 0)
    if a.out_dir:
        import json
        with open(out("coherence.jsonl"), "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps({k: v for k, v in r.items() if k != "_steps"}, sort_keys=True) + "\n")
    blocks.append(P4.render(rows, hist_at=(0.3, 0.5)))
    print("\n\n".join(blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
