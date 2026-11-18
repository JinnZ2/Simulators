"""M1 input-brief record. Rules from COMBINED_SPEC section 7."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import brief as B  # noqa: E402

SPLIT = "system continuity and configuration continuity as separate readings"


def sa():
    return B.InputBrief("study-aperture", "2026-11-11",
                        (B.Item("chat work order", verbatim="layers: system, relational, boundary, control, continuity"),))


def r257():
    return B.InputBrief("#257", "2026-11-11",
                        (B.Item("SPEC_GPT.md", verbatim="continuity ... " + SPLIT),))


class Rules(unittest.TestCase):
    def test_brief_needs_builder_date_and_items(self):
        for bad in (dict(builder="", recorded_at="2026-11-11", items=(B.Item("x", verbatim="y"),)),
                    dict(builder="a", recorded_at="", items=(B.Item("x", verbatim="y"),)),
                    dict(builder="a", recorded_at="2026-11-11", items=())):
            with self.assertRaises(B.BriefError):
                B.InputBrief(**bad)

    def test_item_is_verbatim_or_sha256(self):
        self.assertEqual(len(B.Item("x", verbatim="abc").sha256), 64)
        B.Item("x", sha256="a" * 64)
        for bad in (dict(), dict(sha256="xyz"), dict(sha256="A" * 64)):
            with self.assertRaises(B.BriefError):
                B.Item("x", **bad)

    def test_verbatim_and_its_hash_must_agree(self):
        with self.assertRaises(B.BriefError):
            B.Item("x", verbatim="abc", sha256="0" * 64)

    def test_missing_brief_reads_unrecorded_with_reason(self):
        s = B.brief_state(None)
        self.assertEqual(s.state, B.BRIEF_UNRECORDED)
        self.assertTrue(s.reason)
        self.assertEqual(B.brief_state(sa()).state, "RECORDED")

    def test_shared_source_split_by_level(self):
        r = B.shared_source(dict(concept="continuity", split=SPLIT), sa(), r257())
        self.assertEqual(r["concept"].state, B.CUE_IN_BOTH)
        self.assertEqual(r["split"].state, B.CUE_IN_ONE)
        self.assertIn("#257", r["split"].reason)

    def test_unrecorded_brief_makes_every_level_unrecorded(self):
        r = B.shared_source(dict(concept="continuity"), None, r257())
        self.assertEqual(r["concept"].state, B.BRIEF_UNRECORDED)

    def test_hash_only_item_cannot_be_searched(self):
        h = B.InputBrief("h", "2026-11-11", (B.Item("x", sha256="b" * 64),))
        r = B.shared_source(dict(concept="continuity"), h, r257())
        self.assertEqual(r["concept"].state, B.CUE_UNSEARCHABLE)

    def test_cue_in_neither_is_its_own_state(self):
        r = B.shared_source(dict(naming="REACTIVITY"), sa(), r257())
        self.assertEqual(r["naming"].state, B.CUE_IN_NEITHER)

    def test_states_distinct_and_reasons_nonempty(self):
        self.assertEqual(len(set(B.STATES)), len(B.STATES))
        r = B.shared_source(dict(a="continuity", b=SPLIT, c="zzz"), sa(), r257())
        self.assertTrue(all(v.reason for v in r.values()))


if __name__ == "__main__":
    unittest.main()
