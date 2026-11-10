"""Tests for meander-ledger. Ids match ledger/tests.yaml. stdlib only.

    python3 tests/test_meander.py     # one line per test and the count; exit 1 on any FAIL

Each test function is named by its id. run_all() returns {id: PASS | FAIL | NOT_TESTABLE}
so the forest checker (forest-model-ledger/tools/check_ledger.py --tests, via the
tests/test_l0.py shim) can read admitting tests. NOT_TESTABLE is not PASS.
"""
import csv, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from model import meander, l0_audit
from tools import scatter

FOREST = os.path.join(os.path.dirname(HERE), "forest-model-ledger")
SHORT = dict(E=0.3, steps=300)


class NotTestable(Exception):
    pass


_cache = {}


def run(seed=0, **kw):
    key = (seed, repr(sorted(kw.items())))
    if key not in _cache:
        r = meander.run(dict(SHORT, **kw), seed=seed, record_every=100)
        _cache[key] = (r, l0_audit.audit(r))
    return _cache[key]


def T_SED_CLOSURE():
    r, a = run()
    assert a["sediment"]["verdict"] == "CLOSED", a["sediment"]
    assert r["ledger"]["bank_input"] > 0 and r["ledger"]["inflow"] > 100, "closed on a trivial throughput"


def T_SED_LEAK_DETECTED():
    _, a = run(leak=0.05)
    assert a["sediment"]["verdict"] == "LEAK" and a["_overall"] == "FAIL", a["sediment"]
    assert run()[1]["_overall"] == "PASS", "clean run must not read as a leak"


def T_VOID_PRINTED():
    _, a = run()
    b = a["sediment"]["boundary"]
    assert b["groundwater"] is None and b["overbank_fines"] is None
    assert a["momentum"]["verdict"] == "VOID" and a["momentum"]["misclosure"] is None
    assert "momentum" in a["_void"]
    txt = l0_audit.report(a)
    assert re.search(r"groundwater\s*[:=]?\s*void", txt), txt
    assert "momentum  VOID" in txt


def T_IDENTITY_FLAGGED():
    _, a = run()
    assert sorted(a["_identity"]) == ["energy", "water"], a["_identity"]
    assert a["sediment"]["identity"] is False
    assert l0_audit.report(a).count("IDENTITY") >= 2


def T_VERDICT_AGREES_FOREST():
    code = ("import sys; sys.path.insert(0, %r); from model import l0_audit as f; "
            "cases=[(0.0,10.0),(1e-12,10.0),(1e-6,10.0),(5.0,1.0),(-3e-9,0.5)]; "
            "print([f.verdict(m,t) for m,t in cases])") % FOREST
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if p.returncode != 0:
        raise NotTestable("forest verdict did not import: " + p.stderr.strip().splitlines()[-1])
    forest = eval(p.stdout.strip())
    mine = [l0_audit.verdict(m, t) for m, t in [(0.0, 10.0), (1e-12, 10.0), (1e-6, 10.0), (5.0, 1.0), (-3e-9, 0.5)]]
    assert mine == forest, (mine, forest)


def T_ALPHA_ONLY():
    # aspect 10 with Cf 0.01 and aspect 20 with Cf 0.005 share alpha = 2 Cf / H = 0.2
    r1, _ = run(aspect=10.0)
    r2, _ = run(Cf=0.005)
    assert abs(r1["alpha"] - r2["alpha"]) < 1e-12
    assert r1["x"] == r2["x"] and r1["y"] == r2["y"], "equal alpha but different planform"
    r3, _ = run(Cf=0.02)
    assert r3["x"] != r1["x"], "a different alpha must move the planform (else the test is silent)"


def T_SUPPLY_NO_PLANFORM():
    lo, _ = run(supply=0.2)
    hi, _ = run(supply=2.0)
    assert lo["x"] == hi["x"] and lo["y"] == hi["y"]
    assert lo["ledger"]["store"] != hi["ledger"]["store"], "supply must move the bed store"


def T_SCATTER_KNOWN():
    cols = ["Water-surface width (m)", "Wavelength (m)", "Meander length (m)", "Sinuosity",
            "wavelength", "Slope (degrees)", "MAJOR1", "Province", "Meander Class"]
    rows = []
    for i in range(1, 41):
        w = 10.0 * i
        lam = 12.0 * w
        for k in range(2):            # two points per meander, widths w and w (median w)
            rows.append([w, lam, 100.0 + i, 1.5, lam, 1.0, "Sand", "P", "Mature"])
    rows.append([50.0, -9999, 1, 1, 1, 1, "Sand", "P", "Mature"])   # sentinel
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
        wr = csv.writer(f)
        wr.writerow(cols)
        wr.writerows(rows)
        path = f.name
    try:
        a = scatter.analyse(path)
    finally:
        os.unlink(path)
    assert a["counts"]["meanders"] == 40 and a["counts"]["sentinel"] == 1, a["counts"]
    assert abs(a["ratio"]["median"] - 12.0) < 1e-9, a["ratio"]
    assert abs(a["loglog_fit"][0] - 1.0) < 1e-9
    assert a["null"]["r2_max"] < 0.5
    assert a["counts"]["mixed_cls"] == 0


def T_CARDS_READ():
    # subprocess: both folders ship packages named tools/ and model/, which collide in one process
    code = ("import sys; sys.path.insert(0, %r); from ledger.toolkit import coincidence_card as cc; "
            "cards = cc.load_all(%r); "
            "print([(n, cc.read(c)[0], c['reading_declared']) for n, c in sorted(cards.items())])") % (FOREST, HERE)
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if p.returncode != 0:
        raise NotTestable("forest coincidence_card did not run: " + p.stderr.strip().splitlines()[-1])
    rows = eval(p.stdout.strip())
    assert len(rows) >= 4, rows
    for n, derived, declared in rows:
        assert derived == declared, (n, derived, declared)


QFIELDS = ["question", "layer", "raised_by", "instrument", "cross_domain", "status"]


def T_QUESTIONS_SCHEMA():
    text = open(os.path.join(HERE, "QUESTIONS.md"), encoding="utf-8").read()
    blocks = re.split(r"^### (Q-\d+)\s*$", text, flags=re.M)[1:]
    assert blocks, "no questions"
    ids = blocks[0::2]
    assert len(ids) == len(set(ids)), "duplicate question id"
    for qid, body in zip(blocks[0::2], blocks[1::2]):
        for f in QFIELDS:
            assert re.search(rf"^{f}\s*:\s*\S", body, re.M), (qid, f)
        lay = re.search(r"^layer\s*:\s*(.*)$", body, re.M).group(1)
        assert re.search(r"\bL[0-5]\b", lay), (qid, lay)
        st = re.search(r"^status\s*:\s*(.*)$", body, re.M).group(1).strip()
        assert st.startswith("OPEN"), (qid, "status must be a placeholder, not an answer: " + st)


TESTS = [T_SED_CLOSURE, T_SED_LEAK_DETECTED, T_VOID_PRINTED, T_IDENTITY_FLAGGED, T_VERDICT_AGREES_FOREST,
         T_ALPHA_ONLY, T_SUPPLY_NO_PLANFORM, T_SCATTER_KNOWN, T_CARDS_READ, T_QUESTIONS_SCHEMA]


def run_all(verbose=False):
    out = {}
    for t in TESTS:
        try:
            t()
            out[t.__name__] = "PASS"
        except NotTestable as e:
            out[t.__name__] = "NOT_TESTABLE"
            if verbose:
                print(f"  {t.__name__}: {e}")
        except Exception as e:
            out[t.__name__] = "FAIL"
            if verbose:
                print(f"  {t.__name__}: {type(e).__name__}: {e}")
    return out


if __name__ == "__main__":
    res = run_all(verbose=True)
    for k, v in res.items():
        print(f"{v:13s} {k}")
    print(f"checks: {len(res)}   failed: {sum(v == 'FAIL' for v in res.values())}   "
          f"not_testable: {sum(v == 'NOT_TESTABLE' for v in res.values())}")
    sys.exit(1 if any(v == "FAIL" for v in res.values()) else 0)
