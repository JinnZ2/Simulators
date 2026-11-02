"""tools/narrative_check.py: planted selftest plus doc-vs-code agreement. CC0, stdlib only.

The marker list lives in two places (MARKERS in the code, two blocks in NARRATIVE_CHECK.md);
these tests make the doc's copies checkable against the code instead of trusting them.
"""
import importlib.util
import os
import re
import unittest

TOOLS = os.path.join(os.path.dirname(__file__), "..", "tools")


def _load():
    spec = importlib.util.spec_from_file_location("narrative_check", os.path.join(TOOLS, "narrative_check.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class NarrativeCheck(unittest.TestCase):
    def setUp(self):
        self.mod = _load()
        with open(os.path.join(TOOLS, "NARRATIVE_CHECK.md"), encoding="utf-8") as f:
            self.doc = f.read()
        self.keys = [m.key for m in self.mod.MARKERS]

    def test_selftest(self):
        self.assertEqual(self.mod.selftest(), 0)

    def test_twelve_markers_public_record_before_join_ask(self):
        self.assertEqual(len(self.keys), 12)
        self.assertEqual(self.keys[-2:], ["public_record_unchecked", "join_ask"])

    def test_doc_marker_block_matches_code_order(self):
        block = self.doc.split("## Markers", 1)[1].split("```text", 1)[1].split("```", 1)[0]
        listed = [ln.split()[0] for ln in block.strip().splitlines()]
        self.assertEqual(listed, self.keys)

    def test_classical_roots_table_covers_every_marker(self):
        table = self.doc.split("## Classical roots", 1)[1].split("## ", 1)[0]
        rows = re.findall(r"^\| ([a-z_]+) \|", table, re.M)
        self.assertEqual(sorted(rows), sorted(self.keys))


if __name__ == "__main__":
    unittest.main()
