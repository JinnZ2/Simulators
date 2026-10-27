#!/usr/bin/env python3
"""SAL-WO5 evidence: grade the lab's transition engine with this repo's own
null-harness, as one concrete test of whether the two tool families fit.

Gate under test: "scan_transitions flags at least one candidate region"
(the lab, unmodified). Graded by null-harness.bake_off (imported by path,
unmodified) on two regimes:

    demo regime   uniform noise on [0, 100], threshold 10 (the lab's shipped null)
    quiet regime  normal noise, sd 1, threshold 10

each against a positive control: the same noise plus one planted step of
+30 at the midpoint. 12 cases per draw, matching the lab's demo.

null-harness needs numpy; without it this prints NOT_RUN and exits 0.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE / "lab_0_3"))

try:
    import numpy  # noqa: F401
except ImportError:
    print("fold_probe: NOT_RUN (null-harness needs numpy, which is not installed)")
    sys.exit(0)

from scope_audit_lab.transitions import Case, scan_transitions  # noqa: E402

spec = importlib.util.spec_from_file_location("_null_harness", ROOT / "null-harness" / "null_harness.py")
nh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nh)

N = 12
STEP = 30.0
THRESHOLD = 10.0


def gate(series):
    cases = [Case(f"c{i}", float(i), float(v)) for i, v in enumerate(series)]
    return len(scan_transitions(cases, threshold=THRESHOLD)["candidate_regions"]) > 0


def uniform(rng):
    return rng.uniform(0, 100, N)


def normal(rng):
    return rng.normal(0, 1, N)


def with_step(gen):
    def g(rng):
        x = gen(rng).copy()
        x[N // 2:] += STEP
        return x
    return g


def run(draws=1000):
    rows = []
    for name, gen in (("demo regime: uniform[0,100], th 10", uniform),
                      ("quiet regime: normal sd 1, th 10", normal)):
        r = nh.bake_off(gate, gen, with_step(gen), n_draws=draws)
        rows.append((name, r))
    return rows


def render(rows):
    out = ["scope-audit-lab / fold_probe.py (null-harness grading the lab engine)", "=" * 70,
           f"gate: scan flags >= 1 region; {N} cases; positive control adds a +{STEP:g} step", ""]
    for name, r in rows:
        out.append(f"{name:<40} FP {r['FP']:.3f}  TP {r['TP']:.3f}  -> {r['verdict']}")
    out += ["", "the same engine grades CONSTANT_FIRES or OK depending only on the noise",
            "width against the threshold: the grade is a property of the regime, which",
            "is the SAL_004 reading, here produced by the repo's own grader."]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("fold_probe.py is a probe; its result is pinned in test_fold_probe.py")
        sys.exit(2)
    print(render(run()))
