#!/usr/bin/env python3
# operator_swap.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The spec's load-bearing claim is an OPERATOR SWAP, and the swap is
# arithmetic, not hydraulics:
#
#     independent-node:  breach iff  max(wave, pool) >= crest
#     coupled:           breach iff      wave + pool  >= crest
#
# This file is the arithmetic and only the arithmetic. It contains no
# reservoir, no chain, no data, no coefficient with a physical unit that
# is a claim about a real structure. It establishes WHEN the two
# operators disagree, and it is provable rather than sampled.
#
# THREE RESULTS, each demonstrated:
#
#   1. max(a,b) <= a+b for non-negative a,b. So independent-node
#      evaluation NEVER breaches a node coupled evaluation does not: the
#      bias is ONE-SIDED, always toward understating. (extraction-
#      blindness-sim's one-sided operators, on a threshold.)
#
#   2. The disagreement band has width exactly `pool`. Independent
#      requires wave >= crest; coupled requires wave >= freeboard =
#      crest - pool. So the two disagree precisely for
#      freeboard <= wave < crest, a band whose width IS the antecedent
#      pool level -- the fuller the reservoir at t0, the wider the
#      window in which independent-node evaluation is wrong. That is the
#      spec's "antecedent state is the gain" made exact.
#
#   3. Outside that band the two operators AGREE, in both directions:
#      a wave below the freeboard breaches neither, a wave at or above
#      the crest breaches both. The swap is decisive only in the middle,
#      which is why it is also the null (see chain.py).

import sys

# The two operators. Named, so the swap is a one-line diff and the
# selftest can assert nothing else differs between the runs.
INDEPENDENT = "max"
COUPLED = "sum"


def combine(op, wave, pool):
    """The quantity fed to the breach test, under either operator."""
    if op == INDEPENDENT:
        return max(wave, pool)
    if op == COUPLED:
        return wave + pool
    raise ValueError(op)


def breaches(op, wave, pool, crest):
    """Breach iff the combined quantity reaches the crest."""
    return combine(op, wave, pool) >= crest


def disagree(wave, pool, crest):
    """The two operators give different breach verdicts on this input."""
    return breaches(INDEPENDENT, wave, pool, crest) \
        != breaches(COUPLED, wave, pool, crest)


def one_sided(wave, pool, crest):
    """Returns the pair (independent_breaches, coupled_breaches).

    The claim is that independent never fires where coupled does not --
    i.e. (True, False) never occurs. Asserted over a sweep in the
    selftest; this returns the pair so a caller can see it."""
    return (breaches(INDEPENDENT, wave, pool, crest),
            breaches(COUPLED, wave, pool, crest))


def disagreement_band(pool, crest):
    """The wave interval [lo, hi) on which the operators disagree.

    Coupled breaches when wave + pool >= crest, i.e. wave >= crest-pool.
    Independent breaches when max(wave,pool) >= crest; since pool < crest
    (a positive freeboard), that is wave >= crest. So they disagree for
        crest - pool  <=  wave  <  crest
    a half-open interval of width exactly `pool`."""
    freeboard = crest - pool
    if pool <= 0:
        return {"lo": None, "hi": None, "width": 0.0,
                "note": "no antecedent pool; nothing to add, no band"}
    return {"lo": freeboard, "hi": crest, "width": float(pool),
            "note": "width equals the antecedent pool level"}


def scan(crest, pool, waves):
    """Every wave in `waves`, labelled by what the operators do."""
    rows = []
    for w in waves:
        ib, cb = one_sided(w, pool, crest)
        if ib and cb:
            label = "both breach"
        elif not ib and not cb:
            label = "neither"
        elif cb and not ib:
            label = "COUPLED ONLY -- the swap is decisive here"
        else:
            label = "INDEPENDENT ONLY -- cannot occur (would violate 1)"
        rows.append((w, ib, cb, label))
    return rows


def render():
    out = []
    w = out.append
    w("OPERATOR SWAP -- the arithmetic of the spec's core claim")
    w("")
    w("The spec: independent-node evaluation feeds max(wave, pool) to the")
    w("breach test; coupled physics feeds wave + pool. This file is that")
    w("swap and nothing else -- no reservoir, no chain, no data.")
    w("")

    # A worked node. Every number here is a bare arithmetic example,
    # labelled as such: units are metres only to read naturally, and
    # nothing below is a claim about any structure.
    crest, pool = 10.0, 4.0
    freeboard = crest - pool
    w("A WORKED NODE (arithmetic example, not a structure):")
    w("  crest 10, antecedent pool 4, so freeboard 6.")
    b = disagreement_band(pool, crest)
    w("  independent breaches when the wave alone reaches the crest:")
    w("      wave >= %.0f" % crest)
    w("  coupled breaches when the wave covers the freeboard:")
    w("      wave >= %.0f" % freeboard)
    w("  so they DISAGREE for  %.0f <= wave < %.0f" % (b["lo"], b["hi"]))
    w("  band width = %.0f, which is the antecedent pool. %s."
      % (b["width"], b["note"]))
    w("")
    w("  a wave of 6, 7, 8 or 9 breaches this node under coupled physics")
    w("  and NOT under independent-node evaluation. Each such wave is,")
    w("  by itself, below the crest; added to a reservoir already 4 deep")
    w("  it is not.")
    w("")
    for wv, ib, cb, label in scan(crest, pool, [3, 6, 8, 10, 12]):
        w("    wave %-4g independent=%-5s coupled=%-5s  %s"
          % (wv, ib, cb, label))
    w("")

    w("RESULT 1 -- the bias is ONE-SIDED.")
    w("  max(a,b) <= a+b for non-negative a,b, so 'INDEPENDENT ONLY'")
    w("  cannot occur: independent-node evaluation never breaches a node")
    w("  coupled evaluation does not. Every disagreement is the")
    w("  independent side UNDER-stating. Asserted over a sweep in the")
    w("  selftest.")
    w("")
    w("RESULT 2 -- the disagreement band width equals the antecedent")
    w("  pool. A node near crest (large pool, small freeboard) has a")
    w("  wide band of waves it passes as safe and coupled physics does")
    w("  not. A node with full freeboard (pool ~ 0) has no band at all.")
    w("  The antecedent state is the gain, exactly.")
    w("")
    w("RESULT 3 -- outside the band the operators AGREE. Below the")
    w("  freeboard: neither breaches. At or above the crest: both do.")
    w("  The swap is decisive only in the middle, which is why the same")
    w("  mechanism supplies the null test in chain.py.")
    w("")
    w("What this file does NOT establish: that the band is entered for")
    w("any real structure, or how a breach at one node changes the wave")
    w("into the next. The first requires data; the second requires the chain.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "operator_swap.py has no checks of its own. The checks that "
            "exercise it live in selftest_rcc.py.\n"
            "    python3 reservoir-chain-coupling/selftest_rcc.py\n")
        sys.exit(2)
    print(render())
