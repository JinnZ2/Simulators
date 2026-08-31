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

CC0.
