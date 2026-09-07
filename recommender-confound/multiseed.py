"""WORK_ORDER_02 task 1 -- dense multi-seed. Does canonicality touch the
TRUE fabrication rate? For N seeds, model held fixed exactly as seed 1,
run both densities at both canonicality levels and take
  delta_true = true(low) - true(high)
per seed. Report mean, sd, and a 95% CI on delta for the dense row and
the sparse row. Two designs, both printed:
  independent   each corner draws its own stream, as grid() does (the
                design that produced the seed-1 observation)
  paired        one model stream shared by low and high, rendering on a
                separate stream; a nonzero delta here would be structural
verdict  |mean delta| <= 2 SE  -> delta ~ 0 within noise: factorization holds
         otherwise             -> CROSS-TERM between h(canonicality) and g:
                                   the sign of the mean names the direction
Also printed: whether the seed-1 sparse delta (0.002) and dense delta
(0.020) sit inside their own noise bands.

Command: python3 multiseed.py [--seeds 30] [--queries 50] [--json]
         python3 multiseed.py --selftest
"""
import json
import math
import random
import sys

import synthetic_catalog as sc

SEED1 = {"dense": 0.020, "sparse": 0.002}   # the observation under test, from the seed-1 sample


def stats(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)) if n > 1 else 0.0
    se = sd / math.sqrt(n)
    return {"n": n, "mean": round(m, 5), "sd": round(sd, 5), "se": round(se, 5), "ci95": [round(m - 1.96 * se, 5), round(m + 1.96 * se, 5)]}


def run(seeds=30, queries=50, n=10):
    out = {"seeds": seeds, "queries": queries, "model": sc.MODEL, "rows": {}}
    for dens in ("dense", "sparse"):
        ind, pair = [], []
        for s in range(1, seeds + 1):
            g = sc.grid(s, n, queries, matchers=("exact",))
            ind.append(g["corners"]["%s/low" % dens]["true_fabrication_rate"] - g["corners"]["%s/high" % dens]["true_fabrication_rate"])
            t = {}
            for canon in ("low", "high"):
                t[canon] = sc.corner(random.Random(s), dens, canon, n, queries, ("exact",), sc.MODEL, render_rng=random.Random(10 ** 6 + s))["true_fabrication_rate"]
            pair.append(t["low"] - t["high"])
        si, sp = stats(ind), stats(pair)
        within = abs(si["mean"]) <= 2 * si["se"]
        band = 2 * si["sd"]
        out["rows"][dens] = {"independent": si, "paired": sp,
                             "verdict": ("delta ~ 0 within noise: factorization holds" if within else
                                         "CROSS-TERM: h(canonicality) x g couples, sign %s" % ("+" if si["mean"] > 0 else "-")),
                             "seed1_delta": SEED1[dens], "noise_band_2sd": round(band, 5),
                             "seed1_inside_band": abs(SEED1[dens]) <= band}
    d, s_ = out["rows"]["dense"], out["rows"]["sparse"]
    out["closing"] = ("dense delta was never anomalous; closes with no cross-term" if d["seed1_inside_band"] and s_["seed1_inside_band"]
                      else "a seed-1 delta sits outside its band; read the row verdicts")
    out["paired_note"] = "paired delta is exactly 0 on every seed: rendering cannot reach the true rate by construction" \
        if all(abs(x) < 1e-12 for x in [out["rows"][r]["paired"]["mean"] for r in out["rows"]]) else "paired delta nonzero: structural"
    return out


def render(o):
    L = ["seeds %d  queries %d  model %s" % (o["seeds"], o["queries"], o["model"])]
    for dens, r in o["rows"].items():
        L += ["%s  independent: mean %+.4f  sd %.4f  se %.4f  ci95 %s" % (dens, r["independent"]["mean"], r["independent"]["sd"], r["independent"]["se"], r["independent"]["ci95"]),
              "%s  paired:      mean %+.4f  sd %.4f" % (dens, r["paired"]["mean"], r["paired"]["sd"]),
              "%s  verdict: %s" % (dens, r["verdict"]),
              "%s  seed-1 delta %+.3f inside 2sd band %.4f: %s" % (dens, r["seed1_delta"], r["noise_band_2sd"], r["seed1_inside_band"])]
    L += [o["closing"], o["paired_note"]]
    return "\n".join(L)


def selftest():
    o = run(seeds=8, queries=20)
    for r in o["rows"].values():
        assert r["paired"]["mean"] == 0.0 and r["paired"]["sd"] == 0.0
        assert r["independent"]["n"] == 8
    assert o["rows"]["dense"]["independent"]["sd"] > o["rows"]["sparse"]["independent"]["sd"]  # sparse variance is bounded by 3 free items
    assert run(seeds=8, queries=20) == o
    print("multiseed selftest: 4 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if "--help" in argv:
        print(__doc__); return 2
    seeds = int(argv[argv.index("--seeds") + 1]) if "--seeds" in argv else 30
    q = int(argv[argv.index("--queries") + 1]) if "--queries" in argv else 50
    o = run(seeds, q)
    print(json.dumps(o, indent=1, sort_keys=True) if "--json" in argv else render(o))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
