# threshold-states/

Code for `threshold-states-in-animal-escape.md` (repo root). The document
is the instrument; this folder holds the one part of it that computes.

- `interaction.py` is the two-reference interaction test from section 8. It
  reads a joint (multimodal) response against S, the additive expectation,
  and M, the largest single facilitating response, at a declared
  tolerance.
  Precedence, step 0 first:

      0  S - M <= 2*tol            BELOW_RESOLUTION
      1  |joint - M| <= tol        REDUNDANT
      2  |joint - S| <= tol        ADDITIVE
      3  joint > S + tol           RESONANT
      4  M + tol < joint < S - tol ENHANCED_SUBADDITIVE
      5  joint < M - tol           ANTAGONISTIC (OPEN class)

  Cue sign (operator, after outside case OC-2; PROPOSED): S+ and M are taken over the
  facilitating cues (>= 0), N is the sum of the suppressive cues (< 0) and
  is recorded as its own term, and S = S+ + N. Step 0 reads S+ - M.
  - No facilitating cue: NO_FACILITATING_CUE.
  - With N < 0 the M band and the S band can still touch or swap order
    after step 0. A joint that satisfies one row gets it; one that
    satisfies two raises `BandsOverlap` naming both.
  - The split changes a reading only where S - M <= 2·tol < S+ - M; there
    the old rule said BELOW_RESOLUTION. Pinned by test.
  - Suppression is arithmetic here. It does not define ANTAGONISTIC.

  Tolerance (operator, after outside case OC-1): tol = {value, mode},
  mode `absolute` or `relative_to_M` (value × M). A tol with no declared
  mode, a bare number included, refuses (`ToleranceModeUndeclared`). An
  undeclared tol is UNRATED, not zero. All five rows are evaluated every
  time.
- `test_interaction.py` has one case per row, the edges at M±tol and
  S±tol, the S - M = 2·tol edge, a Fraction sweep, the cue-sign split
  (against the old rule), and refusals.
  - Run: `python3 threshold-states/test_interaction.py`
  - Sample: `samples/test_interaction.sample.txt`

- `outside_cases.json` holds five cases authored outside the module
  (chat-side, 2026-10-07), landed as delivered. `run_outside.py` runs them
  against `interaction.py` as authored and reports AGREE / DISAGREE;
  `test_outside.py` pins the result.
  - Run: `python3 threshold-states/run_outside.py` (exit 1 while any case
    disagrees)
  - Result now: **0 of 5 count toward the lift**, so the flag stays
    SELF-GRADED. All five refuse, since each gives tol as a bare number.
    OC-1 expected that refusal (AGREE). OC-1 and OC-2 are NON_INDEPENDENT:
    the tol rule and the cue-sign split were written in answer to them.
    OC-3, OC-4, OC-5 are CASE_AUTHOR_ERROR: underspecified tol. With either
    mode declared they read what their author expected (pinned).
  - Before both changes: 3 of 5 agreed (OC-3, OC-4, OC-5); sample @ bd7d055.
  - Fresh outside cases are to be written from the spec text alone, before
    the fix code is seen. Only status INDEPENDENT counts.
  - Samples: `samples/run_outside.sample.txt`, `samples/test_outside.sample.txt`
- Canonical module (operator, 2026-10-07): `threshold-states/interaction.py`.
  A second build of the same day (`interaction_class.py`, repo root) is
  archived whole in `archive/interaction_class/` with its PROVENANCE; the
  root file is now a redirect. Before the split the two builds agreed on
  all five outside cases.

SELF-GRADED: the tests and the module share an author. Nothing here
describes any animal or any paper. Stdlib only, CC0.
