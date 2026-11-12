# Law audit card vs existing dirs: coverage report

Work order: LAW AUDIT CARD vs EXISTING DIRS (2026-11-09). Read-only, no edits.

- Read at: `JinnZ2/Simulators` `origin/main` = `a8028b2`, from a throwaway detached worktree,
  removed afterwards. Nothing was committed.
- Status: items 1-4 DONE. Nothing BLOCKED.

---

## 1. The two directories

### 1a. `law-as-unvalidated-measurement/`

**Stated purpose** (README, verbatim):

> A correction notice against an external deep-research report, the register of
> what that report names that does not exist, the three settle items for the
> dyed-fuel enforcement ledger, and a design note for the eval the report's §8.1
> should have specified. The report itself is NOT landed here.

**Method** (`check.py` header, verbatim):

> Recomputes the mechanical items of the correction notice. Two layers:
>   1  arithmetic and structure that need no external file
>   2  checks against the target report, run ONLY when --report PATH is given;
>      without it every report-side row reads NOT_PRESENT, which is not a pass.

**Inputs** (README, verbatim):

> target report     "Law as Unvalidated Measurement - Deep Research and Opportunity Map.md" + 6 figures
> input it read     two memory notes (regulation-archaeology-failure-strata, why-recovery-box-edge-instrument),
>                   present in no repository reachable from this session

**Outputs.** Five records: the correction notice, `NAMED_AND_ABSENT.md`, the ledger settle, a
design note, and `check.py`.

**Status** (README, verbatim):

> DESIGN_frame-substitution-eval.md                          PROPOSED; no harness

**Code runs, in a throwaway worktree.**

- Bare run: `checks: 38   FAIL: 0   NOT_PRESENT: 1   (NOT_PRESENT is a gap, not a pass)`, exit 0.
- `--selftest`: refused with `check.py IS the check; run it bare or with --report PATH`, exit 2.
  It has no separate selftest by design.
- The one NOT_PRESENT row is the report file, which is not in the tree.

### 1b. `law-measurement-correction/`

**Stated purpose** (README, verbatim):

> The correction notice against an outside report, filed beside the records the
> dispatch asked for. Same arrangement as `deep-research-correction/`, with one
> difference: the report itself is **not** in this folder, because its file was
> not delivered to the session that filed this.

**Method** (`check.py` header, verbatim):

> Reads the seven records in this folder back and checks what is checkable
> about them. It edits none of them and adjudicates no claim in the report.

**Inputs.** The same outside report, by name only. The dispatch's CC-1..CC-5 items.

**Outputs.**

- The notice.
- `NAMED_AND_ABSENT.md`.
- `VERIFICATION_2026-10-04.md`, which puts each item in one of three states: VERIFIED,
  CONTRADICTED or NOT_FOUND.
- `DYED_FUEL_LEDGER_SETTLE.md`, `DESIGN_frame-substitution-eval.md`, `RECONCILIATION.md`,
  `CC3b_PRIMARY_RERUN_2026-10-04.md`, `CC4_MERGED.md`.

**Status** (README, verbatim):

> Two copies of sections A-G now exist; which folder merges is the owner's decision.

> Every VERIFIED and CONTRADICTED row, and the column A settlement, rests
> on a web-search result that names the URL and carries the quoted text, not on
> the page having been opened.

**Code runs, in a throwaway worktree.**

- Bare run: prints readings 1-7, exit 0.
- `--selftest`: `selftest: 24/24 passed`, exit 0.

### Shared reading

Neither directory is a per-law audit instrument. Both are correction records about one outside
report, "Law as Unvalidated Measurement". The only law-level material in them is:

- the dyed-fuel ledger settle,
- the EU fiscal-marker review cycle (correction notice §C),
- the Sunday-laundry NOT_FOUND rule (§D),
- a design for a frame-substitution eval. Its measurand is the AI's domain of answer, not the
  law.

---

## 2-3. Coverage: card field | covered by | missing

| card field | covered by (dir/file) | missing |
|---|---|---|
| stated purpose (first principles) | Nowhere as a field. Nearest is the kept item in correction notice §G (both dirs), "premise-registry schema (rule -> stated premise -> type -> timestamp -> review flag)", which is KEPT as content and not built. §D's rule: "if the laundry statute + premise cannot be located, output NOT_FOUND." | No field, no record type, no check |
| target outcome (e.g. safety) | Nowhere | Field absent |
| enforcement mechanism as specified | Partial and law-specific: `LEDGER_SETTLE-dyed-fuel-2026-10-03.md` / `DYED_FUEL_LEDGER_SETTLE.md` column A settles the specified dose against 26 CFR 48.4082-1(b) ("at least 3.9 pounds of the solid dye standard Solvent Red 26 per thousand barrels"). | Not general; one statute only |
| evidence enforcement produces the outcome (cuts declared, no welds) | Nowhere for laws. Correction notice §B finds measurand substitutions in the REPORT's evidence (e.g. "Word count ≠ premise count"), which is the method in kind, but aimed at the report, not at a law's effect. | Field absent; no outcome-evidence ledger |
| cut-sensitivity (does the verdict flip if the boundary moves?) | Nowhere. The ledger's column B is the nearest instance: `NOT_EVALUABLE`, "defines 'site' nowhere", with five candidate readings, "Which it is changes column B by that factor." That is boundary sensitivity, recorded as a single unevaluable cell. | No flip test |
| scope still valid? (purpose outlived?) | Not in either dir. Correction notice §C records the EU marker as a "cycle of scheduled reviews, not one lag" and notes the review triggers are "tax evasion, health damage, environmental damage". §B line: "Texas sunset as premise recheck ←✗ reviews AGENCIES, not empirical basis of rules". | Field absent; see sunset note below |
| verdict: KEEP / EDIT / REDO / RETIRE / UNRESOLVED | Nowhere for laws. §G uses KEEP / REBUILD for parts of the REPORT ("KEEP OECD ex-post numbers ..."; "REBUILD §8.1 benchmark"). | Five-value field absent |
| void fields stay void | In method: NOT_PRESENT "is not a pass" (dir A); NOT_EVALUABLE and UNFILLED fields in both ledger settles ("SEPARATE, UNFILLED FIELD"). | Not applied to a law card, because no card exists |

### NAME_COLLISIONs

These are names the card shares with existing tree vocabulary that carries a different meaning.

- **verdict.**
  - The repo-wide rule, and READ_ME_THIS_WAY §4: "The tools **read**. They do not decide anyone's
    value. A readout is not an automatic ranking or verdict."
  - A KEEP/RETIRE verdict field on a law is the term that rule warns against.
  - It needs a stated reading, for example "verdict = recommended action under the declared cut,
    owner decides".
- **KEEP / REBUILD.** Correction notice §G (both dirs) uses KEEP/REBUILD for parts of a report.
  The card uses KEEP/REDO for laws. That is a different object, and REDO ≠ REBUILD.
- **KEEP** also appears in other senses:
  - `gap-markers/GAP_MARKERS.md` L57 ("KEEP IT", a sampling assumption),
  - `ledger/ADDENDUM.md` L15 ("KEEP the cobol_ledger if"),
  - `instrument-index/INDEX-SPEC.md` L238.
- **cut.**
  - `undeclared-cuts/` (a register of unrun experiments),
  - `ontology-probe` term-cut,
  - `nonidentity-census` and `selection_cuts.py` cuts,
  - `animacy-pass/unweld.py` declared boundary.
  - The card's "cut" means an accounting boundary. That is closest to `declared-frame`'s
    `boundary` field, and to `animacy-pass/unweld.py` "boundary".
- **weld.** `category-weld/` defines a weld as independent quantities fused into one term. The
  card's "no welds" matches that meaning, but should point there explicitly.
- **scope.** `fold-matrix`/`declared-frame` use scope for frame fields. TAF
  `core/regulatory_scope_audit.py` uses scope for a regulation's operating envelope. That second
  one is the card's meaning.
- **stated purpose.** TAF `core/regulatory_scope_audit.py` L87:
  `first_principle_intent: str           # what harm it was meant to prevent`.
  Same concept, different field name. It is outside the two dirs and outside Simulators.
- **VOID.** Round 7 introduced VOID in `model-provenance` and `cutoff-attribution`, meaning "no
  information". That is the card's sense, so it is consistent, not a clash. Noted so both stay
  that way.

### Obsolete-law / sunset cases

Neither dir handles them as cases.

- Both carry the same §B line flagging that Texas sunset review "reviews AGENCIES, not empirical
  basis of rules".
- Both carry §F numbers: "Texas Sunset: 95 abolished (42 + 53) ... 34 more states adopted some
  sunset form".
- Both carry the §F inconsistency note: "decline and adoption are different claims, both need
  dates".

The one existing obsolete-law instrument found is outside Simulators: TAF
`core/regulatory_scope_audit.py`.

- It declares `first_principle_intent` and per-regulation `ScopeVar` ranges.
- Its verdict is one of IN SCOPE, `[OUT OF SCOPE -- INTENT EXPIRED]` or OUT OF SCOPE INTENT
  PRESERVED.
- That covers the card's "scope still valid / purpose outlived".
- In Simulators, `reg-uncertainty-registry/` (WO-REG-1) holds regulatory decisions with
  direction, consequence, reversals and gaps. Its README does not state a purpose-outlived or
  sunset field. That was not checked further here.

---

## 4. Proposal (not built): smallest additive change

Add one new file and one check. Nothing existing is edited.

1. **`law-audit-card/CARD_SCHEMA.md`.** A new folder, so neither law dir is touched. It holds the
   card's eight fields, each carrying one of OBSERVED / DERIVED / PROPOSED / VOID.
   - VOID is never 0 and is never dropped.
   - `stated_purpose` reuses TAF's `first_principle_intent` by name, cross-referenced.
   - `cut` is defined as `declared-frame`'s `boundary` and points there.
   - "no welds" points to `category-weld/`.
   - `verdict` is redefined as "recommended action under the declared cut; owner decides". This
     answers the READ_ME_THIS_WAY collision.
   - REDO is distinguished from §G's REBUILD.
2. **`law-audit-card/card.py` (stdlib).** Loads a card and refuses it, naming the field, if any
   of these holds:
   - a field is missing (VOID must be written, not omitted);
   - a verdict is set while `evidence` or `cut` is VOID. The verdict is then forced to
     UNRESOLVED.
   - the cut-sensitivity field has fewer than two declared boundaries. Its value is
     FLIPS / HOLDS / VOID, computed by re-reading the verdict under each declared boundary.
3. **Seed one card per existing law specimen**, from material already in the tree:
   - 26 CFR 48.4082-1, with enforcement mechanism from the settled column A and evidence VOID;
   - EU 2022/197 marker, with scope from §C;
   - the Sunday laundry law, with every field VOID.
   - Nothing is drafted from memory.

Sunset and obsolete-law handling would then be the card's `scope_still_valid` field. That field
can import TAF `regulatory_scope_audit`'s three verdicts, which would turn the field's free text
into a declared check.
