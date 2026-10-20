# SPDX-License-Identifier: CC0-1.0
"""
curation.py -- the records this registry's coder authored, as data.

Everything here is PROPOSED unless a field says otherwise: it is one
coder's reading (ACT-REGISTRY, this session), tied to ledger rows in
verification/ that anyone can re-run. tools/build.py joins it with the
verbatim source (source/kimmy_v1/*.csv, pinned) and the verification
ledger, applies CHANGES in order, and writes registry/*.json. Nothing in
registry/ is edited by hand; validate.py rebuilds and compares.

Conventions
    rows      verification ledger ids (V###, E###, F###, G###) whose
              claims the record rests on
    Cr        (Pr, Ir, Dr, rationale): consequence of a wrongful
              RESTRICTION, RUS-0.2 section 6b; each axis 1-3
    r1        RUS-0.2 R1a/R1b/none with its basis
    forcing   (kind, direction the forcing pushes, rows)
"""

CODER = "ACT-REGISTRY"
DATE = "2026-10-19"

# ---------------------------------------------------------------- sources

HOST_KIND = [
    ("federalregister.gov", "primary_record"),
    ("accessdata.fda.gov", "primary_record"),
    ("supremecourt.gov", "court"), ("law.cornell.edu", "court"),
    ("pmc.ncbi.nlm.nih.gov", "peer_reviewed"), ("pubmed.ncbi", "peer_reviewed"),
    ("jamanetwork.com", "peer_reviewed"), ("nejm.org", "peer_reviewed"),
    ("journals.plos.org", "peer_reviewed"), ("sciencedirect.com", "peer_reviewed"),
    ("nature.com", "peer_reviewed"),
    ("fda.gov", "agency_page"), ("epa.gov", "agency_page"),
    ("justice.gov", "agency_page"), ("iarc.who.int", "agency_page"),
    ("ec.europa.eu", "agency_page"), ("nrc.gov", "standard"),
    ("iec.ch", "standard"), ("gradeworkinggroup.org", "standard"),
    ("ipcc.ch", "standard"),
    ("hklaw.com", "law_firm"), ("ogletree.com", "law_firm"),
    ("crowell.com", "law_firm"), ("lowenstein.com", "law_firm"),
    ("gibsondunn.com", "law_firm"), ("goldbergsegalla.com", "law_firm"),
    ("verdantlaw.com", "law_firm"),
    ("nbcnews.com", "news"), ("statnews.com", "news"), ("npr.org", "news"),
    ("medpagetoday.com", "news"), ("onclive.com", "news"),
    ("fdli.org", "secondary"), ("usrtk.org", "secondary"),
    ("drugwatch.com", "secondary"), ("newslow.com", "blog"),
    ("ro.co", "secondary"), ("acibademinternational.com", "blog"),
    ("crystalquest.com", "blog"), ("microplasticsapp.com", "blog"),
]

BUNDLE_SOURCES = [
    ("SRC-K-REPORT", "kimmy_v1/direction_of_uncertainty_report.md",
     "source/kimmy_v1/direction_of_uncertainty_report.md"),
    ("SRC-K-CSV", "kimmy_v1/coded_decisions.csv",
     "source/kimmy_v1/coded_decisions.csv"),
    ("SRC-K-ANNEX", "kimmy_v1/annex_a_regrading.csv",
     "source/kimmy_v1/annex_a_regrading.csv"),
    ("SRC-K-STD", "kimmy_v1/regulatory_uncertainty_standard_draft.md (RUS-0.1)",
     "source/kimmy_v1/regulatory_uncertainty_standard_draft.md"),
    ("SRC-REVIEW", "REVIEW_v1.md", "source/REVIEW_v1.md"),
    ("SRC-WO", "WORK_ORDER.md + WORK_ORDER_1a.md", "WORK_ORDER.md"),
]

# ---------------------------------------------------------------- actors

ACTORS = [
    # coders of this registry and of its sources
    ("ACT-KIMI", "coder", "Kimi deep research (kimmy_v1)", "originator of the coded sample, Annex A and RUS-0.1", "2026-10-18", []),
    ("ACT-REVIEWER", "coder", "REVIEW_v1 reviewer (chat session)", "originator of findings R1-R5", "2026-10-18", []),
    ("ACT-REGISTRY", "coder", "registry coder (this session)", "adjudicator of NCRs; coder of RUS-0.2 consequence-of-restriction axes and every PROPOSED field in tools/curation.py", "2026-10-18/2026-10-19", []),
    ("ACT-CODER2", "coder", "second coder (fresh session, no repository, no conversation)", "codes a 10-row subset blind to every prior value; independence set by its contamination probe", "2026-10-19", []),
    # agencies and offices
    ("ACT-FDA", "agency", "U.S. Food and Drug Administration", "regulator", "1906-", []),
    ("ACT-FDA-CDER", "office", "FDA Center for Drug Evaluation and Research", "drug review office", "-", []),
    ("ACT-FDA-CDRH", "office", "FDA Center for Devices and Radiological Health", "device review office", "-", []),
    ("ACT-FDA-FOOD", "office", "FDA food program (CFSAN; Human Foods Program from 2024)", "food and color additive office", "-", []),
    ("ACT-FDA-REVIEWTEAM-A02", "office", "CDER review team for eteplirsen", "review team whose recommendation was set aside", "2016", ["F004"]),
    ("ACT-EPA", "agency", "U.S. Environmental Protection Agency", "regulator", "1970-", []),
    ("ACT-EPA-OPP", "office", "EPA Office of Pesticide Programs", "pesticide registration office", "-", ["F025"]),
    ("ACT-EPA-OW", "office", "EPA Office of Water", "drinking water office", "-", []),
    ("ACT-EPA-ORCR", "office", "EPA Office of Resource Conservation and Recovery", "hazardous waste listing office", "-", ["V063"]),
    ("ACT-DEA", "agency", "Drug Enforcement Administration", "scheduling", "-", ["F030"]),
    ("ACT-DOJ", "agency", "U.S. Department of Justice", "scheduling order", "-", ["V013"]),
    ("ACT-OSHA", "agency", "Occupational Safety and Health Administration", "workplace standards; no shift-work standard", "1970-", ["V085"]),
    ("ACT-CONGRESS", "legislature", "U.S. Congress", "enacted the 1977 saccharin moratorium", "1977", ["V063", "E024"]),
    ("ACT-PRESIDENT", "office", "President of the United States", "executive order on marijuana rescheduling", "2025-2026", ["F030", "V077"]),
    ("ACT-SCOTUS", "court", "Supreme Court of the United States", "Monsanto v. Durnell", "2026", ["V009", "V010"]),
    ("ACT-CA9", "court", "U.S. Court of Appeals for the Ninth Circuit", "LULAC v. Regan (2021); NRDC v. EPA (2022)", "2021-2022", ["E029", "E031"]),
    ("ACT-CA8", "court", "U.S. Court of Appeals for the Eighth Circuit", "Red River Valley Sugarbeet Growers v. Regan (2023)", "2023", ["E030"]),
    ("ACT-IARC", "international_body", "International Agency for Research on Cancer", "hazard classification", "-", ["V048", "V080", "V081", "V110"]),
    ("ACT-EFSA", "international_body", "European Food Safety Authority", "E171 opinion 2021", "-", ["V041"]),
    ("ACT-EC", "international_body", "European Commission", "EU approvals and bans", "-", ["V056", "V115", "E022"]),
    ("ACT-JECFA", "international_body", "Joint FAO/WHO Expert Committee on Food Additives", "aspartame ADI", "-", ["V110"]),
    ("ACT-EMA-PRAC", "international_body", "EMA Pharmacovigilance Risk Assessment Committee", "GLP-1 thyroid review 2023", "2023", ["V036"]),
    ("ACT-DK-AES", "agency", "Danish National Board of Industrial Injuries (Arbejdsskadestyrelsen)", "occupational disease compensation", "2008-", ["V083", "F035"]),
    ("ACT-DE-ASB", "advisory_committee", "German Medical Expert Advisory Board on Occupational Diseases", "occupational disease list advice", "-", ["V084", "E040"]),
    # persons (role at the time of the decision)
    ("ACT-P-WOODCOCK", "person", "Janet Woodcock", "CDER director (2016); acting FDA commissioner (2021)", "2007-2021", ["F001", "F004"]),
    ("ACT-P-CALIFF", "person", "Robert Califf", "FDA commissioner (2016; 2022-2025)", "2016;2022-2025", ["F004", "F007"]),
    ("ACT-P-CAVAZZONI", "person", "Patrizia Cavazzoni", "CDER director (2021)", "2019-2025", ["F001"]),
    ("ACT-P-DUNN", "person", "Billy Dunn", "director, CDER Office of Neuroscience (2021)", "2021", ["F002"]),
    ("ACT-P-BUMPUS", "person", "Namandje Bumpus", "FDA chief scientist (2023)", "2023", ["F007"]),
    ("ACT-P-HAMBURG", "person", "Margaret Hamburg", "FDA commissioner (2011)", "2009-2015", ["F013"]),
    ("ACT-P-KENNEDY", "person", "Donald Kennedy", "FDA commissioner (1977)", "1977-1979", ["F029"]),
    ("ACT-P-REGAN", "person", "Michael Regan", "EPA administrator (2021-2024)", "2021-2025", ["F024", "F026", "F027"]),
    ("ACT-P-ZELDIN", "person", "Lee Zeldin", "EPA administrator (2025-)", "2025-", ["F027", "F028"]),
    ("ACT-P-ROWLAND", "person", "Jess Rowland", "chair, EPA Cancer Assessment Review Committee (glyphosate)", "2015-2016", ["F023"]),
    # advisory committees
    ("ACT-AC-PCNS", "advisory_committee", "FDA Peripheral and Central Nervous System Drugs Advisory Committee", "advised on aducanumab (2020), eteplirsen (2016), donanemab (2024)", "-", ["F001", "F004", "F014"]),
    ("ACT-AC-AADPAC", "advisory_committee", "FDA Anesthetic and Analgesic Drug Products Advisory Committee", "advised on Zohydro ER (2012)", "2012", ["F006", "V075"]),
    ("ACT-AC-BRUDAC", "advisory_committee", "FDA Bone, Reproductive and Urologic Drugs Advisory Committee", "advised on Makena (2019) and flibanserin (2015, joint)", "-", ["V018", "F011"]),
    ("ACT-AC-MAKENA-HEARING", "advisory_committee", "advisory committee at the October 2022 Makena withdrawal hearing", "advised withdrawal", "2022", ["F007"]),
    ("ACT-AC-AAC-DSARM", "advisory_committee", "FDA Arthritis and Drug Safety and Risk Management Advisory Committees (joint)", "advised on COX-2 inhibitors (2005)", "2005", ["V019", "F008"]),
    ("ACT-AC-AMDAC", "advisory_committee", "FDA Antimicrobial Drugs Advisory Committee", "advised on molnupiravir (2021)", "2021", ["V021", "F010"]),
    ("ACT-AC-ODAC", "advisory_committee", "FDA Oncologic Drugs Advisory Committee", "advised on bevacizumab breast indication (2010, 2011)", "-", ["V025", "F013"]),
    ("ACT-AC-OBGYN", "advisory_committee", "FDA Obstetrics and Gynecology Devices Panel", "advised on transvaginal mesh (2011)", "2011", ["F016"]),
    ("ACT-AC-ORTHO", "advisory_committee", "FDA Orthopaedic and Rehabilitation Devices Panel", "advised on metal-on-metal hips (2012)", "2012", ["F017"]),
    # sponsors, registrants and petitioners
    ("ACT-SP-BIOGEN", "sponsor", "Biogen", "sponsor, aducanumab", "-", ["F001"]),
    ("ACT-SP-SAREPTA", "sponsor", "Sarepta Therapeutics", "sponsor, eteplirsen", "-", ["F004", "V073"]),
    ("ACT-SP-ZOGENIX", "sponsor", "Zogenix", "sponsor, Zohydro ER", "-", ["F006"]),
    ("ACT-SP-COVIS", "sponsor", "Covis Pharma", "sponsor, Makena", "-", ["F007"]),
    ("ACT-SP-MERCK", "sponsor", "Merck", "sponsor, rofecoxib; molnupiravir (with Ridgeback)", "-", ["V020", "F010"]),
    ("ACT-SP-SPROUT", "sponsor", "Sprout Pharmaceuticals", "sponsor, flibanserin", "-", ["F011", "F012"]),
    ("ACT-SP-GENENTECH", "sponsor", "Genentech", "sponsor, bevacizumab", "-", ["F013"]),
    ("ACT-SP-LILLY", "sponsor", "Eli Lilly", "sponsor, donanemab", "-", ["F014"]),
    ("ACT-SP-SHIRE", "sponsor", "Shire", "sponsor, ProAmatine (midodrine)", "-", ["F015"]),
    ("ACT-SP-MESH", "sponsor", "transvaginal mesh manufacturers (incl. Boston Scientific, Coloplast)", "device sponsors", "-", ["F016"]),
    ("ACT-SP-MOM", "sponsor", "metal-on-metal hip manufacturers (incl. DePuy)", "device sponsors", "-", ["F017"]),
    ("ACT-SP-NOVO", "sponsor", "Novo Nordisk", "sponsor, liraglutide and semaglutide", "-", ["F018"]),
    ("ACT-SP-SYNGENTA", "sponsor", "Syngenta", "registrant, atrazine; neonicotinoids", "-", ["F021", "F025"]),
    ("ACT-SP-BAYER", "sponsor", "Bayer (Monsanto)", "registrant, glyphosate; neonicotinoids", "-", ["F031", "F025"]),
    ("ACT-SP-CORTEVA", "sponsor", "Corteva (Dow)", "registrant, chlorpyrifos", "-", ["F024"]),
    ("ACT-CSPI", "sponsor", "Center for Science in the Public Interest", "petitioner, Red No. 3", "2022-2025", ["F019", "F009"]),
    ("ACT-CRE", "sponsor", "Center for Regulatory Effectiveness", "information-quality petitioner, atrazine", "2002", ["F021"]),
    ("ACT-ETS", "sponsor", "Even the Score (advocacy campaign)", "advocacy for flibanserin approval", "2014-2015", ["F012"]),
]

# ---------------------------------------------------------------- authority

AUTHORITIES = [
    # id, level, citation, title, ledger row or None
    ("AUTH-FDCA-505", "statute", "FD&C Act sec. 505(d), 21 U.S.C. 355(d)", "drug approval: substantial evidence", "E006"),
    ("AUTH-FDCA-506C", "statute", "FD&C Act sec. 506(c), 21 U.S.C. 356(c)", "accelerated approval", "E001"),
    ("AUTH-FDCA-505-1", "statute", "FD&C Act sec. 505-1", "REMS", "E007"),
    ("AUTH-FDCA-505O4", "statute", "FD&C Act sec. 505(o)(4)", "safety labeling changes", "E014"),
    ("AUTH-FDCA-564", "statute", "FD&C Act sec. 564, 21 U.S.C. 360bbb-3", "emergency use authorization", "E008"),
    ("AUTH-FDCA-510K", "statute", "FD&C Act sec. 510(k)", "premarket notification", "E015"),
    ("AUTH-FDCA-513", "statute", "FD&C Act sec. 513; FDASIA 2012 sec. 608", "device classification by order", "E016"),
    ("AUTH-FDCA-409", "statute", "FD&C Act sec. 409, 21 U.S.C. 348; Delaney clause 409(c)(3)(A)", "food additives", "E020"),
    ("AUTH-FDCA-721", "statute", "FD&C Act sec. 721, 21 U.S.C. 379e; Delaney clause 721(b)(5)(B)", "color additives", "E019"),
    ("AUTH-PHSA-351", "statute", "Public Health Service Act sec. 351", "biologics licensing", None),
    ("AUTH-FDORA-3210", "statute", "FDORA (Consolidated Appropriations Act 2023) sec. 3210", "expedited withdrawal of accelerated approvals", "E005"),
    ("AUTH-SSLA-1977", "statute", "Saccharin Study and Labeling Act, Pub. L. 95-203", "saccharin moratorium and warning label", "E024"),
    ("AUTH-FIFRA-3G", "statute", "FIFRA sec. 3(g)", "registration review", "E025"),
    ("AUTH-FIFRA-4", "statute", "FIFRA sec. 4", "reregistration", "E026"),
    ("AUTH-FIFRA-24B", "statute", "FIFRA sec. 24(b)", "uniformity of labeling", "E032"),
    ("AUTH-FFDCA-408", "statute", "FFDCA sec. 408, 21 U.S.C. 346a (FQPA 1996)", "pesticide tolerances: reasonable certainty of no harm", "E027"),
    ("AUTH-SDWA-1412", "statute", "SDWA sec. 1412", "national primary drinking water regulations; CCL 1412(b)(1)", "E033"),
    ("AUTH-SDWA-1445", "statute", "SDWA sec. 1445(a)(2)", "unregulated contaminant monitoring", "E035"),
    ("AUTH-RCRA", "statute", "RCRA sec. 3001, 42 U.S.C. 6921", "hazardous waste listing", None),
    ("AUTH-CSA-201", "statute", "Controlled Substances Act sec. 201, 21 U.S.C. 811", "scheduling", "E037"),
    ("AUTH-OSHA-6B", "statute", "OSH Act sec. 6(b), 29 U.S.C. 655", "standard setting", "E038"),
    ("AUTH-OSHA-5A1", "statute", "OSH Act sec. 5(a)(1)", "general duty clause", "E038"),
    ("AUTH-PDUFA", "statute", "Prescription Drug User Fee Act (1992-)", "drug review user fees", "E041"),
    ("AUTH-MDUFA", "statute", "Medical Device User Fee Amendments (2002-)", "device review user fees", "E041"),
    ("AUTH-PRIA", "statute", "Pesticide Registration Improvement Act (2004-)", "pesticide registration fees", "E042"),
    ("AUTH-APPROP", "statute", "annual appropriations", "regulator funding by appropriation", None),
    ("AUTH-DK-WCA", "statute", "Danish Act on Workers' Compensation; Occupational Diseases Committee", "occupational disease recognition", "E039"),
    ("AUTH-DE-SGB7-9", "statute", "SGB VII sec. 9; Berufskrankheiten-Verordnung", "occupational disease list", "E040"),
    ("AUTH-21CFR314H", "regulation", "21 CFR 314 Subpart H (314.500-314.560)", "accelerated approval, drugs; 314.530 withdrawal", "E002"),
    ("AUTH-21CFR601E", "regulation", "21 CFR 601 Subpart E (601.40-601.46)", "accelerated approval, biologics; 601.43 withdrawal", "E003"),
    ("AUTH-21CFR314.126", "regulation", "21 CFR 314.126", "adequate and well-controlled studies", "E006"),
    ("AUTH-21CFR14", "regulation", "21 CFR Part 14", "public advisory committees", "E010"),
    ("AUTH-21CFR314.600", "regulation", "21 CFR 314.600-314.650; 601.90-601.95 (67 FR 37988)", "Animal Rule", "E012"),
    ("AUTH-21CFR201.57", "regulation", "21 CFR 201.57(c)(1)", "boxed warning", "E014"),
    ("AUTH-21CFR807E", "regulation", "21 CFR 807 Subpart E", "510(k) procedures", "E015"),
    ("AUTH-21CFR884.5980", "regulation", "21 CFR 884.5980 (final order, January 2016)", "transvaginal POP mesh class III", "E017"),
    ("AUTH-21CFR888.3330", "regulation", "21 CFR 888.3330 (final order, February 2016)", "metal-on-metal hip PMA call", "E018"),
    ("AUTH-21CFR74.303", "regulation", "21 CFR 74.303", "FD&C Red No. 3 listing", "E019"),
    ("AUTH-21CFR180.30", "regulation", "21 CFR 180.30", "BVO interim food additive", "E021"),
    ("AUTH-21CFR73.575", "regulation", "21 CFR 73.575", "titanium dioxide color additive", "E022"),
    ("AUTH-21CFR172.804", "regulation", "21 CFR 172.804", "aspartame", "E023"),
    ("AUTH-21CFR180.37", "regulation", "21 CFR 180.37", "saccharin interim food additive", "E024"),
    ("AUTH-40CFR155C", "regulation", "40 CFR 155 Subpart C", "registration review procedures", "E025"),
    ("AUTH-86FR48315", "regulation", "86 FR 48315 (August 30, 2021)", "chlorpyrifos tolerance revocation", "E028"),
    ("AUTH-89FR86418", "regulation", "89 FR 86418 (October 2024)", "Lead and Copper Rule Improvements", "E033"),
    ("AUTH-89FR32532", "regulation", "89 FR 32532 (April 2024)", "PFAS NPDWR", "E034"),
    ("AUTH-40CFR141.40", "regulation", "40 CFR 141.40", "UCMR", "E035"),
    ("AUTH-75FR78918", "regulation", "75 FR 78918 (December 17, 2010)", "saccharin delisting, RCRA and CERCLA", "E036"),
    ("AUTH-21CFR1308", "regulation", "21 CFR 1308", "schedules of controlled substances", "E037"),
    ("AUTH-GD-EXPEDITED", "guidance", "FDA, Expedited Programs for Serious Conditions (May 2014)", "expedited programs guidance", "E004"),
    ("AUTH-GD-ANIMALRULE", "guidance", "FDA, Product Development Under the Animal Rule (October 2015)", "Animal Rule guidance", "E013"),
    ("AUTH-HHS-EUA-2020", "order", "HHS sec. 564 declaration, March 27, 2020", "COVID-19 EUA declaration", "E008"),
    ("AUTH-EO-MARIJUANA", "order", "executive order directing marijuana rescheduling", "executive direction", "F030"),
    ("AUTH-CA9-LULAC-2021", "court_decision", "LULAC v. Regan (9th Cir. Apr. 29, 2021)", "order to act on chlorpyrifos", "E029"),
    ("AUTH-CA8-RRV-2023", "court_decision", "Red River Valley Sugarbeet Growers v. Regan (8th Cir. Nov. 2, 2023)", "vacatur of chlorpyrifos revocation", "E030"),
    ("AUTH-CA9-NRDC-2022", "court_decision", "NRDC v. EPA (9th Cir. June 17, 2022)", "vacatur of glyphosate human-health finding", "E031"),
    ("AUTH-SCOTUS-DURNELL", "court_decision", "Monsanto Co. v. Durnell, No. 24-1068 (June 25, 2026)", "FIFRA preemption of state failure-to-warn claims", "V009"),
    ("AUTH-EU-2022-63", "international_instrument", "Commission Regulation (EU) 2022/63", "E171 removed", "E022"),
    ("AUTH-EU-2004-248", "international_instrument", "Commission Decision 2004/248/EC", "atrazine non-inclusion", "V115"),
    ("AUTH-EU-DWD-2020-2184", "international_instrument", "Directive (EU) 2020/2184", "drinking water, PFAS parameters, watch list", "V112"),
]

# chains, statute first; the decision itself is the last node
CHAINS = {
    "A01": ["AUTH-FDCA-506C", "AUTH-PHSA-351", "AUTH-21CFR601E", "AUTH-21CFR14", "AUTH-GD-EXPEDITED"],
    "A02": ["AUTH-FDCA-506C", "AUTH-21CFR314H", "AUTH-21CFR14", "AUTH-GD-EXPEDITED"],
    "A03": ["AUTH-FDCA-505", "AUTH-21CFR314.126", "AUTH-21CFR14"],
    "A04": ["AUTH-FDCA-506C", "AUTH-21CFR314H", "AUTH-21CFR14"],
    "A05": ["AUTH-FDCA-505", "AUTH-21CFR14"],
    "A06": ["AUTH-FDCA-564", "AUTH-HHS-EUA-2020", "AUTH-21CFR14"],
    "A07": ["AUTH-FDCA-505", "AUTH-FDCA-505-1", "AUTH-21CFR14"],
    "A08": ["AUTH-FDCA-506C", "AUTH-PHSA-351", "AUTH-21CFR601E", "AUTH-21CFR14"],
    "A09": ["AUTH-PHSA-351", "AUTH-21CFR14"],
    "A10": ["AUTH-FDCA-506C", "AUTH-21CFR314H"],
    "B00": ["AUTH-FDCA-510K", "AUTH-21CFR807E"],
    "B00b": ["AUTH-FDCA-510K", "AUTH-21CFR807E"],
    "B01": ["AUTH-FDCA-513", "AUTH-21CFR884.5980"],
    "B02": ["AUTH-FDCA-513", "AUTH-21CFR888.3330"],
    "B03": ["AUTH-FDCA-505", "AUTH-21CFR314.600", "AUTH-GD-ANIMALRULE"],
    "B04": ["AUTH-FDCA-505O4", "AUTH-21CFR201.57"],
    "B05": ["AUTH-FDCA-721", "AUTH-21CFR74.303"],
    "B06": ["AUTH-FDCA-409", "AUTH-21CFR180.30"],
    "B07": ["AUTH-FDCA-721", "AUTH-21CFR73.575"],
    "B08": ["AUTH-FDCA-409", "AUTH-21CFR172.804"],
    "C01": ["AUTH-FIFRA-4"],
    "C02": ["AUTH-FIFRA-3G", "AUTH-40CFR155C"],
    "C03": ["AUTH-FIFRA-3G", "AUTH-40CFR155C"],
    "C04": ["AUTH-FFDCA-408", "AUTH-86FR48315", "AUTH-CA9-LULAC-2021"],
    "C05": ["AUTH-FIFRA-3G", "AUTH-40CFR155C"],
    "C06": ["AUTH-SDWA-1412", "AUTH-89FR86418"],
    "C07": ["AUTH-SDWA-1412", "AUTH-89FR32532"],
    "C08": ["AUTH-SDWA-1445", "AUTH-40CFR141.40"],
    "C09": ["AUTH-RCRA", "AUTH-75FR78918"],
    "C10": ["AUTH-FIFRA-3G", "AUTH-FIFRA-24B", "AUTH-SCOTUS-DURNELL"],
    "C11": ["AUTH-OSHA-6B", "AUTH-OSHA-5A1"],
    "D01": ["AUTH-CSA-201", "AUTH-21CFR1308", "AUTH-EO-MARIJUANA"],
    "D02": ["AUTH-FDCA-409", "AUTH-21CFR180.37", "AUTH-SSLA-1977"],
}

FUNDING = [  # (actor, authority, rows)
    ("ACT-FDA-CDER", "AUTH-PDUFA", ["E041", "F033"]),
    ("ACT-FDA-CDRH", "AUTH-MDUFA", ["E041"]),
    ("ACT-FDA-FOOD", "AUTH-APPROP", ["E041"]),
    ("ACT-EPA-OPP", "AUTH-PRIA", ["E042"]),
    ("ACT-EPA-OW", "AUTH-APPROP", []),
    ("ACT-OSHA", "AUTH-APPROP", []),
]

DELEGATION = [  # (child, parent)
    ("ACT-FDA-CDER", "ACT-FDA"), ("ACT-FDA-CDRH", "ACT-FDA"), ("ACT-FDA-FOOD", "ACT-FDA"),
    ("ACT-FDA-REVIEWTEAM-A02", "ACT-FDA-CDER"),
    ("ACT-EPA-OPP", "ACT-EPA"), ("ACT-EPA-OW", "ACT-EPA"), ("ACT-EPA-ORCR", "ACT-EPA"),
    ("ACT-DEA", "ACT-DOJ"),
]

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
 "C11": dict(type="NON_DECISION", sub=["night_shift_work"], end=["breast_cancer", "prostate_cancer", "colorectal_cancer", "circadian_disruption"],
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

# C11, the added case, as the source CSV would carry it (NCR-R5)
C11_ROW = dict(id="C11", year=2026, agency="OSHA", decision="Night shift work: no OSHA standard (US); IARC Group 2A",
    evidence_class="human_epi+animal", uncertainty="high", direction="go_ahead", cost_bearer="employer",
    mirror="yes", verified="S", note="added by NCR-R5; exposure coded by rotation pattern, not ever/never; sources V080-V087")
C11_RUS = dict(P=3, I=3, D=1, rationale_P="millions of night workers", rationale_I="cancer latent, irreversible", rationale_D="a standard can be revised")

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
    ("M11", "IARC: night shift work Group 2A", 2019, "IARC", "C11", "night shift - cancer (not in the source's mirror table)", None, None, ["V080", "V081"]),
    ("M12", "Denmark: compensation for breast cancer after night work", 2008, "DK", "C11", "night shift - compensation", None, None, ["V083", "F035"]),
    ("M13", "Germany: not recognized as occupational disease", 2010, "DE", "C11", "night shift - recognition", None, None, ["V084"]),
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
    ("EA-01", "glyphosate", "gut_microbiome", "NOT_ASSESSED", ["C03", "C10"], "EPA glyphosate human-health risk assessment and interim decision (2017-2020)", ["glyphosate", "microbiome", "EPA"], ["G034"], "work-order example; state comes from ledger row G034 if run"),
    ("EA-02", "microplastics", "microplastic_occurrence", "NOT_ASSESSED", ["C08"], "UCMR 6 proposal (July 2026)", ["UCMR 6", "microplastics"], ["V011", "V061"], "national occurrence data will not be generated"),
    ("EA-03", "polypropylene", "mesh_erosion", "NOT_REQUIRED", ["B00"], "510(k) clearance file", ["510(k)", "clinical data"], ["V029", "E015"], "substantial equivalence requires no clinical data"),
    ("EA-04", "cobalt", "metallosis", "NOT_REQUIRED", ["B00b"], "510(k) clearance files", ["510(k)", "clinical data"], ["V030", "E015"], "substantial equivalence requires no clinical data"),
    ("EA-05", "night_shift_work", "breast_cancer", "NOT_RESOLVED", ["C11"], "Travis et al. 2016 pooled cohorts; IARC Vol 124", ["night shift", "rotation", "forward", "backward", "permanent night"], ["V082", "V086", "V087"], "exposure coded ever/never or duration; rotation pattern not resolved for cancer endpoints"),
    ("EA-06", "aducanumab", "alzheimer_cognition", "NOT_RESOLVED", ["A01"], "approval record, June 2021", ["clinical benefit", "confirmatory"], ["V015", "V016"], "clinical benefit unconfirmed at approval; surrogate basis"),
    ("EA-07", "eteplirsen", "dystrophin", "NOT_RESOLVED", ["A02"], "approval record, September 2016", ["clinical benefit", "confirmatory"], ["F004"], "clinical benefit unconfirmed at approval; surrogate basis"),
    ("EA-08", "titanium_dioxide", "genotoxicity", "NOT_LOCATED", ["B07"], "FDA reassessment of E171 after EFSA 2021", ["FDA", "titanium dioxide", "genotoxicity"], ["V041"], "an FDA reassessment was not located; the absence is the source's statement"),
]
