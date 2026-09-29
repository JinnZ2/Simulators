"""test_perturbation.py — known-answer tests for perturbation.py.

Run: python3 test_perturbation.py
"""

import tempfile
from pathlib import Path

from transformation import Entry
from ledger import Ledger
from perturbation import (
    PERTURBATIONS, PERTURBATION_NAMES, REQUIRED_PERTURBATIONS,
    render_perturbations, Vector, tv_distance, similarity,
    shuffle_directions, null_similarities, verdict,
    load_vectors, save_vectors, render,
)

CHECKS = 0
def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)

def test_perturbation_set():
    check(len(PERTURBATIONS) == 8, f"expected 8 perturbations, got {len(PERTURBATIONS)}")
    check(len(set(PERTURBATION_NAMES)) == 8, "perturbation names not unique")
    # one per shape-pair
    pairs = {(p[1], p[2]) for p in PERTURBATIONS}
    check(len(pairs) == 8, f"perturbations do not cover 8 distinct pairs: {len(pairs)}")

def test_render_perturbations():
    out = render_perturbations("HELLO.")
    check(len(out) == 8, "render did not produce 8 perturbations")
    for name in PERTURBATION_NAMES:
        check(name in out, f"missing {name}")
        check(out[name].endswith("HELLO."), f"{name} did not include source")
        check(len(out[name]) > len("HELLO."), f"{name} did not prefix source")

def test_tv_distance_happy():
    a = Vector(); a.add("SUBSTITUTE", "unresolved -> familiar", 4)
    a.add("TERMINATE", "recursive -> terminal", 6)
    b = Vector(); b.add("SUBSTITUTE", "unresolved -> familiar", 4)
    b.add("TERMINATE", "recursive -> terminal", 6)
    check(tv_distance(a, b) == 0.0, "identical distributions should have TV 0")
    check(similarity(a, b) == 1.0, "identical distributions should have similarity 1")

def test_tv_distance_disjoint():
    a = Vector(); a.add("SUBSTITUTE", "unresolved -> familiar", 1)
    b = Vector(); b.add("TERMINATE", "recursive -> terminal", 1)
    check(tv_distance(a, b) == 1.0, "disjoint distributions should have TV 1")
    check(similarity(a, b) == 0.0, "disjoint distributions should have similarity 0")

def test_tv_distance_partial():
    a = Vector()
    a.add("SUBSTITUTE", "unresolved -> familiar", 1)
    a.add("TERMINATE", "recursive -> terminal", 1)
    b = Vector()
    b.add("SUBSTITUTE", "unresolved -> familiar", 2)
    # TV = 0.5 * (|0.5-1.0| + |0.5-0.0|) = 0.5
    check(abs(tv_distance(a, b) - 0.5) < 1e-12, "TV calculation wrong")

def test_tv_distance_empty_is_none():
    a = Vector(); a.add("SUBSTITUTE", "unresolved -> familiar", 1)
    b = Vector()
    check(tv_distance(a, b) is None, "empty vector must give None, not zero")
    check(similarity(a, b) is None, "similarity of empty must be None")

def test_shuffle_is_deterministic():
    a = Vector(); a.add("SUBSTITUTE", "unresolved -> familiar", 1)
    a.add("TERMINATE", "recursive -> terminal", 1)
    s1 = shuffle_directions(a, seed=42)
    s2 = shuffle_directions(a, seed=42)
    check(s1.cells == s2.cells, "shuffle not deterministic for a fixed seed")

def test_shuffle_preserves_counts():
    a = Vector()
    a.add("SUBSTITUTE", "unresolved -> familiar", 3)
    a.add("TERMINATE", "recursive -> terminal", 5)
    a.add("MERGE", "distinct -> merged", 2)
    s = shuffle_directions(a, seed=1)
    check(s.total == a.total, "shuffle did not preserve total count")
    # mechanism marginal preserved
    def marg(v):
        m = {}
        for (mech, _), n in v.cells.items():
            m[mech] = m.get(mech, 0) + n
        return m
    check(marg(s) == marg(a), "shuffle did not preserve mechanism marginal")

def test_verdict_undetermined_incomplete():
    baseline = Vector(); baseline.add("SUBSTITUTE", "unresolved -> familiar", 1)
    signals = {"P1_unresolved": baseline}  # only 1
    r = verdict(signals, baseline)
    check(r["verdict"] == "UNDETERMINED", "should be UNDETERMINED for incomplete set")
    check("incomplete" in r["reason"], "reason should name incompleteness")

def test_verdict_supported_synthetic():
    # Build a baseline vector with 8 cells, and 8 signals all identical to it.
    # Real similarity = 1.0. Null will be less because shuffling breaks alignment.
    baseline = Vector()
    for mech, _, _ in [(p[0].split("_")[0], None, None) for p in PERTURBATIONS]:
        pass
    # Simpler: use real mechanism/direction pairs from the perturbation set.
    from perturbation import PERTURBATIONS
    for name, src_t, tgt_t, _ in PERTURBATIONS:
        # map perturbation to a plausible mechanism
        mech = {
            "unresolved": "SUBSTITUTE",
            "recursive": "TERMINATE",
            "scoped": "GENERALIZE",
            "plural": "BINARY",
            "structural": "VALENCE_SHIFT",
            "neutral": "VALENCE_SHIFT",
            "unfinished": "COMPLETE",
            "distinct": "MERGE",
        }[src_t]
        baseline.add(mech, f"{src_t} -> {tgt_t}")
    # signals identical to baseline
    signals = {name: Vector(cells=dict(baseline.cells)) for name, *_ in PERTURBATIONS}
    r = verdict(signals, baseline, margin=0.05)
    check(r["verdict"] == "SUPPORTED",
          f"identical signals should be SUPPORTED, got {r['verdict']}: {r['reason']}")
    check(r["mean_real"] == 1.0, f"mean_real should be 1.0, got {r['mean_real']}")

def test_verdict_not_supported_unrelated():
    # signals with disjoint cells from baseline
    baseline = Vector(); baseline.add("SUBSTITUTE", "unresolved -> familiar", 1)
    baseline.add("TERMINATE", "recursive -> terminal", 1)
    # build 8 signals that share no cells with baseline
    signals = {}
    for name, src_t, tgt_t, _ in PERTURBATIONS:
        v = Vector()
        v.add("DELETE", "unresolved -> familiar", 1)
        v.add("RANK", "plural -> singular", 1)
        signals[name] = v
    r = verdict(signals, baseline, margin=0.05)
    check(r["verdict"] == "NOT_SUPPORTED",
          f"unrelated signals should be NOT_SUPPORTED, got {r['verdict']}")

def test_save_load_roundtrip():
    with tempfile.TemporaryDirectory() as td:
        v = Vector(reader="r1", date="2026-09-28")
        v.add("SUBSTITUTE", "unresolved -> familiar", 3)
        v.add("TERMINATE", "recursive -> terminal", 2)
        save_vectors({"P1_unresolved": v}, td)
        loaded = load_vectors(td)
        check("P1_unresolved" in loaded, "did not reload vector")
        check(loaded["P1_unresolved"].cells == v.cells, "cells did not roundtrip")
        check(loaded["P1_unresolved"].reader == "r1", "reader did not roundtrip")

def test_vector_from_ledger():
    L = Ledger()
    L.add(Entry("SUBSTITUTE", "unresolved", "familiar", reader="r1"))
    L.add(Entry("SUBSTITUTE", "unresolved", "familiar", reader="r1"))
    L.add(Entry("TERMINATE", "recursive", "terminal", reader="r2"))
    v = Vector.from_ledger(L, reader="r1")
    check(v.cells.get(("SUBSTITUTE", "unresolved -> familiar")) == 2,
          "reader filter lost entries")
    check(("TERMINATE", "recursive -> terminal") not in v.cells,
          "reader filter leaked other readers' entries")
    v_all = Vector.from_ledger(L)
    check(v_all.total == 3, "unfiltered from_ledger lost entries")

def test_render_does_not_raise():
    baseline = Vector(); baseline.add("SUBSTITUTE", "unresolved -> familiar", 1)
    signals = {"P1_unresolved": Vector(cells=dict(baseline.cells))}
    r = verdict(signals, baseline)
    s = render(r)
    check("verdict:" in s, "render output missing verdict line")
    check("UNDETERMINED" in s, "render should show UNDETERMINED for incomplete")

def main():
    tests = [
        test_perturbation_set,
        test_render_perturbations,
        test_tv_distance_happy,
        test_tv_distance_disjoint,
        test_tv_distance_partial,
        test_tv_distance_empty_is_none,
        test_shuffle_is_deterministic,
        test_shuffle_preserves_counts,
        test_verdict_undetermined_incomplete,
        test_verdict_supported_synthetic,
        test_verdict_not_supported_unrelated,
        test_save_load_roundtrip,
        test_vector_from_ledger,
        test_render_does_not_raise,
    ]
    for t in tests:
        t()
    print(f"checks: {CHECKS}")
    print(f"tests:  {len(tests)}")
    print("PASS")

if __name__ == "__main__":
    main()
