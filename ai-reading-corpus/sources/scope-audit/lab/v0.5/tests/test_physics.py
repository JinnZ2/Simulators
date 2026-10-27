"""Tests for the v0.4 law-driven physics demonstration domains."""
from __future__ import annotations
import math
import unittest

from scope_audit_lab.core import validate_record
from scope_audit_lab.physics_demos import (
    stopped_light_cases, polarized_light_cases, em_resonance_cases,
    gravity_transect_cases, doppler_passby_cases, rlc_coupling_entries,
    run_physics_demo_suite, GENERATORS, DOMAINS, SCAN_THRESHOLDS,
    LAW_SIM_LABEL, G_SI, MGAL_PER_SI,
)


class StoppedLightTests(unittest.TestCase):
    def test_calibration_point(self):
        cases, _ = stopped_light_cases()
        for c in cases:
            if abs(c.factor_value - 1.0) < 0.05:
                self.assertAlmostEqual(c.output_value, 17.0, delta=2.0)
                return
        # exact grid may skip 1.0 MHz; check the law at the nearest point
        nearest = min(cases, key=lambda c: abs(c.factor_value - 1.0))
        expected = 17.0  # by construction of omega_k2
        omega = nearest.factor_value * 1e6
        omega_k2 = (1e6)**2 * (299_792_458.0 / 17.0 - 1.0)
        v = 299_792_458.0 * omega**2 / (omega**2 + omega_k2)
        self.assertAlmostEqual(nearest.output_value, v, places=9)

    def test_monotonic_decrease_in_given_order(self):
        cases, _ = stopped_light_cases()
        outs = [c.output_value for c in cases]
        for a, b in zip(outs, outs[1:]):
            self.assertGreater(a, b)

    def test_provenance_declares_no_planted_structure(self):
        _, prov = stopped_light_cases()
        self.assertEqual(prov["planted_structure"], "none (smooth law curve)")
        self.assertIn("doi:10.1038/17561", prov["reference"])


class PolarizedLightTests(unittest.TestCase):
    def test_malus_endpoints(self):
        cases, _ = polarized_light_cases()
        self.assertEqual(cases[0].output_value, 1000.0)
        mid = [c for c in cases if c.factor_value == 90.0][0]
        self.assertEqual(mid.output_value, 0.0)
        last = cases[-1]
        self.assertAlmostEqual(last.output_value, 1000.0, places=9)

    def test_symmetry(self):
        cases, _ = polarized_light_cases(step_deg=10.0)
        by_angle = {c.factor_value: c.output_value for c in cases}
        for theta in (10.0, 20.0, 30.0, 40.0, 60.0, 80.0):
            self.assertAlmostEqual(by_angle[theta], by_angle[180.0 - theta],
                                   places=9)

    def test_steepest_at_45_and_135(self):
        cases, _ = polarized_light_cases()
        deltas = [abs(b.output_value - a.output_value)
                  for a, b in zip(cases, cases[1:])]
        lefts = [a.factor_value for a in cases[:-1]]
        steepest = lefts[deltas.index(max(deltas))]
        self.assertIn(steepest, (40.0, 45.0, 130.0, 135.0))


class EmResonanceTests(unittest.TestCase):
    def test_peak_at_resonance(self):
        cases, prov = em_resonance_cases()
        f0 = prov["parameters"]["resonance_hz"]
        self.assertAlmostEqual(f0, 159.155, places=2)
        peak = max(cases, key=lambda c: c.output_value)
        self.assertGreater(peak.output_value, 40.0)  # ideal peak is V0/R = 50 mA
        self.assertLess(abs(peak.factor_value - f0) / f0, 0.07)

    def test_far_from_resonance_current_small(self):
        cases, _ = em_resonance_cases()
        self.assertLess(cases[0].output_value, 20.0)
        self.assertLess(cases[-1].output_value, 20.0)

    def test_coupling_entries_shape(self):
        entries = rlc_coupling_entries()
        self.assertEqual(len(entries), 30)
        for e in entries:
            self.assertIn("factor_a", e)
            self.assertIn("factor_b", e)
            self.assertIn("output", e)
        self.assertEqual(len({e["case_id"] for e in entries}), 30)


class GravityTransectTests(unittest.TestCase):
    def test_peak_matches_law(self):
        cases, prov = gravity_transect_cases(noise_sd_mgal=0.0)
        peak = max(cases, key=lambda c: c.output_value)
        self.assertEqual(peak.factor_value, 0.0)
        expected = G_SI * 1e9 / 100.0**2 * MGAL_PER_SI
        self.assertAlmostEqual(peak.output_value, expected, places=12)
        self.assertAlmostEqual(prov["parameters"]["peak_anomaly_mgal"],
                               expected, places=12)

    def test_symmetry_without_noise(self):
        cases, _ = gravity_transect_cases(noise_sd_mgal=0.0)
        by_x = {c.factor_value: c.output_value for c in cases}
        for x in (50.0, 125.0, 300.0):
            self.assertAlmostEqual(by_x[x], by_x[-x], places=12)

    def test_planted_structure_declared(self):
        _, prov = gravity_transect_cases()
        self.assertIn("planted by construction", prov["planted_structure"])

    def test_deterministic_given_seed(self):
        a, _ = gravity_transect_cases(seed=5)
        b, _ = gravity_transect_cases(seed=5)
        self.assertEqual([c.output_value for c in a],
                         [c.output_value for c in b])


class DopplerTests(unittest.TestCase):
    def test_frequency_ordering(self):
        cases, _ = doppler_passby_cases()
        by_t = {c.factor_value: c.output_value for c in cases}
        self.assertGreater(by_t[-10.0], 1000.0)
        self.assertEqual(by_t[0.0], 1000.0)
        self.assertLess(by_t[10.0], 1000.0)

    def test_steepest_near_closest_approach(self):
        cases, _ = doppler_passby_cases()
        deltas = [abs(b.output_value - a.output_value)
                  for a, b in zip(cases, cases[1:])]
        lefts = [a.factor_value for a in cases[:-1]]
        steepest = lefts[deltas.index(max(deltas))]
        self.assertLessEqual(abs(steepest), 1.0)


class SuiteTests(unittest.TestCase):
    def test_suite_shape_and_validation(self):
        records = run_physics_demo_suite()
        scans = [r for r in records if r.record_type == "transition_scan"]
        exps = [r for r in records if r.record_type == "experiment"]
        self.assertEqual(len(scans), len(DOMAINS))
        self.assertEqual(len(exps), 4)
        self.assertEqual(records[-1].record_type, "audit_event")
        for r in records:
            validate_record(r.to_dict())

    def test_every_scan_flags_at_least_one_region(self):
        records = run_physics_demo_suite()
        for r in records[:len(DOMAINS)]:
            self.assertGreater(len(r.payload["candidate_regions"]), 0,
                               r.payload["scan_label"])

    def test_law_labels_present(self):
        records = run_physics_demo_suite()
        for r in records[:len(DOMAINS)]:
            self.assertIn("law_provenance", r.payload)
            blob = str(r.payload)
            self.assertIn("law-driven simulation", blob)
        self.assertIn("interpretation", records[0].payload)

    def test_thresholds_match_domains(self):
        records = run_physics_demo_suite()
        for domain, r in zip(DOMAINS, records[:len(DOMAINS)]):
            self.assertEqual(r.payload["config"]["threshold"],
                             SCAN_THRESHOLDS[domain])

    def test_payloads_deterministic(self):
        # record ids are random by design; compare payloads with id-bearing
        # cross-reference fields scrubbed
        a = run_physics_demo_suite()
        b = run_physics_demo_suite()
        for ra, rb in zip(a, b):
            pa = {k: v for k, v in ra.payload.items()
                  if k not in ("linked_record_ids", "subject_record_ids")}
            pb = {k: v for k, v in rb.payload.items()
                  if k not in ("linked_record_ids", "subject_record_ids")}
            self.assertEqual(pa, pb)

    def test_no_verdict_anywhere(self):
        for r in run_physics_demo_suite():
            if "verdict" in r.payload:
                self.assertIsNone(r.payload["verdict"])
            blob = str(r.payload)
            self.assertNotIn("significant at", blob)
            self.assertNotIn("boundary confirmed", blob)


if __name__ == "__main__":
    unittest.main()
