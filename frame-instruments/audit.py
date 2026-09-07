"""Audit of frame-instruments, computed rather than asserted. Imports the
build modules by path (unique names, so the audit itself cannot suffer
FI_001) and edits nothing. Every finding prints the number that decides
it. Same-node: builder and auditor are one system (FI_010); the numbers
are the part anyone can recompute.

Command: python3 audit.py
"""
import importlib.util
import io
import os
import random
import sys
import unittest
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(build, name):
    sys.path.insert(0, os.path.join(HERE, build))
    spec = importlib.util.spec_from_file_location("%s_%s" % (build, name), os.path.join(HERE, build, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    return mod


def fi_001():
    """module-name collision across builds under one process"""
    t1, t4 = load("b1", "test_b1"), load("b4", "test_b4")
    res = []
    for m in (t1, t4):
        r = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.defaultTestLoader.loadTestsFromModule(m))
        res.append((r.testsRun, len(r.failures) + len(r.errors)))
    return {"b1_then_b4 (run, failed)": res}, all(f == 0 for _, f in res)


def _fixture12(t, score):
    rng = random.Random(1)
    bases, traces = [], []
    for k in range(12):
        bases.append(t.base_row(i=k))
        n = rng.randrange(0, 120)
        traces.append(t.trace(["x%d_%d" % (k, j) for j in range(n)] + t.BASE_CONT[n:], i=k))
    return score.sweep(bases, traces, t.DS, t.LS)


def fi_002(t, score, summarise):
    """L-axis stability on the top-decile set is 1.0 by construction; separation set moves"""
    summ = summarise.summarise(_fixture12(t, score))
    top = sorted(set(s["jaccard"] for s in summ if s.get("sweep_axis") == "L" and s["position_set"] == "top_decile_div" and s["jaccard"] is not None))
    sep = sorted(set(s["jaccard"] for s in summ if s.get("sweep_axis") == "L" and s["position_set"] == "separation_resync0" and s["jaccard"] is not None))
    return {"top_decile_L_jaccard_values": top, "separation_L_jaccard_values": sep}, top == [1.0] and any(v < 1.0 for v in sep)


def fi_003(order):
    """ordered successor pairs per block"""
    rows, _ = order.assign(4, 7)
    succ = Counter((o[k], o[k + 1]) for o in [r["order"] for r in rows] for k in range(3))
    return {"distinct_pairs": len(succ), "max_count": max(succ.values())}, len(succ) == 12 and max(succ.values()) == 1


def fi_004(agree, lock, t2):
    """a commit appended after release cannot validate a rewritten D1"""
    h = lambda p, q: lock.response_hash({"posed": p, "target": q})
    released = [{"reader_id": "r3", "case_id": "k1", "commit_sha256": h("first", "x")}]
    rows = [t2.resp("r3", "k1", "D1", "whether the pump ran dry", "the pump"), t2.resp("r3", "k1", "D2", "whether the pump ran dry", "the pump")]
    try:
        agree.score(rows, t2.CASES, released, 0.2)
        refused = False
    except agree.Invalid:
        refused = True
    return {"rewritten_D1_refused": refused}, refused


def fi_005(t, score):
    """shifted rejoin: resync and div disagree (recorded, not repaired)"""
    shifted = ["x"] + t.BASE_CONT[:-1]
    s = {(r["D"], r["L"]): r for r in score.sweep([t.base_row()], [t.trace(shifted)], t.DS, t.LS)}
    return {"resync_all_D_all_L": sorted(set(v["resync_D"] for v in s.values())),
            "div_by_D_at_L4": {k[0]: v["div_D"] for k, v in s.items() if k[1] == 4}}, True


def fi_006(t, score, summarise, permute, nulls):
    """N4 rests on one permutation draw: spread over 30 seeds"""
    seps = _fixture12(t, score)
    real = summarise.summarise(seps)
    vals, trig = [], 0
    for seed in range(30):
        n4 = nulls.n4(real, summarise.summarise(permute.permute(seps, seed)))
        vals.append(n4["number"]["mean_adjacent_D_jaccard_permuted"])
        trig += bool(n4["triggered"])
    return {"real": nulls.n4(real, real)["number"]["mean_adjacent_D_jaccard_real"], "permuted_min": min(vals),
            "permuted_max": max(vals), "triggered_of_30": trig}, True


def fi_007(agree, lock, t2):
    """A vs D1 with one auditor per side is NOT EVALUABLE, never a pass"""
    rel = [{"reader_id": "r2", "case_id": "k1", "commit_sha256": lock.response_hash({"posed": "Y", "target": "Q"})}]
    head = agree.score([t2.resp("r1", "k1", "A", "X", "P"), t2.resp("r2", "k1", "D1", "Y", "Q")], t2.CASES, rel, 0.2)[0]
    return {"evaluable": head["evaluable"], "failed": head["failed"]}, head["evaluable"] is False and head["failed"] is None


def fi_008(t, score, summarise):
    """saturated ties: the whole stratum is the top decile and says so"""
    bases = [t.base_row(i=k) for k in range(12)]
    traces = [t.trace(["z%d_%d" % (k, j) for j in range(128)], i=k) for k in range(12)]
    cell = [s for s in summarise.summarise(score.sweep(bases, traces, t.DS, t.LS)) if "n_rows" in s][0]
    return {"top_decile_count": cell["top_decile_count"], "n_tied_at_cutoff": cell["n_tied_at_cutoff"], "n_rows": cell["n_rows"]}, \
        cell["top_decile_count"] == cell["n_rows"] and cell["n_tied_at_cutoff"] == cell["n_rows"] - 2


def main():
    t, score, summarise, permute, nulls = (load("b1", n) for n in ("test_b1", "score", "summarise", "permute", "nulls"))
    order, lock, agree, t2 = (load("b2", n) for n in ("order", "lock", "agree", "test_b2"))
    findings = [("FI_001", "module collision under one process", fi_001()),
                ("FI_002", "L-axis stability, top-decile vs separation set", fi_002(t, score, summarise)),
                ("FI_003", "Williams square: successor pairs per block", fi_003(order)),
                ("FI_004", "post-release commit cannot rewrite D1", fi_004(agree, lock, t2)),
                ("FI_005", "shifted rejoin: resync vs div (recorded)", fi_005(t, score)),
                ("FI_006", "N4 is one permutation draw (recorded)", fi_006(t, score, summarise, permute, nulls)),
                ("FI_007", "vacuous A vs D1 check at one auditor", fi_007(agree, lock, t2)),
                ("FI_008", "saturated ties in the top decile", fi_008(t, score, summarise))]
    ok = 0
    for fid, title, (num, holds) in findings:
        ok += bool(holds)
        print("%s  %-48s %s  %s" % (fid, title, "holds" if holds else "FAILS", num))
    print("%d of %d computed findings hold as recorded in CLAIM_TABLE.md" % (ok, len(findings)))
    return 0 if ok == len(findings) else 1


if __name__ == "__main__":
    sys.exit(main())
