"""Known-answer tests for derive.py: constructed walks with stipulated counts; neutral case names."""
import os, sys, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derive as D  # noqa: E402

P = {"PA": {"path_id": "PA", "gap_id": "GX", "rule": "a"}, "PB": {"path_id": "PB", "gap_id": "GX", "rule": "b"}}
def w(wid, path, fam, L, exp, case, outcome, repair=None):
    return {"path_id": path, "walk_id": wid, "reader_family": fam, "L": L, "exposure_prior_walks": exp, "case": case,
            "outcome": outcome, "repair_needed": repair, "provenance": "fixture", "date": "2026-11-19"}
WALKS = [w("w1", "PA", "fam1", 2, "no", "c1", "holds"), w("w2", "PA", "fam2", 3, "no", "c2", "holds"),
         w("w3", "PA", "fam3", 2, "yes", "c1", "holds"), w("w4", "PA", "fam4", None, "unknown", "c3", "breaks"),
         w("w5", "PA", "fam1", 1, "no", "c1", "needs_exception", "add a clause"),
         w("w6", "PB", "fam1", 2, "no", "c1", "breaks", "rule cannot place the wrapper")]

class Derive(unittest.TestCase):
    def test_columns_are_kept_apart(self):
        d = D.derive(P, WALKS)["PA"]
        self.assertEqual(d["by_column"], {"independent": 2, "traffic": 1, "exposure_unknown": 1, "dependent": 1})
        self.assertEqual(d["outcomes"]["independent"]["holds"], 2)
        self.assertEqual(d["outcomes"]["traffic"]["holds"], 1)          # traffic holds are not added to independent
        self.assertEqual((d["independent_cases"], d["independent_families"]), (2, 2))
        self.assertEqual(d["repairs"], ["add a clause"])
    def test_traffic_never_becomes_independent(self):
        many = [w("t%d" % i, "PB", "f%d" % i, 4, "yes", "c%d" % i, "holds") for i in range(10)]
        d = D.derive(P, WALKS + many)["PB"]
        self.assertEqual(d["by_column"]["independent"], 1)
        self.assertEqual(d["by_column"]["traffic"], 10)
    def test_no_score_field(self):
        d = D.derive(P, WALKS)
        for r in d.values():
            self.assertFalse({"score", "rank", "winner", "stability"} & set(r))
    def test_errors_caught(self):
        bad = [dict(WALKS[0], outcome="pass"), dict(WALKS[1], exposure_prior_walks="no idea"), dict(WALKS[2], path_id="PZ"),
               WALKS[0]]
        self.assertGreaterEqual(len(D.errors(P, bad)), 4)
    def test_shipped_files_load_and_are_empty(self):
        paths, walks = D.load(os.path.join(HERE, "walks.jsonl"), os.path.join(HERE, "paths.json"))
        self.assertEqual(walks, [])
        self.assertEqual(D.errors(paths, walks), [])
        self.assertEqual(len(paths), 14)

if __name__ == "__main__":
    unittest.main()
