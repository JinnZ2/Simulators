# measurement-fork

Take one system and design the measurement three ways at once, then diff the
designs rather than the results.

The product is the four-cell diff. What does exactly one frame reach; where
do two frames use the same word for different quantities; where do they agree
so an existing result is reusable as-is; and what does nothing reach at all.

The last cell is the point. It is called the growth edge and it is the one a
harness is most likely to suppress by accident.

## Contents

| File | What it is |
| --- | --- |
| [`compare.py`](compare.py) | The three-way diff. **Delivered, verbatim.** |
| [`conventional.py`](conventional.py) | Arm 1 — the design a field would actually run. **Delivered, verbatim.** |
| [`coupling.py`](coupling.py) | Arm 2 — the missing side of every organism/environment relation. **Delivered, verbatim.** |
| [`quantities.py`](quantities.py) | What a quantity is, and when two are the same one. **Reconstructed.** |
| [`widen.py`](widen.py) | Arm 3 — options, not quantities. Ranks nothing. **Reconstructed.** |
| [`validate.py`](validate.py) | Is the spec complete enough to fork on? **Reconstructed.** |
| [`systems/`](systems/) | Worked spec exercising every branch. |
| [`coverage_check.py`](coverage_check.py) | Null-tests the RESIDUAL classifier. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Seven claims (`MF_001..007`). |
| [`samples/`](samples/) | Pinned output. |

```bash
python3 validate.py systems/variable_provisioning.json   # spec complete?
python3 compare.py  systems/variable_provisioning.json   # the fork
python3 coverage_check.py                                # audit the classifier
```

Standard library only, deterministic.

## The delivered package does not run

`compare.py` imports `quantities`, `widen` and `validate`. None of the three
was in the drop, so `conventional.py` and `coupling.py` both fail on their
first import.

All three are reconstructed here from the call sites, which fully determine
the contracts. Choices beyond what the call sites fix are marked `[CHOICE]`
in the source, and the one place a reconstruction choice affects a finding is
flagged in that finding. (`MF_001`)

## What the design gets right

**`object_of` carried in the quantity itself.** A quantity is
`(base, object_of, normalizer)`, and two quantities are the same one only
when all three match. That is [`reasoning-gate/`](../reasoning-gate/)'s
`G-DIM` moved one stage earlier: `G-DIM` voids a ratio at *report* time once
its operands turn out to belong to different objects; carrying `object_of` in
the quantity makes the mismatch visible at *design* time, before anything is
run. On the worked spec it fires twice, both real. (`MF_002`)

**The conventional arm is written to be competent.** Its docstring is
explicit that the defaults it encodes are not errors and each has a real
reason. The gaps then show up as gaps rather than mistakes, which is the only
way this comparison stays honest — a straw conventional arm would make every
other cell meaningless.

**`blind_to` is required on every probe.** An arm reaching a quantity alone
is only interesting next to what the others could not see.

**The empty cell is handled.** On the worked spec, `SAME QUANTITY, DIFFERENT
ROUTE` comes back empty, and `compare.py` says so as a result rather than as
an absence:

> none -- the arms share no quantity at all. That is itself a finding: the
> designs do not overlap, so no existing result speaks to the coupling
> questions.

That is the strongest thing the fork produces. The two arms are not
disagreeing; they are not addressing the same quantities. (`MF_003`)

## What it gets wrong

### A non-measuring arm suppresses the growth edge

`compare.py` pools every arm into `allp` and runs `coverage()` over all of
it — including the widen arm, of which its own output says:

> `[widen] -- options, not quantities.`

An option is not a measurement. Counting it toward coverage lets a proposal
to *rename* a question mark that question as *reached*:

```
residual, widen included (compare.py as delivered) : 0 of 7
residual, measuring arms only                      : 1 of 7
  [NO ARM] which measured differences reverse if the
           reference population is changed
```

RESIDUAL is the cell the docstring calls the product. It is where a false
COVERED costs most, because a missing measurement that never appears there is
not on any list at all.

This one depends partly on the reconstruction — the `widen.py` here echoes
each open question's text, which makes the effect maximal. The structural
point survives either way: an arm proposing no quantity should not sit in the
denominator of a cell about which quantities are missing. **Fix is one line:**
build the coverage pool from the measuring arms. (`MF_004`)

### The classifier is beaten by a single probe's vocabulary

`coverage()` marks a question COVERED when stemmed-token overlap clears 60%
of its distinct stems. Against three deliberate nulls it refuses two and
fires on one:

```
silent   does the organism report the environment coupling latency ...
COVERED  measure the instrument organism environment consequence variance
silent   what colour is the apparatus
```

The firing null shares five of its six stems with the coupling arm's
autocorrelation probe (*"measure the environment's own variance
structure ..."*). So the failure mode is specific: a null built from **one
probe's** vocabulary beats the threshold; one built from the whole pool's
does not.

`compare.py` is already candid about the middle band — PARTIAL is explicitly
"not resolved here. Resolve by hand." That caution belongs on COVERED too,
since COVERED is the verdict that removes a question from the list. (`MF_005`)

### The bundled gate is a stale copy

The drop also carried `gate.py` and `guards.json`. Both are the **pre-repair**
versions of the files already in [`reasoning-gate/`](../reasoning-gate/) — a
170-line diff, with every repair absent:

| repair | bundled copy |
| --- | --- |
| `close(diverged=...)` | missing |
| denial records written before raising | missing |
| `claim(..., scope=...)` layer downgrade | missing |
| registry rejects a blank `fail_message` | missing |
| `promote()` / `ratio()` refuse to overwrite | missing |
| docstring example that runs | missing |
| `G-FIT` stage | still `post`, enforced at `pre` |
| `G-CTRL` stage | still `pre`, also fires at `post` |

**Neither file is checked in here.** The repo's convention is to *import* the
gate — [`msiaf-gdprf-bridge/`](../msiaf-gdprf-bridge/) and
[`reasoning-dial/gate_dial.py`](../reasoning-dial/gate_dial.py) both do,
specifically so the two cannot drift. This drop is the drift those imports
exist to prevent, arriving on schedule:

```python
GATE_SRC = os.environ.get("GATE_SRC", "../reasoning-gate")
sys.path.insert(0, GATE_SRC)
from gate import Gate, Resolution, Control
```

(`MF_006`)

## What is unrun

`systems/variable_provisioning.json` is a test fixture written to exercise
every branch, not a research design. The load-bearing question for the tool
is untouched: **on a real design, does the fork surface a quantity the
designers had not considered?**

Everything here checks that the instrument can see its own gaps. Whether it
sees anyone else's is unmeasured. (`MF_007`)

## Cross-repo

- [`reasoning-gate/`](../reasoning-gate/) — `G-DIM` at report time; this is
  the same check at design time. Also the source of the stale copy in
  `MF_006`.
- [`null-harness/`](../null-harness/) — `coverage_check.py` is its
  known-null/known-signal invariant applied to a classifier rather than to a
  gate. `MF_004` is the `CONSTANT_SILENT` case one level up: the residual
  cell that cannot report a gap.
- [`divergence-playground/`](../divergence-playground/) — the same
  three-frames-on-one-object shape, with readers instead of measurement
  designs. Its `agree_by_accident` cell is `SAME QUANTITY, DIFFERENT ROUTE`
  with the null attached.
- [`triad-playground/`](../triad-playground/) — the coupling arm's whole
  argument (a standard instrument reads one side of a relation and reports it
  as a property of the organism) is the fourth-layer problem stated in
  measurement rather than in observers.
- [`instrument-epistemology/`](../instrument-epistemology/) — `blind_to` is
  its blindness map, required per probe instead of graded per instrument.

## License

CC0-1.0, matching the repository default and the delivered files' headers.
