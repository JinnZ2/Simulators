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

[added 2026-11-23, follow-up order] Superseded by section 2b, where the
join ran. The text below is kept as written.

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

## 2b. Mycorrhizal-type join: retry after the host change (2026-11-23)

Section 2 is kept as written. The follow-up order had gbif.org and
api.gbif.org added to the environment's allowed hosts; the retry ran.

[OBSERVED] Record verified before use, 2026-11-23T18:13:16Z, from
https://api.gbif.org/v1/dataset/744edc21-8dd2-474e-8a0b-b8c3d56a3c2d :

    title      Taxon occurrence data for the FungalRoot database
    doi        10.15468/a7ujmj
    citation   Soudzilovskaia N A, Vaessen S, Barcelo M, He J, Rahimlou S,
               Abarenkov K, Brundrett M C, Gomes S, Merckx V, Martinez-Suz
               L, Tedersoo L. Taxon occurrence data for the FungalRoot
               database. PlutoF. Occurrence dataset
               https://doi.org/10.15468/a7ujmj accessed via GBIF.org on
               2026-11-23.
    license    CC BY-NC 4.0 (so the records are NOT committed here; this
               repository is CC0)
    records    36515

[OBSERVED] Fetch. The Darwin Core archive sits on orphans.gbif.org,
which the proxy still refuses (403 to CONNECT, 18:13:26Z). The records
were read through the occurrence API instead:

    URL        https://api.gbif.org/v1/occurrence/search?datasetKey=
               744edc21-8dd2-474e-8a0b-b8c3d56a3c2d&limit=L&offset=N
               (L 300 for offsets 0-10199, L 100 after)
    UTC        2026-11-23T18:13:56Z to 19:11Z
    file       fungalroot_occurrences_full.jsonl: one line per record in
               offset order, holding key, occurrenceID, scientificName,
               species, genus, family, taxonRank, taxonomicStatus,
               acceptedScientificName and the MeasurementOrFact pairs
               other than "Source". It is this run's extract, not the
               API's raw bytes, which were not kept.
    bytes      14523948
    sha256     430ab42cadb7412deeb7fa9f81ae8e0cb8f9c8c60bba23bc5c125b8834410980
    records    36515 lines, 36515 distinct keys

What this source is and is not: occurrence records, each a published
report of a mycorrhizal type on one taxon. It is not the paper's
genus-level table (the journal host is not reachable). A species type
here is this run's rule over that species' records; a genus type is the
same rule over all of the genus's records and is tagged "genus". The type
map and the taxon rule are in the script docstring. The map was written
after the first 10200 records' type values had been seen and before any
join; one further value turned up in the full file and is reported
uncounted. The 0.2 threshold was not varied. Five PSF "Species" values
are community mixes, not taxa; they read NOT RECORDED. No type was
filled from recall. [OBSERVED]

Printed by `python3 holdout/explore_next_steps.py myc SOURCE_CSV
FUNGALROOT_JSONL`, pasted by script.

    MYCORRHIZAL-TYPE JOIN: FungalRoot occurrence records; spent holdout, scores nothing
      source file: 36515 records, 14523948 bytes, sha256 asserted; species names with a counted type: 15547; genera: 4180
      source type values outside the declared map (not counted): AM-like (non-vascular plants) x22
      MATCH RATE (no fill: unmatched = NOT RECORDED, kept)
        side     unit      total   species-level   genus-level   NOT RECORDED   matched share
        anchor   rows       3707            2997           647             63   0.983
        anchor   species     489             357           111             21   0.957
        holdout  rows       2262            1829           388             45   0.980
        holdout  species     295             214            72              9   0.969
      TYPE COUNTS: rows / studies
        side     stratum          AM            ECM           AM+ECM        NM            OTHER         NOT RECORDED  
        anchor   pooled           3197 / 139    133 / 16      137 / 20      176 / 21      1 / 1         63 / 14       
        anchor   Self-Other       2812 / 118    94 / 14       92 / 19       142 / 20      1 / 1         57 / 12       
        anchor   Self-Sterilized  385 / 58      39 / 8        45 / 9        34 / 9        0 / 0         6 / 4         
        holdout  pooled           2020 / 43     111 / 10      34 / 6        52 / 10       0 / 0         45 / 5        
        holdout  Self-Other       1883 / 39     97 / 9        34 / 6        48 / 10       0 / 0         43 / 5        
        holdout  Self-Sterilized  137 / 21      14 / 2        0 / 0         4 / 3         0 / 0         2 / 1         
      LIFE FORM AGAINST TYPE: rows that are Woody / all rows of the type
        anchor   pooled           222 / 3197    133 / 133     136 / 137     44 / 176      0 / 1         10 / 63       
        holdout  pooled           135 / 2020    110 / 111     34 / 34       0 / 52        0 / 0         4 / 45        
      B4 RERUN: myc_type in place of Life.form; phase_b.fit unchanged; one contrast at a time
        cell = estimate [80% interval] studies rows ; thin = under 5 studies on either level
        Life.form Woody - Nonwoody (as sealed)
          Self-Other       anchor   +0.0696 [ -0.0162,  +0.1507] 133 st  3198 rows   level studies 38 / 99
                           holdout  +0.0301 [ -0.0755,  +0.0950]  42 st  2105 rows   level studies 16 / 31
          Self-Sterilized  anchor   +0.2989 [ +0.0157,  +0.6146]  65 st   509 rows   level studies 24 / 42
                           holdout  +0.3275 [ +0.1657,  +0.5363]  23 st   157 rows   level studies 9 / 17
        ECM - AM
          Self-Other       anchor   +0.3793 [ +0.2445,  +0.4669] 124 st  2906 rows   level studies 14 / 118
                           holdout  +0.1219 [ +0.0537,  +0.2016]  41 st  1980 rows   level studies 9 / 39
          Self-Sterilized  anchor   +0.3213 [ +0.0392,  +0.6359]  62 st   424 rows   level studies 8 / 58
                           holdout  +0.3146 [ -0.3369,  +0.4966]  23 st   151 rows   level studies 2 / 21  thin
        AM+ECM - AM
          Self-Other       anchor   +0.0288 [ -0.0790,  +0.1264] 122 st  2904 rows   level studies 19 / 118
                           holdout  +0.1815 [ +0.1157,  +0.3037]  40 st  1917 rows   level studies 6 / 39
          Self-Sterilized  anchor   +0.2479 [ -0.0163,  +0.5234]  60 st   430 rows   level studies 9 / 58
                           holdout not checkable (one level absent: 0 / 21 studies)
        NM - AM
          Self-Other       anchor   -0.0067 [ -0.1630,  +0.1085] 122 st  2954 rows   level studies 20 / 118
                           holdout  -0.5324 [ -0.8587,  -0.2031]  39 st  1931 rows   level studies 10 / 39
          Self-Sterilized  anchor   +0.1417 [ -0.1945,  +0.3031]  60 st   419 rows   level studies 9 / 58
                           holdout  -0.3797 [ -0.7066,  -0.0646]  21 st   141 rows   level studies 3 / 21  thin
        any ECM - AM
          Self-Other       anchor   +0.1927 [ +0.0735,  +0.2841] 126 st  2998 rows   level studies 27 / 118
                           holdout  +0.1377 [ +0.0793,  +0.2089]  41 st  2014 rows   level studies 10 / 39
          Self-Sterilized  anchor   +0.2809 [ +0.0264,  +0.5187]  63 st   469 rows   level studies 14 / 58
                           holdout  +0.3146 [ -0.3369,  +0.4966]  23 st   151 rows   level studies 2 / 21  thin
      SPECIES TEST: missing_column_finder.analyse (unchanged), before and after 5 myc columns are added
        share = Species share of the spread left after the columns ; excess = share minus null mean
        stratum          side     columns   left     between-study: share  excess  flag   within-study: share  excess  flag
        Self-Other       anchor   11 bef    0.9566                   0.854  -0.023  -             0.346  +0.226  FLAG        
                                  16 aft    0.9418                   0.856  -0.021  -             0.339  +0.227  FLAG        
                         holdout  11 bef    0.9673                   0.773  -0.201  -             0.309  +0.161  FLAG        
                                  15 aft    0.9230                   0.774  -0.200  -             0.275  +0.124  FLAG        
                         pooled   11 bef    0.9731                   0.813  -0.023  -             0.314  +0.205  FLAG        
                                  16 aft    0.9589                   0.815  -0.021  -             0.303  +0.198  FLAG        
        Self-Sterilized  anchor   10 bef    0.8507                   0.611  -0.205  -             0.583  +0.146  FLAG        
                                  14 aft    0.8453                   0.600  -0.215  -             0.586  +0.152  FLAG        
                         holdout  11 bef    0.7233                   0.997  +0.054  -             0.334  +0.093  -           
                                  14 aft    0.7002                   0.997  +0.053  -             0.346  +0.098  -           
                         pooled   11 bef    0.8700                   0.635  -0.205  -             0.541  +0.134  -           
                                  15 aft    0.8664                   0.633  -0.207  -             0.543  +0.138  -           
      DOES THE SPECIES SHARE DROP? (after minus before; read on excess against the finder's own MIN_EXCESS, 0.02)
        stratum          side     test            share     excess    reading
        Self-Other       anchor   between_study   +0.0019   +0.0023  no change (under 0.02)
        Self-Other       anchor   within_study    -0.0065   +0.0015  no change (under 0.02)
        Self-Other       holdout  between_study   +0.0001   +0.0001  no change (under 0.02)
        Self-Other       holdout  within_study    -0.0342   -0.0367  drops
        Self-Other       pooled   between_study   +0.0018   +0.0018  no change (under 0.02)
        Self-Other       pooled   within_study    -0.0103   -0.0071  no change (under 0.02)
        Self-Sterilized  anchor   between_study   -0.0101   -0.0098  no change (under 0.02)
        Self-Sterilized  anchor   within_study    +0.0034   +0.0059  no change (under 0.02)
        Self-Sterilized  holdout  between_study   -0.0008   -0.0009  no change (under 0.02)
        Self-Sterilized  holdout  within_study    +0.0121   +0.0049  no change (under 0.02)
        Self-Sterilized  pooled   between_study   -0.0019   -0.0020  no change (under 0.02)
        Self-Sterilized  pooled   within_study    +0.0018   +0.0038  no change (under 0.02)

[DERIVED] Reading.

    match       98% of rows on each side get a type (anchor 0.983,
                holdout 0.980); about four fifths of those at species
                level, the rest through the genus aggregate.
    spread      the type is lopsided: AM carries 86% of anchor rows and
                89% of holdout rows. ECM, AM+ECM and NM each sit on 6 to
                21 studies per side when pooled.
    B4          with ECM against AM in place of woody against nonwoody,
                Self-Other is positive on both sides with both intervals
                excluding zero (anchor +0.38, holdout +0.12); "any ECM"
                against AM likewise (+0.19, +0.14). The sealed Life.form
                contrast in the same stratum had both intervals across
                zero. Inside Self-Sterilized the holdout has 2 studies
                with an ECM species: thin, not read.
                NM against AM: near zero on the anchor side, negative on
                the holdout side in both strata (Self-Other -0.53,
                interval excluding zero). The two sides disagree.
                AM+ECM against AM: the sides differ in size in
                Self-Other (+0.03, +0.18).
    Species     adding the five myc columns leaves the Species share
                where it was. Between-study: no change in any of six
                cells. Within-study: one cell of six drops by more than
                0.02 (Self-Other holdout, excess +0.161 to +0.124) and
                stays flagged. Mycorrhizal type, as joined here, does
                not account for the Species clustering.
    scope       exploratory, after the holdout was spent; five contrasts
                by two strata by two sides with no correction. All but one
                ECM or AM+ECM row on each side is Woody (table above), so
                "ECM - AM" is not separated from life form here. Types come from records
                of mixed quality under one hand-set rule.

## 3. Design doc

Item 3 is `holdout/HOLDOUT_NEXT_DESIGN.md`. It seals nothing and runs no
fit.

## 4. Order 335-F2 (run 2026-11-24 UTC; exploratory, post-holdout, scores nothing)

Follow-up 2 on the mycorrhizal join of section 2b. Same source file, same
type map, same fit (`phase_b.fit`, imported and unchanged) and the same
cluster bootstrap. Thin here means under 3 studies on either level of a
contrast, as the order sets it (section 2b used 5). Printed by
`python3 holdout/explore_next_steps.py f2 SOURCE_CSV FUNGALROOT_JSONL`,
pasted by script. The script prints block 4 before block 3.

    ORDER 335-F2 on the FungalRoot join (36515 records); exploratory, post-holdout, scores nothing
      cell = estimate [80% interval] studies rows ; thin = under 3 studies on either level
      1 SEPARATION: ECM - AM inside Life.form == Woody only (all-rows cell beside it)
        Self-Other       anchor  woody only   +0.4228 [ +0.2391,  +0.5853]  33 st   252 rows   level studies 14 / 27
                                 all rows     +0.3793 [ +0.2445,  +0.4669] 124 st  2906 rows   level studies 14 / 118
                         holdout woody only   +0.1883 [ +0.0697,  +0.3698]  15 st   206 rows   level studies 8 / 13
                                 all rows     +0.1219 [ +0.0537,  +0.2016]  41 st  1980 rows   level studies 9 / 39
        Self-Sterilized  anchor  woody only   +0.0121 [ -0.2173,  +0.2066]  22 st   103 rows   level studies 8 / 18
                                 all rows     +0.3213 [ +0.0392,  +0.6359]  62 st   424 rows   level studies 8 / 58
                         holdout woody only   +0.0576 [ -0.5782,  +0.2688]   9 st    39 rows   level studies 2 / 7  thin
                                 all rows     +0.3146 [ -0.3369,  +0.4966]  23 st   151 rows   level studies 2 / 21  thin
      2 LEAVE-ONE-STUDY-OUT (each study in the contrast removed in turn)
        contrast   stratum          side     full est   min        max        drops  - / +   sign holds   largest-study row share
        ECM - AM   Self-Other       anchor    +0.3793    +0.2756    +0.4056   124    0 / 124  yes          0.120
        ECM - AM   Self-Other       holdout   +0.1219    +0.1040    +0.1615    41    0 / 41   yes          0.395
        NM - AM    Self-Other       anchor    -0.0067    -0.0448    +0.0705   122   117 / 5    no           0.134
        NM - AM    Self-Other       holdout   -0.5324    -0.6247    -0.2898    39   39 / 0    yes          0.414
        NM - AM    Self-Sterilized  anchor    +0.1417    -0.0624    +0.2091    60    1 / 59   no           0.179
        NM - AM    Self-Sterilized  holdout   -0.3797    -0.5728    -0.1708    21   21 / 0    yes          0.227
      4 FIT-RULE COLUMNS, Phase C definitions, holdout read against the ANCHOR fit (not sealed)
        direction: read only when the holdout 80% interval excludes zero, else INDETERMINATE
        interval_hit: holdout estimate inside the anchor interval ; overlap: the two intervals overlap
        contrast       stratum          anchor dir  holdout dir     direction       interval_hit  overlap
        ECM - AM       Self-Other       positive    positive        hit             no            no
        ECM - AM       Self-Sterilized  positive    INDETERMINATE   INDETERMINATE   yes           yes   thin
        AM+ECM - AM    Self-Other       positive    positive        hit             no            yes
        AM+ECM - AM    Self-Sterilized  not checkable on holdout
        NM - AM        Self-Other       negative    negative        hit             no            no
        NM - AM        Self-Sterilized  positive    negative        miss            no            yes
        any ECM - AM   Self-Other       positive    positive        hit             yes           yes
        any ECM - AM   Self-Sterilized  positive    INDETERMINATE   INDETERMINATE   yes           yes   thin
      3 THRESHOLD SWEEP: taxon rule at MYC_MIN 0.1 / 0.2 / 0.3 (0.2 is the rule used everywhere else)
        MYC_MIN 0.1
          side     rows: species  genus  NOT RECORDED    rows by type: AM  ECM  AM+ECM  NM  OTHER
          anchor           2997    647            63                  3160  119  191  173  1
          holdout          1829    388            45                  2010  56  117  34  0
          ECM - AM, Self-Other, anchor   +0.3563 [ +0.2383,  +0.4414] 121 st  2870 rows   level studies 12 / 116
          ECM - AM, Self-Other, holdout  +0.1288 [ +0.0402,  +0.2395]  40 st  1935 rows   level studies 8 / 37
        MYC_MIN 0.2
          side     rows: species  genus  NOT RECORDED    rows by type: AM  ECM  AM+ECM  NM  OTHER
          anchor           2997    647            63                  3197  133  137  176  1
          holdout          1829    388            45                  2020  111  34  52  0
          ECM - AM, Self-Other, anchor   +0.3793 [ +0.2445,  +0.4669] 124 st  2906 rows   level studies 14 / 118
          ECM - AM, Self-Other, holdout  +0.1219 [ +0.0537,  +0.2016]  41 st  1980 rows   level studies 9 / 39
        MYC_MIN 0.3
          side     rows: species  genus  NOT RECORDED    rows by type: AM  ECM  AM+ECM  NM  OTHER
          anchor           2997    647            63                  3201  140  109  193  1
          holdout          1829    388            45                  2003  113  23  78  0
          ECM - AM, Self-Other, anchor   +0.3814 [ +0.2453,  +0.4657] 124 st  2917 rows   level studies 15 / 118
          ECM - AM, Self-Other, holdout  +0.1266 [ +0.0605,  +0.2084]  41 st  1974 rows   level studies 9 / 40

[DERIVED] Reading.

    1 separation   inside Self-Other the ECM - AM difference is still
                   there among woody rows alone, on both sides, with
                   both intervals excluding zero (anchor +0.42, holdout
                   +0.19). In that stratum it is not life form under
                   another name.
                   inside Self-Sterilized it is not there among woody
                   rows (anchor +0.01, interval across zero); the
                   all-rows +0.32 in that stratum goes with life form.
                   The holdout cell there is thin (2 ECM studies).
    2 LOSO         ECM - AM, Self-Other: positive under every single
                   removal on both sides (124 of 124, 41 of 41).
                   NM - AM: the holdout sign holds under every removal
                   in both strata; the anchor sign does not (it sits at
                   zero in Self-Other and flips once in
                   Self-Sterilized). The largest study carries 39% and
                   41% of the holdout rows in the Self-Other contrasts.
    3 sweep        the taxon rule's threshold moves rows between ECM
                   and AM+ECM (holdout ECM rows 56 / 111 / 113) and
                   leaves the match counts alone. ECM - AM in Self-Other
                   stays positive with the interval excluding zero at
                   all three settings on both sides (anchor +0.36 to
                   +0.38, holdout +0.12 to +0.13).
    4 fit rules    read against the anchor fit: 4 direction hits (all
                   Self-Other), 1 miss (NM - AM, Self-Sterilized), 2
                   INDETERMINATE (both thin), 1 not checkable.
                   interval_hit is "no" for three of the four hits: the
                   sign carries over, the size does not (ECM - AM in
                   Self-Other is about a third of its anchor size).
    scope          none of this was sealed. These are anchor fits and
                   holdout fits made after the holdout was read, on a
                   join built after it was read; "hit" here is a
                   description, not a score. No correction for the
                   number of contrasts.

### 4.5 Source pin

[OBSERVED] As returned by the GBIF API at fetch time (dataset call at
2026-11-23T18:13:16Z; first occurrence call at 18:13:26Z):

    dataset key           744edc21-8dd2-474e-8a0b-b8c3d56a3c2d
    doi                   10.15468/a7ujmj
    dataset modified      2023-03-21T15:05:30.028+00:00
    dataset created       2019-12-08T21:05:20.984+00:00
    dataset version       NOT RECORDED (no version field was read; the
                          archive endpoint URL ends ".232.zip", meaning
                          not checked)
    last crawled          2026-10-30T14:37:39.938+00:00, crawl id 344
                          (read off the first occurrence record)
    record count          36515
    fetch code commit     NOT RECORDED: the two paging scripts ran from
                          the session's scratch directory and were never
                          committed
                          [added 2026-11-24, order 335-F3] committed after
                          the fact at 0f9d282, holdout/fungalroot_fetch/
                          (three steps as run; see section 4.7). The
                          extract hash is regenerable in principle and
                          has NOT been regenerated: a second fetch was
                          not run (about 40 minutes at the proxy's
                          rate). It would reproduce the hash only if
                          GBIF returns the same records in the same
                          offset order; the API states no such
                          guarantee that this run read, and a re-crawl
                          of the dataset would change it.
    type-rule code        holdout/explore_next_steps.py, functions
                          fungalroot() and _taxon_type(); first committed
                          at ba43407, file hash pinned at efa9422
    order 335-F2 code     the commit that adds this section

### 4.6 License

[OBSERVED] No per-taxon type map is committed. The branch holds the PSF
anchor file, the scripts and the records; the FungalRoot extract and any
species-to-type table exist only in the session's scratch directory.
What is committed from the join is aggregate: counts of rows and studies
per type, and fit estimates. The script holds the map from the source's
type VALUES to the five classes, which names no taxon. Nothing was
removed from the branch.

### 4.7 Order 335-F3 (run 2026-11-24 UTC; exploratory, post-holdout, scores nothing)

Fetch code. [OBSERVED] Committed at 0f9d282, no data and no taxon table:

    holdout/fungalroot_fetch/step1_first_10200.py
        sha256 a487aa71711aa5563f08e8375499b07777bfa49bec1f84ab1df1006c3fd9bb2f
        ran inline; text copied from the session transcript
    holdout/fungalroot_fetch/step2_sequential_unused.py
        sha256 e199a71201ee1657431af886535e97d031ca23a6162e98c0497e0843afab71c5
        scratch file byte for byte under a comment header; stopped after
        one page; output not used
    holdout/fungalroot_fetch/step3_parallel.py
        sha256 0dfbc7123cc0ffaf80c92db6d2b02f5d0544be37957509215c5d489a926a3aeb
        scratch file byte for byte under a comment header; the assembly
        commands are in its header

Site. The dataset has no field named site. Its only location field is
the Latitude / Longitude pair, so site = that pair. The README does not
say what the pair locates (coordinate_meaning is an empty slot), so a
"site" here may be a collection point, a study area or an institution.
[OBSERVED]

Printed by `python3 holdout/explore_next_steps.py f3 SOURCE_CSV
FUNGALROOT_JSONL`, pasted by script.

    ORDER 335-F3 on the FungalRoot join (36515 records); exploratory, post-holdout, scores nothing
      2 LEAVE-ONE-SITE-OUT: site = (Latitude, Longitude) pair; each site in the contrast removed in turn
        anchor  315 sites, 155 studies; sites shared by more than one study: 11; studies with more than one site: 33
        holdout 58 sites, 47 studies; sites shared by more than one study: 3; studies with more than one site: 7
        contrast   rows        stratum          side     full est   min        max        sites  - / +   sign holds   largest-site row share
        ECM - AM   all rows    Self-Other       anchor    +0.3793    +0.3656    +0.4056    219    0 / 219  yes          0.120
        ECM - AM   all rows    Self-Other       holdout   +0.1219    +0.1019    +0.1615     47    0 / 47   yes          0.395
        ECM - AM   woody only  Self-Other       anchor    +0.4228    +0.3422    +0.4970    118    0 / 118  yes          0.119
        ECM - AM   woody only  Self-Other       holdout   +0.1883    +0.0939    +0.2587     15    0 / 15   yes          0.311
        NM - AM    all rows    Self-Other       anchor    -0.0067    -0.0383    +0.0705    163  158 / 5    no           0.134
        NM - AM    all rows    Self-Other       holdout   -0.5324    -0.6247    -0.2898     45   45 / 0    yes          0.414
        NM - AM    all rows    Self-Sterilized  anchor    +0.1417    +0.0203    +0.2091    120    0 / 120  yes          0.115
        NM - AM    all rows    Self-Sterilized  holdout   -0.3797    -0.5728    -0.1708     24   24 / 0    yes          0.227
      3 SIZE GAP, ECM - AM inside Self-Other: what differs between the sides (counts and two fits)
        a) rows by match level, per type          ECM: species  genus  genus share     AM: species  genus  genus share
           anchor                                           90      4  0.043              2264    548  0.195      
           holdout                                          54     43  0.443              1595    288  0.153      
        b) species-level matches only
           anchor  all levels      +0.3793 [ +0.2445,  +0.4669] 124 st  2906 rows   level studies 14 / 118
                   species only    +0.4096 [ +0.2686,  +0.4950] 117 st  2354 rows   level studies 13 / 112
           holdout all levels      +0.1219 [ +0.0537,  +0.2016]  41 st  1980 rows   level studies 9 / 39
                   species only    +0.1279 [ +0.0384,  +0.2282]  39 st  1649 rows   level studies 7 / 37
        c) largest study dropped (the same drop as in the 335-F2 leave-one-study-out)
           anchor  without Fitzpatrick,2017 (350 rows, 0.120 of the contrast's rows, 0 of them ECM)    +0.3948 [ +0.2593,  +0.4830] 123 st  2556 rows   level studies 14 / 117
           holdout without Dostal et al. 2021 (782 rows, 0.395 of the contrast's rows, 0 of them ECM)    +0.1132 [ +0.0562,  +0.1760]  40 st  1198 rows   level studies 9 / 38
        d) mix, rows / studies
           Experimental.setting   Greenhouse    Field         
           anchor  ECM           93 / 13       1 / 1         
           anchor  AM            2681 / 106    131 / 15      
           holdout ECM           66 / 7        31 / 3        
           holdout AM            1482 / 33     401 / 8       
           Phase2.time            <= 3 mo       3-6 mo        6-12 mo       > 12 mo       NOT RECORDED  
           anchor  ECM           26 / 4        30 / 3        35 / 5        3 / 2         0 / 0         
           anchor  AM            2233 / 68     478 / 39      23 / 6        73 / 8        5 / 1         
           holdout ECM           1 / 1         15 / 2        16 / 4        65 / 3        0 / 0         
           holdout AM            708 / 22      535 / 10      348 / 6       292 / 6       0 / 0         

[DERIVED] Reading. Nothing below is read as cause.

    2 sites      ECM - AM inside Self-Other keeps its sign under every
                 single-site removal, all rows and woody only, both
                 sides. NM - AM: holdout sign holds in both strata;
                 anchor Self-Other does not (it sits at zero).
    3 size gap   anchor +0.38, holdout +0.12. What lines up with the
                 gap and what does not:
                 lines up      a) match level: 4% of anchor ECM rows are
                               typed at genus level against 44% of
                               holdout ECM rows.
                               d) setting: 1 of 94 anchor ECM rows is
                               Field against 31 of 97 holdout ECM rows.
                               d) duration: 3 of 94 anchor ECM rows run
                               over 12 months against 65 of 97 holdout
                               ECM rows.
                 does not      b) species-level matches only: the gap
                               stays (anchor +0.41, holdout +0.13).
                               c) largest study dropped: the gap stays
                               (anchor +0.39, holdout +0.11); neither
                               largest study has an ECM row.
                 So the genus-level typing is on the list of differences
                 but removing it does not close the gap. Setting and
                 duration differ sharply between the sides for ECM rows
                 and were not refit (the order allows no further fits).
                 The holdout ECM rows come from 9 studies.

Crowding.

"ECM-AM contrasts were chosen after the earlier tables were seen, by a
 proposer whose training may contain a published ECM-positive /
 AM-negative feedback claim. Direction recovery here is a known-answer
 reading, not a blind test. crowding: dense (DERIVED, not probed)."

NM-AM: CURIOSITY branch. The anchor Self-Other estimate is about zero
(-0.0067, interval across zero), so the direction "hit" recorded for it
in section 4, block 4, is void.

Observer slots: null.

## Provenance

Base branch: claude/denominator-sorter (PR #334) at commit c0a7d77.
Code: `holdout/explore_next_steps.py` (standard library only).
Follow-up order of 2026-11-23: sections 1b, 1c and 2b. Order 335-F2:
section 4. Order 335-F3: section 4.7 and holdout/fungalroot_fetch/. FungalRoot records:
section 2b (fetched extract, sha256 asserted by the script, not
committed).
Source data: Zenodo record 10403125, file PSF.data.EL.open.csv, fetched
2026-11-23T16:41:49Z from
https://zenodo.org/api/records/10403125/files/PSF.data.EL.open.csv/content,
1609518 bytes, sha256
bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c
(asserted by the script; not committed). anchor_studies.csv sha256
e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438,
asserted. The readings in section 1 are this run's.
