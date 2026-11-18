"""Round 3: surrogate-calibrated rule, STATISTICAL replication (different random draws than the author's, so counts are
compared as rates, not cell for cell).
Spec as stated by the author (reply to the ask, item 5 + round-3 item 4b): n = 400; classes memory/white/drift/step;
windows 20/50/100/200; 100 series per class per window (seeds 0..99; white 10000+s); S = 100 phase-randomised
surrogates (rfft, amplitudes kept, DC and Nyquist phase 0, others uniform [0, 2 pi), irfft); observed Kendall taus of
rolling variance and rolling lag-1 autocorrelation; per-tau one-sided upper p = (1 + #(tau_surr >= tau_obs)) / (S + 1);
flag iff both p <= 0.05.
Numpy fast path for rolling statistics and tau; first checked against the module's own functions on 20 series.
Run: FORMULA_AUDIT_DIR=/path/to/formula-audit python3 replicate_surrogate.py [--check-only]"""
import os, sys, random
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.environ.get("FORMULA_AUDIT_DIR", "formula-audit"))
from glyph import precursor as P
import replicate_x0zero as R

N, S, ALPHA = 400, 100, 0.05
WINS = (20, 50, 100, 200)
KINDS = ("memory", "white", "drift", "step")
KOFF = {"memory": 1, "white": 2, "drift": 3, "step": 4}


def roll_stats(X, w):
    """X shape (m, n) -> rolling variance and lag-1 autocorr, each shape (m, n-w+1)."""
    V = np.lib.stride_tricks.sliding_window_view(X, w, axis=1)          # (m, k, w)
    mu = V.mean(axis=2, keepdims=True)
    D = V - mu
    den = (D ** 2).sum(axis=2)
    var = den / w
    num = (D[:, :, :-1] * D[:, :, 1:]).sum(axis=2)
    ac = np.where(den == 0, 0.0, num / np.where(den == 0, 1.0, den))
    return var, ac


def tau_rows(Y):
    """Kendall tau against index for each row of Y (m, k); NaN where all ties."""
    d = Y[:, None, :] - Y[:, :, None]                                   # d[i,j] = y_j - y_i
    iu = np.triu(np.ones((Y.shape[1], Y.shape[1]), dtype=bool), 1)
    s = np.sign(d)[:, iu]
    conc = (s > 0).sum(axis=1); disc = (s < 0).sum(axis=1); tot = conc + disc
    return np.where(tot == 0, np.nan, (conc - disc) / np.where(tot == 0, 1, tot))


def taus(X, w):
    var, ac = roll_stats(X, w)
    return tau_rows(var), tau_rows(ac)


def surrogates(x, rng):
    F = np.fft.rfft(x); amp = np.abs(F)
    ph = rng.uniform(0, 2 * np.pi, size=(S, F.shape[0]))
    ph[:, 0] = 0.0
    if len(x) % 2 == 0: ph[:, -1] = 0.0
    return np.fft.irfft(amp * np.exp(1j * ph), n=len(x), axis=1)


def flag(x, w, rng):
    tv, ta = taus(np.vstack([x[None, :], surrogates(x, rng)]), w)
    if np.isnan(tv[0]) or np.isnan(ta[0]): return False
    pv = (1 + np.sum(tv[1:] >= tv[0])) / (S + 1); pa = (1 + np.sum(ta[1:] >= ta[0])) / (S + 1)
    return bool(pv <= ALPHA and pa <= ALPHA)


def make(kind, s):
    if kind == "memory": return np.array(R.series("memory", s, N))
    if kind == "white": return np.array(R.series("white", s + 10000, N))
    r = random.Random(s)
    if kind == "drift": return np.array([0.02 * t + r.gauss(0, 1) for t in range(N)])
    return np.array([(3.0 if t >= N // 2 else 0.0) + r.gauss(0, 1) for t in range(N)])


def job(a):
    kind, w, s = a
    return a, flag(make(kind, s), w, np.random.default_rng(1000003 * s + 17 * w + KOFF[kind]))


def check():
    bad = 0
    for s in range(20):
        x = make(("memory", "white")[s % 2], s)
        for w in (20, 100):
            tv, ta = taus(x[None, :], w)
            mv = P.kendall_tau(P.rolling(list(x), w, P.variance)); ma = P.kendall_tau(P.rolling(list(x), w, P.lag1_autocorr))
            if abs(tv[0] - mv) > 1e-9 or abs(ta[0] - ma) > 1e-9: bad += 1
    print("fast path vs module: %d mismatches in 40 comparisons" % bad)
    return bad


if __name__ == "__main__":
    bad = check()
    if bad or "--check-only" in sys.argv: sys.exit(1 if bad else 0)
    jobs = [(k, w, s) for k in KINDS for w in WINS for s in range(100)]
    with Pool() as p: res = p.map(job, jobs, chunksize=4)
    tab = {}
    for (k, w, s), f in res: tab[(k, w)] = tab.get((k, w), 0) + int(f)
    print("surrogate-calibrated flags out of 100 (n=400, S=100, alpha=0.05)")
    print("%-7s" % "", *["w=%-4d" % w for w in WINS])
    for k in KINDS: print("%-7s" % k, *["%-6d" % tab[(k, w)] for w in WINS])
