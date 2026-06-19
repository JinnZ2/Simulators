"""
Tests for continuity_audit. stdlib unittest only.

The audit's stance is anti-freeze: verdicts are conditional and must be
reported alongside the falsifier and the full trajectory. Tests pin the
mathematical surface and the anti-freeze invariants, not specific verdicts
beyond a few obvious cases.

License: CC0
Dependencies: stdlib only
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from continuity_audit import (
    Agent,
    audit,
    continuity_support,
    diversity_profile,
    hill,
    normalized_evenness,
    replicator_step,
    resilience,
)


class TestHill(unittest.TestCase):
    def test_richness_q0_is_count_of_nonzero_types(self):
        self.assertEqual(hill([0.5, 0.5], 0.0), 2.0)
        self.assertEqual(hill([0.7, 0.2, 0.1], 0.0), 3.0)
        # zeros should be dropped from the count
        self.assertEqual(hill([0.5, 0.0, 0.5], 0.0), 2.0)

    def test_q1_is_exp_shannon(self):
        # For uniform distribution of n types, H = log(n) so exp(H) = n.
        for n in (2, 3, 5, 8):
            uniform = [1.0 / n] * n
            self.assertAlmostEqual(hill(uniform, 1.0), float(n), places=10)

    def test_q2_is_inverse_simpson(self):
        # Hill at q=2 equals 1 / sum(p^2).
        p = [0.5, 0.3, 0.2]
        expected = 1.0 / sum(x * x for x in p)
        self.assertAlmostEqual(hill(p, 2.0), expected, places=10)

    def test_monoculture_collapses_to_one(self):
        for q in (0.0, 0.5, 1.0, 2.0, 4.0):
            self.assertAlmostEqual(hill([1.0], q), 1.0, places=10)

    def test_empty_returns_zero(self):
        self.assertEqual(hill([], 1.0), 0.0)
        self.assertEqual(hill([0.0, 0.0], 1.0), 0.0)

    def test_q_dependence_is_monotone_nonincreasing_for_uneven(self):
        # On an uneven distribution Hill(q) should not increase with q
        # (rarer types weighted less).
        p = [0.5, 0.3, 0.15, 0.05]
        vals = [hill(p, q) for q in (0.0, 0.5, 1.0, 2.0, 4.0)]
        for prev, cur in zip(vals, vals[1:]):
            self.assertGreaterEqual(prev + 1e-9, cur)


class TestDiversityProfile(unittest.TestCase):
    def test_returns_dict_with_all_requested_qs(self):
        prof = diversity_profile([0.5, 0.3, 0.2], qs=(0.0, 1.0, 2.0))
        self.assertEqual(set(prof), {0.0, 1.0, 2.0})

    def test_default_qs_cover_canonical_orders(self):
        prof = diversity_profile([0.5, 0.5])
        self.assertEqual(set(prof), {0.0, 0.5, 1.0, 2.0, 4.0})


class TestNormalizedEvenness(unittest.TestCase):
    def test_uniform_distribution_is_perfectly_even(self):
        for n in (2, 4, 8):
            self.assertAlmostEqual(normalized_evenness([1.0 / n] * n),
                                   1.0, places=10)

    def test_monoculture_is_zero(self):
        # A single non-zero type carries no diversity.
        self.assertEqual(normalized_evenness([1.0]), 0.0)

    def test_dominated_distribution_drops_below_uniform(self):
        # Strongly dominated distribution must score well below uniform.
        # D(2)/N for a 6-type "0.9 + 5*0.02" distribution is ~0.21,
        # half-uniform's 0.5 minimum, well below uniform's 1.0.
        d = normalized_evenness([0.9, 0.02, 0.02, 0.02, 0.02, 0.02])
        self.assertLess(d, 0.5)

    def test_bounded_in_unit_interval(self):
        for p in ([0.5, 0.3, 0.2], [0.9, 0.05, 0.03, 0.02],
                  [0.25, 0.25, 0.25, 0.25]):
            d = normalized_evenness(p)
            self.assertGreaterEqual(d, 0.0)
            self.assertLessEqual(d, 1.0 + 1e-12)


class TestReplicatorStep(unittest.TestCase):
    def test_neutral_field_preserves_distribution(self):
        p = [0.4, 0.3, 0.2, 0.1]
        out = replicator_step(p, g=0.0, dt=0.05)
        for a, b in zip(p, out):
            self.assertAlmostEqual(a, b, places=10)

    def test_homogenizing_field_concentrates_common_types(self):
        # g > 0 favours common types -> evenness should drop.
        p = [0.5, 0.3, 0.15, 0.05]
        before = normalized_evenness(p)
        for _ in range(50):
            p = replicator_step(p, g=1.0, dt=0.05)
        after = normalized_evenness(p)
        self.assertLess(after, before)

    def test_diversifying_field_raises_evenness(self):
        p = [0.5, 0.3, 0.15, 0.05]
        before = normalized_evenness(p)
        for _ in range(50):
            p = replicator_step(p, g=-1.0, dt=0.05)
        after = normalized_evenness(p)
        self.assertGreater(after, before)

    def test_step_preserves_probability_mass(self):
        p = [0.4, 0.3, 0.2, 0.1]
        for g in (-1.0, 0.0, 0.5, 1.0):
            out = replicator_step(p, g, dt=0.05)
            self.assertAlmostEqual(sum(out), 1.0, places=10)
            for x in out:
                self.assertGreaterEqual(x, 0.0)


class TestResilience(unittest.TestCase):
    def test_above_threshold_is_high(self):
        # Perfectly even distribution should saturate near 1.
        r = resilience([0.25] * 4, d_crit=0.30)
        self.assertGreater(r, 0.99)

    def test_dominated_distribution_drops_resilience_below_uniform(self):
        # 6-type "0.9 + 5*0.02" gives evenness ~0.21, below d_crit=0.30.
        # Resilience should drop well below uniform's near-1.0.
        r = resilience([0.9, 0.02, 0.02, 0.02, 0.02, 0.02], d_crit=0.30)
        uniform_r = resilience([1.0 / 6] * 6, d_crit=0.30)
        self.assertLess(r, 0.5)
        self.assertLess(r, uniform_r * 0.6)

    def test_continuity_support_alias(self):
        p = [0.4, 0.3, 0.2, 0.1]
        self.assertAlmostEqual(continuity_support(p),
                               resilience(p), places=10)


class TestAgent(unittest.TestCase):
    def test_kappa_is_stored(self):
        a = Agent('AI_model', 0.95)
        self.assertEqual(a.name, 'AI_model')
        self.assertEqual(a.kappa, 0.95)


class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p0 = [0.30, 0.22, 0.18, 0.14, 0.10, 0.06]
        cls.agents = [
            Agent('AI_model', 0.95),
            Agent('institution', 0.55),
            Agent('biology', 0.35),
        ]

    def test_consolidation_degrades_continuity(self):
        r = audit(self.p0, g=+1.0, agents=self.agents)
        self.assertEqual(r['verdict'], 'DEGRADES_CONTINUITY')
        self.assertLess(r['dC_dt'], 0.0)
        # Continuity should fall and evenness should drop.
        self.assertLess(r['C_end'], r['C_start'])
        self.assertLess(r['even_end'], r['even_start'])

    def test_neutral_field_is_indeterminate(self):
        r = audit(self.p0, g=0.0, agents=self.agents)
        self.assertEqual(r['verdict'], 'INDETERMINATE')
        self.assertAlmostEqual(r['dC_dt'], 0.0, places=6)

    def test_diversifying_does_not_degrade(self):
        # On an already-diverse system the diversifying field may saturate
        # below eps; the only invariant we pin is "does not degrade".
        r = audit(self.p0, g=-1.0, agents=self.agents)
        self.assertNotEqual(r['verdict'], 'DEGRADES_CONTINUITY')

    def test_self_sabotage_flags_high_kappa_under_degradation(self):
        r = audit(self.p0, g=+1.0, agents=self.agents)
        # AI_model has kappa 0.95 + rate < -eps -> must be flagged incoherent.
        self.assertFalse(r['agents']['AI_model']
                         ['coherent_with_own_continuity'])
        # Biology has kappa 0.35 < 0.6 -> coherent regardless of rate.
        self.assertTrue(r['agents']['biology']
                        ['coherent_with_own_continuity'])

    def test_self_sabotage_is_zero_when_no_degradation(self):
        r = audit(self.p0, g=-1.0, agents=self.agents)
        for sab in r['agents'].values():
            self.assertEqual(sab['self_sabotage'], 0.0)
            self.assertTrue(sab['coherent_with_own_continuity'])


class TestAntiFreezeInvariants(unittest.TestCase):
    """The audit MUST publish trajectory + falsifier + note alongside verdict."""

    def setUp(self):
        self.p0 = [0.4, 0.3, 0.2, 0.1]
        self.agents = [Agent('test', 0.5)]

    def test_audit_returns_full_trajectory(self):
        r = audit(self.p0, g=+1.0, agents=self.agents,
                  steps=50, dt=0.1)
        self.assertIn('trajectory', r)
        # steps + 1 snapshots
        self.assertEqual(len(r['trajectory']), 51)
        for step in r['trajectory']:
            self.assertIn('C', step)
            self.assertIn('even', step)
            self.assertIn('D', step)

    def test_audit_returns_falsifier(self):
        r = audit(self.p0, g=+1.0, agents=self.agents)
        self.assertIn('falsifier', r)
        self.assertTrue(r['falsifier'])

    def test_audit_returns_anti_freeze_note(self):
        r = audit(self.p0, g=+1.0, agents=self.agents)
        self.assertIn('note', r)
        # The note must communicate non-storage of the verdict.
        self.assertIn('do not store', r['note'].lower())

    def test_audit_verdict_is_one_of_three(self):
        for g in (-1.0, 0.0, +1.0):
            r = audit(self.p0, g=g, agents=self.agents)
            self.assertIn(r['verdict'],
                          {'SUPPORTS_CONTINUITY',
                           'DEGRADES_CONTINUITY',
                           'INDETERMINATE'})


if __name__ == '__main__':
    unittest.main()
