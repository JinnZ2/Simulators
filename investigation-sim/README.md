# investigation-sim

CSB-style incident investigation, broadened past chemical process to
**industrial, manufacturing and infrastructure**, pointed at one
question:

> Was this KNOWN, CALCULATED, CONCEIVED AND NOT BUILT, or sitting in a
> gap no instrument covered — and which, because they need different
> remedies.

Built to be run **forward**, on live systems, which is both the stated
purpose and the only mode that escapes the trap below.

    python3 investigation-sim/bins.py               # the report
    python3 investigation-sim/bins.py --case <id>
    python3 investigation-sim/bins.py --forward forward_example.json
    python3 investigation-sim/bins.py --selftest    # 77 checks

`SPEC.md` is written first and **parsed** by `bins.py` — bin names,
non-bin verdicts, routing table and mode list all come out of the
spec at import, so a decision changed in one and not the other turns
the selftest red.

## The trap, stated before the design

Every case in an incident-report corpus is a case where something
happened. Investigators look for prior warning and usually find it, so
a classifier run over that corpus will report that foreknowledge
existed. That is a property of the sampling frame.

**No rate is computable from it.** "N% of incidents were foreseeable"
needs a denominator of hazards carrying the same signature where
nothing happened, and that population is the one `generation-capacity`
R4 names as structurally uncounted: prevention produces the absence of
an output and no counter increments. `rate()` raises rather than
returning a number, and the exception names both the uncounted
population and the way out.

**The way out is not a better corpus — it is running forward.** A
forward run has no incident to select on: the frame is *systems we
pointed it at*, chosen before any outcome. Retrospective mode exists
to **calibrate** the classifier and is forbidden from emitting a rate.

The folder's central piece of luck is that the epistemically sound
mode and the useful mode are the same mode.

## The five bins

| bin | | routes to |
|---|---|---|
| `KNOWN_ROUTED_AWAY` | a report existed and reached a channel where reading was optional | `report-typing` |
| `CALCULATED_UNCLOCKED` | a governing number survived and the conditions under which it held did not | `claim-record`, `criteria-drift` |
| `CONCEIVED_NOT_BUILT` | a control was designed, sometimes costed, and not implemented | `fold-matrix` |
| `GAP_UNINSTRUMENTED` | no instrument was pointed at it, by the instrument's constitution | `uninstrumented` |
| `NOT_FORESEEN` | genuinely novel | — |

Plus two that are not bins: **`NOT_DERIVABLE`** (the record cannot
say) and **`MULTIPLE`** (more than one fires, which is the ordinary
case).

**`NOT_FORESEEN` must be reachable.** A classifier that never returns
it is `CONSTANT_FIRES` — telling the operator what they came to hear —
and the selftest requires a constructed case that lands there.

## The distinction the whole thing rests on

`NOT_DERIVABLE` is **not** `NOT_FORESEEN`. Both fire nothing; they
carry opposite instructions. One says look harder. The other says stop
looking.

So the distinction lives in the **input**, not the output. Signals are
three-valued:

    PRESENT      the record says it exists
    ABSENT       the record was searched and says it does not
    UNSEARCHED   nobody looked, or the record cannot say

`ABSENT` is a measurement; `UNSEARCHED` is not. A missing field reads
`UNSEARCHED` and never `ABSENT`. Collapsing the two files a case with
a destroyed record as genuinely novel — the reading that stops anyone
looking, and the failure mode most worth designing out.

## Two readouts that need no denominator

**Route-to-remedy mismatch.** Per case: does the remedy address a bin
that fired? A case binned `GAP_UNINSTRUMENTED` whose recommendation is
a training change is a remedy aimed at a different bin. One case at a
time, no population required.

**The recursion.** An issued recommendation that is not implemented
*is* a control conceived and not built — bin 3, produced by the
process investigating bin 3, one level up. Checkable from
recommendation status alone, which investigation bodies already
publish. This is the readout most likely to survive contact with a
real corpus.

## Forward mode

Occupancy: which bins currently hold across systems in scope, as
counts of systems. Never a probability, never a ranking.

Its `unsearched_signals` column has **no retrospective analogue**. By
the time there is an incident, every signal has been searched —
searching them is what an investigation is. The count only exists
while nothing has happened yet, which is the state the tool is for.
On the shipped example `no_instrument` is the least-searched signal,
which is the ordinary result: it is the signal whose absence leaves no
gap in any record to notice.

## Scope

- No probability, frequency, or risk estimate. Nothing it emits is a
  likelihood.
- No hazard ranking.
- No individual or organisation named as a cause. Bins are properties
  of a record and of an instrument set.
- **Every case is constructed** and says so in its own file. Egress
  here is an allowlist and every incident-report host is outside it,
  so no CSB, NTSB, HSE or equivalent report has been read. The design
  is built to be run by someone who has them.

On the `no_severity` screen: its scope in this repo is the **emitted
report**, and the report is clean under one declared exemption
(`recommendation`), measured with the three-arm harness rather than
taken. The exemption is worth naming as a limit — an investigation
folder's working vocabulary *is* the screened vocabulary. `warning`,
`recommendation`, `hazard` are the domain's own nouns, not severity
language this tool is adding, and a screen written for spreadsheet
audits does not know the difference.

## What it found on itself

**`IS_004`.** `remedy_mismatch` returned `bool(fires) and aims not in
fires`, so on a case where nothing fired it returned `mismatch: False`
and the report rendered it as *"addresses a bin that fired."* Found by
running the report on the first pass. `IS_003` had designed exactly
that repair into the signals; I then failed to apply it two functions
later, in the function whose entire job is a three-way comparison.

**`IS_007`.** The guard written to prove `classify` never reads
`case["truth"]` grepped the function body as a string — and the
docstring says *"Never reads `case['truth']`"*, so the guard fired on
the sentence saying it does not. `UNI_009` / `T1-1` inside the guard.
Repaired with AST, both halves pinned.

**`IS_008`.** Four of five routes are declared and not wired. The
wired one imports `uninstrumented.MECHANISMS` and refuses a mechanism
outside it — imported, not copied, because five stale copies of one
gate is what copying produced last time (`MF_006`, `MF_011`). The
other four are the folder's largest open item and each is a small,
specific piece of work, named per route in `CLAIM_TABLE.md`.

## Files

| | |
|---|---|
| `SPEC.md` | written first, parsed by the code |
| `bins.py` | classifier, the two denominator-free readouts, forward mode, the refused rate |
| `selftest_bins.py` | 77 checks; every S7 falsifier gets an arm |
| `cases/` | seven constructed cases, one per verdict |
| `forward_example.json` | a four-system forward run |
| `CLAIM_TABLE.md` | `IS_001..IS_010` with a REFUTATION_PROTOCOL |
| `samples/` | pinned output, both modes |

Stdlib only, parses under Python 3.9, phone-buildable, CC0.

Siblings: `uninstrumented/` (the exclusion register, and the one wired
route), `generation-capacity/` (R4, the uncounted non-event that makes
the rate uncomputable), `report-typing/` (a report typed by the
reporter's position), `claim-record/` (a figure whose clock is
derived, never stored), `fold-matrix/` (plan against practice),
`closure-cost/` (a variable closed before the event arrived),
`move-set/` (refusals as verdicts).
