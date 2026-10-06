# SPDX-License-Identifier: CC0-1.0
"""
test_sense.py -- the redirect target named by sense_as_match.py (root).

sense_as_match.py refuses --selftest and says "run test_sense.py". This is
that file. It runs the module's own run_checks() and exits with its code.

SELF-GRADED. Every check here was written by the same hand as the module it
checks, so a pass is a REGRESSION result, not validation -- the same status
tools/known_answer.py records for its own registry (MSV_023). What would
change that: an expected value traced to a source outside this repository,
or to a second author.

NOT the instrument in sense-as-match/. That folder is a shape-space matcher
built to its own work order, with its own test_sense.py (SAM_011). This file
is about the root module only, which is a sense-at-match-site gate.

KNOWN STATE as committed: 16 of 18 pass, exit 1. Both failures trace to
one cause:
  - "positive control fires on a term not at the match site"
  - "score returns UNRATED on a failed gate"
gate() checks only that the TERM appears whole-word in the source text. The
control's text ("The word disrespect appears here.") contains the term and
not the basis, so gate() returns (True, "OK"). The control expects
NOT_AT_MATCH_SITE, i.e. a basis check the gate does not make. Either the
control is mis-specified or the gate is missing a clause; which one is the
author's call and is not decided here. Nothing in sense_as_match.py is
edited by this file.

Stdlib only.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import sense_as_match  # noqa: E402


def main() -> int:
    print("sense_as_match.py run_checks() -- self-graded, see header")
    return sense_as_match.run_checks()


if __name__ == "__main__":
    sys.exit(main())
