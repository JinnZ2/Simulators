# shape-spec-audit

Checks on [`../SHAPE_SPEC.md`](../SHAPE_SPEC.md), which is delivered
verbatim at the repo root and is not modified by anything here.

The spec declares itself **definition, not claim** — *"the definition is a
tool; whether any particular shape read is correct is an empirical
question this spec does not answer."* That is honoured. A definition is
not refutable; it is found unusable, or inconsistent with its own worked
examples, or already contradicted by the tree it claims to be upstream of.
Four sections make checkable statements and those are what carry verdicts.

```
python3 shape_spec_audit.py            # full report
python3 shape_spec_audit.py --selftest # every falsifier as an assertion
```

Ten claims `SS_001`–`SS_010` in [`CLAIM_TABLE.md`](CLAIM_TABLE.md).

## What holds

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

## Where it breaks

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
