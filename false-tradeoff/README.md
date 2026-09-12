# false-tradeoff

Diagnostic for apparent dilemmas. Tests whether a stated tradeoff is **real
or manufactured** by the option set and the accounting boundary.

CC0. Python 3, stdlib only. No network. Phone-buildable.
`python3 false_tradeoff.py` for the case table, `python3 test_tradeoff.py`
for the checks.

---

## MEASURAND

Given a problem stated as a tradeoff between side A and side B: **is the
tradeoff a property of the system, or an artifact of how the problem was
posed?**

**The instrument does not resolve tradeoffs. It classifies them.**

Nothing here weights, ranks, prefers or recommends a side. The structural
guarantee is stronger than the promise: swapping A and B leaves the flag set
identical, asserted over every case.

---

## THE FOUR CHECKS

```
                      the dilemma as posed
                               |
     +----------+--------------+--------------+------------+
     |          |                             |            |
  CHECK 1    CHECK 2                       CHECK 3      CHECK 4
 provenance  branch back                   boundary     horizon
     |          |                             |            |
  who handed  what eliminated            who is inside  when does the
  you the     the unlisted                 whose         saving come
  options?    options?                     ledger?         back?
     |          |                             |            |
 STIPULATED   RULE_BOUND               BOUNDARY_ARTIFACT  DEFERRAL_ARTIFACT
 _OPTION_SET
```

| | check | fires when | the case it is for |
|---|---|---|---|
| 1 | option set provenance | every option STIPULATED, none OBSERVED | trolley: difficulty is in the stipulation |
| 2 | branch back | every eliminating constraint is of kind RULE | a dilemma that holds only while the rules do |
| 3 | boundary cut | an entity **both sides depend on** is in one ledger and not the other | the cut runs through one system |
| 4 | horizon / deferral | horizons differ AND the saving lands past its own horizon, inside its own boundary | skipped upkeep is relocation, not saving |

**Flags are a SET.** Multiple fire. No priority ordering, no winner, no
collapse to a single verdict, no confidence score.

---

## WHAT IS SUPPLIED, NOT INFERRED

```
DILEMMA
  statement      carried as a label. read by NOTHING.  <- asserted over the AST
  options[]      label + provenance OBSERVED|STIPULATED|DERIVED + source
  sides          A, B
  constraints[]  kind PHYSICAL|RULE|UNSTATED + text
  boundary_A/B   entities in each ledger
  depends_A/B    entities each side depends on        <- [CHOICE 3], see below
  horizon_A/B    amount + unit                        <- [CHOICE 1], see below
  deferred_costs side + entity + time                 <- [CHOICE 2], see below
  conserved_quantity                                   reported, gates nothing
```

No prose is parsed into structure. A field not supplied is `None`, the check
that reads it returns `NOT_EVALUABLE`, and `INSUFFICIENT` joins the flag set.

**An unrunnable check never reports a silent pass.** A check that could not
run and a check that ran and found nothing are different results, and only
one of them is evidence.

---

## PASS CONDITION — case G

`GENUINE_TRADEOFF` must be reachable and must fire on case G alone.

```
CASE G   one reservoir, two draws
         - one conserved quantity between two uses
         - horizon_A == horizon_B
         - both uses inside the same declared boundary
         - the eliminating constraint is kind PHYSICAL
         - no return path from either use to the other in the horizon

PASS iff   read(G).flags == {GENUINE_TRADEOFF}
           AND G really is that case, asserted field by field
           AND some other case returns something else
```

**An instrument that dissolves every dilemma is not a diagnostic. It is a
preference dressed as a method.** Both outcomes occur on the shipped set and
the test asserts it, so the pass condition cannot be met by an instrument
that only ever finds artifacts.

---

## THREE PLACES THE ORDER'S MACHINERY DOES NOT REACH ITS OWN WORDS

Each is demonstrated in code, not argued, and none is repaired by widening
the enum.

**1. An UNSTATED constraint is a defect with no member to return it.**
§3 calls it a defect that must be reported and not smoothed over. The return
enum has six members and none says so. It is reported in the record, and a
caller reading only the flag set never sees it.

```
CASE U   one PHYSICAL constraint, one UNSTATED
         -> flags {GENUINE_TRADEOFF}, defects 1
```

**2. CHECK 3 reads an input the intake does not supply.**
It compares the *dependency set* of both sides; §2 lists only the ledger
boundaries. Read the boundary as the dependency set and every shared entity
is inside both by construction, so the exclusive test is false for all of
them and the check can never fire at any input.

```
boundary_as_dependency_is_silent()  ->  ever_fired 0 of 4 trials
```

The dependency set is therefore a separate declared field, and an absent one
is `NOT_EVALUABLE`.

**3. GENUINE_TRADEOFF's own definition names a condition no check tests.**
§4 defines it as *conserved quantity, same horizon, boundary intact*. Same
horizon is CHECK 4 and boundary intact is CHECK 3; the conserved quantity is
tested by nothing. It is not added as a fifth gate, because a dilemma
failing it would have no member to return. The field is carried and
reported.

```
CASE U   names no conserved quantity   ->  {GENUINE_TRADEOFF}
```

---

## FOUND BY RUNNING

Running the module as a script bound it as `__main__` while `cases.py`
imported it by name, building **two copies of every Enum**, so every
identity comparison in CHECK 1 and CHECK 2 read False and both went silent.
Four of nine cases read `GENUINE_TRADEOFF` — the direction §5 warns about,
arriving as a defect rather than a bias.

Repaired at the entry point and pinned by running that path in a
subprocess, in both directions.

---

## WHAT IS REFUSED

```
- no valuation. nothing weights, ranks or prefers a side.
  checked two ways: an AST scan of both code files for valuation-named
  identifiers and dict keys, null-tested on a plant; and swap invariance,
  asserted case by case, which is the mechanical content of the rule.
- no prose parsing. no check reads the statement string, asserted over the
  AST of all four check functions.
- an UNSTATED constraint is never treated as an absent constraint.
- no confidence score. flags fire or they do not.
```

---

## PARAMETERS

Declared, printed in every record, and carrying no basis beyond the table.

```
[CHOICE 1]  horizons as amount + unit, compared in days
            day 1 / week 7 / month 30.4375 / quarter 91.3125 / year 365.25
            an unregistered unit raises rather than defaulting
[CHOICE 2]  a deferred cost declares WHEN it lands and on WHICH entity
[CHOICE 3]  the dependency set is a field of its own, not the boundary
```

---

## STATE

Nine hand-built cases, all CONSTRUCTED, no real organisation, incident or
person named anywhere. Nothing has been run against a real decision; the
case set exercises the instrument and measures nothing. Expected flag sets
live in the test file, not in `cases.py`, so no case can agree with the
instrument by construction. The check count is printed by
`python3 test_tradeoff.py`.

---

## FILES

```
false_tradeoff.py   the four checks + DECLARATION
cases.py            9 hand-built dilemmas, structure only
test_tradeoff.py    the checks, stdlib only, no pytest
samples/            one pinned run
CLAIM_TABLE.md      FT_001..FT_013 with falsifiers
WORK_ORDER.md       delivered verbatim
```
