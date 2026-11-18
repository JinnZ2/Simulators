"""Run: FORMULA_AUDIT_DIR=/path/to/formula-audit python3 replicate_lengths.py
Series-length claims in Kimi's notes: memory class, limit 0.5, fixed absolute window; same constructions, n varied."""
import os
import sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.environ.get("FORMULA_AUDIT_DIR", "formula-audit"))
from glyph import precursor as P
import replicate_x0zero as R
def one(a):
    kind, seed, n, w = a
    xs = R.series(kind, seed + (10000 if kind == "white" else 0), n)
    tv = P.kendall_tau(P.rolling(xs, w, P.variance)); ta = P.kendall_tau(P.rolling(xs, w, P.lag1_autocorr))
    return (kind, n, w, tv is not None and ta is not None and tv >= 0.5 and ta >= 0.5)
if __name__ == "__main__":
    jobs = [(k, s, n, w) for k in ("memory", "white") for n in (60, 100, 200, 400) for w in (20, 50) for s in range(200) if w + 2 <= n]
    with Pool() as p: res = p.map(one, jobs, chunksize=8)
    import collections; c = collections.Counter((k, n, w) for k, n, w, h in res if h)
    print("limit 0.5, out of 200 (own series via random.Random)")
    for w in (20, 50):
        print("w=%d  memory by n:" % w, {n: c[("memory", n, w)] for n in (60, 100, 200, 400)}, " white FA:", {n: c[("white", n, w)] for n in (60, 100, 200, 400)})
    # matched half-series window at n=60 (w30) and n=200 (w100), limits 0.3 and 0.5, as in the first note
    def cell(n, w, lim):
        jobs2 = [(k, s, n, w) for k in ("memory", "white") for s in range(200)]
        out = {"memory": 0, "white": 0}
        for k, s, nn, ww in jobs2:
            xs = R.series(k, s + (10000 if k == "white" else 0), nn)
            tv = P.kendall_tau(P.rolling(xs, ww, P.variance)); ta = P.kendall_tau(P.rolling(xs, ww, P.lag1_autocorr))
            out[k] += int(tv is not None and ta is not None and tv >= lim and ta >= lim)
        return out
    for n, w in ((60, 30), (200, 100)):
        for lim in (0.5, 0.3):
            print("n=%d w=%d limit=%s ->" % (n, w, lim), cell(n, w, lim))
