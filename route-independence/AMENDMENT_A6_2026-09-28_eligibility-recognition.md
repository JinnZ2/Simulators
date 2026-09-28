# FWO AMENDMENT A-6 — 2026-09-28
# Eligibility-gated terminus count, and the recognition asymmetry
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to A-1..A-5. A-3.1 rules apply (units on counts, falsifier ==
NOT prediction, NONE vs NOT_RECORDED, coverage printed with holds).

## 1. ORIGIN
OBSERVED (Kavik): entry to the reservation and Amish case sets is
  itself gated. A non-native person is not welcome on a reservation, and
  a non-Amish person is not welcome into Amish community; neither way of
  life can be adopted from outside. A person of mixed descent whose
  people were migrant or nomadic, never received a reservation, and were
  never registered with the federal government has no such place. That
  person must live in the general society under the money rules, with
  no choice.
DERIVED (Claude): A-5 measured which termini EXIST across case sets.
  That is not the number of termini REACHABLE by a given person. The two
  were merged in A-5, so this is the fourth instance of the class (meld,
  endpoint count, branch-as-route, exists-as-reachable).
  A-5's terminus_kinds is kept. It answers a different question.

## 2. SCHEMA
### 2a. entry gate per case set
  case_sets.entry_condition   text, sourced
  eligibility_basis {BIRTH, DESCENT_DOCUMENTED, ENROLLMENT_BY_NATION,
                     RECOGNITION_BY_STATE, COMMUNITY_ADMISSION,
                     DEFAULT_RESIDENT, NOT_RECORDED}
  acquirable_by_outsider {TRUE, FALSE, RARE, NOT_RECORDED}
      RARE requires a sourced rate or count; no rate -> NOT_RECORDED
  entry_revocable_by {NONE, named office/body, NOT_RECORDED}
  Entry is often a chain: e.g. the nation must be recognized, and then
  the person must be enrolled. Store entry as an A-4 chain, not a flag.
### 2b. person profiles (constructed, never real individuals)
  profile_id, attributes {descent_documented, enrolled_in, recognized_
  nation_member, community_admitted, residence_jurisdiction}
  PROFILES ARE CONSTRUCTED TEST CASES. No real person's details go in
  this folder.
### 2c. measurands
  eligible_sets(profile)           = case sets whose entry chain resolves
                                     TRUE for the profile (unit: case sets)
  reachable_terminus_kinds(profile, need)
                                   = terminus_kinds pooled over
                                     eligible_sets(profile) only (unit: kinds)
  reachable_nonmonetary_chains(profile, need)            (unit: chains)
  exists_vs_reachable_gap(profile, need)
      = terminus_kinds(all sets) minus reachable_terminus_kinds
        (unit: kinds; printed as the set, not only the count)
### 2d. lawful status of unrecognized practice
A route documented only in the practice of a people with no recognized
legal status gets lawful_reach NOT_RECORDED, never FALSE and never TRUE.
Recorded separately: recognition_status {RECOGNIZED, UNRECOGNIZED,
TERMINATED, RESTORED, NOT_RECORDED} with dated change events (reuse the
A-2 gate_change_events table).

## 3. RECOGNITION ASYMMETRY — its own instrument
Question: does the recognition instrument's EVIDENCE FORM presume
continuous occupation of a bounded territory? If so, peoples whose
pattern was mobile are filtered at the recording step, not on the
merits, and every downstream route count inherits that filter.
Sources to pull (all grade K until read):
  RA-1  25 CFR Part 83, the federal acknowledgment criteria (83.11),
        read in full: which criteria's accepted evidence refers to
        residence, geographic concentration, or continuous community
  RA-2  the criterion barring members who are predominantly members of
        another acknowledged tribe — record how it treats a person of
        mixed descent across several peoples
  RA-3  one Termination-era act and its restoration act (the Menominee
        termination in 1954 and restoration in 1973 are the candidate
        pair) -> recognition as revocable_by Congress, same structure as
        A-2.1's revocable permission
  RA-4  one nation's published enrollment criteria (descent documentation,
        lineal or quantum) -> ENROLLMENT_BY_NATION
  RA-5  an Amish-conversion rate or count from published ethnography ->
        grounds RARE or leaves it NOT_RECORDED
Measurand:
  residence_presuming_criteria = criteria in RA-1 whose accepted
  evidence forms include residence or geographic concentration
  (unit: criteria, printed with the clause text reference)

## 4. FIXTURES (all constructed)
P-0   default resident, no descent documentation, no admission
      -> eligible_sets = {CS-G}
P-1   enrolled member of the CS-R nation -> {CS-G, CS-R}
P-2   Amish by birth, baptized -> {CS-G, CS-A}
P-3   documented descent from several peoples, none recognized, no
      enrollment anywhere -> {CS-G}. FAIL FIXTURE: A-5 code, which
      pools all sets, reports P-3's reachable termini as those of every set.
P-4   member of a nation whose recognition was terminated and later
      restored -> eligibility is time-indexed; evaluated at both dates

## 5. EXPECTED — Claude's, committed before code
E-A6-1  eligible_sets(P-3) = 1 (unit: case sets).
        FALSIFIER: eligible_sets(P-3) >= 2.
E-A6-2  exists_vs_reachable_gap is non-empty for >= 1 of P-0..P-4 for
        some need (unit: profiles).
        FALSIFIER: the gap is empty for every profile and need.
        NOTE: if A-5 finds that CS-R and CS-A share CS-G's termini, this
        falsifier fires. That is a result, not a failure: the termini
        match and entry gating changes nothing about them. Report both.
E-A6-3  residence_presuming_criteria >= 1 (unit: criteria) on reading
        RA-1 in full.
        FALSIFIER: 0 criteria after a full read. NOT_EVALUABLE until
        RA-1 is read; do not fill it from memory.
E-A6-4  under RA-3, eligible_sets for P-4 differs between the
        termination date and the restoration date (unit: case sets).
        FALSIFIER: identical at both dates.
CONSISTENCY CHECK (not a prediction): if E-A5-1 holds, then
reachable_nonmonetary_chains(P-3) = 0 follows mechanically. It is
asserted in the code, not scored as a hold.

## 6. SCOPE LIMITS
- Profiles are constructed. No real person, family, or unrecognized
  people is named or described in this folder.
- CS-R is one named nation. Entry rules differ across nations; no
  result generalizes past the sourced nation.
- "Not welcome" is recorded as entry_condition only where a source
  states the rule; otherwise acquirable_by_outsider = NOT_RECORDED.
- Section 3 measures the evidence form of the recognition instrument.
  It makes no claim about any specific petition's merits.
- Nothing here is legal advice or a statement of law beyond the cited
  text (RIN_076).
