# Missing-column finder: exploratory run on the PSF residuals

CC0. Exploratory. Nothing here is a test and nothing here is scored.

Status: EXPLORATORY. Co-authored, Kavik + Claude, work order of
2026-11-22. Run date (UTC): 2026-11-22. Observer slots: null.

"Holdout spent at Phase C; this is exploratory and scores nothing."

Tags: DERIVED = computed in this run from the data and the stated
choices; PROPOSED = a reading or a next step, untested; OBSERVED = seen
in this run (gate lines, hashes); NOT RECORDED = nobody in this run
looked. Every reading of the data below is DERIVED. None is a finding
about plant-soil feedback; the candidates are places to look.

Every number in the indented blocks was printed by
`python3 ledger/toolkit/missing_column_finder.py run SOURCE_CSV` and
pasted by script. None was typed.

## 1. What the tool does

    spread   weighted sum of squares of rr about its weighted mean,
             weights 1/(var + tau2), tau2 from an intercept-only fit
    a, b     each of the 12 recorded columns fitted alone (the Phase B
             slope fit, imported unchanged), then all 12 together
    c        on the residuals of the all-columns fit, three grouping
             tests, each against a permutation null (499 shuffles):
               lab             rows by Author; rows shuffled
               between-study   study means by label; studies shuffled
               within-study    residuals minus study mean, by label;
                               rows shuffled inside each study
    d        FLAG = share above every null share AND share minus null
             mean >= 0.02. A flagged grouping is a MISSING COLUMN
             candidate.

Region = 20-degree latitude by 20-degree longitude bins. The two FLAG
constants, the bin width and the shuffle count are hand-set and were
fixed before the gate was run; the gate passed on its first run and
nothing was adjusted afterwards. [OBSERVED]

Region, Year, Species and Family are never read at row level: that
would count the lab spread a second time under another name.

## 2. Gate (before any real run)

    known-answer, hidden variable tied to Family: flagged on 5 of 5 seeds  PASS
    known-answer, hidden variable tied to region: flagged on 5 of 5 seeds  PASS
    known-answer, hidden variable tied to Author: flagged on 5 of 5 seeds  PASS
    null-harness, pure noise: 0 candidates over 5 seeds (35 tests)  PASS
    GATE PASS

[OBSERVED] Known-answer: synthetic rows shaped like the dataset (60
studies) with one hidden effect tied to a grouping and to no column. The
tool flagged the planted grouping on every seed, in three placements
(inside studies, between studies, per lab). Null-harness: the same rows
with pure sampling noise; no candidate on any seed.

Gate scope: the synthetic rows carry no between-study spread unless it
is planted. Real data always has some, so the lab test was expected to
flag on real data and its flag alone says little (section 5).

## 3. Explained spread, per column

Source file sha256 asserted before the run
(bb56ba5a...c82c, the Phase A fetch). Anchor = Year <= 2018, holdout =
Year > 2018, pooled = all rows.

    anchor (<= 2018): 3707 rows, 155 studies, tau2 0.2205
      column                 share alone   slope      rows
      Experimental.setting     0.0000     -0.0104   3707
      Phase2.time              0.0009     +0.0048   3701
      Approach                 0.0003     -0.0302   3707
      Phase1.culti             0.0138     -0.1767   3707
      SoilTp                   0.0049     -0.0861   3707
      Life.form                0.0035     +0.1000   3707
      F.H                      0.0042     -0.0842   3707
      Sp.origin                0.0081     +0.1374   3707
      MAT                      0.0000     +0.0001   3707
      MAP                      0.0041     -0.0001   3707
      AI                       0.0206     -0.2378   3707
      Latitude.abs             0.0196     -0.0101   3707
      all 12 columns together: share 0.0585, left 0.9415 (3701 complete rows)
      grouping patterns on what is left:
        Author   groups  154
          lab             share 0.250  null mean 0.040  null max 0.068  excess +0.210  FLAG
        region   groups   30
          between-study   share 0.207  null mean 0.210  null max 0.518  excess -0.002  -
          within-study    share 0.003  null mean 0.001  null max 0.003  excess +0.002  -
        Year     groups   20
          between-study   share 0.116  null mean 0.177  null max 0.518  excess -0.061  -
          within-study    nested in Author (constant inside every study)
        Species  groups  487
          between-study   share 0.702  null mean 0.820  null max 0.957  excess -0.118  -
          within-study    share 0.289  null mean 0.113  null max 0.145  excess +0.177  FLAG
        Family   groups   72
          between-study   share 0.076  null mean 0.214  null max 0.514  excess -0.138  -
          within-study    share 0.053  null mean 0.016  null max 0.043  excess +0.037  FLAG
      MISSING COLUMN candidates: Author (lab), Species (within_study), Family (within_study)

    holdout (> 2018): 2262 rows, 47 studies, tau2 0.1380
      column                 share alone   slope      rows
      Experimental.setting     0.0012     -0.0378   2262
      Phase2.time              0.0000     -0.0001   2262
      Approach                 0.0017     +0.0686   2262
      Phase1.culti             0.0060     -0.0895   2262
      SoilTp                   0.0022     -0.0429   2262
      Life.form                0.0032     +0.0731   2262
      F.H                      0.0018     -0.0402   2262
      Sp.origin                0.0090     -0.1385   2262
      MAT                      0.0031     +0.0048   2262
      MAP                      0.0024     +0.0000   2262
      AI                       0.0015     +0.0406   2262
      Latitude.abs             0.0024     -0.0019   2262
      all 12 columns together: share 0.0237, left 0.9763 (2262 complete rows)
      grouping patterns on what is left:
        Author   groups   47
          lab             share 0.110  null mean 0.019  null max 0.042  excess +0.091  FLAG
        region   groups   18
          between-study   share 0.530  null mean 0.350  null max 0.762  excess +0.180  -
          within-study    share 0.003  null mean 0.001  null max 0.004  excess +0.001  -
        Year     groups    4
          between-study   share 0.012  null mean 0.051  null max 0.457  excess -0.039  -
          within-study    nested in Author (constant inside every study)
        Species  groups  295
          between-study   share 0.864  null mean 0.956  null max 1.000  excess -0.092  -
          within-study    share 0.270  null mean 0.132  null max 0.170  excess +0.138  FLAG
        Family   groups   57
          between-study   share 0.441  null mean 0.296  null max 0.748  excess +0.145  -
          within-study    share 0.082  null mean 0.024  null max 0.042  excess +0.058  FLAG
      MISSING COLUMN candidates: Author (lab), Species (within_study), Family (within_study)

    pooled: 5969 rows, 202 studies, tau2 0.1844
      column                 share alone   slope      rows
      Experimental.setting     0.0003     -0.0311   5969
      Phase2.time              0.0003     +0.0017   5963
      Approach                 0.0000     -0.0023   5969
      Phase1.culti             0.0111     -0.1458   5969
      SoilTp                   0.0036     -0.0679   5969
      Life.form                0.0033     +0.0890   5969
      F.H                      0.0035     -0.0697   5969
      Sp.origin                0.0018     +0.0638   5969
      MAT                      0.0004     +0.0025   5969
      MAP                      0.0002     -0.0000   5969
      AI                       0.0062     -0.1097   5969
      Latitude.abs             0.0103     -0.0058   5969
      all 12 columns together: share 0.0393, left 0.9607 (5963 complete rows)
      grouping patterns on what is left:
        Author   groups  201
          lab             share 0.219  null mean 0.033  null max 0.050  excess +0.186  FLAG
        region   groups   33
          between-study   share 0.240  null mean 0.174  null max 0.449  excess +0.066  -
          within-study    share 0.002  null mean 0.001  null max 0.003  excess +0.002  -
        Year     groups   24
          between-study   share 0.094  null mean 0.146  null max 0.385  excess -0.052  -
          within-study    nested in Author (constant inside every study)
        Species  groups  667
          between-study   share 0.706  null mean 0.792  null max 0.939  excess -0.086  -
          within-study    share 0.266  null mean 0.099  null max 0.125  excess +0.167  FLAG
        Family   groups   85
          between-study   share 0.069  null mean 0.191  null max 0.515  excess -0.122  -
          within-study    share 0.049  null mean 0.012  null max 0.024  excess +0.036  FLAG
      MISSING COLUMN candidates: Author (lab), Species (within_study), Family (within_study)

[DERIVED] Reading of the column tables:

    all 12 recorded columns together explain about 0.06 of the spread on
    the anchor side, 0.02 on the holdout side and 0.04 pooled. Between
    0.94 and 0.98 of the spread is left.

    no single column explains more than about 0.02 on either side. The
    two largest on the anchor side (AI, Latitude.abs, about 0.02 each)
    are near 0.002 on the holdout side.

    the slope on AI and on Sp.origin has opposite signs on the two
    sides, as Phase C already recorded.

## 4. Same candidates on both sides?

    same candidates on both sides?
      Author   anchor lab                          holdout lab                          both
      region   anchor -                            holdout -                            neither
      Year     anchor -                            holdout -                            neither
      Species  anchor within_study                 holdout within_study                 both
      Family   anchor within_study                 holdout within_study                 both

    candidate shapes (pooled):
      clusters by Author; tests lab; 201 groups; excess lab +0.186
          expiry_condition: a per-study methods table joined on Author: soil source and storage, sterilisation method, pot volume, inoculum fraction, watering and light regime
      clusters by Species; tests within_study; 667 groups; excess within_study +0.167
          largest group mean residual: Sporobolus neglectus   +0.588 (49 rows)
          largest group mean residual: Plantago rugelii       +0.449 (50 rows)
          largest group mean residual: Amorpha canescens      +0.429 (30 rows)
          expiry_condition: species traits joined on Species: mycorrhizal type, N-fixing status, growth rate, seed mass
      clusters by Family; tests within_study; 85 groups; excess within_study +0.036
          largest group mean residual: Pinaceae               +0.271 (52 rows)
          largest group mean residual: Anacardiaceae          -0.249 (25 rows)
          largest group mean residual: Hypericaceae           -0.247 (23 rows)
          expiry_condition: lineage traits joined on Family: mycorrhizal type, N-fixing status, a phylogeny for the sampled families

The "largest group mean residual" lines are row-level means of the
all-columns residual for groups with at least 20 rows. They show the
shape; they are not the within-study quantity the flag was computed on.

## 5. Candidates

Three groupings were flagged, the same three on the anchor side, the
holdout side and pooled. All readings DERIVED; all next steps PROPOSED.

    1  Author (lab)
       shape      studies differ from each other by more than row noise
                  allows: lab share 0.25 anchor, 0.11 holdout, against a
                  null near 0.02 to 0.04
       clusters   by study
       caveat     between-study spread is the ordinary state of a
                  meta-analysis. This flag says the 12 columns do not
                  account for it; it does not say what does.
       expiry     a per-study methods table joined on Author: soil source
                  and storage, sterilisation method, pot volume, inoculum
                  fraction, watering and light regime

    2  Species (within study)
       shape      inside one study, rows of the same species sit
                  together: within-study share 0.29 anchor, 0.27 holdout,
                  against a null near 0.11 to 0.13
       clusters   by species, inside studies
       caveat     Sp.origin and Life.form are species-level columns and
                  are already in the fit; this is what is left after them.
       expiry     species traits joined on Species: mycorrhizal type,
                  N-fixing status, growth rate, seed mass

    3  Family (within study)
       shape      weaker version of 2: within-study share 0.05 anchor,
                  0.08 holdout, against a null near 0.02
       clusters   by family, inside studies
       caveat     NOT independent of 2. Every species has one family, so
                  a species pattern produces a family pattern by nesting.
                  Whether family adds anything beyond species was not
                  tested: NOT RECORDED.
       expiry     lineage traits joined on Family: mycorrhizal type,
                  N-fixing status, a phylogeny for the sampled families

Not flagged on either side: region (between or within study) and Year
(between study). Year cannot be read within a study. On the holdout side
region between-study had excess +0.180 and Family between-study +0.145
without clearing the null maximum; with 47 studies that test has little
reach, so "not flagged" there is weak. [DERIVED]

## 6. Limits

    exploratory     the holdout is spent; agreement between the two sides
                    here is not a replication test, and nobody
                    pre-stated these candidates
    one fit         residuals come from one linear all-columns fit with
                    no interactions; a grouping can flag because a
                    recorded column acts non-linearly, not because a
                    column is missing
    nesting         Species sits inside Family; region and Year sit
                    mostly inside Author. Only the nulls separate them.
    thresholds      hand-set, checked on one synthetic design, 5 seeds
    not registered  the tool has no ledger/toolkit yaml entry, is not in
                    tests/test_toolkit.py and has no held-out gate; its
                    gate is its own --gate. Trust: PROPOSED.
    holdout rows    not committed; the run rebuilds them from the source

## Provenance

Co-authored, Kavik + Claude, work order of 2026-11-22 (END marker
present). Base branch: claude/forest-holdout-phase-c (PR #332). Code:
`ledger/toolkit/missing_column_finder.py`, which imports `_wls` and
`dummy` from `holdout/phase_b.py` unchanged; the intercept-only
variance, the all-columns fit and the grouping tests are new in it.
Source data: Zenodo record 10403125, sha256 asserted, not committed.
The readings in sections 3 to 5 are this run's.
