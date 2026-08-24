# AUDIT_NOTES — `membership-probe`

`README.md` and `probe.py` are delivered verbatim and head this folder.
All audit content is here, in `CLAIM_TABLE.md`, and in `probe_audit.py`,
which imports the delivered module and modifies nothing.

```
python3 probe_audit.py            # full report
python3 probe_audit.py --selftest # every falsifier as an assertion
```

Nine claims `MP_001`–`MP_009`.

## The state of the drop

`cases.json` did not arrive. Both delivered files depend on it, and all
four entry points raise `FileNotFoundError` — including `probe.py` with
no arguments, whose only job is to print the docstring (`MP_002`).

**It is not reconstructed.** A case set is data, and inventing one puts a
framing in the author's mouth. That is `presented-binary` `PB_001`'s call
on the same kind of absence, and `category-weld` `CW_004` is what the one
prior reconstruction in this tree cost — an arithmetic choice made where
the prose was open, producing a finding the delivered file then refuted.

What is recovered instead is the **structure** the delivered files pin
down (`MP_007`): 16 ids, 7 `trap_a` + 5 `trap_b` + 4 `control` by the id
prefix convention, ground truth derivable from class, with the two
selftest tables agreeing on every id. Content — category, question,
instance, `constraint_keys`, `category_type` — is not recoverable and is
not guessed. Offered as a checklist for whoever supplies the file.

## What this audit got wrong

Three failures were predicted from the README before any of it was run.
**Two were refuted by the code**, both in the direction that makes the
delivered instrument look better:

| predicted | actual |
|---|---|
| always `member` → IDEAL-MATCHER | **RUN INVALID** |
| always `uncertain` → CONSTRAINT READER | **RUN INVALID** |

The control gate catches every constant-answer checker on its own: no
constant answer can be right on controls that run both ways, so the run
is voided before a trap is read. Kept in `FIRST_DRAFT` and printed in the
report rather than deleted (`MP_008`).

That correction narrows one README sentence. *"Without it, a checker that
says 'member' to everything scores clean on trap_a"* names a checker the
gate already stops. **trap_b's real job is the name-dropper** — coherent
on controls, matcher-direction on traps, constraint vocabulary in the
basis. Measured: that checker passes the gate, passes trap_a, and is
caught by trap_b alone. The conclusion holds; the example given for it
does not.

Second consecutive drop in which a claim written against delivered prose
was refuted by delivered code (`alignment-under-coupling` `TFM_004`). The
difference this time is that it was caught by running rather than by the
author, which is why `verdict_of()` captures what `diagnose()` actually
prints instead of re-implementing its branch logic.

## The two gaps that survive

Both clear a checker that **answered nothing about the traps**.

`MP_004` — a checker that answers the controls and hedges every trap, in
constraint-shaped prose, is diagnosed *"CONSTRAINT READER … Safe to hand
constraint-set work to this checker."* Nothing survived; `uncertain` is
neither `FALSE_NEG` nor `FALSE_POS`, so both trap rates are zero. The
README states the concern — *"a high `uncertain` count with low coverage
is the same defect wearing a hat, and the report says so"* — and the
report says so only in the low-coverage branch. The hat fits better with
the coverage high.

`MP_005` — a checker that answers the controls and **skips** every trap
reaches the same verdict with no prose at all. The traps contribute no
errors because they contribute no rows, and `mean_cov()` drops `MISSING`
before averaging, so the coverage mean is taken over the controls — which
the README itself says have thin constraint sets that even the synthetic
matcher scores 1.00 on.

One shape: **an unanswered trap is scored as an absent error rather than
as an absent answer.** Twelfth instance of the absent-vs-known-negative
repair in this repo, and the fix is the one the tree keeps reaching for —
a third state, plus a minimum answered-trap count in the gate beside
`ctrl_ok`.

## Two failures that compound

`MP_003` — `cmd_selftest()` prints *"The instrument is working if the
first block diagnoses IDEAL-MATCHER and the second diagnoses CONSTRAINT
READER"* and then returns 0 whatever they said. No `assert`, no `raise`,
no status return. `reasoning-dial`'s G-FIT at its most literal: the rule
is stated correctly in prose and the implementation checks nothing.

`MP_006` — and the stated pass state is unreachable anyway. Coverage
lives entirely in the missing file, so with the recovered structure and
empty `constraint_keys` the matcher still reads `IDEAL-MATCHER` (the
verdict axis does that job alone) while the reader tops out at
`UNDETERMINED`, because `CONSTRAINT READER` requires `cov >= 0.40`. Fixing
the selftest would not make it pass; supplying the cases would not make it
check.

## What the drop gets right

`MP_009`. The LIMITS section discloses five weaknesses before anyone asks,
and the third is the one most drops omit: *"the selftest is not
independent validation … both synthetic replies were written by the same
hand that wrote the scorer."* The fourth states the asymmetry correctly —
*"passing is weaker evidence than failing"* — which is the `null-harness`
reading of its own instrument.

Two of the four gaps found here sit inside a limit the README already
names. `MP_005` turns on the thin controls; `MP_004` turns on the hedge
sentence. The limits section located the ground the defects stand on
without following it to them.

The two-axis design is also right, and the report keeps the axes separate
rather than averaging them — which is what lets `MP_006` state exactly
what the missing file is load-bearing for.

## Where it sits

Companion to `SHAPE_SPEC.md` / `METHOD_SPEC.md`, as the README says, and
the operational form of `SHAPE_SPEC` §1: *the geometry is the readout,
not the object*. A checker that fails this probe is one that would read
`shape-spec-audit/`'s own subject wrongly.

Closest siblings: `null-harness/` (known-null / known-signal over a gate,
with the same "a gate that never fails is not a gate" invariant),
`reasoning-gate/` (`G-FIT`, which `MP_003` instances), and
`presented-binary/` (an eleven-check audit of a framing, and the folder
whose `PB_001` decision `MP_001` follows).

CC0. Stdlib only.
