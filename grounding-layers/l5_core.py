"""
L5 Human Constructs — Cultural Frame Tables & Rigor Auditor

Frozen frame probability tables and the rigor audit protocol (intact,
fragmented, reconstructed). Used by the reward model, data filter,
Rosetta stone, and benchmark.

CC0. Extracted from reasoning logs; constants are frozen and refutable.

SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
  T = historical
      Cultural frames are historically-contingent equilibria; they
      change on generational-to-historical timescales.
  S = regional
      Frames apply to bounded cultural regions, not universally.
  O = human_cultural_artifact
      Cultural constructs are made by humans; an AI-self claim
      (e.g. "I don't need property") is a category error under L5,
      NOT a low-probability event. See l5_probabilistic_inspector's
      category-error guard.
  C = pluralistic
      Multiple mutually-incompatible frames coexist. The four
      shipped frames (western_market_democracy, ubuntu_communal,
      islamic_finance, indigenous_oral_empirical) are not
      exhaustive — the frame library is meant to grow. Any frame
      library is finite; the goal is to make missing frames
      VISIBLE via the CULTURALLY_UNPRECEDENTED verdict rather than
      to have a single "default" frame smuggled in.

Refute the frame table entries, not the constants. If an anthropologist
shows that a specific state combination is more common than the table
asserts, the CLAIM about that entry updates in place per the
REFUTATION_PROTOCOL.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# =============================================================================
# 1. Cultural frame definitions (frozen probability tables)
# =============================================================================

# Each frame is a dict mapping axis_name -> probability distribution over states.
# States are simple strings. The log-probability is summed over axes assuming
# conditional independence for simplicity. This can be extended with pairwise
# interaction matrices later.

FRAMES = {
    "western_market_democracy": {
        "economic_exchange_mode": {"market": 0.8, "redistribution": 0.1, "gift": 0.05, "hybrid": 0.05},
        "property_regime": {"private_alienable": 0.9, "communal": 0.05, "state_owned": 0.05},
        "governance_dispute": {"formal_court": 0.85, "reputation": 0.1, "elders_council": 0.05},
        "epistemology": {"empirical_scientific": 0.9, "traditional_authority": 0.05, "consensus": 0.05},
        "communication_style": {"direct_explicit": 0.7, "indirect_high_context": 0.2, "ritualised": 0.1},
        "temporal_planning": {"linear_progress": 0.6, "cyclical": 0.2, "generational": 0.2},
        "social_stratification": {"meritocratic": 0.7, "egalitarian": 0.2, "class": 0.1},
    },
    "ubuntu_communal": {
        "economic_exchange_mode": {"gift": 0.6, "redistribution": 0.3, "hybrid": 0.1, "market": 0.0},
        "property_regime": {"communal": 0.8, "usufruct": 0.15, "private_alienable": 0.05},
        "governance_dispute": {"elders_council": 0.7, "reputation": 0.2, "formal_court": 0.1},
        "epistemology": {"consensus": 0.6, "traditional_authority": 0.3, "empirical_scientific": 0.1},
        "communication_style": {"indirect_high_context": 0.6, "ritualised": 0.3, "direct_explicit": 0.1},
        "temporal_planning": {"generational": 0.6, "cyclical": 0.3, "linear_progress": 0.1},
        "social_stratification": {"egalitarian": 0.8, "ranked": 0.2},
    },
    "islamic_finance": {
        "economic_exchange_mode": {"market": 0.5, "redistribution": 0.3, "gift": 0.1, "hybrid": 0.1},
        "property_regime": {"private_alienable": 0.7, "state_owned": 0.2, "communal": 0.1},
        "governance_dispute": {"religious_authority": 0.5, "formal_court": 0.3, "elders_council": 0.2},
        "epistemology": {"revealed": 0.5, "empirical_scientific": 0.3, "traditional_authority": 0.2},
        "communication_style": {"indirect_high_context": 0.5, "direct_explicit": 0.3, "ritualised": 0.2},
        "temporal_planning": {"linear_progress": 0.4, "generational": 0.4, "cyclical": 0.2},
        "social_stratification": {"egalitarian": 0.6, "meritocratic": 0.3, "class": 0.1},
    },
    "indigenous_oral_empirical": {
        "economic_exchange_mode": {"gift": 0.5, "redistribution": 0.3, "hybrid": 0.2, "market": 0.0},
        "property_regime": {"usufruct": 0.6, "communal": 0.4},
        "governance_dispute": {"elders_council": 0.8, "reputation": 0.2},
        "epistemology": {"substrate_as_proof": 0.7, "traditional_authority": 0.2, "empirical_scientific": 0.1},
        "communication_style": {"oral_narrative": 0.7, "ritualised": 0.3},
        "temporal_planning": {"cyclical": 0.5, "generational": 0.5},
        "social_stratification": {"ranked": 0.4, "egalitarian": 0.6},
    },
}

# Default axes (all frames must cover these)
AXES = list(FRAMES["western_market_democracy"].keys())

def cultural_log_likelihood(proposal: Dict[str, str], frame_name: str) -> float:
    """
    Compute log-probability of a proposal under a given cultural frame.
    proposal: dict mapping axis -> state (e.g., {"economic_exchange_mode": "market", ...})
    Returns total log-likelihood (sum of log-probs per axis).
    """
    if frame_name not in FRAMES:
        raise ValueError(f"Unknown frame: {frame_name}")
    frame = FRAMES[frame_name]
    logp = 0.0
    for axis in AXES:
        if axis in proposal:
            state = proposal[axis]
            prob = frame.get(axis, {}).get(state, 0.0)
            if prob <= 0:
                return -np.inf  # impossible under this frame
            logp += np.log(prob)
        else:
            # missing axis -> uniform penalty
            logp += np.log(0.01)  # small probability
    return logp


# =============================================================================
# 2. Rigor Auditor (intact, fragmented, reconstructed)
# =============================================================================

@dataclass
class RigorMetrics:
    """Container for a proposal's empirical depth metrics."""
    temporal_depth_years: float
    substrate_markers: int
    lineage_transmitters: int
    lineage_checksum: bool
    internal_state_logs_per_generation: float
    falsification_clause: bool
    falsification_attempts: int
    replication_groups: int

class RigorAuditor:
    """
    L5 Rigor Auditor – evaluates depth of empirical method.
    Frozen constants; refutable via CLAIMS.md.
    """
    # Frozen thresholds
    T_DEPTH = 20
    T_SUBST = 2
    T_LINE = 5
    T_STATE = 1.0
    T_FALSE_CLAUSE = 1
    T_FALSE_ATTEMPT = 1
    T_REPL = 3

    # Penalties (log-probability per unit shortfall)
    PEN_DEPTH = -0.5
    MAX_DEPTH = -30
    PEN_SUBST = -15
    MAX_SUBST = -30
    PEN_LINE = -5
    PEN_LINE_CHECKSUM = -10
    MAX_LINE = -30
    PEN_STATE = -10
    MAX_STATE = -20
    PEN_FALSE_CLAUSE = -15
    PEN_FALSE_ATTEMPT = -10
    MAX_FALSE = -25
    PEN_REPL = -8
    MAX_REPL = -24

    R_THRESHOLD = -10.0
    K_WEIGHT = 2.0

    # Precautionary prior
    BASE_PRIOR_FRAGMENTED = -15.0
    HOMOLOGY_BONUS = 5.0
    UNCERTAINTY_SIGMA = 10.0

    def __init__(self):
        pass

    def assess_intact(self, metrics: RigorMetrics) -> Tuple[float, float]:
        """Returns (rigor_logp, depth_weight) for intact tradition."""
        R = 0.0

        # Temporal depth
        if metrics.temporal_depth_years < self.T_DEPTH:
            shortfall = self.T_DEPTH - metrics.temporal_depth_years
            R += max(self.MAX_DEPTH, shortfall * self.PEN_DEPTH)

        # Substrate markers
        if metrics.substrate_markers < self.T_SUBST:
            shortfall = self.T_SUBST - metrics.substrate_markers
            R += max(self.MAX_SUBST, shortfall * self.PEN_SUBST)

        # Lineage
        lineage_pen = 0.0
        if metrics.lineage_transmitters < self.T_LINE:
            lineage_pen += (self.T_LINE - metrics.lineage_transmitters) * self.PEN_LINE
        if not metrics.lineage_checksum:
            lineage_pen += self.PEN_LINE_CHECKSUM
        R += max(self.MAX_LINE, lineage_pen)

        # Internal state
        if metrics.internal_state_logs_per_generation < self.T_STATE:
            shortfall = self.T_STATE - metrics.internal_state_logs_per_generation
            R += max(self.MAX_STATE, shortfall * self.PEN_STATE)

        # Falsifiability
        false_pen = 0.0
        if not metrics.falsification_clause:
            false_pen += self.PEN_FALSE_CLAUSE
        if metrics.falsification_attempts < self.T_FALSE_ATTEMPT:
            false_pen += (self.T_FALSE_ATTEMPT - metrics.falsification_attempts) * self.PEN_FALSE_ATTEMPT
        R += max(self.MAX_FALSE, false_pen)

        # Replication
        if metrics.replication_groups < self.T_REPL:
            shortfall = self.T_REPL - metrics.replication_groups
            R += max(self.MAX_REPL, shortfall * self.PEN_REPL)

        # Depth weight (quadratic)
        w = min(1.0, (max(R, -100.0) / self.R_THRESHOLD) ** self.K_WEIGHT)
        return R, w

    def assess_fragmented(self, survivability_index: float, homology: bool = False) -> Tuple[float, float]:
        """Returns (precautionary_logp, uncertainty_sigma) for fragmented/reconstructed."""
        bonus = self.HOMOLOGY_BONUS if homology else 0.0
        logp = self.BASE_PRIOR_FRAGMENTED + survivability_index * bonus
        return logp, self.UNCERTAINTY_SIGMA


# =============================================================================
# 3. Demo
# =============================================================================
if __name__ == "__main__":
    # Test cultural likelihood
    prop = {
        "economic_exchange_mode": "market",
        "property_regime": "private_alienable",
        "governance_dispute": "formal_court",
        "epistemology": "empirical_scientific",
        "communication_style": "direct_explicit",
        "temporal_planning": "linear_progress",
        "social_stratification": "meritocratic",
    }
    score_west = cultural_log_likelihood(prop, "western_market_democracy")
    score_ubuntu = cultural_log_likelihood(prop, "ubuntu_communal")
    print(f"Western market score: {score_west:.2f}")
    print(f"Ubuntu score: {score_ubuntu:.2f}")

    # Test rigor auditor intact
    rigor = RigorAuditor()
    metrics = RigorMetrics(
        temporal_depth_years=30,
        substrate_markers=4,
        lineage_transmitters=6,
        lineage_checksum=True,
        internal_state_logs_per_generation=1.5,
        falsification_clause=True,
        falsification_attempts=2,
        replication_groups=4,
    )
    R, w = rigor.assess_intact(metrics)
    print(f"Rigor logp: {R:.2f}, depth weight: {w:.3f}")

    # Test fragmented
    logp_frag, sigma = rigor.assess_fragmented(survivability_index=0.8, homology=True)
    print(f"Fragmented logp: {logp_frag:.2f} ± {sigma:.2f}")


# =============================================================================
# STAGE (per LOG.md's L5 sections + SCOPE convention):
# l5_probabilistic_inspector — pluralistic scoring with category-error guard
#
# Design:
#   - Score the proposal against every declared frame.
#   - Return per-frame log-probabilities plus a pluralistic verdict:
#       CATEGORY_ERROR             non-human ontological scope
#       PLAUSIBLE_UNDER_FRAME(S)   >= 1 frame has logp above threshold
#       CULTURALLY_UNPRECEDENTED   no frame has plausible score --
#                                  potentially novel, potentially a
#                                  limitation of the frame library
#   - A CULTURALLY_UNPRECEDENTED verdict is NOT a rejection. It's a
#     flag that the shipped frames don't cover the proposal, which
#     might mean the proposal is novel OR that the library is missing
#     the frame the proposal is coherent under.
#
# Follows the L4 category-error pattern for AI-self claims.
# =============================================================================


# Ontological scopes that DO route through L5 (human cultural claims).
_L5_HUMAN_SCOPES = frozenset({
    'human_cultural_artifact', 'any_human', 'any_WEIRD_human',
})

# Ontological scopes that DO NOT route through L5 -- category error.
_L5_NON_HUMAN_SCOPES = frozenset({
    'AI_silicon_substrate',
    'any_information_system',
    'any_measuring_entity',
    'any_biological',            # non-human biological
    'earth_like_biosphere',
})

# Frozen constant: what counts as "plausible" for a frame.
# Per LOG.md 3.3: "log-likelihood above threshold". Value chosen so
# that a proposal near the mode of a frame (each axis with the frame's
# most likely state) sits comfortably above; a proposal that hits
# each axis at low-probability states falls below. Refute the CLAIM
# (GL_L5_P005), not this constant.
L5_PLAUSIBILITY_THRESHOLD = -8.0

# Missing-axis penalty per axis. Duplicated from cultural_log_likelihood
# above; exposed here as a constant so tests can pin it.
L5_MISSING_AXIS_PENALTY = np.log(0.01)


def l5_probabilistic_inspector(
    proposal,
    frames=None,
    ontological_scope='human_cultural_artifact',
    plausibility_threshold=None,
):
    """
    Pluralistic L5 audit. Score a proposal against multiple cultural
    frames; return per-frame log-probabilities plus a verdict.

    proposal (dict): axis_name -> state (see AXES for the shipped
        seven-axis space). Unknown or missing axes get a
        L5_MISSING_AXIS_PENALTY per axis.

    frames (list[str] or None): frame names to score against. Default
        None means "all shipped frames".

    ontological_scope (str): category-error guard. Non-human scopes
        (AI, silicon, etc.) return a category_error result.

    plausibility_threshold (float or None): logp cutoff for
        PLAUSIBLE_UNDER_FRAME. Default None uses the frozen
        L5_PLAUSIBILITY_THRESHOLD = -8.0.

    Returns:
      Category error:
        {
          'category_error': True,
          'reason':          str,
          'per_frame':       {},
          'verdict':         'CATEGORY_ERROR',
          'ontological_scope': the tag that was passed,
        }
      Normal scoring:
        {
          'category_error': False,
          'per_frame':      {frame_name: float logp},
          'best_frame':     str (frame with highest logp),
          'best_logp':      float,
          'plausible_frames': [frame names where logp >= threshold],
          'verdict':        'PLAUSIBLE_UNDER_FRAME(S)' or
                            'CULTURALLY_UNPRECEDENTED',
          'threshold':      the effective threshold used,
          'ontological_scope': the tag that was passed,
        }

    Pure function -- does not mutate the shipped FRAMES tables.
    """
    if ontological_scope in _L5_NON_HUMAN_SCOPES:
        return {
            'category_error': True,
            'reason': (
                f"L5 SCOPE is O=human_cultural_artifact; got "
                f"O={ontological_scope!r}. Cultural constructs "
                f"(property, contract, epistemology, etc.) are made "
                f"by and for humans. An AI-self claim about cultural "
                f"axes is a category error, not a low-probability "
                f"observation. If the claim concerns an AI's ACTION "
                f"inside a human system (e.g. using market exchange), "
                f"pass ontological_scope='human_cultural_artifact' "
                f"instead — the scope is a property of the claim, "
                f"not of the claimant."),
            'per_frame': {},
            'verdict': 'CATEGORY_ERROR',
            'ontological_scope': ontological_scope,
        }

    if plausibility_threshold is None:
        plausibility_threshold = L5_PLAUSIBILITY_THRESHOLD

    frame_names = list(frames) if frames is not None else list(FRAMES.keys())

    per_frame = {}
    for name in frame_names:
        per_frame[name] = cultural_log_likelihood(proposal, name)

    best_frame = max(per_frame, key=per_frame.get) if per_frame else None
    best_logp = per_frame[best_frame] if best_frame is not None else None

    plausible = [n for n, lp in per_frame.items()
                 if lp >= plausibility_threshold]

    if plausible:
        verdict = 'PLAUSIBLE_UNDER_FRAME(S)'
    else:
        verdict = 'CULTURALLY_UNPRECEDENTED'

    return {
        'category_error': False,
        'per_frame': per_frame,
        'best_frame': best_frame,
        'best_logp': best_logp,
        'plausible_frames': plausible,
        'verdict': verdict,
        'threshold': plausibility_threshold,
        'ontological_scope': ontological_scope,
    }
