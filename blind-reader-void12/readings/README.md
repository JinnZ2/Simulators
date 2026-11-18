# Readings filed so far

Two pilots, both 2026-11-18, both filed whatever they showed. Neither counts toward confirming a pair (`PREREG.md`, rule 5: same family as the first reading, as far as we know).

| | pilot-A (brief as written) | pilot-B (brief without the "even if..." clause) |
|---|---|---|
| status by the blindness rule | `UNCERTAIN` (q1, q2, q3 answered `unsure`: the reader says it cannot inspect its training) | `BLIND` (all `no`) |
| declared pairs agreeing with the key | 7 of 8 | 7 of 8 |
| the pair that differs | `GAP_INSTRUMENT_CRASH \| CRASHED`, MAPS in the key, PARTIAL here | same pair, same way |
| groups | 9, identical to the key's | 9, identical to the key's |
| adjusted Rand index over 105 term pairs | 1.000 | 1.000 |
| slot sets equal to the key's | 3 of 15 | 3 of 15 |

## What the two pilots show

1. **The pipeline works.** Both responses validated first time, the scorer ran, and the neutral ids and shuffle were handled without confusion.
2. **The grouping agrees completely, for both briefs.** Each reader built its 9 groups from the definitions and the sources and ended with the first reading's groups: the same 6 pairs joined, none added, none dropped. The two pilots also agree with each other (identical partitions; 13 of 15 slot sets identical). Removing the clause from the brief changed nothing visible at this size.
3. **What that does and does not mean.** It is what you would expect if the groups are what the definitions say. It is also what you would expect if readers of one model family share a reading habit, which two runs of the same family cannot rule out. It is not an independent confirmation, and it cannot say the first reading is right. The test that would separate those is a reader from another family, or a person.
4. **The slots are where the readings part, and the key is the weaker side there.** Only 3 of 15 slot sets equal the key's. The key's slots for seven terms were declared by the first reader (T01, T02, T06, T07, T11, T12, T13) and several are short symbolic lists such as `D, t` or `m, tol, U`. Both pilots instead listed the actual named fields of the record each source produces (for the `numcheck` terms, 21 to 27 top-level keys of the result record). Both choices can be defended; they answer different questions. Tier agreement at the pair level is therefore less informative than grouping agreement, and the scorer reports them separately for this reason.
5. **The one MAPS in the key depends on that choice.** See `2026-11-18_pilot-A/RUN_NOTES.md`.

## Things both pilots noticed in the sources (independently; facts checked by us at the pinned commit)

These are about the other projects' files, not about this folder. Nothing was edited.

- `thermodynamic-accountability-framework/calibration/unified_audit.py`, lines 113 to 117, still say the all-crash case is "not reachable on this branch (a raise is RED here); reachable once the crash-as-coverage change (#82) lands". The same file's code and the glossary route a raise to coverage. The pinned commit is also the current head of that repository's default branch as of this run.
- `.../calibration/expiry_register.py`, lines 146 to 148, record a rank map entry `"UNKNOWN": 1` at `unified_audit.py` line 80. That text is no longer in the file at the pinned commit (`UNKNOWN` is excluded from the rank table, lines 86 to 89). The register marks the row "Recorded, not changed", so it may be an intended historical record; it now describes a state the file no longer has.
- `COMBINED_SPEC.md` line 321 names the crash record `CRASHED(exception, call, inputs)` and line 335 `CRASHED(exception, path)`; the code uses `path` and, in the coverage entry, `input`.
