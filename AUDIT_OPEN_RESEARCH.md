# AUDIT_OPEN_RESEARCH.md

**Audit of the `OPEN_RESEARCH.md` batch (19 folders) plus `CATALOGUE.md`,
`simulation-hypothesis-budget/STUDY_PATHS.md`, and the two
`columbia-chain-cascade/` protocol documents.**

Run 2026-08-31 against blob `d3fe0b8`. Spelling, structure, and
cross-reference resolution were checked mechanically; every count below is
reproducible from the tree. Nothing here is a judgement on the content of the
claims — the audit checks whether a reader can *find* and *cite* them.

Two categories are kept apart on purpose. **Repaired** items were mechanical
and unambiguous and are fixed in this commit. **Reported** items need an
author decision and are left standing, because guessing which numbering is
canonical would put a claim in someone's mouth.

---

## REPAIRED

| id | finding | scope |
|---|---|---|
| `OR_001` | **20 of 23 delivered documents carried no markdown structure.** Zero `#` headings, zero pipe tables, `·` in place of `-`. Pasted out of a chat rendering, so on GitHub a claim table rendered as one unbroken paragraph. Restored: headings, pipe tables, list bullets, bold field labels. | 19 files |
| `OR_002` | **A hard claim-id collision.** `climate-modeling/OPEN_RESEARCH.md` defined `CCC_001`–`CCC_018`; `columbia-chain-cascade/` already defines `CCC_001`–`CCC_018`. Identical prefix, identical range, eighteen different claims — and `bridge-impoundment/OPEN_RESEARCH.md` cites `CCC_001` and `CCC_007` meaning the Columbia ones. Renamed the climate-modeling set to `CMA_`, which is unused elsewhere in the tree. The prefix lived in exactly one file, so nothing else moved. **Reversible in one `sed` if the author wants the other prefix.** | 1 file |
| `OR_003` | **A misspelling that was the finding.** `BI_010`'s whole point is that the NVE register never ranks on an English query because the phenomenon indexes under its Norwegian name — and the name was written `jøkullaup`, missing the `h`. The term is `jøkulhlaup` (Icelandic *jökulhlaup*). A reader running the entry's own instruction would have searched a string that does not exist. Corrected in `README.md`, `CLAUDE.md`, `bridge-impoundment/{README,CLAIM_TABLE,OPEN_RESEARCH}.md`. | 5 files |
| `OR_004` | A retrieval-tool artifact left in the prose: `【4†L50-L??】` at `design-basis-ai/OPEN_RESEARCH.md`. Removed. | 1 file |

`OR_003` was **not** applied to `bridge-impoundment/SOURCE_DROP_V2.md`,
`bridge-impoundment/ADDENDUM_DELIVERY.md` or
`mining-increment/ADDENDUM_DELIVERY.md`. Those are delivered verbatim and stay
verbatim; the correction is recorded here instead.

**Content preservation for `OR_001` is proved, not asserted.** Stripping
`| * # ` - ·` and all whitespace from each restored file reproduces the same
string as the same operation on the file at `HEAD`, for 19 of 19 files. The
restoration adds markup and moves nothing.

---

## REPORTED — needs an author decision

### `OR_005` — a restatement that renumbers is not a restatement

This is the finding with the widest consequence and the one an automated
check cannot settle.

Several `OPEN_RESEARCH.md` files restate their folder's claims under the
folder's own prefix but with **different numbers**, so one id names two
claims depending on which file is open. Verified by hand on
`aperiodic-order-sim-stack/`:

| id | canonical (`CLAIM_TABLE.md`) | `OPEN_RESEARCH.md` |
|---|---|---|
| `AOS_003` | the decisive gap is largely inside the artifact budget | *(same)* |
| `AOS_004` | direction survives; magnitude does not | the Cascade sample is sparser and differently shaped |
| `AOS_005` | SIM-C's null is entered as positive evidence | the drop's finite-size baseline is matched-N |
| `AOS_006` | the S(k) figure measures the aperture, not the tiling | the three simulations do not converge |

`AOS_001`–`003` align; `AOS_004` onward do not. Same shape confirmed by hand
in `uninstrumented/` (`UNI_001` canonical is *the entry structure separates
stated confidence from the shape*; in `OPEN_RESEARCH.md` it is *eight
exclusion mechanisms are identified, not seven*).

A containment comparison across the whole batch flags the same pattern in
`bridge-impoundment`, `category-weld`, `closure-cost`, `constraint-assembly`,
`conversation-type`, `criteria-drift` and `design-basis-ai`, and finds
`anchor-interval`, `blame-attribution` and `consensus-anchor` clean. That scan
is a **screen, not a measurement** — it can misfire where the canonical entry
is a one-line heading and the restatement is a paragraph — so the seven are
candidates for a per-folder read, not a count to quote.

Nothing is renumbered here. The decision is which file is canonical, and it
belongs to the author.

**Falsifier:** for each flagged folder, read the canonical table and the
restatement side by side. If the ids align, the screen misfired and this
finding narrows to the two confirmed folders.

### `OR_006` — `CA_` is now a three-way collision

`constraint-assembly/` (`CA_001`–`CA_018`) and `clustering-axes/`
(`CA_001`–`CA_010`) already shared the prefix; `CLAUDE.md` tolerates it with
*"cite with the folder"*. `consensus-anchor/` now adds `CA_001`–`CA_009`,
making three folders and no free range. Unlike `OR_002` this prefix appears in
`consensus-anchor/CLAIM_TABLE.md` and `README.md` as well, so a rename is a
change to the folder's canonical table and was not made unilaterally.

### `OR_007` — three claim rows are truncated in delivery

| where | state |
|---|---|
| `aperiodic-order-sim-stack` `AOS_005` | ends mid-formula at an unterminated code span: *"The report validates ` D_f(AB) − D_f(Cascade)"*. No status. |
| `instrument-bias-sims` `IBS_012` | 40 characters total: *"`**S10/M4: the readout compared r`"*. No status. Also, the folder ships `s1`…`s9` and **no `s10`**, so the row names a sim that is not there. |
| `nonidentity-census` `NID_003` | English half is complete; the Chinese half stops mid-sentence at an unterminated code span. The English also lost characters in transit — *"`[a-z]+(?:s ed)matches plural nouns, sofirms,`"* against the canonical *"`[a-z]+(?:s|ed)` matched plural nouns, so `firms`…"* — the pipe and two spaces are gone. |

Not repaired: the missing text is not recoverable from the tree, and inventing
it would be worse than the gap. The restored tables carry these rows with an
**empty status cell** rather than a guessed one, so they are visible.

`category-weld` `CW_009` was a false positive of the same scan — its status is
`UNTESTED`, a valid value that was simply not in the status vocabulary.

### `OR_008` — new claim prefixes with no canonical table behind them

Six folders acquired a numbered claim vocabulary that exists **only** in
`OPEN_RESEARCH.md`:

| folder | new prefix | what the folder already used |
|---|---|---|
| `antifungal-mechanism-sim` | `AFM_001`–`018` | no numbered table |
| `climate-modeling` | now `CMA_001`–`018` | no numbered table |
| `condition-scoped-authority` | `CSA_001`–`016` | no numbered table |
| `instrument-bias-sims` | `IBS_001`–`020` | `S1`–`S9` per-sim ids |
| `nonidentity-census` | `NID_001`–`017` | `T1-1`, `T2-4`, `T6-3` … |
| `sim-span` | `SPAN_001`–`014` | no numbered table |

The first two and `condition-scoped-authority` are pure additions and are
fine. The last three now carry **two claim vocabularies for one folder**;
`nonidentity-census` is the sharpest, since `T1-1` is cited from outside the
folder and `NID_003` restates it under a second name.

Ten folders also extend past their canonical range — `AMOC` `RGS_005`–`014`
(canonical stops at `004`), `closure-cost` `CC_011`–`017` (canonical `006`),
`conversation-type` `CT_007`–`012`, `constraint-assembly` `CA_014`–`018`,
`bridge-impoundment` `BI_011`–`015`, `blame-attribution` `BA_011`–`013`,
`category-weld` `CW_018`, `aperiodic-order-sim-stack` `AOS_011`. If those are
new claims, the folder's own claim table has not been told.

### `OR_009` — the batch is bilingual in 4 of 23 documents

`CATALOGUE.md`, `nonidentity-census/`, `sim-span/` and `uninstrumented/` are
EN/中文 throughout, in parallel columns. The other nineteen are
English-only. Both are defensible; the mix is not obviously intended, and it
is recorded so it is a decision rather than an accident. The restoration
preserved the bilingual layout and split it into proper two- and four-column
tables.

---

## WHAT WAS CHECKED AND CAME BACK CLEAN

- **Spelling.** ~77,000 words across the batch, dictionary-checked with code
  spans, paths, identifiers and claim ids masked. Every unrecognised token was
  read: all are domain terms (*spinodal*, *echinocandin*, *quasiperiodic*,
  *speleothems*), proper names (*Stommel*, *Kramers*, *Ammann–Beenker*,
  *Liestøl*, *Arcement*), tool names, or consistent British spellings
  (*behaviour*, *normalisation*, *categorise*). One real error, `OR_003`.
- **Retrieval and placeholder artifacts.** `【…】`, `[N†L…]`, `TODO`, `TBD`,
  `??`, `[citation needed]`, `contentReference`. One hit, `OR_004`.
- **Claim ids cited across folders resolve.** `bridge-impoundment` → `CCC_*`,
  `consensus-anchor` → `SHB_*`/`OE_*`/`RD_*`, `nonidentity-census` → `MF_020`
  all point at ids that exist.
- **Repo-wide prefix scan.** Every `XXX_NNN` prefix defined by two or more
  folders was enumerated; the pre-existing ones (`MP_`, `SS_`) are unchanged by
  this batch, `CCC_` is `OR_002`, `CA_` is `OR_006`.
- **The three `columbia-chain-cascade` / `simulation-hypothesis-budget`
  documents already carry correct markdown** and were not touched. They are
  the reference rendering the other twenty now match.

---

## STANDING

`OR_001`–`OR_004` are repaired and pinned by the checks named above.
`OR_005`–`OR_009` are open and each names what would settle it.

The batch's content is not in question anywhere in this file. What was wrong
was that a reader could not render it, and in seven-plus folders could not
cite it unambiguously. Both are cheap to fix and neither was visible from
inside a chat window, which is the ordinary reason this class of defect ships.

---

## RUN AGAINST `RESEARCH_RENDER.md`

The schema landed after this audit was written, and it makes four things
mechanically checkable that were previously matters of taste. Counts below are
over the 20 rendered folders (19 plus `divergence-playground/`, `OR_014`).

### `OR_010` — the six-shape section filled itself, 18 times out of 19

`RESEARCH_RENDER.md` §6 names this as the schema's known failure mode: *a
sentence formula gets built, and then run six times whether or not there are
six shapes.* Measured: **18 of 19 folders fill all six slots**, one fills
three. Zero leave a slot empty.

§6's test is *name the DROPPED mechanism and answer INFLUENCE; if you cannot
name a mechanism, delete the entry.* Neither field exists anywhere: **0 of 19
folders name `DROPPED`, 0 of 19 name `INFLUENCE`.** So the test that would
have caught the padding was not available when the sections were written, and
the sections are uniformly full — which is the signature §6 predicts rather
than a coincidence.

The formula is visible in the text. Every shape entry runs the same three
beats: *many analyses treat X as Y* → *but …* → *so "X as Y" often means "we
treated Z as the explanation". That is a causal attribution error, not
evidence that …*. Where a folder had a real sixth shape the beats carry a
mechanism; where it did not, they carry the sentence.

**What would settle it:** run §6's test on each of the 114 shape entries and
answer `INFLUENCE`. The entries that cannot name a dropped mechanism are the
padded ones, and the count of those is the size of the effect.

### `OR_011` — the padding gap is one gap, and it is the same gap every time

§3 says a count target produces padding. The original protocol asked for
10–20. Measured: of the 16 folders with numbered gaps, **11 sit at exactly 10
or 11** — at the floor of the target, not distributed across it.

And the last gap is the same gap in **15 of 16 folders**: *USER GUIDE —
Non-Specialist Translation*, varying only in who the non-specialist is
(non-modeler, non-engineer, non-expert, clinician). The one exception,
`antifungal-mechanism-sim`, ends on a real mechanism gap.

That gap also carries the anti-pattern §3 quotes by name. §3's weak example is
*"readers find the guide unhelpful"*; the batch contains **16 falsifiers of
exactly that shape**, e.g. *"Non-specialists find the guide unhelpful or
incomprehensible."* One reaction-shaped falsifier per folder, in the gap that
appears in every folder.

So the padding and the un-checkable falsifier are not two findings. They are
one slot, filled by formula, at the tail of almost every list.

§3 gives the two exits and does not require deleting the gap: operationalise
it (*what measured behaviour changes?* — a stranger completes a named task
using only the guide) or mark it `UNDEFINED` and say so. A translation gap is
a real gap; *somebody's reaction* is not a settling condition for it.

### `OR_012` — `What it opens` is absent from every gap in the batch

§3 calls this line **not optional**: *a gap that closes and points nowhere is
a dead end built on purpose.* Measured: **0 of 19 folders carry it**, 182 gap
entries between them. The schema anticipates this — *"the worked instances
stop at the falsifier"* — and both worked instances do exactly that, so the
absence is inherited from the references rather than introduced.

This is the cheapest of the open items and the one with the most compounding
value, because it is what turns a gap list into a traversable map rather than
a queue.

### `OR_013` — the vocabularies are mostly already separate

§5 calls mixing `SUPPORTED` with `NOT_STUDIED` the schema's main defect.
Measured, the batch is better than the schema's self-assessment: **0 of 19 gap
entries carry a claim status**, and **2 of 19 claim tables carry a knowledge
state**. The knowledge states in gap entries are clean — 181 of 183 draw from
§5's six, the two exceptions being one `OPEN` and one `VERIFIED`.

Claim statuses are looser. §2 allows three values; the batch uses **six plus
qualifiers** — 252 `SUPPORTED`, 11 `UNVERIFIED`, 11 `REPAIRED`, then 4 `OPEN`,
1 `UNMEASURED`, 1 `PARTIAL`, 1 `UNTESTED`, and the 3 empty cells from
`OR_007`. `OPEN` and `UNTESTED` are both `UNVERIFIED` with a reason, which §2
already asks for; `UNMEASURED` and `PARTIAL` are knowledge states standing in
a claim-status column, which is §5's defect in its smaller form.

Class prefixes vary the same way. §3 names four; conformance runs from 10 of
11 down to **0 of 15**, and the five folders at zero are the five with the
most gaps — the relation runs the wrong way for a count target, which is
`OR_011` seen from the other side.

### `OR_014` — the second worked instance was filed under a placeholder name

`RESEARCH_RENDER.md` §0 names two worked instances. `nonidentity-census/`
renders as `OPEN_RESEARCH.md` like the rest of the batch. The other was
`divergence-playground/a.md` — the same three documents, the same opening
line, 18 `DP_` claims, 11 gaps, all six shapes — under a filename nobody
would open on purpose, and consequently missed by the `OR_001` restoration,
which globbed `*/OPEN_RESEARCH.md`.

Renamed to `divergence-playground/OPEN_RESEARCH.md` and restored, content
preservation proved against `HEAD` as before. Nothing in the tree referenced
the old path. A reference instance that cannot be found is not serving as a
reference.

Its `DP_002` is the claim §2 quotes as the model of a self-indicting opening —
*the XOR is not a cryptographic seal* — so the schema's own example was, until
this commit, inside a file named `a.md`.

### One tension worth naming: `OR_002` against §2's "never renumber"

§2 states *ids are permanent. A superseded claim keeps its id and changes its
status. Never renumber.* `OR_002` renamed 18 ids, `CCC_001`–`018` →
`CMA_001`–`018` in `climate-modeling/`.

The rule and the repair do not actually collide — §2's ID SCHEME is *three-
letter folder prefix + sequence*, and `CCC_` was two folders' prefix at once,
so the rename restored the scheme rather than breaking the permanence rule.
But it is a renumber by the letter of the sentence, it is recorded here rather
than argued away, and it is reversible in one `sed` if the author would rather
`columbia-chain-cascade` move instead. What is not reversible is leaving both.

---

## READ IN THE MAP VOCABULARY

`META-PROTOCOL.md` §4B is the state set this audit is really using, and the
translation is exact:

- `OR_001`–`OR_004` are `OFF` readings that were cheap enough to walk. The
  direction of each miss named the fix: markup absent → restore markup, one
  prefix in two folders → free the newer one, one missing letter → the letter.
- `OR_005`–`OR_009` are **gaps** — nodes with edges pointing at them that this
  session did not reach. Each names what would settle it, which is what makes
  it a destination rather than a hole.
- `OR_007` is `§12`'s last line instanced: three rows lost their status in
  delivery, and the restored tables carry them **empty** rather than guessed,
  because a missing value written as a value is the one move that cannot be
  undone by a later reader.
- Nothing here is marked failed, rejected, or wrong. The batch's content was
  never in question. What was true is that a reader could not render it, and
  in several folders could not cite it unambiguously — and neither of those is
  visible from inside a chat window, which is the ordinary reason this class
  of thing ships.

CC0.
