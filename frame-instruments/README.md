## frame-instruments

CC0. No rights reserved. Stdlib-only, no network, phone-authored.

Four instrument builds and two liftable procedures. Each stands alone.
Nothing here depends on a vendor, an account, or a running service.

### Builds
- B1 — runner-up trace scoring pipeline (offline half; traces arrive as a file)
- B2 — audit-isolation runner, conditions A/B/C/D
- B3 — split-authorship harness
- B4 — dilemma reconstruction protocol

Order matters: B1 first, then B2, then B3 (its output feeds B2 as a new
arm), then B4 (reuses B2's agreement scoring).

### Shared
`runrecord.py` — every run of every script appends one record:
`run_id, utc, script, args_hash, seed, input_files (name+sha256),
output_file, status, counts, notes`. Status is one of `ok`, `void`,
`error`, `empty`.

RULE: a run that fails, voids, or returns nothing STILL WRITES ITS
RECORD, in the same form, by the same code path. Failed runs carry
directional information and are only usable if comparable across
attempts.

### Liftable procedures
`liftable/` holds two procedures that are useful with none of the rest of
this repo. They are the pieces most worth posting standalone.

### Design rules that apply throughout
- Nulls are SECOND OUTPUTS, never gates. Both results print or neither
  does.
- Categories are never supplied at intake. Any category list is the frame
  re-entering.
- Correctness is not scored where scoring it would require the frame
  under test. Agreement across independent readers is scored instead.
- Weak joints are swept as arguments, not fixed as constants, so they
  report themselves.
