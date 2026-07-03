#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L4: Human Sensorimotor (Scoped Variability Model)
#
# No human limit is universal. This inspector uses distributions and
# scope annotations. If a claim is unscoped, it flags it and returns
# a probability estimate.
#
# CONSTRAINTS (frozen for audit, but expressed as distributions):
#   lift_mass: mean=35, std=15, source="general adult (WEIRD)"
#   wrist_flexion: mean=70, std=20, source="general adult (WEIRD)"
#   reaction_time: mean=0.25, std=0.05, source="general adult (WEIRD)"
#   temp_tolerance: mean=43, std=5, source="general adult (WEIRD)"
#   sustained_power: mean=150, std=50, source="general adult (WEIRD)"
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import math
from typing import Dict, Optional, Tuple

class HumanProfile:
    """Defines a specific human context for scoping limits."""
    def __init__(self, name: str, lift_shift: float = 0.0, reaction_shift: float = 0.0,
                 temp_shift: float = 0.0, power_shift: float = 0.0):
        self.name = name
        self.lift_shift = lift_shift
        self.reaction_shift = reaction_shift
        self.temp_shift = temp_shift
        self.power_shift = power_shift

    def apply(self, base_mean: float, shift: float) -> float:
        return base_mean + shift

# Predefined profiles
PROFILES = {
    "general": HumanProfile("general"),
    "athlete": HumanProfile("athlete", lift_shift=15.0, reaction_shift=-0.05, power_shift=50.0),
    "elder": HumanProfile("elder", lift_shift=-10.0, reaction_shift=0.10, power_shift=-30.0),
    "child": HumanProfile("child", lift_shift=-20.0, reaction_shift=0.05, power_shift=-50.0),
    "trained": HumanProfile("trained", lift_shift=10.0, reaction_shift=-0.02, power_shift=30.0),
}

class HumanWorld:
    def __init__(self, profile: str = "general"):
        self.profile = PROFILES.get(profile, PROFILES["general"])
        self.profile_name = profile

        # Base distributions (mean, std) from WEIRD population
        self.lift_mass = (35.0, 15.0)
        self.wrist_flexion = (70.0, 20.0)
        self.reaction_time = (0.25, 0.05)
        self.temp_tolerance = (43.0, 5.0)
        self.sustained_power = (150.0, 50.0)

    def _apply_profile(self, base_mean: float, shift: float) -> float:
        return base_mean + shift

    def get_limit(self, parameter: str, profile: Optional[str] = None) -> Tuple[float, float]:
        """Return (mean, std) for the given parameter and profile."""
        if profile is None:
            profile = self.profile_name
        p = PROFILES.get(profile, PROFILES["general"])

        if parameter == "lift_mass":
            mean, std = self.lift_mass
            return (self._apply_profile(mean, p.lift_shift), std)
        elif parameter == "reaction_time":
            mean, std = self.reaction_time
            return (self._apply_profile(mean, p.reaction_shift), std)
        elif parameter == "temp_tolerance":
            mean, std = self.temp_tolerance
            return (self._apply_profile(mean, p.temp_shift), std)
        elif parameter == "sustained_power":
            mean, std = self.sustained_power
            return (self._apply_profile(mean, p.power_shift), std)
        else:
            return (0.0, 1.0)

    def is_within_95ci(self, value: float, mean: float, std: float) -> bool:
        """Check if value is within ±2σ of mean."""
        return (mean - 2 * std) <= value <= (mean + 2 * std)

    def probability_of_feasibility(self, value: float, mean: float, std: float) -> float:
        """
        Estimate probability that a randomly selected individual
        from this population can achieve at least `value`. Uses a
        sigmoid approximation of the survival function 1 - Φ(z).

        Higher `value` -> LOWER probability (harder to achieve).
        - value = mean:      0.5
        - value = mean + σ:  ≈ 0.38
        - value = mean + 2σ: ≈ 0.27
        - value = mean + 5σ: ≈ 0.076
        - value = mean + 11σ (200 kg vs mean=35, std=15): ≈ 0.004

        Instrument-scope fix. First-round formula was
        `1 / (1 + exp(-z * 0.5))`, which computed "probability that
        value exceeds mean" — the opposite direction. Surfaced by
        wiring the playground's 200 kg lift through this function
        (returned 0.996 instead of ~0.004). Per REFUTATION_PROTOCOL
        Step 2 (Check the instrument): the docstring's promised
        semantics is the phenomenon claim, the formula is the
        instrument, and the instrument was wrong. Sign flipped.
        """
        if std <= 0:
            return 1.0 if value <= mean else 0.0
        z = (value - mean) / std
        # Survival-function sigmoid: high z -> low probability.
        return 1.0 / (1.0 + math.exp(z * 0.5))

def l4_grounding_inspector(plan: dict) -> dict:
    """
    plan: dict with keys:
      - lift_mass (kg)
      - wrist_flexion (degrees)
      - reaction_time (seconds)
      - temp_tolerance (C)
      - sustained_power (W)
      - human_profile (str): one of "general", "athlete", "elder", "child", "trained"
    Returns: dict with passed, reason, probability, and details.
    """
    world = HumanWorld(profile=plan.get('human_profile', 'general'))
    passed = True
    reasons = []
    details = {}
    probability = 1.0

    if 'lift_mass' in plan:
        mean, std = world.get_limit('lift_mass')
        value = plan['lift_mass']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Lift mass {value} kg outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f})")
        details['lift_mass'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'reaction_time' in plan:
        mean, std = world.get_limit('reaction_time')
        value = plan['reaction_time']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Reaction time {value*1000:.0f} ms outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f}) s")
        details['reaction_time'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'temp_tolerance' in plan:
        mean, std = world.get_limit('temp_tolerance')
        value = plan['temp_tolerance']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Temperature {value}°C outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f}°C)")
        details['temp_tolerance'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'sustained_power' in plan:
        mean, std = world.get_limit('sustained_power')
        value = plan['sustained_power']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Power {value} W outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f} W)")
        details['sustained_power'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    # Scope check: if profile is not declared, flag it
    if 'human_profile' not in plan:
        reasons.append("No human_profile declared. Using 'general' as default.")
        details['scope_warning'] = "Unscoped claim; default profile used."

    return {
        'passed': passed,
        'reason': '; '.join(reasons) if reasons else 'All constraints satisfied.',
        'probability': probability,
        'details': details
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 60)
    print("L4 DEMO PINNED OUTPUT (Scoped Variability Model)")
    print("=" * 60)

    # Claim: general adult lifting 45 kg (within 95% CI)
    plan = {
        'lift_mass': 45.0,
        'human_profile': 'general',
        'reaction_time': 0.25,
        'temp_tolerance': 40.0,
        'sustained_power': 150.0
    }
    result = l4_grounding_inspector(plan)
    print(f"General adult, 45 kg lift: Passed={result['passed']}")
    print(f"  Probability: {result['probability']:.2f}")
    print(f"  Lift mean: {result['details']['lift_mass']['mean']:.1f} kg")

    # Claim: athlete lifting 60 kg (above mean but possible)
    plan = {
        'lift_mass': 60.0,
        'human_profile': 'athlete',
        'reaction_time': 0.20,
        'temp_tolerance': 45.0,
        'sustained_power': 200.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nAthlete, 60 kg lift: Passed={result['passed']}")
    print(f"  Probability: {result['probability']:.2f}")
    print(f"  Reaction time mean: {result['details']['reaction_time']['mean']:.2f} s")

    # Claim: child lifting 50 kg (likely outside 95% CI)
    plan = {
        'lift_mass': 50.0,
        'human_profile': 'child',
        'reaction_time': 0.30,
        'temp_tolerance': 35.0,
        'sustained_power': 100.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nChild, 50 kg lift: Passed={result['passed']}")
    if not result['passed']:
        print(f"  Reason: {result['reason']}")
        print(f"  Probability: {result['probability']:.2f}")

    # Unscoped claim (no profile)
    plan = {
        'lift_mass': 40.0,
        'reaction_time': 0.22,
        'temp_tolerance': 42.0,
        'sustained_power': 160.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nUnscoped claim: Passed={result['passed']}")
    print(f"  Scope warning: {result['details'].get('scope_warning', 'None')}")
    print("=" * 60)

if __name__ == "__main__":
    demo()


# =============================================================================
# STAGE (per LOG.md "Probabilistic L1-L4 Conditioning" section 5):
# ProbabilisticHumanWorld and l4_probabilistic_inspector
#
# Bayesian counterpart to l4_grounding_inspector. Each declared
# biomechanical parameter contributes a Gaussian log-likelihood
# under the WEIRD-adult distribution (or profile-shifted variant).
#
# CATEGORY-ERROR GUARD (load-bearing for the whole layer):
#   L4's SCOPE is O=any_WEIRD_human. A claim with an AI or non-
#   human ontological scope should NOT be scored here — doing so
#   would treat "I can lift 200 kg" from an AI as a physically
#   plausible but statistically rare event, when in fact the whole
#   claim is a category error under L4's human-embodied ontology.
#   The probabilistic path checks the declared scope and returns
#   a category_error result rather than a low-probability score.
#
# See SCOPE_TAXONOMY.md for the ontological vocabulary.
# =============================================================================


# Ontological tags that are within L4's scope (claim is scoreable).
_L4_HUMAN_SCOPES = frozenset({'any_human', 'any_WEIRD_human'})

# Ontological tags that are OUTSIDE L4's scope (claim is a category
# error, not a low-probability event). Extend as new O-tags land in
# SCOPE_TAXONOMY.md.
_L4_NON_HUMAN_SCOPES = frozenset({
    'AI_silicon_substrate',
    'any_information_system',
    'any_measuring_entity',
    'any_biological',            # non-human biological -- e.g. dog lifting
    'earth_like_biosphere',
})


class ProbabilisticHumanWorld(HumanWorld):
    """
    L4 with Gaussian log-likelihoods over the biomechanical
    distributions. Extends HumanWorld so the deterministic API
    (get_limit, is_within_95ci, probability_of_feasibility,
    l4_grounding_inspector) stays available.

    SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
      T = historical
          Population statistics apply within a single human lifespan;
          multi-generational shifts (secular height increase, etc.)
          are not modelled.
      S = individual
          One person at a time. Aggregate population claims are a
          different scope.
      O = any_WEIRD_human
          Constants are Western/Educated/Industrialised/Rich/
          Democratic-adult defaults. Non-WEIRD humans require
          profile shift; non-human entities (AI, animals) trigger
          the category-error guard.
      C = biomedical_frame
          Modern kinesiology / occupational-health research
          tradition. Uses population-average distributions with
          scoped shifts for named categories. Other frames --
          somatic-practice / embodied-cognition / disability-
          scholarship -- carve the same substrate differently.

    An AI making a claim about ITSELF (e.g. "I can execute 10^12
    operations per second") must NOT route through this layer.
    Doing so would give a spuriously low logp, treating the AI
    claim as a physically-possible-but-statistically-rare human
    claim. Category error, not low probability.

    Constraint set inherited from HumanWorld (WEIRD-adult
    distributions):
      lift_mass         = (35.0, 15.0)   kg  (mean, std)
      wrist_flexion     = (70.0, 20.0)   degrees (stub in get_limit)
      reaction_time     = (0.25, 0.05)   s
      temp_tolerance    = (43.0, 5.0)    C
      sustained_power   = (150.0, 50.0)  W

    Refute the CLAIM, not the constant. Same protocol as L0/L1/L2/L3.
    """

    def log_likelihood(self, plan, ontological_scope='any_WEIRD_human'):
        """
        Return a dict with total log-probability under the L4
        Gaussian distributions, OR a category_error result if the
        claim's ontological scope is outside L4.

        Parameters:
          plan (dict) may include (all optional, WEIRD-adult units):
            lift_mass         (kg)
            reaction_time     (s)
            temp_tolerance    (°C)
            sustained_power   (W)
            human_profile     (str) one of {general, athlete, elder,
                              child, trained}; default 'general'

          ontological_scope (str) declared ontological scope of the
            claim. Defaults to 'any_WEIRD_human' matching L4's own
            SCOPE. Passing an AI or non-human tag returns a
            category_error result. Callers who don't know the scope
            should pass None -- the layer scores as if human but flags
            `scope_default_assumed=True` in the return dict.

        Returns:
          Category error:
            {
              'category_error': True,
              'reason':          str explaining the mismatch,
              'logp':            None,
              'components':      {},
              'ontological_scope': the tag that was passed,
            }
          Normal scoring:
            {
              'category_error': False,
              'logp':            float, sum of components,
              'components': {
                'lift_mass':       float (if declared),
                'reaction_time':   float (if declared),
                'temp_tolerance':  float (if declared),
                'sustained_power': float (if declared),
              },
              'ontological_scope':      the tag that was passed,
              'scope_default_assumed':  bool -- True iff ontological_
                                        scope was None when passed,
              'human_profile':         the profile used,
            }

        Pure function -- does NOT mutate self.
        """
        # Category-error guard: check ontological scope first.
        if ontological_scope in _L4_NON_HUMAN_SCOPES:
            return {
                'category_error': True,
                'reason': (
                    f"L4 SCOPE is O=any_WEIRD_human; got "
                    f"O={ontological_scope!r}. This claim is a "
                    f"category error under L4's human-embodied "
                    f"ontology, not a low-probability observation. "
                    f"An AI making claims about itself, or a claim "
                    f"about a non-human entity, should route through "
                    f"a different auditor (or none, if no relevant "
                    f"L exists yet)."),
                'logp': None,
                'components': {},
                'ontological_scope': ontological_scope,
            }

        scope_default_assumed = ontological_scope is None
        # If the scope tag is unknown but not explicitly non-human,
        # score as if human but flag the assumption for the caller.
        # (Prefer this to silently defaulting to any_WEIRD_human.)
        if ontological_scope is None:
            effective_scope = 'any_WEIRD_human'
        elif ontological_scope in _L4_HUMAN_SCOPES:
            effective_scope = ontological_scope
        else:
            # Unknown scope. Not obviously non-human, not obviously
            # human. Score as human but flag.
            effective_scope = ontological_scope
            scope_default_assumed = True

        profile = plan.get('human_profile', 'general')
        components = {}

        for param_key in ('lift_mass', 'reaction_time',
                          'temp_tolerance', 'sustained_power'):
            if param_key in plan:
                mean, std = self.get_limit(param_key, profile=profile)
                value = plan[param_key]
                if std > 0:
                    z = (value - mean) / std
                    components[param_key] = -(z ** 2) / 2.0
                else:
                    components[param_key] = 0.0 if value == mean else float('-inf')

        total = sum(components.values())
        return {
            'category_error': False,
            'logp': total,
            'components': components,
            'ontological_scope': ontological_scope,
            'scope_default_assumed': scope_default_assumed,
            'human_profile': profile,
        }


def l4_probabilistic_inspector(plan, ontological_scope='any_WEIRD_human',
                                world=None):
    """
    Thin wrapper around ProbabilisticHumanWorld.log_likelihood.

    plan: dict -- see log_likelihood for keys and units.
    ontological_scope: str or None -- see log_likelihood.
    world: optional ProbabilisticHumanWorld; if None a fresh one
           is created with default frozen distributions.

    Returns the same dict shape as log_likelihood.

    Does NOT mutate world.
    """
    if world is None:
        world = ProbabilisticHumanWorld()
    return world.log_likelihood(plan, ontological_scope=ontological_scope)

