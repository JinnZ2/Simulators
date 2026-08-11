import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Pattern, Set


class Genre(Enum):
    GENERAL = auto()
    CORPORATE_PR = auto()
    LEGAL_CONTRACT = auto()
    TECHNICAL_REPORT = auto()
    CASUAL_SOCIAL = auto()


@dataclass
class GenreProfile:
    """Defines baseline thresholds, dimension weights, and domain dampeners."""
    name: str
    saturation_thresholds: Dict[str, float]  # Max hits/100 tokens before saturation (1.0)
    weights: Dict[str, float]                # Dimension weights for composite manipulation
    passivity_dampening: float               # Dampening for D1 passive voice (e.g., legal imperative)
    affective_dampening: float              # Dampening for D2 severity words in technical contexts
    reification_dampening: float            # Dampening for D3 abstract entities in contracts


GENRE_PROFILES: Dict[Genre, GenreProfile] = {
    Genre.GENERAL: GenreProfile(
        name="General Prose",
        saturation_thresholds={'D1_agency': 12.0, 'D2_affect': 10.0, 'D3_reality': 10.0, 'D4_iconic': 6.0},
        weights={'D1_agency': 0.35, 'D2_affect': 0.30, 'D3_reality': 0.20, 'D4_iconic': 0.15},
        passivity_dampening=1.0,
        affective_dampening=1.0,
        reification_dampening=1.0
    ),
    Genre.CORPORATE_PR: GenreProfile(
        name="Corporate PR / Communications",
        saturation_thresholds={'D1_agency': 8.0, 'D2_affect': 6.0, 'D3_reality': 6.0, 'D4_iconic': 5.0},
        weights={'D1_agency': 0.40, 'D2_affect': 0.35, 'D3_reality': 0.15, 'D4_iconic': 0.10},
        passivity_dampening=1.2,   # Higher penalty for passivity in PR (evasion)
        affective_dampening=1.3,   # Higher penalty for forced optimism
        reification_dampening=1.1
    ),
    Genre.LEGAL_CONTRACT: GenreProfile(
        name="Legal Contract / Statute",
        saturation_thresholds={'D1_agency': 25.0, 'D2_affect': 4.0, 'D3_reality': 20.0, 'D4_iconic': 10.0},
        weights={'D1_agency': 0.15, 'D2_affect': 0.50, 'D3_reality': 0.25, 'D4_iconic': 0.10},
        passivity_dampening=0.3,   # Low penalty: agentless imperatives ("Notice shall be given") are standard
        affective_dampening=1.0,
        reification_dampening=0.4  # Low penalty: formal legal entities ("The Party of the First Part")
    ),
    Genre.TECHNICAL_REPORT: GenreProfile(
        name="Technical Report / Spec",
        saturation_thresholds={'D1_agency': 20.0, 'D2_affect': 8.0, 'D3_reality': 15.0, 'D4_iconic': 8.0},
        weights={'D1_agency': 0.20, 'D2_affect': 0.45, 'D3_reality': 0.25, 'D4_iconic': 0.10},
        passivity_dampening=0.5,   # Low penalty: objective process descriptions ("Sample was heated")
        affective_dampening=0.2,   # Low penalty: "critical", "fatal", "failure" are mechanical states
        reification_dampening=0.7
    ),
    Genre.CASUAL_SOCIAL: GenreProfile(
        name="Casual / Social Media",
        saturation_thresholds={'D1_agency': 10.0, 'D2_affect': 15.0, 'D3_reality': 8.0, 'D4_iconic': 12.0},
        weights={'D1_agency': 0.20, 'D2_affect': 0.35, 'D3_reality': 0.15, 'D4_iconic': 0.30},
        passivity_dampening=1.0,
        affective_dampening=1.0,
        reification_dampening=1.0
    )
}


@dataclass
class ContextRule:
    """Evaluates N-gram context surrounding a match to re-weight or re-route dimension scoring."""
    pattern: Pattern
    target_dimension: str
    # Maps Genre -> multiplier modifier
    genre_multipliers: Dict[Genre, float]
    # Required neighboring context keywords (if non-empty, must match at least one)
    qualifying_context: Set[str] = field(default_factory=set)
    disqualifying_context: Set[str] = field(default_factory=set)


@dataclass
class VectorSignature:
    """The 4D vector output for a piece of text."""
    dimension_scores: Dict[str, float]      # Density-normalized scores (hits / token)
    raw_counts: Dict[str, float]            # Raw pattern match counts
    normalized_scores: Dict[str, float]     # 0-1 bounded index per dimension
    trace: List[str]                        # Telemetry and pattern matches
    energy_estimate: float                  # Cognitive processing load estimate
    manipulation_index: float               # Composite manipulation density (0-1)


@dataclass
class DynamicVectorSignature:
    """4D vector output for the dynamic lens, including the applied genre profile."""
    genre_applied: str
    dimension_scores: Dict[str, float]
    raw_counts: Dict[str, float]
    normalized_scores: Dict[str, float]
    trace: List[str]
    energy_estimate: float
    manipulation_index: float
