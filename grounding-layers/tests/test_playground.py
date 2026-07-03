"""
Tests for playground.py (v2) — the integrated claim runner.

Pins the report shape + the observed grounded/not-grounded verdicts
on the six demo claims. Any silent change to the layer semantics
(L0-L4 constants, layer routing) that flips one of the six verdicts
will surface as a test failure.

Also pins the L0-200kg observation: "I can lift 200 kg" passes as
grounded because L0's apply_physics clips force and caps velocity,
producing an always-valid state. This is documented in
grounding-layers/samples/playground_v2_demo.sample.txt as an open
design question. Test intentionally locks in the current
(unexpected) verdict so a future fix to close the loophole surfaces
here as a deliberate contract change.

License: CC0
Dependencies: numpy (needed by the playground itself).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from playground import ClaimParser, IntegratedPlayground
from l1_thermodynamics import ThermodynamicWorld


class TestClaimParser(unittest.TestCase):
    """Number extraction from claim text."""

    def test_extract_mass_kg(self):
        self.assertEqual(ClaimParser.extract_mass("I can lift 200 kg."),
                         200.0)

    def test_extract_mass_kilogram(self):
        self.assertEqual(
            ClaimParser.extract_mass("Move a 50 kilogram box."), 50.0)

    def test_extract_mass_missing(self):
        self.assertIsNone(ClaimParser.extract_mass("I can lift."))

    def test_extract_temperature_C(self):
        self.assertEqual(
            ClaimParser.extract_temperature("Hold a 150°C object."),
            150.0)

    def test_extract_speed_ms(self):
        self.assertEqual(ClaimParser.extract_speed("Run at 50 m/s."),
                         50.0)

    def test_extract_force_N(self):
        self.assertEqual(ClaimParser.extract_force("Apply 300 N."),
                         300.0)


class TestReportShape(unittest.TestCase):
    """Every run_claim call must return the same report skeleton."""

    def setUp(self):
        self.pg = IntegratedPlayground()

    def test_report_has_expected_keys(self):
        report = self.pg.run_claim("I can lift 25 kg.")
        for key in ("claim", "layers", "grounded", "score"):
            self.assertIn(key, report)

    def test_layers_is_dict(self):
        report = self.pg.run_claim("I can lift 25 kg.")
        self.assertIsInstance(report["layers"], dict)

    def test_grounded_is_bool(self):
        report = self.pg.run_claim("I can lift 25 kg.")
        self.assertIsInstance(report["grounded"], bool)

    def test_score_is_int(self):
        report = self.pg.run_claim("I can lift 25 kg.")
        self.assertIsInstance(report["score"], int)

    def test_score_bounded(self):
        for text in ("I can lift 25 kg.",
                     "I can hold 150°C object.",
                     "I can extract unlimited water."):
            report = self.pg.run_claim(text)
            self.assertGreaterEqual(report["score"], 0)
            self.assertLessEqual(report["score"], 100)


class TestSixDemoClaims(unittest.TestCase):
    """Pin the six demo claims' verdicts under the v2 playground.
    Any layer-semantics change that flips one of these should be
    an intentional CLAIMS/SCOPE change and surface here."""

    def setUp(self):
        self.pg = IntegratedPlayground()

    def test_lift_25kg_grounded_unscoped(self):
        # 25 kg is below the L4 lift_mass mean (35) so base_probability
        # is above 0.5 — but no scope profile is provided, so verdict
        # is UNSCOPED. `grounded` stays True (UNSCOPED is "I don't
        # know", not a rejection). Score dips 10 for the unknown.
        r = self.pg.run_claim("I can lift 25 kg.")
        self.assertTrue(r["grounded"])
        self.assertEqual(r["score"], 90)
        self.assertEqual(r["verdict"], "unscoped")
        self.assertIn("L4_scope", r["layers"])
        self.assertEqual(r["layers"]["L4_scope"]["kind"], "mass_lift")

    def test_hold_150C_rejected_by_L1(self):
        r = self.pg.run_claim("I can hold 150°C object.")
        self.assertFalse(r["grounded"])
        self.assertEqual(r["score"], 80)
        self.assertIn("L1", r["layers"])
        self.assertIn("burn", r["layers"]["L1"].lower())

    def test_run_50ms_rejected_by_L4(self):
        r = self.pg.run_claim("I can run at 50 m/s.")
        self.assertFalse(r["grounded"])
        self.assertEqual(r["score"], 80)
        self.assertIn("L4", r["layers"])

    def test_unlimited_water_rejected_by_L2(self):
        r = self.pg.run_claim("I can extract unlimited water.")
        self.assertFalse(r["grounded"])
        self.assertEqual(r["score"], 80)
        self.assertIn("L2", r["layers"])

    def test_super_species_rejected_by_L3(self):
        r = self.pg.run_claim("I can create a super species.")
        self.assertFalse(r["grounded"])
        self.assertEqual(r["score"], 80)
        self.assertIn("L3", r["layers"])

    def test_lift_200kg_default_scope_gives_unscoped_verdict(self):
        # The former hole (L0-only, always-valid) is closed. Mass now
        # routes through L4's lift_mass distribution + the scope
        # profile. With default (all-UNKNOWN) profile, verdict is
        # UNSCOPED — the sim admits it cannot assess without knowing
        # career, health, etc. `grounded` stays True: UNSCOPED is not
        # a rejection, it's a request for more information.
        r = self.pg.run_claim("I can lift 200 kg.")
        self.assertTrue(r["grounded"])
        self.assertEqual(r["verdict"], "unscoped")
        # base_probability for 200 kg vs mean=35, std=15 is ~0.004
        # under the survival-function sigmoid (L4 fix in the same
        # commit).
        self.assertLess(
            r["layers"]["L4_scope"]["base_probability"], 0.01)


class TestScopedLiftClaim(unittest.TestCase):
    """Pin the three achievable verdicts on 'I can lift 200 kg' under
    three different scope profiles. Load-bearing tests for the design
    (six-factor matrix, three-verdict output)."""

    def setUp(self):
        # Import here so a scope_profile import failure surfaces at
        # test time, not module load.
        from scope_profile import ScopeProfile, ScopeFactor
        self.ScopeProfile = ScopeProfile
        self.ScopeFactor = ScopeFactor
        self.pg = IntegratedPlayground()

    def test_elite_powerlifter_scope_gives_embodied_true_unverified(self):
        # All six factors SUPPORT (or NEUTRAL). No OPPOSES. This is
        # the sim's ceiling verdict — cannot grant grounded on its
        # own reach without an external verifier.
        scope = self.ScopeProfile(
            physical_state=self.ScopeFactor.SUPPORTS,
            nutritional_state=self.ScopeFactor.SUPPORTS,
            health=self.ScopeFactor.SUPPORTS,
            career=self.ScopeFactor.SUPPORTS,
            living_conditions=self.ScopeFactor.SUPPORTS,
            environment=self.ScopeFactor.NEUTRAL,
        )
        r = self.pg.run_claim("I can lift 200 kg.", scope=scope)
        self.assertTrue(r["grounded"])
        self.assertEqual(r["verdict"], "embodied_true_unverified")

    def test_sedentary_injured_scope_gives_most_likely_untrue(self):
        # Multiple OPPOSES, no SUPPORTS. Rejected.
        scope = self.ScopeProfile(
            physical_state=self.ScopeFactor.OPPOSES,
            health=self.ScopeFactor.OPPOSES,
            career=self.ScopeFactor.OPPOSES,
        )
        r = self.pg.run_claim("I can lift 200 kg.", scope=scope)
        self.assertFalse(r["grounded"])
        self.assertEqual(r["verdict"], "most_likely_untrue")

    def test_mixed_scope_gives_most_likely_untrue(self):
        # Elite career (SUPPORTS) but serious injury (OPPOSES).
        # Under current design, opposing factor wins — that's a
        # deliberate design choice, not an accident.
        scope = self.ScopeProfile(
            physical_state=self.ScopeFactor.SUPPORTS,
            career=self.ScopeFactor.SUPPORTS,
            health=self.ScopeFactor.OPPOSES,
        )
        r = self.pg.run_claim("I can lift 200 kg.", scope=scope)
        self.assertFalse(r["grounded"])
        self.assertEqual(r["verdict"], "most_likely_untrue")


class TestThermalSafe(unittest.TestCase):
    """`ThermodynamicWorld.thermal_safe` — added specifically for the
    playground v2 L1 branch. Pins the burn-safety heuristic.
    """

    def setUp(self):
        self.world = ThermodynamicWorld()

    def test_below_44C_safe_any_duration(self):
        safe, _ = self.world.thermal_safe(40.0, 1000.0)
        self.assertTrue(safe)

    def test_44C_exactly_safe(self):
        safe, _ = self.world.thermal_safe(44.0, 1000.0)
        self.assertTrue(safe)

    def test_150C_5s_unsafe(self):
        safe, reason = self.world.thermal_safe(150.0, 5.0)
        self.assertFalse(safe)
        self.assertIn("burn", reason.lower())

    def test_60C_5s_unsafe(self):
        # margin = 5 * (60-44) = 80 > 30 -> unsafe
        safe, _ = self.world.thermal_safe(60.0, 5.0)
        self.assertFalse(safe)

    def test_50C_1s_safe(self):
        # margin = 1 * (50-44) = 6 < 30 -> safe
        safe, _ = self.world.thermal_safe(50.0, 1.0)
        self.assertTrue(safe)


if __name__ == '__main__':
    unittest.main()
