"""
Tests for scope_profile.py — the six-factor scope matrix + verdict
assessment.

The design being pinned (JinnZ2's spec):

  Six factors:  physical_state, nutritional_state, health, career,
                living_conditions, environment.

  Four factor states: UNKNOWN (default), NEUTRAL, SUPPORTS, OPPOSES.

  Three achievable verdicts:
    - UNSCOPED                 (all factors UNKNOWN)
    - EMBODIED_TRUE_UNVERIFIED (at least one SUPPORTS, none OPPOSE)
    - MOST_LIKELY_UNTRUE       (no SUPPORTS, or SUPPORTS + OPPOSES,
                                or only NEUTRAL factors)

  One reserved verdict:
    - EXTERNALLY_VERIFIED      (sim cannot grant this; external
                                verification substrate only)

License: CC0
Dependencies: stdlib only.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from scope_profile import (
    ScopeFactor,
    ScopeProfile,
    Verdict,
    assess_probability_claim,
)


class TestScopeProfile(unittest.TestCase):
    """The six-factor container."""

    def test_default_all_unknown(self):
        p = ScopeProfile()
        for factor, value in p.as_dict().items():
            self.assertEqual(value, ScopeFactor.UNKNOWN,
                             f'{factor} not UNKNOWN by default')

    def test_is_fully_unknown_default(self):
        self.assertTrue(ScopeProfile().is_fully_unknown())

    def test_is_fully_unknown_false_after_declaration(self):
        p = ScopeProfile(career=ScopeFactor.SUPPORTS)
        self.assertFalse(p.is_fully_unknown())

    def test_six_factors_defined(self):
        p = ScopeProfile()
        self.assertEqual(set(p.as_dict()), {
            "physical_state",
            "nutritional_state",
            "health",
            "career",
            "living_conditions",
            "environment",
        })

    def test_supporting_factors(self):
        p = ScopeProfile(
            physical_state=ScopeFactor.SUPPORTS,
            career=ScopeFactor.SUPPORTS,
            health=ScopeFactor.OPPOSES,
        )
        self.assertEqual(
            set(p.supporting_factors()),
            {"physical_state", "career"})

    def test_opposing_factors(self):
        p = ScopeProfile(
            physical_state=ScopeFactor.SUPPORTS,
            health=ScopeFactor.OPPOSES,
            living_conditions=ScopeFactor.OPPOSES,
        )
        self.assertEqual(
            set(p.opposing_factors()),
            {"health", "living_conditions"})

    def test_declared_factors_omits_unknown(self):
        p = ScopeProfile(career=ScopeFactor.SUPPORTS,
                         health=ScopeFactor.NEUTRAL)
        self.assertEqual(set(p.declared_factors()),
                         {"career", "health"})


class TestVerdictUnscoped(unittest.TestCase):
    """UNSCOPED — fully-unknown profile, regardless of base_probability."""

    def test_default_profile_yields_unscoped(self):
        verdict, _ = assess_probability_claim(0.5, ScopeProfile())
        self.assertEqual(verdict, Verdict.UNSCOPED)

    def test_unscoped_regardless_of_base_probability(self):
        for prob in (0.0, 0.001, 0.5, 0.999, 1.0):
            verdict, _ = assess_probability_claim(prob, ScopeProfile())
            self.assertEqual(verdict, Verdict.UNSCOPED,
                             f'prob={prob} did not yield UNSCOPED')


class TestVerdictEmbodiedTrueUnverified(unittest.TestCase):
    """EMBODIED_TRUE_UNVERIFIED — at least one SUPPORTS, no OPPOSES.
    This is the sim's ceiling — it cannot grant EXTERNALLY_VERIFIED."""

    def test_single_support_no_oppose(self):
        p = ScopeProfile(career=ScopeFactor.SUPPORTS)
        verdict, reason = assess_probability_claim(0.001, p)
        self.assertEqual(verdict, Verdict.EMBODIED_TRUE_UNVERIFIED)
        self.assertIn("career", reason)

    def test_all_six_support(self):
        p = ScopeProfile(
            physical_state=ScopeFactor.SUPPORTS,
            nutritional_state=ScopeFactor.SUPPORTS,
            health=ScopeFactor.SUPPORTS,
            career=ScopeFactor.SUPPORTS,
            living_conditions=ScopeFactor.SUPPORTS,
            environment=ScopeFactor.SUPPORTS,
        )
        verdict, _ = assess_probability_claim(0.001, p)
        self.assertEqual(verdict, Verdict.EMBODIED_TRUE_UNVERIFIED)

    def test_supports_plus_neutrals_still_embodied(self):
        p = ScopeProfile(
            career=ScopeFactor.SUPPORTS,
            environment=ScopeFactor.NEUTRAL,
            health=ScopeFactor.NEUTRAL,
        )
        verdict, _ = assess_probability_claim(0.001, p)
        self.assertEqual(verdict, Verdict.EMBODIED_TRUE_UNVERIFIED)


class TestVerdictMostLikelyUntrue(unittest.TestCase):
    """MOST_LIKELY_UNTRUE — no SUPPORTS, or SUPPORTS + OPPOSES, or
    only NEUTRAL factors declared."""

    def test_single_oppose_no_support(self):
        p = ScopeProfile(health=ScopeFactor.OPPOSES)
        verdict, reason = assess_probability_claim(0.5, p)
        self.assertEqual(verdict, Verdict.MOST_LIKELY_UNTRUE)
        self.assertIn("health", reason)

    def test_supports_plus_opposes_is_untrue(self):
        # A single opposing factor defeats supports under current
        # design (severe injury defeats elite career).
        p = ScopeProfile(
            physical_state=ScopeFactor.SUPPORTS,
            career=ScopeFactor.SUPPORTS,
            health=ScopeFactor.OPPOSES,
        )
        verdict, reason = assess_probability_claim(0.001, p)
        self.assertEqual(verdict, Verdict.MOST_LIKELY_UNTRUE)
        self.assertIn("Mixed scope", reason)

    def test_only_neutrals_is_untrue(self):
        p = ScopeProfile(
            physical_state=ScopeFactor.NEUTRAL,
            health=ScopeFactor.NEUTRAL,
        )
        verdict, reason = assess_probability_claim(0.5, p)
        self.assertEqual(verdict, Verdict.MOST_LIKELY_UNTRUE)
        self.assertIn("no factor SUPPORTS", reason)


class TestArchitecturalCeiling(unittest.TestCase):
    """EXTERNALLY_VERIFIED cannot be produced from within the sim."""

    def test_externally_verified_is_never_returned(self):
        # Sweep a wide variety of profiles; none should yield
        # EXTERNALLY_VERIFIED. That verdict is reserved for external
        # substrate; assess_probability_claim never grants it.
        profiles = [
            ScopeProfile(),
            ScopeProfile(career=ScopeFactor.SUPPORTS),
            ScopeProfile(
                physical_state=ScopeFactor.SUPPORTS,
                health=ScopeFactor.SUPPORTS,
                career=ScopeFactor.SUPPORTS,
            ),
            ScopeProfile(health=ScopeFactor.OPPOSES),
            ScopeProfile(
                physical_state=ScopeFactor.SUPPORTS,
                health=ScopeFactor.OPPOSES,
            ),
        ]
        for prob in (0.0, 0.5, 1.0):
            for p in profiles:
                verdict, _ = assess_probability_claim(prob, p)
                self.assertNotEqual(verdict, Verdict.EXTERNALLY_VERIFIED)


if __name__ == '__main__':
    unittest.main()
