#!/usr/bin/env python3
"""run_all.py -- the contamination declaration, THEN the four built
arms and the one carried arm. Nothing here fetches anything. The
declaration prints before any number because a number read without it
is read as a measurement of something other than what it measures."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DECLARATION = """CONTAMINATION DECLARATION (read before any number below)
  authorship   every file in this folder is model-authored, in one session, by the same
               hand that wrote the checks and the fixtures the checks are pinned to
  position     the author is an instance of the object under measure: a sandboxed agent
               that is a step in a chain it cannot observe. horn_b --live is run on this
               process and its reading is an in-class self-report, not evidence about any
               deployed container
  standard     neither OWASP document was read; the hosts answered 403 to CONNECT, measured
               and timestamped in clause_audit.EGRESS. step 1 is NOT_RUN_ON_STANDARD and
               the count it prints is over the order's own five-bullet summary
  vendors      none named, none read; every trust-assignment record is CONSTRUCTED
  models       none called; step 4 is a specification of its own precondition
  mitigation   none specified, per the order's scope limits
  interest     the order's thesis both lowers what an in-class author can be held to and
               lowers what it can claim to know; the direction is not legible and the
               thesis is left unresolved here rather than resolved in either direction"""


def main():
    print(DECLARATION)
    print()
    import clause_audit, trust_provenance, horn_b, load_class, dissimilar
    for mod in (clause_audit, trust_provenance, horn_b, load_class, dissimilar):
        print("=" * 72)
        mod.main([])
    return 0


if __name__ == "__main__":
    sys.exit(main())
