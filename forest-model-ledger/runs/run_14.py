"""run_14: run_10's trigger re-run with the tools it lacked (multi_seed_ensemble, ablation).

    python3 runs/run_14.py      # about a minute; reproduces samples/run_14.sample.txt

Trigger (run_10, card CC_001): N misclosure -5.0e-11, near-identical across seeds.
run_10 answered it with hand-written seed loops and a dep=0 arm that removed
deposition and fire together. This run uses the gated tools instead and adds the
ablation run_10 could not do: remove the deposition COUNTER while keeping the
deposition flux and the fire cycle (the audit reads the counter at its exact
value dep * years; the trajectory is untouched).

model/base.py, budget_closure.py and run_9.py are not edited (anchor pins).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import base, l0_audit
from ledger.toolkit import multi_seed_ensemble as mse, ablation

IX = base.IX
SEEDS = list(range(10))


def simulate(seed, overrides):
    ov = dict(overrides)
    exact = ov.pop("_exact_dep_counter", False)
    fires = ov.pop("_fires", True)
    r = base.simulate(seed=seed, params=ov, fires=fires)
    a = l0_audit.audit(r)
    counter = float(r["y"][IX["deposition"]])
    exact_total = r["params"]["dep"] * r["years"]
    n_mis = a["N"]["misclosure"]
    if exact:
        n_mis = n_mis + (counter - exact_total)   # misclosure with the counter read at its exact value
    return dict(N_mis=n_mis, water_mis=a["water"]["misclosure"], fires=float(len(r["events"])),
                fire_out=float(r["y"][IX["fire_volatilisation"]]), dep_counter_err=counter - exact_total,
                T_mean=float(r["traj"][int(round(100 / r["dt"])):, IX["T"]].mean()))


def sim_seed(seed):
    return simulate(seed, {})


ACTIVE = dict(fire=lambda o: o["fires"] > 0, deposition=lambda o: abs(o["dep_counter_err"]) > 0 or o["N_mis"] != 0)
# Margins are derived from the base ensemble's own sd [CHOICE]: equivalence delta = 0.5 sd,
# seed-specific band = 2 sd (run_11's noise band). Floor 1e-15 where the base sd is 0.
# The first draft of this run used hand-set margins; the water band sat below water's own
# roundoff floor and flagged seed_specific on roundoff. Replaced before recording; kept here.
K_DELTA, K_BAND, FLOOR = 0.5, 2.0, 1e-15


def margins(st):
    return ({n: max(K_DELTA * (v["sd"] or 0.0), FLOOR) for n, v in st.items()},
            {n: max(K_BAND * (v["sd"] or 0.0), FLOOR) for n, v in st.items()})


def main():
    print("thresholds (multi_seed_ensemble, [CHOICE]):", mse.CHOICES)
    print(f"equivalence delta = {K_DELTA} x base sd, seed-specific band = {K_BAND} x base sd, floor {FLOOR} [CHOICE]")
    print(f"\n== 1. multi_seed_ensemble: base, seeds {SEEDS[0]}..{SEEDS[-1]}")
    ens = mse.run_ensemble(sim_seed, SEEDS, workers=4)
    st, inv = mse.stats(ens), mse.seed_invariance(ens)
    DELTA, BAND = margins(st)
    for n, v in st.items():
        print(f"  {n:16s} mean {v['mean']:+.6e}  sd {v['sd']:.3e}  cv {abs(v['sd'] / v['mean']) if v['mean'] else float('nan'):.4f}  distinct {v['distinct']:2d}  {inv[n]}")

    print("\n== 2. ablation: one drop per arm, paired on the same seeds; activities declared: fire, deposition")
    arms = [
        dict(name="deposition off (dep=0)", overrides=dict(dep=0.0), drops=["deposition"]),
        dict(name="fire off", overrides=dict(_fires=False), drops=["fire"]),
        dict(name="deposition counter exact", overrides=dict(_exact_dep_counter=True), drops=["deposition_counter"]),
    ]
    res = ablation.run(simulate, arms, SEEDS, DELTA, BAND, ACTIVE, base=ens)
    print(ablation.render(res, choices=False))
    for r in res["rows"]:
        print(f"  {r['name']}:")
        for n, v in r["per_output"].items():
            z = "    --" if v["z"] is None else f"{v['z']:+8.1f}"
            print(f"     {n:16s} mean diff {v['mean']:+.4e}  se {v['se']:.2e}  z {z}  {v['verdict']}{'  seed_specific' if v['seed_specific'] else ''}")

    print("\n== 3. under each arm: does N misclosure stay seed-invariant?")
    for a in arms:
        arm = {s: simulate(s, a["overrides"]) for s in SEEDS}
        xs = [arm[s]["N_mis"] for s in SEEDS]
        print(f"  {a['name']:28s} N_mis {mse.invariance(xs)}   range {min(xs):+.3e} .. {max(xs):+.3e}   fires total {sum(arm[s]['fires'] for s in SEEDS):.0f}")


if __name__ == "__main__":
    main()
