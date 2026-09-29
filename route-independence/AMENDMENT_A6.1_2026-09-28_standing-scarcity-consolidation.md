# FWO AMENDMENT A-6.1 — 2026-09-28
# Access standing, the imposed-scarcity coupling, and the consolidation chain
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to A-6. A-3.1 rules apply.

## 1. ORIGIN
OBSERVED (Kavik): a person of mixed descent can be welcomed on several
  reservations while not being part of those peoples, and so does not
  receive the same treatment. The reason given is that the resources
  there are limited and gated by state and other regulation. Many
  reservations hold mixes of peoples, some of whom were never
  land-based: nomads and trail keepers who were placed onto land and
  consolidated. Few were peoples of that land, and consolidation
  continued afterward.
DERIVED (Claude): A-6's TRUE/FALSE eligibility cannot represent
  "admitted, not member". Standing therefore acts per ROUTE, not per
  case set. The scarcity that makes standing matter is imposed from
  outside the set, so it is a coupling to gates already in the schema.
  It is not a community-internal fact.

## 2. SCHEMA
### 2a. access_standing (replaces the boolean result of A-6 2c)
  access_standing {MEMBER, ADMITTED_NOT_MEMBER, EXCLUDED, NOT_RECORDED}
  eligible_sets(profile) now returns (case_set, standing) pairs
### 2b. per-route standing requirement
  routes.min_standing {ADMITTED_NOT_MEMBER, MEMBER, NOT_RECORDED}
  allocation_limited {TRUE, FALSE, NOT_RECORDED}
  reachable_* measurands (A-6 2c) include a route only if
  profile standing >= route min_standing
  NEW: standing_gap(profile, case_set)
       = routes in set with min_standing > profile standing (unit: routes)
### 2c. imposed-scarcity coupling
  couplings row type IMPOSED_SCARCITY:
    source = an external gate (A-2/A-3 gate_id, with layer from A-5 2d)
    target = allocation_limited route inside a case set
    effect = tightens allocation; raises effective min_standing
  RULE: allocation_limited = TRUE with no IMPOSED_SCARCITY row is
  flagged SCARCITY_UNATTRIBUTED. It is never silently read as internal.
### 2d. consolidation chain
  consolidation_events: event_id, instrument, date, grade,
    peoples_in (list | NOT_RECORDED), unit_out,
    mechanism {REMOVAL, CONSOLIDATION, CONVERSION_TO_CORPORATE,
               TERMINATION, RESTORATION}
    prior_mode_of_peoples_in {TERRITORIAL, MOBILE, MIXED, NOT_RECORDED}
  residence_presumption_chain = ordered pair
    (consolidation_event that created the unit,
     recognition evidence path that rewards residence in that unit)
  A chain with a missing link is reported with the missing link
  named. It is never collapsed into a single criterion read.

## 3. SOURCED CASES (grades as of this amendment)
CE-1  Indian Removal Act, May 28 1830, 4 Stat. 411.        P (citation)
      Mechanism REMOVAL. Removal treaties under it approached seventy,
      moving nearly 50,000 people by the end of Jackson's presidency,
      with the destination intended to be confined to what became
      eastern Oklahoma (history.state.gov).                   S
      NPS gives about 100,000 removed in total across five nations.
      The two figures cover different scopes. Record both, do not merge.
CE-2  Worcester v. Georgia (1832): held that Georgia could not extend
      its law over Cherokee land; removal proceeded anyway.   S
      -> lawful_reach and physical outcome diverge on the record.
         This is the A-4 split with a court ruling attached.
CE-3  Alaska Native Claims Settlement Act, PL 92-203, Dec 18 1971.
      Extinguished aboriginal title; revoked all reservations except
      Metlakatla; created 12 regional corporations and 200+ village
      corporations.                                           S (several)
      Mechanism CONVERSION_TO_CORPORATE. Land claim -> shareholding,
      governed by corporate law. Same structure as A-2.1: a right
      converted into a holding under another instrument.
      Metlakatla = the single non-converted control.
      Forcing event: federal leasing/state selection frozen by unresolved
      Native title (Kodiak ANCSA history PDF, 1971)           S
      The Prudhoe Bay/pipeline link is supported only by Grokipedia -> K.
      Pull an agency or congressional source before any hold.
CE-4  25 CFR 83.11(b), current: distinct community from 1900 to present,
      "understood flexibly" in context of history, geography, culture,
      social organization (eCFR).                             P
      83.11(b)(2): "more than sufficient" evidence paths include
        (i)   >50% reside in an area almost exclusively of members
        (ii)  >=50% married within the entity
        (iii) >=50% keep distinct cultural patterns
        (iv)  distinct social institutions covering >=50%
        list TRUNCATED in the retrieved text; further paths NOT_RECORDED
      residence_presuming_paths >= 1 (unit: evidence paths)
      total_paths = NOT_RECORDED. Read the full eCFR text.
CE-5  1994 rule 83.7(f): criteria apply to groups that "historically
      combined and functioned as a single autonomous political entity."
      1994 83.1: continuous = from first sustained contact with
      non-Indians.                                            S
      Whether the current rule retains 83.7(f) = NOT_RECORDED.
      E-A6-3 is scored on the CURRENT text only.

## 4. STILL TO SOURCE
S-1  one denied Part 83 petition whose finding turned on 83.11(b)
     (the community criterion); record which evidence paths failed
S-2  one agency roll or treaty placing >= 3 distinct peoples in one
     administrative unit (Indian Territory agencies are candidates)
S-3  a people recorded as MOBILE before a consolidation event, sourced
     by ethnography or treaty text, not by assumption
S-4  a documented case of a Native land base reassigned after resource
     development in Alaska, beyond the general ANCSA case
S-5  full current 83.11 text; total evidence-path count

## 5. EXPECTED — Claude's, committed before code
E-A6.1-1  With a constructed IMPOSED_SCARCITY row on one route,
          standing_gap(P-ADMITTED) >= 1 (unit: routes).
          FALSIFIER: standing_gap = 0 (unit: routes).
E-A6.1-2  At least one residence_presumption_chain has BOTH links sourced
          at grade >= S (unit: chains).
          FALSIFIER: 0 chains with both links sourced.
          Status now: consolidation link CE-1 at S; recognition link
          CE-4(i) at P; the join between them (same peoples, same unit)
          is NOT sourced -> NOT_EVALUABLE until S-2/S-3 land.
E-A6.1-3  CE-3 conversion: every Alaska case except Metlakatla carries
          mechanism CONVERSION_TO_CORPORATE (unit: cases with a
          different mechanism = 0).
          FALSIFIER: >= 1 non-Metlakatla case with another mechanism.
E-A6-3 REVISED: residence_presuming_paths >= 1 (unit: evidence
          paths) HELD(P) on current text. The earlier "criteria" unit was
          wrong: the presumption sits in an evidence path, not in a
          criterion's wording.

## 6. SCOPE LIMITS
- No person's family history goes in this folder. Kavik's statement is
  carried in section 1 in general form only.
- One consolidation chain proves nothing about all recognized units.
  Report per chain.
- The regulation's flexibility clause is recorded alongside the
  evidence paths. The residence path is one route to sufficiency, not
  a requirement.
- Figures from different scopes (CE-1) are never pooled.
