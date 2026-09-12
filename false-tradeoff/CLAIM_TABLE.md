# CLAIM_TABLE — false-tradeoff

Claims are about the INSTRUMENT. Nothing here is a claim about any real
decision, and no case in `cases.py` is a report of one.

`FT_*` ids are permanent. A refuted claim is updated; the checks are not
retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| FT_001 | case G returns GENUINE_TRADEOFF alone, and G is the case §5 specifies | SUPPORTED |
| FT_002 | the instrument does not dissolve every dilemma | SUPPORTED |
| FT_003 | nothing ranks, weights or prefers a side | SUPPORTED, two ways |
| FT_004 | no check reads the statement string | SUPPORTED |
| FT_005 | all six returns are reachable, one case each | SUPPORTED |
| FT_006 | an unrunnable check never reports a silent pass | SUPPORTED |
| FT_007 | an UNSTATED constraint is a defect with no member to return it | FINDING |
| FT_008 | CHECK 3 reads an input §2 does not supply, and the boundary reading makes it silent at every input | FINDING |
| FT_009 | GENUINE_TRADEOFF's own definition names a condition no check tests | FINDING |
| FT_010 | CHECK 1's two clauses are not independent | FINDING |
| FT_011 | the entry point silenced two checks toward GENUINE; found by running | REPAIRED |
| FT_013 | INSUFFICIENT joins the flag set rather than replacing it; the exclusive reading stays recoverable | DECIDED |
| FT_012 | nothing has been run against a real decision | UNVERIFIED |

---

## FT_001 — the critical falsifier

`read(CASE_G)` returns exactly `{GENUINE_TRADEOFF}`. The test asserts the
case is the one §5 describes rather than a lookalike: `horizon_a.days() ==
horizon_b.days()`, `boundary_a == boundary_b`, at least one eliminating
constraint of kind `PHYSICAL`, and a named conserved quantity.

`GENUINE_TRADEOFF` is also asserted never to co-fire with another flag and
never to co-fire with `INSUFFICIENT`.

**Falsified if** case G returns any other set, or if the flag can be reached
on an intake where a check could not run.

---

## FT_002 — it does not dissolve every dilemma

Both outcomes occur on the shipped set: some case returns
`{GENUINE_TRADEOFF}` and some case returns something else, asserted in one
check. Without it, FT_001 could be satisfied by an instrument that returns
GENUINE for everything.

**Falsified if** a case set can be built on which no flag other than
`GENUINE_TRADEOFF` ever fires, or on which `GENUINE_TRADEOFF` never fires.

**Known limit:** this shows both branches are live on nine authored cases.
It does not establish that the split falls in the right place on a real
dilemma, which is FT_012.

---

## FT_003 — no valuation

Two independent checks, because a name scan alone is weak.

1. **AST scan** of `false_tradeoff.py` and `cases.py` for valuation-named
   identifiers and dict-literal keys, split on `_` and camelCase so
   `side_score` fires and `betterment_note` does not. Comments and free
   docstrings are excluded deliberately: the module and README have to be
   able to NAME what they refuse, and a substring scan fires on the sentence
   saying so. Null-tested on a plant.
2. **Swap invariance.** `swap_sides()` exchanges A and B in every field, and
   the flag set is asserted identical, case by case. This is the mechanical
   content of the rule: an instrument with any preference between the sides
   cannot be symmetric under exchange.

**Falsified if** a case is exhibited whose flag set moves under swap, or if
any returned flag is not a `TradeoffRead` member.

**Known limit:** the token list is stepped around by paraphrase. A field
named `side_a_score` fires; one named `s1` does not. Swap invariance is the
check that does not depend on naming.

---

## FT_004 — no prose parsing

`statement` is carried and read by nothing: the test walks the AST of all
four check functions and asserts no attribute access to `statement` appears
in any of them.

**Falsified if** any check branches on the statement text.

---

## FT_005 — every return reachable

Six members, nine cases, each member produced by at least one. A declared
member that no path populates cannot be told from a member nobody looked for.

**Falsified if** a member becomes unreachable. Note the weaker form this
leaves open: the cases were written to reach them, so this shows no path is
dead and does not show the boundaries between them fall in the right place.

---

## FT_006 — absent is not clean

A check missing an input returns `NOT_EVALUABLE` with the field named,
`fired` stays False, `INSUFFICIENT` joins the set, and `GENUINE_TRADEOFF`
cannot. A constraint list that is **absent** (`None`) and one that is
**empty** (`[]`) are separate states: the first is NOT_EVALUABLE, the second
is evaluable and silent.

That second distinction is load-bearing. `all([])` is True, so the
unguarded CHECK 2 rule would report a dilemma held by no stated constraint
as one held entirely by permission. The guard is asserted in both
directions, so it is not silencing the real case.

**Falsified if** any path lets an unrunnable check contribute to a
`GENUINE_TRADEOFF` reading.

---

## FT_007 — the defect with no member

§3 says an UNSTATED constraint "is a defect and must be reported, not
smoothed over". The return enum has six members and none of them says so,
and §6's case T confirms it is not a flag, since T's expected set is
`{STIPULATED_OPTION_SET}` alone while its constraints are UNSTATED.

It is reported in the record as `unstated_constraint_defects` and printed
in the render. **Case U is the demonstration**: one PHYSICAL constraint and
one UNSTATED, everything else clean, returning `{GENUINE_TRADEOFF}` with a
defect recorded — the smoothing §3 forbids, occurring in the return value
rather than in the record.

**Not repaired by widening the enum**, because the order fixes it.

**Closed by** either a seventh member or an explicit statement that the
defect channel is the record. The choice is the author's.

---

## FT_008 — CHECK 3 reads an input the intake does not supply

§3 CHECK 3 compares "the dependency set of BOTH sides". §2 lists
`boundary_A` and `boundary_B` and no dependency set.

Reading the boundary as the dependency set is not a workaround, it is
fatal: `shared` becomes `boundary_A & boundary_B`, so every shared entity is
inside both by construction and the exclusive test is false for all of them.
`boundary_as_dependency_is_silent()` runs it over four trials and the check
fires **0 times** — silent at every input, which is a `CONSTANT_SILENT`
detector.

`depends_a` / `depends_b` are therefore separate declared fields
(`[CHOICE 3]`), absent ones are `NOT_EVALUABLE`, and the check is shown to
fire with them present (case B, the cut running through `crew`).

**Falsified if** an input is exhibited on which CHECK 3 fires while the
dependency set is read as the boundary.

---

## FT_009 — the conserved quantity gates nothing

§4 defines `GENUINE_TRADEOFF` as "conserved quantity, same horizon, boundary
intact". Same horizon is CHECK 4 and boundary intact is CHECK 3. **The
conserved quantity is tested by no check.**

It is not added as a fifth gate, because a dilemma failing it would then
have no member to return: the enum has six and none says "not conserved".
The field is carried and reported, and `check_conserved_is_not_gated()`
states the reason in the module.

Case U names no conserved quantity and returns `{GENUINE_TRADEOFF}`.

**Closed by** a seventh member, or by a statement that the four checks are
the whole definition and §4's prose is a description of the usual case.

---

## FT_010 — CHECK 1's two clauses are not independent

"every option is STIPULATED **and** no OBSERVED option exists": the first
entails the second, so the conjunction is redundant on the literal reading.
The second clause carries information only on a set with no OBSERVED option
that is not all-STIPULATED, which the rule as written does **not** fire on.

Case P is that set: two STIPULATED and one DERIVED. No option was observed,
and the check is silent. Both states are in the record
(`all_stipulated`, `no_observed_option`, `provenance_counts`) so the reading
is visible without the rule being changed.

**Falsified if** a reading of CHECK 1 is stated under which the second
clause does work that the first does not.

---

## FT_011 — the entry point silenced two checks

Found by running, not by reading. `python3 false_tradeoff.py` bound the
module as `__main__` while `cases.py` imported it as `false_tradeoff`,
building **two copies of every Enum**. A member of one copy is not the
member of the other, so every `is` comparison in CHECK 1 and CHECK 2 read
False and both checks went silent.

Four of nine cases read `GENUINE_TRADEOFF`, including the trolley. The
direction matters: the failure runs toward the reading §5 warns about, so an
instrument built to dissolve dilemmas and one with this defect print the
same table.

Repaired by importing the module by name in the script path, and pinned by
running that path in a subprocess and asserting case T reports
`STIPULATED_OPTION_SET` and does not report `GENUINE`.

**Falsified if** the script path and the imported path ever disagree again.

---

## FT_013 — INSUFFICIENT joins the read, it does not replace it

[CHOICE 4]. §2 says an unsupplied field degrades the read to
`INSUFFICIENT`; §4 says several flags may fire and the return is the set.
Read together these give two rules, and they disagree on a dilemma where one
check ran and another could not.

The exclusive reading discards a check that ran because a different one was
not supplied, which loses a measurement that was taken. So `INSUFFICIENT`
joins the set: case T with its dependency sets removed returns
`{STIPULATED_OPTION_SET, INSUFFICIENT}` rather than `{INSUFFICIENT}` alone.

Nothing is lost by the choice, because the exclusive reading is recoverable
from the same record — `intake_missing` is empty exactly when every check
ran, so a caller wanting the strict rule reads that field instead of the
flag set. Both directions are pinned.

**Falsified if** a caller is shown for whom a flag that fired alongside
`INSUFFICIENT` is misleading in a way `intake_missing` does not correct.

---

## FT_012 — nothing has been run

Nine constructed dilemmas exercise the instrument and measure nothing. No
real decision has been read, no boundary or dependency set has been taken
from a real ledger, and no horizon has been read off a real accounting
window.

The order's own falsifier is a property of the code and is met. Whether the
four checks separate posed dilemmas from structural ones is untouched in
both directions.

**Closed by** one real dilemma whose intake is supplied by someone who
holds the record, with the flags read afterwards rather than before.
