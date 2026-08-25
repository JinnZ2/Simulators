# Q2 — OBSERVER EXCLUSION: LEAD-TIME MEASUREMENT SPEC

Status: marker under exploration. Not a position under defence.
Licence: CC0. No attribution required. Take it and run it.
Dated: 2026-08-24

---

## 0. WHO THIS IS FOR

Anyone looking for a runnable question. This is a specified
measurement with a falsifier attached, on data that already exists
in the public record. It needs no new fieldwork, no cohort access,
no ethics approval. It is a literature-and-archive study.

It has not been run. That is the reason it is written down.

---

## 1. THE SHAPE

Some populations hold high-hour, longitudinal, same-site observation
of a system, and are outside the channel that supplies observations
to the literature on that system.

Working examples of such a population: hunters, trappers, ranchers,
farmers, commercial fishers, long-haul operators, field maintenance
crews.

The condition is not that these observations were solicited and
rejected. The condition is that no instrument was pointed at them.
There is no survey, no register, no intake path. The question was
formable and was not entered.

This is distinct from:
- Q1, unasked — no population identified as holding a reading.
- Q3, superseded-but-current — a published correction failing to
  displace the prior reading.

Q2 is: reading held, no channel.

---

## 2. TRIGGER CASE

Wolf social structure.

Captive-population research (Schenkel 1947; Mech 1970) produced a
dominance-contest model. Mech published a field-based correction in
1999 (Can. J. Zool. 77:1196-1203) reporting packs as family groups
with a breeding pair, no dominance contest.

Field-observer populations in wolf range — hunters, trappers,
ranchers — were not observing a dominance contest during the period
the captive model was current. This is a first-hand report from one
such observer and is the seed for the case, not evidence for it.

If that reading was in fact widespread and dateable, the excluded
population converged on the corrected model while the captive model
was the literature standard.

The size of that interval is the measurement.

---

## 3. THE MEASUREMENT

**LEAD-TIME (L)**

For a case c:

    L(c) = year_literature_adopts(c) - year_excluded_reading_dateable(c)

where:

- `year_excluded_reading_dateable` = earliest year the excluded
  population's reading appears in a dateable artifact (see §4).
- `year_literature_adopts` = year of the peer-reviewed publication
  that establishes the reading in the field, OR the year a field
  body issues a position statement carrying it, whichever is being
  measured. Record both; they are different quantities.

L > 0: the excluded reading preceded the literature.
L ≈ 0: no lead.
L < 0: the literature preceded the excluded reading.

**Report the full distribution of L, including negative values.**
See §6. An instrument that only collects L > 0 cases is selecting
on outcome and measures nothing.

---

## 4. DATING THE EXCLUDED READING — THE HARD PART

This is where the study lives or dies. The excluded reading is oral
by default. It has to be found in a dateable artifact.

Candidate sources, roughly in order of tractability:

1. **Trade and hobby periodicals.** Trapper, hunting, ranching, and
   farming magazines, published continuously, archived, and full of
   first-hand behavioural accounts. Largely undigitised, which is
   why they are unsearched, which is why the question is available.
2. **Agricultural extension records.** Land-grant university
   extension services collected field reports for a century.
   State archives; many digitised.
3. **Wildlife agency hearing testimony.** Public comment on
   depredation, season-setting, and management rules. Dated,
   transcribed, attributed by occupation, and public record.
4. **Depredation and bounty claim records.** Behavioural description
   attached to a date and a location.
5. **Oral history collections.** Held by state historical societies
   and tribal archives. Dated at collection, not at observation —
   record both dates.
6. **Predator control agency field notes.** Government trappers
   filed reports. Federal and state archives.

Recording rule: log the artifact date, the claimed observation date,
and whether they differ. A 1980 interview describing a 1950
observation is one data point with two dates, not two data points.

---

## 5. CASE SELECTION

Select cases on the **existence of a literature reversal**, before
looking at what the excluded population said. Reversal first,
excluded reading second. Reversing the order selects on outcome.

Inclusion criteria for a case:
- A documented change in the field's accepted reading.
- An identifiable observer population with routine exposure to the
  same system.
- At least one dateable artifact from that population addressing the
  same variable.

Candidate domains beyond wolves — unverified, listed as leads:
- Predator behaviour and livestock interaction generally.
- Soil condition and tillage effects.
- Insect population dynamics on continuously worked ground.
- Fish stock behaviour and movement.
- Weather-response behaviour in herd animals.

---

## 6. THE INVERSE — MANDATORY

Collect and report cases where the excluded population's reading was
**wrong** and the literature was right, with equal effort.

This is not balance. It is the only thing that makes L interpretable.
Without the negative arm, the measurement cannot distinguish
"this population holds accurate readings the literature lacks" from
"this population holds many readings and some were right."

Design the search so the negative arm cannot be under-collected:
select cases in §5 before examining direction, and report the count
of cases dropped at each stage.

---

## 7. FALSIFIERS

The marker fails if:

**F1.** Dateable artifacts from the excluded population cannot be
found at sufficient density. The reading may exist and be
unrecoverable. This is a real outcome and should be published as
one — it bounds what any future study can do.

**F2.** L is distributed around zero. No systematic lead.

**F3.** Accuracy of the excluded reading is at or below base rate
once the negative arm is collected.

**F4.** The apparent lead is explained by the literature's own
publication and consensus lag rather than by exclusion — i.e. the
field's internal observers held the same reading at the same time
and it took the same number of years to surface. **This is the most
likely confound.** Control: check whether the reading appears in
field biologists' unpublished notes, conference abstracts, or
correspondence during the same window.

---

## 8. WHAT IT DOES NOT MEASURE

- Not whether the excluded population is more reliable in general.
- Not whether their reading is causally prior to the correction.
  Convergence is not transmission. A field biologist reaching the
  same conclusion independently is the expected case.
- Not a claim about any individual observer's accuracy.
- Not the mechanism of exclusion. That is a separate question and
  needs a separate instrument.

L measures interval only.

---

## 9. ADJACENT, IF L > 0 SURVIVES

The follow-on question, which is cheaper than it looks: what would
an intake channel cost. Rail (FRA C3RS) and air (FAA ASRS) both run
confidential non-punitive reporting held outside the employer, and
both have measured effects. Those are existing, costed, operating
designs for receiving observation from a population the formal
system does not poll.

Whether that structure transfers to field observation is untested.

---

## 10. KNOWN LIMITS OF THIS SPEC

- Seed case is n=1 and rests on one first-hand report. It is a
  reason to look, not evidence.
- "Excluded population" is not yet operationally defined. A working
  definition needs a criterion for routine exposure and a criterion
  for channel absence. Neither is written here.
- L conflates two different literature events (first publication vs
  body adoption). Recording both is a workaround, not a fix.
- Undigitised sources mean the search is labour-bound, and labour
  bound to physical archives biases toward whichever states and
  decades happen to be catalogued.
