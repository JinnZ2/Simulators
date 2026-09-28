# FWO AMENDMENT A-5 — 2026-09-28
# Terminus diversity: are "independent routes" branches of one chain?
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to FWO-5, FWO-8, A-1..A-4. Nothing retracted.
A-3.1 rules apply: counts carry units, falsifier == NOT prediction,
NONE vs NOT_RECORDED, coverage printed with every hold.

## 1. ORIGIN
OBSERVED (Kavik): on a reservation, among the Amish, or anywhere else,
  a person is still gated by the same things — by community, state,
  county, and other layers. Whatever the setting, the basic needs of life
  have no way out except through the money token. Her framing, carried
  as hers: gating the ability of life is anti-life, and that is where
  this society currently is.
  Her framing is provenance only. It does not appear in field names,
  enums, or output wording.
DERIVED (Claude): the instrument has counted routes (endpoints and
  chains). The stronger claim is about TERMINI: chains may differ in
  length and in which gates they cross while bottoming out in the same
  leaf. If so, routes counted as independent are BRANCHES of one chain.
  This is the third instance of one error class — the meld (A-1), the
  endpoint count (A-4), and now branch-as-route.

## 2. SCHEMA
### 2a. resolved terminus
From A-4 3d, every chain has termini in {BODY, TOKEN, NOT_RECORDED,
CYCLE}. TOKEN leaves are resolved further through FWO-8:
  token_type {MONETARY, CITATION, CREDENTIAL, SOCIAL_STANDING,
              OTHER_NAMED}
  follow converts_to until a type with no converts_to, or until a
  CYCLE is hit
  resolved_terminus = (kind, final token_type, hops)
A CREDENTIAL leaf converting to MONETARY in 2 hops resolves to
(TOKEN, MONETARY, 2). Hops are kept; the terminus is not the first
token seen.
### 2b. measurands
  terminus_kinds(case_set, need)
      = set of distinct resolved termini                  (unit: kinds)
  nonmonetary_chains(case_set, need)
      = chains with >= 1 resolved terminus that is not
        (TOKEN, MONETARY, *)                              (unit: chains)
  cycles are reported apart and never counted as non-monetary
### 2c. independence re-read
A FWO-5 route marked INDEPENDENT that shares every resolved terminus
with another route is reclassified BRANCH_OF(route_id). The FWO-5 row
is kept; the new reading prints beside it.
### 2d. jurisdiction layering
A step's gates may come from several layers. Each gate row gains:
  layer {FEDERAL, STATE, COUNTY, MUNICIPAL, TRIBAL, COMMUNITY_RULE,
         PRIVATE_RULE}
COMMUNITY_RULE covers unwritten or internal rules (e.g. a church
district's rules). Its grade is capped at S unless a published text
exists.

## 3. CASE SETS — separate sourcing, no case set inherits another's rows
CS-G   general: the rows from A-2..A-4.
CS-R   reservation. ONE named nation with a PUBLISHED tribal code, plus
       the federal trust-land layer. Do not generalise across nations;
       each nation is its own case set. Sources needed:
       R-1 tribal code sections on water, fuel/wood, and housing or
           land assignment
       R-2 federal trust-land rule governing land use/leasing (the BIA
           layer)
       R-3 state/county rules that reach trust land, if any; record
           the reach explicitly, never assume it
CS-A   Amish. Start from the existing route-independence Amish case
       and RIN_063 (property tax on the land one lives on). Sources:
       A-1s Wisconsin v. Yoder (1972)                     K
       A-2s the self-employment tax exemption for qualifying religious
            groups (IRC 1402(g))                           K
       A-3s published ethnography of district rules (e.g. Kraybill)
            -> COMMUNITY_RULE, grade <= S
       A-4s county property-tax obligation on Amish-held land, one
            named county
Needs run in each case set: WATER->POTABLE, FOOD, THERMAL (A-3
actuators), SHELTER.

## 4. FIXTURES
F-B1  two routes with different step lists and the same resolved
      terminus -> BRANCH. This is the fail fixture: unamended FWO-5
      code reads both as INDEPENDENT.
F-B2  a CREDENTIAL leaf with converts_to MONETARY in 2 hops ->
      resolves (TOKEN, MONETARY, 2), not CREDENTIAL.
F-B3  a chain whose termini are BODY only (constructed; flagged,
      hold-ineligible). Proves the non-monetary count can be nonzero.
F-B4  a CYCLE chain -> reported apart; nonmonetary_chains unchanged.

## 5. EXPECTED — Claude's, committed before code
E-A5-1  CS-G, each need: nonmonetary_chains = 0 (unit: chains).
        FALSIFIER: nonmonetary_chains >= 1 for any need.
E-A5-2  CS-R: terminus_kinds(CS-R, need) == terminus_kinds(CS-G, need)
        for every need, with (TOKEN, MONETARY) present in both.
        FALSIFIER: the two sets differ for any need.
E-A5-3  CS-A: the same comparison against CS-G.
        FALSIFIER: the sets differ for any need.
        NOTE: E-A5-2/3 are about TERMINI only. Chain length and gate
        layers are expected to differ; report steps_per_chain and the
        layer mix beside each result, uninterpreted.
E-A5-4  Re-reading FWO-5 INDEPENDENT rows under 2c reclassifies >= 1
        route as BRANCH (unit: routes).
        FALSIFIER: 0 routes reclassified.
Report each falsifier firing as its own finding. A falsifier firing on
E-A5-2 or E-A5-3 is information, not a failure of the case set.

## 6. SCOPE LIMITS
- CS-R and CS-A need sourcing before any hold. Until then they are
  NOT_EVALUABLE and must not be filled from CS-G.
- COMMUNITY_RULE sources are capped at S.
- terminus_kinds says nothing about burden size. Two case sets can
  share a terminus with very different gate counts and joule costs.
  That comparison is a separate measurand, not assumed here.
- Nothing in this folder is a statement about the law of any
  jurisdiction or about any community's practice beyond its cited
  source (RIN_076).
- FWO-15 RESEND is still pending, separate from this.
