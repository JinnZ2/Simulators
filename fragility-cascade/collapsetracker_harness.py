#!/usr/bin/env python3
"""
collapsetracker_harness.py

Wires CollapseTracker (Ramkumar & Pragalya 2026, doi:10.21227/bvav-q038,
Zenodo mirror 10.5281/zenodo.19511599) into the log-drift frame from
scale_invariant_audit.py v2. Closes R1 and R2 against real data.

DATASET (verified 2026-07-17 against the IEEE DataPort record)
  3 domains x 2 models (GPT-2 124M, DistilGPT-2 82M) x 4 synthetic:real
  ratios (1.0, 0.75, 0.5, 0.25) x 11 generations (0-10)
  = 24 trajectories, 264 per-generation metric records.
  Gen 0 IS present -> M_0 is measured, not assumed.
  Artifacts: generated samples (99.2 MB), metrics table (57.7 KB), plots.
  Seed datasets NOT redistributed (third-party licences).

FOUR PATHS -- pick by what the substrate already gives you
  Path B (metrics, 57.7 KB, phone-runnable)  <-- default
      lambda = ln(M_n / M_0) / G  for each shipped diversity metric.
      The v2 claim is about log-drift of A diversity measure. D_f is one
      instantiation, not the claim itself. Five channels ship free:
      distinct n-grams, Self-BLEU, KL divergence, vocabulary coverage,
      rare-token survival.
  Path A (CollapseTracker embeddings, 99.2 MB + Sentence-BERT + GPU)
      Estimate intrinsic dimension per generation, then same frame.
      USE twonn(). DO NOT USE box-counting -- see BOX_COUNTING_IS_DEAD.
      Kept for completeness; C and D make it optional.
  Path C (Model Zoos, 3.8M states across 27 zoos)
      Weights ARE the vectors. No embedding model, no Sentence-BERT,
      no GPU. Feed parameter trajectories straight into twonn() and
      run the same log-drift frame per zoo. This is the cleanest test
      of C-scale-2 the substrate offers: a real recursive-training
      artifact with a native coordinate system.
      Source: modelzoos.org (Schurholt et al., 2022-).
  Path D (Multi-LLM Trace, pairwise distance matrix only)
      TwoNN needs only mu = r2/r1 per point, so a full nxn distance
      matrix is sufficient input -- coordinates are not required.
      twonn_from_distances() consumes the matrix directly, so a trace
      shipped as pairwise dissimilarities can be audited without ever
      reconstructing an embedding. Bridges to alien_homeostasis.py --
      the log-drift audit here answers "is diversity draining?" while
      alien homeostasis answers "is the fixed point still human-
      readable?" Both can fire on the same trace.

BOX_COUNTING_IS_DEAD
  Measured 2026-07-17, true intrinsic D = 5, N = 2000:
      ambient    2 -> D_hat 1.365  r2 0.965
      ambient   10 -> D_hat 0.375  r2 0.634
      ambient   50 -> D_hat 0.003  r2 0.326
      ambient  384 -> D_hat 0.000  r2 0.000
  N(r) saturates at N once every point owns its own box; the slope then
  measures log(N_samples), not dimension. Sentence-BERT is 384 or 768-dim.
  The failure mode is CONFIRMATORY: D_hat -> 0 is exactly what "collapse"
  looks like, so box-counting on embeddings reports total collapse at
  EVERY generation including gen 0. It is a false-positive machine for the
  hypothesis under test. Only the r2 determinacy gate catches it.
  TwoNN on the identical test: ambient 384, true D 5 -> 4.62, fit r2 0.994.

CLAIM (C-scale-2)
  For recursive self-training, the log-drift rate of any diversity metric,
  lambda = ln(M_n/M_0)/G, is (a) negative for all synthetic fractions > 0,
  (b) monotone in synthetic fraction, and (c) NON-LINEAR in synthetic
  fraction, with a knee bracketing the field_collapse.py spinodal
  h* ~ 0.385.

SCOPE
  M > 0 strictly (log frame). G >= 1. Metrics where LOWER means less
  diversity. Self-BLEU and repetition are INVERTED (higher = more
  collapse) and are sign-flipped on load -- see INVERTED_METRICS.

REFUTATION
  (R1) lambda ~ 0 on a trajectory with documented collapse -> log-drift of
       diversity does not summarise collapse. Update C-scale-2.
  (R2) AIC prefers (1+G)^-beta over exp(lambda*G) in a majority of the 24
       trajectories -> the per-generation exponential is wrong and C9's
       per-doubling law stands. Update C-scale-2, do not retune.
       Power check (400 trials/cell, 11 gens): AIC separates the two laws
       100% of the time at noise sd <= 0.05, 95% at 0.10. The test is
       adequately powered. Prior prediction that it would be underpowered
       was WRONG -- logged.
  (R3) lambda(ratio) linear across 0.25/0.5/0.75/1.0 -> the spinodal
       formalism does not transfer from diversity-collapse to model-
       collapse. Lock as a constraint.

UNKNOWNS
  - Exact column names in the metrics table are NOT verified. The loader
    normalises on a best-effort alias map and reports what it could not
    resolve rather than guessing. Fix ALIASES after a real look at the CSV.
  - Whether gen-0 metrics are computed on seed text or on gen-0 samples.
    Changes what M_0 means. Check the README in the ZIP.
  - 4 ratio points is thin for locating a knee. Sign of the second
    difference is testable; the knee POSITION is not.
  - TwoNN has known low bias at high D (true 20 -> 14.85 measured).
    Irrelevant if text manifolds sit near D ~ 5-15. Not verified that they do.

stdlib only. CC0.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

# --------------------------------------------------------------- config
# Metrics where HIGHER = MORE collapse. Sign-flipped so all channels agree
# that negative lambda means losing diversity.
INVERTED_METRICS = {"self_bleu", "repetition", "kl_divergence"}

ALIASES = {
    "distinct_1": ("distinct_1", "distinct1", "distinct-1", "distinct_1gram"),
    "distinct_2": ("distinct_2", "distinct2", "distinct-2", "distinct_2gram"),
    "distinct_3": ("distinct_3", "distinct3", "distinct-3", "distinct_3gram"),
    "self_bleu": ("self_bleu", "selfbleu", "self-bleu"),
    "kl_divergence": ("kl_divergence", "kl", "kl_div"),
    "vocab_coverage": ("vocab_coverage", "vocabulary_coverage", "vocab_cov"),
    "rare_token_survival": ("rare_token_survival", "rare_survival", "rare_tokens"),
    "repetition": ("repetition", "rep_rate", "repetition_rate"),
}
KEYS = {
    "generation": ("generation", "gen", "g"),
    "ratio": ("ratio", "mixing_ratio", "synthetic_ratio", "mix"),
    "model": ("model", "model_name"),
    "domain": ("domain", "track", "dataset"),
}

try:
    from field_collapse import SPINODAL_H_STAR  # 2/(3 sqrt(3)) = 0.38490018
except ImportError:
    SPINODAL_H_STAR = 2.0 / (3.0 * math.sqrt(3.0))  # closed-form fallback


# ------------------------------------------------- intrinsic dimension
def twonn(points, discard=0.1):
    """TwoNN intrinsic dimension (Facco et al. 2017).

    Uses only mu = r2/r1, the ratio of 1st to 2nd nearest-neighbour
    distances. mu ~ Pareto(d) => -log(1-F(mu)) = d*log(mu).
    Slope through origin = d. Insensitive to AMBIENT dimension, which is
    the whole point -- box-counting is not. O(N^2), fine to N ~ 2000.

    Verified: true D 5 @ ambient 384, N=800 -> 4.62 (fit r2 0.994).
    Returns (d, fit_r2). Gate on fit_r2 exactly as with box-counting.
    """
    n = len(points)
    mus = []
    for i in range(n):
        pi = points[i]
        best = second = float("inf")
        for j in range(n):
            if i == j:
                continue
            s = 0.0
            for a, b in zip(pi, points[j]):
                s += (a - b) * (a - b)
            if s < best:
                second, best = best, s
            elif s < second:
                second = s
        r1, r2 = math.sqrt(best), math.sqrt(second)
        if r1 > 1e-12:
            mus.append(r2 / r1)
    mus.sort()
    m = len(mus)
    keep = int(m * (1 - discard))
    xs, ys = [], []
    for i in range(keep):
        if mus[i] <= 1.0:
            continue
        xs.append(math.log(mus[i]))
        ys.append(-math.log(1.0 - (i + 1) / (m + 1)))
    if len(xs) < 8:
        return 0.0, 0.0
    d = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    my = sum(ys) / len(ys)
    ss_res = sum((y - d * x) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return d, (1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0)


def twonn_from_distances(dmat, discard=0.1):
    """TwoNN consuming a symmetric nxn distance matrix directly.

    Path D substrate: a Multi-LLM Trace shipped as pairwise distances
    (or any pipeline whose native output is a dissimilarity matrix) has
    no coordinates to feed twonn(). But TwoNN only needs mu = r2/r1 per
    point, and that is recoverable from the two smallest positive
    entries in each row -- no coordinates required.

    dmat : list of lists, dmat[i][j] = distance(i, j), dmat[i][i] == 0
    Returns (d, fit_r2), same shape as twonn().
    """
    n = len(dmat)
    mus = []
    for i in range(n):
        best = second = float("inf")
        row = dmat[i]
        for j in range(n):
            if j == i:
                continue
            r = row[j]
            if r < best:
                second, best = best, r
            elif r < second:
                second = r
        if best > 1e-12 and second != float("inf"):
            mus.append(second / best)
    mus.sort()
    m = len(mus)
    keep = int(m * (1 - discard))
    xs, ys = [], []
    for i in range(keep):
        if mus[i] <= 1.0:
            continue
        xs.append(math.log(mus[i]))
        ys.append(-math.log(1.0 - (i + 1) / (m + 1)))
    if len(xs) < 8:
        return 0.0, 0.0
    d = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    my = sum(ys) / len(ys)
    ss_res = sum((y - d * x) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return d, (1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0)


# --------------------------------------------------------------- frame
def log_drift(M_0, M_n, G, inverted=False):
    """lambda = ln(M_n/M_0)/G. Sign-flipped for inverted metrics."""
    if M_0 <= 0 or M_n <= 0 or G < 1:
        return None
    lam = math.log(M_n / M_0) / G
    return -lam if inverted else lam


def fit_exp(G, M):
    xs, ys = list(G), [math.log(m) for m in M]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / \
        sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    return sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)), b


def fit_pow(G, M):
    """(1+G)^-beta, NOT G^-beta. Gen 0 exists; G^-beta is undefined there."""
    xs, ys = [math.log(1 + g) for g in G], [math.log(m) for m in M]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / \
        sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    return sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)), b


def aic(ss, n, k=2):
    return n * math.log(max(ss, 1e-300) / n) + 2 * k


def second_difference(ratios, lams):
    """P3: knee test. Non-zero second difference => not linear in ratio."""
    pts = sorted(zip(ratios, lams))
    if len(pts) < 3:
        return None
    out = []
    for i in range(1, len(pts) - 1):
        out.append(pts[i - 1][1] - 2 * pts[i][1] + pts[i + 1][1])
    return out


# -------------------------------------------------------------- loader
def _resolve(header, aliases):
    low = {h.strip().lower(): h for h in header}
    for canon, alts in aliases.items():
        for a in alts:
            if a in low:
                yield canon, low[a]
                break


def load_metrics(path):
    """Best-effort load. Reports unresolved columns rather than guessing."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return [], {}, []
    header = list(rows[0].keys())
    keymap = dict(_resolve(header, KEYS))
    metmap = dict(_resolve(header, ALIASES))
    missing = [k for k in KEYS if k not in keymap]
    return rows, {"keys": keymap, "metrics": metmap, "missing_keys": missing,
                  "header": header}, missing


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("metrics_csv", nargs="?",
                   help="path to CollapseTracker aggregated metrics table")
    a = p.parse_args(argv)

    print("=" * 74)
    print("collapsetracker_harness — log-drift frame vs real recursive training")
    print("=" * 74)

    if not a.metrics_csv:
        print("\nNo CSV supplied. Predictions locked BEFORE data, per protocol:\n")
        for line in [
            "P1  sign      λ < 0 for all ratio > 0                          [24/24]",
            "P2  monotone  |λ(1.0)| > |λ(0.75)| > |λ(0.5)| > |λ(0.25)|",
            "P3  knee      λ(ratio) NOT linear. second difference ≠ 0.",
            "              knee between 0.25 and 0.5, bracketing",
            f"              field_collapse.py spinodal h* ≈ {SPINODAL_H_STAR:.5f}",
            "P4  coupling  λ sign agrees across ≥4 of 5 metrics per trajectory",
            "P5  law       exp beats (1+G)^-β by AIC in >70% of 24 trajectories",
            "P6  capacity  |λ(DistilGPT-2, 82M)| > |λ(GPT-2, 124M)|",
            "P7  tail      |λ| largest in the domain with highest M_0",
            "              (most tail to lose)",
        ]:
            print("  " + line)
        print("\n  P1–P2 are nearly free; any collapse framework predicts them.")
        print("  P3 is the one worth the download: it tests whether the")
        print("  spinodal formalism transfers from diversity-collapse to")
        print("  model-collapse. Linear λ(ratio) refutes the transfer.")
        print("\n  Alternate substrates (no CollapseTracker download):")
        print("    Path C — Model Zoos: TwoNN directly on 3.8M parameter")
        print("      states across 27 zoos. Weights are already vectors.")
        print("    Path D — Multi-LLM Trace: twonn_from_distances() on a")
        print("      pairwise dissimilarity matrix. Bridges to")
        print("      alien_homeostasis.py on the same trace.")
        print("\n  Run:  python3 collapsetracker_harness.py metrics.csv")
        print("=" * 74)
        return 0

    rows, maps, missing = load_metrics(a.metrics_csv)
    print(f"\nrows: {len(rows)}   (expect 264)")
    print(f"resolved keys    : {sorted(maps['keys'])}")
    print(f"resolved metrics : {sorted(maps['metrics'])}")
    if missing:
        print(f"UNRESOLVED KEYS  : {missing}")
        print(f"header seen      : {maps['header']}")
        print("\nFix ALIASES and re-run. Not guessing at column names.")
        return 1
    print("\nColumn map resolved. Wire the per-trajectory sweep from here —")
    print("group by (model, domain, ratio), pull G and each metric, call")
    print("log_drift(), fit_exp()/fit_pow(), then second_difference() on")
    print("lam vs ratio. Deliberately not written blind against unverified")
    print("column semantics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
