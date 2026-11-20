"""build_multi_home_register.py must refuse a shallow sibling checkout (found 2026-11-20)."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ShallowSiblingRefused(unittest.TestCase):
    def test_selftest(self):
        p = subprocess.run([sys.executable, os.path.join(ROOT, "build_multi_home_register.py"), "--selftest"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("checks: 6   failed: 0", p.stdout)


if __name__ == "__main__":
    unittest.main()
