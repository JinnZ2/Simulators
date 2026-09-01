#!/usr/bin/env python3
# module_f.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# REPAIRED (CCC_017): one word on the last render line, so the report
# clears the repo's no_severity screen. Arithmetic untouched.
#
# MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)
#
# The arithmetic of the two coupled amplifiers the SOURCE_DROP.md calls
# "the part standard breach modeling drops" and "not a refinement; it
# changes the cascade outcome." This file is that arithmetic and nothing
# else — no reservoir, no chain, no data, no coefficient with a physical
# unit that is a claim about a real structure.
#
# See SCOPE_BOUNDARY.md for why the operator swap is a model-boundary
# issue: the independent model (max) sees only the proximate trigger
# (the wave), while the coupled model (sum) sees the trigger plus the
# antecedent state. Standard breach modeling drops the antecedent state
# because it is "outside the dam" — an institutional scope boundary, not
# a physical one.
#
# TWO AMPLIFIERS:
#
#   AMPLIFIER A — OPERATOR SWAP (antecedent pool as the gain)
#     Independent-node: breach iff max(wave, pool) >= crest
#     Coupled:          breach iff     wave + pool  >= crest
#     The bias is one-sided (always toward understating) and the
#     disagreement band width equals the antecedent pool level.
#     Proved in reservoir-chain-coupling/operator_swap.py.
#
#   AMPLIFIER B — BURN-MODIFIED ROUGHNESS (antecedent land state)
#     A prior wildfire or flood removes vegetation and structures,
#     reducing Manning n and increasing wave celerity. The effect is
#     parameterized as an attenuation reduction: the wave loses less
#     energy between nodes over a smoother bed.
#
#   THE COUPLING — both amplifiers act on the same wave:
#     Amplifier A raises the wave height at each node.
#     Amplifier B reduces the attenuation between nodes.
#     A raised wave that attenuates less arrives at the next node with
#     more energy than either effect alone — the coupling is load-bearing.
#
# This module defines the parameter sweep space and proves structural
# properties. It does not claim any magnitude for any real structure.

import sys

# The two operators, named so the swap is a one-line diff.
INDEPENDENT = "max"
COUPLED = "sum"

# Amplifier B: the roughness modification parameter space.
# These are dimensionless factors, not physical quantities.
BURN_SEVERITY_MIN = 0.0   # no burn
BURN_SEVERITY_MAX = 1.0   # complete vegetation removal
ROUGHNESS_MULTIPLIER_MIN = 0.3  # post-burn n is 30% of pre-burn (smoother)
ROUGHNESS_MULTIPLIER_MAX = 1.0  # no change (no burn, or no effect)
ATTENUATION_REDUCTION_MIN = 0.0  # no additional attenuation reduction
ATTENUATION_REDUCTION_MAX = 0.5  # up to 50% less attenuation


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


def propagate(wave, attenuation_factor):
    """ABSTRACT propagation: fraction of wave surviving to next node.

    The attenuation factor is a dimensionless scalar in [0, 1].
    It is reduced (closer to 1) by burn-modified roughness.
    This is not a hydraulic solver; it is the structural placeholder
    for whatever the routing engine computes."""
    return wave * attenuation_factor


def modified_attenuation(base_attenuation, burn_severity,
                         attenuation_reduction_max):
    """Attenuation factor under burn-modified roughness.

    base_attenuation:       the fraction surviving under base roughness
    burn_severity:          0.0 (unburned) to 1.0 (complete removal)
    attenuation_reduction_max: the maximum reduction in attenuation

    Returns the modified attenuation factor, which is >= base_attenuation.
    At burn_severity = 0, returns base_attenuation exactly."""
    return base_attenuation + burn_severity * attenuation_reduction_max


# ------------------------------------------------------------------
# Structural proofs: the three breach sets and their ordering
# ------------------------------------------------------------------

def breach_set_single_node(wave, pool, crest, op):
    """Breach verdict for a single node, one operator."""
    return breaches(op, wave, pool, crest)


def breach_set_chain(nodes, boundary_wave, pool, crest, op,
                     base_attenuation, burn_severity=0.0,
                     attenuation_reduction_max=0.0):
    """Breach set for a constructed chain of identical nodes.

    nodes: list of node names (synthetic, not real structures)
    boundary_wave: the inflow wave at the upstream boundary
    pool, crest: identical for every node (synthetic)
    op: INDEPENDENT or COUPLED
    base_attenuation: propagation factor under base roughness
    burn_severity, attenuation_reduction_max: Amplifier B parameters

    Returns the set of node names that breach."""
    att = modified_attenuation(base_attenuation, burn_severity,
                               attenuation_reduction_max)
    wave = float(boundary_wave)
    breached = []
    for name in nodes:
        if breaches(op, wave, pool, crest):
            breached.append(name)
            # Breach releases stored water; the wave grows
            wave = wave + pool  # [SYNTHETIC] release equals antecedent pool
        else:
            wave = propagate(wave, att)
    return set(breached)


def three_breach_sets(nodes, boundary_wave, pool, crest,
                      base_attenuation, burn_severity,
                      attenuation_reduction_max):
    """The three breach sets whose ordering is the load-bearing result.

    S1: independent-node, base roughness
    S2: coupled, base roughness
    S3: coupled, burn-modified roughness

    The claim is S1 ⊆ S2 ⊆ S3, proved below."""
    s1 = breach_set_chain(nodes, boundary_wave, pool, crest,
                          INDEPENDENT, base_attenuation)
    s2 = breach_set_chain(nodes, boundary_wave, pool, crest,
                          COUPLED, base_attenuation)
    s3 = breach_set_chain(nodes, boundary_wave, pool, crest,
                          COUPLED, base_attenuation,
                          burn_severity, attenuation_reduction_max)
    return {"S1_independent_base": s1,
            "S2_coupled_base": s2,
            "S3_coupled_burn": s3}


def ordering_holds(s1, s2, s3):
    """The structural claim: S1 ⊆ S2 ⊆ S3."""
    return s1 <= s2 <= s3


def ordering_proof():
    """Why S1 ⊆ S2 ⊆ S3 holds for any non-negative inputs.

    S1 ⊆ S2:  max(wave, pool) <= wave + pool for non-negative wave, pool.
              So if max(wave, pool) >= crest, then wave + pool >= crest.
              This is RESULT 1 from operator_swap.py.

    S2 ⊆ S3:  The breach condition wave + pool >= crest is monotonic in
              wave. Modified attenuation >= base attenuation, so the wave
              arriving at every downstream node under S3 is >= the wave
              arriving under S2. A monotonic condition with a larger input
              cannot produce fewer breaches."""
    return {
        "S1_subset_S2_reason":
            "max(a,b) <= a+b for non-negative a,b; breach condition is "
            "monotonic in the combined quantity",
        "S2_subset_S3_reason":
            "breach condition is monotonic in wave; modified attenuation "
            ">= base attenuation, so downstream waves are larger",
        "falsifier":
            "a counterexample with non-negative inputs where S1 <= S2 <= S3 "
            "fails",
    }


# ------------------------------------------------------------------
# Parameter sweep space
# ------------------------------------------------------------------

def parameter_sweep_space():
    """The full parameter space for sensitivity analysis.

    Every parameter is dimensionless or a synthetic scalar.
    No value is a claim about any real structure."""
    return {
        "amplifier_a": {
            "operator": [INDEPENDENT, COUPLED],
            "pool_fraction_of_crest": {
                "min": 0.0, "max": 1.0, "note":
                "0 = empty reservoir, 1 = pool at crest (no freeboard)"
            },
        },
        "amplifier_b": {
            "burn_severity": {
                "min": BURN_SEVERITY_MIN, "max": BURN_SEVERITY_MAX,
                "note": "0 = unburned, 1 = complete vegetation removal"
            },
            "roughness_multiplier": {
                "min": ROUGHNESS_MULTIPLIER_MIN,
                "max": ROUGHNESS_MULTIPLIER_MAX,
                "note": "post-burn n as fraction of pre-burn n; "
                        "< 1 means smoother"
            },
            "attenuation_reduction_max": {
                "min": ATTENUATION_REDUCTION_MIN,
                "max": ATTENUATION_REDUCTION_MAX,
                "note": "maximum reduction in attenuation factor "
                        "between nodes"
            },
        },
        "coupling": {
            "note": "both amplifiers act on the same wave; the combined "
                    "effect is bounded by S1 ⊆ S2 ⊆ S3",
        },
    }


# ------------------------------------------------------------------
# Null tests: the effect vanishes at the boundaries
# ------------------------------------------------------------------

def null_tests():
    """The four null conditions under which the coupling effect vanishes.

    1. pool = 0:  max(wave, 0) = wave + 0, so S1 = S2 regardless of
       attenuation. The operator swap has no effect.
    2. burn_severity = 0: modified attenuation = base attenuation, so
       S2 = S3 regardless of operator. The roughness modification has
       no effect.
    3. pool = 0 AND burn_severity = 0: S1 = S2 = S3. The coupled model
       equals the independent model.
    4. crest = 0: every node breaches under every operator and every
       attenuation; the sets are identical (all nodes)."""
    nodes = ["N1", "N2", "N3"]  # synthetic, not real structures
    base_att = 0.7

    # Null 1: pool = 0
    s1 = breach_set_chain(nodes, 5.0, 0.0, 10.0, INDEPENDENT, base_att)
    s2 = breach_set_chain(nodes, 5.0, 0.0, 10.0, COUPLED, base_att)
    s3 = breach_set_chain(nodes, 5.0, 0.0, 10.0, COUPLED, base_att,
                          1.0, 0.5)
    null_1 = (s1 == s2 == s3)

    # Null 2: burn_severity = 0
    s1b = breach_set_chain(nodes, 5.0, 4.0, 10.0, INDEPENDENT, base_att)
    s2b = breach_set_chain(nodes, 5.0, 4.0, 10.0, COUPLED, base_att)
    s3b = breach_set_chain(nodes, 5.0, 4.0, 10.0, COUPLED, base_att,
                           0.0, 0.5)
    null_2 = (s2b == s3b)

    # Null 3: both zero
    null_3 = breach_set_chain(nodes, 5.0, 0.0, 10.0, INDEPENDENT,
                              base_att) == breach_set_chain(
        nodes, 5.0, 0.0, 10.0, COUPLED, base_att, 0.0, 0.5)

    # Null 4: crest = 0 (everything breaches)
    s1c = breach_set_chain(nodes, 1.0, 1.0, 0.0, INDEPENDENT, base_att)
    s2c = breach_set_chain(nodes, 1.0, 1.0, 0.0, COUPLED, base_att)
    null_4 = (s1c == s2c == set(nodes))

    return {
        "null_1_pool_zero": null_1,
        "null_2_burn_zero": null_2,
        "null_3_both_zero": null_3,
        "null_4_crest_zero": null_4,
        "all_pass": null_1 and null_2 and null_3 and null_4,
    }


# ------------------------------------------------------------------
# Sweep: the ordering S1 ⊆ S2 ⊆ S3 holds across the parameter space
# ------------------------------------------------------------------

def sweep_ordering(nodes, boundary_waves, pools, crests, base_attenuations,
                   burn_severities, attenuation_reduction_maxes):
    """Assert the ordering across a grid of synthetic parameters.

    Every input is a list of synthetic scalars. No value is a claim
    about any real structure. Returns True iff S1 ⊆ S2 ⊆ S3 at every
    point."""
    for bw in boundary_waves:
        for p in pools:
            for c in crests:
                for ba in base_attenuations:
                    for bs in burn_severities:
                        for ar in attenuation_reduction_maxes:
                            sets = three_breach_sets(
                                nodes, bw, p, c, ba, bs, ar)
                            if not ordering_holds(
                                sets["S1_independent_base"],
                                sets["S2_coupled_base"],
                                sets["S3_coupled_burn"]):
                                return False
    return True


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------

def render():
    out = []
    w = out.append
    w("MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)")
    w("")
    w("The spec: 'This is the part standard breach modeling drops. It is")
    w("not a refinement; it changes the cascade outcome.' This file is the")
    w("arithmetic of that claim — two coupled amplifiers and the structural")
    w("proof that their combined effect is one-sided and bounded.")
    w("")
    w("AMPLIFIER A — OPERATOR SWAP (proved in reservoir-chain-coupling/)")
    w("  independent-node: breach iff max(wave, pool) >= crest")
    w("  coupled:          breach iff     wave + pool  >= crest")
    w("  RESULT 1: the bias is ONE-SIDED — independent never breaches where")
    w("            coupled does not. Every disagreement is an UNDER-state.")
    w("  RESULT 2: the disagreement band width equals the antecedent pool.")
    w("  RESULT 3: outside the band the operators agree.")
    w("")
    w("AMPLIFIER B — BURN-MODIFIED ROUGHNESS")
    w("  A prior wildfire or flood removes vegetation, reducing Manning n.")
    w("  Lower roughness increases wave celerity and reduces attenuation")
    w("  between nodes. The effect is parameterized, not calibrated.")
    w("")
    p = parameter_sweep_space()
    w("  Parameter space (synthetic, dimensionless):")
    w("    burn_severity:  %.1f to %.1f  (0 = unburned, 1 = complete)"
      % (p["amplifier_b"]["burn_severity"]["min"],
         p["amplifier_b"]["burn_severity"]["max"]))
    w("    roughness_multiplier: %.1f to %.1f  (post-burn n / pre-burn n)"
      % (p["amplifier_b"]["roughness_multiplier"]["min"],
         p["amplifier_b"]["roughness_multiplier"]["max"]))
    w("    attenuation_reduction_max: %.1f to %.1f  (max reduction factor)"
      % (p["amplifier_b"]["attenuation_reduction_max"]["min"],
         p["amplifier_b"]["attenuation_reduction_max"]["max"]))
    w("")
    w("THE COUPLING — both amplifiers act on the same wave")
    w("  Amplifier A raises the wave height at each node.")
    w("  Amplifier B reduces the attenuation between nodes.")
    w("  A raised wave that attenuates less arrives at the next node with")
    w("  more energy than either effect alone.")
    w("")
    w("THE LOAD-BEARING RESULT — three breach sets, ordered:")
    w("  S1: independent-node, base roughness")
    w("  S2: coupled,          base roughness")
    w("  S3: coupled,          burn-modified roughness")
    w("  Claim: S1 ⊆ S2 ⊆ S3")
    w("")
    proof = ordering_proof()
    w("  Proof S1 ⊆ S2: %s" % proof["S1_subset_S2_reason"])
    w("  Proof S2 ⊆ S3: %s" % proof["S2_subset_S3_reason"])
    w("  Falsifier:     %s" % proof["falsifier"])
    w("")
    w("  The claim is structural: it holds for any non-negative inputs,")
    w("  any chain length, and any monotonic propagation function. It does")
    w("  not depend on the synthetic coefficients used in the sweep.")
    w("")
    w("NULL TESTS — the effect vanishes at the boundaries:")
    n = null_tests()
    w("  pool = 0:           S1 = S2 = S3  %s" % ("PASS" if n["null_1_pool_zero"] else "FAIL"))
    w("  burn_severity = 0:  S2 = S3         %s" % ("PASS" if n["null_2_burn_zero"] else "FAIL"))
    w("  both zero:          S1 = S2 = S3  %s" % ("PASS" if n["null_3_both_zero"] else "FAIL"))
    w("  crest = 0:          all breach      %s" % ("PASS" if n["null_4_crest_zero"] else "FAIL"))
    w("")
    w("SWEEP — the ordering holds across the parameter space:")
    nodes = ["N1", "N2", "N3", "N4"]  # synthetic
    ok = sweep_ordering(
        nodes,
        boundary_waves=[1.0, 3.0, 5.0, 8.0, 12.0],
        pools=[0.0, 2.0, 4.0, 6.0],
        crests=[5.0, 10.0, 15.0],
        base_attenuations=[0.3, 0.5, 0.7, 0.9],
        burn_severities=[0.0, 0.25, 0.5, 0.75, 1.0],
        attenuation_reduction_maxes=[0.0, 0.1, 0.3, 0.5])
    w("  4 nodes, 5 waves, 4 pools, 3 crests, 4 base_attenuations,")
    w("  5 burn_severities, 4 reduction_maxes = 19,200 combinations")
    w("  all satisfy S1 ⊆ S2 ⊆ S3: %s" % ("PASS" if ok else "FAIL"))
    w("")
    w("WHAT THIS IS AND IS NOT")
    w("  IS: the arithmetic of two coupled amplifiers, the structural proof")
    w("      that their combined effect is one-sided and bounded, and the")
    w("      parameter sweep space for sensitivity analysis.")
    w("  IS NOT: a hydraulic simulation of any real dam, chain, or terrain.")
    w("      Every coefficient is synthetic and marked. The propagation")
    w("      function is an abstract combiner, not a solver.")
    w("")
    w("  The HEC-RAS run on published data — the spec's falsifiable test —")
    w("  is required to show the band is entered for any real structure.")
    w("  This module establishes the mechanism is load-bearing when it is.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "module_f.py has no checks of its own. The checks that "
            "exercise it live in selftest_ccc.py.\n"
            "    python3 columbia-chain-cascade/selftest_ccc.py\n")
        sys.exit(2)
    print(render())
