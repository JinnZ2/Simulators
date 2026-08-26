# investigation-sim — CLAIM_TABLE

`IS_001..IS_010`. Claims about the design and the code in this folder.

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
| `IS_002` | `NOT_FORESEEN` is reachable, and a constructed case reaches it. A classifier that cannot return it is `CONSTANT_FIRES`. | SUPPORTED |
| `IS_003` | `NOT_DERIVABLE` and `NOT_FORESEEN` are kept apart **in the input**, not in the output: signals are three-valued and the third value carries the distinction. | SUPPORTED |
| `IS_004` | Route-to-remedy has three states and two were built. The third was found by running the report. | SUPPORTED |
| `IS_005` | The recursion is checkable from recommendation status alone, with no denominator and no reading of the incident. | SUPPORTED |
| `IS_006` | The primary bin on a `MULTIPLE` case is **declared, never computed**. A computed primary is a root-cause argument and this module does not make one. | SUPPORTED |
| `IS_007` | The guard written to prove `classify` never reads `truth` fired on the docstring saying it does not. | SUPPORTED |
| `IS_008` | Four of five routes are **declared and not wired**. This is the folder's largest open item. | SUPPORTED |
| `IS_009` | The forward mode's `unsearched_signals` readout has no retrospective analogue. | SUPPORTED |
| `IS_010` | No real report has been read and no case here is a real event. | UNVERIFIED |

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

## IS_008 — four routes are declared and not wired

    KNOWN_ROUTED_AWAY      -> report-typing            DECLARED
    CALCULATED_UNCLOCKED   -> claim-record, criteria-drift  DECLARED
    CONCEIVED_NOT_BUILT    -> fold-matrix              DECLARED
    GAP_UNINSTRUMENTED     -> uninstrumented           WIRED

The wired one imports `uninstrumented.MECHANISMS` and refuses a
mechanism outside it. Imported, not copied — five stale copies of one
gate is what copying produced last time (`MF_006`, `MF_011`), and
`tools/check_gate_drift.py` exists because of it.

The other four are checked only for the folder existing. That is the
folder's largest open item and each is a specific, small piece of
work:

- `report-typing` — a `KNOWN_ROUTED_AWAY` case should carry the
  channel the report landed in and whether that channel generates an
  action item, which is `reverse_arm_score`'s `b_time_to_action`
  pointed at an internal report rather than a televised one.
- `claim-record` — a `CALCULATED_UNCLOCKED` case should be able to
  emit an actual claim record, whose `derive_clock` refuses a stored
  date and derives one from a time constant and a coupling. The bin's
  whole content is a figure whose clock was stripped, and that module
  is the instrument for exactly that.
- `fold-matrix` — a `CONCEIVED_NOT_BUILT` case is `plan_exists` /
  `practice_tracks_plan`, which that module already has as a column
  the code cannot merge into `basis`.

**Falsifier:** the routes wired, or a route that turns out not to fit
when tried.

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
