# encoding-selection — claim table

Claims are about the instrument and the order's own arithmetic, schema
and material. None is a claim about any reader, any format's arrival
cost, or what any encoding carries.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph.

| id | claim | status |
|---|---|---|
| ES_001 | Kendall's W by hand reproduces fixed-in-advance answers, and the three rules fire in both directions on constructed worlds | SUPPORTED |
| ES_002 | "W above chance" has no chance in the order; a permutation null supplies one, declared | SUPPORTED |
| ES_003 | "variance in recovered quantity" is over a set-valued field whose vocabulary ends in `other`; a distance is chosen and declared, and `other` is one bit | SUPPORTED |
| ES_004 | H3's "table readers" names a kind and not a format; the class is declared and every format's rate is printed beside it | SUPPORTED |
| ES_005 | both seed items are this repository's own artifacts, and M2 states the pre-correction reading the trucking row withdrew on the order's own date | SUPPORTED |
| ES_006 | the seven encodings per item are not shipped and are not authored here; the instrument validates an encodings file against the item's fact list and refuses an added fact | SUPPORTED |
| ES_007 | a decline is a third state beside a ranking and a between-subjects blank, and the first build counted it per row instead of per reader | SUPPORTED |
| ES_008 | W pools rankers only over a common format set; F7 is each reader's own encoding and cannot enter a pooled W unless every ranker ranked their own | SUPPORTED |
| ES_009 | nothing here bears on H1, H2 or H3 | UNVERIFIED |

## ES_001 — known answers first

W is 1.0 on identical rankings, 168/216 on a three-ranker hand case
(rank sums 4, 5, 9; S = 14), and None with one ranker or one item.
Jaccard distance is 0 on identical sets, 1 on disjoint, 0 on two empty
sets. M1's ratio is arithmetic: 4 days over 4 hours is 24. A world where
recovery tracks the format returns within-format distance 0 and
between-format distance above 0 (H2 not falsified); a world where it
tracks the reader returns the reverse (H2 FALSE). Consistent rankers
return W 1.0 with p below the threshold (H1 FALSE); scattered rankers
do not. Prose at 0 and the table class at 1 leave H3 standing; equal
rates fire it.

## ES_002 — chance for W

The rule says *Kendall's W above chance* and gives no chance. Under a
small number of rankers W is far from zero on independent rankings, so
a fixed threshold would be a guess. `[CHOICE 1]` draws 2000
permutations, shuffling each ranker's order independently, and reports
the share of draws at or above the observed W, with the alpha printed.
A chi-square approximation would give a number by a different route;
neither is in the order, and the one used is declared.

## ES_003 — a distance for a set

P3 codes each response for a SET of recovered quantities over an
eight-item vocabulary, and H2's rule compares within-format to
between-format *variance* of that set. A set has no variance until a
distance is chosen. `[CHOICE 2]` uses mean pairwise Jaccard distance,
pooled within formats and across formats on the same item, plus the
same distance across the formats one within-subjects reader saw, which
is H2's second clause measured directly. The vocabulary's last entry is
`other`, so two readers recovering two different unlisted quantities
read as agreeing on one bit; the distance is bounded by the vocabulary
from below.

## ES_004 — which formats are "table readers"

H3 contrasts prose with *tabular or dimensional formats*. F3 is
dimensional by name and F5 is per-row by description; F4 states
exclusions and is the format whose native quantity is closest to what
H3 asks readers to name, and it is neither tabular nor dimensional.
`[CHOICE 3]` takes F3 and F5 as the class and prints every format's
rate beside it; `[CHOICE 4]` reads *same rate* as prose at or above
the class. Both are printed on every render so they can be moved.

## ES_005 — the material is the repository

M1 is `hf-incident-extract`'s M1 explore ratio: 4 hours to solve, ~4
days mapping a declared-but-unimplemented scorer property, 24:1. M2 is
`readout-count`'s trucking seed row. The order's MATERIAL condition is
*a finding the reader does not already hold*, and any reader of this
repository holds both — as does the model that drafted the order and
the one that built this instrument. More specifically: M2 reads *three
declared channels, zero returns*, which is the parent order's v0 seed
cell; `TRUCKING_ROW_v0_1.md`, dated 2026-09-02 like this order, corrects
the count to 0.5 on one partial-return channel and re-types the three
as complaint channels. The material's fact set moved on the day the
order was written. The FACTS list here transcribes the order as
delivered; an encoding of M2 carrying `zero returns` carries a fact the
sibling has since withdrawn.

## ES_006 — the encodings are not here

The order says all seven encodings must be published verbatim and that
encoding one content seven ways is a judgment call. None arrived, and
none is authored here: the encodings are the experimental material, and
writing them would put the instrument's author in the sample the order
excludes. What the instrument does is validate an encodings file — seven
formats per item, each with text and a declared carried / dropped split
over the item's fact list — and refuse an encoding that carries a fact
not on the list (the order's *without adding facts*), one that both
carries and drops a fact, or one with no text. The order's *omission is
DATA* is the `dropped` list, counted per format.

## ES_007 — declines, and a defect found by running

P4 says declines are declines, not missing data. The schema here has
three states on `rank_given`: an ordered list, the literal `declined`
(which requires a reason), and blank, which is legal only on a
between-subjects row. W is computed over rankers and the decline count
is printed beside it as a rate, never subtracted from anything. The
first build counted declines per row — a reader who saw six formats and
declined once was six declines — and the constructed world caught it;
corrected to one per reader per item, and recorded here rather than
silently, since it is the kind of count that reads as plausible at any
value.

## ES_008 — F7 and the pooled W

W is defined over rankers who ranked the same items. F7 is the reader's
own encoding, different for every reader, so it can enter a pooled W
only if every ranker ranked their own F7 alongside F1–F6 — and then
"F7" names a different object in each row. The instrument refuses to
pool rankers over different format sets and names the sets; the
constructed worlds rank F1–F6.

## ES_009 — UNVERIFIED

No reader has read anything. Every number here is a property of the
instrument on constructed rows, and the origin n=1 is excluded by the
order's own last limit.
