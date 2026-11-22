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

## Provenance

Co-authored, Kavik + Claude, work order of 2026-11-22 (END marker
present). Base branch: claude/forest-holdout-phase-c (PR #332); separate
from the missing_column_finder branch, which this work does not touch.
Code: `ledger/toolkit/denominator_sorter.py`; `run` and `--gate` use the
standard library only, and the addendum's `lab` command imports
`ledger/toolkit/missing_column_finder.py` (numpy), brought onto this
branch by merge from its own branch, unedited.
Source data: Zenodo record 10403125, sha256 asserted, not committed.
The reading in section 6 is this run's.
