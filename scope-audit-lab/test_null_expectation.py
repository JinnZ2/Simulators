#!/usr/bin/env python3
"""Checks for null_expectation.py (SAL-WO1). Stdlib only.

The decisive check runs the lab's OWN null_baseline_scan, unmodified, at
many replications and requires its mean flag count to sit inside a stated
tolerance of the closed form, for both of the lab's distributions. A
closed form that disagreed with the instrument it describes would be a
second figure, not a known answer.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "lab_0_3"))

import null_expectation as ne  # noqa: E402
from scope_audit_lab.experiments import null_baseline_scan  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


# --- closed forms by hand
ok("uniform th=0 -> P=1", ne.p_exceed_uniform(100, 0) == 1.0)
ok("uniform th=10,w=100 -> 0.81", abs(ne.p_exceed_uniform(100, 10) - 0.81) < 1e-12)
ok("uniform th=w -> 0", ne.p_exceed_uniform(100, 100) == 0.0)
ok("uniform th>w -> 0, not negative", ne.p_exceed_uniform(100, 150) == 0.0)
ok("uniform width 0 -> None", ne.p_exceed_uniform(0, 1) is None)
ok("normal th=0 -> P=1", ne.p_exceed_normal(1.0, 0) == 1.0)
ok("normal th=2sd -> erfc(1)", abs(ne.p_exceed_normal(1.0, 2.0) - math.erfc(1)) < 1e-15)
ok("normal sd<=0 -> None", ne.p_exceed_normal(0, 1) is None)
ok("expected flags 12 cases at .81 -> 8.91", abs(ne.expected_flags(12, 0.81) - 8.91) < 1e-12)
ok("one case -> None (no pair), not 0", ne.expected_flags(1, 0.81) is None)

# --- states
v, st = ne.from_generator("uniform", {"low": 0, "high": 100}, 10, 12, "relative")
ok("relative kind -> NOT_DERIVED, no number", v is None and st.startswith("NOT_DERIVED"))
v, st = ne.from_generator("cauchy", {}, 10, 12)
ok("unknown distribution -> NOT_DERIVED", v is None and st.startswith("NOT_DERIVED"))
v, st = ne.from_generator("uniform", {"low": 0, "high": 100}, 10, 1)
ok("one case -> NO_DENOMINATOR", v is None and st == "NO_DENOMINATOR")

# --- the shipped null record
x = ne.read_null_record(ne.first_null_record(ne.DEFAULT_STREAM))
ok("shipped record: expected 8.91", abs(x["expected"] - 8.91) < 1e-9)
ok("shipped record: recorded 8.88 within 0.1", abs(x["gap"]) < 0.1)

# --- the lab's own generator, unmodified, against the closed form
for dist, params, th in (("uniform", {"low": 0.0, "high": 100.0}, 10.0),
                         ("uniform", {"low": 0.0, "high": 100.0}, 60.0),
                         ("normal", {"mean": 0.0, "sd": 5.0}, 7.0)):
    kw = dict(low=params.get("low", 0.0), high=params.get("high", 100.0)) if dist == "uniform" \
        else dict(mean=params["mean"], sd=params["sd"])
    rec = null_baseline_scan(n_cases=12, n_replications=4000, threshold=th, seed=11,
                             distribution=dist, **kw)
    got = rec["recorded_summary"]["mean_candidate_regions"]
    want, _ = ne.from_generator(dist, rec["generator"]["parameters"], th, 12)
    # 4000 replications x 11 dependent pairs: a 0.1 tolerance on the mean is
    # several standard errors wide on the scale of these counts.
    ok(f"lab {dist} th={th:g}: mean {got:.3f} vs closed form {want:.3f}", abs(got - want) < 0.1)

# --- the module refuses --selftest
src = (HERE / "null_expectation.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)

failed = [n for n, c in checks if not c]
for n, c in checks:
    print(("PASS " if c else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
