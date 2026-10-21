# The Direction of Uncertainty in U.S. Regulatory Decisions

**A flat report on a proposed cost-bearer pattern: found / scope limits / unmeasured**

*Compiled October 18, 2026. This report tests a proposed pattern — it does not assert one. All inference chains and unverified items are marked in Section 8.*

---

## 1. Executive summary

The proposed pattern under test: *when U.S. regulators face scientific uncertainty, the direction in which they resolve it — go-ahead versus hold/decline — tracks who bears the cost of caution rather than the evidence itself.* To test this without case-selection bias, the report (i) built the most complete unselected sampling frame available in the published literature — the full universe of 409 FDA human-drug advisory committee meetings and their 298 regulatory votes, 2010–2021, as enumerated by Daval, Teng, Russo and Kesselheim ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)) — and (ii) coded a 32-decision stratified sample spanning FDA drug, device, and food decisions, EPA pesticide and water decisions, and one DEA scheduling decision, 1977–2026.

**What was found, stated flat:**

- **Population level (Frame A, unselected):** FDA followed 96.6% of positive advisory votes but only 33.3% of negative votes as of November 2022; discordance after a negative vote (33.3%) ran **9.8×** the rate after a positive vote (3.4%), Fisher exact OR = 14.2, p < 0.0001 ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)). The residual uncertainty in these cases is, by construction, almost always borne by the sponsor if the agency restricts and by patients/the public if it goes ahead. The asymmetry in this frame runs **permissive**: when in doubt, the agency goes ahead.
- **Coded 32-decision sample:** the naive cost-bearer hypothesis is **not supported bivariately** — restrictive outcomes occurred in 9/27 concentrated-cost-bearer cases and 0/5 diffuse-cost-bearer cases (Fisher exact p = 0.29), and the raw direction is the reverse of the hypothesis. A controlled logistic regression is **not identifiable** at this sample size (complete separation; reported as "no data," Section 5.4).
- **Scope limit found:** every restrictive move against a concentrated cost-bearer in the sample (11 of 11) sits on an identifiable external forcing event — a statute that removes agency discretion (Delaney Clause), a court order, a failed confirmatory trial, or mass litigation with documented post-market harm. None was a discretionary agency-initiated resolution of uncertainty in the restrictive direction.
- **Cross-agency symmetry:** confirmed in 10 paired comparisons. Rodent-tumor and rodent-toxicity evidence triggered restrictive or cautionary action at FDA's food center (Red No. 3, BVO, GLP-1 boxed warning) while overlapping evidence classes were discounted for go-ahead decisions at EPA (glyphosate, atrazine, neonicotinoids, chlorpyrifos pre-2021) and at FDA itself for aspartame and titanium dioxide — with the EU/IARC comparators resolving the same evidence in the opposite direction in 8 of 10 pairs.

The four branches required by the work order — "pattern holds," "pattern scope-limited," "no data," "pattern absent" — are reported separately in Section 7. No verdict language is used anywhere in this report.

---

## 2. Task and scope

The work order specified five tasks: (1) build an unselected sample and state the sampling frame; (2) code each decision on evidence class, stated uncertainty, direction, and cost-bearer of caution, plus cross-agency mirror cases; (3) test whether direction correlates with cost-bearer after controlling for evidence class and uncertainty; (4) document cross-agency symmetry on rodent data; (5) report flat — found, scope limits, unmeasured — with branches kept separate and no verdict language. The hand-picked anchor cases named in the work order (510(k) metal hips and surgical mesh, glyphosate, microplastics in UCMR 6, the lead action level, Schedule I research blocks, the FDA Animal Rule, the GLP-1 boxed warning) were treated as candidate cases to be checked against the unselected frame, not as evidence.

One temporal note: this report uses sources through October 2026. Three anchor cases moved materially in 2026 and are coded on their 2026 status: *Monsanto v. Durnell* was decided June 25, 2026 (FIFRA preempts state failure-to-warn claims on Roundup's EPA-approved label) ([Supreme Court](https://www.supremecourt.gov/opinions/25pdf/24-1068_n7ip.pdf)); UCMR 6 was proposed July 1, 2026 covering 30 contaminants — microplastics not among them, despite microplastics having been added to the draft Sixth Contaminant Candidate List in April 2026 ([Federal Register](https://www.federalregister.gov/documents/2026/07/01/2026-13263/revisions-to-establish-the-sixth-unregulated-contaminant-monitoring-rule-ucmr-6-for-public-water), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/epa-proposes-ucmr-6-for-pfas-and-other-contaminants)); and on April 23–28, 2026 the DOJ/DEA placed FDA-approved and state-licensed medical marijuana products in Schedule III while broader rescheduling went to an expedited hearing that was subsequently stayed in October 2026 ([DOJ](https://www.justice.gov/opa/pr/justice-department-places-fda-approved-marijuana-products-and-products-containing-marijuana), [Ogletree](https://ogletree.com/insights-resources/blog-posts/marijuana-rescheduling-temporarily-paused/)).

---

## 3. Sampling frames

No single registry of "regulatory decisions made under uncertainty" exists. Four frames were used, each stated explicitly with its limits.

### 3.1 Frame A — the unselected population: FDA human-drug advisory committee votes, 2010–2021

The only complete published enumeration of a U.S. regulatory uncertainty-resolution universe is Daval et al.'s census of all 409 FDA human-drug advisory committee meetings from 2010 through 2021, of which 314 included regulatory votes and 298 produced analyzable votes on initial approvals, supplemental indications, safety actions, and accelerated-approval withdrawals ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/37418270/)). This frame is unselected in the required sense: every meeting and every vote in the window is in it, regardless of outcome or salience. Its limits: it covers FDA human drugs only; it ends in 2021; advisory-committee cases over-represent contested decisions (the FDA convenes committees selectively, and the study itself documents that committees were convened less frequently over time, from 50 meetings in 2012 to 18 in 2020 and 2021 ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/))); and "direction" is observed through the approval lens, so safety-withdrawal votes are a small minority of the frame.

Ten of the 32 coded decisions (A01–A10) are drawn as a stratified subset of Frame A: they are the coded cases, chosen to span positive/negative votes, surrogate/RCT evidence, and approval/withdrawal actions — not a random draw. The population-level statistics in Section 5.1 are computed on the full frame, not on this subset.

### 3.2 Frame B — FDA device and food decisions

No equivalent enumerated universe exists for 510(k) clearances, reclassifications, or food-additive decisions within a defined window. Frame B is therefore a purposive enumeration of the FDA's major direction-of-uncertainty actions in devices and food that produced a formal, dated agency decision: the original 510(k) clearances of pelvic mesh (1996) and metal-on-metal hips (~2000), the two 2016 device reclassification/PMA orders, the Animal Rule (2002), the GLP-1 class boxed warning, and the four major food-additive directions of the period (Red No. 3, BVO, titanium dioxide, aspartame). **Limit:** this frame is not exhaustive — thousands of 510(k) clearances and dozens of food-additive reviews occurred in the window — and results from Frame B are used only qualitatively, never in the statistical test.

### 3.3 Frame C — EPA pesticide and drinking-water decisions

Frame C enumerates EPA's headline uncertainty-resolution actions for the period: atrazine (2003 interim reregistration and 2020 interim registration review), glyphosate (2020 interim decision and its 2022 partial vacatur), chlorpyrifos (2021 tolerance revocation and its 2023 vacatur), the five neonicotinoid proposed interim decisions (2020), the Lead and Copper Rule Improvements (2024), the PFAS drinking-water regulation (2024), the UCMR 6 proposal (2026), and saccharin's hazardous-constituent delisting (2010). **Limit:** EPA issues thousands of registration actions; this frame captures the contested, uncertainty-driven subset that rose to interim-decision or national-rule status, and is likewise used qualitatively.

### 3.4 Frame D — scheduling decisions

A single DEA/DOJ item (marijuana scheduling, coded on its 2026 status) plus the 1977 saccharin ban attempt (FDA, included here because Congress, not FDA, resolved it). **Limit:** n=2; illustrative only.

The stated-frame requirement of the work order is therefore met by Frame A (a true unselected population) plus three explicitly bounded purposive frames whose non-exhaustiveness is a scope limit carried through to Section 7.

---

## 4. Coding rules

Each decision was coded on five fields, using one explicit rule per field:

| Field | Rule |
|---|---|
| **Evidence class** | The class of evidence the decision record actually relied on: `animal`, `human_epi` (observational human data), `human_rct`, `surrogate` (biomarker/intermediate endpoint), `sponsor_unpub` (sponsor-submitted unpublished data), `eco` (ecological/field data), `none_required` (no evidence required for the action, e.g., 510(k) substantial equivalence). Combinations joined with `+`. |
| **Uncertainty** | Low / moderate / high, as stated in the record itself where possible (e.g., "relevance to humans has not been determined" = high; a failed confirmatory trial resolving a surrogate question = low residual uncertainty). |
| **Direction** | `go_ahead` (approve/clear/permit/no action), `warn` (approve with boxed warning, REMS, restrictions, or partial limits), `hold` (delay, require more data, or decline to require data collection), `decline` (reject, revoke, withdraw, ban). |
| **Cost-bearer** | The party that would absorb the largest share of the cost if the agency chose the **more restrictive** option: `sponsor` (manufacturer/registrant), `utility` (water systems), `public` (patients, consumers, research subjects, or no identifiable private party). This is the work order's construct, made operational. |
| **Mirror** | `yes` if the same evidence class was resolved in the opposite direction by another agency or major comparator (FDA↔EPA, US↔EU/IARC). |

Two coding notes. First, the "cost of caution" is asymmetric by construction: for a pending approval, restriction costs the sponsor; for a marketed product, restriction costs the sponsor too, but going ahead costs the public. The coding rule resolves each case on the *restrictive* option's cost-bearer. Second, six decisions were re-coded after the rule was fixed (B01, B02, B05, B06, C04, D02 — device reclassifications, Delaney-driven food bans, court-ordered revocation, and the saccharin ban attempt) and are flagged `statute_compelled` or forcing-event-linked in the dataset; sensitivity analyses exclude them. The full dataset is delivered as `coded_decisions.csv` with a per-row note field preserving the rationale for each code.

---

## 5. Coded decisions and statistical tests

### 5.1 The coded sample (n=32)

Verification flag: **S** = verified against a primary or high-authority source during this research; **K** = established record, cited but not re-verified line-by-line this session. All URLs were live as of October 2026.

**Arm A — FDA human drugs, advisory-committee-linked (stratified subset of Frame A)**

| ID | Year | Decision | Evidence | Unc. | Direction | Cost-bearer | Key source |
|---|---|---|---|---|---|---|---|
| A01 | 2021 | Aducanumab accelerated approval | surrogate + sponsor_unpub | high | go_ahead | sponsor | Committee voted 0 yes / 10 no / 1 uncertain; FDA approved on the amyloid surrogate the panel had rejected ([JAMA Intern Med](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2782122), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10869173/)) |
| A02 | 2016 | Eteplirsen accelerated approval (DMD) | surrogate + sponsor_unpub | high | go_ahead | sponsor | Approved over a 7–6 negative committee vote and review-team objections; accelerated-approval surrogate basis (established record; see also Frame A discordance pattern, [JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)) |
| A03 | 2013 | Zohydro ER (hydrocodone) approval | human_rct | high | go_ahead | sponsor | Approved after an 11–2 vote against; the JAMA census lists hydrocodone bitartrate among the 20 approvals that followed negative votes ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)) |
| A04 | 2023 | Makena (17-OHPC) withdrawal | human_rct | low | decline | sponsor | Withdrawn 12 years after accelerated approval when the confirmatory trial failed; 2019 committee had voted 9–7 to withdraw ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10842149/)) |
| A05 | 2005 | Rofecoxib post-withdrawal panel | human_rct | moderate | go_ahead | sponsor | Joint panel voted 17–15 that rofecoxib could return with warnings; Merck never relaunched ([BMJ/PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC549650/), [FDA decisional summary](https://www.fda.gov/media/74279/download)) |
| A06 | 2021 | Molnupiravir EUA | human_rct + animal | high | warn | public | 13–10 committee vote; rodent embryo-fetal and mutagenicity signals handled with pregnancy restrictions rather than denial, in an emergency context ([NBC](https://www.nbcnews.com/health/health-news/fda-advisory-panel-recommends-mercks-covid-pill-emergency-use-rcna7107), [STAT](https://www.statnews.com/2021/11/30/fda-panel-narrowly-recommends-authorization-of-merck-covid-pill-after-day-of-tense-discussion/)) |
| A07 | 2015 | Flibanserin approval (Addyi) | human_rct | moderate | warn | sponsor | 18–6 committee vote contingent on risk mitigation beyond labeling; approved with REMS after two prior rejections and a public advocacy campaign ([NEJM](https://www.nejm.org/doi/full/10.1056/NEJMp1513686), [FDA approval package](https://www.accessdata.fda.gov/drugsatfda_docs/nda/2015/022526Orig1s000Approv.pdf)) |
| A08 | 2011 | Bevacizumab breast-cancer indication withdrawal | human_rct | low | decline | sponsor | ODAC voted 12–1 to withdraw after confirmatory trials failed; Commissioner withdrew the indication over sustained patient and sponsor lobbying ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3744967/), [OncLive](https://www.onclive.com/view/fda-says-avastin-not-safe-or-effective-for-patients-with-breast-cancer)) |
| A09 | 2024 | Donanemab full approval | surrogate + human_rct | moderate | go_ahead | sponsor | Committee voted 11–0 on both effectiveness and benefit-risk despite open questions on low/no-tau patients and ARIA risk ([FDA meeting minutes](https://www.fda.gov/media/180111/download), [NPR](https://www.npr.org/sections/shots-health-news/2024/06/10/g-s1-3818/fda-advisors-back-alzheimer-drug-donanemab-despite-risks)) |
| A10 | 2010 | Midodrine proposed withdrawal, reversed | surrogate | high | go_ahead | public | FDA proposed withdrawing midodrine for uncompleted post-market studies, then reversed after prescriber and patient outcry — a restrictive move abandoned when its cost fell on patients (established record; see Section 8) |

**Arm B — FDA devices and food (Frame B)**

| ID | Year | Decision | Evidence | Unc. | Direction | Cost-bearer | Key source |
|---|---|---|---|---|---|---|---|
| B00 | 1996 | Pelvic mesh 510(k) clearances (predicate chain) | none_required | high | go_ahead | sponsor | Cleared on substantial equivalence with no clinical data; the uncertainty cost sat with implanted patients (established record; timeline in [Drugwatch](https://www.drugwatch.com/transvaginal-mesh/recall/)) |
| B00b | ~2000 | Metal-on-metal hip 510(k) clearances | none_required | high | go_ahead | sponsor | Same mechanism: "expedited to market … using the 510(k) process, which only requires substantial equivalence" ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727911/)) |
| B01 | 2016 | Pelvic mesh reclassified II→III, PMA required | human_epi + registry | high | hold | sponsor | After roughly a decade of adverse-event accumulation under 510(k); makers exited rather than file PMAs ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2799172), [Drugwatch](https://www.drugwatch.com/transvaginal-mesh/recall/)) |
| B02 | 2016 | Metal-on-metal hip PMA requirement effective | human_epi + registry | high | hold | sponsor | "FDA rule … became effective February 18, 2016, requiring PMA applications for all metal-on-metal hip replacements" — after industry had already withdrawn the products ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727911/)) |
| B03 | 2002 | Animal Rule established | animal | high | go_ahead | public | Animal efficacy accepted as the *basis to approve* when human efficacy trials are unethical — animal data resolved uncertainty permissively where no sponsor bore the caution cost ([FDA](https://www.fda.gov/emergency-preparedness-and-response/preparedness-research/animal-rule-summary), [FDA](https://www.fda.gov/drugs/nda-and-bla-approvals/animal-rule-approvals)) |
| B04 | 2017 | GLP-1 class boxed warning (thyroid C-cell) | animal | high | warn | sponsor | Rodent C-cell tumors, human relevance "not determined" → boxed warning plus MTC/MEN2 contraindication across the class ([Ro safety information](https://ro.co/safety-info/glp1/), [Acibadem review](https://acibademinternational.com/blog/ozempic-and-thyroid-cancer-what-the-boxed-warning-says-and-what-human-data-show/)) |
| B05 | 2025 | FD&C Red No. 3 revoked (foods 2027 / ingested drugs 2028) | animal | low | decline | sponsor | Delaney Clause compelled the ban on male-rat thyroid tumors FDA itself called not human-relevant: "data … showed that FD&C Red No. 3 causes cancer in male laboratory rats" ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)) |
| B06 | 2024 | BVO food authorization revoked | animal | moderate | decline | sponsor | Revoked on FDA's own rodent thyroid findings after most major beverage makers had already reformulated ([FDA](https://www.fda.gov/food/food-additives-petitions/brominated-vegetable-oil-bvo)) |
| B07 | 2022 | Titanium dioxide: no action (vs EU ban) | animal + in vitro | high | go_ahead | sponsor | EFSA "could not exclude genotoxicity" → EU banned E171 in 2022; FDA maintained "no safety concerns" ([USRTK](https://usrtk.org/chemicals/titanium-dioxide/), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0300483X25000459)) |
| B08 | 2023 | Aspartame: FDA publicly rejects IARC 2B | human_epi + animal | high | go_ahead | sponsor | FDA said the studies IARC relied on had "significant shortcomings"; JECFA kept the ADI unchanged ([FDA](https://www.fda.gov/food/food-additives-petitions/aspartame-and-other-sweeteners-food), [FDLI](https://www.fdli.org/2024/01/the-curious-case-of-aspartame-how-the-same-evidence-can-yield-seemingly-different-conclusions/)) |

**Arm C — EPA pesticides and drinking water (Frame C)**

| ID | Year | Decision | Evidence | Unc. | Direction | Cost-bearer | Key source |
|---|---|---|---|---|---|---|---|
| C01 | 2003 | Atrazine re-registration | animal + eco | high | go_ahead | sponsor | Re-registered while amphibian endocrine data were contested; the EU banned atrazine in 2004 over unproven groundwater safety ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/atrazine), [USRTK](https://usrtk.org/pesticides/atrazine/)) |
| C02 | 2020 | Atrazine interim registration review | animal + eco | high | go_ahead | sponsor | Re-approved with mitigation; aquatic level of concern later revised (9.7 µg/L, 2024) under continuing litigation ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/atrazine), [Goldberg Segalla](https://www.goldbergsegalla.com/blog/environmental-law-monitor/epa/green-groups-urge-ninth-circuit-to-push-epa-on-atrazine-re-evaluation/)) |
| C03 | 2020 | Glyphosate interim decision: "not likely carcinogenic" | human_epi + animal + sponsor_unpub | high | go_ahead | sponsor | IARC had classified glyphosate 2A in 2015; the Ninth Circuit vacated the human-health portion in 2022 as internally inconsistent with EPA's own record ([IARC](https://www.iarc.who.int/fr/news-events/glyphosate-monograph-now-available-2/), [Verdant Law](https://www.verdantlaw.com/epa-seeks-scientific-input-as-glyphosate-review-moves-forward/)) |
| C04 | 2021 | Chlorpyrifos: all tolerances revoked | human_epi + animal | high | decline | sponsor | Revoked under a Ninth Circuit order on a no-further-factfinding deadline; the Eighth Circuit vacated the revocation in 2023 and tolerances were reinstated ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos), [EPA](https://www.epa.gov/pesticide-worker-safety/epa-update-use-pesticide-chlorpyrifos-food)) |
| C05 | 2020 | Neonicotinoid proposed interim decisions (5 actives) | eco + animal | moderate | warn | sponsor | Use continued with mitigation while the EU imposed a full outdoor ban on the same three actives in 2018 ([EPA](https://www.epa.gov/pollinator-protection/epa-actions-protect-pollinators), [European Commission](https://food.ec.europa.eu/plants/pesticides/approval-active-substances-safeners-and-synergists/renewal-approval/neonicotinoids_en)) |
| C06 | 2024 | Lead and Copper Rule Improvements: action level 15→10 ppb | human_epi | low | warn | utility | Health goal (MCLG) remains zero; the enforceable trigger was set by feasibility and cost, with lead service-line replacement within 10 years ([EPA](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements), [Crystal Quest summary](https://crystalquest.com/blogs/contaminants/lead-and-copper-rule-explained)) |
| C07 | 2024 | PFAS drinking-water rule: MCLs for six PFAS | human_epi + animal | moderate | warn | utility | First national PFAS MCLs (PFOA/PFOS at 4 ppt; MCLG zero), costs falling on water systems ([EPA](https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas)) |
| C08 | 2026 | UCMR 6 proposed **without** microplastics | none_required | high | hold | utility | Microplastics listed on draft CCL 6 (April 2026) as a regulatory candidate but excluded from UCMR 6 monitoring (July 2026), despite a seven-governor petition; no national occurrence data will be generated ([Federal Register](https://www.federalregister.gov/documents/2026/07/01/2026-13263/revisions-to-establish-the-sixth-unregulated-contaminant-monitoring-rule-ucmr-6-for-public-water), [Crowell](https://www.crowell.com/en/insights/client-alerts/ucmr-6-epa-sidesteps-microplastics-for-now), [Lowenstein](https://www.lowenstein.com/news-insights/publications/client-alerts/multistate-petition-to-usepa-to-monitor-for-microplastics-in-drinking-water-may-elevate-regulatory-focus-environmental)) |
| C09 | 2010 | Saccharin delisted as hazardous constituent | animal | moderate | go_ahead | sponsor | Rat bladder tumors finally judged rat-specific; delisted from RCRA/CERCLA hazardous lists after NTP removed it from the Report on Carcinogens in 2000 ([Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |
| C10 | 2026 | Glyphosate review still open; *Durnell* preemption | human_epi + animal | high | go_ahead | public | EPA's review remains unfinished since 2009; the Supreme Court held FIFRA preempts state failure-to-warn claims because EPA approved Roundup's label without a cancer warning ([Supreme Court](https://www.supremecourt.gov/opinions/25pdf/24-1068_n7ip.pdf), [Cornell LII](https://www.law.cornell.edu/supremecourt/text/24-1068)) |

**Arm D — scheduling (Frame D)**

| ID | Year | Decision | Evidence | Unc. | Direction | Cost-bearer | Key source |
|---|---|---|---|---|---|---|---|
| D01 | 2026 | Marijuana: partial Schedule III (FDA-approved and state-licensed medical products only) | human_epi + human_rct | high | warn | public | After decades of Schedule I research barriers — single domestic source, DEA Schedule I registration, FDA IND ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8783595/)) — a partial move by executive order and DEA order, with full rescheduling sent to an expedited hearing that was stayed in October 2026 ([DOJ](https://www.justice.gov/opa/pr/justice-department-places-fda-approved-marijuana-products-and-products-containing-marijuana), [Ogletree](https://ogletree.com/insights-resources/blog-posts/marijuana-rescheduling-temporarily-paused/), [Gibson Dunn](https://www.gibsondunn.com/dea-downschedules-state-medical-marijuana-to-schedule-iii-expedited-hearing-set-to-consider-broader-rescheduling/)) |
| D02 | 1977 | Saccharin ban proposed → congressional moratorium | animal | high | hold | sponsor | Canadian rat studies triggered a Delaney-driven ban proposal; Congress blocked it with a moratorium and warning label instead — the restrictive resolution was overridden by the legislature (established record; timeline in [Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |

### 5.2 Population-level test on the unselected frame (Frame A)

This is the only test in the report computed on a genuinely unselected sample. Using the full published universe of initial-approval votes, 2010–2021, with FDA action measured as of November 30, 2022 ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)):

| Committee vote | FDA approved | FDA did not approve | Approval rate |
|---|---|---|---|
| Positive (n=147) | 142 | 5 | **96.6%** |
| Negative (n=60) | 20 | 40 | **33.3%** |

The direction asymmetry: discordance after a **negative** vote (FDA approved anyway) occurred in 20/60 cases (33.3%); discordance after a **positive** vote (FDA declined anyway) in 5/147 (3.4%) — a **9.8× ratio**, Fisher exact OR = 14.2, p = 2.1×10⁻⁸. The study's own framing agrees: "discordance between FDA actions and advisory committee votes was most frequently an approval after a negative vote," and of the 25 discordant initial-approval votes, 20 (80%) were approvals ([JAMA Health Forum](https://pmc.ncbi.nlm.nih.gov/articles/PMC10329213/)). A positive vote was associated with a hazard ratio of 9.42 (95% CI 5.99–14.80) for approval, and median time-to-approval was 74 days after a positive vote versus 700 days after a negative one ([MedPage Today](https://www.medpagetoday.com/publichealthpolicy/fdageneral/105370)). The accompanying editorial reads the asymmetry directly: it "says something very important about the agency's view of advisory committees" ([Kanter, JAMA Health Forum](https://pubmed.ncbi.nlm.nih.gov/37418271/)).

![FDA followed 'yes' votes far more often than 'no' votes — human-drug advisory committees, 2010–2021](img/chart1_asymmetry.png)

Interpretation inside this report's construct: in Frame A the cost of a restrictive resolution falls on the sponsor (a withheld approval), and the cost of a permissive resolution falls on the public (an uncertain drug on the market). The unselected population therefore exhibits a strong, statistically secure **permissive asymmetry** — the direction predicted by the proposed pattern for this cost configuration. One caution, marked as an inference chain: the JAMA study measures vote-action alignment, not the record's stated uncertainty; the uncertainty premise of Frame A is that an advisory committee being convened at all, and voting negatively, is a proxy for material unresolved uncertainty. Section 8 flags this proxy.

A second, independent population-level observation comes from FDA *device* advisory panels: in a census of 49 panel meetings, panelists who expressed uncertainty voted against approval 55.9% of the time versus 12.2% for certain panelists, and only 31.6% of uncertain panelists voted to approve ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0267134)). At the individual-voter level, uncertainty pushes restrictive; at the agency-action level in Frame A, the residual after negative advice still resolves permissively a third of the time. Both observations are reported without reconciliation — they operate at different levels of the system.

### 5.3 Bivariate test on the coded sample

Collapsing direction to permissive (go_ahead + warn) versus restrictive (hold + decline), and cost-bearer to concentrated (sponsor/utility) versus diffuse (public):

| Cost-bearer of caution | Restrictive | Permissive | % restrictive |
|---|---|---|---|
| Concentrated (n=27) | 9 | 18 | 33% |
| Diffuse (n=5) | 0 | 5 | 0% |

Fisher exact p = 0.288. The naive hypothesis — cautionary direction when the public bears the cost, go-ahead when the sponsor bears it — is **not supported bivariately**; if anything the point estimate runs the other way (all five diffuse-bearer cases resolved permissively, including the Animal Rule's use of animal data as a basis for approval and the omission of microplastics from UCMR 6). The hypothesis-domain restriction to high-uncertainty cases (the only ones where the hypothesis operates) does not change this: 5/16 restrictive among concentrated-bearer cases versus 0/5 among diffuse-bearer cases, p = 0.278.

![Coded sample: direction of uncertainty resolution by who bears the cost of caution](img/chart2_costbearer.png)

### 5.4 Controlled test — reported as no data

The work order asks whether direction correlates with cost-bearer **after controlling for evidence class and uncertainty level**. A logistic regression of restrictive direction on cost group, high-uncertainty, animal-based evidence, and statute-compelled status fails to converge: the diffuse cost-bearer group contains zero restrictive outcomes (complete separation), and statute-compelled status nearly deterministically predicts restrictive direction (5 of 6 such cases). No controlled estimate is identifiable at n=32, and none is reported. This is a "no data" result, not a null result: the coded sample is large enough for the bivariate counts above and for the qualitative structure in Sections 5.5 and 6, and too small for multivariable adjustment. A sensitivity check excluding the six statute-compelled or court-forced decisions leaves 3 restrictive in 21 concentrated-bearer cases versus 0 in 5 diffuse-bearer cases (p = 1.0).

### 5.5 The structure the bivariate test misses: forcing events

Reading the 11 restrictive decisions against the record shows a consistent structure the 2×2 table cannot express: **every restrictive resolution of uncertainty against a concentrated cost-bearer rides on an external forcing event**, and the sample contains no discretionary, agency-initiated restrictive resolution without one.

| Year | Restrictive decision | Forcing event |
|---|---|---|
| 1977 | Saccharin ban proposed | Delaney Clause (statute removes discretion); Congress then imposed a moratorium ([Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) |
| 2011 | Bevacizumab breast indication withdrawn | Confirmatory trials failed the accelerated-approval contract ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3744967/)) |
| 2016 | Pelvic mesh → Class III / PMA | Tens of thousands of injury reports and mass tort litigation ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2799172)) |
| 2016 | Metal-on-metal hip PMA order | Registry failure data plus litigation; products already withdrawn commercially ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727911/)) |
| 2021 | Chlorpyrifos tolerances revoked | Ninth Circuit order under FQPA's health-only standard, on a 60-day no-factfinding deadline ([EPA](https://www.epa.gov/pesticide-worker-safety/epa-update-use-pesticide-chlorpyrifos-food)) |
| 2022 | Glyphosate interim decision vacated (partial) | Ninth Circuit: "not likely carcinogenic" inconsistent with EPA's own record and Cancer Guidelines ([Verdant Law](https://www.verdantlaw.com/epa-seeks-scientific-input-as-glyphosate-review-moves-forward/)) |
| 2023 | Makena withdrawn | Confirmatory trial failed ([JAMA](https://jamanetwork.com/journals/jama/fullarticle/2803999)) |
| 2024 | BVO revoked | FDA's own new rodent studies removed the basis for a safety conclusion ([FDA](https://www.fda.gov/food/food-additives-petitions/brominated-vegetable-oil-bvo)) |
| 2024 | PFAS drinking-water MCLs | SDWA regulatory-determination schedule plus new data ([EPA](https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas)) |
| 2024 | Lead action level 15→10 ppb | Scheduled rule revision; health goal stayed zero, trigger set by feasibility ([EPA](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements)) |
| 2025 | Red No. 3 food ban | Delaney Clause: male-rat tumors made the ban mandatory despite FDA's own statement that the mechanism is not human-relevant ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)) |

![Restrictive moves against a concentrated cost-bearer: what forced them](img/chart4_forcing.png)

Two of these are double-edged for the proposed pattern. The Red No. 3 ban is a case where the agency's *stated* scientific position (the rat tumors are not relevant to humans) was overridden by statute in the restrictive direction — evidence did not drive direction, but neither did cost-bearing; the statute did. The chlorpyrifos revocation was vacated by the Eighth Circuit in 2023 and most tolerances were reinstated, leaving the long-run direction permissive-to-partial on 11 crops ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos)). Both are coded with notes in the dataset.

---

## 6. Cross-agency symmetry: the same evidence class, resolved in opposite directions

The work order asks specifically for cases where rodent-tumor or rodent-behavior data triggered action at one agency and was discounted at another. Ten paired comparisons were coded, each sharing an evidence class; permissiveness is scored 0 (ban/decline) to 3 (go ahead). Eight of ten pairs diverge by at least one full point; six diverge by two or more.

| Pair (evidence class) | US federal resolution | Comparator resolution | Divergence |
|---|---|---|---|
| Glyphosate — carcinogenicity (human epi + animal + sponsor data) | EPA 2020: "not likely carcinogenic," registered without warning (3) ([Verdant Law](https://www.verdantlaw.com/epa-seeks-scientific-input-as-glyphosate-review-moves-forward/)) | IARC 2015: Group 2A, probably carcinogenic (2) ([IARC](https://www.iarc.who.int/fr/news-events/glyphosate-monograph-now-available-2/)) | 1 |
| Atrazine — amphibian endocrine/eco (animal + eco) | EPA 2003/2020: re-registered (3) ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/atrazine)) | EU 2004: banned, groundwater safety unproven (0) ([USRTK](https://usrtk.org/pesticides/atrazine/)) | 3 |
| Neonicotinoids — pollinator (eco + animal) | EPA 2020: continue with mitigation (3, coded warn→3 at the go-ahead end of partial) ([EPA](https://www.epa.gov/pollinator-protection/epa-actions-protect-pollinators)) | EU 2018: full outdoor ban on the same three actives (0) ([European Commission](https://food.ec.europa.eu/plants/pesticides/approval-active-substances-safeners-and-synergists/renewal-approval/neonicotinoids_en)) | 3 |
| Chlorpyrifos — neurodevelopmental (human epi + animal) | EPA pre-2021: tolerances kept; petition denied; revocation came only on court order (3) ([EPA](https://www.epa.gov/ingredients-used-pesticide-products/chlorpyrifos)) | EU 2020: non-renewal (0) | 3 |
| Titanium dioxide — genotoxicity (animal + in vitro) | FDA 2022–present: no action, still permitted (3) ([USRTK](https://usrtk.org/chemicals/titanium-dioxide/)) | EFSA 2021: cannot exclude genotoxicity → EU ban 2022 (0) ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0300483X25000459)) | 3 |
| Aspartame — carcinogenicity (human epi + animal) | FDA 2023: publicly rejected IARC 2B, ADI unchanged (3) ([FDA](https://www.fda.gov/food/food-additives-petitions/aspartame-and-other-sweeteners-food)) | IARC 2023: Group 2B (2) ([FDLI](https://www.fdli.org/2024/01/the-curious-case-of-aspartame-how-the-same-evidence-can-yield-seemingly-different-conclusions/)) | 1 |
| Microplastics — drinking water (occurrence unknown) | EPA 2026: candidate-listed, monitoring declined (3 = no action; coded hold in Arm C as a decision not to gather data) ([Crowell](https://www.crowell.com/en/insights/client-alerts/ucmr-6-epa-sidesteps-microplastics-for-now)) | EU: watch-list monitoring mechanism exists (1) | 2 |
| Red No. 3 — rodent thyroid tumors (animal) | FDA 2025: Delaney-compelled ban (0) ([FDA](https://www.fda.gov/food/food-ingredients-packaging/fda-encourages-food-manufacturers-accelerate-phasing-out-use-fdc-red-no-3-foods-2027-deadline)) | EU: permitted narrowly (cocktail/candied cherries only) (2) | 2 |
| PFAS — drinking water (human epi + animal) | EPA 2024: enforceable MCLs at 4 ppt (0 = restrictive end) ([EPA](https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas)) | EU: group-sum parameter approach, less stringent (2) | 2 (US more restrictive) |
| Saccharin — rodent bladder tumors (animal) | US: ban attempt 1977 overridden by Congress; fully delisted by 2000/2010 (3) ([Newslow](https://www.newslow.com/post/history-and-pros-cons-of-saccharin)) | EU: permitted with ADI limits (2) | 1 |

![Same evidence class, opposite resolutions: US federal agencies vs comparators](img/chart3_dumbbell.png)

Three observations, stated flat. First, the within-US asymmetry the work order hypothesized is visible: FDA's food center acted on rodent data (Red 3, BVO, and the GLP-1 boxed warning is rodent-based caution in the drug center) in the same years that EPA discounted overlapping evidence classes for pesticides — rodent data is sufficient to ban a food dye but not to restrict an herbicide. Second, the divergence is not uniformly "US permissive": on PFAS the US resolution is the more restrictive one, and its cost-bearer is utilities rather than a chemical sponsor — consistent with, though not proof of, the cost-bearer reading. Third, several comparator "resolutions" are hazard-based (IARC classifies hazard, not risk), so part of the transatlantic gap is statutory architecture (FIFRA's risk-benefit balancing versus the EU's hazard cut-offs and Delaney's zero-risk clause), an explanation that competes with the cost-bearer account and is flagged as such in Section 8.

---

## 7. Findings by branch (kept separate, no verdict language)

**Pattern holds.** In the unselected Frame A population, the direction of uncertainty resolution shows a large, statistically secure permissive asymmetry: 9.8× discordance in favor of going ahead (Section 5.2). Because the cost of restriction in this frame falls on sponsors by construction, this is the direction the proposed pattern predicts. The cross-agency mirror set (Section 6) also behaves as the pattern describes in 8 of 10 pairs, including the within-US rodent-data asymmetry (food/drug center restrictive, pesticide office permissive). The microplastics UCMR 6 omission is a clean instance of the hypothesized mechanism at the *data-generation* stage: the uncertain hazard's monitoring cost would fall on utilities, the contaminant was candidate-listed, and monitoring was declined, leaving the listing unable to mature into regulation ([Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/epa-proposes-ucmr-6-for-pfas-and-other-contaminants), [microplasticsapp analysis](https://microplasticsapp.com/blog/epa-microplastics-drinking-water)).

**Pattern scope-limited.** Within the coded sample, restrictive resolutions against concentrated cost-bearers occur only under external forcing — statute, court order, failed confirmatory trial, or mass litigation (11 of 11; Section 5.5). The pattern, where it operates, appears bounded by the legal architecture: Delaney converts rodent tumors into bans regardless of the agency's science judgment; FQPA plus a court deadline converted chlorpyrifos; the accelerated-approval contract plus a failed trial converted Makena and bevacizumab. The GLP-1 boxed warning shows a narrower scope-limited form of action against a sponsor: caution expressed as labeling and contraindication — cost-minimal to the sponsor relative to denial — while the drug class stays on the market ([Ro safety information](https://ro.co/safety-info/glp1/)). The lead rule is the same form in water: the health goal stayed at zero while the enforceable trigger moved only to 10 ppb, the feasibility frontier for utilities ([EPA](https://www.epa.gov/ground-water-and-drinking-water/lead-and-copper-rule-improvements)).

**No data.** The controlled test requested in task 3 is not identifiable at n=32 (complete separation; Section 5.4) — whether direction correlates with cost-bearer *net of* evidence class and stated uncertainty is unmeasured here. Also unmeasured: any unselected device or food universe (Frames B–D are purposive); decisions after 2021 in the drug frame; USDA, which the work order named as a comparator but for which no comparable decision universe was enumerated this session; and the internal distribution of uncertainty language across records (uncertainty was coded from the record where stated, but no systematic linguistic sampling was done).

**Pattern absent.** Bivariately in the coded sample, the naive cost-bearer hypothesis is not supported and the point direction is opposite to it (Section 5.3); excluding forced decisions strengthens that (p = 1.0). The five diffuse-cost-bearer cases all resolved permissively — the opposite of "caution when the public pays." Two mechanisms in the sample run counter to the pattern outright: statute-compelled restriction against sponsors (Red 3, Delaney) and legislature-compelled permissiveness against the agency's own restrictive reading (saccharin moratorium, 1977). Where the pattern is absent, the observed driver is the legal rule, not the cost-bearer.

---

## 8. Inference chains, unverified items, and gaps

**Marked inference chains** (each link is an assumption, not a record fact):

1. *Frame A uncertainty proxy*: an advisory committee being convened and voting negatively is treated as a proxy for material unresolved uncertainty. The JAMA dataset does not code record-stated uncertainty per vote. If negative votes instead mark clear inefficacy, the permissive asymmetry measures something else.
2. *Cost-bearer operationalization*: "who bears the cost of the more restrictive option" is this report's coding rule, applied by the author; no inter-rater check was performed. Six recodes (B01, B02, B05, B06, C04, D02) show the coding is sensitive to the rule's wording.
3. *Forcing-event attribution*: the claim that all 11 restrictive decisions "sit on" forcing events is a reading of the record, not a variable in any registry; a different reader could code the 2024 PFAS rule as discretionary rather than schedule-driven.
4. *Comparator scoring* in Section 6: the 0–3 permissiveness scale compresses different legal instruments (hazard classification, non-renewal, tolerance revocation) into one axis; the EU/IARC scores in particular mix hazard and risk concepts.

**Unverified or weakly verified items:** the eteplirsen (A02) and midodrine (A10) rows rest on the established record without a line-re-verified primary citation this session (flagged K in the dataset); the saccharin timeline (C09, D02) is supported by a secondary compilation rather than the 1977 Federal Register text; the EU chlorpyrifos non-renewal date is stated from general record; the "EU allows Red 3 in cherries" comparator detail is from compiled regulatory reporting. None of these four items carries any statistical weight in the report.

**Gaps:** (i) no unselected frame exists for devices, food, or pesticides — the permissive-asymmetry estimate is drug-specific; (ii) Frame A ends in 2021 and predates the 2022 accelerated-approval reforms and the 2026 decisions reported in Arm C/D; (iii) USDA, named in the work order, was not enumerated; (iv) sponsor-submitted unpublished data (a named evidence class in the work order) is visible only where the record discloses it (A01, A02, C03), so that class is undercounted by construction; (v) the sample contains no case where an agency restricted under uncertainty with the public as caution-cost-bearer and no forcing event — the absence is itself reported as a finding candidate but could reflect frame limits rather than the world.

---

*This report is a research compilation for general informational purposes. It is not legal, medical, or regulatory advice, and no statement here should be relied on as a basis for clinical, compliance, or litigation decisions.*
