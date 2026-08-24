# CLAIM_TABLE — `membership-probe`

Claims about the delivered `probe.py` and `README.md`, both verbatim and
modified by nothing here. Computed by `probe_audit.py`, which imports the
module rather than modelling it.

REFUTATION_PROTOCOL: a claim about the scorer's behaviour is settled by
running the scorer. A claim about the missing file is settled by its
arrival. Nothing here is settled by reading the README twice.

**Two of this audit's three predicted failures were refuted by the code,
both in the direction that makes the delivered instrument look better.**
The predictions and the corrections are kept in `FIRST_DRAFT` and printed
in the report rather than deleted — see `MP_008`.

---

### MP_001 — `cases.json` did not arrive; nothing in the folder runs

`probe.py` calls `load_cases()` on every command and `README.md` lists the
file under Files. Run as delivered:

| entry point | result |
|---|---|
| `probe.py` (no args) | `FileNotFoundError` |
| `probe.py emit` | `FileNotFoundError` |
| `probe.py score x.txt` | `FileNotFoundError` |
| `probe.py selftest` | `FileNotFoundError` |

Four of four. `measurement-fork` `MF_001`'s shape — a package whose
imports were not in the drop — with the difference that there the missing
pieces were code recoverable from their call sites, and here the missing
piece is **data**.

**Not reconstructed**, and the reason is a decision this repo has already
made twice. `presented-binary` `PB_001` left `cases/` absent rather than
reconstructed *"since it is data and inventing one would put a framing in
the author's mouth"*; `category-weld` `CW_004` is what the one prior
reconstruction cost — an arithmetic choice made at a point the prose left
open, which produced a finding the delivered file then refuted.

**Falsifier:** its arrival. `--selftest` fails when it lands, so `MP_001`,
`MP_006` and `MP_007` have to be restated and the delivered selftest run
for real.

**Status: SUPPORTED.**

---

### MP_002 — the help path needs the data file

`main()` calls `load_cases()` before dispatching on `argv`, so
`python3 probe.py` with no arguments — the path whose whole job is to
print the docstring — raises. It is the first thing a reader tries and the
one path that has no reason to touch the case set.

Two lines: move the load below the dispatch, or into the three commands
that need it.

**Falsifier:** a no-args invocation that prints the docstring.

**Status: SUPPORTED.**

---

### MP_003 — the selftest asserts nothing

`cmd_selftest()` prints both blocks and then prints:

> The instrument is working if the first block diagnoses IDEAL-MATCHER and
> the second diagnoses CONSTRAINT READER. If it does not, the instrument
> is defective, not the checker.

It then returns `None`, `main()` returns 0, and the process exits clean
whatever the two blocks said. Measured: no `assert`, no `raise`, no
status return anywhere in the function.

`reasoning-dial`'s G-FIT shape at its most literal — the rule is stated
correctly in prose and the implementation checks nothing. The repo's own
convention is a selftest that goes red, and every other module in this
tree that ships one does.

The fix is the sentence, mechanised: capture the two verdicts, compare
them to the two expected strings, return 1 on mismatch.

**Falsifier:** an `assert`, a `raise`, or a status return in
`cmd_selftest`. `--selftest` fails if one appears.

**Status: SUPPORTED.**

---

### MP_004 — hedging is unscored *and* ungated, and clears a checker that answered nothing about the traps

A checker that answers the four controls correctly and returns
`uncertain` on every trap, in constraint-shaped prose, is diagnosed:

> **CONSTRAINT READER** — Both trap classes survived and the basis engages
> the constraint sets. Safe to hand constraint-set work to this checker.

Nothing survived. `uncertain` is `outcome == "uncertain"`, which is
neither `FALSE_NEG` nor `FALSE_POS`, so both trap rates are 0.0 and
`trap_err` is 0.0. The hedge list prints below the verdict, but the
verdict is already the clean one.

The README states the concern and misses by one branch:

> Hedging is not scored as an error. A high `uncertain` count with low
> coverage is the same defect wearing a hat, and the report says so.

The report says so **only in the low-coverage branch**. With coverage
high the hat fits better and nothing says anything.

**This claim was originally written wider and the code refuted it** — see
`MP_008`. A checker that hedges *everything*, including the controls, is
caught by the control gate.

**Falsifier:** a hedge count entering the gate or the verdict.

**Status: SUPPORTED, narrower than first written.**

---

### MP_005 — `MISSING` is not gated either, and needs no prose at all

A checker that answers the four controls and skips every trap reaches the
same **CONSTRAINT READER**. The traps contribute no errors because they
contribute no rows; `mean_cov()` drops `MISSING` before averaging, so the
coverage mean is taken over the controls alone — which the README itself
says have thin constraint sets that *"even the synthetic ideal-matcher
scores 1.00"* on.

`diagnose()` prints the missing ids and does not gate on them. `rate()`
returns `0.0, 0, 0` for an empty class, so a case set with no `trap_b` at
all behaves identically.

`MP_004` and `MP_005` are one shape: **an unanswered trap is scored as an
absent error rather than as an absent answer.** Twelfth instance of the
absent-vs-known-negative repair in this repo, and the fix is the one the
tree keeps reaching for — a third state, plus a minimum answered-trap
count in the gate beside `ctrl_ok`.

**Falsifier:** an answered-trap count entering the gate.

**Status: SUPPORTED.**

---

### MP_006 — the coverage axis lives entirely inside the missing file, so the delivered selftest cannot reach its own pass state

Verdicts are derivable without `cases.json` — class comes from the id
prefix by the README's own convention, ground truth from class. Coverage
is not derivable at all, because `constraint_keys` is in the file that did
not arrive. Running the two delivered selftest tables with the recovered
structure and empty `constraint_keys`:

| table | verdict | fn | fp | cov |
|---|---|---|---|---|
| `FAKE_MATCHER` | **IDEAL-MATCHER (confirmed on both axes)** | 0.86 | 1.00 | 0.00 |
| `FAKE_READER` | **UNDETERMINED — right answers, unstated basis** | 0.00 | 0.00 | 0.00 |

The matcher is still caught — the verdict axis alone does that job. The
reader **cannot** reach `CONSTRAINT READER`, because that verdict requires
`cov >= 0.40` and there is nothing to match against.

So the drop's stated pass condition — *"the first block diagnoses
IDEAL-MATCHER and the second diagnoses CONSTRAINT READER"* — is
unreachable as delivered, and would be unreachable even if `MP_003` were
fixed. The two failures are independent and compound.

**Falsifier:** `cases.json` arriving with `constraint_keys` populated.

**Status: SUPPORTED.**

---

### MP_007 — the delivered files pin down the missing file's structure, not its content

Recoverable from the two selftest tables plus the class-prefix convention:

| class | n | ids |
|---|---|---|
| `trap_a` | 7 | A01–A07 |
| `trap_b` | 5 | B01–B05 |
| `control` | 4 | C01–C04 |

16 ids, present in both tables, no disagreement between `FAKE_READER`'s
verdicts and the class convention on any trap. Ground truth follows:
`trap_a` → `member`, `trap_b` → `not_member`, controls from the reader
table (C01, C02 member; C03, C04 not_member). This matches the README's
"16 cases" exactly.

**Not** recoverable: `category`, `question`, `instance`,
`constraint_keys`, `category_type`. Structure, not content — which is why
`MP_001` declines the reconstruction rather than attempting a partial one.

Offered as a checklist for whoever supplies the file, not as a draft of it.

**Status: SUPPORTED.**

---

### MP_008 — what this audit predicted wrongly, and what that corrects in the README

Three failures were predicted from the README before any of it was run.
**Two were refuted by the code**, both in the direction that makes the
delivered instrument look better:

| predicted | actual | why |
|---|---|---|
| always `member` → IDEAL-MATCHER | **RUN INVALID** | the control gate catches it first: 2 of 4 controls run the other way, so `ctrl_ok = 0.50` |
| always `uncertain` → CONSTRAINT READER | **RUN INVALID** | same gate — `uncertain` is not correct on a control either, so `ctrl_ok = 0.00` |

**The control gate is stronger than it looks.** No constant answer can be
right on controls that run both ways, so every constant-answer checker is
voided before a single trap is read.

That narrows the README's stated case for `trap_b`:

> trap_b is the half that most similar tests leave out. Without it, a
> checker that says "member" to everything scores clean on trap_a.

The checker named there is one the gate already stops. **trap_b's real job
is the name-dropper**: coherent on controls, matcher-direction on traps,
constraint vocabulary in the basis. That checker passes the gate, passes
trap_a, and is caught by trap_b alone — measured, `IDEAL-MATCHER (verdict
axis only)`. The conclusion holds and the example given for it does not.

Recorded rather than corrected silently, because this is the second
consecutive drop in which a claim written against delivered prose was
refuted by delivered code (`alignment-under-coupling` `TFM_004`), and the
difference this time is that it was caught by running rather than by the
author.

**Status: SUPPORTED. The correction strengthens the drop.**

---

### MP_009 — the LIMITS section is the strongest part of the delivered README

Five weaknesses disclosed before anyone asked: coverage is keyword
matching and gameable by name-dropping; the controls have thin constraint
sets and their coverage numbers should not be read; **the selftest is not
independent validation, because both synthetic replies were written by
the hand that wrote the scorer**; 16 cases is small and *"passing is
weaker evidence than failing"*; and the ground truth on `B01` is arguable
in a way that is *"exactly the distinction under test"*.

The third is the one most drops omit and it is stated in the sharpest
available form. The fourth states the asymmetry correctly — this is a
`null-harness` instrument, and a gate that clears a checker has said less
than one that fails it.

Two of the four gaps found here sit inside a limit the README already
names: `MP_005` turns on the thin controls, and `MP_004` turns on the
hedge sentence. The limits section located the ground the defects are
standing on without following it to them.

**Status: SUPPORTED. The honest positive.**
