"""
confound_sweep.py
-----------------
P1 failed. Same-family models do not correlate more than cross-family models
(p = 0.42, significant in 0/12 seeds). But the inflation is real and large
(N_eff = 2.48 from 15 models, 6.29x).

So the coherence is there and the declared phylogeny does not explain it.

THE NON-EXPLANATION IS THE SIGNAL. Something is making 15 estimators agree, and
it is not their mathematical ancestry. What?

The correlation matrix in `phylogeny.py` is CONFOUNDED. It mixes at least four
sources, and reports their sum as one number:

    1. real structure in the signal
    2. shared measurement window   (all 15 estimators see the same 40 points)
    3. shared preprocessing        (all 15 see the same detrended series)
    4. genuine estimator kinship   (the thing P1 tried and failed to measure)

You cannot attribute inflation to (4) until you have subtracted (1), (2), (3).
Nobody did. This module does.

THE DISCRIMINATING TEST
-----------------------
Feed the same 15 estimators PURE WHITE NOISE. There is no signal, no regime,
no structure, nothing to converge on.

  If inflation vanishes    -> the coherence was in the SIGNAL. Estimators are fine.
  If inflation SURVIVES    -> the coherence is in the APPARATUS. The estimators
                              agree because they are all squinting through the
                              same 40-point window, not because the world
                              has structure. Every "consensus" built this way is
                              measuring its own instrument.

That second case is the one that matters. It would mean a 90-model ensemble
agreeing about ENSO could be reporting the shape of its own rolling window.

Falsifiable claims:
  C1. Inflation on white noise is ~1.0x (no phantom consensus without signal).
      REFUTED IF inflation on noise is comparable to inflation on signal.
  C2. Breaking input coupling (per-model window offsets) reduces inflation.
      REFUTED IF inflation is unchanged when models stop sharing exact inputs.
  C3. Diversifying preprocessing reduces inflation.
      REFUTED IF unchanged.
  C4. Inflation depends on window length W. Short windows resolve less shared
      structure -> less inflation.
      REFUTED IF inflation is flat in W.
  C5. Once input coupling and preprocessing are broken, the within-family gap
      emerges (phylogeny was masked by confounds, not absent).
      REFUTED IF the gap stays at chance -> phylogeny is genuinely absent, and
      P1's failure was real rather than confounded.

Refutation protocol: update the claim, never retune the estimator.

CC0. stdlib only. Phone-buildable.
"""

import math
import random

import models as M
from core import _mean, _std
from phylogeny import (artificial_consensus, within_vs_cross,
                       correlation_matrix, eigenvalues_sym, participation_ratio)


N = 320
SHIFT = 170


# ----------------------------------------------------------------- generators

def structured_signal(seed=3):
    """AR(1) + sinusoid with a regime shift. Real structure to converge on."""
    rng = random.Random(seed)
    x, prev = [], 0.0
    for t in range(N):
        period, noise, phi = (40.0, 0.25, 0.80) if t < SHIFT else (13.0, 0.65, 0.35)
        prev = phi * prev + (1 - phi) * math.sin(2 * math.pi * t / period) \
               + rng.gauss(0, noise)
        x.append(prev)
    return x


def white_noise(seed=3):
    """No structure. Nothing to agree about. The control."""
    rng = random.Random(seed + 9001)
    return [rng.gauss(0, 1) for _ in range(N)]


def red_noise(seed=3, phi=0.8):
    """
    AR(1), no oscillation, no regime shift. Autocorrelation but no 'events'.
    The honest null for geophysical time series -- white noise is too easy a
    control, because real climate data is red even with nothing happening.
    """
    rng = random.Random(seed + 4242)
    x, prev = [], 0.0
    for _ in range(N):
        prev = phi * prev + rng.gauss(0, 1)
        x.append(prev)
    return x


# -------------------------------------------------------------- preprocessors

def pp_raw(x):
    return x[:]


def pp_detrend(x):
    m = _mean(x)
    return [v - m for v in x]


def pp_difference(x):
    return [x[i] - x[i - 1] for i in range(1, len(x))]


def pp_standardize(x):
    m, s = _mean(x), _std(x) + 1e-9
    return [(v - m) / s for v in x]


PREPROCESSORS = [pp_raw, pp_detrend, pp_difference, pp_standardize]


# --------------------------------------------------------------- the harness

def run_condition(signal, window=40, offset_jitter=0, preproc_diverse=False,
                  seed=0):
    """
    Produce the model-score matrix under a given experimental condition.

    offset_jitter : each model sees the signal starting at a random offset in
                    [0, offset_jitter]. Breaks EXACT input sharing while keeping
                    the same underlying process. jitter=0 -> everyone sees the
                    same points (the confounded baseline).
    preproc_diverse: each model gets a randomly assigned preprocessor instead of
                    all sharing one.
    """
    rng = random.Random(seed)
    mods = M.all_models()
    series = {}
    for m in mods:
        m.window = window
        off = rng.randint(0, offset_jitter) if offset_jitter else 0
        pp = rng.choice(PREPROCESSORS) if preproc_diverse else pp_detrend
        x = pp(signal[off:])
        if len(x) <= window + 5:
            continue
        series[m.name] = m.predict(x).prediction

    if len(series) < 3:
        return None
    L = min(len(v) for v in series.values())
    return {k: v[:L] for k, v in series.items()}


def measure(series):
    if series is None:
        return None
    ac = artificial_consensus(series)
    p1 = within_vs_cross(series, n_perm=600, seed=5)
    return {
        "n_eff": ac["n_empirical"],
        "inflation": ac["inflation_factor"],
        "gap": p1["gap"],
        "p": p1["p_value"],
        "phylo_visible": p1["p_value"] < 0.05,
    }


def avg_over_seeds(fn, seeds=8, **kw):
    """Every number here gets a seed sweep. No single-seed findings."""
    rows = []
    for s in range(seeds):
        sig = kw["gen"](s)
        r = measure(run_condition(sig, seed=s,
                                  window=kw.get("window", 40),
                                  offset_jitter=kw.get("offset_jitter", 0),
                                  preproc_diverse=kw.get("preproc_diverse", False)))
        if r:
            rows.append(r)
    if not rows:
        return None
    return {
        "n_eff": _mean([r["n_eff"] for r in rows]),
        "inflation": _mean([r["inflation"] for r in rows]),
        "gap": _mean([r["gap"] for r in rows]),
        "p": _mean([r["p"] for r in rows]),
        "phylo_hits": sum(r["phylo_visible"] for r in rows),
        "n": len(rows),
    }


# -------------------------------------------------------------------- report

def report(seeds=8):
    print("=" * 78)
    print("CONFOUND SWEEP — what is actually driving the 6.29x consensus inflation?")
    print("=" * 78)

    # ---------------------------------------------------------------- C1
    print("\n[C1] THE APPARATUS TEST — same 15 estimators, no signal to agree on")
    print(f"{'generator':<22} {'N_eff':>7} {'inflation':>10} {'phylo p':>9}")
    print("-" * 78)
    for name, gen in (("structured signal", structured_signal),
                      ("red noise (AR1)", red_noise),
                      ("white noise", white_noise)):
        r = avg_over_seeds(None, seeds=seeds, gen=gen)
        print(f"{name:<22} {r['n_eff']:>7.2f} {r['inflation']:>9.2f}x {r['p']:>9.3f}")

    base = avg_over_seeds(None, seeds=seeds, gen=structured_signal)
    rn = avg_over_seeds(None, seeds=seeds, gen=red_noise)
    wn = avg_over_seeds(None, seeds=seeds, gen=white_noise)

    print("\n     DECOMPOSITION (inflation is additive across these strata):")
    print(f"       apparatus floor      {wn['inflation']:5.2f}x   "
          f"(white noise: NOTHING to agree about)")
    print(f"       + autocorrelation    {rn['inflation'] - wn['inflation']:+5.2f}x  "
          f"-> {rn['inflation']:.2f}x  (red noise: memory, no events)")
    print(f"       + real structure     {base['inflation'] - rn['inflation']:+5.2f}x  "
          f"-> {base['inflation']:.2f}x  (regime shift present)")

    frac = wn["inflation"] / base["inflation"]
    print(f"\n     C1 is NOT a binary. It is a floor. {frac:.0%} of the observed")
    print(f"     inflation is present with NO SIGNAL AT ALL. On pure white noise,")
    print(f"     15 independent estimators collapse to N_eff = {wn['n_eff']:.2f}.")
    print(f"     ~{15 - wn['n_eff']:.0f} of 15 votes are manufactured by the apparatus")
    print("     before the world contributes anything.")
    print("     A 90-model ensemble reporting consensus has not shown that its")
    print("     agreement exceeds this floor. Almost nobody computes the floor.")

    # ---------------------------------------------------------------- C2, C3
    print("\n[C2/C3] DECONFOUNDING — break shared inputs, then shared preprocessing")
    print(f"{'condition':<34} {'N_eff':>7} {'inflation':>10} {'phylo p':>9} {'hits':>6}")
    print("-" * 78)
    conds = [
        ("baseline (shared everything)",  dict(offset_jitter=0,  preproc_diverse=False)),
        ("+ offset jitter (inputs differ)", dict(offset_jitter=25, preproc_diverse=False)),
        ("+ diverse preprocessing",        dict(offset_jitter=0,  preproc_diverse=True)),
        ("+ both",                         dict(offset_jitter=25, preproc_diverse=True)),
    ]
    res = {}
    for label, kw in conds:
        r = avg_over_seeds(None, seeds=seeds, gen=structured_signal, **kw)
        res[label] = r
        print(f"{label:<34} {r['n_eff']:>7.2f} {r['inflation']:>9.2f}x "
              f"{r['p']:>9.3f} {r['phylo_hits']:>3}/{r['n']}")

    b = res["baseline (shared everything)"]["inflation"]
    for label, _ in conds[1:]:
        d = res[label]["inflation"] - b
        print(f"     {label:<32} delta inflation = {d:+.2f}x")

    # ---------------------------------------------------------------- C4
    print("\n[C4] TIMESCALE AXIS — does the window itself manufacture agreement?")
    print(f"{'window W':>9} {'N_eff':>7} {'inflation':>10} {'phylo p':>9}")
    print("-" * 78)
    infl_by_w = {}
    for W in (10, 20, 40, 80):
        r = avg_over_seeds(None, seeds=seeds, gen=structured_signal, window=W)
        if r:
            infl_by_w[W] = r["inflation"]
            print(f"{W:>9} {r['n_eff']:>7.2f} {r['inflation']:>9.2f}x {r['p']:>9.3f}")
    if len(infl_by_w) > 1:
        ws = sorted(infl_by_w)
        trend = infl_by_w[ws[-1]] - infl_by_w[ws[0]]
        print(f"\n     inflation(W={ws[-1]}) - inflation(W={ws[0]}) = {trend:+.2f}x")
        print(f"     C4 {'SUPPORTED' if abs(trend) > 0.5 else 'REFUTED'}: "
              f"inflation {'depends on' if abs(trend) > 0.5 else 'is flat in'} window length.")

    # ---------------------------------------------------------------- C5
    print("\n[C5] Does phylogeny EMERGE once the confounds are removed?")
    bl = res["baseline (shared everything)"]
    full = res["+ both"]
    n = full["n"]
    expected_by_chance = 0.05 * n     # hits expected at alpha=0.05 under the null

    print(f"     baseline     mean phylo p = {bl['p']:.3f}   "
          f"significant in {bl['phylo_hits']}/{bl['n']} seeds")
    print(f"     deconfounded mean phylo p = {full['p']:.3f}   "
          f"significant in {full['phylo_hits']}/{n} seeds")
    print(f"     hits expected by chance at alpha=0.05: {expected_by_chance:.1f}/{n}")

    # A knife-edge (1 > 0) is exactly the error this repo exists to catch.
    # Demand hits clearly above the chance floor before claiming emergence.
    clearly_above = full["phylo_hits"] >= max(3, 3 * expected_by_chance)
    direction = full["p"] < bl["p"]

    if clearly_above:
        print("     C5 SUPPORTED: phylogeny was MASKED by the confounds, not absent.")
        print("     -> P1's failure was a measurement artifact. The tree may be real.")
    elif direction:
        print("     C5 INCONCLUSIVE. Mean p moved the right way "
              f"({bl['p']:.3f} -> {full['p']:.3f}), but "
              f"{full['phylo_hits']}/{n} significant seeds is AT CHANCE.")
        print("     -> Suggestive of masking. NOT evidence of it. Do not promote this.")
        print("        Needs more seeds, or stronger deconfounding, to become testable.")
        print("     -> Reporting '1 > 0, therefore supported' would be the exact")
        print("        knife-edge error this repo was built to catch.")
    else:
        print("     C5 REFUTED: phylogeny does not emerge even deconfounded.")
        print("     -> P1's failure was REAL. Declared mathematical ancestry does not")
        print("        predict estimator agreement. The tree is decoration. Drop it.")

    print("\n" + "=" * 78)
    print("WHAT THE GAP WAS HIDING")
    print("=" * 78)
    print("""
  The correlation matrix reported ONE number and it was a SUM of four sources.
  Attributing it to 'mathematical kinship' was never licensed by the data.

  Consensus among models is not evidence about the world until you have shown
  the models were not all looking through the same instrument at the same time
  in the same way. Until then, agreement measures the apparatus.

  This is the metrology point, applied to models instead of thermometers:
      corruption(trend) = corruption(measurement) x corruption(framework)
  Multiplicative. You cannot audit the framework while the measurement is shared.
""")


if __name__ == "__main__":
    report()
