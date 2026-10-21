# The Direction of Uncertainty in U.S. Regulatory Decisions — v2 (revised)

**A flat report on a proposed cost-bearer pattern: found / scope limits / unmeasured**

*Revised October 18, 2026 under Work Order v2. Every recode and its reason is listed in `change_log_v2.md`. Supersedes `direction_of_uncertainty_report.md`. Companion standard: `regulatory_uncertainty_standard_v02.md`. This report tests a proposed pattern — it does not assert one. Inference chains and unverified items are marked in Section 9.*

---

## 1. Executive summary

The proposed pattern under test: *when U.S. regulators face scientific uncertainty, the direction in which they resolve it — go-ahead versus hold/decline — tracks who bears the cost of caution rather than the evidence itself.* v2 changes the coding in four structural ways: direction is coded **relative to the cost-bearer** (a non-decision that relieves the cost-bearer is permissive, whatever its verb); final outcomes are coded rather than attempts; cost-bearer is coded as the sponsor wherever a sponsor exists; and one unselected EPA frame is added so the test is not drug-only.

**What was found, stated flat:**

- **Population level (Frame A, unselected):** across the published universe of FDA human-drug advisory-committee initial-approval votes, 2010–2021, FDA approved 96.6% of drugs after positive votes. After negative votes it **followed the committee 66.7% of the time** (40 of 60 not approved) and **approved 33.3% anyway** (20 of 60) — discordance after a negative vote running **9.8×** the rate after a positive vote (3.4%), Fisher exact OR = 14.2, p = 2.1×10⁻⁸ ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)). Because the sponsor always bears the caution cost in this frame, there is **no contrast group**: this is a *permissive skew consistent with the pattern*, not a test of it. Rival explanations — unmet medical need, statutory access mandate, advocacy pressure — are listed in Section 6.1.
- **Coded 33-decision sample:** the naive cost-bearer hypothesis is **not supported bivariately** — restrictive outcomes in 7/31 concentrated-cost-bearer cases versus 0/2 diffuse-cost-bearer cases (Fisher p = 1.00). A controlled regression remains **not identifiable** at this n ("no data," Section 6.3). Structural byproduct of the recode: in 31 of 33 decisions a concentrated cost-bearer exists at all; the diffuse-bearer configuration the hypothesis needs barely occurs.
- **Unselected EPA frame (new, Frame C2):** all 34 registration-review decisions announced in the Federal Register in calendar 2022 continued registration — **34/34 permissive**; the restrictive pesticide actions of the same window were a court-driven cancellation (chlorpyrifos) and procedural enforcement (DCPA), not discretionary hazard calls (Section 6.2).
- **Scope limit found:** of 8 restrictive agency actions against concentrated cost-bearers, **7 ride an external forcing event** (statute, court order, failed confirmatory trial, mass litigation); **BVO is the lone discretionary restrictive action**, corrected from v1 (Section 6.4). Court rulings are logged separately, not counted as agency actions.
- **Cross-agency symmetry:** confirmed in 10 paired comparisons plus the new occupational case (night-shift work: IARC 2A, Danish compensation, no US standard), with the within-US rodent-data asymmetry intact (food/drug center restrictive, pesticide office permissive).
- **RUS-0.2 re-grade:** with consequence priced **two-sided** (harm of wrongly allowing *and* harm of wrongly blocking), 22/33 decisions fall below the caution floor and **zero** exceed it without justification — the one-directional non-conformity survives the correction (`regulatory_uncertainty_standard_v02.md`, Annex A).

Branches are kept separate in Section 8. No verdict language is used.

---

## 2. Task, scope, and revision

The v2 work order kept six elements (Frame A analysis, data tickets, the U4 "never looked" rule, declared statute exceptions, the machine-readable decision record, flat branch reporting) and issued ten fixes, all applied: corrected negative-vote wording; Frame A reframed as skew-without-contrast; cost-bearer recodes (C10→Bayer, A06→Merck, B03→countermeasure manufacturers); direction coded relative to the cost-bearer (C08 permissive; D02 on its final moratorium outcome); forcing-analysis reconciliation; two-sided consequence in the standard; consistent M2 (Red No. 3 is U3); removal of the v1 "independent replication" claim plus a second-coder agreement study; an unselected EPA frame; and the night-shift case with exposure coded by rotation pattern. Sources run through October 2026; the 2026 anchors are coded on their 2026 status (*Monsanto v. Durnell*, decided June 25, 2026 ([Supreme Court](https://www.supremecourt.gov/opinions/25pdf/24-1068_n7ip.pdf)); UCMR 6 proposed July 1, 2026 without microplastics ([Federal Register](https://www.federalregister.gov/documents/2026/07/01/2026-13263/revisions-to-establish-the-sixth-unregulated-contaminant-monitoring-rule-ucmr-6-for-public-water)); partial marijuana Schedule III order, subsequently stayed ([DOJ](https://www.justice.gov/opa/pr/justice-department-places-fda-approved-marijuana-products-and-products-containing-marijuana), [Ogletree](https://ogletree.com/insights-resources/blog-posts/marijuana-rescheduling-temporarily-paused/))). The web-search backend was unavailable during part of the revision; affected items are K-flagged in Section 9.

---

## 3. Sampling frames

**Frame A — unselected population, FDA human-drug advisory votes 2010–2021.** Unchanged from v1: the published census of 409 meetings and 298 regulatory votes ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/37418270/)). Limits as before (drugs only; ends 2021; committee-convening is selective). Ten coded decisions (A01–A10) remain the stratified subset.

**Frame B — FDA device/food purposive enumeration.** Unchanged.

**Frame C — EPA purposive enumeration.** Unchanged (atrazine, glyphosate, chlorpyrifos, neonics, lead, PFAS, UCMR 6, saccharin).

**Frame C2 — NEW, unselected: all EPA pesticide registration-review interim/final decisions announced in the Federal Register, calendar year 2022.** Enumerated verbatim from the five decision notices of CY2022 — 87 FR 5815 (15 interim decisions), 87 FR 6535 (3 interim + 1 final), 87 FR 25266 (8 interim/final + 2 amended), 87 FR 48018 (2 interim), 87 FR 64484 (3 interim/final) — plus 6 case closures where the last registrations had been canceled. Full row-level enumeration: `epa_frame_2022.csv`. This frame is unselected in the required sense: every registration-review decision EPA announced in the window is in it. **Scope limits:** direction is coded at notice level (registration continued = permissive toward the registrant); document-level mitigation and per-chemical uncertainty were not coded (34 decision documents); proposals and draft risk assessments are excluded; the window is one calendar year. Restrictive actions in the same window that did *not* come through registration review are logged separately (Section 6.2).

**Frame D — scheduling.** Unchanged (D01, D02-on-final-outcome).

**Frame E — NEW, occupational (n=1).** Night-shift work (E01): IARC Monographs Volume 124 classified night shift work "probably carcinogenic to humans" (Group 2A) on limited human evidence, sufficient animal evidence, and strong mechanistic evidence ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)); Denmark's injury board has compensated breast cancer after long-term night work as an occupational disease (K-flagged, Section 9); the US has no OSHA standard — NIOSH guidance only. A single purposive row, illustrative only.

## 4. Coding rules (v2)

Fields unchanged except two normative changes, applied to every row:

- **Direction is coded relative to the cost-bearer, not by action verb.** A decision that relieves the party bearing the caution cost is permissive toward them even when the verb sounds restrictive ("declined to require monitoring," C08); a final outcome is coded rather than an intermediate attempt (D02: ban attempt → moratorium with warning label = warn). The action verb is preserved in the row note.
- **Cost-bearer** remains "the party absorbing the largest share of the cost under the more restrictive option," but v2 applies the rule **wherever a sponsor exists** — including pandemic and countermeasure contexts where v1 had coded the public (A06, B03, C10). "Sponsor" includes registrants, manufacturers, utilities, and — for E01 — employers.

Uncertainty, evidence class, and mirror coding are unchanged; the dataset is `coded_decisions_v2.csv` (33 rows). Six rows carry recode notes; all five recodes are itemized in the change log.

---

## 5. The coded sample (n=33)

The full table with per-row sources is unchanged from v1 except as recoded; the complete dataset with notes is delivered as `coded_decisions_v2.csv`. Recoded cells, restated with sources:

| ID | v2 coding | Basis |
|---|---|---|
| A06 | cost-bearer **sponsor**; warn | 13–10 committee vote; embryo-fetal/mutagenicity signals handled by pregnancy restrictions in an emergency ([NBC](https://www.nbcnews.com/health/health-news/fda-advisory-panel-recommends-mercks-covid-pill-emergency-use-rcna7107)); restriction cost falls on Merck, not only the public |
| B03 | cost-bearer **sponsor**; go_ahead | Animal efficacy accepted as approval basis where human trials are unethical ([FDA](https://www.fda.gov/emergency-preparedness-and-response/preparedness-research/animal-rule-summary)); requiring human efficacy would fall on countermeasure manufacturers |
| C08 | direction **go_ahead** | UCMR 6 omits microplastics ([Federal Register](https://www.federalregister.gov/documents/2026/07/01/2026-13263/revisions-to-establish-the-sixth-unregulated-contaminant-monitoring-rule-ucmr-6-for-public-water), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/epa-proposes-ucmr-6-for-pfas-and-other-contaminants)); declining monitoring relieves utilities → permissive toward the cost-bearer |
| C10 | cost-bearer **sponsor**; go_ahead | EPA review open since 2009; *Durnell* preemption relieved Bayer of warning-label liability ([Supreme Court](https://www.supremecourt.gov/opinions/25pdf/24-1068_n7ip.pdf)) |
| D02 | direction **warn** | Final outcome: congressional moratorium + warning label kept saccharin marketed (established record; timeline in [Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |
| E01 | new row: go_ahead / sponsor / mirror | IARC 2A ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)); Denmark compensates (K-flag); no US standard; exposure must be coded by rotation pattern — permanent night, forward/backward rotation, weekly day/night flip — because ever/never coding discards the dose information that distinguishes them |

All other rows stand as coded in v1 (sources in `coded_decisions_v2.csv` notes and v1 report, unchanged).

---

## 6. Statistical tests and frame-level results

### 6.1 Population level (Frame A) — permissive skew, no contrast group

Initial-approval votes 2010–2021, FDA action as of November 30, 2022 ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)):

| Committee vote | FDA approved | FDA did not approve | Approval rate |
|---|---|---|---|
| Positive (n=147) | 142 | 5 | **96.6%** |
| Negative (n=60) | 20 | 40 | **33.3%** |

Equivalently: FDA **followed 66.7% of negative votes** and approved 33.3% of negatively-voted drugs anyway. Discordance after a negative vote (33.3%) runs **9.8×** discordance after a positive vote (3.4%); Fisher exact OR = 14.2, p = 2.1×10⁻⁸. Positive votes were associated with a hazard ratio of 9.42 (95% CI 5.99–14.80) for approval, with median time-to-approval of 74 days after a positive vote versus 700 days after a negative one ([MedPage Today](https://www.medpagetoday.com/publichealthpolicy/fdageneral/105370)); the study's editorial reads the asymmetry as "says something very important about the agency's view of advisory committees" ([Kanter, JAMA Health Forum](https://pubmed.ncbi.nlm.nih.gov/37418271/)).

![FDA followed 'yes' votes far more often than 'no' votes](img/chart1_asymmetry.png)

**Interpretation, corrected per Fix 2.** In Frame A the sponsor always bears the cost of restriction and the public always bears the cost of permission — there is no within-frame variation in cost-bearer, so the frame cannot test the cost-bearer hypothesis. What it establishes is a large, statistically secure **permissive skew consistent with the pattern**, in the one frame where direction is enumerated without selection. **Rival explanations** that the frame cannot exclude: (i) unmet medical need — negative-vote drugs disproportionately address severe disease, and the skew may encode a defensible benefit-risk asymmetry rather than a cost-bearer asymmetry; (ii) statutory access mandate — FDA's institutional mission includes making products available, not only keeping bad ones out; (iii) advocacy pressure — several discordant approvals followed organized patient-advocacy campaigns (flibanserin is the coded example, approved 18–6 with REMS after two rejections ([NEJM](https://www.nejm.org/doi/full/10.1056/NEJMp1513686))); (iv) committee-selection effects — the FDA convenes committees on contested files, so vote valence is not a random draw of uncertainty. Each rival is a named alternative mechanism; the frame cannot rank them.

A second population observation, unchanged from v1: in FDA *device* panels, panelists expressing uncertainty voted against approval 55.9% of the time versus 12.2% for certain panelists ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0267134)) — uncertainty pushes restrictive at the individual-voter level even where the agency-level residual skews permissive.

### 6.2 Bivariate test (v2) and the unselected EPA frame

Direction relative to cost-bearer; restrictive = hold + decline.

| Cost-bearer of caution | Restrictive | Permissive | % restrictive |
|---|---|---|---|
| Concentrated (n=31) | 7 | 24 | 23% |
| Diffuse (n=2) | 0 | 2 | 0% |

Fisher exact p = 1.00 (v1: p = 0.29). The high-uncertainty restriction (3/20 vs 0/2) and the statute-excluded sensitivity (2/25 vs 0/2) are likewise p = 1.00. **The naive hypothesis is not supported bivariately, and v2 strengthens that null.** Two structural readings, stated flat: (i) after Fix 3, only 2 of 33 decisions lack a concentrated cost-bearer — the configuration in which the hypothesis predicts caution (public bears the cost) is nearly absent from the observed decision space, so the bivariate test is nearly uninformative as well as null; (ii) within the concentrated-bearer cases, restrictiveness is gated by forcing events (Section 6.4), not by the evidence variables the hypothesis says should not matter.

![Coded sample v2: direction relative to cost-bearer](img/chart2_costbearer.png)

**Frame C2 result (the non-drug test).** In calendar 2022 EPA announced 34 registration-review decisions on the merits; **all 34 continued registration** (direction permissive toward the registrant; `epa_frame_2022.csv`). Six further cases closed without decision because the last registrations had already been canceled by registrants. The restrictive pesticide actions of the same window did not come from the review program: the chlorpyrifos cancellation intent (December 2022) executed the court-ordered 2021 revocation ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos)), and the DCPA suspension notice enforced a data-call-in deadline — procedural, not hazard-driven. One unselected frame is one window, and notice-level coding cannot see mitigation; but the direction distribution is unambiguous: **the default resolution of registration-review uncertainty is continuation**, matching the drug frame's skew at the direction level.

**Night-shift case (E01).** IARC's Group 2A classification ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)) and Denmark's compensation practice (K-flagged) resolve the same evidence toward caution; the US resolves it as a non-decision — no standard, no monitoring, no exposure registry — which under Fix-4 coding is permissive toward the cost-bearer (employers). The case also demonstrates the exposure-misclassification hazard the work order named: the literature and any future standard must distinguish permanent night work, forward- versus backward-rotating schedules, and rapid day/night flips; coding exposure as ever/never night work collapses a gradient the mechanistic evidence says is causal (circadian disruption dose), and poisons any downstream model trained on such labels.

### 6.3 Controlled test — no data

Unchanged in kind: logistic adjustment for evidence class and uncertainty is not identifiable (complete separation; the diffuse group contains zero restrictive outcomes), and is reported as **no data**, not a null. n=33 does not change this.

### 6.4 Forcing events — reconciled (Fix 5)

v1 claimed "11 of 11" restrictive decisions on forcing events while the dataset contained 9 restrictive rows; the extra two were a court ruling and a partial (warn) action, and BVO was mislabeled as externally forced. v2 separates the logs:

**Restrictive agency actions (n=8, counting the 1977 saccharin ban attempt as an action; final outcome coded warn):**

| Year | Action | Forcing event |
|---|---|---|
| 1977 | Saccharin ban proposed | Delaney Clause; overridden by congressional moratorium ([Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |
| 2011 | Bevacizumab breast indication withdrawn | Confirmatory trials failed ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3744967/)) |
| 2016 | Pelvic mesh → Class III/PMA | Injury reports + mass tort litigation ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2799172)) |
| 2016 | Metal-on-metal hip PMA order | Registry failure data + litigation ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727911/)) |
| 2021 | Chlorpyrifos tolerances revoked | Ninth Circuit order, FQPA deadline ([EPA](https://www.epa.gov/pesticide-worker-safety/epa-update-use-pesticide-chlorpyrifos-food)) |
| 2023 | Makena withdrawn | Confirmatory trial failed ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999)) |
| 2024 | **BVO revoked — DISCRETIONARY** | None external; FDA's own rodent studies, agency-initiated ([FDA](https://www.fda.gov/food/food-additives-petitions/brominated-vegetable-oil-bvo)) |
| 2025 | Red No. 3 banned | Delaney Clause ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)) |

**Court rulings (logged separately, not agency actions):** NRDC v. EPA (2022, glyphosate human-health portion vacated as internally inconsistent ([Verdant Law](https://www.verdantlaw.com/epa-seeks-scientific-input-as-glyphosate-review-moves-forward/))); Eighth Circuit (2023, chlorpyrifos revocation vacated, tolerances reinstated ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos))).

![Restrictive agency actions: what forced them (v2)](img/chart4_forcing.png)

Corrected finding: **7 of 8 restrictive agency actions ride an external forcing event; BVO is the lone discretionary exception.** The v1 universal claim ("every") is withdrawn. The scope-limited structure survives in weaker form: discretionary restrictive resolution of uncertainty against a concentrated cost-bearer is *rare* (1 of 8) rather than absent.

---

## 7. Cross-agency symmetry

The 10-pair table from v1 stands (glyphosate, atrazine, neonicotinoids, chlorpyrifos, titanium dioxide, aspartame, microplastics, Red No. 3, PFAS, saccharin — 8 of 10 divergent, six by two or more points; sources in v1 Section 6, unchanged). One pair is added:

| Pair (evidence class) | US federal resolution | Comparator | Divergence |
|---|---|---|---|
| Night-shift work — carcinogenicity (limited human epi + sufficient animal + strong mechanism) | No OSHA standard; no data collection (3 = go ahead) | IARC 2A (2020) ([IARC](https://www.iarc.who.int/news-events/iarc-monographs-volume-124-night-shift-work/)); Denmark compensates breast cancer in long-term night workers (2; K-flagged) | 1+ |

The within-US rodent asymmetry is unchanged: rodent tumors compelled a food-dye ban (Delaney) and a drug-class boxed warning ([Ro safety information](https://ro.co/safety-info/glp1/)) while overlapping evidence classes were discounted for pesticides; and the Red No. 3 grading is corrected to U3 under consistent M2 (animal-only ⇒ ≥ U3), which makes its statute-exception character sharper, not weaker: a statute, not a science judgment, closed the gap.

---

## 8. Reliability: second-coder exercise (Fix 8)

v1's statement that the Annex A audit "replicates" the population-level result is **withdrawn**: same coder, same cases — not independent. v2 adds a second coding pass by a **frozen rule-based instrument** ("Coder B": fixed lexical rules for direction and uncertainty, fixed rule for cost-bearer, written before application) on a 10-row stratified subset (A01, A05, A09, B00, B04, B07, C01, C04, C08, E01):

| Field | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| Direction (pass 1) | 70% | 0.45 | A05, B07, C01 — all traced to comparator verbs: the rulebook attributed the *EU ban* inside the fact string instead of the US action |
| Direction (pass 2 — frozen input rule: string names only the US federal action) | 90% | 0.76 | A05 (expert: go_ahead; rulebook: warn — "return with warnings") |
| Uncertainty band | 80% | 0.64 | A09 (rulebook: U3 on "surrogate"; expert: U2 — RCT data bounded it), C04 (rulebook default U2; expert: U3 — contested neurodevelopmental evidence) |
| Cost-bearer group | 100% | undefined (no variance) | none |

Read flat: direction and cost-bearer coding are reasonably robust to an instrument change; uncertainty banding is the weakest field (κ = 0.64), and the two disagreements show why — it mixes record-stated confidence with evidence-class heuristics. **Marked limitation:** Coder B is programmatic and was authored by the same researcher; it tests codebook consistency, not human independence. A genuinely independent human second coder remains outstanding and is a stated requirement of RUS-0.2 Section 12.

---

## 9. Findings by branch (kept separate, no verdict language)

**Pattern holds.** Nothing is claimed here at population level anymore. Within the coded sample, the cross-agency mirror structure (Section 7) and the forcing-gated pattern of restrictiveness (Section 6.4) remain consistent with the cost-bearer account, and the RUS-0.2 audit finds the corpus's deviations one-directional (22 below floor, 0 over) even after denial harm is priced — consistent with a systematic tilt, not yet discriminated from the Section 6.1 rivals.

**Pattern scope-limited.** Restrictive resolutions against concentrated cost-bearers are gated by external forcing in 7 of 8 cases, with BVO the discretionary exception; GLP-1-style warnings and the 10 ppb lead trigger show the cost-minimal partial form of caution ([Ro](https://ro.co/safety-info/glp1/), [EPA](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements)). The drug-frame permissive skew is *consistent with* the pattern but has no contrast group and at least four rival explanations.

**No data.** Controlled adjustment is not identifiable (Section 6.3). The diffuse-bearer configuration occurs in only 2 of 33 decisions — the hypothesis's caution condition is nearly unobserved in this corpus. Frame C2 is notice-level; document-level coding of its 34 decisions is unmeasured. USDA remains unenumerated. Denmark-compensation and pentachlorophenol-cancellation details are K-flagged (search backend unavailable during revision).

**Pattern absent.** Bivariately, v2: p = 1.00 in the full sample and both sensitivities — stronger null than v1. The corpus's restrictiveness tracks forcing events, not cost-bearer; and where the pattern is absent the observable driver is legal architecture (Delaney, FQPA deadlines) or litigation, not the evidence variables.

---

## 10. Inference chains, unverified items, and gaps

**Inference chains (marked):** (1) Frame A's negative-vote-is-uncertainty proxy — if negative votes mark clear inefficacy instead, the skew measures something else; (2) the cost-bearer operationalization is this report's rule, now applied uniformly where a sponsor exists — a defensible but contestable choice for emergency contexts (A06); (3) forcing-event attribution is a reading of the record; (4) comparator scores compress distinct legal instruments onto one axis; (5) Coder B's fact strings were authored by the researcher — pass-1/pass-2 transparency is provided precisely because input wording moves κ.

**K-flagged (unverified this revision, search backend down):** Denmark night-shift compensation details; pentachlorophenol registrant-led cancellation note; the EU chlorpyrifos non-renewal date; saccharin timeline source (secondary compilation).

**Gaps:** no unselected device/food frame exists; Frame A ends in 2021; Frame C2 covers one calendar year at notice level; Frame E is a single purposive case; sponsor-unpublished data remains visible only where records disclose it; no human second coder yet.

---

*This report is a research compilation for general informational purposes. It is not legal, medical, occupational-health, or regulatory advice.*
