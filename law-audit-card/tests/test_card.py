"""Tests for law-audit-card. CC0, stdlib unittest. Run: python3 tests/test_card.py"""
import copy
import glob
import io
import json
import os
import re
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import aggregate  # noqa: E402
import card  # noqa: E402


def text(p):
    with io.open(p, encoding="utf-8") as fh:
        return fh.read()


def seed(name):
    return card.load(os.path.join(HERE, "cards", name + ".json"))


def V(why="x"):
    return {"tag": "VOID", "value": None, "basis": why}


def full():
    """A constructed card with every field filled; CONSTRUCTED, not a law."""
    c = {k: V() for k in card.FIELDS}
    c.update(id="constructed",
             stated_purpose={"tag": "PROPOSED", "value": "prevent harm h", "basis": "constructed"},
             enforcement={"tag": "OBSERVED", "value": {"mechanism": "m", "enforcer": "Agency A"}, "basis": "constructed"},
             evidence={"tag": "OBSERVED", "value": "e", "basis": "constructed"},
             evaluator={"tag": "OBSERVED", "value": {"evaluator": "Body B"}, "basis": "constructed"},
             cut_sensitivity={"tag": "VOID", "value": None, "basis": "",
                              "boundaries": [{"boundary": "b1", "evidence_reading": "SUPPORTS"},
                                             {"boundary": "b2", "evidence_reading": "SUPPORTS"}]},
             disposition={"tag": "PROPOSED", "value": {"value": "KEEP", "reader": "reader-1", "date": "2026-11-10"},
                          "basis": "reader"})
    return c


class TestShape(unittest.TestCase):
    def test_every_field_required(self):
        c = full()
        del c["evaluator"]
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_void_iff_null(self):
        c = full()
        c["target_outcome"] = {"tag": "VOID", "value": "x", "basis": "b"}
        with self.assertRaises(card.CardRefused):
            card.read(c)
        c["target_outcome"] = {"tag": "OBSERVED", "value": None, "basis": "b"}
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_observed_needs_basis(self):
        c = full()
        c["evidence"]["basis"] = ""
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_last_tested_needs_date_and_tester(self):
        c = full()
        c["last_tested"] = {"tag": "OBSERVED", "value": {"date": "2020"}, "basis": "b"}
        with self.assertRaises(card.CardRefused):
            card.read(c)


class TestCut(unittest.TestCase):
    def test_holds_flips_void(self):
        c = full()
        self.assertEqual(card.read(c)["cut_sensitivity"]["value"], "HOLDS")
        c["cut_sensitivity"]["boundaries"][1]["evidence_reading"] = "DOES_NOT_SUPPORT"
        self.assertEqual(card.read(c)["cut_sensitivity"]["value"], "FLIPS")
        c["cut_sensitivity"]["boundaries"] = c["cut_sensitivity"]["boundaries"][:1]
        self.assertEqual(card.read(c)["cut_sensitivity"]["tag"], "VOID")

    def test_undetermined_does_not_count(self):
        c = full()
        c["cut_sensitivity"]["boundaries"][1]["evidence_reading"] = "UNDETERMINED"
        self.assertEqual(card.read(c)["cut_sensitivity"]["tag"], "VOID")

    def test_boundary_is_declared_frame_field(self):
        self.assertEqual(card.frame_boundary_field(), "boundary")
        c = full()
        del c["cut_sensitivity"]["boundaries"][0]["boundary"]
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_asserted_value_must_match(self):
        c = full()
        c["cut_sensitivity"].update(tag="DERIVED", value="FLIPS", basis="asserted")
        with self.assertRaises(card.CardRefused):
            card.read(c)


class TestCircularity(unittest.TestCase):
    def test_same_party_is_conditional(self):
        c = full()
        c["evaluator"]["value"]["evaluator"] = "agency a"
        self.assertEqual(card.read(c)["circularity"]["value"], "CONDITIONAL(circular_eval)")

    def test_different_and_void(self):
        c = full()
        self.assertEqual(card.read(c)["circularity"]["value"], "INDEPENDENT_AS_DECLARED")
        c["evaluator"] = V()
        self.assertEqual(card.read(c)["circularity"]["tag"], "VOID")


class TestDisposition(unittest.TestCase):
    def test_reader_assigned_survives_when_inputs_present(self):
        r = card.read(full())
        self.assertEqual(r["disposition"]["value"], {"value": "KEEP", "reader": "reader-1", "date": "2026-11-10"})

    def test_forced_unresolved_when_evidence_or_cut_void(self):
        for which in ("evidence", "cut"):
            c = full()
            if which == "evidence":
                c["evidence"] = V()
            else:
                c["cut_sensitivity"]["boundaries"] = []
            r = card.read(c)
            self.assertEqual(r["disposition"]["value"]["value"], "UNRESOLVED")
            self.assertEqual(r["disposition"]["reader_assigned"]["value"], "KEEP")

    def test_reader_and_date_required(self):
        c = full()
        c["disposition"]["value"]["reader"] = None
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_vocabulary(self):
        self.assertEqual(card.DISPOSITIONS, ("KEEP", "EDIT", "REVISE", "RETIRE", "UNRESOLVED"))
        self.assertNotIn("REDO", card.DISPOSITIONS)
        self.assertEqual(card.DISPOSITION_MAP["REDO"], "REVISE")
        c = full()
        c["disposition"]["value"]["value"] = "REDO"
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_tool_writes_no_disposition(self):
        self.assertEqual(card.tool_writes_no_disposition(), [])
        planted = text(os.path.join(HERE, "card.py")) + '\nX = {"value": "RETIRE"}\n'
        self.assertEqual(card.tool_writes_no_disposition(planted), ["RETIRE"])


class TestScope(unittest.TestCase):
    def setUp(self):
        if card.taf_path() is None:
            self.skipTest("TAF checkout not found (set TAF_PATH)")

    def block(self, density, intent):
        return {"regulation": {"id": "R", "scope": [{"name": "d", "valid_range": [0, 10]}]},
                "conditions": {"d": density}, "intent_still_applicable": intent}

    def test_taf_verdicts_read_from_source(self):
        self.assertEqual(card.taf_verdicts(), ("IN SCOPE", "OUT OF SCOPE -- INTENT EXPIRED",
                                               "OUT OF SCOPE -- INTENT PRESERVED"))

    def test_derive_through_taf(self):
        for d, intent, want in ((5, None, "IN SCOPE"), (50, False, "OUT OF SCOPE -- INTENT EXPIRED"),
                                (50, True, "OUT OF SCOPE -- INTENT PRESERVED")):
            c = full()
            c["taf_audit"] = self.block(d, intent)
            self.assertEqual(card.read(c)["scope_valid"]["value"], want)

    def test_undeclared_intent_out_of_scope_is_void(self):
        c = full()
        c["taf_audit"] = self.block(50, None)
        self.assertEqual(card.read(c)["scope_valid"]["tag"], "VOID")

    def test_label_outside_taf_refused(self):
        c = full()
        c["scope_valid"] = {"tag": "PROPOSED", "value": "STILL GOOD", "basis": "b"}
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_not_reimplemented(self):
        self.assertNotIn("class ScopeAudit", text(os.path.join(HERE, "card.py")))


class TestSeeds(unittest.TestCase):
    def test_seeds_read_and_force_unresolved(self):
        for p in glob.glob(os.path.join(HERE, "cards", "*.json")):
            r = card.read(card.load(p))
            self.assertEqual(r["disposition"]["value"]["value"], "UNRESOLVED", p)

    def test_laundry_all_void(self):
        r = card.read(seed("sunday_laundry"))
        self.assertEqual([n for n in card.FIELDS if n != "disposition" and r[n]["tag"] != "VOID"], [])

    def test_cited_lines_exist(self):
        cites = 0
        for p in glob.glob(os.path.join(HERE, "cards", "*.json")):
            for m in re.finditer(r"(law-[a-z-]+/[A-Za-z0-9_.-]+\.md):(\d+)(?:-(\d+))?", text(p)):
                lines = text(os.path.join(REPO, m.group(1))).splitlines()
                self.assertGreaterEqual(len(lines), int(m.group(3) or m.group(2)), m.group(0))
                cites += 1
        self.assertGreater(cites, 5)

    def test_dyed_fuel_quote_is_in_the_ledger(self):
        q = seed("dyed_fuel")["enforcement"]["value"]["mechanism"]
        led = " ".join(text(os.path.join(REPO, "law-as-unvalidated-measurement",
                                         "LEDGER_SETTLE-dyed-fuel-2026-10-03.md")).split())
        self.assertIn(q, led)

    def test_aggregate(self):
        r = aggregate.count()
        self.assertEqual((r["tested_any"], r["tested_against_purpose"], r["unresolved"], r["n"]), (1, 0, 1, 3))
        self.assertIn("ILLUSTRATIVE", aggregate.render(r))

    def test_purpose_readings(self):
        c = card.read(full())
        self.assertEqual(aggregate.purpose_reading(c)[0], "NOT_TESTED")
        base = full()
        for flag, want in ((True, "AGAINST_PURPOSE"), (False, "OTHER_MEASURAND"), (None, "UNRESOLVED")):
            c = copy.deepcopy(base)
            c["last_tested"] = {"tag": "OBSERVED", "value": {"date": "2020", "tester": "t", "measurand": "m",
                                                           "matches_purpose": flag}, "basis": "constructed"}
            self.assertEqual(aggregate.purpose_reading(card.read(c))[0], want)
        c["stated_purpose"] = V()
        c["last_tested"]["value"]["matches_purpose"] = True
        self.assertEqual(aggregate.purpose_reading(card.read(c)), ("UNRESOLVED", "stated_purpose VOID"))

    def test_matches_purpose_is_three_valued(self):
        c = full()
        c["last_tested"] = {"tag": "OBSERVED", "value": {"date": "2020", "tester": "t", "matches_purpose": "yes"},
                            "basis": "b"}
        with self.assertRaises(card.CardRefused):
            card.read(c)

    def test_coverage_landed_verbatim(self):
        self.assertTrue(text(os.path.join(HERE, "COVERAGE.md")).startswith(
            "# Law audit card vs existing dirs: coverage report"))

    def test_samples_regenerate(self):
        self.assertEqual(aggregate.render(aggregate.count()) + "\n",
                         text(os.path.join(HERE, "samples", "aggregate.sample.txt")))

    def test_cli_refuses_selftest(self):
        for m in ("card.py", "aggregate.py"):
            p = subprocess.run([sys.executable, os.path.join(HERE, m), "--selftest"], capture_output=True)
            self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1).result
    n, bad = r.testsRun, len(r.failures) + len(r.errors)
    print("checks: %d   failed: %d   skipped: %d" % (n, bad, len(r.skipped)))
    sys.exit(1 if bad else 0)
