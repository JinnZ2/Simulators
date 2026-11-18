"""Toolkit gate: the check every tool passes before it is trusted. stdlib only.

Work order 2026-11-11 (toolkit build, staged): every tool, before trusted, has
  - known-answer planted cases, some that must fire and some that must stay silent
  - a null harness: FP = 0 and TP = 1 on its declared null and signal draws

A tool's gate result is written into its toolkit entry (field `gate`) and
re-run by `python3 tools/check_ledger.py --tests`. A NEEDS_TOOL row may move to
the cleared table only when the tool's gate reads PASS (tools/check_ledger.py).

What the gate does NOT establish: FP = 0 on n draws is a property of the
threshold, the draw count and the draw distribution, not proof the detector
never misfires. Each tool states the threshold that buys it.
"""
import random

VERDICTS = ("PASS", "CONSTANT_SILENT", "CONSTANT_FIRES", "NO_DISCRIMINATION", "FAIL_FP", "FAIL_TP")


def known_answers(cases, fn):
    """cases: list of (name, expected, *args). fn(*args) -> got. Returns rows and PASS/FAIL."""
    rows = []
    for name, expect, *args in cases:
        got = fn(*args)
        rows.append(dict(name=name, expect=expect, got=got, ok=(got == expect)))
    fires = sum(1 for r in rows if r["expect"] not in (False, None, "SILENT"))
    return dict(rows=rows, n=len(rows), failed=[r["name"] for r in rows if not r["ok"]],
                verdict="PASS" if all(r["ok"] for r in rows) else "FAIL", n_expect_fire=fires)


def null_harness(detector, draw_null, draw_signal, n=200, seed=0):
    """detector(x) -> bool. draw_*(rng) -> x. FP over n null draws, TP over n signal draws."""
    rng = random.Random(seed)
    fp = sum(bool(detector(draw_null(rng))) for _ in range(n)) / n
    tp = sum(bool(detector(draw_signal(rng))) for _ in range(n)) / n
    if fp == 0 and tp == 1:
        v = "PASS"
    elif tp == 0 and fp == 0:
        v = "CONSTANT_SILENT"
    elif tp == 1 and fp == 1:
        v = "CONSTANT_FIRES"
    elif tp <= fp:
        v = "NO_DISCRIMINATION"
    elif fp > 0:
        v = "FAIL_FP"
    else:
        v = "FAIL_TP"
    return dict(fp=fp, tp=tp, n=n, seed=seed, verdict=v)


def null_harness_seeds(detector, draw_null, draw_signal, n=200, seeds=(0, 1, 2, 3, 4)):
    """The same harness over several harness seeds; the worst fp and tp are reported.
    A gate that passes on one harness seed and not on the next is not passed: picking
    the seed that passes is the cherry-pick the harness exists to catch."""
    runs = [null_harness(detector, draw_null, draw_signal, n, s) for s in seeds]
    fp, tp = max(r["fp"] for r in runs), min(r["tp"] for r in runs)
    worst = next((r["verdict"] for r in runs if r["verdict"] != "PASS"), "PASS")
    return dict(fp=fp, tp=tp, n=n, seed=f"{seeds[0]}-{seeds[-1]}", verdict=worst, per_seed=[r["verdict"] for r in runs])


def combine(known, legs):
    """legs: {name: null_harness result}. PASS only when known answers and every leg pass."""
    ok = known["verdict"] == "PASS" and all(l["verdict"] == "PASS" for l in legs.values())
    return dict(verdict="PASS" if ok else "FAIL", known=known, legs=legs)


def summary(g):
    """The compact form stored in a toolkit entry's `gate` field."""
    return dict(verdict=g["verdict"], known_answer=f"{g['known']['n'] - len(g['known']['failed'])} of {g['known']['n']}",
                null_legs={k: f"fp {v['fp']} tp {v['tp']} n {v['n']} seed {v['seed']} {v['verdict']}" for k, v in g["legs"].items()})


if __name__ == "__main__":
    print("refused: library. Gates run from forest-model-ledger/tests/test_toolkit.py")
    raise SystemExit(2)
