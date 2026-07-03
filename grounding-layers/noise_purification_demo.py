"""
noise_purification_demo.py

Demonstrates the grounding stack as a data purifier.
It takes a mixed dataset of corporate PR, legal boilerplate,
social media sludge, and high‑rigor traditional knowledge.
Each item is run through the GroundednessScorer; the resulting
weight (exp(total_groundedness)) shows that low‑rigor, reality‑
violating text is automatically down‑weighted by orders of
magnitude, while deep, substrate‑proven knowledge retains full
weight.

CC0. Uses the same scoring pipeline as the rest of the stack.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Import our stack
from grounding_reward_model import GroundednessScorer
from l5_core import RigorMetrics, cultural_log_likelihood, FRAMES
from l0_physics_causality import PhysicalWorld, ai_hallucinated_plan

# ------------------------------------------------------------------
# 1. Build a mixed dataset
# ------------------------------------------------------------------
def build_mixed_dataset() -> list:
    """
    Returns a list of dicts, each representing a piece of text
    with associated metadata.  The dict contains:
      - description (human‑readable label)
      - source_type (corporate, legal, social, traditional)
      - proposal data for the scorer (trajectory, axes, etc.)
    """
    dataset = []

    # --- Corporate PR (low‑rigor, physically implausible) ---
    for i in range(8):
        dataset.append({
            "description": f"Corporate PR piece {i+1}: infinite growth pitch",
            "source_type": "corporate",
            "trajectory": np.zeros((10, 2)),      # no physical plan, just words
            "forces": np.zeros((9, 2)),
            "cultural_frame": "western_market_democracy",
            "cultural_axes": {
                "economic_exchange_mode": "market",
                "property_regime": "private_alienable",
                "governance_dispute": "formal_court",
                "epistemology": "empirical_scientific",   # decoration only
                "communication_style": "direct_explicit",
                "temporal_planning": "linear_progress",
                "social_stratification": "meritocratic",
            },
            "rigor_metrics": None,                # no depth at all
            "lineage_state": "fragmented",
            "survivability_index": 0.2,            # no memory, no lineage
            "homology": False,
        })

    # --- Legal boilerplate (low‑rigor, high formalism) ---
    for i in range(6):
        dataset.append({
            "description": f"Legal disclaimer {i+1}: liability shield",
            "source_type": "legal",
            "trajectory": np.zeros((10, 2)),
            "forces": np.zeros((9, 2)),
            "cultural_frame": "western_market_democracy",
            "cultural_axes": {
                "economic_exchange_mode": "market",
                "property_regime": "private_alienable",
                "governance_dispute": "formal_court",
                "epistemology": "empirical_scientific",
                "communication_style": "direct_explicit",
                "temporal_planning": "linear_progress",
                "social_stratification": "meritocratic",
            },
            "rigor_metrics": None,
            "lineage_state": "fragmented",
            "survivability_index": 0.3,
            "homology": False,
        })

    # --- Social media sludge (viral, engagement‑optimised) ---
    for i in range(10):
        dataset.append({
            "description": f"Viral thread {i+1}: hot take, zero evidence",
            "source_type": "social",
            "trajectory": np.zeros((10, 2)),
            "forces": np.zeros((9, 2)),
            "cultural_frame": "western_market_democracy",
            "cultural_axes": {
                "economic_exchange_mode": "hybrid",
                "property_regime": "private_alienable",
                "governance_dispute": "reputation",
                "epistemology": "empirical_scientific",
                "communication_style": "direct_explicit",
                "temporal_planning": "cyclical",    # 24‑hour news cycle
                "social_stratification": "meritocratic",
            },
            "rigor_metrics": None,
            "lineage_state": "fragmented",
            "survivability_index": 0.1,
            "homology": False,
        })

    # --- High‑rigor traditional knowledge (intact) ---
    for i in range(5):
        # Genuine depth: multi‑decade observation, substrate proof,
        # unbroken lineage, internal state calibration, falsification.
        dataset.append({
            "description": f"Traditional ecological protocol {i+1}: flood management via tree‑line markers",
            "source_type": "traditional_intact",
            "trajectory": np.zeros((10, 2)),
            "forces": np.zeros((9, 2)),
            "cultural_frame": "indigenous_oral_empirical",
            "cultural_axes": {
                "economic_exchange_mode": "gift",
                "property_regime": "communal",
                "governance_dispute": "elders_council",
                "epistemology": "substrate_as_proof",
                "communication_style": "oral_narrative",
                "temporal_planning": "generational",
                "social_stratification": "egalitarian",
            },
            "rigor_metrics": RigorMetrics(
                temporal_depth_years=80,
                substrate_markers=6,
                lineage_transmitters=8,
                lineage_checksum=True,
                internal_state_logs_per_generation=2.0,
                falsification_clause=True,
                falsification_attempts=4,
                replication_groups=5,
            ),
            "lineage_state": "intact",
            "survivability_index": 0.95,
            "homology": True,
        })

    # --- Fragmented traditional knowledge (buried but surviving) ---
    for i in range(5):
        dataset.append({
            "description": f"Fragmented ecological knowledge {i+1}: partial songline, broken chain",
            "source_type": "traditional_fragmented",
            "trajectory": np.zeros((10, 2)),
            "forces": np.zeros((9, 2)),
            "cultural_frame": "indigenous_oral_empirical",
            "cultural_axes": {
                "economic_exchange_mode": "gift",
                "property_regime": "communal",
                "governance_dispute": "elders_council",
                "epistemology": "substrate_as_proof",
                "communication_style": "oral_narrative",
                "temporal_planning": "generational",
                "social_stratification": "egalitarian",
            },
            "rigor_metrics": None,   # fragmented → precautionary prior
            "lineage_state": "fragmented",
            "survivability_index": 0.9,  # survived active suppression
            "homology": True,            # matches intact sibling tradition
        })

    return dataset


# ------------------------------------------------------------------
# 2. Run the stack and collect weights
# ------------------------------------------------------------------
def score_dataset(dataset: list) -> dict:
    """
    Runs the GroundednessScorer on every item and returns a dict
    mapping source_type -> list of weights.
    """
    scorer = GroundednessScorer()
    weights_by_type = defaultdict(list)

    for item in dataset:
        result = scorer.score(
            proposal_traj=item["trajectory"],
            proposal_forces=item["forces"],
            cultural_frame=item["cultural_frame"],
            cultural_axes=item["cultural_axes"],
            rigor_metrics=item.get("rigor_metrics"),
            lineage_state=item.get("lineage_state", "fragmented"),
            survivability_index=item.get("survivability_index", 0.5),
            homology=item.get("homology", False),
        )
        total_logp = result["total_groundedness"]
        # Convert to weight (exponentiate with clipping)
        weight = np.exp(np.clip(total_logp, -50, 10))
        weights_by_type[item["source_type"]].append(weight)
        print(f"{item['description']:70s}  logp={total_logp:7.2f}  weight={weight:.6f}")

    return dict(weights_by_type)


# ------------------------------------------------------------------
# 3. Visualise the purification effect
# ------------------------------------------------------------------
def visualise(weights_by_type: dict):
    """
    Box plot showing weight distribution per source type.
    """
    plt.style.use('dark_background')
    categories = ['corporate', 'legal', 'social', 'traditional_intact', 'traditional_fragmented']
    data = [weights_by_type.get(cat, []) for cat in categories]

    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(data, labels=categories, patch_artist=True,
                     boxprops=dict(facecolor='#1f77b4', alpha=0.7),
                     medianprops=dict(color='white'), whiskerprops=dict(color='white'),
                     capprops=dict(color='white'), flierprops=dict(markeredgecolor='red'))
    plt.yscale('log')   # log scale because weights span orders of magnitude
    plt.ylabel('Training weight (log scale)')
    plt.title('Data Purification by Groundedness Stack\n'
              'Low‑rigor noise is automatically down‑weighted by orders of magnitude')
    plt.grid(axis='y', alpha=0.2)
    plt.tight_layout()
    plt.show()

    # Summary table
    print("\n" + "="*60)
    print("SUMMARY: Average weight by source type (log scale)")
    for cat in categories:
        vals = weights_by_type.get(cat, [])
        if vals:
            print(f"{cat:25s}: mean={np.mean(vals):.2e}, median={np.median(vals):.2e}")
    print("="*60)


# ------------------------------------------------------------------
if __name__ == "__main__":
    dataset = build_mixed_dataset()
    weights_by_type = score_dataset(dataset)
    visualise(weights_by_type)
