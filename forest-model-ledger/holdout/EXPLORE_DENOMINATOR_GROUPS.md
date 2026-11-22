# Denominator groups: exploratory sort of the PSF studies

CC0. Exploratory. Nothing here is a test and nothing here is scored.

Status: EXPLORATORY. Co-authored, Kavik + Claude, work order of
2026-11-22. Run date (UTC): 2026-11-22. Observer slots: null.

"Holdout spent at Phase C; this is exploratory and scores nothing."

Tags: DERIVED = computed in this run from the data and the stated
choices; PROPOSED = a reading or a next step, untested; OBSERVED = seen
in this run (gate lines, hashes); NOT RECORDED = a field the source
leaves empty, or something nobody in this run looked at. Every grouping
below is DERIVED. [stated] = the owner said it directly; a standing
definition or expectation, not a finding.

Every number in the indented blocks was printed by
`python3 ledger/toolkit/denominator_sorter.py run SOURCE_CSV` and pasted
by script. None was typed.

## 1. What the sorter does

A study's denominator signature is read from seven recorded columns, in
this order:

    Experimental.setting | Phase2.time (bin) | Approach | Phase1.culti |
    SoilTp | Phase2.grow | Response

    per field    the SET of values the study's rows carry. A study with
                 both arms reads "A+B"; it is not forced onto one side.
    missing      NOT RECORDED, never imputed
    time bins    months: <=3, 3-6, 6-12, >12 (hand-set)
    group        studies with IDENTICAL signatures
    singleton    a study matching no other: "no common denominator",
                 kept and listed

RULE: comparisons and pooling only WITHIN a group. A difference BETWEEN
groups is recorded as a candidate scope effect, never as a
contradiction. The sorter fits nothing and compares no effect sizes; it
only says which studies share a denominator.

Ids (D01, D02, ...) name signatures, numbered by pooled study count, and
are the same in all three tables.

## 2. Gate (before real data)

    known-answer, 3 planted groups + 6 loners: recovered exactly on 5 of 5 seeds  PASS
    null, 40 studies all different: no group reported on 5 of 5 seeds  PASS
    missing field reads NOT RECORDED and is not merged with a recorded value  PASS
    GATE PASS

[OBSERVED] Known-answer: 15 synthetic studies in 3 planted groups plus 6
loners; one planted group has different Phase2.time values inside one
bin, and one loner has a missing Response. Null: 40 studies each with a
design nobody else has. Both passed on every seed, on the first run.

## 3. Groups

Source file sha256 asserted before the run (bb56ba5a...c82c). Anchor =
Year <= 2018, holdout = Year > 2018.

    anchor (<= 2018): 155 studies, 3707 rows -> 35 scope groups holding 94 studies (2884 rows); 61 studies with no common denominator
      id    studies   rows  signature
      D01       7     164  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D03       6     465  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
      D02       5     144  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D05       5      19  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D04       3     418  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D12       3     382  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D14       3     256  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D08       3      60  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
      D11       3      48  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D09       3      30  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D15       3      26  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D06       3      23  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D07       3       5  Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D33       2     174  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Total_biomass
      D13       2     105  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D29       2      88  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D23       2      66  Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D38       2      60  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
      D31       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
      D32       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D19       2      42  Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D43       2      39  Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D41       2      26  Greenhouse | <=3mo+3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D34       2      22  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
      D18       2      20  Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D25       2      20  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D37       2      16  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D21       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D22       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
      D17       2       8  Field | 3-6mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
      D28       2       6  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D30       2       6  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D39       2       5  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
      D40       2       3  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D16       2       2  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      studies with a field NOT RECORDED: Phase2.time 1

    holdout (> 2018): 47 studies, 2262 rows -> 6 scope groups holding 14 studies (459 rows); 33 studies with no common denominator
      id    studies   rows  signature
      D01       3     111  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D04       3      78  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D02       2      96  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D26       2      77  Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D42       2      75  Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D10       2      22  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      studies with a field NOT RECORDED: none

    pooled: 202 studies, 5969 rows -> 43 scope groups holding 122 studies (3487 rows); 80 studies with no common denominator
      id    studies   rows  signature
      D01      10     275  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D02       7     240  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D04       6     496  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D03       6     465  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
      D05       5      19  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D06       4      29  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D12       3     382  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D14       3     256  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D13       3     113  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D08       3      60  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
      D10       3      58  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D11       3      48  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D09       3      30  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D15       3      26  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D16       3       6  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D07       3       5  Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D33       2     174  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Total_biomass
      D29       2      88  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D26       2      77  Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D42       2      75  Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D23       2      66  Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D38       2      60  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
      D31       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
      D32       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D19       2      42  Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D43       2      39  Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D24       2      28  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D41       2      26  Greenhouse | <=3mo+3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D20       2      24  Field | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D34       2      22  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
      D18       2      20  Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D25       2      20  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D35       2      18  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D37       2      16  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D21       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D22       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
      D27       2      10  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D36       2      10  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D17       2       8  Field | 3-6mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
      D28       2       6  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D30       2       6  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D39       2       5  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
      D40       2       3  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      studies with a field NOT RECORDED: Phase2.time 1

## 4. Groups present on both sides

    signatures present on both sides (anchor studies/rows ; holdout studies/rows):
      D01   anchor   7 /  164 ; holdout   3 /  111   group on both sides
      D02   anchor   5 /  144 ; holdout   2 /   96   group on both sides
      D04   anchor   3 /  418 ; holdout   3 /   78   group on both sides
      D06   anchor   3 /   23 ; holdout   1 /    6   one study on a side
      D10   anchor   1 /   36 ; holdout   2 /   22   one study on a side
      D13   anchor   2 /  105 ; holdout   1 /    8   one study on a side
      D16   anchor   2 /    2 ; holdout   1 /    4   one study on a side
      D20   anchor   1 /   12 ; holdout   1 /   12   one study on a side
      D24   anchor   1 /   24 ; holdout   1 /    4   one study on a side
      D27   anchor   1 /    8 ; holdout   1 /    2   one study on a side
      D35   anchor   1 /    2 ; holdout   1 /   16   one study on a side
      D36   anchor   1 /    4 ; holdout   1 /    6   one study on a side
      groups on both sides: 3 ; signatures on both sides at all: 12 ; anchor only: 84 ; holdout only: 27
      holdout studies inside a both-sides group: 8 of 47 ; holdout rows: 285 of 2262

[DERIVED] Only a signature that is a group on both sides could carry a
real holdout test, and this holdout is spent. Three signatures qualify
(D01, D02, D04). They hold 8 of the 47 holdout studies. A further nine
signatures appear on both sides with a single study on one of them.

## 5. No common denominator

    no common denominator
      id    studies   rows  signature
      D01       7     164  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D03       6     465  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
      D02       5     144  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D05       5      19  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D04       3     418  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D12       3     382  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D14       3     256  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D08       3      60  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
      D11       3      48  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D09       3      30  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D15       3      26  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D06       3      23  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D07       3       5  Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D33       2     174  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Total_biomass
      D13       2     105  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D29       2      88  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D23       2      66  Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D38       2      60  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
      D31       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
      D32       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D19       2      42  Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D43       2      39  Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D41       2      26  Greenhouse | <=3mo+3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D34       2      22  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
      D18       2      20  Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D25       2      20  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D37       2      16  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D21       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D22       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
      D17       2       8  Field | 3-6mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
      D28       2       6  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D30       2       6  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D39       2       5  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
      D40       2       3  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D16       2       2  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      studies with a field NOT RECORDED: Phase2.time 1

    holdout (> 2018): 47 studies, 2262 rows -> 6 scope groups holding 14 studies (459 rows); 33 studies with no common denominator
      id    studies   rows  signature
      D01       3     111  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D04       3      78  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D02       2      96  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D26       2      77  Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D42       2      75  Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D10       2      22  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      studies with a field NOT RECORDED: none

    pooled: 202 studies, 5969 rows -> 43 scope groups holding 122 studies (3487 rows); 80 studies with no common denominator
      id    studies   rows  signature
      D01      10     275  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D02       7     240  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D04       6     496  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D03       6     465  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
      D05       5      19  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D06       4      29  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D12       3     382  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D14       3     256  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D13       3     113  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D08       3      60  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
      D10       3      58  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D11       3      48  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D09       3      30  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D15       3      26  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D16       3       6  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D07       3       5  Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D33       2     174  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Total_biomass
      D29       2      88  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D26       2      77  Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D42       2      75  Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D23       2      66  Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D38       2      60  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
      D31       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
      D32       2      54  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D19       2      42  Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D43       2      39  Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D24       2      28  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D41       2      26  Greenhouse | <=3mo+3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
      D20       2      24  Field | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D34       2      22  Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
      D18       2      20  Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D25       2      20  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      D35       2      18  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D37       2      16  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D21       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D22       2      14  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
      D27       2      10  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
      D36       2      10  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D17       2       8  Field | 3-6mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
      D28       2       6  Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D30       2       6  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D39       2       5  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
      D40       2       3  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
      studies with a field NOT RECORDED: Phase2.time 1

    signatures present on both sides (anchor studies/rows ; holdout studies/rows):
      D01   anchor   7 /  164 ; holdout   3 /  111   group on both sides
      D02   anchor   5 /  144 ; holdout   2 /   96   group on both sides
      D04   anchor   3 /  418 ; holdout   3 /   78   group on both sides
      D06   anchor   3 /   23 ; holdout   1 /    6   one study on a side
      D10   anchor   1 /   36 ; holdout   2 /   22   one study on a side
      D13   anchor   2 /  105 ; holdout   1 /    8   one study on a side
      D16   anchor   2 /    2 ; holdout   1 /    4   one study on a side
      D20   anchor   1 /   12 ; holdout   1 /   12   one study on a side
      D24   anchor   1 /   24 ; holdout   1 /    4   one study on a side
      D27   anchor   1 /    8 ; holdout   1 /    2   one study on a side
      D35   anchor   1 /    2 ; holdout   1 /   16   one study on a side
      D36   anchor   1 /    4 ; holdout   1 /    6   one study on a side
      groups on both sides: 3 ; signatures on both sides at all: 12 ; anchor only: 84 ; holdout only: 27
      holdout studies inside a both-sides group: 8 of 47 ; holdout rows: 285 of 2262

    no common denominator (pooled), 80 studies:
      D91   Batten et al. 2008                              4 rows  Greenhouse | <=3mo | Self-Other | Community | Whole soil | Alone | Aboveground
      D62   Bauer,2017                                     72 rows  Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
      D44   Bayandala et al. 2016                           4 rows  Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D116  Beckstead and Parker 2003                       2 rows  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D74   Bever 1994                                     12 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Total_biomass
      D89   Bezemer et al. 2006a Ecology                    2 rows  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone+Competition | Total_biomass
      D109  Bodelier et al. 2006                            6 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Alone+Competition | Total_biomass
      D71   Callaway et al. 2004b Nature                    8 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community+Monoculture | Inoculum | Competition | Total_biomass
      D117  Callaway,2013                                  23 rows  Greenhouse | <=3mo+3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D123  Chen et al. 2018                                4 rows  Greenhouse | >12mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D52   Chung,2019                                      4 rows  Field | >12mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
      D88   Crawford-Knight,2017                            2 rows  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone+Competition | Aboveground
      D86   De Deyn et al. 2004a                           13 rows  Greenhouse | 6-12mo | Self-Sterilized | Community | Whole soil | Competition | Aboveground
      D64   De Long et al. 2021                             5 rows  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
      D60   Dom\xednguez-Begines et al. 2021                2 rows  Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D121  Dostal et al. 2021                            800 rows  Greenhouse | <=3mo+3-6mo+6-12mo | Self-Other | Monoculture | Inoculum | Alone+Competition | Aboveground
      D111  Dudenhoeffer et al. 2018                        9 rows  Greenhouse | <=3mo | Self-Sterilized | Community+Monoculture | Inoculum | Competition | Aboveground
      D57   Forero et al. 2019                            518 rows  Field+Greenhouse | <=3mo+3-6mo+>12mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D100  Gillespie and Allen 2006                        3 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community+Monoculture | Inoculum | Alone | Aboveground
      D68   Gomez-Aparicio et al. 2017                      8 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
      D79   Gundale et al. 2014                             2 rows  Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D122  Hawkes,2013                                    16 rows  Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
      D56   Heinze,2016                                    18 rows  Field+Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D49   Heinze,2019                                    72 rows  Field | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D47   Heinze,2020                                    40 rows  Field | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D58   Hemrova,2016                                   28 rows  Field+Greenhouse | <=3mo+>12mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
      D99   Holah and Alexander 1999                        4 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Competition | Aboveground
      D101  Huangfu et al. 2022                            24 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone+Competition | Total_biomass
      D55   Jiang et al. 2022                              38 rows  Field+Greenhouse | 6-12mo+>12mo | Self-Other | Community | Inoculum+Whole soil | Alone+Competition | Aboveground
      D61   Jin et al. 2020                                 2 rows  Greenhouse | 3-6mo | Self-Other | Community+Monoculture | Whole soil | Alone | Total_biomass
      D73   Kembel et al. 2018                             94 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D87   Kim et al. 2015                                 7 rows  Greenhouse | 6-12mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D85   Kuebbing et al. 2015                            6 rows  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D69   Kuebbing et al. 2016                            6 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community+Monoculture | Inoculum | Alone | Aboveground
      D92   Kulmatiski et al. 2011 SBB                      2 rows  Greenhouse | <=3mo | Self-Other | Community | Whole soil | Competition | Aboveground
      D53   Kulmatiski, unpubl. Data                        6 rows  Field | NOT RECORDED | Self-Other | Community | Whole soil | Competition | Aboveground
      D50   Lance et al. 2020                              16 rows  Field | >12mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D96   Larios et al. 2015                             12 rows  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone+Competition | Aboveground
      D83   Le Roux et al. 2018                             7 rows  Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Alone | Aboveground
      D93   Li et al. 2011 SAS                              3 rows  Greenhouse | <=3mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D106  Li et al. 2022                                  2 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Competition | Aboveground
      D115  Liang et al. 2016                               6 rows  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D45   Liang et al. 2020                              30 rows  Field | 6-12mo | Self-Other | Community | Whole soil | Competition | Total_biomass
      D65   Lozano.2019                                    13 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Competition | Aboveground
      D75   Lucero et al. 2020                              8 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
      D78   Ma,2019                                         6 rows  Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Competition | Aboveground
      D120  Maron et al. 2014                              12 rows  Greenhouse | <=3mo+3-6mo | Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D104  McGinn et al. 2018                             75 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D114  Meijer et al. 2011                              3 rows  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Alone | Aboveground
      D66   Niu et al 2007                                  8 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Competition | Total_biomass
      D110  Nuske et al. 2021                              10 rows  Greenhouse | <=3mo | Self-Sterilized | Community+Monoculture | Inoculum | Alone | Total_biomass
      D107  Packer and Clay 2004                            4 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum+Whole soil | Alone | Aboveground
      D97   Peacher et al. 2020                             8 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D82   Pfennigwerth et al. 2018                       29 rows  Greenhouse | 6-12mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D70   Pizano et al. 2014                              3 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community+Monoculture | Inoculum | Alone | Total_biomass
      D67   Png et al. 2018                                48 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum+Whole soil | Alone | Aboveground
      D63   Qu et al. 2018                                 12 rows  Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
      D84   Reinhart and Callaway 2004                     10 rows  Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D98   Reinhart et al. 2003                            8 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone+Competition | Total_biomass
      D81   Rigg et al. 2016                               20 rows  Greenhouse | 3-6mo+6-12mo+>12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D54   Schittko et al. 2016                           16 rows  Field+Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D103  Semchenko et al. 2017                           4 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Aboveground
      D95   Smith,2012                                      2 rows  Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
      D90   Spitzer et al. 2021                            18 rows  Greenhouse | <=3mo | Self-Other | Community | Inoculum | Competition | Total_biomass
      D118  Stein et al. 2020                              62 rows  Greenhouse | <=3mo+3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone+Competition | Total_biomass
      D59   Stotz, 2018                                     1 rows  Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Total_biomass
      D51   Suding et al. 2004                              2 rows  Field | >12mo | Self-Other | Community | Whole soil | Alone | Total_biomass
      D105  Suguenza et al. 2006                           12 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Alone | Total_biomass
      D72   Tang et al. 2021                               12 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
      D108  Troelstra et al. 2001                           4 rows  Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Alone | Total_biomass
      D113  Van der Stoel et al. 2002                       1 rows  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Total_biomass
      D80   Wagner et al. 2011                             10 rows  Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
      D76   Wang YK et al. 2020                            32 rows  Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone+Competition | Aboveground
      D102  Wang et al. 2021 PE                             3 rows  Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Total_biomass
      D46   Werger et al. 2020                              8 rows  Field | <=3mo | Self-Other | Community | Inoculum | Alone | Aboveground
      D94   Wubs,2018,FE                                   34 rows  Greenhouse | <=3mo | Self-Other | Community+Monoculture | Inoculum | Competition | Aboveground
      D77   Xi et al. 2018                                  2 rows  Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Alone | Aboveground
      D112  Xi et al. 2020                                 12 rows  Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone+Competition | Total_biomass
      D48   Yelenik,2011                                   20 rows  Field | <=3mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
      D119  de la Pena et al. 2010                          8 rows  Greenhouse | <=3mo+3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum+Whole soil | Alone+Competition | Total_biomass

Study labels are the source's Author strings, non-ASCII characters
escaped.

## 6. Reading

All DERIVED; next steps PROPOSED.

    most studies do not share a denominator with many others. Pooled,
    the largest group holds 10 of 202 studies; 80 studies match no other
    study on these seven fields.

    the holdout side is more scattered than the anchor side: 14 of 47
    holdout studies sit in a group, against 94 of 155 anchor studies.
    Part of that is size: fewer studies give fewer chances to match.

    the Phase A/C comparison pooled every study on each side. By the
    rule above, an anchor-to-holdout difference in a pooled fit is first
    a candidate scope effect: the two sides are different mixes of
    denominators (section 4: 84 signatures are anchor only, 27 holdout
    only).

    a within-group test is small by construction. The three both-sides
    groups hold 3, 2 and 3 holdout studies.

## 7. Limits

    exploratory     the holdout is spent; nothing here was pre-stated
    seven fields    the signature is only as fine as the recorded
                    columns. Two studies in one group can still differ
                    in soil source, pot volume, sterilisation method or
                    anything else the source does not record.
    exact match     one differing field splits a group. A coarser
                    signature (fewer fields, wider bins) gives larger
                    groups; which fields matter is not tested here.
    time bins       hand-set. A study at 3.0 months and one at 3.1 land
                    in different bins.
    set per field   a study with both arms never matches a study with
                    one arm, even where a row-level subset would.
    not registered  the tool has no ledger/toolkit yaml entry, is not in
                    tests/test_toolkit.py and has no held-out gate; its
                    gate is its own --gate. Trust: PROPOSED.
    holdout rows    not committed; the run rebuilds them from the source

## 8. Addendum (2026-11-22): lab test inside groups, three empty slots

Added on the same branch after the run above. Sections 1 to 7 are
unchanged and `run` prints the same output as before, byte for byte.
[OBSERVED]

### 8.1 Three empty slots per study

    lab_institution     NOT RECORDED on 202 of 202 studies
    lab_country         NOT RECORDED on 202 of 202 studies
    governance_regime   NOT RECORDED on 202 of 202 studies
                        (permits, sterilization or biosafety rules,
                        funding mandates)
    expiry_condition    filled from each paper's affiliations and methods

The source has no column for any of the three and nothing is imputed.
Latitude and Longitude give the field site, not the lab's location, and
are not used to fill them. The slots take no part in the match: two
unknowns are not a match. Every scope group in sections 3 to 5 is
therefore matched on seven recorded fields and unmatched-or-unknown on
these three.

[stated] Institutional mandates and governance rules are expected to be
a common denominator difference across fields.

### 8.2 Lab test inside each scope group: gate FAILED, real run NOT done

The test is missing_column_finder's Author (lab) test, imported
unchanged (its share, its shuffled null, its FLAG rule), applied to one
scope group at a time, with spread taken about the group mean. A group
that flags would be tagged "signature-matched, protocol-unmatched".

A gate at scope-group size was run first (4 studies, 15 rows each):

    gates first:
    known-answer, 3 planted groups + 6 loners: recovered exactly on 5 of 5 seeds  PASS
    null, 40 studies all different: no group reported on 5 of 5 seeds  PASS
    missing field reads NOT RECORDED and is not merged with a recorded value  PASS
    GATE PASS
    lab test at group size, planted lab effect: flagged on 4 of 5 seeds  FAIL
    lab test at group size, pure noise: clean on 5 of 5 seeds  PASS
    LAB GATE FAIL
    GATE FAIL: not run on real data

[OBSERVED] The planted-effect leg flagged on 4 of 5 seeds. Under the
order's rule a failed gate stops the real run, so the lab test was NOT
run on the anchor, holdout or pooled groups. There is no per-group
lab-spread table and no group is tagged protocol-unmatched. Tag state
for every group: NOT RECORDED.

[OBSERVED] The miss, read without changing anything: on the seed that
did not flag, the four planted lab effects were all drawn within 0.06 of
zero, against row noise of 0.1 to 0.3. The observed share (0.190) sat
just under the largest shuffled share (0.204).

[DERIVED] So the gate, as written, sometimes plants almost nothing, and
at 4 studies the test cannot see a lab difference that small. The gate
was not redesigned after seeing it fail and the flag rule was not
loosened. Two readings stay open and the owner picks: the gate design is
at fault (plant fixed, separated lab effects), or the test is too weak
at scope-group size to be trusted on groups of 2 to 10 studies. Most
real groups hold 2 or 3 studies, smaller than the gate's 4.

Dated note 2026-11-22, reason for the redesign in section 10: "random
planted effects can fall near zero; pass/fail at one size cannot
separate tool failure from low power." The failed gate result above is
kept as run.

## 9. Amended addendum (2026-11-22): arms, field drops, power-gated lab test

Dated note: this addendum replaces the first one. Section 8 is kept as
written; its lab gate ran at 4 studies and its `lab` command is now the
`addendum` command. Items 4 and 5 of the amended addendum (the three
empty slots and the [stated] line) are section 8.1, unchanged.

Printed by `python3 ledger/toolkit/denominator_sorter.py addendum
SOURCE_CSV` and pasted by script. `run` still prints the section 3 to 5
output byte for byte. [OBSERVED]

    known-answer, 3 planted groups + 6 loners: recovered exactly on 5 of 5 seeds  PASS
    null, 40 studies all different: no group reported on 5 of 5 seeds  PASS
    missing field reads NOT RECORDED and is not merged with a recorded value  PASS
    GATE PASS
    lab test at 5 studies, planted lab effect: flagged on 4 of 5 seeds  FAIL
    lab test at 5 studies, pure noise: clean on 5 of 5 seeds  PASS
    LAB GATE FAIL

### 9.1 UNIT = study x arm

An arm is one value combination of the seven fields present in a
study's rows. Every row sits in exactly one arm; an arm signature has
single values. At arm level a group needs units from at least two
studies. The study-level run is kept beside it.

    1 UNIT = study x arm (study-level kept beside it)
      side               level   units  groups  units in groups  singletons
      anchor (<= 2018)   study     155      35               94          61
      anchor (<= 2018)   arm       233      57              208          25
      holdout (> 2018)   study      47       6               14          33
      holdout (> 2018)   arm        80      18               48          32
      pooled             study     202      43              122          80
      pooled             arm       313      66              282          31
      study level: signatures that are groups on both sides 3 ; units in them 23 (holdout 8)
      arm   level: signatures that are groups on both sides 13 ; units in them 103 (holdout 37)

[DERIVED] Splitting into arms removes most of the scatter that came from
set-valued fields: pooled, 282 of 313 arm units share a denominator with
an arm from another study, against 122 of 202 studies. Signatures that
are groups on both sides of 2018 go from 3 to 13, and holdout units
inside them from 8 to 37.

### 9.2 Field-drop sensitivity (report only; the signature is unchanged)

For each field: leave it out, regroup, report. Within-group residual
spread = weighted mean square of the finder's all-columns residuals
about each group's mean, with a group-count correction. "same rows" reads
it on the rows grouped under the full signature, before and after the
drop, so the two numbers are comparable; "own rows" reads it on whatever
rows the dropped signature groups. The mark uses "same rows".

    2 FIELD-DROP SENSITIVITY (pooled; signature not changed)
      residuals: rebuilt all-columns fit explains 0.039316, finder reports 0.039316  MATCH
      study level
        dropped field         groups  singletons  both-sides groups  units in them  spread same rows  spread own rows  mark
        (none)                   43          80                  3             23            0.2756           0.2756  -
        Experimental.setting     43          73                  3             23            0.2757           0.2666  moves outcome
        Phase2.time              44          31                  6             52            0.2807           0.2616  moves outcome
        Approach                 40          45                  6             48            0.2834           0.3187  moves outcome
        Phase1.culti             46          40                  8             49            0.2758           0.2893  moves outcome
        SoilTp                   43          55                  3             29            0.2767           0.3066  moves outcome
        Phase2.grow              40          47                  6             49            0.2851           0.2881  moves outcome
        Response                 46          50                  3             31            0.2803           0.2966  moves outcome
      arm level
        dropped field         groups  singletons  both-sides groups  units in them  spread same rows  spread own rows  mark
        (none)                   66          31                 13            103            0.2705           0.2705  -
        Experimental.setting     65          19                 16            122            0.2706           0.2631  moves outcome
        Phase2.time              37           5                 14            182            0.2785           0.2782  moves outcome
        Approach                 43          23                 11            130            0.2897           0.2955  moves outcome
        Phase1.culti             44          15                 19            187            0.2781           0.2724  moves outcome
        SoilTp                   45          20                 18            164            0.2809           0.2810  moves outcome
        Phase2.grow              40          26                 17            189            0.2897           0.2917  moves outcome
        Response                 47          17                 14            167            0.2787           0.2770  moves outcome

[DERIVED] By the order's rule (a drop that does not raise within-group
spread), no field is marked "splits without moving outcome" at either
level. Two things qualify that:

    the rule has no noise band. Dropping Experimental.setting raises the
    same-rows spread by 0.0001 at both levels (0.2756 to 0.2757, 0.2705
    to 0.2706). Whether a rise that small is distinguishable from none
    was not tested: NOT RECORDED.

    merging groups can only keep or raise the uncorrected spread on the
    same rows. The group-count correction is what lets a drop read as
    "does not raise", and it is small here. The rule is therefore tilted
    toward "moves outcome".

    largest rises at arm level: Approach and Phase2.grow (0.2705 to
    0.2897 each). Smallest: Experimental.setting, then Phase1.culti and
    Phase2.time.

### 9.3 Lab spread inside each group: gate FAILED again, real run NOT done

Power gate as ordered: the lab test may run only on groups with at
least 5 studies (chosen, no external source); smaller groups would read
"underpowered, not tested".

    3 LAB SPREAD inside each group (power gate: >= 5 studies)
      LAB GATE FAIL: lab test not run on real data

The synthetic gate was re-run at the smallest allowed size, 5 studies
of 15 rows:

    seed 0  planted effects +0.038 -0.063 +0.522 -0.221 -0.041  share 0.619  null max 0.234  excess +0.571  FLAG
    seed 1  planted effects +0.104 +0.635 +0.082 -0.028 +0.185  share 0.610  null max 0.281  excess +0.556  FLAG
    seed 2  planted effects +0.057 +0.039 -0.054 +0.046 +0.217  share 0.259  null max 0.299  excess +0.199  -
    seed 3  planted effects +0.612 -0.088 -0.289 +0.173 +0.614  share 0.708  null max 0.188  excess +0.658  FLAG
    seed 4  planted effects -0.196 +0.063 +0.254 -0.358 +0.014  share 0.485  null max 0.206  excess +0.434  FLAG

[OBSERVED] Null leg clean on 5 of 5 seeds; planted leg flagged on 4 of
5. On seed 2 four of the five planted lab effects are within 0.06 of
zero and one is +0.217; the observed share (0.259) is under the largest
of 499 shuffled shares (0.299).

Under the sorter order's rule a failed gate stops the real run. The lab
test was NOT run on any real group. No per-group lab-spread table
exists and no group is tagged "signature-matched, protocol-unmatched".
Tag state for every group: NOT RECORDED. The gate's planted draw and
the flag rule were left as written.

[DERIVED] The power gate changes which groups would be tested; it does
not change what the synthetic gate measures, which is that the test
misses a lab difference when most labs barely differ. What a flag would
mean is not in doubt (the null leg is clean); what a non-flag would mean
is.

### 9.4 Slots

    4 slots per study: lab_institution, lab_country, governance_regime ; NOT RECORDED on 202 of 202 studies ; expiry_condition: filled from each paper's affiliations and methods

## 10. Lab test power curve, then the real lab test (2026-11-22)

Printed by `python3 ledger/toolkit/denominator_sorter.py power
SOURCE_CSV` and pasted by script. Synthetic first; the rule was fixed in
the order before any real group was read.

    synthetic groups   k studies of 15 rows; row variance uniform on
                       0.01 to 0.1, as in the failed gate
    lab effects        FIXED: equally spaced, centred, scaled to the
                       stated spread sd (for k = 2 that is +sd and -sd)
    cells              50 seeds each; flag rule unchanged
    constants          the sizes, the four sd values, 0.8 and 0.05 are
                       chosen, no external source

    POWER CURVE (synthetic only): 15 rows per study, 50 seeds per cell, flag rule unchanged
      detection rate, lab effects fixed at spread sd
      k studies   sd 0.05   sd 0.10   sd 0.20   sd 0.40   false-flag (pure noise)
              2      0.08      0.24      0.90      1.00      0.00
              3      0.04      0.30      0.94      1.00      0.00
              4      0.04      0.50      1.00      1.00      0.00
              5      0.06      0.40      1.00      1.00      0.00
              8      0.04      0.80      1.00      1.00      0.00
    RULE (declared before real data): detection >= 0.8 at sd 0.2 and false-flag <= 0.05
      qualifying sizes: 2, 3, 4, 5, 8 ; a real group of k studies is read at the largest tested size <= k

[OBSERVED] Every tested size qualifies, including k = 2 (detection 0.90
at sd 0.2). No false flag in 250 pure-noise groups. At sd 0.1 detection
is between 0.24 and 0.80 and at sd 0.05 it is near the false-flag
floor: the test does not see lab differences that small at these sizes.

[DERIVED] This settles the two gate failures in sections 8.2 and 9.3 as
low power on one draw, not a fault in the test: that draw planted lab
effects near zero.

Scope of the curve, which the rule does not cover: it was run at 15
rows per study. Many real groups are thinner. Each table below counts
the tested groups under 15 rows per study; for those, a non-flag says
less than the curve suggests. A flag does not depend on the curve (the
false-flag rate is what backs it).

### 10.1 Real lab test

Spread is taken about each group's mean, with no column fitted first
(section 8.2 gives the reason). Pooled tables list every tested group;
side tables list flagged groups only, with the counts for the rest.

    anchor (<= 2018), study level: 35 groups; 33 tested; 0 underpowered at this size; 2 not checkable (rows barely exceed studies); 2 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 16 of 33 ; flagged among them: 0
      flagged groups only:
      studies   rows   lab share  null mean  null max   excess   tag / signature
          6     465      0.388      0.010     0.040   +0.378   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
          2      60      0.197      0.018     0.163   +0.179   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass

    anchor (<= 2018), arm level: 57 groups; 54 tested; 0 underpowered at this size; 3 not checkable (rows barely exceed studies); 7 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 38 of 54 ; flagged among them: 2
      flagged groups only:
      studies   rows   lab share  null mean  null max   excess   tag / signature
         11     701      0.293      0.014     0.043   +0.279   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
          9     445      0.077      0.020     0.068   +0.057   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
          6     141      0.467      0.039     0.173   +0.428   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
          5      60      0.598      0.059     0.574   +0.539   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
          4      76      0.223      0.042     0.196   +0.180   signature-matched, protocol-unmatched
            Greenhouse | 6-12mo | Self-Other | Community | Inoculum | Alone | Aboveground
          2      22      0.449      0.042     0.381   +0.407   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
          2      39      0.225      0.024     0.161   +0.201   signature-matched, protocol-unmatched
            Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground

    holdout (> 2018), study level: 6 groups; 6 tested; 0 underpowered at this size; 0 not checkable (rows barely exceed studies); 2 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 1 of 6 ; flagged among them: 0
      flagged groups only:
      studies   rows   lab share  null mean  null max   excess   tag / signature
          3     111      0.277      0.018     0.099   +0.259   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
          2      75      0.349      0.011     0.104   +0.338   signature-matched, protocol-unmatched
            Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass

    holdout (> 2018), arm level: 18 groups; 18 tested; 0 underpowered at this size; 0 not checkable (rows barely exceed studies); 3 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 10 of 18 ; flagged among them: 1
      flagged groups only:
      studies   rows   lab share  null mean  null max   excess   tag / signature
          3      36      0.394      0.060     0.394   +0.334   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
          3     111      0.277      0.017     0.138   +0.259   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
          2      75      0.349      0.011     0.166   +0.338   signature-matched, protocol-unmatched
            Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass

    pooled, study level: 43 groups; 42 tested; 0 underpowered at this size; 1 not checkable (rows barely exceed studies); 6 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 22 of 42 ; flagged among them: 0
      every tested group:
      studies   rows   lab share  null mean  null max   excess   tag / signature
         10     275      0.210      0.030     0.118   +0.180   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
          7     240      0.015      0.024     0.069   -0.009   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          6     465      0.388      0.010     0.042   +0.377   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
          6     496      0.084      0.010     0.050   +0.074   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
          5      19      0.347      0.198     0.779   +0.149   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
          4      29      0.160      0.095     0.370   +0.065   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
          3       5      0.438      0.478     0.993   -0.041   not flagged
            Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
          3      60      0.004      0.034     0.137   -0.029   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
          3      30      0.018      0.076     0.423   -0.058   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
          3      58      0.288      0.036     0.208   +0.252   signature-matched, protocol-unmatched
            Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
          3      48      0.018      0.045     0.289   -0.028   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
          3     382      0.018      0.005     0.026   +0.013   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          3     113      0.040      0.020     0.114   +0.020   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
          3     256      0.011      0.009     0.075   +0.002   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
          3      26      0.078      0.082     0.388   -0.004   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
          3       6      0.862      0.371     0.862   +0.491   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
          2       8      0.324      0.161     0.614   +0.163   not flagged
            Field | 3-6mo | Self-Other | Community | Whole soil | Alone+Competition | Aboveground
          2      20      0.006      0.057     0.521   -0.050   not flagged
            Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
          2      42      0.095      0.028     0.265   +0.067   not flagged
            Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          2      24      0.001      0.045     0.405   -0.044   not flagged
            Field | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          2      14      0.002      0.086     0.478   -0.084   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
          2      14      0.016      0.076     0.622   -0.060   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
          2      66      0.038      0.011     0.106   +0.027   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
          2      28      0.049      0.040     0.329   +0.009   not flagged
            Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
          2      20      0.366      0.045     0.552   +0.320   not flagged
            Greenhouse | 3-6mo | Self-Other+Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
          2      77      0.006      0.014     0.129   -0.008   not flagged
            Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
          2      10      0.253      0.113     0.477   +0.139   not flagged
            Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          2       6      0.912      0.203     0.912   +0.709   not flagged
            Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          2      88      0.000      0.013     0.093   -0.013   not flagged
            Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Aboveground
          2       6      0.232      0.199     0.658   +0.034   not flagged
            Greenhouse | 6-12mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
          2      54      0.028      0.020     0.161   +0.008   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
          2      54      0.017      0.017     0.135   +0.000   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Aboveground
          2     174      0.015      0.005     0.054   +0.010   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone+Competition | Total_biomass
          2      22      0.391      0.040     0.391   +0.351   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
          2      18      0.221      0.050     0.476   +0.171   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Inoculum | Alone | Total_biomass
          2      10      0.174      0.113     0.654   +0.061   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Community | Whole soil | Alone | Aboveground
          2      16      0.000      0.071     0.748   -0.071   not flagged
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
          2      60      0.197      0.017     0.194   +0.180   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other+Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
          2       5      0.640      0.228     0.640   +0.412   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
          2      26      0.192      0.038     0.302   +0.154   not flagged
            Greenhouse | <=3mo+3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
          2      75      0.349      0.010     0.110   +0.339   signature-matched, protocol-unmatched
            Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
          2      39      0.225      0.028     0.265   +0.197   not flagged
            Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground

    pooled, arm level: 66 groups; 65 tested; 0 underpowered at this size; 1 not checkable (rows barely exceed studies); 13 flagged
      tested groups with fewer than 15 rows per study (thinner than the power curve's groups): 44 of 65 ; flagged among them: 6
      every tested group:
      studies   rows   lab share  null mean  null max   excess   tag / signature
         15     388      0.206      0.031     0.081   +0.175   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
         14     591      0.076      0.022     0.063   +0.054   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
         13     293      0.122      0.039     0.105   +0.084   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
         12     883      0.258      0.012     0.049   +0.246   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
         11      75      0.474      0.139     0.437   +0.336   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
          8      52      0.648      0.139     0.627   +0.509   signature-matched, protocol-unmatched
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Aboveground
          8      96      0.577      0.060     0.447   +0.517   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
          8      48      0.500      0.166     0.593   +0.335   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
          7      24      0.443      0.236     0.670   +0.208   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Total_biomass
          7      64      0.092      0.097     0.310   -0.005   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Total_biomass
          7     438      0.026      0.013     0.048   +0.013   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          6      32      0.328      0.160     0.519   +0.168   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Alone | Aboveground
          6     141      0.467      0.039     0.200   +0.428   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
          6      62      0.171      0.082     0.341   +0.089   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
          5     296      0.046      0.012     0.063   +0.034   not flagged
            Field | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          5     103      0.028      0.039     0.282   -0.011   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
          5     157      0.016      0.015     0.247   +0.001   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Alone | Total_biomass
          5      94      0.217      0.047     0.196   +0.170   signature-matched, protocol-unmatched
            Greenhouse | 6-12mo | Self-Other | Community | Inoculum | Alone | Aboveground
          5      26      0.413      0.155     0.586   +0.258   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Alone | Total_biomass
          4      24      0.270      0.138     0.782   +0.132   not flagged
            Field | 3-6mo | Self-Other | Community | Whole soil | Competition | Aboveground
          4      25      0.494      0.115     0.802   +0.379   not flagged
            Field | >12mo | Self-Other | Community | Whole soil | Competition | Aboveground
          4      47      0.347      0.063     0.323   +0.284   signature-matched, protocol-unmatched
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Alone | Total_biomass
          4      61      0.007      0.050     0.185   -0.042   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Total_biomass
          4     268      0.030      0.011     0.061   +0.019   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Competition | Aboveground
          4      13      0.196      0.251     0.884   -0.055   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Alone | Total_biomass
          4      35      0.401      0.079     0.582   +0.322   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Alone | Total_biomass
          4      65      0.109      0.049     0.250   +0.059   not flagged
            Greenhouse | <=3mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
          4      21      0.551      0.155     0.502   +0.395   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Inoculum | Competition | Total_biomass
          4      12      0.685      0.274     0.791   +0.412   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Alone | Total_biomass
          3      22      0.029      0.088     0.516   -0.059   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Aboveground
          3      30      0.018      0.067     0.415   -0.049   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Competition | Total_biomass
          3      18      0.298      0.116     0.609   +0.182   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Alone | Aboveground
          3      37      0.118      0.051     0.306   +0.067   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Competition | Total_biomass
          3      10      0.687      0.214     0.742   +0.473   not flagged
            Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Alone | Aboveground
          3      45      0.069      0.045     0.484   +0.024   not flagged
            Greenhouse | 6-12mo | Self-Sterilized | Community | Inoculum | Alone | Aboveground
          3       7      0.450      0.316     0.812   +0.134   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Inoculum | Alone | Aboveground
          3       7      0.008      0.303     0.800   -0.295   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Inoculum | Competition | Aboveground
          3      21      0.041      0.091     0.483   -0.049   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Inoculum | Competition | Total_biomass
          3      10      0.310      0.212     0.701   +0.099   not flagged
            Greenhouse | <=3mo | Self-Other | Community | Whole soil | Alone | Aboveground
          3      80      0.123      0.022     0.145   +0.100   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Alone | Aboveground
          3      10      0.413      0.188     0.896   +0.225   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Inoculum | Competition | Aboveground
          3       7      0.920      0.328     0.920   +0.592   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Alone | Aboveground
          3       9      0.443      0.232     0.883   +0.211   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Competition | Total_biomass
          3      10      0.513      0.210     0.732   +0.303   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Competition | Aboveground
          2       4      0.696      0.298     0.696   +0.397   not flagged
            Field | 3-6mo | Self-Other | Community | Whole soil | Alone | Aboveground
          2      42      0.095      0.028     0.232   +0.067   not flagged
            Field | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          2       6      0.817      0.204     0.817   +0.613   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Inoculum | Competition | Total_biomass
          2      16      0.015      0.069     0.471   -0.053   not flagged
            Greenhouse | 3-6mo | Self-Other | Community | Whole soil | Alone | Aboveground
          2      11      0.100      0.084     0.515   +0.016   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Inoculum | Competition | Total_biomass
          2     252      0.006      0.003     0.039   +0.003   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          2      24      0.115      0.039     0.411   +0.076   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          2       7      0.255      0.186     0.590   +0.070   not flagged
            Greenhouse | 3-6mo | Self-Other | Monoculture | Whole soil | Competition | Total_biomass
          2      11      0.493      0.106     0.689   +0.386   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Competition | Aboveground
          2       6      0.472      0.164     0.472   +0.308   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Community | Inoculum | Competition | Total_biomass
          2      16      0.013      0.065     0.527   -0.053   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Community | Whole soil | Alone | Aboveground
          2       6      0.941      0.190     0.941   +0.751   not flagged
            Greenhouse | 3-6mo | Self-Sterilized | Monoculture | Inoculum | Competition | Aboveground
          2      77      0.006      0.014     0.112   -0.008   not flagged
            Greenhouse | 6-12mo | Self-Other | Community | Whole soil | Competition | Aboveground
          2      86      0.008      0.012     0.163   -0.004   not flagged
            Greenhouse | 6-12mo | Self-Other | Monoculture | Inoculum | Alone | Aboveground
          2      10      0.253      0.117     0.477   +0.135   not flagged
            Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Alone | Aboveground
          2       6      0.912      0.208     0.912   +0.704   not flagged
            Greenhouse | 6-12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground
          2       6      0.491      0.094     0.491   +0.398   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Community | Whole soil | Alone | Total_biomass
          2       5      0.915      0.250     0.915   +0.664   not flagged
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Alone | Aboveground
          2      22      0.449      0.050     0.436   +0.399   signature-matched, protocol-unmatched
            Greenhouse | <=3mo | Self-Sterilized | Monoculture | Whole soil | Competition | Total_biomass
          2      75      0.349      0.012     0.128   +0.337   signature-matched, protocol-unmatched
            Greenhouse | >12mo | Self-Other | Community | Inoculum | Alone | Total_biomass
          2      39      0.225      0.030     0.244   +0.195   not flagged
            Greenhouse | >12mo | Self-Other | Monoculture | Whole soil | Competition | Aboveground

[DERIVED] Reading, scoped to these groups and this test:

    pooled, study level   6 of 42 tested groups flagged
    pooled, arm level     13 of 65 tested groups flagged
    tagged                each flagged group carries "signature-matched,
                          protocol-unmatched": its studies share all
                          seven recorded fields and still differ from
                          each other by more than row noise allows
    not flagged           is NOT "protocol-matched". At spread sd 0.1 the
                          test misses most of the time, and most
                          unflagged groups are thinner than the curve's.
                          Their tag stays NOT RECORDED.
    same signature        several flagged groups recur across the side
                          and pooled tables; they are one group seen
                          more than once, not independent flags
    many tests            about 65 groups were tested per pooled table
                          at a false-flag rate the synthetic run put at
                          0 of 250; no correction was applied

What the flag cannot say: which unrecorded difference separates the
labs. That is what the three empty slots in section 8.1 and the
finder's Author expiry_condition are for.

## Provenance

Co-authored, Kavik + Claude, work order of 2026-11-22 (END marker
present). Base branch: claude/forest-holdout-phase-c (PR #332); separate
from the missing_column_finder branch, which this work does not touch.
Code: `ledger/toolkit/denominator_sorter.py`; `run` and `--gate` use the
standard library only, and the addendum's `lab` command imports
`ledger/toolkit/missing_column_finder.py` (numpy), brought onto this
branch by merge from its own branch, unedited. The amended addendum
(section 9) is the `addendum` command; it rebuilds the finder's
all-columns residuals from the finder's own parts and checks the
explained share against the finder before using them. Section 10 is the
`power` command: a synthetic power curve, a size rule fixed in the order
before real data, then the real lab test on qualifying groups.
Source data: Zenodo record 10403125, sha256 asserted, not committed.
The reading in section 6 is this run's.
