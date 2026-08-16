# CLAIM_TABLE — uninstrumented

Twelve claims, `UNI_001..012`. **Three repaired** (`UNI_003`, `UNI_009`,
`UNI_010`), see *Repairs* at the end.

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
