# law-audit-card

PROPOSED | co-authored (JinnZ2 + Claude) | CC0 | stdlib only.

A card per law: what it says it is for, what enforces it, what evidence
there is that the enforcement produces the outcome, and whether anyone has
checked. Built from the proposal in `COVERAGE.md` section 4 (landed
verbatim from the read-only coverage report of 2026-11-10). Additive: the
two existing `law-*` dirs are not touched.

The tools **read**. They do not decide anyone's value; a readout is not a
ranking or a verdict (`READ_ME_THIS_WAY.md` section 4). So the
`disposition` field is **reader-assigned**, with a reader id and a date.
`card.py` never writes KEEP, EDIT, REVISE or RETIRE (checked from its own
AST, with a planted case showing the check fires). Its only move on that
field is to **force UNRESOLVED** when `evidence` or `cut_sensitivity` is
VOID, keeping the reader's assignment beside it as `reader_assigned`.

## Fields

Each is `{"tag", "value", "basis"}`, tag one of OBSERVED / DERIVED /
PROPOSED / VOID. VOID means no information: value is null and the field is
written, never omitted. OBSERVED and PROPOSED need a basis.

```text
stated_purpose    what the law says it is for. Same concept as TAF
                  core/regulatory_scope_audit.py `first_principle_intent`;
                  passed to it, not redefined
target_outcome    the outcome it is meant to produce
enforcement       {mechanism, enforcer}
evidence          that enforcement produces the outcome
cut_sensitivity   DERIVED from >= 2 declared boundaries, each a declared-frame
                  `boundary` (declared-frame/v2/check_frame.py) with an evidence
                  reading SUPPORTS / DOES_NOT_SUPPORT / UNDETERMINED:
                  readings differ -> FLIPS, agree -> HOLDS, < 2 determined -> VOID
scope_valid       one of TAF's three verdicts, read from TAF's own source:
                  IN SCOPE / OUT OF SCOPE -- INTENT EXPIRED /
                  OUT OF SCOPE -- INTENT PRESERVED. With a `taf_audit` block the
                  card is run through TAF's audit() (DERIVED). Out of scope with
                  intent undeclared -> VOID: TAF defaults that case to "intent
                  applies" and the card does not take the default
last_tested       {date, tester}; VOID if never
evaluator         {evaluator}
circularity       DERIVED: enforcer == evaluator -> CONDITIONAL(circular_eval);
                  differ -> INDEPENDENT_AS_DECLARED (names compared, nothing
                  checked); either VOID -> VOID
anchor_date       the date the card's facts are anchored to
disposition       {value, reader, date}, value in
                  KEEP / EDIT / REVISE / RETIRE / UNRESOLVED
```

A card may assert a derived field. If the assertion disagrees with the
derivation, the card is refused.

**REVISE, not REDO.** The proposal's REDO is renamed REVISE so it does not
read as REBUILD in the correction notice section G, which applies to parts
of a *report*, not to a law. Mapping, also in `card.DISPOSITION_MAP`:

```text
REDO     -> REVISE
REBUILD  -> not a disposition (correction notice section G, parts of a REPORT)
```

**Welds.** "No welds" in the evidence is `category-weld/`'s sense
(independent quantities fused into one term); use `category-weld/weld.py`
on the evidence's terms. The card does not reimplement it.

## TAF

`card.py` points to TAF and imports it; it does not reimplement the scope
audit. It looks for `core/regulatory_scope_audit.py` under `$TAF_PATH`, or
in a sibling checkout named `thermodynamic-accountability-framework`.
Without one, scope-label checks read NOT_TESTABLE and the TAF tests are
skipped (reported, not passed).

## Seeds and aggregate

```text
cards/dyed_fuel.json       26 CFR 48.4082-1: enforcement OBSERVED (the settled
                           column A quote), evidence VOID, cut VOID (column B)
cards/eu_marker.json       EU 2022/197: enforcement and last_tested (2019
                           evaluation) OBSERVED at search depth; rest VOID
cards/sunday_laundry.json  every field VOID (correction notice section D:
                           statute NOT_FOUND)
```

Every value is taken from the two `law-*` dirs with a `path:line` basis;
nothing is drafted from memory. All three read UNRESOLVED.

`aggregate.py` counts cards whose `last_tested` is not VOID as "laws checked
against own purpose". On the seeds: 1 of 3. **ILLUSTRATIVE**: the seeds were
picked because the tree already held material on them, so this is a count
over seeds, not a rate about laws.

```sh
python3 card.py cards/*.json
python3 aggregate.py
TAF_PATH=/path/to/thermodynamic-accountability-framework python3 tests/test_card.py
```

Neither module accepts `--selftest`.

## Open

- `INDEPENDENT_AS_DECLARED` compares two names. It cannot see shared funding
  or staff (`assessor-coupling/`).
- `last_tested` does not say what the test was against. The EU 2019 evaluation
  tested removal resilience; whether that is "its own purpose" is the reader's
  call, and the stated purpose is VOID on that card.
- No enforcer is stated in the tree for either seeded law, so circularity is
  VOID on all three.
