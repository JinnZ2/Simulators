# OBSERVER EXCLUSION — LEAD-TIME MEASUREMENT SPEC

Status: marker under exploration. Not a position under defence.
Licence: CC0. No attribution required.
Dated: 2026-08-24. Supersedes Q2_OBSERVER_EXCLUSION_SPEC.md, same date.

---

## 0. WHO THIS IS FOR

Anyone looking for a runnable question. A specified measurement with
falsifiers, on records that already exist. No new fieldwork, no
cohort access, no ethics approval. Literature-and-archive study.

It has not been run.

---

## 1. NAMING — READ THIS BEFORE CITING

This class is **observer exclusion**: a population holds a reading,
and no intake channel exists. No survey, no register, no path. The
question was formable and no instrument was pointed at it.

It is **not** the class previously filed as Q2 / *unaskable*. That
one is a different mechanism: a channel exists and **entry costs the
asker standing** — the label applies prior to content, so the
question is penalised rather than absent. That mechanism remains
filed separately and is the candidate exclusion mechanism for the
`uninstrumented` register under the name *affect routing*.

Two mechanisms, two names:
- **observer exclusion** — no channel.
- **unaskable / affect routing** — channel present, entry penalised.

An earlier draft of this spec collapsed them. Anything citing "Q2"
for the no-channel case is citing the collapsed version.

Also distinct from:
- **Q1 unasked** — no population identified as holding a reading.
- **Q3 superseded-but-current** — published correction not
  displacing the prior reading.

---

## 2. TRIGGER CASE

Wolf social structure. Captive-population research (Schenkel 1947;
Mech 1970) produced a dominance-contest model; Mech published a
field-based correction in 1999 (Can. J. Zool. 77:1196-1203) reporting
family groups with a breeding pair.

Field-observer populations in wolf range — hunters, trappers,
ranchers — were reportedly not observing a dominance contest while
the captive model was standard. One first-hand report. Seed, not
evidence.

**None of §5–§8 depends on this case.** The bias structure below is
a property of a censoring process and a coding protocol and holds
for any case with this shape.

---

## 3. THE MEASUREMENT

For case c:

    L_raw(c) = year_literature_adopts(c) − year_first_surviving_artifact(c)

`year_literature_adopts`: the establishing peer-reviewed publication,
OR the year a field body issues a position statement carrying the
reading. **Record both. They are different quantities** — in the
wolf case, 1999 and 2008 (veterinary) and 2019 (trainer association).

`year_first_surviving_artifact`: earliest dateable artifact from the
excluded population carrying the reading.

L_raw is not the quantity of interest. §4 gives the correction.

Report the full distribution including negative values. See §7.

---

## 4. THE CENSORING CORRECTION — THE STRUCTURAL CORE

`year_first_surviving_artifact` is set by when someone wrote it down
**and the artifact survived**, not by when the reading was held. Two
independent delays sit between holding and record:

- **δ_write** — holding to inscription.
- **δ_survive** — inscription to present availability, governed by
  an archival hazard.

Both push the measured date later. **L_raw is attenuated, and the
attenuation runs against the hypothesis.** At a stipulated 0.06/yr
archival hazard, a true ten-year lead measures −5.6 on average and
comes out positive only 47% of the time; a true twenty-year lead
measures 4.4.

Consequence worth stating plainly: **a positive L_raw survives this
bias.** A null does not distinguish "no lead" from "lead erased by
censoring."

**The estimator is already in the corpus.** Every artifact carries
two dates — artifact date and claimed observation date. Their
difference is a per-artifact draw from δ_write. Log both on every
record. This is not bookkeeping; it is the control.

    δ̂ = distribution of (artifact_date − claimed_observation_date)
    L_adj = L_raw − median(δ̂), reported with the full δ̂ spread

Limits of the estimator, stated: it recovers δ_write, not δ_survive;
it is itself right-censored, since artifacts recording long-past
observations are the ones most likely already lost; and artifacts
with no claimed observation date drop out non-randomly. Report the
proportion of records carrying both dates as a headline number. It
bounds everything else.

Report L_raw and L_adj side by side. Never L_adj alone.

---

## 5. CASE SELECTION AND ARTIFACT CODING — BOTH PRE-REGISTERED

**5a. Case selection.** Select on the existence of a documented
literature reversal, **before** examining what the excluded
population said. Reversal first, excluded reading second. The
reverse order selects on outcome.

Inclusion: documented change in the field's accepted reading; an
identifiable population with routine exposure to the same system; at
least one dateable artifact from that population addressing the same
variable.

Report the count dropped at each stage.

**5b. Artifact coding — the one bias running toward the hypothesis.**
Case selection being pre-registered does not protect the coding step.
Trade-press prose is frequently ambiguous about which reading it
carries, and an unblinded coder has a free parameter there. At 40%
ambiguous and an 80%-vs-25% acceptance gap between coders who know
the hypothesis and coders who don't, roughly 22% of the corpus enters
at earlier dates, inflating L directly.

Required:
- Coders blind to hypothesis, to case direction, and to the year
  the literature adopted.
- Strip or mask dates during the reading pass; attach after coding.
- Written coding rules fixed before the corpus is opened.
- Second coder on a sample; report agreement.
- Log ambiguous-rate as a reported quantity, not a footnote.

This is the only bias in the design pointing toward the hypothesis.
Every other one points away.

---

## 6. DATING — SOURCE LEADS

The excluded reading is oral by default and must be found in a
dateable artifact. Roughly by tractability:

1. **Trade and hobby periodicals** — trapper, hunting, ranching,
   farming press. Continuous, archived, full of first-hand
   behavioural accounts, largely undigitised. The undigitised part
   is why they are unsearched and why the question is available.
2. **Agricultural extension records** — land-grant services, a
   century of field reports; many digitised.
3. **Wildlife agency hearing testimony** — dated, transcribed,
   occupation-attributed, public record.
4. **Depredation and bounty claim records** — behaviour description
   attached to date and location.
5. **Oral history collections** — state historical societies, tribal
   archives. Dated at collection, not at observation; §4's two-date
   rule is mandatory here.
6. **Predator control agency field notes** — government trappers
   filed reports; federal and state archives.

---

## 7. THE INVERSE — MANDATORY

Collect cases where the excluded reading was **wrong** and the
literature right, with equal effort. Not balance — the only thing
that makes L interpretable. Without it, the design cannot separate
"this population holds accurate readings the literature lacks" from
"this population holds many readings and some were right."

Direction is examined only after §5a selection closes.

---

## 8. FALSIFIERS — AND WHAT SEPARATES THEM

The earlier draft listed three falsifiers that return the same
observation: L near zero, the reading late or absent. §4's δ̂ is what
separates them.

**F1 — recovery failure.** Artifacts not found at sufficient density.
*Signature:* few records, and those carrying both dates show large or
uninformative δ̂. **Publishable null.** It bounds what any future
study can do and should be written up as a result.

**F2 — no lead.** *Signature:* adequate record density, δ̂ estimated
with reasonable spread, and L_adj distributed around zero.

**F3 — accuracy at base rate.** Once the §7 arm is collected, the
excluded reading is right no more often than chance. Independent of
δ̂; independent of L.

**F4 — publication lag, not exclusion.** The field's own observers
held the same reading in the same window and it took the same years
to surface. *Proposed control:* field biologists' unpublished notes,
conference abstracts, correspondence.

**F4's control is better archived than the thing it controls.**
Institutional archives against undigitised trade press. Simulated
with both populations holding the reading in the same year, the
record shows the field first 74% of the time. So F4 gets accepted on
an archiving difference rather than a holding difference. The
excluded population needs roughly an eight-year true lead before the
record shows it first more often than not.

F4 is therefore **not a clean falsifier as posed**. To use it, run
§4's two-date estimator separately on each population and compare
δ̂ distributions before comparing dates. If the δ̂ distributions
differ, the raw date comparison is uninterpretable and F4 must be
reported as untestable on this corpus.

---

## 9. WHAT IT DOES NOT MEASURE

- Not general reliability of the population.
- Not transmission. Convergence is not causation; independent
  arrival at the same reading is the expected case.
- Not any individual observer's accuracy.
- Not the mechanism of exclusion — separate question, separate
  instrument, and see §1 for why the two mechanisms must not be
  merged into one.

L measures interval only.

---

## 10. ADJACENT, IF L SURVIVES

What an intake channel costs. Rail (FRA C3RS) and air (FAA ASRS) run
confidential non-punitive reporting held outside the employer, both
with measured effects. Existing, costed, operating designs for
receiving observation from a population the formal system does not
poll. Transfer to field observation is untested.

---

## 11. KNOWN LIMITS

- Seed case is n=1 on one first-hand report. Reason to look, not
  evidence.
- "Excluded population" is not operationally defined here. Needs a
  criterion for routine exposure and a criterion for channel absence.
  Neither is written.
- L conflates two literature events. Recording both is a workaround.
- δ̂ recovers δ_write only; δ_survive remains stipulated, and the
  0.06/yr figure above is a placeholder, not a measurement. Anyone
  running this should estimate it from a known-complete archive
  before relying on L_adj.
- Labour bound to physical archives biases toward catalogued states
  and decades. This is a coverage problem **and** a bias in L.
