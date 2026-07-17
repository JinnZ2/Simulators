"""
Tests for the sustained-heat sensor degradation audit.

The module is a lumped seven-layer pass over one driver (temperature over
time). The tests pin:

  - MATERIALS shape (required fields, sane ranges) so a silent edit surfaces
  - the deterministic converters (f_to_c, surface amplification above air)
  - pair_mismatch: order-agnostic d_cte, the GREEN/YELLOW/RED thresholds,
    and displacement scaling with span
  - compression_set: Q10 acceleration at reference, monotonic clamp to 1.0,
    and the "no gasket model" escape hatch
  - aging_multiplier: identity at the 25 C reference, monotone increasing
  - corruption_signature: the both-conditions gate on the low-bias read
  - audit: worst-flag-wins verdict and the shipped heat-dome case (RED)

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thermal_sensor_degradation_audit import (
    MATERIALS,
    aging_multiplier,
    audit,
    compression_set,
    corruption_signature,
    f_to_c,
    pair_mismatch,
    sensor_drift,
    surface_temp_c,
    wet_bulb_c,
)


class TestMaterials(unittest.TestCase):
    REQUIRED = {"cte", "t_service_c", "creep_onset_c"}

    def test_every_entry_has_required_fields(self):
        for name, data in MATERIALS.items():
            with self.subTest(material=name):
                self.assertEqual(set(data.keys()), self.REQUIRED)

    def test_creep_onset_not_above_service_ceiling(self):
        for name, data in MATERIALS.items():
            with self.subTest(material=name):
                self.assertLessEqual(data["creep_onset_c"], data["t_service_c"])

    def test_cte_positive(self):
        for name, data in MATERIALS.items():
            with self.subTest(material=name):
                self.assertGreater(data["cte"], 0)


class TestConverters(unittest.TestCase):
    def test_f_to_c_known_points(self):
        self.assertAlmostEqual(f_to_c(32.0), 0.0)
        self.assertAlmostEqual(f_to_c(212.0), 100.0)

    def test_surface_hotter_than_air_in_sun(self):
        self.assertGreater(surface_temp_c(40.0), 40.0)

    def test_wind_reduces_surface_amplification(self):
        calm = surface_temp_c(40.0, wind_ms=0.0)
        windy = surface_temp_c(40.0, wind_ms=5.0)
        self.assertLess(windy, calm)

    def test_wet_bulb_below_dry_bulb(self):
        # unsaturated air: wet bulb sits below dry bulb
        self.assertLess(wet_bulb_c(40.0, 45.0), 40.0)


class TestPairMismatch(unittest.TestCase):
    def test_d_cte_order_agnostic(self):
        ab = pair_mismatch("steel_1018", "nylon_66", 100, 50)
        ba = pair_mismatch("nylon_66", "steel_1018", 100, 50)
        self.assertEqual(ab["d_cte_1e6K"], ba["d_cte_1e6K"])
        self.assertEqual(ab["microstrain"], ba["microstrain"])

    def test_matched_cte_is_green(self):
        # concrete vs steel: near-identical CTE, small strain
        res = pair_mismatch("concrete", "steel_1018", 300, 85)
        self.assertEqual(res["flag"], "GREEN")

    def test_flag_thresholds(self):
        # microstrain = d_cte * delta_t; pick delta_t to straddle bands
        d_cte = abs(MATERIALS["aluminum_6061"]["cte"]
                    - MATERIALS["steel_1018"]["cte"])  # 11.9
        green = pair_mismatch("aluminum_6061", "steel_1018", 100, 400 / d_cte)
        yellow = pair_mismatch("aluminum_6061", "steel_1018", 100, 700 / d_cte)
        red = pair_mismatch("aluminum_6061", "steel_1018", 100, 1500 / d_cte)
        self.assertEqual(green["flag"], "GREEN")
        self.assertEqual(yellow["flag"], "YELLOW")
        self.assertEqual(red["flag"], "RED")

    def test_displacement_scales_with_span(self):
        short = pair_mismatch("steel_1018", "nylon_66", 100, 50)
        long = pair_mismatch("steel_1018", "nylon_66", 200, 50)
        self.assertAlmostEqual(long["displacement_um"],
                               2 * short["displacement_um"], places=1)


class TestCompressionSet(unittest.TestCase):
    def test_no_model_for_unknown_material(self):
        res = compression_set("steel_1018", 100, 30)
        self.assertIn("note", res)
        self.assertNotIn("set_fraction", res)

    def test_q10_acceleration_at_reference(self):
        # at the 70 C reference, accel factor is 1.0
        res = compression_set("epdm_rubber", 70.0, 10)
        self.assertAlmostEqual(res["set_fraction"], 0.004 * 10, places=3)

    def test_clamped_to_one(self):
        res = compression_set("nitrile_rubber", 150.0, 365)
        self.assertLessEqual(res["set_fraction"], 1.0)
        self.assertEqual(res["flag"], "RED")

    def test_hotter_sets_faster(self):
        cool = compression_set("epdm_rubber", 70.0, 5)["set_fraction"]
        hot = compression_set("epdm_rubber", 90.0, 5)["set_fraction"]
        self.assertGreater(hot, cool)


class TestAging(unittest.TestCase):
    def test_identity_at_reference(self):
        self.assertAlmostEqual(aging_multiplier(25.0), 1.0, places=6)

    def test_monotone_increasing(self):
        self.assertLess(aging_multiplier(25.0), aging_multiplier(50.0))
        self.assertLess(aging_multiplier(50.0), aging_multiplier(70.0))

    def test_sensor_drift_shape(self):
        res = sensor_drift(43.3, 15.0, 0.25, 45)
        self.assertIn("projected_drift_pct", res)
        self.assertIn(res["flag"], {"GREEN", "YELLOW", "RED"})


class TestCorruptionSignature(unittest.TestCase):
    def test_signature_fires_on_collapse_and_clip(self):
        before = [20, 25, 30, 35, 40, 45]
        during = [37.0, 37.1, 37.2, 37.0, 37.1]  # low variance, clipped range
        res = corruption_signature(before, during)
        self.assertTrue(res["variance_collapse"])
        self.assertTrue(res["range_clipping"])
        self.assertIn("LOW-BIAS", res["read"])

    def test_no_signature_when_range_preserved(self):
        before = [20, 25, 30, 35, 40, 45]
        during = [22, 28, 33, 38, 44, 50]
        res = corruption_signature(before, during)
        self.assertFalse(res["variance_collapse"])
        self.assertNotIn("LOW-BIAS", res["read"])


class TestAuditDriver(unittest.TestCase):
    def test_worst_flag_wins(self):
        # one RED pair should drive the whole package RED
        res = audit(air_f=110, rh_pct=45, days=45,
                    pairs=[("aluminum_6061", "abs_plastic", 150)],
                    gaskets=[])
        self.assertEqual(res["verdict"], "RED")

    def test_benign_case_not_red(self):
        # matched CTE pair, no gaskets, mild conditions
        res = audit(air_f=70, rh_pct=40, days=1,
                    pairs=[("concrete", "steel_1018", 300)],
                    gaskets=[])
        self.assertIn(res["verdict"], {"GREEN", "YELLOW"})

    def test_shipped_heat_dome_case_is_red(self):
        res = audit(air_f=110, rh_pct=45, days=45,
                    pairs=[("aluminum_6061", "abs_plastic", 150),
                           ("steel_1018", "nylon_66", 100),
                           ("concrete", "steel_1018", 300)],
                    gaskets=["epdm_rubber", "nitrile_rubber"])
        self.assertEqual(res["verdict"], "RED")
        self.assertEqual(len(res["pairs"]), 3)
        self.assertEqual(len(res["gaskets"]), 2)

    def test_corruption_readings_optional_absent_by_default(self):
        res = audit(air_f=70, rh_pct=40, days=1,
                    pairs=[("concrete", "steel_1018", 300)], gaskets=[])
        self.assertNotIn("corruption", res)

    def test_corruption_signature_fires_and_flags_red(self):
        # Physical layers are benign (GREEN) but the record itself is
        # corrupted -> the whole package verdict must go RED.
        before = [20, 25, 30, 35, 40, 45]
        during = [37.0, 37.1, 37.2, 37.0, 37.1]
        res = audit(air_f=70, rh_pct=40, days=1,
                    pairs=[("concrete", "steel_1018", 300)], gaskets=[],
                    readings_before=before, readings_during=during)
        self.assertIn("corruption", res)
        self.assertTrue(res["corruption"]["variance_collapse"])
        self.assertTrue(res["corruption"]["range_clipping"])
        self.assertEqual(res["verdict"], "RED")

    def test_corruption_negative_leaves_verdict_alone(self):
        # Signature does NOT fire; physical layers benign -> not RED.
        before = [20, 25, 30, 35, 40, 45]
        during = [22, 28, 33, 38, 44, 50]
        res = audit(air_f=70, rh_pct=40, days=1,
                    pairs=[("concrete", "steel_1018", 300)], gaskets=[],
                    readings_before=before, readings_during=during)
        self.assertIn("corruption", res)
        self.assertNotEqual(res["verdict"], "RED")


if __name__ == "__main__":
    unittest.main()
