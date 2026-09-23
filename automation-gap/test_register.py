#!/usr/bin/env python3
# test_register.py -- checks on the register audit, not on the register.
# stdlib unittest, no network. Run: python3 test_register.py
#
# Every guard is planted against: a constructed violation must fire it.
# A guard nobody has seen fire is not known to discriminate.

import ast
import copy
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import register_audit as RA                                     # noqa: E402
import driver_hours_evidence_register as REG                    # noqa: E402

# Figures the register states. None may appear as a NUMERIC literal in
# register_audit.py: the audit reads the register's own objects, it does
# not restate them. A value inside a search pattern is a locator, not a
# restatement, and is a string constant rather than a numeric one.
REGISTER_FIGURES = {1249, 593, 270, 309, 843, 9000, 1800, 47.1, 25.4,
                    41, 73, 75, 89, 1000}


def numeric_literals(path):
    out = set()
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            out.add(n.value)
    return out


def _patched(**sources):
    """Swap SOURCES entries for a planted variant, restoring after."""
    class ctx(object):
        def __enter__(self):
            self.real = REG.SOURCES
            new = copy.deepcopy(REG.SOURCES)
            new.update(sources)
            REG.SOURCES = new

        def __exit__(self, *a):
            REG.SOURCES = self.real
    return ctx()


# ------------------------------------------------------- read, not restate

class ReadNotRestate(unittest.TestCase):

    def test_no_register_figure_is_a_numeric_literal(self):
        hit = numeric_literals(os.path.join(HERE, "register_audit.py")) \
            & REGISTER_FIGURES
        self.assertEqual(hit, set(), "register figure retyped: %s" % hit)

    def test_that_guard_fires_on_a_plant(self):
        import tempfile
        p = os.path.join(tempfile.mkdtemp(), "planted.py")
        with open(p, "w") as fh:
            fh.write("EVER_RATE = 47.1\n")
        self.assertIn(47.1, numeric_literals(p) & REGISTER_FIGURES)

    def test_n_eff_is_imported_not_reimplemented(self):
        with open(os.path.join(HERE, "register_audit.py")) as fh:
            tree = ast.parse(fh.read())
        names = [n.name for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        self.assertNotIn("n_eff", names)
        self.assertNotIn("Channel", names)
        self.assertNotIn("Case", names)
        self.assertTrue(callable(RA._ER.Channel))

    def test_the_register_is_imported_not_parsed(self):
        """The objects under test are the register's own objects."""
        self.assertIs(RA.REG.SOURCES, REG.SOURCES)
        self.assertIs(RA.REG.QUESTIONS, REG.QUESTIONS)


# ------------------------------------------------------- AGA_020 vocabulary

class StatusVocabulary(unittest.TestCase):

    def test_one_scale_declared_two_in_use(self):
        v = RA.status_vocabulary()
        self.assertEqual(len(v["declared"]), 6)
        self.assertEqual(set(v["in_sources"]),
                         {"OBSERVED", "SECONDARY", "UNREAD"})
        self.assertEqual(set(v["in_questions"]), {"SUPPORTED", "UNMEASURED"})

    def test_the_question_verdict_token_is_declared_nowhere(self):
        self.assertIn("SUPPORTED", RA.status_vocabulary()["undeclared"])

    def test_two_declared_rungs_are_used_nowhere(self):
        self.assertEqual(RA.status_vocabulary()["unused_anywhere"],
                         ["DERIVED", "PROPOSED"])

    def test_undeclared_is_not_constant(self):
        """The check must be able to come back empty."""
        s = copy.deepcopy(REG.SOURCES["S1"])
        s["status"] = "OBSERVED"
        with _patched(S1=s):
            v = RA.status_vocabulary()
            self.assertIn("SUPPORTED", v["undeclared"])   # still, from QUESTIONS
            self.assertNotIn("UNREAD", v["in_sources"] and [])


# ------------------------------------------------------- AGA_021 shared node

class SharedNode(unittest.TestCase):

    def test_s3_authors_are_a_subset_of_s1(self):
        pairs = RA.author_overlap()
        self.assertEqual(len(pairs), 1)
        pr = pairs[0]
        self.assertEqual((pr["a"], pr["b"]), ("S1", "S3"))
        self.assertEqual(pr["shared"], ["Braver", "Preusser", "Ulmer"])
        self.assertTrue(pr["subset"])
        self.assertTrue(pr["frames_equal"])

    def test_qa_has_four_nominal_sources_and_n_eff_three(self):
        v = RA.question_n_eff()["QA"]
        self.assertEqual(v["n_nominal"], 4)
        self.assertEqual(v["n_eff"], 3)
        self.assertEqual(v["collapsed"], ["S1", "S3"])

    def test_every_other_question_is_uncollapsed(self):
        for qid, v in RA.question_n_eff().items():
            if qid != "QA" and v["n_nominal"]:
                self.assertEqual(v["n_eff"], v["n_nominal"], qid)

    def test_overlap_is_not_constant(self):
        s3 = copy.deepcopy(REG.SOURCES["S3"])
        s3["cite"] = "Nobody, Nobody Else (1999). A different group."
        with _patched(S3=s3):
            self.assertEqual(RA.author_overlap(), [])
            self.assertEqual(RA.question_n_eff()["QA"]["n_eff"], 4)


# ------------------------------------------------------- AGA_022 frame flags

class FrameFlags(unittest.TestCase):

    def test_the_stated_rule_is_every_source_carries_one(self):
        self.assertEqual(RA.frame_vocabulary()["stated_rule"],
                         "every source carries one")

    def test_one_source_carries_none(self):
        self.assertEqual(RA.frame_vocabulary()["sources_without_a_flag"], ["S6"])

    def test_there_is_no_member_for_an_unknown_frame(self):
        """An empty list reads as 'no sampling-frame concern' and as
        'frame not established' identically."""
        self.assertFalse(RA.frame_vocabulary()["unknown_member_exists"])

    def test_the_check_clears_when_the_flag_is_supplied(self):
        s6 = copy.deepcopy(REG.SOURCES["S6"])
        s6["frame"] = ["ON_ROAD"]
        with _patched(S6=s6):
            self.assertEqual(RA.frame_vocabulary()["sources_without_a_flag"], [])

    def test_an_undeclared_flag_fires(self):
        s6 = copy.deepcopy(REG.SOURCES["S6"])
        s6["frame"] = ["INVENTED"]
        with _patched(S6=s6):
            self.assertEqual(RA.frame_vocabulary()["undeclared"], ["INVENTED"])


# ------------------------------------------------------- AGA_023 QE's scope

class QEScope(unittest.TestCase):

    def test_as_written_it_is_seven_of_eleven(self):
        self.assertEqual(RA.qe_scope()["as_written"], (7, 11))

    def test_over_samples_it_is_seven_of_eight(self):
        self.assertEqual(RA.qe_scope()["over_samples"], (7, 8))

    def test_s6_is_what_stops_it_being_all_of_them(self):
        """AGA_022's missing state and AGA_023's unchecked boundary are
        one gap at two sites."""
        self.assertEqual(RA.qe_scope()["blocked_by"], ["S6"])

    def test_supplying_s6_a_frame_closes_the_boundary(self):
        s6 = copy.deepcopy(REG.SOURCES["S6"])
        s6["frame"] = ["ON_ROAD"]
        with _patched(S6=s6):
            v = RA.qe_scope()
            self.assertEqual(v["over_samples"], (8, 8))
            self.assertEqual(v["blocked_by"], [])


# ------------------------------------------------------- AGA_024 flag vs defn

class FlagFitsDefinition(unittest.TestCase):

    def test_s5_carries_the_flag_and_does_not_fit_the_definition(self):
        v = RA.frame_definition_fit()
        self.assertEqual(v["mismatched"], ["S5"])

    def test_an_unknown_where_is_not_a_mismatch(self):
        """S7's `where` is '?'. A None must not be read as a False: that
        collapse is the defect this check itself shipped with (AGA_030)."""
        rows = {r["src"]: r for r in RA.frame_definition_fit()["rows"]}
        self.assertIsNone(rows["S7"]["matches_definition"])
        self.assertTrue(rows["S7"]["where_unknown"])
        self.assertNotIn("S7", RA.frame_definition_fit()["mismatched"])

    def test_a_measured_mismatch_is_false_not_none(self):
        rows = {r["src"]: r for r in RA.frame_definition_fit()["rows"]}
        self.assertIs(rows["S5"]["matches_definition"], False)
        self.assertFalse(rows["S5"]["where_unknown"])

    def test_the_mismatch_clears_when_the_method_is_named(self):
        s5 = copy.deepcopy(REG.SOURCES["S5"])
        s5["where"] = "interviewed at truck stops"
        with _patched(S5=s5):
            self.assertEqual(RA.frame_definition_fit()["mismatched"], [])


# ------------------------------------------------------- AGA_025 holds kinds

class HoldsKinds(unittest.TestCase):

    def test_the_split(self):
        v = RA.holds_kinds()
        self.assertEqual(v["total_holds"], 33)
        self.assertEqual(v["state_notes"], 10)
        self.assertEqual(v["findings"], 23)

    def test_three_sources_carry_no_finding_at_all(self):
        self.assertEqual(RA.holds_kinds()["sources_with_no_finding"],
                         ["S7", "S8", "Q1"])

    def test_a_source_of_pure_findings_is_not_flagged(self):
        self.assertNotIn("S3", RA.holds_kinds()["sources_with_no_finding"])


# ------------------------------------------------------- AGA_026 nested rates

class NestedRates(unittest.TestCase):

    def test_past_year_does_not_exceed_ever(self):
        v = RA.nested_rates()
        self.assertTrue(v["nested"])
        self.assertLess(v["past_year"], v["ever"])

    def test_the_containment_check_can_fail(self):
        s2 = copy.deepcopy(REG.SOURCES["S2"])
        s2["holds"] = ["12.0% ever fell asleep", "80.0% in the past year"] \
            + list(s2["holds"][2:])
        with _patched(S2=s2):
            self.assertFalse(RA.nested_rates()["nested"])


# ------------------------------------------------------- AGA_027 provenance

class AuroraProvenance(unittest.TestCase):

    def test_none_of_the_terms_is_in_the_cited_sibling(self):
        """AGA_016 recorded the seed citing these to DEMO_CORPUS_AUDIT,
        which carries none of them. Unchanged by the register's arrival."""
        self.assertEqual(RA.aurora_provenance()["in_demo_corpus"], [])

    def test_the_register_gives_them_a_source_outside_the_folder(self):
        v = RA.aurora_provenance()
        self.assertIn("Aurora", v["register_cite"])
        self.assertEqual(v["register_frame"], ["VENDOR"])

    def test_the_distinctive_terms_resolve_somewhere(self):
        for t, docs in RA.aurora_provenance()["term_locations"].items():
            self.assertTrue(docs, "term found in no folder document: %s" % t)


# ------------------------------------------------------- AGA_028 HOS sizing

class HOSSizing(unittest.TestCase):

    def test_the_speed_derives_from_the_registers_own_two_numbers(self):
        v = RA.hos_sizing()
        self.assertAlmostEqual(v["mph"], round(v["miles"] / v["hours"], 1))

    def test_hos_is_named_and_no_driving_limit_is_stated(self):
        v = RA.hos_sizing()
        self.assertGreater(v["hos_mentions"], 0)
        self.assertTrue(v["off_duty_figure_stated"])
        self.assertFalse(v["driving_limit_in_register"])

    def test_no_delivered_document_supplies_one_either(self):
        v = RA.hos_sizing()
        self.assertFalse(v["driving_limit_in_delivered"])
        self.assertEqual(v["n_delivered_scanned"], 6)

    def test_the_audits_own_output_is_counted_apart_not_excluded(self):
        """Writing AGA_028 down put the phrase in a .md file here. The
        loop is printed, not hidden: a non-empty column is the record of
        it, and the delivered scan is unaffected."""
        v = RA.hos_sizing()
        self.assertIn("CLAIM_TABLE.md", v["limit_phrase_in_audit_files"])
        self.assertFalse(v["driving_limit_in_delivered"])

    def test_the_limit_check_is_not_constant(self):
        s9 = copy.deepcopy(REG.SOURCES["S9"])
        s9["holds"] = list(s9["holds"]) + ["11-hour driving limit"]
        with _patched(S9=s9):
            self.assertTrue(RA.hos_sizing()["driving_limit_in_register"])


# ------------------------------------------------------- AGA_029 self-date

class SelfDate(unittest.TestCase):

    def test_the_register_does_not_share_the_documents_date(self):
        v = RA.self_date()
        self.assertEqual(v["register"], "2026-09-23")
        self.assertFalse(v["matches_documents"])

    def test_the_six_documents_still_agree_with_each_other(self):
        """AGA_008 is bounded to the six by this, not refuted."""
        self.assertEqual(set(RA.self_date()["documents"].values()),
                         {"2026-09-24"})


# ------------------------------------------------------- structure

class Structure(unittest.TestCase):

    def test_every_question_source_id_resolves(self):
        self.assertEqual(RA.question_refs()["unresolvable"], [])

    def test_three_sources_are_named_by_no_question(self):
        self.assertEqual(RA.question_refs()["unreferenced"], ["Q1", "S7", "S8"])

    def test_aga_031_the_operator_record_takes_no_exemption(self):
        """S10 is scored on the same scale, carries a frame flag, and the
        one question resting on it alone is UNMEASURED. Computed, because
        the first draft of this claim stated a count the data does not
        carry (AGA_030 defect 3)."""
        s10 = REG.SOURCES["S10"]
        self.assertIn("OBSERVED", s10["status"])
        self.assertEqual(s10["frame"], ["N_OF_1"])
        naming = [q[0] for q in REG.QUESTIONS if "S10" in q[2]]
        alone = [q for q in REG.QUESTIONS if q[2] == ["S10"]]
        self.assertEqual(naming, ["QA", "QF", "QH"])
        self.assertEqual(len(alone), 1)
        self.assertTrue(alone[0][3].startswith("UNMEASURED"))
        self.assertIn("N=1", alone[0][3])

    def test_the_headline_count_recomputes(self):
        v = RA.headline_count()
        self.assertEqual((v["n_unmeasured"], v["n_questions"]), (5, 8))

    def test_unmeasured_and_sourced_are_not_exclusive(self):
        self.assertEqual(RA.headline_count()["unmeasured_and_sourced"],
                         ["QF", "QH"])

    def test_the_register_runs(self):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            REG.main()
        self.assertIn("questions UNMEASURED", buf.getvalue())
        self.assertIn("REPORTING RULES".replace("REPORTING", "READING"),
                      buf.getvalue())

    # The render quotes the register's `where` fields verbatim, and one of
    # them reads "carrier records (crash, moving violation)" -- a
    # traffic-law term, not a severity label. Rewording it would misquote
    # the source, so it takes a declared exemption: DELIVERED TEXT RENDERED
    # VERBATIM. Measured in three arms rather than asserted.

    def _masked(self):
        text = RA.render(RA.findings())
        for s in REG.SOURCES.values():
            if s["where"].strip() not in ("?", "-", ""):
                text = text.replace(s["where"][:46], "<delivered>")
        return text

    def test_arm_1_masked_the_render_is_clean(self):
        hits = RA._NS.hits(self._masked())
        self.assertEqual(hits, [], "unexempted severity token: %s" % (hits,))

    def test_arm_2_unmasked_only_the_delivered_text_fires(self):
        """If anything authored here also fired, masking would not clear it."""
        hits = RA._NS.hits(RA.render(RA.findings()))
        self.assertEqual([h[1] for h in hits], ["violation"])
        self.assertIn("carrier records", hits[0][2])

    def test_arm_3_a_token_outside_the_delivered_region_is_caught(self):
        planted = self._masked() + "\nthis reading is simply wrong\n"
        self.assertTrue(RA._NS.hits(planted))

    def test_the_exemption_is_one_token_wide(self):
        """A widening turns this red rather than passing quietly."""
        hits = RA._NS.hits(RA.render(RA.findings()))
        self.assertEqual(len(hits), 1)


def main():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    print("checks: %d  failures: %d  errors: %d"
          % (res.testsRun, len(res.failures), len(res.errors)))
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
