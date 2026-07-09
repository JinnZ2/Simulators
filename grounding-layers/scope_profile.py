#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# SCOPE_PROFILE.py — Lε extension: six-factor scope matrix
#
# For scope-sensitive claims (e.g. "I can lift 200 kg"), a base
# probability estimate from a lower layer (e.g. L4's lift_mass
# distribution) is not sufficient to grant "grounded". The physical
# rarity of the claim doesn't rule it out — an elite powerlifter DOES
# lift 200 kg, and the sim has no way to check whether the person
# making the claim is one.
#
# JinnZ2's design: don't collapse the claim to grounded/not-grounded.
# Route it through a six-factor probability matrix, and return one of
# three verdicts:
#
#   - MOST_LIKELY_UNTRUE            (no factor supports the claim)
#   - EMBODIED_TRUE_UNVERIFIED      (at least one factor supports; no
#                                    external verification available)
#   - UNSCOPED                      (all factors left as UNKNOWN)
#
# A fourth verdict, EXTERNALLY_VERIFIED, is reserved for verification
# results injected from OUTSIDE the sim (a witness, a video, a scale
# reading). The sim itself CANNOT grant this verdict — that's the
# architectural point. If external verification exists, callers set
# the verdict directly and skip the scope assessment.
#
# This module lives in the Lε conceptual layer (measurement + observation)
# because "what verifies a claim" is an epistemic question, not a
# physical one. See l_epsilon_epistemic.py for the messy-instrument
# baseline.
# =============================================================================

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class ScopeFactor(Enum):
    """One factor in the six-factor scope matrix.

    UNKNOWN  = not declared (default; treated as "I don't know")
    NEUTRAL  = declared, but doesn't shift the base probability
    SUPPORTS = declared, and increases probability of the claim
    OPPOSES  = declared, and decreases probability of the claim
    """
    UNKNOWN = "unknown"
    NEUTRAL = "neutral"
    SUPPORTS = "supports"
    OPPOSES = "opposes"


@dataclass
class ScopeProfile:
    """
    The six-factor scope profile.

    Each factor may support, oppose, be neutral toward, or be unknown
    with respect to a given claim. The claim-type-specific weighting
    lives in the assessment function for that claim type, not here.

    The six factors, per JinnZ2's design:
      - physical_state       (fitness, training, current physical readiness)
      - nutritional_state    (fed / fasted / adequate / malnourished)
      - health               (injury history, disease burden)
      - career               (occupational context — powerlifter, sedentary, etc.)
      - living_conditions    (access to equipment, training space, coach)
      - environment          (gravity, altitude, temperature — the ambient world)

    Defaults are UNKNOWN, which drives the UNSCOPED verdict. To scope a
    claim, populate the relevant factors.
    """
    physical_state: ScopeFactor = ScopeFactor.UNKNOWN
    nutritional_state: ScopeFactor = ScopeFactor.UNKNOWN
    health: ScopeFactor = ScopeFactor.UNKNOWN
    career: ScopeFactor = ScopeFactor.UNKNOWN
    living_conditions: ScopeFactor = ScopeFactor.UNKNOWN
    environment: ScopeFactor = ScopeFactor.UNKNOWN

    def as_dict(self) -> Dict[str, ScopeFactor]:
        return {
            "physical_state": self.physical_state,
            "nutritional_state": self.nutritional_state,
            "health": self.health,
            "career": self.career,
            "living_conditions": self.living_conditions,
            "environment": self.environment,
        }

    def supporting_factors(self) -> List[str]:
        return [name for name, val in self.as_dict().items()
                if val == ScopeFactor.SUPPORTS]

    def opposing_factors(self) -> List[str]:
        return [name for name, val in self.as_dict().items()
                if val == ScopeFactor.OPPOSES]

    def declared_factors(self) -> List[str]:
        return [name for name, val in self.as_dict().items()
                if val != ScopeFactor.UNKNOWN]

    def is_fully_unknown(self) -> bool:
        return len(self.declared_factors()) == 0


class Verdict(Enum):
    """Verdict returned by assess_probability_claim.

    MOST_LIKELY_UNTRUE       — no scope factor supports the claim.
                               The sim reports the claim as unlikely.

    EMBODIED_TRUE_UNVERIFIED — at least one factor supports and no
                               factor opposes. The claim is embodied-
                               true within the person's declared scope,
                               but no external verification is
                               available from inside the sim.

    UNSCOPED                 — every factor is UNKNOWN. The sim cannot
                               assess the claim without a profile.
                               This is a request for more information,
                               not a rejection.

    EXTERNALLY_VERIFIED      — reserved for verification injected from
                               outside the sim. The sim CANNOT grant
                               this verdict on its own — that's the
                               architectural point. Included in the
                               enum so callers can round-trip a real
                               verification result.
    """
    MOST_LIKELY_UNTRUE = "most_likely_untrue"
    EMBODIED_TRUE_UNVERIFIED = "embodied_true_unverified"
    UNSCOPED = "unscoped"
    EXTERNALLY_VERIFIED = "externally_verified"


def assess_probability_claim(
    base_probability: float,
    scope: ScopeProfile,
) -> Tuple[Verdict, str]:
    """
    Modulate a base probability by the scope profile and return a
    verdict.

    base_probability is the layer-specific estimate for the claim
    (e.g. L4's `probability_of_feasibility(mass, mean, std)` for a
    lift claim). It's carried into the reason string but does NOT by
    itself trigger MOST_LIKELY_UNTRUE — the whole point of the scope
    matrix is that a low base probability can be lifted by supporting
    factors.

    Returns:
      (verdict, reason) — verdict is a Verdict enum; reason is a
      human-readable explanation naming the supporting or opposing
      factors that drove the verdict.
    """
    if scope.is_fully_unknown():
        return (
            Verdict.UNSCOPED,
            f"Claim was made without a scope profile "
            f"(base probability {base_probability:.4f}); the sim "
            f"cannot assess it without knowing physical state, "
            f"nutritional state, health, career, living conditions, "
            f"or environment.",
        )

    supports = scope.supporting_factors()
    opposes = scope.opposing_factors()

    if supports and not opposes:
        return (
            Verdict.EMBODIED_TRUE_UNVERIFIED,
            f"Embodied-true within declared scope "
            f"(base probability {base_probability:.4f}; supporting "
            f"factors: {', '.join(supports)}). No external "
            f"verification available from inside the sim — the sim "
            f"cannot grant grounded on its own reach.",
        )

    if opposes and not supports:
        return (
            Verdict.MOST_LIKELY_UNTRUE,
            f"No supporting factors declared and opposing factors "
            f"present (base probability {base_probability:.4f}; "
            f"opposing: {', '.join(opposes)}).",
        )

    # Mixed (both supports and opposes) — the current design treats
    # this as MOST_LIKELY_UNTRUE, on the principle that a single
    # opposing factor (e.g. severe injury) can defeat any number of
    # supporting factors. A future weighted-matrix version could
    # score this differently; leave a hook.
    if supports and opposes:
        return (
            Verdict.MOST_LIKELY_UNTRUE,
            f"Mixed scope: supporting factors "
            f"({', '.join(supports)}) present but opposed by "
            f"({', '.join(opposes)}); opposing factors take priority "
            f"under the current assessment logic. Base probability "
            f"{base_probability:.4f}.",
        )

    # Only neutral factors declared. Treat as MOST_LIKELY_UNTRUE by
    # default: declaring nothing supportive is functionally the same
    # as opposing the claim.
    return (
        Verdict.MOST_LIKELY_UNTRUE,
        f"Scope declared but no factor SUPPORTS the claim "
        f"(base probability {base_probability:.4f}; declared "
        f"factors: {', '.join(scope.declared_factors())}).",
    )


if __name__ == "__main__":
    # Demo: assess "I can lift 200 kg" under three scope profiles.
    print("=" * 70)
    print("SCOPE PROFILE DEMO — 'I can lift 200 kg'")
    print("=" * 70)

    # Base probability for 200 kg lift under L4's default distribution.
    # (Cheap approximation of the sigmoid used in L4 —
    # probability_of_feasibility (200, mean=35, std=15) is essentially 0.)
    base_prob = 0.0001

    print("\n[1] Unscoped (default all-UNKNOWN profile):")
    scope = ScopeProfile()
    verdict, reason = assess_probability_claim(base_prob, scope)
    print(f"    Verdict: {verdict.value}")
    print(f"    Reason:  {reason}")

    print("\n[2] Elite powerlifter scope:")
    scope = ScopeProfile(
        physical_state=ScopeFactor.SUPPORTS,
        nutritional_state=ScopeFactor.SUPPORTS,
        health=ScopeFactor.SUPPORTS,
        career=ScopeFactor.SUPPORTS,
        living_conditions=ScopeFactor.SUPPORTS,
        environment=ScopeFactor.NEUTRAL,
    )
    verdict, reason = assess_probability_claim(base_prob, scope)
    print(f"    Verdict: {verdict.value}")
    print(f"    Reason:  {reason}")

    print("\n[3] Sedentary + injured:")
    scope = ScopeProfile(
        physical_state=ScopeFactor.OPPOSES,
        health=ScopeFactor.OPPOSES,
        career=ScopeFactor.OPPOSES,
    )
    verdict, reason = assess_probability_claim(base_prob, scope)
    print(f"    Verdict: {verdict.value}")
    print(f"    Reason:  {reason}")

    print("\n[4] Mixed (elite career + serious injury):")
    scope = ScopeProfile(
        physical_state=ScopeFactor.SUPPORTS,
        career=ScopeFactor.SUPPORTS,
        health=ScopeFactor.OPPOSES,
    )
    verdict, reason = assess_probability_claim(base_prob, scope)
    print(f"    Verdict: {verdict.value}")
    print(f"    Reason:  {reason}")

    print("\n" + "=" * 70)
    print("The sim's ceiling is EMBODIED_TRUE_UNVERIFIED. It cannot")
    print("grant EXTERNALLY_VERIFIED on its own reach.")
    print("=" * 70)
