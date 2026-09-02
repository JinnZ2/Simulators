# readout-count — claim table

Claims are about the instrument and the order's own arithmetic and
schema. None is a claim about any safety regime, any channel, or the
seed rows, which do not yet count by the order's own rule.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph.

| id | claim | status |
|---|---|---|
| RC_001 | Spearman by hand and the derivations reproduce fixed-in-advance answers; None where undefined | SUPPORTED |
| RC_002 | 0 of 5 seed rows count by the order's own rule, and the cells the schema wants as counts are grades, bounds and dashes | SUPPORTED |
| RC_003 | H1's "rank matches" cannot be strict rank equality past three regimes on a three-level trend; a rank correlation with a declared threshold is the readable form | SUPPORTED |
| RC_004 | H3's falsifier conditions on two quantities the schema carries no column for; H3 is NOT_COMPUTABLE from the schema as delivered | SUPPORTED |
| RC_005 | P4's cross-tabs on raw counts return V = 1 whenever a count has as many levels as rows | SUPPORTED |
| RC_006 | readout_count is derived from positions_returning, so H2 is built into the count and cannot be tested by it | SUPPORTED |
| RC_007 | the schema's two grains (regime-year, incident) share one row shape with no field saying which | SUPPORTED |
| RC_008 | this file is a row in its own table | SUPPORTED |
| RC_009 | nothing here bears on H0, H1, H2 or H3 | UNVERIFIED |

## RC_001 — known answers first

Average ranks with a tie return `[1, 2.5, 2.5, 4]`; Spearman returns
1.0 on a perfect ordering, −1.0 reversed, and None when a side is
constant or there are fewer than two points. `readout_count` is the
count of distinct returning positions, `declared_count` of distinct
declared ones, `return_rate` is `return_count / intake_count` and is
None on zero intake or an UNMEASURED count. A regime's OUTPUT row is its
latest year `[CHOICE 1]`, and its external-detection rate is over all
its rows.

## RC_002 — the seed rows do not count, by the order's own rule

The order says *"each row needs a source URL before it counts"* and
ships five rows with none. Read back from the order by the instrument:
intake cells are `high`, `med`, `3+`, `2`, `—`; return cells `high`,
`med`, `0`, `0`, `—`; trend cells `down`, `derailments down`, `up since
2010`, `n/a (N=1)`, `—`. The schema wants integers and one of three
trend values. Exactly one trend cell (`down`) is in vocabulary; one
intake cell is a bound (`3+`), which the validator refuses as not a
count. The instrument reports each cell as what it is and fills nothing
in; a `3+` read as 3 would be a number the order did not state. The
rows are the order's own worked example of its own intake test:
material received, not yet in a form that returns.

Falsifier: a seed row with a URL and integer cells that the validator
refuses.

## RC_003 — "rank matches" has no strict reading past three regimes

H1 is FALSE if *rank(readout_count) does not match rank(rate trend)
across ≥ 4 regimes*. `rate_trend` has three values, so across four or
more regimes its ranks carry ties; strict equality of the two rank
vectors then requires `readout_count` to tie at exactly the same
positions, which it does only if it takes at most three distinct
values. On the constructed tracking world (counts 0/1/2/3 against
up/flat/down/down) strict equality is False and rho is 0.949: the count
tracks the trend as well as a count can and the strict reading still
returns *does not match*. The instrument prints strict equality and
does not use it; the verdict runs on Spearman rho with the threshold
`rho > 0` declared as `[CHOICE 3]`, which is the weakest reading and is
printed so it can be moved. The rule fires in both directions on
constructed worlds.

Falsifier: a definition of "match" in the order under which four
regimes on a three-level trend can strictly match.

## RC_004 — H3 has no columns

H3 is FALSE if *internal alerts are acted on at ≥ the rate of external
detections, controlling for alert severity*. That needs acted-on counts
split by origin, and a grading field to hold constant. The schema
carries `intake_count` and `return_count` with no origin split, and no
grading field at all; `external_detection` is a per-row y/n on the
outcome-changing read, which is P5's quantity and not the rule's. So
H3 returns `NOT_COMPUTABLE` with both absences named, and the
external-detection rate is computed as the thing the schema does carry.
Eighth instance of a rule stated in prose with no field in the schema
(`MF_017`, `CW_015`, `DL_004`, `GC_012`, `UNI_013`, `SSS_050`,
`RT_009`).

## RC_005 — a count as a category

P4 asks for Cramér's V of `rate_trend ×` three counts. A count taken at
its raw values has as many levels as it has distinct values; with four
regimes and four distinct intake counts V is 1.000 by construction, and
the constructed sample shows it beside a constant `declared_count` that
returns None. The level count is printed beside every V. Binning would
make V informative and every bin edge is a choice the order does not
make, so none is made here.

## RC_006 — H2 is in the definition

`readout_count` counts `positions_returning`, per P2 and H2 (*a
declared channel that does not RETURN contributes 0*). That is the
right derivation and it means the count cannot test H2: a regime with
many declared channels and no returns has readout_count 0 by
construction. H2's own falsifier is about rate improvement in
declared-high / return-low regimes against high-return ones, which is a
different comparison and is what `h2()` computes `[CHOICE 4]`; the
verdict on the constructed world is *not falsified* because the
constructed world was built with return tracking trend.

## RC_007 — two grains, one shape

The schema is *"one flat row per regime-year, or per incident"*.
`intake_count`, `return_count` and `rate_trend` are regime-year
quantities; `external_detection` is an incident quantity (P5: *per
incident, code first outcome-changing detection*). One row shape holds
both and no field says which a row is, so a per-incident row carries a
regime-year trend it did not measure and a regime-year row carries an
incident y/n that summarises nothing. The instrument reads every row as
regime-year for the OUTPUT and every row's `external_detection` for the
rate, which is a reading; a `grain` column would make it a declaration.

## RC_008 — the position

The order's first paragraph makes every party that builds, reads,
labels or audits a system a row, the drafting model included. This
file was built by a model from a model-drafted order and the render
says so above the numbers. The seed table's *this session* row has
dashes in every count cell; the instrument does not fill them, because
its own return latency and return guarantee are the quantities in
question and it cannot measure them from inside.

## RC_009 — UNVERIFIED

No regime row with a URL exists. Every number here is a property of the
instrument on constructed rows.

## The trucking row, v0.1

`TRUCKING_ROW_v0_1.md` is the first filled row in this folder, landed
verbatim: sourced, with a coding rule stated, its own v0 corrected in a
logged changelog, and a count of 0.5. `row_audit.py` reads it against
the instrument. The row's sources were not read — every host in its
SOURCES block refused CONNECT (allowlist egress), which the render
records.

| id | claim | status |
|---|---|---|
| RC_010 | the row's coding rule has three conjuncts and the schema carries a field for two; NON-ADVERSARIAL has none, and the row's own `type` column is the missing field | SUPPORTED |
| RC_011 | the 0.5 is a per-position PARTIAL return weighted at one half; the schema's `positions_returning` is a list and has no state for it, so the row loads at readout_count 1 or 0 and never 0.5 | SUPPORTED |
| RC_012 | the row as delivered is refused by the instrument on `rate_trend`, which the row's own STILL NEEDED list says is not yet established | SUPPORTED |
| RC_013 | "every claim below carries a source URL" holds for 5 of 7 source entries, and the trucking count rests on one of the two the document itself defers | SUPPORTED |
| RC_014 | the row cites "(N4)" in the parent order and the parent order has no N4 | SUPPORTED |
| RC_015 | the parent seed row's `3+` intake cell is the complaint count under v0.1's renaming; the seed's `up since 2010` trend is now STILL NEEDED | SUPPORTED |
| RC_016 | the OTHER LAYERS table and the complaint count use different units | SUPPORTED |

## RC_010 — the rule against the schema

*readout_count counts positions with a NON-ADVERSARIAL, HELD, RETURNING
channel for condition reports.* HELD maps to `holder == third_party`
and RETURNING to membership in `positions_returning`. NON-ADVERSARIAL
maps to nothing: the schema has no channel-type field. The row itself
supplies one — its OTHER LAYERS table carries a `type` column with
values complaint / inspection / enforcement / readout / remedy, and the
whole correction to v0 is that the count depends on that column. The
distinction the row says it *actually measures* is the one column its
parent schema cannot record; `RC_004`'s shape, arriving from the data
side rather than the falsifier side.

## RC_011 — what the 0.5 is

Under the row's own rule, over its own OTHER LAYERS table: one layer is
readout-typed (NHTSA VOQ) and its return is *"yes, partial"*. Weight
partial at one half and the count is 0.5; count only full returns and
it is 0.0. The delivered 0.5 is therefore the half reading of a
per-position return state, the `[CHOICE 2]` question from
`label-position-test` `LPT_003` on a new field. The parent schema holds
returning positions as a list, so a position is in it or not: transcribed
as delivered and loaded with any trend, the row reads readout_count 1
with declared_count 4. The list has no half, and the instrument cannot
reproduce the row's headline number from the row's own fields. A
per-position return state (y | partial | n) is the missing column.

## RC_012 — refused on the row's own gap

`rate_trend` is a closed vocabulary and the row supplies none — its
STILL NEEDED list opens with the per-VMT crash series that would give
one. The validator refuses the row on that cell; supplying any of the
three values loads it, and none of the three is the row's. The parent
seed cell `up since 2010` was a value; v0.1 withdraws it to a
requirement. That is the correct direction and it means the trucking
row is, today, one cell short of loading.

## RC_013 — five of seven

The row opens *"Every claim below carries a source URL."* Its SOURCES
block has seven entries; five carry a URL and two are deferred in the
document's own words — *cite the current NHTSA complaint page before
use* and *cite ... before use; C3RS IMOU text to be located*. The
trucking count names NHTSA VOQ as its sole readout-typed channel, so
the one number the row exists to produce rests on the deferred entry.
The document flags it itself; the audit records that the flag sits
under the count. The four hosts that do carry URLs refused CONNECT once
each and are recorded, not read.

## RC_014 — a pointer to a section that does not exist

*"The survey that would make it one is in the parent work order
(N4)."* The parent order's ids are H0–H3 and P1–P6. No N4. The nearest
referent by content is the parent's WHAT WOULD MOVE THIS BEYOND CURRENT
REACH bullet on a trucking C3RS pilot, or `zero-sum-curriculum-null`'s
N4, which is an ablation run and not a survey. `LPT_011`'s shape:
a label from another document, or from a draft of this one, carried
into a file where it resolves to nothing.

## RC_015 — the seed cells, renamed

The parent seed row for trucking reads positions *none (NHTSA VOQ =
equipment only)*, intake `3+`, return `0`, trend `up since 2010`. v0.1
reads the same facts as: readout_count 0.5 (VOQ, partial), complaint
count ≥ 3, trend STILL NEEDED. The seed's `3+` was never an intake
count in the schema's sense; it was the complaint-channel count, and
v0.1 says so — *"a different quantity"*. The seed row was the row's own
v0 error in cell form, and the parent order's own P2 (count only
positions whose channel returns) is what the correction applies.

## RC_016 — units

The OTHER LAYERS table types two rows complaint (carrier HR; FMCSA
NCCDB as one row) and one remedy (OSHA STAA). The count block says
complaint_count ≥ 3. Three is reached only by counting NCCDB's two
routes (coercion, harassment) apart, which the CORRECTION section does
and the table does not, or by counting the remedy-typed row as a
complaint, which the table's own typing does not. The table counts
rows and the count counts routes.

## The exclusion stack

`EXCLUSION_STACK_trucking.md` enumerates twelve filters between an
operator holding a readout and that readout entering a record, coded by
mechanism, survival multiplicative, every rate unmeasured. Landed
verbatim; `stack_audit.py` reads it against the row, the parent order,
the schema, and the `uninstrumented` register (imported). Its sources
were not read: all seven hosts refused CONNECT.

| id | claim | status |
|---|---|---|
| RC_017 | P2's definition of RETURN has three disjuncts, and L11 shows they come apart: a settlement is a corrective action that enters no held record, and the schema cannot say which disjunct fired | SUPPORTED |
| RC_018 | the document's arithmetic reproduces from its own figures; the stated percentages sum to 101 and merit reads 22 in one section and 21 in another, both roundings of 21.5 | SUPPORTED |
| RC_019 | survival over twelve layers with zero measured rates is None, and the instrument never defaults an unmeasured layer to 1 | SUPPORTED |
| RC_020 | the row's phantom "(N4)" now has a referent, S4, in this document; S5 is the row's own STILL NEEDED item | SUPPORTED |
| RC_021 | L0 is the row's six-item readout list, item for item; the document restates rather than extends it | SUPPORTED |
| RC_022 | two layers map onto register mechanisms, one partially, and L11 maps onto none of the eight | SUPPORTED |

## RC_017 — the disjunction in P2

The parent order's P2 counts *positions whose channel has a documented
RETURN (a reply, a corrective action, a report entering a held
record)*. Three disjuncts, any one sufficient. L11 states that the
modal success of the complaint channel is a private settlement that
*publishes nothing* and that *the condition that triggered the refusal
does not enter any safety dataset*. A settlement is a corrective action
on the employment matter — disjunct two — and it fails disjunct three.
So a position whose channel returns only through settlements counts as
returning under P2 and delivers nothing to the record the count is
supposed to measure. The schema holds `positions_returning` as a list
and has no field for which disjunct fired; the row's `type` column
(`RC_010`) and this are the same missing column seen from two sides,
since a readout-typed channel is one whose return is disjunct three.
The stack's closing sentence — *a channel whose success condition is a
confidential settlement cannot function as a readout channel* — is
P2's own definition with the disjunction removed.

## RC_018 — the arithmetic

GAO STAA rows: 183 + 32 + 59 = 274. Percentages computed 66.8 / 11.7 /
21.5 against stated 67 / 12 / 22, which sum to 101; L10's per-hundred
67 / 12 / 21 sums to 100, so merit is rounded up in L8 and down in
L10. Of 21, 0.95 × 21 = 19.95 against *~20 settlements, ~1 order*.
*Roughly five to one* is 100/21 = 4.76; L7's *~1-in-5* against N/merit
is 4.64. And 0.5^11 = 1/2048, the number the STRUCTURE sentence points
at. Every stated figure follows from the figures beside it; the
document's own KNOWN LIMITS carry the 2009 date on the source.

## RC_019 — survival with nothing measured

The stack says survival is multiplicative and S3 says no per-layer rate
is published. `survival()` multiplies measured rates and returns None
if any layer is unmeasured; on the delivered stack that is twelve
layers, zero rates, None. A default of 1.0 for an unmeasured layer
would be the most flattering value on a filter, on the field the
document exists to measure.

## RC_020 — the phantom resolves forward

`RC_014` recorded the row's *"(N4)"* as pointing at nothing in the
parent order. The stack's S4 is *per-carrier reply rate to internal
driver technical submissions (board-sampled; identity filter
self-enforcing)*, which is the survey the row's OPEN INSTANCE named
in the same words. S5 is the row's own STILL NEEDED item on NCCDB
filings versus dispositions. The pointer was to a document not yet
written; it now exists under a different id in a different file, and
the row still says N4.

## RC_021 — L0 is the row's list

Six items in the row, six in L0, six matched by content. The stack
restates the readout list rather than extending it, and types it —
*EXCLUSION BY CHANNEL TYPE* — which is `RC_010`'s missing column
named as a filter.

## RC_022 — mechanisms, by import

Against the register's eight: L0 reads as MODALITY (a complaint
instrument in the condition's channel), L2 as PROXY SUBSTITUTION (a
named rule breach stands in for the condition as the filable target),
L5 partially as AUDIT ASYMMETRY (the burden on one side, where the
register's sense is a guard on one side). L11 — the successful outcome
removes the information from the record — fits none of the eight; its
nearest neighbour is `observer-exclusion`'s classification-note
candidate, recorded and filed under a category that is not evidence.
Declared readings, checked against the register's tuple by import.
