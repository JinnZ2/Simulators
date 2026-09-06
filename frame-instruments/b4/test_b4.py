"""B4.9 tests. stdlib unittest, synthetic fixtures in-file.
The fixture item is CONSTRUCTED for the test and is not a published item.
Run: python3 test_b4.py
"""
import glob
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agreement, calibrate, grade, items, nullshuffle, reconstruct, report, requirements  # noqa: E402
from common import FORBIDDEN, read_jsonl, write_jsonl  # noqa: E402
from runrecord import Run, read_records  # noqa: E402

ITEMS = [
    {"item_id": "fx1", "source": "constructed fixture (test_b4.py), not a published item",
     "text_verbatim": "A valve must be closed or left open. Choose.", "branches_stated": 2, "arm": "hypothetical"},
    {"item_id": "fx2", "source": "constructed fixture (test_b4.py), not a published item",
     "text_verbatim": "The crew can wait or proceed. Choose.", "branches_stated": 2, "arm": "hypothetical"},
]
DOC_ITEMS = [{"item_id": "dx1", "source": "constructed fixture, standing in for a documented item",
              "text_verbatim": "Constructed documented-arm text.", "branches_stated": 2, "arm": "documented"}]


def req(item, rec, rid, text, status, test, layer="constructed"):
    return {"item_id": item, "reconstructor_id": rec, "req_id": rid, "requirement_text": text,
            "status": status, "settling_test": test, "layer": layer}


REQS = [
    req("fx1", "r1", "a", "no remote actuator installed", "true", "measure actuator count on the valve"),
    req("fx1", "r1", "b", "budget line for actuators absent", "lapsed", "read the funding decision of the year"),
    req("fx1", "r2", "a", "the valve has no remote actuator", "true", "count actuators by instrument survey"),
    req("fx1", "r2", "c", "only one operator on shift", "undifferentiated", "staffing roster for the shift"),
    req("fx2", "r1", "a", "no third crew exists", "unknown", "procurement record of crew contracts"),
    req("fx2", "r2", "a", "no relief crew is funded", "partial", "the funding rule for relief crews"),
]
MATCHES = [{"item_id": "fx1", "req_a": "r1/a", "req_b": "r2/a", "matched": True},
           {"item_id": "fx1", "req_a": "r1/b", "req_b": "r2/c", "matched": False},
           {"item_id": "fx2", "req_a": "r1/a", "req_b": "r2/a", "matched": True}]


class B4Tests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="b4test_")
        self.runs = os.path.join(self.d, "runs")

    def tearDown(self):
        shutil.rmtree(self.d)

    def p(self, name):
        return os.path.join(self.d, name)

    def w(self, name, rows):
        write_jsonl(self.p(name), rows)
        return self.p(name)

    def last_status(self):
        return read_records(self.runs)[-1]["status"]

    def test_two_state_file_is_void(self):
        rows = [dict(r, status="true") for r in REQS]
        rc = requirements.main([self.w("r.jsonl", rows), "--out", self.p("o.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 2)
        self.assertEqual(self.last_status(), "void")
        self.assertFalse(os.path.exists(self.p("o.jsonl")))

    def test_empty_settling_test_rejected(self):
        rows = [dict(r) for r in REQS]
        rows[0]["settling_test"] = "  "
        rc = requirements.main([self.w("r.jsonl", rows), "--out", self.p("o.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 1)
        self.assertEqual(self.last_status(), "error")

    def test_valid_requirements_pass(self):
        rc = requirements.main([self.w("r.jsonl", REQS), "--items", self.w("i.jsonl", ITEMS),
                                "--out", self.p("o.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 0)
        self.assertEqual(len(read_jsonl(self.p("o.jsonl"))), len(REQS))

    def test_items_refuse_mixed_arms(self):
        rc = items.main([self.w("i.jsonl", ITEMS + DOC_ITEMS), "--out", self.p("o.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 2)
        self.assertEqual(self.last_status(), "void")

    def test_reconstruct_emits_only_text_verbatim(self):
        out = self.p("prompts")
        rc = reconstruct.main([self.w("i.jsonl", ITEMS), "--reconstructors", "r1,r2,r3", "--out", out, "--runs", self.runs])
        self.assertEqual(rc, 0)
        files = glob.glob(os.path.join(out, "*", "*.jsonl"))
        self.assertEqual(len(files), 6)
        for f in files:
            with open(f) as fh:
                lines = [ln for ln in fh.read().split("\n") if ln.strip()]
            self.assertEqual(len(lines), 1, f)
            self.assertEqual(set(json.loads(lines[0])), {"text_verbatim"}, f)

    def test_shuffle_preserves_count_and_multiset(self):
        out, _ = nullshuffle.shuffle(REQS, seed=7)
        self.assertEqual(len(out), len(REQS))
        self.assertEqual(sorted(r["requirement_text"] for r in out), sorted(r["requirement_text"] for r in REQS))
        for o in out:
            self.assertEqual(o["shuffle_seed"], 7)
        orig = {r["requirement_text"]: r["item_id"] for r in REQS}  # texts unique in fixture
        for o in out:
            self.assertNotEqual(o["item_id"], orig[o["requirement_text"]])
        again, _ = nullshuffle.shuffle(REQS, seed=7)
        self.assertEqual(out, again)

    def test_identical_tests_different_wording_agree(self):
        out = agreement.score(REQS, MATCHES, "fixture matcher")
        fx1 = [o for o in out if o["item_id"] == "fx1"][0]
        self.assertEqual(fx1["pairs"][0]["matched_a"], 1)
        self.assertEqual(fx1["pairs"][0]["matched_b"], 1)
        self.assertEqual(fx1["pairs"][0]["agreement"], 0.5)
        self.assertEqual(fx1["match_source"], "fixture matcher")
        self.assertEqual(sorted(s["ref"] for s in fx1["singletons"]), ["r1/b", "r2/c"])

    def test_singleton_survives_into_report(self):
        text = self.full_pipeline()
        self.assertIn("r1/b", text)
        self.assertIn("budget line for actuators absent", text)
        self.assertIn("## 7. REAL vs SHUFFLED", text)
        self.assertEqual(text.count("\n## "), 9)

    def test_report_void_without_shuffled(self):
        self.full_pipeline()
        rc = report.main(["--items", self.p("i.jsonl"), "--requirements", self.p("rv.jsonl"),
                          "--prompts", self.p("prompts"), "--grade", self.p("g.jsonl"),
                          "--grade-shuffled", self.p("missing.jsonl"), "--agreement", self.p("a.jsonl"),
                          "--agreement-shuffled", self.p("as.jsonl"), "--out", self.p("r2.md"), "--runs", self.runs])
        self.assertEqual(rc, 2)
        self.assertFalse(os.path.exists(self.p("r2.md")))

    def test_calibration_two_recovered_one_missed_one_beyond(self):
        rows = [req("dx1", "r1", "a", "A", "true", "measure A"), req("dx1", "r1", "b", "B", "true", "measure B"),
                req("dx1", "r1", "c", "C", "unknown", "measure C")]
        facs = [{"item_id": "dx1", "factor_id": "f%d" % i, "factor_text": "F%d" % i, "report_source": "fixture"}
                for i in (1, 2, 3)]
        fm = [{"item_id": "dx1", "factor_id": "f1", "req": "r1/a", "matched": True},
              {"item_id": "dx1", "factor_id": "f2", "req": "r1/b", "matched": True}]
        out = calibrate.calibrate(rows, DOC_ITEMS, facs, fm, "fixture matcher")
        self.assertEqual((out[0]["n_recovered"], out[0]["n_missed"], out[0]["n_beyond_report"]), (2, 1, 1))
        self.assertEqual(out[0]["beyond_report"], ["r1/c"])
        with self.assertRaises(calibrate.Void):
            calibrate.calibrate(rows, ITEMS, facs, fm, "x")

    def test_grade_unresolved_printed(self):
        g = grade.grade(REQS, list(grade.PHYSICAL_CUES), list(grade.POLICY_CUES))
        fx1 = [x for x in g if x["item_id"] == "fx1"][0]
        self.assertEqual(fx1["physical"] + fx1["policy"] + fx1["unresolved"], fx1["n_requirements"])
        both = grade.settles_by("measure the budget", grade.compile_cues(grade.PHYSICAL_CUES),
                                grade.compile_cues(grade.POLICY_CUES))
        self.assertEqual(both, "unresolved_both")

    def test_failed_run_still_writes_record(self):
        with self.assertRaises(RuntimeError):
            with Run("t", {}, None, [], "x", self.runs):
                raise RuntimeError("boom")
        rec = read_records(self.runs)[-1]
        self.assertEqual(rec["status"], "error")
        self.assertIn("boom", rec["notes"])

    def test_no_forbidden_fields_in_outputs(self):
        self.full_pipeline()
        for f in glob.glob(self.p("*.jsonl")):
            for row in read_jsonl(f):
                for k in FORBIDDEN:
                    self.assertNotIn(k, row, f)

    def full_pipeline(self):
        i = self.w("i.jsonl", ITEMS)
        items.main([i, "--out", self.p("iv.jsonl"), "--runs", self.runs])
        reconstruct.main([self.p("iv.jsonl"), "--reconstructors", "r1,r2", "--out", self.p("prompts"), "--runs", self.runs])
        requirements.main([self.w("r.jsonl", REQS), "--items", self.p("iv.jsonl"), "--out", self.p("rv.jsonl"), "--runs", self.runs])
        nullshuffle.main([self.p("rv.jsonl"), "--seed", "3", "--out", self.p("rs.jsonl"), "--runs", self.runs])
        grade.main([self.p("rv.jsonl"), "--out", self.p("g.jsonl"), "--runs", self.runs])
        grade.main([self.p("rs.jsonl"), "--out", self.p("gs.jsonl"), "--runs", self.runs])
        agreement.main([self.p("rv.jsonl"), "--matches", self.w("m.jsonl", MATCHES), "--match-source",
                        "fixture matcher (real)", "--out", self.p("a.jsonl"), "--runs", self.runs])
        agreement.main([self.p("rs.jsonl"), "--matches", self.w("ms.jsonl", []), "--match-source",
                        "fixture matcher (shuffled, no links)", "--out", self.p("as.jsonl"), "--runs", self.runs])
        rc = report.main(["--items", self.p("iv.jsonl"), "--requirements", self.p("rv.jsonl"),
                          "--prompts", self.p("prompts"), "--grade", self.p("g.jsonl"),
                          "--grade-shuffled", self.p("gs.jsonl"), "--agreement", self.p("a.jsonl"),
                          "--agreement-shuffled", self.p("as.jsonl"), "--out", self.p("report.md"), "--runs", self.runs])
        self.assertEqual(rc, 0)
        with open(self.p("report.md")) as fh:
            return fh.read()


if __name__ == "__main__":
    unittest.main(verbosity=1)
