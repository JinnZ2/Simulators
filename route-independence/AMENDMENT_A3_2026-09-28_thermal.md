# FWO AMENDMENT A-3 — 2026-09-28
# Thermal regulation: actuators, stacked gates, direction, condition index,
# cross-stock coupling
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to FWO-5, FWO-8, A-1, A-2, A-2.1. Nothing retracted.

## RULES
R1  Commit section 6 (EXPECTED) alone, before any code.
R2  Sourced inputs only. Grades: P primary read / S secondary / K known,
    unverified. K rows are stored, flagged, and hold-ineligible.
R3  Every new suite ships a fail fixture.
R4  Failed predictions first.

## 1. ORIGIN
OBSERVED (Kavik): human thermal regulation is token-gated too — clothing,
  fans, air circulation, heating, fires.
PROPOSED (Claude): for water, the regulator is mostly internal and only
  the source is gated. For thermal, the unclothed physiological range is
  narrow, so most of the ACTUATOR is external (objects, energy,
  structure, land). The external part is the part a gate can reach.
  Therefore thermal may carry more gate surface than water. This is a
  prediction, not a finding.
PROPOSED (Claude): a gate is an ACTUATOR fault. The existing stocks
  material covers SENSOR faults (cold suppressing thirst). They are two
  distinct fault classes in one regulator. Do not merge them.

## 2. SCHEMA
### 2a. actuators
  actuator_id
  stock      {THERMAL, WATER, FOOD, AIR, SLEEP}
  direction  {WARM, COOL, RETAIN, SHED}
  locus      {BODY, EXTERNAL_OBJECT, EXTERNAL_ENERGY,
              EXTERNAL_STRUCTURE, LAND_ACCESS}
Seed rows (hers, plus Claude's additions marked C):
  clothing (RETAIN; SHED), fans (COOL), air circulation / ventilation
  (COOL), heating by utility (WARM), open fire (WARM), wood stove
  (WARM, C), self-built shelter (RETAIN, C), shade and water immersion
  (COOL, C), body-only: posture, activity, huddling, sleep timing
  (BOTH, C).

### 2b. gates — many per actuator, ORDERED (stacked in series)
  gate_id, actuator_id, order (1..n, order hit)
  gate_kind  {TOKEN_PURCHASE, METERED_TOKEN, PERMIT, PROHIBITION,
              CONDITION_BAN, CODE_STANDARD, PRIVATE_RULE}
     PRIVATE_RULE = lease, HOA, or landlord rule — not a statute
  jurisdiction, t_from, t_to                        (as A-2)
  trigger_condition  None | named condition (e.g. drought declaration)
  gate_state         A-2 enum; default UNKNOWN
  access_is_right    {TRUE, FALSE, UNKNOWN}          (A-2.1 proposal,
  revocable_by       None | named office              adopted here)
  source, grade
An actuator's state at (jurisdiction, t, condition) is the SERIES of its
gates. It never collapses to one gate_state.

### 2c. couplings — how a gate on one stock reaches another
  coupling_id, from_stock, to_stock, mechanism, sign,
  sensor_effect {NONE, SENSOR_CORRUPTED}, source, grade
Seed row: THERMAL -> WATER. Cold suppresses thirst and raises urine
  output (cold diuresis), so the water sensor moves opposite to the
  stock. sensor_effect = SENSOR_CORRUPTED. Grade K: attach a physiology
  citation before any hold.
RULE: a gate propagates across stocks ONLY through a declared coupling
  row. No implicit propagation.

### 2d. derived quantities
  gates_per_actuator(j, t, cond)       count; also split by gate_kind
  nonmarket_gates(j, t, cond)          excludes TOKEN_PURCHASE
  ungated_residue(j, t, cond)          actuators with zero gates
  residue_capacity                     NOT COMPUTED. Whether the ungated
      residue can hold core temperature under a condition needs
      physiological data not supplied. Field exists; value
      NOT_EVALUABLE.

### 2e. direction is never pooled
No expression may combine WARM and COOL gates into one value. Assert by
AST (the pattern of RIN_062 and RIN_071). Shedding clothes to cool and
acquiring clothes to warm are gated by different bodies of rule.

## 3. SOURCING LIST — every fixture below is K until one of these lands
T-1  Grants Pass v. Johnson (US Sup. Ct. 2024): public-camping bans are
     enforceable. Closes self-built shelter on public land.
     Read the opinion; record the date and holding.
T-2  USFS firewood permits: one named national forest, with its
     permit rule.
T-3  Winter utility disconnection: one state WITH a seasonal
     moratorium and one WITHOUT. Statute or commission rule text.
T-4  Burn ban: one county-level ban with its trigger condition in the
     text.
T-5  Wood heater emission standard: EPA NSPS for residential wood
     heaters. Cite the rule and its effective year.
T-6  Public indecency statute, one state: gates the SHED direction.
T-7  PRIVATE_RULE: one real lease or HOA clause banning window AC units
     or restricting window opening. It must be an actual document, not
     a description.
T-8  Physiology citation for cold diuresis / thirst suppression (for
     the coupling row).
T-9  Human thermoneutral range, unclothed (for the section 1 claim
     that the internal regulator is narrow).

## 4. FIXTURES
F-T1  shelter, self-built, public land, US city, t >= 2024 (T-1)
F-T2  open fire, county X, trigger = drought declaration: two rows,
      condition active and condition inactive (T-4)
F-T3  utility heat, state A with moratorium vs state B without, same
      winter date (T-3)
F-T4  wood stove: a 4-gate series — device purchase -> emission
      standard -> fuel (purchase OR T-2 permit) -> burn ban (T-5, T-2,
      T-4)
F-T5  clothing SHED, state X (T-6)
F-T6  body-only huddling: zero gates. CONSTRUCTED, flagged, not
      hold-eligible.
FAIL FIXTURE: F-T4 run through unamended A-2 code must return ONE
  gate_state for a 4-gate series. Stacking is not representable
  before this amendment.
FAIL FIXTURE 2: an input pooling F-T5 (SHED) with a clothing RETAIN row
  must be rejected by the 2e assertion.

## 5. SCOPE LIMITS
- All rows are K. No hold is possible until section 3 is worked.
- Nothing in this folder is a statement about the law of any
  jurisdiction (RIN_076 applies).
- residue_capacity is deliberately uncomputed.
- The gate_kind enum is a first cut. TOKEN_PURCHASE is a gate by
  definition, which makes some predictions near-definitional (see
  E-A3-2).
- FWO-15 RESEND is still pending, separate from this.

## 6. EXPECTED — Claude's, committed before code
E-A3-1  Unamended code collapses F-T4's four gates to one state and
        accepts the pooled SHED+RETAIN input. The amended code does
        neither.
E-A3-2  WEAKNESS STATED FIRST: counting TOKEN_PURCHASE, every
        EXTERNAL_OBJECT actuator is gated trivially. So the real
        prediction is:
        E-A3-2a  At t=2026, in each sourced jurisdiction, every
                 EXTERNAL actuator carries >= 1 NON-MARKET gate
                 (permit, prohibition, condition ban, code standard,
                 or private rule).
        FALSIFIER: any sourced external actuator whose only gate is
                 TOKEN_PURCHASE. Clothing RETAIN is the likely
                 falsifier. Report it if it fires.
E-A3-3  The WARM-gating and COOL-gating instruments are disjoint in the
        sourced set: no single instrument gates both directions.
        FALSIFIER: one instrument appearing on both sides.
E-A3-4  ungated_residue at t=2026 contains BODY-locus actuators only.
        FALSIFIER: any sourced non-body actuator with zero gates.
E-A3-5  The THERMAL -> WATER coupling propagates the F-T1 gate into the
        water loop only via row 2c. Removing the coupling row removes
        the propagation. Asserted in the test.
E-A3-6  Condition coincidence (a burn ban active during a cold event)
        is NOT_EVALUABLE without weather data. Registered as open, not
        predicted.
