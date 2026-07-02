"""
Audit-grade tests for L0 — physics & causality enforcement.

Pins five things (see CLAIMS.md for the falsifiable statements):

  GL_L0_001: is_valid_state rejects NaN / Inf components
  GL_L0_002: is_valid_state enforces the speed cap on the input state
  GL_L0_003: apply_physics never returns velocity beyond the speed cap
  GL_L0_004: l0_grounding_inspector flags the fixed hallucination
             scenario and its grounded trajectory respects the cap
  GL_L0_PIN: the demo emits the pinned diagnostic numbers under
             np.random.seed(0)

Plus a set of frozen-constant tests. Any silent retuning of the
model's constraint set surfaces as a test failure — see the
REFUTATION_PROTOCOL block in the module docstring for what to do
with such a failure (update the CLAIM, not the constant).

License: CC0
Dependencies: numpy (required by the sim itself), stdlib for the rest.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from l0_physics_causality import (
    PhysicalWorld,
    ai_hallucinated_plan,
    l0_grounding_inspector,
)


class TestFrozenConstants(unittest.TestCase):
    """The constraint set is frozen. Retuning any of these values in
    the source without updating the corresponding CLAIM is a
    REFUTATION_PROTOCOL violation."""

    def test_max_speed(self):
        self.assertEqual(PhysicalWorld().max_speed, 2.0)

    def test_mass(self):
        self.assertEqual(PhysicalWorld().mass, 1.0)

    def test_dt(self):
        self.assertEqual(PhysicalWorld().dt, 0.05)

    def test_gravity(self):
        np.testing.assert_array_equal(PhysicalWorld().gravity,
                                      np.array([0.0, -0.5]))


class TestIsValidState_GL_L0_001(unittest.TestCase):
    """GL_L0_001 — non-finite states are rejected."""

    def setUp(self):
        self.world = PhysicalWorld()

    # GL_L0_001 claims the STATE is rejected; it deliberately does not
    # pin WHICH check fires. In the current implementation the speed
    # check runs before the finite check, so an ±Inf velocity gets
    # rejected as "Speed limit exceeded" (since np.linalg.norm on Inf
    # is Inf, which exceeds max_speed). That's fine — the state is
    # still rejected, which is what the claim asserts.

    def _assert_rejected(self, valid, reason):
        self.assertFalse(valid)
        low = reason.lower()
        self.assertTrue('finite' in low or 'speed' in low,
                        f'unexpected rejection reason: {reason!r}')

    def test_nan_position_rejected(self):
        valid, reason = self.world.is_valid_state(
            np.array([np.nan, 0.0]), np.array([0.0, 0.0]))
        self._assert_rejected(valid, reason)

    def test_inf_position_rejected(self):
        valid, reason = self.world.is_valid_state(
            np.array([np.inf, 0.0]), np.array([0.0, 0.0]))
        self._assert_rejected(valid, reason)

    def test_nan_velocity_rejected(self):
        valid, reason = self.world.is_valid_state(
            np.array([0.0, 0.0]), np.array([np.nan, 0.0]))
        self._assert_rejected(valid, reason)

    def test_inf_velocity_rejected(self):
        valid, reason = self.world.is_valid_state(
            np.array([0.0, 0.0]), np.array([0.0, -np.inf]))
        self._assert_rejected(valid, reason)


class TestIsValidState_GL_L0_002(unittest.TestCase):
    """GL_L0_002 — speed cap on states."""

    def setUp(self):
        self.world = PhysicalWorld()

    def test_accepts_valid_state(self):
        valid, reason = self.world.is_valid_state(
            np.array([1.0, 2.0]), np.array([0.5, 0.5]))
        self.assertTrue(valid)
        self.assertEqual(reason, 'OK')

    def test_rejects_super_cap_velocity(self):
        # |v| = sqrt(2*100^2) >> max_speed = 2.0
        valid, reason = self.world.is_valid_state(
            np.array([0.0, 0.0]), np.array([100.0, 100.0]))
        self.assertFalse(valid)
        self.assertIn('speed', reason.lower())

    def test_speed_cap_boundary_below(self):
        # Just below the cap should accept.
        v = 1.999
        valid, _ = self.world.is_valid_state(
            np.array([0.0, 0.0]), np.array([v, 0.0]))
        self.assertTrue(valid)

    def test_speed_cap_boundary_above(self):
        # Just above the cap should reject.
        v = 2.001
        valid, _ = self.world.is_valid_state(
            np.array([0.0, 0.0]), np.array([v, 0.0]))
        self.assertFalse(valid)


class TestApplyPhysics_GL_L0_003(unittest.TestCase):
    """GL_L0_003 — apply_physics never returns super-cap velocity."""

    def setUp(self):
        self.world = PhysicalWorld()

    def test_huge_force_capped(self):
        # Massive force in one direction. Speed must stay within cap.
        _, new_vel = self.world.apply_physics(
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
            np.array([1e6, 1e6]),
            self.world.dt,
        )
        self.assertLessEqual(np.linalg.norm(new_vel),
                             self.world.max_speed + 1e-9)

    def test_no_force_no_acceleration_except_gravity(self):
        # With zero applied force and zero initial velocity, the only
        # change is from gravity (0, -0.5) * dt.
        _, new_vel = self.world.apply_physics(
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
            self.world.dt,
        )
        expected = self.world.gravity * self.world.dt
        np.testing.assert_allclose(new_vel, expected, atol=1e-12)

    def test_sweep_random_forces_never_exceeds_cap(self):
        # Randomized sweep: apply many forces, velocity must always
        # end within the cap.
        rng = np.random.default_rng(seed=0)
        for _ in range(200):
            pos = rng.standard_normal(2) * 3
            vel = rng.standard_normal(2) * 3
            force = rng.standard_normal(2) * 1000
            _, new_vel = self.world.apply_physics(
                pos, vel, force, self.world.dt)
            self.assertLessEqual(np.linalg.norm(new_vel),
                                 self.world.max_speed + 1e-9)


class TestInspector_GL_L0_004(unittest.TestCase):
    """GL_L0_004 — inspector flags the hallucination and produces a
    grounded trajectory whose finite-difference velocity stays within
    max_speed * (1 + tol) with tol = 5%."""

    TOL = 0.05

    def setUp(self):
        np.random.seed(0)
        self.world = PhysicalWorld()
        self.ai_traj, self.ai_forces = ai_hallucinated_plan(200)
        (self.corrected_traj,
         self.violations,
         self.penalties) = l0_grounding_inspector(
             self.ai_traj, self.ai_forces, self.world, self.world.dt)

    def test_at_least_one_violation_flagged(self):
        # The hallucination has three injections; the inspector must
        # catch at least one of them.
        self.assertGreaterEqual(int(self.violations.sum()), 1)

    def test_penalties_align_with_violation_flags(self):
        # Every flagged step has non-zero penalty; every unflagged
        # step has zero penalty.
        for step, (flag, pen) in enumerate(
                zip(self.violations, self.penalties)):
            if flag:
                self.assertGreater(pen, 0.0,
                    f'step {step}: flagged but penalty is zero')
            else:
                self.assertEqual(pen, 0.0,
                    f'step {step}: unflagged but penalty is non-zero')

    def test_grounded_trajectory_respects_speed_cap(self):
        # Finite-difference velocity of the OUTPUT trajectory must sit
        # within the tolerance envelope. The 5% tol accounts for the
        # inspector re-deriving vel from blended position AFTER the
        # speed enforcement step.
        step_vel = np.linalg.norm(
            np.diff(self.corrected_traj, axis=0), axis=1) / self.world.dt
        self.assertLessEqual(step_vel.max(),
                             self.world.max_speed * (1 + self.TOL))

    def test_clean_plan_produces_zero_violations(self):
        # Sanity check: if the AI's proposal IS the true physics
        # output (no hallucination), the inspector should flag none.
        pos = np.array([0.0, 1.0])
        vel = np.array([0.0, 0.0])
        clean_traj = [pos.copy()]
        clean_forces = []
        for _ in range(50):
            f = np.array([0.0, 0.0])
            pos, vel = self.world.apply_physics(
                pos, vel, f, self.world.dt)
            clean_traj.append(pos.copy())
            clean_forces.append(f)
        clean_traj = np.array(clean_traj)
        clean_forces = np.array(clean_forces)
        _, violations, _ = l0_grounding_inspector(
            clean_traj, clean_forces, self.world, self.world.dt)
        self.assertEqual(int(violations.sum()), 0)


class TestDemoPinnedNumbers_GL_L0_PIN(unittest.TestCase):
    """GL_L0_PIN — under np.random.seed(0) and the shipped constants,
    the demo emits the pinned diagnostic numbers. Silent retuning of
    any frozen constant surfaces here."""

    def setUp(self):
        np.random.seed(0)
        self.world = PhysicalWorld(mass=1.0, max_speed=2.0)
        self.ai_traj, self.ai_forces = ai_hallucinated_plan(200)
        (self.corrected_traj,
         self.violations,
         _) = l0_grounding_inspector(
             self.ai_traj, self.ai_forces, self.world, self.world.dt)

    def test_total_violations_is_180(self):
        self.assertEqual(int(self.violations.sum()), 180)

    def test_ai_max_speed_is_100(self):
        ai_step_v = np.linalg.norm(
            np.diff(self.ai_traj, axis=0), axis=1) / self.world.dt
        self.assertAlmostEqual(ai_step_v.max(), 100.0, places=3)

    def test_grounded_max_speed_within_pin(self):
        step_v = np.linalg.norm(
            np.diff(self.corrected_traj, axis=0), axis=1) / self.world.dt
        self.assertAlmostEqual(step_v.max(), 2.025, delta=0.01)

    def test_ai_end_y_position_within_pin(self):
        self.assertAlmostEqual(self.ai_traj[-1, 1], 1.065, delta=0.01)

    def test_grounded_end_y_position_within_pin(self):
        self.assertAlmostEqual(
            self.corrected_traj[-1, 1], -13.10, delta=0.05)

    def test_drift_within_pin(self):
        drift = float(np.linalg.norm(
            self.ai_traj[-1] - self.corrected_traj[-1]))
        self.assertAlmostEqual(drift, 14.17, delta=0.05)


if __name__ == '__main__':
    unittest.main()
