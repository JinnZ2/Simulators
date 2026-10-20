# RUS-0.2 — Regulatory Uncertainty Standard

**Classification of uncertainty and two-sided consequence, minimum direction requirements, symmetry audit, and data-generation obligations for science-based regulatory decisions**

*Draft 0.2 (proposed) — October 18, 2026. Supersedes Draft 0.1. Changes from 0.1: two-sided consequence grading (C_permit / C_restrict) with the floor set from the gap; modifier M2 applied consistently (animal-only evidence ⇒ ≥ U3); coding-reliability requirements (inter-rater agreement) added; Annex A re-graded on 33 decisions under the two-sided rule. A design artifact — not adopted by any body. Companion documents: `direction_of_uncertainty_report_v2.md`, `change_log_v2.md`, `annex_a_regrading_v2.csv`.*

---

## Foreword

Engineering disciplines resolved, decades ago, the problem that regulatory science still handles case-by-case: decisions under uncertainty are governed by *pre-committed* margins rather than post-hoc judgment. Draft 0.2 corrects a structural asymmetry in 0.1: consequence of error is now scored **in both directions**. A wrongly permitted hazard harms the exposed; a wrongly blocked therapy, essential service, or research program harms the denied. The standard now sets the minimum direction class from the *gap* between the two, which is how engineering actually treats opposing failure modes — the margin belongs to the side with the worse error, and both errors are priced.

## 1. Scope

As in 0.1: any regulatory decision resolving scientific uncertainty in a direction — permit, permit-with-conditions, conditional, defer, restrict — across drugs, devices, food additives, pesticides, environmental contaminants, occupational exposures, and scheduling. Occupational health is now explicitly in scope (Annex A row E01): an agency that never issues a standard is making a covered decision under this standard, not standing outside it.

## 2. Normative and informative references

Unchanged from 0.1: IEC 61508 ([IEC](https://www.iec.ch/functionalsafety/explained/)); GRADE ([GRADE Working Group](https://www.gradeworkinggroup.org/)); IPCC calibrated uncertainty language ([Mastrandrea et al., 2010](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)); 10 CFR Part 50 Appendix B ([NRC](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html)); ISO 31000; FAIR principles ([Wilkinson et al., 2016](https://www.nature.com/articles/sdata201618)). Added as informative: IARC Monographs Volume 124, *Night Shift Work* (Group 2A, 2020) ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)) — used in Annex A.

## 3. Terms and definitions

As in 0.1, plus:

- **C_permit:** consequence grade of an erroneous *permissive* resolution (harm if wrongly allowed).
- **C_restrict:** consequence grade of an erroneous *restrictive* resolution (harm if wrongly blocked — denied therapy, denied essential service, blocked research, denied data).
- **Gap (G):** C_permit score − C_restrict score; determines the matrix column (Section 8).
- **Denial harm:** the concrete, graded cost of restriction, which shall be evidenced at the same standard as hazard harm — named population, named harm, irreversibility — not asserted as a generic "cost."

## 4. The Decision Record (minimum schema)

Unchanged from 0.1 (versioned, machine-readable, public registry, sponsor-data labeling, cross-agency linkage), with two additions: `consequence_permit` and `consequence_restrict` replace the single `consequence` object, each carrying per-axis P/I/D scores and a one-line rationale; and `coding` gains a `reliability` sub-object (see Section 12).

## 5. Uncertainty classification (normative)

Criteria table unchanged from 0.1 (U1 resolved / U2 bounded / U3 substantial / U4 unquantified). Modifiers, now stated exhaustively: **M1** — no adequate data ⇒ U4. **M2** — animal-only evidence with unresolved human extrapolation ⇒ at least U3. *M2 is applied regardless of how confident the agency's narrative sounds:* FD&C Red No. 3 is graded U3 even though the agency characterized the rat tumors as not human-relevant, because the human-relevance judgment itself rests on mechanism extrapolation, not human data ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)). A record-stated confidence level may be reported alongside the grade but does not override M1/M2.

**Exposure descriptor requirement (new):** where the decision concerns a patterned exposure (shift work, intermittent dosing, episodic environmental release), the DR shall record the exposure by its pattern dimensions — for night work: permanent-night versus forward-rotating versus backward-rotating versus rapid day/night flip — not by ever/never status. Ever/never coding of patterned exposures is non-conforming under this standard because it destroys dose information the evidence base actually contains; the night-shift literature's residual inconsistency is substantially an exposure-misclassification artifact (background in the companion report, Section 6.2).

## 6. Consequence classification — two-sided (normative)

Both directions of error are scored on the same three axes (1–3 each, summed, banded 3–4 → grade 1, 5 → 2, 6–7 → 3, 8–9 → 4):

| Axis | 1 | 2 | 3 |
|---|---|---|---|
| **P — affected population** | < 10⁵ | 10⁵–10⁷ | > 10⁷ or environmentally/occupationally ubiquitous |
| **I — harm irreversibility** | reversible | partially reversible | irreversible, latent, or intergenerational |
| **D — decision reversibility** | readily reversible | reversible with difficulty | near-irreversible (environmental release, implant, entrenched exposure) |

For **C_permit**, "harm" means hazard to the exposed. For **C_restrict**, "harm" means denial: loss of the only effective therapy for a progressive disease (high I), interruption of an essential service (water, food preservation), or foreclosure of research (a scheduling decision that prevents the very studies that would resolve the uncertainty — a self-sealing U4 trap). Denial harm must be evidenced, per Section 3; where no denial harm can be evidenced, C_restrict defaults to the lowest band and the matrix tightens accordingly.

## 7. Direction classes (normative)

Unchanged from 0.1: D1 permit; D2 permit-with-conditions; D3 conditional with sunset and data ticket; D4 defer with data ticket; D5 restrict. The D3 defect noted in 0.1 stands: real-world conditional approvals without automatic expiry and enforceable tickets are parking orbits (Makena: 12 years to a failed confirmatory trial ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999))).

## 8. The decision matrix — floor set from the gap (normative)

Matrix rows (uncertainty) and base columns are unchanged; the **column is selected by the gap** G = C_permit − C_restrict:

|  | G ≤ −1 | G = 0 | G = 1–2 | G ≥ 3 |
|---|---|---|---|---|
| **U1** | D1 | D1 | D2 | D2 |
| **U2** | D1 | D2 | D3 | D3 |
| **U3** | D2 | D3 | D4 | D4 |
| **U4** | D3 | D4 | D4 | D5 |

A negative gap (restriction hurts more than permission) shifts the floor permissive; a positive gap shifts it restrictive; the matrix no longer assumes permission is the dangerous error.

**Overlays:**

- **R1 (resolved-harm override):** evidence at U1–U2 of actual harm or absent benefit ⇒ required class D5.
- **R2 (bounded margin, two-sided):** exceeding the floor by one class is conforming by margin. Exceeding it by two or more classes while C_restrict > C_permit is non-conforming (*over-restrictive with denial harm*) — the standard now prices denial, so unbounded conservatism is no longer free.
- **R3 (statute/judicial exception):** departures compelled by law or court order shall be declared with the instrument named (Delaney Clause; FQPA consent-decree deadline). Undeclared departures are non-conforming even when legally compelled.
- **R4 (ticket obligation):** D3/D4 and any non-decision at U ≥ 3 carry a data ticket with owner, deadline, deposit, and re-grading date. Non-delivery converts D3 to D4 automatically; ticketless deferral at U ≥ 3 is non-conforming per se.
- **R5 (emergency modifier):** formally declared emergency shifts the gap one column permissive for the duration; authorization must be time-limited with a ticket.
- **R6 (self-sealing prohibition, new):** where restriction itself prevents the evidence from being generated (research-scheduling, monitoring declined), the restriction shall be re-graded annually and cannot persist past two cycles without new justification — uncertainty maintained by the agency's own inaction does not count as uncertainty resolved.

## 9. Symmetry audit (normative)

Unchanged from 0.1: identical evidence profile + same U + same gap ⇒ same direction class, or a declared reason (statute, dose, route, population, methodology). The night-shift comparison is the new canonical audit case: IARC Group 2A classification ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)); Denmark compensates breast cancer after long-term night work as an occupational disease (K-flagged citation, companion report Section 6.2); the US has no standard at all — not even a data-collection requirement. Under this standard that pair reads: same profile, same U, divergence unexcused → SYMMETRY-FAIL, plus an R4 ticket obligation on the US side.

## 10. Data-generation obligation (normative)

Unchanged from 0.1, plus R6 above.

## 11. Calibration (normative)

Unchanged from 0.1.

## 12. Conformity assessment and coding reliability (normative)

Grading shall be performed by at least two coders — at least one independent of the lead analyst — on a sample of not less than 20% of decisions, with Cohen's κ reported per field (direction, U, C_permit, C_restrict, cost-bearer). κ < 0.6 on any field triggers codebook revision before conformity claims are published. *Annex A of this draft does not yet meet this clause:* the second coder was a frozen rule-based instrument authored by the same researcher (agreement 90%, κ = 0.76 on direction; 80%, κ = 0.64 on uncertainty; 100% on cost-bearer group — full results and the comparator-verb artifact are in the companion report Section 8). A human second coder is outstanding and is the first requirement of any 0.3 revision.

---

## Annex A (normative) — Re-graded worked example: 33 decisions, 1977–2026, under two-sided consequence

Full audit trail with per-axis scores and rationales: `annex_a_regrading_v2.csv`. Summary:

| Status | Count | Share |
|---|---|---|
| CONFORM (exact) | 6 | 18% |
| CONFORM (exceeds floor) | 2 | 6% |
| CONFORM (R5 emergency) | 1 | 3% |
| STATUTE/JUDICIAL-EXCEPTION (undeclared) | 2 | 6% |
| **NON-CONFORM: below floor** | **22** | **67%** |
| NON-CONFORM: over-restrictive with denial harm | **0** | **0%** |

![Annex A v2 conformity audit](img/chart5_conformity.png)

**Findings, stated flat.**

1. **One-directional non-conformity survives the two-sided re-grade.** With denial harm priced, 22 of 33 decisions still fall below the caution floor and none exceeds it without justification. The two-sided correction changed individual grades — donanemab moves to conform (G = −1: denying an Alzheimer's therapy to a progressive-disease population carries C_restrict 4), flibanserin to exceeds-floor — but did not move the direction of the corpus's deviations. This is a stronger result than 0.1's, because the obvious objection ("you only priced hazard, not denial") is now engineered into the scoring and the skew persists.
2. **The largest deviations remain the no-data cells** (mesh and metal-on-metal 510(k) clearances: U4, G = 3, floor D5, actual D1) — permissive resolution at maximum uncertainty and maximum positive gap.
3. **The lone discretionary restrictive action** (BVO, FDA's own rodent thyroid studies, substitutes available ([FDA](https://www.fda.gov/food/food-additives-petitions/brominated-vegetable-oil-bvo))) grades as exceeds-floor conforming: G = 3, floor D4, actual D5, within the one-class margin.
4. **The new occupational row behaves like the environmental rows:** night-shift work (U3, G = 2, floor D4 — at minimum a data/monitoring obligation with pattern-coded exposure; actual D1) falls below the floor, extending the pattern beyond FDA/EPA to OSHA's non-decision space.
5. *Limitations (unchanged in kind):* single-researcher grading with a programmatic second pass (Section 12 non-conformity acknowledged); C_restrict rationales are argued per case in the CSV and are the most contestable axis; the gap→column calibration is a v0.2 choice, publishable as variants.

## Annex B (informative) — Mapping to existing instruments

Unchanged from 0.1; add: two-sided consequence ↔ ASME/pressure-vessel dual failure-mode analysis and IEC 61508's distinction between hazard of action and hazard of inaction; R6 ↔ sunset clauses in administrative law and adaptive-management triggers in NEPA practice.

## Annex C (informative) — Corpus integrity

Unchanged from 0.1 in intent; the v2 dataset (`coded_decisions_v2.csv`) now encodes direction *relative to the cost-bearer*, which is the orientation a forecasting model actually needs — verb-based labels ("hold") encode opposite signs for the same economics depending on who pays, and any model trained on verbs inherits that inversion. The change log ships as a separate auditable artifact (`change_log_v2.md`) so the corpus carries its own revision history.

---

*Draft 0.2 for discussion. Not medical, legal, or regulatory advice; not an adopted standard. Data and grading artifacts delivered alongside for reproduction and re-calibration.*
