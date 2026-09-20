# records/

Empty, and that is the finding.

The ledger reads claim records. It does not run sims and it does not
produce records: a record is emitted by the sim that owns the claim,
because the operands and the expression are things only the sim knows.

**Nothing in this repository emits claim records yet.** That is the gap
between the ledger existing and the ledger being used, and it is on the
emitting side, one sim at a time.

`ledger.py` refuses an empty record set with exit 2 rather than printing a
clean ledger over zero rows. A report with no findings and no denominator
reads as all-clear and is not one.

## What a record looks like

See `ledger/record.py` for the schema and
`ledger/fixtures/records/` for worked examples. The fixtures are
CONSTRUCTED and say so in their own `status` fields; they exist to
exercise the ledger's paths, and no value in them is a measurement of
anything.

Minimum:

```json
{
  "claim_id": "SSS_017",
  "sim": "sheet-structure-scan",
  "value": "696",
  "precision": 3,
  "operands": [],
  "provenance": "MEASURED",
  "falsifier": "a rerun over the same workbook reads other than 696",
  "falsifier_test": "tests/test_reader.py::test_shared_formula_count",
  "status": "SUPPORTED"
}
```

A DERIVED record adds an `expression` naming what was done with the
operands. Operand references are `sim:claim_id`, or a bare `claim_id`
resolving inside the emitting sim. They are qualified because in this
repository a `claim_id` is not unique: `CA_`, `RC_`, `MP_`, `SS_` and
`EMRG_` are each owned by two or three folders and every one of them
numbers from 001, so `RC_003` alone names three different claims.

## Why not transcribe the existing claim tables

Because a transcription is `CARRIED`, and a ledger seeded from
transcriptions would mark almost everything downstream `DERIVED_WEAK`
while saying nothing about whether the sims still compute what they say
they compute. The point of the ledger is the recompute, and the recompute
needs operands the transcriber does not have.
