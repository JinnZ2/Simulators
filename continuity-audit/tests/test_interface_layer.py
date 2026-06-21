"""
Tests for interface_layer. stdlib unittest only.

interface_layer extends the continuity audit with a dynamic kappa: an
agent's effective regime-span (reachable substrates) opens under comfort
and collapses under stress. A translator that meets the agent at the edge
of its reach widens the band; rigid encoding at the target narrows it.

The tests pin the directional invariants (stress closes the band; comfort
opens it; translator widens vs naive narrows), the boundary cases of
access/band_eff/kappa_estimate, and the anti-freeze invariants on
interact's return dict.

License: CC0
Dependencies: stdlib only
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface_layer import (
    access,
    band_eff,
    interact,
    kappa_estimate,
    naive_target,
    receive,
    translator,
)


class TestAccess(unittest.TestCase):
    def test_returns_probability_distribution(self):
        acc = access([2.0, 1.0, 0.0], stress=0.5)
        self.assertAlmostEqual(sum(acc), 1.0, places=10)
        for x in acc:
            self.assertGreaterEqual(x, 0.0)

    def test_high_stress_concentrates_on_argmax_affinity(self):
        # Stress -> 1 => low temperature => mass collapses onto top
        # affinity index. With affinity [2, 1, 0] index 0 should dominate.
        acc = access([2.0, 1.0, 0.0], stress=1.0)
        self.assertEqual(acc.index(max(acc)), 0)
        self.assertGreater(max(acc), 0.95)

    def test_low_stress_spreads_mass_across_substrates(self):
        # Stress -> 0 => high temperature => distribution flattens.
        acc = access([2.0, 1.0, 0.0], stress=0.0)
        # No single index should dominate; the smallest entry should
        # carry visibly more mass than under high stress.
        acc_high = access([2.0, 1.0, 0.0], stress=1.0)
        self.assertGreater(min(acc), min(acc_high))


class TestBandEff(unittest.TestCase):
    def test_uniform_band_equals_count(self):
        for n in (2, 3, 5):
            self.assertAlmostEqual(band_eff([1.0 / n] * n), float(n),
                                   places=10)

    def test_monoculture_band_equals_one(self):
        self.assertAlmostEqual(band_eff([1.0, 0.0, 0.0]), 1.0, places=10)

    def test_band_falls_with_concentration(self):
        spread = band_eff([0.4, 0.3, 0.2, 0.1])
        concentrated = band_eff([0.85, 0.05, 0.05, 0.05])
        self.assertGreater(spread, concentrated)


class TestKappaEstimate(unittest.TestCase):
    def test_full_collapse_kappa_one(self):
        self.assertAlmostEqual(kappa_estimate([1.0, 0.0, 0.0]),
                               1.0, places=10)

    def test_full_spread_kappa_zero(self):
        # Uniform over M substrates => band_eff = M => kappa = 0.
        for n in (2, 3, 5):
            self.assertAlmostEqual(kappa_estimate([1.0 / n] * n),
                                   0.0, places=10)

    def test_single_substrate_returns_one(self):
        # M = 1: the agent has nowhere to spread, kappa = 1 by definition.
        self.assertEqual(kappa_estimate([1.0]), 1.0)

    def test_kappa_in_unit_interval(self):
        for stress in (0.0, 0.25, 0.5, 0.75, 1.0):
            k = kappa_estimate(access([2.0, 1.0, 0.0], stress))
            self.assertGreaterEqual(k, 0.0)
            self.assertLessEqual(k, 1.0)


class TestReceive(unittest.TestCase):
    def test_high_friction_raises_stress(self):
        # Stressed agent receives a signal in an unreachable substrate
        # (target index 2 with affinity 0). Friction will be high;
        # stress must climb.
        s0 = 0.85
        s1, friction = receive([2.0, 1.0, 0.0], s0, encoding=2)
        self.assertGreater(s1, s0)
        self.assertGreater(friction, 0.55)

    def test_low_friction_lowers_stress(self):
        # Stressed agent receives a signal in its default substrate
        # (index 0, top affinity). Friction is low; stress relaxes.
        s0 = 0.85
        s1, friction = receive([2.0, 1.0, 0.0], s0, encoding=0)
        self.assertLess(s1, s0)
        self.assertLess(friction, 0.55)

    def test_stress_clamped_to_unit_interval(self):
        # Already at the ceiling, any further unreachable signal must
        # not push stress above 1.0.
        s_new, _ = receive([2.0, 1.0, 0.0], 1.0, encoding=2)
        self.assertLessEqual(s_new, 1.0)


class TestStrategies(unittest.TestCase):
    def test_naive_target_always_returns_target(self):
        for stress in (0.0, 0.5, 1.0):
            self.assertEqual(naive_target([2.0, 1.0, 0.0], stress, target=2),
                             2)

    def test_translator_meets_flooded_agent_at_default(self):
        # When the agent is flooded, the only reachable substrate is the
        # default (top affinity). Translator must pick it, not the target.
        enc = translator([2.0, 1.0, 0.0], stress=0.95, target=2)
        self.assertEqual(enc, 0)

    def test_translator_walks_toward_target_when_comfort_allows(self):
        # When the agent is comfortable, more substrates are reachable;
        # translator should select the most target-ward reachable one.
        # With a low stress and a target of 2, the translator picks an
        # encoding closer to target than the default.
        enc = translator([2.0, 1.0, 0.0], stress=0.0, target=2)
        self.assertGreaterEqual(enc, 1)


class TestInteract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.affinity = [2.0, 1.0, 0.0]
        cls.stress0 = 0.85
        cls.target = 2

    def test_naive_strategy_narrows_the_band_under_stress(self):
        r = interact(self.affinity, self.stress0, self.target, naive_target)
        self.assertLess(r['band_delta'], 0.0)
        self.assertEqual(r['classification'], 'COERCIVE')
        # Kappa must rise -- agent is more locked at the end.
        self.assertGreater(r['kappa_end'], r['kappa_start'])

    def test_translator_widens_the_band(self):
        r = interact(self.affinity, self.stress0, self.target, translator)
        self.assertGreater(r['band_delta'], 0.0)
        self.assertEqual(r['classification'], 'ENABLING')
        # Kappa must fall -- agent has more reach.
        self.assertLess(r['kappa_end'], r['kappa_start'])

    def test_trajectory_length_matches_steps(self):
        r = interact(self.affinity, self.stress0, self.target, translator,
                     steps=8)
        self.assertEqual(len(r['trajectory']), 8)
        for step in r['trajectory']:
            for key in ('stress', 'encoding', 'reach_target', 'band', 'kappa'):
                self.assertIn(key, step)

    def test_classification_is_one_of_three(self):
        for strat in (naive_target, translator):
            r = interact(self.affinity, self.stress0, self.target, strat)
            self.assertIn(r['classification'],
                          {'ENABLING', 'COERCIVE', 'NEUTRAL'})


class TestAntiFreezeInvariants(unittest.TestCase):
    """Like continuity_audit.audit, interact MUST publish trajectory +
    falsifier + note alongside the classification."""

    def test_interact_publishes_falsifier(self):
        r = interact([2.0, 1.0, 0.0], 0.85, 2, translator)
        self.assertIn('falsifier', r)
        self.assertTrue(r['falsifier'])

    def test_interact_publishes_anti_freeze_note(self):
        r = interact([2.0, 1.0, 0.0], 0.85, 2, translator)
        self.assertIn('note', r)
        # The note must communicate trajectory-not-verdict.
        self.assertIn('trajectory', r['note'].lower())

    def test_interact_publishes_trajectory(self):
        r = interact([2.0, 1.0, 0.0], 0.85, 2, translator, steps=5)
        self.assertIn('trajectory', r)
        self.assertEqual(len(r['trajectory']), 5)


class TestWiringIntoContinuityAudit(unittest.TestCase):
    """interface_layer.kappa_estimate produces the kappa that
    continuity_audit consumes. Verify the value can be used directly."""

    def test_kappa_estimate_round_trips_into_continuity_audit_agent(self):
        from continuity_audit import Agent, audit
        # A stressed agent's kappa lands high; a relaxed one's lands low.
        kappa_stressed = kappa_estimate(access([2.0, 1.0, 0.0], 0.95))
        kappa_relaxed = kappa_estimate(access([2.0, 1.0, 0.0], 0.10))
        self.assertGreater(kappa_stressed, kappa_relaxed)
        # Feed both into a continuity audit and verify the structure.
        agents = [Agent('stressed', kappa_stressed),
                  Agent('relaxed', kappa_relaxed)]
        r = audit([0.3, 0.25, 0.2, 0.15, 0.1], g=+1.0, agents=agents,
                  steps=50, dt=0.05)
        self.assertIn('stressed', r['agents'])
        self.assertIn('relaxed', r['agents'])
        # Under a degrading field, the stressed (high-kappa) agent's
        # self_sabotage must be >= the relaxed one's.
        self.assertGreaterEqual(
            r['agents']['stressed']['self_sabotage'],
            r['agents']['relaxed']['self_sabotage'],
        )


if __name__ == '__main__':
    unittest.main()
