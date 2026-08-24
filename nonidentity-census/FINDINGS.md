# FINDINGS

Work order: `WORK_ORDER.md`. Boundary decisions: `BOUNDARY.md` (first-class
result, per the OUTPUT clause). Commands: `REPRODUCE.md`.

T1-T4 in shape-index format. T5 separate, as specified.

**Status vocabulary note.** shape-index defines four statuses: `CANDIDATE`,
`MULTI_DOMAIN`, `CONSTRAINT_IDENTIFIED`, `BROKEN`. Two entries below carry
`NOT_RUN`, which is **not** one of them. `BROKEN` means a shape was tried and
failed; these were not tried. Extending a controlled vocabulary silently is
the failure that repo's `GateType.REPRESENTATION` note records, so the
extension is stated here instead of assumed.

---

## T1 — DETECTION, NOT KEYWORD

```
status             CANDIDATE
provenance         MODEL_SEEDED
flows              abstracts
switches           classification of the main causal claim's subject
gated_on           predicate class of the claim verb
held_constant      field, valence
units              counts; share decided by predicate vs by table
switch_direction   BIDIRECTIONAL
switch_periodicity APERIODIC
gate_type          REPRESENTATION
closure_mode       REPRESENTATIONAL
constraint         none identified
constraint_stated  False
```

### structural layer

Built. `t1_predicate_unit.py`, stdlib, parses under 3.9, `--selftest` PASS.

Three steps, not equally sound, and the module says so before its first line
of code:

| step | method | lexical? |
|---|---|---|
| 1 claim selection | ordered rule, BOUNDARY D0, selects by verb class | no |
| 2 subject extraction | span before first finite verb, head noun | partly — see T1-2 |
| 3 classification | predicate for claim-level nouns, unit table otherwise | **yes, for everything not claim-level** |

### T1-1 — the detector built to escape lexical detection decides most cases lexically

On its own authored known-signal set, n=12:

```
decided by predicate : 2
decided by table     : 10
undecidable          : 0
```

**10 of 12, 83%, decided by a word list.** Only `market` — the one unit
BOUNDARY D2 resolves at the claim rather than at the noun — is decided by
predicate structure, and it is decided twice, once each way, from the same
noun.

The work order's premise is that lexical search fails because the identity
assumption is premise, not vocabulary. Step 3 reproduces that failure for
every head noun not on the claim-level list. The detector reports
`decided_by` per row so the size of the unfixed problem is a number rather
than a caveat.

Repair direction, not taken here: every unit on the D3 table is in principle
claim-level, as D2 argues for `market`. Moving them there requires a
predicate classifier that generalizes past the two hand-written verb sets,
which is not a stdlib heuristic.

### T1-2 — first null-test run scored 6 of 12, and the cause is a defect not a limit

Recorded because the first number is evidence about how the instrument was
built and the second is not.

| run | known-signal recovered | known-null fired | fail class |
|---|---|---|---|
| first | 6/12 | 0/5 | OK |
| after repair | 12/12 | 0/5 | OK |

Four of the six misses had one cause: the finite-verb pattern
`[a-z]+(?:s|ed)` matches plural nouns, so `firms`, `populations`,
`households`, `institutions` were each read as the sentence's verb and the
subject span came back empty. Two more had a second cause: the head noun was
taken from inside a prepositional phrase, so `the rate of transmission`
returned `intervention` and `energy flux through the boundary layer` returned
`layer`.

Both are fixed. Neither was found by reading the code; both were found by
running the null test, which is the argument for having one.

`fail class` reads `OK` on **both** rows. A harness that returns OK at 6/12
and OK at 12/12 is not discriminating between those two states — the
`null-harness` classifier is built to catch a gate that never fires or always
fires, and it does not catch a gate that is half wrong. Recorded against the
harness, not against this detector.

### T1-3 — the selftest found a word carrying two opposite calls

`BOUNDARY.md` D3 files `state, nation, jurisdiction` as identity-bearing and
`equilibrium, steady state` as non-identity. The head noun of both is
`state`. The transcription check between BOUNDARY and the code caught it; the
table was written without noticing.

This is case `021`'s sense substitution operating inside this instrument's
own vocabulary, three files after `021` was audited. Repair is a two-token
table checked before the unigram table, plus an `AMBIGUOUS_HEAD` set that
returns `UNDECIDABLE` for a bare `state` rather than guessing.

### lexical layer

Reported separately and not blended into the above, per shape-index.

The D3 unit table is 60 tokens. Token overlap between the table and any
corpus is a vocabulary operation. It is what step 3 runs on and it is scored
as vocabulary, which is what it is.

### T1-4 — the ground truth is authored by the party that wrote the classifier

12/12 measures internal consistency, not validity. Both the known-signal set
and the classifier were written here, in one sitting. This is
`triad-playground` `TP_003`'s shared-bias result and it is not repaired by
adding cases — only by ground truth from a party that did not write the
detector.

### T1-5 — the verb-first test, run against the first instrument

`BOUNDARY.md` D6, supplied by the operator after `t1_predicate_unit.py` had
run and after T1-1 was reported. Implemented as
`t1_verb_first.py`, selftest PASS. Both instruments run; neither was edited to
match the other.

```
D1/D3 instrument vs D6 verb-first test, n=12
agree 9   DISAGREE 1   CONTESTED 2
```

Six-option tally, and the arms it maps to:

```
BEARER_REQUIRED  5      identity        5
READS_WITHOUT    2      process         5
VERB_CARRIES_IT  3      own arm         2
BOTH_READINGS    2      no observation  0
NO_FRONTING      0
UNGRAMMATICAL    0
```

**The one disagreement is `KS-09`, the niche.** `the niche remained
unoccupied for three seasons`. D1's three-part test fails it on *predicated
on* — the niche is the slot, the occupant is the carrier — so the first
instrument scores it non-identity. D6 fronts it to `remaining unoccupied for
three seasons` and the residue asks *what* remained, so the second instrument
scores it bearer-required.

Both instruments are internally consistent and they disagree about one thing:
whether a slot with a state predicated on it is a carrier. That is a real
question and neither test settles it. Recorded, not resolved.

### T1-6 — a prediction of mine failed, and the data cannot test it either way

Before running the comparison I predicted that the disagreements would fall on
the rows the first instrument decided by word list, and that the rows it
decided by predicate structure would agree. That is the shape T1-1 would
imply.

Measured:

| how the first instrument decided | n | not agreeing |
|---|---|---|
| by table | 10 | 2 (20%) |
| by predicate | 2 | 1 (50%) |

The by-predicate share is **worse**, not better. At n=2 that figure supports
nothing in either direction — which is the actual finding: the prediction was
stated as though the run would test it, and the run cannot. Kept rather than
dropped, because a prediction that turns out untestable by the data it was
made about is information about the design, not about the world.

### T1-7 — a third of the judgements were not made on what the instrument produced

`read_on` was added after the first scored run, when inspecting the residues
showed some answers could not have come from them.

```
judged on RESIDUE          8
judged on CLAIM            1
judged on DROPPED_SUBJECT  3
```

`KS-01` is the `CLAIM` row: `firms with concentrated ownership reduce
investment following the reform` fronts to `concentrating ownership reduce
investment following the reform`, which is not English. The fronter takes its
main verb from `t1_predicate_unit.subject_span`, which read `concentrated` as
the finite verb. The judgement was made on the original claim, which is the
right answer reached by not using the instrument.

So the instrument was used as specified on 8 of its own 12 items. That number
exists only because the field was added; before it, the run looked clean.

### T1-8 — `VERB_CARRIES_IT` is not an option of the verb-first test

All three of its judgements read `DROPPED_SUBJECT`, and that is not an
accident of who judged. **The operation deletes the subject. This option is a
claim about the subject.** `the rate of transmission fell` fronts to `falling
after the intervention`; nothing in that residue says the deleted subject was
a nominalization of `transmit`. You have to look at what was thrown away.

This is the option argued for hardest in the module docstring, on the grounds
that folding it into `READS_WITHOUT` hides an identity framing wearing a noun.
That argument still holds. What does not hold is calling it an option of this
test.

Relocation, not deletion — two forms available and neither taken here:

- a **pre-step**, asked of the subject before fronting, leaving five
  post-fronting options;
- a **conjunction** — residue reads without one AND the dropped subject was an
  event nominalization — which makes it explicitly two observations.

Enforced meanwhile: `--selftest` now fails if any `VERB_CARRIES_IT` judgement
claims to have been read off the residue.

### T1-9 — the morphological proxy recovers a third of the rule

Suffix shape is a property of a token's form rather than membership in a list,
so a proxy built on `-tion` / `-ment` / `-ance` / `-ing` is one step less
lexical than the D3 table. Measured against the recorded judgements:

```
agreement 4/12
```

The two decisive misses are `populations` and `institutions`. Both carry
`-tion`; both require a bearer. Running the other way, `flux`, `rate`,
`market` and `loop` carry no nominalizing suffix and three of the four are
process.

So the rule is not recoverable from word shape either. Elicitation is the
honest implementation, not a fallback taken for want of effort.

### T1-10 — what D6 buys, and what it costs

**Buys:** the lexically-decided share goes from **10 of 12 to 0 of 12**. No
word list is consulted at any point. That is the actual repair to T1-1, and it
came from the operator, not from the instrument.

**Costs:** the discriminator is now one judgement per item, made by one reader
with no second reader and no blind condition. That is not a smaller weakness
than a word list, it is a different one — a word list is at least inspectable
by someone who was not there. `reasoning-dial` `RD_009`'s G-STATE gap now sits
on the load-bearing step.

**And it produces a number the first instrument could not:** `BOTH_READINGS`
at **2 of 12** is the first measure here of how often the question is
genuinely undecidable rather than merely unanswered. Under the binary rule as
given, those two would have gone wherever the reader leaned, unrecorded.

---

## T2 — BASE RATE

```
status             NOT_RUN
provenance         n.a.
flows              (none)
switches           UNSPECIFIED
gated_on           corpus access
held_constant      n.a.
units              n.a.
switch_direction   UNSPECIFIED
switch_periodicity UNSPECIFIED
gate_type          AVAILABILITY
closure_mode       PHYSICAL
constraint         egress policy of the execution environment
constraint_stated  True
```

### T2-1 — not run, and the reason is external and dated

The stratified sample across eight fields requires abstracts. Every bulk
source tried was refused by the environment's network egress proxy:

```
2026-08-23T22:57:24.124Z  connect_rejected  api.crossref.org:443
2026-08-23T22:57:24.358Z  connect_rejected  api.openalex.org:443
2026-08-23T22:57:24.608Z  connect_rejected  export.arxiv.org:443
detail: gateway answered 403 to CONNECT (policy denial or upstream failure)
```

`WebFetch` on `api.openalex.org` returns `EGRESS_BLOCKED`. Web *search*
works; bulk metadata retrieval does not.

**Not approximated.** A sample assembled from search snippets is selected on
searchability, which is a sampling frame chosen on a variable correlated with
the one under test — `UNI_126`'s failure, and the work order's own reason for
building T1 rather than a keyword scan. The reproduction command in
`REPRODUCE.md` runs T2 unchanged from an unblocked host.

### T2-2 — the prediction is untested and one boundary decision already runs against it

T2 predicts non-zero non-identity "only where the substrate forces it
(ecology, thermo, control)." `BOUNDARY.md` D2 files `population` — ecology's
most common unit — as **identity-bearing**, on all three tests. If the
prediction holds when T2 runs, it will hold with ecology's dominant unit
scored against it, which makes it a stronger result than it would have been.
If it fails, D2 is the first thing to check.

### T2-3 — the proposal replaces T2's output, and the first half of it holds

`BOUNDARY.md` D7, relayed after D6 had run. Implemented as `t2_window.py`,
selftest PASS.

A distribution of windows instead of a count of papers. Three things it buys,
and the third is the one that matters most here:

1. **D3's table dissolves.** Every term becomes claim-level, which is what
   D2 argued only `market` was and what T1-1 measured the cost of.
2. **No citation API.** The blocker on the original T2 was bulk abstracts for
   a base rate. A window distribution needs fewer, deeper reads.
3. **The discriminator comes off the reader.** T1-10 recorded D6's cost as a
   single judgement per item with no second reader. A measurement interval is
   printed in a methods section; it is not a judgement at all.

**This is a change to the work order.** T2 as delivered says "Report
proportion non-identity PER FIELD." That output is replaced, not
supplemented, and the original remains unproduced. Flagged rather than
absorbed.

### T2-4 — it names one window and uses two, and its own examples split 2-1

| example, as given | which window | why |
|---|---|---|
| `population ... dissolves at generational rate` | `W_dissolve` | when the term stops denoting the same thing. A property of the world |
| `firm: quarters` | `W_measure` | a quarter is a reporting interval. Firms are not observed to dissolve quarterly, they are observed quarterly |
| `market: the window it's priced at` | `W_measure` | stated as a measurement interval in the proposal's own words |

**Two of three are `W_measure`.** And the requirement attached to the
proposal — *the window has to come from the claim's own measurement
interval* — is that conflation stated as a rule rather than caught by it.

The seed run shows the consequence directly: `P-2` and `P-3` come back
`UNDECIDABLE` because their `W_dissolve` is `NOT_LOCATED`, and it is left
`NOT_LOCATED` rather than back-filled from the interval, which is the error
under audit.

### T2-5 — the ratio is the finding, not the window

`W_measure / W_dissolve`, a `reasoning-gate` G-RES pair:

| verdict | condition | reading |
|---|---|---|
| `CANNOT_HAVE_SEEN_IT` | ratio >= margin | the study is too coarse to have watched the term dissolve. Its identity framing **could not have failed** at this resolution |
| `RESOLVES_IT` | ratio <= 1/margin | sampling well inside the stable regime; the framing is licensed by the apparatus |
| `MARGINAL` | between | inside the declared margin either way |
| `UNDECIDABLE` | either window missing or unbounded | no ratio is computed |

Constructed known-truth pair, and they separate:

```
N-coarse   CANNOT_HAVE_SEEN_IT  ratio=20
N-fine     RESOLVES_IT          ratio=0.05
```

A field where most papers sample far coarser than their unit's dissolution
window is a field where the identity premise is unfalsifiable by the
apparatus in use. That is `null-harness` `CONSTANT_SILENT` at field scale,
and it is a sharper claim than either the original count or a raw window
distribution — it says per claim whether the assumption was *testable*, not
whether it was *made*.

Same shape as `uninstrumented/coupling_audit/provisioning.py`, where bone
collagen is 12.2x too coarse for a seasonal feature, so the coupling
hypothesis cannot fail in that tissue and is reported
`UNASKABLE_IN_THIS_TISSUE` rather than refuted.

### T2-6 — the other reading is coherent and cannot fail

The proposal can be read scale-relatively: the window is the term *as used in
this paper*, so `W = W_measure` by construction. That reading is defensible
and it makes the instrument incapable of returning a negative — every claim
satisfies it, and a paper sampling at the wrong scale for its own unit is
undetectable.

`MF_020`'s shape: a design that cannot emit a result capable of failing its
own falsifier. Both readings are stated in the module; the two-number one is
built because it can.

### T2-7 — two refusals and one disclosed constant

`window()` refuses rather than defaulting, in three places:

- **`generation` is not a unit until a referent is named.** The referents in
  the module's own table span **5.82 orders of magnitude** (human 25 y
  against *E. coli* 20 min, a factor of 657,450). The proposal's
  `generational rate` names none. The figure in the error message is computed
  from the table and `--selftest` fails if the two drift apart — a first
  draft asserted "about seven orders" and was wrong by more than an order.
- **A window with no basis is refused.** A number with no stated source is
  what the module exists to stop.
- **`NOT_LOCATED` and `UNBOUNDED` are separate**, and neither carries a
  value. A term nobody looked up and a term that does not dissolve are
  different findings. Thirteenth instance of that repair in this drop family.

The disclosed constant: `MARGIN = 2.0`, with no basis. It is the same kind of
stipulated threshold `presented-binary`'s `B10` discloses about
`HANDOFF_CEILING`, and it is disclosed here rather than defended. Nothing
establishes that 2x is where "could not have seen it" begins.

`distribution()` additionally refuses stipulated input unless the caller asks
for it, and prints a banner when it does. Every window in the seed is
`STIPULATED`; no methods section was read.

### T2-8 — what it unblocks, and what it does not

**Removes** T2's bulk requirement: no citation API, no stratified thousands.

**Adds** a depth requirement: methods sections, which sit behind more
paywalls than abstracts, not fewer. The egress gate that refused Crossref,
OpenAlex and arXiv would refuse publisher full text at least as often.

**Net:** T2 becomes runnable by hand at small n and remains **not runnable**
at the eight-field stratified scale the work order specifies. A scope change,
not an unblocking, and the work order's stated output stays unproduced either
way.

What would run it: fifty methods sections, eight fields, two numbers and a
basis string each. That is an afternoon for someone with library access and
is not reachable from here.

---

## T6 — WINDOW DECLARATION vs ENTITY READING

`t6_window_declaration.py`, selftest PASS. Boundary file reused, not
re-derived. No column codes intent, and none is inferred anywhere in the
module.

Two instruments supply two columns, kept apart so the EXIT check means
something: `reading` comes from D6 (`BEARER_REQUIRED` → ENTITY,
`READS_WITHOUT` / `VERB_CARRIES_IT` → PROCESS, `BOTH_READINGS` →
UNDETERMINED); `decided_by` is carried forward verbatim from T1's own
classifier. T1's `TABLE` is this work order's `LEXICAL` — the rename is
recorded, not applied silently.

### T6-1 — the null test passes; the columns are not welded

Three rows per cell, hand-built, none is a paper.

```
window       reading         n   LEXICAL  PREDICATE  UNDECIDABLE
YES          ENTITY          3   1        0          2
YES          PROCESS         3   0        0          3
NO           ENTITY          3   3        0          0
NO           PROCESS         3   3        0          0
```

**Off-diagonals built: `YES × ENTITY` = 3, `NO × PROCESS` = 3.** The STOP
condition did not fire. T6 may proceed.

### T6-2 — the off-diagonals are ordinary, which is what makes the test worth running

They were not contrived. A methods section stating quarterly surveys, with
`firms` as the main term and `reducing investment` requiring a bearer, is an
unremarkable economics paper. `Allocation proceeds without any central
coordinator`, with no interval stated anywhere, is an unremarkable
theoretical one. Had either cell needed a strained construction, the
hypothesis would have been measuring one variable twice; neither did.

### T6-3 — the null set as specified is confounded, and the confound is mine

`decided_by` needs **5 of 12** rows moved to make the two window arms carry
identical distributions:

```
NO   arm  {LEXICAL: 6}
YES  arm  {LEXICAL: 1, UNDECIDABLE: 5}
```

The cause is construction, not the world. The `NO` rows were built by reusing
T1's own fixture sentences, whose head nouns (`populations`, `institutions`,
`allocation`, `diffusion`) are all in the D3 table. The `YES` rows were
written fresh, with terms (`transport`, `turnover`, `mixing`, `colonies`)
that are not. So `decided_by` was tracking which rows were copied and which
were typed.

A matched set — the **same three head nouns in both window arms of each
reading** — takes it to **0 of 12**:

```
NO   arm  {LEXICAL: 5, UNDECIDABLE: 1}
YES  arm  {LEXICAL: 5, UNDECIDABLE: 1}
```

**Consequence for the EXIT check:** the null set as specified cannot deliver
a readable `decided_by` baseline, because its exposure and its instrument
column move together for a reason that has nothing to do with the
hypothesis. The fix is a matched design, not more rows. Both sets ship;
`--null` runs the specified one, `--matched` runs the corrected one.

### T6-4 — the first association metric was wrong and reported 0.83 where the truth is 0

The first version took the majority `decided_by` label per window arm over
the total. That returns the **marginal majority rate**, so on the matched
set — where the two arms are identical by construction and the association
is exactly zero — it read `10/12 = 0.83`.

Replaced with a count of rows that would have to change `decided_by` to make
the arms identical: 5 of 12 as-specified, 0 of 12 matched. No coefficient, no
p-value, per the work order.

The wrong number is recorded here rather than dropped, and the module's
docstring carries it too. A metric that reads high on a set built to read
zero is the same failure class as a gate that returns `OK` at 6 of 12
(T1-2), found the same way — by running it on something whose answer was
known in advance.

### T6-5 — one of the UNDECIDABLE values is an extraction defect, not a vocabulary gap

`N-A2`, *"We show that participants who relocated earned more"*, extracts
`main_term = who`. The subject extractor takes the relative pronoun rather
than `participants`, and `who` is in T1's `PRONOUN` set, so the row scores
`UNDECIDABLE`.

So the 5-of-12 in T6-3 is part construction choice and part bug. The bug is
in `t1_predicate_unit.subject_span`, inherited by everything downstream, and
it is left in place rather than patched mid-run — patching the extractor
under an instrument whose output is being measured changes the measurement.

### T6-6 — `AMBIGUOUS` and `UNDETERMINED` never fire

The specified null design is a 2×2 and both are terminal values outside it.
Nothing in the run shows the instrument can emit either — `null-harness`
`CONSTANT_SILENT` on two of the schema's own values, in a work order that
named them terminal precisely so they would not be resolved away.

Recorded, not repaired. Repairing means changing the null test the work order
specified, and the module prints the gap at the end of `--null` rather than
adding cells nobody asked for.

### T6-7 — the real run has zero eligible papers, and not for T2's reason

`eligible_sample()` returns `[]`.

T1's twelve items are authored sentences written in this repo. They have no
methods section and no figure axis, so every row would take `window_source =
NONE` and `window_declared = NO` by construction — **one column constant
across the entire sample**. That is the welded-column failure arriving from
the sample side rather than the concept side, and running it would produce a
2×2 with two empty columns that looked like a result.

The work order permits a `CONVENIENCE` label. Not taken: a convenience sample
still has to be able to vary the exposure, and this one cannot. Bulk sources
remain refused by egress (T2-1), and a snippet sample is refused for the
reason T2 refused it.

### T6-8 — the EXIT condition is unevaluable on constructed data, stated rather than answered

On the matched set:

```
reading x window_declared     3 / 3 / 3 / 3     balanced BY CONSTRUCTION
reading x decided_by          LEXICAL-ENTITY 6, LEXICAL-PROCESS 4,
                              UNDECIDABLE-PROCESS 2
```

The first table carries no information by design and is printed to show that
it does not. The second is measured but sits on rows whose readings were
assigned when the rows were built, so it reports the vocabulary of the
constructed set and not a finding about papers.

The EXIT check — *if reading correlates with decided_by more strongly than
with window_declared, the instrument is the finding again* — needs a sample
where neither column was set by the person building it. That is T6-7's
blocker, unchanged.

**Field is recorded per row and not adjusted for**, per the confound rule.
In the as-specified set the eight fields spread one-per-cell rather than
clustering, which is also a construction property and not evidence about
field convention.

### T6-9 — the spec error is accepted, and the shape it belongs to has two directions

The relaying instance attributes `AMBIGUOUS` / `UNDETERMINED` never firing to
the specification rather than the implementation: two terminal values named,
then a 2×2 with no cell for either. Accepted — nothing in the module could
have emitted them without adding cells the work order did not ask for.

The shape it is placed in needs one distinction kept. The named neighbour,
`anyOf[1].properties.events` being `{"type": "array"}` with no item schema
(`INSTANCE_LOG_INDEX` R26), is a schema that **cannot refuse** anything: its
rejection branch is unreachable. T6's is a schema that **cannot emit** a
value it declares: its emission branch is unreachable. Duals, not the same
shape, and collapsing them loses which end is broken — the fix for one is a
tighter constraint, for the other a wider design.

The shape both belong to: **a declared state with no path to it.** Two
directions, and the direction is part of the finding.

**Third instance not verified here.** The eval-awareness papers "varying the
cue and reporting the condition" are carried as the relaying instance states
them. No such material is in this tree and the literature claim was not
checked, so it is recorded at the same status as `ANC_010` and `HO_005` —
carried, not confirmed, and nothing here rests on it. Two of the three are
verified in this repo; the count of three is theirs.

### T6-10 — the standing step, built, and what it caught on its first run

*"No metric ships without a known-answer run"* is now `tools/known_answer.py`
plus `tests/test_known_answer_gate.py`, in the pairing
`tools/check_gate_drift.py` and `tests/test_gate_drift.py` already use. 67
tests green.

The registry refuses three things, so it is not decorative: a metric with no
cases; a case with no stated basis for its expected value; and **a case set
whose expected values are all equal**, since such a set cannot detect a
constant metric, which is the failure both seeds are instances of.

Three catches on the first run, and none came from reading:

1. **It refused its own seed.** The first `_verdict` case set had two cases
   and both expected `True`. `register()` raised `BadCaseSet` on its own
   rule before any metric was tested. The third case — two constant-fires
   gates, expected `False` — exists because of that refusal and is recorded
   as such in the note.
2. **It pins the real defect in the canonical file.**
   `null-harness/null_harness.py::_verdict` returns `OK` for `TP=0.5` and
   `TP=1.0` alike. `null_harness.py` imports numpy at module scope and numpy
   is not installed here, so `_verdict` is extracted by source text from the
   current file, refused if the extracted source contains an import, and
   recorded `NOT_RUN` with the reason if extraction fails. It extracted, and
   the case fails, pinned.
3. **It caught a transposed number in my own record of an error.** The
   replaced metric's as-specified case was written as `0.83`, which is the
   *matched* set's figure; the real value is `0.92`. Corrected. This is the
   third catch in this exchange and the first on a *record* of an error
   rather than on a metric — the same operation, one level up.

**What it does not do**, stated rather than left to be discovered:

- **It does not find metrics.** Coverage is a hand-kept manifest in the
  test. Deciding whether a function is a metric is not a lexical property of
  its name, and a repo-wide scan for metric-shaped functions would be
  `T1-1`'s word-list failure one level up. The manifest is therefore the
  weak point and is named as one.
- **Enforcement is at test time, not use time.** Nothing in the repo calls
  `require()` in anger, so the gate fires when the suite runs and not while
  a metric is being used. It catches an unregistered metric; it does not
  catch an unrun one at the callsite.
- **The replaced metric is kept runnable** rather than deleted, so its error
  stays checkable rather than only described, and its matched-set case fails
  by design.

---

## T3 — MARGIN CHECK

```
status             NOT_RUN
provenance         n.a.
gated_on           T2 output
constraint         conditional on T2; no non-identity cases exist to log
constraint_stated  True
```

T3 iterates over "every non-identity case found." T2 found none because T2
did not run. The three fields per case — field, inside/outside the funding
and review institutions, survived-into-citation or died — are specified and
unpopulated. Citation survival additionally needs the same blocked APIs.

---

## T4 — EXCLUSION MECHANISM

```
status             CANDIDATE
provenance         MODEL_SEEDED
flows              claims
switches           which unit a claim can predicate on
gated_on           whether the corpus admits a non-carrier subject
held_constant      the language, which admits it
units              n.a. — precondition unmeasured
switch_direction   UNSPECIFIED
switch_periodicity APERIODIC
gate_type          REPRESENTATION
closure_mode       UNSPECIFIED
constraint         none identified
constraint_stated  False
```

### T4-1 — the ordinal is taken; this would be a twelfth, not a ninth

The work order says "may require a ninth mechanism." The register carries
eight, and three more are already proposed against them in this repo:

| n | mechanism | folder |
|---|---|---|
| 9 | CATEGORY WELD | `category-weld/MECHANISM_09.md` |
| 10 | GENERATION CAPACITY REMOVED | `generation-capacity/MECHANISM_10.md` |
| 11 | DERIVATION DISCARDED | `derivation-discarded/MECHANISM_11.md` |

`uninstrumented/coupling_audit` also declined to claim a ninth and took the
ordinal question seriously for the same reason. Any entry from this census
enters at 12.

### T4-2 — tested against all eleven; none applies cleanly, and the closest is refuted by T1's own output

Not force-fitted, per the instruction. Results:

| mechanism | applies? | why |
|---|---|---|
| **STORAGE** — medium cannot hold the shape | **NO, and this is the decisive one** | it is the best-looking candidate and T1 refutes it. `Results show that allocation proceeds without any central coordinator` is ordinary English, was classified `NON_IDENTITY`, and required no new construction. The medium holds the shape. What is at issue is what claims are *made*, not what the medium can *carry* |
| PROXY SUBSTITUTION — enforceable measure displaces the target | PARTIAL | the citable, fundable, and authorable unit is individuated, and that is an enforceable stand-in for the thing studied. Close, and it names a mechanism outside the corpus rather than inside it |
| GENERATION CAPACITY REMOVED | PARTIAL | shape matches — a framing the corpus cannot generate — but mechanism 10 is about a *party* whose generative capacity was removed upstream at a scale it cannot reach, and no party is identified here |
| SCALAR DEMAND — function collapsed to a number | PARTIAL, by analogy only | the analogue would be a relation collapsed to an entity. The existing mechanism is specifically numeric |
| MODALITY, BUDGET BOUNDARY, AUTHORED REFERENCE, AUDIT ASYMMETRY, SCORED AS WASTE, CATEGORY WELD, DERIVATION DISCARDED | NO | none names a missing unit of analysis |

### T4-3 — no twelfth mechanism is proposed, and the reason is the precondition

T4's antecedent is "if the rate is near-zero." T2 did not run, so the rate is
unmeasured. Proposing a mechanism now would file it on an unmeasured rate,
which is `UNI_007` — a mechanism arriving from the instrument side with no
case behind it, unable to sort anything.

The candidate is held, not filed:

```
candidate      UNIT OF ANALYSIS UNAVAILABLE
distinct from  the eight: those exclude a QUANTITY; this excludes the
               CARRIER a quantity would be predicated on
distinct from  9, 10, 11 per T4-2
blocked on     T2
files at       12, if T2 supports it
```

---

## T5 — IDENTITY LOAD DISCRIMINATOR

Separate thread, as specified. Method: four web searches, terms in
`REPRODUCE.md`. Bulk APIs blocked; search available.

### T5-1 — the answer is not "no such comparison exists". It is narrower and more useful

**The design exists, at material effect held constant at zero.** The
minimal-group merger experiments — van Leeuwen, van Knippenberg & Ellemers,
*Personality and Social Psychology Bulletin* 29(6), 2003 — manipulate
perceived continuity of the pre-merger identity and measure post-merger
identification. Minimal groups carry no material stakes by construction, so
material effect is held constant, at zero.

That is the degenerate case of the work order's design. It shows identity
load moves the outcome with material loss absent. It does **not** put the two
models against each other, because at zero material loss the self-interest
model predicts nothing to compare.

### T5-2 — the design at matched non-zero material loss did not surface

Four searches. What came back:

- identity threat as an **outcome** of reform, and as a **moderator** of
  resistance — extensively;
- material self-interest and status-quo bias — extensively;
- both variables in one paper — yes (minority-group resistance, where
  material disadvantage and cultural-identity erosion are noted as coupled);
- **the two varied against each other with material effect held constant at
  a non-zero level — no instance located.**

The nearest available domain is municipal amalgamation, where fiscal outcome
is measurable and identity dissolution is the explicit grievance. The Dutch
comparison located (enforced vs voluntary amalgamation) varies the
**process**, not identity preservation at matched fiscal effect. It is the
right substrate for the design and is not the design.

### T5-3 — a search-based negative is weak evidence, and its weakness is the same one T1 exists for

Four searches over one index, in the vocabulary of whoever indexed it. If
the comparison exists under terms none of the four searches used, this
reports absence, not a result — `UNI_005`. The reason is exactly the work
order's own reason for T1: the design is a *predicate structure* — hold one
term fixed, vary the other — and structures do not announce themselves
lexically.

The falsifier is cheap and stated: one located study varying identity
preservation with non-zero material effect matched across arms refutes T5-2.

### T5-4 — the reform-resistance branch's own weak point, from the same searches

The self-interest and identity-load models are not stated as rivals in the
located literature. They are stated as compounding — material disadvantage
"coupled with" identity erosion. A discriminator needs them to come apart,
and the literature's default framing is that in the field they do not. That
is a reason the design is missing which is not neglect: the cases where they
diverge may be rare in the world, not merely unstudied.

---

## Sources located in T5

- van Leeuwen, van Knippenberg & Ellemers (2003), *Continuing and Changing
  Group Identities: The Effects of Merging on Social Identification and
  Ingroup Bias* — https://journals.sagepub.com/doi/10.1177/0146167203029006001
- van Knippenberg et al. (2002), *Organizational identification after a
  merger: A social identity perspective* — https://pubmed.ncbi.nlm.nih.gov/12133226/
- *Dilemmas of resistance: How concerns for cultural aspects of identity
  shape and constrain resistance among minority groups* —
  https://www.tandfonline.com/doi/full/10.1080/10463283.2023.2176663
- *Strategic coupling of administrative rationality and cultural imaginaries
  in municipal amalgamations* —
  https://www.sciencedirect.com/science/article/pii/S0962629824001768
- *Fiscal outcomes arising from amalgamation: more complex than merely
  economies of scale* —
  https://www.tandfonline.com/doi/full/10.1080/14719037.2023.2174586
- *What determines citizens' attitudes to municipal mergers?* —
  https://www.tandfonline.com/doi/full/10.1080/01442872.2024.2345288

Titles and venues are as returned by search. Not read in full; T5-1's
description of the minimal-group design rests on the search summary and the
paper's title, and is the one claim here that a reader should check before
building on it.
