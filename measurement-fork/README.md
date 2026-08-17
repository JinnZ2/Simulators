# measurement-fork

Same system description, three study designs, one diff.

This is a marker — an idea being tested for fit, not a position
under defense. Test fit, extend it, or report where it breaks.

CC0-1.0. stdlib only. No network. Phone-buildable.

## Run

    python3 validate.py systems/<spec>.json     # refuses to guess
    python3 compare.py  systems/<spec>.json     # the product

Added checks (not delivered) — see [`AUDIT_NOTES.md`](AUDIT_NOTES.md)
and [`CLAIM_TABLE.md`](CLAIM_TABLE.md):

    python3 sweep_check.py                      # the sweep rule
    python3 falsifier_sweep.py                  # can the design fail?
    python3 coverage_check.py                   # null-test the classifier
    python3 residual_audit.py                   # adjudicate the growth edge
    python3 proposed_probes.py                  # K14-K18 vs MF_010

Individual arms, if you want the raw probe lists:

    python3 conventional.py systems/<spec>.json
    python3 coupling.py     systems/<spec>.json
    python3 widen.py        systems/<spec>.json

## Arms

    conventional.py   what a field would actually run.
                      Competent, not strawmanned. Every default
                      in it has a real reason. Swappable —
                      drop in your own generator behind the
                      same interface.

    coupling.py       relation-side probes. Rule: when a
                      quantity is a relation between organism
                      and environment, the standard instrument
                      reads one side and reports the result as
                      a property of the organism. This arm
                      generates the missing side, and the ratio.

    widen.py          instrumentation options. Does not ask
                      what the system is. Asks what else could
                      be pointed at it. Refuses to rank — a
                      ranked list is a shortest path.

## The four cells

    SOLE REACH        quantity reached by exactly one arm.
                      What that frame buys.

    VOID RATIO        same base name, different quantity
                      (different object_of or normalizer).
                      Two designs appearing to agree while
                      measuring unlike things. A ratio or a
                      disagreement across this line is
                      undefined.

    SAME QUANTITY,    identical quantity, different protocol.
    DIFFERENT ROUTE   The conventional number is sound here.
                      Usable as-is, no redesign needed.
                      An empty cell is itself a finding.

    RESIDUAL          open questions, banded:
                      COVERED / PARTIAL / NO ARM.
                      PARTIAL is not resolved by the tool.
                      NO ARM is the growth edge.

## Quantity identity

A quantity is not a name:

    base        what is counted
    normalizer  what it is divided by (None = raw)
    object_of   organism | environment | coupling | instrument

Same base, different object_of, is not the same quantity. That
is the void-ratio case and it is caught structurally rather than
by inspection.

## Adding a system

Copy `systems/provisioning_calibration.json`, edit, run
`validate.py`. It emits questions for missing or ambiguous
fields and exits nonzero rather than filling anything in. A
generator that guesses at an unstated boundary is the failure
this toolset exists to catch.

`open_questions` may be badly named. That is fine — the
comparator scores coverage against them and reports PARTIAL
where the naming is the problem.
