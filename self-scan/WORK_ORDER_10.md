WORK ORDER 10 — SCAN 4 ON THIS REPO'S OWN CLAUDE.md

Target: JinnZ2/Simulators/CLAUDE.md (4636 lines, 314 KB)
Local clone, no network needed.

S1. CLASSIFY FIRST
  RETROSPECTIVE by WO6 rule — operands resolve inside
  this file tree. Confirm programmatically, don't assume.
  Any PROSPECTIVE section (roadmap, "what comes next",
  proposal.md summaries) -> OUT_OF_SCOPE, counted, never
  in a denominator.

S2. EXTRACT CHECKABLE CLAIMS
  Three kinds, kept separate:
    COUNT      "23 tests green", "69 tests green",
               "40 pass, 2 skip", "15 files total"
    IDENTITY   "byte-reproducible from X",
               "regenerates byte-identically",
               "v1 core files byte-identical between
                the two folders"
    NUMERIC    reported sim outputs: 0.65/0.12/80,
               0.334, N_eff 2.48, T_crit 9 months
  Non-checkable prose counted, not tested.

S3. RESOLVE AGAINST THE TREE
  COUNT    -> run the named test suite, compare
  IDENTITY -> regenerate or diff, compare bytes
  NUMERIC  -> run the named script, compare output
  Unrunnable (missing dep, PEP 701, non-stdlib not
  installed) -> NOT_TESTABLE with the reason. Not a
  divergence.

S4. BINS
  MAINTAINED         a test in the repo asserts it
  HOLDS_UNMAINTAINED holds now, nothing asserts it
  DIVERGED           file and stated value differ
  NOT_TESTABLE
  Bins are the finding. No score.

S5. THE THING NO WORKBOOK COULD DO
  For every DIVERGED claim, recover the divergence date
  from git: last commit touching the named artifact vs
  last commit touching the CLAUDE.md paragraph.
  Emit the interval. This is the first run where
  UNRECOVERABLE should not appear — if it does, say
  why.

S6. RATE
  DIVERGED/(DIVERGED+HOLDS). Print n. No curve.
  Compare to UNFCCC's 0.913 as a second point, flagged
  as a different document class — n=2, no direction
  claimed.

S7. CONSTRAINT
  stdlib for the scanner. Running a folder's own suite
  may need that folder's deps — declare per item.
  No severity language. Absence first-class.
  Not blind: this file has been read.
