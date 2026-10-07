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

SELF-GRADED: the tests and the module share an author. Nothing here
describes any animal or any paper. Stdlib only, CC0.
