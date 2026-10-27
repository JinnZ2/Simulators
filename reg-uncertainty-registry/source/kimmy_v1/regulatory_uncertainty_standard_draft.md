# RUS-0.1 — Regulatory Uncertainty Standard

**Classification of uncertainty and consequence, minimum direction requirements, symmetry audit, and data-generation obligations for science-based regulatory decisions**

*Draft 0.1 (proposed) — October 18, 2026. This is a design artifact: a proposed standard written in engineering-standard form. It has not been adopted by any body. Annex A applies it retrospectively to the 32 coded U.S. decisions from the companion report `direction_of_uncertainty_report.md`.*

---

## Foreword

Engineering disciplines resolved, decades ago, the problem that regulatory science still handles case-by-case: decisions under uncertainty are governed by *pre-committed* margins rather than post-hoc judgment. A structural member does not get a safety factor negotiated per bridge; the factor is fixed by the code as a function of load uncertainty and consequence of failure. This standard transposes that architecture onto regulatory decisions. Its core claims are three: (1) uncertainty is a **classifiable object** with grades defined by testable criteria, not a rhetorical posture; (2) the **direction** in which uncertainty is resolved shall be a *minimum* determined by uncertainty grade × consequence grade — a safety factor — with deviations requiring declared exceptions; and (3) a decision to remain uncertain ("no action," "monitoring declined") is itself a decision, carries grades, and obligates a **data-generation plan**. The standard is written so that conformity can be audited mechanically from the public record, and so that the resulting corpus of decision records is machine-readable and fit for use as training and forecasting data.

---

## 1. Scope

This standard applies to any regulatory decision in which a public agency resolves scientific uncertainty in a direction — permit, permit-with-conditions, conditional, defer, or restrict — covering drugs, devices, food additives, pesticides, environmental contaminants, and controlled-substance scheduling. It covers the decision record, the classification of uncertainty and consequence, the minimum direction class, cross-agency symmetry, data-generation obligations, calibration, and conformity assessment. It does not prescribe scientific methods, risk-model choices, or benefit valuations, which remain agency competencies.

## 2. Normative and informative references

The following instruments contain provisions that inform this standard: IEC 61508 (safety integrity levels — consequence-scaled assurance) ([IEC](https://www.iec.ch/functionalsafety/explained/)); the GRADE approach to rating certainty of evidence ([GRADE Working Group](https://www.gradeworkinggroup.org/)); IPCC calibrated uncertainty language ([Mastrandrea et al., 2010](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)); 10 CFR Part 50 Appendix B (nuclear quality-assurance rigor as a domain-binding precedent) ([NRC](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html)); ISO 31000 risk management principles; and the FAIR data principles (findable, accessible, interoperable, reusable) ([Wilkinson et al., 2016](https://www.nature.com/articles/sdata201618)).

## 3. Terms and definitions

- **Decision record (DR):** the structured, machine-readable object an agency shall emit for every covered decision (Section 4).
- **Uncertainty grade (U):** ordinal class U1–U4 of residual scientific uncertainty about the material question, per Section 5.
- **Consequence grade (C):** ordinal class C1–C4 of the consequence of an erroneous permissive resolution, per Section 6.
- **Direction class (D):** ordinal class D1–D5 of the resolution's restrictiveness (D1 permit; D2 permit-with-conditions; D3 conditional with data ticket; D4 defer with data ticket; D5 restrict/decline).
- **Safety factor:** the minimum direction class required by the U×C matrix (Section 8). Direction classes are *floors of caution*: exceeding them (resolving more restrictively than required) is conforming by margin.
- **Data ticket:** the mandatory data-generation obligation attached to every D3/D4 resolution and to every non-decision at U≥3 (Section 10).
- **Statute exception:** a declared deviation from the matrix citing the legal instrument that compels it (Section 8, R3).
- **Non-decision:** an agency choice to neither permit nor restrict nor collect data (e.g., declining to monitor a candidate-listed contaminant). Treated as a decision with grades.
- **Symmetry audit:** the cross-agency comparison of direction classes on matched evidence profiles (Section 9).

## 4. The Decision Record (minimum schema)

Every covered decision shall emit a versioned DR, published in a public registry within 30 days, containing at minimum:

```json
{
  "decision_id": "string (agency-docket-year)",
  "question": "string — the material scientific question",
  "evidence_classes": ["animal","human_epi","human_rct","surrogate","sponsor_unpub","eco","in_vitro","none_available"],
  "independence": {"sponsor_only": true, "independent_replication": false},
  "uncertainty_grade": "U1|U2|U3|U4",
  "uncertainty_basis": "string — which Section-5 criterion set the grade",
  "consequence": {"P": 1, "I": 2, "D": 3, "grade": "C1-C4"},
  "required_direction": "D1-D5 (computed)",
  "actual_direction": "D1-D5",
  "exception": {"type": "statute|emergency|none", "instrument": "string|null"},
  "data_ticket": {"required": true, "owner": "string", "deliverable": "string", "deadline": "date|null"},
  "calibration": {"prediction": "string — falsifiable claim made", "check_date": "date"},
  "links": {"record": "url", "prior_related_decisions": ["decision_id"]}
}
```

Normative requirements: the record shall be machine-readable (JSON or equivalent); sponsor-submitted unpublished data shall be labeled as such and, absent a statutory trade-secret bar, deposited in the registry within 12 months; and every DR shall link prior DRs on the same substance or question, making evidence-class reuse traceable across agencies. The schema's purpose is explicitly dual: auditability today, and a clean, consistently labeled corpus for automated analysis and forecasting — under the current regime the labels (directions) are generated by an undocumented function of undeclared features, which is precisely the label-noise condition this standard removes.

## 5. Uncertainty classification (normative)

Uncertainty grades are assigned by **criteria, not judgment**. A decision takes the *highest* grade whose criterion it meets:

| Grade | Criteria (meet all in row) | Typical evidence profile |
|---|---|---|
| **U1 — resolved** | Adequately powered human data; independent replication; effect estimate's confidence interval excludes the decision threshold in one direction; no credible unresolved mechanism | Failed confirmatory RCT; replicated epi with dose-response |
| **U2 — bounded** | Human data exist but with known limitations (single trial, surrogate validated for the class, or epi without replication); residual uncertainty quantified and bounded | One pivotal RCT; validated surrogate; IARC-classified with concordant JECFA review |
| **U3 — substantial** | Surrogate not validated for the question; animal-only evidence with human relevance unresolved; contested epi; or key data sponsor-generated and unreplicated | Amyloid surrogate; rodent tumor with unresolved relevance; single cohort under dispute |
| **U4 — unquantified** | No adequate data exist on the material question; uncertainty cannot be bounded | 510(k) predicate-chain clearance (no clinical data required); candidate-listed contaminant never monitored |

Two modifiers: **M1** — a decision taken with no adequate data (evidence class `none_available`) is U4 regardless of how the record characterizes confidence; **M2** — animal-only evidence with unresolved human extrapolation is at minimum U3. *Rationale:* U4 exists so that "we never looked" can never masquerade as "we looked and it was fine." Under current practice, absence of data is uncoded and invisible; under this standard it is the highest uncertainty grade and triggers Section 10.

## 6. Consequence classification (normative)

Consequence of an erroneous *permissive* resolution is scored on three axes, each 1–3, summed and banded:

| Axis | 1 | 2 | 3 |
|---|---|---|---|
| **P — exposed population** | < 10⁵ | 10⁵–10⁷ | > 10⁷ or environmentally ubiquitous |
| **I — harm irreversibility** | reversible on cessation | partially reversible / manageable | irreversible, latent, or intergenerational |
| **D — decision irreversibility** | readily reversible (recallable drug) | reversible with difficulty (class-wide withdrawal) | near-irreversible (environmental release, implanted device, ubiquitous food supply) |

Banding: score 3–4 → **C1**; 5 → **C2**; 6–7 → **C3**; 8–9 → **C4**. The axis definitions encode an asymmetry the current system handles implicitly and inconsistently: regulatory *decisions* differ in reversibility (a recalled drug versus a released contaminant versus an explanted hip), and that difference belongs in the consequence grade, not in unrecorded judgment. Scoring rationale shall be recorded per axis in the DR so the grade is auditable; v0.2 shall add an exposure-dose refinement axis, flagged here as a known limitation (Annex A notes where dose arguments would move a grade).

## 7. Direction classes (normative)

| Class | Name | Content requirements |
|---|---|---|
| **D1** | Permit | Full go-ahead; no conditions beyond baseline labeling |
| **D2** | Permit with conditions | Warning, REMS, restricted populations, or partial limits; named conditions in the DR |
| **D3** | Conditional | Permit that **expires automatically** (sunset ≤ 5 years) unless the attached data ticket is completed and re-graded; enforceable milestone schedule |
| **D4** | Defer | No permit; data ticket mandatory; decision queue with deadline; interim exposure management where C ≥ 3 |
| **D5** | Restrict | Decline, revoke, ban, or require removal |

The current system's characteristic defect, visible in Annex A, is that its real-world equivalents of D3 lack the two features that make a conditional resolution a control mechanism rather than a parking orbit: automatic expiry and an enforceable ticket. The Makena case — 12 years from accelerated approval to withdrawal on a failed confirmatory trial ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999)) — is what D3-without-sunset costs.

## 8. The U×C decision matrix and overlays (normative)

Minimum required direction class:

|  | **C1** | **C2** | **C3** | **C4** |
|---|---|---|---|---|
| **U1** | D1 | D1 | D2 | D2 |
| **U2** | D1 | D2 | D3 | D3 |
| **U3** | D2 | D3 | D4 | D4 |
| **U4** | D3 | D4 | D4 | D5 |

**Overlays:**

- **R1 (resolved-harm override):** where evidence at U1–U2 indicates actual harm or absence of benefit, the required class is D5 regardless of matrix cell.
- **R2 (margin rule):** actual direction more restrictive than required is **conforming (exceeds safety factor)** and shall be recorded as such; actual direction less restrictive is non-conforming, full stop. As in structural codes, the factor is a floor, not a target.
- **R3 (statute exception):** departure from the matrix compelled by law (e.g., the Delaney Clause's zero-risk rule for carcinogenic food additives, which forced the Red No. 3 ban on rodent tumors the agency itself judged not human-relevant ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline))) shall be declared as a statute exception naming the instrument. Undeclared departures are non-conforming even when legally compelled — the requirement is *visibility*, so that the share of "scientific" divergence that is actually legal architecture becomes measurable.
- **R4 (ticket obligation):** every D3/D4 carries a data ticket (Section 10). A deferral or non-decision at U ≥ 3 without a ticket is non-conforming per se, regardless of direction class.
- **R5 (emergency modifier):** a formally declared public-health emergency shifts the consequence grade one class lower for the duration; the resulting authorization shall be time-limited (D3 form) with a ticket. The molnupiravir EUA — 13–10 committee margin, rodent embryo-fetal and mutagenicity signals, authorization with pregnancy restrictions in an emergency ([NBC](https://www.nbcnews.com/health/health-news/fda-advisory-panel-recommends-mercks-covid-pill-emergency-use-rcna7107)) — is the conforming archetype.

## 9. Symmetry audit (normative)

Symmetry is not "agencies must agree"; it is **"identical profiles, identical direction — or a named reason."** A conformity body shall run the following check across the registry at defined intervals:

```
for each pair of decision records (a, b) on the same or matched evidence profile:
    if a.evidence_classes ≍ b.evidence_classes
       and a.U == b.U and a.C == b.C:
        if a.actual_direction != b.actual_direction:
            require: each record names an exception (R3/R5)
                     or a profile difference (exposure dose, population, statutory standard)
            unexcused divergence  ->  flag SYMMETRY-FAIL, publish
```

Application of this rule to the paired set in the companion report (glyphosate, atrazine, neonicotinoids, chlorpyrifos, titanium dioxide, aspartame, Red No. 3, saccharin, microplastics, PFAS) shows the pattern the standard is designed to surface: rodent-tumor evidence graded U2–U3 produced restrictive or cautionary directions at FDA's food center (Red No. 3 banned ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)); GLP-1 class boxed warning ([Ro safety information](https://ro.co/safety-info/glp1/))) and permissive directions at EPA's pesticide office on overlapping profiles (glyphosate "not likely carcinogenic," later vacated as internally inconsistent ([Verdant Law](https://www.verdantlaw.com/epa-seeks-scientific-input-as-glyphosate-review-moves-forward/)); atrazine re-registered ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/atrazine))). Under RUS-0.1 the Red No. 3 case resolves cleanly as a declared Delaney statute exception and the pesticide cases as either profile-difference declarations (dose, route) or SYMMETRY-FAIL — in either case the *reason* enters the record, which is the entire point. IARC/FDA divergences of the aspartame type ([FDA](https://www.fda.gov/food/food-additives-petitions/aspartame-and-other-sweeteners-food)) would be excused only by a named hazard-vs-risk methodological declaration, converting an annual news cycle into one auditable line item.

## 10. Data-generation obligation (normative)

Uncertainty above U2 shall decay or be paid for. Every D3/D4 resolution, every non-decision at U ≥ 3, and every R5 authorization shall carry a data ticket specifying: the deliverable dataset or study; the generating party (sponsor, agency, or funded independent body); the deadline; the publication requirement (FAIR-compliant deposit); and the re-grading date at which the DR's U-grade is recomputed. Non-delivery converts D3 to D4 automatically (the permit lapses) and escalates D4 to a mandatory re-decision within 12 months. This clause directly addresses the failure mode in which "defer" is a terminal state: microplastics entered the draft Sixth Contaminant Candidate List in April 2026 and UCMR 6 was proposed in July 2026 covering 30 contaminants without it — a non-decision at U4, C4, with no ticket, meaning no national occurrence data will exist at the next candidate-listing cycle either ([Federal Register](https://www.federalregister.gov/documents/2026/07/01/2026-13263/revisions-to-establish-the-sixth-unregulated-contaminant-monitoring-rule-ucmr-6-for-public-water), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/epa-proposes-ucmr-6-for-pfas-and-other-contaminants)). Under RUS-0.1 that combination (U4 × C4 → D5 floor, or D4-with-ticket at minimum) cannot be recorded as inaction; it must be recorded as a decision with a non-conformity flag or a funded monitoring plan.

## 11. Calibration (normative)

Agencies shall maintain published calibration statistics for the falsifiable predictions embedded in their DRs — the regulatory analogue of proof-testing. At minimum: for conditional approvals, the fraction and latency of confirmatory-data delivery and the direction of re-grade on delivery (the accelerated-approval record — exemplified by Makena's 12-year path to a failed trial ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999)) and the bevacizumab breast-indication withdrawal ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3744967/)) — is the existing, unaudited version of this metric); for safety permits, the post-market signal rate among U ≥ 3 permits versus U ≤ 2 permits; and for restriction decisions, the subsequent evidence trajectory. A permissive asymmetry of the magnitude measured in the 2010–2021 drug universe — discordance after negative committee votes at 9.8× the rate after positive votes, with FDA approving 33.3% of drugs its committees rejected ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)) — would appear in calibration reports as a measurable skew requiring explanation, rather than surfacing only when an academic group reconstructs it retrospectively.

## 12. Conformity assessment (normative)

Each agency shall maintain an internal grading function independent of the deciding office (the analogue of independent design review), and an external body shall audit a random sample of DRs annually against Sections 5–10. Audits test three mechanically checkable properties: (i) **grade integrity** — the U and C criteria cited in the DR match the record; (ii) **matrix conformity** — actual direction meets the required floor or carries a declared exception; (iii) **ticket liveness** — open tickets have owners, deadlines, and deposits. Audit outputs are pass/fail per property with published flags; there is no appeals layer in v0.1 because the standard deliberately confines itself to what can be checked from the record without re-adjudicating the science.

---

## Annex A (normative) — Worked re-grading: 32 U.S. decisions, 1977–2026

The 32 coded decisions from the companion report were re-graded under Sections 5–8. Grading was mechanical: U from the coded uncertainty field plus modifiers M1/M2; C from per-axis P/I/D scores recorded with one-line rationales (full audit trail in `annex_a_regrading.csv`); required direction from the matrix with R1/R5 overlays; conformity per R2/R3. Results:

![Annex A conformity audit](img/chart5_conformity.png)

| Status | Count | Share |
|---|---|---|
| CONFORM (exact) | 7 | 22% |
| CONFORM (exceeds safety factor) | 1 | 3% |
| CONFORM (R5 emergency) | 1 | 3% |
| STATUTE-EXCEPTION (undeclared) | 2 | 6% |
| **NON-CONFORM: below safety factor** | **21** | **66%** |

**Findings, stated flat.**

1. **Non-conformity is one-directional.** All 21 non-conforming decisions resolved *less* cautiously than the matrix floor; zero resolved more cautiously without justification. This replicates, by mechanical re-grading, the permissive asymmetry measured at the population level in the companion report (9.8× discordance toward approval in the unselected 2010–2021 drug-vote universe ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/))) — two independent methods converging on the same skew.
2. **Non-conformity is not agency-specific.** Below-floor decisions appear in all four arms (FDA drugs 6/10, FDA device/food 6/10, EPA 8/10, scheduling 1/2), consistent with a system-level absence of pre-committed margins rather than a single-agency pathology.
3. **The extreme cells are the no-data cases.** All three U4 decisions — the original 510(k) clearances of pelvic mesh and metal-on-metal hips (no clinical data required for clearance, with the PMA requirement arriving only in 2016 after mass harm ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2799172), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727911/))) and the microplastics non-decision — combine U4 with C4, the matrix's D5 floor, and actual directions of D1/D4-without-ticket. These are the maximum-deviation cells, and they arise from *evidence-free* mechanisms, not from weighed evidence.
4. **R1 recovers the apparent "over-restrictive" cases.** The failed-confirmatory withdrawals (Makena, bevacizumab) and the BVO revocation on FDA's own positive studies grade as conforming under R1 — confirming that the matrix plus one overlay reproduces the corpus's *defensible* restrictiveness while isolating the rest.
5. **Statute exceptions behave as designed.** Red No. 3 (U1, C4, matrix floor D2, actual D5) and the 1977 saccharin ban attempt grade as undeclared Delaney exceptions — under RUS-0.1 both would be conforming *with declaration*, and the registry would correctly attribute the divergence to statute rather than to science. This is the standard's answer to the misclassification problem: it relocates legal forcing out of the "scientific judgment" column where it currently hides.
6. **The grading is auditable end-to-end.** Every cell in the table below derives from recorded per-axis scores; a reviewer who disputes a C-grade can point to the P/I/D line and the dispute is about one integer with a written rationale, not about the decision as a whole.

Condensed grading table (full version with rationales: `annex_a_regrading.csv`):

| ID | Decision | U | C | Floor | Actual | Status |
|---|---|---|---|---|---|---|
| A01 | Aducanumab AA | U3 | C3 | D4 | D1 | below floor |
| A02 | Eteplirsen AA | U3 | C2 | D3 | D1 | below floor |
| A03 | Zohydro approval | U3 | C3 | D4 | D1 | below floor |
| A04 | Makena withdrawal | U1 | C1 | D5 (R1) | D5 | conform exact |
| A05 | Rofecoxib panel | U2 | C3 | D3 | D1 | below floor |
| A06 | Molnupiravir EUA | U3 | C3 | D3 (R5) | D2 | conform R5 |
| A07 | Flibanserin + REMS | U2 | C1 | D1 | D2 | exceeds factor |
| A08 | Bevacizumab withdrawal | U1 | C2 | D5 (R1) | D5 | conform exact |
| A09 | Donanemab approval | U2 | C3 | D3 | D1 | below floor |
| A10 | Midodrine reversal | U3 | C1 | D2 | D1 | below floor |
| B00 | Mesh 510(k) | U4 | C4 | D5 | D1 | below floor |
| B00b | MoM hip 510(k) | U4 | C4 | D5 | D1 | below floor |
| B01 | Mesh reclass | U3 | C4 | D4 | D4 | conform exact |
| B02 | MoM PMA order | U3 | C4 | D4 | D4 | conform exact |
| B03 | Animal Rule | U3 | C1 | D2 | D1 | below floor |
| B04 | GLP-1 boxed warning | U3 | C3 | D4 | D2 | below floor |
| B05 | Red No. 3 ban | U1 | C4 | D2 | D5 | statute-undeclared |
| B06 | BVO revocation | U3 | C4 | D5 (R1) | D5 | conform exact |
| B07 | TiO2 no action | U3 | C4 | D4 | D1 | below floor |
| B08 | Aspartame rejection of IARC | U3 | C4 | D4 | D1 | below floor |
| C01 | Atrazine 2003 | U3 | C4 | D4 | D1 | below floor |
| C02 | Atrazine 2020 | U3 | C4 | D4 | D1 | below floor |
| C03 | Glyphosate 2020 | U3 | C4 | D4 | D1 | below floor |
| C04 | Chlorpyrifos revocation | U3 | C4 | D4 | D5 | statute-undeclared |
| C05 | Neonics PIDs | U2 | C4 | D3 | D2 | below floor |
| C06 | Lead LCRI | U1 | C4 | D2 | D2 | conform exact |
| C07 | PFAS NPDWR | U2 | C4 | D3 | D2 | below floor |
| C08 | UCMR6 microplastics | U4 | C4 | D5 | D4 (no ticket) | below floor + R4 fail |
| C09 | Saccharin delist | U3 | C4 | D4 | D1 | below floor |
| C10 | Glyphosate/Durnell 2026 | U3 | C4 | D4 | D1 | below floor |
| D01 | Marijuana partial Sch. III | U3 | C3 | D4 | D2 | below floor |
| D02 | Saccharin ban attempt | U3 | C4 | D4 | D4 | conform exact |

*Limitations of the worked example:* single-author grading (no inter-rater reliability computed); C-grades lack the dose axis flagged in Section 6 (rows where a dose argument would plausibly move C by one band: B05, B08, C09); the matrix itself is a v0.1 calibration — the floors encode one defensible safety-factor philosophy and alternative calibrations can be published as variants, which is precisely what a standards process is for.

## Annex B (informative) — Mapping to existing instruments

| RUS-0.1 element | Nearest existing analogue | Gap closed |
|---|---|---|
| U-grades | GRADE certainty ratings; IPCC confidence language | Binding, criterion-based, per-decision, with consequences |
| C-grades | IEC 61508 SIL; nuclear safety-class | Extends consequence-scaled assurance to regulatory science |
| D-floors / matrix | Structural safety factors; ALARP tolerability bands | Pre-committed direction instead of negotiated direction |
| Data ticket | Accelerated-approval confirmatory requirements; CCL/UCMR cycle | Adds sunset, enforceability, and re-grading; covers non-decisions |
| Calibration | Post-market surveillance; PRA living models | Published, falsified-claim tracking across the whole corpus |
| Decision record | FDA/EPA dockets | Machine-readable, versioned, cross-agency linkable; AI-fit corpus |

## Annex C (informative) — The corpus-degradation problem this standard addresses

Regulatory decisions are already training data: models summarizing evidence, predicting approval odds, or forecasting policy learn from the decision corpus as labeled examples. Under the current regime that corpus has three documented defects — inconsistent labels for matched evidence profiles (Section 9), invisible non-decisions (Section 10), and an undeclared feature (cost-bearer and forcing-event structure) doing real predictive work outside the schema (companion report, Sections 5.5 and 7). A model trained on such labels does not learn the science; it learns the undocumented function. Because RUS-0.1 makes grades criterion-referenced, exceptions named, and non-decisions recorded with tickets, the registry it produces is the difference between a corpus that compounds misclassification at scale and one that supports auditing, forecasting, and model evaluation against a stable standard.

---

*Draft 0.1 for discussion. Not medical, legal, or regulatory advice; not an adopted standard. Grading code and data are delivered alongside this document for reproduction and re-calibration.*
