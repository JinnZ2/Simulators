"""Toolkit: residual_regression. Tool #5 of the staged build (work order 2026-11-11). numpy.

Entry: ledger/toolkit/residual_regression.yaml. Gate: tests/test_toolkit.py.

Measurement artifact or biology? Regress a residual on METHOD fields (dt, step count,
run length, a bookkeeping counter's own error) and on BIOLOGY fields (parameters,
state the model computes), and ask which block explains it.

  fit(rows, residual, method, biology)
    R2_M, R2_B, R2_MB         ordinary least squares with an intercept
    dM = R2_MB - R2_B         what the method block adds beyond biology
    dB = R2_MB - R2_M         what the biology block adds beyond method
    p_M, p_B                  permutation p of each increment: rows of the tested block
                              shuffled, the other block held          [CHOICE: N_PERM 500]
    collinear                 a method column predicted from the biology block (or the
                              reverse) at R2 >= COLLINEAR: the blocks cannot be told apart

  verdict
    NOT_SEPARABLE    collinear: any attribution would be the regression's choice
    METHOD_ARTIFACT  dM significant and material, dB not
    BIOLOGY          dB significant and material, dM not
    MIXED            both
    UNEXPLAINED      neither
  significant = p < ALPHA, material = increment >= MIN_DR2      [CHOICE: ALPHA 0.01, MIN_DR2 0.10]

Which field is "method" and which is "biology" is declared by the caller, never
inferred; a mis-declared field moves the verdict and the declaration is printed.
"""
import os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
import numpy as np

N_PERM, ALPHA, MIN_DR2, COLLINEAR = 500, 0.01, 0.10, 0.95
CHOICES = dict(N_PERM=N_PERM, ALPHA=ALPHA, MIN_DR2=MIN_DR2, COLLINEAR=COLLINEAR)


def r2(X, y):
    """Columns are standardised first. Found by running (run_18): unscaled, a residual-sized
    column (1e-11) beside a step count (1e4) was rank-truncated away by lstsq and the fit
    read UNEXPLAINED while that column alone gave R2 1.0. Constant columns are dropped."""
    if X.shape[1] == 0:
        return 0.0
    sd = X.std(axis=0)
    keep = sd > 0
    if not keep.any():
        return 0.0
    Z = (X[:, keep] - X[:, keep].mean(axis=0)) / sd[keep]
    y = (y - y.mean()) / (y.std() or 1.0)
    A = np.column_stack([np.ones(len(y)), Z])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    ss = float(((y - y.mean()) ** 2).sum())
    if ss == 0.0:
        return 0.0
    return 1.0 - float(((y - A @ coef) ** 2).sum()) / ss


def _matrix(rows, names):
    return np.array([[float(r[n]) for n in names] for r in rows]) if names else np.zeros((len(rows), 0))


def collinear(XM, XB):
    worst = 0.0
    for X, Y in ((XB, XM), (XM, XB)):
        if X.shape[1] == 0:
            continue
        for j in range(Y.shape[1]):
            if np.ptp(Y[:, j]) > 0:
                worst = max(worst, r2(X, Y[:, j]))
    return worst


def fit(rows, residual, method, biology, seed=0, n_perm=N_PERM):
    y = np.array([float(r[residual]) for r in rows])
    XM, XB = _matrix(rows, method), _matrix(rows, biology)
    both = np.column_stack([XM, XB])
    R2M, R2B, R2MB = r2(XM, y), r2(XB, y), r2(both, y)
    dM, dB = R2MB - R2B, R2MB - R2M
    rng = np.random.default_rng(seed)

    def perm_p(block, other, d):
        hits = 0
        for _ in range(n_perm):
            P = block[rng.permutation(len(y))]
            hits += (r2(np.column_stack([P, other]), y) - r2(other, y)) >= d - 1e-15
        return (hits + 1) / (n_perm + 1)

    pM = perm_p(XM, XB, dM) if XM.shape[1] else 1.0
    pB = perm_p(XB, XM, dB) if XB.shape[1] else 1.0
    col = collinear(XM, XB)
    return dict(R2_M=R2M, R2_B=R2B, R2_MB=R2MB, dM=dM, dB=dB, p_M=pM, p_B=pB, collinear_r2=col,
                verdict=verdict(dM, dB, pM, pB, col), method=list(method), biology=list(biology), n=len(rows))


def verdict(dM, dB, pM, pB, col):
    if col >= COLLINEAR:
        return "NOT_SEPARABLE"
    m = pM < ALPHA and dM >= MIN_DR2
    b = pB < ALPHA and dB >= MIN_DR2
    return "MIXED" if m and b else "METHOD_ARTIFACT" if m else "BIOLOGY" if b else "UNEXPLAINED"


def render(f):
    return (f"n {f['n']}  method {f['method']}  biology {f['biology']}\n"
            f"  R2 method {f['R2_M']:.3f}  biology {f['R2_B']:.3f}  both {f['R2_MB']:.3f}  "
            f"dM {f['dM']:.3f} (p {f['p_M']:.3f})  dB {f['dB']:.3f} (p {f['p_B']:.3f})  collinear R2 {f['collinear_r2']:.3f}\n"
            f"  verdict {f['verdict']}")


# ---------------------------------------------------------------- gate: planted cases + null harness
def _rows(rng, n, kind, noise=0.3):
    out = []
    for _ in range(n):
        m, b = rng.uniform(0, 1), rng.uniform(0, 1)
        y = {"method": 3 * m, "biology": 3 * b, "both": 3 * m + 3 * b, "none": 0.0}[kind] + rng.gauss(0, noise)
        out.append(dict(m=m, b=b, y=y))
    return out


def _col_rows(rng, n):
    out = []
    for _ in range(n):
        b = rng.uniform(0, 1)
        out.append(dict(m=2 * b + 0.001 * rng.gauss(0, 1), b=b, y=3 * b + rng.gauss(0, 0.3)))
    return out


def known_cases():
    import random
    r = random.Random(5)
    V = lambda rows: fit(rows, "y", ["m"], ["b"], n_perm=200)["verdict"]
    return [
        ("residual driven by the method field: METHOD_ARTIFACT", "METHOD_ARTIFACT", lambda: V(_rows(r, 40, "method"))),
        ("residual driven by the biology field: BIOLOGY", "BIOLOGY", lambda: V(_rows(r, 40, "biology"))),
        ("both drive it: MIXED", "MIXED", lambda: V(_rows(r, 40, "both"))),
        ("pure noise: UNEXPLAINED (silent)", "UNEXPLAINED", lambda: V(_rows(r, 40, "none"))),
        ("method column is a copy of the biology column: NOT_SEPARABLE", "NOT_SEPARABLE", lambda: V(_col_rows(r, 40))),
        ("a residual-scale method column beside a 1e4-scale one still reads METHOD_ARTIFACT", "METHOD_ARTIFACT",
         lambda: fit([dict(m=x["m"] * 1e-11, big=1e4 * r.uniform(0, 1), b=x["b"], y=x["y"] * 1e-11) for x in _rows(r, 40, "method")],
                     "y", ["big", "m"], ["b"], n_perm=200)["verdict"]),
        ("r2 of an exact line is 1", 1.0, lambda: round(r2(np.array([[0.0], [1.0], [2.0]]), np.array([1.0, 3.0, 5.0])), 12)),
    ]


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())
    det = lambda rows: fit(rows, "y", ["m"], ["b"], n_perm=150)["verdict"] in ("METHOD_ARTIFACT", "MIXED")
    legs = dict(method_explains=G.null_harness_seeds(det, lambda r: _rows(r, 30, "biology"), lambda r: _rows(r, 30, "method"),
                                                     n=60, seeds=seeds))
    return G.combine(known, legs)


if __name__ == "__main__":
    print("refused: library. Gate: python3 tests/test_toolkit.py ; run: runs/run_18.py")
    raise SystemExit(2)
