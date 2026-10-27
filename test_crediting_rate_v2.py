# SPDX-License-Identifier: CC0-1.0
"""test_crediting_rate_v2.py -- run the live crediting_rate_v2.py selftest.

Runs `crediting-rate/crediting_rate_v2.py --selftest` and exits with its
code. The live module is SELFTEST-class: 55 checks, 0 failed @9262516.

This is coverage of live code. It does NOT close the redirect contract
violation KNOWN_RED.md section 19.3 records. That redirect sits in the
archived copy crediting-rate/archive/f168f79/crediting_rate_v2.py, and its
target crediting-rate/test_crediting_v2.py exists only at commit f168f79.
This file is deliberately not at that path, so an archived contract cannot
read as satisfied by a live test it never named.

Usage: python3 test_crediting_rate_v2.py      (exit code = the selftest's)
Stdlib only.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "crediting-rate", "crediting_rate_v2.py")


def main():
    p = subprocess.run([sys.executable, MODULE, "--selftest"],
                       cwd=os.path.dirname(MODULE))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
