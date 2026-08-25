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

`METHOD_SPEC.md` arrived after `SS_001`–`SS_010` were written, and §1 of
it blocks a misapplication it says was observed *"in the session this file
was written in"* — this one. `MS_001` runs the ten claims against the
stated criterion and is declared as self-grading. Three SS claims move on
contact with the second spec and all three are marked in place.

REFUTATION_PROTOCOL: a claim that needs a computation is settled by
`shape_spec_audit.py` or `shadow_read.py`. A claim about a document's internal consistency is
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

**SHARPENED BY `MS_003` on `METHOD_SPEC.md`'s arrival.** That spec supplies
the asymmetry this claim was missing, and it runs the other way from §7's
default: §3's UNDERDETERMINED DISAPPEARANCE discounts *disappearance*,
which is §4's **confirming** branch, while §7 discounts *persistence*,
which is §4's **refuting** branch. Persistence is the better-determined of
the two. Read `MS_003` for the current form; this claim's substance is
unchanged and its statement is superseded.

**Status: SUPPORTED, superseded in form by `MS_003`.**

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

**CONFIRMED BY THE AUTHOR'S OWN LATER RULE.** `METHOD_SPEC.md` §5 lists
what a read is *"NOT upgraded by"*: **"more instances sharing the geometry
without a checked constraint set."** That is this claim as a rule. §3 of
the same file then offers the same seven items, qualified *"separate runs,
no shared ancestry, same geometry"*, with no constraint set checked for
any of them. See `MS_002`.

**Status: SUPPORTED. The direction of §6's argument survives; the count
overstates it, and §5 of the companion spec says so.**

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

**ESCALATED.** `METHOD_SPEC.md` cites it three more times, makes it third
in §6's stated read order, and references it **by ordinal** — *"See
READING_PROTOCOL.md, third blocked conflation"* — a pointer to a numbered
item in a file with no items. See `MS_007`.

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

---
---

# `MS_001`–`MS_007` — claims about `METHOD_SPEC.md`

The file is delivered verbatim at the repo root and is modified by
nothing here. It declares itself a statement of **epistemic class**, and
§1's central move — *a method is not falsifiable and does not need to be*
— is correct and is not contested anywhere below. The scientific method,
syllogistic logic and dimensional analysis are indeed not falsifiable, and
the parallel objection §1 constructs (*"the scientific method always
resolves to 'the experiment was confounded'"*) is indeed one nobody
accepts.

What follows is about the two specs' fit with each other, plus one
instrument the file's own §4 turns out to specify.

---

### MS_001 — none of the ten SS claims ranges over the method; declared as self-grading

§1 blocks a misapplication *"observed in AI review of this work, more than
once, including in the session this file was written in"* — the session
that produced `SS_001`–`SS_010`. The charge has a stated signature: it
applies a **claim-level** criterion (falsifiability) to a **method-level**
object. So the test is what each claim's criticism ranges over.

| claim | ranges over | object |
|---|---|---|
| `SS_001` | not an objection | records §1's distinction as the contribution |
| `SS_002` | a rule | §10's naming rule, measured on this repo |
| `SS_003` | an example | §4's lung/delta worked example |
| `SS_004` | **a read** | §7's default, against §4's refuting branch |
| `SS_005` | evidence | §6's recurrence list, as evidence |
| `SS_006` | not an objection | computes that §9 is right |
| `SS_007` | not an objection | records §3 step 3 and §2 as sound |
| `SS_008` | a fact | whether a named file is on disk |
| `SS_009` | a fact | key sets on four JSON entries |
| `SS_010` | a rule | §10's two-state outcome |

**Ranging over the method: 0 of 10.**

`SS_004` is the one to look at, and it aims at exactly the layer §1 names
as the falsifiable one: *"The falsifiable layer is the INDIVIDUAL READ,
not the method. See SHAPE_SPEC.md section 4 (removal test)."* `SS_004`
says §7 discounts §4's refuting branch — a claim **about the removal
test**, not a demand that the method refute itself. METHOD_SPEC makes it
heavier rather than lighter, by placing all the refutation weight there.

**Declared:** this audit is grading itself against a charge aimed at it and
has an interest in the outcome. The object of each claim is quoted rather
than summarised so a reader who disagrees has something to disagree with,
and the classification is hand-coded, which `--selftest` states rather
than hides. **Nothing here establishes the charge is wrong about other
reviews** — it is a claim about ten claims in one file, and the file is
the one being graded.

**Falsifier:** any SS claim whose criticism ranges over the method.
`--selftest` fails if the classification finds one.

**Status: SUPPORTED, with the interest declared.**

---

### MS_002 — §5 forbids what §3 does, which confirms `SS_005` in the author's own words

§5, under WHAT A READ IS WORTH:

> **NOT upgraded by** more instances sharing the geometry without a
> checked constraint set

§3, under n=1 ON SOME DOMAINS:

> recurrence ACROSS SUBSTRATES inside that one instance is what carries
> the weight — vasculature, rivers, lightning, roots, mycelium, cracks,
> dendritic solidification: **separate runs, no shared ancestry, same
> geometry.**

Seven instances, qualified by *same geometry*, with no constraint set
checked for any of them. §5's rule disqualifies §3's evidence.

`SS_005` reached this by regrouping the list into three constraint
families and is the weaker statement, because the regrouping is
hand-assigned. This one needs no regrouping: both halves are quoted from
one delivered file and the rule is the author's.

**The steelman, which is real.** Under §2's own framing — the process ran
the trial, n enormous — lightning and dendritic solidification *are*
separate trials, and three replications of one protocol are three trials,
not one. That is right, and it means the list does two different jobs
needing two different counts. For *"does this constraint set reliably
produce this geometry"*, seven is the honest count. For *"are these the
same shape"*, it is not, because that is the thing being claimed and
counting instances of it assumes the conclusion. §3 and §6 use the list
for the second job.

**Falsifier:** a constraint set checked and stated for two items §3 lists
under different substrates.

**Status: SUPPORTED.**

---

### MS_003 — the two specs' asymmetries run opposite, and §7's default falls on the better-determined branch

`SHAPE_SPEC` §4's removal test has two branches:

| branch | what it does | discounted by | determinacy |
|---|---|---|---|
| form **differs** — the shape disappears | **confirms** the read | `METHOD_SPEC` §3 | **open set** — "at least one was removed, but not which" |
| form **unchanged** — the shape persists | **refutes** the read | `SHAPE_SPEC` §7 | **bounded** — the alternative is equifinality, and it has to be exhibited |

`METHOD_SPEC` §3: *"A shape DISAPPEARING tells you at least one was
removed, but not which. Disappearance is informative and
underdetermined."* That discounts §4's **confirming** branch, and it is
correct.

`SHAPE_SPEC` §7: *"Where the read contradicts the shape, the default
reading is instrument error."* That discounts §4's **refuting** branch.

So each spec discounts the branch the other leaves standing — and the two
branches are not equally determined. Disappearance ranges over an open
set of candidate removals, by §3's own words. Persistence ranges over a
**bounded** set: for a shape to survive without its named constraint,
some substitute must be doing that constraint's work, and a substitute has
to be exhibited to be claimed. **§7's default therefore falls on the
better-determined of the two.**

This is the sharpened form of `SS_004`, and it is sharper because
`METHOD_SPEC` supplied the machinery. `SS_004` could say only that §6
disclaims the prior §7 spends; this says which branch the discount belongs
on.

**The repair is one clause:** scope §7's default to **disappearance**
reads, where §3 supplies the justification, and exclude **persistence**
reads, where §4's falsifier lives. `rigidification-sensor/` §0 remains the
precedent for the second half — state the prior and mark it open to attack.

**Falsifier:** an argument that persistence-under-removal is at least as
underdetermined as disappearance — which would need the substitute
constraint's candidate set to be unbounded in the way the removed one's is.

**Status: SUPPORTED, and supersedes `SS_004`'s statement.**

---

### MS_004 — §2's natural-experiment argument is sound and has a literature this session cannot reach

> the difference between this method and conventional experiment is WHO
> RAN THE TRIAL, not whether a trial was run.

The structural argument holds as stated, and the trade it names —
control against trial count, in opposite directions, *"neither is the
mature form of the other"* — is the right shape. Nothing here contests it.

It is also not novel, which strengthens it: this is the standing position
of the **historical sciences** (geology, paleontology, evolutionary
biology, cosmology), and the argument that they are not epistemically
inferior to experimental science is a developed one — Carol Cleland's work
on historical vs experimental method is the nearest match carried in
memory, with a *smoking gun* asymmetry that would bear directly on
`MS_003`: traces of a past event tend to be **over**determined, many
traces to one cause, which is why historical science can be decisive.

**Not verified from here.** The egress gate refuses the sources that would
check it, and this repo's standing convention on unreachable literature
(`ANC_010`, `CD_009`, `RD_015`, `HO_005`) is to mark it rather than assert
it. Nothing in this audit rests on the attribution.

**It is watchable rather than merely unverified.** `notes/study_watch.py`
runs on a GitHub Actions runner precisely because the runner reaches
Crossref, OpenAlex and arXiv. §2's claim is a literature question with a
retrievable answer, and it is the first item in this drop family that the
watcher was built for.

**Falsifier:** the retrieval. Either the historical-science literature says
this, or it does not.

**Status: UNVERIFIED — a gap with a named instrument pointed at it.**

---

### MS_005 — §4's shadow read supplies the test it says it lacks, and one limit it does not mention

> the shape is not pointed at directly. It is described by the GAPS IT
> CASTS. Each statement is one gap. The object is what they are all
> tangent to.

The metaphor is exact enough to compute with. A tangent to a convex body
is a supporting half-plane `x·u ≤ h`; *"what they are all tangent to"* is
the intersection; and for a convex body the intersection over all
directions recovers it exactly. `shadow_read.py` does this, registered in
`tools/known_answer.py` under the standing rule:

| statements | state | area | known answer |
|---|---|---|---|
| four tangents at distance 1 | `OUTLINED` | 4.000000 | 4, a 2×2 square |
| six tangents about the unit circle | `OUTLINED` | 3.464102 | `2√3`, circumscribed hexagon |
| two opposing statements | `UNDER_OUTLINED` | — | vertical direction unconstrained |
| `x ≤ 0` and `x ≥ 1` | `INCONSISTENT` | — | no object is tangent to both |

**Two things fall out that the prose lacks.**

*A failure mode.* §4 offers one reading of statements that appear to
conflict — *"separate tangents to one boundary, not competing claims"* —
and a set of half-planes can have empty intersection, in which case there
is no boundary and the statements really are inconsistent. §4 has no cell
for that, so every apparent conflict routes to the reassuring reading.
This is `SS_010`'s shape a second time: a two-state classification whose
missing third state is the unflattering one.

*A completion number.* *"Complete when the gaps constrain the object to
one form"* is the intersection being bounded; how far from complete is its
**area**. Under-outlined stops being a stated state and becomes a measured
one — which is what §5's confidence readout would need to move a marker on
this read path.

**And one limit the formalisation makes visible rather than creates.**
Tangents recover a **convex hull** and nothing finer. Demonstrated: an
L-shape and its hull have identical support values in **72 of 72**
directions, true area 3.0 against hull area 3.5. So if the object is
non-convex, §4's completion condition can **never** be met — not for want
of statements, by construction. Worth knowing before an outline that will
not close is read as the reader not having said enough.

**Falsifier:** a formalisation of "gaps cast" on which two statements
cannot be jointly unsatisfiable. `--selftest` fails if `INCONSISTENT`
becomes unreachable in the fixtures.

**Status: SUPPORTED. The section is right that the read path exists and
does not state what closes it or what breaks it.**

---

### MS_006 — §3's SUBSTRATE EXCLUSION cross-reference lands, on a subfolder rather than the mechanism list

> Human exceptionalism is exactly this defect: humans excluded as an
> admissible domain … Cross-references the exclusion mechanisms in the
> `uninstrumented` repo.

It resolves, and to something more specific than the eight-mechanism list.
`uninstrumented/coupling_audit/` already runs a **`species` gate** mapped
to **`AUDIT_ASYMMETRY`**, with three seed entries — and §3's example is
the same gate pointed the other way. There, companion animals are excluded
from a human food-security accounting. Here, humans are excluded from a
cross-species density comparison. One gate type, two directions, and
neither side notices because the exclusion is upstream of the reading in
both.

The termite comparison §3 names is the coupling audit's own open question
in a different substrate: a quantity that could be registered, machinery
that exists, and an agent it is not run on.

**Falsifier:** a reading on which human exceptionalism is one of the eight
named mechanisms rather than the subfolder's `species` gate.

**Status: SUPPORTED.**

---

### MS_007 — `READING_PROTOCOL.md` is now load-bearing on two specs and referenced by ordinal

Cited **three times** in `METHOD_SPEC.md` and once in `SHAPE_SPEC.md`.
Third in §6's stated read order. And §4 references it by **ordinal** —
*"See READING_PROTOCOL.md, third blocked conflation"* — a pointer to a
numbered item in a file with no items.

Escalated from `SS_008`. It now carries: marker status (§5's *"a read is a
MARKER, not a result … Do not resolve it in either direction on its
behalf"* is attributed to it), the blocked conflations (§4 depends on the
third one), and the ecosystem-wide scope claim.

The two specs delivered so far are careful about their own contents. The
third file is where both put the rules governing how they are read, and it
is the one not in the tree.

**Falsifier:** its arrival.

**Status: UNVERIFIED. A gap, and the largest one in the family.**
