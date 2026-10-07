# law-as-unvalidated-measurement

A correction notice against an external deep-research report, the register of
what that report names that does not exist, the three settle items for the
dyed-fuel enforcement ledger, and a design note for the eval the report's §8.1
should have specified. The report itself is NOT landed here.

```
target report     "Law as Unvalidated Measurement - Deep Research and Opportunity Map.md" + 6 figures
delivered as      032cc481-OKComputer_Law_Measurement_Report_Critique.zip
sha256            3205096cfb344bc2132ccc923570157c4c3d5ff5722c24ab9886b19d109f7f66
author            Kimi OKComputer (another model). Not the repo owner's writing.
input it read     two memory notes (regulation-archaeology-failure-strata, why-recovery-box-edge-instrument),
                  present in no repository reachable from this session
why not landed    the audit dispatch: the report is not an evidence layer for the notes and is not to be
                  filed as one; if uncommitted, commit only the correction and a pointer to the zip name
```

## Files

```
CORRECTION-law-as-unvalidated-measurement-2026-10-03.md   sections A-G verbatim from the auditor's packet;
                                                           section H this session's verification pass
NAMED_AND_ABSENT.md                                        why-recovery, split-ledger/parks, the two /areas/
                                                           notes, RECOVER-THE-LAW
LEDGER_SETTLE-dyed-fuel-2026-10-03.md                      column A settled (3.9 lb SR26-eq / 1000 bbl),
                                                           column B NOT_EVALUABLE, columns E/F split zeroed/moved
DESIGN_frame-substitution-eval.md                          PROPOSED; no harness
check.py                                                   recomputes the mechanical items; reads the report
                                                           ONLY if handed its path, and reports NOT_PRESENT
                                                           otherwise, never a pass
```

## Placement

Located per the dispatch's LOCATE FIRST: `regulation-archaeology` and
`why-recovery` live in no repository; `uninstrumented/` lives here; the
dyed-fuel-diff specimen lives in `JinnZ2/dyed-fuel-diff`. The precedent for a
correction against an external report about this material is
`deep-research-correction/` (named in the dispatch as
`CORRECTION-simulators-deep-research-2026-09-18.md`; the file in the tree is
`deep-research-correction/CORRECTION_NOTICE.md`). Landed beside it as its own
folder because the target is a different document about different material.

## Run

```
python3 check.py                      # mechanical checks without the report
python3 check.py --report PATH.md     # adds the quote and hash checks against the report file
```

Stdlib only. Parses under 3.9. CC0.
