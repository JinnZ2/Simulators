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
