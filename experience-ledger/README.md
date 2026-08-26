# experience-ledger

Origin claims confer present-tense standing, and the standing is almost
never rechecked. The module does not score the claim — it emits **the
maintenance question the field skipped**.

Delivered verbatim in `experience_ledger.py`. Audit in
`ledger_audit.py`, which imports it and modifies nothing. Claims
`EL_001..EL_009`.

**No claim about any person is recorded or judged here.** `probes/`
holds audit-authored branch probes, labelled as such in every file, and
they exist to reach code paths.

**The field-behaviour claim is not tested.** Whether *"coded since I was
twelve"* is granted continuity and *"ran machinery from age six"* is
not is an empirical statement about fields, and nothing here measures
it. It is the module's central assertion and it stays an assertion.

## What it is

Six decay classes, and the asymmetry is the point: **competence decays,
standing does not.** Physiological (fast, weeks), procedural-motor
(slow, precision before sequence), declarative-component (fast, *and*
the referent can be superseded independently of the person),
substrate-mechanics (very slow, transfers laterally), judgment-under-
load (structure holds, calibration goes stale) — and `standing`, which
is named in its own entry as not a competence at all.

Transfer runs on shared **substrate**, not shared domain label, and
`transfer()` refuses to emit an aggregate coefficient: component
knowledge and mechanics move at different rates out of the same hours,
so one number averages two things that move independently. That refusal
is the strongest move in the module and it is built in, not found in
audit.

## What the audit found

**It is the decomposition of a folded term the tree already registered.**
`fold-matrix/fold_register.py` lists `experience` as a candidate with
`substitutes_for: "accumulated hours + continuity + transfer, none
checked"` and a `residual_tell` that is this module's header in
compressed form. The register named the components and marked them
unchecked; this is the instrument for checking them, arrived at
independently. `PROOF_CASE` is material for the `counter_case` cell the
register leaves `UNFILLED` — it does not close `FM_038`, since the cell
is still empty there.

**The module returns its own verdict on its own proof case.**
`PROOF_CASE` rendered as a claim comes back `CONTINUITY ASSERTED, NOT
MEASURED`. That is honest rather than a fault: the decay half is
physiology and holds, and the granting half — that a field would extend
continuity here and not ask — is the unmeasured half the argument rests
on.

**The help text is the string `None`.** The header is `#` comments, not
a docstring, so `__doc__` is `None` and `main()`'s else branch prints
it. `--transfer` is advertised in the usage block and unimplemented;
`--schema` is implemented and unadvertised.

**There is no state for "checked, and nothing was found."**
`maintained is UNCHECKED` is an identity test against `None`, so `""`,
`0`, `False` and `[]` all read as measured. A checker who looked and
found no maintenance cannot say so. That lands on the one field the
whole module turns on.

Three smaller: `question_skipped: null` means both *this class has no
measurable* and *no question was skipped*; `score: UNCHECKED` is on one
branch of three, so a caller reading it gets a `KeyError` on the others;
and `Same grammatical form` holds over three of the four header
examples — *"ran the school paper / scouts"* names an activity, not an
origin, and is the one whose handling note has to supply the time span.

## Running it

    python3 experience-ledger/experience_ledger.py --classes
    python3 experience-ledger/experience_ledger.py --schema
    python3 experience-ledger/experience_ledger.py --check probes/branch_measurable.json
    python3 experience-ledger/ledger_audit.py --selftest
    python3 experience-ledger/ledger_audit.py

Stdlib only, parses under Python 3.9, CC0.

Siblings: `fold-matrix/` (the register entry this decomposes),
`domain-ledger/` (four uncombined ratios and `no composite emitted` —
the same refusal), `uninstrumented/` (SCALAR DEMAND, which the
aggregate refusal avoids), `closure-cost/` (a variable closed before
the event arrived; here it is a variable granted before the check).
