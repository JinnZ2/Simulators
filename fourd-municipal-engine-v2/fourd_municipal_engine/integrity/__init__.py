"""Integrity module: entity resolution and corruption risk scoring.

STDLIB-ONLY (rapidfuzz optional with difflib fallback).
"""

from fourd_municipal_engine.integrity.entity_resolution import (
    EntityRecord,
    EntityNormalizer,
    EntityResolutionMatcher,
)
from fourd_municipal_engine.integrity.corruption_risk import CorruptionRiskCalculator

__all__ = [
    "EntityRecord",
    "EntityNormalizer",
    "EntityResolutionMatcher",
    "CorruptionRiskCalculator",
]
