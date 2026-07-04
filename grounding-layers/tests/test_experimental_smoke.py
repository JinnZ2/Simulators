"""
Smoke tests for grounding-layers/experimental/ instruments.

These are NOT audit-grade tests. The experimental instruments don't
yet have CLAIMS.md entries; this suite just verifies that the demos
run, the return dicts have the expected top-level keys, and the
canonical demo verdicts match their pinned outcomes.

License: CC0
Dependencies: stdlib only.
"""

import os
import sys
import unittest

# experimental/field_compass.py and audit-grade field_compass.py share
# a filename. Load the experimental modules by explicit path via
# importlib so we don't collide with the audit-grade module (which
# would win under regular sys.path lookup because grounding-layers/
# sits earlier on the path).
import importlib.util

_EXP_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'experimental'))


def _load(module_name, filename):
    path = os.path.join(_EXP_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_fc = _load('_exp_field_compass', 'field_compass.py')
_hfs = _load('_exp_holistic_field_state', 'holistic_field_state.py')
_cc = _load('_exp_calibration_channels', 'calibration_channels.py')

Compass = _fc.Compass
Frame = _fc.Frame
Node = _fc.Node
Read = _fc.Read
verdict = _fc.verdict

Channel = _hfs.Channel
Edge = _hfs.Edge
FieldState = _hfs.FieldState
Trust = _hfs.Trust
compare = _hfs.compare

CC_Channel = _cc.Channel
CC_Density = _cc.Density
CC_Relation = _cc.Relation
CC_REGISTRY = _cc.REGISTRY
cc_by_relation = _cc.by_relation
cc_entry_map = _cc.entry_map
cc_convergence_table = _cc.convergence_table


# =============================================================================
# field_compass smoke tests
# =============================================================================

class TestCompassBasics(unittest.TestCase):
    """Smoke tests for the aligner shape."""

    def _frame(self):
        return Frame(system='truck', driver='groove_65mph',
                     channels=('steering_feel', 'tie_rod_right',
                               'bump_response'))

    def test_delta_reports_not_ready_when_no_reads(self):
        c = Compass(self._frame())
        d = c.delta()
        self.assertFalse(d['ready'])

    def test_delta_reports_missing_ai_when_only_human_read(self):
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.5))
        d = c.delta()
        self.assertFalse(d['ready'])
        self.assertEqual(d['missing'], Node.AI.value)

    def test_delta_ready_with_both_reads(self):
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.5))
        c.orient(Read(Node.AI, 'tie_rod_right', 0.5, 0.5))
        d = c.delta()
        self.assertTrue(d['ready'])
        self.assertTrue(d['match'])

    def test_location_disagreement_flags(self):
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.5))
        c.orient(Read(Node.AI, 'steering_feel', 0.5, 0.5))
        d = c.delta()
        self.assertFalse(d['location']['agree'])


class TestCompassVerdict(unittest.TestCase):
    """Verdict semantic tests."""

    def _frame(self):
        return Frame(system='truck', driver='groove_65mph',
                     channels=('steering_feel', 'tie_rod_right'))

    def test_await_read_when_missing(self):
        v = verdict(Compass(self._frame()))
        self.assertEqual(v['action'], 'await_read')

    def test_hold_model_when_reads_match(self):
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.5))
        c.orient(Read(Node.AI, 'tie_rod_right', 0.5, 0.5))
        v = verdict(c)
        self.assertEqual(v['action'], 'hold_model')
        self.assertIsNone(v['learned'])

    def test_topology_lesson_on_location_disagreement(self):
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.5))
        c.orient(Read(Node.AI, 'steering_feel', 0.5, 0.5))
        v = verdict(c)
        self.assertIn('coupling_topology_wrong', v['learned'])

    def test_early_broadcast_lesson(self):
        # location matches; human sees system CLOSER to break
        # (shift_margin much lower than AI's).
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.30))
        c.orient(Read(Node.AI, 'tie_rod_right', 0.5, 0.80))
        v = verdict(c)
        self.assertIn('early_broadcast', v['learned'])

    def test_amplification_lesson(self):
        # location matches; margins match; but human peak_load much
        # higher than AI's (model damped a channel that amplifies).
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.70, 0.50))
        c.orient(Read(Node.AI, 'tie_rod_right', 0.30, 0.50))
        v = verdict(c)
        self.assertIn('amplification_underweighted', v['learned'])

    def test_rule_names_the_correction_direction(self):
        # Any mismatch verdict should surface the rule
        # "update the CLAIM. never retune the human read."
        c = Compass(self._frame())
        c.orient(Read(Node.HUMAN, 'tie_rod_right', 0.5, 0.30))
        c.orient(Read(Node.AI, 'tie_rod_right', 0.5, 0.80))
        v = verdict(c)
        self.assertEqual(
            v['rule'],
            'update the CLAIM. never retune the human read.')


# =============================================================================
# holistic_field_state smoke tests
# =============================================================================

class TestChannelTrust(unittest.TestCase):
    def test_gated_channel_is_not_live(self):
        c = Channel('soil_taste', 'skipped', Trust.GATED)
        self.assertFalse(c.live())

    def test_high_trust_channel_is_live(self):
        c = Channel('soil_bounce', 'slow rebound', Trust.HIGH)
        self.assertTrue(c.live())

    def test_baseline_trust_channel_is_live(self):
        c = Channel('mineral_taste', 'metallic', Trust.BASELINE)
        self.assertTrue(c.live())


class TestFieldStateStressField(unittest.TestCase):
    def _minimal_stack(self):
        fs = FieldState('garden', 'plot_a', 'now')
        fs.read(Channel('humidity', 'dry', Trust.HIGH, magnitude=0.5))
        fs.read(Channel('soil', 'compressed', Trust.HIGH,
                        magnitude=0.4))
        fs.couple('humidity', 'soil', 'stresses', 0.6)
        return fs

    def test_stress_field_excludes_gated_channels(self):
        fs = self._minimal_stack()
        fs.read(Channel('taste', 'not run', Trust.GATED))
        sf = fs.stress_field()
        self.assertNotIn('taste', sf)

    def test_stresses_mode_adds_load(self):
        # humidity magnitude 0.5 * transfer 0.6 = 0.3 added to soil.
        fs = self._minimal_stack()
        sf = fs.stress_field()
        self.assertAlmostEqual(sf['soil'], 0.3, places=6)

    def test_amplifies_mode_adds_load(self):
        fs = FieldState('truck', 'axle', 'now')
        fs.read(Channel('a', '', Trust.HIGH, magnitude=0.4))
        fs.read(Channel('b', '', Trust.HIGH, magnitude=0.0))
        fs.couple('a', 'b', 'amplifies', 0.5)
        sf = fs.stress_field()
        self.assertAlmostEqual(sf['b'], 0.2, places=6)

    def test_damps_mode_subtracts_load(self):
        fs = FieldState('sim', 's', 'now')
        fs.read(Channel('driver', '', Trust.HIGH, magnitude=0.5))
        fs.read(Channel('damped', '', Trust.HIGH, magnitude=0.0))
        fs.couple('driver', 'damped', 'damps', 0.4)
        sf = fs.stress_field()
        self.assertAlmostEqual(sf['damped'], -0.2, places=6)

    def test_stress_field_ordered_by_load_descending(self):
        fs = FieldState('s', 's', 'now')
        fs.read(Channel('low', '', Trust.HIGH, magnitude=0.1))
        fs.read(Channel('high', '', Trust.HIGH, magnitude=0.9))
        fs.read(Channel('mid', '', Trust.HIGH, magnitude=0.5))
        fs.couple('low', 'low', 'stresses', 1.0)
        fs.couple('high', 'high', 'stresses', 1.0)
        fs.couple('mid', 'mid', 'stresses', 1.0)
        sf = fs.stress_field()
        keys = list(sf.keys())
        # Self-coupled: load(x) = |mag(x)| * 1.0.
        self.assertEqual(keys[0], 'high')
        self.assertEqual(keys[-1], 'low')


class TestFieldStateShiftMargin(unittest.TestCase):
    def test_shift_margin_clamped_zero(self):
        # Very high peak load -> shift_margin = 0.
        fs = FieldState('s', 's', 'now')
        fs.read(Channel('a', '', Trust.HIGH, magnitude=1.0))
        fs.read(Channel('b', '', Trust.HIGH, magnitude=0.0))
        fs.couple('a', 'b', 'stresses', 2.0)  # drives b's load to 2.0
        self.assertEqual(fs.shift_margin(), 0.0)

    def test_shift_margin_one_when_no_load(self):
        fs = FieldState('s', 's', 'now')
        fs.read(Channel('a', '', Trust.HIGH, magnitude=0.0))
        self.assertEqual(fs.shift_margin(), 1.0)


class TestFieldStateVerdict(unittest.TestCase):
    def test_verdict_return_shape(self):
        fs = FieldState('garden', 'plot', 'now')
        fs.read(Channel('soil', '', Trust.HIGH, magnitude=0.5))
        fs.read(Channel('plant', '', Trust.HIGH, magnitude=0.3))
        fs.couple('soil', 'plant', 'stresses', 0.5)
        v = fs.verdict()
        for key in ('substrate', 'where', 'when', 'concentration',
                    'peak_load', 'shift_margin', 'gated',
                    'confidence'):
            self.assertIn(key, v)

    def test_gated_channels_listed(self):
        fs = FieldState('garden', 'plot', 'now')
        fs.read(Channel('soil', '', Trust.HIGH, magnitude=0.3))
        fs.read(Channel('taste', '', Trust.GATED))
        v = fs.verdict()
        self.assertIn('taste', v['gated'])
        self.assertNotIn('soil', v['gated'])


class TestCompareRefutation(unittest.TestCase):
    def test_match_when_all_within_tol(self):
        p = {'concentration': 'soil', 'peak_load': 0.3,
             'shift_margin': 0.7}
        m = {'concentration': 'soil', 'peak_load': 0.32,
             'shift_margin': 0.68}
        r = compare(p, m)
        self.assertTrue(r['match'])
        self.assertEqual(r['action'], 'hold_model')

    def test_miss_when_location_differs(self):
        p = {'concentration': 'plant_vigor', 'peak_load': 0.3,
             'shift_margin': 0.7}
        m = {'concentration': 'soil_bounce', 'peak_load': 0.3,
             'shift_margin': 0.7}
        r = compare(p, m)
        self.assertFalse(r['match'])
        self.assertEqual(r['action'], 'log_delta -> update_claim')

    def test_miss_when_scalar_beyond_tol(self):
        p = {'concentration': 'soil', 'peak_load': 0.3,
             'shift_margin': 0.7}
        m = {'concentration': 'soil', 'peak_load': 0.7,
             'shift_margin': 0.3}
        r = compare(p, m)
        self.assertFalse(r['match'])


# =============================================================================
# calibration_channels smoke tests
# =============================================================================

class TestCalibrationRegistry(unittest.TestCase):
    """Shape checks on the flat channel registry."""

    def test_registry_has_eight_channels(self):
        self.assertEqual(len(CC_REGISTRY), 8)

    def test_registry_entries_are_channel_instances(self):
        for c in CC_REGISTRY:
            self.assertIsInstance(c, CC_Channel)

    def test_channel_has_expected_fields(self):
        c = CC_REGISTRY[0]
        for field_name in ('name', 'couples', 'entry', 'density',
                           'relation', 'gives'):
            self.assertTrue(hasattr(c, field_name))

    def test_channel_is_frozen(self):
        c = CC_REGISTRY[0]
        with self.assertRaises(Exception):
            c.name = 'mutated'

    def test_channel_names_are_unique(self):
        names = [c.name for c in CC_REGISTRY]
        self.assertEqual(len(names), len(set(names)))


class TestCalibrationEnums(unittest.TestCase):
    def test_density_has_three_values(self):
        self.assertEqual(len(list(CC_Density)), 3)
        for name in ('DENSE', 'MEDIUM', 'SPARSE'):
            self.assertTrue(hasattr(CC_Density, name))

    def test_relation_has_five_values(self):
        self.assertEqual(len(list(CC_Relation)), 5)
        for name in ('FORMALIZES', 'METHOD', 'CROSS_CHECK',
                     'TRANSLATES', 'FOIL'):
            self.assertTrue(hasattr(CC_Relation, name))


class TestCalibrationViews(unittest.TestCase):
    def test_by_relation_filters(self):
        formalizes = cc_by_relation(CC_Relation.FORMALIZES)
        self.assertTrue(len(formalizes) >= 1)
        for c in formalizes:
            self.assertIs(c.relation, CC_Relation.FORMALIZES)

    def test_by_relation_returns_tuple(self):
        result = cc_by_relation(CC_Relation.FOIL)
        self.assertIsInstance(result, tuple)

    def test_entry_map_is_dict_of_lists(self):
        m = cc_entry_map()
        self.assertIsInstance(m, dict)
        for entry, names in m.items():
            self.assertIsInstance(entry, str)
            self.assertIsInstance(names, list)
            self.assertTrue(len(names) >= 1)

    def test_entry_map_covers_every_channel(self):
        m = cc_entry_map()
        flat = [n for names in m.values() for n in names]
        self.assertEqual(len(flat), len(CC_REGISTRY))

    def test_convergence_table_shape(self):
        t = cc_convergence_table()
        self.assertEqual(len(t), len(CC_REGISTRY))
        for row in t:
            self.assertEqual(len(row), 4)


class TestHarmonicReadIsInRegistry(unittest.TestCase):
    """The whole point: harmonic read sits among documented peers."""

    def _find(self, name):
        for c in CC_REGISTRY:
            if c.name == name:
                return c
        return None

    def test_coupled_harmonic_read_present(self):
        self.assertIsNotNone(self._find('coupled_harmonic_read'))

    def test_coupled_harmonic_read_is_sparse(self):
        c = self._find('coupled_harmonic_read')
        self.assertIs(c.density, CC_Density.SPARSE)

    def test_coupled_harmonic_read_formalizes(self):
        c = self._find('coupled_harmonic_read')
        self.assertIs(c.relation, CC_Relation.FORMALIZES)

    def test_bayesian_fusion_is_the_foil(self):
        c = self._find('bayesian_sensor_fusion')
        self.assertIsNotNone(c)
        self.assertIs(c.relation, CC_Relation.FOIL)


class TestDemosRun(unittest.TestCase):
    """Each experimental instrument's __main__ demo should run cleanly."""

    def test_field_compass_demo_runs(self):
        import runpy
        runpy.run_path(os.path.join(_EXP_DIR, 'field_compass.py'),
                        run_name='__main__')

    def test_holistic_field_state_demo_runs(self):
        import runpy
        runpy.run_path(
            os.path.join(_EXP_DIR, 'holistic_field_state.py'),
            run_name='__main__')

    def test_calibration_channels_demo_runs(self):
        import runpy
        runpy.run_path(
            os.path.join(_EXP_DIR, 'calibration_channels.py'),
            run_name='__main__')


if __name__ == '__main__':
    unittest.main()
