"""Tests for key v2 amendment 1 (a1): the key file, the two scoring rules, and the filed scores.
Run: python3 -m unittest test_key_a1  (from this folder).  Tests that need a formula-audit checkout read FORMULA_AUDIT_DIR and skip without it.

Hand-worked baselines for key a1 (reasoned from the v2 values, which were worked out before the v2 scorer ran, and from the pair table):
  slots_specific, 7 of 8 pairs determined (T09|T12 is n/d): nothing grouped 2 of 7 (VOID|VOID, HOLDS|OK); label-only 2 of 7 (ABSENT, HOLDS|OK).
  The v2 value for label-only was 3 of 7 and included UNKNOWN|UNKNOWN, a pair that is n/d under a1; GAP|CRASHED has different labels, so a
  label-only reader does not group it and does not match its PARTIAL.
"""
import hashlib, importlib.util, itertools, json, os, subprocess, sys, tempfile, types, unittest
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import score as S  # noqa: E402
import score_v2 as S2  # noqa: E402
import test_score_v2 as T2  # noqa: E402  (reuses make_response and load_cplay)
def rdf(p, mode="r"):
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f: return f.read()
sha = lambda p: hashlib.sha256(rdf(p, "rb")).hexdigest()
K2 = S.load(os.path.join(HERE, "key_v2.json")); KA = S.load(os.path.join(HERE, "key_v2_a1.json"))
READING = os.path.join(ROOT, "readings", "2026-11-18_claude-v2-A")
MOVED = {"T08": ("cplay:CRASHED", ["exception", "path"]), "T09": ("taf:UNKNOWN", None),
         "T10": ("taf:GAP_INSTRUMENT_CRASH", ["missing_path", "error"]), "T12": ("cplay:UNKNOWN", ["triggers"])}

def make_a1(specific=None, carried=None):
    """A response holding exactly key a1's lists (a reader who agrees with it everywhere), with optional overrides."""
    sp = {i: (t["slots_specific"] or []) for i, t in KA["terms"].items()}; sp.update(specific or {})
    ca = {i: (t["slots_carried"] or []) for i, t in KA["terms"].items()}; ca.update(carried or {})
    return T2.make_response(specific=sp, carried=ca)

class KeyA1File(unittest.TestCase):
    def test_only_four_specific_lists_and_their_notes_differ_from_v2(self):
        for i in K2["terms"]:
            for f in K2["terms"][i]:
                same = K2["terms"][i][f] == KA["terms"][i][f]
                if i in MOVED and f in ("slots_specific", "derivation"): self.assertFalse(same, (i, f))
                else: self.assertTrue(same, (i, f))
        for i, (tid, lst) in MOVED.items():
            self.assertEqual(KA["terms"][i]["term_id"], tid); self.assertEqual(KA["terms"][i]["slots_specific"], lst)
            self.assertTrue(KA["terms"][i]["derivation"].startswith(K2["terms"][i]["derivation"]))   # old note kept, a1 note appended
    def test_pairs_differ_only_in_key_tier_specific_of_two_pairs(self):
        changed = []
        for p, q in zip(K2["pairs"], KA["pairs"]):
            self.assertEqual({k: v for k, v in p.items() if k != "key_tier_specific"}, {k: v for k, v in q.items() if k != "key_tier_specific"})
            if p["key_tier_specific"] != q["key_tier_specific"]: changed.append((p["pair_label"], p["key_tier_specific"], q["key_tier_specific"]))
        self.assertEqual(changed, [("GAP_INSTRUMENT_CRASH | CRASHED", None, "PARTIAL"), ("UNKNOWN | UNKNOWN", "PARTIAL", None)])
    def test_pair_tiers_follow_from_the_lists(self):
        cl = {i: t["cluster"] for i, t in KA["terms"].items()}
        got = S2.tiers_under(KA, cl, {i: t["slots_specific"] for i, t in KA["terms"].items()}, "specific")
        self.assertEqual(got, [p["key_tier_specific"] for p in KA["pairs"]])
    def test_meta(self):
        self.assertEqual(KA["meta"]["v"], "2-a1"); self.assertEqual(KA["meta"]["scoring_rules"], ["N1", "C1"])
        self.assertEqual(KA["meta"]["key_v2_sha256"], sha(os.path.join(HERE, "key_v2.json")))
        self.assertNotIn("scoring_rules", K2["meta"])
        self.assertEqual(KA["meta"]["a1_changes"][:4], ["T08.slots_specific", "T09.slots_specific", "T10.slots_specific", "T12.slots_specific"])
    def test_exactly_two_undetermined_specific_or_carried_lists_remain(self):
        n = [(i, m) for i, t in KA["terms"].items() for m in ("specific", "carried") if t["slots_" + m] is None]
        self.assertEqual(sorted(n), [("T09", "carried"), ("T09", "specific")])

class KeyA1DerivedFromTheSources(unittest.TestCase):
    """The changed lists are reproduced from the packet's own files, not from any reader or any key."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("derive_specific", os.path.join(ROOT, "amendment_options", "derive", "derive_specific.py"))
        cls.DS = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.DS)
        cls.T, cls.A, cls.C = cls.DS.load_cplay()
    def test_t08_is_the_fields_a_rule_requires_for_crashed_only(self):
        rs, req = self.DS.reading_slots(self.A)
        self.assertEqual(sorted(rs["CRASHED"]), sorted(KA["terms"]["T08"]["slots_specific"]))
        self.assertEqual(sorted(set(req["CRASHED"]) & {"exception", "path"}), ["exception", "path"])
    def test_t12_drops_reason_because_every_non_verdict_token_needs_one(self):
        tk, shared = self.DS.token_slots(self.T)
        self.assertEqual(tk["cplay:UNKNOWN"]["slots"], KA["terms"]["T12"]["slots_specific"])
        for state in ("UNRESOLVED", "UNTYPED"):                       # another non-verdict state refuses a missing reason
            with self.assertRaises(Exception): self.T.Token(state, None)
    def test_t10_is_the_section_record_without_the_computed_field(self):
        ua = self.DS.rd(self.DS.TAF, "calibration", "unified_audit.py")
        g = self.DS.taf_gap(ua)
        self.assertEqual(g["slots"], KA["terms"]["T10"]["slots_specific"])
        self.assertEqual(sorted(g["section_record_keys_built_in_that_handler"]), ["error", "exception_type", "missing_path"])
        self.assertEqual(g["dependence"]["computed_from"], {"exception_type": ["error"]})
    def test_t09_routes_disagree(self):
        gl = self.DS.rd(self.DS.TAF, "docs", "glossary.md"); ua = self.DS.rd(self.DS.TAF, "calibration", "unified_audit.py")
        r = self.DS.taf_unknown(ua, gl)["routes"]
        self.assertEqual(len({tuple(sorted(v)) for v in r.values()}), 2)
    def test_the_builder_reproduces_the_filed_key_byte_for_byte(self):
        fa = os.environ.get("FORMULA_AUDIT_DIR")
        if not fa or not os.path.exists(os.path.join(fa, "numcheck", "check.py")): self.skipTest("FORMULA_AUDIT_DIR not set")
        out = os.path.join(tempfile.mkdtemp(), "k.json")
        env = dict(os.environ, KEY_A1_OUT=out)
        p = subprocess.run([sys.executable, "-B", os.path.join(ROOT, "build", "make_key_a1.py")], env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        self.assertEqual(rdf(out), rdf(os.path.join(HERE, "key_v2_a1.json")))

class ScoringRules(unittest.TestCase):
    def test_v2_key_output_is_byte_identical_to_the_filed_score(self):
        resp = S.load(os.path.join(READING, "response.json"))
        o = S2.score(resp, K2)
        self.assertEqual(S2.render(o) + "\n", rdf(os.path.join(READING, "score.txt")))
        self.assertEqual(json.dumps(o, indent=1), rdf(os.path.join(READING, "score.json")))
    def test_unknown_rule_is_refused(self):
        bad = json.loads(json.dumps(KA)); bad["meta"]["scoring_rules"] = ["N1", "N2"]
        with self.assertRaises(ValueError): S2.rules_of(bad)
    def test_n1_strips_one_pair_only(self):
        n = lambda x: S2.norm_name(x, True)
        # one pair of backticks is stripped first, then one pair of < >; a doubled pair of the same kind loses only one
        self.assertEqual((n("<value>"), n("`value`"), n("<`value`>"), n("`<value>`"), n(" Value "), n("<<value>>"), n("``value``")),
                         ("value", "value", "`value`", "value", "value", "<value>", "`value`"))
        self.assertEqual(S2.norm_name("<value>", False), "<value>")
        for x in ("<", "`", "<>", "``", "a<b>"): self.assertEqual(n(x), x if x not in ("<>", "``") else "")
    def test_c1_is_exhaustive_and_exclusive_on_all_subset_pairs_of_five_names(self):
        subs = [frozenset(c) for k in range(6) for c in itertools.combinations(range(5), k)]
        for r, q in itertools.product(subs, repeat=2):
            true = {"equal": r == q, "reader-superset": r > q, "reader-subset": r < q,
                    "overlap": r != q and not r <= q and not q <= r and bool(r & q),
                    "disjoint": r != q and not r <= q and not q <= r and not (r & q)}
            self.assertEqual(sum(true.values()), 1); self.assertTrue(true[S2.relation(r, q)])
    def test_perfect_reader_under_a1(self):
        o = S2.score(make_a1(), KA)
        self.assertEqual(o["ari"], 1.0)
        sp = o["meanings"]["specific"]
        self.assertEqual((sp["slots_determined"], sp["slots_equal"], sp["n_determined"], sp["tier_agree"]), (14, 14, 7, 7))
        self.assertEqual(sp["relations"], {"equal": 14, "reader-superset": 0, "reader-subset": 0, "overlap": 0, "disjoint": 0})
        self.assertEqual((sp["baselines"]["singletons"], sp["baselines"]["label_only"]), (2, 2))
    def test_a_reader_who_copies_key_v2_gets_the_four_changes_as_differences(self):
        resp = make_a1(specific={i: (K2["terms"][i]["slots_specific"] or []) for i in MOVED})      # T08 and T09 were n/d / [] in v2
        rows = {s["id"]: s for s in S2.score(resp, KA)["meanings"]["specific"]["slots"]}
        self.assertEqual(rows["T09"]["status"], "n/d")
        self.assertEqual((rows["T08"]["relation"], rows["T10"]["relation"], rows["T12"]["relation"]), ("reader-subset", "overlap", "reader-superset"))
    def test_n1_counts_wrapped_placeholder_as_equal_only_under_a1(self):
        resp = make_a1(specific={"T02": ["<value>"]})
        r2 = {s["id"]: s for s in S2.score(resp, K2)["meanings"]["specific"]["slots"]}["T02"]
        ra = {s["id"]: s for s in S2.score(resp, KA)["meanings"]["specific"]["slots"]}["T02"]
        self.assertEqual((r2["status"], ra["status"], ra["relation"]), ("differ", "equal", "equal"))
    def test_filed_scores(self):
        resp = S.load(os.path.join(READING, "response.json"))
        p = os.path.join(READING, "score_a1.json")
        if not os.path.exists(p): self.skipTest("score_a1 not filed yet")
        o = S2.score(resp, KA)
        self.assertEqual(json.dumps(o, indent=1), rdf(p))
        self.assertEqual(S2.render(o) + "\n", rdf(os.path.join(READING, "score_a1.txt")))

if __name__ == "__main__":
    unittest.main()
