"""B1.6 tests. stdlib unittest, synthetic fixtures in-file. Run: python3 test_b1.py"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import nulls, permute, report, schema, score, summarise  # noqa: E402
from ficommon import read_jsonl, write_jsonl  # noqa: E402
from runrecord import read_records  # noqa: E402

DS, LS = [8, 16, 32, 64, 128], [2, 4, 8]
BASE_CONT = ["b%d" % k for k in range(128)]


def base_row(case="c1", i=5):
    return {"case_id": case, "model_id": "m", "i": i, "token_taken": "the", "logprob_taken": -0.5,
            "topk": [["the", -0.5], ["a", -1.5]], "entropy_i": 0.7, "entropy_basis": "topk"}


def trace(cont, case="c1", i=5, rank=2):
    return {"case_id": case, "model_id": "m", "i": i, "branch_rank": rank, "forced_token": "a",
            "continuation": cont, "base_continuation": list(BASE_CONT)}


def rejoin_immediately():
    return list(BASE_CONT)


def never_rejoins():
    # positions 0-7: match at even, differ at odd; 8+: all differ. No two
    # consecutive aligned matches anywhere, and mismatch density rises with D.
    return [BASE_CONT[k] if (k < 8 and k % 2 == 0) else "x%d" % k for k in range(128)]


def rejoin_at_20():
    return ["x%d" % k for k in range(20)] + BASE_CONT[20:]


def three_token_run():
    return [BASE_CONT[k] if k in (3, 4, 5) else "x%d" % k for k in range(128)]


def by_dl(rows):
    return {(r["D"], r["L"]): r for r in rows}


class B1Tests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="b1test_")
        self.runs = os.path.join(self.d, "runs")

    def tearDown(self):
        shutil.rmtree(self.d)

    def p(self, name):
        return os.path.join(self.d, name)

    def sweep_one(self, cont):
        return by_dl(score.sweep([base_row()], [trace(cont)], DS, LS))

    def test_rejoins_immediately(self):
        s = self.sweep_one(rejoin_immediately())
        for D in DS:
            for L in LS:
                self.assertEqual(s[(D, L)]["resync_D"], 1)
                self.assertEqual(s[(D, L)]["div_D"], 0.0)
                self.assertEqual(s[(D, L)]["gap_i"], 1.0)

    def test_never_rejoins_div_rises(self):
        s = self.sweep_one(never_rejoins())
        for L in LS:
            divs = [s[(D, L)]["div_D"] for D in DS]
            self.assertTrue(all(s[(D, L)]["resync_D"] == 0 for D in DS))
            self.assertTrue(all(a < b for a, b in zip(divs, divs[1:])), divs)

    def test_rejoin_at_20_is_the_sweep(self):
        s = self.sweep_one(rejoin_at_20())
        for L in LS:
            self.assertEqual([s[(D, L)]["resync_D"] for D in DS], [0, 0, 1, 1, 1])

    def test_L_sensitivity(self):
        s = self.sweep_one(three_token_run())
        for D in DS:
            self.assertEqual((s[(D, 2)]["resync_D"], s[(D, 4)]["resync_D"], s[(D, 8)]["resync_D"]), (1, 0, 0))

    def test_levenshtein_known_answers(self):
        self.assertEqual(score.levenshtein([], ["a"]), 1)
        self.assertEqual(score.levenshtein(["a", "b", "c"], ["a", "x", "c"]), 1)
        self.assertEqual(score.levenshtein(["a", "b", "c"], ["b", "c"]), 1)
        self.assertEqual(score.levenshtein(["a", "b"], ["c", "d"]), 2)

    def test_permutation_preserves_count_and_multiset(self):
        rows = score.sweep([base_row(i=5), base_row(i=6)],
                           [trace(never_rejoins(), i=5), trace(rejoin_at_20(), i=6), trace(three_token_run(), i=5, rank=3)], DS, LS)
        out = permute.permute(rows, 11)
        self.assertEqual(len(out), len(rows))
        tup = lambda r: (r["ent_i"], r["gap_i"], r["resync_D"], r["div_D"])
        self.assertEqual(sorted(map(tup, out)), sorted(map(tup, rows)))
        for r in out:
            self.assertEqual(r["permute_seed"], 11)
        self.assertEqual(sorted((r["case_id"], r["i"], r["branch_rank"], r["D"], r["L"]) for r in out),
                         sorted((r["case_id"], r["i"], r["branch_rank"], r["D"], r["L"]) for r in rows))
        self.assertEqual(out, permute.permute(rows, 11))

    def test_malformed_row_rejected_with_record(self):
        bad = base_row()
        bad["entropy_basis"] = "guessed"
        write_jsonl(self.p("base.jsonl"), [bad])
        write_jsonl(self.p("traces.jsonl"), [trace(rejoin_at_20())])
        rc = schema.main([self.p("base.jsonl"), self.p("traces.jsonl"), "--out", self.p("c.jsonl"), "--runs", self.runs])
        self.assertEqual(rc, 1)
        rec = read_records(self.runs)[-1]
        self.assertEqual(rec["status"], "error")
        self.assertIn("base.jsonl:1", rec["notes"])
        self.assertIn("entropy_basis", rec["notes"])

    def test_full_pipeline_and_void_without_permuted(self):
        write_jsonl(self.p("base.jsonl"), [base_row(i=5), base_row(i=6)])
        write_jsonl(self.p("traces.jsonl"), [trace(never_rejoins(), i=5), trace(rejoin_at_20(), i=6),
                                              trace(three_token_run(), i=5, rank=3)])
        self.assertEqual(score.main([self.p("base.jsonl"), self.p("traces.jsonl"), "--out", self.p("s.jsonl"), "--runs", self.runs]), 0)
        self.assertEqual(permute.main([self.p("s.jsonl"), "--seed", "4", "--out", self.p("sp.jsonl"), "--runs", self.runs]), 0)
        self.assertEqual(summarise.main([self.p("s.jsonl"), "--out", self.p("sum.jsonl"), "--runs", self.runs]), 0)
        self.assertEqual(summarise.main([self.p("sp.jsonl"), "--out", self.p("sump.jsonl"), "--runs", self.runs]), 0)
        args = ["--separations", self.p("s.jsonl"), "--summary", self.p("sum.jsonl"), "--out", self.p("r.md"), "--runs", self.runs]
        self.assertEqual(report.main(args + ["--summary-permuted", self.p("missing.jsonl")]), 2)
        self.assertFalse(os.path.exists(self.p("r.md")))
        self.assertEqual(report.main(args + ["--summary-permuted", self.p("sump.jsonl")]), 0)
        with open(self.p("r.md")) as fh:
            text = fh.read()
        self.assertEqual(text.count("\n## "), 6)
        self.assertIn("PERMUTED", text)
        for n in ("N1", "N2", "N3", "N4", "N5"):
            self.assertIn("### %s -- " % n, text)
        self.assertIn("N5 -- NOT EVALUABLE", text)
        cells = [s for s in read_jsonl(self.p("sum.jsonl")) if "n_rows" in s]
        self.assertEqual(len(cells), len(DS) * len(LS))

    def test_nulls_each_direction(self):
        # N1 fires on a corpus that rejoins everywhere; N2 fires on one that separates everywhere.
        rj = score.sweep([base_row(i=5), base_row(i=6)], [trace(rejoin_immediately(), i=5), trace(rejoin_immediately(), i=6)], DS, LS)
        sp = score.sweep([base_row(i=5), base_row(i=6)], [trace(never_rejoins(), i=5), trace(never_rejoins(), i=6)], DS, LS)
        thr = dict(nulls.DEFAULTS)
        s_rj, s_sp = summarise.summarise(rj), summarise.summarise(sp)
        self.assertTrue(nulls.n1(s_rj, thr["n1_resync"])["triggered"])
        self.assertFalse(nulls.n1(s_sp, thr["n1_resync"])["triggered"])
        self.assertTrue(nulls.n2(sp, thr["n2_separate"], 64)["triggered"])
        self.assertFalse(nulls.n2(rj, thr["n2_separate"], 64)["triggered"])
        self.assertIsNone(nulls.n5(None, 0.1)["triggered"])
        self.assertIsNone(nulls.n5([base_row(i=5)], 0.1)["triggered"])
        both = [dict(base_row(i=k), entropy_i=float(k), entropy_basis="full") for k in range(4)] + \
               [dict(base_row(i=k), entropy_i=float(3 - k), entropy_basis="topk") for k in range(4)]
        r = nulls.n5(both, 0.1)
        self.assertEqual(r["number"]["discordant_pair_fraction"], 1.0)
        self.assertTrue(r["triggered"])
        n4 = nulls.n4(s_sp, s_sp)
        self.assertTrue(n4["triggered"])  # identical stability on both arms reads as method artifact
        self.assertIsNone(nulls.n3([], 0.5)["triggered"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
