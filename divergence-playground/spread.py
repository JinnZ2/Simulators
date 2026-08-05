#!/usr/bin/env python3
"""
spread.py -- 3-axis spread metric over an ensemble of Readings.  stdlib, CC0.

Readings are structured, not scalar.  Variance won't compare them.
Three axes, computed independently, each in [0, 1]:

  axis 1  VERDICT     do they name the same branch?
                      categorical.  cheap.  weakest signal.

  axis 2  MECHANISM   same causal chain?
                      1 − Jaccard on the edge set.  order-independent
                      by construction of Reading.canonical(), so two
                      readings using different notation for the same
                      chain compare equal.

  axis 3  COLLAPSE    would the same experiment resolve them?
                      canonical (vary, observe, criterion) tuple.
                      THIS is the strong axis.  If two readings propose
                      the same test, they're near-identical operationally,
                      whatever their prose said.  Different tests →
                      genuine disagreement even under matched verdicts.

Reported alongside the three numbers:

  clusters        readers whose canonical readings match exactly
                  → shared prior, not independent evidence.
  agree_by_accident   FLAG: verdict axis says agree, collapse axis says
                      disagree.  This is the cell variance would miss.
  cheap_collapses     collapse conditions that appear in >= 2 readings
                      → auto-ranked queue (the "run this next" list).
"""

from collections import Counter
from itertools import combinations
from typing import List, Tuple, Dict

from reading import Reading


# --- per-axis distance -----------------------------------------------------

def _verdict_spread(readings: List[Reading]) -> float:
    """Fraction of readings that are NOT the modal verdict."""
    if len(readings) <= 1:
        return 0.0
    counts = Counter(r.verdict for r in readings)
    modal = counts.most_common(1)[0][1]
    return 1.0 - modal / len(readings)


def _jaccard_dist(a: frozenset, b: frozenset) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return 1.0 - inter / union


def _mechanism_spread(readings: List[Reading]) -> float:
    """Mean pairwise Jaccard distance on the mechanism-edge sets."""
    if len(readings) <= 1:
        return 0.0
    edge_sets = [frozenset(tuple(e) for e in r.mechanism) for r in readings]
    dists = [_jaccard_dist(a, b) for a, b in combinations(edge_sets, 2)]
    return sum(dists) / len(dists)


def _collapse_key(r: Reading) -> Tuple:
    c = r.collapse
    return (tuple(sorted(c["vary"])), c["observe"], c["criterion"])


def _collapse_spread(readings: List[Reading]) -> float:
    """Fraction of readings whose collapse condition is NOT the modal one."""
    if len(readings) <= 1:
        return 0.0
    keys = [_collapse_key(r) for r in readings]
    counts = Counter(keys)
    modal = counts.most_common(1)[0][1]
    return 1.0 - modal / len(readings)


# --- clustering / accident / cheap ---------------------------------------

def _clusters(items: List[Tuple[str, object]]) -> List[List[str]]:
    """Group reader_ids by identical canonical fingerprint."""
    groups: Dict[object, List[str]] = {}
    for rid, key in items:
        groups.setdefault(key, []).append(rid)
    return sorted((g for g in groups.values() if len(g) > 1),
                  key=lambda g: (-len(g), g))


def clusters(named_readings: List[Tuple[str, Reading]]) -> Dict[str, List[List[str]]]:
    """Reader groupings under each axis.  Same-axis grouping = shared prior."""
    verdict_groups = _clusters([(rid, r.verdict) for rid, r in named_readings])
    mech_groups = _clusters([
        (rid, frozenset(tuple(e) for e in r.mechanism)) for rid, r in named_readings])
    collapse_groups = _clusters([(rid, _collapse_key(r)) for rid, r in named_readings])
    canonical_groups = _clusters([(rid, r.canonical()) for rid, r in named_readings])
    return {"verdict": verdict_groups, "mechanism": mech_groups,
            "collapse": collapse_groups, "canonical": canonical_groups}


def agreement_accident(readings: List[Reading]) -> bool:
    """FLAG: verdict axis says agree, collapse axis says disagree.
    Same conclusion by different routes -- variance would never catch."""
    return _verdict_spread(readings) == 0.0 and _collapse_spread(readings) > 0.0


def cheap_collapses(named_readings: List[Tuple[str, Reading]]) -> List[Dict]:
    """Collapse conditions proposed by >= 2 readers, ordered by
    (count desc, criterion length asc).  Auto-ranked run queue."""
    keys = [(rid, _collapse_key(r), r.collapse) for rid, r in named_readings]
    by_key: Dict[Tuple, Dict] = {}
    for rid, k, coll in keys:
        d = by_key.setdefault(k, {"count": 0, "proposers": [], "collapse": coll})
        d["count"] += 1
        d["proposers"].append(rid)
    rows = [v for v in by_key.values() if v["count"] >= 2]
    rows.sort(key=lambda d: (-d["count"], len(d["collapse"].get("criterion", ""))))
    return rows


# --- top-level ------------------------------------------------------------

def report(named_readings: List[Tuple[str, Reading]]) -> Dict:
    readings = [r for _, r in named_readings]
    return {
        "n_readers": len(readings),
        "verdict_spread": _verdict_spread(readings),
        "mechanism_spread": _mechanism_spread(readings),
        "collapse_spread": _collapse_spread(readings),
        "clusters": clusters(named_readings),
        "agree_by_accident": agreement_accident(readings),
        "cheap_collapses": cheap_collapses(named_readings),
    }


def print_report(named_readings: List[Tuple[str, Reading]], fork_id: str = "") -> None:
    r = report(named_readings)
    hdr = f"SPREAD REPORT" + (f"  --  {fork_id}" if fork_id else "")
    print(hdr); print("=" * len(hdr))
    print(f"  readers                : {r['n_readers']}")
    print(f"  verdict spread   [0..1]: {r['verdict_spread']:.2f}")
    print(f"  mechanism spread [0..1]: {r['mechanism_spread']:.2f}")
    print(f"  collapse spread  [0..1]: {r['collapse_spread']:.2f}"
          "   <- strong axis")
    if r["agree_by_accident"]:
        print()
        print("  ! AGREE-BY-ACCIDENT FLAG: same verdict, different collapse")
        print("    → variance would never catch this. Investigate.")
    print()
    for axis, groups in r["clusters"].items():
        if groups:
            print(f"  clusters on {axis:<10}: {groups}"
                  f"  ← shared prior, not independent evidence"
                  if axis == "canonical" else
                  f"  clusters on {axis:<10}: {groups}")
    if r["cheap_collapses"]:
        print()
        print("  RUN QUEUE (collapse conditions proposed by >= 2 readers):")
        for i, c in enumerate(r["cheap_collapses"], 1):
            v = ", ".join(c["collapse"]["vary"])
            print(f"    {i}. vary [{v}], observe {c['collapse']['observe']!r}"
                  f"  (proposed by {c['count']}: {', '.join(c['proposers'])})")


# --- self-test ------------------------------------------------------------

def _r(v, edges, coll_vary, coll_obs, coll_crit):
    return Reading(verdict=v, mechanism=edges,
                   collapse={"vary": coll_vary, "observe": coll_obs,
                             "criterion": coll_crit})


def _t_all_identical_zero_spread():
    r = _r("A", [("x", "r", "y")], ["p"], "q", "c")
    nr = [("r1", r), ("r2", r), ("r3", r)]
    rep = report(nr)
    assert rep["verdict_spread"] == 0.0
    assert rep["mechanism_spread"] == 0.0
    assert rep["collapse_spread"] == 0.0


def _t_all_different_high_spread():
    nr = [("r1", _r("A", [("a", "r", "b")], ["p"], "q1", "c")),
          ("r2", _r("B", [("c", "r", "d")], ["p2"], "q2", "c")),
          ("r3", _r("C", [("e", "r", "f")], ["p3"], "q3", "c"))]
    rep = report(nr)
    assert rep["verdict_spread"] > 0.5
    assert rep["mechanism_spread"] == 1.0    # no shared edges
    assert rep["collapse_spread"] > 0.5


def _t_agree_by_accident_flag():
    # same verdict, different collapse -- the interesting cell
    nr = [("r1", _r("A", [("a", "r", "b")], ["p"], "q", "c1")),
          ("r2", _r("A", [("a", "r", "b")], ["z"], "q", "c2"))]
    rep = report(nr)
    assert rep["verdict_spread"] == 0.0
    assert rep["collapse_spread"] == 0.5
    assert rep["agree_by_accident"] is True


def _t_cheap_collapse_ranking():
    coll = ["p1", "p2"]
    obs, crit = "q", "cri"
    nr = [("r1", _r("A", [], coll, obs, crit)),
          ("r2", _r("B", [], coll, obs, crit)),
          ("r3", _r("C", [], ["z"], obs, crit))]
    rep = report(nr)
    assert len(rep["cheap_collapses"]) == 1
    assert rep["cheap_collapses"][0]["count"] == 2
    assert set(rep["cheap_collapses"][0]["proposers"]) == {"r1", "r2"}


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
