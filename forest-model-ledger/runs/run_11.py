"""Run 11: assumption_nudge on the candidate anchor (run_9). Anchor test 3.

    python3 runs/run_11.py          # several minutes; pinned in samples/run_11.sample.txt

model/base.py is not edited: every nudge is a parameter override.
Nudge size: x1.1 and x0.9 per hand-set parameter                    [CHOICE]
Structural nudges are larger and say so in their label.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from model import base
from ledger.toolkit import assumption_nudge as an
from ledger.toolkit import budget_closure

IX = base.IX
SCOPE = ["L0_N_BUDGET", "L0_WATER_BUDGET", "L1_UPTAKE_MM", "L1_DECOMP_FIRST_ORDER", "L1_LEACHING",
         "L2_TREE_GROWTH", "L2_GRASS_GROWTH", "L2_FUNGAL_POOL", "L3_TREE_FUNGUS_EXCHANGE", "L3_LIGHT_CEILING",
         "L4_FIRE_FUEL_MOISTURE"]
NN = an.NOT_NUDGEABLE


def pm(*names):
    out = []
    for n in names:
        v = base.DEFAULTS[n]
        out += [dict(label=f"{n} x1.1", params={n: v * 1.1}), dict(label=f"{n} x0.9", params={n: v * 0.9})]
    return out


NUDGES = {
    ("L0_N_BUDGET", "A1"): [dict(label="leak 0.3 (off-table path)", params=dict(leak=0.3), expect="N LEAK; misclosure grows with run length")],
    ("L0_N_BUDGET", "A2"): pm("dep"),          # a constant extra input is what a non-zero void boundary term would be here
    ("L0_N_BUDGET", "A3"): (NN, "one currency is the state vector's shape; a second N form needs new pools"),
    ("L0_WATER_BUDGET", "A1"): (NN, "no off-table water path exists to switch on; the planted leak is N only"),
    ("L0_WATER_BUDGET", "A2"): (NN, "a second soil layer, snow or interception needs new pools"),
    ("L1_UPTAKE_MM", "A1"): (NN, "well-mixed is the absence of space; needs a spatial model"),
    ("L1_UPTAKE_MM", "A2"): pm("uT", "uG", "K"),
    ("L1_DECOMP_FIRST_ORDER", "A1"): (NN, "decomposer limitation needs a microbial pool (BR_MICROBE_EXPLICIT)"),
    ("L1_DECOMP_FIRST_ORDER", "A2"): pm("kT", "kG", "Wh"),
    ("L1_LEACHING", "A1"): (NN, "the functional form is fixed in the flux table; only its coefficient moves"),
    ("L1_LEACHING", "A2"): pm("leach"),
    ("L2_TREE_GROWTH", "A1"): pm("mT"),
    ("L2_TREE_GROWTH", "A2"): (NN, "age or size structure needs cohorts"),
    ("L2_GRASS_GROWTH", "A1"): pm("mG"),
    ("L2_GRASS_GROWTH", "A2"): (NN, "a seed bank or immigration is a new inflow row; none exists to switch on"),
    ("L2_FUNGAL_POOL", "A1"): (NN, "a second guild needs a second pool"),
    ("L2_FUNGAL_POOL", "A2"): pm("mF"),
    ("L3_TREE_FUNGUS_EXCHANGE", "A1"): [dict(label="Kf x10 (near-linear)", params=dict(Kf=base.DEFAULTS["Kf"] * 10))],
    ("L3_TREE_FUNGUS_EXCHANGE", "A2"): (NN, "a C-denominated payment needs a C budget, which is VOID"),
    ("L3_TREE_FUNGUS_EXCHANGE", "A3"): pm("b", "c", "Kf"),
    ("L3_LIGHT_CEILING", "A1"): [dict(label="KT,KG x10 (ceiling lifted)", params=dict(KT=base.DEFAULTS["KT"] * 10, KG=base.DEFAULTS["KG"] * 10),
                                      expect="runaway (run 4: no ceiling)")],
    ("L3_LIGHT_CEILING", "A2"): pm("KT", "KG", "aG", "aT"),
    ("L4_FIRE_FUEL_MOISTURE", "A1"): (NN, "threshold sharpness is in the event test, not a parameter"),
    ("L4_FIRE_FUEL_MOISTURE", "A2"): (NN, "partial-stand fire needs space (BR_FIRE_PERCOLATION)"),
    ("L4_FIRE_FUEL_MOISTURE", "A3"): pm("fuel_th", "W_dry", "p_ign", "burn", "vol", "kill_G", "kill_T"),
    # parameters no listed assumption owns: nudged anyway, reported as a ledger gap
    ("UNOWNED", "water"): pm("P0", "season", "et", "drain", "drought_sd") + [dict(label="drought +0.1", params=dict(drought=0.1))],
}


def outputs(res):
    """End states are one phase of the fire cycle, so pools are read as means over
    years 100-300; counts and exports are whole-run totals."""
    tr, y = res["traj"], res["y"]
    gone = np.nonzero(tr[:, IX["G"]] < 1e-6)[0]
    late = tr[int(round(100 / res["dt"])):]
    return dict(fires=float(len(res["events"])), T_mean=float(late[:, IX["T"]].mean()), S_mean=float(late[:, IX["S"]].mean()),
                F_mean=float(late[:, IX["F"]].mean()), litter_mean=float((late[:, IX["Lt"]] + late[:, IX["Lg"]]).mean()),
                W_mean=float(late[:, IX["W"]].mean()),
                leach_out=float(y[IX["leaching"]]), fire_out=float(y[IX["fire_volatilisation"]]),
                grass_gone_yr=float(res["t"][gone[0]]) if len(gone) else float(res["years"]))


def main():
    scope = an.scope_assumptions(SCOPE)
    an.check_coverage(scope, NUDGES)
    owned = {k for key, v in NUDGES.items() if not isinstance(v, tuple) and key[0] != "UNOWNED" for n in v for k in n["params"]}
    unowned = {k for n in NUDGES[("UNOWNED", "water")] for k in n["params"]}
    never = sorted(set(base.DEFAULTS) - owned - unowned)
    print(f"assumptions in scope: {len(scope)}   with a nudge: {sum(1 for k, v in NUDGES.items() if not isinstance(v, tuple) and k[0] != 'UNOWNED')}   not nudgeable here: {sum(1 for v in NUDGES.values() if isinstance(v, tuple))}")
    print(f"parameters: {len(base.DEFAULTS)} in DEFAULTS; nudged under an assumption {len(owned)}; owned by NO listed assumption {sorted(unowned)}; never nudged {never}")
    print(f"not nudged at all: INIT ({len(base.INIT)} values) and dt (dt is run_9 and run_10)\n")
    res = an.run(NUDGES, base.simulate, outputs, budget_closure.audit, (base.DEFAULTS, base.INIT),
                 log=lambda s: print("  ..", s, file=sys.stderr, flush=True))
    print(an.render(res))
    import json
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples", "run_11.json")
    json.dump(dict(sd=res["sd"], ref_mean=res["ref_mean"], rows=[dict(key=list(r["key"]), label=r["label"], diff=r.get("diff"), flags=r.get("flags"),
              worst=r.get("worst"), returned=r.get("returned")) for r in res["rows"]]), open(out, "w"), indent=1, sort_keys=True)
    print("\nexpected failure signatures:")
    for r in res["rows"]:
        if r.get("expect", "void") != "void":
            print(f"  {r['key'][0]}.{r['key'][1]} {r['label']}: expected '{r['expect']}'   got verdicts {r['verdicts']}  T_mean {r['mean']['T_mean']:.2f}  outside {r['outside']}")


if __name__ == "__main__":
    main()
