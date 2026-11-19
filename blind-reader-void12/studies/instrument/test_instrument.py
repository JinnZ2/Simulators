"""Tests for the M01 / M02 instrument. Run from this folder: python3 -m unittest test_instrument"""
import copy, json, os, sys, unittest
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as V  # noqa: E402
fx = lambda n: json.load(open(os.path.join(HERE, "fixtures", n), encoding="utf-8"))
M01_RECORDS = json.load(open(os.path.join(os.path.dirname(HERE), "m01_records.json"), encoding="utf-8"))

# --- the fixture rules, applied mechanically, so a fixture's stipulated answer is checked, not trusted ---------------
def tag(case):
    f = case["field"]
    if f in case.get("documented_only", []): return "NO"
    on_all = all(f in i for i in case["target"])
    on_other = any(f in i for i in case["others"])        # presence: a key set to None counts
    return "YES" if on_all and not on_other else "NO"

def independence(case):
    if case["field"] in case.get("documented_only", []): return "UNRESOLVED"
    return "NO" if case["field"] in case["computed_from"] else "YES"

def carried(case):
    recs = {r["record_id"]: r for r in case["records"]}
    own = [r for r in case["records"] if r["relationship"] == "TERM_OWN_RECORD"]
    rule = case["scope_rule"]
    if rule == "TERM_OWN_RECORD_ONLY": counted = [r["record_id"] for r in own]
    elif rule == "ALL_REPORTING_PATH_RECORDS":
        counted = [r["record_id"] for r in case["records"] if r["on_reporting_path"] and r["relationship"] != "WRAPPER_RECORD"]
    elif rule == "FIRST_WRAPPER_ONLY":
        counted = [r["record_id"] for r in own] + [r["record_id"] for r in case["records"] if r["relationship"] == "WRAPPER_RECORD" and r["depth"] == 1]
    else: raise ValueError(rule)
    opened = []
    if case["traversal_rule"] == "OPEN":
        for rid in list(counted):
            for ref in recs[rid]["nested_field_refs"].values():
                if ref not in counted: opened.append(ref); counted.append(ref)
    fields = [f for rid in counted for f in recs[rid]["fields"]]
    return {"counted": counted, "opened": opened, "fields": fields}

class Fixtures(unittest.TestCase):
    def test_m01_fixtures_follow_their_own_rule(self):
        cases = fx("m01_known_answer.json")["cases"]
        self.assertGreaterEqual(len(cases), 7)
        for c in cases:
            got = {"TAG": tag(c), "INDEPENDENCE": independence(c)}
            self.assertEqual(got["TAG"], c["expected"]["TAG"], c["case_id"])
            self.assertEqual(got["INDEPENDENCE"], c["expected"]["INDEPENDENCE"], c["case_id"])
            self.assertEqual(got["TAG"] == "YES" and got["INDEPENDENCE"] == "YES", c["expected"]["slot"], c["case_id"])
    def test_m01_ka07_keeps_the_alternative_reading(self):
        c = [c for c in fx("m01_known_answer.json")["cases"] if c["case_id"] == "M01-KA-07"][0]
        applic = all(i.get(c["field"]) is not None for i in c["target"]) and not any(i.get(c["field"]) is not None for i in c["others"])
        self.assertTrue(applic)                                       # by applicability it would be YES
        self.assertEqual(c["expected"]["alternative_reading"]["TAG_by_applicability"], "YES")
    def test_m02_fixtures_follow_their_own_rule(self):
        cases = fx("m02_known_answer.json")["cases"]
        self.assertGreaterEqual(len(cases), 5)
        for c in cases:
            self.assertEqual(carried(c), c["expected"], c["case_id"])
    def test_fixtures_use_no_packet_names(self):
        packet = json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "scoring", "key_v2_a1.json"), encoding="utf-8"))
        names = set()
        for t in packet["terms"].values():
            for m in ("slots_specific", "slots_carried"):
                names |= set(t[m] or [])
        for n in ("m01_known_answer.json", "m02_known_answer.json"):
            data = fx(n)
            used = set()
            for c in data["cases"]:
                for i in c.get("target", []) + c.get("others", []): used |= set(i)
                used |= set(c.get("documented_only", [])) | ({c["field"]} if "field" in c else set())
                for r in c.get("records", []): used |= set(r["fields"])
            self.assertEqual(used & names, set(), "%s uses packet field names" % n)

class M01Validator(unittest.TestCase):
    def test_the_filed_m01_records_validate(self):
        self.assertEqual(V.m01_errors(M01_RECORDS), [])
    def test_a_reader_listing_a_computed_field_is_valid(self):
        # the behaviour under study: all three filed readers list covers_effect, which key a1 excludes
        x = [r for r in M01_RECORDS if r["field"] == "covers_effect" and r["reader"]["listed"] == "LISTED"]
        self.assertEqual(len(x), 3)
        self.assertTrue(all(r["source"]["origin"] == "COMPUTED" and r["key_a1"]["listed"] == "NOT_LISTED" for r in x))
        self.assertEqual(V.m01_errors(x), [])
    def test_not_recorded_must_be_null(self):
        r = copy.deepcopy([x for x in M01_RECORDS if x["reader"]["basis_kind"] is None][0])
        r["reader"]["basis_kind"] = "OTHER"
        self.assertTrue(V.m01_errors([r]))
    def test_unknown_enum_refused(self):
        r = copy.deepcopy(M01_RECORDS[0]); r["source"]["origin"] = "SOMETHING"
        self.assertTrue(V.m01_errors([r]))

def session(**o):
    s = {"study_id": "M02", "reader_id": "R-1", "family": "test", "packet": {"version": "v2", "variant": "A", "sha256": "x"},
         "condition": "D0", "instruction_sha256": None, "arm": "PARALLEL", "sequence_index": 1, "prior_condition": None,
         "term_id": "T10", "scope_rule": None, "traversal_rule": None, "rule_quote": None, "rule_provenance": "NOT_RECORDED",
         "ambiguity_stated": None, "unmatched_names": [],
         "records": [{"record_id": "R0", "relationship": "TERM_OWN_RECORD", "on_reporting_path": True, "depth": 0, "fields": ["a"],
                      "nested_field_refs": {}, "catalog_provenance": "SCRIPT_DERIVED", "counted": "COUNTED", "opened": None,
                      "counted_provenance": "CODER_INFERRED"}]}
    s.update(o); return s

class M02Validator(unittest.TestCase):
    def test_a_d0_session_with_nothing_stated_is_valid(self):
        self.assertEqual(V.m02_errors([session()]), [])
    def test_silence_is_not_a_rule(self):
        self.assertTrue(V.m02_errors([session(scope_rule="TERM_OWN_RECORD_ONLY")]))      # set, but NOT_RECORDED
    def test_reader_stated_rule_needs_its_quote(self):
        self.assertTrue(V.m02_errors([session(condition="D3", instruction_sha256="y", scope_rule="OTHER", rule_provenance="READER_STATED")]))
        self.assertEqual(V.m02_errors([session(condition="D3", instruction_sha256="y", scope_rule="OTHER",
                                               rule_provenance="READER_STATED", rule_quote="I count ...")]), [])
    def test_experimental_condition_needs_its_instruction_hash(self):
        self.assertTrue(V.m02_errors([session(condition="D1")]))
    def test_sequential_needs_prior_condition(self):
        self.assertTrue(V.m02_errors([session(arm="SEQUENTIAL", sequence_index=2)]))
    def test_nested_ref_must_resolve(self):
        s = session(); s["records"][0]["nested_field_refs"] = {"a": "NOWHERE"}
        self.assertTrue(V.m02_errors([s]))

if __name__ == "__main__":
    unittest.main()
