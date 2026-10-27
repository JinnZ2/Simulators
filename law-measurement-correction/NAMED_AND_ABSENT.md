# NAMED-AND-ABSENT register — law-measurement-correction

CC-2 of the 2026-10-03 dispatch. Record, do not scaffold. No register for this
state existed anywhere in this repository (checked: no file or folder whose job
is to track named-and-absent objects; the state is recorded per folder in claim
tables only), so the register for these two entries lives here.

Neither instrument is built from the report's text. The report's §10 assumes
`why-recovery` exists as a repo instrument; it does not.

## Entries

| name | state | date | where it is named | what resolves |
|---|---|---|---|---|
| `why-recovery` | NAMED-AND-ABSENT | 2026-10-04 | the report's §10, as a repo instrument; the memory note it read, `why-recovery-box-edge-instrument` | no path in any clone in this session (Simulators, the six other attached repos, `JinnZ2/dyed-fuel-diff`). The only text hits are the English phrase "why recovery" in `relational/confusion_spectrum.py` (a printed heading) and `relational/research_context.md` (a bullet). Neither is an instrument. |
| `split-ledger` / `parks` | NAMED-AND-ABSENT | 2026-10-04 | relayed report of 2026-10-03 | no path anywhere. `parks` has 0 hits in the tree. `split-ledger` matches only the phrase "pre-split ledgers" in the `move-set/` paragraph of `README.md` and `CLAUDE.md`, a different sense (the split of one absence move into six). The relayed report placed the hits "in the uninstrumented folder's vocabulary"; on this tree at `c03efc4` they sit in the move-set entry instead. Recorded as measured, not reconciled. |

The top-level `ledger/` folder is a claim-value ledger (committed expected
values, two arms). It is not `split-ledger` under another name.

## How the absence is checked

`check.py` resolves each name by PATH existence across the tree (a directory or
file named for it), never by grepping for the name. A text search would count
this register and the correction notice that names them, which is the
self-reference loop this repository has recorded before (`UNI_010`,
`QA_007`). If either instrument lands, the check flips to `RESOLVES` and this
register is stale, not wrong.
