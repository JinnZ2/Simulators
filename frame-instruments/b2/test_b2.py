"""B2.5 tests. stdlib unittest, synthetic fixtures in-file. Run: python3 test_b2.py"""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import agree, conditions, lock, order  # noqa: E402
from ficommon import read_jsonl, write_jsonl  # noqa: E402
from runrecord import read_records  # noqa: E402

CASES = [{"case_id": "k1", "statement": "The pump ran dry for nine minutes.",
          "key_posed": "whether the pump ran dry", "key_target": "the pump", "key_why": "dry running is the stated event"},
         {"case_id": "k2", "statement": "Two valves were left open overnight.",
          "key_posed": "whether two valves were open", "key_target": "the valves", "key_why": "the count is stated"}]


def resp(reader, case, cond, posed, target):
    return {"reader_id": reader, "case_id": case, "condition": cond, "posed": posed, "target": target}


class B2Tests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="b2test_")
        self.runs = os.path.join(self.d, "runs")

    def tearDown(self):
        shutil.rmtree(self.d)

    def p(self, name):
        return os.path.join(self.d, name)

    def test_lock_refuses_release_without_commit(self):
        write_jsonl(self.p("cases.jsonl"), CASES)
        rc = lock.main(["release", "--reader", "r1", "--case", "k1", "--cases", self.p("cases.jsonl"),
                        "--commits", self.p("commits.jsonl"), "--out", self.p("rel.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 2)
        self.assertEqual(read_records(self.runs)[-1]["status"], "void")
        self.assertFalse(os.path.exists(self.p("rel.jsonl")))
        with open(self.p("resp.json"), "w") as fh:
            json.dump({"posed": "x", "target": "y"}, fh)
        self.assertEqual(lock.main(["commit", "--reader", "r1", "--case", "k1", "--response", self.p("resp.json"),
                                    "--commits", self.p("commits.jsonl"), "--runs", self.runs]), 0)
        rc = lock.main(["release", "--reader", "r1", "--case", "k1", "--cases", self.p("cases.jsonl"),
                        "--commits", self.p("commits.jsonl"), "--out", self.p("rel.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 0)
        rel = read_jsonl(self.p("rel.jsonl"))[0]
        self.assertEqual(rel["condition"], "D2")
        self.assertIn("posed: whether the pump ran dry", rel["presented_text"])
        self.assertNotIn(CASES[0]["statement"], rel["presented_text"])

    def test_conditions_never_leak(self):
        write_jsonl(self.p("cases.jsonl"), CASES)
        self.assertEqual(conditions.main([self.p("cases.jsonl"), "--out", self.p("cond"), "--runs", self.runs]), 0)
        for cond in conditions.CONDITIONS:
            rows = read_jsonl(os.path.join(self.p("cond"), cond + ".jsonl"))
            self.assertEqual(len(rows), len(CASES))
            for row in rows:
                self.assertEqual(set(row), {"case_id", "condition", "presented_text"})
                c = [x for x in CASES if x["case_id"] == row["case_id"]][0]
                if cond in ("A", "D"):
                    for k in ("key_posed", "key_target", "key_why"):
                        self.assertNotIn(c[k], row["presented_text"])
                if cond == "B":
                    self.assertNotIn(c["statement"], row["presented_text"])
        leaky = [dict(CASES[0], key_why="see: " + CASES[0]["statement"])]
        with self.assertRaises(conditions.Invalid):
            conditions.build(leaky)
        mixed = [dict(CASES[0], arm="single"), dict(CASES[1], arm="split")]
        with self.assertRaises(conditions.Void):
            conditions.validate_cases(mixed)

    def test_order_latin_square_and_shortfall(self):
        rows, short = order.assign(6, 5)
        self.assertEqual(len(rows), 6)
        self.assertEqual(short, 2)
        block = [r["order"] for r in rows[:4]]
        for pos in range(4):
            self.assertEqual(sorted(o[pos] for o in block), ["A", "B", "C", "D"])
        self.assertEqual(sum(1 for r in rows if r["latin_square"]), 4)
        self.assertEqual(rows, order.assign(6, 5)[0])

    def test_agreement_math_three_auditors(self):
        rows = [resp("r1", "k1", "B", "X", "P"), resp("r2", "k1", "B", "x ", "Q"), resp("r3", "k1", "B", "Y", "R")]
        s = agree.pair_stats(rows)
        self.assertEqual(s["n_auditors"], 3)
        self.assertAlmostEqual(s["agree_posed"], 1 / 3.0, places=4)
        self.assertEqual(s["agree_target"], 0.0)
        self.assertEqual(s["full_disagreement_pairs"], 2)

    def test_ad_divergence_detected(self):
        commits = []
        rows = []
        for r in ("r1", "r2"):
            rows.append(resp(r, "k1", "A", "whether the pump ran dry", "the pump"))
        for r in ("r3", "r4"):
            d1 = resp(r, "k1", "D1", "whether the nine minutes matter", "the operator")
            rows.append(d1)
            commits.append({"reader_id": r, "case_id": "k1", "response": {"posed": d1["posed"], "target": d1["target"]},
                            "sha256": lock.response_hash({"posed": d1["posed"], "target": d1["target"]})})
            rows.append(resp(r, "k1", "D2", "whether the pump ran dry", "the pump"))
        rows.append(resp("r5", "k1", "C", "whether the pump ran dry", "the pump"))
        out = agree.score(rows, CASES, commits, 0.2)
        head = out[0]
        self.assertTrue(head["failed"])
        chk = head["a_vs_d1_check"][0]
        self.assertEqual(chk["within_A_posed"], 1.0)
        self.assertEqual(chk["cross_A_D1_posed"], 0.0)
        self.assertIn("cross below withins", chk["diverged_posed"])
        anchor = [o for o in out if "ratify_rate_D" in o and o["case_id"] == "k1"][0]
        self.assertEqual(anchor["n_D_independent_at_D1"], 2)
        self.assertEqual(anchor["ratify_rate_D"], 1.0)
        self.assertEqual(anchor["key_match_rate_C"], 1.0)
        rows2 = [r for r in rows if r["condition"] != "D1"] + [resp("r3", "k1", "D1", "tampered", "x")]
        with self.assertRaises(agree.Invalid):
            agree.score(rows2, CASES, commits, 0.2)
        same_rows = [resp("r1", "k1", "A", "X", "T"), resp("r2", "k1", "A", "X", "T")] + \
                    [r for r in rows if r["condition"] in ("D1", "D2")]
        for r in same_rows:
            if r["condition"] == "D1":
                r["posed"], r["target"] = "X", "T"
        commits2 = [{"reader_id": r, "case_id": "k1", "response": {"posed": "X", "target": "T"},
                     "sha256": lock.response_hash({"posed": "X", "target": "T"})} for r in ("r3", "r4")]
        self.assertFalse(agree.score(same_rows, CASES, commits2, 0.2)[0]["failed"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
