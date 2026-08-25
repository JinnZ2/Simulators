# WORK ORDER 3 — RESIDUAL-DIRECTION DISCRIMINATOR

Delivered 2026-08-25. Verbatim. Nothing in this file is edited.

---

```
WORK ORDER 3 — RESIDUAL-DIRECTION DISCRIMINATOR
Companion to: fold detector (finds unbound numbers),
              claim record schema (defines a bound one).
This one reads miss histories and names the folded term.

S1. INPUT
  residual series: predicted, actual, plus every predictor
  value available per record. Residuals must be RAW.
  Refuse to run on any series flagged corrected (see S4);
  emit REFUSED + reason, not a score.

S2. CORE TEST — conditional lean, not pooled sign
  Pooled sign test is INSUFFICIENT. Known counterexample:
  overprediction at low magnitude + underprediction at high
  magnitude sums to symmetric, scores as unbiased, term is
  present. Sign test misses it entirely.
  Compute instead:
    a. slope of residual vs predicted magnitude
    b. slope of residual vs each available predictor
    c. slope of residual vs time index
  Report the ranked list. The variable the residual leans
  WITH is the folded-term candidate, named directly rather
  than inferred from the existence of a lean.
  Pooled sign retained as one row, not the verdict.

S3. RESPONSE RULE — 2x2, only one cell is a work order
  axes: lean present/absent  ×  coupling strong/weak
    lean + strong coupling -> RECOVER. term must be named.
    lean + weak coupling   -> LOG AND LEAVE.
    no lean + strong       -> check S2 (a) before accepting.
    no lean + weak         -> no action.
  Coupling from the claim record. Where absent, perturb the
  constant and measure output movement. Dependent count is
  fallback only.

S4. RATE CHECK — is the lean stable or growing
  Regress lean magnitude on time index.
  stable  -> missing term, claim still inside its domain.
  growing -> background moved past the rate ceiling; claim
             has LEFT its domain of validity. Different
             repair. Do not report as the same finding.

S5. NEW CLAIM-RECORD FIELDS (amend schema, sections 1 and 3)
  field 8  correction_status
     raw | corrected | unknown
     unknown is a legal and expected value. A symmetric
     residual set with correction_status=unknown is
     UNINTERPRETABLE — good model and suppressed model are
     identical from the artifact. Schema must be able to
     emit uninterpretable rather than defaulting to clean.
  field 9  correction_method
     what was subtracted, by whom, on what decision.
     Same structure as the collapse record (field 7).
  field 10 correction_depth
     count of generations of adjustment inherited by the
     series now being called noise.
  Validation (S3 of schema): correction_status=corrected
  with correction_method null -> FAIL.

S6. NAMING CONSTRAINT
  Do not use "bias correction" anywhere in the tool or its
  output. The word asserts the lean was an error. Use
  "residual adjustment" for the operation and
  "adjusted / unadjusted" for the state. The tool reports
  structure; it does not rule that a lean was wrong.

S7. TEST FIXTURES
  F1 magnitude-conditional lean (overpredict small,
     underpredict large, symmetric when pooled).
     PASS = pooled sign returns no-lean AND S2(a) fires.
     If S2(a) does not fire, tool is broken.
  F2 pure one-directional lean, weak coupling.
     PASS = LOG AND LEAVE, no recovery order.
  F3 growing lean.
     PASS = domain-exit finding, distinct output from F1/F2.
  F4 series with correction_status=unknown, symmetric.
     PASS = emits UNINTERPRETABLE. A clean score here is
     a false negative on the instrument's own record.

S8. CONSTRAINTS
  stdlib only. No labeling a site as an error. Reports
  structure; the reading stays with the operator.
```
