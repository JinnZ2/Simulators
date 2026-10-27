# FWO-15 — Enclosure as corpus validity limit
**Target: Claude Fable 5.1**
**Repo: route-independence/ (same tree as FWO-8..14)**
stdlib only, CC0, phone-buildable

```
STATUS   RECONSTRUCTED 2026-10-04
         The original 2026-09-27 spec text was not recovered.
         Rebuilt from the memory object
         /areas/enclosure-as-corpus-validity-limit.md.
         If the original surfaces, it SUPERSEDES this text.
         Declare RECONSTRUCTED in the README and the module docstring.
SCOPE    excludes what already shipped:
           lag count            -> FWO-11 lag_count.py
           question selection   -> FWO-9  question_space.py
         reference those modules; do not rebuild them
```

---

## 0. OBJECT
```
HERS      once water, food, thermal regulation and homeostasis
          are all gated through one externally controlled token,
          what can be observed is the behavior the enclosure
          forces, not what humans are or can do
HERS      industrial-scale farming is the comparison; mark it
          as a real application
HERS      not observable from inside the frame (self-referential)
DERIVED   = an external-validity failure. Measured on the enclosed
          population, generalized to "humans", with no control
          condition in the written record. Animal science carries
          this caveat routinely for captive/production animals.
          For humans it is absent (Claude's read, NOT searched).
DERIVED   carries to AI: a model trained on that corpus inherits
          the enclosed sample as its picture of humans
TERMS     "enclosure", "captive", "domesticated" are used in their
          animal-science external-validity sense. No political
          position is advanced. State this at the top of the README.
```

## 1. BUILD A — enclosure_caveat_register.py
```
QUESTION  does human behavioral literature declare the
          resource-gating condition of its sample the way
          captive-animal literature declares housing/provision?

CODING SCHEMA per study (each field value | ABSENT):
  E1  population sampled
  E2  provision regime declared?  (how subjects meet water,
      food, thermal needs: token-gated | mixed | direct | ABSENT)
  E3  generalization target stated  ("humans", "adults",
      named population, ABSENT)
  E4  external-validity caveat present re: provision regime?
      YES | NO | ABSENT
  E5  arm  human | captive-animal | production-animal

OUTPUT    caveat rate per arm, with n and sampling frame
RULES     - sampling frame declared BEFORE coding
          - human arm rate vs animal arm rate is the comparison;
            no rate is reported without its frame
          - E2 = ABSENT is the expected modal human value;
            report it as a finding, not missing data
          - DESIGN_WRITTEN is acceptable if no corpus is in hand;
            then ship the schema + scorer + fixtures only
```

## 2. BUILD B — coupling_gradient.py
```
QUESTION  behavior before vs after a population's coupling to
          the token, timestamped by the instrument that coupled it

CASE ROW
  population
  coupling_instrument   lease | permit | building approval |
                        tax | barter-accounting rule | other
  coupling_date         dated, sourced — or ABSENT
  behavior_before       field + source
  behavior_after        field + source
  coupling_completeness full | partial | gradual
  CONFOUNDS (REQUIRED COLUMN — case rejected without it):
    never fully outside | mechanization | roads | media |
    other, named

SEED CASES (HERS, all UNCHECKED — verify or mark ABSENT):
  Amish: now need money for leases, permits, building approvals
  German village groups, Dutch, Indigenous peoples: historically
    operated outside the token
  barter less constrained 1950s–1970s, then accounted in dollars
  -> a shared barter-rule date gives MANY cases on ONE treatment
     date (DERIVED design lever, Claude's)

RULES     - no case enters with an undated coupling instrument;
            it goes to a HELD list, not the analysis
          - a pre-meld record is the CONTROL CONDITION, not
            prehistory; label it control
          - survivor filter stated in every output
```

## 3. KEY-HOLDER RULE (standing)
```
EXPECTED_FWO-15.md committed ALONE before any module,
as done at fd198aa for FWO-8..14
expected values: rates/bands per arm, case-count floor
anything implementation-first -> REGRESSION, not validation
```

## 4. BRANCHES — report distinct, never collapse
```
caveat gap confirmed     human arm rate << animal arm rate
no gap                   rates comparable (informative)
scope-limited            gap only in named sub-literatures
unmeasured               corpus not in hand -> DESIGN_WRITTEN
coupling shift visible / not visible / confounded beyond read
```

## 5. PRIOR-ART CHECK — run first, report NOT_RUN if skipped
```
- WEIRD-sample literature (Henrich et al.): covers cultural
  sampling, likely NOT the provision-regime axis. Confirm.
- captive-animal external-validity reviews: cite as the
  animal-arm standard
- enrichment / confinement-behavior literature pointed at
  humans: Claude's read is absent; verify
```

## 6. RETURN
```
per module: BUILT | DESIGN_WRITTEN, checks, fail fixtures
EXPECTED file commit hash (must precede modules)
prior-art: RUN result | NOT_RUN
held cases count, and why held
```
