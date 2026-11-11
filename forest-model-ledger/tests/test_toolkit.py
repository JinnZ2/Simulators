"""Toolkit gates (work order 2026-11-11, toolkit build, staged). stdlib only.

Every tool the brief names passes a gate before it is trusted: known-answer planted
cases (some fire, some stay silent) and a null harness with FP = 0 and TP = 1 on
its declared draws, over harness seeds 0-4. The result is stored in the tool's
entry (field `gate`); tools/check_ledger.py --tests re-runs this and fails on drift.

    python3 tests/test_toolkit.py            # one line per tool and per leg; exit 1 on any FAIL
    python3 tests/test_toolkit.py --detail   # every known-answer row
"""
import importlib, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from ledger.toolkit import gate as G

# tool id -> module in ledger/toolkit/. Order is the build order of the work order.
GATED = ["multi_seed_ensemble"]


def run(tool):
    mod = importlib.import_module(f"ledger.toolkit.{tool}")
    return mod.gate()


def run_all():
    return {t: run(t) for t in GATED}


if __name__ == "__main__":
    res = run_all()
    bad = 0
    for t, g in res.items():
        s = G.summary(g)
        print(f"{s['verdict']:4s}  {t:24s} known {s['known_answer']}")
        for leg, line in s["null_legs"].items():
            print(f"      {'':24s} null[{leg}] {line}")
        if "--detail" in sys.argv:
            for r in g["known"]["rows"]:
                print(f"      {'ok ' if r['ok'] else 'BAD'} {r['name']}: expect {r['expect']!r} got {r['got']!r}")
        bad += s["verdict"] != "PASS"
    print(f"{len(res)} tools gated, {bad} failed")
    sys.exit(1 if bad else 0)
