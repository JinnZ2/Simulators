<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# Next steps after the Approach strata: B1 climate coverage, mycorrhizal-type join

CC0. Exploratory. Nothing here is a test and nothing here is scored.

Status: EXPLORATORY. Co-authored, Kavik + Claude, work order of
2026-11-23 (END marker present; the order is marked PROPOSED). Run date
(UTC): 2026-11-23. Observer slots: null.

"Holdout spent at Phase C; this is exploratory and scores nothing."

Tags: DERIVED = computed in this run from the data and the stated
choices; OBSERVED = seen in this run (hashes, fetch results);
PROPOSED = a reading or a next step, untested; NOT RECORDED = nobody in
this run looked, or the source could not be read.

Every number in the indented blocks of section 1 was printed by
`python3 holdout/explore_next_steps.py coverage SOURCE_CSV` and pasted by
script, as were the blocks of sections 1b and 1c by their own commands.
None was typed.

## 1. B1 climate coverage (ranges only, no refit)

AI and MAP, anchor (Year <= 2018) against holdout, pooled and inside each
Approach. A study with both approaches counts in both strata. Quantiles
are over rows. The mark rule and its two constants are hand-set and were
written into the script before the table was seen. [OBSERVED]

    B1 CLIMATE COVERAGE: ranges only, no refit; spent holdout, scores nothing
      row-level quantiles; MAP in mm; mark rule: narrower = holdout width < 0.8 x anchor width,
      shifted = more than 10% of holdout rows outside the anchor min-max
      AI
        stratum          side     studies  rows       min        q1       med        q3       max       p10       p90
        pooled           anchor       155  3707    0.0494    0.6076    0.9477    1.0948    3.6840    0.2622    1.1708
                         holdout       47  2262    0.1163    0.5570    0.5570    0.7142    4.5728    0.3059    1.0802
        Self-Other       anchor       133  3198    0.1043    0.6317    0.9477    1.0948    3.6840    0.3094    1.1708
                         holdout       42  2105    0.1163    0.5570    0.5570    0.7142    4.5728    0.3059    1.0802
        Self-Sterilized  anchor        65   509    0.0494    0.5575    0.7594    1.0800    2.3275    0.2382    1.1708
                         holdout       23   157    0.1163    0.6151    0.7791    0.9324    3.5511    0.3307    1.1575
        stratum          overlap of ranges        share of     share of     holdout/anchor   holdout rows outside
                         (min-max)                anchor rng   holdout rng  width            the anchor min-max
        pooled           [0.1163, 3.6840]          0.982        0.801        1.226               6 of  2262 = 0.0027
        Self-Other       [0.1163, 3.6840]          0.997        0.801        1.245               6 of  2105 = 0.0029
        Self-Sterilized  [0.1163, 2.3275]          0.971        0.644        1.508               2 of   157 = 0.0127
        most common single value (rows are not spread evenly over studies):
          pooled           anchor   0.9477  on 0.110 of rows
          pooled           holdout  0.5570  on 0.354 of rows
          Self-Other       anchor   0.9477  on 0.124 of rows
          Self-Other       holdout  0.5570  on 0.380 of rows
          Self-Sterilized  anchor   1.1708  on 0.094 of rows
          Self-Sterilized  holdout  0.7791  on 0.204 of rows
      MAP
        stratum          side     studies  rows       min        q1       med        q3       max       p10       p90
        pooled           anchor       155  3707      50.0     598.0     835.0     926.0    3500.0     391.0    1080.0
                         holdout       47  2262     235.0     502.0     507.0     788.1    3753.0     475.0    1600.0
        Self-Other       anchor       133  3198     157.7     598.0     847.0     862.0    3500.0     390.0    1072.8
                         holdout       42  2105     235.0     502.0     502.0     788.1    3084.0     475.0    1691.0
        Self-Sterilized  anchor        65   509      50.0     585.0     805.0    1051.0    2939.0     479.0    1209.0
                         holdout       23   157     235.0     731.9     826.0    1265.0    3753.0     475.0    1600.0
        stratum          overlap of ranges        share of     share of     holdout/anchor   holdout rows outside
                         (min-max)                anchor rng   holdout rng  width            the anchor min-max
        pooled           [235.0, 3500.0]           0.946        0.928        1.020               2 of  2262 = 0.0009
        Self-Other       [235.0, 3084.0]           0.852        1.000        0.852               0 of  2105 = 0.0000
        Self-Sterilized  [235.0, 2939.0]           0.936        0.769        1.218               2 of   157 = 0.0127
        most common single value (rows are not spread evenly over studies):
          pooled           anchor   849.0  on 0.110 of rows
          pooled           holdout  502.0  on 0.354 of rows
          Self-Other       anchor   849.0  on 0.124 of rows
          Self-Other       holdout  502.0  on 0.380 of rows
          Self-Sterilized  anchor   1062.0  on 0.094 of rows
          Self-Sterilized  holdout  826.0  on 0.204 of rows
      READ (DERIVED), by the rule above
        B1 AI  pooled           flip within a shared range
        B1 AI  Self-Other       flip within a shared range
        B1 AI  Self-Sterilized  flip within a shared range
        B1 MAP pooled           flip within a shared range
        B1 MAP Self-Other       flip within a shared range
        B1 MAP Self-Sterilized  flip within a shared range
      beside the mark, not part of it: the same two tests on the central band (p10-p90)
        col  stratum          holdout/anchor width   holdout rows outside anchor p10-p90   narrower  shifted
        AI   pooled              0.852                 0.0858                              no        no
        AI   Self-Other          0.899                 0.1981                              no        yes
        AI   Self-Sterilized     0.887                 0.1210                              no        yes
        MAP  pooled              1.633                 0.1490                              no        yes
        MAP  Self-Other          1.781                 0.1344                              no        yes
        MAP  Self-Sterilized     1.541                 0.4076                              no        yes

[DERIVED] Reading.

    mark        all six cells read "flip within a shared range". The
                holdout min-max range is not narrower than the anchor's
                by the rule, and at most 1.3% of holdout rows lie
                outside the anchor min-max. By the order's rule the B1
                flip is not marked as extrapolation.
    beside it   the min-max range is set by a few extreme rows on both
                sides. Inside the range the holdout rows sit elsewhere:
                the pooled holdout median AI is 0.557 against the
                anchor's 0.948, and one AI value (0.5570, MAP 502)
                carries 35% of all holdout rows and 38% of the
                Self-Other holdout rows. On the central band (anchor
                10th to 90th percentile) five of six cells read
                "shifted". These lines do not change the mark; the rule
                was fixed first and is kept.
    scope       ranges and row counts only. Nothing here says why the
                slope differs, and a shared range does not make the flip
                a reversal: every holdout B1 interval in section 12 of
                EXPLORE_DENOMINATOR_GROUPS.md includes zero.
    unresolved  whether the B1 holdout slope is carried by the one
                heavily sampled site. A leave-one-study-out refit would
                show it; the order asked for ranges only, so it was not
                run.
                [added 2026-11-23, follow-up order] It was then run:
                section 1b. The answer is no.

## 1b. Leave-one-study-out, holdout B1 (follow-up order of 2026-11-23)

Each holdout study removed in turn and the B1 fit rerun, pooled and
inside each Approach. The fit is `phase_b.fit` called through
`phase_c.FITS`, imported and unchanged. The mark rule was written into
the script before the table was seen. Printed by
`python3 holdout/explore_next_steps.py loso SOURCE_CSV`, pasted by script.

    LEAVE-ONE-STUDY-OUT, holdout B1: phase_b.fit (imported, unchanged); spent holdout, scores nothing
      dominant site: AI 0.557, MAP 502; 800 of 2262 holdout rows; studies with rows there: Dostal et al. 2021 (800 rows)
      id      stratum          anchor     holdout    LOSO slope range        signs   site removed                 studies  rows   mark
                               slope      slope      min        max        -  +    slope [80% interval]
      B1 AI   pooled            -0.2378    +0.0407    +0.0158    +0.0559    0 47    +0.0377 [ -0.0115,  +0.0865]     46   1462   flip not carried by that site
      B1 AI   Self-Other        -0.1497    +0.0406    +0.0089    +0.0583    0 42    +0.0416 [ -0.0067,  +0.0909]     41   1305   flip not carried by that site
      B1 AI   Self-Sterilized   -0.6103    +0.0188    -0.1530    +0.0602    4 19    +0.0188 [ -0.3317,  +0.1337]     23    157   flip not carried by that site
      B1 MAP  pooled            -0.1164    +0.0373    +0.0206    +0.0445    0 47    +0.0349 [ -0.0057,  +0.0623]     46   1462   flip not carried by that site
      B1 MAP  Self-Other        -0.0672    +0.0344    +0.0048    +0.0424    0 42    +0.0344 [ -0.0180,  +0.0621]     41   1305   flip not carried by that site
      B1 MAP  Self-Sterilized   -0.3222    +0.0445    -0.0147    +0.0802    2 21    +0.0445 [ -0.1275,  +0.1613]     23    157   flip not carried by that site
      the single removals that move the slope most:
        B1 AI  pooled           lowest  +0.0158 without Segnitz et al. 2020 (71 rows); highest  +0.0559 without Forero et al. 2019 (518 rows)
        B1 AI  Self-Other       lowest  +0.0089 without Segnitz et al. 2020 (71 rows); highest  +0.0583 without Forero et al. 2019 (518 rows)
        B1 AI  Self-Sterilized  lowest  -0.1530 without Nuske et al. 2021 (10 rows); highest  +0.0602 without Uddin et al. 2021 (2 rows)
        B1 MAP pooled           lowest  +0.0206 without Segnitz et al. 2020 (71 rows); highest  +0.0445 without Forero et al. 2019 (518 rows)
        B1 MAP Self-Other       lowest  +0.0048 without Segnitz et al. 2020 (71 rows); highest  +0.0424 without Forero et al. 2019 (518 rows)
        B1 MAP Self-Sterilized  lowest  -0.0147 without Nuske et al. 2021 (10 rows); highest  +0.0802 without Stein et al. 2020 (32 rows)

[DERIVED] Reading.

    mark        "flip not carried by that site" in all six cells. The
                dominant site is one study (Dostal et al. 2021, 800
                rows). With it removed the pooled and Self-Other slopes
                stay positive and move by less than 0.004. It has no
                Self-Sterilized rows, so that stratum's fit is the same
                with and without it.
    range       pooled and Self-Other: the slope is positive under every
                single removal (47 of 47 and 42 of 42). No one study
                carries the sign.
                Self-Sterilized: the sign depends on single studies.
                Removing Nuske et al. 2021 (10 rows) takes the AI slope
                from +0.019 to -0.153; 4 of 23 removals give a negative
                AI slope and 2 of 23 a negative MAP slope.
    scope       point estimates. Every interval printed above includes
                zero, as did the full holdout fits. Removing one study
                at a time does not test two or more acting together.

## 1c. Largest single study's share of rows, beside every fit

The order asks for this beside every fit already in this record. This
record holds no fit of its own apart from section 1b; the fits it reads
are the six Phase B fits, so the share is given for each of those, per
side and stratum. Printed by
`python3 holdout/explore_next_steps.py share SOURCE_CSV`, pasted by
script.

    LARGEST SINGLE STUDY'S SHARE OF ROWS beside each Phase B fit (rows the fit can use); counts only
      id      stratum          anchor: share  rows   studies     holdout: share  rows   studies
      B1 AI   pooled                  0.110   3707     155              0.354   2262      47
      B1 AI   Self-Other              0.124   3198     133              0.380   2105      42
      B1 AI   Self-Sterilized         0.147    509      65              0.204    157      23
      B1 MAP  pooled                  0.110   3707     155              0.354   2262      47
      B1 MAP  Self-Other              0.124   3198     133              0.380   2105      42
      B1 MAP  Self-Sterilized         0.147    509      65              0.204    157      23
      B2      pooled                  0.110   3701     154              0.354   2262      47
      B2      Self-Other              0.124   3192     132              0.380   2105      42
      B2      Self-Sterilized         0.147    509      65              0.204    157      23
      B3      pooled                  0.110   3707     155              0.354   2262      47
      B3      Self-Other              0.124   3198     133              0.380   2105      42
      B3      Self-Sterilized         0.147    509      65              0.204    157      23
      B4      pooled                  0.110   3707     155              0.354   2262      47
      B4      Self-Other              0.124   3198     133              0.380   2105      42
      B4      Self-Sterilized         0.147    509      65              0.204    157      23
      R5      pooled                  0.110   3707     155              0.354   2262      47
      R5      Self-Other              0.124   3198     133              0.380   2105      42
      R5      Self-Sterilized         0.147    509      65              0.204    157      23

[DERIVED] The share is the same for all six fits inside a cell because
the same rows enter each (B2 drops 6 anchor rows with no Phase2.time).
The largest holdout study carries 35% of holdout rows (38% inside
Self-Other); the largest anchor study carries 11% (12%). Rows are not
the fit's weights: the bootstrap resamples studies, so a large study
moves the point estimate more than it narrows the interval.

## 2. Mycorrhizal-type join: STOPPED, nothing joined

The FungalRoot database could not be fetched, so item 2 stopped at its
first step, as the order says. No type was filled from recall. The B4
rerun with myc_type and the Species test with myc_type were not run.

[OBSERVED] Fetch log, 2026-11-23 UTC.

    16:42:00Z  https://api.gbif.org/v1/dataset/search?q=FungalRoot
               refused: the environment proxy answered 403 to CONNECT
    16:42:07Z  https://zenodo.org/api/records?q=FungalRoot   answered
               4 hits (records 5006671, 19061124, 10643546, 23174799);
               none is the FungalRoot database
    16:42:07Z  www.gbif.org, plutof.ut.ee, nph.onlinelibrary.wiley.com,
               api.crossref.org: no connection through the proxy
    16:42:18Z  https://datadryad.org/api/v2/search?q=FungalRoot  answered
               0 datasets
    16:42:18Z  https://doi.org/10.15468/a7ujmj   answered 302 to
               https://www.gbif.org/dataset/744edc21-8dd2-474e-8a0b-b8c3d56a3c2d
               the DOI came from model knowledge; that it resolves to a
               GBIF dataset page is observed; the page itself could not
               be read, so the record is NOT verified

    record verified    no
    file, bytes, sha256    NOT RECORDED (nothing fetched)
    match rate, anchor     NOT RECORDED
    match rate, holdout    NOT RECORDED
    B4 with myc_type, per Approach            NOT RECORDED (not run)
    Species share with myc_type added         NOT RECORDED (not run)

[PROPOSED] What would unblock it: gbif.org and api.gbif.org reachable
from the environment, or the FungalRoot occurrence file and the paper's
genus-level table supplied as files with their source URLs. The join
rule in the order (Species, then Genus, level tagged, unmatched kept as
NOT RECORDED) is unchanged and unbuilt.

## 3. Design doc

Item 3 is `holdout/HOLDOUT_NEXT_DESIGN.md`. It seals nothing and runs no
fit.

## Provenance

Base branch: claude/denominator-sorter (PR #334) at commit c0a7d77.
Code: `holdout/explore_next_steps.py` (standard library only).
Source data: Zenodo record 10403125, file PSF.data.EL.open.csv, fetched
2026-11-23T16:41:49Z from
https://zenodo.org/api/records/10403125/files/PSF.data.EL.open.csv/content,
1609518 bytes, sha256
bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c
(asserted by the script; not committed). anchor_studies.csv sha256
e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438,
asserted. The readings in section 1 are this run's.
