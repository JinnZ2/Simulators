# SPDX-License-Identifier: CC0-1.0
"""
test_sense.py -- the redirect target named by sense_as_match.py (root).

sense_as_match.py refuses --selftest and says "run test_sense.py". This is
that file. It runs the module's own run_checks(), then the added cases
below, and exits nonzero if either has a failure.

SELF-GRADED. Every check here was written by the same hand as the module it
checks, so a pass is a REGRESSION result, not validation -- the same status
tools/known_answer.py records for its own registry (MSV_023). What would
change that: an expected value traced to a source outside this repository,
or to a second author.

NOT the instrument in sense-as-match/. That folder is a shape-space matcher
built to its own work order, with its own test_sense.py (SAM_011). This file
is about the root module only, which is a sense-at-match-site gate.

KNOWN STATE as committed: 18 of 18 module checks and 3 of 3 added cases
pass, exit 0.

History (KNOWN_RED.md sections 12-13). At dd0f794 this file ran 16 of 18:
the positive control and "score returns UNRATED on a failed gate" both
failed because gate() checked only that the TERM appeared whole-word, never
the BASIS. The author confirmed the control was correct and the gate was
missing a clause. Before the gate was touched, one added case (term
present, basis present, basis in a different paragraph) was written here
and run against the unpatched gate: FAIL, as predicted. gate() then gained
[CHOICE 6] (the basis must sit inside a match site, a paragraph holding the
term). After: 18/18 and 3/3.

The self-graded flag STAYS. The added case is by the same hand as the gate
it tests. What lifts it: a case authored outside this module -- a second
author, or an expected value traced to a source outside this repository --
passing against gate() as it stands.

Stdlib only.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import sense_as_match  # noqa: E402


# ADDED CASE, outside the module's run_checks(). Term present, basis present,
# basis NOT at the match site: the two sit in different paragraphs. Written
# before gate() was patched, and run against the unpatched gate first, so its
# first result is on record (KNOWN_RED.md section 13). Same hand as the
# module: this does not lift the self-graded flag.
SPLIT_SITE_TEXT = ("His disrespect was noted.\n\n"
                   "Elsewhere: taking for granted, and thereby missing "
                   "information.")


def added_cases():
    rec = sense_as_match.SenseRecord(
        term="disrespect",
        sense="informational",
        sense_class="speaker_supplied",
        basis="taking for granted, and thereby missing information",
        locator="ops/CONTORT-AXIS.md:14",
    )
    term_present = sense_as_match.locate(SPLIT_SITE_TEXT, rec.term) is not None
    basis_present = rec.basis in SPLIT_SITE_TEXT
    ok, reason = sense_as_match.gate(rec, SPLIT_SITE_TEXT)
    return [
        ("[added] fixture: term present in text", term_present),
        ("[added] fixture: basis present in text", basis_present),
        ("[added] basis present but not at match site -> NOT_AT_MATCH_SITE",
         ok is False and reason == "NOT_AT_MATCH_SITE"),
    ]


def main() -> int:
    print("sense_as_match.py run_checks() -- self-graded, see header")
    rc = sense_as_match.run_checks()
    print("added cases (test_sense.py) -- self-graded, same hand")
    added = added_cases()
    for name, ok in added:
        print(("PASS " if ok else "FAIL ") + name)
    n_fail = sum(1 for _, ok in added if not ok)
    print("%d/%d" % (len(added) - n_fail, len(added)))
    return 1 if (rc or n_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
