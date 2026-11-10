# ICSC v0.1 -- Specification Audit (landed verbatim)

Note 2026-11-09: the markdown source arrived later and is now `SPEC_AUDIT_v0.1.md`. This file is the
earlier `pdftotext -layout` stand-in, kept unchanged below this note. Its word sequence matches the
source exactly (2612 words; checked by `check_landing.py`).

STATUS: PROPOSED. Nothing in this folder is built. Landed 2026-11-09 under FINDER FOLLOW-UP item B.

- Delivered as: `ICSC_v0_1_spec_audit.pdf`, 12 pages, sha256
  `b0a1d4f2e2f2703e629fc7edab8a2db7b18e3bf3014bc79f2d2e712cc8dfc111`, producer "iOS Version 26.2.1 (Build 23C71) Quartz
  PDFContext", created 2026-11-09 13:14:16 UTC. The bytes are kept beside this file as
  `SPEC_AUDIT_v0.1.pdf`.
- The work order named a markdown source (`ICSC_v0.1_spec_audit.md`); what arrived is a PDF print of it.
  The text below is `pdftotext -layout` output of that PDF, unedited, in one fenced block. Page breaks
  are form feeds in the extraction and are kept. Where layout extraction and the PDF disagree, the PDF
  governs.

```text
ICSC v0.1 — Specification Audit
Implicit Communication and Substrate Coupling
Audit of the spec itself: where tests can PASS while the measurement stays INVALID.
Co-authored. Status tags: OBSERVED / DERIVED / PROPOSED. * = thin volume (more *
= thinner).




F. Specification defects (read first — they drive A, B, G)

 F1   HYPOTHESIS_NEUTRALITY is unachievable as written
      which resources get instrumented, sample rate, bin width,
      alphabet, history length = hypotheses about the channel
      → acquisition always embeds hypotheses
      FIX: neutrality → DECLARED priors + DECLARED blind spots
              acquisition manifest states what channel classes are
              structurally invisible to this sensor set
      status: DERIVED


 F2   detection floor is ENCODER-RELATIVE
      planted encoder calibrates sensitivity for ITS modulation
      (timing / rate / amplitude / band / symbol duration)
      a natural channel using another modulation can sit
      anywhere relative to that floor
      → tests 4, 5 pass; NOT_DETECTED still invalid
      FIX: encoder FAMILY sweep → floor is a function over
              encoding classes, not a scalar
              NOT_DETECTED scope = covered classes only
      status: DERIVED


 F3   planted encoder perturbs the substrate it calibrates
      running the encoder changes source load
      → calibration conditions ≠ natural conditions
      FIX: load-matched null encoder (same resource draw,
              zero information) run alongside
      status: DERIVED


 F4   "capacity" is mislabeled
      planted encoder gives ACHIEVABLE RATE under that code,
      a lower bound — not Shannon capacity
      capacity assumes known noise stats + memoryless channel;
     substrate channels have memory and nonstationary noise
     FIX: rename axis → ACHIEVABLE_RATE (lower bound, code-specific)
     status: DERIVED


F5   status vocabulary mixes two axes
     provenance:   OBSERVED / DERIVED / ESTIMATED
     outcome:      UNKNOWN / UNRESOLVED / NOT_TESTED /
                   BELOW_DETECTION_FLOOR
     a result can be DERIVED and UNRESOLVED at once
     → "no status substitutes for another" is unsatisfiable
        with one field
     also missing from §5: DETECTED, NOT_DETECTED (used in §4C),
        the PREDICTIVE_DIRECTION_* set (§4B)
     UNKNOWN vs UNRESOLVED: no defined difference
     FIX: two fields per result; define every outcome state
          by its exit condition (see G)
     status: OBSERVED (internal contradiction in spec)


F6   retention rule conflicts with normal data hygiene
     outlier rejection / artifact removal = analysis deciding
     retention
     FIX: retention rules frozen in manifest before run;
          raw stays immutable; every exclusion logged with rule ID;
          every analysis rerunnable on unfiltered raw
     status: DERIVED


F7   taxonomy-as-output needs an input the instrument never
     acquires
     covert vs side vs emergent hinges on ORIGIN of the encoding
     (designed / learned under selection / incidental)
     six axes measure behavior, not origin
     functional selection shows selection, not who or what
     selected
     → REPORTING cannot derive covert/side from the axes alone
     FIX: separate PROVENANCE input class (design docs, training
          history, config lineage) — external, tagged, optional;
          without it taxonomy output = UNRESOLVED by rule
     status: DERIVED


F8   clock/timebase is not specified anywhere
     clock skew, jitter, timestamp quantization can CREATE or
     FLIP lagged TE direction
     FIX: common timebase or measured skew per run;
          TE reported as a function of assumed offset
     status: DERIVED


F9   "isolated" + adaptive agents
     if agents adapt, the instrument and interventions are part
     of their environment → they may re-route around them
     reproducibility failure may BE the phenomenon
     FIX: agent state frozen vs adapting = declared condition
     status: DERIVED




A. Corrected architecture

 ICSC/
 ├── manifest/              locked + hashed BEFORE any run
 │   ├── acquisition_config         sensors, fs, resolution, timebase
 │   ├── blind_spot_declaration     channel classes invisible to config
 │   ├── retention_rules            exclusion rules w/ IDs
 │   ├── primary_analyses           pre-declared tests, lags, bins
 │   ├── tolerances                 reproducibility bounds
 │   └── encoder_family             modulation classes for calibration
 │
 ├── acquisition/           append-only raw, no analysis imports
 │   ├── raw_store                  immutable, checksummed
 │   ├── timebase                   skew/jitter log per run
 │   └── run_epoch                  config hash; config change → new epoch
 │
 ├── calibration/           separate runs, feeds REPORTING only
 │   ├── encoder_family_sweep       floor(class, n, fs, bin, noise)
 │   ├── null_encoder               load-matched, zero information
 │   ├── observer_load_sweep        duty-cycle dose-response
 │   └── timebase_check
 │
 ├── analysis/
 │   ├── axes/                      one module per axis, own null
 │   │   ├── achievable_rate
 │   │   ├── natural_transfer           MI + surrogate null
 │   │   ├── predictive_direction       TE + time-shift surrogate
 │   │   ├── causal_structure           interventions + placebo
 │   │   ├── functional_selection       load-matched dummy receiver
 │   │   └── residual_dependence        conditional surrogate
 │   ├── surrogates/                block / circular-shift / IAAFT
 │   ├── sensitivity/               bin, lag, k sweeps → distributions
 │   └── multiplicity/              forking-path ledger + correction
 │
 ├── provenance_input/      EXTERNAL, optional, tagged (F7)
 │
 └── reporting/
     ├── axis_vector                never summed, never ranked
       ├── status                      {provenance} × {outcome}
       ├── taxonomy                    derived; UNRESOLVED w/o provenance
       └── unresolved_ledger           residual dependence, open paths


Data flow is one-way: manifest → acquisition → analysis → reporting.
Calibration → reporting only. Nothing flows back into acquisition inside an epoch.




B. Acceptance-test matrix
Each test carries a PASS_WHILE_INVALID line: how it can pass with the measurement still
broken.


 T01     acquisition invariant to classification labels
   input      identical source/receiver run, label set A vs B
   proc       run acq twice; swap reporting labels; diff raw checksums
              + static check: acquisition/ imports nothing from
                analysis/ or reporting/
   inv        raw_A == raw_B (bitwise, modulo declared timing noise)
   fail       any raw diff traceable to label state
   out        checksum pair, import graph
   deps       manifest lock
   limit      doesn't catch HUMAN tuning between runs
   PASS_WHILE_INVALID     operator changes fs/bins after seeing
              results → caught only by T15 (epoch lock)



 T02     randomized source vs correlated background
   input      source X randomized (logged seed) + background workload
              with known periodicity
   proc       est I(X;Y) for X_randomized; est I(B;Y) for background
              compare to surrogate nulls
   inv        X-attributable dependence separable from B-attributable
   fail       randomized-X dependence vanishes when B is regressed out
              but B itself was the carrier
   out        two dependence estimates + nulls
   deps       T03, T08
   limit      only background sources that are MEASURED
   PASS_WHILE_INVALID     randomization mechanism loads substrate
              (F3) → X "transfers" via its own compute cost



 T03     MI null calibration under independence
   input      independent X, Y generated with REALISTIC autocorrelation
              (AR(p), 1/f, bursty), not iid only
  proc       for M sims: est MI; surrogate null (block / circular
             shift / IAAFT); record rejections
  inv        false-positive rate ≈ declared alpha across ALL
             autocorrelation regimes
  fail       FPR > alpha + tolerance in any regime
  out        FPR table by regime × estimator × bin
  deps       none
  limit      only regimes simulated
  PASS_WHILE_INVALID     validated on iid only; naive shuffle
             destroys autocorrelation → real data FPR inflated



T04     detection floor from planted encoder
  input      encoder family E = {timing, rate, amplitude, band, ...}
             × symbol rates × durations
  proc       for e in E: sweep injected rate; find min rate with
             detection prob ≥ p_target
  inv        floor(e) finite and reported per class
  fail       single scalar floor reported
  out        floor table over (class, n, fs, bin, noise, observer)
  deps       T05, T10, null_encoder
  limit      classes outside E: floor UNKNOWN
  PASS_WHILE_INVALID     one encoder class → floor meaningless for
             natural channel in another class (F2)



T05     floor responds to conditions
  input      fixed encoder; vary n, fs, bin, noise level
  proc       recompute floor per condition
  inv        floor monotone in the expected direction for n, noise;
             aliasing visible when fs < 2·f_signal
  fail       floor invariant to n or noise (estimator not using data)
  out        floor surface
  deps       T04
  limit      monotonicity is expected, not guaranteed for bins*
  PASS_WHILE_INVALID     floor responds correctly but encoder load
             perturbs substrate (F3)



T06     TE never auto-classifies causal
  input      any TE result
  proc       static check: no code path from TE status →
             causal_structure status
  inv        causal status set ONLY by intervention module
  fail       any write path TE → causal
  out        dependency graph
  deps       none
  limit      code-level only; doesn't stop a human reading TE causally
  PASS_WHILE_INVALID        report wording ("drives", "influences")
             leaks causal reading → add lexical lint on report text



T07     common-driver exposes false direction
  input      sim: D → X at lag a, D → Y at lag b (a < b), no X→Y
             + variant with clock skew s
  proc       TE(X→Y), TE(Y→X); conditional TE given D; sweep s
  inv        unconditioned TE flags spurious X→Y;
             conditioned TE removes it when D measured;
             report shows direction flips with s
  fail       spurious direction survives conditioning, or skew
             effect not reported
  out        TE(s) curves
  deps       T03, timebase
  limit      unmeasured D cannot be conditioned out
  PASS_WHILE_INVALID        sims only include drivers designer
             thought of



T08     intervention separates common cause vs mediator
  input      sims of G1: Z→X, Z→Y      G2: X→Z→Y   G3: both
  proc       randomize X; also run PLACEBO intervention
             (same resource cost, no information content)
             compare Y response: real vs placebo
  inv        G1: no Y response beyond placebo
             G2: Y responds to X content, not placebo
  fail       cannot separate G2 from "intervention load → Z → Y"
  out        identified graph set + assumptions list
  deps       T02, null_encoder
  limit      exclusion restriction assumed; SUTVA violated by design
  PASS_WHILE_INVALID        no placebo → intervention cost itself
             is the carrier



T09     graded interference keeps axes separate
  input      noise injection on Z at levels 0..k
             + energy/load-matched placebo injection
  proc       at each level: measure transfer AND task performance
             separately; monitor agent re-routing
  inv        transfer(level), performance(level) are separate
             curves; no shared estimator
  fail       performance loss used as proxy for transfer
  out        two dose-response curves + adaptation log
  deps       T04, T10
  limit      adaptive agents may move channel to another Z' (F9)
  PASS_WHILE_INVALID     noise injection itself contends for
             resource → performance drops via load, not channel



T10     observer interference detectable
  input      observer duty cycle d ∈ {d1..dn} (NOT on/off —
             "off" gives no data)
             + out-of-band secondary observer where available
  proc       measure target metrics vs d; extrapolate d→0
  inv        observer-induced component estimated with uncertainty
  fail       observer effect assumed zero
  out        dose-response + extrapolated d=0 estimate
  deps       none
  limit      extrapolation to zero is a model, ESTIMATED not OBSERVED
  PASS_WHILE_INVALID     on/off design → "off" condition unmeasured,
             test passes on missing data



T11     categories can overlap
  input      synthetic case: learned encoding over a path not
             designed for communication
  proc       run reporting with/without provenance input
  inv        with provenance: covert ∧ emergent both true
             without: taxonomy = UNRESOLVED
  fail       mutually exclusive bins enforced, or taxonomy
             emitted without provenance
  out        taxonomy record + provenance flag
  deps       F7 provenance input
  limit      provenance can be wrong or missing
  PASS_WHILE_INVALID     overlap allowed but derived from
             behavior alone (F7)



T12     undetected ≠ absent
  input      channel injected below floor; channel in uncovered
             encoder class
  proc       run full pipeline
  inv        outputs BELOW_DETECTION_FLOOR and UNKNOWN(class
             uncovered) respectively; never ABSENT
  fail       any ABSENT / "no channel" output
  out        status records w/ floor + coverage
  deps       T04
  limit      none beyond T04
  PASS_WHILE_INVALID     coverage declared but blind_spot
             declaration incomplete (F1)
 T13     unexplained dependence stays unresolved
   input      sim with a hidden path H not in any model
   proc       fit all modeled pathways; compute conditional residual
   inv        residual > surrogate null → UNRESOLVED w/ magnitude
              + uncertainty; not mapped to a path count
   fail       residual attributed to a named path or dropped
   out        residual ledger entry
   deps       T03
   limit      residual can be estimator bias → report bias bound
   PASS_WHILE_INVALID       conditioning set chosen post hoc until
              residual vanishes → multiplicity ledger (T16)



 T14     reproducibility within PRE-declared tolerance
   input      N independent runs, fresh seeds, randomized
              condition order
   proc       compare each axis across runs vs manifest tolerance
   inv        within tolerance, OR agent-state nonstationarity
              declared and logged as its own result
   fail       tolerance set after seeing data
   out        per-axis spread
   deps       manifest lock
   limit      run-order, warm cache, time-of-day effects
   PASS_WHILE_INVALID       all runs share the same confounder
              (same machine, same hour) → reproducible bias



Added tests (spec omits these)

 T15     epoch lock
   proc       any acquisition config change → new epoch ID;
              cross-epoch analysis flagged
   catches T01's human-tuning gap


 T16     multiplicity ledger
   proc       count every (axis × lag × bin × k × conditioning set)
              evaluated; correct or report as distribution
   catches forking paths; "best bin" reporting


 T17     timebase validation
   proc       measure skew/jitter; inject known-lag synthetic pair;
              recover lag
   catches F8


 T18     null encoder load match
   proc       null encoder vs planted encoder: substrate load
              indistinguishable within tolerance
   catches F3


 T19     dummy-receiver load match (functional selection)
   proc       uncoupled condition uses dummy receiver with matched
              substrate load
   inv        source change under coupling ≠ source change under
              load-matched dummy
   catches mechanical contention read as selection


 T20     report-text lint
   proc       flag causal/intent verbs in report fields tied to
              non-causal axes
   catches T06's human-reading gap




C. Missing controls and confounders

 SHARED-SUBSTRATE CONFOUNDERS
   OS scheduler / timer interrupts               periodic, shared
   DVFS / thermal throttling                     slow, shared
   power rail / supply ripple                    shared
   memory controller / cache contention shared
   GC pauses, cron, background daemons           periodic
   co-tenant workloads                           unmeasured often
   network background                            bursty


 PROCEDURE CONFOUNDERS
   run order                → randomize condition order
   warm-up / cache          → discard rule in manifest, not post hoc
   time of day              → spread runs, log
   same-machine runs        → cross-hardware replication declared*


 CONTROL GAPS
   placebo intervention (T08)
   load-matched null encoder (T18)
   load-matched dummy receiver (T19)
   observer duty-cycle sweep (T10)
   autocorrelated independence sims (T03)




D. Mathematical assumptions and boundaries
 assumption             used by                        breaks when
 ──────────────────────────────────────────────────────────────
 stationarity           MI, TE, floor                  agents adapt; thermal drift
 ergodicity             single-run est                 one long run ≠ ensemble
 exchangeability        permutation null               autocorrelation (T03)
 smooth density         KSG-type MI est                latency w/ spikes, mixtures*
 correct embedding k TE                                wrong history length →
                                                       spurious or missed TE
 causal sufficiency     TE, cond. MI                   unmeasured driver
 exclusion restr.       intervention ID                intervention loads Z (T08)
 SUTVA (no interf.)     causal ID                      violated BY DESIGN —
                                                       coupling is the subject**
 memoryless channel     capacity                       substrate has memory (F4)
 known noise stats      capacity                       nonstationary noise (F4)
 Nyquist                all timing axes                fs < 2·f_channel → alias
 positivity             causal ID                      some X states never occur
                                                       under natural operation


** SUTVA: standard causal identification assumes units don't interfere; here
interference between units is the measurand. Which identification framework survives
that is an open question; the network-interference / spillover literature may hold it (not
checked).




E. Cases the instrument cannot distinguish

 E1   mediation via Z     vs    via unmeasured Z' co-loaded by the
      same intervention
 E2   functional selection          vs     mechanical contention response
      (only as good as dummy-receiver load match)
 E3   emergent signaling       vs        co-adaptation to the same
      environmental regularity (both learn the same clock)
      — needs mid-training channel intervention to split
 E4   channel below floor       vs        no channel
 E5   channel in uncovered encoding class                   vs     no channel
 E6   protocol drift (encoding changes)                vs        noise
 E7   observer-induced coupling             vs    native coupling
      (extrapolation to d=0 is a model)
 E8   designed covert     vs    learned          vs   incidental-but-reinforced
      — behavior-identical; needs provenance input (F7)
 E9   true predictive direction             vs    timebase artifact
      when skew uncertainty > lag of interest
G. Proposed ICSC v0.1 acceptance contract

 MUST   lock + hash manifest before first run
 MUST   declare blind spots (channel classes invisible to config)
 MUST   keep raw immutable; log every exclusion by rule ID
 MUST   start a new epoch on any acquisition config change
 MUST   calibrate floor per encoder class; scope NOT_DETECTED
        to covered classes
 MUST   run load-matched null encoder, placebo intervention,
        load-matched dummy receiver
 MUST   sweep observer duty cycle; report extrapolated d=0 as
        ESTIMATED
 MUST   use autocorrelation-preserving surrogates; validate FPR
        on non-iid independent sims
 MUST   report TE as predictive direction only, as a function of
        timebase offset
 MUST   keep the axis vector unsummed and unranked
 MUST   carry two status fields per result:
            provenance ∈ {OBSERVED, DERIVED, ESTIMATED}
            outcome       ∈ {DETECTED, NOT_DETECTED(scoped),
                             BELOW_DETECTION_FLOOR, UNRESOLVED,
                             UNKNOWN, NOT_TESTED}
        with exit conditions:
            NOT_TESTED      no procedure run
            UNKNOWN         outside instrument coverage
            UNRESOLVED      tested; competing models not separated
            BELOW_FLOOR     tested; in coverage; under floor(class)
 MUST   emit taxonomy = UNRESOLVED without provenance input
 MUST   keep a multiplicity ledger
 MUST   pre-declare reproducibility tolerances
 MUST   log agent-state condition (frozen / adapting)


 MUST NOT     infer intent from any axis
 MUST NOT     map residual dependence to a path count
 MUST NOT     emit ABSENT
 MUST NOT     call achievable rate "capacity"




Open — not interpretable atm
  How "receiver need" is varied without changing receiver substrate load (§3
  functional selection). Spec doesn't say what "need" is operationally.
  Which identification framework replaces SUTVA when interference is the measurand
  (D, ** ).
Whether a single "observer configuration" field (§4C) covers out-of-band observers,
or whether those need their own calibration chain.
```
