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
