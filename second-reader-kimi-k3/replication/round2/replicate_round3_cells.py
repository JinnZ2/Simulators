"""Round 3: n=200 grid (w 20/40/60/100, limits .3/.5) and the Python side of the six JS-pair cells, 200 seeds,
construction as stated (planted: Random(s), x0=0.0, coef 0.05+0.9 t/(n-1); white: Random(10000+s)).
Flag rule = module's: both Kendall taus (rolling variance, rolling lag-1 autocorr) >= limit.
Run: FORMULA_AUDIT_DIR=/path/to/formula-audit python3 replicate_round3_cells.py"""
import os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.environ.get("FORMULA_AUDIT_DIR", "formula-audit"))
from glyph import precursor as P
import replicate_x0zero as R
def job(a):
    kind, s, n, w = a
    xs = R.series(kind, s + (10000 if kind == "white" else 0), n)
    tv = P.kendall_tau(P.rolling(xs, w, P.variance)); ta = P.kendall_tau(P.rolling(xs, w, P.lag1_autocorr))
    return a, [(lim, tv is not None and ta is not None and tv >= lim and ta >= lim) for lim in (0.3, 0.5)]
if __name__ == "__main__":
    cells = [(200, w) for w in (20, 40, 60, 100)] + [(60, 20), (70, 50), (150, 100), (400, 50), (200, 20)]
    cells = list(dict.fromkeys(cells))
    jobs = [(k, s, n, w) for (n, w) in cells for k in ("memory", "white") for s in range(200)]
    with Pool() as p: res = p.map(job, jobs, chunksize=8)
    tab = {}
    for (k, s, n, w), fl in res:
        for lim, hit in fl: tab[(n, w, lim, k)] = tab.get((n, w, lim, k), 0) + int(hit)
    for (n, w) in cells:
        for lim in (0.3, 0.5):
            print("n=%d w=%d limit %.1f: planted %d/200  white %d/200" % (n, w, lim, tab[(n, w, lim, "memory")], tab[(n, w, lim, "white")]))
