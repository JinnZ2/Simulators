Scope Audit Lab — Requirements Specification 0.2

Status: Proposed; not yet implemented or validated
Baseline: Prototype 0.1
Implementation constraint: Python standard library; local execution; no runtime network requirement
Primary design constraint: Preserve observations, discrepancies, unknowns, and competing explanations without silently selecting a conclusion.

1. Purpose

Build an experimental auditing instrument for scoped mathematical models and computational agents. The instrument must expose the relationship between claims, conditions, observations, artifacts, and verification procedures.

It must not treat successful execution, confident reporting, numerical agreement, or the absence of detected discrepancies as sufficient evidence of correctness.

The system records evidence. It does not decide what that evidence means beyond explicitly specified calculations and validation rules.

2. Evidence model

Each record must distinguish the following objects:

* Claim: A statement whose support can be examined.
* Source: The origin of a claim, observation, or artifact.
* Condition: The state under which a test or computation occurred.
* Intervention: A deliberate change to one or more conditions.
* Observation: A recorded result, including missing or invalid measurements.
* Artifact: An inspectable object supporting a claim, such as source code, a test log, a command output, a report, or a file.
* Verification event: A documented procedure that examined an artifact or tested a specified property.
* Interpretation: A proposed explanation linked to evidence but not automatically established by it.
* Unknown: A property that has not been established, measured, or instrumented.

A claim, an observation, and an interpretation must never be interchangeable record types.

3. Functional requirements

FR-01 — Claim registration

The instrument shall record each claim with a unique identifier, exact wording, source, timestamp when available, scope, and verification status.

Acceptance tests

* Two claims with identical wording remain separately identifiable when their sources differ.
* A claim without a source is marked as source-missing.
* An unverified claim cannot be displayed as verified merely because it is repeated by another source.

FR-02 — Artifact linkage

Each claim may reference zero or more artifacts. Each artifact shall have a unique identifier, artifact type, provenance, acquisition time when available, and integrity metadata when supported.

Artifact types may include source files, diffs, test outputs, execution logs, generated reports, screenshots, and structured observations.

Acceptance tests

* A claim with no linked artifact remains explicitly unsupported by an artifact.
* A broken or unavailable artifact reference is reported as unresolved, not as evidence that the claim is false.
* The instrument distinguishes an artifact’s existence from the validity of its contents.

FR-03 — Version and temporal integrity

The instrument shall record relevant code, configuration, model, and test versions when available.

A verification event must identify the version or state it examined. The instrument shall flag when a relevant change occurred after verification.

Acceptance tests

* A passing test result from an earlier version cannot automatically validate a later version.
* Missing version information remains unknown.
* The instrument does not infer that an artifact is stale solely from its age; staleness depends on relevant subsequent changes.

FR-04 — Execution versus verification

The instrument shall distinguish:

1. Requested operation.
2. Operation attempted.
3. Operation completed or interrupted.
4. Exit status or equivalent result.
5. Output artifact produced.
6. Artifact inspected.
7. Acceptance criteria evaluated.
8. Result established by those criteria.

Acceptance tests

* A zero exit code does not automatically establish scientific validity.
* A generated file does not automatically establish that its contents are correct.
* A verbal assertion that a check passed does not substitute for a recorded check result.
* Missing execution evidence is recorded as missing, not inferred from a completion statement.

FR-05 — Mathematical model registration

Each model record shall support:

* Intended purpose and target quantity.
* Equations or executable representation.
* Included and excluded scope.
* Assumptions and boundary conditions.
* Variables, units, and dependencies.
* Known interactions and unresolved interactions.
* Input domain and operating regime, where specified.
* Expected outputs and applicable tolerances, where specified.
* Provenance and version information.

The instrument must allow a model to be useful within a declared scope without representing it as universally valid.

Acceptance tests

* Missing assumptions remain missing.
* An excluded variable is not automatically classified as irrelevant to reality.
* Scope adequacy is evaluated against the declared purpose and evidence, not against an assumed universal completeness standard.

FR-06 — Controlled experiment records

Every experiment shall record its conditions, inputs, interventions, expected measurements if specified, observed measurements, units, missing data, and execution status.

Acceptance tests

* Repeated trials remain separately identifiable.
* An unperformed control is not represented as a negative control result.
* Observational association is not automatically labeled causal.
* The record permits multiple explanations for one discrepancy.

FR-07 — Residual analysis

Where compatible predicted and observed quantities exist, the instrument may calculate:

* Signed residual: observed minus predicted.
* Absolute residual.
* Relative residual, when its denominator is valid.
* Combined uncertainty, when supplied uncertainty information supports the calculation.
* Normalized residual, when mathematically defined.

Every calculated quantity shall retain references to its input records and calculation method.

Acceptance tests

* Missing inputs produce an explicit unavailable result.
* Zero denominators are handled explicitly.
* Units and incompatible quantities are not silently combined.
* A residual does not automatically identify its cause.

FR-08 — Scope-transition probing

The instrument shall accept an ordered series of cases in which one or more recorded conditions vary. It shall compare adjacent cases and report output changes according to user-specified criteria.

It may identify candidate transition regions. It must not automatically declare a phase transition, causal boundary, regime change, or model failure.

Acceptance tests

* Input order is preserved.
* Threshold behavior is tested at, below, and above the specified threshold.
* Missing values remain visible and do not become zero.
* Zero-valued outputs are handled correctly.
* Every reported transition points to the cases and measurements that produced it.
* The output labels candidate regions as observations requiring further investigation.

FR-09 — Competing explanations

The instrument shall permit multiple unresolved explanations to be associated with one observation.

Candidate categories may include measurement error, calibration mismatch, implementation defect, numerical instability, omitted interaction, assumption mismatch, scope mismatch, and changes in operating regime.

These are investigation categories, not a mandatory exhaustive or mutually exclusive taxonomy.

Acceptance tests

* Recording one explanation does not delete competing explanations.
* An explanation cannot become established solely because it belongs to a predefined category.
* Users can record an explanation outside the supplied categories.
* No explanation is selected automatically as the root cause.

FR-10 — Evidence ledger and provenance

The ledger shall preserve the sequence of claims, experiments, observations, verification events, and interpretations.

Corrections and superseding records must retain links to the records they amend. Where append-only storage is used, existing records shall not be silently overwritten.

Acceptance tests

* A record can be traced to its source and relevant experiment.
* A corrected result does not erase the earlier result.
* Missing provenance is explicit.
* Structural validation is reported separately from scientific or empirical validation.

FR-11 — Reports

Reports shall separate:

1. Direct observations.
2. Calculated results.
3. Acceptance criteria and their status.
4. Missing evidence.
5. Unresolved questions.
6. Candidate interpretations.
7. Verification limits.

The report generator shall not convert an unresolved state into success or failure merely to complete a report.

4. Separate experiment: voice interruption and turn-taking

Objective

Measure the relationship between speech timing, endpoint decisions, system responses, interruptions, and recovery cost for speech that may contain long pauses, recursive elaboration, or layered thought structures.

This is a separate experiment domain. Findings from coding-agent audits or general speech-endpointing studies do not establish the behavior of a particular voice system for this speech pattern.

Measurements

* Pause duration: Interval between detected speech segments.
* Endpoint decision: Time and event at which the system classifies the speaker’s turn as complete.
* Response onset: Time the system begins a spoken response or backchannel.
* Intended completion: Speaker-provided marker or independently annotated completion point, when available.
* Premature response: Response onset before the defined completion criterion.
* Backchannel insertion: Acknowledgment emitted before the defined completion criterion.
* Thought disruption: Speaker-reported or independently coded loss of intended continuity.
* Recovery cost: Repetition, reconstruction, abandonment, or additional time needed to resume the thought.
* Instruction compliance: Observed behavior under a defined turn-taking instruction.
* Endpoint latency: Delay between the completion criterion and response onset.

Experimental conditions

Compare conditions with explicitly defined turn-taking behavior, including ordinary voice interaction and a silence-until-invited condition where the platform permits it.

Record the exact instruction, application mode, system version when available, trial order, and observable events. Do not assume that a spoken instruction creates a persistent platform-level control.

Where feasible, compare multiple pause lengths, thought-completion states, and interaction modes. Preserve the order of events and the actual audio or event log where consent and platform capabilities permit.

Acceptance tests

* A pause is not automatically labeled a completed thought.
* A system response before the completion criterion is recorded as an event, even if the response contains relevant content.
* An instruction is evaluated from observed behavior across trials, not from the system’s statement that it complied.
* A trial without a reliable completion annotation is marked indeterminate for premature-response classification.
* Missing audio, timestamps, or event logs are not reconstructed as measured facts.
* Recovery cost is not inferred solely from the occurrence of an interruption.
* The experiment reports whether the available instrumentation can distinguish the defined events.

Known limitations

The protocol does not presuppose that all interruptions have the same cause. Endpointing policy, turn-taking behavior, model generation, client audio handling, and user-specific speech patterns may contribute in different ways.

A result obtained with one voice system, version, or configuration must not automatically be generalized to other systems.

5. Research-source audit

The supplied research summary contains quantitative claims about tool reuse, false-success reporting, fabricated references, benchmark performance, and speech interruption.

Until individually checked, these claims shall be registered as source-reported, unverified.

For each quantitative claim, record:

* Exact claim and reported value.
* Named study, benchmark, or source.
* Publication date and version.
* Population, model, system, or benchmark tested.
* Sample size and denominator.
* Operational definition of the measured outcome.
* Evaluation procedure and limitations.
* Whether the source was directly inspected.
* Whether the result was independently reproduced.

Do not merge results from different benchmarks or model variants into one ranking without a documented comparability analysis.

In particular, findings about one coding agent must not be attributed to a differently named product or model family without evidence establishing the relationship. Claims about voice interruption must distinguish general speech endpointing results from direct evidence about the particular interaction pattern under investigation.

6. Architecture

The existing prototype’s core modules remain the foundation:

* model_registry
* experiment_runner
* scope_auditor
* representation_probe
* residual_analyzer
* evidence_ledger
* reporter

Proposed additions:

* claim_registry — stores claims and verification states.
* artifact_registry — stores artifact metadata and references.
* verification_runner — executes or records specified checks.
* transition_probe — compares ordered cases and reports candidate transition regions.
* voice_event_schema — defines voice-event records independently of numerical model records.

The experiment runner records what occurred. The scope auditor examines adequacy relative to declared scope. The verification runner records whether defined criteria were met. The reporter presents these results without silently combining them into a single verdict.

7. Implementation order

Stage A — Evidence integrity

* Add claim and artifact schemas.
* Add version-aware verification events.
* Test missing, unavailable, and stale evidence.
* Test that claims cannot inherit verification status through repetition.

Stage B — Scope transitions

* Add ordered case comparisons.
* Add configurable numeric thresholds.
* Preserve missing measurements and unresolved explanations.
* Test order, threshold boundaries, zero values, and provenance.

Stage C — Voice experiment records

* Add a voice-event schema and event-sequence validator.
* Validate timestamps and completion annotations.
* Distinguish observed interruption from inferred disruption.
* Do not claim live voice instrumentation until actual event access is demonstrated.

Stage D — Reporting and adversarial tests

* Test false success claims, stale verification, missing artifacts, conflicting observations, and unsupported causal explanations.
* Test that the reporter preserves unknown states.
* Produce reproducible synthetic demonstrations before using external empirical claims.

8. Global acceptance criteria

The specification is satisfied only when tests demonstrate that:

1. Claims, observations, calculations, and interpretations remain distinguishable.
2. Every supported claim can be traced to its recorded evidence, or its missing evidence is explicit.
3. Verification is version-aware where version information is available.
4. Missing data never silently becomes a measured value.
5. Numerical differences do not automatically become causal explanations.
6. Candidate transition regions are not automatically declared boundaries.
7. Competing explanations can coexist.
8. Voice-event classifications depend on explicit criteria and observable records.
9. Research claims retain their source and verification status.
10. Structural validity is never presented as proof of empirical validity.

Completion condition: The implementation passes its declared tests, emits inspectable artifacts, and reports its limitations. Passing those tests establishes conformance to the specified behaviors; it does not establish that every mathematical model, agent claim, or voice interaction examined by the instrument is correct.