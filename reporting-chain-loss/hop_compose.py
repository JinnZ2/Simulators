# SPDX-License-Identifier: CC0-1.0
"""
hop_compose.py -- WO-5 TRANSIT LOSS, the composable half.

The order's formal floor is the data processing inequality: information
about a source cannot increase along a chain. That is a theorem and is not
re-derived here; it is used as the null. The order's GAP is that the DPI
assumes a FIXED transform, and organizational hops do not have one -- each
hop carries its own objective function. Random loss attenuates toward noise
and cancels; DIRECTED loss compounds in a consistent direction. The order
asks what the terminal output is an estimator OF.

This module answers it exactly, in one model where the answer is closed
form: a linear-Gaussian hop chain

    x_0 = g                      (the ground, what the terminal is read AS)
    x_n = a_n * x_{n-1} + c_n + e_n

with a_n a per-hop gain (the DPI floor lives here), c_n a DIRECTED incentive
offset (a consistent pull -- how the hop looks, what it queues), and e_n a
mean-zero random loss that biases nothing. Then

    E[x_N | g] = (prod a_n) * g  +  sum_k (prod_{j>k} a_j) * c_k

The coefficient on g is the retained gain G = prod a_n; the additive term is
the composed incentive stack B. A reader who takes the terminal AS a scaled
ground reading (ground_hat = x_N / G) carries a bias B / G, and since a lossy
chain has |G| <= 1 the rescaling AMPLIFIES the incentive bias. That is the
order's "estimator of the incentive stack, not the ground", made a number.

Nothing here is a measurement of any plant. The chains are CONSTRUCTED, seeded
where random, and the coefficients carry no units. The claim demonstrated is
about the ARITHMETIC of composition, which is what the order says has not been
run -- the per-hop pieces are documented, the composition is not.

States kept apart (a zero is a zero, an absence is not a zero):
  - no incentive (all c = 0)        -> B is exactly 0.0, verdict NO_INCENTIVE
  - an unspecified gain (a has None)-> NOT_EVALUABLE, never 0
  - a dead hop (prod a == 0)         -> ground unrecoverable; the rescaled
                                        bias is None (GROUND_UNRECOVERABLE),
                                        not an infinity manufactured by the
                                        division

Stdlib only. Parses under 3.9. ASCII only. CC0.

    python3 hop_compose.py            # render the composition
    python3 hop_compose.py --choices  # the [CHOICE n] markers
    python3 test_hop.py               # the checks; prints their count
"""

from __future__ import annotations

import os
import random
import sys

# [CHOICE 1] the ensemble default N-range and the per-hop offset magnitude.
#   The order names no numbers here; these are the sweep the render walks,
#   printed so they are not read as findings.
DEFAULT_NS = (1, 2, 4, 8, 16)
DEFAULT_MAGNITUDE = 1.0
# [CHOICE 2] the ensemble default gain. |a| <= 1 makes each hop lossy or
#   neutral (the DPI floor); 0.9 is a mild per-hop loss, stated not derived.
DEFAULT_GAIN = 0.9
# [CHOICE 3] a gain magnitude at or below this counts a hop as dead -- the
#   ground is unrecoverable through it, so the rescaled bias is refused.
DEAD_GAIN = 1e-12

CHOICES = {
    1: "ensemble N-range %s and offset magnitude %.3g -- the sweep, not a "
       "finding" % (DEFAULT_NS, DEFAULT_MAGNITUDE),
    2: "ensemble gain %.3g; |a|<=1 is the DPI floor, the value is stated"
       % DEFAULT_GAIN,
    3: "dead-hop gain threshold %.3g; at or below it the ground is "
       "unrecoverable and the rescaled bias is None" % DEAD_GAIN,
}


def _has_none(seq):
    return any(x is None for x in seq)


def retained_ground_gain(a):
    """G = prod(a_n), the coefficient the ground survives with. NOT_EVALUABLE
    (None) if any gain is unspecified -- an unspecified gain is not a gain of
    zero and not a gain of one."""
    if _has_none(a):
        return None
    g = 1.0
    for x in a:
        g *= x
    return g


def gain_is_nonincreasing(a):
    """The DPI floor in this model: with every |a_n| <= 1 the magnitude of
    the partial product is non-increasing hop by hop. Returns True/False, or
    None if a gain is unspecified. This is a structural check on the model,
    not a claim about any chain."""
    if _has_none(a):
        return None
    mag = 1.0
    for x in a:
        nxt = mag * abs(x)
        if nxt > mag + 1e-15:
            return False
        mag = nxt
    return True


def composed_bias(a, c):
    """B = sum_k (prod_{j>k} a_j) * c_k -- the incentive stack composed across
    the chain. All c == 0 gives exactly 0.0 (a real zero: no incentive, no
    bias). None if any gain or offset is unspecified.

    This is the load-bearing metric and is registered in
    tools/known_answer.py."""
    if len(a) != len(c):
        return None
    if _has_none(a) or _has_none(c):
        return None
    n = len(a)
    b = 0.0
    for k in range(n):
        downstream = 1.0
        for j in range(k + 1, n):
            downstream *= a[j]
        b += downstream * c[k]
    return b


def rescaled_bias(a, c):
    """The bias carried by a reader who takes the terminal AS a scaled ground
    reading: B / G. None with GROUND_UNRECOVERABLE when the retained gain is
    dead -- the right answer there is that the ground cannot be read back at
    all, not an infinite bias."""
    b = composed_bias(a, c)
    g = retained_ground_gain(a)
    if b is None or g is None:
        return {"value": None, "state": "NOT_EVALUABLE"}
    if abs(g) <= DEAD_GAIN:
        return {"value": None, "state": "GROUND_UNRECOVERABLE"}
    return {"value": b / g, "state": "OK"}


def _classify(b, has_incentive):
    if not has_incentive:
        return "NO_INCENTIVE"
    if b is None:
        return "NOT_EVALUABLE"
    return "DIRECTED_BIAS" if abs(b) > 0.0 else "CANCELLED"


def ensemble(ns=DEFAULT_NS, gain=DEFAULT_GAIN, magnitude=DEFAULT_MAGNITUDE,
             trials=400, seed=0):
    """Directed vs random loss, per chain length. Directed: every hop's
    offset is +magnitude (same sign -- the consistent pull). Random: each
    hop's offset is +/- magnitude with equal probability (mean zero). Over
    the ensemble the directed bias grows with N; the random bias is mean-zero
    and its spread grows only as sqrt(N), so it cancels. Returns one row per
    N with the mean |bias| of each arm and their ratio.

    NOT constant: at magnitude 0 both arms return exactly 0 (NO_INCENTIVE),
    so a run that reads DIRECTED_BIAS everywhere is a property of the offsets,
    not of the code."""
    rng = random.Random(seed)
    rows = []
    for n in ns:
        a = [gain] * n
        dir_abs = []
        rnd_abs = []
        for _ in range(trials):
            c_dir = [magnitude] * n
            c_rnd = [rng.choice([-magnitude, magnitude]) for _ in range(n)]
            dir_abs.append(abs(composed_bias(a, c_dir)))
            rnd_abs.append(abs(composed_bias(a, c_rnd)))
        md = sum(dir_abs) / len(dir_abs)
        mr = sum(rnd_abs) / len(rnd_abs)
        ratio = (md / mr) if mr > 0 else None
        rows.append({
            "N": n,
            "directed_mean_abs_bias": md,
            "random_mean_abs_bias": mr,
            "directed_over_random": ratio,
            "directed_verdict": _classify(md, magnitude != 0),
            "random_verdict": _classify(None if mr > 0 else 0.0,
                                        magnitude != 0),
        })
    return rows


def render():
    out = []
    out.append("WO-5 TRANSIT LOSS -- composition of a linear-Gaussian hop "
               "chain")
    out.append("CONSTRUCTED chains, seeded; coefficients carry no units. "
               "Not a plant.")
    out.append("")
    out.append("[CHOICE 1] %s" % CHOICES[1])
    out.append("[CHOICE 2] %s" % CHOICES[2])
    out.append("[CHOICE 3] %s" % CHOICES[3])
    out.append("")

    out.append("A single directed chain (a=%.2f at every hop, offset +%.2f):"
               % (DEFAULT_GAIN, DEFAULT_MAGNITUDE))
    for n in (1, 4, 16):
        a = [DEFAULT_GAIN] * n
        c = [DEFAULT_MAGNITUDE] * n
        b = composed_bias(a, c)
        g = retained_ground_gain(a)
        rb = rescaled_bias(a, c)
        out.append("  N=%2d  retained gain G=%.5f  composed bias B=%.5f  "
                   "reader bias B/G=%.5f"
                   % (n, g, b, rb["value"]))
    out.append("  the ground survives ever weaker (G falls); the incentive "
               "stack the reader carries (B/G) grows with the chain.")
    out.append("")

    out.append("Directed vs random loss over the ensemble:")
    out.append("  %-4s  %-14s  %-14s  %-10s" %
               ("N", "directed |B|", "random |B|", "ratio"))
    for r in ensemble():
        ratio = "%.3f" % r["directed_over_random"] \
            if r["directed_over_random"] is not None else "--"
        out.append("  %-4d  %-14.5f  %-14.5f  %-10s"
                   % (r["N"], r["directed_mean_abs_bias"],
                      r["random_mean_abs_bias"], ratio))
    out.append("  directed loss compounds; random loss cancels toward the "
               "noise floor. The ratio is the order's DIRECTED-vs-random flip.")
    out.append("")

    out.append("States that are not a zero:")
    out.append("  no incentive (all c=0):   B=%s"
               % composed_bias([0.9, 0.9], [0.0, 0.0]))
    out.append("  unspecified gain:         B=%s"
               % composed_bias([0.9, None], [1.0, 1.0]))
    dead = rescaled_bias([0.9, 0.0, 0.9], [1.0, 1.0, 1.0])
    out.append("  dead hop (G=0):           reader bias %s (%s)"
               % (dead["value"], dead["state"]))
    out.append("")
    out.append("DPI floor holds in the model: partial-product magnitude "
               "non-increasing = %s" % gain_is_nonincreasing([0.9] * 8))
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "hop_compose.py has no --selftest. The checks are in "
            "test_hop.py:\n    python3 %s\n"
            % os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "test_hop.py"))
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
