"""run_1: meander toy base, seeds, slot-1 test, ablations, planted leak. stdlib only.

    python3 runs/run_1.py          # reproduces samples/run_1.sample.txt (about 3 minutes)

Every number is DERIVED (recomputed here) from model/meander.py. Nothing is OBSERVED.
Steady-state statistics are read after BURN steps; the burn length is a [CHOICE].
"""
import os, statistics as st, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from model import meander, l0_audit

STEPS, BURN, EVERY = 6000, 2000, 100
BASE = dict(E=0.3, steps=STEPS)


def q(xs, p):
    xs = sorted(xs)
    i = (len(xs) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def stats(r):
    h = [x for x in r["history"] if x["step"] >= BURN]
    lw = [x["lam_W"] for x in h if x["lam_W"] is not None]
    si = [x["sinuosity"] for x in h]
    c0 = next(x["cutoffs"] for x in r["history"] if x["step"] >= BURN)
    rate = (r["cutoffs"] - c0) / (STEPS - BURN) * 1000
    return dict(lw_med=st.median(lw) if lw else None, lw_p25=q(lw, .25) if lw else None,
                lw_p75=q(lw, .75) if lw else None, lw_n=len(lw), sin_med=st.median(si),
                sin_p25=q(si, .25), sin_p75=q(si, .75), cut_rate=rate,
                store_end=r["ledger"]["store"], point_bar=r["ledger"]["point_bar"],
                bank=r["ledger"]["bank_input"])


CASES = [
    ("base s0", {}, 0), ("base s1", {}, 1), ("base s2", {}, 2),
    ("H deeper  aspect 10", dict(aspect=10.0), 0),
    ("H shallower aspect 40", dict(aspect=40.0), 0),
    ("Cf 0.005", dict(Cf=0.005), 0),
    ("Cf 0.02", dict(Cf=0.02), 0),
    ("bank strong E 0.15", dict(E=0.15), 0),
    ("bank weak E 0.6", dict(E=0.6), 0),
    ("veg 0.5", dict(veg=0.5), 0),
    ("veg 1.0", dict(veg=1.0), 0),
    ("supply 0.2", dict(supply=0.2), 0),
    ("supply 2.0", dict(supply=2.0), 0),
    ("planted leak 0.05", dict(leak=0.05), 0),
]


def main():
    print("run_1  meander toy  (DERIVED; recomputed: python3 runs/run_1.py)")
    print(f"steps {STEPS}  burn {BURN} [CHOICE]  record every {EVERY}  base params: model/meander.py DEFAULTS + {BASE}")
    print()
    rows, audits = [], {}
    for name, extra, seed in CASES:
        r = meander.run(dict(BASE, **extra), seed=seed, record_every=EVERY)
        s = stats(r)
        a = l0_audit.audit(r)
        audits[name] = (a, r)
        rows.append((name, s, a, r))
    print("case                    lam/W med  p25..p75     sinuosity med  p25..p75    cutoffs/1k  sed     sed misclosure  bed store end")
    for name, s, a, r in rows:
        lw = f"{s['lw_med']:6.2f}  {s['lw_p25']:5.2f}..{s['lw_p75']:<5.2f}" if s["lw_med"] else "  void              "
        print(f"{name:23s} {lw}   {s['sin_med']:5.2f}  {s['sin_p25']:4.2f}..{s['sin_p75']:<5.2f}   {s['cut_rate']:6.2f}   "
              f"{a['sediment']['verdict']:6s} {a['sediment']['misclosure']:+.3e}   {s['store_end']:9.3f}")
    print()
    print("decay length H/(2 Cf) in widths, per case (the model's built-in length scale):")
    for name, s, a, r in rows:
        print(f"  {name:23s} H {r['H']:.4f}  alpha {r['alpha']:.3f}  1/alpha {1 / r['alpha']:.2f} W")
    print()
    print("L0 audit, base s0:")
    print(l0_audit.report(audits["base s0"][0]))
    print()
    print("L0 audit, planted leak:")
    print(l0_audit.report(audits["planted leak 0.05"][0]))
    print(f"  hidden leak removed: {audits['planted leak 0.05'][1]['ledger']['leak_hidden']:.3f}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: runs/run_1.py has no selftest; run python3 tests/test_meander.py")
        sys.exit(2)
    main()
