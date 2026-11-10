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

`aggregate.py` reports two counts, both **ILLUSTRATIVE** (the seeds were
picked because the tree already held material on them, so these are counts
over seeds, not rates about laws):

```text
tested_any              last_tested != VOID                          1 of 3
tested_against_purpose  stated_purpose != VOID AND the test's        0 of 3
                        measurand declared to match it
                        (last_tested.value.matches_purpose = true)
unresolved              tested, but purpose VOID or match undeclared 1
```

The match is declared on the card (`matches_purpose`: true / false / null),
never inferred by the tool. The one tested seed, the EU marker, tested
removal resilience in 2019; its stated purpose is VOID, so it reads
UNRESOLVED.

```sh
python3 card.py cards/*.json
python3 aggregate.py
TAF_PATH=/path/to/thermodynamic-accountability-framework python3 tests/test_card.py
```

Neither module accepts `--selftest`.

## Divergence from TAF (recorded 2026-11-10)

TAF `core/regulatory_scope_audit.py` `audit()` treats an absent
`intent_check` as `intent_applicable = True`. So a regulation out of scope
with no intent check reads `[OUT OF SCOPE -- INTENT PRESERVED]`: the intent
is assumed to still apply. This card reads the same case as VOID, since an
undeclared intent is no information. TAF's code is untouched; a dated note
there records this as a candidate correction. Until TAF decides, a card's
`scope_valid` and a direct TAF run can differ on exactly this case, and
`tests/test_card.py` pins the card's reading.

## Open

- `INDEPENDENT_AS_DECLARED` compares two names. It cannot see shared funding
  or staff (`assessor-coupling/`).
- Whether a test's measurand matches the stated purpose is a reader
  declaration (`matches_purpose`); nothing checks it against the texts.
- No enforcer is stated in the tree for either seeded law, so circularity is
  VOID on all three.
