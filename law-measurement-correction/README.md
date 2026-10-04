# law-measurement-correction

The correction notice against an outside report, filed beside the records the
dispatch asked for. Same arrangement as `deep-research-correction/`, with one
difference: the report itself is **not** in this folder, because its file was
not delivered to the session that filed this. The notice carries the zip name.

    report     "Law as Unvalidated Measurement - Deep Research and Opportunity Map.md"
               in OKComputer_Deep_Research_Idea_Exploration.zip, by another model
               (Kimi OKComputer). Not the repo owner's writing, claims or voice.
               Not an evidence layer for the notes it read.

## Files

| file | dispatch item | what it is |
|---|---|---|
| `CORRECTION-law-as-unvalidated-measurement-2026-10-03.md` | CC-1 | sections A-G verbatim from the dispatch, with its provenance block |
| `NAMED_AND_ABSENT.md` | CC-2 | `why-recovery` and `split-ledger / parks`, recorded, not scaffolded |
| `VERIFICATION_2026-10-04.md` | CC-3 | the F/UNVERIFIED items, one of VERIFIED / CONTRADICTED / NOT_FOUND each |
| `DYED_FUEL_LEDGER_SETTLE.md` | CC-4 | column A settled against 26 CFR 48.4082-1; B and E/F NOT_EVALUABLE |
| `DESIGN_frame-substitution-eval.md` | CC-5 | the rebuilt benchmark, design only, PROPOSED |
| `check.py` | — | reads the five records back; edits none |
| `RECONCILIATION.md` | — | this dispatch was also run by another session (`law-as-unvalidated-measurement/`, `60152f7`); row-by-row differences |

## Second pass of the same dispatch

Another session ran this dispatch first, with the report zip and the ledger
rows in hand, into `law-as-unvalidated-measurement/` on branch
`claude/law-measurement-correction`. This folder was pushed to a separate
branch and overwrites nothing. Two copies of sections A-G now exist; which
folder merges is the owner's decision. `RECONCILIATION.md` lists where the two
passes differ.

## Depth, stated once

Every primary source host was refused by this environment's egress gate on
2026-10-04 (eCFR, EUR-Lex, arXiv, OECD, GPO, Cornell LII, IRS, DOJ, DEA, among
others). Every VERIFIED and CONTRADICTED row, and the column A settlement, rests
on a web-search result that names the URL and carries the quoted text, not on
the page having been opened.

## The ledger the CC-4 columns belong to

Not located. It is not in this repository and not in `JinnZ2/dyed-fuel-diff`
(`8d6c210`), which holds a sensor-coupling instrument set with no dose, site,
float or counterfactual column.

## Run

    python3 law-measurement-correction/check.py              # the readings
    python3 law-measurement-correction/check.py --selftest   # readings + planted violations

The check count is printed by `--selftest`, not stored here. Stdlib only,
parses under 3.9, no network, CC0.
