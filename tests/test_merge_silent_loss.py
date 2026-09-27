"""tools/merge_silent_loss.py in the repo suite: the constructed history is
built in a temp directory (a clean merge, a conflict resolved to one side, a
file both sides added, a `-s ours` merge, a moved line, a copied line, a
shallow clone), every state is reached, and the refusals fire. Nothing here
reads this repository's own history -- that is the sample file, and a test
pinned to live history would fail the day the history is rewritten for a
reason unrelated to the instrument."""
import importlib.util
import os
import shutil
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "tools", "merge_silent_loss.py")


def _load():
    spec = importlib.util.spec_from_file_location("merge_silent_loss", PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class TestMergeSilentLoss(unittest.TestCase):

    def test_selftest_green(self):
        mod = _load()
        self.assertEqual(mod.selftest(verbose=False), 0)

    def test_render_marks_refusal_not_zero(self):
        mod = _load()
        text = mod.render([{"merge": "deadbeef0", "status": "BASE_UNREACHABLE",
                            "base": None, "files": {}}])
        self.assertIn("BASE_UNREACHABLE", text)
        self.assertIn("refused 1", text)
        self.assertNotIn("0 files with loss", text)


if __name__ == "__main__":
    unittest.main()
