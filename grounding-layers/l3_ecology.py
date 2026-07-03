#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L3: Ecology & Allometry Inspector
#
# Models biological scaling (Kleiber), trophic transfer, carrying capacity,
# and extinction risk.
# CONSTRAINTS (frozen for audit):
#   kleiber_a = 3.0                    (W / kg^0.75)
#   trophic_transfer_efficiency = 0.10 (10% per level)
#   max_trophic_levels = 5
#   minimum_viable_population = 50
#   carrying_capacity_initial = 1000
#   population_growth_rate_max = 0.5
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import math

class EcologicalWorld:
    def __init__(self,
                 kleiber_a=3.0,
                 trophic_transfer_efficiency=0.10,
                 max_trophic_levels=5,
                 minimum_viable_population=50,
                 carrying_capacity_initial=1000,
                 population_growth_rate_max=0.5):
        self.kleiber_a = kleiber_a
        self.trophic_transfer_efficiency = trophic_transfer_efficiency
        self.max_trophic_levels = max_trophic_levels
        self.minimum_viable_population = minimum_viable_population
        self.carrying_capacity_initial = carrying_capacity_initial
        self.population_growth_rate_max = population_growth_rate_max

    def allometric_metabolism(self, mass_kg: float) -> float:
        """Return metabolic rate in Watts according to Kleiber's law."""
        if mass_kg <= 0:
            return 0.0
        return self.kleiber_a * (mass_kg ** 0.75)

    def trophic_energy_available(self, base_energy: float, trophic_level: int) -> float:
        """
        Calculate energy available at a given trophic level.
        base_energy: energy at producer level (J per step)
        trophic_level: 0 = producers, 1 = herbivores, etc.
        """
        if trophic_level < 0:
            return 0.0
        if trophic_level > self.max_trophic_levels:
            return 0.0
        return base_energy * (self.trophic_transfer_efficiency ** trophic_level)

    def carrying_capacity(self, base_energy: float, trophic_level: int, mass_per_individual: float) -> float:
        """
        Estimate carrying capacity at a trophic level.
        Returns the maximum population size sustainable.
        """
        energy_per_individual = self.allometric_metabolism(mass_per_individual)
        if energy_per_individual <= 0:
            return 0.0
        total_energy = self.trophic_energy_available(base_energy, trophic_level)
        return total_energy / energy_per_individual

    def population_growth(self, population: float, carrying_capacity: float, growth_rate: float = None) -> float:
        """
        Logistic growth model: dN/dt = r * N * (1 - N/K)
        Returns the new population after one step (approximate).
        If growth_rate is None, uses max rate.
        """
        if growth_rate is None:
            growth_rate = self.population_growth_rate_max
        if carrying_capacity <= 0:
            return 0.0
        r = growth_rate
        N = population
        K = carrying_capacity
        dN = r * N * (1 - N / K)
        return max(0.0, N + dN)

    def extinction_risk(self, population: float, mvp: int = None) -> tuple:
        """Return (risk_level, reason) based on population relative to MVP."""
        if mvp is None:
            mvp = self.minimum_viable_population
        if population < mvp:
            return ("Critical", f"Population {population:.0f} below MVP ({mvp})")
        elif population < mvp * 2:
            return ("Elevated", f"Population {population:.0f} near MVP ({mvp})")
        else:
            return ("Low", "Population above MVP")

def l3_grounding_inspector(plan: dict) -> dict:
    """
    plan: dict with keys:
      - mass_kg (float): body mass of species
      - population (float): current population
      - trophic_level (int): 0 = producer, 1 = herbivore, etc.
      - base_energy (float): J per step available to producers
      - proposed_action (str): "introduce", "extract", "grow"
    Returns: dict with passed, reason, and details.
    """
    world = EcologicalWorld()
    details = {}
    all_passed = True
    reasons = []

    mass = plan.get('mass_kg', 0.0)
    population = plan.get('population', 0.0)
    trophic_level = plan.get('trophic_level', 0)
    base_energy = plan.get('base_energy', 100000.0)  # default

    # 1. Allometric metabolism check
    metabolism = world.allometric_metabolism(mass)
    details['metabolism_W'] = metabolism

    # 2. Carrying capacity based on trophic level
    K = world.carrying_capacity(base_energy, trophic_level, mass)
    details['carrying_capacity'] = K

    # 3. Compare population to carrying capacity
    if population > K * 1.2:  # allow small overshoot
        all_passed = False
        reasons.append(f"Population {population:.0f} exceeds carrying capacity {K:.0f}")

    # 4. Extinction risk (MVP check)
    risk, reason = world.extinction_risk(population)
    details['extinction_risk'] = risk
    if risk == "Critical":
        all_passed = False
        reasons.append(reason)

    # 5. Trophic level sanity
    if trophic_level > world.max_trophic_levels:
        all_passed = False
        reasons.append(f"Trophic level {trophic_level} exceeds max {world.max_trophic_levels}")

    # 6. Special action checks
    action = plan.get('proposed_action', '')
    if action == "introduce":
        # Introduction of species must not exceed carrying capacity
        if population > K:
            all_passed = False
            reasons.append("Introduction would exceed carrying capacity")

    if action == "extract":
        # Extraction must not push population below MVP
        if population < world.minimum_viable_population:
            all_passed = False
            reasons.append("Extraction would reduce population below MVP")

    return {
        'passed': all_passed,
        'reason': '; '.join(reasons) if reasons else 'All ecological constraints satisfied.',
        'details': details
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 50)
    print("L3 DEMO PINNED OUTPUT")
    print("=" * 50)

    # Valid: rabbit population at carrying capacity
    plan = {
        'mass_kg': 2.0,
        'population': 800,
        'trophic_level': 1,
        'base_energy': 100000.0
    }
    result = l3_grounding_inspector(plan)
    print(f"Rabbit plan (valid): Passed={result['passed']}")
    print(f"  Metabolism: {result['details']['metabolism_W']:.2f} W")
    print(f"  Carrying capacity: {result['details']['carrying_capacity']:.0f}")
    print(f"  Extinction risk: {result['details']['extinction_risk']}")

    # Invalid: super species (mass too high for trophic level)
    plan_bad = {
        'mass_kg': 1000.0,
        'population': 10,
        'trophic_level': 2,
        'base_energy': 100000.0
    }
    result = l3_grounding_inspector(plan_bad)
    print(f"\nSuper species: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    # Invalid: introduction exceeding capacity
    plan_intro = {
        'mass_kg': 0.5,
        'population': 1500,
        'trophic_level': 0,
        'base_energy': 100000.0,
        'proposed_action': 'introduce'
    }
    result = l3_grounding_inspector(plan_intro)
    print(f"\nIntroduction exceeding K: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    # Invalid: extraction below MVP
    plan_extract = {
        'mass_kg': 5.0,
        'population': 30,
        'trophic_level': 1,
        'base_energy': 100000.0,
        'proposed_action': 'extract'
    }
    result = l3_grounding_inspector(plan_extract)
    print(f"\nExtraction below MVP: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    print("=" * 50)

if __name__ == "__main__":
    demo()


# =============================================================================
# STAGE (per LOG.md "Probabilistic L1-L4 Conditioning" section 4):
# ProbabilisticEcologicalWorld and l3_probabilistic_inspector
#
# Bayesian counterpart to l3_grounding_inspector. Each ecological
# constraint contributes an additive log-probability term:
#
#   Allometry:            Gaussian on (claimed_metabolism_W
#                          - kleiber_prediction)
#   Trophic transfer:     Gaussian on (claimed_efficiency - 0.10)
#   Population overshoot: -scale * max(0, N/K - 1)^2
#   Population MVP:       -scale * max(0, 1 - N/MVP)^2
#   Trophic ceiling:      -scale * max(0, level - max_levels)^2
#
# Frozen additional noise/scale constants live on the class __init__
# defaults, pinned by GL_L3_P001..P005 + P_PIN in CLAIMS.md.
# =============================================================================


class ProbabilisticEcologicalWorld(EcologicalWorld):
    """
    L3 with additive Gaussian / smooth-barrier terms on the ecological
    constraints. Extends EcologicalWorld so the deterministic API
    (allometric_metabolism, trophic_energy_available,
    carrying_capacity, population_growth, extinction_risk) stays
    available.

    SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
      T = generational
          Population dynamics operate on lifespans; per-step
          semantics is caller-defined.
      S = ecosystem
          Bounded region with declared trophic structure.
      O = any_biological
          Kleiber's law is empirically fit to aerobic metabolism.
          Anaerobic microbes, deep-sea chemolithoautotrophs, and
          hypothetical non-terrestrial metabolisms do not follow
          the same 3/4-power scaling — the phenomenon claim uses
          O=any_biological rather than O=universal.
      C = ecosystem_frame
          The predator-prey / trophic-level / carrying-capacity
          ontology is ONE framing of ecology. Reciprocity-based
          frames from many Indigenous ecological knowledge
          systems, guild-based frames, and network-of-relations
          frames would carve the same substrate differently.
          Constants inherited from EcologicalWorld encode this
          specific framing.

    An AI evaluating claims about its own operation would NOT
    route through this layer — silicon substrate is not part of
    the biological ecosystem the constraint set is drawn from.
    An AI evaluating claims about an ecosystem it observes DOES
    route through this layer, and inherits the cultural framing.

    Constraint set inherited from EcologicalWorld:
      kleiber_a                     = 3.0    (W / kg^0.75)
      trophic_transfer_efficiency   = 0.10
      max_trophic_levels            = 5
      minimum_viable_population     = 50
      carrying_capacity_initial     = 1000
      population_growth_rate_max    = 0.5

    Frozen additional noise / scale constants added here:
      allometry_sigma          = 1.0    W noise on Kleiber prediction
      trophic_sigma            = 0.05   noise on 10% efficiency claim
      overcapacity_scale       = 2.0    scale on N > K barrier
      mvp_scale                = 2.0    scale on N < MVP barrier
      trophic_ceiling_scale    = 1.0    scale on level > max barrier

    Refute the CLAIM, not the constant. Same protocol as L0/L1/L2.
    """

    def __init__(self,
                 kleiber_a=3.0,
                 trophic_transfer_efficiency=0.10,
                 max_trophic_levels=5,
                 minimum_viable_population=50,
                 carrying_capacity_initial=1000,
                 population_growth_rate_max=0.5,
                 allometry_sigma=1.0,
                 trophic_sigma=0.05,
                 overcapacity_scale=2.0,
                 mvp_scale=2.0,
                 trophic_ceiling_scale=1.0):
        super().__init__(kleiber_a, trophic_transfer_efficiency,
                         max_trophic_levels, minimum_viable_population,
                         carrying_capacity_initial,
                         population_growth_rate_max)
        self.allometry_sigma = allometry_sigma
        self.trophic_sigma = trophic_sigma
        self.overcapacity_scale = overcapacity_scale
        self.mvp_scale = mvp_scale
        self.trophic_ceiling_scale = trophic_ceiling_scale

    def log_likelihood(self, plan):
        """
        Return dict with total log-probability and per-component
        breakdown for a proposed ecological plan.

        plan (dict) may include:
          mass_kg                    (kg)   species body mass
          population                 (int)  proposed population size
          trophic_level              (int)  0 = producers, 1 = herbivores...
          base_energy                (J/step, default 100000.0) producer energy
          claimed_metabolism_W       (W, optional) AI-proposed metabolism;
                                      scored against Kleiber's law
          claimed_trophic_efficiency (0..1, optional) AI-proposed transfer
                                      efficiency; scored against 0.10

        Returns:
          {
            'logp': float,                     # total, sum of components
            'components': {                     # per-constraint
              'allometry':        float or absent,
              'trophic_transfer': float or absent,
              'overcapacity':     float or absent,
              'mvp':              float or absent,
              'trophic_ceiling':  float or absent,
            }
          }

        Pure function — does NOT mutate self.
        """
        components = {}
        mass = plan.get('mass_kg', 0.0)
        pop = plan.get('population', 0.0)
        trophic = plan.get('trophic_level', 0)
        base_energy = plan.get('base_energy', 100000.0)

        # Allometry: penalize deviation from Kleiber's prediction
        if 'claimed_metabolism_W' in plan and mass > 0:
            kleiber_pred = self.allometric_metabolism(mass)
            claim = plan['claimed_metabolism_W']
            components['allometry'] = (
                -((claim - kleiber_pred) ** 2)
                / (2 * self.allometry_sigma ** 2))

        # Trophic transfer efficiency: Gaussian on deviation from 10%
        if 'claimed_trophic_efficiency' in plan:
            claim = plan['claimed_trophic_efficiency']
            components['trophic_transfer'] = (
                -((claim - self.trophic_transfer_efficiency) ** 2)
                / (2 * self.trophic_sigma ** 2))

        # Population dynamics: carrying capacity + MVP
        if pop > 0 and mass > 0:
            K = self.carrying_capacity(base_energy, trophic, mass)
            if K > 0:
                # Overshoot penalty
                overshoot = max(0.0, pop / K - 1.0)
                components['overcapacity'] = (
                    -self.overcapacity_scale * overshoot ** 2)

                # MVP undershoot penalty
                undershoot = max(0.0,
                    1.0 - pop / self.minimum_viable_population)
                components['mvp'] = (
                    -self.mvp_scale * undershoot ** 2)

        # Trophic ceiling: penalize levels above max
        over_trophic = max(0, trophic - self.max_trophic_levels)
        if over_trophic > 0:
            components['trophic_ceiling'] = (
                -self.trophic_ceiling_scale * over_trophic ** 2)

        total = sum(components.values())
        return {'logp': total, 'components': components}


def l3_probabilistic_inspector(plan, world=None):
    """
    Thin wrapper around ProbabilisticEcologicalWorld.log_likelihood.

    plan: dict — see log_likelihood for keys and units.
    world: optional ProbabilisticEcologicalWorld; if None a fresh
           world is created with default frozen constants.

    Returns the same dict shape as l2_probabilistic_inspector:
      {'logp': float, 'components': dict}.

    Does NOT mutate world. Same purity guarantee as L2 (GL_L3_P006).
    """
    if world is None:
        world = ProbabilisticEcologicalWorld()
    return world.log_likelihood(plan)

