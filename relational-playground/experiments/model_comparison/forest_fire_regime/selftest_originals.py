#!/usr/bin/env python3
"""Entry point beside the ported originals: runs tests/test_originals.py and prints its count."""
import os, sys, unittest

if __name__ == "__main__":
    tests = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tests")
    suite = unittest.defaultTestLoader.discover(tests, pattern="test_originals.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(0 if result.wasSuccessful() and result.testsRun else 1)
