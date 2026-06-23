"""
Tests for incentive_blindspot_sim. stdlib unittest only.

The module's stance is REFUTATION_PROTOCOL: weights are frozen estimates,
claims carry the falsifiable content, and a failing claim means the claim
or the topology must change -- not the weights. The tests enforce this
discipline:

  - the WEIGHTS dict is locked to the published values; any retuning
    surfaces as a test failure that forces an honest update to the
    documented topology rather than a silent weight tweak;
  - every CLAIM_BS_xxx must return SUPPORTED on the shipped scenarios;
  - the mechanical invariants (state space [0,1], p_fail monotone and
    bounded, the multiplicative visibility gate, the trajectory length)
    are pinned;
  - the headline divergence (closed vs. open final P_fail) is asserted
    with the documented gap.

License: CC0
Dependencies: stdlib only
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from incentive_blindspot_sim import (
    CLAIMS,
    SCENARIOS,
    WEIGHTS,
    claim_BS_001,
    claim_BS_002,
    claim_BS_003,
    claim_BS_004,
    clamp,
    p_fail,
    run,
    step,
)


class TestFrozenWeights(unittest.TestCase):
    """REFUTATION_PROTOCOL: weights are frozen estimates. Any retuning
    must surface as a test failure, not slip past silently."""

    EXPECTED_WEIGHTS = {
        'alpha_V':      0.18,
        'k_complexity': 0.040,
        'k_blind':      0.050,
        'k_patch':      0.18,
        'k_conf':       0.09,
        'k_humility':   0.16,
        'k_entrench':   0.06,
        'k_narrow':     0.05,
        'decay':        0.02,
        'lam':          2.5,
    }

    def test_weights_match_published_estimates(self):
        self.assertEqual(set(WEIGHTS.keys()),
                         set(self.EXPECTED_WEIGHTS.keys()))
        for key, expected in self.EXPECTED_WEIGHTS.items():
            self.assertAlmostEqual(WEIGHTS[key], expected, places=10,
                                   msg=f'weight {key!r} drifted; if this is '
                                       'a deliberate refinement, document '
                                       'the change in the README and update '
                                       'this test')


class TestClamp(unittest.TestCase):
    def test_clamps_above_unit(self):
        self.assertEqual(clamp(1.5), 1.0)

    def test_clamps_below_zero(self):
        self.assertEqual(clamp(-0.2), 0.0)

    def test_passes_through_in_range(self):
        self.assertAlmostEqual(clamp(0.42), 0.42, places=10)

    def test_custom_bounds(self):
        self.assertEqual(clamp(3.0, lo=0.0, hi=2.0), 2.0)
        self.assertEqual(clamp(-1.0, lo=-0.5, hi=1.0), -0.5)


class TestPFail(unittest.TestCase):
    def test_zero_blindspot_is_zero_failure(self):
        self.assertEqual(p_fail(0.0), 0.0)

    def test_saturates_below_one_in_meaningful_range(self):
        # 1 - exp(-lam * B) is strictly < 1 for any B where exp doesn't
        # underflow. The model's state space caps B at 1.0; verifying
        # the bound there is what matters in practice.
        for B in (0.1, 0.5, 1.0):
            self.assertLess(p_fail(B), 1.0)

    def test_monotone_in_blindspot(self):
        Bs = [0.0, 0.1, 0.3, 0.5, 0.8, 1.0]
        ps = [p_fail(b) for b in Bs]
        for prev, cur in zip(ps, ps[1:]):
            self.assertGreater(cur, prev)

    def test_matches_published_lambda(self):
        # P_fail(1.0) with lam=2.5 -> 1 - exp(-2.5) ~= 0.9179
        self.assertAlmostEqual(p_fail(1.0), 1.0 - math.exp(-2.5),
                               places=10)


class TestStep(unittest.TestCase):
    def test_returns_dict_with_same_keys(self):
        s = SCENARIOS['credentialed_closed']['init']
        params = SCENARIOS['credentialed_closed']['params']
        out = step(s, params)
        self.assertEqual(set(out.keys()), set(s.keys()))

    def test_state_remains_in_unit_interval(self):
        s = dict(SCENARIOS['credentialed_closed']['init'])
        params = SCENARIOS['credentialed_closed']['params']
        for _ in range(100):
            s = step(s, params)
            for var, value in s.items():
                self.assertGreaterEqual(value, 0.0,
                                        f'{var} fell below 0')
                self.assertLessEqual(value, 1.0,
                                     f'{var} rose above 1')

    def test_multiplicative_gate_on_visibility(self):
        # When any single gate is at 1.0, the V_target is the floor.
        # With transparency_floor=0, V_target collapses to 0.
        s = {'C': 1.0, 'M': 0.0, 'F': 0.0, 'V': 0.5,
             'B': 0.0, 'X': 0.0}
        params = {'complexity_rate': 0.0, 'transparency_floor': 0.0}
        out = step(s, params)
        # V should be pulled down toward 0 by alpha_V.
        self.assertLess(out['V'], s['V'])

    def test_transparency_floor_holds_visibility(self):
        s = {'C': 1.0, 'M': 1.0, 'F': 1.0, 'V': 0.5,
             'B': 0.0, 'X': 0.0}
        params = {'complexity_rate': 0.0, 'transparency_floor': 0.6}
        out = step(s, params)
        # V should track toward the 0.6 floor, not toward 0.
        self.assertGreater(out['V'], s['V'])


class TestRun(unittest.TestCase):
    def test_default_horizon_is_61_snapshots(self):
        # steps=60 by default, snapshot taken before each step + a final
        # one after the last step -> 61 entries.
        traj = run(SCENARIOS['credentialed_closed'])
        self.assertEqual(len(traj), 61)

    def test_custom_horizon_respected(self):
        traj = run(SCENARIOS['credentialed_closed'], steps=10)
        self.assertEqual(len(traj), 11)

    def test_first_snapshot_is_init(self):
        traj = run(SCENARIOS['credentialed_closed'])
        for var, value in SCENARIOS['credentialed_closed']['init'].items():
            self.assertAlmostEqual(traj[0][var], value, places=10)


class TestPublishedClaims(unittest.TestCase):
    """REFUTATION_PROTOCOL: every shipped claim must verify SUPPORTED on
    the shipped scenarios under the shipped weights. If any fails, the
    discipline is to update the claim (or the topology), NOT to retune
    the weights to make it pass."""

    def test_claim_BS_001_supported(self):
        verdict, _ = claim_BS_001()
        self.assertEqual(verdict, 'SUPPORTED')

    def test_claim_BS_002_supported(self):
        verdict, _ = claim_BS_002()
        self.assertEqual(verdict, 'SUPPORTED')

    def test_claim_BS_003_supported(self):
        verdict, _ = claim_BS_003()
        self.assertEqual(verdict, 'SUPPORTED')

    def test_claim_BS_004_supported(self):
        verdict, _ = claim_BS_004()
        self.assertEqual(verdict, 'SUPPORTED')

    def test_CLAIMS_registry_lists_all_four(self):
        labels = {label for label, _ in CLAIMS}
        self.assertEqual(len(labels), 4)
        for label in labels:
            self.assertTrue(label.startswith('CLAIM_BS_'))


class TestHeadlineDivergence(unittest.TestCase):
    """Pin the empirical signature documented in the README's table."""

    def test_final_p_fail_matches_published_values(self):
        closed = run(SCENARIOS['credentialed_closed'])[-1]
        opened = run(SCENARIOS['distributed_open'])[-1]
        floored = run(SCENARIOS['closed_with_transparency'])[-1]
        # Match the README's "What the current run shows" table, with a
        # tolerance that allows for honest weight refinement so long as
        # the documented contrast survives.
        self.assertAlmostEqual(p_fail(closed['B']), 0.918, places=2)
        self.assertAlmostEqual(p_fail(opened['B']), 0.377, places=2)
        self.assertAlmostEqual(p_fail(floored['B']), 0.724, places=2)

    def test_closed_exceeds_floored_exceeds_open(self):
        # The headline ordering MUST hold even if weights are refined.
        closed = run(SCENARIOS['credentialed_closed'])[-1]
        opened = run(SCENARIOS['distributed_open'])[-1]
        floored = run(SCENARIOS['closed_with_transparency'])[-1]
        self.assertGreater(p_fail(closed['B']), p_fail(floored['B']))
        self.assertGreater(p_fail(floored['B']), p_fail(opened['B']))

    def test_complexity_off_still_drives_substantial_blindness(self):
        # The README states "closed structure with complexity off still
        # reaches B ~= 0.855". The gates alone -- not the complexity --
        # drive the blindness. Pin this with a tolerance that lets the
        # weights be refined but holds the qualitative ordering.
        off_scn = {
            'init': dict(SCENARIOS['credentialed_closed']['init']),
            'params': {'complexity_rate': 0.0,
                       'transparency_floor': 0.0},
        }
        final_B_off = run(off_scn)[-1]['B']
        self.assertGreater(final_B_off, 0.7)


class TestScenariosShape(unittest.TestCase):
    def test_every_scenario_has_init_and_params(self):
        for name, scn in SCENARIOS.items():
            with self.subTest(scenario=name):
                self.assertIn('init', scn)
                self.assertIn('params', scn)

    def test_every_init_state_in_unit_interval(self):
        for name, scn in SCENARIOS.items():
            with self.subTest(scenario=name):
                for var, value in scn['init'].items():
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.0)

    def test_every_init_state_carries_the_six_variables(self):
        expected = {'C', 'M', 'F', 'V', 'B', 'X'}
        for name, scn in SCENARIOS.items():
            with self.subTest(scenario=name):
                self.assertEqual(set(scn['init'].keys()), expected)


if __name__ == '__main__':
    unittest.main()
