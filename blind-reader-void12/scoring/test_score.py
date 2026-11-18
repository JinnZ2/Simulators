"""Tests for the blind-reader packet, the key and the scorer. Run: python3 -m unittest test_score  (from this folder).
Expectations for the two baselines were worked out by hand before the scorer was run:
  singletons (nothing grouped): only VOID|VOID (same label, different cluster -> HOMONYM) and HOLDS|OK (NONE) agree: 2 of 8.
  label-only (cluster = label): UNKNOWN pair PARTIAL, ABSENT pair PARTIAL, HOLDS|OK NONE agree: 3 of 8.
"""
import copy, hashlib, json, os, re, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import score as S  # noqa: E402

KEY = S.load(os.path.join(HERE, "key.json"))
TEMPLATE = S.load(os.path.join(ROOT, "reader_packet", "response_template.json"))


def make_response(clusters=None, slots=None):
    r = copy.deepcopy(TEMPLATE)
    r.update(reader_label="test", model_family="test", date_utc="2026-01-01")
    for i, t in KEY["terms"].items():
        r["terms"][i] = {"cluster": (clusters or {}).get(i, str(t["cluster"])), "predicate": "p",
                         "slots": list((slots or {}).get(i, t["slots"])),
                         "slots_basis": "DECLARED" if t["slots"] else "NONE_STATED", "source_lines_read": "x",
                         "confidence": "HIGH", "could_also_join": []}
    for q in r["attestation"]:
        r["attestation"][q] = "no" if q.startswith("q") else r["attestation"][q]
    return r


class KeyAndPacket(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(KEY["terms"]), 15)
        self.assertEqual(len(KEY["pairs"]), 8)
        self.assertEqual(len({t["cluster"] for t in KEY["terms"].values()}), 9)
        self.assertEqual(sorted(p["key_tier"] for p in KEY["pairs"]),
                         sorted(["MAPS"] + ["PARTIAL"] * 5 + ["HOMONYM", "NONE"]))

    def test_key_matches_first_reader_module(self):
        p = os.path.join(ROOT, "..", "combined-playground", "cplay", "vocab_branches.py")
        with open(p, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        self.assertEqual(h, KEY["meta"]["first_reader_module_sha256"],
                         "vocab_branches.py changed since the key was built: rebuild the key and say so in the log")

    def test_packet_manifest_hashes(self):
        pd = os.path.join(ROOT, "reader_packet")
        man = S.load(os.path.join(pd, "PACKET_MANIFEST.json"))
        for f, m in man["files"].items():
            with open(os.path.join(pd, f), "rb") as fh:
                b = fh.read()
            self.assertEqual(hashlib.sha256(b).hexdigest(), m["sha256"], f)
        on_disk = {os.path.relpath(os.path.join(d, f), pd).replace(os.sep, "/")
                   for d, _, fs in os.walk(pd) for f in fs} - {"PACKET_MANIFEST.json"}
        self.assertEqual(on_disk, set(man["files"]))

    def test_packet_has_no_key_vocabulary(self):
        pd = os.path.join(ROOT, "reader_packet")
        allowed = {("sources/Simulators/combined-playground/cplay/closure.py", "SPLIT")}
        preds = {t["predicate"] for t in KEY["terms"].values()}
        for d, _, fs in os.walk(pd):
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), pd).replace(os.sep, "/")
                if rel == "PACKET_MANIFEST.json":
                    continue
                with open(os.path.join(d, f), encoding="utf-8") as fh:
                    txt = fh.read()
                for w in ("MAPS", "PARTIAL", "HOMONYM", "SPLIT", "V-A", "V-B", "V-C"):
                    if re.search(r"\b%s\b" % re.escape(w), txt) and (rel, w) not in allowed:
                        self.fail("%s contains %s" % (rel, w))
                low = txt.lower()
                for w in preds | {"vocab_branches", "second reader", "second-reader", "void-12", "blind"}:
                    self.assertNotIn(w.lower(), low, "%s contains %r" % (rel, w))

    def test_variant_brief_has_no_key_vocabulary_and_differs_only_by_the_clause(self):
        with open(os.path.join(ROOT, "variants", "READER_BRIEF.variant_B.md"), encoding="utf-8") as fh:
            b = fh.read()
        with open(os.path.join(ROOT, "reader_packet", "READER_BRIEF.md"), encoding="utf-8") as fh:
            a = fh.read()
        self.assertEqual(a.replace(", even if the second system attaches different extra fields or detail", ""), b)
        for w in ("MAPS", "PARTIAL", "HOMONYM", "SPLIT"):
            self.assertIsNone(re.search(r"\b%s\b" % w, b))
        low = b.lower()
        for w in {t["predicate"] for t in KEY["terms"].values()} | {"vocab_branches", "void-12", "second reader"}:
            self.assertNotIn(w.lower(), low)

    def test_terms_json_has_only_neutral_fields(self):
        t = S.load(os.path.join(ROOT, "reader_packet", "terms.json"))["terms"]
        self.assertEqual(len(t), 15)
        for x in t:
            self.assertEqual(set(x), {"id", "label", "definition", "source"})
            self.assertEqual(set(x["source"]), {"repo", "commit", "path", "served_as", "anchor"})
        ids = [x["id"] for x in t]
        pos = {i: n for n, i in enumerate(ids)}
        for p in KEY["pairs"]:
            self.assertGreater(abs(pos[p["left"]] - pos[p["right"]]), 1, "a declared pair sits next to each other")

    def test_ordered_and_set_slot_equality_agree_on_key(self):
        for p in KEY["pairs"]:
            if p["same_predicate"]:
                a, b = KEY["terms"][p["left"]]["slots"], KEY["terms"][p["right"]]["slots"]
                self.assertEqual(S.slotset(a) == S.slotset(b), tuple(a) == tuple(b))


class Scoring(unittest.TestCase):
    def test_perfect_reader(self):
        o = S.score(make_response(), KEY, nulls=200)
        self.assertEqual(o["tier_agree"], 8)
        self.assertEqual(o["ari"], 1.0)
        self.assertEqual(o["blind_status"], "BLIND")
        self.assertEqual(o["term_pairs"], {"both_join": 6, "reader_only": 0, "key_only": 0, "neither": 99, "total": 105})
        self.assertTrue(all(s["jaccard"] == 1.0 for s in o["slots"]))

    def test_singletons_baseline_is_2_of_8(self):
        cl = {i: "s" + i for i in KEY["terms"]}
        o = S.score(make_response(clusters=cl), KEY, nulls=0)
        self.assertEqual(o["tier_agree"], 2)
        self.assertEqual(o["baselines"]["singletons"]["tier_agree"], 2)

    def test_label_only_baseline_is_3_of_8(self):
        cl = {i: t["label"] for i, t in KEY["terms"].items()}
        o = S.score(make_response(clusters=cl), KEY, nulls=0)
        self.assertEqual(o["tier_agree"], 3)
        self.assertEqual(o["baselines"]["label_only"]["tier_agree"], 3)

    def test_one_wrong_join_is_one_difference(self):
        cl = {i: str(t["cluster"]) for i, t in KEY["terms"].items()}
        ids = {t["label"] + "|" + t["term_id"]: i for i, t in KEY["terms"].items()}
        a = ids["VOID|fa:VOID"]; b = ids["VOID|cplay:VOID"]
        cl[b] = cl[a]                                    # reader merges the two VOIDs
        o = S.score(make_response(clusters=cl), KEY, nulls=0)
        row = next(r for r in o["pairs"] if r["pair"] == "VOID | VOID")
        self.assertEqual((row["reader"], row["key"], row["agree"]), ("MAPS", "HOMONYM", False))
        self.assertEqual(o["tier_agree"], 7)
        self.assertEqual(o["term_pairs"]["reader_only"], 1)
        self.assertLess(o["ari"], 1.0)

    def test_slot_spelling_changes_tier_not_cluster(self):
        sl = {i: t["slots"] for i, t in KEY["terms"].items()}
        a = next(i for i, t in KEY["terms"].items() if t["term_id"] == "taf:GAP_INSTRUMENT_CRASH")
        sl[a] = sl[a][:-1]                               # drop one slot from one member of the MAPS pair
        o = S.score(make_response(slots=sl), KEY, nulls=0)
        row = next(r for r in o["pairs"] if r["pair"].startswith("GAP_INSTRUMENT_CRASH"))
        self.assertEqual(row["reader"], "PARTIAL")
        self.assertEqual(o["ari"], 1.0)

    def test_validation(self):
        r = make_response()
        self.assertEqual(S.validate(r, KEY), [])
        r2 = copy.deepcopy(r); del r2["terms"]["T03"]
        self.assertIn("missing term T03", S.validate(r2, KEY))
        r3 = copy.deepcopy(r); r3["terms"]["T01"]["slots_basis"] = "GUESS"
        self.assertTrue(any("slots_basis" in e for e in S.validate(r3, KEY)))
        r4 = copy.deepcopy(r); r4["terms"]["T01"]["slots_basis"] = "NONE_STATED"; r4["terms"]["T01"]["slots"] = ["x"]
        self.assertTrue(any("NONE_STATED" in e for e in S.validate(r4, KEY)))
        r5 = copy.deepcopy(r); r5["attestation"]["q1_seen_pair_table_with_verdicts"] = ""
        self.assertTrue(any("q1" in e for e in S.validate(r5, KEY)))
        r6 = copy.deepcopy(r); r6["terms"]["T99"] = r6["terms"]["T01"]
        self.assertIn("unknown term T99", S.validate(r6, KEY))

    def test_blind_status(self):
        base = {q: "no" for q in ("q1_seen_pair_table_with_verdicts", "q2_seen_predicate_sentence_by_someone_else",
                                  "q3_seen_vocabulary_mapping_or_second_reader_report", "q4_told_how_many_clusters_or_pairs",
                                  "q5_used_anything_outside_packet", "q6_prior_sessions_about_this_project")}
        self.assertEqual(S.blind_status(base), ("BLIND", []))
        b = dict(base, q3_seen_vocabulary_mapping_or_second_reader_report="yes")
        self.assertEqual(S.blind_status(b)[0], "NOT_BLIND")
        b = dict(base, q2_seen_predicate_sentence_by_someone_else="unsure")
        self.assertEqual(S.blind_status(b)[0], "UNCERTAIN")
        b = dict(base, q5_used_anything_outside_packet="yes")
        self.assertEqual(S.blind_status(b), ("BLIND", ["q5_used_anything_outside_packet"]))

    def test_reference_numbers(self):
        lo, hi = S.cp_interval(8, 8)
        self.assertAlmostEqual(lo, 0.025 ** (1 / 8), places=6)
        self.assertEqual(hi, 1.0)
        lo, hi = S.cp_interval(4, 8)
        self.assertAlmostEqual(lo, 0.1570, places=3); self.assertAlmostEqual(hi, 0.8430, places=3)
        self.assertAlmostEqual(S.ari(list("aabb"), list("xxyy")), 1.0)
        self.assertAlmostEqual(S.ari(list("aabb"), list("xyxy")), -0.5)

    def test_null_distribution(self):
        ag, ar = S.null_distribution(KEY, 4000, seed=1)
        self.assertLess(abs(sum(ar) / len(ar)), 0.02)                     # ARI is centred near 0 by construction
        self.assertLess(max(ar), 1.0 + 1e-9)
        self.assertEqual(max(ag) <= 8, True)
        o = S.score(make_response(), KEY, nulls=4000)
        self.assertLess(o["null"]["p_ari_ge_observed"], 0.001)


if __name__ == "__main__":
    unittest.main()
