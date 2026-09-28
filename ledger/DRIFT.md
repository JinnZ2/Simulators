# DRIFT

Append-only. Never pruned. Each entry is one run in which a value moved
away from its committed EXPECTED value.

A pruned drift log cannot tell a value that never moved from one whose
movement was deleted, which is why nothing is ever removed from here.

No entries: no run has found drift. That is not the same as no run having
looked -- `ledger/records/` is empty, so no run has had anything to look
at. See `ledger/records/README.md`.
