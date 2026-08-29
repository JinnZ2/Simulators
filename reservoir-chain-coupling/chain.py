#!/usr/bin/env python3
# chain.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The spec's MINIMAL FALSIFIABLE TEST, as a STRUCTURAL harness:
#
#     RUN 1  each node independent, node takes max(wave, pool)
#     RUN 2  coupled, out(n) = ic(n+1), antecedent gain per node
#     compare breach sets. Identical -> claim refuted. RUN 2 breaches
#     nodes RUN 1 does not -> the operator swap is load-bearing.
#
# FIRM / SOFT SEPARATION, the sustained-activation-gate discipline:
#
#   FIRM: max(a,b) <= a+b, so RUN 1's breach set is always a subset of
#   RUN 2's; a chain of thresholds can compound the difference
#   downstream; and a reach (one-node) study cannot see across nodes.
#   These are arithmetic and hold for any non-negative inputs.
#
#   SOFT: route() below is an ABSTRACT COMBINER, not a hydraulic solver.
#   It advances a scalar "wave" down a chain of scalar "pools" against
#   scalar "crests", with a breach adding a fixed release and an intact
#   node attenuating by a fixed factor. Every coefficient is SYNTHETIC
#   and marked. It is faithful to the spec's PROPAGATION loop
#   (out(n) feeds ic(n+1); route identical for both runs; only the
#   combine operator swapped) and it is NOT a model of any real dam.
#
# So this harness shows the operator swap is DETECTABLE and CAN be
# load-bearing on a constructed chain. Whether it IS load-bearing for
# any real chain is the HEC-RAS run on published data -- unreachable
# here, and the subject of columbia-chain-cascade.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import operator_swap as OP  # noqa: E402

# [SYNTHETIC] A breach releases stored water, adding to the wave that
# reaches the next node. An intact node attenuates. Both are fixed
# scalars with no physical calibration -- they set the STRUCTURE of the
# propagation, not a magnitude anyone should quote. The finding does not
# depend on their values (asserted: it survives a sweep of both).
RELEASE_GAIN = 3.0
ATTENUATION = 0.7


class Node(object):
    def __init__(self, name, crest, pool, owner="UNASSIGNED"):
        self.name = name
        self.crest = float(crest)
        self.pool = float(pool)        # antecedent pool at t0 (the gain)
        self.owner = owner

    @property
    def freeboard(self):
        return self.crest - self.pool


def route(node, wave_in, op):
    """Advance one node. The ONLY thing that differs between RUN 1 and
    RUN 2 is `op` -- everything else is identical, so a breach-set
    difference is attributable to the operator swap alone.

    Returns (breached, wave_out). ABSTRACT COMBINER, not hydraulics."""
    breached = OP.breaches(op, wave_in, node.pool, node.crest)
    if breached:
        wave_out = wave_in + RELEASE_GAIN     # [SYNTHETIC] stored water joins
    else:
        wave_out = wave_in * ATTENUATION      # [SYNTHETIC] intact node damps
    return breached, wave_out


def run_chain(nodes, boundary_inflow, op):
    """The spec's PROPAGATION loop, one operator."""
    ic = float(boundary_inflow)
    breach_set = []
    trace = []
    for node in nodes:
        breached, ic = route(node, ic, op)
        if breached:
            breach_set.append(node.name)
        trace.append((node.name, round(ic, 4), breached))
    return {"op": op, "breach_set": breach_set, "trace": trace,
            "downstream_wave": round(ic, 4)}


def compare(nodes, boundary_inflow):
    """RUN 1 vs RUN 2. The falsifiable test."""
    r1 = run_chain(nodes, boundary_inflow, OP.INDEPENDENT)
    r2 = run_chain(nodes, boundary_inflow, OP.COUPLED)
    s1, s2 = set(r1["breach_set"]), set(r2["breach_set"])
    coupled_only = sorted(s2 - s1)
    independent_only = sorted(s1 - s2)  # must always be empty (RESULT 1)
    return {
        "run1_independent": r1, "run2_coupled": r2,
        "breach_sets_identical": s1 == s2,
        "coupled_breaches_extra": coupled_only,
        "independent_breaches_extra": independent_only,
        "verdict":
            "REFUTED (for this chain): breach sets identical, coupling "
            "negligible" if s1 == s2 else
            "LOAD-BEARING (for this chain): coupled breaches %d node(s) "
            "independent does not" % len(coupled_only),
    }


# ---------------------------------------------------------- the fixtures

# THREE CONSTRUCTED CHAINS, each labelled by what it is built to show.
# All values SYNTHETIC. None is any real reservoir.

def signal_chain():
    """Intermediate freeboards: each node's pool puts the arriving wave
    in the disagreement band. Built to make the swap load-bearing, and
    to compound downstream."""
    return [Node("A", crest=10, pool=4),
            Node("B", crest=10, pool=5),
            Node("C", crest=10, pool=6),
            Node("D", crest=10, pool=6)]


def null_high_freeboard():
    """Full freeboard everywhere: no wave in the chain reaches any
    crest under either operator. Built so the breach sets are IDENTICAL
    and the harness must report REFUTED -- the spec's own refutation
    condition, and proof the detector does not always fire."""
    return [Node("A", crest=100, pool=1),
            Node("B", crest=100, pool=1),
            Node("C", crest=100, pool=1)]


def null_no_freeboard():
    """Pools already at crest: even max breaches every node, so both
    operators breach everything and the sets are again IDENTICAL. The
    swap is decisive only in the middle band -- this is the OTHER null,
    and it bounds the effect from above."""
    return [Node("A", crest=10, pool=10),
            Node("B", crest=10, pool=10),
            Node("C", crest=10, pool=10)]


def one_sided_holds(nodes_list, inflows):
    """RESULT 1 across many chains: independent_only is always empty."""
    for nodes in nodes_list:
        for q in inflows:
            c = compare(nodes, q)
            if c["independent_breaches_extra"]:
                return False
    return True


def render():
    out = []
    w = out.append
    w("RESERVOIR-CHAIN COUPLING -- the minimal falsifiable test, run")
    w("")
    w("The spec: RUN 1 independent (max), RUN 2 coupled (sum), compare")
    w("breach sets. This runs it on CONSTRUCTED chains -- route() is an")
    w("abstract combiner, not a hydraulic solver, every coefficient")
    w("synthetic and marked. It shows the swap is detectable and can be")
    w("load-bearing; it says nothing about any real reservoir.")
    w("")
    w("  [SYNTHETIC] breach release gain %.1f, intact attenuation %.1f"
      % (RELEASE_GAIN, ATTENUATION))
    w("")

    inflow = 6.0
    w("1. SIGNAL CHAIN -- pools put the wave in the disagreement band")
    c = compare(signal_chain(), inflow)
    w("   boundary inflow %.0f" % inflow)
    w("   RUN 1 (independent, max):  breach set %s"
      % (c["run1_independent"]["breach_set"] or "none"))
    w("   RUN 2 (coupled, sum):      breach set %s"
      % (c["run2_coupled"]["breach_set"] or "none"))
    w("   coupled breaches extra:    %s" % (c["coupled_breaches_extra"]))
    w("   %s" % c["verdict"])
    w("")
    w("   the wave down the chain, per operator:")
    w("     node   independent      coupled")
    t1 = dict((n, (v, b)) for n, v, b in c["run1_independent"]["trace"])
    t2 = dict((n, (v, b)) for n, v, b in c["run2_coupled"]["trace"])
    for n, _v, _b in c["run1_independent"]["trace"]:
        v1, b1 = t1[n]
        v2, b2 = t2[n]
        w("     %-6s %6.2f %-8s %6.2f %s" % (
            n, v1, "BREACH" if b1 else "", v2, "BREACH" if b2 else ""))
    w("   Under coupled physics a breach at A raises the wave into B,")
    w("   which breaches and raises it into C, and so on -- the")
    w("   difference COMPOUNDS downstream. A one-node reach study sees")
    w("   node A alone and cannot produce this.")
    w("")

    w("2. NULL, HIGH FREEBOARD -- no wave reaches any crest")
    cn = compare(null_high_freeboard(), inflow)
    w("   breach sets identical: %s" % cn["breach_sets_identical"])
    w("   %s" % cn["verdict"])
    w("   The detector does not always fire. On a chain with full")
    w("   buffer the coupling term is genuinely negligible, and the")
    w("   harness reports the spec's own refutation verdict.")
    w("")

    w("3. NULL, NO FREEBOARD -- pools already at crest")
    cz = compare(null_no_freeboard(), inflow)
    w("   breach sets identical: %s" % cz["breach_sets_identical"])
    w("   %s" % cz["verdict"])
    w("   The other bound: when every node is already at crest, even")
    w("   max breaches all of them, so the swap changes nothing. The")
    w("   effect lives only in the intermediate antecedent-state band")
    w("   operator_swap.py RESULT 2 measures.")
    w("")

    w("4. RESULT 1 HOLDS ACROSS ALL THREE CHAINS")
    ok = one_sided_holds(
        [signal_chain(), null_high_freeboard(), null_no_freeboard()],
        [2, 4, 6, 8, 10, 14])
    w("   independent-node evaluation breaches a node coupled does not:")
    w("     ever observed: %s" % (not ok is True and "yes" or "no"))
    w("   The bias is one-sided in every run: RUN 1's breach set is")
    w("   always a subset of RUN 2's. Independent-node evaluation can")
    w("   only understate the chain, never overstate it.")
    w("")

    w("WHAT THIS IS AND IS NOT")
    w("  IS: a demonstration that the operator swap is detectable, that")
    w("  it compounds down a chain, that it is one-sided, and that it")
    w("  vanishes outside an antecedent-state band -- all on synthetic")
    w("  chains, all arithmetic.")
    w("  IS NOT: evidence that the band is entered for any real chain.")
    w("  That is the spec's falsifiable test on published data through")
    w("  HEC-RAS, which requires the engine and the terrain -- unreachable")
    w("  here; see columbia-chain-cascade for the measured blockers.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "chain.py has no checks of its own. The checks that exercise "
            "it and operator_swap.py live in selftest_rcc.py.\n"
            "    python3 reservoir-chain-coupling/selftest_rcc.py\n")
        sys.exit(2)
    print(render())
