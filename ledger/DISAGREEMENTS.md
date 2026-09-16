# DISAGREEMENTS

py_ledger against cobol_ledger. Recorded, never resolved by picking a
winner. py_ledger is authoritative for REACHABILITY; cobol_ledger is
authoritative for PRECISION. A row here is a place where those two
authorities return different numbers.

No entries, and the reason is not agreement. GnuCOBOL is absent from this
environment -- `cobc` and `cobcrun` both resolve to nothing -- so
`cobol_ledger/LEDGER.cob` has never been compiled, the cobol arm reports
UNAVAILABLE, and every claim in every run so far is PRECISION_UNVERIFIED.

An unavailable arm is not agreement. Nothing in this file has been checked.
