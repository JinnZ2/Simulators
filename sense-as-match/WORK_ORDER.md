WORK ORDER — sense_as_match.py + test_sense.py (rebuild from spec)
Target: Claude Code. stdlib only, CC0. Tags: OBSERVED/DERIVED/PROPOSED.

WHY
Repo references sense_as_match.py; it redirects to test_sense.py, never
committed. No original recovered. Rebuild from spec; do not hunt an original.

MEASURAND
A pattern arrives from ANY sensor/channel. Reduce it to its SHAPE. Match the
shape against a known set, IN SHAPE SPACE. The channel that delivered it is
METHOD: held aside, never used in the match. (Match on the measurand, never
the method.)

THREE RETURN STATES — all three must exist
1. KNOWN       shape matches a held shape -> return it.
2. NEW         no match AND incoming is DEFINITE -> register new shape.
3. UNCOALESCED plastic / not yet definable -> do NOT force to nearest
               neighbour. Hold with an attached probability field; collapses
               to KNOWN or NEW only when that field crosses a declared
               threshold.
Load-bearing: (3). A matcher that forces every input to nearest-neighbour
destroys the information in a thing that has not settled. This file refuses
to force.

CONTRACT
- match(incoming_shape, known_set) -> {state, shape, between?}
- uncoalesced items carry an updatable probability field that resolves on
  threshold.
- channel metadata may be stored for audit but MUST NOT enter the match.

test_sense.py — every path
- known -> KNOWN; definite novel -> NEW; plastic -> UNCOALESCED (not forced);
  uncoalesced + evidence -> collapses; NEGATIVE: uncoalesced never returns
  KNOWN by nearest-neighbour; same shape via two channels -> same state.

RULES
stdlib only, CC0. Discover repo convention first. Fix the redirect once
test_sense.py is committed. Mark gaps in-line. No author/characterization
section. Own branch, suite before/after, no PR until confirmed.
