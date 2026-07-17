#!/usr/bin/env python3
# semantic_drift_test.py — CC0, stdlib-only, phone-buildable
#
# INSTRUMENT FOR: does machine-mediated text accelerate moral-overlay
# drift on measurement words, and how does it interact with declining
# veto capacity (population's ability to push a sense back to terrain)?
#
# REFUTATION PROTOCOL: claim fails → edit the claim, never retune the sim.
# ANTI-FREEZE: output is trajectory. claims scored at end.
# NO INTERIOR STATES: speakers have sense values, exposure, veto rate.
#
# STATE VARIABLE
# ──────────────
#   m ∈ [0,1]  moral load carried by one word-sense
#              0 = pure measurement ("slack rope")
#              1 = pure verdict     ("sinful soul")
#
# ARCHITECTURE
# ─────────────
#   Humans     m_i ← m_i + λ·(corpus − m_i) − β_i·(m_i − 0)
#              λ  exposure coupling (reading pulls you toward corpus)
#              β_i veto rate (terrain use pulls the word back to
#                  measurement — the slack rope is right there)
#   Machine    m_M = clip( corpus·a + s )
#              a  amplification (safety prior resolves ambiguity
#                 toward the moralized reading), s fixed offset
#   Corpus     next = (1−f)·mean(humans) + f·m_M
#              f  machine-mediated fraction of new text
#
# CLAIM_TABLE
# ─────────────
#   C1  f=0 (no machine): m equilibrates at a stable fixed point
#       λ·c/(λ+β) — drift stops. language self-corrects.
#   C2  equilibrium m rises MONOTONICALLY with f (a>1 fixed).
#   C3  the ratchet needs amplification: with a=1, s=0, machine
#       mediation at any f does not raise equilibrium m above the
#       f=0 value. mediation alone is neutral; amplification drives.
#   C4  declining veto β(t) interacts SUPER-ADDITIVELY with f:
#       Δm(f↑ & β↓ together) > Δm(f↑ alone) + Δm(β↓ alone).
#       the two curves crossing is worse than the sum of each.

import random, statistics as st

SEED, N, GENS = 3, 200, 300
LAM = 0.10          # exposure coupling
BETA0 = 0.08        # initial mean veto rate
AMP, OFFS = 1.06, 0.01   # machine amplification + safety offset
M0 = 0.30           # historical moral load already in the corpus

def clip(x): return max(0.0, min(1.0, x))

def run(f, a=AMP, s=OFFS, beta_decay=0.0, gens=GENS, seed=SEED):
    rng = random.Random(seed)
    hum = [clip(rng.gauss(M0, 0.08)) for _ in range(N)]
    beta = [max(0.005, rng.gauss(BETA0, 0.02)) for _ in range(N)]
    corpus = M0
    traj = []
    for t in range(gens):
        m_machine = clip(corpus * a + s)
        corpus = clip((1 - f) * st.mean(hum) + f * m_machine)
        decay = (1 - beta_decay) ** t
        hum = [clip(h + LAM * (corpus - h) - b * decay * h)
               for h, b in zip(hum, beta)]
        traj.append(corpus)
    return traj

def tail(traj, k=20): return st.mean(traj[-k:])

def main():
    print("E1  no machine (f=0): does drift stop?")
    t0 = run(0.0)
    print(f"    m: start={M0} → gen100={round(t0[99],3)} → end={round(tail(t0),3)}")
    c1 = abs(t0[-1] - t0[-40]) < 0.005          # flat tail = fixed point

    print("E2  equilibrium vs machine fraction f (a=1.06)")
    eq = {}
    for f in (0.0, 0.2, 0.4, 0.6, 0.8):
        eq[f] = tail(run(f))
        print(f"    f={f}  m_eq={round(eq[f],3)}")
    fs = sorted(eq)
    c2 = all(eq[fs[i+1]] > eq[fs[i]] for i in range(len(fs)-1))

    print("E3  mediation without amplification (a=1, s=0)")
    neut = {f: tail(run(f, a=1.0, s=0.0)) for f in (0.0, 0.4, 0.8)}
    for f, v in neut.items():
        print(f"    f={f}  m_eq={round(v,3)}")
    c3 = all(neut[f] <= neut[0.0] + 0.01 for f in neut)

    print("E4  interaction: f=0.6 rise × veto decay 1%/gen")
    base   = tail(run(0.0, beta_decay=0.0))
    d_f    = tail(run(0.6, beta_decay=0.0)) - base
    d_b    = tail(run(0.0, beta_decay=0.01)) - base
    d_both = tail(run(0.6, beta_decay=0.01)) - base
    print(f"    Δ(f alone)={round(d_f,3)}  Δ(β↓ alone)={round(d_b,3)}"
          f"  Δ(both)={round(d_both,3)}  sum={round(d_f+d_b,3)}")
    c4 = d_both > d_f + d_b

    print("\nCLAIM_TABLE evaluation (refute → edit claim, not sim)")
    for name, ok in (("C1", c1), ("C2", c2), ("C3", c3), ("C4", c4)):
        print(f"    {name}  {'HOLDS' if ok else 'REFUTED — update the claim'}")

if __name__ == "__main__":
    main()
