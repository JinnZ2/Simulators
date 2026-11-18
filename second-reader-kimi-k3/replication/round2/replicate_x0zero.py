"""Round 2: start value x_0 = 0.0, as stated in the reply to the ask. Otherwise the same.
Replication of the RAW fixed-limit table in Kimi K3's one-page note (Pasted_content_77).
Run: FORMULA_AUDIT_DIR=/path/to/formula-audit python3 replicate_raw_table.py
Uses glyph/precursor.py's own kendall_tau / rolling / variance / lag1_autocorr (formula-audit main, file sha256
d1eab08effbc...). RNG is Python's random.Random (Kimi's is not stated; seeds therefore do not give the same series).
Constructions as declared in the note: memory, drift, step, white; n = 400; seeds 0..199 (white: 10000..10199).
Flag per the module: PRECURSOR iff both Kendall taus >= limit. Surrogate calibration is NOT replicated here.
"""
import json
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("FORMULA_AUDIT_DIR", "formula-audit"))
from glyph import precursor as P  # noqa: E402

N = 400
WS = (20, 50, 100, 200)
LIMS = (0.3, 0.5)
SEEDS = 200


def series(kind, seed, n=N):
    r = random.Random(seed)
    if kind == "memory":
        x, out = 0.0, []
        for t in range(n):
            rho = 0.05 + 0.90 * t / (n - 1)
            x = rho * x + r.gauss(0, 1)
            out.append(x)
        return out
    if kind == "drift":
        return [0.02 * t + r.gauss(0, 1) for t in range(n)]
    if kind == "step":
        return [(3.0 if t >= n // 2 else 0.0) + r.gauss(0, 1) for t in range(n)]
    return [r.gauss(0, 1) for _ in range(n)]


def taus(job):
    kind, seed = job
    xs = series(kind, seed + (10000 if kind == "white" else 0))
    out = {}
    for w in WS:
        out[w] = (P.kendall_tau(P.rolling(xs, w, P.variance)), P.kendall_tau(P.rolling(xs, w, P.lag1_autocorr)))
    return kind, seed, out


if __name__ == "__main__":
    jobs = [(k, s) for k in ("memory", "drift", "step", "white") for s in range(SEEDS)]
    with Pool() as pool:
        res = pool.map(taus, jobs, chunksize=4)
    table = {}
    for kind, seed, out in res:
        for w, (tv, ta) in out.items():
            for lim in LIMS:
                hit = tv is not None and ta is not None and tv >= lim and ta >= lim
                table.setdefault((kind, w, lim), 0)
                table[(kind, w, lim)] += int(hit)
    print("rates out of", SEEDS, "(n=%d, own RNG)" % N)
    for lim in LIMS:
        print("limit", lim)
        print("  w   memory  drift  step  white")
        for w in WS:
            print("  %-3d %6d %6d %5d %5d" % (w, *(table[(k, w, lim)] for k in ("memory", "drift", "step", "white"))))
    json.dump({"n": N, "seeds": SEEDS, "rng": "random.Random", "cells": {"%s|w%d|lim%s" % k: v for k, v in table.items()}},
              open(os.path.join(HERE, "replicate_raw_table_x0zero.json"), "w"), indent=1)
