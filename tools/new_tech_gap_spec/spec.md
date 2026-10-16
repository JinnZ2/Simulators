# NEW-TECH GAP SPEC

An instrument for reading a new technology before it ships: which standard
interfaces it touches, what nobody has measured, where the jurisdictions
leave a seam, and who carries the cost while the rules catch up. It is not
a finding about any product and not a position for or against any product.

Status tags on every item:

    OBSERVED    recorded fact, source named
    DERIVED     follows from OBSERVED items by stated reasoning
    PROPOSED    a design, rule or experiment offered for testing
    UNMEASURED  a quantity that exists and has no measurement on record

Requirement words follow RFC 2119 usage: SHALL (mandatory, testable),
SHOULD (default, deviation needs a stated reason), MAY (permitted).

---

## 0. DISCIPLINES

D1  [PROPOSED] Every requirement SHALL be written so a third party can
    test it: a condition, a measurement, a pass/fail line.

D2  [PROPOSED] Rules SHALL attach to the 14 standard interfaces in
    section 1, not to a named device. A technology declares the
    interfaces it touches; an auditor SHALL check all 14 anyway, and an
    interface the maker did not declare is reported as UNDECLARED, never
    as clear. No per-device patches.

D3  [PROPOSED] Each rule SHALL carry a trace to the hazard it controls.
    A rule whose hazard is shown gone (design change, measurement) SHALL
    retire. A rule with no hazard trace is not admitted.

D4  [PROPOSED] Interim rules SHALL carry a sunset date. At sunset the rule
    either hardens (with the measurement that justified it) or lapses.

D5  [PROPOSED] The maker SHALL declare a design envelope (speeds, loads,
    surfaces, weather, users, duration). Use outside the envelope is not
    excluded from review; it is routed to section 10 (forward
    trajectories) as a branch.

D6  [DERIVED] Absence of evidence of harm is not a measurement. A
    quantity no one has measured is tagged UNMEASURED and stays open; it
    is never entered as zero.

---

## 1. THE 14 STANDARD INTERFACES

For each interface the auditor records: TOUCHED / NOT TOUCHED /
UNDECLARED, the contact mechanism, and the rule (if any) that already
covers it.

 1. Ground          surfaces, roadbed, subsurface, soil, structures at grade
 2. Air / airspace  flight levels, plume, emissions, noise propagation
 3. Human body      operator: injury, exposure, fatigue, sensory load
 4. Bystander       people who did not choose the technology
 5. Automation      other machines that must perceive or react to it
 6. Data custody    what is recorded, where it goes, who can get it back
 7. Energy          storage, release, failure energy, charging/refill
 8. Jurisdiction    which authority's rules apply, and where they stop
 9. Labor           work it changes, workers it exposes, employment status
10. Maintenance     inspection, repair, recertification, end of life
11. Money           who pays for damage, wear, enforcement, insurance
12. Responders      fire, EMS, police, tow: what they meet at a scene
13. Law / judicial  (sub-table below)
14. Governance      (sub-table below)

### 1.13 Law / judicial

For each body of law the auditor records FITS / AMBIGUOUS / ABSENT.

    tort / product liability
    criminal
    privacy / wiretap
    contract
    insurance
    property
    4th Amendment (search, seizure, data)

[DERIVED] AMBIGUOUS is the expensive state. ABSENT invites a new rule;
AMBIGUOUS invites litigation, and each body of law marked AMBIGUOUS is
a place where cost accrues case by case until an appellate court
settles it. The count of AMBIGUOUS rows feeds the court projection in
section 10.

### 1.14 Governance

Layers: federal / state / local / corporate (terms of service, platform
policy, employer policy) / social (norms, informal enforcement).

[DERIVED] The gap is where layers contradict, not where one layer is
silent. The auditor SHALL list every pair of layers whose rules cannot
both be obeyed, and every pair where one layer's compliance is
evidence against the actor under another layer.

---

## 2. CHECKLIST (10 SECTIONS)

### S1. Contact surfaces
[PROPOSED] List every physical, informational and financial surface the
technology meets, mapped to the 14 interfaces. Undeclared surfaces
found by the auditor are listed apart from declared ones.

### S2. Jurisdiction map and seams
[PROPOSED] Draw each authority's boundary (agency, level, geography).
Mark every seam: a place where the technology crosses from one
authority to another, or sits where neither claims it. For each seam:
who enforces, with what tool, and what happens to an incident that
falls in it.

### S3. Dependency chain and single points of failure
[PROPOSED] Trace the chain from inputs (energy, parts, software,
network, compute) to safe operation. Name every element whose failure
alone removes a safety function. A safety function that depends on one
log, one server, one sensor or one vendor is a single point of failure
and SHALL be named as one.

### S4. Actual use, with misuse as the baseline
[PROPOSED] Model the population that will actually buy and use the
technology, not the intended user. Deliberate misuse, stunt use,
copycat use and use for content production SHALL be the baseline case,
not a tail case. Design controls are tested against the baseline.

### S5. Third-party, bystander and automation exposure
[PROPOSED] For each party who did not choose the technology: what
reaches them, at what energy, with what warning. Automated systems
(AVs, driver-assist, building systems, alarms) count as exposed parties
and SHALL be tested for perception and response.

### S6. Unmeasured quantities
[PROPOSED] List every quantity a rule, fee or liability split would
need and that has no measurement on record. Tag each UNMEASURED. No
rule or fee that depends on an UNMEASURED quantity SHALL harden until
it is measured; the measurement plan is part of this section.

### S7. Liability at every handoff
[PROPOSED] At each handoff in the chain (maker, seller, owner, operator,
service provider, cloud, insurer, public budget) state who carries a
loss that originates there and under which body of law. A handoff with
no stated bearer is a gap.

### S8. Maintenance, repair, aftermarket
[PROPOSED] Inspection intervals, recertification, who is qualified to
repair, what certification exists for them, what DIY and aftermarket
modification does to the envelope, and how end of life is handled.

### S9. Closest precedent and where it breaks
[PROPOSED] Name the closest existing technology and rule set, then the
specific points where the analogy fails. The break points are the gaps.

### S10. Forward trajectories
See section 3.

---

## 3. S10 IN DETAIL: FORWARD TRAJECTORIES

### 3.1 Gates
[PROPOSED] Three upstream gates are checked before any projection:

    electricity   grid capacity, price, outage exposure
    supply chains parts, materials, tooling, single-source items
    compute       cloud capacity, model access, data-center dependence

A gate failure (sustained shortage, price shock, loss of a supplier)
SHALL trigger review of every downstream projection that assumed the
gate open.

### 3.2 Branches
[PROPOSED] Each projection branch records:

    adjacent technology     what it combines or competes with
    direction               use / misuse / convergence
    probability band        likely / plausible / edge
    basis tag               OBSERVED / DERIVED / PROPOSED / UNMEASURED
    early signals           what would show the branch is live
    sections reopened       which of S1-S9 must be redone if it goes live

### 3.3 Version stamp and incident log
[PROPOSED] Every projection SHALL carry a version and date. Real
incidents are logged against the projection that did or did not
anticipate them. A projection is not edited after the fact; a new
version is issued beside it.

### 3.4 Court projection
[PROPOSED] From the 1.13 table:

    n_ambiguous          count of bodies of law marked AMBIGUOUS
    time_to_precedent    estimated years until an appellate ruling
                         settles each
    interim_cost         cost accruing per year, by budget that pays it
    default_bearer       the party that cannot push the cost elsewhere

Comparators for time_to_precedent:
- [OBSERVED, carried] Ride-share worker classification and liability
  took roughly a decade of litigation and legislation, and parts are
  still contested.
- [OBSERVED, carried] Drone overflight and privacy law remains
  unsettled at the property-line and 4th Amendment level.

[DERIVED] The default bearer is whoever cannot push the cost off:
usually the injured bystander, the local public budget, or the worker
without an employer of record.

---

## 4. CROSS-CUTTING GAPS

G1  [UNMEASURED] Cybersecurity and remote takeover: can the safety
    function be disabled or triggered remotely, and by whom.
G2  [UNMEASURED] End of life: stored energy, pressure vessels,
    batteries and data left in retired units.
G3  [PROPOSED] International and tribal crossover: tribal lands and
    border regions carry separate jurisdiction; the S2 map SHALL include
    them, not default them to the surrounding state.
G4  [UNMEASURED] Combined interactions between new technologies (a
    wearable recording an incident involving an airborne vehicle seen by
    an AV). Each spec is written alone; the combinations are read by no
    one.
G5  [DERIVED] Standards lag: consensus standards (SAE, ASTM, UL, IEEE)
    take years; a technology can ship before a standard exists, and the
    spec SHALL say which interfaces have no standard.
G6  [DERIVED] Insurer withdrawal: when insurers exclude or decline a
    risk, the risk does not disappear; it moves to public budgets and to
    the injured party. Track exclusions as an early signal.

---

## 5. CLOCK-RATE MISMATCH

[DERIVED] Products move on a release clock (months). Rules move on a
rulemaking clock (years). Courts move on a precedent clock (a decade).
Between the release and the rule, the cost lands on whoever is on the
fastest clock with the least power to move it.

Experiments to close the mismatch, all PROPOSED, sector fit UNMEASURED:

a.  [PROPOSED] Launch gated on spec filing: a completed gap spec is
    filed before sale; filing is not approval, only disclosure.
b.  [PROPOSED] Provisional rules at announcement: interim rules issue
    when a product is announced and sunset or harden on measurement (D4).
c.  [PROPOSED] Continuous telemetry to regulators: incident and use
    data flow to the regulator during the interim period, so the
    measurement in S6 accrues at the release clock.
d.  [PROPOSED] Maker risk bond scaled to the unmeasured quantities: the
    larger the S6 list, the larger the bond; the bond shrinks as items
    are measured.

[UNMEASURED] Whether any of a-d fits a given sector (vehicles, consumer
electronics, medical, aviation) has not been tested.

---

## 6. SCOPE LIMITS

- This spec lists gaps. It does not estimate the probability of any
  harm and does not rank technologies.
- Every OBSERVED item in a worked case cites a source; sources were
  read through search results only unless stated otherwise.
- The spec is written from the risk-mitigation side for common workers
  and responders. A reader holding a different side should expect
  different weights, not different gaps.
