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
| [`quantities.py`](quantities.py) | What a quantity is, and when two are the same one. **Delivered, verbatim.** Closed `OBJECTS` vocabulary. |
| [`widen.py`](widen.py) | Arm 3 — options, not quantities. Ranks nothing. **Reconstructed.** |
| [`validate.py`](validate.py) | Is the spec complete enough to fork on? **Reconstructed.** |
| [`systems/`](systems/) | `provisioning_calibration.json` **delivered, verbatim**; `variable_provisioning.json` is a fixture exercising every branch. |
| [`coverage_check.py`](coverage_check.py) | Null-tests the RESIDUAL classifier on the fixture. |
| [`residual_audit.py`](residual_audit.py) | Adjudicates the RESIDUAL cell by hand on the real spec. **The result.** |
| [`gate_fork.py`](gate_fork.py) | The fork's own claims through [`../reasoning-gate/`](../reasoning-gate/). Imports the gate, does not copy it. |
| [`proposed_probes.py`](proposed_probes.py) | K14–K18 against the gaps `MF_010` named. |
| [`CLAIM_TABLE.md`](CLAIM_TABLE.md) | Eleven claims (`MF_001..011`). |
| [`samples/`](samples/) | Pinned output. |

```bash
python3 validate.py systems/provisioning_calibration.json  # spec complete?
python3 compare.py  systems/provisioning_calibration.json  # the fork
python3 residual_audit.py                                  # the growth edge
python3 coverage_check.py                                  # audit the classifier
python3 gate_fork.py                                       # gated
python3 proposed_probes.py                                 # do K14-K18 close them?
#   K17 landed in widen.py as a design-directed move -- see MF_016
python3 ../tools/check_gate_drift.py                       # one gate?
```

Standard library only, deterministic.

## The result

`provisioning_calibration.json` through the fork, RESIDUAL cell adjudicated
by reading protocols rather than counting tokens:

```
residual as delivered      0 of 9   widen pooled into coverage
residual, measuring arms   5 of 9   widen excluded
residual, adjudicated      3 of 9   protocols read
```

Zero understates. Five overstates. **Three is the growth edge:**

```
[NO PROBE] coupling bandwidth
           latency and contingency_consistency measure delay and
           reliability of the loop. Neither measures how much can
           cross it per unit time.

[NO PROBE] whether trust in own sensing is a measurement or a belief
           confidence/accuracy reaches the confidence-validity gap,
           not whether reliance on the sensor was ever validated
           against outcome.

[NO PROBE] reversibility after regime shift
           nothing measures relearn RATE after the buffer is removed.
```

The third has a stated prediction and no instrument. The predicted contrast
is a **rate** — fast relearn against slow relearn once the buffer is removed
— and no K-probe returns a rate. Every one measures a level, a ratio, a
slope or a variance, all at fixed regime. The stated falsifier has the same
shape: *ratio flat across the provisioning gradient* needs the gradient
swept, and the probes as generated sit at one point on it.

**One probe closes both.** Error against trials-since-shift, fitted for a
time constant, at two or more provisioning levels. (`MF_010`)

### K14–K18 against those three gaps

Five probes specified since. Adjudicated by reading protocols;
`coupling.py` is unmodified.

| gap | verdict | via |
| --- | --- | --- |
| `whether trust in own sensing is a measurement or a belief` | **CLOSED** | K15 |
| `reversibility after regime shift` | **PARTIAL** | K14 |
| `coupling bandwidth` | **OPEN** | — |

**K14 is the first probe in the arm that returns a rate**, which is what
`MF_010` turned on. K15 closes its gap by injecting a *known* deviation —
scoring the sensing apparatus against ground truth rather than its own
report.

`reversibility` goes partial: K14 supplies the provisioning gradient the
stated falsifier needs, but nothing measures relearn rate *after* the
buffer is removed. K16 is a latency swept against staleness at **fixed
regime**; the predicted contrast is across a regime change.

K18's `object_of` is `design` — outside `quantities.OBJECTS`, so by
`MF_008` it is a widen move rather than a probe. The specification says so
itself. (`MF_014`)

**The mediation chain is the strongest part:**

```
practice_rate falls              K14
  -> baseline_freshness degrades   K15   lag 1
    -> detection_latency rises     K16   lag 2

falsifier: if K14 predicts K16 with K15 controlled out,
           the causal chain is wrong
```

Refutable by a partial correlation, direction named in advance, does not
depend on the effect being large.

Its one gap is that **the lags are ordinal.** A mediation test sampled
coarser than its own lag returns the chain collapsed into a single step —
indistinguishable from the chain being wrong, and it would read as the
falsifier firing. Declare the units and it becomes a `G-RES` pair:
sampling interval against the lag being resolved. (`MF_015`)

## Still missing from the package

`widen.py` and `validate.py` are reconstructed from the call sites;
`quantities.py` has since been delivered and replaces its reconstruction.
Choices beyond what the call sites fix are marked `[CHOICE]` in the source,
and any finding that leans on one says so. (`MF_001`)

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

### The schema refuses what the comparator counts

The delivered `quantities.py` enforces a closed vocabulary:

```python
OBJECTS = ("organism", "environment", "coupling", "instrument")

def quantity(base, object_of, normalizer=None):
    if object_of not in OBJECTS:
        raise ValueError(...)
```

The widen arm proposes options about the **design**, which is not on that
list — so `quantity()` raises and a widen output cannot be constructed as a
quantity at all. `MF_004` argued this from behaviour. The delivered schema
reaches it from the type system, independently. (`MF_008`)

`widen.py` here now builds its records with a local `option()` helper tagged
`object_of="design"`, deliberately outside the vocabulary, plus
`is_quantity(p)` so consumers filter mechanically rather than by convention.

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

### And on the real spec it is wrong in the other direction too

The false positives above are one half. On `provisioning_calibration` the
classifier also **misses two questions a coupling probe was explicitly
written for**:

| question | probe | why it missed |
| --- | --- | --- |
| `environmental autocorrelation` | K09 `autocorrelation [environment]` | 2 stems, need 2, hits 1. `environmental` does not stem to `environment` — `_stem` strips `-ies/-es/-s` only |
| `domain match between calibrating environment and test items` | K08 `task_performance / domain_match` | 7 stems, need 4, hits 3. Misses by one |

The two error types are independent and point opposite ways, landing on
different questions. **No single threshold fixes both** — raising it worsens
the false negatives, lowering it worsens the false positives. The widen
pooling is a one-line fix; the stemming is not fixable by threshold.
(`MF_009`)

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

Three more arrived in the next drop, same pattern:

| file | differing lines | what is missing |
| --- | ---: | --- |
| `make_docs.py` | 12 | `_stages()` — multi-stage guards render under one stage only |
| `README.md` | 16 | lists 5 files; the folder has 11 |
| `GUARDS.md` | 48 | `G-FIT` still under POST |

Five bundled files, five stale, across three drops. (`MF_011`)

**Fixed on the repo side.** [`gate_fork.py`](gate_fork.py) now runs this
folder's claims through the canonical gate by import, so there is nothing
here to go stale. [`../tools/check_gate_drift.py`](../tools/check_gate_drift.py)
finds any gate-family copy by content rather than filename, and
[`../tests/test_gate_drift.py`](../tests/test_gate_drift.py) fails the repo
suite if one lands. (`MF_012`)

Running it here also found a gap in the gate. The residual count is a
property of the coverage classifier, and a physical-scope claim resting only
on instrument-level quantities was recorded `supported`:

```
claim : [supported] the measurement design has 3 unmeasured quantities
```

`G-LAYER` downgraded on generator-level support and said nothing about
instrument-level. Now fixed upstream — a physical claim with no
physical-level support at all is `qualified`, and the same run splits:

```
claim : [supported] no probe in any measuring arm reaches 3 of the
                    spec's open questions            (instrument scope)
claim : [qualified] the measurement design has 3 unmeasured quantities
        ^ physical scope claim with no physical-level support:
          rests entirely on instrument
```

The distinction is real: a quantity can be unmeasured because nobody wrote
the probe, or because it is not measurable, and a count of the probe list
cannot separate those. (`MF_013`)

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

`MF_007` asked whether the fork surfaces a quantity its designers had not
considered. On `provisioning_calibration` it surfaces three, and one of them
has a stated prediction attached — so the answer is yes on n=1.

What is still unrun is the probe itself. `MF_010` names it; nobody has
measured a relearn rate.

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
