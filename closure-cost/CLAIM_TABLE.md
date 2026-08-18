# CLAIM TABLE — CLOSURE COST

---

**C1.** Response delay after an unexpected event tracks whether the variable
was carried as live beforehand, not the severity of the event.

*Falsifier:* matched exposure and matched severity, where people who had
carried the variable at a low live probability show no latency advantage over
people who had closed it.

*Status:* untested. No case in the file has a latency distribution.

---

**C2.** A closed variable has no handling class attached, because none was
needed. The delay when it fires is categorisation, not reaction.

*Falsifier:* a delay that persists after the event has been correctly
categorised, of the same magnitude as the pre-categorisation delay.

*Status:* untested and currently unfalsifiable with available data —
categorisation time is not separately recorded anywhere in the sources.

---

**C3.** A procedure gap is a downstream readout of the closed prior, not an
independent explanation of non-response.

*Falsifier:* a population that rates an event as a live possibility, has the
procedure available to them, and still does not acquire it — at the same rate
as a population that has closed the event.

*Status:* supported in one direction by the Hawaii case, where information
availability was at the local-instance level and the gap persisted anyway,
and where those who had the procedure largely did not act on it. Not
established. One case, retrospective self-report.

---

**C4.** Instrument closure and event closure are different quantities.

*Falsifier:* an intervention that moves one and moves the other by the same
amount.

*Status:* structural. Held apart in the schema. The Hawaii case contains a
fragment of the instrument branch inside an event-branch case — silence on
the air-raid sirens read as evidence of no threat — and whether that should
be split out is open.

---

**C5.** Instrument-branch failures cluster on intermediaries with long
correct records, rather than on unfamiliar situations.

*Falsifier:* failure rate flat or falling against the intermediary's
reliability record, exposure held constant.

*Status:* untested and it inverts the standard scoring, which is what makes
it worth running. The rail-crossing data is the nearest available series and
the exposure denominator there is modelled per warning-device category, which
is circular for this purpose.

---

## DISCLOSED WEAKNESSES

**`variable_state` is inferred, never measured.** Nothing in any source
recorded a prior probability before the event. In Hawaii it is inferred from
the procedure-knowledge finding, which is the same evidence C3 uses — so C3
and the coding of that case are not independent.

**Retrospective self-report throughout.** Risk estimates are revised after
the event, in the direction that makes the revision invisible.

**Correctly inferring a false alarm is not a categorisation failure.** In
Hawaii some fraction of non-responders reasoned their way to the right
answer. The published work does not separate them from those who stalled, and
the case cannot carry weight on the mechanism until it does.

**Recall method unspecified.** Free, prompted, recognition, and demonstrated
recall give different numbers. Applies to `breakdown-cones` and to
`generation-capacity` R1 identically.

**No case is quantified.** Every `diagnostic_spend` is `--`. The tool's
central readout has never been taken.

**This module does not measure the mechanism.** At best it measures whether
non-response clusters where priors were closed. Whether the cause is
category-absence in the person is a further step, not evidenced here, and
should not be read off these fields.
