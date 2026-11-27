WORK ORDER: model-output-audit, run 2 (JinnZ2/Simulators, branch model-output-audit)
Keep run 1 untouched; file as run_2/.

1. INDEPENDENT AUDITOR
   Rerun every decided claim and the 8 pass-claim side notes with a non-Anthropic
   open model (Gemma or equivalent, local) + stdlib reruns. Record auditor per verdict.
   Report agreement rate between auditors.

2. ADJUDICATE THE 8 PASS CLAIMS
   For each: rerun at writing commit and at HEAD, in bare stdlib env and current env.
   Classify: OVERCLAIM (fails at writing commit) | ENV_DEPENDENT | STALE | void.

3. READ, DON'T PROBE
   Read the 101 probe-based verdicts (48 DECLARED_LIMIT, 53 ENV_DEPENDENT) line by line.

4. TIGHTEN CLAIM EXTRACTION
   Drop mentions: pass counts, usage lines, failures reported as fixed.
   Keep only assertions that something fails, can't run, or is defective.
   Report new candidate count.

5. SPEC FIDELITY (new axis)
   Where the stated spec is recoverable (chat log, commit msg, README, work order):
   fidelity = MATCH | DRIFT | MISSING_SPEC (void); drift_type: omitted step,
   changed logic, added constraint, wrong constant, inverted condition.
   Tabulate drift rate by model, version, date, topic; print n every cell.

RULES: agency void; no "sabotage" label as a finding; grades only; every number from records.
Commit + push, no PR. Observer slots: null.
