# SPDX-License-Identifier: CC0-1.0
"""
curation_cases.py -- per-case curation, comparators, outcomes, conflicts,
unlocated inputs, endpoint absences, reversals and the R8 candidate rows.

PROPOSED unless a field says otherwise: one coder's reading (ACT-REGISTRY).
The source coding (bundle/source/current/coded_decisions_v3.csv and
annex_a_regrading_v2.csv) is never restated here; tools/build.py reads it
from the pinned files and this module adds only what the source does not
carry: actors, authority chains, per-axis C_restrict (a second coding beside
the source sums), forcing, the substitution field, R6 fields, reversal links.

Old C11 (night shift, added by NCR-R5 before the consolidated bundle) is the
bundle's E01; the swap is CHANGE CHG-INPUT-01.
"""

# ---------------------------------------------------------------- cases

# Per-case curation. Fields:
#   type      DECISION | NON_DECISION (a retype is a CHANGE under NCR-N18)
#   sub, end  SUBSTANCE / ENDPOINT local keys
#   rows      ledger rows supporting the case facts
#   r1        (R1a|R1b|none, basis)
#   Cr        (Pr, Ir, Dr, rationale)
#   forcing   (kind, direction pushed, rows) or None
#   decided, recommended, overruled, sponsor   actor ids
#   outcomes  outcome ids
CASES = {
 "A01": dict(type="DECISION", sub=["aducanumab"], end=["alzheimer_cognition", "amyloid_pet", "aria"], rows=["V015", "V016", "F001"],
    r1=("none", "U3; surrogate not validated for the clinical question"),
    Cr=(3, 3, 1, "millions with Alzheimer disease; progressive, no disease-modifying alternative in 2021; an approval withheld can be granted later"),
    forcing=None, decided=["ACT-FDA-CDER", "ACT-P-CAVAZZONI", "ACT-P-WOODCOCK"], recommended=[], overruled=["ACT-AC-PCNS"], sponsor="ACT-SP-BIOGEN", outcomes=[]),
 "A02": dict(type="DECISION", sub=["eteplirsen"], end=["dystrophin"], rows=["F004", "F005", "V073"],
    r1=("none", "U3; dystrophin surrogate not validated"),
    Cr=(1, 3, 2, "about 1e4 patients with exon-51-amenable DMD; progressive and fatal, no alternative in 2016; small sponsor whose viability the record discusses"),
    forcing=None, decided=["ACT-P-WOODCOCK", "ACT-P-CALIFF"], recommended=[], overruled=["ACT-AC-PCNS", "ACT-FDA-REVIEWTEAM-A02"], sponsor="ACT-SP-SAREPTA", outcomes=[]),
 "A03": dict(type="DECISION", sub=["hydrocodone_bitartrate"], end=["opioid_use_disorder"], rows=["V005", "V075", "F006"],
    r1=("none", "U3; abuse liability contested"),
    Cr=(2, 1, 1, "chronic-pain patients on extended-release opioids; other ER opioids available; approval can follow later"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=[], overruled=["ACT-AC-AADPAC"], sponsor="ACT-SP-ZOGENIX", outcomes=[]),
 "A04": dict(type="DECISION", sub=["hydroxyprogesterone_caproate"], end=["preterm_birth"], rows=["V017", "V018", "F007"],
    r1=("R1a", "confirmatory trial failed to show benefit (V017): absence of benefit at U1"),
    Cr=(2, 3, 2, "pregnancies at risk of preterm birth; if the drug worked, preterm birth is irreversible and no approved alternative existed; withdrawal ends generic supply"),
    forcing=("failed_confirmatory_trial", "restrictive", ["V017"]), decided=["ACT-P-CALIFF", "ACT-P-BUMPUS"], recommended=["ACT-AC-BRUDAC", "ACT-AC-MAKENA-HEARING"], overruled=[], sponsor="ACT-SP-COVIS", outcomes=[]),
 "A05": dict(type="DECISION", sub=["rofecoxib"], end=["myocardial_infarction", "stroke"], rows=["V019", "V020", "F008"],
    r1=("none", "U2; cardiovascular harm established with a claimed analgesic/GI benefit, so not 'harm with no benefit claimed'"),
    Cr=(3, 1, 1, "millions with arthritis; other NSAIDs and celecoxib available; readily reversed"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=["ACT-AC-AAC-DSARM"], overruled=[], sponsor="ACT-SP-MERCK", outcomes=["OUT-A05-NORELAUNCH"]),
 "A06": dict(type="DECISION", sub=["molnupiravir"], end=["embryo_fetal_toxicity", "mutagenicity", "covid_outcomes"], rows=["V021", "V022", "E008", "E009", "F010"],
    r1=("none", "U3; rodent signals with unresolved human relevance"),
    Cr=(3, 2, 1, "pandemic-scale outpatient population; other antivirals authorized around the same time; an authorization denied can be revisited"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=["ACT-AC-AMDAC"], overruled=[], sponsor="ACT-SP-MERCK", outcomes=[], r5=True),
 "A07": dict(type="DECISION", sub=["flibanserin"], end=["hsdd_efficacy", "orthostatic_hypotension"], rows=["V023", "V024", "V076", "F011", "F012"],
    r1=("none", "U2; modest benefit and hypotension/syncope risk both claimed"),
    Cr=(2, 1, 1, "premenopausal women with HSDD; harm of a withheld drug is reversible and non-fatal; readily reversed"),
    forcing=None, decided=["ACT-FDA-CDER", "ACT-P-WOODCOCK"], recommended=["ACT-AC-BRUDAC"], overruled=[], sponsor="ACT-SP-SPROUT", outcomes=[]),
 "A08": dict(type="DECISION", sub=["bevacizumab"], end=["overall_survival"], rows=["V025", "V026", "F013"],
    r1=("R1a", "confirmatory trials showed no overall-survival benefit (V025): absence of benefit at U1"),
    Cr=(2, 2, 1, "metastatic breast cancer patients; chemotherapy alternatives; other indications remain, so readily reversed"),
    forcing=("failed_confirmatory_trial", "restrictive", ["V025"]), decided=["ACT-P-HAMBURG"], recommended=["ACT-AC-ODAC"], overruled=[], sponsor="ACT-SP-GENENTECH", outcomes=[]),
 "A09": dict(type="DECISION", sub=["donanemab"], end=["alzheimer_cognition", "aria"], rows=["V027", "V028", "F014"],
    r1=("none", "U2; modest benefit and ARIA risk both claimed"),
    Cr=(3, 3, 1, "millions with early Alzheimer disease; progressive; readily reversed"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=["ACT-AC-PCNS"], overruled=[], sponsor="ACT-SP-LILLY", outcomes=[]),
 "A10": dict(type="DECISION", sub=["midodrine"], end=["orthostatic_hypotension"], rows=["V074", "E011", "F015"],
    r1=("none", "U3; surrogate (standing blood pressure) never confirmed"),
    Cr=(2, 2, 2, "dependent patients with symptomatic orthostatic hypotension; few alternatives in 2010; generic makers exit on withdrawal"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=[], overruled=[], sponsor="ACT-SP-SHIRE", outcomes=[]),
 "B00": dict(type="DECISION", sub=["polypropylene"], end=["mesh_erosion"], rows=["V029", "E015"],
    r1=("none", "U4 by M1"),
    Cr=(2, 1, 1, "women undergoing prolapse repair; native-tissue repair available; clearance can follow later"),
    forcing=None, decided=["ACT-FDA-CDRH"], recommended=[], overruled=[], sponsor="ACT-SP-MESH", outcomes=[]),
 "B00b": dict(type="DECISION", sub=["cobalt", "chromium"], end=["metallosis"], rows=["V030", "E015"],
    r1=("none", "U4 by M1"),
    Cr=(2, 1, 1, "hip replacement patients; metal-on-polyethylene and ceramic bearings available; clearance can follow later"),
    forcing=None, decided=["ACT-FDA-CDRH"], recommended=[], overruled=[], sponsor="ACT-SP-MOM", outcomes=[]),
 "B01": dict(type="DECISION", sub=["polypropylene"], end=["mesh_erosion"], rows=["V029", "V031", "E016", "E017", "F016"],
    r1=("none", "U3 as graded by the source"),
    Cr=(2, 1, 2, "prolapse patients; native-tissue repair available; makers exited rather than file PMAs"),
    forcing=("litigation_post_market_harm", "restrictive", ["V029", "V031"]), decided=["ACT-FDA-CDRH"], recommended=["ACT-AC-OBGYN"], overruled=[], sponsor="ACT-SP-MESH", outcomes=["OUT-B01-STOPSALE"]),
 "B02": dict(type="DECISION", sub=["cobalt", "chromium"], end=["metallosis"], rows=["V030", "E018", "F017"],
    r1=("none", "U3 as graded by the source"),
    Cr=(2, 1, 2, "hip patients; other bearings available; products already withdrawn commercially"),
    forcing=("litigation_post_market_harm", "restrictive", ["V030"]), decided=["ACT-FDA-CDRH"], recommended=["ACT-AC-ORTHO"], overruled=[], sponsor="ACT-SP-MOM", outcomes=[]),
 "B03": dict(type="DECISION", sub=["pyridostigmine_bromide"], end=["nerve_agent_survival"], rows=["V032", "V033", "E012", "E013"],
    r1=("none", "U3; efficacy from animals only"),
    Cr=(3, 3, 2, "national population protected by stockpiled countermeasures; without the pathway no countermeasure can be approved (human trials unethical); countermeasure development base would not form"),
    forcing=None, decided=["ACT-FDA"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "B04": dict(type="DECISION", sub=["liraglutide", "semaglutide"], end=["thyroid_c_cell_tumor"], rows=["V034", "V035", "V036", "E014", "F018"],
    r1=("none", "U3; rodent C-cell tumors, human relevance not determined"),
    Cr=(3, 2, 1, "tens of millions on the class; other glucose-lowering and weight drugs, less effective; a label change is readily reversed"),
    forcing=None, decided=["ACT-FDA-CDER"], recommended=[], overruled=[], sponsor="ACT-SP-NOVO", outcomes=[]),
 "B05": dict(type="DECISION", sub=["erythrosine"], end=["thyroid_follicular_tumor_rodent"], rows=["V037", "V038", "E019", "F019"],
    r1=("none", "U3 after M2 (animal-only, extrapolation unresolved); R1 requires U1-U2"),
    Cr=(1, 1, 2, "manufacturers reformulate; substitute colors exist; reformulation cost is sunk"),
    forcing=("statute", "restrictive", ["V037", "E019"]), decided=["ACT-FDA-FOOD"], recommended=["ACT-CSPI"], overruled=[], sponsor=None, outcomes=["OUT-B05-DEADLINES"]),
 "B06": dict(type="DECISION", sub=["bvo"], end=["thyroid_function"], rows=["V039", "V040", "E021", "F020"],
    r1=("none", "U3 (M2); R1 requires U1-U2 (NCR-N05)"),
    Cr=(1, 1, 1, "few remaining users; most majors had reformulated; readily reversed"),
    forcing=("agency_own_study", "restrictive", ["V039"]), decided=["ACT-FDA-FOOD"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "B07": dict(type="NON_DECISION", sub=["titanium_dioxide"], end=["genotoxicity"], rows=["V041", "V042", "E022"],
    r1=("none", "U3"),
    Cr=(1, 1, 2, "manufacturers reformulate; imperfect substitutes; reformulation sunk"),
    forcing=None, decided=["ACT-FDA-FOOD"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "B08": dict(type="NON_DECISION", sub=["aspartame"], end=["hepatocellular_carcinoma"], rows=["V043", "V044", "V110", "E023"],
    r1=("none", "U3"),
    Cr=(3, 1, 1, "millions relying on low-calorie sweeteners incl. people with diabetes; other sweeteners exist; readily reversed"),
    forcing=None, decided=["ACT-FDA-FOOD"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "C01": dict(type="DECISION", sub=["atrazine"], end=["amphibian_endocrine"], rows=["V045", "V046", "E026", "F021", "F022"],
    r1=("none", "U3; ecological question, M2 not applied"),
    Cr=(2, 2, 1, "corn and sorghum growers; alternatives costlier; readily reversed"),
    forcing=None, decided=["ACT-EPA-OPP"], recommended=[], overruled=[], sponsor="ACT-SP-SYNGENTA", outcomes=[]),
 "C02": dict(type="DECISION", sub=["atrazine"], end=["amphibian_endocrine", "aquatic_toxicity"], rows=["V045", "V047", "E025"],
    r1=("none", "U3; ecological question"),
    Cr=(2, 2, 1, "as C01"),
    forcing=None, decided=["ACT-EPA-OPP"], recommended=[], overruled=[], sponsor="ACT-SP-SYNGENTA", outcomes=[]),
 "C03": dict(type="DECISION", sub=["glyphosate"], end=["nhl"], rows=["V048", "V049", "E025", "E031", "F023"],
    r1=("none", "U3"),
    Cr=(3, 2, 1, "agriculture broadly; alternatives more toxic or need tillage; readily reversed"),
    forcing=None, decided=["ACT-EPA-OPP"], recommended=[], overruled=[], sponsor="ACT-SP-BAYER", outcomes=["OUT-C03-VACATUR"]),
 "C04": dict(type="DECISION", sub=["chlorpyrifos"], end=["neurodevelopment"], rows=["V052", "V053", "E027", "E028", "E029", "E030", "F024"],
    r1=("none", "U3 as graded by the source"),
    Cr=(2, 2, 1, "growers; alternatives for some pests limited; reversed in fact (2023 vacatur)"),
    forcing=("court_order", "restrictive", ["V053", "E029"]), decided=["ACT-P-REGAN", "ACT-EPA"], recommended=[], overruled=[], sponsor="ACT-SP-CORTEVA", outcomes=["OUT-C04-VACATUR"]),
 "C05": dict(type="DECISION", sub=["imidacloprid", "clothianidin", "thiamethoxam", "dinotefuran", "acetamiprid"], end=["pollinator_colony"], rows=["V055", "E025", "F025"],
    r1=("none", "U2; ecological question"),
    Cr=(2, 2, 1, "growers; alternatives exist but costlier; readily reversed"),
    forcing=None, decided=["ACT-EPA-OPP"], recommended=[], overruled=[], sponsor="ACT-SP-BAYER", outcomes=[]),
 "C06": dict(type="DECISION", sub=["lead"], end=["neurodevelopment", "blood_lead"], rows=["V057", "V058", "E033", "F026"],
    r1=("R1a", "harm established at U1 (MCLG zero) and no party claims a benefit of lead in drinking water; NCR-N06"),
    Cr=(3, 1, 2, "ratepayers nationally; financial cost, reversible; capital sunk"),
    forcing=("new_data_scheduled_rule", "restrictive", ["V057"]), decided=["ACT-P-REGAN"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "C07": dict(type="DECISION", sub=["pfoa", "pfos", "pfhxs", "pfna", "hfpo_da", "pfbs"], end=["kidney_cancer", "immune_response"], rows=["V059", "V060", "E034", "F027"],
    r1=("R1a", "harm indicated at U2 and no party claims a benefit of PFAS in drinking water; NCR-N06"),
    Cr=(3, 1, 2, "ratepayers nationally; financial cost; treatment capital sunk"),
    forcing=("new_data_scheduled_rule", "restrictive", ["V059"]), decided=["ACT-P-REGAN"], recommended=[], overruled=[], sponsor=None, outcomes=["OUT-C07-RESCIND"]),
 "C08": dict(type="NON_DECISION", sub=["microplastics"], end=["microplastic_occurrence"], rows=["V011", "V012", "V061", "V062", "V067", "E035", "F028"],
    r1=("none", "U4 by M1"),
    Cr=(2, 1, 1, "sampled utilities and their ratepayers bear monitoring cost; financial, reversible"),
    forcing=None, decided=["ACT-P-ZELDIN", "ACT-EPA-OW"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "C09": dict(type="DECISION", sub=["saccharin"], end=["bladder_tumor_rodent"], rows=["V063", "E036"],
    r1=("none", "U3 (M2)"),
    Cr=(1, 1, 1, "waste handlers keep a listing; reversible"),
    forcing=None, decided=["ACT-EPA-ORCR"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "C10": dict(type="NON_DECISION", sub=["glyphosate"], end=["nhl"], rows=["V009", "V010", "V050", "V051", "V064", "E032", "F031"],
    r1=("none", "U3"),
    Cr=(3, 2, 1, "as C03"),
    forcing=None, decided=["ACT-EPA-OPP", "ACT-SCOTUS"], recommended=[], overruled=[], sponsor="ACT-SP-BAYER", outcomes=["OUT-C10-DURNELL"]),
 "E01": dict(type="NON_DECISION", sub=["night_shift_work"], end=["breast_cancer", "prostate_cancer", "colorectal_cancer", "circadian_disruption"],
    rows=["V080", "V081", "V082", "V083", "V084", "V085", "V086", "V087", "E038", "F034"],
    r1=("none", "U3: limited human evidence, sufficient animal evidence, strong mechanistic evidence (V081)"),
    Cr=(3, 3, 2, "millions of night workers; 24-hour essential services (care, power, transport) cannot stop; a ban loses livelihoods and services"),
    forcing=None, decided=["ACT-OSHA"], recommended=[], overruled=[], sponsor=None, outcomes=[]),
 "D01": dict(type="DECISION", sub=["cannabis", "thc"], end=["pain_mmj"], rows=["V013", "V014", "V065", "V066", "V077", "E037", "F030"],
    r1=("none", "U3"),
    Cr=(3, 2, 2, "millions of medical users; partial alternatives; research capacity forgone under Schedule I"),
    forcing=None, decided=["ACT-DOJ", "ACT-DEA", "ACT-PRESIDENT"], recommended=[], overruled=[], sponsor=None, outcomes=["OUT-D01-STAY"]),
 "D02": dict(type="DECISION", sub=["saccharin"], end=["bladder_tumor_rodent"], rows=["V063", "E020", "E024", "F029"],
    r1=("none", "U3 (M2)"),
    Cr=(3, 2, 2, "millions incl. people with diabetes; saccharin was the only non-caloric sweetener after the 1970 cyclamate ban; reformulation sunk"),
    forcing=("statute", "restrictive", ["V063", "E020"]), decided=["ACT-P-KENNEDY", "ACT-CONGRESS"], recommended=[], overruled=[], sponsor=None, outcomes=["OUT-D02-MORATORIUM"],
    stages=[("stage1", "hold", "FDA proposed ban, March 1977, Delaney clause", ("statute", "restrictive")),
            ("final", "warn", "Saccharin Study and Labeling Act, November 1977: moratorium plus warning label", ("statute", "permissive"))]),
}

# ---------------------------------------------------------------- comparators

COMPARATORS = [
    # id, title, year, agency, us_case, pair, us_score, comp_score, rows
    ("M01", "IARC: glyphosate Group 2A", 2015, "IARC", "C03", "glyphosate - carcinogenicity", 3, 2, ["V048"]),
    ("M02", "EU: atrazine non-inclusion", 2004, "EU", "C01", "atrazine - amphibian endocrine/eco", 3, 0, ["V115", "V046"]),
    ("M03", "EU: outdoor ban on three neonicotinoids", 2018, "EU", "C05", "neonicotinoids - pollinator", 3, 0, ["V056"]),
    ("M04", "EU: chlorpyrifos non-renewal", 2020, "EU", "C04", "chlorpyrifos - neurodevelopmental (US side = pre-2021 retention, not C04)", 3, 0, ["V054"]),
    ("M05", "EFSA/EU: E171 cannot exclude genotoxicity; ban", 2022, "EU", "B07", "titanium dioxide - genotoxicity", 3, 0, ["V041", "E022"]),
    ("M06", "IARC: aspartame Group 2B; JECFA ADI unchanged", 2023, "IARC", "B08", "aspartame - carcinogenicity", 3, 2, ["V110"]),
    ("M07", "EU: drinking-water watch list mechanism", 2020, "EU", "C08", "microplastics - drinking water", 3, 1, ["V113"]),
    ("M08", "EU: erythrosine permitted narrowly (cherries)", 2008, "EU", "B05", "Red No. 3 - rodent thyroid tumors", 0, 2, ["V111"]),
    ("M09", "EU: PFAS group parameters in drinking water", 2020, "EU", "C07", "PFAS - drinking water", 0, 2, ["V112"]),
    ("M10", "EU: saccharin permitted with ADI", 2008, "EU", "C09", "saccharin - rodent bladder tumors", 3, 2, ["V114"]),
    ("M11", "IARC: night shift work Group 2A", 2019, "IARC", "E01", "night shift - cancer (not in the source's mirror table)", None, None, ["V080", "V081"]),
    ("M12", "Denmark: compensation for breast cancer after night work", 2008, "DK", "E01", "night shift - compensation", None, None, ["V083", "F035"]),
    ("M13", "Germany: not recognized as occupational disease", 2010, "DE", "E01", "night shift - recognition", None, None, ["V084"]),
    ("M14", "EMA PRAC: no causal GLP-1/thyroid cancer link", 2023, "EU", "B04", "GLP-1 - thyroid (not in the source's mirror table)", None, None, ["V036"]),
]
SOURCE_MIRROR_PAIRS = 10  # report section 6 table rows

# ---------------------------------------------------------------- outcomes

OUTCOMES = [
    ("OUT-A05-NORELAUNCH", "Merck did not relaunch rofecoxib after the 2005 panel vote", "2005", "market_exit", "decline", ["V020"], "A05"),
    ("OUT-B01-STOPSALE", "FDA ordered remaining makers to stop selling transvaginal POP mesh", "2019-04", "agency_followup", "decline", ["V029", "F016"], "B01"),
    ("OUT-B05-DEADLINES", "Red No. 3 removal deadlines: foods January 2027, ingested drugs January 2028", "2027", "scheduled", "decline", ["V037"], "B05"),
    ("OUT-C03-VACATUR", "Ninth Circuit vacated the human-health portion of the 2020 glyphosate interim decision", "2022-06-17", "court", "hold", ["V049", "E031"], "C03"),
    ("OUT-C04-VACATUR", "Eighth Circuit vacated the chlorpyrifos tolerance revocation; tolerances reinstated", "2023-11-02", "court", "warn", ["V052", "E030"], "C04"),
    ("OUT-C07-RESCIND", "EPA proposed rescinding four of six PFAS limits, keeping PFOA/PFOS", "2025", "proposal", "warn", ["V060", "F027"], "C07"),
    ("OUT-C10-DURNELL", "Supreme Court: FIFRA preempts state failure-to-warn claims on the EPA-approved label (7-2)", "2026-06-25", "court", "go_ahead", ["V009", "V010"], "C10"),
    ("OUT-D01-STAY", "expedited hearing on broader marijuana rescheduling stayed", "2026-10", "stay", "hold", ["V014"], "D01"),
    ("OUT-D02-MORATORIUM", "Congress imposed a moratorium on the saccharin ban with a warning label", "1977-11", "legislature", "warn", ["V063", "E024"], "D02"),
]

# ---------------------------------------------------------------- conflicts

CONFLICTS = [
    # id, actor, type, decision, rows, statement, recusal
    ("CF-A01-COLLAB", "ACT-P-DUNN", "reputational_institutional", "A01", ["F002"], "congressional committees reported an atypical FDA-sponsor collaboration before the aducanumab approval", None),
    ("CF-A01-RESIGN", "ACT-AC-PCNS", "reputational_institutional", "A01", ["F003"], "three committee members resigned after the approval set their advice aside", None),
    ("CF-A01-WAIVER", "ACT-AC-PCNS", "disclosure_record", "A01", ["F032"], "18 U.S.C. 208 waiver record for the November 6, 2020 meeting", None),
    ("CF-A02-SPONSORFIN", "ACT-P-WOODCOCK", "reputational_institutional", "A02", ["F005"], "the approval dispute record refers to the sponsor's financial condition", None),
    ("CF-A05-PANELTIES", "ACT-AC-AAC-DSARM", "financial", "A05", ["F009"], "panelists with industry ties; vote outcome depended on them", None),
    ("CF-A07-ADVOCACY", "ACT-ETS", "funding_source", "A07", ["F012"], "advocacy for approval funded in part by the sponsor", None),
    ("CF-C01-DQA", "ACT-CRE", "funding_source", "C01", ["F021"], "information-quality petition against the frog studies", None),
    ("CF-C01-FUNDING", "ACT-SP-SYNGENTA", "funding_source", "C01", ["F022"], "registrant-funded studies in the record", None),
    ("CF-C03-ROWLAND", "ACT-P-ROWLAND", "reputational_institutional", "C03", ["F023"], "EPA review chair's communications with the registrant disclosed in litigation", None),
]
# Every case without a located disclosure record gets a disclosure_record
# CONFLICT whose state comes from ledger rows G### (per-case search) when
# present, else UNREACHABLE (not searched; egress). Built in build.py.

# ---------------------------------------------------------------- unlocated inputs (WO-REG-1a D)

UNLOCATED = [
    ("EV-U01", "A01", "sponsor_unpub", "Biogen trial data and analyses submitted to FDA (EMERGE/ENGAGE post-hoc analyses) relied on for the approval", "sponsor-submitted; full analyses not public"),
    ("EV-U02", "A02", "sponsor_unpub", "Sarepta dystrophin measurements submitted to FDA", "sponsor-submitted; underlying data not public"),
    ("EV-U03", "C03", "sponsor_unpub", "registrant-submitted glyphosate studies relied on by EPA", "confidential business information under FIFRA"),
    ("EV-U04", "C02", "sponsor_unpub", "Syngenta model used to reduce the atrazine protection factor (coded_decisions.csv C02 note)", "registrant model; not located in a public docket from here"),
    ("EV-U05", "B00", "absence", "clinical data for the 1996 mesh clearance", "none required under 510(k) substantial equivalence"),
    ("EV-U06", "B00b", "absence", "clinical data for the metal-on-metal hip clearances", "none required under 510(k) substantial equivalence"),
]

# ---------------------------------------------------------------- absences

ABSENCES = [
    ("EA-01", "glyphosate", "gut_microbiome", "NOT_ASSESSED", ["C03", "C10"], "EPA glyphosate human-health risk assessment and interim decision (2017-2020)", ["glyphosate", "microbiome", "EPA"], ["H001"], "work-order example (consolidated WO Part A); state from ledger row H001"),
    ("EA-02", "microplastics", "microplastic_occurrence", "NOT_ASSESSED", ["C08"], "UCMR 6 proposal (July 2026)", ["UCMR 6", "microplastics"], ["V011", "V061"], "national occurrence data will not be generated"),
    ("EA-03", "polypropylene", "mesh_erosion", "NOT_REQUIRED", ["B00"], "510(k) clearance file", ["510(k)", "clinical data"], ["V029", "E015"], "substantial equivalence requires no clinical data"),
    ("EA-04", "cobalt", "metallosis", "NOT_REQUIRED", ["B00b"], "510(k) clearance files", ["510(k)", "clinical data"], ["V030", "E015"], "substantial equivalence requires no clinical data"),
    ("EA-05", "night_shift_work", "breast_cancer", "NOT_RESOLVED", ["E01"], "Travis et al. 2016 pooled cohorts; IARC Vol 124", ["night shift", "rotation", "forward", "backward", "permanent night"], ["V082", "V086", "V087"], "exposure coded ever/never or duration; rotation pattern not resolved for cancer endpoints"),
    ("EA-06", "aducanumab", "alzheimer_cognition", "NOT_RESOLVED", ["A01"], "approval record, June 2021", ["clinical benefit", "confirmatory"], ["V015", "V016"], "clinical benefit unconfirmed at approval; surrogate basis"),
    ("EA-07", "eteplirsen", "dystrophin", "NOT_RESOLVED", ["A02"], "approval record, September 2016", ["clinical benefit", "confirmatory"], ["F004"], "clinical benefit unconfirmed at approval; surrogate basis"),
    ("EA-08", "titanium_dioxide", "genotoxicity", "NOT_LOCATED", ["B07"], "FDA reassessment of E171 after EFSA 2021", ["FDA", "titanium dioxide", "genotoxicity"], ["V041"], "an FDA reassessment was not located; the absence is the source's statement"),
]

# ---------------------------------------------------------------- consolidated-bundle overlay
#
# Per-case fields the source does not carry, keyed by case id.
#   frame      A-E coded sample frames as the source names them; R8 for the
#              restrictive-side candidates this registry adds (NCR-R8);
#              C2 for the 2022 EPA frame; PRIOR for out-of-sample anchors
#              that a REVERSAL needs at its other end
#   alt        (claimed, named, grade): does the source's C_restrict
#              rationale credit "alternatives exist"; the alternative it
#              names (None = unnamed); the alternative's own C_permit grade
#              (None = not graded anywhere in the bundle). Rule SUB (NCR-R9)
#              reads these three and nothing else.
#   forced     (action_forced, outcome_forced): was the agency's action /
#              the legal outcome compelled by statute or court (RUS-0.2 R3)
#   r6         (blocking, cycles_held, justification): blocking = the
#              restriction or the declined monitoring prevents the evidence
#              that would resolve it; cycles_held = annual cycles held at
#              the decision date (None = not evaluable); justification =
#              "none" | "self_sealed_only" | "independent"
#   r6b        a loosening of a self-sealing restriction (RUS-0.3 R6b)
#   r1_scope   RUS-0.3 reading of R1: "market_status" (R1 applies: the
#              decision sets whether a product is on the market) or
#              "level_setting" (contaminant standard; D5 has no referent)

EXTRA = {
    "A01": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A02": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A03": dict(frame="A", alt=(True, "other opioids", None), forced=(False, False), r1_scope="market_status"),
    "A04": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A05": dict(frame="A", alt=(True, "other NSAIDs", None), forced=(False, False), r1_scope="market_status"),
    "A06": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A07": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A08": dict(frame="A", alt=(True, "other agents", None), forced=(False, False), r1_scope="market_status"),
    "A09": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "A10": dict(frame="A", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "B00": dict(frame="B", alt=(True, "native-tissue repair", None), forced=(False, False), r1_scope="market_status"),
    "B00b": dict(frame="B", alt=(True, "other bearing couples", None), forced=(False, False), r1_scope="market_status"),
    "B01": dict(frame="B", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "B02": dict(frame="B", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "B03": dict(frame="B", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "B04": dict(frame="B", alt=(False, None, None), forced=(False, False), r1_scope="market_status"),
    "B05": dict(frame="B", alt=(True, None, None), forced=(True, True), r1_scope="market_status"),
    "B06": dict(frame="B", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "B07": dict(frame="B", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "B08": dict(frame="B", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C01": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C02": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C03": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C04": dict(frame="C", alt=(True, None, None), forced=(True, True), r1_scope="market_status"),
    "C05": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C06": dict(frame="C", alt=(False, None, None), forced=(False, False), r1_scope="level_setting"),
    "C07": dict(frame="C", alt=(False, None, None), forced=(False, False), r1_scope="level_setting",
                substitution_note="R9 reference case: PFOA replaced in manufacture by HFPO-DA (GenX), itself regulated in this rule (G023)"),
    "C08": dict(frame="C", alt=(False, None, None), forced=(False, False), r1_scope="level_setting",
                r6=(True, None, "none")),
    "C09": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "C10": dict(frame="C", alt=(True, None, None), forced=(False, False), r1_scope="market_status"),
    "D01": dict(frame="D", alt=(False, None, None), forced=(False, False), r1_scope="market_status", r6b=True),
    "D02": dict(frame="D", alt=(False, None, None), forced=(True, True), r1_scope="market_status"),
    "E01": dict(frame="E", alt=(False, None, None), forced=(False, False), r1_scope="level_setting",
                r6=(True, None, "none")),
}

# Restrictive-side candidates (NCR-R8) and anchors. These rows are not in
# the source; every field is PROPOSED by ACT-REGISTRY, single coder, and the
# rows are SELECTED ON DIRECTION -- they make R2's over-restrictive branch
# testable and are never pooled into a bivariate test of the sample.
NEW_CASES = {
 "D03": dict(type="DECISION", frame="R8", year=2016, agency="DEA/DOJ",
    decision="DEA denies petitions to reschedule marijuana (Schedule I maintained)",
    evidence_class="human_epi+human_rct", uncertainty="high",
    action="decline", outcome="decline", cost_bearer_L="public", cost_bearer_S="public",
    note="Krumm petition and Washington/Rhode Island governors' petition; denial letter July 19 2016, 81 FR 53767 (G036); HHS evaluation binding on scientific matters (CSA 201(b))",
    Cp=(3, 2, 2, "harm if wrongly rescheduled to II: millions with access to prescription cannabis products; dependence partly reversible; a schedule can be revised"),
    Cr_axes=(3, 2, 3, "harm if wrongly kept in I: patients and researchers nationally; research foreclosed; self-sealing -- the schedule blocks the studies that would move it"),
    alt=(False, None, None), forced=(False, False), r1_scope="market_status",
    r6=(True, 46, "self_sealed_only"),
    sub=["cannabis", "thc"], end=["pain_mmj"], rows=["G036", "G018"],
    decided=["ACT-DEA"], recommended=["ACT-HHS"], overruled=[], sponsor=None, outcomes=[]),
 "D04": dict(type="NON_DECISION", frame="R8", year=2025, agency="DEA/DOJ",
    decision="Psilocybin held in Schedule I through 2025 despite FDA breakthrough designations (2018, 2019)",
    evidence_class="human_rct", uncertainty="high",
    action="decline", outcome="decline", cost_bearer_L="public", cost_bearer_S="sponsor",
    note="Schedule I since the CSA (1970) (G034); COMPASS (2018) and Usona (2019) breakthrough therapy designations (G037); Aggarwal petition denied, Ninth Circuit asked DEA to explain (G034)",
    Cp=(2, 2, 2, "harm if wrongly rescheduled: patients in supervised treatment; adverse psychiatric events partly reversible; a schedule can be revised"),
    Cr_axes=(2, 3, 3, "harm if wrongly kept in I: patients with treatment-resistant depression; suicide risk is irreversible; self-sealing research barrier"),
    alt=(False, None, None), forced=(False, False), r1_scope="market_status",
    r6=(True, 55, "none"),
    sub=["psilocybin"], end=["depression"], rows=["G037", "G020", "G034"],
    decided=["ACT-DEA"], recommended=[], overruled=[], sponsor="ACT-SP-COMPASS", outcomes=[]),
 "PCP22": dict(type="DECISION", frame="C2", year=2022, agency="EPA-OPP",
    decision="Pentachlorophenol: final registration review decision requiring cancellation of all uses (five-year phase-out)",
    action="decline", outcome="decline",
    note="87 FR 6535 (G002); EPA release 'EPA Requires Cancellation of Pentachlorophenol to Protect Human Health' (G001): risks to workers outweigh benefits given viable alternatives; source row coded go_ahead / registrant-led (NCR-R6)",
    rows=["G001", "G002"], decided=["ACT-EPA-OPP"], recommended=[], overruled=[], sponsor="ACT-SP-PENTA",
    forcing=("none", "restrictive", ["G001"]), sub=["pentachlorophenol"], end=[]),
 "A04P": dict(type="DECISION", frame="PRIOR", year=2011, agency="FDA-CDER",
    decision="Makena (17-OHPC) accelerated approval",
    action="go_ahead", outcome="decline",
    note="anchor for REV-A04; approval date not verified here (G031 UNSEEN); V017 states withdrawal about 12 years after accelerated approval",
    rows=["V017", "G031"], decided=["ACT-FDA-CDER"], recommended=[], overruled=[], sponsor="ACT-SP-COVIS", sub=["hydroxyprogesterone_caproate"], end=["preterm_birth"]),
 "A08P": dict(type="DECISION", frame="PRIOR", year=2008, agency="FDA-CDER",
    decision="Bevacizumab breast-cancer accelerated approval",
    action="go_ahead", outcome="decline",
    note="anchor for REV-A08; approval February 2008 (G038)",
    rows=["G038"], decided=["ACT-FDA-CDER"], recommended=[], overruled=[], sponsor="ACT-SP-GENENTECH", sub=["bevacizumab"], end=["overall_survival"]),
 "SCH1-1970": dict(type="DECISION", frame="PRIOR", year=1970, agency="Congress",
    decision="Marijuana placed in Schedule I by the Controlled Substances Act",
    action="decline", outcome="warn",
    note="anchor for REV-D01-1970; the 2026 order moves two categories to Schedule III (G019)",
    rows=["G019"], decided=["ACT-CONGRESS"], recommended=[], overruled=[], sponsor=None, sub=["cannabis"], end=[]),
}

# Reversals (WO-REG-1b): links between two decisions, or a decision and a
# court or legislative act. Never encoded inside one row.
#   (id, from_case, to (case id or act text), from_direction, to_direction,
#    initiator actor, initiator_type, mechanism, date_from, date_to,
#    date_rows, harm (text or None), harm_rows, note)
REVERSALS = [
    ("REV-D02", "D02", "Saccharin Study and Labeling Act (Pub. L. 95-203)", "decline", "warn",
     "ACT-CONGRESS", "legislature", "legislature", "1977-03-09", "1977-11-23", ["G011"], None, [],
     "moratorium plus warning label; industry lobbying recorded in the source note"),
    ("REV-A10", "A10", "FDA deferral by agreement with the sponsor (February 2012)", "decline", "go_ahead",
     "ACT-FDA-CDER", "agency_under_pressure", "agency_under_pressure", "2010-08", "2012-02", ["G010"], None, [],
     "Sept 2010 was a clarification that the drug could stay on the market while the proposal proceeded, not a reversal (G010 DIFFERS); patient and prescriber objections; Shire agreed to two further studies"),
    ("REV-C04", "C04", "Red River Valley Sugarbeet Growers v. Regan, 85 F.4th 881 (8th Cir. 2023)", "decline", "warn",
     "ACT-TG-RRVSGA", "trade_group", "court", "2021-08-30", "2023-11-02", ["G008", "G009"], None, [],
     "court on petition of grower and farm groups; tolerances legally in effect again (89 FR, Feb 5 2024)"),
    ("REV-C03", "C03", "NRDC v. EPA (9th Cir. June 17, 2022); EPA withdrawal of the interim decision (Sept 23, 2022)", "go_ahead", "vacated",
     "ACT-PIL-NRDC", "public_interest_litigant", "court", "2020-01-22", "2022-06-17", ["G033", "G006", "G007"], None, [],
     "a permissive action vacated within its lifetime; products remain on the market (G006), so the legal status of the substance did not move toward restriction"),
    ("REV-B00-B01", "B00", "B01", "go_ahead", "hold",
     "ACT-IC-MESH", "injured_class", "mass_harm_litigation", "2002", "2016-01", ["G035", "G014"],
     "2,874 medical device reports for urogynecologic mesh 2008-2010, 1,503 for POP repair (MDRs, not confirmed injuries)", ["G015"],
     "the dataset's B00 year 1996 is the first SUI sling clearance; the first POP mesh clearance was 2002 (G035)"),
    ("REV-B00b-B02", "B00b", "B02", "go_ahead", "hold",
     "ACT-IC-MOM", "injured_class", "mass_harm_litigation", "2000", "2016-02-18", ["G032", "G039"], None, ["G017"],
     "harm count at reversal not documented here; ASR recall covered about 93,000 implants worldwide (an implant count, not a harm count)"),
    ("REV-A04", "A04P", "A04", "go_ahead", "decline",
     "ACT-FDA-CDER", "agency_new_evidence", "new_evidence", "2011-02", "2023-04-05", ["V017", "G031"], None, [],
     "accelerated approval withdrawn after the confirmatory trial failed; approval month not verified here"),
    ("REV-A08", "A08P", "A08", "go_ahead", "decline",
     "ACT-FDA-CDER", "agency_new_evidence", "new_evidence", "2008-02", "2011-11-18", ["G038", "V025", "V026"], None, [],
     "accelerated approval withdrawn after confirmatory trials; ODAC voted 6-0 to withdraw (G038)"),
    ("REV-D01-2016", "D03", "D01", "decline", "warn",
     "ACT-PRESIDENT", "executive", "executive_order", "2016-07-19", "2026-04-23", ["G036", "G019"], None, [],
     "partial: two categories to Schedule III; contested in the D.C. Circuit (SAM v. DOJ)"),
    ("REV-D01-1970", "SCH1-1970", "D01", "decline", "warn",
     "ACT-PRESIDENT", "executive", "executive_order", "1970-10-27", "2026-04-23", ["G019"], None, [],
     "same reversal measured from the original placement; carried beside REV-D01-2016, never both counted"),
]
# The two D01 rows are one reversal measured from two anchors; reversals.py
# counts one of them per reading and says which.
REVERSAL_ALIASES = {"REV-D01-1970": "REV-D01-2016"}

# Frames the work order or a review names that this registry identified and
# did not load (each is a gap node, never a blank).
FRAMES_NOT_LOADED = [
    ("FR-CRL-2025", "FDA complete response letters published July 10 2025 (200+ letters, 2020-2024)",
     "exists (G021 VERIFIED); restrictive-side decisions, mostly for products later approved; openFDA database not reachable from here (egress)", ["G021"]),
    ("FR-CLINHOLD", "FDA clinical holds in a stated window",
     "no public FDA listing located; disclosure is by sponsors (G022 not searched)", ["G022"]),
    ("FR-C2-DOCS", "the 34 Frame C2 decision documents coded at document level (mitigation, use cancellations)",
     "notice-level coding only in the source; document-level coding not run (NCR-R6)", []),
    ("FR-USDA", "USDA decisions", "unenumerated in the source and here", []),
]
