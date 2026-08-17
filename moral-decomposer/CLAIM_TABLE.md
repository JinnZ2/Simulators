# CLAIM TABLE — MORAL CLAIM DECOMPOSER

Each claim carries a falsifier. Status is what the repo supports, not what
is believed.

---

**M1.** Disagreements presented as moral or ethical disagreements decompose
into divergent claims about the option distribution — who has optionality,
who decides, and what was taken out of the variable environment.

*Falsifier:* a case where both sides' stage-1 readings match on every party
and every held-fixed variable, and a disagreement remains.

*Status:* two cases, both reduce. n=2, both constructed by the model rather
than drawn from documented disputes. This is weak evidence and the weakest
part of the repo.

---

**M2.** What looks like a value difference is usually a boundary decision
about whose optionality enters the tally.

*Falsifier:* a case with matched tally boundaries and divergent weighting of
the same admitted parties.

*Status:* both cases reduce this way. Same n=2 limit.

---

**M3.** A frame requiring an internal ordering does not terminate — it
generates further boundary cuts, and the cuts are typically undocumented.

*Falsifier:* an ordering frame with a documented criterion that requires no
further cuts, sustained over time.

*Status:* asymmetry appears in both cases (3 undocumented cuts vs 0, both
times, in opposite file positions). Cut lists are enumerated by hand, so the
count reflects the enumerator, not a survey. Not a measurement.

---

**M4.** A developmentally acquired frame is an option ceiling rather than a
position selected from a set.

*Falsifier:* evidence that frames acquired in development are revised at the
same rate as frames adopted later, given the same counter-evidence.

*Status:* untested. Recorded as the `acquired` field, set on one side of one
case. Links to `uninstrumented` mechanism 10.

---

**M5.** Zero live residue across cases is an absence, not a proof.

*Status:* stated in the tool output and enforced by the schema: the selftest
includes a fixture with a live residue item, so a non-empty residue is
representable and the instrument is not rigged toward M1.

---

## DISCLOSED WEAKNESSES

**Both cases are model-constructed.** Neither is a documented dispute between
real parties. A case where each side's stage-1 entries are filled in by that
side, rather than by one party modelling both, would test M1 very differently
— the reductions here were produced by the same process that predicts them.

**Cut enumeration is not a survey.** Stage 3 counts what was listed. A frame
looks terminating if nobody listed its cuts. `terminates` is currently an
asserted field, not derived.

**`held_fixed` is free text.** Two sides can state the same variable in
different words and the mismatch will read as divergence. No controlled
vocabulary.

**Welded terms are flagged, not decomposed.** `welded_terms` is a pointer to
`category-weld`. Nothing checks that the decomposition happened first, and
both cases carry unresolved welds.
