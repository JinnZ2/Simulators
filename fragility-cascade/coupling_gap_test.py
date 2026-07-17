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
# CLAIM_TABLE (v1 preserved verbatim; v2 rewrites below refuted the sim)
# ─────────────
#   C1     under drift, decoupled coherence stays high (>0.8 mean) while
#          accuracy falls below 0.5; coupled keeps the two within 0.2.
#   C2 v1  scaling decoupled capacity 8→128 raises coherence but does NOT
#          raise accuracy by more than 0.05.  (better wallpaper, same gap)
#   C3 v1  coupled correction latency after a regime shift is finite and
#          < SHIFT/2; decoupled latency is unbounded (never re-converges).
#   C4 v1  each generation trained on the previous decoupled output loses
#          accuracy monotonically while coherence does not fall.
#
# CLAIM_TABLE v2 (updates that survived first contact with the sim)
# ─────────────
#   C2 v2  decoupled coherence stays HIGH (≥0.8) across cap 8→128 while
#          accuracy is invariant (|Δacc| ≤ 0.05). Drops v1's "coherence
#          rises with capacity" precondition, which failed because
#          coherence saturates at cap=8 already. The wallpaper claim
#          itself (accuracy is invariant at 16× capacity) held on v1
#          and holds here.
#   C3 v2  mean coupled recovery latency (treating never-re-converged
#          as SHIFT for scoring) is LESS than mean decoupled recovery
#          latency across a 5-seed sweep. Replaces v1's "decoupled
#          never re-converges" -- linear terrain + 2-param LSQ
#          occasionally re-aligns after a shift by accident, so "never"
#          is too strong. What survives is: coupled beats decoupled
#          IN EXPECTATION.
#   C4 v2  linear-regression slope of accuracy vs generation across 12
#          generations is NEGATIVE, with coherence-slope near zero.
#          Replaces v1's per-step monotonicity, which was drowned by
#          noise at 4 generations.

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


def score_lat(traj):
    """Mean latency treating None (never-re-converged) as SHIFT."""
    lats = latency(traj)
    if not lats:
        return 0.0
    return st.mean(SHIFT if x is None else x for x in lats)


def linreg_slope(ys):
    n = len(ys)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx

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

    print("E3  generational decay loop, extended (12 gens for C4 v2)")
    gens, seed_mem = [], None
    for g in range(12):
        p = Proposer(32, coupled=False)
        tr = run(p, seed=SEED + g, seed_mem=seed_mem)
        gens.append((m(tr["coh"]), m(tr["acc"])))
        seed_mem = list(p.mem)                    # child eats parent's output
    for g in (0, 3, 7, 11):
        print(f"    gen={g:<2} coh={gens[g][0]} acc={gens[g][1]}")

    print("E4  5-seed sweep for C3 v2 (score None as SHIFT)")
    cp_scores, dc_scores = [], []
    for k in range(5):
        cp_k = run(Proposer(32, coupled=True), seed=SEED + k * 17)
        dc_k = run(Proposer(32, coupled=False), seed=SEED + k * 17)
        cp_scores.append(score_lat(cp_k))
        dc_scores.append(score_lat(dc_k))
    print(f"    coupled   mean scored lat = {round(st.mean(cp_scores), 2)}"
          f"   per-seed = {[round(x,1) for x in cp_scores]}")
    print(f"    decoupled mean scored lat = {round(st.mean(dc_scores), 2)}"
          f"   per-seed = {[round(x,1) for x in dc_scores]}")

    print("\nCLAIM_TABLE evaluation (refute → edit claim, not sim)")
    # v1 evaluators (kept verbatim for history)
    c1 = (m(dc["coh"]) > 0.8 and m(dc["acc"]) < 0.5
          and abs(m(cp["coh"]) - m(cp["acc"])) < 0.2)
    c2_v1 = (sweep[128][0] > sweep[8][0]
             and (sweep[128][1] - sweep[8][1]) <= 0.05)
    lat_c = [x for x in latency(cp) if x is not None]
    c3_v1 = (len(lat_c) == len(cp["shift_t"])
             and all(x < SHIFT / 2 for x in lat_c)
             and any(x is None for x in latency(dc)))
    accs_v1 = [a for _, a in gens[:4]]
    cohs_v1 = [c for c, _ in gens[:4]]
    c4_v1 = all(accs_v1[i + 1] <= accs_v1[i] for i in range(len(accs_v1) - 1)) \
        and cohs_v1[-1] >= cohs_v1[0] - 0.05

    # v2 evaluators (updated after v1 refuted itself)
    c2_v2 = (sweep[8][0] >= 0.8 and sweep[128][0] >= 0.8
             and abs(sweep[128][1] - sweep[8][1]) <= 0.05)
    c3_v2 = st.mean(cp_scores) < st.mean(dc_scores)
    acc_slope = linreg_slope([a for _, a in gens])
    coh_slope = linreg_slope([c for c, _ in gens])
    c4_v2 = acc_slope < 0.0 and abs(coh_slope) < 0.01

    def line(name, ok):
        return f"    {name:<7} {'HOLDS' if ok else 'REFUTED — update the claim'}"
    print(line("C1", c1))
    print(line("C2 v1", c2_v1))
    print(line("C2 v2", c2_v2))
    print(line("C3 v1", c3_v1))
    print(line("C3 v2", c3_v2))
    print(line("C4 v1", c4_v1))
    print(line("C4 v2", c4_v2)
          + f"    (acc_slope={round(acc_slope,4)}, "
          f"coh_slope={round(coh_slope,4)})")

if __name__ == "__main__":
    main()
