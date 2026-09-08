# CLAIM TABLE — enclosure-first-residual

Claims from building work order K. `WORK_ORDER.md` is untouched.

**REFUTATION PROTOCOL.** The fixtures are the claim. A check that fails
updates the claim or the fixture, never the tool's output to suit it.
Where the order's own decision table is what the fixtures refute, the
table is kept runnable and printed, and the corrected reading is the
updated claim.

All numbers below are from `python3 enclosure_first_residual.py demo`
with the seeds in `FIXTURES`; the full text is `samples/demo.sample.txt`.

---

### EFR_001 — the null gate runs and prints first, and it refuses a trait

Every term that reaches a fit prints the null band before the between
fit; the selftest asserts the order of the two lines in every block.

| fixture | null band | observed between residual | gate |
|---|---|---|---|
| F2 trait only | [0.9143, 0.9995] | **0.9807** | inside, `UNKNOWN_measurable` |
| F1 enclosure only | [0.9041, 0.9994] | 0.2015 | below, proceed |

F2 has a strong trait (sd 2 against noise sd 1) and the between residual
is 0.98. A trait-first intake would have reported a trait here. The order
says the enclosure terms had no traction, so nothing is a trait candidate
yet, and that is what returns.

**Falsifier:** a panel whose observed between residual sits inside the
null band and still yields a trait return.

**Status: SUPPORTED.**

---

### EFR_002 — `option_set_size` alone overstates, on every fixture that fits

The order's NOTE says the nominal count will overstate. The decision
model uses `effective_exits` (+ `reversible_count`); the nominal model
uses `option_set_size` only. Both are fit and printed.

| fixture | residual, effective | residual, nominal only |
|---|---|---|
| F1 | 0.2015 | 0.4777 |
| F3 | 0.5581 | 0.7154 |
| F4 | 0.3430 | 0.4557 |
| F5 | 0.2028 | 0.4364 |
| F7 | 0.2760 | 0.6663 |

The nominal model leaves more behavior unexplained in every case, which
is the residual a trait attribution would then absorb.

**Falsifier:** a panel where the nominal count fits as well as the
effective count, which would mean unreachable or unaffordable exits are
doing work.

**Status: SUPPORTED** (on generated panels whose behavior was made from
`effective_exits`; the field version of this claim is open).

---

### EFR_003 — the step-4 table as written puts an enclosure-only panel in the confound cell

F1: `behavior = 10 - effective_exits + noise(sd 1)`, forty persons, two
exogenous windows each, no trait, no selection.

```
between arm   residual 0.2015  CI [0.1415, 0.2839]
within arm    residual 0.4291  CI [0.2460, 0.5855]   null band [0.8184, 0.9982]
ratio         2.1297           CI [1.1888, 3.4953]   table cell: >
literal return: VARIABLE_UNIDENT(confound: residual_within 0.429 > residual_between 0.201)
```

With `y = a + b e + eps`, no trait:

```
r_between = s^2 / (b^2 V[e] + s^2)
r_within  = 2 s^2 / (b^2 V[delta e] + 2 s^2)
```

They are equal only when `V[delta e] = 2 V[e]`, i.e. when the two windows
are independent draws. In a panel, enclosure at t1 is close to enclosure
at t0, so `V[delta e] < 2 V[e]` and `r_within > r_between`. The order's
`>` cell is reached by the simplest possible enclosure-only data.

**Falsifier:** a normalisation of the two residuals under which F1 lands
in `<<` while F3 (`EFR_004`) lands in `~`. `EFR_004` shows why there is
none.

**Status: REFUTED as written.** The table is retained and runnable
(`--table-literal`), its cell is printed on every run, and the claim is
updated to the corrected reading in `EFR_005`.

---

### EFR_004 — a stable trait only lowers the ratio, so the table's cells are ordered backwards

F3 is F1 plus a person trait with sd 2.

| | F1 (no trait) | F3 (trait sd 2) |
|---|---|---|
| between residual | 0.2015 | 0.5581 |
| within residual | 0.4291 | 0.4064 |
| ratio | **2.1297** | **0.7282** |
| table cell | `>` | `~` |

The trait enters the between residual (`V[t]` in both numerator and
denominator, pushing toward 1) and cancels in the differenced within arm.
So adding a trait always moves the ratio *down*. The table places the
trait cell (`~`) above the enclosure cell (`<<`) on the ratio axis. Those
two facts cannot both hold: whatever value separates F1 from F3, F3 is
below it, so if F1 is read as the enclosure account then F3 is read as
enclosure too and the trait is missed; if F3 is read as trait then F1 is
read as something above trait, which the table calls confound.

**Falsifier:** a generative model in which a stable person-level term
raises `residual_within / residual_between`.

**Status: SUPPORTED. The ordering, not any threshold, is the problem.**

---

### EFR_005 — a corrected reading of the same two arms lands all seven fixtures

Same ingredients the order asked for (null, between, within, ratio, CI)
plus one the fixtures forced: the person-stable share of the between
residual, against a null from shuffling person labels.

```
within residual below its null band?   no  -> VARIABLE_UNIDENT (confound)
                                       yes, but CI reaches back in -> UNKNOWN_measurable
person-stable share above its null?    yes -> TRAIT_RESIDUAL
                                       no  -> ENCLOSURE_DOMINANT
```

| fixture | within vs null | person-stable share vs null | return |
|---|---|---|---|
| F1 | 0.429 < [0.818, 0.998] | 0.430 vs [0.336, 0.631] not above | `ENCLOSURE_DOMINANT(0.571, [0.414, 0.754])` |
| F3 | 0.406 < [0.822, 0.999] | **0.855** vs [0.343, 0.629] above | `TRAIT_RESIDUAL(0.477, [0.276, 0.669])` |
| F4 | **0.869** inside [0.801, 0.997] | 0.573 vs [0.347, 0.662] not above | `VARIABLE_UNIDENT` (confound) |

`ENCLOSURE_DOMINANT`'s fraction is `1 - residual_within`: the share of
within-person behavior change that enclosure change explains.
`TRAIT_RESIDUAL`'s fraction is `(person-stable share) x residual_between`:
the share of between-arm behavior variance that enclosure leaves *and*
that sits with the person, with a cluster bootstrap over persons for the
CI. F3's return also notes that enclosure moves behavior within person
(fraction 0.594): a trait that survived the control is a trait beside an
enclosure effect, not instead of one.

**Falsifier:** a generative model among the four branches that the
reading sends to the wrong return; or a panel where the person-stable
share is above null with no trait in the model.

**Status: SUPPORTED on the fixtures.** The person-stable check with two
windows per person is a two-observation ANOVA share and its null band is
wide ([0.34, 0.63]); more windows per person narrow it.

---

### EFR_006 — the confound row has no return-type entry; G's `VARIABLE_UNIDENT` is the peer class

The order's step 4 has three rows; its RETURN TYPE list has entries for
the first two and for the gates, but not for *confound, likely selection
into windows; report and stop*. Returning it as `UNKNOWN_measurable`
would conflate it with the null gate; returning it as `BLOCKED` would
name no blocker.

G's enum has `VARIABLE_UNIDENT`: the variable doing the work cannot be
identified from this design. That is what a between association not
reproduced within person means. The record carries `kind: CONFOUND` and
`return_class: VARIABLE_UNIDENT`, and `label()` prints both.

**Falsifier:** a reading of G under which `VARIABLE_UNIDENT` means
something other than this.

**Status: SUPPORTED. A choice, recorded rather than made quietly.**

---

### EFR_007 — a chosen change is out of envelope even when the between arm has traction

F5 is F1 with every second window's `change_origin` set to `chosen`.

```
envelope: 40 within pairs, 0 exogenous, 40 chosen (excluded)
between arm  residual 0.2028  CI [0.1343, 0.2737]   (well below the null band)
-> OUT_OF_ENVELOPE
```

The between arm is printed. It is not returned as a score. The order's
envelope says reverse causation is unresolvable when the person chose the
change, and a strong between fit is exactly what reverse causation would
also produce.

Pairs of `unknown` origin are excluded the same way and counted
separately; a panel with only unknown-origin pairs returns
`BLOCKED(no_within_person_windows)` with the count in the reason, not
`OUT_OF_ENVELOPE`, because nothing established that the person chose.

**Falsifier:** a case where a chosen change should still enter the
within arm.

**Status: SUPPORTED.**

---

### EFR_008 — the unit is the person-window, and a person-level panel is blocked, not scored

F7 is F1 with one window per person.

```
flagged: 40 single-window person(s) go to the between arm only
between arm  n=40  residual 0.2760  CI [0.1578, 0.4265]
-> BLOCKED(no_within_person_windows)
```

A person-level design would have returned the between residual 0.276 as
its result and called the rest trait. Here the between arm is reported,
the forty persons are flagged by id, and the return is `BLOCKED` with the
order's own blocker name. The other blocker, `unoperationalized_term`, is
F6.

**Falsifier:** a single-window panel from which the within arm can be
run.

**Status: SUPPORTED.**

---

### EFR_009 — method-layer present and absent give the same returns; the branch set round-trips through F

```
selftest: PASS (0 checks failed)  method-layer=present
selftest: PASS (0 checks failed)  method-layer=absent      (METHOD_LAYER_PATH=none)
```

Present: the five mirrored `ReturnClass` values are checked equal to
`G.ReturnClass`; every return is constructed as a `G.CriterionResult`,
so `SCORED` without a value raises; the branch set is built with
`F.BranchSet.from_dict`, serialized, and reloaded equal. The F1 run
eliminates `trait_plain` with `eliminated_by` naming the run and the
return; the other three branches stay open, because nothing in this
instrument alone eliminates them.

Absent: same returns, same branch-set JSON (schema 1.0), record says so.
The dependency is located, never vendored; the CI runner has no
method-layer checkout and runs the absent path, with two tests skipped
by name.

**Falsifier:** a return that differs between the two modes, or a
branch-set JSON F refuses to load.

**Status: SUPPORTED.**
