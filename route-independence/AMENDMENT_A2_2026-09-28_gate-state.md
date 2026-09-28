# FWO AMENDMENT A-2 — 2026-09-28
# Gate state is time- and jurisdiction-indexed; routes carry removal events
License: CC0. Stdlib only. Target: Claude Code.
Repo: JinnZ2/Simulators  Branch: claude/coupling-check-disaster-twiklx
Folder: route-independence/
Additive to FWO-5, FWO-8, A-1. Nothing retracted. Nothing auto-assigned.

## RULES (unchanged, restated)
R1  Commit EXPECTED (section 5) alone, before any code. Separate commit.
R2  Sourced inputs only. A fixture row with no source is tagged
    CONSTRUCTED_UNSOURCED and cannot contribute to any hold.
R3  Every new test suite ships with a fail fixture.
R4  Report failed predictions first.

## 1. DEFECT — author: Claude
F-A3 ("rainwater on own land, no permit regime") was CONSTRUCTED, not
observed. It failed R2 in Claude's own design. The condition "no permit
regime" did all the work, and it is false in named jurisdictions.
Correction from Kavik (OBSERVED, hers): where collection is restricted,
the route is gated. The gate is enforced by a dollar fine, confiscation,
and escalation.
Further (OBSERVED, hers): subsistence routes such as gleaning after the
harvest and eating from public land were ordinary practice and are now
closed or permit-gated. These are REMOVALS WITH DATES, not absent routes.

## 2. SOURCED INPUTS
Source grade: P = primary text read; S = secondary summary read;
K = known citation, not verified this session (verify before use).

G-1  England, gleaning, before 1788. The customary license to glean was
     recognised. Hale, Norfolk Summer Assizes 1668, quoted in the
     Steel v Houghton report: the license arises "by the general custom
     of England" but must be specially pleaded.          [P, Wikisource]
G-2  Steel v Houghton et Uxor (1788) 1 H Bl 51; 126 ER 32. Holding: no
     person has a right at common law to glean in the harvest field, and
     neither do the settled poor of a parish.            [P/S]
     Lord Loughborough, paraphrased: relief of the poor is a religious
     duty, not a legal obligation.                       [S, swarb]
     COURT CONFLICT: Wikipedia says House of Lords. Peter King (Law and
     History Review, doi 10.2307/743812) says Court of Common Pleas.
     Carry Common Pleas (peer-reviewed). Record the conflict. Do not
     resolve it silently.
G-3  Leviticus 19:9-10, 23:22; Deuteronomy 24:19-21. Codified gleaning
     provision.                                          [K]
W-1  Colorado. HB 16-1005 (2016); C.R.S. 37-96.5-103. Residential
     rooftop collection permitted up to 110 gal combined, max 2
     containers. Before 2016: effectively prohibited for most
     residential users.                                  [S, multiple]
W-2  Utah. Collection up to 2,500 gal with registration; 100 gal
     without.                                            [S]
W-3  States with no volume cap on residential collection (e.g. Texas;
     SB 769 (2011) bars HOA prohibition).                [S]
NOT SOURCED, no fixture until sourced:
     - US public-land foraging prohibitions and permit regimes
       (name the unit and the regulation).
     - UK Theft Act 1968 s.4(3), wild-plant carve-out.    [K]
     - Colorado pre-2016 penalty schedule (fine amounts, confiscation)
       as statute text.

## 3. SCHEMA
### 3a. Gate state is indexed, never bare
Every route row gains the following fields:
  jurisdiction      str, required
  t_from, t_to      ISO date or None (open-ended)
  gate_state        enum {OPEN, METERED_PERMISSION, PROHIBITED,
                          DISCRETIONARY, UNKNOWN}; default UNKNOWN,
                          which blocks scoring
     DISCRETIONARY = access exists only at the gate-holder's pleasure;
                     no enforceable claim (the G-2 reclassification)
  gate_instrument   statute / case / regulation id, or None
  gate_source       source id from section 2, required unless UNKNOWN
A route with no jurisdiction or no t reads UNKNOWN. It never reads OPEN.

### 3b. Removal / change events
New table gate_change_events:
  route_id, jurisdiction, date, instrument,
  from_state, to_state, source, grade (P/S/K)
Grade-K events are stored and flagged. They are excluded from holds.

### 3c. RIN_061 fix — obligation_origin
Add NONE = "no obligation present; origin inapplicable".
NONE is distinct from UNDECIDED = "not yet determined".
Re-read the 10 routes held as UNDECIDED for that reason. Each moves to
NONE only on stated grounds. Report the count.
(If you would rather ship this in the FWO-15 resend, drop 3c.)

## 4. FIXTURES
F-A3   RETIRED. Keep the row, tag CONSTRUCTED_UNSOURCED, exclude from
       holds. Do not delete it: it is the record of the defect.
F-W1   CO rainwater, t < 2016-08-10          PROHIBITED           W-1
F-W2   CO rainwater, t >= 2016-08-10         METERED_PERMISSION   W-1
F-W3   UT rainwater, >100 gal unregistered   PROHIBITED           W-2
F-W4   TX rainwater                          OPEN                 W-3
F-G1   England gleaning, t < 1788            OPEN (customary)     G-1
F-G2   England gleaning, t >= 1788           DISCRETIONARY        G-2
FAIL FIXTURE: F-W1 vs F-W2. The need, the physical act and the
jurisdiction are identical; only t differs. The unamended code must
return one identical record for both.
(Verify the HB 16-1005 effective date against the statute. If it
differs, update the date and cite it.)

## 5. EXPECTED — committed before code (Claude's predictions)
E-A2-1  Unamended code returns identical records for F-W1 and F-W2.
        The amended code separates them on gate_state alone.
E-A2-2  F-G1 -> F-G2 registers as one change event, OPEN ->
        DISCRETIONARY. It does not register as route absence. A count
        of routes at t=2026 misses it; a removal count finds it.
E-A2-3  In the delivered case set, at t=2026, no subsistence route
        (water, food, shelter) reads OPEN in every sourced jurisdiction.
        FALSIFIER: any single route OPEN in all sourced jurisdictions.
        W-3/F-W4 already make rainwater OPEN somewhere. The prediction
        is about "every", and the result must be reported per
        jurisdiction, not as one pooled number.
E-A2-4  DISCRETIONARY is not OPEN. No expression may treat a
        DISCRETIONARY route as independent. Assert this by AST, as with
        RIN_062.

## 6. INCORPORATED FROM AN EXTERNAL MODEL DOCUMENT (audited, not adopted whole)
TAKEN:   time-indexing of the monetary/gate variable (M_t). It is
         implemented here as gate_state over (jurisdiction, t).
         prevalence != necessity; enforcement != consent. These are
         already consistent with FWO-5 and A-1.
NOT TAKEN:
  - Its alternative-path list (hunting, gathering, sharing, barter,
    mutual aid) is ungated. This amendment's finding is that such
    paths carry dated closures. Listing them as open is the same
    defect as F-A3.
  - Its falsification form "exists R: FoodAccess(no money, R)" tests
    for existence in ANY regime. The instrument needs availability at
    (jurisdiction, t). A path open in 1700 says nothing about 2026.
  - Its provenance scale. Keep OBSERVED / DERIVED / PROPOSED plus the
    source grades P/S/K.

## 7. SCOPE LIMITS
- W-1..W-3 are secondary sources. Primary statute text is unread.
  Holds read HELD(S) until primaries are attached.
- The G-2 court conflict is open.
- The gate_state enum is a first cut. METERED_PERMISSION merges volume
  caps with registration; split them if a case needs it.
- No foraging fixtures until section-2 gaps are sourced.
- RIN_047 lag figures remain quarantined. They are not touched here.
- FWO-15 is still absent from both agent returns. RESEND is still
  pending and separate from this amendment.