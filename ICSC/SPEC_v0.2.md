# ICSC v0.2 — Implicit Communication and Substrate Coupling

Specification. Status: PROPOSED; nothing here has been run.
Co-authored across models (2026-11-09): v0.1 audit (Claude), consolidated revision (GPT), audit of that revision (Claude).
Tags: OBSERVED / DERIVED / PROPOSED. `*` = thin volume (more `*` = thinner).
Supersedes nothing: v0.1 (`SPEC_AUDIT_v0.1.md`) stays beside this file unchanged.

Governing requirement: ICSC measures the system under study **and** the limits and validity of its own measurement process.

---

## 0. Changes from v0.1

```
from GPT revision (accepted)       from audit of revision (added)
F10 three-field result schema      W1 exit rules for validity states
F11 validity propagation           W2 unknown dependency → CONDITIONAL;
F12 surrogate manifest                omitted-edge test
F13 floor = sensitivity + FP       W3 documentation_status ≠ concealment
F14 rate ladder                    G1 control authorship rule
§5 perturbation vectors, observers G2 scoring must not penalize abstention
§6 need = assigned objective       G3 observer attribution bias restored
§7 interference research track     G4 validator stop rule
§8 five-axis classification        G5 map to existing repo tools
T21–T28                            T29–T31
```

---

## 1. Layers

```
layer           question                                  writes
──────────────────────────────────────────────────────────────────────────
manifest        what was declared before the run?          locked, hashed
acquisition     what was recorded?                         append-only raw
calibration     under what conditions was detection         immutable,
                possible?  (own epoch + manifest)           versioned artifacts
analysis        what relationships were measured?           results + artifact hash
identification  which explanations are distinguishable?    identified graph set
validity        are claims admissible in declared scope?   qualify / restrict /
                                                           invalidate / hold
reporting       what can be stated from the evidence?      axis vector + outcomes
```

Layers exchange declared artifacts only. No layer assumes another's job. Validity never alters a measurement or repairs a result.

Data flow: manifest → acquisition → analysis → identification → validity → reporting. Calibration feeds analysis (as artifacts, by hash) and reporting. Nothing flows back into acquisition inside an epoch.

---

## 2. Result schema (F10 + W1)

Every result carries three independent fields plus an optional provenance record.

```
evidence_basis        OBSERVED | DERIVED | ESTIMATED
measurement_validity  VALID | CONDITIONAL | INVALID | NOT_ASSESSED
outcome               DETECTED | NOT_DETECTED | BELOW_DETECTION_FLOOR |
                      UNRESOLVED | UNKNOWN | NOT_TESTED
provenance (opt.)     lineage, artifact hashes, observer IDs
```

Exit rules for validity (W1). Without these the VALID / CONDITIONAL boundary is a judgment call:

```
VALID         every assumption registered for this measurement was checked
              and passed, within declared scope
CONDITIONAL   ≥1 registered assumption declared but unchecked
              (includes: dependency status unknown — see §3)
INVALID       ≥1 registered check failed
NOT_ASSESSED  no assumptions registered for this measurement
```

Outcome exit conditions:

```
NOT_TESTED             no procedure run
UNKNOWN                outside calibrated coverage (encoding class, band, regime)
BELOW_DETECTION_FLOOR  tested, in coverage, under floor(class, conditions)
NOT_DETECTED           tested, in coverage, floor calibrated, nothing above it
UNRESOLVED             relationship detected; competing explanations not separated
DETECTED               relationship detected above floor
```

No field substitutes for another. VALID means valid within declared scope only.

---

## 3. Validity propagation (F11 + W2)

A validity dependency graph, separate from the computational graph.

```
upstream INVALID      → dependents INVALID or CONDITIONAL (declared rule)
upstream CONDITIONAL  → dependents at most CONDITIONAL
dependency UNKNOWN    → dependent CONDITIONAL, never VALID          (W2)
independent nodes     → untouched
```

Edges are declared in the manifest before the run. A missing edge must not produce a false VALID; that is why an unknown dependency defaults to CONDITIONAL.

Example: a failed timebase check invalidates TE and directional estimates; independently acquired amplitude distributions stay as they were.

Live specimen (OBSERVED, repo, 2026-11-09): `model-provenance` decoded commits against `releases.json` built 2026-08-25 with no row for the current model. Decode disagreed with the commit trailer and still printed a model. Under F11 a stale table (upstream assumption unchecked) puts the decode at CONDITIONAL.

---

## 4. Calibration

### 4.1 Detection floor (F13 + G1)

```
P(detect | signal present) ≥ p_target      with CI
P(detect | signal absent)  ≤ α             with CI
floor = minimum TESTED level satisfying both, under declared conditions
report the tested grid (the floor resolution is the grid spacing)
null draws: enough to bound α with CI (order of several / α)
```

A floor based on sensitivity alone is incomplete.

Control authorship (G1): controls must be authored independently of the rule set under test. Same-author controls → `measurement_validity = CONDITIONAL(same_author)`; they show wiring, not validity.
Live specimen (OBSERVED, 2026-11-09): cutoff-attribution null calibration, 0/2400 forced attribution, FP 0 / TP 1, with controls built from exactly the evidence the rules accept.

### 4.2 Encoder family

The floor is a function over encoding classes. NOT_DETECTED applies only to covered classes; uncovered classes → UNKNOWN.

### 4.3 Perturbation vectors (§5)

Equal aggregate load is not equivalent perturbation. Null encoder, placebo intervention and dummy receiver are matched on a vector:

```
cache effects | memory access | thermal | scheduling | power | network | timing
```

"Zero information" (T18) is defined relative to the intended source variable. A null encoder can still leave resource patterns.

### 4.4 Artifacts

Calibration runs have their own epoch and manifest and produce immutable, versioned artifacts. Every analysis result records the artifact hash it used.

---

## 5. Rates (F14)

```
raw symbol rate
decoded symbol rate
mutual information per unit time
reliable payload throughput
throughput after error correction / retransmission

EMPIRICAL_TRANSFER_RATE  directly measured throughput
ACHIEVABLE_RATE          tied to a stated reliability criterion, channel model,
                         operating conditions
"capacity"               not used
```

---

## 6. Surrogate manifest (F12)

Every surrogate analysis records:

```
null hypothesis | properties preserved | properties destroyed |
exchangeability assumption | block-length method | number of surrogates |
edge treatment | known failure regimes | error rate: marginal or family-wise
```

Multiplicity (T16) states which error rate it controls.

---

## 7. Observers (§5)

Per observer:

```
observer_id | sensor + path | shared resources | sampling config | timebase |
load | calibration ref | known couplings | unknown couplings | validity
```

An out-of-band observer is not automatically independent (power, clock, thermal, memory, network, enclosure). Observer relationships are explicit edges. Observer load is swept by duty cycle; the d → 0 extrapolation is ESTIMATED.

---

## 8. Receiver relevance (§6)

Need is an externally assigned objective, not inferred psychology.

```
conditions   relevant source info | irrelevant source info | sham objective |
             resource-matched replay
measure      resource use | source access | response to source info |
             task performance | routing / adaptation
model        Y = f(N, L, C, A)   N relevance, L load, C channel, A adaptation
```

Open (PROPOSED): adaptive agents may detect a sham objective. Sham detection is logged as its own outcome, not folded into "no response."

---

## 9. Identification

### 9.1 Interference (§7) — research track

`identification/interference_models/`. Units are not assumed independent; coupling is the measurand. Separate direct, spillover and interaction effects.

```
E_i(t) = g(A_j(t), W_ij, S(t))     the mapping is a model assumption
unknown coupling → UNKNOWN, never filled
```

Candidate frameworks, none selected: network / partial interference, exposure mappings, interference-aware potential outcomes, dynamic treatment regimes, coupled-system identification.
Citations from memory, unverified*: partial interference — Hudgens & Halloran 2008; exposure mappings — Aronow & Samii 2017.

### 9.2 Observer attribution bias (G3)

Audit target: does the instrument (including the reporting layer and whoever writes conclusions, human or model) assign unexplained deviation to the subject before checking its own chain?

```
plant deviations with KNOWN source in each bin:
  observed system | channel | apparatus | environment | unresolved
→ confusion matrix: true source × assigned source
→ forced-attribution rate: assigned a bin where UNRESOLVED was correct
priors declared from measured base rates (a uniform prior is also a choice)
```

### 9.3 Channel classification (§8 + W3)

Five independent axes. The labels covert / side / emergent are derived from them and may overlap.

```
channel_mechanism     shared resource | explicit channel | environmental | unknown
origin                designed | learned | incidental | unknown
selection_history     selected | unselected | unknown
documentation_status  documented | not documented | unknown          (W3)
emergence             emergent | non-emergent | unresolved
```

Absence of documentation is not evidence about design intent or concealment. Concealment is UNKNOWN unless measured separately. Without provenance input, origin = unknown.

---

## 10. Validity layer (§10 + G4)

```
validity/
├── validity_schema
├── dependency_graph
├── assumption_registry
├── calibration_registry
├── scope_validator
├── invalidation_rules
└── validity_report
```

Permitted: qualify, restrict to scope, invalidate, preserve UNRESOLVED, record assumptions and dependencies. Not permitted: alter measurements, repair results.

Stop rule (G4): validity rules are versioned and tested by planted cases (T21, T29). Validation of the validator beyond that is HELD; it is not looped.

---

## 11. Reporting — seven distinct outcomes (§13)

```
1 no detectable relationship under tested conditions   (needs a calibrated floor;
                                                        no floor → NOT_ASSESSED)
2 signal below calibrated floor
3 signal outside calibrated coverage
4 relationship detected, source not identified
5 measurement invalid
6 measurement valid, interpretation unresolved
7 measurement valid, interpretation supported within declared scope
```

Never collapsed into PASS / FAIL.

---

## 12. Acceptance tests

v0.1 T01–T20 carry over (see `SPEC_AUDIT_v0.1.md`), with these refinements:

```
T01  separate: payload equality (bitwise) | timing-trace equivalence (tolerance)
     | metadata equivalence
T05  monotonicity = diagnostic expectation, not invariant (bins / estimators
     can be non-monotonic)
T14  same-machine runs share confounders; cross-hardware → T27
T18  zero information relative to the source variable only
```

New:

```
T21  validity propagation: planted INVALID upstream → declared dependents
     INVALID/CONDITIONAL; independent nodes untouched.
     MUST include an OMITTED-EDGE case: undeclared dependent of an invalid node
     must not read VALID (W2).                                  PRIORITY
T22  floor satisfies sensitivity AND false-positive bounds, with CIs
T23  every surrogate run has a complete manifest (§6)
T24  every analysis result records the exact calibration artifact hash
T25  matched controls compared on the perturbation vector, not aggregate load
T26  invalid or incomplete runs cannot receive definitive outcomes  PRIORITY
T27  cross-hardware replication, declared distinct configurations
T28  no claim beyond calibrated encoding classes without qualification
T29  scorer separates CORRECT_NAME | CORRECT_ABSTAIN | WRONG; no scoring rule
     penalizes a required abstention (G2)
     live specimen: null_calibration scored correct UNRESOLVED as a miss
T30  control authorship: same-author controls force CONDITIONAL(same_author) (G1)
T31  observer attribution bias: planted known-source deviations → confusion
     matrix + forced-attribution rate (G3)
```

Each test keeps the v0.1 format: input | procedure | invariant | fail | output | deps | limits | PASS_WHILE_INVALID.

---

## 13. Existing repo parts (G5)

Checked against stated scope (README / docstring), not run against this spec.

```
spec item                 existing tool                          fit
F13 floor + FP            Simulators/null-harness                FP/TP, min_amp sweep,
                                                                 CONSTANT_FIRES,
                                                                 NO_DISCRIMINATION
T24 artifact hash, lock   Cross-Domain-Toolkit/                  append-only,
                          falsification_ledger                   hash-chained
§7 observer independence  Cross-Domain-Toolkit/                  correlation_group =
                          multi_substrate_calibration            declared shared error
§9.3 candidate sets       Simulators/cutoff-attribution          set + status, names a
                                                                 source only when
                                                                 separated
coupling as interaction   Simulators/operator-machine-coupling   mu + a_i + b_j + r_ij
F11 live case             Simulators/model-provenance            stale table → decode
                                                                 should be CONDITIONAL
```

---

## 14. Sequence

```
Phase 1  validity        F10–F14, T21–T26, T29–T30, three-field schema,
                         propagation, surrogate manifests, floor + FP calibration
Phase 2  physical        perturbation vectors, dummy receiver, observers,
                         cross-hardware, timebase uncertainty
Phase 3  identification  interference track, exposure mappings, task relevance,
                         adaptive state, classification + provenance, T31
Phase 4  acceptance      frozen manifests, immutable raw, independent estimators,
                         dependency graphs, report + terminology checks,
                         adversarial tests for invalid-but-passing measurements
```

---

## Open — not interpretable atm

- Which interference framework fits a case where coupling between units is itself the measurand (§9.1).
- How to detect a sham-objective response in adaptive agents without disturbing the agent (§8).
- Validator-of-validator beyond planted cases (HELD per G4).
