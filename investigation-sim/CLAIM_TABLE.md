# investigation-sim — CLAIM_TABLE

`IS_001..IS_014`. Claims about the design and the code in this folder.

**Second pass, 2026-08-26.** All four routes are now WIRED, not
declared. `IS_008` closes; `IS_011..IS_013` are what wiring them
found.

**Third pass, same day.** A sixth bin, `HELD_BUT_UNASKED`, added after
`gap-markers` `GM_005` mapped its own five states against these bins
and found no bin for `unasked`. `IS_014` records it, and `IS_002` is
narrowed rather than left standing.

**Nothing here is a claim about any real incident, organisation, or
person.** Every case is constructed and labelled so in its own file.
Egress from this environment is an allowlist and every incident-report
host is outside it (`MS_004` status), so no CSB report — or any other
investigation report — has been read.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the instrument. Where a check and a claim disagree, the
disagreement goes in the checker's output.

| id | claim | status |
|---|---|---|
| `IS_001` | No rate is computable from a retrospective corpus, and `rate()` raises rather than returning one. The mode that escapes the trap is FORWARD, which is also the stated purpose. | SUPPORTED |
| `IS_002` | `NOT_FORESEEN` is reachable, and a constructed case reaches it. A classifier that cannot return it is `CONSTANT_FIRES`. | SUPPORTED, **narrowed 2026-08-26** — reachability was asserted and correctness was not; see `IS_014` |
| `IS_003` | `NOT_DERIVABLE` and `NOT_FORESEEN` are kept apart **in the input**, not in the output: signals are three-valued and the third value carries the distinction. | SUPPORTED |
| `IS_004` | Route-to-remedy has three states and two were built. The third was found by running the report. | SUPPORTED |
| `IS_005` | The recursion is checkable from recommendation status alone, with no denominator and no reading of the incident. | SUPPORTED |
| `IS_006` | The primary bin on a `MULTIPLE` case is **declared, never computed**. A computed primary is a root-cause argument and this module does not make one. | SUPPORTED |
| `IS_007` | The guard written to prove `classify` never reads `truth` fired on the docstring saying it does not. | SUPPORTED |
| `IS_008` | Four of five routes were declared and not wired. | **CLOSED 2026-08-26** — all four wired, each importing its supplier's own function |
| `IS_009` | The forward mode's `unsearched_signals` readout has no retrospective analogue. | SUPPORTED |
| `IS_010` | No real report has been read and no case here is a real event. | UNVERIFIED |
| `IS_011` | `claim-record` returns `UNDERIVABLE` on exactly the cases `CALCULATED_UNCLOCKED` is about — the bin restated by a module that did not know it existed. | SUPPORTED |
| `IS_012` | Wiring `report-typing` surfaced `RT_008` where it costs something. The consumer reports the missing arm without patching the supplier. | SUPPORTED |
| `IS_013` | The supplier's return shape varies by outcome, and the arm written to prove a route is not `CONSTANT_SILENT` is the arm that found the consumer could not handle success. | SUPPORTED |
| `IS_014` | The four original signals could not express *the data was held and nobody asked*, so such a case coded honestly landed on `NOT_FORESEEN`. A sixth bin, found by a sibling folder's vocabulary rather than by any check here. | SUPPORTED |

---

## IS_001 — the selection trap, and the mode that escapes it

Every case in an incident-report corpus is a case where something
happened. Investigators look for prior warning and usually find it, so
a classifier run over that corpus reports that foreknowledge existed —
which is a property of the sampling frame.

"N% of incidents were foreseeable" needs a denominator of hazards
carrying the same signature where nothing happened, and that
population is the one `generation-capacity` R4 names as structurally
uncounted: prevention produces the absence of an output and no counter
increments. `uninstrumented` `UNI_126` and
`simulation-hypothesis-budget` `SHB_023` are the same shape — a frame
selected on the variable under test — and
`derivation-discarded` `DD_003` is the measured version, where the EIA
post-audit literature publishes three narrowings that are never
multiplied.

So `rate()` raises. The exception names the uncounted population and
names the mode that escapes it, and both are asserted.

**The escape is not a better corpus.** A forward run has no incident
to select on: the frame is *systems we pointed it at*, chosen before
any outcome. Retrospective mode exists to calibrate the classifier —
do the bins separate on cases where the answer is independently known
— and is forbidden from emitting a rate.

That the tool's stated purpose is avoidance and the mode that escapes
the trap is the forward one is the folder's central piece of luck: the
epistemically sound mode and the useful mode are the same mode.

**Falsifier:** a denominator. Enumerate hazards carrying a given
signature where nothing happened, and the rate becomes computable —
`generation-capacity` R4 is the work order for exactly that.

## IS_002 — the negative is reachable

`NOT_FORESEEN` is a bin, and the calibration set contains a case built
to land there: a feedstock contaminant nobody had characterised, from
a process change two tiers up a supply chain.

It was the hardest case to author honestly, and its authoring note
records the contestable call rather than smoothing it: whether an
incoming assay covering only specified species is *fit for purpose*
(so the case is genuinely novel) or is *a constitutional exclusion*
(so it is `GAP_UNINSTRUMENTED`). Recorded, not resolved.

That contest is not a weakness of the case. It is where the line
between bin 4 and bin 5 actually falls, and an instrument that never
lands near it is not being asked anything.

**Falsifier:** the negative unreachable on the calibration set, which
`--selftest` fails on.

## IS_003 — the distinction lives in the input

`NOT_DERIVABLE` and `NOT_FORESEEN` both fire nothing. A verdict-level
distinction between them would be a guess, so the distinction is in
the **signal**, which is three-valued:

    PRESENT      the record says it exists
    ABSENT       the record was searched and says it does not
    UNSEARCHED   nobody looked, or the record cannot say

`ABSENT` is a measurement. `UNSEARCHED` is not. All-`ABSENT` reaches
`NOT_FORESEEN`; all-`UNSEARCHED` reaches `NOT_DERIVABLE`; a missing
field reads `UNSEARCHED` and never `ABSENT`.

The two verdicts carry opposite instructions — one says look harder,
the other says stop looking — so collapsing them files a case with a
destroyed record as genuinely novel. That is the reading that stops
anyone looking, and it is the failure mode most worth designing out.

Fifteenth-plus instance of the absent-vs-known-negative repair in this
repository, and one of the few designed in before any data rather than
found in audit. What is new here is the **site**: previous instances
put the third state on an output field; this puts it on the input, so
every verdict downstream inherits it.

**Falsifier:** any path where the two produce one value.

## IS_004 — the third state I did not build, found by running

`remedy_mismatch` compares the bin a remedy addresses against the bins
that fired. The first version returned
`bool(fires) and aims not in fires`, so on a case where **nothing
fired** it returned `mismatch: False`, which the report rendered as
*"addresses a bin that fired."*

Visible in the first run of the report, on the `not-foreseen` case: a
remedy aimed at `GAP_UNINSTRUMENTED` on a case where no bin fired,
reported as correctly aimed. The two states a boolean over an empty
list collapses are *aimed at a bin that fired* and *no bin fired, so
there is nothing to aim at* — and the second is the more interesting
one, because a remedy for a hazard the record does not support is a
finding, not a pass.

`IS_003` designed this repair into the signals and I then failed to
apply it two functions later, in the function whose entire job is a
three-way comparison. Recorded rather than quietly fixed.

**Falsifier:** a case where the third state and one of the other two
are indistinguishable in the output.

## IS_005 — the recursion

An issued recommendation that is not implemented **is** a control
conceived and not built — bin 3, produced by the process investigating
bin 3, one level up.

Checkable from recommendation status alone: no denominator, no reading
of the incident, no judgement about whether the remedy was the right
one. `OPEN` and `CLOSED_UNIMPLEMENTED` are the recursion; `IMPLEMENTED`
is not; `UNRECORDED` and a missing status return `None` rather than
`False`, because *not recorded* is not *implemented*.

This is the readout most likely to survive contact with a real corpus,
because recommendation status is a field investigation bodies already
publish.

**Falsifier:** a status vocabulary where the distinction does not
hold, or a body that does not track implementation.

## IS_006 — the primary is declared, never computed

On a `MULTIPLE` case the module takes a declared primary and refuses
one that names a bin which did not fire. It does not compute one.

A computed primary is an argument about which cause is root, and
ranking causes is the move that lets an investigation stop at the
cheapest one. The module reports every bin that fired and puts the
ordering on the person who has to defend it.

`uninstrumented` `UNI_003` reached the same place about its own
mechanism list — the mechanisms are not exclusive, so filing is a
choice and an entry should carry a primary plus a list.

**Falsifier:** any path that infers a primary from the signals.

## IS_007 — the guard fired on the sentence saying it does not

`classify` must not read `case["truth"]`, because `truth` is the
calibration set's answer key. The check grepped the function body as a
string — and the body's docstring says *"Never reads
`case['truth']`"*, so the guard written to prove the field is unread
fired on the sentence saying it is unread.

`UNI_009` / `T1-1` inside the guard. Repaired with AST: parse the
function, drop the docstring node, collect string constants from what
remains. Both halves are pinned — that `truth` is absent from the
body, and that it is present in the docstring, which is what broke the
first version.

**Falsifier:** a read of `truth` in `classify` that the AST check
misses.

## IS_008 — CLOSED. All four routes wired

    KNOWN_ROUTED_AWAY      -> report-typing.score              WIRED
    CALCULATED_UNCLOCKED   -> claim-record.derive_clock        WIRED
    CONCEIVED_NOT_BUILT    -> fold-matrix.plan_column          WIRED
    GAP_UNINSTRUMENTED     -> uninstrumented.MECHANISMS        WIRED

Every one imports the supplier and calls the supplier's own function.
Nothing is copied and nothing is reimplemented — five stale copies of
one gate is what copying produced last time (`MF_006`, `MF_011`), and
`tools/check_gate_drift.py` exists because of it.

**The suppliers' refusals reach this side intact**, and that is the
property worth having. `fold-matrix` returns `UNREAD` where a plan was
not supplied, not `no`. `report-typing` returns `contrast: None` and
`verdict: None` until both arms and a second coder exist.
`uninstrumented` refuses a mechanism outside its eight-item tuple.
`claim-record` refuses a stored date.

**The `multiple` case is the cross-boundary test.** It fires three
bins and supplies no supplier block, and the three routes return three
*distinct* undeclared states — `FIGURE_UNDECLARED`, `UNREAD`,
`INSTANCES_UNDECLARED` — each in its own supplier's vocabulary, none
guessing. The absent-vs-known-negative repair holding across an import
boundary is a stronger result than it holding inside one module,
because none of the four suppliers was written with this consumer in
mind.

**Falsifier:** a supplier whose refusal does not survive the boundary,
or a route that turns out not to fit when a real case is coded.

## IS_009 — the readout with no retrospective analogue

Forward mode reports `unsearched_signals`: across the systems in
scope, how many have never been searched on each signal.

A retrospective investigation cannot produce this. By the time there
is an incident every signal has been searched, because searching them
is what an investigation is. The count only exists while nothing has
happened yet, which is the state the tool is for.

On the shipped example, `no_instrument` is the least-searched signal —
and that is the ordinary result, because it is the signal whose
absence leaves no gap in any record to notice.

**Falsifier:** an investigation body that publishes, per closed case,
which signals it did not search.

## IS_010 — nothing here is a real event

Seven constructed cases, each declaring `constructed: true`, each
carrying a per-signal basis and an authoring note. Ground truth lives
in how the case was authored, never in what the classifier says —
`playground/`'s rule.

No CSB report, NTSB report, HSE report, or any other investigation
document has been read. This environment's egress is an allowlist and
every such host is outside it. The design is built to be run by
someone who has the reports; it has not been run on one.

**Falsifier:** run it on a real corpus. The first thing to check is
whether the four signals are codable from a published report at all,
and the second is `IS_005`, which needs only the recommendation table.

---

## IS_011 — the bin, restated by a module that did not know it existed

`CALCULATED_UNCLOCKED` is defined as *a governing number whose domain
of validity or re-check interval was stripped — the figure survived
and the conditions under which it held did not.*

`claim-record.derive_clock` was built for an unrelated purpose: it
refuses a stored date and derives a shelf life from a time constant
and a dimensionless coupling. Handed the bridge-posting case, it
returns:

    clock    UNDERIVABLE
    why      no date is emitted; time_constant and coupling is not
             measured
    missing  time_constant, coupling

That is the bin's own definition, produced by an instrument that has
never heard of the bin, and it names *which* sub-fields are absent —
which is the remedy, computed rather than written.

The route is not `CONSTANT_SILENT`: a constructed figure with a
measured time constant and a measured coupling comes back `DERIVED`
with a shelf life and a next-check date. Both branches are exercised.

**Falsifier:** a `CALCULATED_UNCLOCKED` case where `derive_clock`
returns `DERIVED` — which would mean the figure has a clock, and the
bin was mis-assigned.

## IS_012 — a supplier defect, surfaced where it costs something

`report-typing` `RT_008`: `CONTROL` requires a comparison arm and
`score()` enforces it nowhere, so a one-arm input returns a
well-formed `by_seat` with nothing saying the denominator is absent.

There, it was a defect in a scorer with no data. Here it is a scorer
handed a case and returning a rate for one seat, and a consumer that
passes it through inherits the silence.

The split taken: **do not patch the supplier, do not launder it
either.** `known_channel` reads the required seats out of
`INSTANCE_SCHEMA["reporter_seat"]` — the supplier's own declaration —
and reports `denominator_present: False` with a note naming `RT_008`.
The supplier is unmodified; a consumer that patches its supplier is
the drift this repo imports to avoid.

The check is not `CONSTANT_FIRES`: a two-arm input returns
`denominator_present: True` and `control_note: None`.

**Falsifier:** `RT_008` repaired in `report-typing`, at which point
this detection is redundant and should be removed rather than left as
a second implementation.

## IS_013 — the arm that proves a route can succeed found that it could not

`derive_clock`'s return shape **varies by outcome**: `missing` is
present on the `UNDERIVABLE` path and absent on the `DERIVED` one.

    UNDERIVABLE   findings, missing, next_check, regime,
                  shelf_life_base, state, why
    DERIVED       findings, next_check, regime, shelf_life_base,
                  state, why

The consumer used fixed-key access, which works on every failing case
and raises `KeyError` the first time the route succeeds. The selftest
arm that exists *specifically* to show the route is not
`CONSTANT_SILENT` — feed it a clock that can be derived, check the
verdict differs — is what found it.

Both are now asserted: that the shapes differ, that `missing` is the
key which only appears on failure, and that the consumer reports both
without assuming one shape.

Third instance in this folder of a check firing on its own text, too:
the check written to assert `missing` is no longer rebuilt from
`findings` grepped the function source, and the source contains a
comment saying exactly that. Repaired with AST — string constants
only, docstring dropped, and comments are not in the AST at all, which
is what makes it the right tool rather than a longer regex.

**Falsifier:** a supplier with a stable return shape, or a consumer
that reads a key the supplier does not return on some path.

---

## IS_014 — the false negative in the bin that matters most

`gap-markers` landed with five `STATE` values and one of them was
`unasked`: *data exists, collected for another purpose; question never
posed.* Mapping that register's states against these bins, two mapped
and three did not — and `unasked` was the one whose absence had a
consequence here.

Code such a case honestly against the four original signals:

    prior_report          ABSENT   nobody reported it
    figure_without_clock  ABSENT   no governing figure is stale
    designed_control      ABSENT   no control was proposed
    no_instrument         ABSENT   the gauges exist and reported

Every one of those is **true**. Nothing was routed away, no figure lost
its clock, no control was shelved, and the instrument was not blind.
So the case fires nothing and lands on `NOT_FORESEEN` — *genuinely
novel* — while eleven years of gauge record sat in a file.

**That is the worst failure this classifier has.** `IS_002` makes the
reachability of `NOT_FORESEEN` load-bearing on the grounds that a
classifier which never returns it is telling the operator what they
came to hear. The converse was never asserted: a classifier that
returns it *wrongly* tells the operator to stop looking, which is the
one instruction that cannot be recovered from. `IS_002` is narrowed to
say so.

The repair is a **fifth signal**, not a re-reading of the four:
`held_data_unasked` — *was the quantity derivable from data already
held, collected for another purpose, with the question never posed?* —
and a sixth bin, `HELD_BUT_UNASKED`, because this is a foreknowledge
state parallel to the other four rather than a modifier on one.

`cases/held-but-unasked.json` is the case that found it, and its
authoring note records that it reads `ABSENT` on all four original
signals truthfully. Every pre-existing case now states the fifth
signal explicitly rather than defaulting: a missing signal reads
`UNSEARCHED`, which would have moved four verdicts to `NOT_DERIVABLE`
silently.

The bin has **no route yet**, and that is a third state rather than a
second: `NONE_YET` in the spec, parsed into `ROUTE_PENDING_BINS`, kept
apart from the negative's no-route-by-nature. Both render as an empty
supplier list and they are not the same statement.

**What this says about the method.** The gap was not found by any
check in this folder. It was found by a *different vocabulary*, built
for a different purpose by the same operator, mapped against this one —
which is `triad-playground` `TP_008`'s result about decorrelated
shadows, arriving as a fact about two registers rather than two
readers. A single vocabulary cannot enumerate what it has no word for.

**Falsifier:** a real case coded as `HELD_BUT_UNASKED` that turns out
to be one of the other five, or a seventh state in some third
vocabulary that this six cannot express — which is the same test, and
the map in `gap-markers/markers.py` is where it would show.
