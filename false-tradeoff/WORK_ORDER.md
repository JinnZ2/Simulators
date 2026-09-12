# WORK ORDER — `false_tradeoff.py`

Diagnostic for apparent dilemmas. Tests whether a stated tradeoff is real
or manufactured by the option set and the accounting boundary.

CC0. Python 3, stdlib only. No network. Phone-buildable.

---

## 1. MEASURAND

Given a problem stated as a tradeoff between side A and side B, determine
whether the tradeoff is a property of the system or an artifact of how
the problem was posed.

The instrument does **not** resolve tradeoffs. It classifies them.

---

## 2. INTAKE

```
DILEMMA
  statement          : str
  options[]          : each with
                         label
                         provenance : OBSERVED | STIPULATED | DERIVED
                         source     : who supplied it
  sides              : A, B  (the two things said to trade off)
  constraints[]      : each eliminating some unlisted option
                         kind : PHYSICAL | RULE | UNSTATED
                         text
  boundary_A         : entities/costs inside A's ledger
  boundary_B         : entities/costs inside B's ledger
  horizon_A          : time window over which A is accounted
  horizon_B          : time window over which B is accounted
```

Nothing is inferred from the statement string. If a field is not
supplied it is `None`, and the read degrades to `INSUFFICIENT`. No
parsing of prose into structure.

---

## 3. THE FOUR CHECKS

```
CHECK 1 — OPTION SET PROVENANCE
  if every option is STIPULATED and no OBSERVED option exists:
      the option set was handed over, not found.
      flag STIPULATED_OPTION_SET.
  the trolley case. difficulty comes from the stipulation.

CHECK 2 — BRANCH BACK
  for each constraint eliminating an unlisted option, type it:
    PHYSICAL  - material/conservation limit. holds.
    RULE      - permission-layer limit. holds only while the rule does.
    UNSTATED  - no constraint given; the option was dropped silently.
  any UNSTATED constraint is a defect and must be reported, not
  smoothed over.
  a dilemma whose constraints are ALL of kind RULE is not a dilemma
  about the world.

CHECK 3 — BOUNDARY CUT
  compute shared = entities appearing in the dependency set of BOTH
  sides.
  for each e in shared:
      if e is inside boundary_A and outside boundary_B (or reverse):
          the cut runs THROUGH one system.
          flag BOUNDARY_ARTIFACT.
  cost to A that lands on an entity also inside B is not a transfer.
  it is internal.

CHECK 4 — HORIZON / DEFERRAL
  if horizon_A != horizon_B:
      test whether A's saving reappears as a cost inside A's own
      boundary beyond horizon_A.
      if yes: flag DEFERRAL_ARTIFACT.
  the maintenance case. skipped upkeep is not a saving, it is a
  relocation past the accounting window.
```

---

## 4. RETURN ENUM

```python
class TradeoffRead(Enum):
    STIPULATED_OPTION_SET  # options handed over; branch-back not done
    RULE_BOUND             # all eliminating constraints are permission-layer
    BOUNDARY_ARTIFACT      # accounting cut runs through one system
    DEFERRAL_ARTIFACT      # cost relocated past the accounting horizon
    GENUINE_TRADEOFF       # conserved quantity, same horizon, boundary intact
    INSUFFICIENT           # intake incomplete; no read
```

Multiple flags may fire. Return the **set**, not a winner. No priority
ordering, no collapse to a single verdict.

---

## 5. THE CRITICAL FALSIFIER

`GENUINE_TRADEOFF` must be reachable and must fire on the case below.

```
An instrument that dissolves every dilemma is not a diagnostic.
It is a preference dressed as a method.
```

Required passing case:

```
G. a conserved quantity allocated between two uses
   - same time window (horizon_A == horizon_B)
   - both uses inside the same declared boundary
   - the constraint eliminating other options is kind PHYSICAL
   - no return path from either use to the other within the horizon
   -> GENUINE_TRADEOFF, and no other flag
```

If the implementation cannot produce this cleanly, it has been built
to reach a conclusion.

---

## 6. WORKING NULL — hand-built cases

`cases.py`, minimum 6, one per enum member. These four are required:

```
T. trolley: two options, both STIPULATED, no OBSERVED option,
   constraints eliminating the third branch are UNSTATED
   -> {STIPULATED_OPTION_SET}

M. deferred maintenance: horizon_A one quarter, horizon_B ten years,
   the skipped upkeep reappears as failure inside A's own boundary
   -> {DEFERRAL_ARTIFACT}

B. cost-vs-safety where the failure lands on an entity inside both
   ledgers -> {BOUNDARY_ARTIFACT}

G. as section 5 -> {GENUINE_TRADEOFF}
```

---

## 7. DECLARATION BLOCK

```python
DECLARATION = {
    "measurand": "whether a stated tradeoff is structural or posed",
    "axes": ["option_provenance", "constraint_kind",
             "boundary_overlap", "horizon_mismatch"],
    "returns": [m.name for m in TradeoffRead],
    "resolves_tradeoffs": False,
    "scalar_collapse": False,
    "unknown_states": ["INSUFFICIENT"],
}
```

---

## 8. DELIVERABLES

```
false_tradeoff.py   checks + DECLARATION
cases.py            >=6 hand-built, one per enum member
test_tradeoff.py    every member reachable
                    case G returns GENUINE_TRADEOFF alone
                    no function ranks, scores, or weights a side
README.md           the four checks, and case G stated as the
                    pass condition
```

---

## 9. OUT OF SCOPE

```
- no valuation. nothing may weight, rank, or prefer side A over B.
  a function that says which side should win is out of spec.
- no prose parsing. structure is supplied, never inferred.
- do not treat UNSTATED constraints as absent constraints.
  report them; they are the finding.
- do not add a confidence score. flags fire or they do not.
```
