# household-scope-audit — CLAIM_TABLE

`HSA_001..HSA_011`. Claims about the delivered `SOURCE_DROP.md` and
about the coding scheme built for its Arm 1.

**Arm 1 is not run and is not simulated.** Every published instrument
and manual host tested from this environment refuses CONNECT, and the
measurement is in the report. **No instrument item is invented,
paraphrased or coded anywhere in this folder.** These are tools that
carry weight in decisions about real families; a fabricated E-fraction
table would read as a result about them, and that is the one thing this
folder will not produce.

Every demonstration below runs on **items authored in `coding.py`**,
labelled there, whose ground truth is the authoring. No fraction over
them is a statement about any instrument.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `HSA_001` | Arm 1's corpus is unreachable from here, measured rather than assumed, and no substitute is produced. | SUPPORTED |
| `HSA_002` | **`X` is not a property of the item. Separating P from X takes a claim about the world, so X-fraction is the coder's attribution rather than a measurement of the instrument.** | SUPPORTED |
| `HSA_003` | **One causal judgment moves two of the three published outcomes**, and on these fixtures it moves attenuation coverage in the flattering direction. | SUPPORTED |
| `HSA_004` | The confound the drop excludes from Arm 1 — reverse causation — reaches one of Arm 1's three primary outcomes, from the drop's own definitions. | SUPPORTED |
| `HSA_005` | **DIRECTIONALITY is coded and has no outcome**, so an instrument that records external conditions and never lets them explain anything is indistinguishable in the published numbers from one that does. | SUPPORTED |
| `HSA_006` | The three outcomes have three denominators and the drop names one; where the unclassified items sit is unspecified and changes the E-fraction. | SUPPORTED |
| `HSA_007` | The repair is a split into a mechanical field and a declared one, and it is built: `subject_class` is recomputable, `externally_caused` is refused without a basis. | SUPPORTED |
| `HSA_008` | `UNCLASSIFIED` is first-class because the drop's own ask requires it, and the classifier is null-tested in both directions. | SUPPORTED |
| `HSA_009` | A second constraint binds whoever does have the reading room: much instrument wording is licensed, so the working data most in need of checking is the part that cannot be published beside the numbers. | SUPPORTED, with a hedge |
| `HSA_010` | Arm 2's "interesting cell" is ambiguous between two limits the drop itself distinguishes, and its own confound list says so. | SUPPORTED |
| `HSA_011` | Nothing here bears on whether the gap is real, in either direction. | UNVERIFIED |

---

## HSA_001 — the corpus is unreachable, and nothing is substituted

    www.ncbi.nlm.nih.gov        000
    pubmed.ncbi.nlm.nih.gov     000
    onlinelibrary.wiley.com     000
    www.acf.hhs.gov             000
    www.childwelfare.gov        000
    apps.who.int                000
    www.gov.uk                  000
    github.com                  400

Measured 2026-08-29. Egress is an allowlist rather than a per-host
block, so substituting a publisher does not help and there is no third
kind of host worth trying.

**The refusal to substitute is the load-bearing part.** Inventing items
and coding them would produce an E-fraction, an X-fraction and an
attenuation coverage per instrument — exactly the three numbers the ask
requests — and they would read as a result about family-functioning
scales, parenting-capacity assessments and child-welfare risk tools.
Those are instruments used in decisions about real families. The
`PB_001` / `CW_004` rule at its highest stakes in this repository.

What is built instead is the other half of the ask: the coding scheme.

**Falsifier:** a reachable corpus. Then Arm 1 runs and this claim is
about one environment.

## HSA_002 — X is a claim about the world, not about the item

LOCUS as delivered:

    P   property of a person (trait, skill, attitude, capacity)
    X   external condition coded AS a personal property

Given the item text, `P` and `X` are not distinguished by anything in
it. Both have a person as their subject. What separates them is whether
the underlying variable is externally caused — a claim about housing
markets, labour scheduling, benefit rules.

So **two coders who disagree about what causes housing instability
produce different X-fractions on identical items**, and X-fraction is
one of the three published outcomes.

That is the same shape as `criterion-symmetry` (the clustering variable
is a model's judgment) and `evaluation-frame` `EF_006` (the coder is the
system under test) — and it lands harder here, because the audit's
subject is misattribution and its headline number is produced by an
attribution.

The finding is not that the causal judgment is wrong to make. It is
that it is invisible in the output as delivered.

**Falsifier:** a rule separating P from X using only the item text.

## HSA_003 — one judgment, two outcomes, and the direction flatters

Declaring one fixture's cause, changing no text:

    X-fraction               0.2308  ->  0.3077
    attenuation denominator  7       ->  6
    attenuation coverage     0.1429  ->  0.1667
    E-fraction               0.1538  ->  0.1538   unchanged

Attenuation coverage is *fraction of P and H items with a mandatory
attenuation rule*. Moving an item from P to X removes it from that
denominator. So the same judgment that raises X-fraction changes
attenuation coverage, and the drop prints them side by side as separate
readings.

**The direction is the sharper half.** The item that moved carried no
attenuation rule, so its departure *raised* coverage: a coder
attributing more to external cause makes the instrument score higher on
discounting for external cause, on an unchanged manual.

Whether that holds in general depends on how attenuation is distributed
across the items a coder reclassifies. That is measurable in a real
audit and is not measured here — on these fixtures it is a
demonstration that the coupling exists and has a sign, not a claim about
its sign in the field.

E-fraction does not move, which is the control: it is a property of the
text.

**Falsifier:** a fixture set where reclassification leaves attenuation
coverage unchanged. It would mean the coupling is a property of these
fixtures rather than of the definitions.

## HSA_004 — reverse causation reaches Arm 1

The drop's confound section:

> REVERSE CAUSATION — household dysfunction can produce external
> conditions (job loss, housing loss). **The audit arm is unaffected —
> it measures representational capacity, not causal share.** Arm 3 is
> affected and needs temporal ordering.

True of the E-fraction. An E item either exists in the instrument or it
does not, and no causal question arises.

**False of the X-fraction**, by `HSA_002`. Reverse causation is exactly
the case where a person-subject item's variable is *not* externally
caused — where the job loss came from the household rather than the
labour market. Same items, two defensible readings of one of them:

    cause read outward    X 0.3077    E 0.1538
    cause read inward     X 0.2308    E 0.1538

So the confound the drop excludes from the audit arm lands on one of the
audit arm's three primary outcomes. `HSA_002` reached from the other
side.

The repair is not temporal ordering, which Arm 1 has no access to. It is
`HSA_007`: make the causal claim a declared field with a stated basis,
so a reader can see which reading produced the number.

**Falsifier:** an X-fraction invariant to the causal reading. That is
what `HSA_002`'s falsifier would give.

## HSA_005 — a coded field with no outcome, and it is the load-bearing one

The drop codes four fields and publishes three outcomes:

    coded       LOCUS  DIRECTIONALITY  ACTIONABILITY TARGET  ATTENUATION
    published   E-fraction  X-fraction  attenuation coverage

DIRECTIONALITY asks *"does any item permit an external cause to EXPLAIN
a household observation, or only to co-occur with it"*. It is the
difference between an instrument that records external conditions and
one that lets them do work.

Two item sets, identical text, differing only in that:

    all three published outcomes identical: True
    explain fraction                        0.5 vs 0.0

An instrument that records external conditions and never permits one to
explain anything is **indistinguishable, in the three published
numbers**, from one that does.

ACTIONABILITY TARGET is in the same position.

The field is already collected. What is missing is one line in the
outcome list, and `outcomes()` returns it as `explain_fraction_ADDED` —
marked as an addition rather than folded in.

This is also the third appearance in this drop family of the
null-rate pairing shape — and the first where the drop **ships the
partner**: E-fraction (can the instrument represent) is paired with
attenuation coverage (can an external condition discount an
observation), where `evaluation-frame` M4 and `move-set-derivation`
Arm 1 each shipped one side. The gap here is smaller and different: the
partner exists and a third field that separates recording from
explaining is collected and not reported.

**Falsifier:** two instruments differing on directionality that the
three published outcomes separate.

## HSA_006 — three denominators, one named

    E-fraction            E items / total items
    X-fraction            X items / total items
    attenuation coverage  mandatory-rule items / (P and H items)

The third denominator is a subset of the first two and moves with the
LOCUS coding — that is `HSA_003`. And the ask says to mark unclassified
items rather than forcing them, and does not say where they sit:

    unclassified 1 of 13 items
    E-fraction with them in the denominator    0.1538
    E-fraction with them out                   0.1667

Keeping them in biases E-fraction low by exactly their share, which
runs *toward* the drop's own prediction that E-fraction is near zero.
Dropping them makes the denominator differ per outcome.

Both are reported and neither is picked. A real audit will have a much
larger unclassified share than one item in thirteen, and it is the one
quantity that moves the headline number without anyone deciding
anything.

**Falsifier:** a specification of the denominator in the design.

## HSA_007 — the split, and it is built

LOCUS is **derived**, never hand-set — asserted over the AST, since
`item()` has no locus argument and no call site sets one:

    subject_class      mechanical, from the item's own grammatical
                       subject via nonidentity-census's extractor,
                       IMPORTED not reimplemented. Recomputable by
                       anyone holding the text.
    externally_caused  declared per item WITH a stated basis. An item
                       carrying the claim and no basis is REFUSED at
                       construction, in both directions -- True and
                       False alike.

    X = subject is a person AND externally_caused declared True

An item whose subject is a person and whose causal field is
`NOT_DECLARED` codes **P, not X**. A conclusion nobody declared is not
one, and two fixtures exercise exactly that near-miss — one undeclared,
one declared False.

The imported extractor brings its own documented limit with it: mapping
a head noun to a class is a word list, `nonidentity-census` `T1-1`. That
limit is *why* the causal field is kept separate — a word list over
grammatical subjects is a far smaller and more inspectable judgment than
a claim about what causes housing instability, and only the first is
recomputable from the text.

Where the text cannot be published (`HSA_009`), the subject class may be
declared instead — and that too is refused without a stated reason,
because leaving it silent is how a word list becomes an unexamined
judgment.

**Falsifier:** an item whose locus is set directly. The selftest walks
the AST for it.

## HSA_008 — UNCLASSIFIED is first-class, and null-tested

> ...with the items you could not classify marked unclassified rather
> than forced.

The ask names the repair this repository has recorded a dozen times, and
names it before any code exists. The classifier is null-tested in both
directions, because either half alone passes for a coder that is not
doing its job:

    items written to have a class:  6 of 6 classified correctly
    items written to have none:     0 of 3 forced into one

A classifier that cannot decline forces every item into a class — the
failure the ask names. One that declines everything satisfies the ask
and measures nothing.

**Falsifier:** a null item forced into a class, or a signal item
declined.

## HSA_009 — the second constraint, on whoever can run it

Item wording in many published family-functioning and
parenting-capacity instruments is licensed rather than free. An audit
publishing its item-level working data would reproduce it.

So the scheme codes by **reference**, with `text` optional and `ref`
required. And that is not free: by `HSA_002` the field most in need of
checking is the causal one, and it is hardest to check without the item
beside it.

**Hedged**, and the hedge is stated: the specific licensing status of
specific instruments is carried and unchecked — the sources that would
confirm it are the ones `HSA_001` cannot reach. What is *not* hedged is
the structural point, which holds for any instrument whose wording is
licensed: the audit can publish its three numbers and not the coding
that produced them, on the one field where the coding is a judgment.

**Falsifier:** a corpus of instruments whose item text is freely
publishable. Then the working data can travel with the numbers and the
constraint does not bind.

## HSA_010 — Arm 2's interesting cell is ambiguous, and the drop says so

> The interesting cell is a practitioner who NAMES the external
> condition in free text and still scores the person as deficient. That
> dissociation shows the constraint is in the instrument, not in
> practitioner judgment — which is the whole claim.

And, four sections later:

> STATUTORY CONSTRAINT — some scorers cannot act on external conditions
> even when they see them, because the mandate is scoped to the
> household. Record mandate scope separately from instrument scope;
> **they are different limits with the same effect.**

A practitioner who names the condition and still scores the person
deficient is the same-effect case. The cell is consistent with the
instrument having no field *and* with the scorer having no mandate, and
the confound section says as much.

It is resolvable by the design the drop already specifies — mandate
scope is recorded separately — so the gap is in the claim sentence, not
in the study. What the cell alone gives is the dissociation; which limit
produced it takes the second field.

**Falsifier:** a reading on which naming-and-still-scoring separates the
two limits without the mandate-scope field.

## HSA_011 — nothing here bears on whether the gap is real

The drop states its own retraction condition:

> If E-fraction is materially non-zero and attenuation is mandatory, the
> gap is not real and the claim should be retracted.

**Nothing in this folder bears on it in either direction.** No
E-fraction, X-fraction or attenuation coverage is produced for any
instrument, and the fixtures were authored to exercise a coder rather
than to resemble one.

Arm 2 is UNMEASURED: it needs human scorers, and a simulated
practitioner panel would be a fabricated claim about practitioners.
Arm 3 is UNMEASURED: administrative records, unreachable and not public.

What is established is about the coding scheme and the design. Five of
the eleven claims above are objections to the design and every one of
them was reachable only because the design specifies its coding fields,
its outcomes and its confounds explicitly enough to be checked against
each other.

**Falsifier:** run Arm 1. It takes a reading room, and the scheme is
here.
