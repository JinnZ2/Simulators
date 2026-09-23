#!/usr/bin/env python3
# test_audit.py -- checks on the audit, not on the drop.
# stdlib unittest, no network. Run: python3 test_audit.py
#
# Every guard is planted against: a constructed violation must fire it.

import ast
import inspect
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import audit                                                    # noqa: E402

# Figures the delivered documents carry. None may appear as a numeric literal
# in audit.py: the audit PARSES the documents, it does not restate them.
DOC_FIGURES = {16, 6552, 7323, 9000, 1800, 1.37, 0.26, 81, 40, 0.71, 0.87,
               0.94, 1.05, 11.5, 76.1, 580000, 326000, 12}


def literals(path):
    out = set()
    for n in ast.walk(ast.parse(open(path, encoding="utf-8").read())):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            out.add(n.value)
    return out


class ParseNotRetype(unittest.TestCase):

    def test_no_document_figure_is_a_literal(self):
        hit = literals(os.path.join(HERE, "audit.py")) & DOC_FIGURES
        self.assertEqual(hit, set(), "document figure retyped in audit.py: %s" % hit)

    def test_guard_fires_on_a_plant(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "planted.py")
        open(p, "w").write("N_RECORDS = 16\n")
        self.assertIn(16, literals(p) & DOC_FIGURES)

    def test_halfwidth_is_imported_not_redefined(self):
        tree = ast.parse(open(os.path.join(HERE, "audit.py")).read())
        defs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        self.assertNotIn("halfwidth", defs)
        self.assertNotIn("_halfwidth", defs)
        self.assertTrue(callable(audit.halfwidth))

    def test_parser_is_load_bearing(self):
        """An emptied document must break the checks, not silently pass them.
        A checker that returns clean over nothing is the failure this
        repository has recorded more than once."""
        d = tempfile.mkdtemp()
        for f in audit.DOC.values():
            shutil.copy(os.path.join(HERE, f), os.path.join(d, f))
        open(os.path.join(d, audit.DOC["corpus"]), "w").write("# emptied\n")
        real = audit.HERE
        try:
            audit.HERE = d
            self.assertEqual(audit.matrix(), [])
            self.assertEqual(audit.perfect_records(), [])
            self.assertEqual(audit.distribution_agrees()["n_records"], 0)
        finally:
            audit.HERE = real


class Corpus(unittest.TestCase):

    def test_matrix_parses_every_row(self):
        m = audit.matrix()
        self.assertGreater(len(m), 0)
        for name, cells in m:
            self.assertEqual(len(cells), len(audit.CHECK_ORDER), name)
            for v in cells:
                self.assertIn(v, ("PASS", "PARTIAL", "FAIL", "ABSENT"), name)

    def test_every_column_totals_the_record_count(self):
        d = audit.distribution_agrees()
        for r in d["rows"]:
            self.assertEqual(r["row_total"], d["n_records"], r["column"])

    def test_distribution_agrees_with_the_matrix(self):
        self.assertTrue(audit.distribution_agrees()["all_agree"])

    def test_f1_counterexamples_are_real_rows(self):
        m = dict(audit.matrix())
        t = audit.f1_at_least_three()
        for c in t["counterexamples"]:
            self.assertIn(c["record"], m)
            self.assertEqual(
                c["non_pass"], len([v for v in m[c["record"]] if v != "PASS"]))

    def test_f1_check_can_hold(self):
        """Not CONSTANT_SILENT: a corpus where every humanoid row fails three
        must return holds=True."""
        real = audit.matrix
        try:
            audit.matrix = lambda: [("Optimus X", ["PASS", "ABSENT", "ABSENT",
                                                   "ABSENT", "PASS", "PASS"])]
            self.assertTrue(audit.f1_at_least_three()["holds"])
        finally:
            audit.matrix = real


class Komatsu(unittest.TestCase):

    def test_derived_cells_agree_at_shipped_precision(self):
        k = audit.komatsu_arithmetic()
        bad = [r for r in k["rows"] if not r["agrees"]]
        self.assertEqual(bad, [], "ledger cell disagrees: %s" % bad)

    def test_every_row_carries_its_precision(self):
        for r in audit.komatsu_arithmetic()["rows"]:
            self.assertIsNotNone(r["as_written"], r["quantity"])
            self.assertIsNotNone(r["halfwidth"], r["quantity"])

    def test_tolerance_is_the_documents_not_mine(self):
        """The 12% row recomputes to 11.77. It agrees because the document
        printed a whole percent, not because a tolerance was chosen to make
        it agree. Stating the figure to two places must refuse it."""
        r = [x for x in audit.komatsu_arithmetic()["rows"]
             if x["quantity"] == "hours gain %"][0]
        self.assertEqual(float(audit.halfwidth(r["as_written"])), 0.5)
        self.assertGreater(abs(r["stated"] - r["recomputed"]),
                           float(audit.halfwidth("12.00")))

    def test_tire_range_parses_both_bounds(self):
        """Regression: the separator quantifier was greedy and ate a digit
        group out of '6,000-7,000', parsing the upper bound as 0 and
        returning a range of [20.0, -100.0]."""
        t = audit.tire_range()
        lo, hi = t["range_from_hours_pct"]
        self.assertLess(lo, hi)
        self.assertGreater(lo, 0)
        self.assertAlmostEqual(t["midpoint_pct"], (lo + hi) / 2, places=1)

    def test_tire_known_answer(self):
        """Hand-computed from the hours the document cites."""
        g = audit.komatsu_numbers()
        self.assertAlmostEqual(g["tire_lo"] / g["tire_base"], 1.2, places=6)
        self.assertAlmostEqual(g["tire_hi"] / g["tire_base"], 1.4, places=6)
        t = audit.tire_range()
        self.assertEqual(t["range_from_hours_pct"], [20.0, 40.0])
        self.assertEqual(t["midpoint_pct"], 30.0)
        self.assertTrue(t["stated_is_top_of_range"])


class Scope(unittest.TestCase):

    def test_no_claim_about_the_world(self):
        """The audit reports agreement between documents. No function name
        asserts a fact about haulage, robots or any vendor."""
        tree = ast.parse(open(os.path.join(HERE, "audit.py")).read())
        names = {n.name for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        forbidden = {"is_true", "verify_claim", "confirms", "proves",
                     "validate_finding", "rate", "prevalence"}
        self.assertEqual(names & forbidden, set())

    def test_absent_is_not_counted_as_a_negative(self):
        """AGA_004 reports PASS-counts. ABSENT must not be folded into FAIL
        anywhere in the distribution."""
        d = audit.recomputed_distribution()
        for col, v in d.items():
            self.assertIn("ABSENT", v)
            self.assertIn("FAIL", v)

    def test_ledger_denominator_is_recomputed(self):
        s = audit.parked_strike_share()
        self.assertTrue(s["denominator_agrees"])
        self.assertEqual(s["stated"][1], s["headed_entry_records"])


class SeedRoads(unittest.TestCase):
    """FIELD_LAYER_SEED_ROADS -- the sixth document, and WP1/WP2."""

    def test_tire_ratio_recomputes_at_shipped_precision(self):
        t = audit.seed_tire_ratio()
        self.assertTrue(t["parsed"])
        self.assertTrue(t["lo_agrees"] and t["hi_agrees"])
        # the tolerance is the document's own, not a constant here
        self.assertEqual(t["halfwidth"], [0.05, 0.05])

    def test_tire_ratio_would_refuse_a_wrong_pairing(self):
        """gravel/gravel is 1.0 and must not agree with either bound."""
        t = audit.seed_tire_ratio()
        g = t["cents"]["gravel"]
        self.assertFalse(abs(g / g - t["stated"][0]) <= t["halfwidth"][0])

    def test_cost_and_frequency_are_reported_apart(self):
        c = audit.seed_cost_vs_frequency()
        self.assertTrue(c["parsed"])
        self.assertFalse(c["same_quantity"])
        self.assertGreater(c["factor_between_them"], 10)

    def test_no_verdict_is_issued_on_the_two_rows(self):
        """AGA_014 reports a tension and rules on neither figure."""
        src = inspect.getsource(audit.seed_cost_vs_frequency)
        for word in ("wrong", "error", "should be", "correct value"):
            self.assertNotIn(word, src.split('"""')[2])

    def test_undeclared_provenance_label_is_found(self):
        v = audit.seed_provenance_vocabulary()
        self.assertIn("INDUSTRY-STATED", v["undeclared"])
        self.assertEqual(v["undeclared"], ["INDUSTRY-STATED"])
        self.assertGreater(v["undeclared_rows"], 0)

    def test_declared_labels_are_read_from_the_document(self):
        v = audit.seed_provenance_vocabulary()
        head = audit.text("seed").splitlines()[2]
        for lab in v["declared"]:
            self.assertIn(lab, head)

    def test_provenance_check_is_not_constant(self):
        """A label the header does declare must not be reported undeclared."""
        v = audit.seed_provenance_vocabulary()
        self.assertIn("MEASURED", v["used"])
        self.assertNotIn("MEASURED", v["undeclared"])

    def test_one_crosscite_resolves_and_one_does_not(self):
        c = audit.seed_crosscites()
        by = {x["cite"].split(",")[0]: x for x in c["cites"]}
        self.assertTrue(by["Komatsu scaffold"]["resolves"])
        aur = [x for x in c["cites"] if "demo-corpus" in x["cite"]][0]
        self.assertFalse(aur["resolves"])
        self.assertEqual(aur["supporting_document"], "gap")

    def test_collision_restates_three_figures_and_all_are_contained(self):
        r = audit.seed_rainfall_and_restatement()
        self.assertEqual(len(r["checks"]), 3)
        self.assertTrue(r["all_contained"])

    def test_survey_denominator_has_one_integral_reading(self):
        s = audit.seed_survey_denominator()
        self.assertTrue(s["parsed"])
        self.assertFalse(s["surveyed_reading_is_integral"])
        self.assertTrue(s["responded_reading_is_integral"])

    def test_seed_falsifier_prefix_does_not_collide(self):
        f = audit.falsifier_ids()
        self.assertEqual(f["collisions"], [])
        self.assertTrue(f["seed_prefix_is_new"])
        self.assertEqual(sorted(f["prefixes"]), ["AUT", "RD"])


class NamedAndAbsent(unittest.TestCase):
    """AGA_009 half-closes: WP1 and WP2 arrive, two ledgers do not."""

    def test_wp1_and_wp2_are_filed(self):
        n = audit.named_and_absent()
        self.assertEqual(n["delivered"], ["WP1", "WP2"])
        for k in ("WP1", "WP2"):
            self.assertEqual(n["objects"][k]["filed_in"], ["seed"])

    def test_both_ledgers_are_still_absent_and_still_cited(self):
        n = audit.named_and_absent()
        self.assertEqual(n["still_absent"],
                         ["claim ledger", "trades-shortage ledger"])
        for k in n["still_absent"]:
            self.assertEqual(n["objects"][k]["filed_in"], [])
            self.assertTrue(n["objects"][k]["cited_in"])


class DefectsFoundByRunning(unittest.TestCase):
    """Three defects in the checks above, each pinned by the case that
    exposed it. All three ran toward the reassuring answer."""

    def test_d1_a_wrapped_figure_is_still_found(self):
        """'4x maintenance\n   frequency' wraps in the delivered text; a
        single-space pattern matched nothing and the containment check
        reported two figures where the document restates three."""
        t = audit.text("seed")
        self.assertRegex(t, r"4\u00d7 maintenance\n\s+frequency")
        self.assertEqual(len(audit.seed_rainfall_and_restatement()["checks"]), 3)

    def test_d2_a_citation_is_not_a_second_definition(self):
        """AUT-F1 is defined in the gap audit and cited in the corpus
        audit's cross-links. Counting both reported a collision."""
        f = audit.falsifier_ids()
        self.assertEqual(f["definitions"]["AUT-F1"], ["gap"])
        self.assertIn("corpus", f["citations"]["AUT-F1"])
        self.assertEqual(f["collisions"], [])

    def test_d3_a_mention_is_not_a_delivery(self):
        """Searching for the name reported both ledgers delivered, on the
        strength of the sentences that cite them."""
        n = audit.named_and_absent()
        self.assertIn("komatsu",
                      n["objects"]["trades-shortage ledger"]["cited_in"])
        self.assertFalse(n["objects"]["trades-shortage ledger"]["delivered"])


class Screen(unittest.TestCase):

    def test_render_screens_clean_with_no_exemption(self):
        """The repo's severity screen, imported not copied. The render quotes
        no delivered prose, so any hit would be a word this audit authored."""
        import contextlib
        import importlib.util
        import io
        sp = importlib.util.spec_from_file_location(
            "ns", os.path.join(HERE, os.pardir, "sheet-structure-scan",
                               "no_severity.py"))
        ns = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(ns)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            audit.render(audit.findings())
        self.assertEqual(ns.hits(buf.getvalue()), [])
        self.assertTrue(ns.hits("this value is wrong"), "screen is silent")


def main():
    r = unittest.TextTestRunner(verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    print("checks: %d   failures: %d   errors: %d"
          % (r.testsRun, len(r.failures), len(r.errors)))
    return 0 if r.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
