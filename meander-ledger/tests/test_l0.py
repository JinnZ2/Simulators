"""Shim for forest-model-ledger/tools/check_ledger.py --tests, which imports test_l0.run_all().

Runs tests/test_meander.py in a subprocess: the two folders both ship packages named
tools/ and model/, so importing this folder's tests into the checker's process would
resolve them to the forest's packages. Parses the one-line-per-test output.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run_all():
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_meander.py")], capture_output=True, text=True)
    out = {}
    for line in p.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] in ("PASS", "FAIL", "NOT_TESTABLE") and parts[1].startswith("T_"):
            out[parts[1]] = parts[0]
    return out
