# SPDX-License-Identifier: CC0-1.0
"""interaction_class.py -- REDIRECT (moved 2026-10-07).

Canonical module:  threshold-states/interaction.py
Archived build:    archive/interaction_class/interaction_class.py
Provenance:        archive/interaction_class/PROVENANCE.md

This file holds no classifier. Importing it raises ImportError naming the
canonical module, so nothing reads a stale rule by accident. Run as a
script it exits 2 (EXIT_CONTRACT section 1: wrong entry point).
"""
import sys

_MSG = ("interaction_class.py moved: the canonical module is "
        "threshold-states/interaction.py; run: "
        "python3 threshold-states/test_interaction.py "
        "(archived build: archive/interaction_class/)\n")

if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        # literal, so tools/run_manifest.py can read and resolve the target
        sys.stderr.write("interaction_class.py moved; run: "
                         "python3 threshold-states/test_interaction.py\n")
        sys.exit(2)
    sys.stderr.write(_MSG)
    sys.exit(2)

raise ImportError(_MSG.strip())
