# WORK ORDERS — measurand partition set, delivered verbatim

Delivered 2026-09-18 as one message. Landed unedited below this line; the
build is the five `wo*.py` modules plus `common.py`, the audit is
`CLAIM_TABLE.md` (`MPS_001..`). The delivered text carries em dashes and
is the folder's ASCII exception; every `.py` file is ASCII.

---

# WORK ORDERS — measurand partition set
Opened 2026-09-18. CC0. No attribution required, none wanted.

Four independent designs. Each runs standalone. Each states its own scope
limits and what is NOT known. None requires the others.

Status tags: OBSERVED / DERIVED / PROPOSED.
Anything marked PROPOSED is a design, not a finding.

---

## WO-1 — PARTITION A DEFICIT LABEL

**OBJECT.** A "deficit" score is currently a residual: what is left after
frame, channel and frequency differences go unmeasured. Assessment
instruments are built on ONE setting of all three, so they cannot separate
the four by construction.

**AXES (at least four, interacting — the interaction is its own term):**
```
A1 FRAME      what the reasoning operates over
A2 CHANNEL    what carries it (kinesthetic, oral, visual, spatial, written)
A3 FREQUENCY  operating band on the channel: floor and ceiling (see WO-2)
A4 DOMAIN LOAD  input history weighting (cf. London taxi hippocampus,
                but from childhood and across several domains at once)
```

**DESIGN.**
```
POPULATION: individuals carrying a deficit label
STEP 1: measure A1-A4 SEPARATELY, before any performance scoring
STEP 2: score performance
STEP 3: report the RESIDUAL after A1-A4 are entered
CLAIM UNDER TEST: the residual is what could be called deficit.
                  Everything above it is instrument-setting.
```

**TWO-SETTING ARM (cheaper, runnable first).**
```
Same individual, two reference settings, both labels recorded.
Any individual scoring differently across settings BOUNDS how much of
the label is displacement from a reference rather than a property.
Existence of even one such case sets a floor on the bound.
```

**SCOPE LIMITS.** No claim that the residual is zero. No claim about any
individual. The design separates; it does not demonstrate.

**NOT KNOWN.** Whether any partition study of this kind exists. Not
searched. If it does, this is a join, not a gap.

---

## WO-2 — SWEEP THE OPERATING BAND INSTEAD OF SCORING A POINT

**OBJECT.** Engagement has a FLOOR (minimum stimulation before the task
registers) and a CEILING (saturation, shutdown). Two parameters, capable of
moving independently. The literature treats sensory responsiveness
multidirectionally but files co-occurring hyper- and hypo-responsiveness as
HETEROGENEITY — i.e. as noise to be explained away — rather than as a band
with two endpoints.

**THE MEASUREMENT FAULT.**
```
Every instrument found scores performance at ONE operating point.
The testing room is a fixed stimulation level chosen for the modal subject.
One point on a band carries NO information about where the band sits.
A subject whose band is shifted low is read at or past their ceiling.
=> shutdown-at-ceiling and no-response-below-floor RETURN THE SAME SCORE,
   and both are indistinguishable from deficit.
```

**DESIGN.**
```
INDEPENDENT VARIABLE: stimulation level, swept
DEPENDENT VARIABLE:   task performance at each level
OUTPUT: a CURVE per subject, with floor and ceiling estimated
        NOT a score
REPORT: floor, ceiling, width, and where the standard test point
        falls relative to each
```

**WHY IT MATTERS.** Any single-point instrument is a one-sample estimate of
this curve, taken at a level nobody chose for the subject being tested.

**NEAREST EXISTING WORK (2025):** a questionnaire crossing hyper/hypo
responsiveness WITH high/low stimulus intensity across five modalities,
built to surface patterns not recognisable with existing metrics. Two gaps
remain: it is parent-report, not a measured sweep; and the outcome is
sensory behaviour, not task performance. Nothing found links intensity to
what the subject can DO at each level.

---

## WO-3 — CONTROL MANIFEST AND PREDICTION-ACCURACY FLOOR

**OBJECT.** Longitudinal work reports that expert selection judgment
("the coach's eye") is neither stable nor reliably accurate, scored against
outcomes six years downstream. Between the observation and the outcome sit
variables the observer does not control.

**DERIVED.** What was measured is OBSERVATION + N YEARS OF UNCONTROLLED
VARIANCE, with the whole error assigned to the observation stage. The
finding as stated is mis-located: what is established is that the prediction
does not survive the interval, not that the observation was wrong.

**INTERVENING VARIABLES (partial list):**
```
controllable in principle     nutrition, hydration, sleep opportunity,
                              training load, coaching contact
NOT controllable in principle endocrine developmental timing
                              EXPERIENCED social environment
                              (distinct from received; only the
                              experienced one drives the outcome)
```

**THREE DELIVERABLES, IN ORDER.**
```
WO-3a CONTROL MANIFEST
  For a given program, enumerate per variable:
    HELD / ADVISED ON / NOT TOUCHED
  Required before WO-3b is runnable.
  NOTE why it does not exist: residential academies are documented in
  MARKETING, not measurement. Published descriptions show EDUCATION on
  nutrition and hydration — intervention on knowledge, not control of
  intake. Counter-number: adolescent athletes average ~6.3 h sleep
  against an 8-10 h recommendation, including where sleep is a named
  priority.

WO-3b CONTROL GRADIENT
  Grade programs by degree of environmental control.
  Test prediction accuracy against that gradient.
  Without it, "the eye is unreliable" stands UNPARTITIONED between
  observation error and downstream variance.

WO-3c ACCURACY FLOOR
  State the ceiling on achievable prediction accuracy implied by the
  not-controllable-in-principle variables.
  Every reliability result in this literature is currently read against
  an implicit ceiling of 100%.
```

**GENERAL FORM (this is the transferable part).** A prediction cannot be
scored against an outcome whose variance the predictor does not control.
Not a new method — a rule already standard elsewhere in measurement.

---

## WO-4 — TWO MEASUREMENTS THE MARKET HAS NOT RUN

### WO-4a LUMBER: DIMENSIONAL SUBSTITUTION, MEASURED
```
CLAIM: nominal 4x4 vs actual 3.5x3.5 is not a naming convention,
       it is a structural substitution.
ARITHMETIC (DERIVED): bending stiffness scales with the FOURTH POWER
       of depth. A 12.5% dimensional reduction removes ~40% of
       stiffness — before joinery, wood quality or seasoning enters.
TEST:  same species, full-dimension rough-cut vs dimensional stock,
       load capacity measured to failure.
COST:  lab test. Requires nobody's cooperation, no community access,
       no historical data.
OUTCOME EITHER WAY IS INFORMATIVE:
       confirms -> the code-compliant path carries a measured
                   stiffness deficit
       breaks   -> the dimensional claim is disposed of cheaply
```

### WO-4b STRUCTURES: SURVIVAL ANALYSIS, MATCHED
```
OBSERVED (field report): barns standing 250 yr, sheds 100+ yr,
       Driftless area, built by transmission that leaves NO DOCUMENT,
       maintained multi-generationally by the families who inherited
       them; same methods carried to bridges and carriages.
SEARCHED: no durability or failure-rate comparison of these against
       code-built equivalents exists. All ten results returned were
       BUILDERS SELLING BARNS; durability claims are marketing copy
       ("150 years or more with proper maintenance"), with the
       maintenance clause load-bearing in every one.
SAMPLE IS UNUSUALLY FAVOURABLE:
       dated, geographically clustered, identical weather exposure,
       standing beside conventionally built structures of similar age,
       construction dates in county records for BOTH populations.
DESIGN: matched survival analysis, age and exposure controlled.
CRITICAL SPLIT — do not collapse:
       MAINTAINED-IN-USE  and  SURVIVING-NEGLECTED
       are different quantities. Both informative. Report separately.
```

**WHY THESE TWO SIT TOGETHER.** A method can be gated on DOCUMENTATION
while its PERFORMANCE has never been measured. Where that holds, the gate
is not enforcing a standard the method failed — there is no evidence on
either side. It is enforcing a channel.

---

## WO-5 — DESELECTION SCORED ON THE WRONG OUTCOME

**OBJECT.** Talent research reports that most work focuses on the
successful athlete. The standard reading is survivor bias. That reading is
wrong, or at least mis-located.

**DERIVED.** The bias is not in WHO SURVIVES. It is in WHAT OUTCOME
survival is scored against.
```
score on the podium        -> non-podium athletes are failures
score on what was learned  -> every trained athlete gained it,
                              including the released ones
```
The failure category is MANUFACTURED by the choice of measurand.

**DESIGN.**
```
COMPARE: deselected athletes  vs  untrained age peers
ON:      balance, spatial awareness, load tolerance, controlled
         falling, transferable motor structure
PREDICTION (PROPOSED): deselected athletes ahead on nearly everything
         except the specific measure they were released for.
NOT FOUND in any search: nobody runs this comparison, because the
         program's purpose sets the scale and everything else the
         training produced is invisible to it.
```

**IMPORT NOTE.** The sports frame is worth importing into assessment
contexts — it supplies reportable conditions, input history as a declared
variable, mismatch as a PAIRING statement rather than a person-property,
and TRANSFER as a standard move when a channel closes. It carries the
deselection problem only if the PODIUM is imported alongside it as the
measurand. Frame and scoring choice are separable. Mark the line on import.

---

## COMMON STRUCTURE ACROSS WO-1 to WO-5

```
An observation made in ONE setting is scored against an outcome
produced by MANY unmeasured variables, and the entire error is
assigned to the thing being observed.

WO-1  the child carries it
WO-3  the observer's judgment carries it
WO-4  the building method carries it
WO-5  the released athlete carries it

Same instrument fault. Four populations.
```
