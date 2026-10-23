# SPDX-License-Identifier: CC0-1.0
"""
curation_ncr.py -- the corrective-action layer, as data: sources, the
source statements an NCR corrects (located by substring in the pinned
files, never by remembered line numbers), NCRs, and the CHANGE records that
tools/build.py applies.

Every NCR here is adjudicated by ACT-REGISTRY. Review items R1-R14 were
originated by ACT-REVIEWER, a different session; the adjudicator read each
item before adjudicating it, so independence is CONTAMINATED-BY-PRIOR, never
BLIND. Audit items N01-N24 were originated AND adjudicated by ACT-REGISTRY:
independence NOT_INDEPENDENT, and each is flagged single-failure until a
second party checks it.

Rigor tier (graded approach, schema/QA_MAPPING.md):
    T1  moves a statistic the revised report states, or the status of a
        decision whose C_permit grade is C4; the disposition must be
        reproduced by a tool (stats.py) and rest on a ledger row
    T2  moves a field without moving a reported statistic; ledger row
    T3  wording or bookkeeping; text check

CHANGE records
    kind      pin | recode | retype | add_object | add_field | add_vocab
    object    registry id, or a frame row key "C2:<chemical>"
    field     the field changed
    from, to  build.py asserts the pinned source carries `from` before it
              writes `to`; a CHANGE whose `from` does not match the source
              fails the build, so this log cannot drift from the data
"""

CODER = "ACT-REGISTRY"
DATE = "2026-10-21"

# ---------------------------------------------------------------- sources

HOST_KIND = [
    ("federalregister.gov", "primary_record"), ("govinfo.gov", "primary_record"),
    ("accessdata.fda.gov", "primary_record"), ("regulations.gov", "primary_record"),
    ("supremecourt.gov", "court"), ("law.cornell.edu", "court"),
    ("cdn.ca9.uscourts.gov", "court"), ("ca8.uscourts.gov", "court"),
    ("pmc.ncbi.nlm.nih.gov", "peer_reviewed"), ("pubmed.ncbi", "peer_reviewed"),
    ("jamanetwork.com", "peer_reviewed"), ("nejm.org", "peer_reviewed"),
    ("journals.plos.org", "peer_reviewed"), ("sciencedirect.com", "peer_reviewed"),
    ("nature.com", "peer_reviewed"), ("academic.oup.com", "peer_reviewed"),
    ("fda.gov", "agency_page"), ("epa.gov", "agency_page"),
    ("justice.gov", "agency_page"), ("dea.gov", "agency_page"),
    ("iarc.who.int", "agency_page"), ("ec.europa.eu", "agency_page"),
    ("efsa.europa.eu", "agency_page"), ("osha.gov", "agency_page"),
    ("nrc.gov", "standard"), ("ecfr.gov", "primary_record"),
    ("iec.ch", "standard"), ("gradeworkinggroup.org", "standard"),
    ("ipcc.ch", "standard"), ("asme.org", "standard"),
    ("hklaw.com", "law_firm"), ("ogletree.com", "law_firm"),
    ("crowell.com", "law_firm"), ("lowenstein.com", "law_firm"),
    ("gibsondunn.com", "law_firm"), ("goldbergsegalla.com", "law_firm"),
    ("verdantlaw.com", "law_firm"), ("mayerbrown.com", "law_firm"),
    ("lawbc.com", "law_firm"),
    ("nbcnews.com", "news"), ("statnews.com", "news"), ("npr.org", "news"),
    ("medpagetoday.com", "news"), ("onclive.com", "news"),
    ("fdli.org", "secondary"), ("usrtk.org", "secondary"),
    ("drugwatch.com", "secondary"), ("newslow.com", "blog"),
    ("ro.co", "secondary"), ("acibademinternational.com", "blog"),
    ("crystalquest.com", "blog"), ("microplasticsapp.com", "blog"),
    ("wikipedia.org", "secondary"),
]

# (id, label, path relative to the folder, superseded?)
BUNDLE_SOURCES = [
    ("SRC-K3-CSV", "coded_decisions_v3.csv", "bundle/source/current/coded_decisions_v3.csv", False),
    ("SRC-K2-ANNEX", "annex_a_regrading_v2.csv", "bundle/source/current/annex_a_regrading_v2.csv", False),
    ("SRC-K2-FRAME", "epa_frame_2022.csv", "bundle/source/current/epa_frame_2022.csv", False),
    ("SRC-K3-SWEEP", "calibration_sweep_v3.csv", "bundle/source/current/calibration_sweep_v3.csv", False),
    ("SRC-K2-REPORT", "direction_of_uncertainty_report_v2.md", "bundle/source/current/direction_of_uncertainty_report_v2.md", False),
    ("SRC-K3-SENS", "sensitivity_upgrades_v3.md", "bundle/source/current/sensitivity_upgrades_v3.md", False),
    ("SRC-K2-STD", "regulatory_uncertainty_standard_v02.md (RUS-0.2)", "bundle/source/current/regulatory_uncertainty_standard_v02.md", False),
    ("SRC-K-CHANGELOG", "change_log_v2.md (v1->v2, v2->v3)", "bundle/source/current/change_log_v2.md", False),
    ("SRC-K1-CSV", "coded_decisions.csv (v1, superseded)", "bundle/source/superseded/v1/coded_decisions.csv", True),
    ("SRC-K1-ANNEX", "annex_a_regrading.csv (v1, superseded)", "bundle/source/superseded/v1/annex_a_regrading.csv", True),
    ("SRC-K1-REPORT", "direction_of_uncertainty_report.md (v1, superseded)", "bundle/source/superseded/v1/direction_of_uncertainty_report.md", True),
    ("SRC-K1-STD", "regulatory_uncertainty_standard_draft.md (RUS-0.1, superseded)", "bundle/source/superseded/v1/regulatory_uncertainty_standard_draft.md", True),
    ("SRC-K2-CSV", "coded_decisions_v2.csv (superseded)", "bundle/source/superseded/coded_decisions_v2.csv", True),
    ("SRC-REVIEW-1", "REVIEW_v1.md", "bundle/reviews/REVIEW_v1.md", False),
    ("SRC-REVIEW-2", "REVIEW_v2.md", "bundle/reviews/REVIEW_v2.md", False),
    ("SRC-REVIEW-3", "REVIEW_v3.md", "bundle/reviews/REVIEW_v3.md", False),
    ("SRC-WO", "WO-REG-1 (consolidated, with 1a and 1b)", "bundle/WORK_ORDER.md", False),
    ("SRC-WO-OLD", "WO-REG-1 and WO-REG-1a as first delivered (superseded by SRC-WO)", "WORK_ORDER.md", True),
]

# ---------------------------------------------------------------- statements
#
# Source statements that an NCR corrects. Each becomes an EVIDENCE node
# (kind statement) with verification CORRECTED and the registry's value
# beside it. `needle` must occur exactly once in the file or the build
# fails; the line number is computed, never typed.
#   (id, source id, needle, ncr, registry value (text; numbers come from
#    stats.py keys named in braces and are filled at build))

STATEMENTS = [
    ("ST-01", "SRC-K2-REPORT", "**34/34 permissive**", "NCR-R6",
     "{c2_permissive} of {c2_merit} merit decisions permissive, {c2_restrictive} restrictive (pentachlorophenol, cancellation required); {c2_na} case closures coded NA"),
    ("ST-02", "SRC-K2-REPORT", "**all 34 continued registration**", "NCR-R6",
     "{c2_permissive} of {c2_merit} continued registration; pentachlorophenol cancellation required (87 FR 6535; G001, G002)"),
    ("ST-03", "SRC-K3-SENS", "in the unselected EPA frame (34/34 continuations)", "NCR-R6",
     "{c2_permissive}/{c2_merit} continuations; pentachlorophenol restrictive and discretionary"),
    ("ST-04", "SRC-K2-REPORT", "**BVO is the lone discretionary restrictive action**", "NCR-R6",
     "two discretionary restrictive actions across the coded sample and Frame C2 (BVO, pentachlorophenol); BVO's discretionary status contested by the earlier California statute (G024)"),
    ("ST-05", "SRC-K2-REPORT", "Corrected finding: **7 of 8 restrictive agency actions ride an external forcing event; BVO is the lone discretionary exception.**", "NCR-R14",
     "{forced_list_forced} of {forced_list_n} restrictive agency actions in the coded sample carry a forcing event (A10 coded as an unmet post-market requirement); {forced_all_forced} of {forced_all_n} with Frame C2's pentachlorophenol"),
    ("ST-06", "SRC-K2-REPORT", "**The naive hypothesis is not supported bivariately, and v2 strengthens that null.**", "NCR-R11",
     "not testable at this n under Rule S (diffuse cell n=2); the v2 recode removed information, it did not strengthen a null"),
    ("ST-07", "SRC-K-CHANGELOG", "The bivariate \"pattern absent\" result **strengthens**.", "NCR-R11",
     "a weaker test (diffuse cell 5 -> 2), not a stronger null"),
    ("ST-08", "SRC-K2-REPORT", "8 of 10 divergent, six by two or more points", "NCR-N10",
     "{mirror_divergent} of 10 divergent, {mirror_ge2} by two or more points, recomputed from the v1 Section 6 table the sentence summarizes"),
    ("ST-09", "SRC-K3-SENS", "Of 24 permissive actions, **zero** were reversed toward restrictive within their decision's lifetime.", "NCR-R14",
     "on action: 1 permissive action vacated within its lifetime (C03, court, on petition of public-interest litigants); on legal status: 0 moved to restrictive"),
    ("ST-10", "SRC-K3-SENS", "16–20 years later", "NCR-N20",
     "{rev_b_min}-{rev_b_max} years: the POP mesh clearance chain starts 2002, not 1996 (1996 is the first SUI sling clearance; G035)"),
    ("ST-11", "SRC-K3-SENS", "Agency reversed after prescriber/patient outcry; proposal never effectuated", "NCR-N19",
     "August 2010 proposal; September 2010 clarification that the drug could stay on the market; February 2012 withdrawal deferred by agreement with the sponsor for two further studies (G010)"),
    ("ST-12", "SRC-K3-SENS", "the below-floor count ranges from 15 to 25 of 33", "NCR-R13",
     "{sweep_below_min}-{sweep_below_max} of 33 across the variants the registry reproduces (M0-M5) and M7; {sweep_below_min}-25 if M6's published 25 is taken as stated, though no U3 row reproduces it (NCR-N07)"),
    ("ST-13", "SRC-K3-SENS", "**over-restrictive violations are zero in every variant**", "NCR-R13",
     "zero over-restrictive in the source sample on the annex basis is untestable ({over_possible_annex} rows could produce it); on the action basis A10 grades over-restrictive; with the R8 rows D03, D04 the branch fires"),
    ("ST-14", "SRC-K-CHANGELOG", "Corpus is permissive in **both** error directions", "NCR-R12",
     "one direction: where denial harm dominates, decisions came in one class more permissive than the floor; no restricting row with C_restrict > C_permit in the source sample"),
    ("ST-15", "SRC-K2-REPORT", "Read flat: direction and cost-bearer coding are reasonably robust to an instrument change", "NCR-R10",
     "reliability figure for direction is pass 1, kappa 0.45 (70% agreement); pass 2 (kappa 0.76) followed a rule adopted after pass-1 disagreements were inspected and is a codebook revision"),
    ("ST-16", "SRC-K3-SENS", "gated by external forcing in 7 of 8 cases, reversed toward permissive in 3 of 9", "NCR-R14",
     "one list: {forced_list_forced} of {forced_list_n} carry a forcing event and {rev_toward_perm} of {forced_list_n} were reversed toward permissive"),
    # ST-17 withdrawn before the first build: see NCR-N09 (REJECT)
    ("ST-18", "SRC-K-CHANGELOG", "**zero over-restrictive non-conformities. One-directional non-conformity survives the two-sided re-grade.**", "NCR-N02",
     "zero on the annex's mixed basis; on the action basis A10 is over-restrictive (C_restrict 5 > C_permit 3, decline D5 against floor D2)"),
    ("ST-19", "SRC-K2-STD", "Full audit trail with per-axis scores and rationales: `annex_a_regrading_v2.csv`.", "NCR-N01",
     "the delivered annex carries axis sums only; per-axis C_permit recovered from the superseded v1 annex for {cp_axes_recovered} of 33 rows; per-axis C_restrict coded by the registry"),
]

# ---------------------------------------------------------------- NCRs
#
# (id, origin, ref, items, evidence, finding, disposition, reason, changes,
#  state, tier, note)

R = "CONTAMINATED-BY-PRIOR"
A = "NOT_INDEPENDENT"

NCRS = [
    # ---- REVIEW_v1 (applied by the originator in v2; checked against v2/v3)
    ("NCR-R1", "REVIEW_v1", "R1", ["FRAME-A"], ["V002"],
     "Executive-summary wording ('followed only 33.3%'); Frame A has no cost-bearer variation, so 'pattern holds' overstates.",
     "ACCEPT", "v2 Fix 1 and Fix 2 applied: the report states FDA followed 40/60 negative votes and approved 20/60 anyway, and reports Frame A as 'permissive skew, no contrast group' with four rival explanations; both checked in the pinned v2 text by stats.py.",
     [], "CLOSED", "T3", None),
    ("NCR-R2", "REVIEW_v1", "R2", ["C10", "A06", "B03", "C08", "D02"], ["V009", "V021", "V033", "V011", "V063"],
     "Diffuse bin holds sponsored products; C08 sign flipped (verb vs cost-bearer); D02 final outcome permissive; result is not testable at this n.",
     "ACCEPT", "v2 recodes present in coded_decisions_v3.csv (C10/A06/B03 cost_bearer sponsor; C08 go_ahead; D02 warn). The registry stores direction twice: direction_verb (the v1 coding, which coded the verb) and direction (relative to the bearer of the cost of caution). 'Not testable' wording carried to NCR-R11.",
     [], "CLOSED", "T1", None),
    ("NCR-R3", "REVIEW_v1", "R3", ["B06"], ["V039"],
     "'11 of 11' against 9 restrictive rows; BVO discretionary.",
     "ACCEPT", "v2 Fix 5 restricted the forcing count to agency actions and reclassified BVO. Residuals: the 7-of-8 / 3-of-9 denominator drift (NCR-R14) and a second discretionary restriction (NCR-R6).",
     [], "CLOSED", "T1", None),
    ("NCR-R4", "REVIEW_v1", "R4", ["RUS-0.1", "B05"], [],
     "RUS-0.1 scores only the harm of a wrong permit; B05 graded U1 against M2; Annex A called an independent replication.",
     "ACCEPT", "v2 Fix 6 (two-sided consequence), Fix 7 (B05 U3 by M2) and Fix 8 (replication claim withdrawn) present. Residual: the R2 margin rule stays asymmetric (NCR-R7).",
     [], "CLOSED", "T1", None),
    ("NCR-R5", "REVIEW_v1", "R5", ["E01"], ["V080", "V081", "V082", "V083", "V084", "V085", "V086", "V087", "G012", "G013"],
     "Add night shift work; code exposure by rotation pattern, never ever/never.",
     "MODIFY", "Loaded as E01 from the bundle (the earlier registry's C11; CHG-INPUT-03). Exposure is typed by rotation pattern; no located source codes it that way, so every E01 evidence node carries rotation_pattern 'not_coded' and the gap is EA-05. Retyped NON_DECISION (NCR-N18). Denmark compensation: a secondary review quote is seen (G013), the Danish primary is not located and the count varies 37/38/40 across secondary sources (G012).",
     ["CHG-INPUT-03", "CHG-N18-05", "CHG-N11-01"], "OPEN", "T2", "open on the Danish primary record"),
    # ---- REVIEW_v2
    ("NCR-R6", "REVIEW_v2", "R6", ["FRAME-C2", "C2:Pentachlorophenol"], ["G001", "G002"],
     "Pentachlorophenol is a required cancellation, coded go_ahead; case closures coded go_ahead; notice-level coding; Frame C2 has no cost-bearer variation.",
     "ACCEPT", "EPA release and 87 FR 6535 seen at search-index depth (G001, G002 MATCH). Pentachlorophenol recoded decline, discretionary (no statute or court forcing located); six case closures recoded NA and excluded from direction counts; sponsor exit logged as a gap, not as permissive. The '34/34' statements (ST-01, ST-02, ST-03) and 'lone discretionary' (ST-04, ST-05) are superseded by computed values.",
     ["CHG-R6-01", "CHG-R6-02", "CHG-R6-03", "CHG-R6-04", "CHG-R6-05", "CHG-R6-06", "CHG-R6-07"], "CLOSED", "T1",
     "document-level coding of the 34 decisions not run (gap FR-C2-DOCS)"),
    ("NCR-R7", "REVIEW_v2", "R7", ["RUS-0.2 R2"], [],
     "R2 tolerance is -1 on one side and +1 (with C_restrict > C_permit) on the other.",
     "MODIFY", "Published as variant M7 (symmetric: one class below the floor conforms by margin) in RUS-0.3, beside, not replacing, R2 as published. Reviewer's 14 below floor under M0+M7 reproduces (stats.py).",
     [], "CLOSED", "T1", None),
    ("NCR-R8", "REVIEW_v2", "R8", ["D03", "D04", "D01"], ["G018", "G019", "G020", "G021", "G034"],
     "No restrictive row has C_restrict > C_permit, so R2's over-restrictive test cannot fire; add restrictive-side candidates.",
     "MODIFY", "Added D03 (2016 denial of marijuana rescheduling petitions) and D04 (psilocybin held in Schedule I through 2025) as PROPOSED rows, one coder, selected on direction, never pooled into a test of the sample. D01 is the loosening of a self-sealing restriction (R6b). FDA clinical holds: no public FDA listing located (FR-CLINHOLD). Refuse-to-file / complete response letters: the July 2025 CRL release exists (G021) and was not loaded (egress; FR-CRL-2025).",
     ["CHG-R8-01", "CHG-R8-02"], "OPEN", "T1", "open on a stated-window frame of FDA restrictive actions"),
    ("NCR-R9", "REVIEW_v2", "R9", ["C07"], ["G023"],
     "C_restrict is lowered wherever 'alternatives exist' without scoring the alternative.",
     "MODIFY", "Rule S in RUS-0.3: the alternatives credit stands only when the alternative is named AND graded with a C_permit grade below the case's own; otherwise C_restrict + 1. No alternative is graded anywhere in the bundle, so every credited row loses the credit under S. Reference case PFOA -> HFPO-DA (GenX), recorded on C07 (G023 UNSEEN at search depth).",
     ["CHG-R9-01"], "CLOSED", "T1", None),
    ("NCR-R10", "REVIEW_v2", "R10", ["SECOND-CODER-B"], [],
     "Coder B pass 2 used a rule adopted after inspecting pass-1 disagreements.",
     "ACCEPT", "Reliability figure for direction is pass 1, kappa 0.45. Pass 2 (0.76) is reported as codebook revision. The registry's own second coder (ACT-CODER2) is a separate exercise with its own contamination probe.",
     [], "CLOSED", "T2", None),
    ("NCR-R11", "REVIEW_v2", "R11", ["CHANGELOG", "E01"], ["G012", "G013"],
     "'Null strengthens' framing; Denmark K-flag.",
     "ACCEPT", "Wording superseded (ST-06, ST-07). Denmark: secondary quote seen (G013); primary not located; the K-flag stays as an UNREACHABLE evidence node, not as a verified fact.",
     [], "OPEN", "T3", "open on the Danish primary record"),
    # ---- REVIEW_v3
    ("NCR-R12", "REVIEW_v3", "R12", ["A01", "A02", "A06", "A09"], [],
     "'Permissive in both error directions' is a logic error.",
     "ACCEPT", "Going ahead where denial harm dominates avoids the denial error; an error in the second direction needs a restricting row with C_restrict > C_permit, which the source sample does not hold. Statement superseded (ST-14). On the action basis A10 is such a row (NCR-N02).",
     [], "CLOSED", "T3", None),
    ("NCR-R13", "REVIEW_v3", "R13", ["SWEEP"], [],
     "The sweep changes the matrix, not the rows, so 'zero over-restrictive in every variant' is structurally guaranteed; add M7; 15-25 should read 14-25.",
     "ACCEPT", "stats.py reports, per variant, the count of rows on which the over-restrictive branch can fire at all; on the annex basis it is zero in every variant (the sweep holds the actuals, and no row whose own actual is D3 or above has C_restrict > C_permit), so the zero is reported HOLDS_UNTESTABLE. Six rows could produce it had the agency restricted (over_reachable). Below-floor range with M7: 14-23 over the reproduced variants, 14-25 with M6's published value (M6 not reproducible, NCR-N07).",
     [], "CLOSED", "T1", None),
    ("NCR-R14", "REVIEW_v3", "R14", ["C03", "A10", "B00", "B00b", "B01", "B02"], ["G006", "G007", "G010", "G033", "G014", "G015", "G032", "G035"],
     "Reversals encoded inside rows; C03 is a permissive action vacated by a court; one restrictive-action list with A10's forcing coded; test reversal speed by initiator.",
     "ACCEPT", "REVERSAL objects link decisions (WO-REG-1b); C03 coded as a permissive action vacated within its lifetime with the products remaining on the market; A10 forcing coded unmet_postmarket_requirement (inference: the requirement dates from the 1996 approval); one list from action_direction; reversals.py tests time-to-reversal by direction with an exact Mann-Whitney test.",
     ["CHG-R14-01", "CHG-R14-02", "CHG-R14-03"], "CLOSED", "T1", None),
    # ---- AUDIT (originated and adjudicated by the registry: single-failure)
    ("NCR-N01", "AUDIT_WO-REG-1", "RUS-0.2 Annex A", ["ANNEX"], [],
     "The standard says the annex carries per-axis scores and rationales; the delivered CSV carries C_permit and C_restrict sums only.",
     "MODIFY", "Per-axis C_permit recovered from the superseded v1 annex where its sums equal the v2 sums; E01 has no per-axis source (gap). Per-axis C_restrict coded by the registry as a second coding beside the source sums; grading runs on both (single-failure check).",
     ["CHG-N01-01"], "CLOSED", "T1", None),
    ("NCR-N02", "AUDIT_WO-REG-1", "Annex A actual column", ["A10", "C04", "D02"], [],
     "The annex grades D02 and A10 on the legal outcome and C04 on the agency action.",
     "MODIFY", "Every row is graded on both bases and on the annex's own mixed basis; on the action basis A10 grades over-restrictive with denial harm (C_restrict 5 > C_permit 3, actual D5, floor D2).",
     [], "CLOSED", "T1", None),
    ("NCR-N03", "AUDIT_WO-REG-1", "coded_decisions_v3.csv B06", ["B06"], ["V039", "G024"],
     "statute_compelled = 1 on B06 while the report and the annex treat BVO as discretionary.",
     "MODIFY", "No federal statute or court compelled the revocation; the source flag is kept as the source's claim and the registry's statute_compelled is 0. The California statute (AB 418, 2023) preceded FDA's final rule and is recorded as a contested candidate forcing event, not as compulsion.",
     ["CHG-N03-01"], "CLOSED", "T1", None),
    ("NCR-N04", "AUDIT_WO-REG-1", "Annex A D02", ["D02"], ["G011", "V063"],
     "D02 carries statute_compelled = 1 (v1, v2 and v3 alike) and its coded direction (warn) is the outcome compelled by Pub. L. 95-203, yet the annex grades it NON-CONFORM: below floor rather than under R3. The source's flag and its own annex disagree.",
     "MODIFY", "statute_compelled kept (the source's value is right); the R3 flags the registry grades on (forced_action: the 1977 proposal under the Delaney clause; forced_outcome: Pub. L. 95-203) recoded True. The annex value is reproduced as published beside the registry's.",
     ["CHG-N04-01", "CHG-N04-02"], "CLOSED", "T1", None),
    ("NCR-N05", "AUDIT_WO-REG-1", "B05 uncertainty", ["B05"], ["V038"],
     "B05 carries two uncertainty values: record-stated low in the dataset, U3 by M2 in grading.",
     "ACCEPT", "Both stored, as uncertainty (source) and U_grade (derived by M2); R1 needs U1-U2 and is not reachable at U3.",
     [], "CLOSED", "T3", None),
    ("NCR-N06", "AUDIT_WO-REG-1", "RUS-0.2 R1", ["C06", "C07", "A05"], [],
     "R1 reads 'evidence at U1-U2 of actual harm or absent benefit => D5'. C06 (U1) and C07 (U2) carry established harm and no claimed benefit; the annex does not apply R1 to them. For a contaminant level, D5 (decline) has no referent.",
     "MODIFY", "RUS-0.3 scopes R1 to decisions that set market status ([CHOICE] r1_scope); level-setting rows (C06, C07, C08, E01) are graded by the matrix. The literal reading is published as variant R1L. A05 (harm established, benefit claimed) is the boundary case and is graded without R1 under both readings.",
     [], "CLOSED", "T1", None),
    ("NCR-N07", "AUDIT_WO-REG-1", "calibration_sweep_v3.csv M6", ["SWEEP"], [],
     "M6 ('M2 + U3 strict') states no U3 row; no U3 row under any of four column rules reproduces 25/6/0/0/2 (closest 24/6/1/0/2).",
     "REJECT", "Not reproducible from the delivered definitions; M6 is reported as published and marked not reproducible; ranges computed by the registry exclude it and say so.",
     [], "CLOSED", "T1", None),
    ("NCR-N08", "AUDIT_WO-REG-1", "calibration_sweep_v3.csv M4", ["SWEEP"], [],
     "M4 ('U3 row relaxed') states no U3 row.",
     "MODIFY", "Reconstructed: U3 = [D1, D2, D3, D3] is the unique row (exhaustive search) that reproduces 16/11/4/0/2; marked reconstructed.",
     [], "CLOSED", "T2", None),
    ("NCR-N09", "AUDIT_WO-REG-1", "sensitivity_upgrades_v3.md section 3", ["SWEEP"], [],
     "The sweep table lists M0 twice.",
     "REJECT", "Not reproduced against the pinned file: sensitivity_upgrades_v3.md section 3 lists each of M0-M6 once (one occurrence of the M0 row). The duplicate was read in a rendering of the document before it was landed and pinned; the finding and its statement node (ST-17) are withdrawn before the first build. The two M3 labels agree once 'col2' is counted from 1: 'floor minimized (uniform column)' and '(all G->col2)' both put every row in the G = 0 column, which reproduces 21/6/4/0/2; counted from 0 (the G = 1-2 column) it gives 25/5/1/0/2.",
     [], "CLOSED", "T3", "withdrawn finding kept under its id (ids are permanent)"),
    ("NCR-N10", "AUDIT_WO-REG-1", "report v2 section 7", ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10"], [],
     "'8 of 10 divergent, six by two or more points' does not follow from the v1 table it summarizes.",
     "MODIFY", "Recomputed from the pair scores: every pair diverges by at least one point, seven by two or more. Statement superseded (ST-08).",
     [], "CLOSED", "T1", None),
    ("NCR-N11", "AUDIT_WO-REG-1", "coded_decisions_v3.csv E01", ["E01"], [],
     "E01 cost_bearer is coded sponsor; the annex rationale names employers.",
     "MODIFY", "Source value kept (cost_group concentrated either way, so no statistic moves); cost_bearer_detail 'employer' added.",
     ["CHG-N11-01"], "CLOSED", "T2", None),
    ("NCR-N12", "AUDIT_WO-REG-1", "coded_decisions_v3.csv E01", ["E01"], [],
     "E01 is a non-decision dated 2022 with no stated basis for the year.",
     "ACCEPT", "Year kept as the source's claim; its basis is NOT_FOUND (gap). A non-decision has no decision date.",
     [], "CLOSED", "T3", None),
    ("NCR-N13", "AUDIT_WO-REG-1", "sensitivity_upgrades_v3.md section 1", ["RULE-L", "RULE-S"], [],
     "Rule L and Rule S tables state restrictive/permissive counts; the review restates them as restrictive/n.",
     "ACCEPT", "Both forms are the same counts (7/21 = 7 of 28); stats.py recomputes the four cells and p from coded_decisions_v3.csv.",
     [], "CLOSED", "T3", None),
    ("NCR-N14", "AUDIT_WO-REG-1", "verification ledger", ["G008"], ["G008"],
     "Chlorpyrifos: the tolerance revocation's effective date (October 29, 2021) and the tolerance expiry (February 28, 2022) are distinct dates.",
     "ACCEPT", "Ledger row CORRECTED; REV-C04 dates from the August 30, 2021 rule.",
     [], "CLOSED", "T3", None),
    ("NCR-N18", "AUDIT_WO-REG-1", "coded_decisions_v3.csv", ["B07", "B08", "C08", "C10", "E01"], [],
     "Five rows record no agency decision on the question they are coded for (no reassessment, no action on a classification, a monitoring list without the item, an open review, no standard).",
     "MODIFY", "Retyped NON_DECISION. They stay in every count the source makes, with the type visible, so a reader can drop them.",
     ["CHG-N18-01", "CHG-N18-02", "CHG-N18-03", "CHG-N18-04", "CHG-N18-05"], "CLOSED", "T2", None),
    ("NCR-N19", "AUDIT_WO-REG-1", "sensitivity_upgrades_v3.md section 2", ["A10"], ["G010"],
     "A10 'agency reversed after prescriber/patient outcry; proposal never effectuated': the September 2010 step was a clarification and the February 2012 step a deferral by agreement with the sponsor.",
     "MODIFY", "Outcome direction kept (the drug stayed on the market); REV-A10 dated to February 2012 with mechanism 'agency under pressure' marked contested. Statement superseded (ST-11).",
     [], "CLOSED", "T2", None),
    ("NCR-N20", "AUDIT_WO-REG-1", "coded_decisions_v3.csv B00", ["B00", "B01"], ["G035", "G014"],
     "B00's year 1996 is the first stress-urinary-incontinence sling clearance; the POP mesh chain that B01 reclassified starts 2002.",
     "MODIFY", "B00.year kept (the pelvic mesh predicate chain does start 1996); REV-B00-B01 runs from 2002. '16-20 years later' superseded (ST-10).",
     [], "CLOSED", "T2", None),
    ("NCR-N21", "AUDIT_WO-REG-1", "coded sample frame", ["SAMPLE"], [],
     "The coded sample was drawn from permissive anchors; reversal and forcing tables are counted inside it.",
     "ACCEPT", "Carried as a scope limit on every statistic that reads the coded sample; the R8 rows and Frame C2 are reported apart and never pooled.",
     [], "CLOSED", "T2", None),
    ("NCR-N22", "AUDIT_WO-REG-1", "verification ledger", ["E01"], ["G012"],
     "The Danish compensation count varies 37/38/40 across secondary sources.",
     "ACCEPT", "No count is stated by the registry; the evidence node says compensation exists (secondary) and the count is NOT_FOUND at primary depth.",
     [], "CLOSED", "T3", None),
    ("NCR-N23", "AUDIT_WO-REG-1", "WO Part A (QA semantics)", ["QA_MAPPING"], ["V090", "V091", "V092", "V093", "V094", "V095", "V096", "V097", "V098", "V099", "V100"],
     "The work order asks that the nuclear-QA mapping be verified, not assumed.",
     "MODIFY", "schema/QA_MAPPING.md maps each borrowed term to its source clause with the ledger state of that clause; unverified clauses are carried as UNREACHABLE.",
     [], "OPEN", "T2", "open on primary-depth reading of 10 CFR 50 Appendix B and NQA-1"),
    ("NCR-N24", "AUDIT_WO-REG-1", "registry coding", ["ACT-REGISTRY"], [],
     "Every PROPOSED field in tools/curation_*.py, every audit NCR and both R8 rows rest on one coder.",
     "ACCEPT", "chain.py flags each such node single-failure; a 10-row second coding (ACT-CODER2) is reported with kappa per field.",
     [], "OPEN", "T1", "open until a second party checks the audit NCRs"),
]

# ---------------------------------------------------------------- CHANGES
#
# (id, kind, object, field, from, to, reason, ncr, wo)

OLD_BUNDLE = "dcaa6d8bb90eb09e541de498a1baad329de3bb272470527298a484ccf58e5aca"
NEW_BUNDLE = "f6265e9e2a513f5166740ab60f260392e307221c1cefcde4f2d2445a29d7a0ed"
CLOSURES = ["Nabam", "Denatonium saccharide", "Cryolite", "Furfural",
            "Mefluidide", "Sabadilla alkaloids"]

CHANGES = [
    ("CHG-INPUT-01", "pin", "bundle", "sha256", OLD_BUNDLE, NEW_BUNDLE,
     "the consolidated WO-REG-1 bundle (WO-REG-1 + 1a + 1b) supersedes the earlier inputs; earlier commits and source/PINS.json kept; superseded v1/v2 files loaded as configuration history only, never graded from",
     None, "WO-REG-1"),
    ("CHG-INPUT-02", "pin", "bundle/MANIFEST.sha256", "entries", 0, 23,
     "the bundle's own manifest is re-checked on every run beside source/PINS.json and registry/MANIFEST.json",
     None, "WO-REG-1"),
    ("CHG-INPUT-03", "recode", "E01", "id", "C11", "E01",
     "the night-shift case the earlier registry added as C11 (NCR-R5) arrives in the bundle as E01; one object, the bundle's id",
     "NCR-R5", "WO-REG-1"),
    ("CHG-WO-1a", "add_vocab", "schema", "object_types", None, "ACTOR, AUTHORITY, CONFLICT; edges decided_by, recommended_by, overruled, delegated_from, funded_by",
     "addendum 1a: authority and actors", None, "WO-REG-1a"),
    ("CHG-SCHEMA-01", "drop_vocab", "schema", "object_types", "FINDING", None,
     "findings are computed by tools/stats.py from the registry; a stored FINDING could drift from the objects it summarizes", None, "WO-REG-1"),
    ("CHG-WO-1b", "add_vocab", "schema", "object_types", None, "REVERSAL; edge reverses; actor types trade_group, public_interest_litigant, injured_class",
     "addendum 1b: reversals", None, "WO-REG-1b"),
    ("CHG-N18-01", "retype", "B07", "type", "DECISION", "NON_DECISION", "no FDA reassessment of E171 located (EA-08)", "NCR-N18", "WO-REG-1"),
    ("CHG-N18-02", "retype", "B08", "type", "DECISION", "NON_DECISION", "FDA did not act on the IARC 2B classification; the ADI stands", "NCR-N18", "WO-REG-1"),
    ("CHG-N18-03", "retype", "C08", "type", "DECISION", "NON_DECISION", "microplastics left off the UCMR 6 proposal: a monitoring decision not taken", "NCR-N18", "WO-REG-1"),
    ("CHG-N18-04", "retype", "C10", "type", "DECISION", "NON_DECISION", "registration review open since 2009; the 2026 event is a court holding, not an agency decision", "NCR-N18", "WO-REG-1"),
    ("CHG-N18-05", "retype", "E01", "type", "DECISION", "NON_DECISION", "no OSHA standard; no decision on the question", "NCR-N18", "WO-REG-1"),
    ("CHG-R6-01", "recode", "C2:Pentachlorophenol", "direction", "go_ahead", "decline",
     "EPA required cancellation of all uses with a five-year phase-out (G001, G002)", "NCR-R6", "WO-REG-1"),
] + [
    ("CHG-R6-%02d" % (i + 2), "recode", "C2:" + name, "direction", "go_ahead", "NA",
     "case closure (registrations already canceled): not a decision on the merits", "NCR-R6", "WO-REG-1")
    for i, name in enumerate(CLOSURES)
] + [
    ("CHG-R8-01", "add_object", "D03", "-", None, "DECISION", "restrictive-side candidate (2016 denial; Schedule I maintained)", "NCR-R8", "WO-REG-1"),
    ("CHG-R8-02", "add_object", "D04", "-", None, "NON_DECISION", "restrictive-side candidate (psilocybin held in Schedule I)", "NCR-R8", "WO-REG-1"),
    ("CHG-R9-01", "add_field", "*", "C_restrict.substitution", None, "(claimed, named, grade) per row",
     "substitution field: the alternative credited in C_restrict, its name and its own grade", "NCR-R9", "WO-REG-1"),
    ("CHG-R14-01", "add_object", "REVERSAL", "-", None, "REV-D02, REV-A10, REV-C04, REV-C03, REV-B00-B01, REV-B00b-B02, REV-A04, REV-A08, REV-D01-2016, REV-D01-1970",
     "reversals link decisions; never encoded inside a row", "NCR-R14", "WO-REG-1b"),
    ("CHG-R14-02", "add_field", "A10", "forcing", None, "unmet_postmarket_requirement",
     "A10's basis (post-market studies never completed under Subpart H) is a forcing event of the Makena type", "NCR-R14", "WO-REG-1b"),
    ("CHG-R14-03", "add_object", "PRIOR", "-", None, "A04P, A08P, SCH1-1970",
     "out-of-sample anchors at the permissive or original end of three reversals", "NCR-R14", "WO-REG-1b"),
    ("CHG-N01-01", "add_field", "*", "C_restrict.axes", None, "(Pr, Ir, Dr) per row, registry coding",
     "second coding of C_restrict beside the source sums", "NCR-N01", "WO-REG-1"),
    ("CHG-N03-01", "recode", "B06", "statute_compelled", "1", "0",
     "no federal statute or court compelled the revocation; AB 418 recorded as a contested candidate", "NCR-N03", "WO-REG-1"),
    ("CHG-N04-01", "recode", "D02", "forced_action", False, True,
     "the agency's 1977 proposal was compelled by the Delaney clause; the annex grades D02 without R3", "NCR-N04", "WO-REG-1"),
    ("CHG-N04-02", "recode", "D02", "forced_outcome", False, True,
     "the coded direction (warn) is the outcome compelled by Pub. L. 95-203; the annex grades D02 without R3", "NCR-N04", "WO-REG-1"),
    ("CHG-N11-01", "add_field", "E01", "cost_bearer_detail", None, "employer",
     "annex rationale names employers; source cost_bearer 'sponsor' kept", "NCR-N11", "WO-REG-1"),
]


def main():
    import sys
    sys.stderr.write("curation_ncr.py is data; checks run in "
                     "tools/validate.py --selftest\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
