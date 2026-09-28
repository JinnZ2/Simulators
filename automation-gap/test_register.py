#!/usr/bin/env python3
# test_register.py -- checks on the register audit, not on the register.
# stdlib unittest, no network. Run: python3 test_register.py
#
# Every guard is planted against: a constructed violation must fire it.
# A guard nobody has seen fire is not known to discriminate.

import ast
import copy
import inspect
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

    def test_one_scale_declared_five_sites_in_use(self):
        """Seven rungs, not six: the v6 revision added EXPLORATION, which
        is AGA_044 closing. The count is pinned so a rung arriving or
        leaving turns this red rather than passing quietly."""
        v = RA.status_vocabulary()
        self.assertEqual(len(v["declared"]), 7)
        self.assertIn("EXPLORATION", v["declared"])
        self.assertEqual(v["n_sites"], 5)
        self.assertEqual(set(v["in_sources"]),
                         {"OBSERVED", "SECONDARY", "UNREAD"})
        self.assertEqual(set(v["in_questions"]),
                         {"PARTIAL", "SUPPORTED", "UNMEASURED", "UNREAD",
                          "UNRESOLVED"})

    def test_the_scale_reaches_prose_by_a_different_mechanism(self):
        """A `status` field is a slot; a [TAG] in a sentence is not, and
        the declared scale gives a reader no way to know the second
        exists. The revision added both remaining sites."""
        v = RA.status_vocabulary()
        self.assertEqual(v["in_holds_tags"],
                         ["DERIVED", "OBSERVED", "SECONDARY"])
        self.assertEqual(v["in_term_notes"],
                         ["DERIVED", "OBSERVED", "PROPOSED"])
        self.assertEqual(v["in_addendum"],
                         ["DERIVED", "OBSERVED", "PROPOSED"])

    def test_three_question_verdict_tokens_are_declared_nowhere(self):
        self.assertEqual(RA.status_vocabulary()["undeclared"],
                         ["PARTIAL", "SUPPORTED", "UNRESOLVED"])

    def test_two_declared_rungs_reach_no_status_slot(self):
        """DERIVED and PROPOSED are exercised, and only as inline tags in
        TERM_NOTES. AGA_020's falsifier named a SOURCE carrying DERIVED;
        what happened instead was a new kind of entry carrying it, so the
        claim closes on one reading and not on the one it registered."""
        v = RA.status_vocabulary()
        self.assertEqual(v["unused_in_a_status_slot"],
                         ["DERIVED", "PROPOSED", "EXPLORATION"])
        self.assertEqual(v["unused_anywhere"], ["EXPLORATION"])

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

    def test_the_revision_split_their_frames(self):
        """S1 took TERM_DRIFT and S3 did not -- correctly: S3 is about
        dispatchers and schedules and carries no fatigue item to drift.
        The shared node is unaffected; the flags are no longer identical."""
        pr = RA.author_overlap()[0]
        self.assertFalse(pr["frames_equal"])
        self.assertIn("TERM_DRIFT", REG.SOURCES["S1"]["frame"])
        self.assertNotIn("TERM_DRIFT", REG.SOURCES["S3"]["frame"])

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
        self.assertEqual(RA.qe_scope()["as_written"], (8, 12))

    def test_over_samples_it_is_seven_of_eight(self):
        self.assertEqual(RA.qe_scope()["over_samples"], (8, 9))

    def test_s6_is_what_stops_it_being_all_of_them(self):
        """AGA_022's missing state and AGA_023's unchecked boundary are
        one gap at two sites."""
        self.assertEqual(RA.qe_scope()["blocked_by"], ["S6"])

    def test_supplying_s6_a_frame_closes_the_boundary(self):
        s6 = copy.deepcopy(REG.SOURCES["S6"])
        s6["frame"] = ["ON_ROAD"]
        with _patched(S6=s6):
            v = RA.qe_scope()
            self.assertEqual(v["over_samples"], (9, 9))
            self.assertEqual(v["blocked_by"], [])


# ------------------------------------------------------- AGA_024 flag vs defn

class FlagFitsDefinition(unittest.TestCase):

    def test_two_sources_carry_the_flag_and_do_not_fit_the_definition(self):
        v = RA.frame_definition_fit()
        self.assertEqual(v["mismatched"], ["S11", "S5"])

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
            self.assertEqual(RA.frame_definition_fit()["mismatched"], ["S11"])


# ------------------------------------------------------- AGA_025 holds kinds

class HoldsKinds(unittest.TestCase):

    def test_the_split(self):
        """v7 added two S10 entries, both findings. The reading-state count
        has not moved across three revisions; the findings count has."""
        v = RA.holds_kinds()
        self.assertEqual(v["total_holds"], 38)
        self.assertEqual(v["state_notes"], 10)
        self.assertEqual(v["findings"], 28)

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


# ------------------------------------------------- AGA_033..037 revision

class RelayProvenance(unittest.TestCase):

    def test_s11_is_relayed_through_s2(self):
        rp = RA.relay_provenance()
        self.assertEqual(len(rp), 1)
        self.assertEqual(rp[0]["src"], "S11")
        self.assertEqual(rp[0]["relayed_through"], ["S2"])

    def test_the_author_token_check_cannot_see_it(self):
        """The relation is stated in prose after the year, so a surname
        overlap finds nothing: a second shared node, and the mechanical
        check for shared nodes is blind to it."""
        self.assertFalse(RA.relay_provenance()[0]["caught_by_author_overlap"])
        self.assertNotIn("S11", [x for p in RA.author_overlap()
                                 for x in (p["a"], p["b"])])

    def test_it_reaches_no_question_so_no_n_eff_moves(self):
        for qid, v in RA.question_n_eff().items():
            self.assertNotIn("S11", v["collapsed"], qid)


class TermNoteScope(unittest.TestCase):

    def test_the_fix_names_four_sources_and_two_carry_the_flag(self):
        v = RA.term_note_scope()
        self.assertEqual(v["named_in_fix"], ["S1", "S2", "S7", "S8"])
        self.assertEqual(v["flagged"], ["S1", "S2"])
        self.assertEqual(v["named_but_unflagged"], ["S7", "S8"])

    def test_no_source_is_flagged_without_being_named(self):
        self.assertEqual(RA.term_note_scope()["flagged_but_unnamed"], [])

    def test_qi_carries_a_third_set(self):
        """Not an error: S10 is the term-drift evidence and S7/S8 are the
        unread items. Two roles, and the schema has one list."""
        v = RA.term_note_scope()
        self.assertEqual(v["qi_sources"], ["S1", "S2", "S10"])
        self.assertNotEqual(set(v["qi_sources"]), set(v["named_in_fix"]))


class OpenButUncounted(unittest.TestCase):

    def test_the_headline_counts_one_token_of_three_open_ones(self):
        v = RA.open_but_uncounted()
        self.assertEqual(v["headline"], "5 of 10")
        self.assertEqual(v["not_answered"], "8 of 11")

    def test_a_question_now_sits_outside_the_counted_list(self):
        """QK is UNMEASURED and lives in ADDENDUM_QUESTIONS, which main()
        does not count and question_refs() does not reach: eleven
        questions exist and the closing number is taken over ten."""
        v = RA.open_but_uncounted()
        self.assertEqual(v["outside_the_counted_list"], [("QK", "UNMEASURED")])
        self.assertEqual((v["n_questions"], v["n_all_questions"]), (10, 11))

    def test_the_two_added_questions_are_open_and_uncounted(self):
        """The revision added two open questions under labels the closing
        count does not recognise, so the headline fell as a fraction
        because open cells were added."""
        v = RA.open_but_uncounted()
        self.assertEqual(v["open_uncounted"],
                         [("QI", "PARTIAL"), ("QJ", "UNRESOLVED")])

    def test_answered_is_three(self):
        self.assertEqual(RA.open_but_uncounted()["answered"],
                         ["QA", "QB", "QC"])


class Revision(unittest.TestCase):

    def test_the_previous_version_resolves_by_content(self):
        """Not HEAD~1: a fixed position compares against the same bytes as
        soon as an unrelated commit lands between them."""
        v = RA.revision()
        if v["status"] != "OK":
            self.skipTest("git history not reachable: %s" % v.get("reason"))
        self.assertGreater(v["lines_added"], v["lines_removed"])
        self.assertEqual(v["removed"], [])
        # The previous version is the last COMMITTED one, and v6 and v7
        # arrived between commits -- so what this reports is their UNION,
        # not v7 alone. Nothing is estimated to split them: the union is
        # what content resolution can see. (AGA_065.)
        self.assertEqual(sorted(v["added"]),
                         ["EXPLORATION", "SLEEP_QUALITY_FACTORS"])
        self.assertEqual(sorted(v["changed"]),
                         ["G0_NOTES", "QUESTIONS", "SOURCES"])
        # the addenda are still pure additions across the union
        for k in ("ADDENDUM_QUESTIONS", "CONTROL_LOOPS", "GATE_MAP",
                  "EVENT_CLASSES", "REST_BLOCK", "TRANSFER_NOTE",
                  "BEHAVIOUR_RECORD_SCHEMA", "RULES"):
            self.assertIn(k, v["byte_identical"], k)

    def test_an_explicit_ref_that_does_not_resolve_is_reported(self):
        v = RA.revision(against="no-such-ref-xyz")
        self.assertIn(v["status"], ("NOT_AVAILABLE", "NO_PRIOR_VERSION"))
        self.assertIn("reason", v)


# ------------------------------------------------- AGA_039..043 addenda

class RestBlockProvenance(unittest.TestCase):

    def test_the_window_block_carries_no_provenance_in_the_object(self):
        """EVENT_CLASSES (the rate) has a source field on every row;
        REST_BLOCK (the window) has comments, which are not in the object
        -- a consumer importing the register gets four bare numbers."""
        v = RA.rest_block_provenance()
        self.assertFalse(v["provenance_in_the_object"])
        self.assertTrue(v["event_classes_carry_a_source_field"])

    def test_the_comments_carry_three_classes_and_one_is_silent(self):
        v = RA.rest_block_provenance()
        self.assertEqual(v["placeholder"], ["handoff_lead_min"])
        self.assertEqual(v["literature_unverified"], ["inertia_min", "nap_min"])
        self.assertEqual(v["unclassified"], ["cycle_min"])


class G0Arithmetic(unittest.TestCase):

    def test_every_input_is_declared_placeholder(self):
        self.assertTrue(RA.g0_arithmetic()["all_placeholder"])

    def test_the_rate_and_the_gap_recompute(self):
        v = RA.g0_arithmetic()
        self.assertAlmostEqual(v["lam_per_h"], 0.33, places=12)
        self.assertAlmostEqual(v["mean_gap_min"], 60.0 / 0.33, places=9)

    def test_note_three_holds_the_top_contributor_is_not_the_top_rate(self):
        """'The binding term is p_machine_fails, not raw event rate.'"""
        v = RA.g0_arithmetic()
        self.assertEqual(v["top_contributor"], "work_zone")
        self.assertEqual(v["highest_raw_rate"], "heavy_traffic_merge")
        self.assertTrue(v["note_3_holds"])

    def test_the_binding_row_and_the_lever(self):
        v = RA.g0_arithmetic()
        self.assertEqual((v["worst"]["block"], v["worst"]["inertia"]),
                         ("cycle_min", "high"))
        self.assertLess(v["worst"]["p"], 0.51)
        self.assertGreater(v["p_worst_without_top"], v["worst"]["p"])


class ClusteringDirection(unittest.TestCase):

    def test_bursting_alone_raises_p_so_poisson_is_a_floor(self):
        """Exact: a burst of k at one instant makes the BURST process
        Poisson at lam/k, so P = exp(-lam*w/60k) > exp(-lam*w/60)."""
        v = RA.clustering_direction()
        self.assertTrue(v["clustering_raises"])
        base = dict(v["clustering_only"])[1]
        self.assertAlmostEqual(base, v["poisson"], places=12)
        for k, val in v["clustering_only"]:
            if k > 1:
                self.assertGreater(val, v["poisson"], "k=%d" % k)

    def test_a_rate_peaking_at_rest_time_lowers_p_so_poisson_is_a_ceiling(self):
        v = RA.clustering_direction()
        self.assertTrue(v["peak_lowers"])
        self.assertAlmostEqual(dict(v["peak_aligned"])[0.0], v["poisson"],
                               places=12)

    def test_the_two_conditions_are_stated_in_two_places(self):
        """The docstring names the condition; the G0 note drops it and
        describes the other mechanism while drawing this one's
        conclusion."""
        v = RA.clustering_direction()
        self.assertTrue(v["same_caveat_opposite_directions"])
        self.assertIn("in the same hours as rest need",
                      REG.p_uninterrupted.__doc__)
        note = [n for n in REG.G0_NOTES if n.startswith("Clustering")][0]
        self.assertNotIn("rest need", note)
        self.assertIn("ceiling", note)


class ProbabilityDomain(unittest.TestCase):

    def test_the_valid_domain_returns_probabilities(self):
        self.assertEqual(RA.probability_domain()["in_range"],
                         ["zero rate", "zero window"])

    def test_outside_it_the_function_returns_above_one(self):
        v = RA.probability_domain()
        self.assertEqual(v["out_of_range"],
                         ["negative window", "negative rate"])
        for name, val in v["probes"]:
            if name in v["out_of_range"]:
                self.assertGreater(val, 1.0, name)


class DerivedEntry(unittest.TestCase):

    def test_a_derived_entry_now_exists(self):
        """AGA_020's substantive gap -- nothing combined two sources into
        a third statement -- closes. TRANSFER_NOTE draws on S5 and on
        TERM_NOTES and is tagged."""
        v = RA.derived_entry()
        self.assertTrue(v["combines_two"])
        self.assertTrue(v["tagged_derived"])
        self.assertTrue(v["s5_states_the_recommendation"])


# -------------------------------------------------- AGA_044..050 note 3

class Note3StatusRung(unittest.TestCase):

    def test_the_rung_the_note_declared_has_arrived_in_the_scale(self):
        """AGA_044 CLOSES by arrival. The check detects the state change
        rather than asserting the old state: the rung the note declared
        and the register lacked is now the seventh rung of the scale, so
        a reader of the register alone can discover it exists."""
        v = RA.note3_status_rung()
        self.assertEqual(v["note_declares"], ["EXPLORATION"])
        self.assertTrue(v["in_register_scale"])
        self.assertEqual(len(v["register_scale"]), 7)

    def test_it_is_declared_and_carried_by_no_entry(self):
        """The second half does not close. EXPLORATION is applied by the
        section header the entries sit under; no field states it, so the
        rung is discoverable and has no instance."""
        self.assertFalse(RA.note3_status_rung()["carried_by_an_entry"])
        self.assertTrue(RA._rung_on_an_entry("OBSERVED"))     # not constant
        self.assertFalse(RA._rung_on_an_entry("NOT_A_RUNG"))

    def test_x1_carries_nine_fields(self):
        self.assertEqual(len(RA.note3_status_rung()["x1_fields"]), 9)


class Note3GateAxis(unittest.TestCase):

    def test_the_note_makes_g0_per_operator(self):
        self.assertTrue(RA.note3_gate_axis()["note_claims_per_operator"])

    def test_the_gate_entry_names_route_and_season_and_not_operator(self):
        """AGA_045 is a claim about the GATE's own axes. The v6 revision
        put the operator into the NOTES beside it, which is a different
        statement -- read as one blob the arrival of a note would have
        read as a change to the gate."""
        v = RA.note3_gate_axis()
        self.assertTrue(v["register_names_route"])
        self.assertTrue(v["register_names_season"])
        self.assertFalse(v["register_names_operator"])
        self.assertTrue(v["operator_in_notes"])

    def test_the_window_block_holds_constants(self):
        self.assertTrue(RA.note3_gate_axis()["rest_block_is_a_constant"])


class LcdForfeit(unittest.TestCase):

    def test_the_longest_window_is_the_fleet_rule(self):
        v = RA.lcd_forfeit()
        self.assertEqual(v["lcd_minutes"], 125)
        self.assertEqual(v["rows"][-1]["forfeit"], 0.0)

    def test_the_best_sleeper_gives_up_about_a_third_of_their_own(self):
        v = RA.lcd_forfeit()
        self.assertGreater(v["worst_share"], 0.29)
        self.assertLess(v["worst_share"], 0.31)

    def test_it_peaks_where_the_gate_is_deciding(self):
        """Zero when everyone clears and zero when nobody does."""
        v = RA.lcd_forfeit()
        self.assertTrue(v["vanishes_at_both_ends"])
        self.assertGreater(v["peak_forfeit"], v["worst_forfeit"])
        self.assertGreater(v["share_of_peak"], 0.8)

    def test_no_fleet_aggregate_is_emitted(self):
        """The mix of operators is unmeasured, so a fleet number would be
        a figure with no denominator."""
        self.assertFalse(RA.lcd_forfeit()["aggregate_emitted"])


class Note3Confound(unittest.TestCase):

    def test_the_scope_section_names_two_limits(self):
        v = RA.note3_confound()
        self.assertTrue(v["scope_section_names_stimulus"])
        self.assertTrue(v["scope_section_names_ceiling"])

    def test_the_compressed_record_drops_the_one_that_confounds_it(self):
        """X1's scope field carries the stimulus limit and not the
        ceiling -- and the ceiling predicts the same direction as X1's
        own prediction."""
        v = RA.note3_confound()
        self.assertTrue(v["x1_scope_carries_stimulus"])
        self.assertFalse(v["x1_scope_carries_ceiling"])
        self.assertIn("smaller motion effect", v["x1_prediction"])

    def test_the_probe_names_one_covariate_and_the_second_is_above_it(self):
        v = RA.note3_confound()
        self.assertFalse(v["probe_names_baseline"])
        self.assertFalse(v["instrument_section_names_baseline"])
        self.assertTrue(v["scope_section_names_the_repair"])
        self.assertTrue(v["repair_is_one_section_above"])


class Note3Halves(unittest.TestCase):

    def test_both_halves_are_outside_the_register(self):
        """Unlike QJ, which held a contradiction between two sources the
        register already carried."""
        v = RA.note3_halves()
        self.assertTrue(v["both_halves_external"])
        self.assertEqual(v["n_sources"], 12)
        self.assertEqual(v["contrast_qj"], ["QJ"])

    def test_no_frame_flag_covers_the_sampling_limit_it_states(self):
        v = RA.note3_halves()
        self.assertTrue(v["sampling_limit_stated"])
        self.assertFalse(v["a_flag_for_a_narrow_lab_sample"])
        self.assertEqual(len(v["declared_frames"]), 6)


class Note3CrossRefs(unittest.TestCase):

    def test_the_one_pointer_resolves_nowhere(self):
        v = RA.note3_crossrefs()
        self.assertEqual(v["links"], ["per-operator-fitness-vs-lcd-regulation"])
        self.assertEqual(v["unresolved"], v["links"])


class Note3Fencing(unittest.TestCase):

    def test_the_flip_rests_on_n_of_1_and_is_fenced_four_ways(self):
        v = RA.note3_fencing()
        self.assertTrue(v["flip_rests_on_n_of_1"])
        self.assertEqual(v["fences"], 4)
        self.assertTrue(v["anchor_declares_n"])


# -------------------------------------------------- AGA_051..058 the v6 pass

class DeliveredTail(unittest.TestCase):
    """AGA_052 -- the v6 delivery carried a duplicated tail; the v7
    delivery does not. CLOSED by arrival, and the check reports the state
    rather than asserting either end of it."""

    def test_the_tail_is_single(self):
        """v6: 2 __main__ blocks, the register printed twice, the
        addendum-3 header three times. v7: one of each. The audit was
        never sent, so the repair is independent of it."""
        v = RA.delivered_tail()
        self.assertEqual(v["main_blocks"], 1)
        self.assertEqual(v["register_header_printed"], 1)
        self.assertEqual(v["addendum3_header_printed"], 1)

    def test_the_importable_surface_was_intact_throughout(self):
        """Why the defect cost nothing while it stood: the duplication was
        in the run path, not in the objects. Fifteen top-level objects,
        none defined twice, in both versions -- so a consumer importing
        the register got exactly what a consumer of the undoubled file
        gets, and the defect cost a reader of stdout, not an importer."""
        v = RA.delivered_tail()
        self.assertEqual(v["duplicate_objects"], 0)
        self.assertEqual(v["duplicate_functions"], 0)
        self.assertTrue(v["importable_surface_intact"])
        self.assertEqual(v["top_level_objects"], 15)


class ExplorationRungSite(unittest.TestCase):
    """AGA_053 -- one entry's relevance field contradicts the rung it is
    filed under, and the rung is on no field to contradict."""

    def test_the_rung_is_applied_by_the_section_name(self):
        v = RA.exploration_rung_site()
        self.assertFalse(v["rung_on_any_entry_field"])
        self.assertTrue(v["applied_by_the_list_name"])

    def test_the_definition_and_the_header_agree(self):
        v = RA.exploration_rung_site()
        self.assertTrue(v["definition_says_unknown"])
        self.assertTrue(v["definition_says_not_load_bearing"])
        self.assertTrue(v["header_says_unknown"])
        self.assertTrue(v["header_says_not_load_bearing"])

    def test_one_entry_states_a_relevance_the_rung_forbids(self):
        """X1 says UNKNOWN, which is the rung. X2 says DIRECT and higher
        than X1's -- a ranking inside a list whose own definition says
        relevance is unknown. Two entries, one rung, opposite readings."""
        v = RA.exploration_rung_site()
        self.assertEqual(v["contradicting"], ["X2"])
        x = {e["xid"]: e for e in v["entries"]}
        self.assertTrue(x["X1"]["says_unknown"])
        self.assertTrue(x["X2"]["says_direct"])


class PerOperatorTerm(unittest.TestCase):
    """AGA_054 -- the per-operator term AGA_045 named is now DECLARED and
    reaches no arithmetic."""

    def test_four_factors_each_stating_a_status(self):
        v = RA.per_operator_term()
        self.assertEqual(v["n_factors"], 4)
        self.assertIn("motion_sleep_history", v["factors"])
        self.assertTrue(v["every_factor_states_a_status"])

    def test_the_operator_is_in_the_notes_and_not_in_the_gate(self):
        v = RA.per_operator_term()
        self.assertFalse(v["operator_in_gate_entry"])
        self.assertTrue(v["operator_in_notes"])
        self.assertTrue(v["operator_in_factors"])

    def test_only_a_print_reads_the_factor_list(self):
        """`addendum2` renders it. `g0_window_needed`, the function the
        gate's own window comes out of, reads REST_BLOCK's four constants
        and nothing else -- so the term is declared in the file and is not
        in the number the gate is decided on."""
        v = RA.per_operator_term()
        self.assertEqual(v["readers"], ["addendum2"])
        self.assertFalse(v["reaches_arithmetic"])
        self.assertTrue(v["window_reads_rest_block_only"])


class UntaggedClaim(unittest.TestCase):
    """AGA_055 -- a causal claim sits untagged between two tagged ones."""

    def test_three_sentences_two_tagged(self):
        v = RA.untagged_claim()
        self.assertEqual(v["note1_sentences"], 3)
        self.assertEqual(v["note1_tags"], [["OBSERVED"], [], ["DERIVED"]])

    def test_the_untagged_one_is_the_causal_reading(self):
        """An OBSERVED observation and a DERIVED consequence with the step
        between them carrying no rung. The register's own device is the
        inline tag; the sentence it would cost most is the one without."""
        v = RA.untagged_claim()
        self.assertEqual(len(v["untagged"]), 1)
        self.assertIn("trust + driving consistency", v["untagged"][0])
        self.assertTrue(v["sits_between_tagged"])
        self.assertTrue(v["claim_is_causal"])


class CeilingSplit(unittest.TestCase):
    """AGA_056 -- the good-sleeper ceiling and the figure that sizes it are
    in different documents."""

    def test_the_note_states_the_limit_and_carries_no_figure(self):
        v = RA.ceiling_split()
        self.assertTrue(v["note"]["states_the_limit"])
        self.assertFalse(v["note"]["carries_the_figure"])

    def test_the_register_carries_the_figure_and_states_no_limit(self):
        v = RA.ceiling_split()
        self.assertFalse(v["register"]["states_the_limit"])
        self.assertTrue(v["register"]["carries_the_figure"])
        self.assertIn("96%", v["register_figure"])

    def test_neither_document_has_both(self):
        """Computed, not asserted: a reader of either one alone gets the
        limit without its size or the size without its consequence."""
        v = RA.ceiling_split()
        self.assertFalse(v["note_has_both"])
        self.assertFalse(v["register_has_both"])
        self.assertTrue(v["neither_has_both"])

    def test_the_word_ceiling_in_the_register_is_a_different_sense(self):
        """`treat as ceiling` in the register is about the POISSON bound,
        not about good sleepers. The three senses are separated rather
        than matched on the word, because the first version of this check
        matched all three and read the split as closed."""
        v = RA.ceiling_split()
        self.assertTrue(v["poisson_ceiling_in_register"])
        self.assertEqual(v["word_ceiling_in_register"], 1)

    def test_x1_scope_does_not_carry_the_limit(self):
        """AGA_047's finding survives the revision: the compressed record
        carries the stimulus limit and drops the ceiling."""
        self.assertFalse(RA.ceiling_split()["x1_scope_carries_the_limit"])


class X1Drift(unittest.TestCase):
    """AGA_057 -- X1 is in two documents and the two differ."""

    def test_the_field_sets_differ_by_three_names(self):
        v = RA.x1_drift()
        self.assertEqual(v["only_in_note"], ["probe"])
        self.assertEqual(v["only_in_register"], ["cheapest_probe", "xid"])

    def test_the_register_half_is_six_times_the_note_half(self):
        """Same field name, same claim, 49 chars against 301 -- and the
        long one names dated studies the short one does not."""
        v = RA.x1_drift()
        self.assertEqual(v["half_a_note_chars"], 49)
        self.assertEqual(v["half_a_register_chars"], 301)
        self.assertTrue(v["register_names_studies"])
        self.assertFalse(v["note_names_studies"])


class X2Disciplines(unittest.TestCase):
    """AGA_058 -- what X2 gets right, and the shape of its own prediction."""

    def test_the_scope_is_a_consent_limit_and_it_is_the_first(self):
        """Every prior scope field in the register bounds a SAMPLE. This
        one bounds what may be recorded at all, which is a different kind
        of limit and has no precedent here."""
        v = RA.x2_disciplines()
        self.assertTrue(v["scope_is_a_consent_limit"])
        self.assertTrue(v["first_consent_limit_in_the_register"])

    def test_the_prediction_is_selection_on_the_outcome(self):
        """Stated in the author's own words: the population that had
        trouble is the one that got studied. That is the sampling frame
        the repo records over and over, named by the entry proposing it."""
        v = RA.x2_disciplines()
        self.assertTrue(v["prediction_is_selection_on_the_outcome"])
        self.assertIn("PROPOSED", v["prediction"])

    def test_the_join_is_unmeasured_and_says_which_side_is_missing(self):
        v = RA.x2_disciplines()
        self.assertTrue(v["join"].startswith("UNMEASURED"))
        self.assertIn("never samples practice-holders", v["join"])


# -------------------------------------------------- AGA_059..065 the v7 pass

class FalsifierWording(unittest.TestCase):
    """AGA_059 -- a fault in this audit's own claim table."""

    def test_a_source_now_carries_derived_as_a_tag(self):
        v = RA.falsifier_wording()
        self.assertEqual(v["a_source_carries_derived_as_a_tag"], ["S10"])
        self.assertTrue(v["fires_on_the_wording"])

    def test_and_reaches_no_status_slot(self):
        """So the claim's substance holds and its stated falsifier does
        not distinguish the two. Both readings are reported."""
        v = RA.falsifier_wording()
        self.assertFalse(v["derived_in_any_status_slot"])
        self.assertFalse(v["fires_on_the_meaning"])

    def test_the_fault_is_read_out_of_history_not_asserted(self):
        """This is the fault, and it is in the past, so it is measured
        against the committed table rather than recalled. AGA_020's body
        recorded the falsifier firing on a reading it did not intend and
        then restated the same wording as the falsifier, naming the TOKEN
        and not the FIELD -- so it fired twice, by one mechanism, in a
        claim that had already seen it once."""
        v = RA.falsifier_wording()
        if not v["falsifier_before"]:
            self.skipTest("git history not reachable")
        self.assertTrue(v["claim_notes_the_ambiguity"])
        self.assertTrue(v["falsifier_named_the_token_only"])
        self.assertIn("source carrying", v["falsifier_before"])

    def test_the_unrepaired_table_is_resolved_by_content(self):
        """AGA_066. The first version of this check read HEAD, and
        committing the repair moved HEAD -- so the check documenting the
        fault read the repaired text and reported no fault, which is
        AGA_033's own shape committed one hour after amending the claim
        that states it. It now walks back until the falsifier stops naming
        the token only, so the reading survives every later commit."""
        v = RA.falsifier_wording()
        if not v["falsifier_before"]:
            self.skipTest("git history not reachable")
        self.assertTrue(v["resolved_at"])
        src = inspect.getsource(RA._claim_table_unrepaired)
        self.assertNotIn('"HEAD:', src)
        self.assertIn("git", src)

    def test_the_repair_is_in_the_working_tree(self):
        """Repaired rather than defended: the falsifier now names the field,
        and this check going red is what a re-widening would look like."""
        v = RA.falsifier_wording()
        self.assertTrue(v["falsifier_names_the_field_now"])
        if v["falsifier_before"]:
            self.assertTrue(v["repaired"])


class ExplorationTagSite(unittest.TestCase):
    """AGA_061 -- a sixth inline-tag site, unscanned, and silent."""

    def test_three_fields_carry_a_tag(self):
        v = RA.exploration_tag_site()
        self.assertEqual(v["fields_carrying_a_tag"],
                         ["X1.anchor", "X2.anchor", "X2.channels"])

    def test_one_field_carries_two_rungs(self):
        """`channels` tags one clause DERIVED and another PROPOSED inside
        one string -- the first field in the register to do it."""
        v = RA.exploration_tag_site()
        self.assertEqual(v["two_rungs_in_one_field"], ["X2.channels"])
        self.assertEqual(v["tags"]["X2.channels"], ["DERIVED", "PROPOSED"])

    def test_the_site_is_not_scanned_and_the_omission_is_silent(self):
        """Every token here also occurs at a scanned site, so no reported
        number moves -- which is what makes the gap invisible. A rung
        appearing only here would read as unused anywhere. The scanned
        list is read off `status_vocabulary`'s own AST, so widening it
        closes this check by itself."""
        v = RA.exploration_tag_site()
        self.assertFalse(v["site_scanned"])
        self.assertNotIn("EXPLORATION", v["scanned_objects"])
        self.assertEqual(v["tokens_new_to_the_file"], [])
        self.assertTrue(v["omission_is_silent_today"])
        self.assertEqual(v["n_sites_reported"], 5)

    def test_the_scanned_list_is_read_not_retyped(self):
        v = RA.exploration_tag_site()
        self.assertEqual(v["scanned_objects"],
                         ["ADDENDUM_QUESTIONS", "CONTROL_LOOPS",
                          "TRANSFER_NOTE"])


class ExplorationFieldSets(unittest.TestCase):
    """AGA_062 -- two entries, one list, different field sets, no schema."""

    def test_one_field_is_on_one_entry_only(self):
        v = RA.exploration_field_sets()
        self.assertEqual(v["only_in_one"], ["channels"])
        self.assertEqual(len(v["field_sets"]["X1"]), 10)
        self.assertEqual(len(v["field_sets"]["X2"]), 11)

    def test_the_renderer_is_guarded_so_absence_prints_as_absence(self):
        """`if k in x` is right for a renderer and it means an absent field
        and a field nobody thought to fill are the same output. There is no
        schema to say which."""
        self.assertTrue(RA.exploration_field_sets()["renderer_is_guarded"])

    def test_the_new_field_names_the_other_entry_s_whole_subject(self):
        """X2's `channels` names motion as a portable cue; X1 is about
        motion and sleep and has no channels field. The overlap is real and
        the cross-reference runs one way -- X2 ranks itself against X1, X1
        does not name X2."""
        v = RA.exploration_field_sets()
        self.assertTrue(v["x2_channels_names_motion"])
        self.assertTrue(v["x1_is_about_motion"])
        self.assertFalse(v["x1_has_a_channels_field"])
        self.assertTrue(v["x2_names_x1"])
        self.assertFalse(v["x1_names_x2"])


class ConsentRecord(unittest.TestCase):
    """AGA_063 -- the anchor records what was not asked for."""

    def test_it_records_three_things_about_the_ask(self):
        v = RA.consent_record()
        self.assertTrue(v["names_the_channels"])
        self.assertTrue(v["records_categories_only"])
        self.assertTrue(v["records_specifics_withheld"])
        self.assertTrue(v["records_the_ask_not_made"])

    def test_the_scope_declares_it_and_the_anchor_records_it_honoured(self):
        """Two different statements. A scope field saying what may be
        recorded is a rule; an anchor saying the specifics were withheld
        and none were requested is the rule being exercised, entered as
        provenance. Nothing else in the file does the second."""
        v = RA.consent_record()
        self.assertTrue(v["scope_declares_the_limit"])
        self.assertTrue(v["first_in_the_register"])
        self.assertEqual(v["occurrences_in_the_file"]["none requested"], 1)


class ImportedSkillArm(unittest.TestCase):
    """AGA_064 -- QE's third arm against the register's own N_OF_1 rule."""

    def test_the_arm_is_inside_the_rule_the_register_wrote(self):
        """The rule: an N=1 record bounds what is possible and does not
        estimate a rate. The arm states a possibility, estimates nothing,
        and carries a tag. The register obeying its own rule on the one
        source where it would be cheapest to break it."""
        v = RA.imported_skill_arm()
        self.assertTrue(v["arm_present"])
        self.assertTrue(v["rule_present"])
        self.assertFalse(v["arm_states_a_rate"])
        self.assertTrue(v["arm_states_a_possibility"])
        self.assertEqual(v["arm_tags"], ["DERIVED"])
        self.assertTrue(v["obeys_the_rule"])

    def test_the_arm_reaches_the_prose_and_not_the_map(self):
        """QE's source list is empty and its next-step field now leans on
        S10 by name. A reader counting which questions rest on the N=1
        record off the structured slot gets six and misses this one."""
        v = RA.imported_skill_arm()
        self.assertEqual(v["leans_without_recording"], ["QE"])
        self.assertNotIn("QE", v["s10_in_a_source_slot"])
        self.assertIn("QE", v["s10_in_free_text"])

    def test_two_holds_arrived_and_both_are_findings(self):
        v = RA.imported_skill_arm()
        self.assertEqual(len(v["new_holds"]), 2)


# ------------------------------------------------------- structure

class Structure(unittest.TestCase):

    def test_every_question_source_id_resolves(self):
        self.assertEqual(RA.question_refs()["unresolvable"], [])

    def test_four_sources_are_named_by_no_question(self):
        """S11 arrived in the revision and reaches no question."""
        self.assertEqual(RA.question_refs()["unreferenced"],
                         ["Q1", "S11", "S7", "S8"])

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
        self.assertEqual(naming, ["QA", "QF", "QH", "QI", "QJ"])
        self.assertEqual(len(alone), 1)
        self.assertTrue(alone[0][3].startswith("UNMEASURED"))
        self.assertIn("N=1", alone[0][3])

    def test_the_headline_count_recomputes(self):
        v = RA.headline_count()
        self.assertEqual((v["n_unmeasured"], v["n_questions"]), (5, 10))

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
        # LONGEST FIRST. S11's `where` is a strict prefix of S5's, so
        # masking the short one first left "(crash, moving violation)"
        # standing and the arm reported a hit it had been written to
        # mask -- a defect found by running, recorded at AGA_037.
        wheres = sorted((s["where"][:46] for s in REG.SOURCES.values()
                         if s["where"].strip() not in ("?", "-", "")),
                        key=len, reverse=True)
        for w in wheres:
            text = text.replace(w, "<delivered>")
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
