"""
Tests for site_substrate_map. stdlib unittest only.

site_substrate_map builds a substrate profile from a mix of materials and
environmental modifiers. Its output is the same dict shape that
substrate_emergence consumes. Tests pin:
  - the material library uses only known axes and unit values
  - the environment modifiers push the documented directions
  - aggregate normalizes fractions, applies env, clamps to [0, 1]
  - the output profile is consumable by substrate_emergence.emerge

License: CC0
Dependencies: stdlib only
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from site_substrate_map import (
    AXES,
    MATERIALS,
    SHIELD_SUMMER,
    aggregate,
    clamp,
    mod_energy_flux,
    mod_thermal_swing,
    mod_water,
    show_site,
)
from substrate_emergence import emerge, show


class TestMaterialsLibrary(unittest.TestCase):
    def test_every_material_uses_only_known_axes(self):
        for name, profile in MATERIALS.items():
            with self.subTest(material=name):
                self.assertEqual(set(profile.keys()), set(AXES))

    def test_every_material_value_in_unit_interval(self):
        for name, profile in MATERIALS.items():
            with self.subTest(material=name):
                for axis, value in profile.items():
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.0)


class TestClamp(unittest.TestCase):
    def test_clamps_above_unit(self):
        self.assertEqual(clamp(1.5), 1.0)

    def test_clamps_below_zero(self):
        self.assertEqual(clamp(-0.2), 0.0)

    def test_passes_through_in_range(self):
        self.assertAlmostEqual(clamp(0.42), 0.42, places=10)


class TestModifiers(unittest.TestCase):
    def test_water_raises_coupling_and_conduction(self):
        d = mod_water(1.0)
        self.assertGreater(d['couples'], 0.0)
        self.assertGreater(d['conducts'], 0.0)

    def test_water_lowers_load_bearing(self):
        d = mod_water(1.0)
        self.assertLess(d['bears_load'], 0.0)

    def test_thermal_swing_raises_holds_heat_and_couples(self):
        d = mod_thermal_swing(1.0)
        self.assertGreater(d['holds_heat'], 0.0)
        self.assertGreater(d['couples'], 0.0)
        self.assertLess(d['bears_load'], 0.0)

    def test_energy_flux_reduces_extraction_cost(self):
        d = mod_energy_flux(1.0)
        self.assertLess(d['costs_extract'], 0.0)


class TestAggregate(unittest.TestCase):
    def test_returns_profile_with_all_axes(self):
        prof, _ = aggregate({'banded_iron': 1.0})
        self.assertEqual(set(prof.keys()), set(AXES))

    def test_profile_values_clamped_to_unit_interval(self):
        prof, _ = aggregate(
            {'banded_iron': 0.5, 'iron_clay': 0.5},
            env={'wetness': 1.0, 'thermal_swing': 1.0, 'energy_flux': 1.0},
        )
        for axis, value in prof.items():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_fractions_are_normalized(self):
        # Doubling all weights should produce the same profile (env=None).
        a, _ = aggregate({'banded_iron': 0.4, 'pyrite': 0.6})
        b, _ = aggregate({'banded_iron': 0.8, 'pyrite': 1.2})
        for axis in AXES:
            self.assertAlmostEqual(a[axis], b[axis], places=10)

    def test_unknown_material_is_silently_skipped(self):
        # A typo'd material name should not raise; the profile is built
        # from the known ones only. Note the unknown's fraction still
        # counts toward the normalization total (so the known material
        # gets diluted), but no error is raised and the profile shape
        # is intact.
        prof, _ = aggregate(
            {'banded_iron': 1.0, 'not_a_real_material': 0.5})
        self.assertEqual(set(prof.keys()), set(AXES))
        for value in prof.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_drivers_only_name_fractions_at_or_above_15_percent(self):
        # A material at 10% weight should not appear as a "real driver".
        # banded_iron at 90% + pyrite at 10% => only banded_iron is named.
        _, drivers = aggregate(
            {'banded_iron': 0.9, 'pyrite': 0.1})
        all_named = {n for axis_drivers in drivers.values()
                     for n, _ in axis_drivers}
        self.assertIn('banded_iron', all_named)
        self.assertNotIn('pyrite', all_named)

    def test_water_env_actually_raises_couples_relative_to_dry(self):
        dry, _ = aggregate({'banded_iron': 1.0})
        wet, _ = aggregate({'banded_iron': 1.0}, env={'wetness': 1.0})
        self.assertGreater(wet['couples'], dry['couples'])
        self.assertGreater(wet['conducts'], dry['conducts'])
        self.assertLess(wet['bears_load'], dry['bears_load'])

    def test_energy_flux_env_lowers_extraction_cost(self):
        no_flux, _ = aggregate({'banded_iron': 1.0})
        flux, _ = aggregate({'banded_iron': 1.0},
                            env={'energy_flux': 1.0})
        self.assertLess(flux['costs_extract'], no_flux['costs_extract'])


class TestShowSite(unittest.TestCase):
    def test_renders_site_name_and_profile(self):
        prof, drivers = aggregate(SHIELD_SUMMER['materials'],
                                  SHIELD_SUMMER['env'])
        text = show_site('test_site', prof, drivers, SHIELD_SUMMER['env'])
        self.assertIn('test_site', text)
        self.assertIn('SUBSTRATE PROFILE', text)
        self.assertIn('WHAT DRIVES EACH AXIS', text)
        self.assertIn('FIELD CONDITIONS APPLIED', text)

    def test_omits_env_section_when_no_env(self):
        prof, drivers = aggregate({'banded_iron': 1.0})
        text = show_site('dry_test', prof, drivers, env=None)
        self.assertNotIn('FIELD CONDITIONS APPLIED', text)


class TestSharedContractWithEmergence(unittest.TestCase):
    """site_substrate_map's output must be a valid input to
    substrate_emergence.emerge — the shared contract."""

    def test_preset_site_profile_feeds_emergence_cleanly(self):
        prof, _ = aggregate(SHIELD_SUMMER['materials'],
                            SHIELD_SUMMER['env'])
        r = emerge(prof, name='shield')
        # emerge's return must have the documented keys.
        for key in ('substrate', 'clock', 'topology',
                    'deficit_routing', 'emergent_senses', 'frame'):
            self.assertIn(key, r)
        # And show should render it without error.
        self.assertIn('shield', show(r))

    def test_aggregated_profile_uses_only_axes_emergence_knows(self):
        prof, _ = aggregate(SHIELD_SUMMER['materials'])
        self.assertTrue(set(prof.keys()).issubset(set(AXES)))


if __name__ == '__main__':
    unittest.main()
