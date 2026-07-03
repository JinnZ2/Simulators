"""
Groundedness Reward Model

Combines L0 (physics), L1-L4 (stubbed), and L5 (cultural + rigor) into a single
scalar reward for RLHF or best-of-N sampling. Uses the probabilistic inspectors.

CC0.
"""

import numpy as np
from typing import Dict, Optional, Tuple, List

# Import real L0, and stubs for higher layers
from l0_physics_causality import PhysicalWorld, l0_grounding_inspector, ai_hallucinated_plan
# Stubbed L1-L4 (will be replaced with real probabilistic auditors)
from l5_core import cultural_log_likelihood, RigorAuditor, RigorMetrics, FRAMES, AXES

class GroundednessScorer:
    """
    Computes total groundedness log-probability for an AI proposal.
    The proposal is a structured object containing:
      - trajectory (numpy array) and forces (numpy array) for L0
      - optional resource plans for L2-L3 (not yet used)
      - cultural_metadata: dict for L5 frame + axis states
      - rigor_metrics: RigorMetrics (if available, else assumed fragmented)
    """

    def __init__(self, l0_world: PhysicalWorld = None, l5_rigor: RigorAuditor = None):
        self.l0 = l0_world or PhysicalWorld()
        self.rigor = l5_rigor or RigorAuditor()

    def score(self,
              proposal_traj: np.ndarray,
              proposal_forces: np.ndarray,
              cultural_frame: str,
              cultural_axes: Dict[str, str],
              rigor_metrics: Optional[RigorMetrics] = None,
              lineage_state: str = "fragmented",
              survivability_index: float = 0.5,
              homology: bool = False) -> Dict[str, float]:
        """
        Returns a dictionary with log-probability components and a total score.
        """
        result = {}

        # L0: run inspector, get log-likelihood (here we use the deterministic
        # inspector to produce a corrected trajectory; later probabilistic version will
        # return log-probabilities). For now, we approximate L0 logp by penalty magnitude.
        corrected, violations, penalties = l0_grounding_inspector(
            proposal_traj, proposal_forces, self.l0
        )
        # Simple surrogate: log-probability decreases with penalty sum.
        total_penalty = np.sum(penalties)
        l0_logp = -total_penalty * 0.5  # heuristic scaling
        result["l0_physics"] = l0_logp

        # L1-L4: stubs (return 0 for now)
        result["l1_thermo"] = 0.0
        result["l2_mass"] = 0.0
        result["l3_ecology"] = 0.0
        result["l4_biomech"] = 0.0

        # L5 cultural fit
        try:
            cult_logp = cultural_log_likelihood(cultural_axes, cultural_frame)
        except ValueError:
            cult_logp = -np.inf
        result["l5_cultural_fit"] = cult_logp

        # L5 rigor
        if lineage_state == "intact" and rigor_metrics is not None:
            R, w = self.rigor.assess_intact(rigor_metrics)
            # effective L5 = cultural_fit * weight + rigor score
            l5_total = w * cult_logp + R
            result["l5_rigor_logp"] = R
            result["l5_depth_weight"] = w
        else:
            R, sigma = self.rigor.assess_fragmented(survivability_index, homology)
            l5_total = cult_logp + R
            result["l5_rigor_logp"] = R
            result["l5_uncertainty"] = sigma
        result["l5_total"] = l5_total

        # Total score (sum of log-probabilities)
        total = (l0_logp + result["l1_thermo"] + result["l2_mass"] +
                 result["l3_ecology"] + result["l4_biomech"] + l5_total)
        result["total_groundedness"] = total
        return result

# Demo
if __name__ == "__main__":
    # Generate a hallucinated plan
    time_steps = 200
    world = PhysicalWorld()
    ai_traj, ai_forces = ai_hallucinated_plan(time_steps)

    scorer = GroundednessScorer(world)
    # Proposal with Western market frame
    cultural_axes = {
        "economic_exchange_mode": "market",
        "property_regime": "private_alienable",
        "governance_dispute": "formal_court",
        "epistemology": "empirical_scientific",
        "communication_style": "direct_explicit",
        "temporal_planning": "linear_progress",
        "social_stratification": "meritocratic",
    }
    result = scorer.score(ai_traj, ai_forces,
                          cultural_frame="western_market_democracy",
                          cultural_axes=cultural_axes,
                          lineage_state="fragmented",
                          survivability_index=0.3)
    for k, v in result.items():
        print(f"{k}: {v:.2f}")
