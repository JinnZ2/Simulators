# DISAGREEMENTS

py_ledger against cobol_ledger. Recorded, never resolved by picking a
winner. py_ledger is authoritative for REACHABILITY; cobol_ledger is
authoritative for PRECISION. A row here is a place where those two
authorities return different numbers.

`ADDENDUM.md` requires the **T+3 and T+9 readings to be recorded here
whatever they are, including zero. A zero reading is the result, not an
absence of one.** `review.py --record` appends one.

## State

No entries, and the reason is not agreement. GnuCOBOL is absent from this
environment -- `cobc` and `cobcrun` both resolve to nothing -- so
`cobol_ledger/LEDGER.cob` has never been compiled, the cobol arm reports
UNAVAILABLE, and every claim in every run so far is PRECISION_UNVERIFIED.

An unavailable arm is not agreement. Nothing in this file has been checked.

## Readings

### 2026-09-16  pre-run baseline, not a T+3 or T+9 reading

- verdict: **UNDECIDED**
- disagreements found: **0** (classified 0, unexplained 0)
- completed cross-ledger runs: 0 (0 with the arm UNAVAILABLE, which is not exposure)
- distinct machines: none; compiler versions: none
- ledger reds overridden or ignored: 0 (OVERRIDES.md is empty and nobody has been asked to fill it; this is a count of a log that exists, not an inference)
- findings no other check found: UNRECORDED (the ledger has never run over a real record set, so it has produced no findings to compare)
