"""run_2: is lam/W in the toy set by width-scaled NUMERICS (cutoff neck, node spacing)
rather than by the decay length H/(2 Cf)? Slot-1 probe on the toy. stdlib only.

    python3 runs/run_2.py          # reproduces samples/run_2.sample.txt (about 4 minutes)
"""
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from model import meander, l0_audit
sys.path.insert(0, os.path.join(HERE, "runs"))
import run_1

CASES = [
    ("base s0 (run_1)", dict(E=0.3, steps=6000), 0),
    ("neck 2 W", dict(E=0.3, steps=6000, neck=2.0, cut_gap=24), 0),
    ("neck 0.5 W", dict(E=0.3, steps=6000, neck=0.5, cut_gap=6), 0),
    ("ds 0.25 W", dict(E=0.3, steps=6000, ds=0.25, cut_gap=24, dt=0.2), 0),
    ("aspect 10, 15000 steps", dict(E=0.3, steps=15000, aspect=10.0), 0),
]

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: runs/run_2.py has no selftest; run python3 tests/test_meander.py")
        sys.exit(2)
    print("run_2  slot-1 probe on the toy  (DERIVED; recomputed: python3 runs/run_2.py)")
    print("case                     lam/W med  p25..p75     sinuosity med  cutoffs/1k  sed verdict")
    for name, p, seed in CASES:
        run_1.STEPS = p["steps"]
        r = meander.run(p, seed=seed, record_every=100)
        s = run_1.stats(r)
        a = l0_audit.audit(r)
        lw = f"{s['lw_med']:6.2f}  {s['lw_p25']:5.2f}..{s['lw_p75']:<5.2f}" if s["lw_med"] else "  void              "
        print(f"{name:24s} {lw}   {s['sin_med']:5.2f}        {s['cut_rate']:6.2f}   {a['sediment']['verdict']}")
