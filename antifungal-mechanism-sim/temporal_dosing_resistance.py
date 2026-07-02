#!/usr/bin/env python3
# temporal_dosing_resistance.py
# Adds the TIME axis the static scorer collapsed. Two structural results:
#   [1] resistance evolution is a KICKED RELAXOR under a dosing schedule
#       (dose = kick; adaptation between kicks; schedule decides the outcome).
#   [2] antagonism is SEQUENCE-DEPENDENT -> the interaction matrix is
#       NON-COMMUTATIVE: J[i->j] != J[j->i]. (New axis vs the reach/avoid kernel.)
# CC0. stdlib only.  (combination pharmacology, therapeutic design)

# ── CONSTRAINTS ──────────────────────────────────────────────
# genotypes over 2 drugs A,B: WT (sens both), RA (resists A), RB, RAB (resists both)
# per step: logistic growth, drug kill (only if drug active AND genotype sensitive),
#           mutation flux WT->RA,RB and RA,RB->RAB at rate mu
# schedule = list of active-drug sets per step. outcome = final total + R-fraction.
# collateral_sensitivity: RA is EXTRA-killed by B (evolutionary steering).
# ─────────────────────────────────────────────────────────────

R, K, MU = 0.5, 1_000_000.0, 1e-4
KILL = 1.2   # kill rate when drug present and genotype sensitive

SENS = {  # genotype -> set of drugs that still kill it
    "WT": {"A", "B"}, "RA": {"B"}, "RB": {"A"}, "RAB": set(),
}


def step(pop, active, collateral=False):
    total = sum(pop.values())
    new = {}
    for g, n in pop.items():
        growth = R * n * (1 - total / K)
        kill = 0.0
        for d in active:
            if d in SENS[g]:
                kill += KILL * n
            if collateral and g == "RA" and d == "B":
                kill += 0.8 * KILL * n          # RA hypersensitive to B
        new[g] = max(0.0, n + growth - kill)
    # mutation flux
    f1 = MU * new["WT"]
    new["WT"] -= 2 * f1; new["RA"] += f1; new["RB"] += f1
    f2 = MU * (new["RA"] + new["RB"])
    new["RA"] -= MU * new["RA"]; new["RB"] -= MU * new["RB"]; new["RAB"] += f2
    return {g: max(0.0, v) for g, v in new.items()}


def run(schedule, collateral=False):
    pop = {"WT": 1e5, "RA": 1.0, "RB": 1.0, "RAB": 0.0}
    for active in schedule:
        pop = step(pop, active, collateral)
    total = sum(pop.values())
    rfrac = pop["RAB"] / total if total > 1 else 0.0
    cleared = total < 1.0
    return total, rfrac, cleared


def schedules(n=40):
    simult = [{"A", "B"}] * n
    seq = [{"A"}] * (n // 2) + [{"B"}] * (n // 2)      # long mono blocks
    cyc = [{"A"} if i % 2 == 0 else {"B"} for i in range(n)]  # fast alternation
    return {"simultaneous": simult, "sequential mono": seq, "fast cycling": cyc}


# ---- [2] sequence-dependent antagonism (non-commutative J) ----
def polyene_azole(order):
    """Ergosterol E is polyene's target; azole depletes E. Order changes kill."""
    E = 1.0
    kill = 0.0
    for drug in order:
        if drug == "polyene":
            kill += 8.0 * E              # efficacy scales with available ergosterol
        elif drug == "azole":
            kill += 7.0                  # azole acts, then depletes ergosterol
            E *= 0.3
    return kill


if __name__ == "__main__":
    print("[1] resistance vs dosing schedule (dose = kick):")
    print(f"{'schedule':<18}{'final_pop':>12}{'R_frac':>9}  outcome")
    for name, sch in schedules().items():
        tot, rf, cl = run(sch)
        print(f"{name:<18}{tot:>12.0f}{rf:>9.3f}  {'CLEARED' if cl else 'survives'}")
    print("  simultaneous suppresses (escape needs both mutations ~mu^2);")
    print("  sequential mono breeds RAB stepwise (each block sweeps a single-R).")

    print("\n  with collateral sensitivity (RA hypersensitive to B):")
    tot, rf, cl = run(schedules()["fast cycling"], collateral=True)
    print(f"  fast cycling -> final_pop {tot:.0f}  {'CLEARED (steered to death)' if cl else 'survives'}")

    print("\n[2] sequence-dependent antagonism (non-commutative J):")
    ab = polyene_azole(["azole", "polyene"])
    ba = polyene_azole(["polyene", "azole"])
    print(f"  azole -> polyene : kill = {ab:.1f}   (ergosterol depleted first, polyene blunted)")
    print(f"  polyene -> azole : kill = {ba:.1f}   (polyene binds first, then azole)")
    print(f"  J[azole->polyene] != J[polyene->azole]  -> matrix is NON-COMMUTATIVE")
