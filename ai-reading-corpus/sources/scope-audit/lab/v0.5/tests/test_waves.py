"""Tests for the v0.5 waves module (light as electromagnetism + sound)."""
from __future__ import annotations
import math
import unittest

from scope_audit_lab.core import validate_record
from scope_audit_lab.waves import (
    em_unification_comparison, em_spectrum_cases,
    longitudinal_contrast_cases, sound_speed_cases,
    run_waves_demo_suite, MU0, EPS0, C_EXACT, EM_BANDS,
    GAMMA_AIR, R_GAS, M_AIR,
)


class EmUnificationTests(unittest.TestCase):
    def test_residual_within_uncertainty(self):
        rec = em_unification_comparison()
        cmp = rec.payload["comparison"]
        self.assertAlmostEqual(cmp["observed_c_m_per_s"], C_EXACT)
        self.assertLess(abs(cmp["residual_m_per_s"]),
                        cmp["prediction_uncertainty_m_per_s"])
        self.assertIsNotNone(cmp["normalized_residual"])
        self.assertLess(abs(cmp["normalized_residual"]), 1.0)

    def test_prediction_matches_formula(self):
        rec = em_unification_comparison()
        cmp = rec.payload["comparison"]
        self.assertAlmostEqual(cmp["predicted_c_m_per_s"],
                               1.0 / math.sqrt(MU0 * EPS0), places=9)

    def test_record_shape(self):
        rec = em_unification_comparison()
        validate_record(rec.to_dict())
        self.assertEqual(rec.payload["experiment_kind"], "em_unification")
        self.assertEqual(rec.payload["interpretation"], "unassigned")
        self.assertIn("definitional structure", str(rec.payload["limitations"]))


class EmSpectrumTests(unittest.TestCase):
    def test_law_holds_per_case(self):
        cases, _ = em_spectrum_cases()
        for c in cases:
            self.assertAlmostEqual(c.factor_value * c.output_value, C_EXACT,
                                   delta=1e-4 * C_EXACT)

    def test_bands_labeled(self):
        cases, _ = em_spectrum_cases()
        labels = {note.split(": ")[1] for c in cases
                  for note in c.notes if note.startswith("band:")}
        self.assertEqual(labels, {b[0] for b in EM_BANDS})

    def test_monotonic_decrease(self):
        cases, _ = em_spectrum_cases()
        outs = [c.output_value for c in cases]
        for a, b in zip(outs, outs[1:]):
            self.assertGreater(a, b)


class LongitudinalContrastTests(unittest.TestCase):
    def test_flat_series(self):
        cases, _ = longitudinal_contrast_cases()
        self.assertTrue(all(c.output_value == 1000.0 for c in cases))
        self.assertEqual(len(cases), 37)

    def test_contrast_with_malus(self):
        from scope_audit_lab.physics_demos import polarized_light_cases
        lon, _ = longitudinal_contrast_cases()
        mal, _ = polarized_light_cases()
        lon_deltas = [abs(b.output_value - a.output_value)
                      for a, b in zip(lon, lon[1:])]
        mal_deltas = [abs(b.output_value - a.output_value)
                      for a, b in zip(mal, mal[1:])]
        self.assertEqual(max(lon_deltas), 0.0)
        self.assertGreater(max(mal_deltas), 80.0)


class SoundSpeedTests(unittest.TestCase):
    def test_room_temperature_value(self):
        cases, _ = sound_speed_cases()
        by_t = {c.factor_value: c.output_value for c in cases}
        self.assertAlmostEqual(by_t[290.0],
                               math.sqrt(GAMMA_AIR * R_GAS * 290.0 / M_AIR),
                               places=9)
        self.assertTrue(335.0 < by_t[290.0] < 348.0)

    def test_monotonic_increase(self):
        cases, _ = sound_speed_cases()
        outs = [c.output_value for c in cases]
        for a, b in zip(outs, outs[1:]):
            self.assertGreater(b, a)


class WavesSuiteTests(unittest.TestCase):
    def test_suite_validates(self):
        records = run_waves_demo_suite()
        self.assertEqual(len(records), 6)
        for r in records:
            validate_record(r.to_dict())
        self.assertEqual(records[-1].record_type, "audit_event")

    def test_longitudinal_scan_flags_nothing_malus_flags(self):
        records = run_waves_demo_suite()
        scans = {r.payload["scan_label"]: r for r in records
                 if r.record_type == "transition_scan"}
        lon = scans["waves demo: longitudinal rotation (law-driven simulation)"]
        mal = scans["waves demo: Malus contrast (law-driven simulation)"]
        self.assertEqual(len(lon.payload["candidate_regions"]), 0)
        self.assertGreater(len(mal.payload["candidate_regions"]), 10)

    def test_no_verdict_anywhere(self):
        for r in run_waves_demo_suite():
            if "verdict" in r.payload:
                self.assertIsNone(r.payload["verdict"])
            blob = str(r.payload)
            self.assertNotIn("significant at", blob)


if __name__ == "__main__":
    unittest.main()
