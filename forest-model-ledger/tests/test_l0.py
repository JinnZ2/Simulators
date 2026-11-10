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


def T_L0_SEED_WIRED_TO_IGNITION():
    seqs = set()
    for seed in range(4):
        res, _ = run(seed=seed, years=100, params=dict(drought_sd=0.0))
        assert abs(res["y"][base.IX["precipitation"]] - 100.0) < 1e-9, "precipitation must be identical across seeds here"
        seqs.add(tuple(round(e[0], 6) for e in res["events"]))
    assert len(seqs) == 4, f"{len(seqs)} distinct fire sequences of 4: seed not reaching the ignition draw"


def T_L0_RESIDUAL_IS_DEPOSITION_COUNTER():
    dt, acc = 1.0 / 52, 0.0
    for _ in range(15600):
        acc = acc + dt / 6 * (1.0 + 2 * 1.0 + 2 * 1.0 + 1.0)
    counter = acc - 300.0
    m = run()[1]["N"]["misclosure"]
    assert counter != 0.0 and abs(m + counter) < 0.05 * abs(counter), (m, counter)
    m0 = run(params=dict(dep=0.0))[1]["N"]["misclosure"]
    assert abs(m0) < 1e-12, m0


def _card(states, branch="void"):
    from ledger.toolkit import coincidence_card as cc
    slots = {n: dict(state=s, evidence="void" if s == "void" else "e") for n, s in zip(cc.SLOTS, states)}
    return dict(id="X", observation="o", trigger="t", slots=slots, reading_declared="void", branch=branch, runs=[], open_issues=[])


def T_TK_CARD_READINGS():
    from ledger.toolkit import coincidence_card as cc
    r = "ruled_out"
    assert cc.read(_card(["supported", "void", r, r, r, "void"]))[0] == "OPEN"
    reading, d = cc.read(_card(["supported", r, r, "supported", r, r]))
    assert reading == "RESOLVED" and d["supported"] == ["shared_constraint", "numerical_artifact"]
    assert cc.read(_card([r, r, r, r, r, "supported"], branch="BR_X"))[0] == "CURIOSITY"
    bad = [_card([r, r, r, r, r, "supported"]),                  # curiosity with no branch
           _card(["supported", r, r, r, r, "supported"]),        # none_of_above declared against the derivation
           _card([r, r, r, r, r, "ruled_out"], branch="BR_X")]   # all five ruled out, none_of_above denied
    c = _card(["supported", r, r, r, r, r]); c["slots"]["shared_constraint"]["evidence"] = "void"; bad.append(c)
    for b in bad:
        try:
            cc.read(b)
        except cc.CardError:
            continue
        raise AssertionError("malformed card accepted")
    c = _card(["supported", r, r, r, r, r]); del c["branch"]
    try:
        cc.read(c); raise AssertionError("dropped field accepted")
    except cc.CardError:
        pass


def T_TK_BUDGET_CLOSURE_MOVED():
    from ledger.toolkit import budget_closure
    assert l0_audit.audit is budget_closure.audit and l0_audit.verdict is budget_closure.verdict


TESTS = [T_L0_SEED_WIRED_TO_IGNITION, T_L0_RESIDUAL_IS_DEPOSITION_COUNTER, T_TK_CARD_READINGS, T_TK_BUDGET_CLOSURE_MOVED,
         T_L0_N_CLOSURE, T_L0_WATER_CLOSURE, T_L0_DT_HALF, T_L0_LEAK_DETECTED, T_L0_NOISE_ARM,
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
