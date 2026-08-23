# operator-structure-echo

**Marker under exploration.** Delivered spec: [`SPEC_ECHO.md`](SPEC_ECHO.md),
landed verbatim.

> Observed: instruments built in this ecosystem recur to the same structural
> shape the operator uses to process the domain by hand.
>
> Not a defect claim. Not a discipline failure. It is a property of a
> single-builder instrument and cannot be removed by effort — only counted.

```
python3 echo_register.py     # one line per module, and it refuses to fill it
python3 corroboration.py     # what agreement between two modules is worth
```

Both take `--selftest`. 23 / 19 checks, 42 in all, green. Samples pinned in
`samples/`, byte-reproducible.

The register reads the module list off the filesystem, so the pinned samples
are a snapshot of the tree as it stood when they were pinned — adding a folder
to the repo moves the counts, by design. The samples are not frozen against
that and should be repinned when the tree changes; the alternative is a
hardcoded list, and this repo has already had one of those go stale.

## Why this is its own folder

The spec offers the choice — fold into `handoff-provenance/` or stand alone —
and leaves it to the operator. Built standalone, on three grounds, and the
placement is one `git mv` from being folded in with nothing else to change:

1. **Different object under test.** `handoff-provenance/` scopes itself to the
   channel between *conversation and code*. This is the channel between
   *builder and instrument*. Both are provenance; they are not the same
   channel.
2. **The register is repo-wide.** One row per module, all 70 of them. That
   does not sit inside a folder about handoffs.
3. **`handoff-provenance/` is itself one of the rows.** Nesting the register
   inside a module it must enumerate puts the register inside its own subject
   population. (Whether that row is a YES is not for this side to say — see
   below.)

## `echo_register.py` — do not correct, log

The instruction is *"Do not correct. Log."* The one line kept per module is
the delivered question: **does this shape match a procedure the operator
already runs unaided? YES / NO / UNEXAMINED.**

The module list is read off the filesystem, not hardcoded — this repo has
already had one partial copy of its own folder index go stale, and `mark()`
refuses a row that is not in the tree.

**Only the operator can fill it, enforced rather than stated.** `mark()`
refuses a YES or a NO without operator attribution. The downstream model
cannot answer *"does this match a procedure you already run unaided"* about
someone else, and a register it could fill itself would be a register of its
guesses.

### UNEXAMINED is not NO

This is the load-bearing line in both modules. Every row defaults UNEXAMINED,
and the consequence the spec names runs on the register's contents. Read
UNEXAMINED as NO and every module comes back independent, the shared generator
disappears, and the readout inverts **while looking unchanged**. So UNEXAMINED
is a third state throughout, never folded into either answer.

### Two kinds, because the delivered list holds two

The spec names three instances and then separates them itself — the first two
are *"the instrument missing a case"*, the third is *"the instrument
REPRODUCING the operator's own processing structure in a domain the operator
did not intend to model"*, and the third is what raises this from a per-repo
note to a subject. Those are different observations, so they are logged apart:
`OMISSION` and `REPRODUCTION`. A YES without a kind is refused.

## The three instances are not three independent observations

Checked by importing `instrument-bias-sims/excluded_subject.py` rather than
restating it:

| delivered | kind | status |
| --- | --- | --- |
| `s4` — no doe | OMISSION | already logged as **S4 (missing doe)** |
| `allocation_coupling` — no untenured continuous observer | OMISSION | already logged as **S10 (missing untenured continuous observer)** |
| `allocation ledger` — cost accounting matches the operator's manual accounting | REPRODUCTION | **new to this subject** |

**The split lands exactly on the kind.** Both OMISSION instances were already
in the excluded-by-construction register; the one REPRODUCTION instance is the
only new one — which is precisely the one the spec says raises this from a
note to a subject. That was asserted in the spec and is now checked
mechanically.

And **all three sit inside `instrument-bias-sims`**, which is one row in a
per-module register. The count of three is a count of two kinds, across one
module, spanning two registers. Two registers agreeing about S4 is one
observation counted twice — the spec's own concern about inherited agreement,
arriving inside the register built to track it.

That module is also the one that got audited hardest in this repo, so it is
where echoes would surface first whether or not it is where they are densest.
**The instance list is a map of where someone looked.**

## The base rate is refused, and not for want of *n*

The spec lists it open: *"base rate unknown; no count yet."* The register
refuses to compute one, and the reason is a **selection effect**, not a small
sample:

> Every row in the examined set is there because someone noticed an echo, and
> noticing one is the same act as finding one.

Three YES out of three examined is what that selection produces whether the
true rate is nine in ten or three in a hundred. Examining more modules the
same way does not fix it — only examining modules chosen **before** looking
would.

## `corroboration.py` — the consequence, made runnable

> If YES is frequent, results across modules are not independent — they share
> a generator. Any agreement between two modules is then weaker evidence than
> it appears, because agreement may be inherited rather than found.

That is a claim about pairs, so this works on pairs and returns a **state**,
never a number:

| state | meaning |
| --- | --- |
| `INHERITED` | both YES — agreement is expected from the shared generator, not evidence |
| `MIXED` | one YES, one NO — the generator is in one arm, unquantified |
| `INDEPENDENT` | both NO, as far as examined |
| `UNKNOWN` | either is UNEXAMINED — not independent, not inherited |

No discount factor is returned. A numeric weight needs a base rate, the base
rate is refused on a selection effect, and any number here would be that
refusal laundered through arithmetic.

### The same register, read two ways

| | correct | UNEXAMINED as NO |
| --- | --- | --- |
| `INHERITED` | 0 | 0 |
| `MIXED` | 0 | 69 |
| `INDEPENDENT` | **0** | **2346** |
| `UNKNOWN` | 2415 | 0 |
| pairs | 2415 | 2415 |

Identical data. **Zero pairs in this repo are established independent** — one
module carries a verdict, every other row is UNEXAMINED. That is not a finding
about the modules; it is the register reporting that the work has not been
done, and it is the correct output for a register nobody has filled.

Fold the default into NO and the same register says almost everything is
independent. The failure needs no bad faith and leaves no trace in the result:
a default silently becomes an answer, and the table looks identical in shape.

## What a YES does not mean

The spec is explicit and it is preserved throughout: not a defect claim, not a
discipline failure, a property of a single-builder instrument that cannot be
removed by effort — only counted.

An instrument that matches its builder's manual procedure may be matching it
**because the procedure is right**. What a YES costs is the independence of
two readings, not the correctness of either. Whether the echo is separable
from ordinary domain expertise is listed open in the spec and **is not
resolved here** — from a pair table, "echoed the procedure" and "was simply
correct" are the same row.

## Open, and left open

- **Base rate unknown; no count yet.** Refused above, with the reason.
- **No method proposed for detecting it from inside — and this module is
  inside.** `mark()` refusing to let the downstream model fill a row prevents
  a register of guesses; it does not produce a detector.
- **Unknown whether it is separable from ordinary domain expertise.**
- **This module has its own row, and it is UNEXAMINED.** A register of
  single-builder echoes, built by the same single builder, is subject to its
  own subject.
- **The register is per module; the instances are per file.** Three instances
  collapse into one row, and a module with one echo and a module with twelve
  are the same YES. The pair table inherits that flattening.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
