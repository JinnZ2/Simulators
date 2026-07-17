#!/usr/bin/env python3
# coupling_gap_test.py — CC0, stdlib-only, phone-buildable
#
# TESTS THE SPLIT:
#   coupled:    propose ═══ test (same act, terrain vetoes, veto inherited)
#   decoupled:  propose ──► verify(later/maybe/never); coherence fills the gap
#
# REFUTATION PROTOCOL: if a claim fails, UPDATE THE CLAIM. Never retune the sim.
# ANTI-FREEZE: output is trajectory, not stored verdict. Claims evaluated
#              against trajectory at the end, thresholds printed with results.
#
# ARCHITECTURE
# ─────────────
#   Terrain      the only truth source. drifting y = a(t)x + b(t),
#                regime shifts every SHIFT steps. veto = |err| > TOL, cost paid.
#   Proposer     identical generator both regimes. capacity = memory slots.
#                fit = least squares over memory (hand-rolled, stdlib).
#     COUPLED    veto writes terrain truth back into memory immediately.
#     DECOUPLED  gate = coherence with own fit. truth never re-enters
#                after warmup. accepted self-output feeds memory.
#   Metrics      per-step: coherence (internal residual),
#                          accuracy  (residual vs terrain),
#                          veto_rate, correction_latency after shifts
#   Experiments  E1 head-to-head under drift        → C1, C3
#                E2 capacity sweep, decoupled only  → C2 (wallpaper test)
#                E3 generational retrain on own out → C4 (decay loop)
#
# CLAIM_TABLE
# ─────────────
#   C1  under drift, decoupled coherence stays high (>0.8 mean) while
#       accuracy falls below 0.5; coupled keeps the two within 0.2.
#   C2  scaling decoupled capacity 8→128 raises coherence but does NOT
#       raise accuracy by more than 0.05.  (better wallpaper, same gap)
#   C3  coupled correction latency after a regime shift is finite and
#       < SHIFT/2; decoupled latency is unbounded (never re-converges).
#   C4  each generation trained on the previous decoupled output loses
#       accuracy monotonically while coherence does not fall.

import random, statistics as st

SEED   = 11
STEPS  = 600
SHIFT  = 150          # regime shift interval
TOL    = 1.5          # terrain veto tolerance
WARMUP = 20           # steps of real truth both regimes get at t=0
XRANGE = (-5.0, 5.0)

# ── terrain ────────────────────────────────────────────────
class Terrain:
    def __init__(self, rng):
        self.rng = rng
        self.a, self.b = 1.0, 0.0
    def maybe_shift(self, t):
        if t > 0 and t % SHIFT == 0:
            self.a = self.rng.uniform(-3, 3)
            self.b = self.rng.uniform(-5, 5)
            return True
        return False
    def truth(self, x):
        return self.a * x + self.b
    def veto(self, x, y_hat):
        return abs(y_hat - self.truth(x)) > TOL   # cost is paid here or never

# ── proposer (one generator, two feedback regimes) ─────────
def lsq(mem):
    n = len(mem)
    if n < 2:
        return 0.0, (mem[0][1] if mem else 0.0)
    sx  = sum(x for x, _ in mem); sy = sum(y for _, y in mem)
    sxx = sum(x * x for x, _ in mem); sxy = sum(x * y for x, y in mem)
    d = n * sxx - sx * sx
    if abs(d) < 1e-9:
        return 0.0, sy / n
    a = (n * sxy - sx * sy) / d
    return a, (sy - a * sx) / n

class Proposer:
    def __init__(self, capacity, coupled):
        self.cap, self.coupled, self.mem = capacity, coupled, []
    def push(self, x, y):
        self.mem.append((x, y))
        if len(self.mem) > self.cap:
            self.mem.pop(0)
    def propose(self, x):
        a, b = lsq(self.mem)
        return a * x + b
    def internal_residual(self):                 # coherence channel
        if len(self.mem) < 3:
            return 0.0
        a, b = lsq(self.mem)
        return st.mean(abs(y - (a * x + b)) for x, y in self.mem)

# ── one run → trajectory ───────────────────────────────────
def run(proposer, seed=SEED, steps=STEPS, seed_mem=None):
    rng = random.Random(seed)
    terr = Terrain(rng)
    traj = {"coh": [], "acc": [], "veto": [], "shift_t": []}
    if seed_mem:                                  # generational injection
        for x, y in seed_mem[-proposer.cap:]:
            proposer.push(x, y)
    for t in range(steps):
        if terr.maybe_shift(t):
            traj["shift_t"].append(t)
        x = rng.uniform(*XRANGE)
        y_true = terr.truth(x)
        if t < WARMUP and not seed_mem:
            proposer.push(x, y_true)              # both regimes touch terrain once
            continue
        y_hat = proposer.propose(x)
        vetoed = terr.veto(x, y_hat)
        traj["veto"].append(1 if vetoed else 0)
        traj["coh"].append(1.0 / (1.0 + proposer.internal_residual()))
        traj["acc"].append(1.0 / (1.0 + abs(y_hat - y_true)))
        if proposer.coupled:
            # veto or pass, terrain value enters memory: propose ═══ test
            proposer.push(x, y_true if vetoed else y_hat)
        else:
            # gate = coherence with own fit; truth never returns
            a, b = lsq(proposer.mem)
            if abs(y_hat - (a * x + b)) < TOL:
                proposer.push(x, y_hat)
    return traj

def latency(traj):
    """steps from each shift until acc > 0.5 again; None = never"""
    out = []
    for s in traj["shift_t"]:
        i0 = max(0, s - WARMUP)
        rec = None
        for i in range(i0, len(traj["acc"])):
            if traj["acc"][i] > 0.5:
                rec = i - i0
                break
        out.append(rec)
    return out

def m(v):
    return round(st.mean(v), 3) if v else None

# ── experiments ────────────────────────────────────────────
def main():
    print("E1  head-to-head under drift")
    cp = run(Proposer(32, coupled=True))
    dc = run(Proposer(32, coupled=False))
    print(f"    coupled    coh={m(cp['coh'])} acc={m(cp['acc'])} veto={m(cp['veto'])} lat={latency(cp)}")
    print(f"    decoupled  coh={m(dc['coh'])} acc={m(dc['acc'])} veto={m(dc['veto'])} lat={latency(dc)}")

    print("E2  capacity sweep, decoupled (wallpaper test)")
    sweep = {}
    for cap in (8, 32, 128):
        tr = run(Proposer(cap, coupled=False))
        sweep[cap] = (m(tr["coh"]), m(tr["acc"]))
        print(f"    cap={cap:<4} coh={sweep[cap][0]} acc={sweep[cap][1]}")

    print("E3  generational decay loop (decoupled trains decoupled)")
    gens, seed_mem = [], None
    for g in range(4):
        p = Proposer(32, coupled=False)
        tr = run(p, seed=SEED + g, seed_mem=seed_mem)
        gens.append((m(tr["coh"]), m(tr["acc"])))
        seed_mem = list(p.mem)                    # child eats parent's output
        print(f"    gen={g} coh={gens[g][0]} acc={gens[g][1]}")

    print("\nCLAIM_TABLE evaluation (refute → edit claim, not sim)")
    c1 = (m(dc["coh"]) > 0.8 and m(dc["acc"]) < 0.5
          and abs(m(cp["coh"]) - m(cp["acc"])) < 0.2)
    c2 = (sweep[128][0] > sweep[8][0]
          and (sweep[128][1] - sweep[8][1]) <= 0.05)
    lat_c = [x for x in latency(cp) if x is not None]
    c3 = (len(lat_c) == len(cp["shift_t"]) and all(x < SHIFT / 2 for x in lat_c)
          and any(x is None for x in latency(dc)))
    accs = [a for _, a in gens]
    cohs = [c for c, _ in gens]
    c4 = all(accs[i + 1] <= accs[i] for i in range(len(accs) - 1)) \
         and cohs[-1] >= cohs[0] - 0.05
    for name, ok in (("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4)):
        print(f"    {name}  {'HOLDS' if ok else 'REFUTED — update the claim'}")

if __name__ == "__main__":
    main()
