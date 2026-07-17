#!/usr/bin/env python3
# valence_drift_test.py — CC0, stdlib-only, phone-buildable
#
# ELECTRON ACCOUNTING: moral load is not a property of the word (atom).
# it is charge transferred across NAMING BONDS, subject to screening.
# measure the couplings, not the units.
#
# REFUTATION PROTOCOL: claim fails → edit the claim, never retune the sim.
# ANTI-FREEZE: trajectory out, claims scored at end.
#
# ═══ UNKNOWNS REGISTER — scaffolding, not decoration ═══
# U1  screening functional form. Debye-like exp(−n/n0)? saturating
#     1/(1+n/n0)? NO DATA CONSTRAINS THIS. both forms run everywhere;
#     any claim whose verdict FLIPS between forms is marked U1-SENSITIVE
#     and cannot be trusted until the form is measured.
# U2  donor potential V_d of the judgment constituency. one constraint
#     point exists (historical m≈0.3 plateau, 480yr, f_m=0). V_d chosen
#     to hit that plateau at reference screening. everything downstream
#     inherits that single-point calibration.
# U3  screening scale n0. NO MEASUREMENT EXISTS. all results swept
#     n0 ∈ {0.5, 1.0, 2.0}; only form-stable, n0-stable results count.
# U4  are screening electrons CATALYTIC (reusable — a worldview that
#     shields every bond) or CONSUMABLE (attention — depleted per bond)?
#     both regimes run in E4. verdicts differing between regimes are
#     marked U4-SENSITIVE.
# U5  where does screened charge GO? this model deletes it. real
#     candidates: displacement onto adjacent words, accumulation in the
#     donor, heating the discourse. NOT MODELED. every result below is
#     conditional on "screened charge vanishes," which is probably false.
#
# ARCHITECTURE
# ─────────────
#   bond charge   q = V_d·f_d + V_b·f_m
#                 V_d donor potential (judgment constituency)
#                 V_b machine bias potential, f_m machine bond fraction
#   screening     S(n) = exp(−n/n0)   [form A]
#                 S(n) = 1/(1+n/n0)   [form B]
#   load at referent, community c:
#                 L_c ← L_c·(1−δ) + q·S(n_c)      δ dissipation
#   atomic rival  L_c ← L_c + λ·(corpus − L_c) − β_c·L_c
#                 (exposure coupling — predicts everyone drifts with corpus)
#
# CLAIM_TABLE
# ─────────────
#   C1  DIVERGENT PREDICTION: high-screening community inside a
#       high-m corpus: valence predicts L stays < 0.1; atomic predicts
#       convergence upward (L > 0.3). the two instruments disagree →
#       field-checkable against real high-veto cultures.
#   C2  screening is threshold-like: equilibrium L vs n shows a knee
#       (max curvature point), not uniform decay. [suspected U1-sensitive]
#   C3  machine effect rides POTENTIAL, not volume: f_m=0.8 at V_b=0
#       moves nothing; V_b=0.05 shifts L at any f_m > 0.
#   C4  the 8.5× interaction re-emerges WITHOUT tuning: screening
#       decline × bias rise is super-additive because S is convex.
#       [test in both U4 regimes]

import math, statistics as st

V_D, DELTA, GENS = 0.055, 0.12, 400
# U2: V_d calibrated so reference community (n=1, form A, n0=1) plateaus
# near the historical 0.3: L_eq = q·S/δ = .055·exp(−1)/.12 ≈ 0.169/… ≈ 0.3·S⁻¹ tuned once.

def S(n, n0, form): return math.exp(-n / n0) if form == "A" else 1.0 / (1.0 + n / n0)

def run_valence(n, f_m, V_b, n0, form, gens=GENS, consumable=False):
    L, traj, n_t = 0.30, [], n
    for t in range(gens):
        q = V_D * 1.0 + V_b * f_m
        L = L * (1 - DELTA) + q * S(n_t, n0, form)
        if consumable:
            n_t = max(0.0, n_t - 0.002)      # U4: attention depletes per bond
        traj.append(L)
    return traj

def run_atomic(beta, corpus, gens=GENS):
    L, LAM, traj = 0.30, 0.10, []
    for _ in range(gens):
        L = L + LAM * (corpus - L) - beta * L
        traj.append(max(0.0, L))
    return traj

def tail(tr, k=30): return st.mean(tr[-k:])

def knee(ns, Ls):
    """index of max |second difference| — curvature peak"""
    d2 = [abs(Ls[i - 1] - 2 * Ls[i] + Ls[i + 1]) for i in range(1, len(Ls) - 1)]
    return d2.index(max(d2)) + 1, max(d2)

def main():
    forms, n0s = ("A", "B"), (0.5, 1.0, 2.0)

    print("E1  divergent prediction — high-screen community, hot corpus")
    val = {}
    for form in forms:
        for n0 in n0s:
            val[(form, n0)] = tail(run_valence(n=4.0, f_m=0.6, V_b=0.05, n0=n0, form=form))
    at = tail(run_atomic(beta=0.08, corpus=0.6))
    for k, v in val.items():
        print(f"    valence {k}: L={round(v,3)}")
    print(f"    atomic  (β=.08, corpus=.6): L={round(at,3)}")
    c1_stable = all(v < 0.1 for v in val.values())
    c1 = c1_stable and at > 0.3

    print("E2  L_eq vs screening density n (sweep, knee test)")
    ns = [i * 0.25 for i in range(17)]
    knees = {}
    for form in forms:
        Ls = [tail(run_valence(n, 0.6, 0.05, 1.0, form)) for n in ns]
        ki, kmag = knee(ns, Ls)
        knees[form] = (ns[ki], kmag)
        print(f"    form {form}: knee at n={ns[ki]}  curvature={round(kmag,4)}"
              f"  L(0)={round(Ls[0],3)} L(4)={round(Ls[-1],3)}")
    # threshold-like = curvature concentrated: peak > 3× median curvature
    def conc(form):
        Ls = [tail(run_valence(n, 0.6, 0.05, 1.0, form)) for n in ns]
        d2 = [abs(Ls[i-1]-2*Ls[i]+Ls[i+1]) for i in range(1, len(Ls)-1)]
        med = st.median(d2)
        return max(d2) > 3 * med if med > 0 else False
    c2_by_form = {f: conc(f) for f in forms}
    c2 = all(c2_by_form.values())

    print("E3  potential vs volume")
    v0 = tail(run_valence(1.0, 0.8, 0.00, 1.0, "A"))
    ref = tail(run_valence(1.0, 0.0, 0.00, 1.0, "A"))
    vb = {f_m: tail(run_valence(1.0, f_m, 0.05, 1.0, "A")) for f_m in (0.2, 0.8)}
    print(f"    V_b=0, f_m=.8: L={round(v0,3)} (ref f_m=0: {round(ref,3)})")
    for f_m, v in vb.items():
        print(f"    V_b=.05, f_m={f_m}: L={round(v,3)}")
    c3 = abs(v0 - ref) < 0.005 and vb[0.2] > ref + 0.005 and vb[0.8] > vb[0.2]

    print("E4  interaction, both U4 regimes (n 2.0→decline, V_b 0→.05)")
    c4_by = {}
    for cons in (False, True):
        b  = tail(run_valence(2.0, 0.6, 0.00, 1.0, "A", consumable=False))
        df = tail(run_valence(2.0, 0.6, 0.05, 1.0, "A", consumable=False)) - b
        db = tail(run_valence(2.0, 0.6, 0.00, 1.0, "A", consumable=cons)) - b
        dB = tail(run_valence(2.0, 0.6, 0.05, 1.0, "A", consumable=cons)) - b
        c4_by[cons] = dB > df + db + 0.005
        print(f"    consumable={cons}: Δf={round(df,3)} Δn={round(db,3)}"
              f" Δboth={round(dB,3)} sum={round(df+db,3)}")
    c4 = all(c4_by.values())

    print("\nCLAIM_TABLE evaluation (refute → edit claim, not sim)")
    tags = {"C1": "" if c1_stable else " [U1/U3-SENSITIVE]",
            "C2": "" if len(set(c2_by_form.values())) == 1 else " [U1-SENSITIVE]",
            "C3": "",
            "C4": "" if len(set(c4_by.values())) == 1 else " [U4-SENSITIVE]"}
    for name, ok in (("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4)):
        print(f"    {name}  {'HOLDS' if ok else 'REFUTED — update the claim'}{tags[name]}")
    print("\n    standing conditions: U2 single-point calibration,")
    print("    U5 screened charge deleted (probably false) — all verdicts conditional.")

if __name__ == "__main__":
    main()
