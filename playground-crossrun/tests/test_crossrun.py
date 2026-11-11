"""Checks on the cross-run. Stdlib unittest.

    python3 -m unittest discover -s playground-crossrun/tests

Most checks read the pinned out/*.json; the two that need a study-aperture checkout
skip with the reason when STUDY_APERTURE_PATH (default ../study-aperture) is absent.
"""
import ast, json, os, subprocess, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(FOLDER, "adapters"))
import common  # noqa: E402
import compare  # noqa: E402
import concept_map  # noqa: E402

HAVE_SA = os.path.isdir(os.path.join(common.SA_EXP, "playground"))


def rows():
    return {r["case_id"]: r for r in common.load("crossrun.json")["rows"]}


def feed(name):
    return {r["case_id"]: r for r in common.load(name)["rows"]}


class CodeRule(unittest.TestCase):
    def test_precedence(self):
        A, F = {("determination", "failed")}, {("physical", "failed")}
        self.assertEqual(compare.code_of(False, False, True, True, True, A, A, False), "ADAPTER")
        self.assertEqual(compare.code_of(True, True, True, True, True, A, A, False), "ADAPTER")
        self.assertEqual(compare.code_of(True, False, False, True, True, A, A, True), "MISSED")   # crash beats slot
        self.assertEqual(compare.code_of(True, False, False, True, True, A, A, False), "NO_SLOT")
        self.assertEqual(compare.code_of(True, False, True, True, False, A, set(), False), "MISSED")
        self.assertEqual(compare.code_of(True, False, True, True, True, A, F, False), "MISCLASSIFIED")
        self.assertEqual(compare.code_of(True, False, True, True, True, A, A, False), "AGREE")
        self.assertEqual(compare.code_of(True, False, True, False, False, set(), set(), False), "AGREE")

    def test_readings_kept_under_no_slot(self):
        r = rows()
        self.assertEqual((r["P-DEF:model-conservation-violation"]["code"], r["P-DEF:model-conservation-violation"]["readings"]),
                         ("NO_SLOT", "MISCLASSIFIED"))
        self.assertEqual(r["P-DEF:unregistered-control"]["readings"], "MISSED")
        self.assertEqual(r["P-DEF:incomplete-ledger-gap"]["readings"], "AGREE")


class PinnedFindings(unittest.TestCase):
    """Each assert is a result reported in README.md; a change here changes the report."""

    def test_clean_instrument_verdict_moves_with_adapter_start_state(self):
        arms = feed("p_into_257.json")["P-CTRL:clean-instrument-validated"]["r_arms"]
        self.assertEqual(arms["y0=-1"]["harness"], "PASS")
        self.assertEqual(arms["y0=0"]["harness"], "MISSES_PLANTED_DEFECTS")
        self.assertEqual(arms["y0=1"]["harness"], "MISSES_PLANTED_DEFECTS")
        self.assertEqual(rows()["P-CTRL:clean-instrument-validated"]["code"], "ADAPTER")

    def test_wrong_instrument_reads_as_constant_fires(self):
        arms = feed("p_into_257.json")["P-DEF:known-answer-violation"]["r_arms"]
        self.assertEqual({a["harness"] for a in arms.values()}, {"CONSTANT_FIRES"})

    def test_null_only_and_empty_ladder_crash_the_257_tool_gate(self):
        f = feed("p_into_257.json")
        for cid in ("P-DEF:null-false-positive", "P-DEF:sensitivity-ladder-empty", "P-DEF:sensitivity-limit-not-established"):
            self.assertEqual(f[cid]["r"]["form"], "CRASH", cid)
            self.assertEqual(rows()[cid]["code"], "MISSED", cid)

    def test_257_accepts_bounded_null_below_effect_size(self):
        self.assertEqual(feed("p_into_257.json")["P-DEF:non-detection-below-sensitivity"]["r"]["label"], "ABSENT_AT_SENSITIVITY(0.1)")

    def test_trust_transfers_across_systems_in_257(self):
        for cid, r in feed("p_into_257.json").items():
            if cid.startswith("P-XSYS:"):
                self.assertTrue(r["r"]["trust_in_other_system"])

    def test_continuity_cells_agree_on_all_five(self):
        r = rows()
        cells = [c for c in r if c.startswith("P-CTRL:") and r[c]["p"].__class__ is str and "cell" in r[c]["p"]]
        self.assertEqual(len(cells), 5)
        self.assertTrue(all(r[c]["code"] == "AGREE" for c in cells))

    def test_forest_runs_indeterminate_without_a_registry(self):
        f = feed("r257_into_p.json")
        for cid in ("R-F9:replay_base", "R-F9:replay_no_fire", "R-F9:native_seed0"):
            self.assertEqual(f[cid]["p"]["axes"]["determination"], "indeterminate")
            self.assertEqual(f[cid]["p_arms"]["self_registered"]["axes"]["determination"], "ok")

    def test_leak_lands_on_the_axis_the_completeness_flag_picks(self):
        a = feed("r257_into_p.json")["R-F9:replay_planted_leak_0.3"]["p_arms"]
        self.assertEqual((a["as_stated"]["axes"]["determination"], a["as_stated"]["axes"]["physical"]), ("failed", "untested"))
        self.assertEqual((a["self_registered"]["axes"]["determination"], a["self_registered"]["axes"]["physical"]), ("ok", "failed"))

    def test_forest_misclosure_reproduces_bit_identically(self):
        for c in common.load("r257_cases.json")["cases"]:
            if c["case_id"].startswith("R-F9:"):
                for b in c["data"]["budgets"].values():
                    self.assertTrue(b["reproduces"], c["case_id"])

    def test_percolation_fixtures_all_refused_by_bound(self):
        f = feed("r257_into_p.json")
        perc = [r for c, r in f.items() if c.startswith("R-KAG:percolation")]
        self.assertEqual(len(perc), 12)
        self.assertTrue(all(r["p"]["refused"] for r in perc))
        self.assertTrue(all(r["p"]["edges"] > 12 or r["p"]["nodes"] > 32 for r in perc))

    def test_branching_nine_agree_three_refused_two_ways(self):
        f = feed("r257_into_p.json")
        br = {c: r["p"] for c, r in f.items() if c.startswith("R-KAG:branching")}
        agree = [c for c, p in br.items() if p.get("matches_257_closed_form")]
        blocked = {c: p for c, p in br.items() if p.get("run_state", "").startswith("blocked")}
        self.assertEqual((len(agree), len(blocked)), (9, 3))
        dets = sorted(p["axes"]["determination"] for p in blocked.values())
        self.assertEqual(dets, ["failed", "ok", "ok"])   # population bound fails; founder bound reads outside-domain

    def test_unknown_without_exit_is_accepted_by_study_aperture(self):
        self.assertTrue(feed("r257_into_p.json")["R-VAL:unknown_without_expiry"]["p"]["accepted"])
        self.assertEqual(rows()["R-VAL:unknown_without_expiry"]["code"], "MISSED")


class ConceptMap(unittest.TestCase):
    def test_every_location_resolves(self):
        if not HAVE_SA:
            self.skipTest("no study-aperture checkout at %s" % common.SA_ROOT)
        n = 0
        for side, path, tok, concept in concept_map.locations():
            f = os.path.join(concept_map.root(side), path)
            self.assertTrue(os.path.exists(f), "%s: %s" % (concept, f))
            with open(f) as fh:
                self.assertIn(tok, fh.read(), "%s: %s not in %s" % (concept, tok, path))
            n += 1
        self.assertGreaterEqual(n, 60)

    def test_both_sides_named_for_every_concept(self):
        for row in concept_map.ROWS:
            self.assertEqual(len(row), 3)
            self.assertTrue(row[1] and row[2], row[0])


class Hygiene(unittest.TestCase):
    def test_report_regenerates(self):
        with open(os.path.join(FOLDER, "STEP1_REPORT.md")) as f:
            before = f.read()
        subprocess.run([sys.executable, os.path.join(FOLDER, "adapters", "compare.py")], check=True, capture_output=True)
        with open(os.path.join(FOLDER, "STEP1_REPORT.md")) as f:
            self.assertEqual(before, f.read())

    def test_compare_imports_neither_playground(self):
        for name in ("compare.py", "common.py", "concept_map.py"):
            tree = ast.parse(open(os.path.join(FOLDER, "adapters", name)).read())
            mods = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} | \
                   {(n.module or "").split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
            self.assertNotIn("playground", mods, name)

    def test_originals_untouched(self):
        self.assertEqual(common.git_dirty(common.SIM_ROOT, "relational-playground"), [])
        if HAVE_SA:
            self.assertEqual(common.git_dirty(common.SA_ROOT, "experimental/playground"), [])


if __name__ == "__main__":
    unittest.main()
