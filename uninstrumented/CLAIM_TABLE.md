# CLAIM_TABLE — uninstrumented

Ten claims, `UNI_001..010`.

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
| `PROXY_SUBSTITUTION` | — (no entry at all — `UNI_007`) |
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
