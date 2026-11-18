"""Replication of the raw-rule variants in the third Kimi note (Pasted_content_78): baseline, logvar, tail50, weighted, vote.
NOT run: cusum, rvh, calibrated variants. Series: Python random, start 0.0, as in replicate_raw_table (x0zero).
Reading choices where the note is silent (all declared): weighted uses 0-based indices i<j with weight (i+j)/2;
tail50 uses all points when fewer than 50; a variant flags iff both taus >= limit. vote: >=3 of 5 windows flag.
Run: FORMULA_AUDIT_DIR=/path/to/formula-audit python3 replicate_variants.py
"""
import math, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.environ.get("FORMULA_AUDIT_DIR", "formula-audit"))
from glyph import precursor as P
import replicate_x0zero as R
LIMS = (0.3, 0.5); VW = (15, 20, 25, 30, 40)
def wtau(xs):
    n = len(xs); num = den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            d = xs[j] - xs[i]
            if d != 0:
                w = (i + j) / 2.0; den += w; num += w if d > 0 else -w
    return None if den == 0 else num / den
def both(tv, ta, lim): return tv is not None and ta is not None and tv >= lim and ta >= lim
def job(a):
    kind, seed, n = a
    xs = R.series(kind, seed + (10000 if kind == "white" else 0), n)
    out = {}
    rv = P.rolling(xs, 20, P.variance); ra = P.rolling(xs, 20, P.lag1_autocorr)
    tv, ta = P.kendall_tau(rv), P.kendall_tau(ra)
    lv = [math.log(v) for v in rv]; tl = P.kendall_tau(lv)
    t5v, t5a = P.kendall_tau(rv[-50:]), P.kendall_tau(ra[-50:])
    wv, wa = wtau(rv), wtau(ra)
    votes = {}
    for w in VW:
        a_, b_ = P.kendall_tau(P.rolling(xs, w, P.variance)), P.kendall_tau(P.rolling(xs, w, P.lag1_autocorr))
        votes[w] = (a_, b_)
    for lim in LIMS:
        out[lim] = {"baseline": both(tv, ta, lim), "logvar": both(tl, ta, lim), "tail50": both(t5v, t5a, lim),
                    "weighted": both(wv, wa, lim), "vote": sum(both(a_, b_, lim) for a_, b_ in votes.values()) >= 3}
    return kind, n, out
if __name__ == "__main__":
    jobs = [(k, s, n) for k in ("memory", "white") for n in (60, 200, 400) for s in range(200)] + \
           [(k, s, 400) for k in ("drift", "step") for s in range(200)]
    with Pool() as p: res = p.map(job, jobs, chunksize=4)
    tab = {}
    for kind, n, out in res:
        for lim, d in out.items():
            for v, hit in d.items(): tab[(lim, v, kind, n)] = tab.get((lim, v, kind, n), 0) + int(hit)
    for lim in LIMS:
        print("limit", lim, " catches n=60/200/400 | white FA n=60/200/400 | drift, step leaks n=400")
        for v in ("baseline", "tail50", "weighted", "logvar", "vote"):
            c = [tab[(lim, v, "memory", n)] for n in (60, 200, 400)]; f = [tab[(lim, v, "white", n)] for n in (60, 200, 400)]
            print("  %-9s %3d %3d %3d | %2d %2d %2d | %3d %3d" % (v, *c, *f, tab[(lim, v, "drift", 400)], tab[(lim, v, "step", 400)]))
