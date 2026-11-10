"""Tests for orientation-chamber. CC0, stdlib unittest. Run: python3 tests/test_chamber.py"""
import glob
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import chamber as C  # noqa: E402
import common  # noqa: E402
import demo  # noqa: E402
import fingerprint as FP  # noqa: E402
import markers as MK  # noqa: E402
import fix  # noqa: E402
import misslog as M  # noqa: E402
import probe as P  # noqa: E402
import selfmode as S  # noqa: E402


def tmplog():
    d = tempfile.mkdtemp()
    return M.MissLog(os.path.join(d, "log.jsonl"))


class TestMisslogCarriesNoScore(unittest.TestCase):
    def test_fields_have_no_score_like_name(self):
        self.assertFalse([f for f in M.FIELDS if common.SCORE_KEYS.search(f)])

    def test_a_score_field_is_refused(self):
        log = tmplog()
        for k in ("score", "grade", "penalty", "points", "passed", "rank"):
            with self.assertRaises(M.LogFieldRefused):
                log.append(action="N", **{k: 1})

    def test_unfilled_fields_stay_null_not_dropped(self):
        log = tmplog()
        rec = log.append(action="N")
        self.assertEqual(set(rec) - {"prev"}, set(M.FIELDS))
        self.assertIsNone(rec["predicted"])
        self.assertIsNone(rec["match"])

    def test_no_prediction_gives_null_match_not_false(self):
        self.assertEqual(P.compare(None, (1, 1)), (None, None))

    def test_append_only_chain_shows_a_rewrite(self):
        log = tmplog()
        log.append(action="N")
        log.append(action="E")
        self.assertTrue(log.verify())
        lines = open(log.path).read().splitlines()
        lines[1] = lines[1].replace('"N"', '"S"')
        open(log.path, "w").write("\n".join(lines) + "\n")
        self.assertFalse(log.verify())

    def test_sample_misslog_has_no_score_key(self):
        for line in open(os.path.join(HERE, "samples", "misslog.sample.jsonl")):
            rec = json.loads(line)
            self.assertFalse([k for k in rec if common.SCORE_KEYS.search(k)], rec)


class TestBannedWords(unittest.TestCase):
    def test_principle_is_verbatim_in_every_header(self):
        self.assertIn(common.PRINCIPLE, common.header())
        self.assertIn(common.PRINCIPLE, fix.render([]))
        first = json.loads(open(os.path.join(HERE, "samples", "misslog.sample.jsonl")).readline())
        self.assertEqual(first["_header"], common.PRINCIPLE)

    def test_all_output_is_clean_with_the_principle_masked(self):
        texts = [fix.render(demo.run(s, tempfile.mktemp()).records()) for s in range(6)]
        texts += [open(p).read() for p in glob.glob(os.path.join(HERE, "samples", "*"))]
        texts += [open(p).read() for p in glob.glob(os.path.join(HERE, "seeds", "*.json"))]
        texts += [MK.render(MK.compare_marks(s)) for s in range(4)]
        texts += [FP.render(FP.decay(demo.CONSTRUCTED_CYCLES, demo.CONSTRUCTED_SEED_FP)),
                  FP.render(FP.decay([], None))]
        for t in texts:
            self.assertEqual(common.banned_hits(t), [])

    def test_the_principle_is_the_only_exemption(self):
        # unmasked, the principle is what trips the scan; nothing else is exempted
        raw = fix.render([])
        self.assertEqual(common.banned_hits(raw.replace(common.PRINCIPLE, "x")), [])
        self.assertIn("wrong", common.PRINCIPLE)

    def test_the_scan_fires_on_a_planted_word(self):
        self.assertEqual(common.banned_hits(common.header() + " that was a mistake"), ["mistake"])
        self.assertEqual(common.banned_hits("it failed"), ["fail"])


class TestClosedLoops(unittest.TestCase):
    LOOP = ["N", "E", "S", "W"]

    def run_loop(self, rules, acts, start=(3, 3), **kw):
        return fix.closed_loop(C.Chamber(rules=rules, start=start, **kw), acts)["state"]

    def test_plain_chamber_closes(self):
        self.assertEqual(self.run_loop({}, self.LOOP), "CLOSED")

    def test_flips_still_close(self):
        self.assertEqual(self.run_loop({"flip_x": True, "flip_y": True}, self.LOOP), "CLOSED")

    def test_momentum_opens_a_wait_loop(self):
        acts = ["N", "WAIT", "S"]
        self.assertEqual(self.run_loop({}, acts), "CLOSED")
        self.assertEqual(self.run_loop({"momentum": True}, acts), "OPEN")

    def test_edge_stop_opens_and_wrap_closes(self):
        acts = ["E", "W"]
        self.assertEqual(self.run_loop({}, acts, start=(6, 3)), "OPEN")
        self.assertEqual(self.run_loop({"wrap": True}, acts, start=(6, 3)), "CLOSED")

    def test_sticky_opens(self):
        self.assertEqual(self.run_loop({"wrap": True, "sticky": True}, ["E", "W"], start=(6, 3)), "OPEN")

    def test_delay_opens_until_waits_catch_up(self):
        self.assertEqual(self.run_loop({"delay": True}, self.LOOP, delay_steps=1), "OPEN")
        self.assertEqual(self.run_loop({"delay": True}, self.LOOP + ["WAIT"], delay_steps=1), "CLOSED")

    def test_not_a_loop(self):
        self.assertEqual(self.run_loop({}, ["N", "N"]), "NOT_A_LOOP")


class TestIndependence(unittest.TestCase):
    def test_same_path_twice_is_one_wall(self):
        log, ch = tmplog(), C.Chamber(rules={})
        P.probe_path(ch, ["N", "E", "S", "W"], log=log)
        P.probe_path(ch, ["N", "E", "S", "W"], log=log)  # closed, so same start: same signature
        loops = fix.loops_readout(log.records())
        self.assertEqual(len(loops), 1)
        v = list(loops.values())[0]
        self.assertEqual(v["walked"], 2)
        self.assertIn("one wall, not 2", v["independence"])

    def test_located_needs_two_independent_paths(self):
        log, ch = tmplog(), C.Chamber(rules={"flip_x": True})
        ch_pos = ch.reported()
        P.probe_path(ch, ["E"], [(ch_pos[0] - 1, ch_pos[1])], log, rule_hypothesis="flip_x")
        r = fix.rules_readout(log.records())
        self.assertEqual(r["flip_x"]["state"], "FLOATING")
        p2 = ch.reported()
        P.probe_path(ch, ["W", "W"], [(p2[0] + 1, p2[1]), (p2[0] + 2, p2[1])], log, rule_hypothesis="flip_x")
        r = fix.rules_readout(log.records())
        self.assertEqual(r["flip_x"]["state"], "LOCATED")
        self.assertEqual(r["sticky"]["state"], "UNTESTED")

    def test_unlocated_counts_untagged_misses(self):
        log, ch = tmplog(), C.Chamber(rules={"flip_y": True})
        p = ch.reported()
        P.probe_path(ch, ["N"], [(p[0], p[1] + 1)], log)
        m = fix.misses_readout(log.records())
        self.assertEqual((m["MISS"], m["UNLOCATED"]), (1, 1))


class TestSelfMode(unittest.TestCase):
    def test_both_levels_logged(self):
        rec = S.record_self(tmplog(), predicted_specific="N", predicted_category="move", actual_specific="E")
        self.assertEqual(rec["match"], {"category": True, "specific": False})

    def test_unmade_prediction_is_null(self):
        rec = S.record_self(None, predicted_category="wait", actual_specific="N")
        self.assertEqual(rec["match"], {"category": False, "specific": None})


class TestReproducible(unittest.TestCase):
    def test_same_seed_same_rules_and_trace(self):
        a, b = C.Chamber(seed=11), C.Chamber(seed=11)
        self.assertEqual(a.reveal(), b.reveal())
        acts = ["N", "E", "WAIT", "S", "W", "W", "N"]
        self.assertEqual([a.step(x) for x in acts], [b.step(x) for x in acts])

    def test_same_seed_same_misslog(self):
        def body(s):
            return [{k: v for k, v in r.items() if k != "prev"} for r in demo.run(s, tempfile.mktemp()).records()]
        self.assertEqual(body(3), body(3))

    def test_seeds_differ(self):
        self.assertTrue(len(set(json.dumps(C.Chamber(seed=s).reveal()["rules"], sort_keys=True) for s in range(20))) > 1)

    def test_sample_regenerates(self):
        out = tempfile.mktemp()
        self.assertEqual(fix.render(demo.run(7, out).records()) + "\n",
                         open(os.path.join(HERE, "samples", "readout.sample.txt")).read())
        self.assertEqual(MK.render(MK.compare_marks(7)),
                         "\n".join(open(os.path.join(HERE, "samples", "markers.sample.txt")).read().splitlines()[:7]))

    def test_unknown_action_raises(self):
        with self.assertRaises(ValueError):
            C.Chamber(rules={}).step("UP")


class TestStillness(unittest.TestCase):
    def test_no_move_is_legal_and_logged(self):
        log, ch = tmplog(), C.Chamber(rules={})
        p = ch.reported()
        rec = P.probe(ch, "NO_MOVE", p, log)
        self.assertEqual((rec["action"], rec["match"], rec["note"]), ("NO_MOVE", True, "stillness control"))
        self.assertEqual(log.records()[-1]["action"], "NO_MOVE")

    def test_stillness_locates_delay(self):
        ch = C.Chamber(rules={"delay": True}, delay_steps=1)
        ch.step("E")
        before = ch.reported()
        self.assertNotEqual(ch.step("NO_MOVE"), before)  # a still probe that moves locates a rule

    def test_no_move_carries_momentum_like_wait(self):
        a, b = C.Chamber(rules={"momentum": True}), C.Chamber(rules={"momentum": True})
        a.step("N"); b.step("N")
        self.assertEqual(a.step("WAIT"), b.step("NO_MOVE"))

    def test_sample_carries_a_stillness_probe(self):
        recs = [json.loads(l) for l in open(os.path.join(HERE, "samples", "misslog.sample.jsonl"))][1:]
        self.assertTrue([r for r in recs if r["kind"] == "world" and r["action"] == "NO_MOVE"])


class TestMarkers(unittest.TestCase):
    def test_types_and_usage(self):
        mk = MK.Markers(C.Chamber(rules={}))
        for t in MK.TYPES:
            mk.place(t)
        self.assertEqual(mk.usage_counts(), dict((t, 1) for t in MK.TYPES))
        with self.assertRaises(ValueError):
            mk.place("FLAG")

    def test_fading_decays(self):
        ch = C.Chamber(rules={})
        mk = MK.Markers(ch)
        mk.place("FADING")
        cell = ch.pos
        for _ in range(MK.FADE_LIFE):
            ch.step("WAIT")
        self.assertFalse(mk.searched(cell))
        self.assertEqual(mk.here(cell), [])

    def test_repel_persists_and_void_covers_neighbours(self):
        ch = C.Chamber(rules={})
        mk = MK.Markers(ch)
        mk.place("REPEL")
        c = ch.pos
        for _ in range(20):
            ch.step("WAIT")
        self.assertTrue(mk.searched(c))
        ch2 = C.Chamber(rules={})
        mk2 = MK.Markers(ch2)
        mk2.place("VOID")
        x, y = ch2.pos
        self.assertTrue(mk2.searched((x + 1, y)))
        self.assertFalse(mk2.searched((x + 2, y)))

    def test_landmark_relocalize(self):
        ch = C.Chamber(rules={})
        mk = MK.Markers(ch)
        lm = mk.place("LANDMARK")
        ch.step("E")
        self.assertEqual(mk.relocalize(lm), {"W": 1, "E": -1, "S": 0, "N": 0})

    def test_marks_sense_the_true_cell_under_delay(self):
        ch = C.Chamber(rules={"delay": True}, delay_steps=2)
        mk = MK.Markers(ch)
        ch.step("E")
        mk.place("PLACED", note="o")
        self.assertEqual(mk.here()[0]["cell"], ch.pos)
        self.assertNotEqual(ch.pos, ch.reported())

    def test_re_search_with_vs_without(self):
        plain = {r["mark"]: r["revisits"] for r in MK.compare_marks(3, rules={})}
        flipped = {r["mark"]: r["revisits"] for r in MK.compare_marks(3, rules={"flip_x": True, "flip_y": True})}
        self.assertLess(plain["REPEL"], plain["none"])      # marks help when the action model is right
        self.assertGreater(flipped["REPEL"], flipped["none"])  # and steer into marked cells when it is not
        self.assertEqual(plain["VOID"], plain["none"])       # VOID marks every neighbour: no guidance

    def test_trial_reproducible(self):
        self.assertEqual(MK.search_trial(5, "REPEL"), MK.search_trial(5, "REPEL"))


class TestFingerprint(unittest.TestCase):
    def test_void_without_prior_conversation(self):
        seed = FP.load_seed("prior-conversation")
        self.assertIsNone(seed["fingerprint"])
        r = FP.decay(demo.CONSTRUCTED_CYCLES, seed["fingerprint"])
        self.assertEqual((r["state"], r["rows"], r["crossing_cycle"]), ("VOID", [], None))

    def test_crossing_cycle(self):
        r = FP.decay(demo.CONSTRUCTED_CYCLES, demo.CONSTRUCTED_SEED_FP)
        self.assertEqual((r["state"], r["crossing_cycle"]), ("CROSSED", 2))

    def test_not_crossed(self):
        r = FP.decay([demo.CONSTRUCTED_CYCLES[0]] * 3, demo.CONSTRUCTED_SEED_FP)
        self.assertEqual(r["state"], "NOT_CROSSED")

    def test_similarity_known_answers(self):
        m = FP.load_seed("median")["fingerprint"]
        self.assertEqual(FP.similarity(m, m), 1.0)
        self.assertEqual(FP.similarity({"WAIT": 1.0}, m), 0.0)
        self.assertIsNone(FP.similarity(None, m))
        self.assertEqual(FP.mix(["NO_MOVE", "WAIT"])["WAIT"], 1.0)


class TestCitation(unittest.TestCase):
    def test_related_work_carried(self):
        r = open(os.path.join(HERE, "README.md")).read()
        self.assertIn("arXiv 2509.21224", r)
        self.assertIn("CARRIED", r)


class TestCli(unittest.TestCase):
    def test_modules_refuse_selftest(self):
        import subprocess
        for m in ("fix.py", "markers.py", "fingerprint.py"):
            p = subprocess.run([sys.executable, os.path.join(HERE, m), "--selftest"], capture_output=True)
            self.assertEqual(p.returncode, 2, m)


if __name__ == "__main__":
    r = unittest.main(exit=False, verbosity=1).result
    n, bad = r.testsRun, len(r.failures) + len(r.errors)
    print("checks: %d   failed: %d" % (n, bad))
    sys.exit(1 if bad else 0)
