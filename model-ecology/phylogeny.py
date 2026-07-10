"""
phylogeny.py
------------
Group models by INHERITED ASSUMPTIONS, not by brand name.

    spectral      : Fourier, wavelet, Hilbert, EMD, SSA
    geometric     : delay embedding, Koopman, recurrence, persistent homology
    probabilistic : Bayesian changepoint, HMM, Gaussian process
    statistical   : autocorrelation, Hurst, mutual information, transfer entropy

THE CLAIM THAT MATTERS
----------------------
If two models agree, is it because they independently found something, or
because they are close relatives who inherited the same assumption and would
therefore make the SAME MISTAKE?

Ninety models agreeing is not ninety pieces of evidence. It might be four.

So we compute two numbers and compare them:

  N_phylo  : effective independent model count implied by the FAMILY TREE.
             Siblings are discounted by within-family similarity.

  N_empir  : effective independent model count implied by the OBSERVED
             correlation spectrum, via participation ratio
                 N_eff = (sum lambda_i)^2 / sum(lambda_i^2)
             over eigenvalues of the model-model correlation matrix.
             N_eff = k when there are k orthogonal directions of agreement;
             N_eff -> 1 when everything moves as one.

  ARTIFICIAL CONSENSUS = N_naive - N_empir,  where N_naive = number of models.

Falsifiable claims:
  P1. Same-family models correlate more than cross-family models, above chance.
      REFUTED IF within-family mean correlation <= cross-family mean correlation.
      If refuted, `family` is not a real axis and the phylogeny is decoration.
  P2. N_phylo tracks N_empir. Refuted if the family tree predicts independence
      that the correlation spectrum does not show (or vice versa) -- in which
      case the TREE IS WRONG and must be revised. Never revise the spectrum.

Refutation protocol: update the claim, never retune the measurement.

CC0. stdlib only.
"""

import math
from core import pearson


FAMILIES = {
    "spectral":      ["fourier", "wavelet", "hilbert", "emd", "ssa"],
    "geometric":     ["delay_embedding", "koopman", "recurrence", "persistent_homology"],
    "probabilistic": ["bayesian_changepoint", "hmm", "gaussian_process"],
    "statistical":   ["autocorrelation", "hurst", "mutual_information", "transfer_entropy"],
}

ANCESTRY = {m: fam for fam, members in FAMILIES.items() for m in members}


# ------------------------------------------------------- correlation matrix

def correlation_matrix(series_by_model: dict) -> tuple:
    names = sorted(series_by_model)
    n = len(names)
    M = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            r = pearson(series_by_model[names[i]], series_by_model[names[j]])
            M[i][j] = M[j][i] = r
    return names, M


# ------------------------------------------- Jacobi eigenvalues (symmetric)

def eigenvalues_sym(M: list, iters: int = 100, tol: float = 1e-10) -> list:
    """
    Cyclic Jacobi rotation. Symmetric matrices only. stdlib, no numpy.
    Returns eigenvalues (unsorted magnitude, we sort descending).
    """
    n = len(M)
    A = [row[:] for row in M]
    for _ in range(iters):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-14:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta ** 2 + 1.0))
                c = 1.0 / math.sqrt(t ** 2 + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return sorted((A[i][i] for i in range(n)), reverse=True)


def participation_ratio(eigs: list) -> float:
    """N_eff = (sum l)^2 / sum(l^2). Equals k for k equal nonzero eigenvalues."""
    eigs = [max(e, 0.0) for e in eigs]
    s1 = sum(eigs)
    s2 = sum(e * e for e in eigs)
    return (s1 * s1) / s2 if s2 > 0 else 0.0


# ---------------------------------------------------------- family structure

def family_of(model_name: str) -> str:
    return ANCESTRY.get(model_name, "unknown")


def _gap(names, M, labels) -> tuple:
    within, cross = [], []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            (within if labels[i] == labels[j] else cross).append(abs(M[i][j]))
    mw = sum(within) / len(within) if within else 0.0
    mc = sum(cross) / len(cross) if cross else 0.0
    return mw, mc, len(within), len(cross)


def within_vs_cross(series_by_model: dict, n_perm: int = 2000, seed: int = 11) -> dict:
    """
    P1 with a NULL. `mw > mc` by 0.001 is not evidence of anything.

    Permute the family labels n_perm times, recompute the gap, and ask how often
    chance produces a gap at least this large. That p-value is the claim.
    A knife-edge difference reported as 'supported' is exactly the kind of
    artificial consensus this repo exists to catch.
    """
    import random as _r
    names, M = correlation_matrix(series_by_model)
    labels = [family_of(n) for n in names]
    mw, mc, nw, nc = _gap(names, M, labels)
    obs_gap = mw - mc

    rng = _r.Random(seed)
    ge = 0
    for _ in range(n_perm):
        perm = labels[:]
        rng.shuffle(perm)
        pw, pc, _, _ = _gap(names, M, perm)
        if (pw - pc) >= obs_gap:
            ge += 1
    p = (ge + 1) / (n_perm + 1)

    return {
        "within_family_mean_abs_r": mw,
        "cross_family_mean_abs_r": mc,
        "gap": obs_gap,
        "p_value": p,
        "P1_supported": p < 0.05,
        "n_within": nw,
        "n_cross": nc,
        "n_perm": n_perm,
    }


def n_phylo(series_by_model: dict) -> float:
    """
    Effective count from the TREE: each family contributes
        1 + (k-1) * (1 - mean_within_family_|r|)
    i.e. perfectly-correlated siblings collapse to one vote.
    """
    names = sorted(series_by_model)
    by_fam: dict = {}
    for nm in names:
        by_fam.setdefault(family_of(nm), []).append(nm)

    total = 0.0
    for fam, members in by_fam.items():
        k = len(members)
        if k == 1:
            total += 1.0
            continue
        rs = []
        for i in range(k):
            for j in range(i + 1, k):
                rs.append(abs(pearson(series_by_model[members[i]],
                                      series_by_model[members[j]])))
        rbar = sum(rs) / len(rs) if rs else 0.0
        total += 1.0 + (k - 1) * (1.0 - rbar)
    return total


def n_empirical(series_by_model: dict) -> float:
    _, M = correlation_matrix(series_by_model)
    return participation_ratio(eigenvalues_sym(M))


def artificial_consensus(series_by_model: dict) -> dict:
    n_naive = float(len(series_by_model))
    ne = n_empirical(series_by_model)
    npy = n_phylo(series_by_model)
    return {
        "n_naive": n_naive,
        "n_empirical": ne,
        "n_phylo": npy,
        "artificial_consensus": n_naive - ne,
        "phylo_error": abs(npy - ne),
        "inflation_factor": n_naive / ne if ne > 0 else float("inf"),
    }
