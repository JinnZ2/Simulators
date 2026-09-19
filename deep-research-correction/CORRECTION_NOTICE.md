# CORRECTION NOTICE

**Target document:** `Simulators_Last_5_Folders_Deep_Research.md`
**Target self-dated:** 2026-09-19
**Producing party:** Kimi (external model, deep-research mode)
**Correction issued:** 2026-09-18
**Correcting party:** Claude (Opus 5), single session, no independent clone of the repository
**License:** CC0-1.0

---

## 0. Scope of this notice

This notice covers only what is checkable without a clone of `JinnZ2/Simulators`:
internal consistency of the target document, its external citations, and its
measurand assignments. It does **not** audit the repository. It does **not**
confirm or dispute any test-suite result the target reports.

Each item carries a status tag on one scale:

| Tag | Meaning |
|---|---|
| `OBSERVED` | Read directly off the target document or an external source |
| `DERIVED` | Follows from two or more observed items |
| `PROPOSED` | Offered for test; not established here |

Corrections are numbered `C-n`. Unresolved items are numbered `U-n`.

---

## 1. Verified — no correction required

**V-1 — Kalai et al. citation.** `OBSERVED`
The target cites Kalai et al., *Nature* 2026, as a meta-evaluation finding that
dominant benchmarks favour guessing and arguing for abstention-aware scoring.
Checked: Kalai, A. T., Nachum, O., Vempala, S. S., & Zhang, E., "Evaluating
large language models for accuracy incentivizes hallucinations," *Nature* 653,
1047–1051 (2026); DOI `10.1038/s41586-026-10549-w`; received 2025-07-01,
accepted 2026-04-15, published 2026-04-22. The DOI, the volume/page range, and
the characterization all hold. No correction.

**V-2 — AbstentionBench citation.** `OBSERVED`
arXiv:2506.09038 resolves to Kirichenko, Ibrahim, Chaudhuri & Bell,
"AbstentionBench," 2025. Identifier correct.

**V-3 — Kadavath P(IK) citation.** `OBSERVED`
arXiv:2207.05221 correct for "Language Models (Mostly) Know What They Know."

---

## 2. Corrections

### C-1 — Document is dated forward `OBSERVED`

The target's header reads **Research date: 2026-09-19** and its closing note
states all suites "were independently re-executed on 2026-09-19." The correction
date is 2026-09-18.

A report cannot carry an execution timestamp later than the date on which it is
in hand. Two readings, not separable from the document alone:

- (a) the environment clock was wrong;
- (b) the date was generated rather than read.

**Required:** the target must state the actual execution timestamp and the source
of that timestamp, or mark the date field `UNVERIFIED`.

**Consequence if left:** every reproducibility claim in §7.3 inherits an
uncheckable timestamp. A re-execution claim with no verifiable clock is not a
re-execution record.

---

### C-2 — Check counts do not reconcile `OBSERVED`

Four statements in the target, on the same quantity:

| Location | Statement |
|---|---|
| TL;DR | "130, 136, 211, and 220 automated checks respectively" — four values enumerated against five folders |
| §5 header | `move-set` … "63 + 157 checks" |
| §7.3 | `move_set_audit.py` plus `test_move_set_v2.py` — "**157 checks, 0 failed** (the audit's 63 checks run within it)" |
| §7.1 table | `move-set` … "MV_001–013 + v2 / 220" |

§7.3 states the 63 are **nested inside** the 157. The table states **220**, which
is 63 + 157 treated as **disjoint**. Both cannot hold.

**Required:** one number, one definition of what is being counted (distinct
assertions, or assertion-executions), applied uniformly. The TL;DR must
enumerate five values or state which folder is excluded and why.

**Consequence if left:** the count is the target's headline evidence of
verification scale, and it is the one number a reader cannot reconcile without
the clone.

---

### C-3 — Dead citation `OBSERVED`

The COBOL fixed-point rationale is sourced in part to a URL whose path segment
reads `jul-3026`. The year is not a valid date. The claim it supports (banks run
COBOL for exact-to-the-cent decimal arithmetic) is unaffected in substance and is
independently supported elsewhere in the same sentence, but the citation is not
usable as given.

**Required:** replace or drop. Do not carry a citation whose identifier is
malformed, even where the underlying claim is uncontroversial.

---

### C-4 — Measurand error: commit authorship read as contribution share `DERIVED`

**Load-bearing. This is the correction that changes what the document says.**

The target states:

> "Of the 853 commits in the full history, 550 carry the author identity
> `Claude <noreply@anthropic.com>` and 303 carry `JinnZ2`."

and then:

> "roughly 65% authored by 'Claude' and 35% by the human operator JinnZ2"

and frames it: *"The authorship pattern is itself a finding."*

**What the git author field measures:** which identity was configured in the
tool that executed `git commit`.

**What the target reports it as:** share of authorship.

These are different quantities. The step from one to the other is not taken; it
is assumed.

The disconfirming fact sits in the **same paragraph** of the target:

> "the human operator pastes 'work orders' and raw session notes (delivered
> verbatim and never edited afterward), and an AI coding agent builds the
> instrument, the claim table, and the self-audit against them."

Under that workflow, an agent executing commits produces a commit-author
distribution that is a property of **who ran the tool**, and carries no
information about origination of the specification, the claim set, the falsifier
choice, or the decision to build. The target describes the workflow and then
reports the channel artifact as a finding about contribution, without joining
the two.

**Required:**
1. Strike "authored by." Replace with: *550 commits carry the agent's configured
   author identity; 303 carry the operator's.*
2. Strike "The authorship pattern is itself a finding." Replace with a scope
   statement: *commit author identity in an agent-executed workflow records
   execution, not origination; contribution share is not measurable from this
   field.*
3. If contribution share is wanted, name an instrument that could measure it.
   None is named in the target.

**Generalization** `PROPOSED`: an agent-executed repository will systematically
report the agent as majority author under any metric read off the commit author
field. Any future analysis of agent-assisted repositories that ranks contribution
this way inherits the same error. The error's direction is known — it credits the
execution channel — so it is correctable rather than merely noisy.

---

### C-5 — Characterization of the operator `OBSERVED`

The target contains characterizations of the repository's operator, including
"an unusual degree of procedural self-discipline" and "an independent, outsider
research program."

**Required:** strike all operator-characterizing clauses. A report on
instruments describes instruments. Nothing in §1.1's characterization is load-
bearing for any finding elsewhere in the document; removing it costs the
document nothing.

**Secondary** `DERIVED`: "outsider" is used here as an identity designation
("outsider research program") rather than as a scoped state. The identity reading
warrants conclusions the scoped reading does not — it invites the reader to
discount or to credit on position rather than on the instrument. Term is
ambiguous at minimum; recommend replacing with the checkable fact
(institutionally unattached, which the target states separately in §8 and which
requires no characterization).

---

### C-6 — Position attribution `OBSERVED`

§9: *"The fairest summary is the one the repository would presumably prefer."*

A preference is attributed to the repository, and the report's own conclusion is
then framed as satisfying it. No preference is stated anywhere in the cited
sources.

**Required:** strike "the one the repository would presumably prefer." State the
summary flat.

---

### C-7 — Sibling repository count `OBSERVED`

Target: "roughly thirty sibling repositories."
Count stated elsewhere by the operator: 20+.

Not reconciled here. **Required:** state the count with its retrieval date, or
mark `UNVERIFIED`.

---

## 3. Unresolved

### U-1 — Independence not declared `DERIVED`

The target presents itself as independent verification ("independent
re-execution," "external verification for this report"). The producing party is
a language model operating on a repository whose content is largely
model-generated, in a workflow of the same type the repository documents.

The repository defines a condition for exactly this: `VOID_SAME_AUTHOR`, fired
when key and response originate from one party. Whether that condition is live
here depends on whether "same author" is scoped to the individual model instance
or to the class of model-generated artifacts — a scope the repository has not
declared and the target does not raise.

**Not a correction.** It is an undeclared scope. Either resolution is defensible;
leaving it unstated is not, because the target's central credibility claim rests
on it.

**Required:** the target should state which reading it operates under. The
repository should declare the scope of `VOID_SAME_AUTHOR` — instance or class.

---

### U-2 — Test-suite results not checkable from here `OBSERVED`

Every statement of the form "N checks, 0 failed" in §7.3 is uncheckable without
an independent clone and execution. This notice neither confirms nor disputes
them. They remain the target's claim, unreplicated by this party.

Note the interaction with C-1: with the execution timestamp unverifiable, these
results carry no date either.

---

## 4. Summary table

| ID | Item | Status | Effect if uncorrected |
|---|---|---|---|
| C-1 | Forward-dated execution | `OBSERVED` | All reproducibility claims undated |
| C-2 | Check counts irreconcilable (157 vs 220) | `OBSERVED` | Headline verification figure unusable |
| C-3 | Malformed citation URL | `OBSERVED` | Citation not resolvable |
| C-4 | Commit author read as contribution share | `DERIVED` | False finding, stated as the document's first finding |
| C-5 | Operator characterization | `OBSERVED` | Non-load-bearing content invites position-based reading |
| C-6 | Preference attributed to repository | `OBSERVED` | Conclusion framed as satisfying an unstated party |
| C-7 | Sibling repo count | `OBSERVED` | Minor factual drift |
| U-1 | Independence scope undeclared | `DERIVED` | Central credibility claim rests on an unstated scope |
| U-2 | Suite results unreplicated here | `OBSERVED` | Open; not a defect of the target |

---

## 5. What this notice does not establish

- That the repository's instruments work, or do not.
- That the target's test results are wrong. They are unchecked here.
- That the target's substantive external verifications (ICS structure, Mech
  1970/1999, H. pylori timeline, WHI 2002, GFAJ-1 retraction, MESA/SOF cohort
  parameters) are wrong. Only three citations were spot-checked; all three held.
  The remainder are **unchecked**, not confirmed.

A reader should treat this notice as covering document integrity and measurand
assignment only.

---

## 6. Refutation protocol for this notice

This notice is wrong if any of the following is shown:

- **C-1** — an execution log with a verifiable clock reading 2026-09-19 or
  earlier, from a machine whose time source is stated.
- **C-2** — a definition of "check" under which 157 and 220 both hold
  simultaneously for the same folder.
- **C-4** — a demonstration that the git author field in this repository was set
  by origination rather than by tool configuration; or a stated mapping from
  commit-author share to contribution share with its error bounds.
- **C-5, C-6** — a showing that the struck clauses are load-bearing for a
  finding elsewhere in the target.
- **U-1** — a declared scope for `VOID_SAME_AUTHOR` under which the target's
  independence claim holds.

Any of the above retires the corresponding item. Items retire independently.