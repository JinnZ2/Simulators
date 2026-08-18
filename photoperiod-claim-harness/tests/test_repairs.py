"""
test_repairs.py -- one test per defect in CLAIM_TABLE.md.

CC0-1.0. Standard library only.

Each test asserted the BROKEN behaviour when it was written and asserts the
repair now, so a regression turns it red. Same arrangement as
../../reasoning-gate/tests/test_gate.py and
../../criteria-drift/tests/test_repairs.py.

    python3 -m unittest discover tests
"""

import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

os.environ["PCH_LOG"] = os.path.join(tempfile.mkdtemp(), "test.jsonl")
import photoperiod_claim_harness as H  # noqa: E402

H.LOGPATH = os.environ["PCH_LOG"]


def claim(cid):
    return next(c for c in H.CLAIM_TABLE if c["id"] == cid)


# ---------------------------------------------------------------------------
# PCH_001 -- a predicate that can fail


class PredicateCanFail(unittest.TestCase):

    def test_c1_still_decides_on_a_live_run(self):
        out = H.s1_mass_denominator()
        self.assertGreater(out["signature_cells"], 0)
        self.assertFalse(claim("C1")["predicate"](out))   # wide spread

    def test_empty_signature_is_undecided_not_supported(self):
        """Was: spread of an empty set = 0.0, which passed `< 1.5`."""
        orig = H._s1_run
        H._s1_run = lambda sc, sae, sk, days=8, dt=0.5: orig(
            sc, 0.0, sk, days=days, dt=dt)
        try:
            rec, out, _ = H.run_claim("C1")
        finally:
            H._s1_run = orig
        self.assertEqual(out["signature_cells"], 0)
        self.assertTrue(rec["status"].startswith("UNDECIDED"))

    def test_require_raises_with_its_reason(self):
        with self.assertRaises(ValueError):
            H.require(False, "because")
        self.assertTrue(H.require(True, "fine"))


# ---------------------------------------------------------------------------
# PCH_002 -- sign and magnitude are separate readouts


class SignAndMagnitude(unittest.TestCase):

    def test_sign_agreement_is_reported_alongside_spread(self):
        out = H.s1_mass_denominator()
        self.assertIn("signature_sign_agreement", out)
        self.assertIn("signature_cells_below_1", out)
        self.assertGreater(out["signature_spread"], 1.5)
        self.assertEqual(out["signature_sign_agreement"], 1.0)

    def test_sign_agreement_is_none_when_there_is_nothing_to_agree_on(self):
        orig = H._s1_run
        H._s1_run = lambda sc, sae, sk, days=8, dt=0.5: orig(
            sc, 0.0, sk, days=days, dt=dt)
        try:
            out = H.s1_mass_denominator()
        finally:
            H._s1_run = orig
        self.assertIsNone(out["signature_sign_agreement"])

    def test_reads_line_names_the_new_readout(self):
        self.assertIn("signature_sign_agreement", claim("C1")["reads"])
        self.assertIn("UNDECIDED", claim("C1")["reads"])


# ---------------------------------------------------------------------------
# PCH_003 -- the guard screens every field


class GuardCoverage(unittest.TestCase):

    POISON = "tune to match the reported result"

    def _edit(self, **over):
        kw = dict(sim_id="S2", mechanism="add a term", basis="literature",
                  prediction="the term shifts the curve",
                  affects=["C2"], reason="mechanism work")
        kw.update(over)
        return H.MechanismEdit(**kw)

    def test_reason_is_screened(self):
        with self.assertRaises(ValueError):
            self._edit(reason=self.POISON)

    def test_mechanism_is_screened(self):
        with self.assertRaises(ValueError):
            self._edit(mechanism=self.POISON)

    def test_basis_is_screened(self):
        """Was: accepted -- `basis` was not read."""
        with self.assertRaises(ValueError):
            self._edit(basis=self.POISON)

    def test_prediction_is_screened(self):
        """Was: accepted -- `prediction` was not read."""
        with self.assertRaises(ValueError):
            self._edit(prediction=self.POISON)

    def test_a_clean_edit_still_registers(self):
        e = self._edit()
        self.assertEqual(e.rec["kind"], "MECHANISM_EDIT")
        self.assertIn("file_hash_before", e.rec)


# ---------------------------------------------------------------------------
# PCH_004 -- settle adjudicates, and knows whether the edit happened


class Settle(unittest.TestCase):

    def _edit(self):
        return H.MechanismEdit("S2", mechanism="add photoinhibition",
                               basis="photoinhibition literature",
                               prediction="low duty penalised further",
                               affects=["C2"], reason="mechanism addition")

    def test_settle_requires_a_bool(self):
        """Was: settle(observed) wrote prediction_held=None forever."""
        e = self._edit()
        with self.assertRaises(ValueError):
            e.settle({"best_duty": 1.0}, None)
        with self.assertRaises(ValueError):
            e.settle({"best_duty": 1.0}, "yes")

    def test_settle_refuses_when_the_file_did_not_change(self):
        """Was: before == after and nothing noticed."""
        e = self._edit()
        with self.assertRaises(ValueError) as cm:
            e.settle({"best_duty": 1.0}, True)
        self.assertIn("hash unchanged", str(cm.exception))

    def test_abandon_is_the_path_for_an_edit_decided_against(self):
        e = self._edit()
        rec = e.abandon("photoinhibition needs an irradiance ceiling the "
                        "spec does not declare")
        self.assertEqual(rec["kind"], "MECHANISM_EDIT_ABANDONED")
        self.assertFalse(rec["file_changed"])

    def test_settle_records_held_when_the_file_did_change(self):
        e = self._edit()
        e.rec["file_hash_before"] = "deliberately-different"
        rec = e.settle({"best_duty": 1.0}, False)
        self.assertIs(rec["prediction_held"], False)
        self.assertTrue(rec["file_changed"])


# ---------------------------------------------------------------------------
# PCH_005 -- the header's usage example


class Usage(unittest.TestCase):

    def test_header_documents_a_claim_id_for_run(self):
        with open(os.path.join(ROOT, "photoperiod_claim_harness.py"),
                  encoding="utf-8") as fh:
            src = fh.read()
        head = src[:src.index("import hashlib")]
        run_lines = [l for l in head.splitlines()
                     if "photoperiod_claim_harness.py run " in l]
        self.assertTrue(run_lines)
        for line in run_lines:
            arg = line.split("run ")[1].split()[0]
            self.assertIn(arg, [c["id"] for c in H.CLAIM_TABLE])

    def test_sweep_still_documents_a_sim_id(self):
        with open(os.path.join(ROOT, "photoperiod_claim_harness.py"),
                  encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn("sweep S2", src)
        self.assertIn("S2", H.SIMS)


# ---------------------------------------------------------------------------
# PCH_007 -- the readout, and the edit category for it


class Readout(unittest.TestCase):

    def test_dark_interval_curve_is_monotone(self):
        """Was: non-monotone, because arms ending mid-cycle were sampled at
        a different phase."""
        dc = H.s2_pool_charging()["dark_interval_curve"]
        for i in range(1, len(dc)):
            self.assertLessEqual(dc[i][1], dc[i - 1][1])

    def test_the_endpoint_is_still_available(self):
        """The repair adds a readout; it does not remove one."""
        r = H._pchlide_run(duty=0.5, dark_block_h=10.0)
        self.assertIn("Chl", r)
        self.assertIn("Chl_endpoint", r)
        self.assertNotAlmostEqual(r["Chl"], r["Chl_endpoint"], places=3)

    def test_no_verdict_moved(self):
        for cid, want in (("C1", "REFUTED"), ("C2", "REFUTED"),
                          ("C3", "REFUTED"), ("C4", "REFUTED"),
                          ("C5", "SUPPORTED")):
            rec, _, _ = H.run_claim(cid)
            self.assertEqual(rec["status"], want, cid)

    def test_instrument_edit_exists_and_screens(self):
        e = H.InstrumentEdit("S2", readout="mean over final period",
                             artifact="end-of-run sampling phase",
                             unchanged="every mechanism and parameter")
        self.assertEqual(e.rec["kind"], "INSTRUMENT_EDIT")
        with self.assertRaises(ValueError):
            H.InstrumentEdit("S2", readout="tune to match", artifact="x",
                             unchanged="y")

    def test_instrument_edit_takes_no_prediction(self):
        """It is not a claim about the world, so it does not register one."""
        import inspect
        args = inspect.signature(H.InstrumentEdit.__init__).parameters
        self.assertNotIn("prediction", args)


# ---------------------------------------------------------------------------
# the README's pipeline, and the fourth provenance type


class ProsePromises(unittest.TestCase):

    def test_residual_router_runs_on_a_claim_that_did_not_hold(self):
        """Was: defined, never called."""
        rec, _, _ = H.run_claim("C2")
        self.assertEqual(rec["status"], "REFUTED")
        self.assertIn("residual_route", rec)
        for k in ("instrument", "noise", "novel", "missing_variable"):
            self.assertIn(k, rec["residual_route"])

    def test_router_does_not_run_on_a_claim_that_held(self):
        rec, _, _ = H.run_claim("C5")
        self.assertEqual(rec["status"], "SUPPORTED")
        self.assertNotIn("residual_route", rec)

    def test_bench_provenance_has_a_path(self):
        """Was: declared in SOURCE, producible by nothing."""
        log = os.path.join(tempfile.mkdtemp(), "b.jsonl")
        old, H.LOGPATH = H.LOGPATH, log
        try:
            self.assertEqual(H.bench_records(log), [])
            H.record_bench("C1", "kWh_per_g_dry", 0.42, "kWh/g",
                           method="65C to constant mass, 72h",
                           kit="scale 0.01 g, kWh meter")
            got = H.bench_records(log)
        finally:
            H.LOGPATH = old
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["kind"], "BENCH")
        self.assertEqual(got[0]["claim"], "C1")

    def test_bench_refuses_a_number_with_no_method(self):
        with self.assertRaises(ValueError):
            H.record_bench("C1", "q", 1.0, "u", method="  ", kit="k")

    def test_bench_refuses_an_unknown_claim(self):
        with self.assertRaises(ValueError):
            H.record_bench("C99", "q", 1.0, "u", method="m", kit="k")

    def test_hypothesis_block_is_deterministic(self):
        """Was: a wall clock stamped one line above the file hash."""
        res = [H.run_claim(c["id"]) for c in H.CLAIM_TABLE]
        a = H.hypothesis_block(res)
        b = H.hypothesis_block(res)
        self.assertEqual(a, b)
        self.assertNotIn("generated 2", a)
        self.assertIn("run id:", a)

    def test_run_id_moves_with_the_statuses(self):
        res = [H.run_claim(c["id"]) for c in H.CLAIM_TABLE]
        one = H.run_id(res)
        res[0][0]["status"] = "SUPPORTED"
        self.assertNotEqual(one, H.run_id(res))


if __name__ == "__main__":
    unittest.main()
