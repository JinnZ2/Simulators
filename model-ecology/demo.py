"""
demo.py
-------
End-to-end audit on a synthetic signal with a known regime shift.

The shift is planted in the SIGNAL, not in the models. Every model computes a
real estimator from the real data. Every claim is free to come out false, and
this script reports what actually happened rather than what was hoped for.

FOUR DEGENERACIES THAT HAD TO BE FIXED (they are the whole lesson):

  1. A 0/1 step `truth` has ZERO VARIANCE inside each half, so every correlation
     against it returns 0.0 and every model gets labeled a crank. The truth must
     be the CONTINUOUS PHYSICAL QUANTITY that actually changed -- here, the local
     variance of the signal -- not a label for the change.

  2. If Observer.score sees only constants (same confidence, same uncertainty for
     every model), observer churn is trivially zero and 'observer-invariant' is a
     measurement of nothing. Diagnostics must be model-specific and computed
     WITHOUT ground truth, or the invariance claim is vacuous.

  3. A cluster threshold that labels every window 'structured' has NO DYNAMIC
     RANGE. D1 is then not false, it is UNTESTABLE. Sweep the threshold and say
     so out loud.

  4. 'within=0.534 vs cross=0.533, therefore supported' is noise reported as
     signal. P1 needs a permutation null.

A pipeline that cannot detect its own degeneracy is not an audit.

Run: python3 demo.py
"""

import random
import math

from core import _mean, _std, pearson
import models as M
from phylogeny import within_vs_cross, artificial_consensus, family_of
from disagreement import classify, rolling, information_contribution
from meta_engine import (sweep_observers, observer_sensitivity,
                         representation_invariance, stability_statement)

N = 320
SHIFT = 170
WINDOW = 40


def make_signal(seed=3):
    """
    Regime A: slow oscillation (period 40), low noise, strong autocorrelation.
    Regime B: fast oscillation (period 13), high noise, weak autocorrelation.
    Nothing model-specific is planted. Only the physics of the signal changes.
    """
    rng = random.Random(seed)
    x, prev = [], 0.0
    for t in range(N):
        period, noise, phi = (40.0, 0.25, 0.80) if t < SHIFT else (13.0, 0.65, 0.35)
        drive = math.sin(2 * math.pi * t / period)
        prev = phi * prev + (1 - phi) * drive + rng.gauss(0, noise)
        x.append(prev)
    return x


def local_variance(signal, window):
    """FIX 1. The continuous physical quantity that actually shifted."""
    return [_std(signal[i - window:i]) for i in range(window, len(signal) + 1)]


def add_diagnostics(results, series):
    """
    FIX 2. Model-specific, truth-free diagnostics so observers have something
    to disagree about. None of these peek at the answer.
    """
    L = min(len(v) for v in series.values())
    consensus = [_mean([series[k][i] for k in series]) for i in range(L)]
    for nm, r in results.items():
        s = series[nm][:L]
        sd = _std(s) + 1e-9
        mu = _mean(s)
        z = [(v - mu) / sd for v in s]
        d2 = [z[i - 1] - 2 * z[i] + z[i + 1] for i in range(1, len(z) - 1)]
        r.confidence = max(0.0, min(1.0, abs(pearson(s[:-1], s[1:]))))
        r.uncertainty = [min(1.0, _std(s))] * len(s)
        r.diagnostics["novelty"] = 1.0 - abs(pearson(s, consensus))
        r.diagnostics["smoothness"] = 1.0 / (1.0 + _std(d2))
    return consensus


def sweep_threshold(series, shift_idx):
    """FIX 3. Find a threshold where the detector actually discriminates."""
    rows = []
    for th in (0.30, 0.45, 0.60, 0.75, 0.85, 0.92):
        roll = rolling(series, window=60, step=5, thresh=th)
        regimes = [r["regime"] for _, r in roll]
        distinct = len(set(regimes))
        early = [r for t, r in roll if t < shift_idx - 30]
        lead = [r for t, r in roll if shift_idx - 30 <= t < shift_idx]

        def frac(rs, k):
            return sum(1 for r in rs if r["regime"] == k) / len(rs) if rs else 0.0

        rows.append({
            "thresh": th, "distinct_regimes": distinct,
            "early_struct": frac(early, "structured"),
            "lead_struct": frac(lead, "structured"),
            "early_isol": frac(early, "isolated"),
            "lead_isol": frac(lead, "isolated"),
            "saturated": distinct == 1,
        })
    return rows


def main():
    signal = make_signal()
    mods = M.all_models()
    results = {m.name: m.predict(signal) for m in mods}
    series = {k: v.prediction for k, v in results.items()}
    L = min(len(v) for v in series.values())
    series = {k: v[:L] for k, v in series.items()}
    shift_idx = SHIFT - WINDOW

    consensus = add_diagnostics(results, series)
    truth = local_variance(signal, WINDOW)[:L]      # FIX 1

    print("=" * 76)
    print(f"MODEL ECOLOGY AUDIT  |  {len(mods)} models, "
          f"{len(set(m.family for m in mods))} families, {L} scored windows")
    print("=" * 76)

    # ----------------------------------------------------------------- P1
    print("\n[P1] Same-family models correlate more than cross-family? (perm null)")
    p1 = within_vs_cross(series)
    print(f"     within |r| = {p1['within_family_mean_abs_r']:.3f} (n={p1['n_within']})   "
          f"cross |r| = {p1['cross_family_mean_abs_r']:.3f} (n={p1['n_cross']})")
    print(f"     gap = {p1['gap']:+.4f}   p = {p1['p_value']:.4f}  "
          f"({p1['n_perm']} label permutations)")
    print(f"     P1 SUPPORTED: {p1['P1_supported']}")
    if not p1["P1_supported"]:
        print("     -> `family` does NOT explain the correlation structure here.")
        print("        The tree is decoration on this data. Revise the TREE.")

    # --------------------------------------------------- artificial consensus
    print("\n[ARTIFICIAL CONSENSUS] how many independent votes are really here?")
    ac = artificial_consensus(series)
    print(f"     naive count = {ac['n_naive']:.0f}    empirical N_eff = "
          f"{ac['n_empirical']:.2f}    phylogenetic N_eff = {ac['n_phylo']:.2f}")
    print(f"     phantom votes = {ac['artificial_consensus']:.2f}    "
          f"inflation = {ac['inflation_factor']:.2f}x")
    print(f"     |N_phylo - N_empir| = {ac['phylo_error']:.2f}  <- P2 error")
    if ac["phylo_error"] > 2.0:
        print("     -> tree predicts far more independence than the spectrum shows.")
        print("        Consistent with P1 failing. The TREE is wrong, not the spectrum.")

    # ----------------------------------------------------------------- D1
    print("\n[D1] Does STRUCTURED disagreement lead the shift? (threshold sweep)")
    print(f"     {'thresh':>7} {'regimes':>8} {'early_str':>10} {'lead_str':>9} "
          f"{'early_iso':>10} {'lead_iso':>9}  status")
    testable = []
    for r in sweep_threshold(series, shift_idx):
        status = "SATURATED (untestable)" if r["saturated"] else "discriminating"
        if not r["saturated"]:
            testable.append(r)
        print(f"     {r['thresh']:>7.2f} {r['distinct_regimes']:>8} "
              f"{r['early_struct']:>10.2f} {r['lead_struct']:>9.2f} "
              f"{r['early_isol']:>10.2f} {r['lead_isol']:>9.2f}  {status}")

    if not testable:
        print("     D1 VERDICT: UNTESTABLE on this signal. Detector saturates at")
        print("     every threshold. Not evidence for D1, not evidence against it.")
    else:
        d_s = _mean([r["lead_struct"] - r["early_struct"] for r in testable])
        d_i = _mean([r["lead_isol"] - r["early_isol"] for r in testable])
        ok = d_s > 0 and d_s > d_i
        print(f"     across discriminating thresholds: d_structured={d_s:+.3f}  "
              f"d_isolated={d_i:+.3f}")
        print(f"     D1 SUPPORTED: {ok}")
        if not ok:
            print("     -> structured disagreement did not lead here. Report it.")
            print("        Update the claim. Do not retune the detector.")

    # ----------------------------------------------------------------- D2
    print("\n[D2] Species census against a CONTINUOUS truth (local variance)")
    census = {n: information_contribution(s, truth, consensus, shift_idx)
              for n, s in sorted(series.items())}
    for sp in ("prophet", "workhorse", "conformist", "crank"):
        mem = [f"{n}[{family_of(n)[:4]}]" for n, v in census.items()
               if v["species"] == sp]
        print(f"     {sp:<11}: {', '.join(mem) if mem else '-'}")
    top = sorted(census.items(), key=lambda kv: -kv[1]["info_contribution"])[:4]
    print("     ranked by INFORMATION CONTRIBUTION (not accuracy):")
    for n, v in top:
        print(f"       {n:<22} pre={v['pre_skill']:+.2f} post={v['post_skill']:+.2f} "
              f"dissent={v['dissent']:.2f}  IC={v['info_contribution']:.3f}")

    # ----------------------------------------------------------------- M1
    print("\n[M1] Observer sensitivity: vary ONLY the observer (32 profiles)")
    os_ = observer_sensitivity(mods, results, sweep_observers(32))
    print(f"     mean rank agreement = {os_['mean_rank_agreement']:.3f}   "
          f"churn = {os_['observer_churn']:.3f}")
    print(f"     OBSERVER-INVARIANT  = {os_['invariant']}")
    print(f"     winners by observer = {os_['winners']}")
    if not os_["invariant"]:
        print("     -> 'the best model' is partly an artifact of who is looking.")

    # ----------------------------------------------------------------- M2
    print("\n[M2] Representation invariance. Manifold audited like everything else.")

    def conclusion(x):
        h = len(x) // 2
        sa, sb = _std(x[:h]), _std(x[h:])
        return abs(sa - sb) / (max(sa, sb) + 1e-9) > 0.15

    ri = representation_invariance(signal, conclusion)
    for rep, ok in ri["support"].items():
        mark = "supports" if ok else ("N/A" if ok is None else "does NOT support")
        star = "   <- the fashionable one" if rep == "manifold" else ""
        print(f"     {rep:<12}: {mark}{star}")
    print(f"     fraction supporting = {ri['fraction_supporting']:.1%}   "
          f"survives all = {ri['survives_all']}")

    # -------------------------------------------------------------- verdict
    print("\n" + "=" * 76)
    print("STABILITY STATEMENT")
    print("=" * 76)
    fam_frac = sum(1 for v in census.values()
                   if v["post_skill"] > v["pre_skill"]) / len(census)
    print("  conclusion: 'a regime transition occurred'")
    print("  " + stability_statement(fam_frac, os_["mean_rank_agreement"],
                                     ri["fraction_supporting"],
                                     round(ac["n_empirical"])))
    best = max(census, key=lambda k: census[k]["info_contribution"])
    print(f"\n  NOT '{best} is the best model.'")
    print("  That sentence is not available from this pipeline, by construction.")


if __name__ == "__main__":
    main()
