#!/usr/bin/env python3
"""SIM-D  temperature null test. stdlib only. CC0.

RUN THIS FIRST. It is the discriminator for the whole marker.

LITERATURE
    Guo, Shang, Clavel: temperature has NO EFFECT on homogenization.
    Counterintuitive, and load-bearing: it means the ordering lives in the
    LEARNED DISTRIBUTION, not in the sampling step.

WHY IT MATTERS
    A naive Ising mapping puts sampling temperature in the role of thermal
    noise T. In that model, raising T MUST reduce ordering. The literature
    says it doesn't. So either:
      (a) the naive mapping is wrong — T is not thermal noise, and the
          ordering is quenched into the distribution itself; or
      (b) the measured "no effect" is an artifact of the diversity metric
          used (token entropy vs embedding clusters vs task-level).

    This sim separates the two by measuring diversity THREE ways under a
    temperature sweep, on a distribution that has been pre-ordered
    (quenched) versus one that is not.

READING
    quenched case shows FLAT diversity vs temperature   -> supports (a)
    quenched case shows RISING diversity vs temperature -> naive mapping
                                                            survives; the
                                                            literature
                                                            result needs
                                                            another
                                                            explanation
    metrics DISAGREE with each other                    -> supports (b),
                                                            and the metric
                                                            choice is the
                                                            real variable

usage:
    python3 sim_d_temperature_null.py
    python3 sim_d_temperature_null.py --samples 8000
"""
import math
import random
import sys

VOCAB = 1000


def zipf(v=VOCAB, s=1.0):
    w = [1.0 / ((i + 1) ** s) for i in range(v)]
    t = sum(w)
    return [x / t for x in w]


def quench(p, strength):
    """Concentrate mass on a few modes — an attractor state baked into the
    distribution itself, independent of sampling. strength=0 -> unchanged."""
    if strength <= 0:
        return list(p)
    q = [x ** (1.0 + strength) for x in p]
    t = sum(q)
    return [x / t for x in q]


def temper(p, T):
    """Apply sampling temperature to a distribution."""
    if T <= 0:
        out = [0.0] * len(p)
        out[p.index(max(p))] = 1.0
        return out
    lg = [math.log(x) / T if x > 0 else -1e18 for x in p]
    m = max(lg)
    e = [math.exp(x - m) for x in lg]
    t = sum(e)
    return [x / t for x in e]


def draw(p, n, rng):
    cum, acc = [], 0.0
    for x in p:
        acc += x
        cum.append(acc)
    out = []
    for _ in range(n):
        r = rng.random() * acc
        lo, hi = 0, len(cum) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < r:
                lo = mid + 1
            else:
                hi = mid
        out.append(lo)
    return out


def m_entropy(samples):
    """Metric 1: token entropy of the empirical sample."""
    c = {}
    for s in samples:
        c[s] = c.get(s, 0) + 1
    n = float(len(samples))
    return -sum((v / n) * math.log(v / n) for v in c.values())


def m_distinct(samples):
    """Metric 2: type-token ratio (distinct fraction)."""
    return len(set(samples)) / float(len(samples))


def m_clusters(samples, k=20):
    """Metric 3: coarse 'embedding cluster' proxy — count of occupied bins
    when vocabulary is bucketed. Mimics embedding-space cluster counts,
    which are insensitive to reshuffling within a bucket."""
    bins = set(s % k for s in samples)
    return len(bins)


def sweep(strength, samples, rng_seed=11):
    p0 = quench(zipf(), strength)
    rows = []
    for T in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
        rng = random.Random(rng_seed)
        s = draw(temper(p0, T), samples, rng)
        rows.append((T, m_entropy(s), m_distinct(s), m_clusters(s)))
    return rows


def verdict(rows, col):
    vals = [r[col] for r in rows]
    lo, hi = min(vals), max(vals)
    span = hi - lo
    ref = abs(sum(vals) / len(vals)) or 1.0
    return "FLAT" if span / ref < 0.10 else "RISES"


def main():
    a = sys.argv[1:]
    samples = int(a[a.index("--samples") + 1]) if "--samples" in a else 5000

    print("SIM-D  temperature null test  [DISCRIMINATOR — run first]")
    print("samples=%d" % samples)
    print("literature: temperature has NO EFFECT on homogenization")
    print()

    for name, strength in (("UNQUENCHED", 0.0), ("QUENCHED", 1.5)):
        print("== %s (quench strength %.1f) ==" % (name, strength))
        rows = sweep(strength, samples)
        print("%-8s %-12s %-12s %s" % ("T", "entropy", "distinct", "clusters"))
        for T, h, d, c in rows:
            print("%-8.2f %-12.3f %-12.4f %d" % (T, h, d, c))
        print("  entropy:  %s" % verdict(rows, 1))
        print("  distinct: %s" % verdict(rows, 2))
        print("  clusters: %s" % verdict(rows, 3))
        print()

    print("READ:")
    print("  QUENCHED flat on all three   -> ordering is in the learned")
    print("     distribution. Naive Ising T-mapping is DEAD. SIM-A's T leg")
    print("     must be reinterpreted before its output means anything.")
    print("  QUENCHED rises               -> naive mapping survives here;")
    print("     the literature null needs a different explanation.")
    print("  Metrics disagree             -> the metric is the variable,")
    print("     not the temperature. Log which metric and stop.")


if __name__ == "__main__":
    main()
