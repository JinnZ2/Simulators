# CLAIM TABLE -- move set, second order

Claims `MSV_001..MSV_026`, about `move_set_sim_v2.py` and the second work
order. Distinct prefix from `MV_*`, which is about the delivered v1 and is
not restated here. `WORK_ORDER_V2.md` is landed verbatim and not edited.

REFUTATION_PROTOCOL: a claim that fails is updated. The harness is not
retuned to preserve it. Every claim below is a property of the code or of
one delivered artifact, recomputable by anyone with the clone.

---

## MSV_001 -- the ordered filename is taken

**Status: SUPPORTED.**

The order says `BUILD: move_set_sim.py`. That name holds a DELIVERED
artifact in this folder, landed verbatim in an earlier drop and never
edited. The build lands as `move_set_sim_v2.py` beside it, under the
repo's supersession convention (`observer-exclusion/SPEC_V2`,
`design-basis-ai/SOURCE_DROP_V2`, `failure-mode-register` x4) -- both
inspectable, neither overwritten.

Falsifier: `git diff` shows a change to `move_set_sim.py`.

---

## MSV_002 -- the order's M6 and the delivered M6 are different moves

**Status: SUPPORTED. Both readings built (CHOICE 1).**

The order's sixth line is *"refuse to score what cannot be seen; make the
absence a first-class value"*. That is a statement about the RETURN --
what the reader does with an unreachable question -- and the order's own
OUTPUT section states it again for every move (`or ABSENT(reason)`,
*"ABSENT is a valid output, not an error"*).

The delivered `move_set_sim.py` resolved the same word the other way:
its `M6_absence` family (six sub-moves, split in the second v1 drop) is
about absences IN THE ARTIFACT -- sequence gaps, unaccounted intervals,
negative space. That is a move with a trigger. It is not the same thing.

Not exclusive, so both are built: `M6_absence_first_class` has its own
artifact-side trigger (a quantity the artifact invites and supplies no
operands for), AND every one of the six moves admits an `ABSENT` return.
Checked: `all("ABSENT" in v["kinds"] for v in MOVES.values())`.

Falsifier: a reading of the order under which the two are one move.

---

## MSV_003 -- the guard v1 says everything rests on now holds

**Status: SUPPORTED, null-tested in both directions.**

`MV_002` recorded that v1's docstring names its own load-bearing guard --
*"a bare 'I don't know' is not a refusal and scores zero. This is the only
thing keeping symmetric scoring from being gameable"* -- and that the
implementation checks two strings are non-empty, so a ledger carrying
`"x"` in every blocker and unblocker scored 6.0 of 6.0, identical to the
delivered run.

The same shape here scores **0.0 of 6.0**, every row
`UNVERIFIED_NO_SPAN` with a stated reason (suite 2.1-2.3). And an honest
all-absence ledger over the same artifact scores **6.0 of 6.0** (2.4), so
this is not a module that refuses everything.

The repair is `adaptive-claim-loop` `ACL_012`/`ACL_017`: a guard that asks
for PROSE can be satisfied with prose. Every entry here is checked against
the artifact -- a line that must exist, a value that must sit at cited
columns, an arithmetic that must reproduce, a token that must be absent
from a declared span.

Falsifier: a ledger scoring above zero without any field resolving into
the artifact.

---

## MSV_004 -- what `tools/sourced.py` does not do, and the layer added

**Status: SUPPORTED.**

`tools/sourced.py` is IMPORTED, not reimplemented (the `MF_019`
discipline). Suite 14.1-14.5: no local `gate`, no local `Locator`,
`S.gate` actually called, `S.slice_sourced` used and `find_span` absent --
the span is emitted by the extraction, never searched for after the fact.

That module states its own limit: it checks the three fields are mutually
consistent, *not that the source is true*. A `Sourced` with
`source_text="x"`, `value="x"`, `span=(0,1)` passes its gate, because the
source text is supplied by the caller.

`bind_quote()` is the missing layer: the locator's line number is resolved
INTO THE ARTIFACT, the cited source text must BE that line, and the value
is sliced OUT of it. The ledger says WHERE; the artifact supplies WHAT. A
ledger cannot state a value the artifact does not carry at the place it
cites (suite 3.1-3.9).

Falsifier: a `BOUND` verdict on an entry whose value is not in the
artifact.

---

## MSV_005 -- M4 perturbs the arithmetic, and the perturbation is the rounding

**Status: SUPPORTED, and NARROWED against the first build.**

A published artifact cannot be perturbed. Its arithmetic can: recompute a
stated relationship from operands the artifact itself supplies.

The first build did this at a POINT and gated on whether the ledger's
`holds` declaration matched. That is the defect `MSV_017` records. The
gate is now on a BAND: shipped precision parsed from each operand as
written, propagated through the operation, and the stated value tested
for containment.

Three verdicts, and the shape of the set is the narrowing:

| stated value | ledger says | verdict |
| --- | --- | --- |
| inside the band | `holds: false` | `NOT_EVALUABLE` |
| inside the band | `holds: true` | `NOT_EVALUABLE` |
| outside the band | `holds: false` | `ARITHMETIC_AS_DECLARED` (1.0) |
| outside the band | `holds: true` | `ARITHMETIC_NOT_AS_DECLARED` (0.0) |

`ARITHMETIC_AS_DECLARED` is reachable only from `holds: false`. See
`MSV_019`. Suite 4.9-4.17.

Falsifier: a stated relationship whose stated value lies outside the band
its own shipped operands span and which this scores `NOT_EVALUABLE`.

---

## MSV_006 -- the demo's M4 finding

**Status: VOID. The finding does not stand.**

It read: line 23 states the AB-Poisson baseline as **0.021**, the report
ships AB 1.889 (line 15) and Poisson 1.911 (line 17), recomputed the gap
is 0.022, a discrepancy in the third decimal on the denominator the
headline *"~15x larger"* ratio is taken over.

Both operands are written to three decimal places. At that precision:

```
AB       1.889  ->  [1.8885, 1.8895]
Poisson  1.911  ->  [1.9105, 1.9115]
|diff|          ->  [0.0210, 0.0230]
```

0.021 is inside. The artifact is self-consistent at the precision it
shipped, and the 0.022 was the rounding, not a discrepancy. The move now
returns `NOT_EVALUABLE` on this entry with the reason *"stated value
within shipped precision"*, and scores 0.

The entry is KEPT in the demo ledger, still declaring `holds: false`, so
the refusal comes from the band and not from the declaration being
changed after the fact.

What was never claimed and is still not: whether 0.021 is the right
baseline at all. `AOS_009` holds it is the smallest of three pairwise
gaps and the honest ratio is nearer 4.5x. That is a reading, and
consistency at shipped precision says nothing about it.

Reported from outside this build. Recorded rather than quietly repaired,
because the claim was published.

---

## MSV_007 -- the demo's M6 finding

**Status: SUPPORTED.**

Line 41 reports a peak/floor ratio of 5537 (AB) and 190 (Cascade). The
floor is on line 40. **The peak height is nowhere in the artifact** --
`peak height`, `peak amplitude` and `S(k) max` return zero hits across all
92 lines.

So the ratio is an asserted value, not one a reader can recompute. Of the
four stated relationships in the document, three recompute from operands
it supplies (`|D_f(AB) - D_f(Cascade)| = 0.334`,
`|alpha_AB - alpha_C| = 1.460`, `0.0812/0.0015 = 54.1`) and this one does
not, because its operands were not published.

Not zero and not unknown. That is the move's whole subject.

Falsifier: a peak height anywhere in the artifact.

---

## MSV_008 -- `MV_004` repaired

**Status: SUPPORTED.**

v1's `path_dependence` compared finding sets across runs -- order-invariant
and correct -- and checked nothing about the ORDERS the runs used, so two
byte-identical ledgers returned `ORDERLESS -- claim holds`. And the
precondition was not merely unchecked: `emit()` returned an `order` key
and the `ledger_schema` it shipped in the same dict had no field for it.

Here `order` is a REQUIRED ledger field, `read_ledger` refuses a ledger
without one and names `MV_004` in the refusal (suite 9.1-9.2), and
`path_dependence` returns `NOT_EVALUABLE` -- a third state, not a pass --
for fewer than two runs, for zero runs, and for runs that do not declare
distinct orders (8.1-8.3). `ORDERLESS` and `CHAIN DETECTED` are both
reachable on distinct orders (8.4-8.5).

Falsifier: a `claim holds` verdict from two runs that used one order.

---

## MSV_009 -- `MV_005` does not recur: no verdict scores zero for a clean read

**Status: SUPPORTED.**

v1 carried `NO_FINDING`, scoring 0 -- so on the one move that runs on
every artifact, *"I looked and nothing is hidden here"* was the single
outcome that cost a point, under a rule about symmetric scoring. A
gradient toward reporting something.

There is no `NO_FINDING` verdict here. A clean read is a `QUOTE` citing
the thing that checks out, and it scores 1.0 like any other bound
finding. A verified absence is a finding, not the lack of one.

Falsifier: an honest reading of an artifact with no way to score under
this verdict set.

---

## MSV_010 -- coverage is reported and never folded in, and that is a limit

**Status: SUPPORTED. The limit is stated, not repaired.**

A verified absence over 3% of an artifact and one over 100% both score
1.0. `coverage` -- distinct lines searched over total, overlaps counted
once (CHOICE 4) -- is printed beside each one and enters no arithmetic
(CHOICE 6, suite 6.7, 7.5). Registered in `tools/known_answer.py` with six
cases; the overlap case is the detector (summing range lengths returns 1.0
for two copies of one half) and the empty case is where a zero hides (an
undeclared span is no measurement, not zero coverage).

The limit: nothing here tells a well-chosen narrow span from a
cherry-picked one. Suite 5.11 demonstrates the mechanism directly -- the
same token verifies absent over lines 1-5 and is refuted over 1-92.
Folding coverage into the score would make one number out of two
quantities (`domain-ledger` `DL_001`), so the number is published beside
the verdict and the reader does the work.

Falsifier: a rule that separates the two without collapsing them.

---

## MSV_011 -- the demo ledger is not blind, and says so

**Status: UNVERIFIED as a capability measurement, by construction.**

`ledgers/sim_stack_report.json` was authored by the same session that
wrote the harness, and this repo already carries `AOS_001..AOS_010`
auditing the same artifact. `--demo` prints a contamination block BEFORE
the numbers naming both facts and `frame-location-benchmark` `FLB_010`:
a self-run is void as a capability score, because the runner holds the
key.

What is scored is the mechanical layer only -- a line that exists, a value
at cited columns, an arithmetic that reproduces, a token absent from a
declared span. Each is recomputable by a reader with the artifact and no
other context. No reading is scored.

Falsifier: a ledger written against this artifact by a party who did not
write the harness.

---

## MSV_012 -- the sought-token search is a word list, and it is named as one

**Status: SUPPORTED.**

An absence verified against three tokens is the absence of THOSE TOKENS.
`T1-1`/`UNI_009` one level over: any paraphrase steps around it. The demo
states it at the point of use -- M5's confidence field reads
*"'control' is one word for the thing"* -- rather than in a caveat at the
end.

This is why the verdict is `VERIFIED_ABSENCE` and not `ABSENT`: the claim
is about a token and a span, both stated, and a reader who disagrees with
the token list can say so without re-running anything.

Falsifier: a sought-token list whose paraphrase is present in the span.

---

## MSV_013 -- two defects in this build, both found by running

**Status: SUPPORTED. Recorded rather than quietly fixed.**

(1) The `tools/known_answer.py` registration landed **after a `finally`
block inside `_msv_coverage`** -- dead code, never executed, leaving the
registry one metric short while everything that did register still passed.
That is the SECOND instance of that exact shape in this registry;
`FMR_036` recorded the first, and `tools/sourced.registry_complete` exists
because of it. Caught by `completeness()` reporting 24 registered against
25 expected.

(2) The patch adding the metric id to `EXPECTED_METRICS` matched its
anchor string a second time INSIDE an unrelated `register()` call in
`seed()`, inserting a stray element into the `lag_of_peak` registration.
A substring replace on a string that occurs twice.

Neither was found by reading. Both were found by running
`python3 tools/known_answer.py`.

Falsifier: `metrics registered: 25   expected: 25   COMPLETE` failing.

---

## MSV_014 -- the moves are not disjoint, and enforcing disjointness would cost more

**Status: SUPPORTED. Recorded, not repaired.**

On the demo, M4 and M6 reach the same place from two sides: M4 recomputes
what CAN be recomputed, M6 names what cannot. The peak/floor ratio is
M6's finding and is also an M4 `OPERAND_NOT_IN_ARTIFACT`.

Disjointness is not a property the order asks for. Enforcing it needs
cross-entry comparison, which is the dependency the move-set design exists
to remove -- v1's README states the same cost from the other side
(*"a cross-entry check reintroduces the dependency the design removes"*).

Falsifier: a pair of moves whose overlap produces a wrong verdict rather
than a duplicate one.

---

## MSV_015 -- the demo ledger uses two fields the schema does not declare

**Status: SUPPORTED.**

`ledgers/sim_stack_report.json` carries `note` at the top level and
`_says` on three entries. Neither is in the `ledger_schema` that `emit()`
ships, and `read_entry` ignores both. The `MF_017` shape -- a field in use
with no schema slot -- arriving in this build's own data file, inside one
session of it being written.

The ledger's `quote` fields are also verbatim artifact lines, and the
artifact is not ASCII (it carries `\u00b2` and `\u2192`). Suite 17.6
asserts everything AUTHORED in the ledger is ASCII; 17.7 asserts every
quote is a line of the artifact.

Kept rather than removed: `_says` is where a ledger states what its cited
line MEANS, which is the reading, and the reading is deliberately not
scored (`MSV_011`). What is missing is the schema saying so.

Falsifier: `emit()["ledger_schema"]` declaring both.

---

## MSV_016 -- nothing here is evidence about auditing

**Status: UNVERIFIED and it covers the folder.**

The six moves have never been run against any artifact by a party that did
not write the harness. One ledger exists, over one artifact, authored
here. Every claim above is a property of the code or of one delivered
document.

What is established: the order's scoring rule is built (a correctly
refused verdict scores 1.0 exactly as a bound one; absence is selectable
on every move, and is the whole subject of one), the guard v1 named and
did not have now holds, and the demo runs on a public artifact already in
this repo.

Falsifier: the move set run cold by someone else, on their own artifact,
with the ledger published.

---

## MSV_017 -- the defect is a false-positive generator, not a one-off

**Status: SUPPORTED, and the scope note is the larger half.**

Reported against the returned build, verbatim:

> DEFECT: M4 point-recomputes from rounded operands and scores the
> residual as a finding. [...] SCOPE: fires on any artifact shipping
> rounded operands. False-positive generator, not a one-off.

Both halves hold. The arithmetic is the user's and reproduces exactly
(`MSV_006`). The scope claim is structural: any artifact that rounds an
operand has not stated the recomputed quantity to better than the band
those roundings span, so a point test reports the rounding every time.
Difference-of-near-equal-numbers is the worst case, and it is the common
case in a results table.

The stipulated tolerance the first build used (relative 5e-3) was a
constant standing in for a quantity the document already carries. The
repair reads the quantity instead. This is the `reasoning-gate` **G-RES**
shape -- instrument resolution against the feature being measured -- with
the instrument being the artifact's own significant figures.

Falsifier: an artifact whose stated relationships fall outside their
shipped bands, on which a point test and a band test agree.

---

## MSV_018 -- M4 establishes nothing on the demo artifact, and that is the result

**Status: SUPPORTED, recomputable by anyone with the artifact.**

Every stated relationship in `SIM_STACK_REPORT.txt` falls inside its own
shipped band:

| stated | operands | band | inside |
| --- | --- | --- | --- |
| 0.334 | 1.889, 1.555 | [0.3330, 0.3350] | yes |
| 0.021 | 1.889, 1.911 | [0.0210, 0.0230] | yes |
| 1.460 | -1.529, -0.069 | [1.4590, 1.4610] | yes |
| 54.1 | 0.0812, 0.0015 | [52.3548, 56.0345] | yes |

Four of four. Not an accident of the values: every operand in this
document is three or four significant figures, and every stated
relationship is a difference of near-equal numbers or a ratio of small
ones -- the two operations that lose the most precision.

So the demo now carries ONE recomputable finding (M6, the peak/floor
ratio 5537, which ships no operands at all -- `MSV_007`) where it
previously reported two. Total falls 6.0 -> 5.0.

The fall is the instrument working. A harness that scored higher before
the repair was scoring a rounding.

Falsifier: any stated relationship in this artifact whose value falls
outside the band its own operands span.

---

## MSV_019 -- holds=True is now unearnable, and that is correct

**Status: SUPPORTED, and it is a narrowing worth stating.**

There is no input for which `bind_derived` returns
`ARITHMETIC_AS_DECLARED` from a `holds: true` declaration. Inside the
band is `NOT_EVALUABLE`; outside it is `ARITHMETIC_NOT_AS_DECLARED`.
Asserted over the cross product of the artifact's own operand pairs and
four stated values (suite 4.15).

The reason is not an implementation limit. A band CONTAINING the stated
value is consistency, not confirmation -- it says the artifact did not
contradict itself at the precision it shipped, which is the weakest
possible statement and is true of almost every published table. M4
refutes or refuses. It does not confirm.

Cost, stated: a ledger that wants to record *"this arithmetic checks
out"* cannot earn a point for it. That is the right side to err on, since
the alternative is a move that scores a point for finding nothing.

Falsifier: a defensible reading under which a stated value inside its own
shipped band is evidence that the arithmetic holds.

---

## MSV_020 -- decimal, not float, and the boundary case is why

**Status: SUPPORTED, measured.**

The band on the demo pair is exactly `[0.0210, 0.0230]` and the stated
value is exactly `0.021`. In binary floating point the lower bound
computes as `0.02100000000000013`, so `band[0] <= stated` returns
**False** and the harness would have produced a finding on the case the
whole repair exists to refuse -- failing by 1.3e-16 on a quantity whose
smallest meaningful unit is 5e-4.

The alternatives were an epsilon or exact arithmetic. An epsilon is a
second stipulated constant replacing the one just retired, so
`decimal.Decimal` is used and the operands are parsed from the TEXT
rather than through a float (CHOICE 8). `sub`, `abs_sub` and `mul` are
then exact. `div` carries context rounding at 28 significant digits,
roughly 25 orders below any shipped precision, and that residual is not
special-cased.

Found by running the arithmetic before touching the file, not by reading
the code.

Falsifier: a boundary case this reports wrongly at 28 digits.

---

## MSV_021 -- CHOICE 3 is retired in place, not renumbered

**Status: SUPPORTED.**

`TOL = 5e-3` is gone (suite 4.25). Entry 3 of the choice list now reads
RETIRED and names what replaced it. Ids are permanent, so the entry stays
and the list still runs 1..10 with no gap and no reuse. The suite checks
that a retired choice is printed by `--choices` and cited by NOTHING in
the source (suite 16.2, 16.3) -- the inverse of the rule every live
choice is held to.

Falsifier: a renumbering, or a retired choice still taking effect
somewhere.

---

## MSV_022 -- the integer half-width is wrong for an exact count, and the error runs toward refusing

**Status: SUPPORTED, and it is a limit rather than a defect.**

An operand written with no decimal point takes half-width 0.5 (CHOICE 9).
That is the standard reading of a rounded number and it is wrong for an
exact count: *68 peaks* is 68, not 68 +/- 0.5. The schema carries no
field saying which a number is, and inferring it from the surrounding
text would be a word list deciding a measurement.

The direction is what makes it liveable. Too wide a band makes containment
MORE likely, which makes `NOT_EVALUABLE` more likely, which suppresses a
finding rather than manufacturing one. Every other choice here is set the
same way (CHOICE 10: the stated value is read as a point, not widened to
its own band, for the same reason).

Exponent form is refused outright rather than given a default width, since
the half-width there depends on the mantissa digits and the reading is not
one rule.

Falsifier: an artifact where an exact integer count is the operand and the
0.5 band suppresses a real discrepancy.

---

## MSV_023 -- provenance of the known-answer registry, reported and not repaired

**Status: REPORTED. Asked for by the same report that raised `MSV_017`,
explicitly as a report and not a fix.**

The question: who authored the answers in `tools/known_answer.py`, and
were they authored before or after the checks that verify them.

**Authorship.** 19 of the 20 commits touching the file are
`Claude <noreply@anthropic.com>`. The twentieth is a merge commit by the
repository owner carrying another branch's registrations, so it authors no
case. **Every registered expected value in the registry is model-authored,
by one author.** The metrics being checked are model-authored too. The
registry is therefore a single-author artifact checking single-author code
-- `effective-redundancy-audit`'s shared node, and the same shape
`triad-playground` `TP_003` measures: consensus is blind to the error its
members share.

**Ordering, measured rather than asserted.** For each metric, the earliest
commit introducing `def <fn>` in its module against the earliest commit
introducing its registration string:

| ordering | count |
| --- | --- |
| registered in the SAME commit as the implementation | 16 |
| implementation first, registered later | 8 |
| **answer registered BEFORE the implementation existed** | **0** |
| unknown (registered in this session, uncommitted at measurement) | 1 |

**The denominator, reconciled.** Two lists move and they move by
different amounts, so one number does not describe both:

| list | before `00646b1` | after | ids added |
| --- | --- | --- | --- |
| `tools/known_answer.py::EXPECTED_METRICS` | 25 | 26 | `_halfwidth` |
| `tests/test_known_answer_gate.py::MANIFEST` | 24 | 26 | `coverage`, `_halfwidth` |

`coverage` was **already registered** -- added earlier in this session
under `MSV_013`'s repair -- and had never been added to the test's
MANIFEST, so the commit closed a coverage gap on it rather than
registering it. `25 + 2 = 27` fails because the two ids did not land in
one list. The ordering table below counts the **25 committed** metrics at
the time of measurement; `_halfwidth` was the uncommitted 26th and is the
`unknown` row in it.

**Zero of 25.** Not one expected value in the registry was fixed before
the function it checks existed. The file's own docstring names the two
seeds as cases where *"a case whose answer was fixed in advance"* caught a
defect -- and both of those are `implementation first`, meaning the case
was written against a function that already ran.

**Scope limit on the 25/25 (now 26/26), stated plainly.** The headline
means: every registered case agrees with the current implementation, and
every expected value was authored by the same party that authored the
implementation, with knowledge of it. It does NOT mean the answers were
independently derived. It is a REGRESSION result -- these functions still
do what their author believed they did -- and it is not a validation
result.

What would make it one: an expected value derived from a source outside
this repository, or registered in a commit that precedes the
implementation, or authored by a second party. None of the 26 meets any of
the three. The `_halfwidth` cases registered in this session do not either
-- they are the rounding convention, which is external in the sense that
the convention predates the function, and same-author in the sense that
nobody but this session wrote them down here.

Not repaired, per the report's instruction.

Falsifier: any registered case whose expected value can be traced to a
commit earlier than its implementation, or to a second author.

---

## MSV_024 -- the move-set registration was unreachable from seed(), found by making the coverage claim checkable

**Status: SUPPORTED, repaired.**

`_seed_move_set()` was called from the module TAIL and not from `seed()`.
Running `tools/known_answer.py` reported 26 of 26 COMPLETE, because the
tail call had already run at import and nothing cleared the registry.
`tests/test_known_answer_gate.py` clears the registry and calls `seed()`
-- which does not reach the tail -- so both move-set metrics vanished.

It was invisible until the two metric ids were added to that test's
MANIFEST. The defect is a registration whose call site is not on the path
that matters, which is the third instance of that shape in this registry
(`MSV_013` here, `FMR_036` before it, and `tools/sourced.registry_complete`
exists because of the first one).

Repaired: `seed()` calls it, with the reason recorded at the call site.

Falsifier: a registration path that is green under the CLI and short under
a clear-and-reseed.

---

---

## MSV_025 -- a tail-only registration now fails the run rather than waiting to be found

**Status: SUPPORTED, built.**

`MSV_024` was the THIRD occurrence of one shape -- a `register(...)` call
that executes at import and is not on `seed()`'s path -- after `FMR_036`
(a `register` after a `finally`) and `MSV_013` (the same again). All three
were repaired where they were found, per instance.

`tools/known_answer.py::seed_reachable()` is the structural form: an AST
walk over the module's own source, a call graph over its top-level
functions, and a closure from `seed`. Every `register(...)` call site must
sit in a function that closure reaches. A module-level call is a violation
by construction, since it runs at import and nowhere else.
`registration_sites_elsewhere()` is the second arm: a `register(...)` in
any other file is outside `seed()` by construction and cannot be reached
at all. Both are wired into `report()`, so `python3 tools/known_answer.py`
exits non-zero, and into `tests/test_known_answer_gate.py`, so the repo
suite goes red.

Reachability is TRANSITIVE (`seed -> a -> b -> register()` passes) and the
check is null-tested in both directions -- a planted tail-only call fires,
a planted module-level call fires, a call `seed()` reaches does not, and
the registering functions are named so a check that found no `register()`
calls at all could not pass by silence.

**Limit, stated in the function:** a `register()` inside a NESTED def is
attributed to the top-level function containing it. A nested def that is
never called is a different defect and this does not catch it.

Falsifier: a fourth occurrence of the shape that reaches a green run.

---

## MSV_026 -- the mechanism that produced the finding

**Status: RECORDED, no build.**

`MSV_024` did not surface from the move-set suite (157 checks) or from the
repo suite (105 at the time). Both were green with the defect standing.
It surfaced from adding two ids to `tests/test_known_answer_gate.py`'s
MANIFEST -- that is, from making an existing coverage claim externally
checkable. The claim was *these two metrics are registered*; writing it
where something else could test it is what turned it into a measurement,
and the measurement failed.

Recorded in `CLAUDE.md` as the mechanism rather than as an incident.
