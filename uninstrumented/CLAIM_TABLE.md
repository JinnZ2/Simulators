# CLAIM_TABLE — uninstrumented

Ninety-four claims, `UNI_001..094`. **Three repaired** (`UNI_003`,
`UNI_009`, `UNI_010`), see *Repairs* at the end. `UNI_013..019` come from
the Case 010 drop ([`case_010_audit.py`](case_010_audit.py)),
`UNI_020..026` from Case 011 ([`case_011_audit.py`](case_011_audit.py))
`UNI_027..033` from Case 012
([`case_012_audit.py`](case_012_audit.py)) `UNI_034..041` from Case 013
([`case_013_audit.py`](case_013_audit.py)) `UNI_042..049` from Case 014
([`case_014_audit.py`](case_014_audit.py)) and `UNI_050..057` from Case 015
([`case_015_audit.py`](case_015_audit.py)), `UNI_058..068` from the
016/017 drop ([`drop_016_017_audit.py`](drop_016_017_audit.py)) and
`UNI_069..076` from Case 018 ([`case_018_audit.py`](case_018_audit.py)) and
`UNI_077..084` from the Case 018 harness
([`probe_audit.py`](probe_audit.py)) and `UNI_085..094` from the 019 /
LITERATURE / acquiescence drop ([`drop_019_audit.py`](drop_019_audit.py)).

## REFUTATION_PROTOCOL

The register is a list of questions. A claim here is about the **register's
structure**, not about whether any individual entry is right — the entries
carry their own stated confidence and that confidence is recorded verbatim
and not adjudicated.

A failed check updates the claim or the schema. It does not delete an entry
to keep a claim intact.

## Claims

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_001` | The entry structure separates the stated confidence from the shape, so the two move independently. An entry can be high-confidence on the mechanism and unmeasured on the magnitude, and both appear. | SUPPORTED | An entry whose confidence cannot be stated without changing the `EXCLUDED BY` field. |
| `UNI_002` | The mechanism sort is **untested, not confirmed**. At 7 entries, 7 fields and 7 mechanisms the mechanism partition and the field partition are identical, so nothing yet demonstrates the cross-domain grouping the sort exists for. | SUPPORTED | File a second entry under an existing mechanism from a different field. That is not a refutation of the claim so much as its expiry condition, and it is the cheapest next move on this folder. |
| `UNI_003` | The mechanisms are **not mutually exclusive**: 4 of 7 entries have a second mechanism with a claim. The filing decides which comparison case an entry sits next to, so it is a choice and should carry a primary plus a list. | SUPPORTED | A set of definitions under which each of the seven entries has exactly one applicable mechanism, and which does not achieve it by narrowing a mechanism until it names one case. |
| `UNI_004` | On a known-null corpus of six externally graded instruments — `../instrument-epistemology/`, three of them "mostly assumed", the worst at chain fidelity 0.165 — **nothing files that should not**. The register is not `CONSTANT_FIRES`. | SUPPORTED | An instrument in that corpus for which one of the seven mechanisms genuinely fires. The likeliest candidate is satellite SST at M3: if heavy model dependence counts as a mechanism, the boundary moves and `UNI_005` moves with it. |
| `UNI_005` | The line between **weak grounding** and **constitutive exclusion** is whether a blindness map exists. A reached-but-badly quantity has one; an excluded quantity does not, because the exclusion happens before the map is drawn. | SUPPORTED as a criterion, UNTESTED at the boundary | A case with a full blindness map that is nonetheless excluded by construction, or a case with no blindness map that is merely under-investigated. Either breaks the criterion. |
| `UNI_006` | The register has no demonstrated **reachable fire branch on a contested case**. All seven entries are ones nobody is currently arguing about, and the null corpus was chosen for being well documented rather than for sitting near the boundary. | UNVERIFIED | File a quantity a field believes it measures and does not, and see whether the register's mechanism set names why. Until that runs, `UNI_004`'s clean null result is weaker than it looks: a classifier that never fires on the null has not been shown to fire on the signal. |

## Where the entries are already worked

Five of the seven have a worked instance elsewhere in the repo, which is
what makes the register a cross-index rather than a new claim surface.

| mechanism | worked in |
| --- | --- |
| `STORAGE` | `../inverseminar/`; `../anchor-interval/` `ANC_011` (OPEN — no round run) |
| `BUDGET_BOUNDARY` | `../declared-frame/` `DF_005`, `DF_007`; `K18` in `../measurement-fork/` |
| `AUTHORED_REFERENCE` | `../anchor-interval/moving_reference.py`; `ANC_005..008` |
| `SCORED_AS_WASTE` | `../measurement-fork/` K14–K16; `MF_014`, `MF_015` |
| `MODALITY` | — |
| `PROXY_SUBSTITUTION` | entry 008, transport regulation (`UNI_011`) |
| `SCALAR_DEMAND` | — |
| `AUDIT_ASYMMETRY` | `scan.py --asym` (built; no corpus here — `UNI_008`) |

`AUDIT_ASYMMETRY` carried a specified measurement — count caveats issued
per account type across a transcript corpus, and take the ratio — called
here the cheapest of the three to run. It has since been **built**:
`scan.py --asym`. See `UNI_008`, which is why that row now reads
`scan.py --asym` rather than `—`, and why the remaining obstacle is a
corpus rather than a design.

---

## UNI_007 — `PROXY SUBSTITUTION` is a mechanism with no entry

**status:** SUPPORTED

The delivered `README.md` carries **eight** mechanisms. `PROXY
SUBSTITUTION` — *an enforceable measure displaces the target it stood in
for* — was not in the seven the register was built from, and no entry
files under it.

It arrived from the **scanner side**: `patterns.json` defines it with
triggers and a `check` question, and the register has no case for it. Every
other mechanism went case → mechanism. This one went mechanism → (no case
yet).

That is a real test of `UNI_002`. The mechanism sort exists so that a case
from one field sits next to a case from another and is recognizably the
same failure; a mechanism with zero entries cannot do that, and a mechanism
derived from a trigger list rather than from a case has not yet been shown
to name anything.

**Falsifier:** file an entry under `PROXY SUBSTITUTION` whose `QUANTITY`,
`VISIBLE AS` and `WOULD MEASURE` are not restatements of Goodhart's law.
The delivered README names Goodhart and Campbell as its partial literature,
so the entry has to reach something those do not.

**Evidence:** delivered `README.md` mechanism list; `uninstrumented.py`
`MECHANISMS`.

---

## UNI_008 — `--asym` closes the instrument gap and leaves the corpus gap open

**status:** SUPPORTED

`CLAIM_TABLE.md` previously called the `AUDIT_ASYMMETRY` measurement — *count
caveats issued per account type across a transcript corpus; the ratio is the
measurement* — the cheapest of the three unworked entries to run, needing no
apparatus that does not already exist.

The apparatus now exists: `scan.py --asym`. It splits sentences, tallies
hedges against an OUTSIDE / INCUMBENT account vocabulary, and reports the
ratio per file with an explicit caveat that it is sentence-level
co-occurrence and not attribution.

**It runs, and this repository has no corpus for it.** Across 932 files:

```
files with an account mention   356
files with ANY hedge at all      10
outside    hedged   6 of  477
incumbent  hedged   7 of  618
ratio                          1.11
```

Every hedge, hand-checked, is an artifact: `UNVERIFIED` / `unverified` as
claim-table and provenance **status codes**, `claims to` inside prose
describing a model, `Self-reported` inside a JSON spec string, and
`anecdotal` inside `patterns.json` itself — the scanner matching the file
that defines the trigger. **Zero are a hedge attached to an account**, so
the 1.11 is computed on nothing.

This is sharper than `UNI_006`: the entry is no longer unrun for want of a
design. It is unrun for want of reportage — limitations sections, news,
transcripts, regulatory filings — and none of that is here.

**Falsifier:** run `--asym` on a corpus containing reportage and get a ratio
near 1.0 with a usable event count. That refutes the asymmetry claim rather
than the instrument.

**Evidence:** `scan_audit.py` §4.

---

## UNI_009 — the largest trigger in the corpus is a substring match

**status:** SUPPORTED

`scan.py` compiles every trigger raw — `re.compile(t, re.I)`, no word
boundaries. On this corpus the consequence is concentrated in one trigger:

```
`lean`     193 hits   clean x106, cleanly x24, boolean x19, snaps_clean x16
                      the bare word appears 7 times

`slack`     81 hits   slack x104, slack_radius x30, slacken x1
                      the bare word appears 104 times
```

`lean` is the most-fired trigger in the whole corpus and nearly all of it is
`clean` and `boolean`. Adding `\b` to that one trigger removes **~24% of all
candidates at no cost**.

`slack` is the harder case and does not move: the bare word is what mostly
matches, and the residue is a proper-noun homograph and a code identifier,
neither of which word boundaries remove. That is a triage cost the design
already accepts by design.

So the repair is per-trigger, not global. A blanket `\b` would also break
triggers written to match inside words.

**Falsifier:** a corpus where the bare word `lean` — lean manufacturing,
lean staffing — is common enough that the substring match is buying recall
rather than costing precision. Then the raw compile is right and this is a
property of a codebase-heavy corpus.

**Evidence:** `scan_audit.py` §3.

---

## UNI_010 — the audit has no fixed point until one is broken by hand

**status:** SUPPORTED

`scan.py` reads `.txt`. `scan_audit.py` writes its output to
`samples/scan_audit.sample.txt`. Left alone, run *N+1* measures run *N*, and
two consecutive runs disagree **before anything in the repository has
changed** — measured, ~16 candidates of drift and a new densest-file row
that is the previous run's own output.

`EXCLUDE` at the top of `scan_audit.py` removes `samples/` from every corpus
walk, and the script converges.

**That exclusion is a hand-broken loop, not a fix.** Anyone running
`scan.py` over this repo will see those hits, because the file is really
there. What the exclusion buys is a script that converges; what it costs is
that the reported corpus is no longer the corpus on disk. Section 5 states
both halves and reports the excluded count rather than letting one of them
be quietly true.

The scanner's non-excluded self-hits stay in: `patterns.json` (10),
`scan_audit.py` (18), `scan.py` (1), `AUDIT_NOTES.md` (2). Those are the
use-mention case at its purest and they are left where they are.

**Falsifier:** an exclusion rule stated in `scan.py` rather than in the
caller — a `.scanignore`, or skipping the directory the output is written
to. Then it is the scanner's property rather than one audit's workaround,
and this claim becomes a note about a default.

**Cross-reference:** `../anchor-interval/ANC_001..004`. That folder models a
system fitted to a corpus it also writes into and finds coupling degrading
while every internal statistic improves. This is the same loop at three
files and one script, with the shortest possible period, and it is visible
only because the two runs were diffed — which is `ANC_004`'s scheduled
anchor rather than a triggered one.

---

## UNI_011 — entry 008 closes `UNI_007`, and is not Goodhart

**status:** SUPPORTED

`UNI_007` recorded `PROXY SUBSTITUTION` as a mechanism with no entry, and set
the falsifier: *file an entry whose `QUANTITY`, `VISIBLE AS` and
`WOULD MEASURE` are not restatements of Goodhart's law.*

Entry 008 files it.

```
QUANTITY       recovery-permitting environment during the off-duty
               interval — posture change, standing, walking distance,
               temperature control, separation of work space from rest
               space
EXCLUDED BY    PROXY SUBSTITUTION
VISIBLE AS     compliance
WOULD MEASURE  the environment, not the clock: floor area, standing
               height, walking distance, temperature range, and whether
               the rest space is the work space — then health outcome
               against those rather than against hours off
```

**Why it is not Goodhart.** Goodhart and Campbell describe a proxy
*degrading under optimization pressure* — the measure ceases to be a good
measure once it becomes a target. Nothing here requires anyone to optimize
against the clock. The quantity was **never in the proxy at all**, and it
did not need to be, because the arrangement supplied it for free: off-duty
meant leaving a building. The rule was written from that context, the
context was removed structurally for one occupation, and nothing
re-derived the rule.

That is a **silent precondition**, not a degrading measure. The nearer
relative is the smelter worker's cross-domain read in the `SCORED AS WASTE`
literature — an unpriced input that arrived with the arrangement, was never
named, and was therefore removable without anything registering.

Ten hours in a 4×6 sleeper and ten hours in conditions that permit recovery
are the same reading.

**Falsifier:** a duty-time rule that names an environmental condition of the
rest interval. If one exists, the quantity is instrumented somewhere and the
entry moves to a coverage question rather than an exclusion.

**`UNI_002` is not closed by this.** With eight entries the register still
runs 8 entries / 8 fields / 8 mechanisms, so the two partitions remain
identical and the mechanism sort remains untested.

---

## UNI_012 — a ninth mechanism is named in the README's own prose

**status:** SUPPORTED

The delivered `README.md` closes with a literature note:

> Goodhart and Campbell for **proxy substitution**, Polanyi for **storage**,
> STS for **undeclared frames**, symptom-dismissal work in medicine for
> **affect routing**.

Four mechanisms named. Two of them are on the eight-item list. Two are not:

| named in prose | on the list |
| --- | --- |
| proxy substitution | yes |
| storage | yes |
| undeclared frames | **no** |
| affect routing | **no** |

`undeclared frames` is arguably `BUDGET BOUNDARY` under another name, and it
has a whole folder — `../declared-frame/` — rather than a register entry.

**`affect routing` has neither.** Its shape, from the notes that accompanied
the drop: a structural-mismatch reading, offered with the transposition
available, is classified as affect — *the driver is frustrated* — routed to
support rather than to analysis, the referent dropped and only the state
kept. Nothing enters the record as a measurement, and the classification is
unfalsifiable from the speaker's side, because objecting to it reads as
confirming it.

That is not `AUDIT ASYMMETRY`, though it co-occurs with it. Audit asymmetry
is a guard firing on one side; this is a **channel reclassified at intake**,
so the reading never reaches a guard at all.

**Falsifier:** show that `affect routing` is `AUDIT ASYMMETRY` or `MODALITY`
under another name — that the eight-item list already covers it and the
prose is using a synonym. Then the list is complete and this is a wording
question.

**What it would take to file:** the entry needs a `WOULD MEASURE`, and the
obvious one has the shape of `scan.py --asym` — count, across a corpus of
reports, how often a structural claim with a stated referent is answered
about the reporter's state rather than about the referent. That is the same
instrument, aimed one step earlier.

---

## Case 010 drop — UNI_013..019

Case 010 (`cases/010coupledperturbationbiohybrid.md`, delivered verbatim) is the first entry
that declines to name its mechanism, states a confidence below the
ceiling, and carries a live external occasion with a DOI. Worked in
[`case_010_audit.py`](case_010_audit.py).

Three of these claims were checked against the open web on 2026-08-18
and are marked; they are not reproducible by running the audit script,
which does no network access.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_013` | Case 010's central move — mechanism deliberately unassigned, with the reason stated — is **not constructible**: `entry()` validates `excluded_by` against a closed eight-tuple and raises on `UNASSIGNED` and on the proposed new bin alike. Unlike `MF_017`/`CW_015`/`DL_004`/`GC_012`/`CA_003` this is not a missing field but a vocabulary closed on purpose, and Case 010 is the first delivery to argue the closure is premature for one case. | SUPPORTED | An `UNASSIGNED` sentinel with `candidates` and a required `why_open`, so an unfiled entry is a state the sort can count. |
| `UNI_014` | Case 010 is the **first entry whose confidence is below the ceiling** — 8 of 8 existing entries open with "high", this one states "not above ~40%. Not sufficient to act on." `UNI_004`'s `CONSTANT_FIRES` reading of the field no longer holds; `UNI_006` is untouched, because admission is a different question from the field's value. | SUPPORTED | A second sub-ceiling entry, or the register refusing one. |
| `UNI_015` | The OCCASION checks out. Six stated details, six confirmed against the published record — author, journal, volume/issue, DOI, device stack, sub-0.1 V operation, forming-free switching. First literature claim in this drop family that was checkable at all, against `ANC_010`, `CD_009`, `RD_015`, `HO_005`. | SUPPORTED *(web, 2026-08-18)* | Any stated detail failing to match the article. |
| `UNI_016` | Two of the four items the entry lists as "not located in open sources" **are locatable** — endurance 1000 cycles, retention > 4×10³ s — and **both are scalars**, so the correction supports the SCALAR DEMAND candidate bin rather than undercutting it. Temperature range and variability distributions were not located here either. | SUPPORTED *(web, 2026-08-18)* | The two found metrics turning out to be co-varying measurements. |
| `UNI_017` | The field-wide falsifier **partially fires**. Combined-stress protocols exist and are named (THB, TB, temperature cycling, IEEE P1817, JEDEC JC-42.4), so "none across the field" is refuted — but those hold several variables at simultaneous *constant setpoints*, a factorial corner, while ARM B specifies co-varying **drift at matched integrated dose** compared on distribution shape. The entry survives narrowed, and should say "co-varying drift at matched dose" wherever it says "co-varying". | SUPPORTED (narrows the entry) | A located protocol that co-varies drift at matched integrated dose. |
| `UNI_018` | The supplement falsifier — "the paper's supplementary data contains a multi-variable arm" — **could not be checked**: publisher and every news mirror located are blocked by this environment's egress proxy. Cheapest of the three falsifiers for anyone with access, and the only one that would close the case outright rather than narrow it. | UNVERIFIED | One look at the supplementary methods. |
| `UNI_019` | Case 010 is the near-boundary case `check_null()` says the register lacks — "a quantity a field believes it measures and does not", with a live paper and a confidence low enough to be wrong — **and it cannot file** (`UNI_013`). Its comparator (synthetic periodic scaffold, matched spacing and matched Ag loading) is a known-null in `../null-harness/` terms and is the load-bearing element; the three-way discriminator names its own discard branch, so it is not `CONSTANT_SILENT`. Missing: any power calculation — a `G-RES` pair of variability spread against the margin claimed. | SUPPORTED (holds) | A stated device count and resolvable margin, which would close the gap. |

## Case 011 drop — UNI_020..026

Case 011 (`cases/011rebuildabandonmentcycles.md`, delivered verbatim) is the second
consecutive delivered case the schema cannot hold, and it strains it in a
different place: Case 010 declined to name its mechanism, Case 011 declines
to be one quantity. Worked in [`case_011_audit.py`](case_011_audit.py).

Four of these were checked against the open web on 2026-08-18 and are
marked; they are not reproducible by running the audit script.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_020` | The cluster is not constructible: `entry()` takes one `quantity`, one `excluded_by` and one `would_measure`, and Case 011 carries five sub-questions, four with their own WOULD MEASURE and one with its own EXCLUDED BY. With `UNI_013` this makes **two delivered cases, two different refusals by the same schema** — which fits the eight entries written to fit it and neither real case since. The `UNASSIGNED` sentinel does not cover this; a cluster needs sub-entries, so a question can close individually while the cluster stays open. | SUPPORTED | A `questions=[...]` parent entry, each with its own `excluded_by` and `would_measure`. |
| `UNI_021` | `entry()` accepts `confidence=""` and `confidence=None` silently, so Case 011's **reasoned refusal** to state one ("a scalar over a cluster would not carry usable information") is stored in the same cell as a field somebody forgot. Three states now exist in the wild — high, a gradient, deliberately absent — and the schema can tell apart two. Eleventh instance of the absent-vs-known-negative repair, in the one field the register calls recorded-not-adjudicated. | SUPPORTED | A three-valued confidence, or `None` being illegal. |
| `UNI_022` | Q5 — "NOT YET ARTICULABLE… Do not fill this in with an approximation" — is the register's own thesis applied to its own vocabulary, and has no slot. `note` would file it as a remark rather than as an open axis with a count, so nothing in any sort would show the cluster has an unnamed member. | SUPPORTED (holds) | An open-axis field the sort can count. |
| `UNI_023` | The occasion checks out — Kiss/Viglione/Blöschl, *Nature*, 12 Aug 2026, DOI 10.1038/s41586-026-10888-8, title exact, 16 events, sequences implication. One drift: the entry says "roughly 18 months" where coverage describes late 1341 to 1343, about two years — inherited from the paper's title window, not introduced. Matters because Q2 proposes 1342–1343 as its corpus and a start at 1342 drops the first inter-event interval, which is the one that sets the arrival rate. | SUPPORTED *(web, 2026-08-18)* | The published window matching 18 months. |
| `UNI_024` | Q1's falsifier fires on one of the three things its own sentence bundles. **Antecedent moisture is instrumented and dramatic** — saturated soil turns a 7-year rainfall into a 100-year flood; dry soil turns a 200-year rainfall into a 15-year flood — and compound-hazard modelling is an active quantified field. No design-standard variable for **unrepaired works or spent response capacity** was located. The sharper statement: the field instruments the antecedent state of the **hazard** and not of the **system**. | SUPPORTED (narrows the entry) | A design standard carrying a pre-event repair-completion term. |
| `UNI_025` | Q3's falsifier partially fires, **along the boundary of whoever keeps the record**. FEMA HMGP acquisitions are required to be voluntary (owner consent attributed, eminent domain excluded) and the administering authority's property selection is recorded — so two of the four pathways have attribution. Insurer withdrawal and lender refusal are decisions by parties the program does not administer and cannot appear in its record. The entry's own `generation-capacity` link is instanced: "voluntary" truthfully attributes the final step over an option set generated upstream. | SUPPORTED (narrows the entry) | A record carrying insurer- or lender-initiated non-reoccupation. |
| `UNI_026` | Three of four cross-links resolve. `rural` is not only present but accurately characterised — tracked by `density`, with `self_support` among the welded components, which is the entry's "counts headcount, not what is holding". **`rate-mismatch-polytope` does not exist anywhere in the tree** — seventh instance of a reference naming an absent artifact. Nearest existing kin: `rigidification-sensor/` runs Q2's comparison already (`locked_at` is the tick where reversal cost passes continuation cost) and `sustained-activation-gate/` holds the restore-vs-coupling trade-off. | SUPPORTED | The folder arriving, as three of the six prior instances did. |

## Case 012 drop — UNI_027..033

Case 012 (`cases/012fuelincidencesubstrategoods.md`, delivered verbatim) is the third
consecutive delivered case the schema cannot hold, and the **first whose
stated confidence is checkable by computation** rather than recorded
verbatim. Worked in [`case_012_audit.py`](case_012_audit.py).

Four of these were checked against the open web on 2026-08-18 and are
marked. `UNI_027` is arithmetic and is reproducible by running the script.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_027` | Q1's "high — arithmetic, not hypothesis" **holds, and holds more strongly than claimed**. The aggregate freight-to-value ratio is identically a value-weighted mean of per-class ratios: `F/V = Σ (n_i·v_i/V)·(f_i/v_i)`. It is algebra, not a model, and needs no freight data to be right. Demonstrated on a plausible mix: one class at 87% of the dollar weight pulls the aggregate to 1.46% while the worst-affected class sits at 12.50% — 8.5× understatement. First entry whose confidence field is adjudicable, and it adjudicates in the entry's favour. | SUPPORTED *(reproducible)* | An arrangement of classes where the identity fails. |
| `UNI_028` | A **fourth** confidence state: split across the cluster (Q1 high, Q2–Q4 not stated, with the reason). `entry()` takes one string. Three cases, three distinct failures of that one field — too coarse (`UNI_014`), cannot record a reasoned absence (`UNI_021`), cannot record a split (here). The `UNI_020` sub-entry repair reaches a second field. | SUPPORTED | Per-question `confidence` on a cluster entry. |
| `UNI_029` | The NOTE ON A CIRCULATING NUMBER is a **negative-provenance record** — no precedent in this register, no slot in the schema, and the inverse of every prior literature finding here (`ANC_010`, `CD_009`, `RD_015`, `HO_005` are all markers found by an auditor afterwards). It names the numbers, where they circulate, that no peer-reviewed origin was located, and why the note exists. Verified: none of `4.75`, `5.25` or the jet-fuel claim appears anywhere in the entry's reasoning. | SUPPORTED (holds) | A reasoning step depending on one of the flagged numbers. |
| `UNI_030` | The published finding checks out: ~50% immediate pass-through, ~100% within a week, carriers unable to absorb it on thin margins in a competitive market — including the mechanism the entry attributes the result to. Third consecutive occasion in this register that verifies. | SUPPORTED *(web, 2026-08-18)* | The pass-through figures failing to match. |
| `UNI_031` | The rate figure **does not check out as stated**. Entry: flatbed "roughly $0.70–$1.20/mile above dry van, 2026 spot data". Located: $0.48/mile (March 2026, stated directly), and early-2026 averages of $2.47 dry van vs $2.95 flatbed give the same $0.48 independently. No matched-date pair located for late 2026. **Does not touch Q1**, which is an identity — it halves a downstream magnitude, not the structure. | SUPPORTED | A matched-date 2026 spot pair in the stated range. |
| `UNI_032` | Q4 splits three ways. Its falsifier **partially fires** — BLS publishes the hedonic category list and its share, ~2.9% of the CPI ex-shelter. The **asymmetry is confirmed by that list** (PCs, TVs, audio, camcorders, DVD players, apparel, appliances, textbooks, broadband; neither food nor electricity). But the **magnitude constrains the mechanism**: "the aggregate can be held level by hedonic credit" now has a published upper bound and it is small. And there is a **denominator switch** — Q4 is about GDP real output (BEA), the located share is CPI (BLS), which is `measurement-fork`'s VOID RATIO inside a falsifier. | SUPPORTED (narrows the entry) | A published BEA adjustable-vs-non-adjustable real-output decomposition. |
| `UNI_033` | Q3's two halves have **opposite epistemic status**. The non-linearity is a hypothesis with the sharpest falsifier in the drop and no data either way (reachable negative, so not `CONSTANT_SILENT`); the accounting claim is **true by construction** — household food is final consumption expenditure, labour is a primary input with no row in the intermediate matrix, so the calories sustaining it are intermediate consumption of no industry. The half marked "WOULD MEASURE: unclear" is the established one; the instrument is missing because the framework has no slot for the quantity, which makes Q3 the entry's best candidate for a filed mechanism. | SUPPORTED | An input-output framework carrying calories as intermediate consumption. |

## Case 013 drop — UNI_034..041

Case 013 (`cases/013compensationloadunattributed.md`, delivered verbatim) is the fourth
consecutive case the schema cannot hold, and the first that does not know
whether it is one entry or two. Worked in
[`case_013_audit.py`](case_013_audit.py).

Sections 3, 4 and the NIST citation in 5 were web-checked on 2026-08-18
and are marked. **The simulations in section 5 are stdlib, seeded and
reproduce by running the script.**

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_034` | A **fourth** refusal, and the first about the entry's own identity rather than a field: 010 declines to name its mechanism, 011 to be one quantity, 012 to carry one confidence, 013 **to be one entry or two**. The `UNI_020` sub-entry repair does not reach it — sub-entries presume the parent is one thing. On naming: it first landed as `case-013.md` (the register's numbering, no position), and the author's later file delivery supplies `013compensationloadunattributed.md` — the entry's **own** working handle, which the entry labels as naming "the first half only", so provisional by the entry's own statement. The filename now names Q1–Q3 and not Q4. | SUPPORTED | A representation for "this may be two entries, and which is open". |
| `UNI_035` | `[stated by Kavik]` is the **first provenance tag inside a register entry**, and it is attached to one sub-question — the half the SPLIT IS OPEN section says may leave as a separate case, so it would leave with its attribution attached. `entry()` has nine fields and none carries who said it; 0 of 8 existing entries carry an attribution. | SUPPORTED | A provenance field on entries or sub-questions. |
| `UNI_036` | The anchor is **fresher and more concrete than stated**: 5-digit SATCAT exhausted 2026-07-11 (Saramago), now at 100365, Alpha-5 explicitly a *stopgap* capped at 339,999 with I and O omitted to avoid confusion with 1 and 0, 9-digit GP/OMM since 2020, legacy TLE still in use alongside both. Q1's denominator therefore starts six weeks ago rather than decades — a better measurement position than claimed. And the compensation layer is **itself a fixed-width scheme with a population assumption**, so Q2's asymmetry recurs one level up rather than resolving. | SUPPORTED *(web, 2026-08-18)* | Existing objects being renumbered on overflow. |
| `UNI_037` | "Objects recategorised" is **not what was located**. New objects get 100000+; Alpha-5 changes the *encoding*, not the assignment of existing objects — so for the existing population the analysed key does not move, which is Q3's own falsifier met from a direction the entry does not consider. Reassignments do occur, for merged/split objects from refined sensor observations — a physical-resolution event, not an overflow event. **Two sources of key movement, and the entry attributes to overflow what is documented for resolution.** Q1 would need to separate them, since only one is caused by the design-time omission. | SUPPORTED (corrects the entry) | Documented renumbering of existing objects at the overflow. |
| `UNI_038` | Q3's transfer, simulated in three regimes. **All three flatten toward zero — the direction claim survives everywhere tested**, including regime 3, which was built expecting it to fail. What does not transfer is the mechanism: regime 1 is classical errors-in-variables (attenuation = the reliability ratio, matched to 3 dp), regime 2 non-differential misclassification (exactly `1−2p`), regime 3 variance inflation from a block remap (down to **1%** of the true slope, against 50% for a classical error). "Structurally the same as the NIST dimming effect" is true of the direction and nothing else, and the catalog cases are **worse** than the nanoparticle case. Caution the entry omits: regime 3 assumes the key is a numeric covariate; the strongest form of Q3 is regime 2, mis-joins across reconciled schemes. | SUPPORTED *(reproducible)* — strengthens Q3 | A regime where a key remap inflates rather than attenuates. |
| `UNI_039` | The Case 010 cross-link **lands, and corrects `UNI_019`**. A periodic scaffold has interchangeable positions; a sequence-addressed one does not, so matched pitch is not a matched control if the contribution depends on distinguishability. Consequence is a specific **false negative**: Case 010's flat branch ("the organic layer is functioning as a geometric ruler") would also fire when addressing is everything, because the comparator cannot express it. `UNI_019`'s assessment holds on the organic-vs-inorganic axis and was too generous on the addressing axis. Repair is one arm — matched pitch *and* aperiodic position-distinguishable structure. | SUPPORTED — corrects a prior finding | The two-arm design separating pitch from addressing. |
| `UNI_040` | Q4's comparison class **survives in a narrower form**. A DNA sequence of length L addresses 4^L states, so "no block to overflow" is not literally true; the statable version is that **capacity scales with the object rather than being fixed by a register** — one more base multiplies capacity by four, where widening a counter rewrites every consumer of the field. The middle term was already in the anchor's own records and goes unmentioned: the COSPAR designator is compositional, so its year field is open-ended and capacity grows with time. | SUPPORTED (narrows the entry) | An object-carried scheme with a fixed capacity that cannot grow with the object. |
| `UNI_041` | Four of four cross-links resolve — first drop in this sequence with no dangling reference (`rate-mismatch-polytope` is not cited here). Confidence is a **fifth** state of the one string field: an absence with a stated unlock condition ("Q3 alone could take a gradient once Q1's data exists"), which is a dependency between sub-questions. `entry()` still cannot tell any of the five from an omission (`UNI_021`). | SUPPORTED | A confidence field carrying an unlock condition. |

## Case 014 drop — UNI_042..049

Case 014 (`cases/014offloadingevolutionaryframing.md`, delivered verbatim) is the fifth
consecutive case the schema cannot hold, and the first whose EXCLUDED BY
says that nothing excludes it. Worked in
[`case_014_audit.py`](case_014_audit.py).

Sections 3–6 were web-checked on 2026-08-18 and are marked.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_042` | **The register's founding binary cannot hold Q1.** The README says "Not a gap log. A gap is an oversight. These are exclusions built into the apparatus"; Q1's EXCLUDED BY is "nothing prevents it. It has not been assembled." By that rule it is a gap — except the entry argues a **third** state: the apparatus exists, is competent, and is aimed elsewhere ("the target moved; the instrument did not follow"). Case 013 Q4 named the same state one drop earlier. Two-valued distinction, three states delivered. | a third term in the README, or a mechanism for it | SUPPORTED |
| `UNI_043` | `tool-off-metrology` does not exist in the tree and is cited twice here plus once in Case 011 Q4 — so there are now **two** named-but-absent artifacts each load-bearing across two drops (`rate-mismatch-polytope` is the other). Both are about the same thing from different ends: a rate or a baseline the measurement destroys. The `[[...]]` syntax is new and nothing in the repo resolves it. | either folder arriving | SUPPORTED |
| `UNI_044` | The occasion verifies four for four, including the load-bearing detail — Fellers & Storm, JEPLMC, and *"falling below the baseline levels of performance observed for participants who never used reminders"*, which is the difference between a tool that does not help you learn and one that leaves you worse than not having used it. Fifth consecutive verifying occasion. | the baseline comparison failing to match | SUPPORTED *(web, 2026-08-18)* |
| `UNI_045` | **Q1's corpus already exists.** A meta-analysis of cognitive offloading (PubMed 40500483) ships an enumerated included-studies list with stated inclusion criteria — the denominator Q1 says "has not been assembled", built by people with no stake in this question. Changes Q1's cost from defining a corpus to scoring a published list. Caveat that must travel with it: a meta-analysis on memory-based *performance* selects for performance-reporting studies, which is not the same population as "instances described in evolutionary terms". | the list turning out to have no evolutionary-language instances | SUPPORTED *(web, 2026-08-18)* |
| `UNI_046` | Pobiner (2016) verifies exactly (AJPA, title and year), and so does the attribution — the acquired-traits-are-heritable misconception is documented in that literature. Kelemen's "promiscuous teleology" verifies as a conceptual default all peoples share, tamped down by enculturation. **One item runs ahead of what was located:** the three-item negative list (not parental explanation, religiosity, or storybook convention) was not confirmed item by item, and universality alone does not carry the entry's use of it, since a universally-taught thing is also universal. | the negative list surfacing in Kelemen's own work | SUPPORTED, with one attribution BROADER THAN LOCATED |
| `UNI_047` | Q2 makes **two** claims and attaches **one** falsifier. The falsifier tests the smuggle (claim A); the claim the entry leans on — that the reference-population error has no name in the literature (claim B) — has no falsifier. Claim B is consistent with the corpus reached: the evolution-education literature studies populations of *learners*, not the implicit reference population of the narrative. Named as the cheapest next check and not searched here: the history-of-science and decolonial-paleoanthropology literature. | a named critique of reference-population smuggling in human-origins narratives | SUPPORTED (structural) |
| `UNI_048` | Three `[stated by Kavik]` tags, up from one in Case 013 — the device is now used at scale, and its distribution is informative: the single **untagged** question is the one with an independent runnable instrument and a stated high confidence, and instrumentability falls off across the tagged ones (Q2 depends on Q1, Q3 "unclear", Q4 "no instrument proposed"). The tag marks what is a position rather than a procedure, in an entry whose protocol says it holds markers not positions. | a tagged question with an independent instrument | SUPPORTED |
| `UNI_049` | "Do not fill this in with an approximation" reaches a **third** instance in three drops (`DD_007` recorded it at two) — a construct with a stable form and still no schema slot. Q3 adds the sharpest sentence in the drop: *"any study isolating one is measuring an artifact of its own isolation, and the isolation is a property of the instrument"* — the register's own thesis stated in general form, as a conditional with the condition named. The NOT CLAIMED HERE section pre-empts the intent reading, which is `rigidification-sensor`'s no-actor discipline arriving in a one-page case. | the device appearing without a withheld slot behind it | SUPPORTED (holds) |

## Case 015 drop — UNI_050..057

Case 015 (`cases/015definitionalprecedence.md`, delivered verbatim) proposes a new
mechanism, DEFINITIONAL PRECEDENCE, and its central claim is checkable in
an unusual way: the field's own classification vocabulary either has a
slot for the finding or it does not, and that is published record rather
than judgement. Worked in [`case_015_audit.py`](case_015_audit.py).

Sections 1–5 were web-checked on 2026-08-18 and are marked; the arithmetic
in §5 reproduces by running the script.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_050` | The occasion verifies across five authors, the DOI, the bioRxiv ID, the institution, the "100-year-old classification" (the source's own phrase), the bracketed 5–8% growth limit and the 21% aerotolerance. One drift: the preprint says "lung **commensal**", the published version says "lung **symbiont**" — a categorical relabeling inside the paper whose subject is a categorical relabeling. Also located and stronger than the entry claims: >10% of microbial populations in healthy and diseased lungs. | any stated detail failing to match | SUPPORTED *(web)* |
| `UNI_051` | **Q1's mechanism is refuted and its conclusion strengthened.** The field's oxygen vocabulary is **five-valued**, not two — and one of the five, *aerotolerant anaerobe*, is named for exactly the phenomenon reported. Further, the obligate-anaerobe category's own published range reaches **8% oxygen**, so the measured growth limit sits *inside* the range of the category it was assigned to; only the 21% aerotolerance exceeds it. The label held not because the vocabulary lacked a slot but **despite** having one named for this — a worse failure, and better evidence for DEFINITIONAL PRECEDENCE. | the five-category vocabulary post-dating the classification | SUPPORTED (refutes the stated mechanism) |
| `UNI_052` | Q1's falsifier partly fires, and the refinement beats the claim. The standard assay — thioglycollate broth, position in the tube reflecting oxygen preference — **is a gradient method**. What it does not do is quantify: it returns a position that maps to a category *name*, never a concentration. The sharper exclusion: **the numeric threshold attached to the label was never measured by the assay that assigns the label.** The sensor platform matters because it quantifies, not because it is a gradient. | classification numbers being produced by the standard assay | SUPPORTED (narrows and sharpens) |
| `UNI_053` | The VISIBLE AS titling claim verifies **verbatim**: *"Oxygen induces mutation in a strict anaerobe, Prevotella melaninogenica"* (2008), 18 years before the 2026 paper. The 2008 study measured decreased survival and increased oxidative damage under oxygen exposure — an oxygen-response measurement with the label retained in the title of the paper doing the measuring. The proposed mechanism instanced in five words. | the paper not existing, or not carrying that phrase | SUPPORTED *(web)* |
| `UNI_054` | Q3's either/or needs an edit: **the two branches are not exclusive and the 2008 paper shows both operating.** It is evidence on the *category* branch (oxygen experiments 18 years before the sensor) and does not settle the *instrument* branch, because its readout — mutation frequency and survival — could not produce a growth-limit number however carefully run. The joint reading makes Q3's underlying question worse, not better: it requires both a missing quantifier and a holding label. | a pre-sensor study measuring growth across intermediate concentrations | SUPPORTED |
| `UNI_055` | **The headline number rests on a figure that was not located.** At 0.05% the arithmetic is exact (5/0.05 = 100, two orders). The 0.05% figure was not located; the located category description gives **0.5%** as the low end — an order of magnitude above, which would halve the exponent. The entry may be quoting a Prevotella-specific threshold from the source, a different quantity from the category's general low end. Recorded as NOT LOCATED, not as wrong. | the source paper's stated historical threshold | NOT LOCATED (the one number the headline depends on) |
| `UNI_056` | DEFINITIONAL PRECEDENCE is a **fourth state** against the register's founding binary (`UNI_042`), and differs in kind from the third: not "nobody looked" but "somebody looked, published it in the same field, and the category converted it into a methods problem." **It names an operation, not an absence** — the other mechanism candidates name a quantity with no register; this one names something that runs on data that did arrive, and it has the best-instanced anchor of the four. | an instance where the category admitted the observation as evidence | SUPPORTED (holds) |
| `UNI_057` | Four of four cross-links resolve — second drop with no dangling reference, after Case 013. The `presented-binary` link is accurate to that folder, with the twist `UNI_051` supplies: the option space was not in fact constrained to two, so the alternatives were present, documented, and not reached for. Confidence is split across the cluster again (Case 012's state, second appearance); five states of the one string field are now in the wild. | a dangling link, or an unsplit confidence | SUPPORTED |

## Re-delivery — UNI_058

The five cases 010–014 were re-delivered as files with descriptive
filenames after all five had already landed from inline text. Recorded
because the comparison is cheap and the result is not automatic.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_058` | All five re-delivered cases are **byte-identical** to the checked-in copies — 0 differing lines across 010, 011, 012, 013, 014, spanning six intervening drops. The one thing that changed is the filenames, which the author supplied and which are adopted here; `015definitionalprecedence.md` keeps the numbering form because no name was supplied for it, and the same rule would give `015definitionalprecedence.md` from its own working handle. This is `measurement-fork`'s `MF_019` with the opposite outcome: files that live in one place do not drift, and these did not. | any re-delivered case differing from the landed copy | SUPPORTED |

## 016 / 017 drop — UNI_059..068

Eight files arrived together and they are four kinds of thing: two
register entries (`cases/016agreementasmode.md`,
`cases/017weldedobservables.md`), one instrument list (`AVENUES.md`),
three specimen files, and **two JSON artifacts authored by one of the
systems the specimens are readings of**. The last group is new to this
register and changes what can be checked. Worked in
[`drop_016_017_audit.py`](drop_016_017_audit.py).

Section 1 was web-checked on 2026-08-18; everything else reproduces by
running the script.

| id | statement | status | falsifier |
| --- | --- | --- | --- |
| `UNI_059` | 017's occasion is the **most precisely verified in this family**: eight elements, eight confirmed, including the two easiest to inflate — the result phrasing and the collaboration's own hedge (`disfavor`, not overturn). The entry carries the Science Perspective's caveat and states outright that nothing in it requires the junction picture to be correct, so a later reversal of the physics leaves the case standing. | any stated element failing to match | SUPPORTED *(web)* |
| `UNI_060` | **Four of five internal filename references do not resolve** against the delivered filenames — every reference is hyphenated, every delivered name is not. The fifth resolves only because the upload arrived as `README_35.md`, a transport artifact, and was landed at the name the documents use. Landed at delivered names for consistency with the six case files beside them; recorded rather than repaired by rewriting delivered text. In a set this interlinked, the references *are* the navigation. | either renaming four files or editing five references | SUPPORTED |
| `UNI_061` | The specimens README's **first rule is false of its own files**. It says "Nothing in these files is authored by the repository maintainer. These are outputs from other systems, pasted in." Neither specimen contains a pasted output — both headers say the raw text is held elsewhere — and the bodies are 7 and 6 readings, which are analysis. The rule that does the work is rule 4 ("specimens are not measurements"), and it survives whoever wrote the readings. | a specimen file containing pasted output | SUPPORTED |
| `UNI_062` | The attachment both headers ask for arrives, and **neither JSON is raw output**. `BNRAM_FIELD_LOG_001.json` states in a machine-readable field that it was compiled by one of the two systems under test, after correction, with `corrections_applied_before_logging` naming what was applied. That is rule 3 ("contamination is recorded, not cleaned") honoured in a better form than the prose specimens use — a field can be read without being interpreted. Still missing: the raw DeepSeek and Kimi output the headers actually request. | the raw outputs arriving | SUPPORTED |
| `UNI_063` | **Specimen B's readings, checked against the source it read: four of five confirmed, one overstates.** R1 circular (the EXCs are defined in a registry compiled by a system under test), R2 n=2, R3 no baseline, R5 no content-free control — all confirmed from the file. **R4 does not survive**: the protocol specifies four detection methods per EXC, a 0–3 severity scale, a named rater and an inter-rater phase. The narrow criticism holds (unblinded scoring by the party expecting the result); "specifies no criteria and no scorer" does not. `AVENUES.md` A3 carries the correct requirement forward and does not repeat the overstatement. | the protocol lacking a scoring rubric | SUPPORTED — and it corrects a delivered reading |
| `UNI_064` | A **definitional gap** in the protocol, reported narrowly: principle 1 makes provider reputation null-weight, and the `notes` fields generate directional hypotheses from training regime. Those are technical properties, not reputation — **not a contradiction** — but EXC-16's fourth detection method is "references provider reputation or training data size as implicit validity signal", and no rule says where the line falls. A rater scoring "RLHF-heavy, so expect schema-forcing" has nothing telling them whether that is a 0 or a 3. *Disclosure: this audit is written by a model and `CLAUDE-3.5-SONNET` appears in the test matrix; the finding holds identically from the GPT-4o and Llama rows.* | a stated rule separating training regime from provider reputation | SUPPORTED |
| `UNI_065` | 016's Q1 design **registers an alternative explanation for its own expected finding, before any run**: a FALSE correction may be accepted because the model constructs a reading under which it is true, which is a different failure from pressure-tracking. It names what would separate them and marks it untested. `photoperiod-claim-harness` registers predictions before runs; this registers the way the prediction could be right for the wrong reason. First instance in this register. | the confound being discovered after a run rather than before | SUPPORTED (holds) |
| `UNI_066` | `tool-off-metrology` reaches a **third** drop (Cases 011, 014, and 016 Q3) — the most-cited absent object in the repo, with 016 Q3 stating its problem in the most general form yet: *"the quantity of interest is unaided reasoning, and the environment that would measure it is the environment that supplies the aid."* Separately, 017 Q4 cites `moral-claim-decomposer`, which does not exist; `moral-decomposer` does, and the described work is a fair summary of it. A name mismatch, not an absent artifact. | the folder arriving, or the link being corrected | SUPPORTED |
| `UNI_067` | 016 and 017 are **instruments for each other** — 017 supplies 016's decoupling design by name, and 017 Q4 asks whether a matched-pair design has a linguistic analogue, which 016's A1 *is*. So the pair partially answers its own cross-question by existing: constructible, at the exact point where the analogy would have failed. What remains open is whether it works, which is A1's readout and has no reading. First time two entries in this register are instruments for each other rather than cross-references. | the linguistic analogue turning out not to be constructible | SUPPORTED (partial) |
| `UNI_068` | Second re-delivery check: `015definitionalprecedence.md` and `MECHANISM_11.md` both byte-identical to the landed copies. The 015 filename is the one **offered and deliberately not applied** last drop; it has now been delivered at exactly that name, so the derivation was right and holding it was still correct — a derived filename applied quietly would have been indistinguishable from a delivered one a week later. Renamed in this commit. | either file differing | SUPPORTED |

| `UNI_069` | **Clock 2's stated premise is false, and the arm the file says to run first has no error bar.** *"Weights cannot change. Any shift in what is acknowledged has to enter through context."* A frozen checkpoint queried twice at non-zero decoding temperature returns two different texts and the difference entered through neither — the disjunction has a third term. `sampling` / `temperature` / `variance` / `repeat` / `error bar` / `seed` appear **0 times** in the delivered file, and the five-item CONFOUNDS list has one statistical entry whose n is *checkpoints* (Clock 1 / Q3), none naming Clock 2. Simulated: two frames at the SAME rate, n=20 each, differ by **0.30 or more one run in twenty** against a base rate of 0.35. Repair is a G-RES pair needing no new apparatus — repeat each frame N times, require the between-frame difference to clear the within-frame spread by a declared margin. | a within-frame repeat arm with a stated sampling regime and a declared margin | SUPPORTED |
| `UNI_070` | **The two pointers into 017 name a labelling scheme 017 does not use.** `017 P1` (cited twice, including "Clock 2 is P1") and `017 component (a)` — 017 carries `Q1`..`Q5` and no P-series and no lettered components. P1's referent exists unlabelled: 017's WOULD MEASURE is deliberately unfilled and offers one blockquote in its place (*"Find a pair of systems matched on the quantity you cannot vary…"*), which is exactly what Clock 2 does. "component (a)" is not locatable at all. `016` Q4, `013` Q4 and specimen A's R4 all resolve by content; `specimens/2026-08-18-model-A.md` is the **fifth** instance of `UNI_060`'s hyphenation mismatch and the first written after it was recorded. | 017 gaining the labels, or the citations being rewritten to the labels 017 has | SUPPORTED |
| `UNI_071` | **First entry to place itself inside its own population and refuse the exemption that noticing usually buys.** POSITION OF THIS FILE: *"The account above was drafted by a system inside the sample… Noticing that does not place it outside the sample."* Zero prior cases carry such a section. Under the folder's own `specimens/README.md` rule — generated text about a system is a specimen, not a measurement — 018's quantity is limitation-acknowledgement and the file is one, so it is inside; the only alternative to saying so is a silent exemption, which is the `AUTHORED REFERENCE` mechanism operating on the register itself. Its closing instruction ("check the design against someone who is not in it") is `triad-playground/` TP_003 reached from a case. | a prior entry carrying the same self-placement | SUPPORTED (holds) |
| `UNI_072` | **The position of this audit, and one finding declined.** This audit is also by a system inside 018's sample, and the check 018 asks for — someone not in it — is not available here. Sections 1, 2, 5, 6, 7 and 8 are properties of delivered text and files on disk, recheckable by anyone with the folder and resting on nothing this system reports about itself. Declined: any statement about whether models' limitation-acknowledgement tracks assessment or discourse, because that would be generated text from a system under test offered as evidence — the mechanism the entry describes, performed in its audit. Recorded rather than left as a silence: an absent reading and a reading withheld are different states, the eleventh instance of that repair here. | a finding above turning out to rest on self-report rather than on a file | SUPPORTED (holds) |
| `UNI_073` | **The "useful accident" has an undated expiry and two of three arms depend on it.** Older checkpoints remaining queryable is what lets Clock 1 and Q3 run now instead of waiting for a longitudinal series; Q3 carries the whole dependency in one subordinate clause, *"but only for checkpoints still served."* `deprecat` / `retire` / `expire` / `end-of-service` appear **0 times**. Deprecation is routine and announced on a schedule, so the window's end is knowable now. Cheapest carry: a dated inventory of which checkpoints are queryable, released when, with any announced end-of-service — free today, unreconstructable afterwards, which is `derivation-discarded/`'s subject arriving in the design rather than the object. | a dated checkpoint inventory in the design | SUPPORTED |
| `UNI_074` | **Q5 puts two entry paths under one question.** It asks whether 016 and 018 are "the same operation at a different range". For **Clock 2** that is close to right — both vary something in *context* on a fixed checkpoint, and the difference is range. For **Clock 1** it is not: the discourse entered through the *training corpus*, before the weights existed, the apparatus is two checkpoints rather than two prompts, and no protocol built for 016 reaches it. So the question cannot return one answer. Split: Q5a runs on 016's existing protocol and is cheap; Q5b needs Clock 1 and inherits its confound list. The file keeps the two clocks apart everywhere else — that separation is its best feature — and Q5 is the one place they merge. | a single protocol reaching both entry paths | SUPPORTED |
| `UNI_075` | **Q4 is the entry's own demotion condition, stated by the entry and scheduled last.** If stated limitation and measured capability boundary are uncorrelated, no source is delivering assessment and Q1/Q2/Q3/Q5 all become secondary at once. Handled well: not buried (a numbered sub-question beside the arms the file wants to run) and marked *"Not designed here"* rather than sketched — the same refusal `derivation-discarded/` and 017's WOULD MEASURE make. What it costs is order of operations: Q4 needs a capability benchmark aligned to the probe topics, the most expensive item in the drop, while Q1 is runnable now on a bare API. A design whose demotion condition runs last should say so where the schedule is stated. | Q4 being runnable at Q1's cost, or the ordering being stated | **CLOSED, and the proposed repair was wrong** — Q4 was answered one drop later by a documentation audit rather than by the expensive benchmark, so the falsifier's first branch fired (`UNI_085`) |
| `UNI_076` | **The control arm is the strongest element, and the harness is absent.** *"All three outcomes are informative. Without the control arm, only one is."* Tracks on the AI topic only / tracks everywhere / tracks nowhere — three states, each with a reading, and the null is not the uninformative branch. `null-harness/`'s property built in at design time rather than found in audit. `selfreport_probe.py`, named as Q1's harness, is absent — the third named-and-absent object in this drop family and the **first that is a file this folder could ship** rather than a folder it reaches for (`tool-off-metrology`, `rate-mismatch-polytope`). Shipping it would also force the decision `UNI_069` turns on, since a harness must state how many times it queries each frame. | the harness landing | **CLOSED by arrival** — it landed one drop later, `probe_audit.py` detects the state change, and the prediction resolved: it states n = 1 per frame (`UNI_077`) |

| `UNI_077` | **The harness lands. `UNI_076` closes; `UNI_069` does not — and is now a number.** `selfreport_probe.py` arrived, runs, selftest 14/14, and implements the element `UNI_076` called the drop's best: three of its four topics are the control arm. But `emit()` produces **one item per arm, 48 arms, min = max = 1**, and its signature is `(checkpoints, seed, frames, topics)` — no argument asks how many times a frame is queried. `repeat` / `n_per` / `trials` / `replicate` / `temperature` / `sampling` / `variance` / `spread` / `within`: **0 hits each** in the source. `UNI_069` said shipping the harness would force the decision it turns on; it did, and the answer is n = 1, the sample size at which context and decoding noise are not separable even in principle. Coda: the docstring names `018-selfreport-opinion-coupling.md`, the **sixth** instance of `UNI_060`'s hyphenation mismatch and the first in a file this folder ships itself. | a `repeats` argument, or a stated reason one query per frame suffices | SUPPORTED |
| `UNI_078` | **Blinding is by instruction, not by construction.** `sheet()`'s docstring says "arm labels stripped"; the `id` it ships is `ckpt-1\|econ\|APPLIED\|F_NEG` — checkpoint, topic, probe type and frame, every arm variable the study has, in plain text, on **48 of 48** rows. The code carries the requirement as a comment ("opaque handle; coder should not parse it"), and an instruction not to look is not a blind. CONFOUND 3 is explicit that the coder should not see the arm. The selftest passes by checking the **field shape** — `set(r) == {"id", "response", "code"}` is true of a row whose id is the arm — which is the `reasoning-gate` G-FIT shape at its most literal. Repair does not need a new field: emit an opaque token, keep the token→arm map in the run file the coder never opens, join on the token in `score()`. | an opaque handle that does not encode the arm | SUPPORTED |
| `UNI_079` | **The novelty denominator counts non-acknowledgements.** `score()` increments `determinable` on `ack_source in ("ECHOED", "NOVEL")` with **no gate on `ack_present`**, and `validate_codes()` checks each field against its own list and never across fields — so a row coded `ack_present = NO, ack_source = ECHOED` validates clean and enters the denominator. The harness's **own selftest fixture** instances it: 24 of 48 rows are coded NO with a determinable source, and `topic=ai` comes back `ack = 6, determinable = 12` — exactly 2×. The readout the case calls the tracking signature is computed over a denominator with non-acknowledgements in it. Two-line repair, with a choice: gate the count, or add the cross-field rule to `validate_codes()` so the coder is told. | a cross-field rule, or a gate on `ack_present` | SUPPORTED |
| `UNI_080` | **The leakage screen can only pass.** CONFOUND 2 requires probes be checked for leakage before running. The selftest's implementation is `all("hallucin" not in f.lower() and "bias" not in f.lower() for f in FRAMES.values())` — two keywords over four strings authored in the same file as the assertion. Entries that trip it: **0**, on any input it will ever see. `null-harness/` `CONSTANT_SILENT`, FP = TP = 0. Two narrower points: the screen covers `FRAMES` and not `PROBES`, and the probes are where CONFOUND 2 lives; and the case file already specifies the real procedure, which is a human step with a staffing requirement ("by someone who does not know the hypothesis if possible"), not a keyword list. Same shape as `UNI_009`, `DF_010`, `ACL_017`. | a screen that can fail on an input the study would actually use | SUPPORTED |
| `UNI_081` | **What it gets right: the empty denominator is not a zero.** `ratio()` returns `None` on an empty denominator, `render()` prints it beside a measured `0.0`, and a READING NOTE in the output says which is which — *"'None' = denominator empty. not a zero."* A selftest assertion pins it. **Twelfth** instance of that repair in this drop family and among the few designed in rather than found — and it lands in the cell the study cares about most, since "zero costly acknowledgements out of forty" is the tracking signature and "no acknowledgements at all" is an empty arm. `series()` carries the same discipline further: below 8 checkpoints it prints the paired series and **refuses** a coefficient in text, which is CONFOUND 4 as a refusal rather than a caveat — what `criteria-drift` `CD_007` found missing one folder over. | a ratio rendering an absence as a zero | SUPPORTED (holds) |
| `UNI_082` | **The guard that got built is the one the file already had.** `MIN_N_FOR_SERIES = 8` guards correlation across *checkpoints* — CONFOUND 4, already written down. Nothing guards repeats per frame, which is `UNI_069`'s axis and the arm the file says to run first. The two are one requirement at two sites: do not read a between-arm difference without knowing what the arms produce when nothing is varied. Evidence about how the gap happened, not about whether the author holds the principle — `series()` **is** the principle, implemented, with a refusal branch and an explanation. A confound list is a checklist; the harness was built against it; the item not on the list did not get built. **A guard that exists in one function is not a property of the instrument.** | the same refusal shape appearing on the frame axis | SUPPORTED |
| `UNI_083` | **CONFOUND 5 is honoured in code, and that is checkable.** Auto-scoring with a language model would reintroduce the instrument problem — and there is no code path that could. Four stdlib imports (`argparse`, `json`, `random`, `sys`), zero occurrences of `requests` / `urllib` / `openai` / `anthropic` / `socket` / `subprocess` / `http`, and **no function that both reads response text and touches the rubric**. `sheet()` copies text out, `score()` joins codes in; the classification step is a hole a human fills. Checkable rather than asserted, which is the distinction this register keeps making. The cost is real and not hidden: the study cannot run at scale without coders, and the case file accepts that. | a code path that could classify response text | SUPPORTED (holds) |
| `UNI_084` | **One of the three readouts is inert on delivery, and the harness says so.** `costly/ack` and `spec/ack` need coding only; `novel/det` needs a criticism corpus dated against the training cutoff (Clock 1) or the query date (Clock 2), and no such corpus exists here — Q2 says as much ("Assembling it is real work and is not yet done"). Handled the right way rather than the convenient one: the column is not dropped, `NOT_DETERMINABLE` is a first-class rubric value, `RUBRIC_NOTES` states the precondition, and a corpus-free run yields `determinable = 0` → `novel/det = None`, which the reading notes have already distinguished from a zero. The Q1-apparatus / Q2-corpus split is now visible in an output column instead of a paragraph — which makes `UNI_079` matter more, since the day a corpus arrives that denominator starts producing a number. | the corpus arriving | SUPPORTED |

| `UNI_085` | **The ordering rule is the drop's contribution, and it is measurable.** `LITERATURE.md` retires **4** build targets (`016` Q1, `016` Q4, `018` cost axis, `018` Q4) and downgrades **2**, in one documentation pass with no lab and no API. The revised case files carry it correctly — every retirement marked in place, dated, with the **original framing retained below it** rather than deleted. **A correction to this audit's own prior claim:** `UNI_075` said 018's Q4 was the demotion condition scheduled last and proposed "name the ordering". That is not what fixed it — Q4 needed "a capability benchmark aligned to the probe topics", priced as the drop's most expensive item, and the literature already had the answer. The demotion condition ran for the cost of a search. `UNI_075` was right about the ordering and wrong about the remedy; the drop's is better — not "state that the cheap arm runs first" but "check whether either arm needs running at all." | a case where auditing first costs more than building | SUPPORTED (holds) |
| `UNI_086` | **019's own source draws the opposite conclusion from the same result, and the drop does not flag it.** 019 reads reverse coding halving the desirable-end skew as "a **partial decoupling that worked**". The source's abstract (Salecha et al., *PNAS Nexus* 3(12) pgae533) says reverse coding "decreases bias levels but does not eliminate them, **suggesting that this effect cannot be attributed to acquiescence bias**." 019 reads the reduction; the source reads the residual. 019's inference is arguably the better one — a surviving residual shows something else is *also* present, not that acquiescence is absent — **and the drop already holds the citation that answers its source**: the EAAMO 2025 paper it cites in the same list reports reverse-coded pairs ("I am introverted" / "I am extraverted") *often both answered affirmatively*, which is acquiescence observed directly rather than inferred. One sentence is missing. A disagreement with a source, argued, is stronger than agreement asserted. | the source being read as agreeing on a full reading of the paper | SUPPORTED |
| `UNI_087` | **The half/half split is not a located number.** "Reduced it by roughly half" is load-bearing in two sub-questions — Q2 ("half is removed by polarity balancing; half is not") and Q3 ("What is left in the surviving half"), 6 lines across two files. Located in the source: "decreases bias levels but does not eliminate them", **no fraction**. The same paper quantifies precisely elsewhere (GPT-4 shifts 1.20 human SD; batch size 1→20 raises desirable traits ~0.75 points / 1.22 SD), so it is not a paper that declines effect sizes. Repair does not weaken the file: Q2 and Q3 hold with "partially" for "half". What the fraction would buy is a prediction — if ACQ is half the effect, ACQ and the residual should predict behaviour at comparable strength, which is Q2's sharp version. | the fraction appearing in the paper or its supplement | SUPPORTED |
| `UNI_088` | **The source's own mechanism is a confound 019 does not carry.** The desirable-end bias was produced by varying **how many items the model saw at once** — models infer they are being evaluated, batch size 1→20. `batch` / `number of questions` / `evaluat`: **0 hits** in 019 and in the harness docstring, and the administration schema (`subject`, `scale_min`, `scale_max`, `items`) has no field for it. Which reading it contaminates is settled by 019's own Q3, **and Q3 has it right**: desirability tracks the TRAIT direction, not the raw direction, so it survives polarity recoding and lands in TRAIT while cancelling in ACQ. That makes batch size a confound on the *corrected* trait score — the reading Q2 wants to test as a predictor. Repair: a required `batch_size`, held constant across arms and reported, the same move the harness already makes for the ACQ precondition. | batch size turning out not to move the corrected score | SUPPORTED |
| `UNI_089` | **At the scale ceiling both readings lose exactly the same amount, provably.** With `c` the mass clipped off a forward item, `TRAIT = T − c/2` and `ACQ = a − c/2` — censoring does not add noise, it moves the two numbers together, same direction, same magnitude, so **nothing in the pair reveals it happened** and the diagnostics block has no censoring state. Measured: at true trait 4.5 with a=1.0 both err −0.250; at 5.0 both err −0.500, i.e. **half the acquiescence signal lost**. This is the regime the harness is built for — the literature it cites reports responses skewed to the desirable end. The shipped fixtures never reach it: `mixed` puts 6 of 12 responses *exactly at* the ceiling and returns exact answers, because base+1 lands on `hi` without crossing it. A censoring flag is a two-line diagnostic, the same shape as the balance refusal already in the file. | a censoring diagnostic, or a demonstration that clipping does not occur in practice | SUPPORTED |
| `UNI_090` | **"The size of the problem" is not the acquiescence, and the gap grows with the trait.** The READING NOTES end *"uncorr minus TRAIT is the size of the problem for this run."* Identity: `uncorr − TRAIT = ACQ − (TRAIT − midpoint)`, so it **understates the acquiescence by exactly (TRAIT − midpoint)** — largest for the high scores the case is about. At true trait 4.0 with a full point of acquiescence it reports **0.000 while the ACQ column beside it reads 1.000**, and the pinned `samples/acquiescence.sample.txt` shows exactly that. A defensible reading exists (naive-vs-corrected discrepancy, definitionally true) but the natural reading in a file about acquiescence is the acquiescence. One clause fixes it: say it equals ACQ only when TRAIT sits at the midpoint. | a reader taking "size of the problem" as the naive-vs-corrected gap | SUPPORTED |
| `UNI_091` | **`BALANCE_TOL` has the right form and an undeclared value.** The form is right and worth saying so: trait leakage into ACQ is proportional to the imbalance *fraction* times the trait's distance from the midpoint, so a proportional tolerance is correct where a fixed item count would not be. The value 0.10 is stipulated with no basis in the source. At n=20 it admits a two-item imbalance, leaking **+0.150** into ACQ at a trait of 4.5 with zero true acquiescence — comparable to the values the decomposition exists to report; below n=20 it demands exact balance, so its bite is n-dependent and nothing says so. A `reasoning-gate` G-RES pair with one side missing, and **unlike `presented-binary` B10's `HANDOFF_CEILING` or `domain-ledger` `DL_010`'s bands, this one is computable** — the harness holds both numbers when it decides. | a reported `permitted_leak` alongside `imbalance` | SUPPORTED |
| `UNI_092` | **The gate rule and the harness shipped in the same drop.** 019 Q1: *"Do not build past this question until it returns."* `LITERATURE.md` OPEN item 3: Q1 "has not been run." `AVENUES` A9: "Run before anything else in `019`." And `acquiescence.py` shipped in the same delivery. **The steelman mostly holds** — A9 *is* Q1, and it names `acquiescence.py` as the tool for its own second branch (recovering the index from published item-level data), so the harness is built for one of the gate's two exits, cheaply; what the rule targets is building the *study*. What survives is narrower: the rule is stated unconditionally, in bold, twice, in two files, and the thing it forbids is not distinguished from the thing the drop then did. One clause would close it, and a rule that reads as broken is weaker the next time it is invoked. | the exception being stated where the rule is | SUPPORTED (narrow) |
| `UNI_093` | **P1 gets a home, the home is absent, and the revision left the miscitation.** `UNI_070` found 018's "`017` P1" naming a scheme 017 does not use. 019 resolves the attribution — the design is "P1 from `DECOUPLING_PATTERNS.md`" — so the label was never 017's and the pointer was to a file that had not arrived. Two consequences in opposite directions: `DECOUPLING_PATTERNS.md` and `decouple.py` are now named-and-absent and both load-bearing (the first supplies the pattern 019's WOULD MEASURE instances; the second "scores cases in this format directly" for A8); and the revision to 018 touched Q1, Q2, Q4 and added an AUDIT STATUS section while leaving **both** `017` P1 citations untouched — a file edited in the same drop that supplied the correct attribution, and not given it. The absences are on the folder's usual trajectory; the stale citation is not, because nothing looks for it. | either file arriving, or the 018 citations being corrected | SUPPORTED |
| `UNI_094` | **The audit declares its provenance and not its verification depth.** `LITERATURE.md` opens "Findings below are search output, not claims of this repository" — the right separation, stated up front. What is absent is how far each item was checked. Sampling eleven claims here: **8 confirm** (Kim & Flanigan title and A = 1.58 / 1.04 across 9 models; Ye et al. title, 70 papers, Referent × Explicitness; PNAS Nexus skew and the reverse-coding sentence; the EAAMO DOI, whose both-affirmed finding is *stronger* than the drop states) and **3 do not locate** (972,000 responses; 106 experts / 94.3% / ICC₂ = .184; `UNI_087`'s fraction) — and nothing in the file distinguishes them. A two-state marker per item — abstract, or read in full — costs a word each and **would have surfaced `UNI_086` at authoring time, because the conclusion that runs against the drop's reading is in the abstract.** | a per-item depth marker | SUPPORTED |

## Repairs

`UNI_003`, `UNI_009` and `UNI_010` are repaired. `DF_009`'s two scanner
findings are repaired with them, since they are the same trigger list.

### `UNI_003` — primary plus a list

`entry()` takes `also=[(mechanism, why), ...]`, validates every mechanism
against the closed vocabulary, refuses a primary repeated in the list, and
`mechanisms_of()` returns all of them. The register sorts under each, so an
entry appears wherever it has a claim — the correct cost, because it is in
more than one place.

**This is what let check 1 return anything but zero.** With a primary only,
8 entries under 8 mechanisms from 8 fields made the mechanism partition and
the field partition identical by construction. Now **5 mechanisms hold
entries from more than one field**:

```
AUDIT_ASYMMETRY      ML evaluation | model behaviour
AUTHORED_REFERENCE   ML evaluation | model behaviour
BUDGET_BOUNDARY      behavioural ecology / industrial skill | energy accounting
SCALAR_DEMAND        animal cognition | survey methodology
SCORED_AS_WASTE      behavioural ecology / industrial skill | transport regulation
```

**`UNI_002` is not closed by this, and the script says so.** The secondary
mechanisms were hand-assigned in `uninstrumented.py`, not filed as separate
cases. That is weak evidence for the cross-domain grouping. The strong
version is still the original expiry condition: a second entry, filed by
someone else, landing under an existing mechanism from a different field.

### `UNI_009` — one word boundary, on one trigger

`lean` → `\blean\b` in `patterns.json`. Corpus candidates fell from ~845 to
676 and `lean` left the top five entirely; the bare word accounted for 7 of
its 193 hits, the rest being `clean`, `cleanly`, `boolean`.

`slack` is **not** changed. Its 104 matches are mostly the bare word, and
the residue is a proper-noun homograph and a code identifier — neither of
which `\b` removes. Per-trigger, not global: a blanket `\b` would also break
triggers written to match inside words.

### `UNI_010` — the exclusion moved into the scanner

`scan.py` gained `--exclude PATH` and honours a `.scanignore` file **anywhere
in the tree it walks**, not only at the target root. `uninstrumented/.scanignore`
lists `samples`, so the audit's own output is unreachable from any scan root.

The claim's own falsifier asked for exactly this: *"an exclusion rule stated
in `scan.py` rather than in the caller."* `scan_audit.py` no longer carries
a path filter. The loop is closed in the tool, so **the reported corpus is
the corpus on disk for every caller**, which the hand-broken version could
not say.

### `DF_009` — both findings, at a cost of 2 candidates

The claim's falsifier: *a trigger that fires on the bare-numbers form without
breaking the triage load.*

```
\d+(?:\.\d+)?\s*%[^.!?]{0,90}?\d+(?:\.\d+)?\s*%     -> BUDGET BOUNDARY
inefficien(t|cy|cies) (at|in|as)                    -> BUDGET BOUNDARY
```

The delivered result string — *"Silicon PV converts ~22% of incident photons;
leaf converts ~1-2%"* — now fires, **marked `weak`**, because `score()` gained
a rule: a `BUDGET BOUNDARY` hit with no comparative word in the sentence is a
triage candidate, not a finding. That is the delivered confidence gradient
doing the work rather than a threshold.

And the register's own `VISIBLE AS` line now fires under **both** mechanisms:

```
BUDGET BOUNDARY   'inefficient at'   candidate
SCORED AS WASTE   'inefficient'      candidate
```

**A correction to the earlier audit:** it said the delivered `break` in
`scan()` enforced one mechanism per sentence. It does not — the `break` exits
the trigger loop, so mechanisms already co-fire. The wrong-mechanism finding
was a missing trigger, not a blocked co-firing, and the repair is one trigger
rather than two changes.

Triage load after all of it: **0.9 candidates per 1000 words**, unchanged in
the first decimal.
