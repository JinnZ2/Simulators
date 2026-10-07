#!/usr/bin/env python3
"""run_all.py -- the contamination declaration, THEN P2, P3, P4, P5, P1.
Nothing here fetches anything. The declaration prints before any number
because a number read without it is read as a measurement of something
other than what it measures."""
import io
import os
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DECLARATION = """CONTAMINATION DECLARATION (read before any number below)
  authorship   every file in this folder is model-authored, in one session, by the same
               hand that wrote the checks and the fixtures the checks are pinned to
  position     P2, P3 and P4 are run by a system of the class whose substrate, corpus
               and reasoning chain they check; a pass is an in-class self-report and
               is not evidence about any deployed model
  fixtures     every input marked CONSTRUCTED was written so that its answer is known;
               no published methods section, study, trial or multi-agent run is read
  egress       this environment reaches no publisher host; the P1 pipeline (open-access
               methods sections) is a paste path, not a fetch
  repository   the dispatch names JinnZ2/cooperative-substrate-proof; creation was refused
               (403, integration credential), so this lands as a self-contained folder
  interest     the framing claim lowers scrutiny of a system that agrees with it; the
               checks establish necessary conditions and no coverage share is measured"""


def main():
    print(DECLARATION)
    print()
    import p2_substrate, p3_comprehension, p4_goal_coherence, p5_lag_declaration, p1_dependency_records
    for mod in (p2_substrate, p3_comprehension, p4_goal_coherence, p5_lag_declaration, p1_dependency_records):
        print("=" * 72)
        mod.main([])
    return 0


if __name__ == "__main__":
    sys.exit(main())
