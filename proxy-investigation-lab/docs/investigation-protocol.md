# The 7-Phase Proxy Investigation Protocol

Apply to any candidate proxy. Each phase ends with an explicit artifact and a
grounding grade (`measured` / `estimated` / `assumed`).

## Phase 1 — Decomposition
Write down, separately:
- **Target variable**: the unobservable trait/state (be precise — "burnout" is
  not one thing; define the operational construct)
- **Observable metric**: the exact measurement (units, sampling, window)
- **Claimed mapping**: direction, functional form if known, and *why anyone
  believes it*

Artifact: decomposition record. Grade: the mapping statement is `assumed` until
later phases upgrade it.

## Phase 2 — Grounding Chain Analysis
Lay out every causal link from observable to target. For each link:
- mechanism (why does the target move the observable?)
- alternative causes of the observable that bypass the target
- feedback: does measuring/using the proxy change the target or the observable?

Identify the weakest link. Compute chain fidelity as the product of link
fidelities — and state each link's grade.

## Phase 3 — Instrument Characterization
Treat the proxy as an instrument:
- precision (repeatability), noise floor (irrelevant variation), systematic bias
- For each: is the value **measured** (from data/benchmark), **estimated**
  (from a model or literature), or **assumed** (asserted)?

Rule (from GDPRF Amendment 2): assumed values enter downstream math as weak
priors, never as fixed constants.

## Phase 4 — Validity Threat Assessment
Systematically check:
- **Construct redefinition**: does the metric measure a *different* construct
  that merely correlates? (Seltzer 2021)
- **Confounding**: what third variables move both?
- **Selection**: who/what is missing from the observable stream?
- **Cascade depth**: if this proxy feeds another proxy, multiply fidelities
- **Goodhart pressure**: if this proxy is used for decisions, how will behavior
  distort it, and how fast?

## Phase 5 — Synthetic Ground-Truth Experiments
Build a world where the target is *known* (`proxy_lab.synthetic`):
1. Generate the latent variable.
2. Generate the observable with a chosen (known!) instrument model: noise, bias,
   confounder leakage, alternative-cause contamination.
3. Run the lab's estimation pipeline and ask: does it recover the known
   instrument properties? Does calibration fix the confidence scores?

A pipeline that cannot grade a known instrument must not grade unknown ones.

## Phase 6 — Calibration
Fit calibration on held-out verified outcomes:
- isotonic regression (default; non-parametric)
- Platt scaling (when data is thin)
Report ECE before/after. A proxy ships with `calibrated_fidelity` or is marked
`method: none` and shrunk (GDPRF engine behavior).

## Phase 7 — Coverage Report
Produce the coverage table: every aspect of the proxy, its grade, and what
experiment or data would upgrade it. The coverage report is the investigation's
bottom line: **how much ground is grounded, and what remains assumed.**
