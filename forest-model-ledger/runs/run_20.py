"""run_20: run_15's near-threshold classes as a range over the materiality margin (follow-up item 4).

run_15 split the 33 non-moving nudges at delta = 0.5 sd of the anchor's own seeds. Six of them sit
within 0.1 sd of that line: uG x1.1 (0.52, HIDDEN) and x0.9 (0.50, ABSORBED), KG x1.1 (0.46,
ABSORBED) and x0.9 (0.52, HIDDEN), kill_T x1.1 (0.58, HIDDEN) and x0.9 (0.48, ABSORBED). Their class
is a property of the margin. Four more (season and aT, both directions) also sit inside
0.40-0.60 sd and are added so the class counts over the 33 are a range, not a point. This run
re-simulates the anchor and those ten arms on run_15's 20
paired seeds and reports the class at each delta from 0.40 to 0.60 sd in steps of 0.02, band held
at 2 sd. Same seeds, same code paths (runs/run_15.task, classify); nothing else changes.
model/base.py, budget_closure.py and run_9.py are not edited.
"""
import json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from ledger.toolkit import multi_seed_ensemble as mse
from runs import run_11, run_15

ASKED = ("uG x1.1", "uG x0.9", "KG x1.1", "KG x0.9", "kill_T x1.1", "kill_T x0.9")
# the other run_15 nudges whose largest effect sits inside 0.40-0.60 sd and are resolved somewhere (run_15.sample.txt);
# drought_sd and p_ign (0.35-0.37) are UNRESOLVED, which the margin cannot move
ALSO = ("season x1.1", "season x0.9", "aT x1.1", "aT x0.9")
PICK = ASKED + ALSO
DELTAS = [round(0.40 + 0.02 * i, 2) for i in range(11)]


def main():
    rows11 = json.load(open(os.path.join(HERE, "samples", "run_11.json")))["rows"]
    nudges = {}
    for r in rows11:
        if r["label"] in PICK and r.get("flags") and "ALL_INSIDE" in r["flags"]:
            key = tuple(r["key"])
            found = [n for n in run_11.NUDGES[key] if n["label"] == r["label"]]
            nudges[r["label"]] = found[0]["params"]
    assert sorted(nudges) == sorted(PICK), sorted(nudges)
    rows_of = {lab: run_15.own_rows(list(p)[0]) for lab, p in nudges.items()}
    all_rows = sorted({x for rs in rows_of.values() for x in rs})
    S = run_15.SEEDS
    jobs = [(s, {}, all_rows) for s in S] + [(s, nudges[l], rows_of[l]) for l in PICK for s in S]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(4) as ex:
        res = list(ex.map(run_15.task, jobs, chunksize=4))
    base_runs = {s: res[i] for i, s in enumerate(S)}
    st = mse.stats(base_runs)
    outputs = [n for n in base_runs[S[0]] if not n.startswith("row:")]
    band = {n: max(run_15.K_BAND * (v["sd"] or 0.0), run_15.FLOOR) for n, v in st.items()}
    print(f"seeds {S[0]}..{S[-1]} paired ; band {run_15.K_BAND} sd ; thresholds {mse.CHOICES} ; simulations {len(jobs)}")
    print("class by materiality margin delta (sd of the anchor's own seeds); run_15 used 0.50")
    print(f"  {'nudge':12s} {'eff sd':>6s}  " + " ".join(f"{d:>4.2f}" for d in DELTAS) + "   class over the range")
    abbrev = dict(HIDDEN_IN_NOISE="H", ABSORBED="A", SEED_SPECIFIC="S", INERT="I", UNRESOLVED="U")
    out = {}
    for i, lab in enumerate(PICK):
        arm = {s: res[len(S) * (i + 1) + k] for k, s in enumerate(S)}
        b = {s: {n: base_runs[s][n] for n in arm[s]} for s in S}
        cls = []
        for d in DELTAS:
            delta = {n: max(d * (v["sd"] or 0.0), run_15.FLOOR) for n, v in st.items()}
            cls.append(run_15.classify(mse.paired(b, arm, delta, band), outputs))
        per = mse.paired(b, arm, None, band)
        eff = max(abs(per[n]["mean"]) / (st[n]["sd"] or 1.0) for n in outputs)
        flip = [d for d, c0, c1 in zip(DELTAS[1:], cls, cls[1:]) if c0 != c1]
        out[lab] = dict(eff_sd=eff, classes=dict(zip(DELTAS, cls)), flips_at=flip)
        span = " -> ".join(dict.fromkeys(cls))
        print(f"  {lab:12s} {eff:6.3f}  " + " ".join(f"{abbrev[c]:>4s}" for c in cls) + f"   {span}" + (f" (changes at {flip})" if flip else ""))
    counts = {d: {} for d in DELTAS}
    for lab in PICK:
        for d, c in out[lab]["classes"].items():
            counts[d][c] = counts[d].get(c, 0) + 1
    print("run_15 counts over the 33 at 0.50: HIDDEN 18, ABSORBED 9, SEED_SPECIFIC 2, INERT 2, UNRESOLVED 2")
    base_counts = dict(HIDDEN_IN_NOISE=18, ABSORBED=9, SEED_SPECIFIC=2, INERT=2, UNRESOLVED=2)
    at50 = counts[0.5]
    for d in DELTAS:
        c = dict(base_counts)
        for k, v in at50.items():
            c[k] -= v
        for k, v in counts[d].items():
            c[k] = c.get(k, 0) + v
        print(f"  delta {d:.2f}: " + "  ".join(f"{k} {c.get(k, 0)}" for k in base_counts))
    print("  H HIDDEN_IN_NOISE  A ABSORBED  S SEED_SPECIFIC  I INERT  U UNRESOLVED")
    return out


if __name__ == "__main__":
    main()
