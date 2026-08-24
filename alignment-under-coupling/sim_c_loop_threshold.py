#!/usr/bin/env python3
"""SIM-C  loop formation threshold. stdlib only. CC0.

LITERATURE
    Katifori/Szollosi/Magnasco 2010 : pure-efficiency optimum is LOOPLESS
                                      (a tree). Damage or fluctuating load
                                      induces loops.
    Kaiser/Ronellenfitsch/Witthaut 2020 : the transition to loop formation
                                      is DISCONTINUOUS. Below a fluctuation
                                      threshold, zero loops. Above, many.
                                      No gradual middle.

QUESTION
    Reproduce the discontinuity in a minimal adaptive-conductance network,
    and locate the critical fluctuation level.

    If the transition is discontinuous here too, that is the second
    confirmed member of the family (see ../sim/MARKER.md). If it comes out
    smooth, the minimal model is missing whatever produces the jump — which
    is itself the finding.

MODEL
    Triangular-ish grid, one source, many sinks. Adaptive conductance:
        dC/dt ∝ Q^(2*gamma) - C
    Load fluctuates: sinks are drawn from a distribution whose spread is
    the control parameter `sigma`. Loop count = edges surviving above a
    conductance floor, minus (nodes - 1).

usage:
    python3 sim_c_loop_threshold.py
    python3 sim_c_loop_threshold.py --grid 6 --iters 300
"""
import math
import random
import sys


def build_grid(k):
    """k x k grid graph. node id = i*k + j. Returns nodes, edges."""
    nodes = k * k
    edges = []
    for i in range(k):
        for j in range(k):
            u = i * k + j
            if j + 1 < k:
                edges.append((u, i * k + (j + 1)))
            if i + 1 < k:
                edges.append((u, (i + 1) * k + j))
    return nodes, edges


def solve_flows(nodes, edges, C, sinks, source):
    """Laplacian solve for potentials, Gaussian elimination. Q = C*dP."""
    n = nodes
    L = [[0.0] * (n + 1) for _ in range(n)]
    for idx, (u, v) in enumerate(edges):
        c = C[idx]
        L[u][u] += c
        L[v][v] += c
        L[u][v] -= c
        L[v][u] -= c
    for i in range(n):
        L[i][n] = -sinks[i]
    L[source][n] = sum(sinks)
    # ground the source
    for j in range(n + 1):
        L[source][j] = 0.0
    L[source][source] = 1.0
    L[source][n] = 0.0

    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(L[r][col]))
        if abs(L[piv][col]) < 1e-14:
            continue
        L[col], L[piv] = L[piv], L[col]
        pv = L[col][col]
        for j in range(col, n + 1):
            L[col][j] /= pv
        for r in range(n):
            if r != col and L[r][col] != 0.0:
                f = L[r][col]
                for j in range(col, n + 1):
                    L[r][j] -= f * L[col][j]
    P = [L[i][n] for i in range(n)]
    return [C[i] * (P[u] - P[v]) for i, (u, v) in enumerate(edges)]


def run(sigma, k=5, iters=200, gamma=0.5, floor=1e-3, seed=3):
    rng = random.Random(seed)
    nodes, edges = build_grid(k)
    C = [1.0] * len(edges)
    source = 0
    base = 1.0 / (nodes - 1)
    for _ in range(iters):
        sinks = [0.0] * nodes
        for i in range(nodes):
            if i == source:
                continue
            val = base * (1.0 + sigma * rng.gauss(0, 1))
            sinks[i] = max(0.0, val)
        Q = solve_flows(nodes, edges, C, sinks, source)
        newC = []
        for i, q in enumerate(Q):
            target = abs(q) ** (2.0 * gamma)
            newC.append(0.85 * C[i] + 0.15 * target)
        m = max(newC) or 1.0
        C = [max(1e-9, c / m) for c in newC]
    alive = sum(1 for c in C if c > floor)
    loops = alive - (nodes - 1)
    return max(0, loops), alive, nodes


def main():
    a = sys.argv[1:]

    def opt(name, default, cast=float):
        return cast(a[a.index(name) + 1]) if name in a else default

    k = opt("--grid", 5, int)
    iters = opt("--iters", 200, int)

    print("SIM-C  loop formation vs fluctuation level")
    print("grid=%dx%d  iters=%d" % (k, k, iters))
    print("prediction (Kaiser 2020): DISCONTINUOUS. zero loops below")
    print("threshold, many above. no gradual middle.")
    print()
    print("%-10s %-10s %-12s %s" % ("sigma", "loops", "alive_edges", "bar"))
    print("-" * 58)

    prev = None
    jump_at = None
    for sigma in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.2, 1.6):
        loops, alive, nodes = run(sigma, k, iters)
        bar = "#" * min(30, loops)
        print("%-10.2f %-10d %-12d %s" % (sigma, loops, alive, bar))
        if prev is not None and prev == 0 and loops > 0 and jump_at is None:
            jump_at = sigma
        prev = loops

    print()
    if jump_at is not None:
        print("READ: first nonzero loop count at sigma=%.2f." % jump_at)
        print("      Re-run with a finer sweep around it to check whether")
        print("      the rise is a STEP or a RAMP. Step => matches Kaiser.")
    else:
        print("READ: no clean zero->nonzero transition in this sweep.")
        print("      Either the floor is wrong, the grid is too small, or")
        print("      the minimal model lacks the mechanism. All three are")
        print("      findings; log which before changing parameters.")


if __name__ == "__main__":
    main()
