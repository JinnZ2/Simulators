# SPDX-License-Identifier: CC0-1.0
"""
curation_core.py -- actors, authority records, authority chains, funding
and delegation, as data (WO-REG-1a A/B; WO-REG-1 consolidated 1a).

PROPOSED unless a field says otherwise: one coder's reading (ACT-REGISTRY),
tied to verification ledger rows (V/E/F/G ids in verification/) that anyone
can re-run. tools/build.py turns these into registry objects; nothing in
registry/ is edited by hand. Split out of the earlier single curation.py
when the consolidated bundle arrived (CHG-INPUT-01); the old module stays in
git history at 294e4af.

Tuples
    ACTORS        (id, type, name, role_at_time, date_range, rows)
    AUTHORITIES   (id, level, citation, title, ledger row or None)
    CHAINS        case id -> [authority ids], statute first
    FUNDING       (actor, authority, rows)
    DELEGATION    (child, parent)
"""

# ---------------------------------------------------------------- actors

ACTORS = [
    # coders of this registry and of its sources
    ("ACT-KIMI", "coder", "Kimi deep research (kimmy v1-v3)", "originator of the coded sample, Annex A, RUS-0.1 and RUS-0.2, the sensitivity addendum", "2026-10-18/2026-10-19", []),
    ("ACT-REVIEWER", "coder", "REVIEW_v1-v3 reviewer (chat session)", "originator of findings R1-R14", "2026-10-18/2026-10-19", []),
    ("ACT-REGISTRY", "coder", "registry coder (this session)", "adjudicator of NCRs; coder of the per-axis C_restrict scores (second coding beside the source sums), the R8 candidate rows, and every PROPOSED field in tools/curation_*.py", "2026-10-18/2026-10-21", []),
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
    ("ACT-CSPI", "public_interest_litigant", "Center for Science in the Public Interest", "petitioner, Red No. 3", "2022-2025", ["F019", "F009"]),
    ("ACT-CRE", "trade_group", "Center for Regulatory Effectiveness", "information-quality petitioner, atrazine", "2002", ["F021"]),
    ("ACT-ETS", "advocacy_group", "Even the Score (advocacy campaign)", "advocacy for flibanserin approval", "2014-2015", ["F012"]),
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
    "E01": ["AUTH-OSHA-6B", "AUTH-OSHA-5A1"],
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

# added with the consolidated bundle: reversal initiators (WO-REG-1b), R8
# candidate rows, the 2022 EPA frame
ACTORS += [
    ("ACT-TG-RRVSGA", "trade_group", "Red River Valley Sugarbeet Growers Association et al. (grower and farm groups)", "petitioners, Eighth Circuit chlorpyrifos case", "2021-2023", ["G009"]),
    ("ACT-PIL-NRDC", "public_interest_litigant", "Natural Resources Defense Council; Pesticide Action Network North America", "petitioners, NRDC v. EPA (9th Cir. 2022)", "2020-2022", ["G007"]),
    ("ACT-PIL-RURAL", "public_interest_litigant", "Rural Coalition; Lideres Campesinas; Farmworker Association of Florida; Beyond Pesticides; Center for Food Safety", "consolidated petitioners, NRDC v. EPA (9th Cir. 2022)", "2020-2022", ["G007"]),
    ("ACT-PIL-LULAC", "public_interest_litigant", "League of United Latin American Citizens et al.", "petitioners, LULAC v. Regan (9th Cir. 2021)", "2007-2021", ["G008", "E029"]),
    ("ACT-IC-MESH", "injured_class", "women injured by transvaginal mesh (MDR reporters and litigants)", "harm reporters and plaintiffs", "2008-2019", ["G015"]),
    ("ACT-IC-MOM", "injured_class", "patients injured by metal-on-metal hips (registry cases and litigants)", "harm reporters and plaintiffs", "2008-2016", ["G017"]),
    ("ACT-IC-MIDODRINE", "injured_class", "patients and prescribers objecting to the midodrine withdrawal proposal", "objectors", "2010", ["G010"]),
    ("ACT-HHS", "agency", "U.S. Department of Health and Human Services", "scientific and medical evaluation for scheduling (CSA 201(b))", "-", ["G019"]),
    ("ACT-CADC", "court", "U.S. Court of Appeals for the D.C. Circuit", "SAM v. DOJ (2026), challenges to the Schedule III order", "2026", ["G019"]),
    ("ACT-SP-PENTA", "sponsor", "pentachlorophenol registrants", "registrants", "-", ["G001", "G002"]),
    ("ACT-SP-REG2022", "sponsor", "registrants of the 2022 registration-review chemicals", "registrants (one actor for the frame)", "2022", ["G002", "G003", "G004", "G005"]),
    ("ACT-CA-LEG", "legislature", "California Legislature (AB 418, California Food Safety Act)", "state ban on BVO and three other additives effective 2027", "2023", ["G024"]),
    ("ACT-SP-COMPASS", "sponsor", "COMPASS Pathways", "psilocybin breakthrough designation holder", "2018-", ["G020"]),
    ("ACT-SP-USONA", "sponsor", "Usona Institute", "psilocybin breakthrough designation holder", "2019-", ["G020"]),
]

AUTHORITIES += [
    ("AUTH-21CFR314.530", "regulation", "21 CFR 314.530", "withdrawal of accelerated approval (drugs)", "G010"),
    ("AUTH-CSA-201B", "statute", "Controlled Substances Act sec. 201(b), 21 U.S.C. 811(b)", "HHS scientific and medical evaluation binding on scientific matters", None),
    ("AUTH-81FR53767", "order", "81 FR 53767 (August 12, 2016)", "denial of petition to reschedule marijuana", "G018"),
    ("AUTH-DOJ-2026-SCHIII", "order", "DOJ final order, April 23, 2026", "marijuana in FDA-approved products and under state medical license to Schedule III", "G019"),
    ("AUTH-87FR6535", "regulation", "87 FR 6535 (February 4, 2022)", "registration review interim decisions and final decision (pentachlorophenol)", "G002"),
    ("AUTH-87FR5815", "regulation", "87 FR 5815 (February 2, 2022)", "registration review interim decisions", "G003"),
    ("AUTH-87FR25266", "regulation", "87 FR 25266 (April 28, 2022)", "registration review interim and final decisions", "G004"),
    ("AUTH-87FR48018", "regulation", "87 FR 48018 (August 5, 2022)", "registration review decisions and case closures", "G005"),
    ("AUTH-87FR64484", "regulation", "87 FR 64484 (October 25, 2022)", "registration review decisions and case closures", "G005"),
    ("AUTH-CA-AB418", "statute", "California Health and Safety Code (AB 418, 2023)", "state ban on BVO, potassium bromate, propylparaben, Red No. 3 from 2027", "G024"),
    ("AUTH-STOCKHOLM-PCP", "international_instrument", "Stockholm Convention, pentachlorophenol listing (2015)", "POP listing; not binding on the US", None),
    ("AUTH-SUBPART-H-AGREEMENT", "order", "FDA-Shire agreement and deferral of midodrine withdrawal (February 2012)", "deferral pending two further studies", "G010"),
]

CHAINS.update({
    "A10": ["AUTH-FDCA-506C", "AUTH-21CFR314H", "AUTH-21CFR314.530"],
    "D03": ["AUTH-CSA-201", "AUTH-CSA-201B", "AUTH-21CFR1308", "AUTH-81FR53767"],
    "D04": ["AUTH-CSA-201", "AUTH-21CFR1308"],
    "D01": ["AUTH-CSA-201", "AUTH-CSA-201B", "AUTH-21CFR1308", "AUTH-EO-MARIJUANA", "AUTH-DOJ-2026-SCHIII"],
    "PCP22": ["AUTH-FIFRA-3G", "AUTH-40CFR155C", "AUTH-87FR6535"],
})
