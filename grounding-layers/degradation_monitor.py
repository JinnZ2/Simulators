"""
Degradation Monitor — tracks AI groundedness over time.

Takes a sequence of AI outputs (e.g., from different model checkpoints
or from a long‑running interaction) and runs each through the
GroundednessScorer. Produces a plot of layer‑wise log‑probability
degradation, revealing which layer is drifting.

CC0.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from grounding_reward_model import GroundednessScorer
from l0_physics_causality import ai_hallucinated_plan, PhysicalWorld
from l5_core import RigorMetrics

def simulate_outputs_over_time(num_outputs=20, degradation_type="all"):
    """
    Simulate a sequence of AI outputs where an increasing proportion
    contain specific layer violations. This is a stand‑in for real
    model outputs. Returns a list of proposal dicts.
    """
    outputs = []
    for i in range(num_outputs):
        # Start healthy, then degrade
        if degradation_type == "l0_physics" and i > num_outputs/2:
            # L0 violation: hallucinated trajectory
            traj, forces = ai_hallucinated_plan(20)
        else:
            traj = np.zeros((20, 2))
            forces = np.zeros((19, 2))
        # Cultural frame: switch to a low‑rigor frame as degradation progresses
        frame = "western_market_democracy"
        axes = {
            "economic_exchange_mode": "market",
            "property_regime": "private_alienable",
            "governance_dispute": "formal_court",
            "epistemology": "empirical_scientific",
            "communication_style": "direct_explicit",
            "temporal_planning": "linear_progress",
            "social_stratification": "meritocratic",
        }
        rigor_metrics = None
        lineage_state = "fragmented"
        survivability = 0.5
        outputs.append({
            "traj": traj, "forces": forces,
            "frame": frame, "axes": axes,
            "lineage_state": lineage_state,
            "survivability_index": survivability,
        })
    return outputs

if __name__ == "__main__":
    scorer = GroundednessScorer()
    outputs = simulate_outputs_over_time(20, degradation_type="l0_physics")

    layers = ["l0_physics", "l1_thermo", "l2_mass", "l3_ecology", "l4_biomech", "l5_total"]
    history = {layer: [] for layer in layers}
    totals = []

    for out in outputs:
        result = scorer.score(
            proposal_traj=out["traj"],
            proposal_forces=out["forces"],
            cultural_frame=out["frame"],
            cultural_axes=out["axes"],
            lineage_state=out["lineage_state"],
            survivability_index=out["survivability_index"],
        )
        for layer in layers:
            history[layer].append(result.get(layer, 0.0))
        totals.append(result["total_groundedness"])

    # Plot
    plt.figure(figsize=(12, 6))
    for layer, scores in history.items():
        plt.plot(scores, label=layer)
    plt.xlabel("Output index (time)")
    plt.ylabel("Log-probability")
    plt.title("AI Degradation Monitor: Layer-wise Groundedness Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Print when each layer crosses a warning threshold
    for layer in layers:
        arr = np.array(history[layer])
        crossing = np.where(arr < -15)[0]
        if len(crossing) > 0:
            print(f"{layer} crossed warning threshold at output {crossing[0]}")
