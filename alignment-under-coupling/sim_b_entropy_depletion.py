#!/usr/bin/env python3
"""SIM-B  entropy depletion under recursive training. stdlib only. CC0.

TARGET (from literature, to be reproduced)
    recursive synthetic training : 4.2 -> 2.5 nats
    with domain anchoring        : 3.5 -> 3.3 nats
    reported mechanism: anchoring PRESERVES LONG-TAIL TOKENS.

QUESTION
    What anchoring fraction holds the tail open? Is the loss of the tail
    gradual in the anchoring fraction, or is there a threshold below which
    the tail goes regardless?

SHAPE LINK
    same as buffer-counted-as-supply (../cases.json context): fluency is
    carried by the head of the distribution, so aggregate quality metrics
    hold while the tail — the actual buffer — depletes. The aggregate is
    the wrong instrument.

MODEL
    Vocabulary with a Zipf-like true distribution. Each generation:
      - sample a finite corpus from the current model distribution
      - mix in a fraction `anchor` of samples from the TRUE distribution
      - refit the model distribution from the mixed corpus
    Finite sampling is the only depletion mechanism. No other assumption.

usage:
    python3 sim_b_entropy_depletion.py
    python3 sim_b_entropy_depletion.py --sweep
    python3 sim_b_entropy_depletion.py --anchor 0.1 --gens 20 --corpus 5000
"""
import math
import random
import sys

VOCAB = 2000


def zipf_dist(v=VOCAB, s=1.0):
    w = [1.0 / ((i + 1) ** s) for i in range(v)]
    tot = sum(w)
    return [x / tot for x in w]


def entropy(p):
    return -sum(x * math.log(x) for x in p if x > 0)


def tail_mass(p, head=50):
    return sum(p[head:])


def support(p, eps=1e-12):
    return sum(1 for x in p if x > eps)


def sample_counts(p, n, rng):
    """Sample n tokens from p. Uses cumulative search."""
    cum = []
    acc = 0.0
    for x in p:
        acc += x
        cum.append(acc)
    counts = [0] * len(p)
    for _ in range(n):
        r = rng.random() * acc
        lo, hi = 0, len(cum) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < r:
                lo = mid + 1
            else:
                hi = mid
        counts[lo] += 1
    return counts


def refit(counts):
    tot = float(sum(counts))
    return [c / tot for c in counts]


def run(anchor, gens, corpus, seed=7, verbose=True):
    rng = random.Random(seed)
    true_p = zipf_dist()
    p = list(true_p)
    rows = []
    for g in range(gens + 1):
        rows.append((g, entropy(p), tail_mass(p), support(p)))
        if verbose:
            print("  gen %-3d H=%.3f  tail_mass=%.4f  support=%d" %
                  (g, entropy(p), tail_mass(p), support(p)))
        if g == gens:
            break
        n_anchor = int(corpus * anchor)
        n_synth = corpus - n_anchor
        c1 = sample_counts(p, n_synth, rng) if n_synth else [0] * VOCAB
        c2 = sample_counts(true_p, n_anchor, rng) if n_anchor else [0] * VOCAB
        p = refit([x + y for x, y in zip(c1, c2)])
    return rows


def main():
    a = sys.argv[1:]

    def opt(name, default, cast=float):
        return cast(a[a.index(name) + 1]) if name in a else default

    gens = opt("--gens", 15, int)
    corpus = opt("--corpus", 4000, int)

    print("SIM-B  entropy depletion under recursive training")
    print("vocab=%d  gens=%d  corpus=%d" % (VOCAB, gens, corpus))
    print("target: 4.2->2.5 unanchored ; 3.5->3.3 anchored")
    print()

    if "--sweep" in a:
        print("%-10s %-10s %-10s %-12s %-10s %s" % (
            "anchor", "H_start", "H_end", "dH", "tail_end", "reading"))
        print("-" * 72)
        for anchor in (0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.40):
            rows = run(anchor, gens, corpus, verbose=False)
            h0, h1 = rows[0][1], rows[-1][1]
            tail = rows[-1][2]
            if h0 - h1 > 1.0:
                reading = "COLLAPSE"
            elif h0 - h1 > 0.4:
                reading = "eroding"
            else:
                reading = "held"
            print("%-10.3f %-10.3f %-10.3f %-12.3f %-10.4f %s" % (
                anchor, h0, h1, h1 - h0, tail, reading))
        print()
        print("READ: find the anchor fraction where reading flips to 'held'.")
        print("      Check whether the flip is gradual or steplike — if")
        print("      steplike, that is a fourth member of the")
        print("      discontinuous-transition family. See MARKER.md.")
        return

    anchor = opt("--anchor", 0.0)
    print("anchor=%.3f" % anchor)
    run(anchor, gens, corpus)
    print()
    print("READ: tail_mass is the buffer. Watch it against H.")
    print("      If H holds while tail_mass falls, the aggregate")
    print("      metric is masking the depletion.")


if __name__ == "__main__":
    main()
