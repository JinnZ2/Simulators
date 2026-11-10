"""L0 tests. Ids match ledger/tests.yaml.

    python3 tests/test_l0.py        # prints one line per test and the count; exit 1 on any FAIL
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import base, l0_audit

_cache = {}


def run(**kw):
    key = repr(sorted(kw.items()))
    if key not in _cache:
        res = base.simulate(**kw)
        _cache[key] = (res, l0_audit.audit(res))
    return _cache[key]


def T_L0_N_CLOSURE():
    _, a = run()
    assert a["N"]["verdict"] == "CLOSED", a["N"]
    assert a["N"]["boundary_in"] > 100, "budget closed on a trivial throughput"


def T_L0_WATER_CLOSURE():
    assert run()[1]["water"]["verdict"] == "CLOSED"


def T_L0_DT_HALF():
    assert run(dt=1 / 104)[1]["N"]["verdict"] == "CLOSED"


def T_L0_LEAK_DETECTED():
    _, a = run(params=dict(leak=0.3))
    assert a["N"]["verdict"] == "LEAK" and a["_overall"] == "FAIL"
    assert a["water"]["verdict"] == "CLOSED", "leak in N must not be blamed on water"
    assert run()[1]["_overall"] == "PASS", "clean run must not read as a leak"


def T_L0_NOISE_ARM():
    v = l0_audit.verdict
    assert v(1e-12, 100.0) == "CLOSED"
    assert v(0.5, 100.0, sigma_meas=0.3) == "NOISE"
    assert v(0.7, 100.0, sigma_meas=0.3) == "LEAK"
    assert v(0.5, 100.0, sigma_meas=None) == "LEAK", "no sigma: NOISE must be unreachable"


def T_L0_VOID_NEVER_CLOSED():
    _, a = run()
    for k in ("C", "P", "energy"):
        assert a[k]["verdict"] == "VOID" and a[k]["misclosure"] is None
    assert a["_void_budgets"] == ["C", "P", "energy"]


def T_L0_VOID_TERMS_PRINTED():
    _, a = run()
    for k in base.VOID_TERMS:
        assert a["N"]["terms"][k] is None
    text = l0_audit.report(a)
    assert text.count("=void") == len(base.VOID_TERMS)


def T_L0_FIRE_EVENT_CONSERVES():
    res = base.simulate(years=1, fires=False)
    y0 = res["y"].copy()
    out = base.fire(res["y"], res["params"])
    assert out > 0
    d_pools = sum(res["y"][base.IX[k]] - y0[base.IX[k]] for k in base.N_POOLS)
    assert abs(d_pools + out) < 1e-12, d_pools + out


TESTS = [T_L0_N_CLOSURE, T_L0_WATER_CLOSURE, T_L0_DT_HALF, T_L0_LEAK_DETECTED, T_L0_NOISE_ARM,
         T_L0_VOID_NEVER_CLOSED, T_L0_VOID_TERMS_PRINTED, T_L0_FIRE_EVENT_CONSERVES]


def run_all():
    results = {}
    for t in TESTS:
        try:
            t()
            results[t.__name__] = "PASS"
        except AssertionError as e:
            results[t.__name__] = f"FAIL {e}"
    return results


if __name__ == "__main__":
    r = run_all()
    for k, v in r.items():
        print(f"{v[:4]}  {k}  {v[5:]}")
    bad = sum(v != "PASS" for v in r.values())
    print(f"{len(r)} tests, {bad} failed")
    sys.exit(1 if bad else 0)
