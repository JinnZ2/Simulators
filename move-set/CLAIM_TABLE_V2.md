# CLAIM TABLE -- move set, second order

Claims `MSV_001..MSV_016`, about `move_set_sim_v2.py` and the second work
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

## MSV_005 -- M4 on a static artifact perturbs the arithmetic, not the system

**Status: SUPPORTED.**

A published artifact cannot be perturbed. Its arithmetic can: recompute a
stated relationship from operands the artifact itself supplies.

The gate is on the DECLARATION, in both directions. A ledger declaring
`holds: true` where the recomputation fails scores 0; one declaring
`holds: false` where it fails scores 1.0. Refusing the second would make a
discrepancy unreportable, which is the finding M4 exists to produce. All
four cells checked (suite 4.1-4.4).

Tolerance is relative 5e-3 and declared (CHOICE 3): the demo artifact
rounds to 3-4 significant figures, so an exact test would report rounding
as a failure.

Falsifier: a stated relationship whose operands the artifact supplies and
which this cannot recompute.

---

## MSV_006 -- the demo's M4 finding

**Status: SUPPORTED, recomputable by anyone with the artifact.**

`aperiodic-order-sim-stack/SIM_STACK_REPORT.txt` line 23 states the
AB-Poisson finite-size baseline as **0.021**. The report ships both
dimensions that gap is between: AB 1.889 (line 15) and Poisson 1.911
(line 17). Recomputed, `|1.889 - 1.911| = 0.022`. Relative discrepancy
0.0476, ten times the declared tolerance.

One in the third decimal, and it is the denominator the headline
*"~15x larger"* ratio is taken over.

What this does NOT say: whether 0.021 is the right baseline at all. That
is a reading and it is not scored here -- `AOS_009` in this repo holds
that 0.021 is the smallest of three pairwise gaps in the space-filling
cluster and the honest ratio is nearer 4.5x. See `MSV_011`.

Falsifier: the report's own D_f values reproducing 0.021 exactly.

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
