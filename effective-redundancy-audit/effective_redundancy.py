# effective_redundancy.py  —  CC0, stdlib only
from dataclasses import dataclass, field
from math import comb

MODES = {
    "A": "authorization", "B": "information", "C": "discretion",
    "D": "maintenance",   "E": "envelope",    "F": "verification",
}

@dataclass
class Channel:
    name: str
    survives_all_shared_nodes: bool   # coder's call, considering EVERY mode

@dataclass
class Case:
    name: str
    domain: str
    outcome: str                      # "failed" | "held"
    modes_present: set = field(default_factory=set)   # subset of MODES
    channels: list = field(default_factory=list)      # list[Channel]

    @property
    def n_nominal(self):
        return len(self.channels)

    @property
    def n_eff(self):
        independent = [c for c in self.channels if c.survives_all_shared_nodes]
        collapsed   = 1 if any(not c.survives_all_shared_nodes
                               for c in self.channels) else 0
        return len(independent) + collapsed


def contingency(cases):
    a = b = c = d = 0
    for x in cases:
        collapsed = (x.n_eff == 1)
        failed    = (x.outcome == "failed")
        if   collapsed and     failed: a += 1
        elif not collapsed and failed: b += 1   # counterexample
        elif collapsed and not failed: c += 1   # counterexample
        else:                          d += 1
    return a, b, c, d


def fisher_exact_2sided(a, b, c, d):
    n, r1, c1 = a+b+c+d, a+b, a+c
    r2 = c + d
    def prob(x):
        return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    p_obs = prob(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return sum(prob(x) for x in range(lo, hi+1) if prob(x) <= p_obs * 1.0000001)


def nominal_means(cases):
    f = [x.n_nominal for x in cases if x.outcome == "failed"]
    h = [x.n_nominal for x in cases if x.outcome == "held"]
    mean = lambda v: sum(v)/len(v) if v else float("nan")
    return mean(f), mean(h)            # prediction: these are CLOSE


def cohen_kappa(c1, c2):               # two coders, aligned label lists
    n = len(c1)
    po = sum(1 for x, y in zip(c1, c2) if x == y) / n
    labels = set(c1) | set(c2)
    pe = sum((c1.count(l)/n) * (c2.count(l)/n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def report(cases):
    a, b, c, d = contingency(cases)
    mf, mh = nominal_means(cases)
    print(f"n = {len(cases)}")
    print(f"2x2  [Neff==1]  failed={a} held={c}   [Neff>1] failed={b} held={d}")
    print(f"counterexamples: failed-with-redundancy={b}  held-without={c}")
    print(f"Fisher two-sided p = {fisher_exact_2sided(a,b,c,d):.4f}")
    print(f"mean N_nominal   failed={mf:.1f}  held={mh:.1f}   (predict: close)")
    for x in cases:
        print(f"  {x.name:28s} Nnom={x.n_nominal} Neff={x.n_eff} "
              f"modes={sorted(x.modes_present)} -> {x.outcome}")
