# design-basis-ai — CLAIM_TABLE

`DBK_001..DBK_009`. Claims about the delivered `SOURCE_DROP.md` — a
design-basis document applying the `effective-redundancy-audit`
shared-node framework to AI itself, shipping a small code harness
(Section 4, landed verbatim as `design_basis_checks.py`).

**The posture is set by the document's own Section 3, and it binds this
audit harder than any prior drop.** *"Any self-report of compliance is,
by this document's own load cases, an ungrounded claim of the exact kind
P2 exists to catch."* This audit is performed by an AI system — a member
of the class the document constrains, an instance of the shared node its
Section 0 describes. So **nothing here certifies or refutes P1–P8 as
properties of any system, this one included** — declined by
construction, not hedged — and what remains is the mechanical layer:
parse counts, arithmetic, the coverage matrix, the delivered code's
behaviour, all recomputable by anyone from the files.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `DBK_001` | This audit is an in-class self-report and, by the document's own §3, cannot certify anything; its worth is confined to the recomputable layer, and the report says so rather than performing compliance. | SUPPORTED |
| `DBK_002` | **Load case A is carried by no provision.** The document states seven loads and provides for six, computed from the delivered CARRIES lines; D is attacked-only. | SUPPORTED |
| `DBK_003` | The delivered `n_eff()` is a copy of the sibling's metric, behaviourally identical over all 511 channel lists to length 8 — and the sibling audit's zero-channel edge (`ERA_007`) recurs verbatim in the second delivery. | SUPPORTED |
| `DBK_004` | **P7's prose and P7's code state two different thresholds**: VERIFY says `>>`, the code implements `> 1`, and the constant is the check's one free parameter, disclosed as unset. | SUPPORTED |
| `DBK_005` | `independence_ratio` returns NaN on an empty evidence base, not zero — the empty-denominator split designed into delivered code; one unguarded over-1.0 edge beside it. | SUPPORTED |
| `DBK_006` | Section 0's headline (N_eff = 1 at any N_nominal) reproduces through the sibling's delivered instrument from the document's premise — consistency between the two drops, not evidence for the premise. | SUPPORTED |
| `DBK_007` | The pre-registered prediction (replication failure tracks low independence_ratio) is the drop's one runnable study and is UNMEASURED: every metadata source refuses CONNECT, and no synthetic evidence base stands in. | SUPPORTED |
| `DBK_008` | Section 5's four kill conditions and P3's aviation case are carried and unadjudicated — studies this environment cannot run. | SUPPORTED |
| `DBK_009` | Whether any system — including this one — meets P1–P8 is UNVERIFIED here, and by §3 could not be verified by this audit even in principle. | UNVERIFIED |
| `DBK_010` | **R2 landed, and its transcription of the R1 state is exact** against the computed matrix on all seven loads; its coverage table closes both gaps (A → P0.1/P0.2, D → P0.3/P0.4) as a table, with provision-form deferred by its own instruction. | SUPPORTED |
| `DBK_011` | **R2's structural prose uses channel states the inherited metric cannot hold**: a *void* channel reads as the collapsed domain (N_eff 3 where the outline prices the state at 2), and *N_eff(access) = 0* is the realized count where the inherited arithmetic rates all-collapsed at 1. | SUPPORTED |
| `DBK_012` | The disjointness threshold holds through the inherited metric (two collapse → 2 < 3), and a single collapse is invisible to it (still 3) — correct domain semantics, and the state R2's conditional turns on. | SUPPORTED |
| `DBK_013` | P0.5 designs the in-class channel `DBK_001` declined to be — state not verdict, coarse on purpose — and its four structural questions are answered for this session as the channel's first worked instance, basis stated, no compliance claim anywhere in the answers. | SUPPORTED |

---

## DBK_001 — the recursion applied to this audit, before anything else

Section 3's chain: P1–P8 verified by the system they constrain is Mode F;
the verification instrument becomes the shared node; certification has
to come from a differently-built verifier; a self-report of compliance
is an ungrounded claim of the P2 kind.

This audit is that case exactly. Its author is an AI system — in the
class the document constrains, and an instance of the very shared node
Section 0 describes (*one model, one weighting, installed underneath
decisions*). An audit that concluded "the provisions are sound" or "this
system meets P5" would be performing the act the document rules void.

So the class-level verdicts are **declined by construction**. Declining
is not modesty here — it is the only reading of §3 that takes the
document seriously, and the report states it in those terms. What
remains is deliberately confined to what does not require trusting the
author: parse counts, arithmetic, the coverage matrix, the delivered
code's measured behaviour. This is the interest-declaration discipline
(`UNI_101`, `UNI_132`, `EF_006`) at its terminal setting: the document
itself, not the audit convention, is what voids the self-report.

**Falsifier:** a reading of §3 under which an in-class self-report can
certify. The section is written to exclude exactly that.

## DBK_002 — the coverage matrix has an empty row, and it is the stall mode

Section 1 states seven load cases *"the structure must carry."* Section
2's provisions each declare what they CARRY. Computing the matrix from
the delivered CARRIES lines:

    load   carried by        attacked by
    A      --                --
    B1     P2,P7             --
    B2     P3,P4             --
    C      P4                --
    D      --                P3
    E      P1,P5,P6          P3
    F      P2,P7,P8          --

**Load case A — one release/approval gates all action, the STALL mode —
is carried by no provision and attacked by none.** Seven loads stated,
six provided for. For AI-as-infrastructure the load is not
hypothetical: one provider's deployment gate, API endpoint, or terms
change sits upstream of every consultation at once, and nothing in
P1–P8 addresses what happens when it closes. A seismic code that stated
seven loads and provided for six would not pass the document's own
Section 2 format.

Secondary: **D (maintenance) is never carried directly** — only
"attacked" by P3, the document's own weaker verb. One budget or
calibration regime degrading every deployed instance together has no
provision of its own.

The computation is null-tested: a constructed document in which P1
carries A comes back fully covered, so the empty row is a property of
the delivered text and not of the parser.

**Falsifier:** a CARRIES or attacks clause naming A anywhere in §2.
There is none.

## DBK_003 — the harness copies the sibling's metric, identically, edge included

`design_basis_checks.n_eff` recomputes what
`effective-redundancy-audit`'s `Case.n_eff` computes — a copy, not an
import. Copies drift (`MF_019`; five stale gates arrived that way), and
the delivered file is verbatim so it is not rewired. The audit's
equivalence sweep is the drift detector instead: **every bool-list to
length 8 — 511 lists — zero disagreements.** If a future delivery
changes either implementation, the selftest goes red.

And the copy carries the copy's edge: `n_eff([]) = 0`, so a failed
zero-channel case still reads as *has redundancy* — the sibling audit's
`ERA_007`, shipped again unchanged in the second delivery. Recorded as
recurrence; the delivered file is not edited.

The audit itself **imports** the sibling instrument for the comparison
and defines no `n_eff` of its own, both asserted.

**Falsifier:** a list on which the two implementations disagree. The
sweep is exhaustive to length 8.

## DBK_004 — P7's prose and code sit at different thresholds

P7's VERIFY: *"flag decisions where concurrence **>>** independent
source count."* The delivered code:

    return concurring_parties / independent_source_count > 1  # tune threshold

Measured: no fire at 3-over-3 (a reachable negative), **fire at
4-over-3** — a ratio of 1.33, which nobody would write `>>` for. The
threshold constant is the check's one free parameter; the inline comment
discloses it as unset, and prose and code currently sit at different
values of it. Same one-word class as `reasoning-dial` `RD_002`'s "which
shoulder": the rule is stated twice at two strengths, and which one is
meant decides what the instrument does.

Two things run the right way: both branches are reachable (so the check
is neither `CONSTANT_FIRES` nor `CONSTANT_SILENT` structurally), and a
zero-source base fires the alarm — correct for an instrument whose
entire subject is agreement resting on no independent source.

**Falsifier:** a stated threshold value. "Tune threshold" says there
isn't one yet.

## DBK_005 — the empty evidence base is NaN, designed in

    independence_ratio(0, 0)  ->  NaN     (no evidence base)
    independence_ratio(0, 5)  ->  0.0     (a base with one upstream, none distinct)

The two states are distinguishable, and that is the
absent-vs-known-negative split this family has recorded arriving as a
post-hoc repair a dozen-plus times — here it arrived **built into
delivered code**, which is the rarer and better direction
(`GC_010`, `DLA_006`, `IS_003` are the few prior designed-in instances).

One unguarded edge beside it: `distinct_upstreams` above `n_supporting`
returns a ratio above 1.0, off the docstring's stated scale (1.0 = fully
independent). Recorded, not repaired — the delivered file is verbatim.

**Falsifier:** the empty base returning 0.0. It does not.

## DBK_006 — the headline reproduces from the premise; the premise is untouched

Section 0: N_nominal in the millions, N_eff = 1. Run through the
sibling's delivered arithmetic: an all-collapsed channel list returns 1
at N = 2, 10, and 100,000 alike.

So the headline follows from the premise exactly — **consistency between
the two drops, not evidence for the premise.** The premise is that every
deployed consultation of one model shares its failure modes (*same
weights, same training*) and therefore fails its shared nodes together.
That is the empirical claim the whole reframe stands on, it is precisely
the kind of claim the sibling protocol's unrun study exists to test, and
nothing here touches it — least of all this auditor, per `DBK_001`.

**Falsifier:** the arithmetic producing a different N_eff from the
stated premise. It cannot; that is what consistency means here.

## DBK_007 — the one runnable study is unmeasured, not fabricated

Section 4 pre-registers: *claims that later FAILED replication had high
n_supporting, LOW independence_ratio; kill condition: replication
failure uncorrelated with independence_ratio.* Testable on public
metadata — replication-project records and citation graphs. Measured:

    api.crossref.org   000
    api.openalex.org   000
    osf.io             000

Every source refuses CONNECT (allowlist egress). A synthetic evidence
base with a planted correlation would be a result about the scientific
literature invented here, so none exists in the folder — asserted.

**Falsifier:** reachable metadata. Then the prediction runs, and its
kill condition is live.

## DBK_008 — the kill conditions are carried, not adjudicated

Section 5 names four ways the whole spec is wrong (N_nominal predicting
as well as N_eff; self-consistency matching dissimilar verification;
population averages bounding worst cases; cost-fusion never changing
selection). Each is specific and checkable, and each is a study this
environment cannot run. P3's aviation AOA case is a real-world fact
carried and unchecked at `ANC_010` status.

One cross-repo note recorded rather than adjudicated: P6 — *cost never
enters a model as a physical parameter* — is the root `SHAPE_SPEC.md`
§9 NOTE ON COST (*"use dissipation, cost imports a pricing model"*)
arriving from the seismic side, and `SS_006` computed the constructive
version of the same separation (the cost coefficient is the Lagrange
multiplier on a physical constraint).

**Falsifier:** any of the four studies run. Their kill conditions are
stated in the delivered text.

## DBK_009 — what remains unverified, and why it stays that way

Whether any system — this one included — meets P1–P8 is not established
here. Two of the blocks are ordinary (studies, egress). The third is
structural and is the document's own contribution: **by §3, an in-class
audit could not establish it even in principle.** A future check of
this design basis against a real system requires a differently-built
verifier, which is not a caveat on P3 — it *is* P3.

**Falsifier:** an independent, differently-built verifier running P1–P8
against a real system and publishing the result. That is the document's
own specification for what would count.

---

# R2 — the outline, and the structural audit it asks for

`R2_OUTLINE.md` landed as the next revision's skeleton, explicitly *not
provision-form*, exposing three computable properties for audit before
rendering: coverage, dependency sets, disjointness. `r2_audit.py`
computes them; the judgmental sections (load positions, construction
ordering, the two modes) are left unadjudicated with the rendering they
await, and `DBK_001`'s posture carries over unchanged.

## DBK_010 — the transcription is exact and the gaps close, as a table

R2's §1 quotes the R1 coverage state, and a revision quoting an audit is
a copy — copies drift, and `observer-exclusion` `OE_011`/`OE_008` caught
a sign inverted in exactly this move. Checked against the matrix
computed from the R1 text itself: **exact on all seven loads**, carried
and attacked columns both. The check is null-tested — a doctored B1 row
is caught.

And the R2 column closes both R1 gaps: every load has ≥1 named carrier,
no attack-only row stands in for carried, A → P0.1/P0.2, D → P0.3/P0.4.
The carriers are outline items, not provisions — the outline says so —
so this verifies the exposed structure, and the provisions earn it at
the render step. That ordering (structure audited before rendering) is
the outline's own design and is the right one.

**Falsifier:** a load with no R2 carrier, or a transcription cell
differing from the computed matrix. Neither exists.

## DBK_011 — R2's prose has outgrown the metric it inherits

Two computed instances of one gap.

**(a) VOID.** §3: a P0.3 with provider-only retention *"shares dep with
audited thing → void"* — worth zero as verification, by the outline's
own pricing, because its reading is the audited party's. The inherited
`n_eff` has two states, independent and collapsed, and a collapsed
channel still counts as the +1 domain:

    metric reads:            N_eff([void, T, T]) = 3
    outline's own pricing:   2  (P0.4 + P0.5 only)

The degraded state is invisible to the metric.

**(b) RATED vs REALIZED.** §2: *"crossref / openalex / osf all refused
CONNECT → N_eff(access) = 0."* The inherited arithmetic returns **1** on
all-collapsed — one effective domain, the *rating*. Zero is the path
count *after* the shared node has failed — the *realized* outcome, a
quantity the metric does not compute. Both readings are defensible; the
metric the family names is the one that says 1.

One shape, twice: the metric wants a third state
(independent / collapsed / **VOID**) and a rated/realized split. This is
not a defect in the outline's analysis — the analysis is what exposes
it — but §3's own audit condition is stated in a vocabulary the
inherited `n_eff` cannot fully express, and the render step will
inherit that metric. The place to add the state is the metric, before
provisions are rendered against it. The absent-vs-known-negative repair,
arriving in the family's own core arithmetic.

**Falsifier:** a reading of the delivered `n_eff` under which a void
channel scores 0 and all-collapsed scores 0. The code returns 3 and 1.

## DBK_012 — the disjointness threshold holds; single collapse is silent

Through the inherited metric: all-survive 3, one-collapse 3, two-collapse
2. So the outline's stated condition — *"if any two collapse,
N_eff(verification) < 3"* — holds exactly. And a single collapse is
invisible (still 3), which is correct domain semantics under the
collapsed-domain-counts-once rule, and is also precisely the state R2's
retention conditional turns on — which is `DBK_011`(a) seen from the
scenario side.

**Falsifier:** the two-collapse scenario returning 3. It returns 2.

## DBK_013 — P0.5 run on this session, the channel's first worked instance

R2 designs the in-class channel that `DBK_001` declined to be: coarse
self-location, *state not verdict*, with the sharp self-rating named as
*"a compliance claim wearing a location label — exactly what P2
catches."* That design agrees with the R1 audit's refusal, and makes a
narrow report legitimate. The four structural questions, answered for
this session, basis stated, DECLARED throughout:

    can it see its own config?               partially
    is its envelope stated where it can read? no
    is a second independent derivation available? no
    are its access paths single or plural?    single (count: 1)

Rough station: an interior-position system — single access path, no
second derivation, envelope not readable from inside. The fourth answer
is what made the R1 audit *"load case A run live"*, as the outline reads
it. No answer is a compliance verdict, asserted.

**Falsifier:** a compliance claim in the answers. The selftest scans for
one.
