# threshold-states/

Code for `threshold-states-in-animal-escape.md` (repo root). The document
is the instrument; this folder holds the one part of it that computes.

- `interaction.py` is the two-reference interaction test from section 8,
  built to the operator's spec decisions Q1-Q4 and the OPEN resolution
  (2026-10-07, PROPOSED). It reads a joint (multimodal) response against
  S = S+ + N, the additive expectation, and M, the largest facilitating
  (>= 0) cue, at a declared tolerance tol = {value, mode}, mode `absolute`
  or `relative_to_M`. It RETURNS every verdict, first match wins:

      1  MALFORMED_INPUT       a non-number in cues/joint; tol value < 0 or
                               non-number (not None); extra tol keys; mode
                               not one of the two
      2  INSUFFICIENT_CUES     fewer than 2 cues
      3  UNRATED               no tol, or tol with no value
      4  MODE_UNDECLARED       value present, mode absent (a bare number)
      5  NO_FACILITATING_CUE   no cue >= 0
      6  BELOW_RESOLUTION      0a  S+ - M <= 2*tol_abs
      7  SUPPRESSION_OVERLAP   0b  S - M  <= 2*tol_abs  (reports I, no class)
      8  rows 1-5              REDUNDANT, ADDITIVE, RESONANT,
                               ENHANCED_SUBADDITIVE, ANTAGONISTIC (OPEN)

  Each verdict carries a distinct `next_action`. 0b replaces the earlier
  `BandsOverlap` refusal; it fires exactly where S - M <= 2*tol < S+ - M,
  the region where the pre-split rule read BELOW_RESOLUTION (pinned).
  Suppression is arithmetic here. It does not define ANTAGONISTIC.
- `test_interaction.py`: one case per row, the band edges, 0a/0b, the
  precedence pairs, the edge inputs, a Fraction sweep against the
  pre-split rule, and a check that classify() never raises on input.
  - Run: `python3 threshold-states/test_interaction.py`
  - Sample: `samples/test_interaction.sample.txt`
- `outside_cases_v2.json`: OC2-01..OC2-30, written chat-side from section 8
  text alone and committed ALONE at 95abc5d, before the build. Encoding of
  NaN, inf, null and an absent tol is stated inside the file.
  `run_outside.py` runs it unmodified and reports PASS / FAIL per case.
  - Result: **30 of 30 PASS**, file blob equal to the committed blob,
    case commit an ancestor of the build. The v2 STATE is OUTSIDE-AGREED,
    which lifts SELF-GRADED for `interaction.py` on these 30 cases.
- `outside_cases.json`: OC-1..OC-5 (v1), still run and still SELF-GRADED:
  none counts (OC-1, OC-2 NON_INDEPENDENT; OC-3..5 CASE_AUTHOR_ERROR, bare
  tol). Under the build each reads MODE_UNDECLARED; OC-1 expected a
  refusal and AGREEs. With either mode declared OC-3..5 read what their
  author expected (pinned).
  - Run: `python3 threshold-states/run_outside.py` (prints v1 then v2;
    exit 0 when v2 is OUTSIDE-AGREED)
  - Samples: `samples/run_outside.sample.txt`, `samples/test_outside.sample.txt`
- Canonical module (operator, 2026-10-07): `threshold-states/interaction.py`.
  A second build of the same day (`interaction_class.py`, repo root) is
  archived whole in `archive/interaction_class/` with its PROVENANCE; the
  root file is now a redirect. Before the split the two builds agreed on
  all five outside cases.

The unit tests and the module share an author, so they are regression
results. The v2 outside cases do not: they were written chat-side from the
spec text and committed before the build. Nothing here describes any
animal or any paper. Stdlib only, CC0.
