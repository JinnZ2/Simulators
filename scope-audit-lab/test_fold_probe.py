#!/usr/bin/env python3
"""Pins fold_probe.py's result (seeded, deterministic). Needs numpy; reports
NOT_RUN without it rather than passing or failing."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    import numpy  # noqa: F401
except ImportError:
    print("test_fold_probe: NOT_RUN (numpy absent)")
    sys.exit(0)
import fold_probe as fp  # noqa: E402

rows = dict(fp.run(draws=300))
checks = [
    ("demo regime grades CONSTANT_FIRES", rows["demo regime: uniform[0,100], th 10"]["verdict"].startswith("CONSTANT_FIRES")),
    ("quiet regime grades OK", rows["quiet regime: normal sd 1, th 10"]["verdict"] == "OK"),
]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
failed = [n for n, v in checks if not v]
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
