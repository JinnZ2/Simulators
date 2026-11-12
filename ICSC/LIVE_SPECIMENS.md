# ICSC live specimens

Cases in this repository where the measurement process, not the system under study, produced the
reading. Each is OBSERVED in this tree and checked by `check_v02.py`. The first two are cited inside
`SPEC_v0.2.md`; the third is added here (2026-11-10). Nothing in the spec is run or built.

| # | spec item | specimen | where |
|---|---|---|---|
| 1 | section 3, F11 / W2 | stale release table: `model-provenance` decoded commits against a table with no row for the current model and still printed a model; under F11 the decode is CONDITIONAL | `model-provenance/CLAIM_TABLE.md` MP_010 |
| 2 | section 4.1 G1, T29, T30 | circular controls: cutoff-attribution null calibration built from exactly the evidence the rules accept, so 0/2400 forced attribution shows wiring, not validity: CONDITIONAL(circular_control) | `cutoff-attribution/null_calibration.py` |
| 3 | section 9.2 G3, T31 | self-firing scanner: an instrument reading its own vocabulary as signal | `law-audit-card/card.py` `tool_writes_no_disposition` |

## 3. Self-firing scanner

**What happened (OBSERVED, 2026-11-10).** `law-audit-card/card.py` has a check that the tool never
writes a disposition: an AST scan for the literals KEEP, EDIT, REVISE and RETIRE outside the
declared vocabulary. Its first run returned `['KEEP', 'EDIT', 'REVISE', 'RETIRE']`. The module
writes no disposition. The hits were the scanner's own list of words to look for, inside the
scanner's own function body.

**ICSC reading.** Under section 9.2 the deviation was assigned to the subject (the module under
test) when its source was the apparatus (the checker). In the section 9.2 bins: true source
`apparatus`, first assigned source `observed system`. The same shape recurs across this tree: a
guard firing on the sentence that states what it refuses (`investigation-sim` IS_007,
`failure-mode-register` FMR_036 / FMR_041, `uninstrumented` UNI_009 / UNI_010).

**Fix.** The checker excludes its own function body, by AST node, not by text (`card.py`
`tool_writes_no_disposition`).

**Planted test.** The fix could make the check go silent on everything, so a planted case shows it
still fires: the module's own source plus one added line `X = {"value": "RETIRE"}` must return
exactly `['RETIRE']` (`law-audit-card/tests/test_card.py`, `test_tool_writes_no_disposition`).

**Limit.** Excluding the checker's own body is right only while the checker writes nothing. If a
later edit made the checker itself write a disposition, the exclusion would hide it.
