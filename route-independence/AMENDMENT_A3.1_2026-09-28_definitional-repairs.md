# FWO AMENDMENT A-3.1 — 2026-09-28 — definitional repairs (authoring errors: Claude)
Additive. R1: commit this block alone before code.

## 1. ONE DEFINITION OF MARKET
MARKET_GATES = {TOKEN_PURCHASE, METERED_TOKEN}
NON_MARKET   = every other gate_kind
Section 2d nonmarket_gates and E-A3-2a both use this definition only.
Re-run E-A3-2a over the K rows under it; print the prior two-definition
result beside it.

## 2. PREDICTION/FALSIFIER COMPLEMENT CHECK (schema-wide)
Every EXPECTED entry declares its predicate P and its falsifier F.
Assert mechanically that F == NOT P over the same domain.
If F is narrower than NOT P, print the gap region, and name the state
UNMET_UNFALSIFIED when a row lands in it.
Apply retroactively to all EXPECTED blocks A-1..A-3; report any
mismatches as claims.

## 3. COUNT WORDS CARRY UNITS
In any prediction, a numeral must name its unit (gates | positions |
rows | cells). An unlabelled count is a lint failure on the EXPECTED
commit.

## 4. NULL SEMANTICS — schema-wide rule, supersedes per-field fixes
No nullable field may use None/empty for two meanings. Every such field
takes an explicit pair:
  NONE          = recorded as absent
  NOT_RECORDED  = not yet determined
Apply to: revocable_by, access_is_right, t_from, t_to (add OPEN_ENDED as
distinct from NOT_RECORDED), trigger_condition, gate_instrument, and
obligation_origin (map UNDECIDED -> NOT_RECORDED; keep NONE).
Report every field migrated and every row whose meaning changed.

## 5. E-A3-3 REPAIR
Instrument disjointness is computed over NON_MARKET gates only. A
market purchase is not an "instrument gating both directions."
Record the unrepaired literal result beside it (A-2 precedent).

## 6. FALSIFIERS REQUIRING ABSENCE
Tag every falsifier that can only fire on a sourced ABSENCE
(clothing RETAIN, TX rainwater) as ABSENCE_BOUND.
An ABSENCE_BOUND falsifier that has not fired is reported as
NOT_TESTABLE_AS_POSED. It is never counted as silent.
Add a clothing RETAIN fixture row: gate_kind TOKEN_PURCHASE only,
grade K, ABSENCE_BOUND.

## 7. COVERAGE IS REPORTED, NOT HIDDEN
Every hold prints cells_covered / cells_total (the 6/50 form) beside
its result.

## 8. EXPECTED (Claude's)
E-A3.1-1  Section 2 finds at least one mismatch in A-1..A-3 besides
          E-A3-2a. Falsifier: zero mismatches found.
E-A3.1-2  Section 4 changes the reading of at least one existing row.
          Falsifier: zero rows change meaning.
