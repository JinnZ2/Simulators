"""B3.4 tests. stdlib unittest, synthetic fixtures in-file. Run: python3 test_b3.py"""
import glob
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for _m in ('arms', 'join', 'split'):  # module names recur across builds; purge so a shared process imports this build's
    sys.modules.pop(_m, None)
sys.path.insert(0, os.path.dirname(HERE))
import arms, join, split  # noqa: E402
from ficommon import read_jsonl, write_jsonl  # noqa: E402
from runrecord import read_records  # noqa: E402

STATEMENTS = [{"case_id": "s1", "statement": "The gauge read zero at shift change."},
              {"case_id": "s2", "statement": "The relief line was capped."},
              {"case_id": "s3", "statement": "No log entry exists for the night."}]
KEYS = [{"case_id": "s1", "key_posed": "whether the gauge read zero", "key_target": "the gauge", "key_why": "stated"},
        {"case_id": "s2", "key_posed": "whether the line was capped", "key_target": "the relief line", "key_why": "stated"},
        {"case_id": "s9", "key_posed": "orphan", "key_target": "orphan", "key_why": "no statement"}]


class B3Tests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="b3test_")
        self.runs = os.path.join(self.d, "runs")

    def tearDown(self):
        shutil.rmtree(self.d)

    def p(self, name):
        return os.path.join(self.d, name)

    def test_role_key_input_is_statement_only(self):
        write_jsonl(self.p("st.jsonl"), STATEMENTS)
        self.assertEqual(split.main(["key", self.p("st.jsonl"), "--out", self.p("key"), "--runs", self.runs]), 0)
        files = glob.glob(self.p("key/*.jsonl"))
        self.assertEqual(len(files), 3)
        for f in files:
            with open(f) as fh:
                lines = [ln for ln in fh.read().split("\n") if ln.strip()]
            self.assertEqual(len(lines), 1)
            obj = json.loads(lines[0])
            self.assertEqual(set(obj), {"statement"})
            for k in ("key_posed", "key_target", "key_why", "arm", "case_id", "context", "prompt"):
                self.assertNotIn(k, obj)
        # any field beyond case_id/statement is generation context and is refused
        write_jsonl(self.p("ctx.jsonl"), [dict(STATEMENTS[0], generation_notes="wrote it thinking of a key")])
        rc = split.main(["key", self.p("ctx.jsonl"), "--out", self.p("key2"), "--runs", self.runs])
        self.assertEqual(rc, 1)
        self.assertEqual(read_records(self.runs)[-1]["status"], "error")
        self.assertFalse(os.path.exists(self.p("key2")))
        self.assertEqual(split.main(["case", "--case-ids", "a1,a2", "--out", self.p("case"), "--runs", self.runs]), 0)
        for f in glob.glob(self.p("case/*.jsonl")):
            with open(f) as fh:
                self.assertEqual(set(json.loads(fh.readline())), {"case_id"})

    def test_arms_never_mixed(self):
        joined, _ = join.join(STATEMENTS[:2], KEYS[:2], "split")
        mixed = joined[:1] + [dict(joined[1], arm="single")]
        write_jsonl(self.p("mixed.jsonl"), mixed)
        rc = arms.main([self.p("mixed.jsonl"), "--out", self.p("v.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 2)
        self.assertEqual(read_records(self.runs)[-1]["status"], "void")
        self.assertFalse(os.path.exists(self.p("v.jsonl")))
        write_jsonl(self.p("one.jsonl"), joined)
        self.assertEqual(arms.main([self.p("one.jsonl"), "--out", self.p("v.jsonl"), "--runs", self.runs]), 0)
        self.assertTrue(all(r["arm"] == "split" for r in read_jsonl(self.p("v.jsonl"))))
        with self.assertRaises(arms.Invalid):
            arms.validate([dict(joined[0], arm="merged")])

    def test_join_preserves_ids_and_counts_drops(self):
        write_jsonl(self.p("st.jsonl"), STATEMENTS)
        write_jsonl(self.p("k.jsonl"), KEYS)
        rc = join.main([self.p("st.jsonl"), self.p("k.jsonl"), "--arm", "split", "--out", self.p("c.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 0)
        rows = read_jsonl(self.p("c.jsonl"))
        self.assertEqual([r["case_id"] for r in rows], ["s1", "s2"])
        self.assertEqual(set(rows[0]), {"case_id", "statement", "key_posed", "key_target", "key_why", "arm"})
        rec = read_records(self.runs)[-1]
        self.assertEqual(rec["counts"]["dropped"], 2)
        self.assertIn("s3", rec["notes"])
        self.assertIn("s9", rec["notes"])
        with self.assertRaises(join.Invalid):
            join.join(STATEMENTS, KEYS, "merged")


if __name__ == "__main__":
    unittest.main(verbosity=1)
