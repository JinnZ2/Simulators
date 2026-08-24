# CLAIM_TABLE — `shape-spec-audit`

Claims about `../SHAPE_SPEC.md`. The spec is delivered verbatim at the
repo root and is not modified by anything here.

The spec declares itself a **definition, not claim**, and that is honoured:
a definition cannot be refuted, only found unusable or inconsistent with
its own worked examples. Four of its sections do make checkable
statements — §4's worked example, §6's evidence, §9's NOTE ON COST, §10's
two rules — and those are what carries a verdict. §1, §2, §3, §5 and §8
are read as argument, and where the reading is favourable it is recorded
as favourable.

REFUTATION_PROTOCOL: a claim that needs a computation is settled by
`shape_spec_audit.py`. A claim about a document's internal consistency is
settled by quoting both halves. Nothing here is settled by preference.

---

### SS_001 — §1's geometry/constraint distinction is the contribution and it holds

> SHAPE = the constraint set a geometry is a solution to.

The distinction does real work, and the test of that is that it makes a
previously-invisible error nameable: porting a branching form to a system
with no flux and no dissipation term is a *category* failure rather than
a weak analogy, and §2 says so before anyone commits it.

The second consequence in §1 — *"the names diverge by field, the
constraint set does not. Searching by vocabulary returns a null over one
field's dictionary and that null gets read as absence of the structure"* —
is `nonidentity-census`'s T1 result stated in advance and from the other
side. That folder built a detector to escape lexical detection and found
**10 of 12** of its own judgements coming off a word list.

**Status: SUPPORTED.**

---

### SS_002 — §10's "a repo that says SHAPE means section 1" is refuted on this repo, by §1's own second consequence

Measured: **964 occurrences across 249 files.** Hand-coded sample of
seven distinct uses returns **six distinct senses**, of which §1's sense
is one:

| use | sense |
|---|---|
| `shape signature` (sha1 of sorted key names) | data-structure fingerprint |
| "the same shape as `DF_010`" | pattern-across-cases |
| "distribution shape", "shape RMS" | geometry — §1's *readout*, not §1 |
| `shape ∈ {NEW, FLAT, WALKING}` | enum tag |
| `domain-ledger/shapes/` | a coverage ledger over a claim |
| "SHAPE BEING TESTED" (`alignment-under-coupling`) | constraint set — §1 |

The count is **raw**. No sense was assigned mechanically, because a
keyword scan deciding word sense is `nonidentity-census` T1-1's failure;
the sample is hand-coded, n=7, and is not a rate.

What makes this more than a naming complaint: §1 predicts exactly this.
*The names diverge by field.* The spec is upstream of a repo whose
dominant use of the word is a different sense, and the enforcement clause
in §10 assumes the convergence its own §1 says does not happen.

**Falsifier:** a sense census over a larger sample returning §1's sense
in the majority.

**Status: §10's rule REFUTED as a description of this repo. §1 is
strengthened by the same measurement.**

---

### SS_003 — §4's removal test is the spec's instrument, and its worked example is not a matched pair

§4's worked example, in full:

> lung: enclosing volume is fixed and uniform, known in advance.
> branching ratio 2^(-1/3) follows.
> river: no enclosing wall to build. second term absent.
> deltas instead of branching to a fixed ratio.
> → the enclosure constraint is load-bearing. removing it changes the
> form. read survives the test.

§5 uses **the same two examples** and assigns them to different classes:

> INTERNAL / UNIFORM … example: lung enclosure.
> EXTERNAL / HETEROGENEOUS … example: delta meeting hardened rock.
> Do not read an external-constraint geometry as an optimum. It is a
> transcript of terrain.

So the pair differs in the named variable *and* in the constraint class
that §5 says changes what the geometry means at all. The test attributes
the form difference to enclosure alone and cannot, because a second
variable moved with it. §4 requires *"a case where that constraint is
genuinely absent"* and delivers one where a second constraint is present.

Same failure as `nonidentity-census` T6-3, where a null set's two arms
differed in a second variable because of how the rows were built —
found there by counting rows-to-move, found here by reading two sections
against each other.

**The repair is already in the document, one section below.** §5's own
delta — *"branches while it can, routes around what it cannot cut"* — is
a within-case matched pair: one system, enclosure fixed, everything fixed,
local substrate varying. That isolates heterogeneity. A second pair
isolating enclosure at fixed class would complete it.

**Falsifier:** a reading on which the delta and the lung differ in
enclosure only.

**Status: SUPPORTED. The instrument is right; the worked example does not
exercise it.**

---

### SS_004 — §6 and §7 point opposite ways about how far to trust a read, and §7 is the unhedged one

§4 has exactly one branch that can refute a shape read:

> If the form is unchanged, the constraint was not load-bearing and the
> read is wrong.

Reaching it requires an observation of the form *constraint absent, form
unchanged* — which is a read contradicting the shape. §7:

> Where the read contradicts the shape, the default reading is instrument
> error … not a discovery that the shape is wrong.

§4 specifies its test over **found** cases (*"find a case where that
constraint is genuinely absent"*) and §7's default disarms it exactly
there. The falsifier survives for interventions, where the observer
removed the constraint and knows it; all three of the spec's worked
examples are found cases.

A default-to-instrument-error rule is licensed by a strong prior on the
shape. §6 states the prior is weak, in its own words: the exponent is
*"a fit to a residue"*, alternatives *"are not in the record"*, and
*"n = 1 on biospheres"*. The section that disclaims the confidence and
the section that spends it are adjacent.

`uninstrumented/` mechanism 6, AUDIT ASYMMETRY — a guard that fires on
one side only — with the register's own definition landing on the spec's
calibration section.

**The repair is one line and has a precedent in this tree.**
`rigidification-sensor/` §0 states its prior openly and marks it *open to
attack*. §7 states a prior and does not mark it as one.

**Falsifier:** a reading of §7 on which some contradicting read is routed
to the shape rather than the instrument.

**Status: SUPPORTED.**

---

### SS_005 — §6's recurrence list is a count over substrates, and independence has to be a count over constraint sets

The list, seven items: vasculature, river networks, lightning, root
systems, mycelium, crack propagation, dendritic solidification —
*"different substrates, different materials, no shared ancestry between
most of them, same geometry. Separate runs converging."*

Grouped by constraint set rather than by material:

| family | items |
|---|---|
| laplacian-growth | lightning, crack propagation, dendritic solidification |
| transport-under-volume-constraint | vasculature, root systems, mycelium |
| erosional-minimum-dissipation | river networks |

**7 items, 3 families** — an upper bound on N_eff, not a measurement of
it, since the families could themselves be related.

The tension is with §1, not with the evidence. §1 says two systems
sharing a constraint set **share a shape**. So lightning and dendritic
solidification are not two confirmations of a shape; they are one shape
seen twice. Historical independence is real and is the right thing to
claim — nobody copied — but the quantity that licenses "separate runs
converging" is independence *of constraint set*, and the list is grouped
by the wrong variable.

`model-ecology/phylogeny.py` computes exactly this statistic (`N_phylo`
vs `N_empirical`, participation ratio of the correlation spectrum with a
permutation null on family labels). The family assignment here is
**hand-assigned** and is the finding's weak point; it is stated per item
in the module so it can be argued with rather than inherited.

And that weak point has a measured precedent pointing one way. The single
place in this repo where a hand-assigned family tree was checked against
a spectrum, `model-ecology`'s **P2 came back REFUTED**: the tree predicted
9.07 independent votes and the spectrum showed 2.48 — *"the tree is wrong.
The spectrum is not."* A hand-assigned tree overstated independence by a
factor of nearly four. If that direction transfers, **3 is an upper bound
that is itself too high**, which runs with this finding rather than
against it — so the honest form is that 3 bounds the list from above and
nothing here bounds it from below.

**Falsifier:** a derivation showing the three families are not reducible
to one another *and* that within-family members differ in a load-bearing
constraint.

**Status: SUPPORTED. The direction of §6's argument survives; the count
overstates it.**

---

### SS_006 — §9's NOTE ON COST is right, and the proof is a duality it does not state

> Cost is an abstraction with no fundamental basis in the physics. The
> measurable quantity is DISSIPATION … Use dissipation.

The published derivation of §4's own exponent (Murray) minimises
`dissipation + K·volume`, where `K` is a metabolic cost coefficient — the
term §9 rejects. So the exponent's survival is a real question. Computed,
symmetric bifurcation, Poiseuille:

| formulation | ratio |
|---|---|
| `2^(-1/3)` | 0.793701 |
| minimise dissipation at **fixed volume**, no cost anywhere | **0.793701** |
| minimise `dissipation + K·volume` (a cost) | 0.793701 |

And pure dissipation with no second term at all is strictly decreasing in
radius (`W` = 1.53e+01 → 1.53e-11 as `r` runs 1 → 1000), so it has no
interior optimum and yields no exponent. The second term is load-bearing.

**But the de-costed form returns the same number**, because minimising
dissipation *subject to* a fixed volume and minimising dissipation *plus a
price on* volume are one stationarity problem. The cost coefficient is the
Lagrange multiplier on a physical constraint — which is why §9's
instruction is satisfiable rather than merely preferable, and why §4's
enclosure framing is the better statement of the same physics.

Same move as `equivalence-field/`'s push to intensive variables and
`earth_economics`'s thermodynamic auditor: a price is a multiplier on a
constraint, and naming the constraint is strictly more informative.

**Falsifier:** a flow-network exponent that the constrained form cannot
reproduce without a price term.

**Status: SUPPORTED, and stronger than the spec states it.**

---

### SS_007 — §3's step 3 is a real instrument and the worked example works

> galaxy is spiral, vasculature is dendritic. both distribute across an
> extent. ask: why is the galaxy not dendritic. recover: angular momentum.

The move is sound and the recovered term is the right one. What makes
step 3 an instrument rather than a heuristic is the property the spec
names: *"Steps 1 and 2 can be done wrong and still look finished; step 3
fails loudly."* A constraint enumeration has no natural stopping rule and
a completed-looking list is indistinguishable from a complete one; a
rival geometry that also solves the stated problem is a **positive
signal** that something is missing, which is the `null-harness` property
of having a reachable fire branch.

§2's BLOCK THIS MISREAD is the same discipline earlier: the failure mode
is registered before anyone commits it, which is
`photoperiod-claim-harness`'s `PENDING_EDITS` shape — the alternative
written down in advance so a later fix cannot be retrofitted as foresight.

**Status: SUPPORTED. The honest positive.**

---

### SS_008 — `READING_PROTOCOL.md` is named in §10 and is not in the tree

> see also: READING_PROTOCOL.md — every repo is a marker for a sensed
> shape needing exploration, not a position under defense

Not present anywhere in the repository. The ninth instance of a
named-and-absent artifact in this drop family (`CW_001`, `PB_001`,
`GC_009`, `PB_015`, `MD_001`, `DL_014`, `UNI_105`, `MF_020`), several of
which arrived a drop later.

Distinguishing feature: this one is load-bearing on the *stance* rather
than on a measurement. §10 routes the reader to it for the rule that a
repo is a marker rather than a position, and that rule is what makes an
audit like this one welcome rather than adversarial.

**Falsifier:** its arrival.

**Status: UNVERIFIED — a gap, not a defect.**

---

### SS_009 — every shape entry in this tree scores 0 of §10's 4 required fields

> a shape entry should carry: solving-for, constraint list,
> why-not-the-other-shape, and the removal test from section 4

Four entries found, by two structural routes (a file under a `shapes/`
directory, or a JSON object with a top-level `shape` key — neither is a
word list, so this is not `T1-1`):

| entry | solving-for | constraints | why-not-other | removal test | score |
|---|---|---|---|---|---|
| `domain-ledger/shapes/hierarchy-cut-generation.json` | absent | absent | absent | absent | **0 of 4** |
| `domain-ledger/anchors/hierarchy-imposed-ordering.json` | absent | absent | absent | absent | **0 of 4** |
| `domain-ledger/samples/skeleton.sample.json` | absent | absent | absent | absent | **0 of 4** |
| `domain-ledger/samples/anchor_skeleton.sample.json` | absent | absent | absent | absent | **0 of 4** |

This is `MF_017` / `CW_015` / `DL_004` / `GC_012` / `UNI_013` again — a
stated rule with no schema slot — and the eleventh instance. Cheaper here
than in most of them, because the spec arrived *after* the schema and
nothing has yet been written to it.

**Falsifier:** any entry scoring above 0. `--selftest` fails if one does.

**Status: SUPPORTED.**

---

### SS_010 — §10's two-state outcome has no cell for the state that actually occurs

> an entry missing the removal test is a geometry note, not a shape
> entry; mark it as such

Two outcomes are offered: **shape entry**, or **geometry note**. The
entry found is neither. `hierarchy-cut-generation.json` has no geometry to
note — it is a coverage ledger over a claim, with a domain set, a
reservation and a pre-registered coding criterion. It uses the word in
`SS_002`'s fifth sense.

So the classification returns the wrong label rather than no label, and
the wrong label is the *reassuring* one: "geometry note" reads as a
shape entry that is merely incomplete, when the entry is not on the scale
at all. Twelfth instance of the absent-vs-known-negative repair this repo
has now recorded across `PB_004`, `PB_012`, `GC_004`, `MD_002`, `GC_010`,
`DL_008`, `CC_002`, `CA_002`, `ACL_004`, `UNI_021`, `SHB_009` — and the
first where the missing third state is *"this is a different sense of the
word"* rather than *"this was not measured"*.

Repair, in the spec's own vocabulary: a third outcome, **not a shape
entry** — the entry does not name a geometry, so §10's fields do not
apply and forcing them would produce a picture that matches and a claim
that is empty, which is §2.

**Falsifier:** a reading of §10 on which `hierarchy-cut-generation.json`
is correctly labelled a geometry note.

**Status: SUPPORTED.**
