# FWO AMENDMENT A-4 — 2026-09-28
# Routes are chains: prerequisite steps, shared gates, required terminal state
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to FWO-5, FWO-8, A-1..A-3.1. Nothing retracted.
A-3.1 rules apply: counts carry units, falsifier == NOT prediction,
NONE vs NOT_RECORDED, coverage printed with every hold.

## 1. DEFECT — author: Claude
The rainwater fixtures (F-W1..F-W4) measured ONE gate on ONE step and
called it the route. Correction from Kavik (OBSERVED, hers):
- Collection needs LAND. You cannot collect in a park or on a sidewalk.
- Raw rainwater is not drinkable. Drinking it straight invites illness.
  Filtration is required.
- Filtration media (charcoal, sand) are themselves gated. Charcoal needs
  fuel burned; fuel needs land access or a permit.
Consequences (DERIVED, Claude):
- A route is a CHAIN of steps, and its gates are the UNION across all
  steps.
- The physical need is POTABLE water, not water. A step sequence that
  does not reach the terminal state does not meet the need.
- The land gate appears more than once and is shared with other routes
  (shelter, fuel). One closure can remove several routes at once. This
  is why counting route ENDPOINTS undercounts.

## 2. SOURCED INPUTS (grades P / S / K as before)
C-1  CO HB 16-1005 enrolled text: collected precipitation may not be
     used "for drinking water or indoor household purposes"; outdoor
     use on the collecting property only.
     Grade P (fragment read). Read the full section 37-96.5-103 before
     any hold.
C-2  Rooftop runoff generally carries bacteria including from animal
     feces (worldwaterreserve.com, 2026).                Grade S
     Replace with a public-health or peer-reviewed source (T-10).
NOT SOURCED:
T-10 A potability standard for harvested rainwater (a public-health
     agency or a peer-reviewed paper).
T-11 A prohibition on collecting water or natural materials in one
     named municipal park (ordinance text).
T-12 A restriction on sand or soil extraction from public land (one
     named rule).
T-13 Charcoal production: a burn or open-fire rule covering it (it may
     reuse T-4).

## 3. SCHEMA
### 3a. needs carry a terminal state
  need_id, stock, terminal_state (e.g. WATER -> POTABLE)
A chain meets the need only if its final step produces terminal_state.

### 3b. chains
  chain_id, need_id, jurisdiction, t
  steps: ordered list; each step has
     step_id, action, produces, requires (list of prerequisite
     step_ids or resource_ids), gates (A-3 gate rows, ordered)
  requires may point into ANOTHER chain (a charcoal step requires the
  fuel chain). Chains form a DAG across needs.
  use_restriction  per step: NONE | NOT_RECORDED | named restriction
     (e.g. C-1: OUTDOOR_ONLY, NOT_FOR_DRINKING)
A step whose output carries a use_restriction excluding terminal_state
cannot feed the terminal step LAWFULLY. Record lawful_reach and
physical_reach separately. Never merge them.

### 3c. shared resources
  resource_id (e.g. LAND_TENURE, FUEL, TOKEN), kind,
  gates (A-3 rows)
A resource referenced by more than one chain is SHARED.
  shared_by(resource) = set of chain_ids   (unit: chains)
  closure_impact(resource) = chains that lose lawful_reach when that
     resource's gate closes                (unit: chains)

### 3d. regress termination
Walk requires recursively. Every chain bottoms out in one of:
  BODY          physical act, no external input
  TOKEN         purchase / metered token
  NOT_RECORDED  walk stopped: no source for the next step
  CYCLE         the walk revisits a node (e.g. fuel -> land -> token
                -> labor -> ...). Report the cycle path. Do NOT break
                it.
  terminus(chain)  = the multiset of termini   (unit: leaves)

### 3e. derived
  gates_per_chain = |union of gates across all steps and requires|
                    (unit: gates)
  steps_per_chain                            (unit: steps)

## 4. FIXTURES (all K unless marked)
F-R1  CO rooftop rainwater -> POTABLE, t=2026:
      LAND_TENURE (shared) -> collect (C-1 cap, OUTDOOR_ONLY) ->
      filter (requires charcoal, sand) -> POTABLE
      charcoal requires FUEL (shared) -> fuel requires LAND_TENURE or
      permit (T-2) -> burn (T-4 / T-13)
F-R2  same chain, no LAND_TENURE (renter or unhoused): collect is
      unreachable lawfully.
F-R3  public park collection, municipality X (T-11): PROHIBITED at
      step 1.
F-R4  boil instead of filter: requires FUEL. This shares the gate with
      thermal chain F-T4 (the A-3 wood stove).
FAIL FIXTURE: F-R1 through unamended A-2/A-3 code must return 1 gate
(unit: gates) for the rainwater route, the collection cap only.

## 5. EXPECTED — Claude's, committed before code
E-A4-1  F-R1: unamended code returns 1 gate. Amended code returns
        >= 4 gates (unit: gates) over >= 4 steps (unit: steps).
        FALSIFIER: amended gates_per_chain(F-R1) < 4.
E-A4-2  For F-R1 at CO t=2026, lawful_reach(POTABLE) = FALSE: C-1
        excludes drinking. physical_reach may be TRUE.
        FALSIFIER: lawful_reach(POTABLE) = TRUE.
E-A4-3  shared_by(LAND_TENURE) >= 3 (unit: chains) across the fixture
        set (water, fuel, shelter).
        FALSIFIER: shared_by(LAND_TENURE) < 3.
E-A4-4  No chain in the fixture set terminates ONLY in BODY; every
        chain has >= 1 TOKEN, NOT_RECORDED or CYCLE leaf
        (unit: leaves).
        FALSIFIER: >= 1 chain whose termini are all BODY.
E-A4-5  closure_impact(LAND_TENURE) > closure_impact(any single
        statutory gate) (unit: chains).
        FALSIFIER: some statutory gate with closure_impact >=
        closure_impact(LAND_TENURE).
All five: run the A-3.1 complement check before committing; print
coverage.

## 6. SCOPE LIMITS
- Everything except C-1 is K or S. No hold reads above HELD(S).
- physical_reach is not a health claim. Potability needs T-10.
- CYCLE termini are reported, not interpreted. Whether a cycle is a
  trap or a normal economy is not decided here.
- Nothing in this folder is a statement about the law of any
  jurisdiction (RIN_076).
- FWO-15 RESEND is still pending, separate from this.
