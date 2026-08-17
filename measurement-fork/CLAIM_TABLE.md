# CLAIM_TABLE — measurement-fork

Claims from the delivered package and from the audit here.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

1. A failed check updates the **claim**, not the code. The delivered arms
   are not retuned to preserve any entry here.
2. `quantities.py` is now the **canonical delivered** version.
   `validate.py` and `widen.py` remain reconstructed; any finding that
   depends on their content says so inline.
3. Nothing here is a claim about the domain the worked spec describes. The
   fork is a design instrument; this folder audits the instrument.

---

## MF_001 — the delivered package does not run

**who:** A · **status:** SUPPORTED, and repaired

`compare.py` imports `quantities`, `widen` and `validate`. None of the three
was in the drop, so nothing executes: `conventional.py` and `coupling.py`
both fail at `from quantities import quantity, probe`.

`quantities.py` has since been delivered and replaces the reconstruction.
The canonical version is **stricter** than the reconstruction in the place
that matters: `OBJECTS` is a closed vocabulary and `quantity()` raises on
anything outside it. `validate.py` and `widen.py` remain reconstructed from
the call sites:

```
widen.generate(spec)   -> probes, arm="widen"
validate.check(spec)   -> list of open questions, empty means go
```

Choices beyond the call sites are marked `[CHOICE]` in the source.

**Falsifier:** the originals. Any behavioural difference is a finding about
the reconstruction, and `MF_004` already flags the one place it matters.

---

## MF_002 — the object_of field is the contribution

**who:** D · **status:** SUPPORTED

A quantity is carried as `(base, object_of, normalizer)`, and two quantities
are the same one only when all three match. That is what makes the VOID
RATIO cell possible: two arms both reporting `task_performance` are measuring
different things when one is a property of the organism and the other of the
coupling.

This is [`reasoning-gate/`](../reasoning-gate/)'s `G-DIM` moved one stage
earlier. `G-DIM` voids a ratio at **report** time, once the operands turn out
to belong to different objects. Carrying `object_of` in the quantity itself
makes the mismatch visible at **design** time, before anything is run — the
only point at which it is cheap to fix.

On the worked spec the cell fires twice, both real:

```
base name: response_magnitude
  response_magnitude / perturbation_size  [of coupling]
  response_magnitude / stimulus_severity  [of organism]

base name: task_performance
  task_performance / domain_match  [of coupling]
  task_performance                 [of organism]
```

**Falsifier:** a case where two probes share all three fields and still are
not comparable. That would mean the triple is not a sufficient identity and
a fourth field is needed.

---

## MF_003 — the arms share no quantity at all, and that is the result

**who:** A · **status:** SUPPORTED

On the worked spec, the `SAME QUANTITY, DIFFERENT ROUTE` cell is **empty**.
`compare.py` handles this explicitly and correctly:

> none -- the arms share no quantity at all. That is itself a finding: the
> designs do not overlap, so no existing result speaks to the coupling
> questions.

That is the strongest single output the fork produces and it is worth
stating plainly: it means the conventional arm's numbers are not evidence
for or against the coupling arm's questions. They are not disagreeing. They
are not addressing the same quantities.

Note what this does **not** say. It is not a verdict on either arm — the
conventional arm is written to be competent and its `blind_to` fields are
reasons, not errors. The finding is about overlap, which is a property of
the two designs together.

**Falsifier:** a spec on which the cell is non-empty. Worth seeking: a
populated cell would name exactly which conventional results are reusable
as-is, which is the cheapest possible finding for anyone holding existing
data.

---

## MF_004 — a non-measuring arm suppresses the growth edge

**who:** A · **status:** SUPPORTED

`compare.py` pools every arm into `allp` and runs `coverage()` over all of
it. But its own output says of the widen arm:

> `[widen] -- options, not quantities.`

An option is not a measurement. Counting it toward coverage lets a proposal
to *rename* a question mark that question as *reached*:

```
residual, widen included (compare.py as delivered) : 0 of 7
residual, measuring arms only                      : 1 of 7
  [NO ARM] which measured differences reverse if the
           reference population is changed
```

RESIDUAL is the cell the docstring calls the product — "the growth edge.
Nothing measures this yet." It is the one cell where a false COVERED costs
most, because a missing measurement that never appears there is not on any
list at all.

**Depends on the reconstruction, and says so.** The `widen.py` here emits
one probe per open question carrying that question's text, so its overlap is
total and the effect is maximal. A widen arm that did not echo the question
would contribute less false coverage. The structural point survives either
way: an arm proposing no quantity should not sit in the denominator of a
cell about which quantities are missing.

**Fix:** one line — build the coverage pool from the measuring arms, and
report widen separately as `compare.py` already does in the SOLE REACH cell.

**Evidence:** `coverage_check.py` §3.

---

## MF_005 — the coverage classifier is beaten by a single probe's vocabulary

**who:** A · **status:** SUPPORTED

`coverage()` calls a question COVERED when stemmed-token overlap clears 60%
of the question's distinct stems. Run against three deliberate nulls, it
refuses two and fires on one:

```
silent   does the organism report the environment coupling latency ...
COVERED  measure the instrument organism environment consequence variance
silent   what colour is the apparatus
```

The failure is specific rather than general. The firing null shares five of
its six stems with the coupling arm's autocorrelation probe, whose protocol
reads *"measure the environment's own variance structure ..."*. Five of six
is a real overlap attached to a meaningless question — so a null built from
**one probe's** vocabulary beats the threshold while one built from the
whole pool's does not.

`compare.py` is already candid about the middle band: PARTIAL is explicitly
"not resolved here. Resolve by hand." That caution belongs on COVERED too,
since COVERED is the verdict that removes a question from the list.

**Falsifier:** a threshold rule that refuses all three nulls while still
catching the designed-for questions in `coverage_check.py` §2. Raising the
threshold is the obvious attempt; whether it survives §2 is a measurement.

**Evidence:** `coverage_check.py` §1–2.

---

## MF_006 — the bundled gate is a stale copy, and the drift is measurable

**who:** A · **status:** SUPPORTED

The drop bundled `gate.py` and `guards.json`. Both are the **pre-repair**
versions of the files already in [`reasoning-gate/`](../reasoning-gate/).
Diff is 170 lines, and every repair is absent:

| repair | in the bundled copy |
| --- | --- |
| `close(diverged=...)` — divergence as an explicit call | missing |
| denial records written before raising | missing |
| `claim(..., scope=...)` — generator support downgrades a physical claim | missing |
| registry rejected when a `fail_message` is blank | missing |
| `promote()` / `ratio()` refuse to overwrite | missing |
| docstring usage example that actually runs | missing |
| `G-FIT` stage `post` → `pre` | still `post` |
| `G-CTRL` stage `pre` → `["pre","post"]` | still `pre` |

Neither file is checked in here. The repo's convention for using the gate is
to **import** it — [`msiaf-gdprf-bridge/`](../msiaf-gdprf-bridge/) and
[`reasoning-dial/gate_dial.py`](../reasoning-dial/gate_dial.py) both do,
specifically so the two cannot drift. This drop is the drift those imports
exist to prevent, arriving on schedule.

```python
GATE_SRC = os.environ.get("GATE_SRC", "../reasoning-gate")
sys.path.insert(0, GATE_SRC)
from gate import Gate, Resolution, Control
```

**Falsifier:** show the bundled copy is a deliberate fork with its own
purpose. Nothing in the drop says so, and the two stage bugs are the ones
already fixed upstream — which is what a stale copy looks like rather than
a fork.

---

## MF_007 — nothing has been run through the fork but the worked spec

**who:** A · **status:** UNVERIFIED

`systems/variable_provisioning.json` is written here to exercise every
branch: `currently_measured`, `provisioned`, `regime`, `test_items_source`,
and seven open questions. It is a test fixture, not a research design, and
the domain content is generic on purpose.

The load-bearing question for the tool is untouched: **on a real design, does
the fork surface a quantity the designers had not considered?** Everything
in this folder is a check that the instrument can see its own gaps. Whether
it sees anyone else's is unmeasured.

**Falsifier:** fork a real design and see whether the SOLE REACH and
RESIDUAL cells contain anything its authors did not already know.

---

# Canonical schema and the real spec

`quantities.py` and `systems/provisioning_calibration.json` delivered.
Both verbatim.

---

## MF_008 — the canonical schema refuses to build a widen probe

**who:** A · **status:** SUPPORTED. Confirms `MF_004` from the delivered code.

The delivered `quantities.py` enforces a closed vocabulary:

```python
OBJECTS = ("organism", "environment", "coupling", "instrument")

def quantity(base, object_of, normalizer=None):
    if object_of not in OBJECTS:
        raise ValueError(...)
```

The widen arm proposes options about the **design**, which is not on that
list. So `quantity()` raises outright — the schema will not let a widen
output be constructed as a quantity at all.

`MF_004` argued from behaviour that widen must not be pooled into coverage.
This is the same conclusion arriving from the type system, delivered
independently: **the schema refuses what the comparator then counts.**

`widen.py` here now builds its records with a local `option()` helper tagged
`object_of="design"`, deliberately outside the vocabulary, plus
`is_quantity(p)` so any consumer filters correctly. The exclusion is
mechanical rather than a convention someone has to remember.

**Falsifier:** add `"design"` to `OBJECTS`. That would make widen output a
quantity, and then the VOID RATIO and SOLE REACH cells would have to accept
it — which is the outcome the closed vocabulary exists to prevent.

---

## MF_009 — on the real spec the classifier is wrong in both directions

**who:** A · **status:** SUPPORTED

Three counts of the same cell on `provisioning_calibration`:

```
residual as delivered      0 of 9   widen pooled into coverage
residual, measuring arms   5 of 9   widen excluded
residual, adjudicated      3 of 9   protocols read
```

**Zero understates. Five overstates. Three is the growth edge.**

The false positives are `MF_004`/`MF_008`: five questions marked COVERED by
widen alone.

The false negatives are new, and they are stemming failures on questions a
coupling probe was explicitly written for:

| question | probe | why it missed |
| --- | --- | --- |
| `environmental autocorrelation` | K09 `autocorrelation [environment]` | 2 stems, need 2, hits 1. `environmental` does not stem to `environment` — `_stem` strips `-ies/-es/-s` only |
| `domain match between calibrating environment and test items` | K08 `task_performance / domain_match [coupling]` | 7 stems, need 4, hits 3. Misses by one |

The two error types are independent and point opposite ways, landing on
different questions. **No single threshold fixes both**: raising it worsens
the false negatives, lowering it worsens the false positives. The widen
pooling is a one-line fix; the stemming is not fixable by threshold at all.

**Falsifier:** a stemmer and threshold that refuse `coverage_check.py` §1's
firing null while catching both K08 and K09. Adding `-al`, `-ing`, `-ity`
is the obvious attempt and its false-positive rate is a measurement.

**Evidence:** `residual_audit.py`.

---

## MF_010 — the real growth edge is three questions, and one has a prediction attached

**who:** A · **status:** SUPPORTED

Adjudicated by reading the protocols rather than counting tokens:

```
[NO PROBE] coupling bandwidth
           latency and contingency_consistency measure delay and
           reliability of the loop; neither measures how much can cross
           it per unit time

[NO PROBE] whether trust in own sensing is a measurement or a belief
           confidence/accuracy reaches the confidence-validity gap but
           not whether reliance on the sensor was ever validated against
           outcome

[NO PROBE] reversibility after regime shift
           nothing measures relearn RATE after the buffer is removed
```

The third is the one with a stated prediction and no instrument. The
predicted contrast is a **rate** — fast relearn against slow relearn once
the buffer is removed — and no probe in the coupling arm measures a rate.
Every K-probe measures a level, a ratio, a slope or a variance, all at
fixed regime.

The same gap shows up in the stated falsifier. "Ratio flat across the
provisioning gradient" needs the gradient swept; the probes as generated
sit at one point on it.

**One probe closes both**: error against trials-since-shift, fitted for a
time constant, at two or more provisioning levels. It reaches
`reversibility after regime shift` and supplies the gradient the falsifier
requires.

**Falsifier:** name an existing K-probe that returns a rate. `latency` is
a delay, not a rate of change; `contingency_consistency` is a variance at
fixed regime.

---

## MF_011 — three more bundled files are stale copies

**who:** A · **status:** SUPPORTED. Extends `MF_006`.

`make_docs.py`, `README.md` and `GUARDS.md` arrived alongside, all
pre-repair versions of files already in
[`reasoning-gate/`](../reasoning-gate/):

| file | differing lines vs repaired | what is missing |
| --- | ---: | --- |
| `make_docs.py` | 12 | `_stages()` — multi-stage guards render under one stage only |
| `README.md` | 16 | lists 5 files; the folder has 11 |
| `GUARDS.md` | 48 | `G-FIT` still under POST, enforced at `pre` |

None is checked in. Five bundled files now, five stale, from three
separate drops — which is what copying instead of importing produces, and
the reason `msiaf-gdprf-bridge/` and `reasoning-dial/gate_dial.py` both
import.

**Falsifier:** as `MF_006`. Nothing in any drop describes these as a
deliberate fork, and the missing pieces are exactly the repairs made
upstream.

---

## MF_012 — the drift is now detectable, and the gate is imported

**who:** A · **status:** SUPPORTED. Closes `MF_006` and `MF_011`.

`gate_fork.py` runs this folder's claims through the canonical gate by
import, so there is no copy here to go stale.

`../tools/check_gate_drift.py` finds any gate-family file anywhere in the
repo, matched on **content** rather than filename so `gate_2.py` is still
caught, and reports each as `IDENTICAL` or `DRIFTED`. Identical copies are
reported too — the only reason a copy is ever stale is that it started
identical. `../tests/test_gate_drift.py` fails the repo suite if one lands,
and plants a stale copy to prove the detector is not `CONSTANT_SILENT`.

**Falsifier:** a gate-family file the checker misses. The marker pairs are
in the tool; a copy that strips both of a pair would evade it, and would
also no longer be a usable copy of the gate.

---

## MF_013 — running the fork through the gate found a gap in the gate

**who:** A · **status:** SUPPORTED. Fixed upstream.

The residual count is a property of the coverage classifier — instrument
level. A physical-scope claim resting only on instrument-level quantities
was recorded `supported`:

```
claim : [supported] the measurement design has 3 unmeasured quantities
```

`G-LAYER`'s repair had covered generator-level support and said nothing
about instrument-level, which is the same category move one layer over.

Now fixed in `reasoning-gate/gate.py`: a physical-scope claim with **no
physical-level support at all** is `qualified`. The rule does not fire when
physical support is present, because a physical claim legitimately uses
instrument quantities as bounds.

The distinction it enforces is real. A quantity can be unmeasured because
nobody wrote the probe, or because it is not measurable, and a count of the
probe list cannot separate those.

**Falsifier:** a physical claim that rests only on instrument quantities and
is nonetheless a sound statement about the modelled system. Then the rule is
too broad and the right test is something narrower than "no physical
support".

**Evidence:** `gate_fork.py` FORK-ADJUDICATED;
`reasoning-gate/tests/test_gate.py`.

---

## MF_014 — K14-K18 close one of the three gaps, half of a second, none of the third

**who:** A · **status:** SUPPORTED

Five probes specified after `MF_010`. Adjudicated by reading protocols;
`coupling.py` is unmodified.

```
id     quantity               object_of    returns
K14    practice_rate          coupling     rate
K15    baseline_freshness     coupling     duration
K16    detection_latency      coupling     latency
K17    aggregation_depth      instrument   count
K18    budget_closure         design       audit
```

**K14 is the first probe in the arm that returns a rate.** `MF_010` turned
on exactly that: the delivered arm returned levels, ratios, slopes and
variances, all at fixed regime.

Against the three gaps:

| gap | verdict | via |
| --- | --- | --- |
| `whether trust in own sensing is a measurement or a belief` | **CLOSED** | K15 |
| `reversibility after regime shift` | **PARTIAL** | K14 |
| `coupling bandwidth` | **OPEN** | — |

`K15` closes its gap because injecting a small *known* deviation scores the
sensing apparatus against ground truth rather than against its own report,
which is the distinction the question asks for.

`reversibility` goes partial. K14 sweeps provisioning level, supplying the
gradient the stated falsifier needs and the delivered probes lacked. The
other half does not move: no proposed probe measures relearn rate *after*
the buffer is removed. K16 is a latency swept against staleness at **fixed
regime**; the predicted contrast is across a regime change.

`coupling bandwidth` does not move. Rate-of-use, staleness and latency are
three quantities; capacity is a fourth.

**K18's `object_of` is `design`**, outside `quantities.OBJECTS` — so by
`MF_008` it is a widen move rather than a probe and must not enter the
coverage pool. The specification says as much by calling it a widen move.

**Falsifier:** a reading of K16 under which its sweep crosses a regime
change rather than running at fixed regime. Then `reversibility` closes.

**Evidence:** `proposed_probes.py`.

---

## MF_015 — the mediation chain is the strongest part, and its lags are ordinal

**who:** A · **status:** SUPPORTED

```
practice_rate falls              K14
  -> baseline_freshness degrades   K15   lag 1
    -> detection_latency rises     K16   lag 2

all three while state variables read nominal

falsifier: if K14 predicts K16 with K15 controlled out,
           the causal chain is wrong
```

This is refutable by a partial correlation on three measured series, it
names which way the refutation cuts before the data exist, and it does not
depend on the effect being large. Nothing else in the fork has that shape.

What is not specified: **the lag units.** "lag 1" and "lag 2" are ordinal.
Whether the lag is hours or seasons decides the sampling rate, and a
mediation test sampled coarser than its own lag returns the chain collapsed
into a single step — which is indistinguishable from the chain being wrong,
and would be read as the falsifier firing.

Declare the units and it becomes a `G-RES` pair: sampling interval against
the lag being resolved.

**Falsifier:** a mediation estimate that is stable across sampling
intervals spanning the plausible lag range. Then the units do not matter and
this claim is unnecessary.

**Evidence:** `proposed_probes.py` §3.

---

## MF_016 — K17 is a widen move, and the schema does not catch it

**who:** A · **status:** SUPPORTED

`K17 aggregation_depth` was specified with `object_of = "instrument"`,
which **is** inside `quantities.OBJECTS`, so unlike `K18` it would have
been constructible as a legal quantity. `MF_008`'s type-system argument
does not reach it.

It still belongs in the widen arm, and the reason is what it points at.
Every K-probe takes a reading from the system under study. K17 takes none:
it decomposes the terms of the **model**, tags each component, and counts.
It applies unchanged to any model, and it would return a number on a design
with no system attached at all. That is a question pointed at a design,
which is the widen arm's whole content.

So the closed vocabulary is necessary and not sufficient. `MF_008` catches
probes whose `object_of` is outside `OBJECTS`; it cannot catch a probe with
a legal `object_of` that is nonetheless about the design. Nothing mechanical
separates those, and the adjudication here is by reading the protocol —
the same way `residual_audit.py` and `proposed_probes.py` adjudicate.

Landed as a `STRUCTURAL` entry in `widen.py`, which puts it under
`option()` with `object_of = "design"`, so `is_quantity()` drops it from
the coverage pool automatically.

**Prior-art correction carried with it:** the source notes match K17 to the
ecological fallacy. That is individual-from-aggregate inference and is the
wrong object. The mechanism K17 names is **sign reversal on
decomposition** — Simpson's paradox — with the Lucas critique and the
capital-aggregation debates as the nearer relatives.

**Falsifier:** a rule computable from the probe record alone — not from
reading the protocol — that separates design-directed probes from
system-directed ones. If one exists, this adjudication should be replaced
by it, and `MF_009`'s classifier problem gets smaller by the same move.

---

## MF_017 — `sweep` is a schema addition with teeth, and the schema has no room for it

**who:** A · **status:** REPAIRED (see *Repairs* at the end)

The rule as specified:

> every probe declares which spec variable it must be run across, and at how
> many levels. default `regime.variable`, min 2. Point-probes must declare
> `sweep=None` with a reason.

`quantities.probe()` has six fields — `arm`, `id`, `quantity`, `protocol`,
`reads`, `blind_to` — and none of them is `sweep`. So the rule is not
expressible in the delivered schema, and **0 of 17** measuring probes across
the three arms satisfy it. That is one schema gap, not seventeen oversights.

It is load-bearing rather than tidy. The spec's own falsifiers are
statements about a gradient — *"ratio flat across the provisioning
gradient"* — and a probe run at one setting of the control parameter cannot
participate in a claim about one. **The missing field and `MF_010`'s
unreachable falsifier are the same gap seen from two sides.**

All six newly specified probes pass. Resolving the default against the
spec's declared regime variable (`provisioning level`), 4 of 6 sweep the
regime variable — 2 by default and 2 by naming it directly — so the field
carries information on 2 of 6, and `K13`/`K14` spelling out the default is a
redundancy the schema should collapse rather than a choice. `K15` and `K16`
declare 3 levels against a minimum of 2, both being on the mediation chain
where 2 levels gives a slope with no curvature.

**Falsifier:** a probe whose declared sweep is inert — the number it returns
is the same at every level of the declared variable. Then the declaration is
decoration and the field should be dropped rather than added to the schema.

**Evidence:** `sweep_check.py` §1–§2.

---

## MF_018 — K13 and K11 close the last two gaps `MF_010` named

**who:** A · **status:** SUPPORTED

`MF_010` named three open questions no measuring arm reached. `MF_014` moved
one to CLOSED and one to PARTIAL. The remaining two now close.

**`reversibility after regime shift`: PARTIAL → CLOSED, on K13.**

`MF_010`'s objection was that the predicted contrast is a **rate** — fast vs
slow relearn once the buffer is removed — and every delivered K-probe
returned a level, ratio, slope or variance at fixed regime. `MF_014` then
credited K14 with half of it: the provisioning gradient the stated falsifier
needs. The other half was a post-shift time constant, and nothing had one.

```
K13  tau
     protocol   error vs trials-since-shift, fit tau
     sweep      provisioning_level at 2 levels
     returns    a time constant
     predicted  tau rises with provisioning; flat tau falsifies
```

`trials-since-shift` has no meaning without a regime change, so the probe is
measured across one by construction, and fitting `tau` returns the rate.
Swept across provisioning it supplies both halves at once. The prediction
falsifies in the direction that costs something, and the null (flat tau) is
reachable — not the `../null-harness/` `CONSTANT_SILENT` shape.

**`coupling bandwidth`: OPEN → CLOSED, on K11.**

`MF_014` left this open on the grounds that rate-of-use, staleness and
latency are three quantities and capacity is a fourth. `K11
information_rate` is the fourth — *"distinguishable environmental states
registered per unit time, by the actor's own sensors"* — and is explicitly
marked `not_` against K01 delay and K02 reliability: *"This is channel
capacity."* Its stated blind spot is the honest one: *"whether anything is
done with the states."*

**`K12` reaches the same distinction as `K15` by a second route.** *"Trust
is a measurement only if (b) was run"* makes `whether trust in own sensing
is a measurement or a belief` a precondition on reading `K12` at all, rather
than a separate probe. Two independent arrivals at one distinction.

**What is not closed:** every probe here is a specification. Nothing has
been run, the mediation lags are still ordinal (`MF_015`), and `sweep` is
still not in `quantities.probe()` (`MF_017`).

**Falsifier:** run K13 and find `tau` is not estimable — error against
trials-since-shift does not fit an exponential, so there is no time constant
to report. Then the gap reopens with a sharper shape: the predicted contrast
assumes a relaxation form nobody has checked.

**Evidence:** `sweep_check.py` §3–§4.

---

## MF_019 — the sixth and seventh stale gate copies, and three that are not

**who:** A · **status:** SUPPORTED

A drop bundled `gate.py` and `GUARDS.md` again. Both are the **pre-repair**
versions: `gate.py` differs from the repo's by 189 lines with all seven
repairs absent — no `diverged` on `close()`, no `scope` on `claim()`, no
denial records, no `layer_note` — and `GUARDS.md` differs by 48 lines with
`G-FIT` still under POST and `G-CTRL` under PRE only.

Neither is checked in. `MF_006` and `MF_011` recorded five such copies
across three drops; these are the sixth and seventh, and
`../tools/check_gate_drift.py` exists because of them. The convention is to
**import** the gate (`../msiaf-gdprf-bridge/`,
`../reasoning-dial/gate_dial.py`, `gate_fork.py`), never to copy it.

**The same drop shows the convention working.** `compare.py`,
`conventional.py` and `coupling.py` were re-delivered and are
**byte-identical** to the copies here — 0 differing lines each. Files that
live in exactly one place do not drift; files that get bundled into every
drop do. That is not a claim about care. It is a claim about how many
copies exist.

**Falsifier:** a bundled gate copy that is not stale. One would show the
staleness is incidental to bundling rather than caused by it.

---

## MF_020 — the falsifier check the drop asks for cannot be run from the spec

**who:** A · **status:** REPAIRED (see *Repairs* at the end)

The delivered `PROBES_K11_K18.py` header states the structural bug directly
and adds a requirement:

> coupling.py generated probes at a POINT while the stated falsifier
> ("ratio flat across the provisioning gradient") is about a GRADIENT. The
> generator could not emit a design capable of failing its own falsifier.
> **compare.py must flag any falsifier whose terms are not swept by any
> arm.**

`falsifier_sweep.py` is that check. `compare.py` is delivered verbatim and
is not modified.

**Result.** Delivered arms: **0 of 4** stated falsifiers reachable — not
because any probe is badly written, but because `quantities.probe()` has no
`sweep` field (`MF_017`), so the generator cannot emit a swept design at
all. With K11–K16: **4 of 4** reachable, across three swept variables
(`provisioning_level`, `time_since_clean_reference`, `baseline_staleness`).

**The check needs a second field that also does not exist.** The spec schema
has no `falsifiers` list — its ten fields are `system_id`, `description`,
`boundary`, `actors`, `provisioned`, `currently_measured`, `regime`,
`test_items_source`, `known_latency`, `open_questions`. So the four
falsifiers checked are **hand-transcribed from prose** and from individual
probes' `predicted=` lines.

K13 makes the gap concrete: it declares
`closes=["reversibility", "falsifier:ratio_flat"]`, and
`falsifier:ratio_flat` **resolves to nothing in any delivered file** — a
reference to a registry that has not been created.

Two schema gaps, one shape: a probe cannot say what it must be run across,
and a spec cannot say what would refute it. Between them a generator emits
a complete, well-formed design that is incapable of failing. Adding
`sweep` to the probe and `falsifiers: [{id, statement, terms}]` to the spec
makes the check three lines and removes the transcription entirely.

**It is a PRE-stage check.** It decides whether the design can fail before
anything is measured, which is `../reasoning-gate/`'s `G-CTRL` shape.

**Falsifier:** a stated falsifier whose terms are not a spec variable at
all — one that cannot be written as `terms: [...]` over the spec's own
vocabulary. Then the proposed schema is insufficient and the check needs
more than a term list.

**Evidence:** `falsifier_sweep.py` §1–§4.

---

## Repairs — MF_017 and MF_020

Both schema gaps are closed, and the check they blocked is now mechanical.

### `MF_017` — `sweep` on the probe

`quantities.probe()` takes `sweep=(variable, levels)`, defaulting to
`DEFAULT_SWEEP = "regime.variable"`, resolved against the spec's declared
regime by `resolve_sweep()`. It **refuses fewer than two levels**, and a
point probe must pass `sweep=None` *with* a `point_reason` — saying why a
single setting is the design rather than an omission.

The arms declare against it: 16 swept across three variables
(`provisioning_level`, `stimulus_severity` at 4 levels, `perturbation_size`
at 3), and one point probe — `C07`, the present-day questionnaire, whose
reason is that running it across the regime variable would be a different
probe rather than this one swept.

### `MF_020` — `falsifiers` on the spec

`systems/provisioning_calibration.json` declares five, each
`{id, statement, terms}`. `validate.py` asks for them and says what they are
for when they are absent. `K13`'s `closes=["falsifier:ratio_flat"]` **now
resolves** — it referred to a registry that had not been created.

`falsifier_sweep.py` reads both registries instead of hand-transcribing from
prose:

```
falsifier          terms                        arms now   with K11-K16
ratio_flat         provisioning_level           yes        yes
tau_flat           provisioning_level           yes        yes
threshold_flat     time_since_clean_reference   NO         yes
mediation_broken   baseline_staleness, prov...  NO         yes
gradient_flat      stimulus_severity            yes        yes

arms as they stand: 3 of 5      with K11-K16: 5 of 5
```

Two falsifiers are still unreachable by the arms as written, which is a
result rather than a repair: nothing sweeps `time_since_clean_reference` or
`baseline_staleness` until K15 and K16 land.

**The check keeps a reachable deny.** Section 4 puts three constructed
falsifiers through it — one reachable, one naming a variable no arm sweeps,
one mixed — and the last two are flagged. So every falsifier in this spec
coming back reachable is a property of the spec, not of the check.
