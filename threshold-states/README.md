# threshold-states/

Code for `threshold-states-in-animal-escape.md` (repo root). The document
is the instrument; this folder holds the one part of it that computes.

- `interaction.py` is the two-reference interaction test from section 8. It
  reads a joint (multimodal) response against S, the sum of the separate
  responses, and M, the largest single one, at a declared tolerance.
  Precedence, step 0 first:

      0  S - M <= 2*tol            BELOW_RESOLUTION
      1  |joint - M| <= tol        REDUNDANT
      2  |joint - S| <= tol        ADDITIVE
      3  joint > S + tol           RESONANT
      4  M + tol < joint < S - tol ENHANCED_SUBADDITIVE
      5  joint < M - tol           ANTAGONISTIC (OPEN class)

  An undeclared tol is UNRATED, not zero. All five rows are evaluated, and
  the call raises unless exactly one holds.
- `test_interaction.py` has one case per row, the edges at M±tol and
  S±tol, the S - M = 2·tol edge, a Fraction sweep, and refusals.
  - Run: `python3 threshold-states/test_interaction.py`
  - Sample: `samples/test_interaction.sample.txt`

- `outside_cases.json` holds five cases authored outside the module
  (chat-side, 2026-10-07), landed as delivered. `run_outside.py` runs them
  against `interaction.py` as authored and reports AGREE / DISAGREE;
  `test_outside.py` pins the result.
  - Run: `python3 threshold-states/run_outside.py` (exit 1 while any case
    disagrees)
  - Result @ 697023e: **3 of 5 agree** (OC-3, OC-4, OC-5). OC-1 expects a
    refusal when tol units are undeclared and gets ENHANCED_SUBADDITIVE.
    OC-2 expects a suppressive (negative) cue not to read BELOW_RESOLUTION,
    and it does at every joint, because S - M is the sum of the non-max cues.
  - Samples: `samples/run_outside.sample.txt`, `samples/test_outside.sample.txt`

SELF-GRADED: the tests and the module share an author. Nothing here
describes any animal or any paper. Stdlib only, CC0.
