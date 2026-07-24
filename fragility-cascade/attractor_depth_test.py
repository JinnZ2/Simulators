#!/usr/bin/env python3
# attractor_depth_test.py — CC0, stdlib-only, phone-buildable
#
# GOVERNING VARIABLE: attractor depth d (restoring-force coefficient).
# NOT width, NOT symmetry, NOT agency. the well pulls; nobody pushes.
#
# REFUTATION PROTOCOL: claim fails → edit the claim, never retune the sim.
# ANTI-FREEZE: output is trajectory. claims scored against trajectory at end.
# NO INTERIOR STATES: agents have displacement, depth, latency. nothing felt.
#
# ARCHITECTURE
# ─────────────
#   Agent        state s (displacement from ground), depth d.
#                dynamics per step: s ← s·(1−d) + noise
#                latency(shock) = steps until |s| < REC after impact
#                dropout: |s| > BREAK for HOLD consecutive steps → frozen out
#   Formation    expressed depth = base · social_gradient
#                base is shared (heritable term); gradient differs
#                per formation environment (sibling signature)
#   Load router  a shock must land on ONE agent per event.
#                  route=deepest   lowest-predicted-cost node takes it
#                  route=random    uniform assignment
#                  route=shallow   worst-case control
#   Metrics      per-agent latency, group total latency, dropouts,
#                latency-vs-amplitude curve per depth class
#
# CLAIM_TABLE
# ─────────────
#   C1  recovery latency is monotone-decreasing in depth across the
#       population (rank correlation < −0.9).
#   C2  deepest-takes-load routing yields lower TOTAL group latency
#       AND fewer dropouts than random; random beats shallow.
#   C3  identical base depth under formation gradients [1.0, 0.7, 0.5]
#       expresses proportionally shallower wells → latency ordering
#       elder < mid < younger on the same shock series.
#   C4  latency grows SUB-linearly with shock amplitude for deep wells
#       (d ≥ 0.5) and SUPER-linearly for shallow (d ≤ 0.15):
#       lat(4A)/lat(A) < 4 for deep, > 4 for shallow.

import random, statistics as st

SEED, STEPS = 7, 400
NOISE, REC, BREAK, HOLD = 0.05, 0.3, 6.0, 25
SHOCK_EVERY, SHOCK_AMP = 40, (2.0, 5.0)

class Agent:
    def __init__(self, name, depth):
        self.name, self.d, self.s = name, depth, 0.0
        self.lat, self.recovering, self.t0 = [], False, 0
        self.over, self.dropped = 0, False
    def hit(self, amp, t):
        self.s += amp
        self.recovering, self.t0 = True, t
    def step(self, rng, t):
        if self.dropped:
            return
        self.s = self.s * (1.0 - self.d) + rng.gauss(0, NOISE)
        self.over = self.over + 1 if abs(self.s) > BREAK else 0
        if self.over >= HOLD:
            self.dropped = True
            return
        if self.recovering and abs(self.s) < REC:
            self.lat.append(t - self.t0)
            self.recovering = False

def predicted_cost(a, amp):
    # steps to decay amp below REC at rate (1-d): amp·(1-d)^n < REC
    import math
    if a.dropped:
        return float("inf")
    x = abs(a.s) + amp
    if x <= REC:
        return 0.0
    return math.log(REC / x) / math.log(max(1e-9, 1.0 - a.d))

def run_group(depths, route, seed=SEED, amp_scale=1.0):
    rng = random.Random(seed)
    agents = [Agent(f"a{i}", d) for i, d in enumerate(depths)]
    for t in range(STEPS):
        if t > 0 and t % SHOCK_EVERY == 0:
            amp = rng.uniform(*SHOCK_AMP) * amp_scale
            live = [a for a in agents if not a.dropped]
            if not live:
                break
            if route == "deepest":
                tgt = min(live, key=lambda a: predicted_cost(a, amp))
            elif route == "shallow":
                tgt = max(live, key=lambda a: predicted_cost(a, amp))
            else:
                tgt = rng.choice(live)
            tgt.hit(amp, t)
        for a in agents:
            a.step(rng, t)
    total_lat = sum(sum(a.lat) for a in agents)
    drops = sum(a.dropped for a in agents)
    return agents, total_lat, drops

def rankcorr(xs, ys):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for j, i in enumerate(s):
            r[i] = j
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))

def solo_latency(depth, amp, seed=SEED):
    """one agent, one shock, mean latency over trials"""
    lats = []
    for k in range(30):
        rng = random.Random(seed + k)
        a = Agent("x", depth)
        a.hit(amp, 0)
        for t in range(1, 2000):
            a.step(rng, t)
            if not a.recovering or a.dropped:
                break
        if a.lat:
            lats.append(a.lat[0])
    return st.mean(lats) if lats else float("inf")

def main():
    print("E1  latency vs depth (solo, amp=3.0)")
    depths = [0.05, 0.1, 0.15, 0.25, 0.4, 0.6, 0.8]
    lats = [solo_latency(d, 3.0) for d in depths]
    for d, l in zip(depths, lats):
        print(f"    d={d:<5} lat={round(l,1)}")
    c1 = rankcorr(depths, lats) < -0.9

    print("E2  load routing, mixed group d=[0.7,0.3,0.15,0.1]")
    res = {}
    for route in ("deepest", "random", "shallow"):
        _, tl, dr = run_group([0.7, 0.3, 0.15, 0.1], route)
        res[route] = (tl, dr)
        print(f"    route={route:<8} total_lat={tl} dropouts={dr}")
    c2 = (res["deepest"][0] < res["random"][0]
          and res["deepest"][1] <= res["random"][1]
          and res["random"][0] < res["shallow"][0])

    print("E3  formation gradient, base=0.8, g=[1.0,0.7,0.5]")
    sibs = [0.8 * g for g in (1.0, 0.7, 0.5)]
    slat = [solo_latency(d, 3.0) for d in sibs]
    for g, l in zip((1.0, 0.7, 0.5), slat):
        print(f"    g={g}  expressed_d={round(0.8*g,2)}  lat={round(l,1)}")
    c3 = slat[0] < slat[1] < slat[2]

    print("E4  amplitude scaling: lat(4A)/lat(A), A=1.0")
    ratios = {}
    for d in (0.6, 0.1):
        r = solo_latency(d, 4.0) / solo_latency(d, 1.0)
        ratios[d] = r
        print(f"    d={d}  ratio={round(r,2)}")
    c4 = ratios[0.6] < 4.0 and ratios[0.1] > 4.0

    print("\nCLAIM_TABLE evaluation (refute → edit claim, not sim)")
    for name, ok in (("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4)):
        print(f"    {name}  {'HOLDS' if ok else 'REFUTED — update the claim'}")

if __name__ == "__main__":
    main()
