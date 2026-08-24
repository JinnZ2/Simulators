# shape-spec-audit

Checks on the root spec family — [`../METHOD_SPEC.md`](../METHOD_SPEC.md)
and [`../SHAPE_SPEC.md`](../SHAPE_SPEC.md) — both delivered verbatim and
modified by nothing here. The folder keeps its original name because links
point at it; it covers both specs and will cover `READING_PROTOCOL.md`
when that arrives.

The spec declares itself **definition, not claim** — *"the definition is a
tool; whether any particular shape read is correct is an empirical
question this spec does not answer."* That is honoured. A definition is
not refutable; it is found unusable, or inconsistent with its own worked
examples, or already contradicted by the tree it claims to be upstream of.
Four sections make checkable statements and those are what carry verdicts.

```
python3 shape_spec_audit.py    # SHAPE_SPEC: the four checkable sections
python3 method_spec_audit.py   # METHOD_SPEC, and what it does to the SS claims
python3 shadow_read.py         # METHOD_SPEC section 4, made decidable
```

Each takes `--selftest`, which runs every falsifier as an assertion.
Seventeen claims in [`CLAIM_TABLE.md`](CLAIM_TABLE.md): `SS_001`–`SS_010`
on SHAPE_SPEC, `MS_001`–`MS_007` on METHOD_SPEC.

## METHOD_SPEC arrived aimed at this folder

Its §1 blocks a misapplication *"observed in AI review of this work, more
than once, including in the session this file was written in"* — the
session that produced the SS claims. That charge is run against them
(`MS_001`) before anything else here.

The blocked error has a stated signature: it applies a **claim-level**
criterion, falsifiability, to a **method-level** object. Classifying the
ten by what their criticism ranges over gives **0 of 10** ranging over the
method — two rules, one worked example, one read, one evidence question,
two facts, three not objections at all. `SS_004`, the closest, aims at
exactly the layer §1 names as the falsifiable one: *"The falsifiable layer
is the INDIVIDUAL READ … See SHAPE_SPEC.md section 4 (removal test)."*

This audit is grading itself against a charge aimed at it and has an
interest in the outcome. The object of each claim is quoted rather than
summarised so a reader who disagrees has something to disagree with, and
nothing in it establishes the charge is wrong about other reviews — it is
a claim about ten claims in one file, and the file is the one being graded.

**§1's central move is correct and is not contested anywhere here.** A
method is not falsifiable and does not need to be; the parallel objection
§1 constructs against the scientific method is indeed one nobody accepts.

## What METHOD_SPEC changes

**`MS_002` confirms `SS_005` in the author's own words, and in stronger
form.** §5 lists what a read is *"NOT upgraded by"*: **"more instances
sharing the geometry without a checked constraint set."** §3 of the same
file then offers seven instances, qualified *"separate runs, no shared
ancestry, same geometry"*, with no constraint set checked for any. `SS_005`
reached this by regrouping the list into three families, which is
hand-assigned; this needs no regrouping — both halves are quoted from one
delivered file and the rule is the author's.

The steelman is real and worth stating: under §2's framing the process ran
the trial, so lightning and dendritic solidification *are* separate trials,
and three replications of one protocol are three trials. The list does two
jobs. For *"does this constraint set reliably produce this geometry"*,
seven is honest. For *"are these the same shape"*, it is not — that is the
thing being claimed.

**`MS_003` sharpens `SS_004` using METHOD_SPEC's own machinery, and the
result is better than what it replaces.** §4's removal test has two
branches, and each spec discounts the one the other leaves standing:

| branch | what it does | discounted by | determinacy |
|---|---|---|---|
| form **differs** — shape disappears | **confirms** | `METHOD_SPEC` §3 | **open set** — "at least one was removed, but not which" |
| form **unchanged** — shape persists | **refutes** | `SHAPE_SPEC` §7 | **bounded** — equifinality, and it must be exhibited |

Disappearance ranges over an open candidate set, by §3's own words.
Persistence ranges over a bounded one: for a shape to survive without its
named constraint, some substitute must be doing that constraint's work,
and a substitute has to be exhibited to be claimed. **So §7's default falls
on the better-determined branch.** The repair is one clause — scope §7 to
disappearance reads, where §3 justifies it, and exclude persistence, where
§4's falsifier lives.

**`MS_007` escalates `SS_008`.** `READING_PROTOCOL.md` is now cited three
times in METHOD_SPEC and once in SHAPE_SPEC, is third in §6's stated read
order, and is referenced **by ordinal** — *"third blocked conflation"* — a
pointer to a numbered item in a file with no items. Both specs are careful
about their own contents; the third file is where both put the rules
governing how they are read, and it is the one not in the tree.

## §4's shadow read, made decidable

The best thing in METHOD_SPEC is §4, and its metaphor is exact enough to
compute with. A tangent to a convex body is a supporting half-plane
`x·u ≤ h`; *"what they are all tangent to"* is the intersection; for a
convex body the intersection over all directions recovers it exactly.
`shadow_read.py` does that, registered in `tools/known_answer.py` under the
standing rule that no metric ships without a known-answer run:

| statements | state | area | known answer |
|---|---|---|---|
| four tangents at distance 1 | `OUTLINED` | 4.000000 | 4, a 2×2 square |
| six tangents about the unit circle | `OUTLINED` | 3.464102 | `2√3`, circumscribed hexagon |
| two opposing statements | `UNDER_OUTLINED` | — | vertical direction unconstrained |
| `x ≤ 0` and `x ≥ 1` | `INCONSISTENT` | — | no object is tangent to both |

Two things fall out that the prose lacks. **A failure mode:** §4 offers one
reading of statements that appear to conflict — *"separate tangents to one
boundary, not competing claims"* — and half-planes can have empty
intersection, in which case there is no boundary and the statements really
are inconsistent. §4 has no cell for that, so every apparent conflict
routes to the reassuring reading. `SS_010`'s shape a second time. **A
completion number:** *"complete when the gaps constrain the object to one
form"* is boundedness, and how far from complete is the **area** — so
under-outlined becomes measured rather than stated.

And one limit the formalisation makes visible rather than creates:
**tangents recover a convex hull and nothing finer.** An L-shape and its
hull have identical support values in **72 of 72** directions, true area
3.0 against hull area 3.5. If the object is non-convex, §4's completion
condition can never be met — by construction, not for want of statements.
Worth knowing before an outline that will not close is read as the reader
not having said enough.

## SHAPE_SPEC — what holds

**§1 is the contribution.** `SHAPE = the constraint set a geometry is a
solution to` makes a previously-unnameable error nameable: porting a
branching form to a system with no flux and no dissipation term is a
category failure, not a weak analogy. §2 registers that failure mode
before anyone commits it — the `photoperiod-claim-harness` `PENDING_EDITS`
move, an alternative written down in advance so a later fix cannot be
retrofitted as foresight.

**§3's step 3 is a real instrument**, and for the reason the spec gives:
a constraint enumeration has no natural stopping rule, so a
completed-looking list is indistinguishable from a complete one, while a
rival geometry that also solves the stated problem is a *positive* signal
that something is missing. Reachable fire branch — `null-harness`'s
property, arrived at from the other direction.

**§9's NOTE ON COST is right and the proof is stronger than the spec
states it.** The published derivation of §4's own exponent minimises
`dissipation + K·volume` with `K` a metabolic cost coefficient — the term
§9 rejects — so whether the exponent survives its removal is a real
question. Computed:

| formulation | ratio |
|---|---|
| `2^(-1/3)` | 0.793701 |
| minimise dissipation at **fixed volume**, no cost anywhere | **0.793701** |
| minimise `dissipation + K·volume` (a cost) | 0.793701 |

Pure dissipation with no second term is strictly decreasing in radius
(`W` runs 1.53e+01 → 1.53e-11 as `r` runs 1 → 1000), so it has no interior
optimum and yields no exponent — the second term is load-bearing. But the
de-costed form returns the same number, because minimising dissipation
*subject to* a fixed volume and minimising dissipation *plus a price on*
volume are one stationarity problem. **The cost coefficient is the
Lagrange multiplier on a physical constraint.** That makes §9's
instruction satisfiable rather than merely preferable, and makes §4's
enclosure framing the better statement of the same physics.

## SHAPE_SPEC — where it breaks

**`SS_002` — §10's "a repo that says SHAPE means section 1" is refuted
here, by §1's own second consequence.** 964 occurrences across 249 files;
a hand-coded sample of seven uses returns six distinct senses, of which
§1's is one. `shape signature` is a sha1 of sorted key names.
`shape ∈ {NEW, FLAT, WALKING}` is an enum tag. `domain-ledger/shapes/`
holds a coverage ledger over a claim. §1 predicts precisely this — *the
names diverge by field* — and §10's enforcement clause assumes the
convergence §1 says does not happen.

The count is raw and no sense was assigned mechanically. A keyword scan
deciding word sense is `nonidentity-census` T1-1's failure, where 10 of 12
judgements came off a word list in the detector built to escape word
lists. The sample is n=7 and is not a rate.

**`SS_003` — §4's removal test is the spec's instrument and its worked
example is not a matched pair.** §4 compares a lung to a river delta and
attributes the form difference to enclosure. §5 uses *the same two
examples* and assigns them to different constraint classes —
internal/uniform vs external/heterogeneous — and says the second is
*"a transcript of terrain"* and must not be read as an optimum. So a
second variable moved with the named one, and §4 requires *"a case where
that constraint is genuinely absent"*, not one where a second constraint
is present.

The repair is already in the document, one section below. §5's delta —
*"branches while it can, routes around what it cannot cut"* — is a
within-case matched pair: one system, enclosure fixed, local substrate
varying. Same failure as `nonidentity-census` T6-3, where a null set's
arms differed in a second variable because of how the rows were built.

**`SS_004` — §6 and §7 point opposite ways about how far to trust a
read.** §4 has exactly one branch that refutes a read: constraint removed,
form unchanged. Reaching it requires an observation that contradicts the
shape, and §7 defaults such observations to instrument error. §4 specifies
its test over *found* cases; §7 disarms it exactly there, leaving the
falsifier reachable for interventions and none of the spec's three worked
examples is one. Meanwhile §6 disclaims the prior that would license §7's
default, in its own words: a *"fit to a residue"*, alternatives *"not in
the record"*, `n = 1` on biospheres.

`uninstrumented/` mechanism 6, AUDIT ASYMMETRY — a guard firing on one
side only — landing on the spec's calibration section. The repair is one
line with a precedent in this tree: `rigidification-sensor/` §0 states its
prior openly and marks it *open to attack*. §7 states a prior and does not
mark it as one.

**`SS_005` — §6's recurrence list counts substrates where independence
needs constraint sets.** Seven items regroup into three families:
laplacian-growth (lightning, crack propagation, dendritic solidification),
transport-under-volume-constraint (vasculature, root systems, mycelium),
erosional-minimum-dissipation (river networks). The tension is with §1,
not with the evidence — §1 says systems sharing a constraint set share a
shape, so two items in one family are one shape seen twice, not two
confirmations. Historical independence is real and is the right claim;
it is just not the quantity that licenses *"separate runs converging."*

The family assignment is hand-assigned and is this finding's weak point.
It has a measured precedent pointing one way: `model-ecology`'s **P2 came
back REFUTED**, a hand-assigned tree predicting 9.07 independent votes
against a spectrum showing 2.48. If that direction transfers, 3 is itself
too high — which runs with the finding rather than against it.

**`SS_009` / `SS_010` — every shape entry in the tree scores 0 of §10's
four required fields, and the label §10 assigns it is the wrong one.**
Four entries found by two structural routes; none carries solving-for, a
constraint list, why-not-the-other-shape, or a removal test. §10 offers
two outcomes — shape entry, or geometry note — and the entry found is
neither, having no geometry to note. It is a coverage ledger over a claim.
The wrong label is the reassuring one: *geometry note* reads as an
incomplete shape entry, when the entry is not on the scale.

Twelfth instance of the absent-vs-known-negative repair in this repo, and
the first where the missing third state is *"this is a different sense of
the word"* rather than *"this was not measured."*

## Two things routed rather than claimed

**§8's open question** — whether a shape's critical point is
scale-invariant or drifts across levels — is correctly marked *"not yet
measured for any shape in this ecosystem."* The nearest existing
instrument is `grounding-layers/temporal_dysrhythmia` (six timescales, μs
to millennia, translator-switch coupling). Routing, not a finding.

**§6's survivorship point** — *"alternative branchings either never
occurred or did not survive, so they are not in the record"* — is the same
structure as `derivation-discarded` `DD_003`'s EIA narrowing and
`UNI_126`'s frame-selected-on-the-variable. Three arrivals at one shape
from three directions, and the spec's is the clearest statement of it.

**`READING_PROTOCOL.md`**, named in §10's see-also, is not in the tree
(`SS_008`). Ninth named-and-absent artifact in this drop family; several
of the prior eight arrived a drop later. This one is load-bearing on the
stance rather than on a measurement — it carries the rule that a repo is
a marker rather than a position under defense, which is what makes an
audit like this one welcome rather than adversarial.

## Note on the arrangement

`SHAPE_SPEC.md` is at the repo root, verbatim, because §10 says *"point at
this file rather than restating it"* and a spec inside an audit folder is
not pointable. That instruction is the `reasoning-gate` `guards.json →
GUARDS.md` convention — one source of truth — and it is the right call
here for a reason this repo has paid for: `measurement-fork` `MF_019`
records seven stale copies of the gate arriving across five drops,
because files bundled into every drop drift and files that live in one
place do not.

Nothing enforces it yet. A copy is detectable by content hash; a
*restatement* is not, and restatement is the failure mode a
point-at-this-file rule invites. What is cheaply detectable is a folder
that uses the word and does not point at the spec — not built here,
recorded as the obvious next guard.

CC0. Stdlib only. Parses under Python 3.9.
