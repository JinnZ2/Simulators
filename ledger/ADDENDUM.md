ADDENDUM. Commit BEFORE the ledger runs.

The COBOL precision ledger is built on an
UNTESTED hypothesis: that float arithmetic
corrupts claim values in this tree. Nothing here
has demonstrated it. The build proceeds as
specified; this addendum makes the hypothesis
falsifiable.

--------------------------------------------------
COMMITTED IN ADVANCE — do not edit after results
--------------------------------------------------
Review dates: T+3 weeks, T+9 weeks from first run.

KEEP the cobol_ledger if, by T+3:
  >= 1 cross-ledger DISAGREEMENT that is not
  explained by a rounding-mode difference in the
  ledger sources themselves

DROP it if, by T+9:
  0 disagreements, AND
  cross-ledger runs completed on >= 3 distinct
  machines or compiler versions

UNDECIDED if:
  fewer than 3 cross-ledger runs completed —
  insufficient exposure, extend, do not conclude

Record the T+3 and T+9 readings in DISAGREEMENTS.md
whatever they are, including zero. A zero reading
is the result, not an absence of one.

--------------------------------------------------
BULK MEASUREMENT — same dates
--------------------------------------------------
At each review, record:
  lines of ledger source vs lines of sim source
  wall time of a full ledger run
  number of findings the ledger produced that were
    NOT found by any other check
  number of times a ledger red was overridden or
    ignored

The last one is the real signal. A gate that gets
routinely overridden has become bulk regardless of
what it catches.

--------------------------------------------------
WHY THIS IS COMMITTED NOW
--------------------------------------------------
Three of the last four corrections in this work
moved an inherited number in the alarming
direction. A reassessment written after the
results is subject to the same pull. This
criterion is written while the outcome is unknown.
