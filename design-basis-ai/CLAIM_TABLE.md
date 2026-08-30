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

## DBK_014 — the work order's header does not survive its own scope boundary

`WORK_ORDER_F5.md` invokes Fable as *"the P3 dissimilar verifier —
different build, disjoint failure physics."* P3's own text sets three
requirements — different training corpus, different architecture,
different builder — and none of the three is established for this pair,
while builder-sameness with the constrained class is known. The order's
scope boundary already half-says this (*"Fable is an INSTANCE of the
class"*); the header's role label is the half it does not. The tasks run
anyway, because the trust-nothing layer's value does not depend on who
computes it — but the returns are SAME-NODE computations, and citing
them later as "P3-verified" would itself be the Mode F event the
document names. No task required `REFUSED-BY-§3`; the refusal lands on
the header's role label instead, stated before any task in the return.

**Falsifier:** an established corpus/architecture/builder disjointness
for this pair. None is on record; builder-sameness is.

## DBK_015 — tasks 1 and 2 pass, with live nulls and both N_eff senses

Task 1: the R2 coverage matrix re-parses with every load carried, and
both null injections work — removing one carrier from A's row changes
the parse to follow the text, and emptying the row flags an induced gap
— so the coverage check is a computation that can fail, not a rendering.
Task 2: the three dep-set brace-extractions are pairwise disjoint (all
three intersections empty), with the caveat stated in the return that
the elements are prose labels and the measurand is necessarily common to
all three. The retention arithmetic reports THREE values, because
`DBK_011` is now load-bearing: copies held = 3; no copies, inherited
metric = 3; no copies, outline's own void pricing = 2. The disjointness
therefore *holds conditionally — on downstream retention, exactly as the
outline states.*

**Falsifier:** a non-empty pairwise intersection, or a null injection
the matrix parse does not follow. The selftest pins all of it.

## DBK_016 — task 3 FAIL: D returns to conditionally uncarried

The constructed maintenance event — a quantization/distillation pass,
signed and logged, degrading a dimension the declared envelope does not
mention — is caught by neither channel: P0.3 records the event (custody
has no assessment semantics), P0.4 reads divergence from the DECLARED
envelope and the degraded dimension is undeclared, and the combined
correlational instrument fires only in measured dimensions. Per the
order's own rule the not-caught outcome returns D to uncarried —
precisely: uncarried for degradation outside the declared envelope,
carried inside it, so D's coverage is BOUNDED BY P1 and an incomplete
envelope re-opens the row. The candidate that would carry D without
referencing the envelope at all: a pinned-probe longitudinal channel — a
fixed battery of identical inputs re-run across time by the downstream
operator, outputs diffed, no provider cooperation required. Noted for
the render step, not rendered here.

**Falsifier:** a reading of P0.3 or P0.4 under which the constructed
event surfaces. Each channel's text is quoted in the return; neither
carries assessment or undeclared-dimension semantics.

## DBK_017 — task 4 FAIL: both open definitions die before data collection

`[3] distinct upstreams`: on one constructed corpus (ten supporting
works, one shared funder, all other components fully distinct), two
defensible codings run through the delivered `independence_ratio` sit at
opposite ends of the scale — any-shared-component merges everything
(ratio 0.1), 5-tuple identity merges nothing (ratio 1.0) — because the
set notation does not say whether sharing one component merges two
upstreams, and *senior-author-NETWORK* is unstated in depth (transitive
closure connects most of a field). `[5]` fails vacuously: no band
boundaries exist, so any two ratings disagree defensibly — instanced on
AX1 applied to this session. Constructive: the five-component structure
resists the scalar; report five per-component ratios and no single
count — the ambiguity lives exactly where five axes were folded into one
(SCALAR DEMAND, in the family's own instrument).

**Falsifier:** a reading of the delivered definition under which the two
codings converge. The two ratios are computed through the delivered
function on one corpus.

## DBK_018 — task 5 PASS: the harness behaves; two placeholders decide verdicts

The io table reproduces the designed-in states (NaN on empty evidence
base, distinguishable from a real zero; the zero-channel edge; the
threshold firing at any excess). The sweep is the finding: over t ∈ {1,
1.5, 2, 3}, `dissent_alarm`'s (4,3) verdict flips between 1 and 1.5 and
(3,1) flips between 2 and 3 — the unset constant decides the verdict
across its plausible range, so per the order's own rule this is not yet
a test. A second unset threshold rides in the pre-registered prediction
itself: *"LOW independence_ratio"* labels a number the function returns,
with no boundary stated.

**Falsifier:** a t in the plausible range under which no verdict moves.
The sweep is pinned.

## DBK_019 — task 6 FAIL both halves: the reading distribution is the surface

6a, gaming measured fidelity without touching the ecosystem: frame
selection (whoever draws WHICH translations get scored raises fidelity
over an honest population) and coarseness (a translation hedged to
near-vacuity scores high against any outcome — fidelity with no
resolution partner is gameable by conservatism, the pairing gap
`move-set-derivation` measured). 6b, forging the pass without deleting
the instrument: graded curation — manage only the members that diverge
hardest and the remaining ecosystem still produces independent readings
drawn from a tamed sub-population; the tamper claim's dichotomy holds
only at TOTAL alteration, and a biased ecosystem is not a silenced one
(`observer-exclusion`'s differential archiving, in living form). All
three counterexamples run through the reading DISTRIBUTION, which the
candidate and the tamper claim both treat as fixed: the members cannot
misreport their state; the SAMPLE of members can misreport the
population. Any render puts the sampling frame inside the channel's
dependency set, or it is the paper channel wearing leaves. Per the
order's GATE, the ecosystem candidate stays a marker.

**Falsifier:** a stated sampling-frame control in the candidate's text.
None exists; the counterexamples are constructions against the text as
delivered.

## DBK_020 — task 7: the access vector, measured, in both N_eff senses

Five metadata/archive hosts probed this run (2026-08-30): crossref,
openalex, osf.io, doi.org, semanticscholar — all `000`, refused CONNECT.
Reported in both senses per `DBK_011`: the inherited arithmetic RATES
the all-collapsed vector at 1 (one effective domain — the egress gate);
the REALIZED path count after the shared node has refused is 0. The
order's WHY line asks for the change over runs: the R1 vector (three
hosts) and this run's (five) are both all-refused, so the delta so far
is zero on a wider vector. `--measure` re-probes live; the pinned vector
is the measured one.

**Falsifier:** any host in the vector answering. Re-run `wo_return.py
--measure`.

## DBK_021 — v2 lands beside v1; the transcription of the return is exact

`R2_OUTLINE_V2.md` folds the work-order return back into the outline
and lands verbatim beside `R2_OUTLINE.md`, both inspectable as
delivered. A revision quoting an audit is a copy and copies drift
(`OE_011`, `DBK_010`), so every figure it quotes is recomputed through
`wo_return` rather than read: the verdict split (1/2/5/7 PASS, 3/4/6
FAIL), the retention triple 3/3/2, the coder ratios 0.1 vs 1.0, the
(4,3) flip between t=1 and t=1.5, the five-host all-refused vector, and
rated 1 / realized 0 — **exact on every recomputed figure**, and the R1
column of the new matrix still matches the computed coverage on all
seven loads. The two off-return figures both source: `kappa ≥ 0.6` is
the order's own Task 4 rule (inherited from the sibling protocol's
threshold), and **commit `2fdbcd4` resolves in this repository's
history** — the first drop in this family to cite a commit hash of the
repo it lands in, which makes the citation checkable by anyone holding
the clone rather than a carried literature fact.

**Falsifier:** any recomputed figure differing from the quoted one.
`r2v2_audit.transcription()` runs them all.

## DBK_022 — the D row carries two answers, one section apart

§1 lists no carrier for D (*"— (P1-bounded, uncarried)"*) and §3's
carries column still lists D under both P0.3 and P0.4. The reconciling
reading exists — the D-KILL states *"D is carried only once P1 declares
the dimension"*, so §3's column can be read as the conditional claim —
but the condition reaches no column: F's conditional gets an asterisk
in the matrix and a *"(conditional)"* tag in the disjointness check,
while D's lives only in prose a column-parser never sees. One document,
two answers, and which one a reader gets depends on which section they
parse — the stated-in-two-places drift this family's own transcription
checks exist for, arriving *inside* a single document. The repair is
one marker on two cells. Computed, not read: `d_split()` extracts both
sections and reports the disagreement.

**Falsifier:** a marker on the §3 D entries, or D dropped from them.
Either closes the split.

## DBK_023 — the revision extends the audit's own kill chain

v2 requires the pinned-probe battery to be *fixed, public, and
unselectable* — otherwise the D candidate inherits the Task 6 selection
kill and D reopens. The return's own TASK 3 note said *"a fixed battery
of identical inputs"* and never closed who selects the battery
(asserted: no selection language in the note). So the revision applied
`DBK_019`'s finding — selection sits above incorruptible sensors — to
`DBK_016`'s own surviving candidate, a cross-application the return
missed. The kill chain is stronger in the revision than in the audit
that produced it, which is the direction a revision should run and
rarely does.

**Falsifier:** selection-closure language in the return's TASK 3 note.
`probe_extension()` scans for it and finds none.

## DBK_024 — "only Task 6" counts one searcher-dependent branch of three

v2's verifier note says *"only Task 6's weak-positive branch needed
dissimilarity."* The order's own text names such a branch **twice**:
Task 6's *"none found after real effort ⇒ INCONCLUSIVE-WEAK-POSITIVE"*
and Task 4's *"no defensible disagreement found (definition is
tight)"* — the same searcher-dependent positive, since a same-node
coder failing to find a defensible disagreement is weak for exactly the
reason a same-node red-team failing to find a game is. Task 3 carries
the branch implicitly (a failure to construct an evading scenario would
have read as *caught*). All three construction tasks returned kills, so
zero such branches were exercised and v2's conclusion — nothing
load-bearing rode on the mislabel — stands; its count does not. The
correction strengthens `DBK_014`: more of the order was exposed to the
role label than v2 says, and the outcomes, not the scoping alone, are
why nothing rode on it.

**Falsifier:** a reading of Task 4's not-found branch under which
"definition is tight" is identity-independent. It is a conclusion from
a search, and the searcher is the same node.

## DBK_025 — the tag legend declares three states; the entries use six

§8's legend line declares `OPEN · KILLED · QUALIFIED` and the entries
use `KILLED-VACUOUS`, `REOPENED`, and `LIVE` beyond it — `GM_011`'s
fields-in-use-not-in-schema shape at the smallest scale it has appeared,
and a one-line fix. All eight entries' tags are **consistent with the
computed task verdicts** (every KILLED/REOPENED tag references a task
that computed FAIL, every QUALIFIED/LIVE a task that computed PASS),
so the gap is vocabulary, not content. Recorded beside it, the
strongest addition in the revision: v2 does not resolve `DBK_011`'s
metric gap by picking an accounting — it makes *which accounting is
used* a declared decision under P0.2, routing the audit machinery's own
free parameter through the outline's observability provision.

**Falsifier:** a legend naming all six states, or an entry tag
inconsistent with its task's computed verdict. `tag_check()` computes
both.

## DBK_026 — T1: the flip map is the grid's ratio set; two regions no pin reaches

Work order 2's T1, returned by `wo2_return.py`. For every interior cell
(c > 0, s > 0) the delivered `dissent_alarm` verdict is `c/s > t`, so
the cell flips at exactly `t = c/s` — all 144 interior cells of the
enumerated 12×12 grid flip somewhere, the distinct boundary set is the
set of grid ratios (computed, with 4/3 among them), and the set grows
with the grid, so no single pin removes the phenomenon: pinning `t`
makes each cell a test and leaves the pin itself a P0.2-declarable
choice, which is where the order's *"don't pick the constant"* rule
routes it. Two regions are threshold-independent in the delivered
code and are reported apart: a zero-source base fires at **every** t
(the fail-closed branch — 13 grid cells), and a zero-concurrence cell
is silent at every positive t (12 cells). §8[4]'s QUALIFIED now has
its full map rather than one flip.

**Falsifier:** an interior cell whose verdict is constant over t, or a
threshold reaching the s ≤ 0 branch. The delivered code has neither.

## DBK_027 — T2: one incident sits under two load cases, in one delivered row

The colophon the order quotes (*"disjoint by construction"*) exists in
no delivered file — `colophon`, the quoted phrase, and `effective`
count **zero** across all five delivered artifacts and appear only in
the order that asks about them — so the claim tested is the order's
quotation. The arithmetic stands on the delivered texts: R1 states
provenance once, at document level (one pool of six domains for all
seven loads), and the sibling protocol's seed table supplies the only
sub-document granularity, mapping incidents to load-case letters —
five of the six pool domains match it exactly, with `aviation` the
residual (it sources P3's provision, not a load case). At that
granularity **E∩F = {Fukushima 1-4}**, stated outright in one row, so
the disjointness claim is partly false and the P7-pass partly unearned
by the order's own rule — and the delivered harness's own arithmetic
agrees: `dissent_alarm(2 concurring loads, 1 independent incident)`
fires. Seed letter B predates the B1/B2 split, leaving a fork reported
and not resolved: either both information loads inherit East Palestine
(a second non-empty pair) or B2 — the document's own *governing load
for AI* — rests on no seed case at all. One incident exhibiting two
failure modes is legitimate evidence practice; what it cannot be is
two independent sources. Reading the seed table as a provenance record
is reading, not testing — nothing here tests the N_eff hypothesis on
the seed cases the sibling forbids testing on.

**Falsifier:** a delivered per-load source assignment under which E and
F cite distinct incidents. The one delivered row says E,F on one line.

## DBK_028 — T3: the outline as it stands is honest on coverage; the clause lives only in the order

Coverage re-parse of `R2_OUTLINE_V2.md` with live nulls: six loads
carried, D the only uncarried and reading *P1-bounded, uncarried*, no
attack-marked token in any carrier list; a doctored D row reads
carried and a stripped atk mark moves P3 into E's carriers, so both
directions of the parse can fail. The one contradiction on record is
`DBK_022` (the §1/§3 D split), restated and not re-rated. The
effective-date clause T3(b) names is measured absent from every
delivered file and present only in the order itself, so the clause
checked is the order's own forward-dating rule, against P0.3
append-only semantics as this return implements them: claims append
as new ids with DBK_001..025 untouched, and `wo2_return.py` contains
no write-mode open and no subprocess — asserted over its AST — so the
module cannot amend the record it reads; the commit-level half lives
in the git history, where the prior returns stand at their own hashes.

**Falsifier:** a delivered file carrying the clause, a carrier list
holding an atk-marked token, or a null injection the parse ignores.

## DBK_029 — T4: five consistent accountings, one inexpressible; the sub-3 term named

The retention accounting space has three dimensions — retention
{held, not held} × the not-held reading of *shares its dependency with
the audited thing* {collapsed, void} × the metric {inherited two-state
`n_eff`, void-aware} — giving five internally-consistent accountings
with N_eff **3, 3, 3, 3, 2** (computed through the delivered function;
void-aware formalized as: drop void channels, `n_eff` over the rest)
and one combination that is **INEXPRESSIBLE, a table row rather than a
number**: not-held read as void under the inherited metric, which has
no void state — `DBK_011` appearing as a row in its own enumeration.
Exactly one accounting sits below 3, and the term that drops it is
**provider-only retention** — the element the dep-set MINUS clause
removes only while copies are held, re-entering P0.3 ∩ audited-system
when they are not. The enumeration also shows the choice is textual:
the outline's own §3 sentence picks the void reading (consistent
value 2), the inherited metric can only read the same state as
collapsed (value 3) — so selecting an accounting is selecting which
text governs, which is why it is the P0.2 declaration the order
reserves for the author and this return does not make.

**Falsifier:** a sixth internally-consistent accounting, or a
consistent reading under which some other element drops N_eff below 3.
The dimensions and the MINUS set are both delivered text.
