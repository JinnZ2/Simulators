"""run_15: run_11's trigger re-run with multi_seed_ensemble and ablation (card CC_003).

    python3 runs/run_15.py      # about four minutes on 4 workers; reproduces samples/run_15.sample.txt

Trigger (run_11, card CC_003): 33 of 64 nudges leave every output inside noise.
Work order 2026-11-11: classify those 33 as inert | absorbed | hidden in noise |
seed-specific. Per nudge, against the anchor on the SAME seeds (common random numbers):

  outputs     run_11's nine outputs (imported, not copied)
  own path    the flux-table rows whose rate the parameter changes, found mechanically:
              the table is evaluated at sampled trajectory states with the parameter at
              x1.0 and x1.1; a row is the parameter's own path if its rate differs.
              Read as the mean rate over years 100-300. A parameter with no row (fire
              terms act in the event test, not the table) has the event channel as its
              own path, which is already in the outputs.

  class (first that applies). MOVED = resolved on common seeds; material = |mean| > delta.
    HIDDEN_IN_NOISE  some output MOVED and material: a real move three unpaired seeds missed
    SEED_SPECIFIC    else, some output seed_specific (mixed signs, |d| > band)
    ABSORBED         else, the change is resolved somewhere -- its own path or an output --
                     but no output moved by a material amount: it arrived and was taken up
                     (the first draft of this run read resolved as moved; see run_15.md)
    INERT            outputs and own path all EXACT_ZERO or EQUIVALENT
    UNRESOLVED       none of the above at this n; kept, not forced into a class

Margins as run_14: delta 0.5 sd, band 2 sd, sd from the anchor's own seeds [CHOICE].
Section 2 runs ablation: grass removed and fire removed, to read the two mechanisms
CC_003 names (grass gone by year 19; the fire cycle as threshold) against the classes.
model/base.py, budget_closure.py and run_9.py are not edited.
"""
import json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import numpy as np
from model import base
from ledger.toolkit import multi_seed_ensemble as mse, ablation
from runs import run_11

IX = base.IX
SEEDS = list(range(20))
K_DELTA, K_BAND, FLOOR = 0.5, 2.0, 1e-15
LATE = 100


def pfacs_for(seed, p, years):
    rng = np.random.default_rng(seed)          # simulate() draws precipitation first from this stream
    return rng.lognormal(-0.5 * p["drought_sd"] ** 2, p["drought_sd"], size=years)


# Parameters that act through the per-year precipitation factor drawn in simulate(), not
# through a table rate: the mechanical test (rates at pfac 1.0) cannot see them. Declared.
PFAC_PARAMS = {"drought_sd": ["precipitation"], "drought": ["precipitation"]}


def own_rows(param, base_params=None):
    """Rows whose rate changes when `param` is scaled x1.1 at sampled states (years 1..300 of seed 0)."""
    if param in PFAC_PARAMS:
        return list(PFAC_PARAMS[param])
    p0 = dict(base.DEFAULTS, **(base_params or {}))
    p1 = dict(p0, **{param: p0[param] * 1.1 if p0[param] != 0 else 0.1})
    r = base.simulate(seed=0)
    rows = set()
    for yr in (1, 2, 5, 10, 18, 50, 150, 299):
        i = int(round(yr / r["dt"]))
        y, t = r["traj"][i], r["t"][i]
        for (n, _, _, a), (_, _, _, b) in zip(base.flux_table(y, t, p0, 1.0), base.flux_table(y, t, p1, 1.0)):
            if a != b:
                rows.add(n)
    return sorted(rows)


def task(args):
    seed, params, rows = args
    r = base.simulate(seed=seed, params=dict(params))
    out = run_11.outputs(r)
    if rows:
        p = r["params"]
        pf = pfacs_for(seed, p, r["years"])
        step = int(round(1 / r["dt"]))
        sums = {n: 0.0 for n in rows}
        idx = range(int(round(LATE / r["dt"])), len(r["t"]), step)
        for i in idx:
            t = r["t"][i]
            for n, _, _, rate in base.flux_table(r["traj"][i], t, p, pf[min(int(t), r["years"] - 1)]):
                if n in sums:
                    sums[n] += rate
        for n in rows:
            out["row:" + n] = sums[n] / len(idx)
    return out


def classify(per_output, outputs):
    """Resolved (MOVED) and material (|mean| > 0.5 sd) are separate axes; see multi_seed_ensemble."""
    v = {n: per_output[n] for n in outputs}
    own = {n: x for n, x in per_output.items() if n.startswith("row:")}
    resolved = lambda x: x["verdict"] == "MOVED"
    if any(resolved(x) and x["material"] for x in v.values()):
        return "HIDDEN_IN_NOISE"
    if any(x["seed_specific"] for x in v.values()):
        return "SEED_SPECIFIC"
    if any(resolved(x) for x in v.values()) or any(resolved(x) for x in own.values()):
        return "ABSORBED"
    if all(x["verdict"] in ("EXACT_ZERO", "EQUIVALENT") for x in per_output.values()):
        return "INERT"
    return "UNRESOLVED"


def main():
    rows11 = json.load(open(os.path.join(HERE, "samples", "run_11.json")))["rows"]
    quiet = [r for r in rows11 if r.get("flags") and "ALL_INSIDE" in r["flags"]]
    nudges = {}
    for r in quiet:
        key = tuple(r["key"])
        found = [n for n in (run_11.NUDGES[key] if not isinstance(run_11.NUDGES[key], tuple) else []) if n["label"] == r["label"]]
        assert len(found) == 1, (key, r["label"])
        nudges[(key, r["label"])] = found[0]["params"]
    print(f"ALL_INSIDE nudges read from samples/run_11.json: {len(nudges)}")
    params_of = {k: list(p)[0] for k, p in nudges.items()}
    rows_of = {pn: own_rows(pn) for pn in sorted(set(params_of.values()))}
    print("own path per parameter (flux rows whose rate the parameter changes):")
    for pn, rs in rows_of.items():
        how = "declared: acts through the precipitation factor" if pn in PFAC_PARAMS else "mechanical"
        print(f"  {pn:10s} {rs or 'none: acts in the fire event test, own path = event channel (in the outputs)'}" + (f"   [{how}]" if rs else ""))
    print(f"seeds {SEEDS[0]}..{SEEDS[-1]} paired; thresholds {mse.CHOICES}; delta {K_DELTA} sd, band {K_BAND} sd [CHOICE]")

    from concurrent.futures import ProcessPoolExecutor
    all_rows = sorted({x for rs in rows_of.values() for x in rs})
    jobs = [(s, {}, all_rows) for s in SEEDS]
    for k, p in nudges.items():
        jobs += [(s, p, rows_of[params_of[k]]) for s in SEEDS]
    print(f"simulations: {len(jobs)}", flush=True)
    with ProcessPoolExecutor(4) as ex:
        res = list(ex.map(task, jobs, chunksize=4))
    base_runs = {s: res[i] for i, s in enumerate(SEEDS)}
    st = mse.stats(base_runs)
    delta = {n: max(K_DELTA * (v["sd"] or 0.0), FLOOR) for n, v in st.items()}
    band = {n: max(K_BAND * (v["sd"] or 0.0), FLOOR) for n, v in st.items()}
    outputs = [n for n in base_runs[SEEDS[0]] if not n.startswith("row:")]
    j = len(SEEDS)
    table, counts = [], {}
    for k in nudges:
        arm = {s: res[j + i] for i, s in enumerate(SEEDS)}
        j += len(SEEDS)
        b = {s: {n: base_runs[s][n] for n in arm[s]} for s in SEEDS}
        per = mse.paired(b, arm, delta, band)
        cls = classify(per, outputs)
        counts[cls] = counts.get(cls, 0) + 1
        moved = [n for n in outputs if per[n]["verdict"] == "MOVED" and per[n]["material"]]
        tiny = [n for n in outputs if per[n]["verdict"] == "MOVED" and not per[n]["material"]]
        ss = [n for n in outputs if per[n]["seed_specific"]]
        own = {n[4:]: per[n]["verdict"] for n in per if n.startswith("row:")}
        topz = max(outputs, key=lambda n: abs(per[n]["z"]) if per[n]["z"] is not None else 0.0)
        eff = max(outputs, key=lambda n: abs(per[n]["mean"]) / (st[n]["sd"] or 1.0))
        table.append((k, cls, moved, ss, own, topz, per[topz]["z"], tiny, eff, abs(per[eff]["mean"]) / (st[eff]["sd"] or 1.0)))
    print("\n== 1. the 33, classified")
    for (key, label), cls, moved, ss, own, topz, z, tiny, eff, effsd in table:
        zs = "--" if z is None else f"{z:+.1f}"
        print(f"  {key[0]+'.'+key[1]:28s} {label:20s} {cls:16s} largest effect {effsd:4.2f} sd ({eff}); top |z| {zs:>6s} ({topz})"
              + (f"  moved {moved}" if moved else "") + (f"  resolved-immaterial {tiny}" if tiny else "") + (f"  seed_specific {ss}" if ss else "")
              + (f"  own path {own}" if own else "  own path: event channel"))
    print("  counts:", dict(sorted(counts.items())))

    print("\n== 2. ablation on the anchor: the two mechanisms CC_003 names")
    active = dict(fire=lambda o: o["fires"] > 0, grass=lambda o: o["grass_gone_yr"] > 0.5)

    def sim(seed, ov):
        ov = dict(ov)
        fires = ov.pop("_fires", True)
        init = ov.pop("_init", None)
        return run_11.outputs(base.simulate(seed=seed, params=ov, fires=fires, init=init))
    abl = ablation.run(sim, [dict(name="grass removed (G0=0, uG=0)", overrides=dict(_init=dict(G=0.0), uG=0.0), drops=["grass"]),
                             dict(name="fire removed", overrides=dict(_fires=False), drops=["fire"])],
                       SEEDS[:10], {n: delta[n] for n in outputs}, {n: band[n] for n in outputs}, active,
                       base={s: {n: base_runs[s][n] for n in outputs} for s in SEEDS[:10]})
    print(ablation.render(abl, choices=False))
    for r in abl["rows"]:
        print(f"  {r['name']}: " + "  ".join(f"{n} {v['verdict']}" for n, v in r["per_output"].items()))


if __name__ == "__main__":
    main()
