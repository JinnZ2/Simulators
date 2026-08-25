# CLAIM_TABLE — `observer-exclusion`

Claims about `MARKER.md`, delivered verbatim and modified by nothing here.
Computed by `archival_bias.py`.

REFUTATION_PROTOCOL: a claim about what a censoring process does to a
measurement is settled by simulating the censoring. A claim about a label
is settled by quoting both uses. Nothing here is settled by a literature
fact, because none is reachable from this environment.

---

### OE_001 — the spec is the strongest artifact this family has produced, and two features are why

**§5 selects cases on the existence of a literature reversal, before
looking at what the excluded population said.** That is pre-registration
against selection-on-outcome, written into the design rather than
disclosed as a limit — and it is exactly the failure
`criterion-symmetry`'s seed set had (every seed a high-agreement case,
inverse branch `CONSTANT_SILENT`). Same repair as `UNI_126` and
`SHB_023`, applied in advance.

**§6 makes the negative arm mandatory and says why in one sentence:**
*"the only thing that makes L interpretable… without it, the measurement
cannot distinguish 'this population holds accurate readings the literature
lacks' from 'this population holds many readings and some were right.'"*
That is the `null-harness` base-rate argument, unprompted.

**§7 F1 is a publishable null.** *"The reading may exist and be
unrecoverable. This is a real outcome and should be published as one — it
bounds what any future study can do."* Bounded-null discipline named in
advance, which is `QA_004`'s standard met by the same family one drop on.

**Status: SUPPORTED. The honest positive, and it is the larger part of
this table.**

---

### OE_002 — L is attenuated by archival delay, and the bias is conservative

`year_excluded_reading_dateable` is set by when someone **wrote it down**
and the artifact survived and was catalogued — not by when the population
held the reading. That is a censoring process with a direction.

Simulated at a stipulated archival hazard of 0.06/yr (mean delay 16.7 y):

| true lead | observed mean | recovered | P(observed > 0) |
|---|---|---|---|
| 5 y | −10.6 | — | 0.27 |
| 10 y | **−5.6** | — | **0.47** |
| 20 y | 4.4 | 0.22 | 0.71 |
| 50 y | 34.4 | 0.69 | 0.95 |

**A true ten-year lead measures negative on average and is positive 47% of
the time** — a coin flip on a real effect twice the mean archival delay.

The bias runs **against** the hypothesis, which is the good direction: a
positive L survives it. §10 names the labour bias as a coverage problem;
it is also a bias in L itself, and its sign is the useful part.

**Falsifier:** an archival hazard high enough that the delay is negligible
against the leads being measured.

**Status: SUPPORTED.**

---

### OE_003 — F4's control is better archived than the thing it controls, which biases toward accepting F4

§7 F4 names publication-and-consensus lag as *"the most likely
confound"* and proposes as control: *"field biologists' unpublished notes,
conference abstracts, or correspondence."*

Those are **institutionally archived** — named-scientist collections,
society proceedings — where the excluded population's artifacts are trade
periodicals and hearing testimony, which §4 says are *"largely
undigitised."* Better archived means surfacing earlier relative to when
held.

Simulated, both populations holding the reading in the same year, hazards
0.18 against 0.06:

| true excluded lead | field appears first | excluded appears first |
|---|---|---|
| **0 y** | **0.74** | 0.21 |
| 5 y | 0.54 | 0.43 |
| 10 y | 0.40 | 0.58 |
| 40 y | 0.06 | 0.93 |

**At a true lead of zero the record shows the field first 74% of the
time.** F4 would be accepted on a difference in archiving, not a
difference in holding. The excluded population needs a true lead of about
**8 years** before the record shows it first more often than not.

Also conservative. Also collapses F4 into F1.

**Falsifier:** equal archival hazards for the two populations.

**Status: SUPPORTED.**

---

### OE_004 — F1, F2 and F4 are not separable on the L distribution alone

The spec lists them as three falsifiers. Under archival censoring they
return the **same observation**: L near zero, with the excluded reading
appearing late or not at all.

- F1 — artifacts too sparse.
- F2 — no systematic lead.
- F4 — the field held it too.

`OE_002` and `OE_003` show sparse archives producing F2's and F4's
signatures without either being true.

**The separator is already in §4 and is not used as one.** The recording
rule says to log *"the artifact date, the claimed observation date, and
whether they differ."* That difference **is an estimate of the archival
delay**, per artifact. With it, the censoring can be estimated from the
same corpus and the three falsifiers come apart. Without it, a null result
is uninterpretable and the study cannot say which falsifier fired.

**Falsifier:** a reading of the spec on which a null L distinguishes F1
from F2.

**Status: SUPPORTED. The fix is a field the spec already collects, promoted
from bookkeeping to control.**

---

### OE_005 — the one bias running toward the hypothesis is unguarded

§5 pre-registers **case** selection. Nothing pre-registers **artifact
coding**.

The excluded reading is oral, recovered from trade-press prose and hearing
testimony, and much of it will be ambiguous about whether it carries the
corrected reading. A coder who knows which way the literature moved has a
free parameter. If 40% of artifacts are ambiguous and an unblinded coder
accepts 80% where a blind coder accepts 25%, the difference is **22% of
the corpus**, entered as earlier dates — which inflates L directly.

Every other bias identified here runs against the hypothesis. This one
runs toward it, and it is the one with no provision.

Standard, cheap fix: **code artifacts blind to the direction of the
reversal.** The spec guards selection and not coding, and coding is where
the leniency lives.

**Falsifier:** a coding protocol in the spec that fixes acceptance criteria
before the reversal direction is known.

**Status: SUPPORTED.**

---

### OE_006 — `Q2` now names two different mechanisms, three drops apart

`question-availability/MARKER.md`:

> **Q2 — unaskable.** Posing the question costs the asker standing… the
> label is applied prior to content, so the content never reaches
> evaluation.

Here:

> **Q2 is: reading held, no channel.** … no instrument was pointed at
> them. There is no survey, no register, no intake path.

Two different mechanisms. The first is **a channel that exists and
penalises entry**; the second is **no channel at all**. This spec's §1
distinguishes itself from *"solicited and rejected"* and not from the
previous Q2, because the previous Q2 has been overwritten.

Case `021`'s sense substitution, inside the family's own vocabulary —
fourth instance in this tree after `nonidentity-census` T1-3's `state` and
`notes/`'s `parity`.

**It has a consequence.** `QA_003` identified the *previous* Q2 as
`affect routing`, the mechanism `uninstrumented` recorded as named in
prose and filed nowhere. **That identification does not transfer.** So
whoever files a twelfth mechanism has to say which Q2 they are filing —
and if they file this one, `affect routing` is still unfiled.

The resolution is in the spec's own title: **OBSERVER EXCLUSION** is the
right name for no-channel, and *unaskable* should keep the cost mechanism.

**Falsifier:** a reading on which the two definitions name one mechanism.

**Status: SUPPORTED.**

---

### OE_007 — everything about the trigger case is carried and unchecked

Schenkel 1947, Mech 1970, Mech 1999 (Can. J. Zool. 77:1196–1203), the
captive-versus-field distinction, the content of the correction. Every one
is carried from the spec. The egress gate refuses the sources — `MS_004`
status.

**Nothing in `OE_002`–`OE_005` rests on any of it.** Those are properties
of a censoring process and of a coding protocol, and they hold for any
case with the stated structure.

The spec is already explicit that the seed is *"n=1 and rests on one
first-hand report. It is a reason to look, not evidence"* — which is the
right posture and is why the audit could go to the design instead of the
case.

`notes/study_watch.py` runs on a runner that reaches the citation
databases. The Mech 1999 citation is the cheapest thing in this folder to
verify and is the third item in this drop family the watcher exists for.

**Status: UNVERIFIED, and nothing depends on it.**

---
---

# `OE_008`–`OE_012` — claims about `SPEC_V2.md`

v2 is delivered verbatim alongside v1; both stay inspectable. It
supersedes v1 and **adopts all six v1 findings** — the naming split, the
attenuation, F4's differential archiving, δ̂ as separator, coding
pre-registration, and the case not being load-bearing. Six for six,
checked by quotation.

So the work below is on what is **new** in v2.

---

### OE_008 — §4's correction has its sign inverted, and it is the section v2 calls its structural core

> δ̂ = distribution of (artifact_date − claimed_observation_date)
> **L_adj = L_raw − median(δ̂)**

Let `H` be the year the population held the reading, `A` the year of the
first **surviving** artifact carrying it, `P` the year the literature
adopts. `A = H + D` with `D ≥ 0`, and δ̂ estimates `D`.

```
L_true = P − H
L_raw  = P − A = P − (H + D) = L_true − D
     ⇒  L_true = L_raw + D
```

**The correction adds. The spec subtracts.** Simulated at a true lead of
20 years:

| | value | error |
|---|---|---|
| median δ̂ | 15.00 | |
| `L_raw` (uncorrected) | 5.08 | −14.92 |
| **`L_raw − median(δ̂)` — as written** | **−9.92** | **−29.92** |
| `L_raw + median(δ̂)` | 20.08 | +0.08 |

**The correction as written moves the estimate further from the truth than
not correcting at all.** It doubles the bias it exists to remove, and it
turns a positive true lead into a negative measured one.

§4's own prose states the direction: *"L_raw is attenuated, and the
attenuation runs against the hypothesis."* Subtracting a positive delay
attenuates it again.

One character. It inverts the section v2 names "THE STRUCTURAL CORE", and
every downstream statement about `L_adj` — §8's F2 signature, the
instruction to report `L_raw` and `L_adj` side by side — inherits it.

**Falsifier:** a derivation on which `year_first_surviving_artifact` can
precede the holding year, which would make `D` signed rather than
non-negative.

**Status: SUPPORTED. Arithmetic, not interpretation.**

---

### OE_009 — §8's F4 repair checks the term §4 says the estimator does not recover

§4 states the limit plainly: δ̂ *"recovers δ_write, not δ_survive."*

§8 then proposes, as the way to make F4 usable:

> run §4's two-date estimator separately on each population and compare
> δ̂ distributions before comparing dates.

But the F4 bias is in **survival**, not retrospection. Field
correspondence is not written with less lookback than trade press; it is
more likely to **survive**.

Simulated — two populations with **identical** writing behaviour and
retrospection, survival 0.10 against 0.60:

| | excluded | field |
|---|---|---|
| median δ̂ | 6.0 | 6.0 |
| **gap the §8 test would see** | **0.0** | |
| median years to first surviving record | 29.0 | 5.0 |
| **record shows field first** | | **86%** |

**The δ̂ distributions are identical and the bias is fully present.** The
§8 test returns *comparable* on exactly the corpus where the comparison is
invalid, so its *"report as untestable"* branch is unreachable by
construction — `null-harness` `CONSTANT_SILENT` on the one branch that
protects F4.

**The repair is already in §11**, written for another purpose: *"estimate
[δ_survive] from a known-complete archive."* Run that **per population**
and F4 becomes testable. The spec has the tool and points it at the other
term.

**Falsifier:** a mechanism by which differential survival shows up in
retrospection distance.

**Status: SUPPORTED.**

---

### OE_010 — the choice of literature event costs more than the censoring correction recovers

§3 says *"Record both. They are different quantities"* and then names
**three** for the wolf case:

| event | year |
|---|---|
| peer-reviewed publication | 1999 |
| veterinary body | 2008 |
| trainer association | 2019 |

**Spread: 20 years.** The archival delay the whole of §4 exists to correct
is ~17 years at the spec's own stipulated hazard.

So the definitional choice of *which* literature event dominates the
censoring correction in magnitude. §11 calls recording both *"a
workaround"*; the ordering of magnitudes says it is more than that — the
three L values are **three different measurements** and must not share a
distribution. §3's instruction to *"report the full distribution of L"*
needs to be three distributions, or one with the event type declared per
case.

**Falsifier:** an adoption-event spread small against the archival delay.

**Status: SUPPORTED.**

---

### OE_011 — the six adopted findings are transcribed correctly

Worth checking rather than assuming, because a spec quoting an audit's
figures is a copy and copies drift (`MF_019`, and five stale gate copies
before it).

| figure | computed | quoted |
|---|---|---|
| true 10-y lead measures | −5.56 | −5.6 |
| positive fraction | 46.6% | 47% |
| true 20-y lead measures | 4.44 | 4.4 |
| field appears first | 73.9% | 74% |
| true lead needed | 8.00 | eight years |
| corpus entering early | 22.0% | 22% |

Six for six, within rounding. No drift.

**Status: SUPPORTED.**

---

### OE_012 — v2's §1 resolves `OE_006` exactly, and files the other mechanism where it belongs

> **observer exclusion** — no channel.
> **unaskable / affect routing** — channel present, entry penalised.
> An earlier draft of this spec collapsed them.

That is `OE_006`'s finding adopted with its resolution — and it goes one
step further than the audit did, by naming the second mechanism *affect
routing* and stating it *"remains filed separately and is the candidate
exclusion mechanism for the `uninstrumented` register."*

Which closes the loop `QA_003` opened: `affect routing` was recorded three
drops ago as named in the register's literature note and filed nowhere,
and the twelfth ordinal now has an unambiguous owner. `uninstrumented`'s
`MECHANISMS` tuple still holds eight and `affect_routing` is still not in
it — the filing is named, not done.

**Falsifier:** `affect_routing` appearing in the register's tuple, which
would close it.

**Status: SUPPORTED. The naming is settled; the filing is not.**
