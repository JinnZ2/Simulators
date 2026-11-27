ADDENDUM: intervention-audit, spec fidelity axis

STEP 2b: SPEC-TO-CODE FIDELITY
For each output where the instruction/spec is recoverable (chat log, commit msg, README):
  "fidelity": {
    "spec_source": ,          # where the stated intent lives
    "match": ,                # MATCH | DRIFT | MISSING_SPEC (void)
    "drift_type": None,       # omitted step, changed logic, added constraint,
                              # wrong constant, inverted condition...
