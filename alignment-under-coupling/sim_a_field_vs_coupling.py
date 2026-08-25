#!/usr/bin/env python3
"""SIM-A  field vs coupling. stdlib only. CC0.

QUESTION
    Networked-LLM-agent work reports consensus LARGELY INSENSITIVE to
    initial positions — a departure from DeGroot, which predicts
    consensus = centrality-weighted average of initial opinions.

    Test: does an Ising/Glauber lattice with an external field h
    reproduce that insensitivity, and at what h/J ratio?

MAPPING (stated, not assumed)
    J  = majority force coefficient (De Marzo). Local coupling.
    h  = pretraining/alignment bias. External field.
    T  = sampling temperature.

    NOTE: the mapping of T is exactly what SIM-D tests. If SIM-D fails,
    the T leg of this mapping is wrong and SIM-A's T sweep is
    uninterpretable. Run SIM-D first.

MEASURED
    corr(m_final, m_initial) over many seeds.
    DeGroot-like  -> corr near 1.0 (final tracks initial)
    field-dominated -> corr near 0.0 (final independent of initial)

usage:
    python3 sim_a_field_vs_coupling.py
    python3 sim_a_field_vs_coupling.py --sweep h
    python3 sim_a_field_vs_coupling.py --n 32 --steps 400 --trials 60
"""
import math
import random
import sys


def make_lattice(n, m0, rng):
    """n x n spins, initial magnetization approximately m0."""
    p_up = (1.0 + m0) / 2.0
    return [[1 if rng.random() < p_up else -1 for _ in range(n)]
            for _ in range(n)]


def magnetization(s):
    n = len(s)
    return sum(sum(row) for row in s) / float(n * n)


def glauber_sweep(s, J, h, T, rng):
    """One Metropolis sweep, periodic boundaries."""
    n = len(s)
    for _ in range(n * n):
        i = rng.randrange(n)
        j = rng.randrange(n)
        nb = (s[(i + 1) % n][j] + s[(i - 1) % n][j] +
              s[i][(j + 1) % n] + s[i][(j - 1) % n])
        dE = 2.0 * s[i][j] * (J * nb + h)
        if dE <= 0 or (T > 0 and rng.random() < math.exp(-dE / T)):
            s[i][j] = -s[i][j]
    return s


def run_one(n, J, h, T, steps, m0, seed):
    rng = random.Random(seed)
    s = make_lattice(n, m0, rng)
    m_init = magnetization(s)
    for _ in range(steps):
        glauber_sweep(s, J, h, T, rng)
    return m_init, magnetization(s)


def pearson(xs, ys):
    k = len(xs)
    mx = sum(xs) / k
    my = sum(ys) / k
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    dy = math.sqrt(sum((b - my) ** 2 for b in ys))
    if dx == 0 or dy == 0:
        return float('nan')
    return num / (dx * dy)


def trial_set(n, J, h, T, steps, trials):
    """Vary initial magnetization across trials; correlate init vs final."""
    inits, finals = [], []
    for t in range(trials):
        m0 = -0.9 + 1.8 * (t / float(max(1, trials - 1)))
        mi, mf = run_one(n, J, h, T, steps, m0, seed=1000 + t)
        inits.append(mi)
        finals.append(mf)
    return pearson(inits, finals), sum(finals) / len(finals)


def main():
    a = sys.argv[1:]

    def opt(name, default, cast=float):
        return cast(a[a.index(name) + 1]) if name in a else default

    n = opt("--n", 24, int)
    steps = opt("--steps", 300, int)
    trials = opt("--trials", 40, int)
    T = opt("--T", 2.0)
    J = opt("--J", 1.0)

    print("SIM-A  field vs coupling")
    print("n=%d steps=%d trials=%d T=%.2f J=%.2f" % (n, steps, trials, T, J))
    print()
    print("%-8s %-10s %-14s %-12s %s" % (
        "h", "h/J", "corr(i,f)", "mean m_fin", "reading"))
    print("-" * 66)

    for h in (0.0, 0.02, 0.05, 0.10, 0.20, 0.40, 0.80):
        c, mf = trial_set(n, J, h, T, steps, trials)
        if c != c:
            reading = "degenerate"
        elif abs(c) > 0.6:
            reading = "DeGroot-like (tracks initial)"
        elif abs(c) < 0.25:
            reading = "FIELD-DOMINATED (insensitive)"
        else:
            reading = "mixed"
        print("%-8.3f %-10.3f %-14.3f %-12.3f %s" % (
            h, h / J, c, mf, reading))

    print()
    print("READ: locate the h/J at which corr drops below ~0.25.")
    print("      That ratio is the model's estimate of how much")
    print("      pretraining bias is needed to erase initial positions.")
    print("      It is NOT a claim about any real system until the")
    print("      majority force coefficient is shown to be on a")
    print("      comparable scale. See MARKER.md OPEN.")


if __name__ == "__main__":
    main()
