"""G3: rows 35-36 -- percolation (two families, kept apart, Q10) and branching (Q11).

Percolation, union-find cluster growth (Newman-Ziff): occupy sites (or bonds) one at a time in a
seeded random order and record the occupied fraction at which a cluster first spans top to bottom.
The two families have separate functions and separate size bounds; neither result feeds the other.

Branching, Galton-Watson: the extinction probability is the smallest fixed point of the offspring
generating function f in [0, 1]. For mean m <= 1 (and not every individual having exactly one
child) q = 1; otherwise q is reached by iterating s <- f(s) from s = 0.

Size bounds are declared; an input past a bound reads APPLICABILITY : OUTSIDE_DOMAIN (Q11), on no
failure axis. Known answers (site ~0.5927, bond 0.5 on the square lattice; Poisson q = e^{lam(q-1)})
are VERIFY-tagged: recalled, no source read by this session.
"""
import math
import random

from . import axes as A

KNOWN_ANSWERS_STATUS = "NOT_CHECKED (VERIFY): recalled, no source read by this session"
SITE_PC_SQUARE = 0.5927      # VERIFY
BOND_PC_SQUARE = 0.5         # VERIFY (exact by duality, recalled)

SITE_L_MAX = 512             # declared bounds, separate per family (Q10)
BOND_L_MAX = 512
PMF_SUPPORT_MAX = 1000


class FamilyError(ValueError):
    pass


class _UF(object):
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def _check_L(L, bound, family):
    if isinstance(L, bool) or not isinstance(L, int) or L < 2:
        raise FamilyError("%s: L is an integer >= 2" % family)
    if L > bound:
        return A.reading("APPLICABILITY", "OUTSIDE_DOMAIN", reason="%s lattice beyond declared bound" % family,
                         bound="L <= %d" % bound)
    return None


def site_spanning_fraction(L, rng):
    """One Newman-Ziff run on an L x L site lattice: occupied fraction at first top-bottom span."""
    n = L * L
    top, bot = n, n + 1
    uf = _UF(n + 2)
    occ = [False] * n
    order = list(range(n))
    rng.shuffle(order)
    for count, s in enumerate(order, 1):
        occ[s] = True
        r, c = divmod(s, L)
        if r == 0:
            uf.union(s, top)
        if r == L - 1:
            uf.union(s, bot)
        for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= rr < L and 0 <= cc < L and occ[rr * L + cc]:
                uf.union(s, rr * L + cc)
        if uf.find(top) == uf.find(bot):
            return count / float(n)
    raise FamilyError("no span after full occupation")


def bond_spanning_fraction(L, rng):
    """One run on L x L nodes with nearest-neighbour bonds: bond fraction at first top-bottom span."""
    n = L * L
    top, bot = n, n + 1
    uf = _UF(n + 2)
    for c in range(L):
        uf.union(c, top)
        uf.union((L - 1) * L + c, bot)
    bonds = [(r * L + c, r * L + c + 1) for r in range(L) for c in range(L - 1)]
    bonds += [(r * L + c, (r + 1) * L + c) for r in range(L - 1) for c in range(L)]
    rng.shuffle(bonds)
    for count, (a, b) in enumerate(bonds, 1):
        uf.union(a, b)
        if uf.find(top) == uf.find(bot):
            return count / float(len(bonds))
    raise FamilyError("no span after all bonds")


def _estimate(fn, L, runs, seed, bound, family):
    out = _check_L(L, bound, family)
    if out is not None:
        return out
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 1:
        raise FamilyError("runs is an integer >= 1")
    rng = random.Random(seed)
    xs = [fn(L, rng) for _ in range(runs)]
    mean = sum(xs) / runs
    sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / (runs - 1)) if runs > 1 else None
    return {"family": family, "L": L, "runs": runs, "seed": seed, "mean": mean, "sd": sd,
            "se": sd / math.sqrt(runs) if sd is not None else None,
            "known_answer": SITE_PC_SQUARE if family == "site" else BOND_PC_SQUARE,
            "known_answer_status": KNOWN_ANSWERS_STATUS}


def site_threshold(L, runs, seed):
    return _estimate(site_spanning_fraction, L, runs, seed, SITE_L_MAX, "site")


def bond_threshold(L, runs, seed):
    return _estimate(bond_spanning_fraction, L, runs, seed, BOND_L_MAX, "bond")


def _pgf(pmf):
    return lambda s: sum(p * s ** k for k, p in enumerate(pmf))


def _iterate(f, tol=1e-15, max_iter=100000):
    s = 0.0
    for i in range(max_iter):
        t = f(s)
        if abs(t - s) <= tol:
            return t, i + 1
        s = t
    raise FamilyError("fixed-point iteration did not converge in %d steps" % max_iter)


def extinction_pmf(pmf):
    """Bounded offspring pmf p_0..p_K. Returns q, or APPLICABILITY OUTSIDE_DOMAIN past the support bound."""
    if not isinstance(pmf, (list, tuple)) or not pmf:
        raise FamilyError("pmf is a non-empty list p_0..p_K")
    if len(pmf) - 1 > PMF_SUPPORT_MAX:
        return A.reading("APPLICABILITY", "OUTSIDE_DOMAIN", reason="offspring support beyond declared bound",
                         bound="K <= %d" % PMF_SUPPORT_MAX)
    if any((not isinstance(p, (int, float))) or isinstance(p, bool) or p < 0 for p in pmf) \
            or abs(sum(pmf) - 1.0) > 1e-12:
        raise FamilyError("pmf entries are >= 0 and sum to 1")
    if len(pmf) > 1 and pmf[1] == 1.0:
        return 0.0                        # every individual has exactly one child: never extinct
    m = sum(k * p for k, p in enumerate(pmf))
    if m <= 1:
        return 1.0
    return _iterate(_pgf(pmf))[0]


def extinction_poisson(lam):
    """Poisson(lam) offspring: q = smallest root in [0, 1] of q = e^{lam (q - 1)}."""
    if isinstance(lam, bool) or not isinstance(lam, (int, float)) or lam < 0:
        raise FamilyError("lam is a number >= 0")
    if lam <= 1:
        return 1.0
    return _iterate(lambda s: math.exp(lam * (s - 1.0)))[0]


def render():
    out = ["known answers: %s" % KNOWN_ANSWERS_STATUS]
    for fn in (site_threshold, bond_threshold):
        r = fn(32, 60, 11)
        out.append("%-4s L=%d runs=%d seed=%d  mean first-span fraction %.4f  se %.4f  known %s"
                   % (r["family"], r["L"], r["runs"], r["seed"], r["mean"], r["se"], r["known_answer"]))
    for lam in (0.5, 1.0, 1.5, 2.0, 3.0):
        out.append("Poisson lam=%-4s extinction q = %.10f" % (lam, extinction_poisson(lam)))
    for pmf in ([0.5, 0.5], [0.25, 0.5, 0.25], [0.25, 0.25, 0.5], [0.0, 1.0]):
        out.append("pmf %-20s extinction q = %.10f" % (pmf, extinction_pmf(pmf)))
    return "\n".join(out)


if __name__ == "__main__":
    print(render())
