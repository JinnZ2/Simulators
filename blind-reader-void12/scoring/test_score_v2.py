"""Tests for packet v2, key v2 and score_v2. Run: python3 -m unittest test_score_v2  (from this folder).
Baselines worked out by hand before the scorer was run (pairs with an undetermined list are left out of the count):
  slots_specific, 7 of 8 pairs determined:  nothing grouped 2 of 7 (VOID|VOID, HOLDS|OK); label-only 3 of 7 (UNKNOWN, ABSENT, HOLDS|OK).
  slots_carried,  7 of 8 pairs determined:  nothing grouped 2 of 7; label-only 2 of 7 (ABSENT, HOLDS|OK).
"""
import copy, hashlib, importlib.util, inspect, json, os, re, sys, types, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import score as S  # noqa: E402
import score_v2 as S2  # noqa: E402
KEY = S.load(os.path.join(HERE, "key_v2.json"))
PK = os.path.join(ROOT, "reader_packet_v2")
SRC = os.path.join(PK, "sources")
TEMPLATE = S.load(os.path.join(PK, "response_template.json"))

def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()

def load_cplay():
    pkg = types.ModuleType("cplay_v2test"); d = os.path.join(SRC, "Simulators", "combined-playground", "cplay"); pkg.__path__ = [d]
    sys.modules["cplay_v2test"] = pkg
    for m in ("tokens", "axes", "closure"):
        spec = importlib.util.spec_from_file_location("cplay_v2test." + m, os.path.join(d, m + ".py"))
        mod = importlib.util.module_from_spec(spec); sys.modules["cplay_v2test." + m] = mod; spec.loader.exec_module(mod); setattr(pkg, m, mod)
    return pkg.tokens, pkg.axes, pkg.closure

def make_response(clusters=None, specific=None, carried=None):
    r = copy.deepcopy(TEMPLATE)
    r.update(reader_label="test", model_family="test", date_utc="2026-01-01")
    for i, t in KEY["terms"].items():
        sp = (specific or {}).get(i, t["slots_specific"] or [])
        ca = (carried or {}).get(i, t["slots_carried"] or [])
        r["terms"][i] = {"cluster": (clusters or {}).get(i, str(t["cluster"])), "predicate": "p",
                         "slots_specific": list(sp), "slots_specific_basis": "DECLARED" if sp else "NONE_STATED",
                         "slots_carried": list(ca), "slots_carried_basis": "DECLARED" if ca else "NONE_STATED",
                         "source_lines_read": "x", "confidence": "HIGH", "could_also_join": []}
    for q in r["attestation"]:
        if q.startswith("q"): r["attestation"][q] = "no"
    return r

class KeyDerivation(unittest.TestCase):
    """Each key list is checked against the packet's own source files, not against any reader."""
    @classmethod
    def setUpClass(cls):
        cls.T, cls.A, cls.C = load_cplay()
        cls.by = {t["term_id"]: t for t in KEY["terms"].values()}
    def sets(self, tid):
        t = self.by[tid]
        return t["slots_specific"], t["slots_carried"]
    def test_cplay_records_by_running_the_pinned_code(self):
        T, A, C = self.T, self.A, self.C
        sp, ca = self.sets("cplay:ExpiryTrigger")
        self.assertEqual(sp, list(inspect.signature(T.ExpiryTrigger.__init__).parameters)[1:])
        self.assertEqual(ca, list(vars(T.ExpiryTrigger("k", "t", "c"))))
        sp, ca = self.sets("cplay:ABSENT_AT_SENSITIVITY")
        self.assertEqual(sp, list(inspect.signature(T.absent_at_sensitivity).parameters))
        self.assertEqual(ca, list(vars(T.absent_at_sensitivity(limit=1, basis="LADDER", effect_size=1, conditions="c", ladder="L"))))
        sp, ca = self.sets("cplay:UNKNOWN")
        self.assertEqual(sp, list(inspect.signature(T.unknown).parameters))
        self.assertEqual(ca, list(vars(T.unknown("r", [T.ExpiryTrigger("k", "t", "c")]))))
        sp, ca = self.sets("cplay:VOID")
        self.assertEqual((sp, ca), ([], list(vars(T.Token("VOID", reason="x")))))
        self.assertEqual(self.sets("cplay:UNRESOLVED"), ([], list(C.FieldToken._fields)))
        self.assertEqual(self.sets("cplay:OK"), ([], list(A.Reading._fields)))
        self.assertEqual(self.sets("cplay:CLOSED_WITHIN")[1], list(A.Reading._fields))
    def test_closed_within_needs_exactly_sigma_and_basis(self):
        A = self.A
        sp = self.sets("cplay:CLOSED_WITHIN")[0]
        self.assertEqual(sp, ["sigma", "basis"])
        for kw in ({}, {"sigma": 1.0}, {"basis": "b"}):
            with self.assertRaises(A.AxisError):
                A.reading("PHYSICAL", "CLOSED_WITHIN", **kw)
        A.reading("PHYSICAL", "CLOSED_WITHIN", sigma=1.0, basis="b")
        A.reading("PHYSICAL", "OK")      # OK needs nothing extra
    def test_crash_carried_is_reading_plus_coverage_entry(self):
        A = self.A
        rd, ce = A.crash(ValueError("e"), path="p", module="m", inputs="i", expiry_condition=None)
        names = list(rd._fields) + [x for x in ce._fields if x not in rd._fields]
        self.assertEqual(self.sets("cplay:CRASHED")[1], names)
        self.assertEqual(len(names), 13)
        self.assertIsNone(self.sets("cplay:CRASHED")[0])
    def test_taf_lists_appear_in_the_pinned_files(self):
        reg = read(SRC, "thermodynamic-accountability-framework", "calibration", "expiry_register.py")
        m = re.search(r"EXPIRY_KEYS = \(([^)]*)\)", reg)
        self.assertEqual(re.findall(r'"(\w+)"', m.group(1)), self.sets("taf:expiry_condition")[0])
        self.assertEqual(self.sets("taf:expiry_condition")[0], self.sets("taf:expiry_condition")[1])
        ua = read(SRC, "thermodynamic-accountability-framework", "calibration", "unified_audit.py")
        i = ua.index("if status == GAP_INSTRUMENT_CRASH:")
        block = ua[i:i + 500]
        self.assertEqual(re.findall(r'"(\w+)":', block)[:6], self.sets("taf:GAP_INSTRUMENT_CRASH")[0])
        self.assertEqual(self.sets("taf:ABSENT_AT_SENSITIVITY"), (["value"], ["value"]))
        self.assertIn("ABSENT_AT_SENSITIVITY(<value>)", read(SRC, "thermodynamic-accountability-framework", "docs", "glossary.md"))
        self.assertIsNone(self.sets("taf:UNKNOWN")[1])
    def test_numcheck_keys_appear_in_the_pinned_file(self):
        src = read(SRC, "formula-audit", "numcheck", "check.py")
        i = src.index("def _blank"); blank = src[i:src.index("def _units")]
        blank_keys = ["kind", "verdict", "void_reason", "status", "deciding_tier", "precision", "rigorous", "fast", "tiers", "triage",
                      "located", "proposal", "intervals", "inputs", "units", "provenance", "slots", "human_interest", "ai_interest"]
        for k in blank_keys:
            self.assertIn('"%s"' % k, blank, k)
        union = self.sets("fa:UNDECIDED")[1]
        self.assertEqual(union[:len(blank_keys)], blank_keys)
        for k in union[len(blank_keys):]:
            self.assertRegex(src, r'rec\["%s"\]' % k, k)
        self.assertEqual(self.sets("fa:VOID")[1], union)
        point = self.sets("fa:HOLDS")[1]
        self.assertEqual(point, blank_keys + ["formula", "bisection"])
        a = src.index("def check_point"); b = src.index("def check_intersection"); c = src.index("def check_all")
        for k in ("formula", "bisection"):
            self.assertRegex(src[a:b], r'rec\["%s"\]' % k)
        for k in union[len(point):]:
            self.assertRegex(src[b:c], r'rec\["%s"\]' % k)
            self.assertNotRegex(src[a:b], r'rec\["%s"\]' % k)
    def test_exactly_two_undetermined_lists(self):
        nulls = sorted((t["term_id"], m) for t in KEY["terms"].values() for m in ("slots_specific", "slots_carried") if t[m] is None)
        self.assertEqual(nulls, [("cplay:CRASHED", "slots_specific"), ("taf:UNKNOWN", "slots_carried")])
    def test_every_term_has_a_derivation(self):
        for t in KEY["terms"].values():
            self.assertGreater(len(t["derivation"]), 40, t["term_id"])

class PacketV2(unittest.TestCase):
    def test_manifest_hashes(self):
        man = S.load(os.path.join(PK, "PACKET_MANIFEST.json"))
        for f, m in man["files"].items():
            with open(os.path.join(PK, f), "rb") as fh:
                self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), m["sha256"], f)
        on_disk = {os.path.relpath(os.path.join(d, f), PK).replace(os.sep, "/") for d, _, fs in os.walk(PK) for f in fs} - {"PACKET_MANIFEST.json"}
        self.assertEqual(on_disk, set(man["files"]))
    def test_sources_and_terms_identical_to_v1(self):
        v1 = os.path.join(ROOT, "reader_packet")
        man1, man2 = S.load(os.path.join(v1, "PACKET_MANIFEST.json")), S.load(os.path.join(PK, "PACKET_MANIFEST.json"))
        for f, m in man1["files"].items():
            if f not in ("READER_BRIEF.md", "response_template.json"):
                self.assertEqual(man2["files"][f], m, f)
    def test_no_key_vocabulary(self):
        preds = {t["predicate"] for t in KEY["terms"].values()}
        allowed = {("sources/Simulators/combined-playground/cplay/closure.py", "SPLIT")}
        for d, _, fs in os.walk(PK):
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), PK).replace(os.sep, "/")
                if rel == "PACKET_MANIFEST.json": continue
                txt = read(d, f)
                for w in ("MAPS", "PARTIAL", "HOMONYM", "SPLIT", "V-A", "V-B", "V-C"):
                    if re.search(r"\b%s\b" % re.escape(w), txt) and (rel, w) not in allowed:
                        self.fail("%s contains %s" % (rel, w))
                low = txt.lower()
                for w in preds | {"vocab_branches", "second reader", "second-reader", "void-12", "blind"}:
                    self.assertNotIn(w.lower(), low, "%s contains %r" % (rel, w))
        self.assertNotIn("vocabulary mapping", read(PK, "PACKET_MANIFEST.json").lower())
    def test_template_and_brief_agree(self):
        brief = read(PK, "READER_BRIEF.md")
        for k in TEMPLATE["terms"]["T01"]:
            self.assertIn("`%s`" % k, brief, k)
        self.assertNotIn("slots_basis", brief)
        self.assertEqual(set(TEMPLATE["terms"]["T01"]), {"cluster", "predicate", "slots_specific", "slots_specific_basis", "slots_carried",
                                                          "slots_carried_basis", "source_lines_read", "confidence", "could_also_join"})
    def test_variant_b_differs_only_by_the_clause(self):
        a, b = read(PK, "READER_BRIEF.md"), read(ROOT, "variants", "READER_BRIEF.v2.variant_B.md")
        self.assertEqual(a.replace(", even if the second system attaches different extra fields or detail", ""), b)
    def test_v1_files_untouched_by_v2(self):
        man = S.load(os.path.join(ROOT, "reader_packet", "PACKET_MANIFEST.json"))
        with open(os.path.join(ROOT, "reader_packet", "READER_BRIEF.md"), "rb") as fh:
            self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), man["files"]["READER_BRIEF.md"]["sha256"])
        with open(os.path.join(HERE, "key.json"), "rb") as fh:
            self.assertEqual(KEY["meta"]["key_v1_sha256"], hashlib.sha256(fh.read()).hexdigest())

class ScoringV2(unittest.TestCase):
    def test_perfect_reader(self):
        o = S2.score(make_response(), KEY)
        self.assertEqual(o["ari"], 1.0)
        for m in S2.MEANINGS:
            x = o["meanings"][m]
            self.assertEqual(x["tier_agree"], x["n_determined"]); self.assertEqual(x["n_determined"], 7)
            self.assertEqual(x["slots_equal"], x["slots_determined"])
        self.assertEqual(o["meanings"]["specific"]["slots_determined"], 14)
        self.assertEqual(o["meanings"]["carried"]["slots_determined"], 14)
    def test_hand_worked_baselines(self):
        o = S2.score(make_response(), KEY)["meanings"]
        self.assertEqual((o["specific"]["baselines"]["singletons"], o["specific"]["baselines"]["label_only"]), (2, 3))
        self.assertEqual((o["carried"]["baselines"]["singletons"], o["carried"]["baselines"]["label_only"]), (2, 2))
    def test_declared_tiers_are_shown_and_differ_from_key_tiers_where_welded(self):
        o = S2.score(make_response(), KEY)["meanings"]
        rows = {r["pair"]: r for r in o["specific"]["pairs"]}
        r = rows["UNDECIDED | UNRESOLVED"]
        self.assertEqual((r["first_reading_declared"], r["key"]), ("PARTIAL", "MAPS"))   # both have no tied fields: equal empty sets
        self.assertEqual(rows["GAP_INSTRUMENT_CRASH | CRASHED"]["key"], None)
        self.assertEqual({r["pair"]: r["key"] for r in o["carried"]["pairs"]}["GAP_INSTRUMENT_CRASH | CRASHED"], "PARTIAL")
        self.assertEqual({r["pair"]: r["key"] for r in o["carried"]["pairs"]}["UNKNOWN | UNKNOWN"], None)
    def test_undetermined_is_neither_match_nor_miss(self):
        o = S2.score(make_response(carried={"T09": ["anything", "at", "all"]}), KEY)["meanings"]["carried"]
        self.assertEqual(o["tier_agree"], 7)
        row = [s for s in o["slots"] if s["id"] == "T09"][0]
        self.assertEqual(row["status"], "n/d")
    def test_meanings_are_scored_separately(self):
        o = S2.score(make_response(specific={"T04": ["kind"]}), KEY)["meanings"]
        self.assertEqual(o["carried"]["slots_equal"], o["carried"]["slots_determined"])
        self.assertEqual(o["specific"]["slots_equal"], o["specific"]["slots_determined"] - 1)
        self.assertEqual(o["specific"]["tier_agree"], 7)                 # that pair is PARTIAL with either list, so the tier count is unchanged
    def test_a_name_may_be_in_one_list_only(self):
        t = [t for t in KEY["terms"].values() if t["term_id"] == "cplay:UNKNOWN"][0]
        self.assertIn("triggers", t["slots_specific"]); self.assertNotIn("triggers", t["slots_carried"])
        self.assertEqual(S2.validate(make_response(), KEY), [])
    def test_validation(self):
        r = make_response(); self.assertEqual(S2.validate(r, KEY), [])
        r = make_response(); r["terms"]["T03"]["slots_specific_basis"] = "x"; self.assertTrue(S2.validate(r, KEY))
        r = make_response(); r["terms"]["T03"]["slots_carried_basis"] = "NONE_STATED"; self.assertTrue(S2.validate(r, KEY))
        r = make_response(); del r["terms"]["T03"]["slots_carried"]; self.assertTrue(S2.validate(r, KEY))
        r = make_response(); v1 = {"cluster": "A", "predicate": "p", "slots": [], "slots_basis": "NONE_STATED", "confidence": "HIGH", "could_also_join": []}
        r["terms"]["T03"] = v1; self.assertTrue(S2.validate(r, KEY))      # a v1-shaped term is refused, not silently scored
    def test_grouping_does_not_depend_on_slots(self):
        a = S2.score(make_response(), KEY)
        b = S2.score(make_response(specific={"T05": []}, carried={"T05": []}), KEY)
        self.assertEqual((a["ari"], a["term_pairs"]), (b["ari"], b["term_pairs"]))

if __name__ == "__main__":
    unittest.main()
