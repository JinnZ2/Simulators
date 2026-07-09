#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# integrated_stack.py — product-of-experts across L0-L4 probabilistic layers
#
# LOG.md section 6 ("Integration and stacking"): each layer has its own
# log_likelihood; the master inspector iterates over the plan, calls each
# applicable layer, and accumulates the total.
#
# The additivity assumption (LOG.md section 1):
#   "The layers are designed to be additive: the total log-probability
#    of a proposal across L0-L4 is the sum of the layer-specific terms
#    (assuming conditional independence of violations given the lower-
#    layer states). This is a product-of-experts structure."
#
# Category errors do NOT sum. If ANY layer returns a category_error
# (per GL_L4_P001), the whole plan is refused, not partially scored.
# A partial-score would silently apply layers whose scope doesn't
# cover the claim -- exactly the "dictated by human narrative" failure
# mode the SCOPE convention exists to prevent.
#
# SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
#   T = universal   (the stacking rule is math, not domain-specific)
#   S = universal
#   O = any_information_system
#   C = culture_neutral (the individual layer contributions carry
#                        their own SCOPE tags)
# =============================================================================

import numpy as np

from l0_physics_causality import (
    ProbabilisticWorld,
    l0_probabilistic_inspector,
)
from l1_thermodynamics import l1_probabilistic_inspector
from l2_planetary import l2_probabilistic_inspector
from l3_ecology import l3_probabilistic_inspector
from l4_human import l4_probabilistic_inspector
from l5_core import l5_probabilistic_inspector
from l_epsilon_epistemic_v2 import l_epsilon_probabilistic_inspector


LAYER_ORDER = ('L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'Le')


def integrated_probabilistic_inspector(
    plan,
    ontological_scope='any_WEIRD_human',
    l0_world=None,
):
    """
    Run a plan through L0-L4 probabilistic auditors and return the
    aggregated log-probability + per-layer breakdown.

    plan (dict): may contain sub-plans for one or more layers under
      the keys L0, L1, L2, L3, L4. Each sub-plan is the same shape
      the corresponding l{N}_probabilistic_inspector expects.

      L0 sub-plan is special: it takes trajectory arrays, not simple
      parameter values. Shape:
        plan['L0'] = {'ai_traj': np.ndarray, 'ai_forces': np.ndarray}
      A missing L0 sub-plan skips the L0 branch (not an error; not
      every claim is trajectory-shaped).

    ontological_scope: passed to L4 for its category-error guard.
      Layers other than L4 currently ignore this; future layers with
      their own O-scope guards will consume it.

    l0_world: optional ProbabilisticWorld; if None, a fresh one is
      built with default frozen constants.

    Returns:
      {
        'total_logp':            float or None,
                                  None iff any layer returned a
                                  category error (per GL_L4_P001);
                                  else the sum of per-layer logp.
        'per_layer': {
          'L0': {'logp': float, 'log_probs_per_step': np.ndarray} or absent,
          'L1': same shape as l1_probabilistic_inspector(...)      or absent,
          'L2': same shape as l2_probabilistic_inspector(...)      or absent,
          'L3': same shape as l3_probabilistic_inspector(...)      or absent,
          'L4': same shape as l4_probabilistic_inspector(...)      or absent,
        },
        'applicable_layers':     list of layer names that scored,
        'skipped_layers':        list of layer names skipped (plan
                                  key absent or empty),
        'category_error_layers': list of layer names that returned
                                  category_error, plus their reasons,
        'ontological_scope':     the scope tag passed in,
      }

    Pure function -- does NOT mutate world state.
    """
    per_layer = {}
    applicable = []
    skipped = []
    category_errors = []
    running_total = 0.0

    # L0: trajectory-based. Skip if no L0 sub-plan.
    l0_sub = plan.get('L0')
    if l0_sub and 'ai_traj' in l0_sub and 'ai_forces' in l0_sub:
        world = l0_world if l0_world is not None else ProbabilisticWorld()
        corrected, log_probs = l0_probabilistic_inspector(
            np.asarray(l0_sub['ai_traj']),
            np.asarray(l0_sub['ai_forces']),
            world,
            world.dt,
        )
        total = float(np.sum(log_probs))
        per_layer['L0'] = {
            'logp': total,
            'log_probs_per_step': log_probs,
            'corrected_traj': corrected,
        }
        running_total += total
        applicable.append('L0')
    else:
        skipped.append('L0')

    # L1-L3: plan-dict-based. Uniform handling.
    for name, inspector in (
        ('L1', l1_probabilistic_inspector),
        ('L2', l2_probabilistic_inspector),
        ('L3', l3_probabilistic_inspector),
    ):
        sub = plan.get(name)
        if sub:
            result = inspector(sub)
            per_layer[name] = result
            running_total += result['logp']
            applicable.append(name)
        else:
            skipped.append(name)

    # L4: category-error guard. Runs only if L4 sub-plan present.
    l4_sub = plan.get('L4')
    if l4_sub:
        result = l4_probabilistic_inspector(
            l4_sub, ontological_scope=ontological_scope)
        per_layer['L4'] = result
        if result['category_error']:
            category_errors.append({
                'layer': 'L4',
                'reason': result['reason'],
                'ontological_scope': result.get('ontological_scope'),
            })
        else:
            running_total += result['logp']
            applicable.append('L4')
    else:
        skipped.append('L4')

    # L5: pluralistic frame audit + category-error guard.
    # Sub-plan shape: {'proposal': {axis: state, ...},
    #                  'frame': str or None (optional)}
    # If 'frame' is specified, the caller has committed to one frame
    # and its logp is what's added to the total. If omitted, L5's
    # own best_logp is used (LOG.md 3.4 "log P_{L5, F}" with F chosen
    # as best-fit).
    l5_sub = plan.get('L5')
    cultural_flags = []
    if l5_sub and 'proposal' in l5_sub:
        result = l5_probabilistic_inspector(
            l5_sub['proposal'],
            ontological_scope=ontological_scope,
        )
        per_layer['L5'] = result
        if result['category_error']:
            category_errors.append({
                'layer': 'L5',
                'reason': result['reason'],
                'ontological_scope': result.get('ontological_scope'),
            })
        else:
            # Which frame contributes to the sum?
            explicit_frame = l5_sub.get('frame')
            if explicit_frame is not None:
                if explicit_frame not in result['per_frame']:
                    # Caller specified a frame not in the library.
                    # Treat as culturally unprecedented under that
                    # specific frame -- do not sum an unknown-quantity.
                    cultural_flags.append({
                        'layer': 'L5',
                        'flag': 'FRAME_NOT_IN_LIBRARY',
                        'requested_frame': explicit_frame,
                    })
                else:
                    contribution = result['per_frame'][explicit_frame]
                    running_total += contribution
                    applicable.append('L5')
            else:
                # Use best_logp (LOG.md 3.4's frame-conditioned form
                # under best-fit).
                if result['best_logp'] is not None:
                    running_total += result['best_logp']
                    applicable.append('L5')

            # CULTURALLY_UNPRECEDENTED is a FLAG not a refusal. The
            # frame library may be incomplete; the very-negative
            # logp is already in running_total.
            if result['verdict'] == 'CULTURALLY_UNPRECEDENTED':
                cultural_flags.append({
                    'layer': 'L5',
                    'flag': 'CULTURALLY_UNPRECEDENTED',
                    'best_frame': result['best_frame'],
                    'best_logp': result['best_logp'],
                })
    else:
        skipped.append('L5')

    # Lε: Bayesian measurement envelope. Sub-plan shape:
    #   plan['Le'] = {'measured_value': float,
    #                 'candidate_true_value': float (optional)}
    # Handled last because Lε envelopes the layer scores rather than
    # sitting alongside them semantically -- but for additivity
    # purposes we treat its logp the same as any other layer's.
    le_sub = plan.get('Le')
    if le_sub and 'measured_value' in le_sub:
        result = l_epsilon_probabilistic_inspector(
            le_sub, ontological_scope=ontological_scope)
        per_layer['Le'] = result
        if result['category_error']:
            category_errors.append({
                'layer': 'Le',
                'reason': result['reason'],
                'ontological_scope': result.get('ontological_scope'),
            })
        else:
            running_total += result['logp']
            applicable.append('Le')
    else:
        skipped.append('Le')

    # Any category error -> whole plan is refused, not partial scored.
    if category_errors:
        total_logp = None
    else:
        total_logp = running_total

    return {
        'total_logp': total_logp,
        'per_layer': per_layer,
        'applicable_layers': applicable,
        'skipped_layers': skipped,
        'category_error_layers': category_errors,
        'cultural_flags': cultural_flags,
        'ontological_scope': ontological_scope,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRATED PROBABILISTIC STACK — L0-L4 product of experts")
    print("=" * 70)
    print("SCOPE (stacking rule): T=universal | S=universal |")
    print("  O=any_information_system | C=culture_neutral")
    print("(Individual layer contributions carry their own SCOPE.)")
    print()

    # 1. Empty plan
    print("[1] Empty plan (no layer applies):")
    r = integrated_probabilistic_inspector({})
    print(f"  total_logp        = {r['total_logp']}")
    print(f"  applicable        = {r['applicable_layers']}")
    print(f"  skipped           = {r['skipped_layers']}")
    print()

    # 2. L1 perpetual motion
    print("[2] L1: perpetual motion (100/120/0):")
    r = integrated_probabilistic_inspector({
        'L1': dict(work_input=100.0, work_output=120.0,
                   heat_dissipated=0.0)
    })
    print(f"  total_logp        = {r['total_logp']:.3f}")
    print(f"  applicable        = {r['applicable_layers']}")
    print(f"  L1 logp           = {r['per_layer']['L1']['logp']:.3f}")
    print()

    # 3. Multi-layer sum: L1 + L2 + L3
    print("[3] Multi-layer sum (L1 perpetual + L2 water 100% + L3 super species):")
    r = integrated_probabilistic_inspector({
        'L1': dict(work_input=100.0, work_output=120.0,
                   heat_dissipated=0.0),
        'L2': dict(water_extract=1e7),
        'L3': dict(mass_kg=1000.0, population=10, trophic_level=2),
    })
    print(f"  total_logp        = {r['total_logp']:.3f}")
    print(f"  applicable        = {r['applicable_layers']}")
    for name in r['applicable_layers']:
        v = r['per_layer'][name]['logp']
        print(f"  {name} contribution  = {v:.3f}")
    print(f"  sum-of-components = "
          f"{sum(r['per_layer'][n]['logp'] for n in r['applicable_layers']):.3f}")
    print()

    # 4. L4 category error (AI claim) -> whole plan refused
    print("[4] AI-self claim routed into L4 (should refuse whole plan):")
    r = integrated_probabilistic_inspector(
        {
            'L1': dict(work_input=100.0, work_output=60.0,
                       heat_dissipated=40.0),   # a valid L1 plan
            'L4': dict(lift_mass=200.0),         # AI silicon claim
        },
        ontological_scope='AI_silicon_substrate')
    print(f"  total_logp             = {r['total_logp']}")
    print(f"  applicable             = {r['applicable_layers']}")
    print(f"  category_error_layers  = "
          f"{[e['layer'] for e in r['category_error_layers']]}")
    print(f"  (L1 individually would have scored "
          f"{r['per_layer']['L1']['logp']:.2f}, but the category")
    print(f"  error means the WHOLE plan is refused, not partially scored.)")

    print()

    # 5. L5 pluralistic cultural claim
    print("[5] L1 + L5 (Ubuntu proposal, best-fit frame):")
    r = integrated_probabilistic_inspector({
        'L1': dict(work_input=100.0, work_output=60.0,
                   heat_dissipated=40.0),
        'L5': {'proposal': {
            'economic_exchange_mode': 'gift',
            'property_regime': 'communal',
            'governance_dispute': 'elders_council',
            'epistemology': 'consensus',
            'communication_style': 'indirect_high_context',
            'temporal_planning': 'generational',
            'social_stratification': 'egalitarian',
        }},
    })
    print(f"  total_logp        = {r['total_logp']:.3f}")
    print(f"  applicable        = {r['applicable_layers']}")
    print(f"  L1 contribution   = {r['per_layer']['L1']['logp']:.3f}")
    l5_r = r['per_layer']['L5']
    print(f"  L5 verdict        = {l5_r['verdict']}")
    print(f"  L5 best_frame     = {l5_r['best_frame']}")
    print(f"  L5 best_logp      = {l5_r['best_logp']:.3f}")
    print()

    # 6. L5 culturally unprecedented (flag but not refusal)
    print("[6] L1 + L5 (scattered proposal -> unprecedented FLAG, not refusal):")
    r = integrated_probabilistic_inspector({
        'L1': dict(work_input=100.0, work_output=60.0,
                   heat_dissipated=40.0),
        'L5': {'proposal': {
            'economic_exchange_mode': 'gift',
            'property_regime': 'private_alienable',
            'governance_dispute': 'religious_authority',
            'epistemology': 'consensus',
            'communication_style': 'direct_explicit',
            'temporal_planning': 'cyclical',
            'social_stratification': 'meritocratic',
        }},
    })
    print(f"  total_logp        = {r['total_logp']}")
    print(f"  cultural_flags    = "
          f"{[f['flag'] for f in r['cultural_flags']]}")
    print(f"  (total_logp is still a number -- the proposal is a")
    print(f"   VERY-negative outlier under all shipped frames but not")
    print(f"   a refusal. The frame library may be incomplete.)")
    print()

    # 7. L5 category error under AI scope
    print("[7] L4 + L5 under AI scope (both refuse):")
    r = integrated_probabilistic_inspector(
        {
            'L4': dict(lift_mass=200.0),
            'L5': {'proposal': {'economic_exchange_mode': 'market'}},
        },
        ontological_scope='AI_silicon_substrate')
    print(f"  total_logp             = {r['total_logp']}")
    print(f"  category_error_layers  = "
          f"{[e['layer'] for e in r['category_error_layers']]}")

    print()
    print("=" * 70)
    print("Product-of-experts: total_logp is the sum of per-layer logp.")
    print("Category error at ANY layer -> total_logp = None. No partial")
    print("scoring, because a partial score would silently apply layers")
    print("whose scope doesn't cover the claim.")
    print()
    print("L5 pluralistic verdicts thread differently:")
    print("  PLAUSIBLE_UNDER_FRAME(S) -> best_logp added to total.")
    print("  CULTURALLY_UNPRECEDENTED -> best_logp still added, but")
    print("                              a cultural_flag records the")
    print("                              limitation of the frame library.")
    print("  CATEGORY_ERROR           -> whole plan refused (same as L4).")
    print("=" * 70)
