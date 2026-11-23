<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# HOLDOUT_NEXT_DESIGN -- design for the next sealed holdout

CC0. Design only. Nothing is sealed, no source is chosen, no fit is run.

Status: PROPOSED. Co-authored, Kavik + Claude, work order of 2026-11-23.
Date (UTC): 2026-11-23. Observer slots: null.

Tags: PROPOSED = a rule or a next step, untested; DERIVED = arithmetic
done here on numbers already on record; OBSERVED = seen in this run;
NOT RECORDED = nobody in this run looked.

## 1. Rules carried from the spent run

    R1  unit        the unit is the arm (study x arm): one Author value
                    with one denominator signature, as arm_units() in
                    ledger/toolkit/denominator_sorter.py builds it. The
                    unit list is fixed and hashed before the seal. Rows
                    are never the unit.
    R2  strata      every prediction, fit and score is made inside one
                    Approach (Self-Other, Self-Sterilized). rr is never
                    pooled across control types. A prediction names its
                    stratum in its id.
    R3  power gate  before any seal: for each prediction, the expected
                    holdout interval half-width is the anchor half-width
                    scaled by sqrt(anchor n / holdout n), n in the units
                    of R1. If that interval, centred on the anchor
                    estimate, cannot exclude zero, the prediction is
                    marked UNDERPOWERED in the sealed file before
                    anything is run. It may still be sealed; it may not
                    be read as a hit or a miss.
    R4  reading     a holdout direction is read only when the holdout
                    80% interval excludes zero; otherwise INDETERMINATE,
                    neither hit nor miss. MODEL and FIT are separate
                    columns, as in Phase C: MODEL tests the run_9
                    mechanism, FIT tests the anchor moderator fit. A
                    direction that holds by construction is reported and
                    not counted.
    R5  read set    the read-set rule covers holdout contact only: no
                    session that predicts may read holdout rows, files
                    derived from them, or call the hosts that serve
                    them. Repository files that hold no holdout data are
                    outside the rule. (Phase B lesson: two harmless
                    reads had to be logged as possible exposure because
                    the rule was written over every file.)
    R6  slots       the 8 empty slots are carried on every unit and
                    filled where the new source allows, else NOT
                    RECORDED, never imputed:
                    lab_institution, lab_country, governance_regime,
                    instrument_manufacturer, instrument_model,
                    calibration_date, measurement_method,
                    coordinate_meaning.

Carried unchanged and not restated here: salted commitment of the
holdout bytes before any branch exists, salted commitment of the
predictions before reveal, every predicted number from code.

[PROPOSED] Two additions from this run's item 1, for Kavik to accept or
drop: (a) a coverage table (moderator ranges, anchor against holdout,
per stratum) is computed at reveal before any slope is read; (b) the
share of holdout rows carried by the single largest study is reported
beside every fit.

## 2. The power gate applied to what is on record (DERIVED)

Arithmetic only, on the anchor estimates and intervals printed in section
12 of EXPLORE_DENOMINATOR_GROUPS.md. Printed by
`python3 holdout/explore_next_steps.py power` and pasted by script; no
fit was run and no data file was opened. The n here is studies, because
that table counts studies; R1 asks for arms, and the arm-level anchor
intervals do not exist yet.

    POWER GATE ARITHMETIC: anchor 80% interval scaled to a holdout n; no fit run, no data opened
      source: the section 12 table in EXPLORE_DENOMINATOR_GROUPS.md, as printed (4 decimals)
      expected half-width at n studies = anchor half-width * sqrt(anchor studies / n)
      studies needed = anchor studies * (anchor half-width / |anchor estimate|)^2, rounded up
      PASS = the expected interval, centred on the anchor estimate, excludes zero
      id      stratum          anchor est  half-width  anchor st   studies   spent holdout:
                                                                   needed    st   exp. half-width  gate
      B1 AI   Self-Other         -0.1497     0.1068       133        68     42     0.1900         FAIL
      B1 AI   Self-Sterilized    -0.6103     0.2772        65        14     23     0.4661         PASS
      B1 MAP  Self-Other         -0.0672     0.0940       133       261     42     0.1674         FAIL
      B1 MAP  Self-Sterilized    -0.3222     0.3073        65        60     23     0.5166         FAIL
      B2      Self-Other         +0.0026     0.0047       132       432     42     0.0083         FAIL
      B2      Self-Sterilized    -0.0093     0.0353        65       937     23     0.0593         FAIL
      B3      Self-Other         -0.0183     0.1253       133      6236     42     0.2230         FAIL
      B3      Self-Sterilized  not checkable on the anchor side (no interval printed)
      B4      Self-Other         +0.0696     0.0834       133       192     42     0.1485         FAIL
      B4      Self-Sterilized    +0.2989     0.2994        65        66     23     0.5034         FAIL
      R5      Self-Other         +0.0721     0.0804       133       166     42     0.1430         FAIL
      R5      Self-Sterilized    +0.4764     0.3249        65        31     23     0.5461         FAIL

[DERIVED] Reading. At the spent holdout's size, 10 of the 11 checkable
cells fail the gate. Had the gate existed, the Phase C result (every
direction INDETERMINATE) was the expected one for those cells. The one
PASS, B1 AI inside Self-Sterilized, rests on an anchor slope of -0.61;
the holdout slope there was +0.02 with an interval including zero.
"Studies needed" assumes the holdout effect equals the anchor effect and
the same spread per study; both are assumptions, and the first failed
for B1.

    scope       80% intervals, studies as n, square-root scaling. A
                stratum whose moderator has no variation on the anchor
                side (B3 inside Self-Sterilized) has no gate value.

## 3. Candidate sources (listed; none picked)

    S1  PSF studies published after 2022
        expected n        NOT RECORDED as a count. Base rate only: the
                          current source holds the studies-per-year
                          figures below.
        Approach mix      NOT RECORDED for the new studies; recent years
                          of the current source are below.
        setting mix       NOT RECORDED for the new studies; same.
        note              a study list has to be assembled by search;
                          no search was run here.

    S2  the Karst et al. 2023 field studies
        expected n        NOT RECORDED
        Approach mix      NOT RECORDED
        setting mix       NOT RECORDED
        note              the paper was not fetched or read in this run.
                          [PROPOSED, from model knowledge, not verified]
                          it reviews field evidence on common
                          mycorrhizal networks; whether its studies
                          report a plant-soil feedback log ratio with a
                          control-soil type at all has to be checked
                          before S2 is a candidate under R2.

Base rate for S1, from the current source. Printed by
`python3 holdout/explore_next_steps.py rate SOURCE_CSV`, pasted by
script.

    PUBLICATION RATE in the source (studies = distinct Author values)
      year   studies   rows   Self-Other st   Self-Sterilized st   Greenhouse st   Field st
      2015        13    214              11                    6              13          0
      2016        16    439              15                    5              15          4
      2017        14    917              14                    5              13          1
      2018        24    787              21                    9              23          1
      2019        11    651               9                    7               8          4
      2020        17    468              16                    6              13          4
      2021        16   1079              15                    8              16          0
      2022         3     64               2                    2               3          1
      last year in the source: 2022 (3 studies; read as a partial year)
      full years 2017-2021: 11 to 24 studies per year, median 16.0

[DERIVED] Reading. If post-2022 publication ran at the 2017-2021 rate,
a three-year window would hold some tens of studies, most with a
Self-Other arm and under half with a Self-Sterilized arm. Against
section 2, that clears the gate for few cells. This is a rate from one
database's inclusion rule, not a count of what exists.

## 4. Open before any seal

    - which source (Kavik picks; none is picked here)
    - arm-level anchor intervals inside each Approach, so R3 can run in
      the units of R1
    - whether UNDERPOWERED predictions are sealed or dropped
    - the mycorrhizal-type join (EXPLORE_NEXT_STEPS.md section 2,
      stopped: source not reachable)

## Provenance

Base branch: claude/denominator-sorter (PR #334) at commit c0a7d77.
Code: `holdout/explore_next_steps.py`, commands `power` and `rate`.
Rules R1-R6 are the work order's, restated; the two additions in section
1 and every reading are this run's. Source data for `rate`: Zenodo
record 10403125, sha256
bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c,
asserted, not committed.
