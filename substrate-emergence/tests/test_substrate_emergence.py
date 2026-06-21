"""
Tests for substrate_emergence. stdlib unittest only.

The module's frame: deficits route, they do not get fixed. Tests pin the
shape of the output (each router returns the expected tuple/list shape),
the boundary cases (read() clamps and defaults), the trajectory contract
(emerge returns the expected dict keys; nothing is a stored verdict), and
internal consistency of the PRESETS (every value in [0, 1], every key in
AXES or a documented extra).

License: CC0
Dependencies: stdlib only
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from substrate_emergence import (
    AXES,
    PRESETS,
    emerge,
    read,
    route_clock,
    route_deficits,
    route_senses,
    route_topology,
    show,
)


class TestRead(unittest.TestCase):
    def test_missing_axis_defaults_to_half(self):
        # The contract: missing keys read as 0.5, neutral.
        self.assertEqual(read({}, 'conducts'), 0.5)
        self.assertEqual(read({'switches': 0.8}, 'conducts'), 0.5)

    def test_clamps_above_unit(self):
        self.assertEqual(read({'conducts': 2.0}, 'conducts'), 1.0)

    def test_clamps_below_zero(self):
        self.assertEqual(read({'conducts': -0.5}, 'conducts'), 0.0)

    def test_passes_through_in_range(self):
        self.assertAlmostEqual(read({'conducts': 0.42}, 'conducts'),
                               0.42, places=10)


class TestRouteClock(unittest.TestCase):
    def test_fast_clock_for_quick_switch_and_dissipate(self):
        cap, why = route_clock({'switches': 0.9, 'dissipates': 0.9})
        self.assertEqual(cap, 'fast_clock')
        self.assertTrue(why)

    def test_slow_tide_for_low_switch_and_dissipate(self):
        cap, why = route_clock({'switches': 0.1, 'dissipates': 0.1})
        self.assertEqual(cap, 'slow_tide')

    def test_breathing_clock_for_middle(self):
        cap, why = route_clock({'switches': 0.5, 'dissipates': 0.5})
        self.assertEqual(cap, 'breathing_clock')


class TestRouteTopology(unittest.TestCase):
    def test_serial_spine_for_good_conduct_low_abound(self):
        cap, _ = route_topology({'conducts': 0.9, 'abounds': 0.2})
        self.assertEqual(cap, 'serial_spine')

    def test_parallel_field_for_low_conduct_high_abound(self):
        cap, _ = route_topology({'conducts': 0.2, 'abounds': 0.9})
        self.assertEqual(cap, 'parallel_field')

    def test_networked_organism_for_mixed(self):
        cap, _ = route_topology({'conducts': 0.5, 'abounds': 0.5})
        self.assertEqual(cap, 'networked_organism')


class TestRouteDeficits(unittest.TestCase):
    def test_each_router_returns_capability_and_explanation(self):
        out = route_deficits({'conducts': 0.1})
        self.assertGreaterEqual(len(out), 1)
        for cap, why in out:
            self.assertTrue(cap)
            self.assertTrue(why)

    def test_heat_becomes_memory_requires_both_conditions(self):
        # Low dissipates alone is not enough; needs holds_heat > 0.55.
        out_one = [c for c, _ in route_deficits({'dissipates': 0.1})]
        self.assertNotIn('heat_becomes_memory', out_one)
        out_both = [c for c, _ in route_deficits(
            {'dissipates': 0.1, 'holds_heat': 0.8})]
        self.assertIn('heat_becomes_memory', out_both)

    def test_balanced_substrate_reports_no_dominant_deficit(self):
        # All-default profile (missing keys) reads 0.5 everywhere; no
        # router should trigger.
        out = route_deficits({})
        caps = [c for c, _ in out]
        self.assertEqual(caps, ['no_dominant_deficit'])

    def test_expensive_extraction_routes_to_use_whats_loose(self):
        out = [c for c, _ in route_deficits({'costs_extract': 0.8})]
        self.assertIn('use_less / use_whats_loose', out)

    def test_low_load_bearing_routes_to_soft_structure(self):
        out = [c for c, _ in route_deficits({'bears_load': 0.2})]
        self.assertIn('let_structure_be_soft', out)


class TestRouteSenses(unittest.TestCase):
    def test_decoupled_when_couples_is_low(self):
        out = [c for c, _ in route_senses({'couples': 0.1})]
        self.assertEqual(out, ['decoupled'])

    def test_thermal_sense_appears_above_threshold(self):
        out = [c for c, _ in route_senses({'couples': 0.4})]
        self.assertIn('thermal_sense', out)

    def test_season_sense_requires_couples_and_holds_heat(self):
        # couples high but holds_heat low -> no season_sense.
        out_one = [c for c, _ in route_senses(
            {'couples': 0.6, 'holds_heat': 0.1})]
        self.assertNotIn('season_sense', out_one)
        out_both = [c for c, _ in route_senses(
            {'couples': 0.6, 'holds_heat': 0.8})]
        self.assertIn('season_sense', out_both)

    def test_field_sense_appears_only_at_very_high_coupling(self):
        out_low = [c for c, _ in route_senses({'couples': 0.7})]
        self.assertNotIn('field_sense', out_low)
        out_high = [c for c, _ in route_senses({'couples': 0.8})]
        self.assertIn('field_sense', out_high)


class TestEmerge(unittest.TestCase):
    def test_returns_expected_keys(self):
        r = emerge({}, name='test')
        self.assertEqual(set(r.keys()), {
            'substrate', 'clock', 'topology',
            'deficit_routing', 'emergent_senses', 'frame',
        })
        self.assertEqual(r['substrate'], 'test')

    def test_frame_documents_the_anti_freeze_stance(self):
        # The frame string should communicate "relationship, not verdict".
        r = emerge({})
        self.assertIn('routed', r['frame'])
        self.assertIn('relationship', r['frame'])

    def test_clock_and_topology_are_tuples(self):
        r = emerge({})
        for key in ('clock', 'topology'):
            self.assertIsInstance(r[key], tuple)
            self.assertEqual(len(r[key]), 2)

    def test_deficit_routing_and_emergent_senses_are_lists_of_pairs(self):
        r = emerge({})
        for key in ('deficit_routing', 'emergent_senses'):
            self.assertIsInstance(r[key], list)
            for item in r[key]:
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)


class TestShow(unittest.TestCase):
    def test_renders_substrate_name(self):
        text = show(emerge({}, name='banded_iron'))
        self.assertIn('banded_iron', text)

    def test_renders_all_section_headers(self):
        text = show(emerge({'conducts': 0.1}, name='probe'))
        for header in ('SUBSTRATE:', 'CLOCK', 'TOPOLOGY',
                       'DEFICITS ROUTE TO:',
                       'SENSES THAT EMERGE FROM COUPLING:'):
            self.assertIn(header, text)


class TestPresets(unittest.TestCase):
    def test_axes_constant_is_complete(self):
        # AXES drives the contract; pin its membership.
        self.assertEqual(set(AXES), {
            'conducts', 'switches', 'dissipates', 'holds_heat',
            'costs_extract', 'abounds', 'bears_load', 'couples',
        })

    def test_all_presets_have_known_axes_and_unit_values(self):
        for name, profile in PRESETS.items():
            with self.subTest(preset=name):
                for axis, value in profile.items():
                    self.assertIn(axis, AXES,
                                  f'preset {name!r} has unknown axis {axis!r}')
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.0)

    def test_all_presets_render_without_error(self):
        for name, profile in PRESETS.items():
            text = show(emerge(profile, name=name))
            self.assertIn(name, text)


if __name__ == '__main__':
    unittest.main()
